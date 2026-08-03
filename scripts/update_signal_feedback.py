#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from signal_inbox import (
    DEFAULT_DB_PATH,
    DEFAULT_REVIEW_DIR,
    apply_feedback,
    connect_db,
    ensure_under_codex_run,
    iso_now,
    main_error,
    parse_feedback_blocks,
    parse_report_date,
    refresh_source_profiles,
    repo_root,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply edited signal review feedback to the local inbox.")
    parser.add_argument("--date", help="Report date in YYYY-MM-DD; defaults to current Asia/Shanghai date")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite path under .codex-run/")
    parser.add_argument("--review", help="Review Markdown path under .codex-run/")
    parser.add_argument("--dry-run", action="store_true", help="Parse and print planned updates without writing")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repo_root()
    report_day = parse_report_date(args.date)
    db_path = ensure_under_codex_run(Path(args.db), root)
    if args.review:
        review_path = ensure_under_codex_run(Path(args.review), root)
    else:
        review_path = ensure_under_codex_run(
            DEFAULT_REVIEW_DIR / f"{report_day:%Y-%m-%d}.md",
            root,
        )
    if not review_path.is_file():
        raise FileNotFoundError(f"review file not found: {review_path}")
    feedback = parse_feedback_blocks(review_path.read_text(encoding="utf-8"))
    if args.dry_run:
        print(f"review={review_path}")
        print(f"feedback_blocks={len(feedback)}")
        for item in feedback:
            print(
                f"{item['candidate_id']} status={item.get('status', '待审')} "
                f"retrospective={item.get('retrospective_status', '待验证')}"
            )
        return 0

    conn = connect_db(db_path)
    try:
        changed = apply_feedback(conn, feedback, iso_now())
        refresh_source_profiles(conn, iso_now())
        conn.commit()
    finally:
        conn.close()
    print(f"updated_candidates={changed}")
    print(f"db={db_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(main_error(exc))
