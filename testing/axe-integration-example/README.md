# axe-integration-example

A minimal, runnable `jest-axe` example for the L3 layer of
`../ENGLYN_TESTING_PROTOCOL.md`, using a static HTML fixture instead of a
React component — for teams (or pages) that render plain markup rather
than a component tree.

## Files

- `fixture.html` — two independent `<section>` fragments: `#compliant`
  (follows the ENGLYN foundation skill's rules) and `#broken` (four
  intentional a11y defects: skipped heading level, icon-only button with
  no accessible name, color-only status dot, image with no `alt`).
- `sample.test.js` — loads the fixture into `jsdom`, runs `axe` against
  each section separately, and asserts `#compliant` is clean while
  `#broken` is caught.

## Setup

```bash
npm i -D jest jest-environment-jsdom jest-axe
```

`jest-environment-jsdom` is a **separate package** as of Jest 28 — Jest's
default test environment is `"node"` now. Without it, every DOM call in
`sample.test.js` throws immediately. Either:

```json
// package.json
{ "jest": { "testEnvironment": "jsdom" } }
```

or rely on the `/** @jest-environment jsdom */` docblock already at the
top of `sample.test.js` (both are present here — belt and braces, since
teams vary on which they prefer).

## Run

```bash
npx jest testing/axe-integration-example/sample.test.js
```

## What it verified (run at write-time, 2026-07-17)

```
npx jest sample.test.js --verbose
PASS (2) FAIL (0)
```

Both assertions hold:

1. `#compliant` — `axe()` returns zero violations (`toHaveNoViolations()`).
2. `#broken` — `axe()` returns at least one violation, and specifically
   includes `button-name` and `image-alt` (the two defects that don't
   depend on CSS layout — see the note below on why those two and not
   `color-contrast`).

## Why this catches the broken variant and what it can't catch

`jsdom` parses and exposes the DOM, but it does not do real CSS layout or
paint. Axe rules that only need DOM structure and computed attribute
values — missing `alt`, missing accessible name, wrong ARIA usage, heading
order — work reliably under `jsdom`. Rules that depend on actual rendered
geometry or paint — `color-contrast` chief among them — are unreliable
under `jsdom` because elements report zero width/height and axe treats
them as not visible, silently skipping the check rather than failing it.
That's not a bug in this example; it's a known, documented limitation of
DOM-only testing.

This is exactly why `ENGLYN_TESTING_PROTOCOL.md` defines **two** axe layers,
not one:

- **L3 unit-level** (`jest-axe`, this example) — fast, runs in CI on every
  commit, catches structural/semantic defects early.
- **L3 browser-level** (`@axe-core/playwright`) — slower, runs against a
  real rendered page, catches contrast, focus-visible state, and anything
  else that only exists after layout.

Treat a clean `jest-axe` run as a floor, not a full pass — the same rule
the parent protocol states for axe-core generally (`ENGLYN_TESTING_PROTOCOL.md`
§L3: "axe-core catches roughly 30–50% of WCAG issues automatically").

## Two independent `#compliant` / `#broken` sections in one fixture

The fixture uses two sibling sections rather than two files so a reviewer
can diff them side by side and see exactly which attributes changed
between the working and broken version — the same "before/after, visual
output identical" discipline used in
`../../skills/englyn-accessible-page/examples/before-after-snippet.html`.
