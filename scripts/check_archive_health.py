#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


SHANGHAI_TZ = timezone(timedelta(hours=8))
AUTOMATION_IDS = [
    "daily-ai-digest-archive",
    "daily-ai-digest-watchdog",
    "weekly-ai-digest-summary",
    "monthly-ai-digest-summary",
    "yearly-ai-digest-summary",
    "daily-ai-digest-notify",
    "weekly-ai-digest-notify",
    "monthly-ai-digest-notify",
    "yearly-ai-digest-notify",
]
REQUIRED_DAILY_SECTIONS = [
    "## 结构化快照",
    "## 主线判断",
    "## 今日评论与判断",
    "## 结构化索引",
    "## 参考来源",
]
DAILY_SECTION_ALIASES = [
    ("AI 新闻", ["## AI 新闻", "## 今日最重要"]),
]
REQUIRED_DAILY_METADATA = [
    "date:",
    "window_start:",
    "window_end:",
    "themes:",
    "signals:",
    "peripheral_themes:",
    "followups:",
    "fact_confidence:",
    "signal_strength:",
]
STRICT_DAILY_METADATA = [
    "opinion_sources:",
    "viewpoint_themes:",
    "research_sources:",
    "research_themes:",
    "research_artifacts:",
    "research_interpretations:",
    "source_checks:",
    "evidence_items:",
]


@dataclass(frozen=True)
class HealthResult:
    label: str
    ok: bool
    details: list[str]


@dataclass(frozen=True)
class CommandResult:
    ok: bool
    output: str


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def daily_path(root: Path, day: date) -> Path:
    return root / "daily" / f"{day:%Y}" / f"{day:%Y-%m}" / f"{day:%Y-%m-%d}.md"


def weekly_path(root: Path, day: date) -> Path:
    iso = day.isocalendar()
    return root / "weekly" / f"{iso.year}" / f"{iso.year}-W{iso.week:02d}.md"


def monthly_path(root: Path, day: date) -> Path:
    return root / "monthly" / f"{day:%Y}" / f"{day:%Y-%m}.md"


def yearly_path(root: Path, day: date) -> Path:
    return root / "yearly" / f"{day:%Y}" / f"{day:%Y}.md"


def codex_home() -> Path:
    override = os.environ.get("CODEX_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".codex"


def iter_days(start: date, end: date) -> list[date]:
    days: list[date] = []
    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)
    return days


def expected_report_days(today: date, lookback_days: int) -> list[date]:
    end = today
    start = today - timedelta(days=lookback_days - 1)
    return iter_days(start, end)


def earliest_daily_date(root: Path) -> date | None:
    dates: list[date] = []
    for path in (root / "daily").glob("[0-9][0-9][0-9][0-9]/*/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"):
        try:
            dates.append(parse_date(path.stem))
        except ValueError:
            continue
    return min(dates) if dates else None


def monday_of_week(day: date) -> date:
    return day - timedelta(days=day.weekday())


def expected_completed_weeks(today: date, lookback_weeks: int) -> list[date]:
    current_week_monday = monday_of_week(today)
    latest_completed = current_week_monday - timedelta(days=7)
    return [latest_completed - timedelta(days=7 * offset) for offset in range(lookback_weeks)]


def expected_completed_months(today: date, lookback_months: int) -> list[date]:
    months: list[date] = []
    year = today.year
    month = today.month - 1
    while len(months) < lookback_months:
        if month == 0:
            month = 12
            year -= 1
        months.append(date(year, month, 1))
        month -= 1
    return months


def expected_completed_years(today: date, lookback_years: int) -> list[date]:
    return [date(today.year - offset, 1, 1) for offset in range(1, lookback_years + 1)]


def filter_by_archive_start(days: list[date], archive_start: date | None) -> list[date]:
    if archive_start is None:
        return days
    return [day for day in days if day >= archive_start]


def filter_weeks_by_archive_start(week_mondays: list[date], archive_start: date | None) -> list[date]:
    if archive_start is None:
        return week_mondays
    return [week for week in week_mondays if week + timedelta(days=6) >= archive_start]


def filter_months_by_archive_start(month_starts: list[date], archive_start: date | None) -> list[date]:
    if archive_start is None:
        return month_starts
    filtered: list[date] = []
    for month_start in month_starts:
        if month_start.month == 12:
            next_month = date(month_start.year + 1, 1, 1)
        else:
            next_month = date(month_start.year, month_start.month + 1, 1)
        if next_month - timedelta(days=1) >= archive_start:
            filtered.append(month_start)
    return filtered


def filter_years_by_archive_start(year_starts: list[date], archive_start: date | None) -> list[date]:
    if archive_start is None:
        return year_starts
    return [year_start for year_start in year_starts if date(year_start.year, 12, 31) >= archive_start]


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
    result = run_command(["git", *args], root)
    if not result.ok:
        return CommandResult(False, result.output or "git command failed")
    return result


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_yaml_list_values(content: str, key: str) -> list[str]:
    values: list[str] = []
    pattern = re.compile(rf"^{re.escape(key)}:\s*$", re.MULTILINE)
    match = pattern.search(content)
    if not match:
        return values
    for line in content[match.end() :].splitlines():
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", line):
            break
        item_match = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if item_match:
            values.append(item_match.group(1).strip().strip("'\""))
    return values


def validate_daily_structure(root: Path, day: date, max_lines: int, strict_template: bool) -> list[str]:
    path = daily_path(root, day)
    if not path.is_file():
        return []
    details: list[str] = []
    try:
        content = read_text(path)
    except UnicodeDecodeError as exc:
        return [f"{path.relative_to(root)} is not valid UTF-8: {exc}"]

    rel = path.relative_to(root)
    lines = content.splitlines()
    expected_title = f"# AI 日报 - {day:%Y-%m-%d}"
    if not lines or lines[0].strip() != expected_title:
        details.append(f"{rel} title mismatch; expected `{expected_title}`")
    if len(lines) > max_lines:
        details.append(f"{rel} has {len(lines)} lines, above threshold {max_lines}")
    for section in REQUIRED_DAILY_SECTIONS:
        if section not in content:
            details.append(f"{rel} missing section `{section}`")
    for label, aliases in DAILY_SECTION_ALIASES:
        if not any(alias in content for alias in aliases):
            details.append(f"{rel} missing section `{label}` or a legacy equivalent")
    for key in REQUIRED_DAILY_METADATA:
        if key not in content:
            details.append(f"{rel} missing metadata key `{key}`")
    if strict_template:
        for key in STRICT_DAILY_METADATA:
            if key not in content:
                details.append(f"{rel} missing strict-template metadata key `{key}`")
    if "http://" not in content and "https://" not in content:
        details.append(f"{rel} has no clickable source link")
    if content.count("```") % 2 != 0:
        details.append(f"{rel} has an unbalanced fenced code block")
    return details


def check_daily_structure(
    root: Path,
    days: list[date],
    max_lines: int,
    strict_template: bool,
) -> HealthResult:
    details: list[str] = []
    for day in days:
        details.extend(validate_daily_structure(root, day, max_lines, strict_template))
    if not details:
        details.append(f"all {len(days)} existing daily reports passed structure checks")
    return HealthResult("daily-structure", not details or details[0].startswith("all "), details)


def validate_weekly_sources(root: Path, week_mondays: list[date]) -> list[str]:
    details: list[str] = []
    for week_monday in week_mondays:
        path = weekly_path(root, week_monday)
        if not path.is_file():
            continue
        try:
            content = read_text(path)
        except UnicodeDecodeError as exc:
            details.append(f"{path.relative_to(root)} is not valid UTF-8: {exc}")
            continue
        for value in extract_yaml_list_values(content, "missing_digest_dates"):
            try:
                missing_day = parse_date(value)
            except ValueError:
                continue
            if daily_path(root, missing_day).is_file():
                details.append(
                    f"{path.relative_to(root)} lists {missing_day:%Y-%m-%d} as missing, "
                    "but the daily file exists"
                )
    return details


def check_weekly_sources(root: Path, week_mondays: list[date]) -> HealthResult:
    details = validate_weekly_sources(root, week_mondays)
    if not details:
        details.append(f"all {len(week_mondays)} weekly source references look consistent")
    return HealthResult("weekly-sources", not details or details[0].startswith("all "), details)


def check_yearly(root: Path, year_starts: list[date]) -> HealthResult:
    missing = [day for day in year_starts if not yearly_path(root, day).is_file()]
    details = [f"missing yearly: {yearly_path(root, day).relative_to(root)}" for day in missing]
    if not missing:
        details.append(f"all {len(year_starts)} expected yearly reports exist")
    return HealthResult("yearly", not missing, details)


def check_automations(root: Path) -> HealthResult:
    details: list[str] = []
    home = codex_home()
    for automation_id in AUTOMATION_IDS:
        path = home / "automations" / automation_id / "automation.toml"
        if not path.is_file():
            details.append(f"missing automation: {path}")
            continue
        try:
            content = read_text(path)
        except UnicodeDecodeError as exc:
            details.append(f"{path} is not valid UTF-8: {exc}")
            continue
        if 'status = "ACTIVE"' not in content:
            details.append(f"{path} is not ACTIVE")
        if "rrule =" not in content:
            details.append(f"{path} missing rrule")
        if str(root) not in content:
            details.append(f"{path} does not reference repository root {root}")
    if not details:
        details.append(f"all {len(AUTOMATION_IDS)} Codex automations are installed and active")
    return HealthResult("automations", not details or details[0].startswith("all "), details)


def check_git(root: Path, fetch: bool) -> HealthResult:
    details: list[str] = []
    ok = True
    if fetch:
        fetch_result = run_git(root, ["fetch", "origin", "main"])
        details.append(f"fetch: {fetch_result.output or 'ok'}")
        ok = ok and fetch_result.ok

    status = run_git(root, ["status", "--short", "--branch"])
    latest = run_git(root, ["log", "-1", "--format=%h %cs %s"])
    upstream = run_git(root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    details.extend(
        [
            f"status: {status.output}",
            f"latest commit: {latest.output}",
            f"upstream: {upstream.output}",
        ]
    )
    ok = (
        ok
        and status.ok
        and latest.ok
        and upstream.ok
        and "ahead" not in status.output
        and "behind" not in status.output
        and "\n" not in status.output
    )
    return HealthResult("git", ok, details)


def check_daily(root: Path, days: list[date]) -> HealthResult:
    missing = [day for day in days if not daily_path(root, day).is_file()]
    details = [f"missing daily: {daily_path(root, day).relative_to(root)}" for day in missing]
    if not missing:
        details.append(f"all {len(days)} expected daily reports exist")
    return HealthResult("daily", not missing, details)


def check_weekly(root: Path, week_mondays: list[date]) -> HealthResult:
    missing = [day for day in week_mondays if not weekly_path(root, day).is_file()]
    details = [f"missing weekly: {weekly_path(root, day).relative_to(root)}" for day in missing]
    if not missing:
        details.append(f"all {len(week_mondays)} expected weekly reports exist")
    return HealthResult("weekly", not missing, details)


def check_monthly(root: Path, month_starts: list[date]) -> HealthResult:
    missing = [day for day in month_starts if not monthly_path(root, day).is_file()]
    details = [f"missing monthly: {monthly_path(root, day).relative_to(root)}" for day in missing]
    if not missing:
        details.append(f"all {len(month_starts)} expected monthly reports exist")
    return HealthResult("monthly", not missing, details)


def print_result(result: HealthResult) -> None:
    marker = "OK" if result.ok else "WARN"
    print(f"[{marker}] {result.label}")
    for detail in result.details:
        print(f"  - {detail}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check archive report continuity.")
    parser.add_argument("--today", help="Asia/Shanghai date in YYYY-MM-DD format.")
    parser.add_argument("--daily-lookback", type=int, default=7)
    parser.add_argument("--weekly-lookback", type=int, default=4)
    parser.add_argument("--monthly-lookback", type=int, default=2)
    parser.add_argument("--yearly-lookback", type=int, default=0)
    parser.add_argument("--daily-max-lines", type=int, default=320)
    parser.add_argument("--fetch", action="store_true", help="Run `git fetch origin main` before git checks.")
    parser.add_argument(
        "--strict-template",
        action="store_true",
        help="Require newly introduced daily metadata fields such as opinion/research/source_checks/evidence_items.",
    )
    parser.add_argument(
        "--skip-automations",
        action="store_true",
        help="Skip checking local Codex automation files.",
    )
    args = parser.parse_args()

    root = repo_root()
    today = parse_date(args.today) if args.today else datetime.now(SHANGHAI_TZ).date()
    archive_start = earliest_daily_date(root)

    daily_days = filter_by_archive_start(expected_report_days(today, args.daily_lookback), archive_start)
    week_mondays = filter_weeks_by_archive_start(
        expected_completed_weeks(today, args.weekly_lookback),
        archive_start,
    )
    month_starts = filter_months_by_archive_start(
        expected_completed_months(today, args.monthly_lookback),
        archive_start,
    )
    year_starts = filter_years_by_archive_start(
        expected_completed_years(today, args.yearly_lookback),
        archive_start,
    )

    results = [
        check_daily(root, daily_days),
        check_daily_structure(root, daily_days, args.daily_max_lines, args.strict_template),
        check_weekly(root, week_mondays),
        check_weekly_sources(root, week_mondays),
        check_monthly(root, month_starts),
    ]
    if args.yearly_lookback > 0:
        results.append(check_yearly(root, year_starts))
    if not args.skip_automations:
        results.append(check_automations(root))
    results.append(check_git(root, args.fetch))

    print(f"Archive health as of {today:%Y-%m-%d} Asia/Shanghai")
    if archive_start:
        print(f"Archive start: {archive_start:%Y-%m-%d}")
    for result in results:
        print_result(result)

    if not all(result.ok for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
