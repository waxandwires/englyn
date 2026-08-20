# Englyn Accessibility Transparency Report — Template

**Purpose.** A periodic, public report answering one question honestly:
*does W+W's Englyn work actually reach the population it claims to serve?*
Generated from aggregate data per `ENGLYN_MEASUREMENT_SCHEMA.md` §4.2 — never
hand-assembled, never rounded up, never citing a number the pipeline
didn't produce. This file is the template a future `englyn_report.py`
renders into; until that generator exists, it's also a manual worksheet.

Every `[bracketed]` field is filled at generation time from
`englyn_daily_rollup`, `englyn_page_inventory`, or the prior `englyn_reports` row.
An empty or "not yet measured" field is preferable to a fabricated one —
see the Methodology section's honesty rule.

---

## Accessibility Transparency Report — [Period Start] to [Period End]

**Published:** [publication date] · **Report ID:** `englyn_reports.id = [id]`
**Prior report:** [link to previous report, or "first report — no prior period"]

---

### 1. Summary

[2–3 sentence plain-language summary: what changed this period, in which
direction, generated from the period-over-period deltas against the prior
`englyn_reports.summary_json` row — ENGLYN_MEASUREMENT_SCHEMA.md §4.2 step 3.]

---

### 2. Aggregate accessibility-preference signals

What share of sessions on wax­andwires.com had each preference flag
active this period, compared to the prior period. Source:
`englyn_daily_rollup.{reduced_motion_share, high_contrast_share,
forced_colors_share}`, site-wide average across the reporting period.

| Signal | This period | Prior period | Change |
|---|---|---|---|
| `prefers-reduced-motion` active | [X]% | [Y]% | [+/-Z pp] |
| `prefers-contrast` active | [X]% | [Y]% | [+/-Z pp] |
| `forced-colors` active | [X]% | [Y]% | [+/-Z pp] |
| Skip-link activation rate | [X]% | [Y]% | [+/-Z pp] |

**What this does and does not show.** These are media-query preference
flags — real signals from real browser/OS settings, aggregated across all
sessions. They are not a headcount of screen reader users, low-vision
users, or any other specific population; a sighted user with motion
sensitivity and a screen reader user both set `prefers-reduced-motion`,
and W+W's telemetry cannot and does not distinguish between them. See §5.

---

### 3. Englyn surface coverage

What share of pages on the site actually carry Englyn tagging, from the
latest `englyn_page_inventory` scan.

| Metric | Value |
|---|---|
| Pages scanned | [N] |
| Pages with any `data-englyn-*` coverage | [N] ([X]%) |
| Pages with a Rule 7 narration section | [N] ([X]%) |
| Pages with `data-englyn-consequence` on every T2/T3 action | [N] ([X]%) |
| Pages with a recorded Rule-10(b) read-aloud pass on file | [N] ([X]%) |

**Narration-gate pass rate** (from `ENGLYN_TESTING_PROTOCOL.md` §L6): [X]%
of shipped Englyn surfaces this period have a recorded manual read-aloud test
on file. This is a process metric — it tells readers whether the manual
gate is actually being run, not skipped under deadline pressure.

---

### 4. Engagement by aggregate preference segment

Does content still land for the aggregate audience segment that has an
accessibility preference active — without ever knowing who that audience
is individually. Source: `scroll_75`/`scroll_100` completion rate,
segmented by whether `accessibility_telemetry` reported the flag active on
the same page-load (ENGLYN_MEASUREMENT_SCHEMA.md §3.4).

| Segment | Scroll-75 completion | Scroll-100 completion |
|---|---|---|
| `reduced_motion: active` | [X]% | [Y]% |
| `reduced_motion: inactive` | [X]% | [Y]% |
| `high_contrast: active` | [X]% | [Y]% |
| `high_contrast: inactive` | [X]% | [Y]% |

A gap here (active segment completing meaningfully less often) is a
finding, not a footnote — it means the aggregate-preference audience is
having a worse experience, and that gets called out in §1, not buried.

---

### 5. Methodology

**What was measured, in plain terms.** Aggregate, cookieless event counts
from Umami, rolled up by page and day, joined against a static scan of
which pages carry Englyn tagging. No individual session was read, replayed,
or profiled to produce this report.

**What was NOT measured, and why.** W+W does not detect, infer, or record
which specific screen reader, browser, or assistive technology any visitor
uses. No user-agent AT sniffing, no timing fingerprints, no speech-rate or
dwell-time profiling — see `ENGLYN_MEASUREMENT_SCHEMA.md` §1.3 for the full
in-bounds/out-of-bounds table. Every number in this report is a
population-level count or rate, never an individual attribution.

**Suppression floor.** Any breakdown fine enough to risk re-identifying a
small population (fewer than 10 sessions in a cell) is suppressed before
publication, per `ENGLYN_MEASUREMENT_SCHEMA.md` §4.4. If a table above omits
a row or shows "suppressed — n < 10" instead of a number, that's this rule
in effect, not an oversight.

**Population-context citation.** Where this report compares W+W's own
aggregate flags against a sense of scale for the broader
assistive-technology-using population, it cites [WebAIM Screen Reader
User Survey — cite the specific edition/year used, e.g. "20XX round,
webaim.org/projects/screenreadersurvey"]. This is an external prior for
context, not a claim that W+W's numbers are drawn from the same
population or method — see `ENGLYN_MEASUREMENT_SCHEMA.md` §4.3.

**Honesty rule.** If a metric in this template has no data yet (new
event, insufficient period, pipeline not yet wired), the field says so
explicitly — "not yet instrumented" or "insufficient data (n < 10)" —
rather than being omitted silently or filled with a placeholder number.
Nothing in this report claims a capability that isn't either already
shipping or explicitly marked proposed/schema-only, matching the rule
`ENGLYN_MEASUREMENT_SCHEMA.md` itself holds to.

---

### 6. Privacy statement

W+W collects aggregate, non-identifying, cookieless accessibility
telemetry only. No individual is profiled, tracked across sessions by
identity, or fingerprinted by device, timing, or assistive-technology
signature. Preference signals (`prefers-reduced-motion`,
`prefers-contrast`, `forced-colors`) are read the same way a browser
already exposes them to any page's CSS — W+W's telemetry adds aggregation
and reporting on top, never new client-side identity or storage. This
boundary is not a compliance minimum; it's the same conviction the rest
of W+W's work stands on — the exact kind of surveillance this brand exists
to reject. Full privacy boundary and rationale:
`ENGLYN_MEASUREMENT_SCHEMA.md` §"Privacy boundary."

---

### 7. Feedback

[Contact path for someone — especially an assistive-technology user — to
report a gap this report's aggregate numbers can't see. "Nothing about us
without us" applies to measurement too: aggregate telemetry tells W+W
*whether* something is working at scale, not *why* it fails for one
person. That second half needs a human channel, not a dashboard.]

---

*Generated from `englyn_daily_rollup`, `englyn_page_inventory`, and the prior
`englyn_reports` row per `ENGLYN_MEASUREMENT_SCHEMA.md` §4.2. Template version:
this file. Report corpus: `products/wax-and-wires/analytics/englyn_reports/`.*
