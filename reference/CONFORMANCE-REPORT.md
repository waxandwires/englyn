---
title: "Conformance report — waxandwires.com"
tier: "Bronze — structurally sound"
measured: 2026-08-19
target: "wax-and-wires-site@3471d86, the build serving in production"
asserted_by: "Micah Eberman, the implementer, self-asserting about his own work"
status: self-assessment. Not an audit. Not attested by a third party.
---

# Conformance report — waxandwires.com

## What this document is

**A self-assessment, published because a standard whose author never ran it against anything
is a proposal, not a standard.**

This is the reference implementation's own report. It is asserted by the person who wrote
both the site and the specification, which is the weakest form of conformance claim available
and is stated as such per **§4**. Nobody attested it. There was no audit.

**Everything the instruments could not determine is published below.** A conformance claim
that omits that is unverifiable, and an unverifiable conformance claim is the failure mode
this specification was built against.

---

## The claim, in the form §4 requires

| | |
|---|---|
| **Tier** | **Bronze — structurally sound** |
| **Layers claimed** | L1 (`englyn-check`), L2, L3 |
| **Layers not claimed** | L1 (`html-validate`) — **24 FAILS, published below** · L4 (measured, not claimed) · L5 (**layer-level CANNOT-CHECK**) · L6 (not instrumented) |
| **Date** | 2026-08-19 |
| **Build** | `wax-and-wires-site@3471d86`, the commit serving in production |
| **Asserted by** | the implementer, about his own work |

**Bronze rests on `englyn-check`, L2 and L3. It does not rest on `html-validate`, which reports 24 FAILS** that are published below with our reasoning rather than suppressed. A reader who thinks those 24 should block the tier has everything needed to say so.

**Silver is not claimed.** L4 has run and returned zero site failures, but the L5 harness is
not reproducible across two runs of the same page, and a tier is not awarded on the strength
of an unreproducible instrument.

---

## Results

| Layer | Instrument | FAILS | Item-level CANNOT-CHECK |
|---|---|---|---|
| **L1** | `englyn-check.mjs`, 16 pages | **0** | 189, each with a stated reason |
| **L1** | `html-validate`, built output | **24** (published, with our disagreement stated) | — |
| **L2** | `englyn-schema-check.mjs`, 375 annotations across 53 source files | **0** | 4 |
| **L3** | axe-core 4.13.0 on Chromium 145.0.7632.6, `dist` served over localhost | **0** | 31 |
| **L4** | Playwright keyboard, 16 pages, 185 checks | **1** (control fixture, see below — 0 on every real page) | 34 |
| **L5** | Guidepup, VoiceOver, Safari, WebKit | — | **LAYER-LEVEL, see below** |
| **L6** | none | — | not instrumented |

### Environment, pinned and recorded

macOS 26.5.1 (25F80) · Node 22.22.0 · Python 3.14.6 · `playwright==1.58.0` ·
axe-core 4.13.0 · Chromium 145.0.7632.6 · Safari with VoiceOver on macOS 26.5.1.

**Recorded because an unpinned interpreter has already produced a pass in this project that
did not reproduce.** A result without its interpreter is not a result.

### Controls

`npm run englyn:selftest` — **all controls pass, in both directions.** Every check has a
must-fail fixture that fires and a must-not-fire fixture that stays quiet.

Stated before the results rather than after, because **a green control suite proves the
instrument works, not that the claim is true.** Every instrument here passed its controls
continuously across a window in which some of its published figures were wrong.

**The 1 L4 FAILS in the table above is one of those controls, not a site defect.** L4 ships a
fixture page (`fixtures/trap.html`) built to contain a real keyboard trap, so the
must-fire detector has something to fire on. It fired: focus returned to the trap candidate
after only 2 of 3 elements were reached. Every real site page — all 16 — returned 0 FAILS.

---

## Everything the instruments could not determine

**This is the part of the report that matters.** Per **§Tiers**, a tier claim must publish its
CANNOT-CHECK list, and per **§4** an instrument's published scope limits are its liability
limits. A verdict that hides what it could not check has widened its exposure, not narrowed it.

### L5 — layer-level CANNOT-CHECK. This is why Silver is not claimed.

The screen-reader layer **ran**, and it is the only layer that has ever caught a defect on
this site. But it does not yet produce a record, for three reasons, all of them ours:

**The harness is not reproducible.** Two runs of the same page returned 16 headings and 17,
one starting at the `<h1>` and one at the web-area announcement. `ENGLYN_AT_HARNESS_PROTOCOL`
§4 requires identical results across two runs. **It does not have them, so no run is a
record.**

**The essay body has never been heard.** Every capture so far walked headings and landmarks.
A read-all pass returned one phrase — the page-arrival announcement — rather than the prose.
**A zero-risk result from that pass is a false clean and is reported as one.**

**Pacing is computed, never measured.** There is no speech-completion signal in the driver's
API. An earlier run reported per-item settle times of 903 to 905 milliseconds, which was
exactly its own polling floor presented as data.

**And one AT, one engine, one session.** VoiceOver on WebKit. **NVDA, JAWS, TalkBack and
Narrator are untested**, and the one defect this layer found is WebKit-specific: virtual-buffer
readers may not reproduce it. Per **§4**, a verdict earned against one assistive technology is
never generalised.

### L3 — 29 items, two rules

**`color-contrast`** — axe declines where text sits over a gradient or an image. **The site
computes its own contrast receipts instead:** `contrast-check.mjs` runs in the build, 21 pairs,
0 failing, tightest margin 4.72:1 against a 4.5:1 floor. Published at `/colophon`.

**`aria-valid-attr-value`** — one node per page, the theme menu's
`aria-controls="theme-menu-list"`. **Verified by hand: the target exists**
(`<ul role="listbox" id="theme-menu-list" aria-label="Colour theme">`). A genuine instrument
ceiling, not a defect.

### L2 — 4 items

Non-literal Astro template expressions, e.g.
`data-englyn-consequence={`Navigates to the ${label} page…`}`. **The source reader cannot
evaluate a runtime value; L1 checks what they render to**, so the requirement is covered by
another layer rather than unmet.

### L4 — 32 items, and two findings downgraded on purpose

Two observations were moved from FAILS to CANNOT-CHECK because **they assert requirements this
specification does not carry**: the skip link not moving focus (a WCAG 2.4.1 finding, 14 of 14
pages) and Escape not collapsing a native `<details>` (9 of 9 pages, where the specification's
rule names modal, popover and menu, and the theme menu passes it 14 of 14).

**Both are real and both reproduced.** They are written up as candidate criteria rather than
counted as failures, because **a checker that fails a site against a requirement its own
specification does not carry has invented the requirement.**

### L1 — 179 items

Per page, each with its reason. The largest classes: action-safety tier inferred from prose
rather than declared (**reported as CANNOT-CHECK, never as a pass**, because a prose pattern
can be accidentally wrong where a declaration cannot); duplicate `<header>` elements whose
landmark surfacing depends on the AT; and heading-list sufficiency, which is a heuristic lead
for a human and never a verdict.

**One of these was resolved by listening rather than by an instrument.** The duplicate-header
question — *whether both surface as landmarks* — was answered on every L5 run: **they do not.**
Only `navigation` and `content information` surfaced. That is a static-layer unknown closed by
a screen reader, for VoiceOver only.

---

## What was found and fixed, published rather than omitted

**A first conformance report that publishes only its passes is the P3P shape.** These are the
defects this instrumentation found on its own reference implementation in the seventy-two hours
before this report.

### The one the automated layers could not see

Every heading on this site is authored in sentence case. CSS rendered them as capitals.
**WebKit hands the style-transformed string to the accessibility tree**, so VoiceOver received
`US` and read the country:

> *"What this buys **U-S**."* &nbsp;&nbsp;·&nbsp;&nbsp; *"What I'm doing about **I-T**."*

Six instances across four pages. **At the time: axe 0 violations, `html-validate` pass, this
project's own checker pass, and a correct DOM.** Four layers green.

**Found by running a screen reader and writing down what it said.** Fixed by removing the
presentational uppercase from prose headings and keeping it on short labels, where a
short-word-as-initialism cannot occur. **Confirmed by ear afterward, twice.**

### Instrument defects, which are the more useful half

**A checker reported CONFORMS on checks 2 through 9 while scanning zero files.** A count with
no denominator is not a measurement. Every check now prints *files examined* and fails if it
disagrees with the expected count.

**A residue check used `\b` word boundaries and missed four evasions** — an underscore, a
hyphen, camelCase, and `U+02BC MODIFIER LETTER APOSTROPHE`, which is a Unicode *letter*, so the
boundary never fires. A case-sensitive term also survived a rewrite that had lowercased it:
**1,581 survivals, verifier reporting success.**

**A speech check tested selector reach instead of content**, and fired on eleven selectors that
were correct while structurally unable to see four live instances of the real defect in `<p>`
song titles.

**And three L5 runs measured the development server**, which injects a toolbar that does not
exist in the production build. **Three runs against a page that does not ship**, noticed by a
person listening to buttons that should not have been there.

### Five copies of one contract, each caught by a weaker signal than the last

An enum was ruled once and lived in five places. Instance one was caught by running two
checkers against each other. Instances two and three by an adversarial review. **Instance four
by nothing at all** — a stale example in a skill document, on no instrument's path. Instance
five by a cheap string sweep that should have run four instances earlier.

**The trend is the finding.** The remaining instances of that class are, by construction, the
ones nothing currently on an instrument's path can see.

---

## How to check this report

**Do not take it on trust. That is the point of publishing it.**

```
git clone https://github.com/waxandwires/wax-and-wires-site
npm ci
npm run englyn:selftest      # controls first. if these do not fire, stop.
npm run build                # L1
npm run englyn:schema        # L2
npm run a11y:axe             # L3
npm run l4:keyboard          # L4
```

**If your numbers differ from the table above, that is a finding and we want it.** A FAILS from
a stranger's clone is worth more to this project than a hundred passes on its own machine.

**And if you use a screen reader:** the L5 gap above is the honest state of this report. The
layer that has caught every defect worth having is the layer we cannot yet run properly. **That
is the section where help is worth most.**

---

*Self-asserted by Micah Eberman, 2026-08-19, against `wax-and-wires-site@3471d86`. Not an
audit. Not attested. This report expires the moment the build changes.*

---

## Correction, 2026-08-19, made before publication

**An earlier draft of this report claimed `html-validate: 0 errors`. That was false.**

It was written from a previous session's summary rather than from a run. **A fresh clone at
`4d819c3` produced 20 errors, exit code 1.** The claim was corrected before this report was
published, which is the only reason it is a correction and not a defect in the wild.

**The clone-and-run block at the end of this report is what caught it.** Running it against
our own repository, cold, was the last check before publication and it earned its place.

### Five were real HTML defects. Fixed.

| count | rule | cause | fix |
|---|---|---|---|
| 2 | `no-implicit-close` | MDX wraps a `<p>`'s content in a second `<p>` when the text starts on a new line, producing `<p><p>` | collapsed the block to one line |
| 2 | `close-order` | the stray `</p>` that produced | same fix |
| 1 | `no-inline-style` | an inline JSX `style={{…}}` on a `<summary>`, whose own source comment said it belonged in scoped CSS | moved to `.run-out__summary` in `tokens.css`, values carried over verbatim |

All five were in `essays/nothing-found`. **20 errors down to 15.**

### Fifteen remained after that correction. `the-ramp` adds nine more — twenty-four now, reported the same way

**They are not suppressed.** The rules were not disabled and the configuration was not
touched. **Tuning a checker until it passes is the defect this project is named after**, and
doing it in the report that argues against it would be indefensible.

This is the announcement essay's own build, adding a 16th page. One of the nine is the same
class already defended below, arriving exactly as expected: a 15th `prefer-native-element`
from the same theme-picker widget every page carries. **Eight are new**, because `the-ramp` is
the first essay to use fenced code blocks and more than one markdown thematic break — its own
build later grew one more `<hr/>` break when a section was added mid-review — and its title,
chosen after the rest of this report was already drafted, is longer than the layout's `<title>`
budget:

**1 × `long-title`** — the rendered `<title>` is `Introducing Englyn ... Because The Ramp Was
Always Load Bearing — Wax+Wires`, 75 characters; html-validate's ceiling is 70. The title text
alone is 63; the site's own ` — Wax+Wires` suffix is what pushes it over, and that suffix is
shared by every page, not something this essay controls. **This one was a deliberate choice,
not an oversight**: offered the option to trim the title to fit, the answer was to keep it as
written and publish the finding instead. `long-title` exists for browser-tab and search-result
truncation, both cosmetic — a screen reader still receives and can announce the full string
regardless of what a tab renders, so nothing here is an accessibility regression, only a linter
preference this title didn't satisfy.

**2 × `no-inline-style`** — Astro's built-in Shiki highlighter emits `<pre style="background-
color:…;color:…;overflow-x:auto">` per code fence, carrying the theme's computed colors
per-token. **The style is toolchain-generated, not hand-authored** — nobody wrote a `style=`
attribute in `the-ramp.mdx`. That is a real distinction but not yet a verified one: we have
not confirmed there is no accessibility-relevant difference between this and an authored
inline style, and Shiki does support a CSS-custom-properties output mode that would resolve
it as a genuine fix rather than a suppression. **Not done for this launch. Publishing the gap
instead of quietly reconfiguring around it.**

**5 × `void-style`** — a markdown thematic break (`---`) compiles to a self-closing `<hr/>`
through the remark/rehype pipeline; the same `<hr>` written inside an Astro component (Hero,
LinerNotes, TitleBlock) compiles without the trailing slash, because that path goes through
Astro's own compiler instead. Two renderers, two serializations of the same void element, zero
functional or accessibility difference — this is the toolchain disagreeing with itself, not a
defect a reader or a screen reader would ever encounter. We have not investigated whether the
remark/rehype pipeline is configurable to match. **Publishing, not fixing, for the same
reason as above: no time pressure justifies tuning a checker to reach a rounder number.**

**15 × `prefer-native-element`** — the theme picker is a `<ul role="listbox">` with
`role="option"` children, opened by a button carrying `aria-haspopup="listbox"`,
`aria-expanded` and `aria-controls`. **That is the APG select-only combobox pattern**, and the
`aria-controls` target was verified present by hand: `<ul role="listbox"
id="theme-menu-list" aria-label="Colour theme">`. html-validate's position is that a native
`<select>` would be better. **We think the pattern is correct. We could be wrong.**

**1 × `aria-label-misuse`** — `<h1 class="hero__headline" aria-label="Authored Intelligence">`.
The visible text is split across decorative spans, so the computed accessible name would be
garbled without it. **It is also what keeps that heading speakable under the uppercase
rendering.** The rule's own wording is *"strictly allowed but not recommended."* **Removing a
working accessibility repair to quiet an advisory rule would be degrading the page to satisfy
a linter.**

### This disagreement is not settled, and it is not ours to settle

**Both defences above were written by the same person who wrote the code they defend, and by
an author who does not use a screen reader daily.** That is the weakest possible position from
which to rule that a linter is wrong about assistive technology.

**Open question, and the most useful thing a reader could answer:**

> **Would a native `<select>` serve a screen reader, a braille display, or a switch user
> better than this combobox pattern does?** And is `aria-label` on a decorated `<h1>` the
> right repair, or is restructuring the heading so it needs no label the right one?

**If you use assistive technology and you have an opinion, that opinion outranks ours and we
will change the code.** File it against
`github.com/waxandwires/englyn`, or against the site repository directly.

**Until someone who uses this daily says otherwise, these 24 stand as published FAILS with a
stated disagreement — not as passes, and not as a tuned-away number.**
