#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


PATTERNS = [
    ("private_key", re.compile(r"BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY")),
    ("bearer_token", re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}")),
    ("wecom_webhook", re.compile(r"qyapi\.weixin\.qq\.com/cgi-bin/webhook/send\?key=[0-9a-fA-F-]{20,}")),
    ("cookie_auth_token", re.compile(r"\b(auth_token|ct0|sessionid)\b\s*[:=]\s*['\"][^'\"]{12,}['\"]", re.I)),
    ("github_token", re.compile(r"\b(ghp|github_pat)_[A-Za-z0-9_]{20,}")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]
SKIP_DIRS = {".git", ".codex-run", "__pycache__"}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def git_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")
    return [root / line for line in result.stdout.splitlines() if line.strip()]


def all_scan_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        paths.append(path)
    return paths


def scan_file(path: Path) -> list[tuple[str, int]]:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    findings: list[tuple[str, int]] = []
    for name, pattern in PATTERNS:
        for match in pattern.finditer(content):
            line_no = content.count("\n", 0, match.start()) + 1
            findings.append((name, line_no))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan repository files for committed secret-like values.")
    parser.add_argument("--all", action="store_true", help="Scan all non-ignored workspace files, not only git-tracked files")
    args = parser.parse_args()
    root = repo_root()
    paths = all_scan_files(root) if args.all else git_files(root)
    failures: list[str] = []
    for path in paths:
        for name, line_no in scan_file(path):
            rel = path.relative_to(root)
            failures.append(f"{rel}:{line_no}: {name}")
    if failures:
        print("Potential secrets found:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"secret_scan=ok files={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
