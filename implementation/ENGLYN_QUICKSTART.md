# ENGLYN Quickstart

The shortest useful adoption path for applying ENGLYN to a single page today. Full model: `ENGLYN_IMPLEMENTATION_GUIDE.md`.

Five moves, in order:

1. **Semantic structure** — one `<h1>`, one `<main>`, real landmarks, no skipped heading levels, no `<div>` standing in for a heading or a button.
2. **Accessible names** — every control names what it affects, not just what it looks like ("Delete" → "Delete draft: Q3 rollout notes").
3. **Chart summaries** — every chart gets a title, a plain-language summary, and a visually-hidden data table with the same numbers.
4. **Live-region policy** — `aria-live="polite"` for advisory updates, `role="alert"` only for genuinely time-sensitive ones, batch rapid updates.
5. **Explicit action consequences** — risky or irreversible actions state what will happen before they happen, via visible copy and `data-englyn-consequence`.

That's it. Don't reach for the full `data-englyn-*` vocabulary or schema-first components until a page actually needs action metadata, provenance, or agent composition — see the FAQ in the implementation guide.

---

## Before / after

**Before** — visually clear, semantically empty:

```html
<div class="card">
  <div class="title">Server Load</div>
  <div class="chart">
    <!-- canvas-rendered bar chart, no text equivalent -->
  </div>
  <div class="value red">92%</div>
  <button onclick="restart()">⟳</button>
</div>
```

A sighted user sees a red number and a refresh icon. A screen reader hears "button" with no name. An agent sees a `<div>` soup with no indication that clicking `⟳` restarts a production server.

**After** — same visual output, meaning made explicit:

```html
<section class="card" aria-labelledby="load-title" data-englyn-primitive="perceive">
  <h3 id="load-title">Server Load</h3>

  <div class="chart" role="img" aria-label="Server load over the last hour: rising from 61% to 92%, currently above the 90% warning threshold.">
    <!-- canvas-rendered bar chart -->
  </div>
  <table class="sr-only">
    <caption>Server load, last hour, percent utilized</caption>
    <tr><th>10:00</th><td>61%</td></tr>
    <tr><th>10:20</th><td>74%</td></tr>
    <tr><th>10:40</th><td>85%</td></tr>
    <tr><th>11:00</th><td>92%</td></tr>
  </table>

  <p class="value red" data-englyn-severity="high">
    92% utilized <span class="sr-only">— above the 90% warning threshold</span>
  </p>

  <button
    onclick="restart()"
    aria-label="Restart server"
    aria-describedby="restart-consequence"
    data-englyn-primitive="act"
    data-englyn-consequence="Drops active connections for approximately 30 seconds while the server restarts.">
    <span aria-hidden="true">⟳</span>
  </button>
  <span id="restart-consequence" class="sr-only">
    This will drop active connections for approximately 30 seconds while the server restarts.
  </span>
</section>
```

Same pixels. A screen reader user now hears what the chart shows, why the number is red, and what the button does before pressing it. An agent can read `data-englyn-severity="high"` and `data-englyn-consequence` and reason about whether to surface, defer, or block the restart action.

```css
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0;
}
```

---

*Wax+Wires — Authored Intelligence. Full model: `ENGLYN_IMPLEMENTATION_GUIDE.md`.*
