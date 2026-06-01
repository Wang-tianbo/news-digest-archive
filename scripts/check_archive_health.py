#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


SHANGHAI_TZ = timezone(timedelta(hours=8))


@dataclass(frozen=True)
class HealthResult:
    label: str
    ok: bool
    details: list[str]


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


def run_git(root: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return result.stderr.strip() or result.stdout.strip() or "git command failed"
    return result.stdout.strip()


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


def check_git(root: Path) -> HealthResult:
    status = run_git(root, ["status", "--short", "--branch"])
    latest = run_git(root, ["log", "-1", "--format=%h %cs %s"])
    details = [f"status: {status}", f"latest commit: {latest}"]
    ok = "ahead" not in status and "behind" not in status and "\n" not in status
    return HealthResult("git", ok, details)


def print_result(result: HealthResult) -> None:
    marker = "OK" if result.ok else "WARN"
    print(f"[{marker}] {result.label}")
    for detail in result.details:
        print(f"  - {detail}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check archive report continuity.")
    parser.add_argument("--today", help="Asia/Shanghai date in YYYY-MM-DD format.")
    parser.add_argument("--daily-lookback", type=int, default=14)
    parser.add_argument("--weekly-lookback", type=int, default=4)
    parser.add_argument("--monthly-lookback", type=int, default=2)
    args = parser.parse_args()

    root = repo_root()
    today = parse_date(args.today) if args.today else datetime.now(SHANGHAI_TZ).date()
    archive_start = earliest_daily_date(root)

    results = [
        check_daily(root, filter_by_archive_start(expected_report_days(today, args.daily_lookback), archive_start)),
        check_weekly(root, filter_weeks_by_archive_start(expected_completed_weeks(today, args.weekly_lookback), archive_start)),
        check_monthly(root, filter_months_by_archive_start(expected_completed_months(today, args.monthly_lookback), archive_start)),
        check_git(root),
    ]

    print(f"Archive health as of {today:%Y-%m-%d} Asia/Shanghai")
    if archive_start:
        print(f"Archive start: {archive_start:%Y-%m-%d}")
    for result in results:
        print_result(result)

    if not all(result.ok for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
