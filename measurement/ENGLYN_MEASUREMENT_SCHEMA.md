# Englyn Measurement Schema

**Workstream D — Measurement.** How Englyn (Englyn) USE
and impact get measured: tagging → analytics → ML. This extends the site's
existing accessibility telemetry and the existing `analytics/` pipeline — it
does not replace or duplicate either. Read those two things first if you
haven't:

- `../../site/src/layouts/Base.astro` — the live `accessibility_telemetry`
  Umami event (4 aggregate flags) + skip-link listener, already shipping.
- `../../site/src/pages/essays/[...slug].astro` — the live `scroll_75` /
  `scroll_100` engagement events.
- `../../analytics/` — the live SUAVE-loop pipeline (`db.py`, `sync.py`,
  `report.py`, `evolve.py`) writing to the W+W analytics database (`backlog.db`;
  deployment-local path).
  `OPERATIONS_GUIDE.md` and `CLAUDE.md` in that directory are the privacy and
  schema ground truth this document extends.

**Privacy boundary — inherited, not relitigated.** Aggregate, non-identifying,
non-fingerprinting. Cookieless. No individual-level assistive-tech profiling,
ever, even where technically possible. Screen-reader use is inferred only
from the same coarse, aggregate signals already live in production
(`prefers-reduced-motion`, `prefers-contrast`, `forced-colors`, skip-link
activation) — never from covert detection (user-agent AT sniffing, timing
fingerprints, speech-rate profiling, or any other side channel). This
boundary is load-bearing: it's the exact kind of surveillance the brand
exists to reject. See §1.3 for the explicit in-bounds/out-of-bounds table.

---

## 1. Tagging layer — from `data-englyn-*` attributes to events

### 1.1 The two tag families and how they relate

Two independent tagging systems meet at the event layer:

1. **`data-englyn-*` attributes** — static, build-time metadata on DOM elements.
   **`spec/VOCABULARY.md` is the normative source** for the attribute set, its
   value enums, and its obligation levels; this document is derivative.
   The seven normative attributes are `data-englyn-primitive`,
   `data-englyn-consequence`, `data-englyn-receipt`, `data-englyn-role`,
   `data-englyn-priority`, `data-englyn-source` and `data-englyn-consumer`.
   These declare *what a region means*. They don't emit telemetry by themselves.

   > **Corrected 2026-08-18.** This list previously named `data-englyn-confidence`
   > and `data-englyn-severity` as live attributes and omitted `role`, `priority`
   > and `consumer`. `confidence` and `severity` have **zero instances** in the
   > reference implementation and are now **reserved, not specified** — the
   > schema columns below that aggregate them will therefore read zero, and that
   > zero is a *measured* zero, not a missing measurement.
2. **Media-query / interaction flags** (already live in `Base.astro`) —
   runtime, aggregate signals about how the page is being consumed:
   `prefers-reduced-motion`, `prefers-contrast`, `forced-colors`, skip-link
   use, scroll depth.

The measurement layer's job is narrow: **when a tagged region is genuinely
interacted with, or a page-level preference signal fires, emit an aggregate
Umami event.** No new client-side identity, no new storage on the client, no
correlation across events beyond what Umami's own cookieless session hashing
already does for existing events.

### 1.2 Event taxonomy

All events extend the existing `accessibility_telemetry` model: same
transport (`window.umami.track`), same `onUmamiReady` polling pattern
(`site/src/lib/umami-client.ts`), same one-shot-per-page-load discipline
where applicable.

| Event name | Status | Fires when | Properties | Aggregate-safe? |
|---|---|---|---|---|
| `accessibility_telemetry` | **Existing** | Once per page-load, plus once on skip-link click | `reduced_motion`, `high_contrast`, `forced_colors` (`active`/`inactive`), `skip_link` (`true`/`false`) | Yes — shipped, unchanged |
| `scroll_75` / `scroll_100` | **Existing** | Essay scroll-depth thresholds crossed | `slug` | Yes — shipped, unchanged |
| `englyn_narration_region` | **New** | A region carrying `data-englyn-primitive="perceive"` and marked as a narration/summary surface (chart summary, AI-disclosure label, action-consequence text) enters the viewport or receives focus | `region_type` (`chart_summary` \| `ai_disclosure` \| `action_consequence`), `state` (`rendered` \| `expanded`), `slug` | Yes — no user identity, one-shot per region per page-load |
| `englyn_keyboard_nav` | **New** | First `Tab` keydown detected on a page (one-shot per page-load, same pattern as skip-link) | `depth_bucket` (`shallow` \| `moderate` \| `deep` — bucketed Tab-press count at time of page unload, never a raw count) | Yes — bucketed, not raw, no per-user history |
| `englyn_action_tier` | **New** | A control carrying `data-englyn-primitive="act"` and an action-safety tier (see implementation guide §"Action-safety tiers") is activated | `tier` (`t1` \| `t2` \| `hotl` \| `t3`), `primitive` (always `act` today, room for co-tagged primitives later) | Yes — action-class only, no payload content |

**Design rule:** every new event is a one-shot-per-page-load boolean or a
bucketed enum, never a raw count, timestamp, or free-text payload. That's
what keeps the aggregate story true under Umami's own cookieless session
model — a raw Tab-press count or a millisecond timing value starts to look
like a behavioral fingerprint even without a cookie.

### 1.3 What's measurable vs. what's out of bounds

| In bounds (aggregate-safe) | Out of bounds (never build) |
|---|---|
| Media-query preference flags (`prefers-reduced-motion`, `prefers-contrast`, `forced-colors`) | User-agent or API sniffing for a specific screen reader (JAWS/NVDA/VoiceOver/TalkBack signatures) |
| Skip-link activation (boolean) | Persistent per-user assistive-tech profile, cookie, or fingerprint of any kind |
| Scroll-depth thresholds (bucketed: 75%/100%) | Raw scroll event streams, mouse/pointer telemetry, or timing-based interaction fingerprints |
| Narration-region view/expand (one-shot boolean per region) | Speech-rate or dwell-time profiling used to infer AT use |
| Keyboard-nav depth (bucketed enum) | Raw keystroke logging, raw Tab-press counts, or any keystroke content |
| Action-tier interaction class (`t1`/`t2`/`hotl`/`t3`) | Logging the actual action payload, target, or outcome content |
| Site-wide or per-page aggregate rollups (this schema, §2) | Any cross-event join keyed on IP, device ID, or Umami's internal visitor hash exposed outside Umami's own dashboard |

If a proposed metric requires correlating two or more of these signals for
the *same identifiable visitor* to be useful, it's out of bounds — the value
has to survive being computed from aggregate counts alone.

---

## 2. Analytics schema (SQLite)

### 2.1 Relationship to the existing `backlog.db`

The existing pipeline (`analytics/db.py`) owns four tables in the shared
W+W analytics database (`backlog.db`; deployment-local path): `posted`,
`metrics_snapshots`, `geo_citations`, `evolve_decisions`. This schema adds
**four new tables, all `englyn_`-prefixed (§4.1)**,
in the same database, following
the same conventions (`INTEGER PRIMARY KEY AUTOINCREMENT`,
`TIMESTAMP DEFAULT CURRENT_TIMESTAMP`, `CREATE TABLE IF NOT EXISTS`). No
existing table is touched, renamed, or altered. Full DDL: `englyn_schema.sql`
in this directory.

**This is proposed schema, not wired into `db.py` yet.** `db.py::bootstrap`
does not currently execute it — that's a deliberate, small follow-up
(`conn.executescript` the Englyn schema alongside the existing `SCHEMA`
constant) left for whoever builds the first writer for these tables, so the wiring
lands with a real consumer instead of speculatively.

### 2.2 Table design

**`englyn_events`** — aggregate event counts, pulled periodically from Umami's
event-breakdown API (the same shape `sync.py` already pulls for
`metrics_snapshots`, scoped to the new Englyn event names). One row per
`(date, event_name, property_name, property_value, page_path)` tuple —
never a per-visitor row. This is the append-only ingest table.

**`englyn_daily_rollup`** — derived, one row per `(date, page_path)`, computed
from `englyn_events` plus the existing `accessibility_telemetry` counts. This
is the table a report generator reads — it's the "session denominator
already applied" view (rates, not raw counts), analogous to what
`report.py::compute_post_cmf` does for content-market-fit today.

**`englyn_page_inventory`** — static, build-time. Not telemetry at all: a
scan of which pages/components carry `data-englyn-*` coverage, how much, and
of what kind. This is the denominator for a compliance score — you can't
say "80% of interactions with rated actions were confirmable" without
knowing how many actions on the page were tagged at all.

**`englyn_reports`** — one row per generated Accessibility Transparency Report
(§4), pointing at the corpus file and holding a small `summary_json` for
report-to-report diffing without re-parsing markdown.

Full DDL: see `englyn_schema.sql`.

---

## 3. ML / feature schema — schema only, model TBD

**Honesty check, stated plainly: no model exists yet. Nothing below is a
trained model, a validated feature, or a claimed prediction. This is the
feature-vector shape a future model would consume, so that today's schema
doesn't have to be redesigned when that work starts.**

### 3.1 Per-page Englyn-compliance feature vector

Derived from `englyn_page_inventory` joined with `englyn_daily_rollup`:

```
{
  page_path: string,
  data_englyn_primitive_count: int,       # from englyn_page_inventory
  tag_coverage: {                       # booleans, from englyn_page_inventory
    confidence: bool, severity: bool, consequence: bool,
    source: bool, receipt: bool
  },
  narration_region_count: int,
  narration_engagement_rate: float,     # englyn_daily_rollup.narration_region_views / sessions
  keyboard_nav_rate: float,             # share of sessions emitting englyn_keyboard_nav
  action_tier_mix: { t1: int, t2: int, hotl: int, t3: int },
  compliance_score: float | null        # placeholder column, scoring method not yet defined
}
```

`compliance_score` exists as a column today (`englyn_page_inventory.compliance_score`)
so downstream consumers have a stable field to read once a scoring method is
chosen. It is `NULL` until that method exists — never a fabricated or
placeholder-nonzero value.

### 3.2 Narration-quality signal (proxy, not ground truth)

`englyn_narration_region` view/expand ratio, segmented by `region_type`, is the
only currently-collectible proxy for "did the narration surface actually get
used." It's a proxy, not a quality measure — high engagement could mean the
narration is useful, or that the default UI forces a click to reveal content
that should have been visible by default. Any future model treating this as
a positive-quality label needs a second signal (e.g., a direct feedback
mechanism) before treating engagement as endorsement.

### 3.3 Aggregate accessibility-audience share trends

Time series of `englyn_daily_rollup.{reduced_motion_share, high_contrast_share,
forced_colors_share}` over time, at the site level. This is the input to
the population-context comparison in the Transparency Report (§4) — trend
direction and magnitude, not individual attribution.

### 3.4 Engagement-by-modality

`scroll_75` / `scroll_100` completion rate, segmented by whether
`accessibility_telemetry` reported `reduced_motion: active` or
`high_contrast: active` on the same page-load. This answers "does content
still land for the aggregate audience segment that has these preferences
active" without ever knowing who that audience is individually. Segmenting
by an aggregate flag that's already collected is safe; segmenting by
anything not already in this schema is not, by construction, since nothing
else identifying is collected.

---

## 4. Data-gathering repositories

### 4.1 Where the data lives

| Repository | Contents | Access pattern |
|---|---|---|
| Umami Cloud | Raw event stream, cookieless session hashing, Umami's own aggregate dashboards | Source of truth for §2.1 `englyn_events` ingest; queried via Umami's API, same credential path `sync.py` already uses (`UMAMI_API_KEY`, `UMAMI_WEBSITE_ID`) |
| W+W analytics database (`backlog.db`, deployment-local path) | `englyn_events`, `englyn_daily_rollup`, `englyn_page_inventory`, `englyn_reports` (this schema) alongside the existing four tables | Read/write via a future `englyn_sync.py` / `englyn_report.py` pair, mirroring `sync.py` / `report.py` |
| `products/wax-and-wires/analytics/englyn_reports/` | Generated Transparency Report artifacts (markdown + optional HTML), analogous to `dashboard.md` / `dashboard.html` sitting beside the pipeline that produces them | Written by a future report generator; read by humans and indexed by `englyn_reports` rows |
| `products/wax-and-wires/englyn/measurement/` (this directory) | The schema and template themselves — the contract, not the data | Static, versioned in git |

**Naming note:** the generated report *corpus* (`englyn_reports/`, plural
directory of dated artifacts) lives next to `analytics/dashboard.md` because
that's where the existing pipeline already puts its periodic generated
output — consistent with `OPERATIONS_GUIDE.md`'s "single pane" convention.
The report *template* (this package's deliverable) lives here in
`englyn/measurement/`. The corpus directory exists and holds two artifacts from
the 2026-07-30 baseline run; the generator that indexes them into
`englyn_reports` rows does not exist yet.

### 4.2 Generating an Accessibility Transparency Report from aggregate data

The report (template: `ENGLYN_TRANSPARENCY_REPORT_TEMPLATE.md`) is generated,
not hand-written, once the pipeline exists:

1. Pull the reporting period's rows from `englyn_daily_rollup` (rates, already
   session-normalized — no raw counts needed for the public-facing numbers).
2. Pull `englyn_page_inventory`'s latest scan for the tag-coverage snapshot.
3. Compute period-over-period deltas against the prior `englyn_reports` row's
   `summary_json`.
4. Render into the template, fill the population-context section with the
   current WebAIM Screen Reader User Survey citation (§4.3) — never
   fabricated, always cited to the actual published survey edition in use.
5. Write the markdown (and optionally HTML) artifact to `englyn_reports/`,
   insert the `englyn_reports` row pointing at it.

This is the Englyn-thesis proof point in practice: *"our stuff reaches the
population it claims to serve"* is a claim that only survives contact with
real, aggregate, honestly-caveated numbers — not a marketing assertion.

### 4.3 Population-context priors

The Transparency Report contextualizes W+W's own aggregate flags (e.g. what
share of sessions have `prefers-reduced-motion` or `prefers-contrast`
active) against **published, external population data** — principally
WebAIM's periodic **Screen Reader User Survey** (webaim.org /
screenreadersurvey.com), a long-running, well-cited public survey of
assistive-technology users' browser/AT pairings, preferences, and reported
satisfaction. W+W's own telemetry cannot and does not claim to measure
screen-reader usage directly (§1.3) — the survey is cited as an external
prior to give readers a sense of scale for the aggregate signals W+W *can*
collect, not as a claim that W+W's numbers are drawn from the same
population or method. Every citation in the report names the specific
survey edition/year used; stale citations are corrected, not left ambiguous.

### 4.4 k-anonymity discipline

Any breakdown fine enough to risk re-identifying a small population (e.g.
`forced_colors: active` sessions on a low-traffic page, in a single day) is
suppressed below a minimum cell size (proposed floor: 10 sessions) before
publication in a report or dashboard. `englyn_daily_rollup` may store the raw
small-cell row for internal trend continuity; the *report generator* is
responsible for applying the suppression floor before anything reaches
`englyn_reports/`. This is standard aggregate-statistics practice and is the
concrete mechanism behind the "aggregate, non-identifying" privacy rule —
not just a policy statement but an enforced floor at publication time.

---

## 5. Summary — what's built vs. proposed today

| Layer | State |
|---|---|
| `accessibility_telemetry`, `scroll_75`/`scroll_100` events | **Live in production** (`Base.astro`, essay page) |
| `englyn_narration_region`, `englyn_keyboard_nav`, `englyn_action_tier` events | **Proposed** — taxonomy defined (§1.2), not yet instrumented in any `.astro` component |
| `englyn_events`, `englyn_daily_rollup`, `englyn_page_inventory`, `englyn_reports` tables | **Proposed DDL**, verified to apply cleanly to a fresh SQLite DB (`englyn_schema.sql`), not yet wired into `db.py::bootstrap` |
| ML feature schema (§3) | **Schema only** — no model, no training data, no claimed accuracy |
| Transparency Report generator | **Not built** — template exists (`ENGLYN_TRANSPARENCY_REPORT_TEMPLATE.md`), no `englyn_report.py` yet |

Nothing in this document claims a capability that isn't either already
shipping or explicitly marked proposed/schema-only.
