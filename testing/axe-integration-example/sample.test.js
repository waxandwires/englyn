/**
 * jest-axe on a static HTML fixture — no React, no component under test,
 * just markup. This is the L3 "unit-level" pattern from
 * ENGLYN_TESTING_PROTOCOL.md §L3 applied to plain HTML instead of a component.
 *
 * Setup:
 *   npm i -D jest jest-environment-jsdom jest-axe
 *
 * jest-environment-jsdom is a SEPARATE package since Jest 28 — Jest's
 * default test environment is "node" now, and every DOM call in this file
 * throws under "node". Either add it to package.json:
 *
 *   { "jest": { "testEnvironment": "jsdom" } }
 *
 * or add a docblock at the top of this file: `@jest-environment jsdom`.
 *
 * Run:
 *   npx jest testing/axe-integration-example/sample.test.js
 */

/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");
const { axe, toHaveNoViolations } = require("jest-axe");

expect.extend(toHaveNoViolations);

const fixtureHtml = fs.readFileSync(
  path.join(__dirname, "fixture.html"),
  "utf8"
);

// Page-level rules that only make sense against a whole rendered document
// (a single <main>, a <title>, top-level landmark regions) — disabled here
// because we're deliberately testing two isolated <section> fragments, not
// a full page. A real ENGLYN page gets these checked for free at the L3
// browser-level layer (@axe-core/playwright against the live route) — see
// ENGLYN_TESTING_PROTOCOL.md §L3. Disabling them here is standard jest-axe
// practice for fragment/component testing, not a way to dodge a real check.
const FRAGMENT_RULES = {
  "landmark-one-main": { enabled: false },
  "page-has-heading-one": { enabled: false },
  region: { enabled: false },
};

function loadFixture() {
  document.documentElement.lang = "en"; // satisfies html-has-lang at the document level
  document.body.innerHTML = fixtureHtml;
}

describe("ENGLYN fixture — axe-core", () => {
  beforeEach(loadFixture);

  it("the ENGLYN-compliant section has zero automatically detectable violations", async () => {
    const section = document.getElementById("compliant");
    const results = await axe(section, { rules: FRAGMENT_RULES });
    expect(results).toHaveNoViolations();
  });

  it("the intentionally-broken section is caught by axe", async () => {
    const section = document.getElementById("broken");
    const results = await axe(section, { rules: FRAGMENT_RULES });

    expect(results.violations.length).toBeGreaterThan(0);

    // Spot-check the SPECIFIC defects planted in fixture.html (icon-only
    // button with no accessible name, image with no alt) rather than just
    // "some violation exists" — this is what makes the test a real
    // regression guard instead of a coin flip that happens to pass.
    // (Not asserting color-contrast here: jsdom doesn't do layout/paint,
    // so axe's visibility-dependent checks are unreliable under it — that
    // gap is exactly why L3 also runs @axe-core/playwright against a real
    // rendered page, see ENGLYN_TESTING_PROTOCOL.md §L3.)
    const ruleIds = results.violations.map((v) => v.id);
    expect(ruleIds).toEqual(expect.arrayContaining(["button-name", "image-alt"]));
  });
});
