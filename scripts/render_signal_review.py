#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from signal_inbox import (
    DEFAULT_DB_PATH,
    DEFAULT_REVIEW_DIR,
    connect_db,
    ensure_codex_run_ignored,
    ensure_under_codex_run,
    main_error,
    parse_report_date,
    render_review_markdown,
    repo_root,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render the daily AI signal candidate Markdown review.")
    parser.add_argument("--date", help="Report date in YYYY-MM-DD; defaults to current Asia/Shanghai date")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite path under .codex-run/")
    parser.add_argument("--limit", type=int, default=20, help="Maximum candidates in the review")
    parser.add_argument("--out", help="Output Markdown path under .codex-run/")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repo_root()
    report_day = parse_report_date(args.date)
    ensure_codex_run_ignored(root)
    db_path = ensure_under_codex_run(Path(args.db), root)
    if args.out:
        out_path = ensure_under_codex_run(Path(args.out), root)
    else:
        out_path = ensure_under_codex_run(
            DEFAULT_REVIEW_DIR / f"{report_day:%Y-%m-%d}.md",
            root,
        )

    conn = connect_db(db_path)
    try:
        markdown = render_review_markdown(conn, report_day, args.limit)
    finally:
        conn.close()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(f"review={out_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(main_error(exc))
