#!/usr/bin/env python3

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import os
import shutil
import subprocess
import time

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback.
    tomllib = None

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python < 3.9 fallback.
    ZoneInfo = None


SHANGHAI_TZ = timezone(timedelta(hours=8))
RRULE_WEEKDAYS = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
DAILY_TRIGGER_HOUR = 9
DAILY_TRIGGER_MINUTE = 5
DAILY_TRIGGER_SECOND = 0
WATCHDOG_TRIGGER_HOUR = 9
WATCHDOG_TRIGGER_MINUTE = 35
WATCHDOG_TRIGGER_SECOND = 0
AUTOMATIONS = [
    {
        "id": "daily-ai-digest-archive",
        "template": "daily-ai-digest-archive.toml.template",
        "rrule_key": "__RRULE_JSON__",
        "schedule": lambda: daily_rrule_for_shanghai_clock(
            DAILY_TRIGGER_HOUR,
            DAILY_TRIGGER_MINUTE,
            DAILY_TRIGGER_SECOND,
        ),
    },
    {
        "id": "daily-ai-digest-watchdog",
        "template": "daily-ai-digest-watchdog.toml.template",
        "rrule_key": "__RRULE_WATCHDOG_JSON__",
        "schedule": lambda: daily_rrule_for_shanghai_clock(
            WATCHDOG_TRIGGER_HOUR,
            WATCHDOG_TRIGGER_MINUTE,
            WATCHDOG_TRIGGER_SECOND,
        ),
    },
    {
        "id": "weekly-ai-digest-summary",
        "template": "weekly-ai-digest-summary.toml.template",
        "rrule_key": "__RRULE_WEEKLY_JSON__",
        "schedule": lambda: weekly_rrule_for_shanghai_weekday(0, 9, 10, 0),
    },
    {
        "id": "monthly-ai-digest-summary",
        "template": "monthly-ai-digest-summary.toml.template",
        "rrule_key": "__RRULE_MONTHLY_JSON__",
        "schedule": lambda: monthly_rrule_for_shanghai_first_day(9, 15, 0),
    },
    {
        "id": "yearly-ai-digest-summary",
        "template": "yearly-ai-digest-summary.toml.template",
        "rrule_key": "__RRULE_YEARLY_JSON__",
        "schedule": lambda: yearly_rrule_for_shanghai_jan1(9, 20, 0),
    },
]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_git_repo(root: Path) -> None:
    git_dir = root / ".git"
    if not git_dir.exists():
        raise SystemExit(
            "This installer must be run from a checked-out git repository. "
            "Please clone the repository first."
        )


def read_origin_url(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def codex_home() -> Path:
    override = os.environ.get("CODEX_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".codex"


def local_timezone():
    if ZoneInfo is not None:
        env_tz = os.environ.get("TZ")
        if env_tz and not env_tz.startswith(":"):
            try:
                return ZoneInfo(env_tz)
            except Exception:
                pass

        localtime = Path("/etc/localtime")
        if localtime.exists():
            try:
                resolved = localtime.resolve()
                parts = resolved.parts
                if "zoneinfo" in parts:
                    zone_key = "/".join(parts[parts.index("zoneinfo") + 1 :])
                    return ZoneInfo(zone_key)
            except Exception:
                pass

    return datetime.now().astimezone().tzinfo


def local_candidates_for_shanghai_datetimes(
    shanghai_datetimes: list[datetime],
) -> list[datetime]:
    candidates: list[datetime] = []

    for shanghai_time in shanghai_datetimes:
        # Use the OS local-time conversion for each target instant so DST
        # transitions are handled even when no IANA timezone name is available.
        candidate = datetime.fromtimestamp(shanghai_time.timestamp(), timezone.utc).astimezone()
        exists = any(
            existing.hour == candidate.hour
            and existing.minute == candidate.minute
            and existing.second == candidate.second
            and existing.weekday() == candidate.weekday()
            and existing.day == candidate.day
            and existing.month == candidate.month
            for existing in candidates
        )
        if not exists:
            candidates.append(candidate)

    return candidates


def utc_candidates_for_shanghai_datetimes(
    shanghai_datetimes: list[datetime],
) -> list[datetime]:
    candidates: list[datetime] = []
    for shanghai_time in shanghai_datetimes:
        candidate = shanghai_time.astimezone(timezone.utc)
        exists = any(
            existing.hour == candidate.hour
            and existing.minute == candidate.minute
            and existing.second == candidate.second
            and existing.weekday() == candidate.weekday()
            and existing.day == candidate.day
            and existing.month == candidate.month
            for existing in candidates
        )
        if not exists:
            candidates.append(candidate)

    return candidates


def clock_candidates_for_shanghai_datetimes(
    shanghai_datetimes: list[datetime],
) -> list[datetime]:
    # Codex cron has shown both local-clock and UTC-clock behavior across app
    # versions. Include both candidates; each automation prompt gates on the
    # real Asia/Shanghai business window before doing any repository work.
    candidates = [
        *local_candidates_for_shanghai_datetimes(shanghai_datetimes),
        *utc_candidates_for_shanghai_datetimes(shanghai_datetimes),
    ]
    unique: list[datetime] = []
    for candidate in candidates:
        exists = any(
            existing.hour == candidate.hour
            and existing.minute == candidate.minute
            and existing.second == candidate.second
            and existing.weekday() == candidate.weekday()
            and existing.day == candidate.day
            and existing.month == candidate.month
            for existing in unique
        )
        if not exists:
            unique.append(candidate)
    return unique


def describe_clock_candidates(candidates: list[datetime]) -> str:
    labels: list[str] = []
    for candidate in candidates:
        label = candidate.strftime("%H:%M:%S %Z")
        if label not in labels:
            labels.append(label)
    return ", ".join(labels)


def describe_weekday_clock_candidates(candidates: list[datetime]) -> str:
    labels: list[str] = []
    for candidate in candidates:
        label = f"{RRULE_WEEKDAYS[candidate.weekday()]} {candidate.strftime('%H:%M:%S %Z')}"
        if label not in labels:
            labels.append(label)
    return ", ".join(labels)


def describe_monthday_clock_candidates(candidates: list[datetime]) -> str:
    labels: list[str] = []
    for candidate in candidates:
        label = f"{candidate.day} {candidate.strftime('%H:%M:%S %Z')}"
        if label not in labels:
            labels.append(label)
    return ", ".join(labels)


def describe_yearday_clock_candidates(candidates: list[datetime]) -> str:
    labels: list[str] = []
    for candidate in candidates:
        label = f"{candidate.month:02d}-{candidate.day:02d} {candidate.strftime('%H:%M:%S %Z')}"
        if label not in labels:
            labels.append(label)
    return ", ".join(labels)


def shanghai_clock_samples(year: int, hour: int, minute: int, second: int) -> list[datetime]:
    return [
        datetime(year, 1, 15, hour, minute, second, tzinfo=SHANGHAI_TZ),
        datetime(year, 7, 15, hour, minute, second, tzinfo=SHANGHAI_TZ),
    ]


def daily_rrule_for_shanghai_clock(hour: int, minute: int, second: int) -> str:
    year = datetime.now(SHANGHAI_TZ).year
    candidates = clock_candidates_for_shanghai_datetimes(
        shanghai_clock_samples(year, hour, minute, second)
    )
    hours = sorted({candidate.hour for candidate in candidates})
    minutes = sorted({candidate.minute for candidate in candidates})
    seconds = sorted({candidate.second for candidate in candidates})
    return (
        "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;"
        f"BYHOUR={','.join(str(value) for value in hours)};"
        f"BYMINUTE={','.join(str(value) for value in minutes)};"
        f"BYSECOND={','.join(str(value) for value in seconds)}"
    )


def weekly_rrule_for_shanghai_weekday(
    shanghai_weekday: int,
    hour: int,
    minute: int,
    second: int,
) -> str:
    year = datetime.now(SHANGHAI_TZ).year
    samples = []
    for sample in shanghai_clock_samples(year, hour, minute, second):
        delta = (shanghai_weekday - sample.weekday()) % 7
        samples.append(sample + timedelta(days=delta))
    candidates = clock_candidates_for_shanghai_datetimes(samples)
    bydays = sorted({RRULE_WEEKDAYS[candidate.weekday()] for candidate in candidates})
    hours = sorted({candidate.hour for candidate in candidates})
    minutes = sorted({candidate.minute for candidate in candidates})
    seconds = sorted({candidate.second for candidate in candidates})
    return (
        f"FREQ=WEEKLY;BYDAY={','.join(bydays)};"
        f"BYHOUR={','.join(str(value) for value in hours)};"
        f"BYMINUTE={','.join(str(value) for value in minutes)};"
        f"BYSECOND={','.join(str(value) for value in seconds)}"
    )


def monthly_rrule_for_shanghai_first_day(hour: int, minute: int, second: int) -> str:
    year = datetime.now(SHANGHAI_TZ).year
    candidates = clock_candidates_for_shanghai_datetimes(
        [
            datetime(year, 1, 1, hour, minute, second, tzinfo=SHANGHAI_TZ),
            datetime(year, 7, 1, hour, minute, second, tzinfo=SHANGHAI_TZ),
        ]
    )
    hours = sorted({candidate.hour for candidate in candidates})
    minutes = sorted({candidate.minute for candidate in candidates})
    seconds = sorted({candidate.second for candidate in candidates})
    return (
        "FREQ=MONTHLY;BYMONTHDAY=1,-1;"
        f"BYHOUR={','.join(str(value) for value in hours)};"
        f"BYMINUTE={','.join(str(value) for value in minutes)};"
        f"BYSECOND={','.join(str(value) for value in seconds)}"
    )


def yearly_rrule_for_shanghai_jan1(hour: int, minute: int, second: int) -> str:
    year = datetime.now(SHANGHAI_TZ).year
    candidates = clock_candidates_for_shanghai_datetimes(
        [datetime(year, 1, 1, hour, minute, second, tzinfo=SHANGHAI_TZ)]
    )
    hours = sorted({candidate.hour for candidate in candidates})
    minutes = sorted({candidate.minute for candidate in candidates})
    seconds = sorted({candidate.second for candidate in candidates})
    return (
        "FREQ=YEARLY;BYYEARDAY=1,-1;"
        f"BYHOUR={','.join(str(value) for value in hours)};"
        f"BYMINUTE={','.join(str(value) for value in minutes)};"
        f"BYSECOND={','.join(str(value) for value in seconds)}"
    )


def render_template(
    template: str,
    repo: Path,
    timestamp_ms: int,
    rrule_replacements: dict[str, str],
) -> str:
    replacements = {
        "__REPO_ROOT_JSON__": json.dumps(str(repo)),
        "__CREATED_AT_MS__": str(timestamp_ms),
        "__UPDATED_AT_MS__": str(timestamp_ms),
        **rrule_replacements,
    }
    for source, target in replacements.items():
        template = template.replace(source, target)
    return template


def validate_toml(rendered: str, target_file: Path) -> None:
    if tomllib is None:
        return
    try:
        tomllib.loads(rendered)
    except tomllib.TOMLDecodeError as exc:
        raise SystemExit(f"Rendered automation TOML is invalid for {target_file}: {exc}") from exc


def atomic_write_text(path: Path, content: str) -> None:
    tmp_path = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp_path.write_text(content, encoding="utf-8")
    tmp_path.replace(path)


def install_one(root: Path, spec: dict[str, object], timestamp_ms: int) -> Path:
    template_path = root / "ops" / "codex" / str(spec["template"])
    if not template_path.is_file():
        raise SystemExit(f"Missing template: {template_path}")

    automation_id = str(spec["id"])
    target_dir = codex_home() / "automations" / automation_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "automation.toml"

    if target_file.exists():
        backup_name = f"{target_file.name}.bak.{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(target_file, target_dir / backup_name)

    rrule = str(spec["schedule"]())
    rrule_key = str(spec["rrule_key"])
    rendered = render_template(
        template_path.read_text(encoding="utf-8"),
        root,
        timestamp_ms,
        {rrule_key: json.dumps(rrule)},
    )
    validate_toml(rendered, target_file)
    atomic_write_text(target_file, rendered)
    return target_file


def main() -> None:
    root = repo_root()
    ensure_git_repo(root)

    detected_local_tz = local_timezone()
    if detected_local_tz:
        local_now = datetime.now().astimezone(detected_local_tz)
    else:
        local_now = datetime.now().astimezone()
    timestamp_ms = int(time.time() * 1000)
    origin_url = read_origin_url(root)

    installed_files: list[tuple[str, Path]] = []
    for spec in AUTOMATIONS:
        installed = install_one(root, spec, timestamp_ms)
        installed_files.append((str(spec["id"]), installed))

    timezone_label = getattr(detected_local_tz, "key", None) or local_now.tzname() or "local"
    year = datetime.now(SHANGHAI_TZ).year
    daily_trigger_times = describe_clock_candidates(
        clock_candidates_for_shanghai_datetimes(
            shanghai_clock_samples(
                year,
                DAILY_TRIGGER_HOUR,
                DAILY_TRIGGER_MINUTE,
                DAILY_TRIGGER_SECOND,
            )
        )
    )
    watchdog_trigger_times = describe_clock_candidates(
        clock_candidates_for_shanghai_datetimes(
            shanghai_clock_samples(
                year,
                WATCHDOG_TRIGGER_HOUR,
                WATCHDOG_TRIGGER_MINUTE,
                WATCHDOG_TRIGGER_SECOND,
            )
        )
    )
    weekly_trigger_slots = describe_weekday_clock_candidates(
        clock_candidates_for_shanghai_datetimes(
            [
                sample + timedelta(days=(0 - sample.weekday()) % 7)
                for sample in shanghai_clock_samples(year, 9, 10, 0)
            ]
        )
    )
    monthly_trigger_slots = describe_monthday_clock_candidates(
        clock_candidates_for_shanghai_datetimes(
            [
                datetime(year, 1, 1, 9, 15, 0, tzinfo=SHANGHAI_TZ),
                datetime(year, 7, 1, 9, 15, 0, tzinfo=SHANGHAI_TZ),
            ]
        )
    )
    yearly_trigger_slots = describe_yearday_clock_candidates(
        clock_candidates_for_shanghai_datetimes(
            [datetime(year, 1, 1, 9, 20, 0, tzinfo=SHANGHAI_TZ)]
        )
    )

    print("Installed Codex automations:")
    for automation_id, path in installed_files:
        print(f"- {automation_id}: {path}")
    print(f"Repository root: {root}")
    print(f"Git origin: {origin_url or 'not configured'}")
    print(f"Local timezone: {timezone_label}")
    print(
        "Daily trigger candidates for "
        f"Asia/Shanghai {DAILY_TRIGGER_HOUR:02d}:{DAILY_TRIGGER_MINUTE:02d}: "
        f"{daily_trigger_times}"
    )
    print(
        "Daily watchdog trigger candidates for "
        f"Asia/Shanghai {WATCHDOG_TRIGGER_HOUR:02d}:{WATCHDOG_TRIGGER_MINUTE:02d}: "
        f"{watchdog_trigger_times}"
    )
    print(f"Weekly trigger candidates for Asia/Shanghai Monday 09:10: {weekly_trigger_slots}")
    print(f"Monthly trigger candidates for Asia/Shanghai day 1 09:15: {monthly_trigger_slots}")
    print(f"Yearly trigger candidates for Asia/Shanghai January 1 09:20: {yearly_trigger_slots}")
    print(
        "RRULEs include both local-clock and UTC-clock candidates because Codex "
        "cron interpretation can vary by app version; prompts no-op outside the "
        "Asia/Shanghai business window."
    )
    if not origin_url:
        print("Warning: no git origin remote found. Automated pushes will fail until origin is configured.")
    print("Rerun this script if the repository path or system timezone changes.")


if __name__ == "__main__":
    main()
