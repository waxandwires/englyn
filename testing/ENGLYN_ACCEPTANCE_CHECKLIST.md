# ENGLYN Acceptance Checklist

**The pre-publish gate.** Companion to `ENGLYN_TESTING_PROTOCOL.md` — that
document explains the six test layers (L1–L6) and why each exists; this
document is the runnable checklist an engineer works through before
shipping a new or materially-changed ENGLYN surface. Every box here maps back
to a specific layer or rule; none are invented fresh.

**Governing documents.** `../spec/VOCABULARY.md` is the single normative
source for every `data-englyn-*` attribute, its value enum, and its
obligation level — this checklist is derivative of it, not the other way
round. `../spec/TIERS.md` defines what **Bronze — structurally sound** and
**Silver — operable end to end** actually require. Where any item below
conflicts with either file, the governing document wins; this file is a
reconciled, runnable copy.

Run this top to bottom. Stop and fix on the first unchecked box in a
"blocks ship" section — don't batch failures for later.

---

## Verdicts

Every item below resolves to one of three verdicts, never two:
**CONFORMS**, **FAILS**, or **CANNOT-CHECK** (`../spec/TIERS.md` § Three
verdicts, never two).

A tier is awarded on CONFORMS across every layer that tier requires, per
`../spec/TIERS.md`. **A CANNOT-CHECK on any required layer means the tier is
not awarded — it does not mean the tier failed**, and a recorded result must
never report a CANNOT-CHECK as either a pass or a fail.

Record every result with the layer stamp it was earned at — `L-MARKUP`,
`L-AOM`, `L-AT`, or `L-HUMAN` (`../spec/TIERS.md` § The layer stamp). A stamp
names its scope inline when the scope is narrower than the stamp itself:
`L-AT (VoiceOver on macOS)`, never a bare `L-AT`. Record an L3 result as
`L-AOM: CONFORMS (axe, 30–50% coverage)`, never as "accessible."

## Tier map

This checklist's sections were written before the tier ladder existed. They
are not reorganized here — the existing section order and items are
preserved — but each is now labeled with the layer(s) it exercises and the
tier, if any, that layer gates under `../spec/TIERS.md`.

| Section | Layer(s) | Gates |
|---|---|---|
| 1. Reference checklist — Structure, items 1–2 | L1 | **Bronze — structurally sound** |
| 1. Reference checklist — Structure, item 3 (keyboard nav) | L4 | **Silver — operable end to end** (not Bronze — see note in-section) |
| 1. Reference checklist — Narration | L1 / L3 | **Bronze — structurally sound** |
| 1. Reference checklist — Agent layer | L2 | **Bronze — structurally sound** |
| 1. Reference checklist — Automated checks actually run | L1, L2, L3 (named explicitly) | **Bronze — structurally sound** |
| 2. Action-safety tier verification | none of L1–L4 | Gates **neither Bronze — structurally sound nor Silver — operable end to end** — a project ship gate, not a conformance-tier requirement |
| 3. Rule-10 read-aloud narration test | L5 | Gates **neither Bronze — structurally sound nor Silver — operable end to end** — L5 is the evidence a **Gold — verified by lived experience** claim would need, and that tier is a v0.2+ destination, not self-certifiable, and is not awarded by this checklist |
| 4. Church/State check | none | Not part of the L1–L6 ladder at all — W+W-package-specific |
| 5. Sign-off | references L6 | L6 is an **orthogonal "instrumented" badge** per `../spec/TIERS.md` — claimable at any tier, required at none |

---

## 0. Before you start

This section is prerequisite scoping, not itself a gated layer — it does not
map to L1–L6 and contributes to no tier.


- [ ] The surface has a name and a URL/path you can point a screen reader
      and `axe` at (staging, or a local build — not just source files).
- [ ] You know which action-safety tier(s) (T1 / T2 / T3 / Blocked, per
      `englyn-accessible-page/SKILL.md` Rule 5) apply to every interactive
      control on the surface. If you can't answer this in one sentence per
      control, stop and answer it before continuing — everything below
      assumes you already know.

---

## 1. Reference checklist (L1–L3, automatable — gates Bronze — structurally sound)

Pulled from `references/englyn-narration-reference.md`'s Pre-Publish
Checklist. Run the automated layers first — they're cheap and catch the
mechanical failures before you spend manual time on the same surface.

### Structure
- [ ] Exactly one `<h1>` and one `<main>`; landmarks named; no skipped
      heading levels. (L1)
- [ ] DOM/reading order matches priority order, independent of visual
      layout. (L1)
- [ ] Keyboard-only navigation works through all critical paths. **(L4 —
      this item gates Silver — operable end to end, not Bronze — structurally
      sound. It is listed here because it was already grouped with
      Structure; a Bronze claim does not require it, and skipping it anyway
      is still a defect against Silver.)**

### Narration (spoken layer)
- [ ] Every number/currency/percent in an `aria-label` keeps digits as
      digits — only units and suffixes are spelled (`$2.4M` →
      `2.4 million dollars`; `12%` → `12 percent`). No spelled-out spoken
      number form ("two point four") appears in an accessible name, and
      never sits beside the digits (Rule 1, revised 2026-08-17). Where a
      digit string is genuinely TTS-ambiguous (a year read as a quantity, a
      phone number), `scripts/spoken_number.py`'s output may appear in
      prose or `aria-describedby` — never in the accessible name itself.
- [ ] Every acronym/symbol in an `aria-label` is expanded per Rule 6 (and
      the domain child skill's terminology table, if one applies).
- [ ] Every decorative icon/symbol is `aria-hidden="true"` with meaning in
      the parent label.
- [ ] Color is not the sole carrier of any status or urgency.
- [ ] Card groups use `role="list"` / `role="listitem"`.
- [ ] Every chart has `role="img"`, a full `aria-label`, and a
      visually-hidden data table.
- [ ] Every alert/risk callout uses `role="alert"` and explains the
      condition in full (Rule 8).
- [ ] Rule 7 `.sr-only` narration section exists, current, opens with an
      sr-only `<h2>`, no `aria-live`, priority order.
- [ ] No focusable children inside `aria-hidden` regions
      (`tabindex="-1"` applied).

### Agent layer

Per `../spec/VOCABULARY.md`'s membership criterion: a conforming page MUST
NOT emit a `data-englyn-*` value outside the published enum, and a
conforming check MUST validate value **membership**, not merely attribute
**presence**. The items below are updated to say so explicitly.

- [ ] Every meaningful region carries `data-englyn-role`, with a value inside
      the published enum in `../spec/VOCABULARY.md` (`narration`, `section`,
      `action`, `status`, `alert`, `stat`, `card`, `chart`, `citations`,
      `run-out`).
- [ ] Every meaningful region carries `data-englyn-primitive`, with a value
      inside the published six-value closed enum in `../spec/VOCABULARY.md`
      (`perceive`, `act`, `announce`, `audit`, `interrupt`, `oversee`).
- [ ] AI-generated content carries `data-englyn-source`, with a value inside
      the published enum in `../spec/VOCABULARY.md` (`manual`, `llm-draft`,
      `research-pipeline`, `analytics`, `build-script`).
      **This item previously also required `AI-generated content carries
      data-englyn-source + data-englyn-confidence`.** `data-englyn-confidence`
      is now **reserved, not specified** in `../spec/VOCABULARY.md` — zero
      instances anywhere in the corpus, in source, build, or fixture. A
      checklist item requiring it was requiring something the specification
      does not define. It is removed from this item; a reserved attribute is
      not a conformance requirement and a checker MUST NOT fail a page for
      omitting it.
- [ ] External write actions carry `data-englyn-receipt` — free text, by
      declaration, a UUID or other durable identifier resolvable by the
      publisher (`../spec/VOCABULARY.md`).

### Automated checks actually run
- [ ] L1 lint (`eslint-plugin-jsx-a11y` and/or `html-validate`) passes.
- [ ] L2 schema validation passes (if the surface is schema/agent-composed),
      **validating `data-englyn-*` value membership against
      `../spec/VOCABULARY.md`, not merely field presence.**
- [ ] L3 `jest-axe` / `@axe-core/playwright` reports zero violations —
      see `axe-integration-example/` for the runnable pattern.

---

## 2. Action-safety tier verification (Rule 5 — blocks ship; gates neither Bronze nor Silver)

This section blocks ship as a project rule, independent of the conformance
ladder — it is not mapped to L1–L4, so a CONFORMS here does not count toward
**Bronze — structurally sound** or **Silver — operable end to end** under
`../spec/TIERS.md`. "Tier" in this section means the T1/T2/T3/Blocked
action-safety tier from `englyn-accessible-page/SKILL.md` Rule 5, a
different and unrelated use of the word from the Bronze/Silver/Gold
conformance tier.

For **every** interactive control on the surface, confirm all of these:

- [ ] The control's tier (T1 / T2 / T3 / Blocked) is correctly assigned —
      re-read Rule 5's table, don't assume the default is safe.
      (This is the 4-tier authoring view. The full governance model in
      `../implementation/ENGLYN_IMPLEMENTATION_GUIDE.md` adds **HOTL** — a
      strongly-governed, reversible auto-execute tier that sits between T2
      and T3. If a control auto-executes with undo, verify it against the
      HOTL row there, not just this simplified set.)
- [ ] T2 controls carry the label pattern "You will review the change
      before it saves" via `aria-describedby` → `.sr-only` span, AND
      `data-englyn-consequence`.
- [ ] T3 controls carry "You will review and edit the draft before it
      sends" — and the control structurally routes to a reviewed draft,
      never a direct send. Verify this by reading the code path, not just
      the label — a T3 label on a control that actually sends immediately
      is worse than no label at all.
- [ ] Blocked actions are structurally excluded from the UI, not just
      hidden or disabled-but-present (a disabled button is still in the
      accessibility tree and still readable as "a thing that exists").
- [ ] No control's visible text is the only place its consequence is
      stated — the consequence is also in the accessible name or
      description, per Rule 5.

---

## 3. Rule-10 read-aloud narration test (L5 gate — blocks ship; gates neither Bronze nor Silver)

L5 does not appear in the **Bronze — structurally sound** or **Silver —
operable end to end** requirement list in `../spec/TIERS.md` — only L1–L4
gate those two tiers. This section is the
evidence a **Gold — verified by lived experience** claim would need, but Gold
is a v0.2+ destination, is explicitly not self-certifiable by this project or
anyone, and is not awarded by this checklist. Running and recording this
section remains a hard ship gate for this project; it is a project-level
quality bar, not a conformance-tier claim.

This is the test static tools cannot run for you. Set a screen reader
running (VoiceOver on macOS is the fastest local option; see the AT
matrix in `ENGLYN_TESTING_PROTOCOL.md` §L5 for the full rotation) and
actually listen.

- [ ] Read every `aria-label` on the surface out loud, in order. Flag any
      that are a data dump instead of an interpretation (e.g. "green
      check" instead of "Deploy succeeded").
- [ ] Confirm no acronym or symbol is spoken letter-by-letter or glyph-by-
      glyph without expansion.
- [ ] Confirm no `aria-label` reads a spelled-out number ("two point four")
      beside its digits, or in place of them — digits stay digits, only
      units/suffixes are spoken. Spot-check at least 3 numeric labels
      against the source value.
- [ ] **The final gate, verbatim from Rule 10(b):** could someone who
      cannot see the page hear it and know what it is, what matters most,
      and what to do next? Answer yes/no explicitly — don't let this
      collapse into "mostly."
- [ ] Record the result per `ENGLYN_TESTING_PROTOCOL.md` §L5's pass/fail/notes
      table format, even for a "pass" — the record is what makes L6's
      "narration-gate pass rate" KPI real instead of assumed.

---

## 4. Church/State check (blocks ship, W+W package only; not part of the L1–L6 ladder)

- [ ] The excluded-term grep from `AAP_PACKAGE_PLAN.md`'s load-bearing
      ruling returns zero hits against every file the surface touches
      (markup, copy, sample data, skill references).

---

## 5. Sign-off

- [ ] All "blocks ship" boxes above are checked, or the exception is
      documented with a reason and a follow-up ticket (L5's table already
      has a place for this — use it, don't leave a silent gap).
- [ ] L6 KPIs (`ENGLYN_TESTING_PROTOCOL.md` §L6) are wired for this surface
      if the observability pipeline is live for it, or explicitly noted
      as "not yet instrumented" if not — never silently assumed. L6 is an
      orthogonal "instrumented" badge per `../spec/TIERS.md` — claimable at
      any tier, required at none; it does not gate this sign-off.
- [ ] If claiming **Bronze — structurally sound** or **Silver — operable end
      to end** for this surface, record the verdict (CONFORMS / FAILS /
      CANNOT-CHECK) and layer stamp for every layer that tier requires, per
      the Verdicts section above and `../spec/TIERS.md` § Self-assessment.
      Publish the run records alongside the claim, or the claim is
      unstamped. A CANNOT-CHECK on any required layer means the tier is not
      awarded, and no tier claim is made for this surface.

Ship only after every box in sections 1–4 is checked. Section 5 is the
record, not a substitute for the work. Shipping is a separate bar from a
tier claim: a surface can ship (sections 1–4 checked) without earning
**Bronze — structurally sound** — for example, if L2 schema validation is
CANNOT-CHECK because it has never been run, Bronze is not awarded even
though the rest of the checklist is clean. Ship-readiness and
conformance-tier are not the same question.
