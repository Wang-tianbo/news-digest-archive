#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from signal_inbox import (
    DEFAULT_CANDIDATE_DIR,
    DEFAULT_CONFIG_PATH,
    DEFAULT_DB_PATH,
    DEFAULT_MANUAL_DIR,
    Source,
    candidate_from_item,
    collect_source,
    connect_db,
    ensure_codex_run_ignored,
    ensure_under_codex_run,
    export_candidates_jsonl,
    insert_candidate,
    insert_raw_item,
    iso_now,
    load_manual_items,
    load_sources,
    main_error,
    parse_report_date,
    print_table,
    refresh_source_profiles,
    record_source_check,
    repo_root,
    upsert_source,
)


def manual_source() -> Source:
    return Source(
        source_id="manual_public_links",
        name="Manual Public Links",
        platform="manual",
        source_role="community",
        source_tier="public",
        source_type="manual_jsonl",
        url="https://example.com/manual-public-links",
        section_hint="AI 圈博主",
        item_type="信息线索",
        run_mode="manual",
        health_status="active",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect public AI signal candidates into the local inbox.")
    parser.add_argument("--date", help="Report date in YYYY-MM-DD; defaults to current Asia/Shanghai date")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Source registry YAML path")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite path under .codex-run/")
    parser.add_argument("--limit-per-source", type=int, default=15, help="Maximum feed items per source")
    parser.add_argument("--dry-run", action="store_true", help="Validate and list eligible public sources only")
    parser.add_argument(
        "--manual-jsonl",
        help="Optional manual public-link JSONL under .codex-run; defaults to the report date manual file",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repo_root()
    report_day = parse_report_date(args.date)
    config_path = (root / args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config)
    sources = load_sources(config_path)
    eligible = [source for source in sources if source.source_tier == "public"]
    skipped = [source for source in sources if source.source_tier != "public"]

    if args.dry_run:
        print(f"Report date: {report_day:%Y-%m-%d}")
        print(f"Config: {config_path}")
        print(f"Eligible public sources: {len(eligible)}")
        print_table([(source.source_id, f"{source.source_type} {source.url}") for source in eligible])
        if skipped:
            print(f"Skipped non-public sources: {len(skipped)}")
            print_table([(source.source_id, source.source_tier) for source in skipped])
        return 0

    ensure_codex_run_ignored(root)
    db_path = ensure_under_codex_run(Path(args.db), root)
    export_path = ensure_under_codex_run(
        DEFAULT_CANDIDATE_DIR / f"{report_day:%Y-%m-%d}.jsonl",
        root,
    )
    if args.manual_jsonl:
        manual_path = ensure_under_codex_run(Path(args.manual_jsonl), root)
    else:
        manual_path = ensure_under_codex_run(
            DEFAULT_MANUAL_DIR / f"{report_day:%Y-%m-%d}.jsonl",
            root,
        )

    run_id = f"collect-{report_day:%Y-%m-%d}-{iso_now()}"
    collected_at = iso_now()
    inserted = 0
    checked = 0

    conn = connect_db(db_path)
    try:
        for source in sources:
            upsert_source(conn, source, collected_at)
        upsert_source(conn, manual_source(), collected_at)

        for source in eligible:
            checked += 1
            checked_at = iso_now()
            try:
                items, status = collect_source(source, args.limit_per_source)
                note = status
            except Exception as exc:  # keep one flaky source from killing the run
                items = []
                status = "partial"
                note = f"{type(exc).__name__}: {exc}"
            for item in items:
                insert_raw_item(conn, source, item, collected_at)
                candidate = candidate_from_item(source, item, report_day, collected_at)
                if insert_candidate(conn, candidate):
                    inserted += 1
            record_source_check(conn, run_id, source.source_id, checked_at, status, len(items), note)

        manual_items = load_manual_items(manual_path, collected_at)
        if manual_items:
            source = manual_source()
            for item in manual_items:
                insert_raw_item(conn, source, item, collected_at)
                candidate = candidate_from_item(source, item, report_day, collected_at)
                if insert_candidate(conn, candidate):
                    inserted += 1
            record_source_check(
                conn,
                run_id,
                source.source_id,
                iso_now(),
                "hit",
                len(manual_items),
                f"loaded manual public links from {manual_path}",
            )

        exported = export_candidates_jsonl(conn, report_day, export_path)
        refresh_source_profiles(conn, iso_now())
        conn.commit()
    finally:
        conn.close()

    print(f"checked_sources={checked}")
    print(f"candidate_upserts={inserted}")
    print(f"exported_candidates={exported}")
    print(f"db={db_path}")
    print(f"jsonl={export_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(main_error(exc))
