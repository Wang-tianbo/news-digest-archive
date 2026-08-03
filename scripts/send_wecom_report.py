#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


SHANGHAI_TZ = timezone(timedelta(hours=8))
MAX_WECOM_MARKDOWN_BYTES = 4096
TARGET_MARKDOWN_BYTES = 3600
LOCAL_ENV_PATH = Path(".codex-run") / "wecom-notify.env"
DEFAULT_STATE_DIR = Path(".codex-run") / "wecom-notify"


@dataclass(frozen=True)
class CommandResult:
    ok: bool
    output: str


@dataclass(frozen=True)
class ReportTarget:
    kind: str
    label: str
    path: Path
    title_prefix: str


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def shanghai_today() -> date:
    return datetime.now(SHANGHAI_TZ).date()


def monday_of_week(day: date) -> date:
    return day - timedelta(days=day.weekday())


def previous_month(day: date) -> date:
    year = day.year
    month = day.month - 1
    if month == 0:
        year -= 1
        month = 12
    return date(year, month, 1)


def report_target(root: Path, kind: str, run_day: date) -> ReportTarget:
    if kind == "daily":
        rel = Path("daily") / f"{run_day:%Y}" / f"{run_day:%Y-%m}" / f"{run_day:%Y-%m-%d}.md"
        return ReportTarget(kind, f"{run_day:%Y-%m-%d}", rel, "AI 日报")

    if kind == "weekly":
        week_monday = monday_of_week(run_day) - timedelta(days=7)
        iso = week_monday.isocalendar()
        rel = Path("weekly") / f"{iso.year}" / f"{iso.year}-W{iso.week:02d}.md"
        return ReportTarget(kind, f"{iso.year}-W{iso.week:02d}", rel, "AI 周报")

    if kind == "monthly":
        month_start = previous_month(run_day)
        rel = Path("monthly") / f"{month_start:%Y}" / f"{month_start:%Y-%m}.md"
        return ReportTarget(kind, f"{month_start:%Y-%m}", rel, "AI 月报")

    if kind == "yearly":
        year_start = date(run_day.year - 1, 1, 1)
        rel = Path("yearly") / f"{year_start:%Y}" / f"{year_start:%Y}.md"
        return ReportTarget(kind, f"{year_start:%Y}", rel, "AI 年报")

    raise ValueError(f"Unsupported report kind: {kind}")


def run_command(args: list[str], cwd: Path) -> CommandResult:
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = result.stdout.strip() or result.stderr.strip()
    return CommandResult(result.returncode == 0, output)


def run_git(root: Path, args: list[str]) -> CommandResult:
    return run_command(["git", *args], root)


def load_local_env(root: Path) -> None:
    env_path = root / LOCAL_ENV_PATH
    if not env_path.is_file():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def remote_contains_report(root: Path, rel_path: Path) -> tuple[bool, str | None]:
    fetch = run_git(root, ["fetch", "origin", "main"])
    if not fetch.ok:
        raise SystemExit(f"notification failed: git fetch origin main failed: {fetch.output}")

    rel = rel_path.as_posix()
    exists = run_git(root, ["cat-file", "-e", f"origin/main:{rel}"])
    if not exists.ok:
        return False, None

    commit = run_git(root, ["log", "-1", "--format=%H", "origin/main", "--", rel])
    if not commit.ok or not commit.output:
        return True, None
    return True, commit.output.splitlines()[0].strip()


def derive_github_base_url(root: Path) -> str | None:
    override = os.environ.get("WECOM_REPORT_BASE_URL", "").strip().rstrip("/")
    if override:
        return override

    origin = run_git(root, ["remote", "get-url", "origin"])
    if not origin.ok or not origin.output:
        return None

    remote = origin.output.strip()
    repo_path = None
    if remote.startswith("git@github.com:"):
        repo_path = remote.split(":", 1)[1]
    else:
        parsed = urllib.parse.urlparse(remote)
        if parsed.netloc.lower() == "github.com":
            repo_path = parsed.path.lstrip("/")

    if not repo_path:
        return None
    if repo_path.endswith(".git"):
        repo_path = repo_path[:-4]
    return f"https://github.com/{repo_path}/blob/main"


def read_report(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_heading(lines: list[str], fallback: str) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def first_matching_line(lines: list[str], prefixes: list[str]) -> str | None:
    for line in lines[:30]:
        stripped = line.strip()
        for prefix in prefixes:
            if stripped.startswith(prefix):
                return stripped
    return None


def section_lines(lines: list[str], headings: list[str]) -> list[str]:
    start = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if any(stripped.startswith(heading) for heading in headings):
            start = index + 1
            break
    if start is None:
        return []

    collected: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        collected.append(line.rstrip())
    return collected


def extract_snapshot(lines: list[str], limit: int = 5) -> list[str]:
    section = section_lines(lines, ["## 30 秒摘要", "## 结构化快照"])
    bullets: list[str] = []
    for line in section:
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped)
        if len(bullets) >= limit:
            break
    return bullets


def extract_judgment(lines: list[str], kind: str) -> list[str]:
    headings = {
        "daily": ["## 我的判断", "## 今日评论与判断", "## 主线判断"],
        "weekly": ["## 本周评论与判断", "## 本周主线"],
        "monthly": ["## 本月评论与判断", "## 本月结论"],
        "yearly": ["## 全年评论与判断", "## 全年结论"],
    }[kind]
    section = section_lines(lines, headings)
    items: list[str] = []
    paragraph: list[str] = []

    for line in section:
        stripped = line.strip()
        if not stripped:
            if paragraph:
                items.append("".join(paragraph))
                paragraph = []
            continue
        if stripped.startswith("<") or stripped.startswith("```"):
            continue
        if stripped.startswith("- "):
            if paragraph:
                items.append("".join(paragraph))
                paragraph = []
            items.append(stripped)
        elif not stripped.startswith("#"):
            paragraph.append(stripped)
        if len(items) >= 3:
            break

    if paragraph and len(items) < 3:
        items.append("".join(paragraph))
    return [truncate_text(item, 320) for item in items[:3]]


def truncate_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "..."


def fit_utf8_bytes(text: str, max_bytes: int) -> str:
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text

    suffix = "\n\n...已截断，查看完整报告获取全部内容。"
    budget = max_bytes - len(suffix.encode("utf-8"))
    if budget <= 0:
        return ""

    clipped = text
    while clipped and len(clipped.encode("utf-8")) > budget:
        clipped = clipped[:-1]
    return clipped.rstrip() + suffix


def report_link(root: Path, rel_path: Path) -> str | None:
    base = derive_github_base_url(root)
    if not base:
        return None
    return f"{base}/{urllib.parse.quote(rel_path.as_posix())}"


def build_markdown(root: Path, target: ReportTarget, content: str, commit: str | None) -> str:
    lines = content.splitlines()
    title = first_heading(lines, f"{target.title_prefix} - {target.label}")
    generated_at = first_matching_line(lines, ["- 生成时间：", "- 生成时间:"])
    coverage = first_matching_line(lines, ["- 覆盖时间窗：", "- 覆盖时间窗:"])
    snapshot = extract_snapshot(lines)
    judgments = extract_judgment(lines, target.kind)
    link = report_link(root, target.path)

    header = f"# {title} 已归档"
    body: list[str] = [header]
    if coverage:
        body.append(f"> {coverage.removeprefix('- ').strip()}")
    if generated_at:
        body.append(f"> {generated_at.removeprefix('- ').strip()}")
    if commit:
        body.append(f"> 远端提交：`{commit[:12]}`")

    if snapshot:
        body.append("\n**摘要快照**")
        body.extend(snapshot)

    if judgments:
        body.append("\n**评论与判断摘录**")
        body.extend(judgments)

    if link:
        link_line = f"\n[查看完整报告]({link})"
    else:
        link_line = f"\n报告路径：`{target.path.as_posix()}`"

    body_text = "\n".join(body)
    link_bytes = len(link_line.encode("utf-8"))
    fitted_body = fit_utf8_bytes(body_text, TARGET_MARKDOWN_BYTES - link_bytes)
    markdown = fitted_body.rstrip() + "\n" + link_line
    return fit_utf8_bytes(markdown, MAX_WECOM_MARKDOWN_BYTES)


def state_dir(root: Path) -> Path:
    configured = os.environ.get("WECOM_NOTIFY_STATE_DIR", "").strip()
    if configured:
        path = Path(configured)
        return path if path.is_absolute() else root / path
    return root / DEFAULT_STATE_DIR


def state_path(root: Path, target: ReportTarget) -> Path:
    safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "-", target.label)
    return state_dir(root) / f"{target.kind}-{safe_label}.json"


def payload_digest(markdown: str) -> str:
    return hashlib.sha256(markdown.encode("utf-8")).hexdigest()


def already_sent(root: Path, target: ReportTarget, commit: str | None, digest: str) -> bool:
    path = state_path(root, target)
    if not path.is_file():
        return False
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return state.get("remote_commit") == commit and state.get("payload_digest") == digest


def write_state(root: Path, target: ReportTarget, commit: str | None, digest: str) -> None:
    directory = state_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    path = state_path(root, target)
    state = {
        "kind": target.kind,
        "label": target.label,
        "report_path": target.path.as_posix(),
        "remote_commit": commit,
        "payload_digest": digest,
        "sent_at": datetime.now(SHANGHAI_TZ).isoformat(),
    }
    tmp_path = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp_path.replace(path)


def send_wecom_markdown(webhook_url: str, markdown: str) -> dict[str, object]:
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": markdown,
        },
    }
    request = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response_text = response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise SystemExit(f"notification failed: WeCom request failed: {exc}") from exc

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise SystemExit("notification failed: WeCom returned non-JSON response") from exc

    if result.get("errcode") != 0:
        errmsg = result.get("errmsg", "unknown error")
        raise SystemExit(f"notification failed: WeCom returned errcode={result.get('errcode')} errmsg={errmsg}")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send an archived report summary to WeCom.")
    parser.add_argument("--kind", choices=["daily", "weekly", "monthly", "yearly"], required=True)
    parser.add_argument(
        "--date",
        help=(
            "Asia/Shanghai automation date in YYYY-MM-DD. For weekly/monthly/yearly, "
            "the script sends the latest completed period before this date."
        ),
    )
    parser.add_argument("--dry-run", action="store_true", help="Print a sanitized preview without sending.")
    parser.add_argument("--force", action="store_true", help="Resend even if the same remote commit was sent.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = repo_root()
    load_local_env(root)

    run_day = parse_date(args.date) if args.date else shanghai_today()
    target = report_target(root, args.kind, run_day)
    report_file = root / target.path
    if not report_file.is_file():
        print(f"notification skipped: report file not found: {target.path.as_posix()}")
        return

    remote_exists, commit = remote_contains_report(root, target.path)
    if not remote_exists:
        print(f"notification skipped: report is not visible on origin/main yet: {target.path.as_posix()}")
        return

    markdown = build_markdown(root, target, read_report(report_file), commit)
    digest = payload_digest(markdown)
    if not args.force and already_sent(root, target, commit, digest):
        print(f"notification skipped: already sent {target.kind} {target.label} at commit {commit[:12] if commit else 'unknown'}")
        return

    if args.dry_run:
        print(f"notification dry-run: {target.kind} {target.label} -> {target.path.as_posix()}")
        print(f"remote commit: {commit[:12] if commit else 'unknown'}")
        print(f"markdown bytes: {len(markdown.encode('utf-8'))}")
        print("--- preview ---")
        print(markdown)
        return

    webhook_url = os.environ.get("WECOM_WEBHOOK_URL", "").strip()
    if not webhook_url:
        print("notification skipped: WECOM_WEBHOOK_URL is not configured")
        return

    send_wecom_markdown(webhook_url, markdown)
    write_state(root, target, commit, digest)
    print(f"notification sent: {target.kind} {target.label} at commit {commit[:12] if commit else 'unknown'}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
