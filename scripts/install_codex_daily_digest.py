#!/usr/bin/env python3

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import os
import subprocess
import shutil
import time


AUTOMATION_ID = "daily-ai-digest-archive"
SHANGHAI_TZ = timezone(timedelta(hours=8))


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


def trigger_candidates_for_year(year: int) -> list[datetime]:
    candidates: list[datetime] = []
    local_now = datetime.now().astimezone()
    local_tz = local_now.tzinfo
    if local_tz is None:
        raise SystemExit("Unable to determine local timezone.")

    for month, day in ((1, 15), (7, 15)):
        shanghai_time = datetime(year, month, day, 9, 0, 0, tzinfo=SHANGHAI_TZ)
        candidate = shanghai_time.astimezone(local_tz)
        exists = any(
            existing.hour == candidate.hour
            and existing.minute == candidate.minute
            and existing.second == candidate.second
            for existing in candidates
        )
        if not exists:
            candidates.append(candidate)

    return candidates


def build_rrule(candidates: list[datetime]) -> str:
    hours = sorted({candidate.hour for candidate in candidates})
    minutes = sorted({candidate.minute for candidate in candidates})
    seconds = sorted({candidate.second for candidate in candidates})
    return (
        "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;"
        f"BYHOUR={','.join(str(value) for value in hours)};"
        f"BYMINUTE={','.join(str(value) for value in minutes)};"
        f"BYSECOND={','.join(str(value) for value in seconds)}"
    )


def render_template(template: str, repo: Path, rrule: str, timestamp_ms: int) -> str:
    replacements = {
        "__REPO_ROOT_JSON__": json.dumps(str(repo)),
        "__RRULE_JSON__": json.dumps(rrule),
        "__CREATED_AT_MS__": str(timestamp_ms),
        "__UPDATED_AT_MS__": str(timestamp_ms),
    }
    for source, target in replacements.items():
        template = template.replace(source, target)
    return template


def main() -> None:
    root = repo_root()
    ensure_git_repo(root)
    template_path = root / "ops" / "codex" / f"{AUTOMATION_ID}.toml.template"
    if not template_path.is_file():
        raise SystemExit(f"Missing template: {template_path}")

    target_dir = codex_home() / "automations" / AUTOMATION_ID
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "automation.toml"

    if target_file.exists():
        backup_name = f"{target_file.name}.bak.{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(target_file, target_dir / backup_name)

    local_now = datetime.now().astimezone()
    year = datetime.now(SHANGHAI_TZ).year
    candidates = trigger_candidates_for_year(year)
    rrule = build_rrule(candidates)
    timestamp_ms = int(time.time() * 1000)

    rendered = render_template(template_path.read_text(), root, rrule, timestamp_ms)
    target_file.write_text(rendered)

    timezone_label = getattr(local_now.tzinfo, "key", None) or local_now.tzname() or "local"
    local_times = ", ".join(candidate.strftime("%H:%M:%S") for candidate in candidates)
    origin_url = read_origin_url(root)

    print(f"Installed {AUTOMATION_ID}.")
    print(f"Automation file: {target_file}")
    print(f"Repository root: {root}")
    print(f"Git origin: {origin_url or 'not configured'}")
    print(f"Local timezone: {timezone_label}")
    print(f"Local trigger candidates for Asia/Shanghai 09:00: {local_times}")
    if not origin_url:
        print("Warning: no git origin remote found. Daily pushes will fail until origin is configured.")
    print("Rerun this script if the repository path or system timezone changes.")


if __name__ == "__main__":
    main()
