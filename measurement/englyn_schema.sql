-- Englyn measurement schema — companion DDL for ENGLYN_MEASUREMENT_SCHEMA.md §2.
--
-- Four new tables, all `englyn_`-prefixed (the report-corpus naming decision
-- was made 2026-08-17: `englyn_reports` -> `englyn_reports`, zero rows and
-- therefore zero migration — the DDL had never been applied) —
-- in the SAME database as the existing
-- W+W analytics database (`backlog.db`; deployment-local path,
-- see the analytics pipeline's db.py::SCHEMA). Follows that file's
-- conventions verbatim: INTEGER PRIMARY KEY AUTOINCREMENT, TIMESTAMP
-- DEFAULT CURRENT_TIMESTAMP, CREATE TABLE IF NOT EXISTS. No existing
-- table is touched, renamed, or altered.
--
-- STATUS: proposed schema, not yet wired into db.py::bootstrap. Applying
-- this file to a fresh DB is safe and idempotent (IF NOT EXISTS) — wiring
-- it into the live pipeline is a deliberate follow-up left for whoever
-- builds the first writer for these tables (see ENGLYN_MEASUREMENT_SCHEMA.md §2.1).
--
-- Verify it applies cleanly:
--   sqlite3 /tmp/englyn_verify.db < englyn_schema.sql && sqlite3 /tmp/englyn_verify.db '.tables'

-- englyn_events — append-only ingest table. One row per
-- (date, event_name, property_name, property_value, page_path) tuple,
-- pulled periodically from Umami's event-breakdown API. NEVER a
-- per-visitor row — see ENGLYN_MEASUREMENT_SCHEMA.md §1.3 for what's out of
-- bounds.
CREATE TABLE IF NOT EXISTS englyn_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,                    -- ISO date (YYYY-MM-DD), the reporting day
    event_name TEXT NOT NULL,              -- e.g. accessibility_telemetry, englyn_narration_region
    property_name TEXT,                    -- e.g. region_type, tier, depth_bucket
    property_value TEXT,                   -- e.g. chart_summary, t2, moderate
    page_path TEXT,                        -- site-relative path the event fired on
    event_count INTEGER NOT NULL DEFAULT 0,-- aggregate count for this tuple on this date
    pulled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (date, event_name, property_name, property_value, page_path)
);

-- englyn_daily_rollup — derived, one row per (date, page_path). Rates, not
-- raw counts — the "session denominator already applied" view a report
-- generator reads, analogous to report.py::compute_post_cmf today.
CREATE TABLE IF NOT EXISTS englyn_daily_rollup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    page_path TEXT NOT NULL,
    sessions INTEGER NOT NULL DEFAULT 0,
    reduced_motion_share REAL,             -- share of sessions with prefers-reduced-motion active
    high_contrast_share REAL,              -- share of sessions with prefers-contrast active
    forced_colors_share REAL,              -- share of sessions with forced-colors active
    skip_link_rate REAL,                   -- share of sessions that activated the skip link
    narration_region_view_rate REAL,       -- englyn_narration_region views / sessions
    keyboard_nav_rate REAL,                -- share of sessions emitting englyn_keyboard_nav
    action_tier_t1_count INTEGER DEFAULT 0,
    action_tier_t2_count INTEGER DEFAULT 0,
    action_tier_hotl_count INTEGER DEFAULT 0,
    action_tier_t3_count INTEGER DEFAULT 0,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (date, page_path)
);

-- englyn_page_inventory — static, build-time scan. Not telemetry: which
-- pages/components carry data-englyn-* coverage, how much, and of what kind.
-- The denominator for a compliance score (ENGLYN_MEASUREMENT_SCHEMA.md §3.1).
CREATE TABLE IF NOT EXISTS englyn_page_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_path TEXT NOT NULL,
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_englyn_primitive_count INTEGER DEFAULT 0,
    has_confidence_tags INTEGER NOT NULL DEFAULT 0,   -- boolean: 0 or 1
    has_severity_tags INTEGER NOT NULL DEFAULT 0,
    has_consequence_tags INTEGER NOT NULL DEFAULT 0,
    has_source_tags INTEGER NOT NULL DEFAULT 0,
    has_receipt_tags INTEGER NOT NULL DEFAULT 0,
    narration_region_count INTEGER DEFAULT 0,
    action_count INTEGER DEFAULT 0,
    compliance_score REAL,                 -- NULL until a scoring method exists — never fabricated
    UNIQUE (page_path, scanned_at)
);

-- englyn_reports — one row per generated Accessibility Transparency Report
-- (ENGLYN_TRANSPARENCY_REPORT_TEMPLATE.md). Points at the corpus file and
-- holds a small summary for report-to-report diffing without re-parsing
-- markdown.
CREATE TABLE IF NOT EXISTS englyn_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    period_start TEXT NOT NULL,            -- ISO date, reporting period start
    period_end TEXT NOT NULL,              -- ISO date, reporting period end
    report_path TEXT NOT NULL,             -- path under analytics/englyn_reports/
    summary_json TEXT,                     -- small rollup for diffing, not the full report body
    UNIQUE (period_start, period_end)
);
