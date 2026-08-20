# TIERS

**What a conformance claim under this specification means, and what it does
not.** Two tiers are defined. One is declared and deliberately left undefined,
because the people who should define it have not been asked yet.

**Status:** created 2026-08-18. Applies to v0.1.0-draft. Normative.

---

## Why this file exists

`spec/UNVERIFIED.md:233-234` says publicly that *"Silver and Bronze are
self-assessable against the published checklist."* Until this file, **no
published document defined what any tier required.** The only definition lived
in a strategy document that the publication manifest denies.

A specification that publishes a conformance ladder and does not publish its
rungs is asking readers to self-assess against a checklist that does not name a
tier — which, measured, is exactly what
`testing/ENGLYN_ACCEPTANCE_CHECKLIST.md` did: **zero tier mentions.**

---

## The ladder

**Tier names never appear naked.** Always "Bronze — structurally sound", never
"Bronze". The reason is in *Why the names carry their qualifier*, below, and it
is not a style preference.

**Scope of that rule, stated because this file would otherwise break it.** It
governs every place a tier is **claimed about a surface** — a badge, a report, a
procurement answer, a README, a commit message, a checklist verdict. It does not
govern prose *inside this file*, where the qualifier is established by the table
above and repeating it in every clause would make the definitions unreadable.
The distinction is claim versus definition: a reader who meets "Bronze" in a
badge has no qualifier available, which is exactly the gap the rule closes; a
reader who meets it here has just read one.

| tier | requires | what the claim actually asserts |
|---|---|---|
| **Bronze — structurally sound** | L1 (static structure / semantic lint) + L2 (schema validation) + L3 (automated a11y, axe-core), **zero violations across all three** | A machine-verifiable claim **about testing**. It says three instruments ran and found nothing. It says nothing about whether anyone could use the thing. |
| **Silver — operable end to end** | Bronze, plus L4 (keyboard-flow) | The same kind of claim, one layer wider. Still a statement about instruments, not about people. |
| **Gold — verified by lived experience** | **A DESTINATION, not a specification. v0.2 or later.** Recorded assistive-technology verification with paid community participation. **Cannot be self-certified, by design.** | The only tier that claims a human found it usable. It does not exist yet, and no Gold claim exists — **including ours**. |

Layer definitions are in `testing/ENGLYN_TESTING_PROTOCOL.md`. Nothing in this
file redefines them.

### L6 is not part of Gold

This amends the earlier July mapping, which placed L6 inside Gold. Two reasons,
either sufficient:

1. **A layer with no verdict cannot gate a tier.** The testing protocol defines
   L6 as *"Continuous, dashboarded — No (alerts, doesn't block)"*. It is a
   dashboard. A dashboard has no pass state to require.
2. **Requiring it would lock out everyone without production telemetry.** A
   component library, a documentation site, a specification's own reference
   implementation — none of them have a production KPI stream, and none of them
   should be structurally barred from the top tier for it.

L6 becomes an **orthogonal badge — "instrumented"** — claimable at any tier,
required at none.

---

## Gold ships as an open invitation, not a specification

Gold is written here as **a call for collaborators to help define it**, and that
is deliberate.

The one objection an open validator cannot answer is benevolent-dictator
governance. Godot rejected OpenGEX partly on it. A standard whose author defines
every rule, including the rules governing the people it claims to serve, has no
answer to *"who decided that, and who could have disagreed?"*

Handing authorship of the tier that governs disabled reviewers **to disabled
reviewers** answers it directly. It is the strongest governance move available
to this project, and it costs nothing but the willingness to publish an
undefined tier.

**What Gold needs, from the people who will define it:**

- What "verified by lived experience" actually checks for on a real surface
- The assistive-technology matrix that constitutes a real record, rather than
  the one this project could reach
- What compensation makes the participation honest rather than extractive
- Whether the tier should exist at all in this shape

**Compensation.** Co-review begins as an open invitation on realistic footing:
unpaid, no date, no rate (`DEC-WW-ENGLYN-COREVIEW-001`). There is no money
coming in, so there is no money going out, and a funded promise made ahead of
funding is the defect this specification already had once. **Gold keeps its
paid-participation requirement, and Gold is the trigger that sets the rate** —
deferring it does not weaken the tier; it is what makes the requirement honest.

**What this project covers first-hand, and what it does not.** The
neurodivergent reading of the problem is direct experience — the case for
compressed text, variable length, and non-linear topology is written from inside
AuDHD experience. Agent-consumer needs are covered directly. **Screen-reader
experience is not.** That sentence is here because it tells a blind reviewer
exactly what they would bring that the author cannot.

---

## Why the names carry their qualifier

**Because axe passed while a screen reader said "U-S."**

Six confirmed instances across four pages of the reference implementation: text
rendered through a CSS `text-transform` uppercase rule, which WebKit hands to
the accessibility tree **already transformed**. `"What this buys us"` is spoken
*"What this buys U-S."* axe: 0 FAILS. html-validate: pass. The Englyn checker:
pass. The DOM: impeccable.

Four automated layers green, and the page says the wrong word out loud. And it
landed in the headings — the busiest channel there is, given that **71.6% of
screen-reader users navigate by heading**.

A bare tier name is that defect in badge form. "Bronze" alone reads as a
verdict on usability. "Bronze — structurally sound" reads as what it is: three
instruments ran and found nothing, which is a floor and not a certification.
The qualifier is the difference between a conformance claim and the P3P
Synthetic Compliance Trap.

---

## The layer stamp

Every verdict carries the layer it was earned at. A pass at one layer says
nothing about the layer above it, and claiming the lower while implying the
higher is the industry-standard lie this specification is trying to be
constitutionally incapable of telling.

| stamp | what was observed | earned by | what it still cannot tell you |
|---|---|---|---|
| **`L-MARKUP`** | the source HTML | L1, L2 | whether the browser built the node you expected |
| **`L-AOM`** | the browser accessibility tree | L3, L4, and any agent tester | whether the platform API received it, and whether any AT reads it that way |
| **`L-AT`** | one specific screen reader's output | L5, one pair at a time | whether any *other* assistive technology behaves the same |
| **`L-HUMAN`** | a person completing a task | paid co-review | nothing further — this is the terminal claim |

A stamp names its scope inline when the scope is narrower than the stamp:
`L-AT (VoiceOver on macOS)`, never a bare `L-AT`. Record an L3 result as
`L-AOM: CONFORMS (axe, 30–50% coverage)` — never as "accessible".

This definition is what `spec/UNVERIFIED.md:71` was already pointing at.

---

## The reference implementation's own tier

**UNKNOWN.**

Not Bronze. **MEASURED 2026-08-18** — receipts in
`../testing/LAYER-RUN-RECORD-2026-08-18.md`. This section previously said L2
and L4 had never run. **Both now exist and have run, and the verdict did not
improve; it acquired evidence.**

| layer | verdict | measured |
|---|---|---|
| L1 static lint | **FAILS** | 15 of 15 pages failing, 26 FAILS |
| L1 `html-validate` | **FAILS** | 20 errors |
| L2 schema | **FAILS** | 4 FAILS across 330 source annotations |
| L3 axe-core | **CANNOT-CHECK** | 0 FAILS, 29 incomplete, every page |
| L4 keyboard | **CANNOT-CHECK** | 0 site FAILS, 32 incomplete (171 checks, 138 CONFORMS) |

Bronze — structurally sound requires zero violations across L1+L2+L3: **none
of the three holds.** Silver — operable end to end requires Bronze plus L4:
**neither holds.** L5 has never run and no `L-AT` record exists.

**Nothing was tuned to reach a verdict.** Where an instrument asserted a
requirement this specification does not carry, it was downgraded to
CANNOT-CHECK with the observation preserved — never to CONFORMS — and the
requirement was written up for ruling rather than quietly adopted or quietly
dropped.

A tier this specification has not earned is not claimed. **A standard that
publishes its ladder and says "we have not climbed it yet" is doing the thing it
asks of everyone else** — and the alternative, publishing a ladder alongside a
self-awarded rung, is the reason nobody trusts self-certification.

`waxandwires.com` must hold **Silver — operable end to end** before this
specification publishes. That is a hard gate, and it is not met today.

---

## What a tier claim is not

- **Not a W3C claim.** Bronze / Silver / Gold are Englyn-defined and
  WCAG-3-inspired. The WCAG 3.0 Working Drafts have used, dropped, and re-used
  these names across 2021–2026; no W3C Recommendation is expected before roughly
  2028. If you report an Englyn tier to a customer, a procurement process, or a
  regulator, you are reporting this specification's tier and nothing else.
- **Not a mapping to WCAG 2.2 or EN 301 549.** None is claimed. That mapping
  waits until the layers have actually run — not before.
- **Not a coverage claim.** Automated checks cover the WCAG floor and,
  depending on methodology, 30–57% of WCAG issues. They cover **0 of the 10
  narration rules** in this specification. The part of Englyn that is not
  already WCAG has no machine check at all and cannot acquire one.

## Self-assessment

**Bronze and Silver are self-assessable** against `testing/ENGLYN_ACCEPTANCE_CHECKLIST.md`
and the layer records it requires. Publish the run records alongside the claim,
or the claim is unstamped.

**Gold is not self-assessable, by anyone, including this project.** It requires
verification the builder structurally cannot supply about their own work. A
self-declared Gold badge is not a conformance statement under this
specification, whoever issues it. If you see one, ask for the
assistive-technology record it rests on; **if there is no record, the correct
verdict is CANNOT-CHECK**, not a pass.

---

## Three verdicts, never two

CONFORMS · FAILS · **CANNOT-CHECK**.

### Two kinds of CANNOT-CHECK, and only one blocks a tier

**Ruled by Micah, 2026-08-19.** The earlier text said a CANNOT-CHECK on any
required layer means the tier is not awarded. That is right for one kind and wrong
for the other, and conflating them makes Bronze unreachable for reasons that have
nothing to do with accessibility.

**LAYER-LEVEL CANNOT-CHECK blocks the tier.** The instrument did not run, could
not reach the target, or could not evaluate the layer at all. **"No violations
found" by an instrument that never executed is the false clean this specification
exists to refuse.** A layer that returns nothing because nothing ran has not
passed.

**ITEM-LEVEL CANNOT-CHECK does not block the tier, and must be published with
it.** The instrument ran, evaluated everything within its reach, and **named
specific items it cannot judge, with a reason for each.** That is the instrument
being truthful about its ceiling, not the target being defective.

**The two are distinguished by a denominator.** A layer-level CANNOT-CHECK has no
denominator: nothing was examined. An item-level one states how many items were
examined, how many were judged, and how many were not. **If a report cannot tell
you what it looked at, treat it as layer-level.**

### The disclosure that makes this honest

**A tier claim MUST publish its CANNOT-CHECK list.** Every item, with the reason
the instrument could not judge it. A tier asserted without that list is
unverifiable, and an unverifiable conformance claim is the P3P failure this
specification is built to prevent.

**This is Verifiable applied to the tier itself.** The claim is not "this page is
accessible." The claim is "these instruments ran, found no violations, and here is
precisely what they could not determine." That is checkable by a stranger, which is
the only kind of claim worth making.

### Why the stricter reading was wrong

Requiring CONFORMS on every item would make Bronze depend on eliminating
constructs no instrument can statically evaluate — an Astro template expression,
a colour on a gradient, an ARIA pattern that needs a human to judge adequacy.
**None of those is an accessibility property.** A standard that withholds its floor
until a static reader can evaluate runtime syntax is measuring the reader, not the
page.

The reference implementation, measured 2026-08-19: L1 **0 FAILS** across 15 pages;
L2 **0 FAILS**, 327 CONFORMS, **4 item-level CANNOT-CHECK** (non-literal template
expressions the source reader cannot evaluate, which L1 covers at render time);
L3 **0 violations**, 29 item-level incomplete. Every CANNOT-CHECK carries its
reason and its denominator.

---

## Reference implementation conformance, measured 2026-08-19

**waxandwires.com holds Bronze — structurally sound.**

Every required layer ran today, against the build now in production
(`wax-and-wires-site@4d819c3`, Cloudflare Pages deploy confirmed).

| layer | instrument | FAILS | item-level CANNOT-CHECK |
|---|---|---|---|
| **L1** | `englyn-check.mjs`, 15 pages | **0** | 179, each with a reason |
| **L1** | `html-validate` | **0** | — |
| **L2** | `englyn-schema-check.mjs`, 331 annotations in 52 source files | **0** | 4 |
| **L3** | axe-core 4.13.0 on Chromium 145.0.7632.6, dist served over localhost | **0** | 29 |

**Interpreter pinned and recorded**, per ledger A18 (a pass recorded without a
pinned interpreter did not reproduce): Python 3.14.6, `playwright==1.58.0`,
axe-core 4.13.0, Chromium 145.0.7632.6.

### The CANNOT-CHECK list, published because the tier claim requires it

**L2, 4 items.** Non-literal Astro template expressions
(`Navigates to the ${label} page…`). The source reader cannot evaluate a runtime
value; **L1 checks what they render to**, so the requirement is covered by another
layer rather than unmet.

**L3, 29 items across 15 pages, two rules:**

- **`color-contrast`** — axe declines to decide where text sits over a gradient or
  an image. **The site computes its own contrast receipts instead**:
  `contrast-check.mjs` runs in the build, 21 pairs, 0 failing, tightest margin
  4.72:1 against a 4.5:1 floor. Published at `/colophon`.
- **`aria-valid-attr-value`** — one node per page, the theme menu's
  `aria-controls="theme-menu-list"`. **Verified by hand: the target exists**
  (`<ul role="listbox" id="theme-menu-list" aria-label="Colour theme">`). A genuine
  instrument limitation, not a defect.

### What Bronze does and does not claim here

It claims **four instruments ran against the live build and found no violations,
and here is exactly what they could not determine.** Nothing more.

It does **not** claim the site is usable by a screen-reader user. **L5 has run
once, agent-driven, and is CANNOT-CHECK at layer level** — the harness is not yet
reproducible across two runs of the same page (see
`ENGLYN_AT_HARNESS_PROTOCOL.md` §4). **Silver requires L4**, which has run and
returned 0 site FAILS with 32 item-level incomplete; the tier is not claimed until
that run is repeated against this build.

**And the defect that proves why the tier is worded this way** was invisible to
every layer above. `text-transform: uppercase` reached WebKit's accessibility tree,
so a screen reader spoke *"What this buys U-S."* axe: 0 violations.
`html-validate`: pass. `englyn-check`: pass. The DOM: correct. **It was found by
listening, and by nothing else.**
