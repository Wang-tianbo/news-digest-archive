#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import sqlite3
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any


SHANGHAI_TZ = timezone(timedelta(hours=8))
DEFAULT_DB_PATH = Path(".codex-run") / "signal-inbox" / "signal-inbox.sqlite3"
DEFAULT_CANDIDATE_DIR = Path(".codex-run") / "signal-candidates"
DEFAULT_REVIEW_DIR = Path(".codex-run") / "signal-reviews"
DEFAULT_MANUAL_DIR = Path(".codex-run") / "signal-inbox" / "manual"
DEFAULT_CONFIG_PATH = Path("config") / "signal-sources.yml"

ALLOWED_SOURCE_TIERS = {"public"}
VALID_STATUSES = {"待审", "已采用", "观察中", "补证据", "重复", "降权", "过期", "暂停源"}
VALID_RETROSPECTIVE_STATUSES = {
    "待验证",
    "被强化",
    "被削弱",
    "被推翻",
    "进入稳定现实",
    "仍未明朗",
}
SECRET_FIELD_RE = re.compile(
    r"(cookie|token|secret|password|passwd|authorization|auth_token|ct0|session)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Source:
    source_id: str
    name: str
    platform: str
    source_role: str
    source_tier: str
    source_type: str
    url: str
    section_hint: str
    item_type: str
    run_mode: str
    health_status: str


@dataclass(frozen=True)
class FeedItem:
    source_id: str
    title: str
    url: str
    published_at: str
    summary: str


@dataclass(frozen=True)
class SignalCandidate:
    candidate_id: str
    source_id: str
    title: str
    url: str
    published_at: str
    collected_at: str
    item_type: str
    section_hint: str
    summary: str
    claim: str
    evidence_urls: list[str]
    score: int
    status: str
    dedupe_key: str
    trend_key: str
    adoption_reason: str
    rejection_reason: str
    retrospective_status: str


@dataclass(frozen=True)
class SourceProfile:
    source_id: str
    seen_count: int
    adopted_count: int
    repeated_count: int
    last_seen_at: str | None
    last_adopted_at: str | None
    failure_rate: float
    duplicate_rate: float


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def now_shanghai() -> datetime:
    return datetime.now(SHANGHAI_TZ)


def parse_report_date(value: str | None) -> date:
    if value:
        return datetime.strptime(value, "%Y-%m-%d").date()
    return now_shanghai().date()


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone(SHANGHAI_TZ).isoformat(timespec="seconds")


def ensure_under_codex_run(path: Path, root: Path) -> Path:
    resolved = (root / path).resolve() if not path.is_absolute() else path.resolve()
    codex_run = (root / ".codex-run").resolve()
    if resolved != codex_run and codex_run not in resolved.parents:
        raise ValueError(f"Refusing to write outside .codex-run: {resolved}")
    return resolved


def ensure_codex_run_ignored(root: Path) -> None:
    gitignore = root / ".gitignore"
    if not gitignore.is_file():
        raise RuntimeError(".gitignore is missing; refusing to write local signal inbox state")
    content = gitignore.read_text(encoding="utf-8")
    if ".codex-run/" not in content and ".codex-run" not in content:
        raise RuntimeError(".codex-run is not ignored by git; refusing to write local signal inbox state")


def normalize_scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def load_sources(path: Path) -> list[Source]:
    if not path.is_file():
        raise FileNotFoundError(f"source config not found: {path}")

    sources: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_sources = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "sources:":
            in_sources = True
            continue
        if not in_sources:
            continue
        if raw_line.startswith("  - "):
            if current:
                sources.append(current)
            current = {}
            rest = raw_line[4:].strip()
            if rest:
                key, sep, value = rest.partition(":")
                if not sep:
                    raise ValueError(f"invalid source entry line: {raw_line}")
                current[key.strip()] = normalize_scalar(value)
            continue
        if current is not None and raw_line.startswith("    "):
            key, sep, value = stripped.partition(":")
            if not sep:
                raise ValueError(f"invalid source field line: {raw_line}")
            current[key.strip()] = normalize_scalar(value)
            continue
        raise ValueError(f"unsupported YAML subset line: {raw_line}")
    if current:
        sources.append(current)

    required = {
        "source_id",
        "name",
        "platform",
        "source_role",
        "source_tier",
        "source_type",
        "url",
        "section_hint",
        "item_type",
        "run_mode",
        "health_status",
    }
    parsed: list[Source] = []
    seen: set[str] = set()
    for source in sources:
        missing = sorted(required - source.keys())
        if missing:
            raise ValueError(f"source {source.get('source_id', '<unknown>')} missing fields: {missing}")
        source_id = source["source_id"]
        if source_id in seen:
            raise ValueError(f"duplicate source_id: {source_id}")
        seen.add(source_id)
        for key, value in source.items():
            if SECRET_FIELD_RE.search(key) or SECRET_FIELD_RE.search(value):
                raise ValueError(f"secret-like value is not allowed in source config: {source_id}.{key}")
        parsed.append(Source(**{key: source[key] for key in required}))
    return parsed


def is_blocked_host(hostname: str) -> bool:
    host = hostname.strip().lower().rstrip(".")
    if host in {"localhost", "0.0.0.0"} or host.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def validate_public_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"unsupported URL scheme: {url}")
    if parsed.username or parsed.password:
        raise ValueError(f"credentials in URL are not allowed: {url}")
    if not parsed.hostname:
        raise ValueError(f"URL has no hostname: {url}")
    if is_blocked_host(parsed.hostname):
        raise ValueError(f"blocked host in URL: {url}")
    if parsed.hostname == "169.254.169.254":
        raise ValueError("metadata endpoint is blocked")


def canonical_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url.strip())
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = re.sub(r"/+$", "", parsed.path or "/")
    query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    filtered = [
        (k, v)
        for k, v in query_pairs
        if not k.lower().startswith("utm_") and k.lower() not in {"ref", "source"}
    ]
    query = urllib.parse.urlencode(filtered)
    return urllib.parse.urlunparse((scheme, netloc, path, "", query, ""))


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def text_digest(value: str, length: int = 16) -> str:
    return stable_hash(value)[:length]


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def summarize_text(value: str, limit: int = 260) -> str:
    text = strip_tags(value)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def parse_datetime_to_iso(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    try:
        parsed = parsedate_to_datetime(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(SHANGHAI_TZ).isoformat(timespec="seconds")
    except (TypeError, ValueError, IndexError, OverflowError):
        pass
    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(SHANGHAI_TZ).isoformat(timespec="seconds")
    except ValueError:
        return text


def fetch_url(url: str, timeout: int = 20) -> bytes:
    validate_public_url(url)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "news-digest-signal-inbox/1.0 (+public-source-rss-github-arxiv)"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(2_000_000)


def first_text(element: ET.Element, names: list[str]) -> str:
    for name in names:
        found = element.find(name)
        if found is not None and found.text:
            return found.text.strip()
    for child in element.iter():
        tag = child.tag.split("}", 1)[-1].lower()
        if tag in {name.split("}", 1)[-1].lower() for name in names} and child.text:
            return child.text.strip()
    return ""


def first_link(element: ET.Element) -> str:
    for child in element.iter():
        tag = child.tag.split("}", 1)[-1].lower()
        if tag != "link":
            continue
        href = child.attrib.get("href")
        rel = child.attrib.get("rel", "alternate")
        if href and rel in {"alternate", ""}:
            return href.strip()
        if child.text and child.text.strip().startswith(("http://", "https://")):
            return child.text.strip()
    return ""


def parse_feed(content: bytes, source: Source) -> list[FeedItem]:
    root = ET.fromstring(content)
    items: list[FeedItem] = []

    rss_items = list(root.findall(".//item"))
    if rss_items:
        for item in rss_items:
            title = first_text(item, ["title"])
            link = first_text(item, ["link"]) or first_link(item)
            published = first_text(item, ["pubDate", "published", "updated", "date"])
            summary = first_text(item, ["description", "summary", "content"])
            if title and link:
                items.append(
                    FeedItem(source.source_id, title, link, parse_datetime_to_iso(published), summary)
                )
        return items

    for entry in root.iter():
        if entry.tag.split("}", 1)[-1].lower() != "entry":
            continue
        title = first_text(entry, ["title"])
        link = first_link(entry)
        published = first_text(entry, ["published", "updated"])
        summary = first_text(entry, ["summary", "content"])
        if title and link:
            items.append(FeedItem(source.source_id, title, link, parse_datetime_to_iso(published), summary))
    return items


def github_atom_url(source: Source) -> str:
    parsed = urllib.parse.urlparse(source.url)
    if parsed.hostname not in {"github.com", "www.github.com"}:
        raise ValueError(f"GitHub source URL must use github.com: {source.url}")
    path = parsed.path.strip("/")
    parts = path.split("/")
    if len(parts) < 2:
        raise ValueError(f"GitHub source URL must include owner/repo: {source.url}")
    owner, repo = parts[0], parts[1]
    if source.source_type == "github_releases":
        return f"https://github.com/{owner}/{repo}/releases.atom"
    if source.source_type == "github_activity":
        return f"https://github.com/{owner}/{repo}/commits.atom"
    raise ValueError(f"unsupported GitHub source_type: {source.source_type}")


def collect_source(source: Source, limit: int) -> tuple[list[FeedItem], str]:
    if source.source_tier not in ALLOWED_SOURCE_TIERS:
        return [], "blocked: source_tier is not public"
    if source.health_status != "active":
        return [], f"partial: source health_status is {source.health_status}"
    if source.run_mode != "auto":
        return [], f"partial: source run_mode is {source.run_mode}"
    if source.source_type in {"rss_atom", "arxiv_query"}:
        feed_url = source.url
    elif source.source_type in {"github_releases", "github_activity"}:
        feed_url = github_atom_url(source)
    else:
        return [], f"blocked: unsupported source_type {source.source_type}"
    content = fetch_url(feed_url)
    items = parse_feed(content, source)
    return items[:limit], "hit" if items else "miss"


def connect_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS sources (
            source_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            source_role TEXT NOT NULL,
            source_tier TEXT NOT NULL,
            source_type TEXT NOT NULL,
            url TEXT NOT NULL,
            section_hint TEXT NOT NULL,
            item_type TEXT NOT NULL,
            run_mode TEXT NOT NULL,
            health_status TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS raw_items (
            raw_id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            url TEXT NOT NULL,
            title TEXT NOT NULL,
            published_at TEXT,
            collected_at TEXT NOT NULL,
            raw_hash TEXT NOT NULL,
            fetch_status TEXT NOT NULL,
            summary TEXT,
            FOREIGN KEY(source_id) REFERENCES sources(source_id)
        );

        CREATE TABLE IF NOT EXISTS candidates (
            candidate_id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            published_at TEXT,
            collected_at TEXT NOT NULL,
            item_type TEXT NOT NULL,
            section_hint TEXT NOT NULL,
            summary TEXT NOT NULL,
            claim TEXT NOT NULL,
            evidence_urls TEXT NOT NULL,
            score INTEGER NOT NULL,
            status TEXT NOT NULL,
            dedupe_key TEXT NOT NULL,
            trend_key TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            adoption_reason TEXT NOT NULL DEFAULT '',
            rejection_reason TEXT NOT NULL DEFAULT '',
            retrospective_status TEXT NOT NULL DEFAULT '待验证',
            last_updated_at TEXT NOT NULL,
            FOREIGN KEY(source_id) REFERENCES sources(source_id)
        );

        CREATE UNIQUE INDEX IF NOT EXISTS idx_candidates_dedupe_key ON candidates(dedupe_key);
        CREATE INDEX IF NOT EXISTS idx_candidates_collected_at ON candidates(collected_at);
        CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);

        CREATE TABLE IF NOT EXISTS source_checks (
            run_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            checked_at TEXT NOT NULL,
            result TEXT NOT NULL,
            item_count INTEGER NOT NULL,
            note TEXT NOT NULL,
            PRIMARY KEY(run_id, source_id)
        );

        CREATE TABLE IF NOT EXISTS source_profiles (
            source_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            source_role TEXT NOT NULL,
            source_tier TEXT NOT NULL,
            seen_count INTEGER NOT NULL,
            adopted_count INTEGER NOT NULL,
            repeated_count INTEGER NOT NULL,
            last_seen_at TEXT,
            last_adopted_at TEXT,
            failure_rate REAL NOT NULL,
            duplicate_rate REAL NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )


def upsert_source(conn: sqlite3.Connection, source: Source, updated_at: str) -> None:
    conn.execute(
        """
        INSERT INTO sources (
            source_id, name, platform, source_role, source_tier, source_type, url,
            section_hint, item_type, run_mode, health_status, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_id) DO UPDATE SET
            name=excluded.name,
            platform=excluded.platform,
            source_role=excluded.source_role,
            source_tier=excluded.source_tier,
            source_type=excluded.source_type,
            url=excluded.url,
            section_hint=excluded.section_hint,
            item_type=excluded.item_type,
            run_mode=excluded.run_mode,
            health_status=excluded.health_status,
            updated_at=excluded.updated_at
        """,
        (
            source.source_id,
            source.name,
            source.platform,
            source.source_role,
            source.source_tier,
            source.source_type,
            source.url,
            source.section_hint,
            source.item_type,
            source.run_mode,
            source.health_status,
            updated_at,
        ),
    )


def make_trend_key(title: str) -> str:
    text = title.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", text)
    words = [word for word in text.split() if len(word) > 1]
    return " ".join(words[:12]) or text_digest(title)


def score_candidate(source: Source, item: FeedItem, published_at: str, report_day: date) -> int:
    score = 4
    if source.source_role in {"official", "research"}:
        score += 2
    elif source.source_role in {"opinion", "community"}:
        score += 1
    if source.section_hint == "AI 研究前沿":
        score += 1
    if published_at:
        try:
            dt = datetime.fromisoformat(published_at)
            window_start = datetime.combine(report_day - timedelta(days=1), datetime.min.time(), SHANGHAI_TZ)
            window_start = window_start.replace(hour=9)
            window_end = datetime.combine(report_day, datetime.min.time(), SHANGHAI_TZ).replace(hour=9)
            if window_start <= dt <= window_end:
                score += 2
            elif dt >= window_end - timedelta(days=7):
                score += 1
        except ValueError:
            pass
    text = f"{item.title} {item.summary}".lower()
    if any(keyword in text for keyword in ["agent", "coding", "eval", "benchmark", "reasoning", "rag"]):
        score += 1
    return max(1, min(score, 10))


def candidate_from_item(source: Source, item: FeedItem, report_day: date, collected_at: str) -> dict[str, Any]:
    url = canonical_url(item.url)
    validate_public_url(url)
    published_at = item.published_at or collected_at
    summary = summarize_text(item.summary or item.title)
    trend_key = make_trend_key(item.title)
    dedupe_key = stable_hash(url)
    content_hash = stable_hash(f"{item.title}\n{summary}")
    candidate_id = f"sig_{dedupe_key[:16]}"
    score = score_candidate(source, item, published_at, report_day)
    return {
        "candidate_id": candidate_id,
        "source_id": source.source_id,
        "title": strip_tags(item.title),
        "url": url,
        "published_at": published_at,
        "collected_at": collected_at,
        "item_type": source.item_type,
        "section_hint": source.section_hint,
        "summary": summary or strip_tags(item.title),
        "claim": strip_tags(item.title),
        "evidence_urls": [url],
        "score": score,
        "status": "待审",
        "dedupe_key": dedupe_key,
        "trend_key": trend_key,
        "content_hash": content_hash,
        "adoption_reason": "",
        "rejection_reason": "",
        "retrospective_status": "待验证",
        "last_updated_at": collected_at,
    }


def insert_candidate(conn: sqlite3.Connection, candidate: dict[str, Any]) -> bool:
    params = {
        **candidate,
        "evidence_urls": json.dumps(candidate["evidence_urls"], ensure_ascii=False),
    }
    cursor = conn.execute(
        """
        INSERT INTO candidates (
            candidate_id, source_id, title, url, published_at, collected_at,
            item_type, section_hint, summary, claim, evidence_urls, score, status,
            dedupe_key, trend_key, content_hash, adoption_reason, rejection_reason,
            retrospective_status, last_updated_at
        ) VALUES (
            :candidate_id, :source_id, :title, :url, :published_at, :collected_at,
            :item_type, :section_hint, :summary, :claim, :evidence_urls, :score, :status,
            :dedupe_key, :trend_key, :content_hash, :adoption_reason, :rejection_reason,
            :retrospective_status, :last_updated_at
        )
        ON CONFLICT(dedupe_key) DO UPDATE SET
            collected_at=excluded.collected_at,
            last_updated_at=excluded.last_updated_at,
            score=max(candidates.score, excluded.score)
        """,
        params,
    )
    return cursor.rowcount > 0


def insert_raw_item(conn: sqlite3.Connection, source: Source, item: FeedItem, collected_at: str) -> None:
    url = canonical_url(item.url)
    raw_hash = stable_hash(f"{source.source_id}\n{url}\n{item.title}\n{item.summary}")
    conn.execute(
        """
        INSERT OR IGNORE INTO raw_items (
            raw_id, source_id, url, title, published_at, collected_at, raw_hash, fetch_status, summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            f"raw_{raw_hash[:16]}",
            source.source_id,
            url,
            strip_tags(item.title),
            item.published_at,
            collected_at,
            raw_hash,
            "hit",
            summarize_text(item.summary),
        ),
    )


def record_source_check(
    conn: sqlite3.Connection,
    run_id: str,
    source_id: str,
    checked_at: str,
    result: str,
    item_count: int,
    note: str,
) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO source_checks (
            run_id, source_id, checked_at, result, item_count, note
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (run_id, source_id, checked_at, result, item_count, note[:500]),
    )


def candidate_rows_for_review(conn: sqlite3.Connection, report_day: date, limit: int) -> list[sqlite3.Row]:
    cutoff = datetime.combine(report_day - timedelta(days=7), datetime.min.time(), SHANGHAI_TZ).isoformat()
    rows = conn.execute(
        """
        SELECT c.*, s.name AS source_name, s.platform, s.source_role, s.source_tier
        FROM candidates c
        JOIN sources s ON c.source_id = s.source_id
        WHERE (
            c.published_at >= ?
            OR ((c.published_at IS NULL OR c.published_at = '') AND c.collected_at >= ?)
            OR c.status = '观察中'
        )
          AND c.status NOT IN ('已采用', '过期', '暂停源')
        ORDER BY c.score DESC, c.published_at DESC, c.collected_at DESC
        LIMIT ?
        """,
        (cutoff, cutoff, limit),
    ).fetchall()
    return rows


def candidate_to_json(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    try:
        data["evidence_urls"] = json.loads(data.get("evidence_urls") or "[]")
    except json.JSONDecodeError:
        data["evidence_urls"] = []
    return data


def export_candidates_jsonl(conn: sqlite3.Connection, report_day: date, path: Path, limit: int = 200) -> int:
    rows = candidate_rows_for_review(conn, report_day, limit)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(candidate_to_json(row), ensure_ascii=False, sort_keys=True) + "\n")
    return len(rows)


def review_bucket(row: sqlite3.Row) -> str:
    if row["status"] in {"重复", "降权"} or row["score"] <= 4:
        return "重复 / 低增量"
    if row["status"] == "观察中":
        return "观察中"
    if row["section_hint"] == "AI 圈博主" and row["score"] >= 5:
        return "可补位"
    if row["score"] >= 8:
        return "今日必看"
    return "观察中"


def render_review_markdown(conn: sqlite3.Connection, report_day: date, limit: int) -> str:
    rows = candidate_rows_for_review(conn, report_day, limit)
    generated_at = iso_now()
    grouped = {
        "今日必看": [],
        "可补位": [],
        "观察中": [],
        "重复 / 低增量": [],
    }
    for row in rows:
        grouped[review_bucket(row)].append(row)

    lines = [
        f"# AI 信号候选 Review - {report_day:%Y-%m-%d}",
        "",
        f"- 生成时间：{generated_at}",
        f"- 候选范围：最近 7 天内未过期、未暂停、未采用的本地候选，最多 {limit} 条",
        "- 使用方式：把每条候选下方 `signal-feedback` 代码块中的 `status`、`adoption_reason`、`rejection_reason` 或 `retrospective_status` 改成你的判断，再运行 `python3 scripts/update_signal_feedback.py --date YYYY-MM-DD`。",
        "- 安全边界：本清单只引用公开来源；不要把 Cookie、Token、私域内容或登录态全文粘贴进 review。",
        "",
    ]
    for bucket, bucket_rows in grouped.items():
        lines.append(f"## {bucket}")
        lines.append("")
        if not bucket_rows:
            lines.append("- 暂无候选")
            lines.append("")
            continue
        for index, row in enumerate(bucket_rows, start=1):
            evidence_urls = json.loads(row["evidence_urls"])
            evidence_text = ", ".join(f"[来源 {i + 1}]({url})" for i, url in enumerate(evidence_urls))
            lines.extend(
                [
                    f"### {index}. {row['title']}",
                    "",
                    f"- 候选 ID：`{row['candidate_id']}`",
                    f"- 来源：{row['source_name']} (`{row['source_id']}`, {row['source_role']})",
                    f"- 建议栏目：{row['section_hint']}",
                    f"- 类型：{row['item_type']}",
                    f"- 分数：{row['score']}/10",
                    f"- 发布时间：{row['published_at'] or 'unknown'}",
                    f"- 采集时间：{row['collected_at']}",
                    f"- trend_key：`{row['trend_key']}`",
                    f"- 摘要：{row['summary']}",
                    f"- 证据：{evidence_text}",
                    "",
                    "```signal-feedback",
                    f"candidate_id: {row['candidate_id']}",
                    f"status: {row['status']}",
                    f"adoption_reason: {row['adoption_reason']}",
                    f"rejection_reason: {row['rejection_reason']}",
                    f"retrospective_status: {row['retrospective_status']}",
                    "```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def parse_feedback_blocks(content: str) -> list[dict[str, str]]:
    blocks = re.findall(r"```signal-feedback\n(.*?)\n```", content, flags=re.DOTALL)
    parsed: list[dict[str, str]] = []
    for block in blocks:
        item: dict[str, str] = {}
        for line in block.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            key, sep, value = line.partition(":")
            if not sep:
                continue
            item[key.strip()] = value.strip()
        if "candidate_id" in item:
            status = item.get("status", "待审")
            retrospective = item.get("retrospective_status", "待验证")
            if status not in VALID_STATUSES:
                raise ValueError(f"invalid status for {item['candidate_id']}: {status}")
            if retrospective not in VALID_RETROSPECTIVE_STATUSES:
                raise ValueError(
                    f"invalid retrospective_status for {item['candidate_id']}: {retrospective}"
                )
            parsed.append(item)
    return parsed


def apply_feedback(conn: sqlite3.Connection, feedback: list[dict[str, str]], updated_at: str) -> int:
    changed = 0
    for item in feedback:
        cursor = conn.execute(
            """
            UPDATE candidates
            SET status=?,
                adoption_reason=?,
                rejection_reason=?,
                retrospective_status=?,
                last_updated_at=?
            WHERE candidate_id=?
            """,
            (
                item.get("status", "待审"),
                item.get("adoption_reason", ""),
                item.get("rejection_reason", ""),
                item.get("retrospective_status", "待验证"),
                updated_at,
                item["candidate_id"],
            ),
        )
        changed += cursor.rowcount
    return changed


def refresh_source_profiles(conn: sqlite3.Connection, updated_at: str) -> None:
    sources = conn.execute("SELECT * FROM sources").fetchall()
    for source in sources:
        stats = conn.execute(
            """
            SELECT
                COUNT(*) AS seen_count,
                SUM(CASE WHEN status='已采用' THEN 1 ELSE 0 END) AS adopted_count,
                SUM(CASE WHEN status='重复' THEN 1 ELSE 0 END) AS repeated_count,
                MAX(collected_at) AS last_seen_at,
                MAX(CASE WHEN status='已采用' THEN last_updated_at ELSE NULL END) AS last_adopted_at
            FROM candidates
            WHERE source_id=?
            """,
            (source["source_id"],),
        ).fetchone()
        checks = conn.execute(
            """
            SELECT
                COUNT(*) AS total_checks,
                SUM(CASE WHEN result NOT IN ('hit', 'miss') THEN 1 ELSE 0 END) AS failed_checks
            FROM source_checks
            WHERE source_id=?
            """,
            (source["source_id"],),
        ).fetchone()
        seen_count = int(stats["seen_count"] or 0)
        repeated_count = int(stats["repeated_count"] or 0)
        total_checks = int(checks["total_checks"] or 0)
        failed_checks = int(checks["failed_checks"] or 0)
        failure_rate = failed_checks / total_checks if total_checks else 0.0
        duplicate_rate = repeated_count / seen_count if seen_count else 0.0
        conn.execute(
            """
            INSERT INTO source_profiles (
                source_id, name, platform, source_role, source_tier, seen_count,
                adopted_count, repeated_count, last_seen_at, last_adopted_at,
                failure_rate, duplicate_rate, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_id) DO UPDATE SET
                name=excluded.name,
                platform=excluded.platform,
                source_role=excluded.source_role,
                source_tier=excluded.source_tier,
                seen_count=excluded.seen_count,
                adopted_count=excluded.adopted_count,
                repeated_count=excluded.repeated_count,
                last_seen_at=excluded.last_seen_at,
                last_adopted_at=excluded.last_adopted_at,
                failure_rate=excluded.failure_rate,
                duplicate_rate=excluded.duplicate_rate,
                updated_at=excluded.updated_at
            """,
            (
                source["source_id"],
                source["name"],
                source["platform"],
                source["source_role"],
                source["source_tier"],
                seen_count,
                int(stats["adopted_count"] or 0),
                repeated_count,
                stats["last_seen_at"],
                stats["last_adopted_at"],
                failure_rate,
                duplicate_rate,
                updated_at,
            ),
        )


def load_manual_items(path: Path, collected_at: str) -> list[FeedItem]:
    if not path.is_file():
        return []
    items: list[FeedItem] = []
    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            data = json.loads(line)
            url = data.get("url", "")
            validate_public_url(url)
            title = data.get("title") or url
            items.append(
                FeedItem(
                    data.get("source_id", "manual_public_links"),
                    title,
                    url,
                    parse_datetime_to_iso(data.get("published_at", "")) or collected_at,
                    data.get("summary", ""),
                )
            )
    return items


def build_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--date", help="Report date in YYYY-MM-DD; defaults to current Asia/Shanghai date")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite path under .codex-run/")
    return parser


def print_table(rows: list[tuple[str, str]]) -> None:
    width = max((len(left) for left, _ in rows), default=0)
    for left, right in rows:
        print(f"{left.ljust(width)}  {right}")


def main_error(exc: Exception) -> int:
    print(f"error: {exc}", file=sys.stderr)
    return 1
