# ENGLYN Testing Protocol

**A Wax+Wires / Authored Intelligence point of view.** Companion to `../implementation/ENGLYN_IMPLEMENTATION_GUIDE.md`. This is the test-layer detail that guide promises: how to actually verify Accessibility Is the Architecture / ENGLYN compliance, with real tools and runnable commands.

---

## The one-contract rule

Accessibility, hydration fidelity, schema validity, and action safety are **one reliability contract, not four separate concerns.** A page that renders correctly but loses its `data-englyn-*` metadata on hydration is exactly as broken as a page missing `alt` text — an agent or screen reader user hits the same wall: meaning that lived in the source is gone by the time it needs to be read. Test them together, report them together, gate on them together.

This protocol defines **6 required test layers.** No layer is optional; each catches failures the others structurally cannot.

| Layer | Catches | Runs | Blocks merge? |
|---|---|---|---|
| L1 — Static structure/semantic lint | Bad HTML, missing labels, heading-order violations, non-serializable props | Every commit (pre-commit / CI) | Yes |
| L2 — Schema validation | Malformed component/payload contracts, missing `data-englyn-*` | Every commit (CI, unit) | Yes |
| L3 — Automated a11y (axe-core) | WCAG-detectable violations: contrast, roles, names, ARIA misuse | Every commit (unit + browser) | Yes |
| L4 — Keyboard-flow | Focus order, traps, unreachable controls, escape/activation failures | Every PR (browser, Playwright) | Yes |
| L5 — Assistive-technology verification | What automated tools cannot see: does it actually make sense spoken aloud | Manual, before ship of any new/changed ENGLYN surface | Yes (release gate) |
| L6 — Regression & observability | Drift over time: issue density creeping up, hydration silently failing in prod | Continuous, dashboarded | No (alerts, doesn't block) |

L1–L4 are automatable and cheap — run them on every change. L5 is manual and expensive — run it before shipping a surface, not on every commit. L6 is passive — it tells you whether the first five layers are actually holding in production.

---

## The tier ladder (`../spec/TIERS.md`)

`../spec/TIERS.md` is normative for what each tier requires; this protocol
only defines the layers themselves. Restated here so the mapping is visible
next to the layer table above, not just in the tier document:

- **Bronze — structurally sound** requires **L1 + L2 + L3, zero violations
  across all three.** A machine-verifiable claim about testing — it says
  three instruments ran and found nothing, and nothing about whether anyone
  could use the thing.
- **Silver — operable end to end** requires **Bronze, plus L4.** The same
  kind of claim, one layer wider.
- **L5 gates neither Bronze — structurally sound nor Silver — operable end
  to end.** It is the evidence a **Gold — verified by lived experience**
  claim would need, but that tier is a v0.2+ destination and an open
  invitation, not a specification — it is not self-certifiable by anyone,
  including this project, and no Gold — verified by lived experience claim
  exists today, including ours.
- **L6 does not gate Gold — verified by lived experience. This amends the
  earlier July mapping, which placed L6 inside that tier.** Two reasons, either sufficient: (1) a layer with
  no verdict cannot gate a tier, and this protocol's own table above defines
  L6 as *"Continuous, dashboarded — No (alerts, doesn't block)"* — a
  dashboard has no pass state to require; (2) requiring production
  telemetry would lock out any surface with no production KPI stream — a
  component library, a documentation site, this specification's own
  reference implementation — from ever reaching the top tier, for reasons
  that have nothing to do with whether the surface is accessible. L6 is now
  an **orthogonal "instrumented" badge**, claimable at any tier, required at
  none.

> **What actually runs on the reference implementation (2026-08-17, RECOMMENDATIONS-V0_1_0 A1/A7).**
> The table above is the *design*. Until 2026-08-17 the reference site had **none of the
> tooling this protocol names for L1–L4** installed (only its own regex checker) — the same shape `ENGLYN_L5_PROCEDURE.md` names for L5, "a
> control that demands proof and provides no way to produce it". As of 2026-08-17:
> **L1** `html-validate` installed (`npm run a11y:html`) and the Englyn static checker
> `scripts/englyn-check.mjs` runs inside `npm run build` and blocks it; **L3**
> `axe-core` runs via `englyn/testing/harness/englyn_axe.py` (`npm run a11y:axe`,
> served over localhost — over `file://` the site renders unstyled and CSS-dependent
> rules false-alarm), advisory, **not wired into the build** (gating is Micah's call);
> **L2** and **L4** were still not run as of that date. **AMENDED 2026-08-18: both
> now exist and have run** — L2 as `site/scripts/englyn-schema-check.mjs`
> (`npm run englyn:schema`, wired into the build), L4 as
> `site/tests/l4-keyboard/` driving a real keyboard in Chromium
> (`npm run l4:keyboard`). Results and verdicts:
> `LAYER-RUN-RECORD-2026-08-18.md`. **All four layers returned a verdict and
> none returned CONFORMS**, so the tier is measured rather than absent — and it
> is still not Bronze — structurally sound. `eslint-plugin-jsx-a11y` does not apply
> (Astro/MDX, not JSX). axe machine-checks the WCAG floor only: 0 of the 10 narration
> rules, and 30–57% of WCAG issues depending on methodology (Deque 2020: 57%);
> automated claims should align to the W3C ACT Rules Format 1.1. A "Blocks merge? Yes"
> above is therefore true only for L1 today; the rest are declared, not enforced.
> **Consequence for the tier ladder, restated on measurement (2026-08-18).**
> The verdict is unchanged, but it is now a measurement rather than an absence.
> **L1 FAILS** (26 across 15 of 15 pages), **L2 FAILS** (4 across 330 source
> annotations), **L3 CANNOT-CHECK** (0 FAILS but 29 incomplete), **L4
> CANNOT-CHECK** (0 site FAILS, 32 incomplete). Bronze — structurally sound
> requires zero violations across L1+L2+L3 and holds none of the three;
> Silver — operable end to end requires Bronze plus L4 and holds neither. Per
> `../spec/TIERS.md` § The reference implementation's own tier, the verdict
> stays **UNKNOWN, not Bronze — structurally sound** — a tier not climbed is
> not claimed. **A CANNOT-CHECK on a required layer means the tier is not
> awarded; it does not mean the layer failed, and it must not be reported as
> either.**

---

## L1 — Static structure / semantic lint

Catch structural mistakes before anything renders: semantic HTML misuse, missing labels, heading-order violations, role misuse, and forbidden non-serializable props on schema-driven components (see `ENGLYN_IMPLEMENTATION_GUIDE.md` § Canonical schema expectations — no functions, framework nodes, or opaque runtime values on the wire).

### Tool: `eslint-plugin-jsx-a11y`

Catches JSX-level a11y mistakes at write time — before a build even happens.

```bash
npm install --save-dev eslint-plugin-jsx-a11y
```

```json
// .eslintrc.json
{
  "plugins": ["jsx-a11y"],
  "extends": ["plugin:jsx-a11y/recommended"],
  "rules": {
    "jsx-a11y/aria-role": "error",
    "jsx-a11y/no-noninteractive-tabindex": "error",
    "jsx-a11y/heading-has-content": "error",
    "jsx-a11y/anchor-is-valid": "error",
    "jsx-a11y/aria-props": "error",
    "jsx-a11y/role-has-required-aria-props": "error"
  }
}
```

```bash
npx eslint . --ext .js,.jsx,.ts,.tsx
```

`plugin:jsx-a11y/recommended` already covers heading order, role misuse, aria-prop mismatches, and missing accessible names on interactive elements. The explicit rules above are the ones worth failing the build over rather than warning.

### Tool: `html-validate`

Runs against rendered/static HTML output (server-rendered pages, generated docs, email templates) — catches what JSX linting can't see because it never touches actual markup.

```bash
npm install --save-dev html-validate
```

```json
// .htmlvalidate.json
{
  "extends": ["html-validate:recommended", "html-validate:a11y"],
  "rules": {
    "heading-level": "error",
    "no-missing-references": "error",
    "element-required-attributes": "error",
    "input-missing-label": "error"
  }
}
```

```bash
npx html-validate "dist/**/*.html"
```

### Forbidden-prop check (schema serializability)

Schema-driven / agent-composed surfaces must stay JSON-serializable. A cheap CI check: grep the compiled schema output for anything that isn't a plain value.

```bash
# Fails the build if a schema payload contains a function, a React/JSX node,
# or an unserialized Date/Map/Set — the wire contract must survive JSON.stringify.
node -e "
const schema = require('./dist/schema.json');
const bad = JSON.stringify(schema, (k, v) => {
  if (typeof v === 'function') throw new Error(\`non-serializable value at key '\${k}'\`);
  return v;
});
console.log('schema is JSON-serializable, ' + bad.length + ' bytes');
"
```

### Manual gate: Rule-10 read-aloud

Static lint cannot catch semantically wrong-but-syntactically-valid markup — an `aria-label="icon"` passes every linter and tells a screen reader user nothing. This is why L1 always closes with the Rule-10(b) read-aloud pass (full procedure in `ENGLYN_ACCEPTANCE_CHECKLIST.md`): read every `aria-label` out loud, confirm it's an interpretation, not a transcription.

---

## L2 — Schema validation

Validate component and payload contracts **before render**, not after. A malformed payload should fail loudly in a test, not silently degrade into a broken or meaningless UI in production.

### Tool: Zod (or equivalent schema-first validator)

```ts
// schema/card.ts
import { z } from "zod";

// Membership, not shape. `role: z.string().min(1)` used to be the field
// below — it accepts any non-empty string, which is a SHAPE constraint, not
// a MEMBERSHIP constraint. That is exactly the defect
// spec/VOCABULARY.md's membership criterion exists to close: a conforming
// checker MUST validate that a data-englyn-* value is inside its published
// enum, not merely that the attribute is present and non-empty.

export const EnglynRole = z.enum([
  "narration", "section", "action", "status", "citations", "run-out",
  "media", "collection", "disclosure", "hero", "banner", "bio", "card",
]);
// Thirteen, CLOSED (amended ruling 2026-08-18). `alert`, `stat` and `chart`
// are RESERVED -- named in the vocabulary, value space not specified -- and
// are deliberately NOT enum members. Do not add them back.

export const EnglynPrimitive = z.enum([
  "perceive", "act", "announce", "audit", "interrupt", "oversee",
]);

export const EnglynSource = z.enum([
  "manual", "generated", "llm-draft", "research-pipeline", "analytics",
  "build-script",
]);

export const EnglynCardSchema = z.object({
  role: z.literal("card"),
  actionId: z.string().optional(),
  title: z.string().min(1),
  body: z.string().min(1),
  // The seven NORMATIVE data-englyn-* attributes per spec/VOCABULARY.md:
  // primitive, consequence, receipt, role, priority, source, consumer.
  // Obligation varies per attribute (MUST/SHOULD, and on which regions) —
  // see spec/VOCABULARY.md, not "required on every meaningful region."
  // `priority` and `consumer` are not modeled on this fixture card and are
  // out of scope for this example.
  englyn: z.object({
    role: EnglynRole,                         // data-englyn-role
    primitive: EnglynPrimitive,                // data-englyn-primitive
    // confidence and severity are RESERVED, NOT SPECIFIED in
    // spec/VOCABULARY.md — zero measured uses anywhere in the corpus (source,
    // build, or fixture). No conformance requirement attaches to either, and
    // a checker MUST NOT fail a page for omitting them. Modeled here, both
    // optional, as their PROPOSED (unruled) value spaces only — this is not
    // a normative field until spec/VOCABULARY.md says so.
    confidence: z.enum(["high", "medium", "low", "unknown"]).optional(),
    severity: z.enum(["low", "medium", "high", "critical"]).optional(),
    consequence: z.string().optional(),       // data-englyn-consequence — free text, by declaration; required if actionId is set + tier >= T2
    source: EnglynSource.optional(),          // data-englyn-source — required for AI-generated content
    receipt: z.string().uuid().optional(),    // data-englyn-receipt — free text, by declaration (a durable identifier); required for external-write actions
  }),
}).superRefine((card, ctx) => {
  if (card.actionId && !card.englyn.consequence) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "actionId present without data-englyn-consequence — Rule 5 violation",
      path: ["englyn", "consequence"],
    });
  }
});

export type EnglynCard = z.infer<typeof EnglynCardSchema>;
```

```ts
// schema/card.test.ts
import { describe, it, expect } from "vitest"; // or jest
import { EnglynCardSchema } from "./card";

describe("EnglynCardSchema", () => {
  it("rejects a card with an action but no consequence label", () => {
    const result = EnglynCardSchema.safeParse({
      role: "card",
      actionId: "archive-draft",
      title: "Q3 rollout notes",
      body: "Draft, unreviewed.",
      englyn: { role: "card", primitive: "act" }, // consequence missing
    });
    expect(result.success).toBe(false);
  });
});
```

Run this as a normal unit-test target (`npm test` / `vitest run schema/`) — no special CI wiring needed, it's just another test file. Validate at the API boundary (server response, agent-composed payload) as well as at component-prop boundaries, so a malformed value can never reach render.

### `data-englyn-*` attribute presence check (rendered output)

Zod validates the payload before render; a second cheap check confirms the attributes actually made it into the DOM (catches hydration drops — see L6).

```ts
// tests/englyn-attrs.test.ts
import { render } from "@testing-library/react";
import { Card } from "../components/Card";

// Published enums, spec/VOCABULARY.md — kept local to this test rather than
// imported so the test still catches a schema/vocabulary drift, not just a
// component regression.
const ENGLYN_ROLE_VALUES = new Set([
  "narration", "section", "action", "status", "citations", "run-out",
  "media", "collection", "disclosure", "hero", "banner", "bio", "card",
]);
const ENGLYN_PRIMITIVE_VALUES = new Set([
  "perceive", "act", "announce", "audit", "interrupt", "oversee",
]);

it("every meaningful region exposes data-englyn-role and data-englyn-primitive with values inside the published enum", () => {
  const { container } = render(<Card {...fixture} />);
  const regions = container.querySelectorAll("[data-englyn-role]");
  expect(regions.length).toBeGreaterThan(0);
  regions.forEach((el) => {
    // Presence — the original assertion. Necessary, not sufficient.
    expect(el).toHaveAttribute("data-englyn-primitive");
    // Membership — the assertion presence-only testing was missing. A typo'd
    // or invented value (the "orientation" / "operate" class of defect,
    // spec/VOCABULARY.md § Two invented values) passes a presence check and
    // must fail this one.
    expect(ENGLYN_ROLE_VALUES.has(el.getAttribute("data-englyn-role"))).toBe(true);
    expect(ENGLYN_PRIMITIVE_VALUES.has(el.getAttribute("data-englyn-primitive"))).toBe(true);
  });
});
```

### What the reference implementation actually runs for L2 (2026-08-18)

The two examples above are React and testing-library; the reference site is
Astro/MDX and has no component-render test harness. L2 runs there as
`site/scripts/englyn-schema-check.mjs` (`npm run englyn:schema`, wired into
`npm run build`), validating `src/**` against the Zod enums in
`site/src/lib/englyn-schema.mjs`, which are copied from `../spec/VOCABULARY.md`.

**It reads source, not `dist/`, and that is the point.** L1 validates every
value a page emitted; it is structurally blind to a branch no content takes.
The first L2 run found `data-englyn-source={nature === 'synthetic' ?
'generated' : 'manual'}` — `generated` is not in the published `source` enum,
no essay is synthetic, so no page emits it and L1 reports clean right up until
the first synthetic reading ships. **The two layers are not two passes over
the same evidence; each is blind to what the other sees.**

Its controls (`npm run englyn:schema:selftest`) fire in both directions,
including the two exemptions that would otherwise blind it: comment bodies are
blanked (an attribute inside a comment is not an emission), and a ternary's
condition is not read as an emitted value. Both are pinned by a must-fire
control as well as a must-not-fire one.

---

## L3 — Automated a11y checks (axe-core)

axe-core is the industry-standard automated WCAG rule engine. It catches roughly 30–50% of WCAG issues automatically (the rest need L4/L5) — treat a clean axe run as a floor, not a certification.

> **A clean axe run is item 12 in the skill's Twelve Silent Failures appendix.** It is listed there because reporting it as certification is the single most common accessibility false zero in the industry, and because none of the other eleven silent failures in that appendix is caught by L1, L2, or L3 either. When recording an L3 result, record it as `L-AOM: CONFORMS (axe, 30–50% coverage)`, never as "accessible."

### Unit-level: `jest-axe`

```bash
npm install --save-dev jest-axe @testing-library/react jsdom
```

```js
// Card.test.jsx
import { render } from "@testing-library/react";
import { axe, toHaveNoViolations } from "jest-axe";
import { Card } from "./Card";

expect.extend(toHaveNoViolations);

it("Card has no automatically detectable a11y violations", async () => {
  const { container } = render(<Card title="Q3 rollout notes" severity="high" />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

A full worked example — including a fixture that's deliberately broken so you can see `jest-axe` catch it — lives in `axe-integration-example/` next to this file.

### Browser-level: `@axe-core/playwright`

Catches issues that only exist after real rendering/hydration/CSS — contrast against computed styles, focus-visible states, dynamically injected content.

```bash
npm install --save-dev @axe-core/playwright @playwright/test
```

```ts
// e2e/dashboard.a11y.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("dashboard has no automatically detectable a11y violations", async ({ page }) => {
  await page.goto("/dashboard");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

```bash
npx playwright test e2e/dashboard.a11y.spec.ts
```

`AxeBuilder` supports `.include()` / `.exclude()` (scope to a container), `.disableRules()` (suppress a known false positive with a comment explaining why), and `.withTags()` (target a specific WCAG conformance level).

### CLI option: Pa11y

Useful for scripted checks against a running URL without writing a test file — good for a pre-deploy smoke check or scanning a whole sitemap.

```bash
npm install -g pa11y pa11y-ci
```

```bash
# Single page
npx pa11y https://staging.example.com/dashboard --standard WCAG2AA

# Whole site, via config
```

```json
// .pa11yci.json
{
  "defaults": { "standard": "WCAG2AA", "timeout": 10000 },
  "urls": [
    "https://staging.example.com/",
    "https://staging.example.com/dashboard"
  ]
}
```

```bash
npx pa11y-ci
```

---

## L4 — Keyboard-flow tests

Automated a11y scanners are largely blind to interaction — they check static/rendered DOM, not what happens when a real keyboard user tabs through it. This layer is Playwright driving the keyboard directly.

What to verify per interactive surface:

- **Focus order** matches visual/priority order (top-to-bottom, left-to-right, or the declared reading order — never silently reordered by CSS).
- **Activation keys** — `Enter`/`Space` activate buttons; `Enter` submits forms; arrow keys move within composite widgets (tabs, listbox, menu) per the ARIA APG pattern for that role.
- **Escape behavior** — `Escape` closes any modal, popover, or menu and returns focus to the triggering element.
- **Focus traps** — a modal/dialog traps Tab within itself; a non-modal region never traps focus.
- **`tabindex` inside `aria-hidden`** — zero focusable descendants inside any `aria-hidden="true"` region (a screen reader user must never be able to tab into content the AT layer has been told doesn't exist).

```ts
// e2e/keyboard-flow.spec.ts
import { test, expect } from "@playwright/test";

test("dashboard: focus order, action activation, and modal escape", async ({ page }) => {
  await page.goto("/dashboard");

  // Focus order: first Tab should land on the Rule-7 narration region's
  // first focusable descendant, or the first real control if narration
  // itself is non-focusable (it usually is — sr-only, not interactive).
  await page.keyboard.press("Tab");
  await expect(page.locator(":focus")).toHaveAttribute("data-englyn-primitive", /perceive|act/);

  // Activation: keyboard Enter must fire the same handler as a click.
  const archiveButton = page.getByRole("button", { name: /archive draft/i });
  await archiveButton.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("dialog", { name: /confirm/i })).toBeVisible();

  // Escape closes the dialog and returns focus to the trigger.
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeHidden();
  await expect(archiveButton).toBeFocused();
});

test("no focusable elements inside aria-hidden regions", async ({ page }) => {
  await page.goto("/dashboard");
  const hiddenFocusables = await page.locator(
    '[aria-hidden="true"] a[href], [aria-hidden="true"] button, [aria-hidden="true"] [tabindex]:not([tabindex="-1"])'
  ).count();
  expect(hiddenFocusables).toBe(0);
});

test("focus trap: modal keeps Tab cycling inside itself", async ({ page }) => {
  await page.goto("/dashboard");
  await page.getByRole("button", { name: /archive draft/i }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();

  const focusableInDialog = dialog.locator("a[href], button, input, [tabindex]:not([tabindex='-1'])");
  const count = await focusableInDialog.count();
  // Tab through every focusable element in the dialog plus one more —
  // focus must land back on the first element, never escape the dialog.
  for (let i = 0; i <= count; i++) {
    await page.keyboard.press("Tab");
  }
  await expect(focusableInDialog.first()).toBeFocused();
});
```

```bash
npx playwright test e2e/keyboard-flow.spec.ts
```

---

## L5 — Assistive-technology verification

Automated tools and keyboard-driven tests cannot tell you whether the *spoken experience* actually makes sense — that a status cell says "Deploy status: failed, rolled back automatically" and not "red X icon." This layer is manual, and it's the release gate: run it on any new or materially changed ENGLYN surface before it ships, not on every commit.

### The test matrix

| Screen reader | Platform | Paired browser | Priority |
|---|---|---|---|
| NVDA | Windows | Firefox | Primary — free, open-source, most-used desktop screen reader in recent WebAIM survey rounds |
| JAWS | Windows | Chrome | Primary — dominant in enterprise/professional deployments |
| VoiceOver | macOS | Safari | Primary — the only screen reader most Mac users have; Safari is Apple's best-supported pairing |
| VoiceOver | iOS | Safari | Primary — mobile is a distinct interaction model (swipe navigation, rotor), test separately from desktop |
| TalkBack | Android | Chrome | Primary — the Android equivalent of VoiceOver; do not skip mobile |
| Narrator | Windows | Edge | Secondary — built-in fallback, lower usage share, still worth a spot-check on flagship flows |

### These six rows are NOT equivalent tests, and the transfer between them is weak

**Added 2026-08-13.** The matrix above is ordered by user share, which is the
right way to allocate time and the wrong way to reason about coverage. The six
pairs are **four architecturally distinct consumers**, and a pass on one does
not mean what a six-row table implies.

| Consumer | Architecture | Failure classes unique to it |
|---|---|---|
| NVDA, JAWS | Off-screen **virtual buffer**, browse mode vs focus mode | Buffer desync from the live tree; mode confusion; virtual cursor position loss on re-render |
| VoiceOver | **No decoupled buffer.** Works the live AXAPI tree directly | Rotor quality; direct-tree focus behaviour |
| TalkBack | Node-tree traversal by touch | Container grouping failures; Explore-by-Touch ordering |
| Refreshable Braille | 40 to 80 cells, tactile, **no audio** | Pin buffer cleared by re-render; cell-budget exhaustion by verbose labels |

**The consequence for this studio specifically.** Per
`ENGLYN_L5_PROCEDURE.md`, the only pair we can currently run is VoiceOver on
macOS, possibly plus iOS. **That is the architectural outlier.** Virtual
buffer desync and browse-versus-focus mode confusion, which are common
failure classes on the two screen readers with the largest desktop share,
**cannot occur on the platform we can test**. They are not "probably fine."
They are untested and untestable here.

So a VoiceOver pass is an `L-AT (VoiceOver/macOS)` verdict and nothing
broader. Four rows in this matrix are CANNOT-CHECK, and the braille consumer
is not in the matrix at all. All five go in `../spec/UNVERIFIED.md` by name,
with the transfer limit stated, not just the missing hardware.

This does not weaken the L5 gate. It is the strongest available argument for
paid co-reviewers, and `ENGLYN_L5_PROCEDURE.md` already makes it: the gate is
un-self-certifiable as a matter of hardware, and buying the hardware would
not fix it, because the thing being tested is whether the surface works for
someone who uses that AT daily.

**Prioritization note:** WebAIM's recurring Screen Reader User Survey (webaim.org/projects/screenreadersurvey) is the standard reference for allocating manual-test time. Current and recent rounds consistently show NVDA and JAWS as the two dominant Windows screen readers (their relative first/second-place ranking has shifted survey to survey as NVDA's free/open-source model gained share), VoiceOver as functionally the only screen reader in daily use on macOS/iOS, and TalkBack as the dominant Android screen reader. Check the current survey before allocating test time — exact percentages move release to release, but the shortlist of "these five/six matter" has been stable for years. Do not skip a platform because it's a smaller slice: for a blind or low-vision user on that platform, it's 100% of their experience.

### What to verify per major flow

Run this per flow (not per page) — a flow is a complete task: "review and archive a draft," "read the dashboard summary and drill into a card," "submit a form and see the result."

1. **Orientation.** Landing on the page/flow, can the user tell what it is and what matters most within the first ~10 seconds of listening? (This is the Rule-7 narration section doing its job.)
2. **Navigation.** Can the user move through headings, landmarks, and lists using the screen reader's own navigation commands (not just Tab) and land somewhere sensible each time?
3. **Comprehension of dynamic content.** When something updates (a status changes, a live region announces), does the user hear it, and does it make sense out of context (not just "updated")?
4. **Action safety.** Before taking a T2/T3 action, does the user hear the consequence statement (Rule 5) before or as part of activating the control — never after?
5. **Charts and complex visuals.** Does the screen reader expose the hidden data table, and does the chart's `aria-label` state what's measured, direction of "better," and outliers — without ever requiring the user to interpret a rendered image?
6. **Error recovery.** If something goes wrong (form validation error, failed action), is the error announced, and is it clear how to recover?

### Recording results

Use a simple pass/fail/notes table per flow × screen reader. Store results alongside the surface's test files (or in `../measurement/` once the observability wiring lands — see L6) so regressions are diffable over time, not just tribal knowledge.

```markdown
## AT verification — Dashboard / Archive draft flow — 2026-07-17

| AT + browser | Orientation | Navigation | Dynamic content | Action safety | Charts | Errors | Notes |
|---|---|---|---|---|---|---|---|
| NVDA + Firefox | Pass | Pass | Pass | Pass | Pass | Pass | — |
| JAWS + Chrome | Pass | Pass | Fail | Pass | Pass | Pass | Live region not announced on second update in a session — investigate polite-region reuse |
| VoiceOver + Safari (macOS) | Pass | Pass | Pass | Pass | Pass | Pass | — |
| VoiceOver + Safari (iOS) | Pass | Fail | Pass | Pass | N/A | Pass | Rotor "headings" list skips h3s inside card group — check heading nesting |
| TalkBack + Chrome | Pass | Pass | Pass | Pass | Pass | Pass | — |
```

A row with any `Fail` blocks ship until resolved or explicitly waived with a documented reason and follow-up ticket.

---

## L6 — Regression & observability

L1–L5 catch problems before ship. L6 tells you whether those gates are actually holding once real users and real agents hit the surface in production — and feeds the numbers into the measurement workstream (`../measurement/`).

### KPIs to track over time

| KPI | Definition | Why it matters | Target direction |
|---|---|---|---|
| **A11y issue density** | axe-core violations per page / per 1,000 DOM nodes, tracked per surface over time | Catches slow drift — a surface that passed L3 at ship time can regress as it's edited | Flat or trending down |
| **Hydration success rate** | % of page loads where the client successfully hydrates without falling back to a degraded/static render | A `data-englyn-*` attribute that only exists pre-hydration is invisible to an agent reading the live DOM | ≥ 99.9% |
| **Render-fallback rate** | % of renders that hit an error boundary or fallback UI instead of the intended component | Fallback UIs are almost never ENGLYN-compliant by design (they're the emergency path) — a rising rate means users are silently losing accessibility | Near zero |
| **Agent-composition success rate** | % of agent-driven schema-composed surfaces that pass schema validation (L2) on first attempt in production | Schema violations in production mean an agent produced output a human or AT user will hit broken | Trending toward 100% |
| **Narration-gate pass rate** | % of shipped ENGLYN surfaces with a recorded Rule-10(b) read-aloud pass on file | This is a process metric, not a runtime one — it tells you whether the manual gate is actually being run, not skipped under deadline pressure | 100% |

### How this feeds the measurement workstream

These are event-level signals, not vanity metrics — each one should be emittable from the running app (a hydration-success beacon, an axe-CI run result, a schema-validation-failure log line) and land in the same analytics pipeline already wired for the site's existing accessibility telemetry (`prefers-reduced-motion` and friends in `Base.astro`). `../measurement/` owns the schema, the aggregation, and the privacy boundary (aggregate, non-fingerprinting — same ruling as the rest of the analytics build); this protocol only defines what the six KPIs mean and when they should fire. Do not build a second, competing telemetry pipe for ENGLYN — extend the one that exists.

**Alerting, not gating.** Unlike L1–L5, L6 does not block a merge or a release — it's a dashboard and an alert. A KPI moving the wrong direction is a signal to open an investigation, not an automatic rollback.

---

## Summary: when each layer runs

```
commit  ──► L1 (lint) ──► L2 (schema) ──► L3-unit (jest-axe)  ──┐
                                                                   ├─► merge
PR      ──► L3-browser (playwright+axe) ──► L4 (keyboard) ─────┘

pre-ship of new/changed ENGLYN surface ──► L5 (manual AT matrix) ──► release gate

production, continuous ──► L6 (KPIs) ──► dashboard + alerts, never blocks
```

See `ENGLYN_ACCEPTANCE_CHECKLIST.md` in this directory for the runnable pre-publish gate that ties L1–L5 together into a single checklist an engineer runs before shipping.
