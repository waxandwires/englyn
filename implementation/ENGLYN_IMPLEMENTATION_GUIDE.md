# ENGLYN Implementation Guide

**A Wax+Wires / Authored Intelligence point of view.** Engineer-ready reference for applying **Accessibility Is the Architecture / ENGLYN** to any digital output: product UI, dashboards, internal tools, generated content, documents, embeds, voice surfaces, and spatial canvases.

---

## Working definitions

**Accessibility Is the Architecture.** The architectural stance that accessibility is not an afterthought but the core reliability layer for human-and-agent systems. If a system's outputs aren't structured for reliable meaning-extraction, they're not reliable for anyone — human or agent.

**ENGLYN.** The five-mark standard (Observable, Verifiable, Explicit, Recoverable, Typed) that makes outputs interpretable, navigable, auditable, interruptible, and safe across humans, assistive tech, and agents. ENGLYN is what Accessibility Is the Architecture looks like when it's implemented: the five marks, resting on a behavioral-primitives model of six primitives (below), applied consistently across a surface.

## The core thesis

> The patterns that make work usable for humans across modalities are the same ones that make it interpretable, reliable, and auditable for agents.

Traditional accessibility work optimizes for one consumer: a human, usually via browser and screen reader. Accessibility Is the Architecture / ENGLYN extends that model. The semantics that help a screen reader user understand a page are the same semantics that help an AI system orient, summarize, navigate, and act safely. The move is from **presentation-first output** to **meaning-first output**.

**Without Accessibility Is the Architecture / ENGLYN** — agents and assistive tech infer structure from layout, styling, and scattered labels: higher ambiguity, weaker chart understanding, unclear action semantics, more hallucination pressure.

**With Accessibility Is the Architecture / ENGLYN** — outputs become structured interface contracts with explicit semantics and action meaning: faster orientation, better summarization, safer action-taking, reusable across screen, voice, and agent flows.

This is the practical form of a belief Wax+Wires already holds: build it for everyone or don't build it. A design that fails a screen reader user is a design that will also fail an agent trying to act on a user's behalf — and both failures trace to the same root cause, meaning that only lives in pixels.

---

## What every engineer implements (the minimum standard)

Any page or digital output should be designed so a sighted human, a screen reader user, and an agent can all extract the same core meaning. Minimum bar:

- **Semantic structure** — real headings, landmarks, lists, tables, buttons, and labels.
- **Accessible names** — every meaningful control, region, and visualization exposes a clear name.
- **Action meaning** — actions state what they affect, what they do, and what the consequence is.
- **Status and interruption model** — dynamic updates are announced in a controlled way.
- **Auditability** — generated or agent-authored outputs carry provenance and confidence cues.
- **Cross-modal readiness** — the same output supports visual, screen reader, and voice narration paths.

**Practical rule:** if a user can only understand an output by visually parsing layout, the output is not yet ENGLYN-compliant.

---

## The behavioral-primitives model (beneath ENGLYN's five marks)

Beneath ENGLYN's five marks (Observable, Verifiable, Explicit, Recoverable, Typed) sits a behavioral-primitives model — a small set of consistent primitives. They shape every surface, not just AI-specific flows.

| Primitive | What it means | Implementation expectation |
|---|---|---|
| **Perceive** | The system understands semantic meaning, not just pixels | Roles, headings, labels, structured regions, reading order |
| **Act** | Actions are bounded, explicit, and typed | Named actions, confirmation rules, safe defaults, no ambiguous controls |
| **Announce** | Changes are surfaced clearly | `aria-live`, status messages, polite/assertive policy |
| **Audit** | Outputs and actions can be explained later | Provenance, receipt IDs, confidence, source references |
| **Interrupt** | Partial states remain valid and recoverable | Graceful degradation, cancellable flows, undo where possible |
| **Oversee** | Humans remain accountable | HITL/HOTL controls, approvals, review states, override paths |

Tag every meaningful region with `data-englyn-primitive` to declare which behavioral phase it participates in — a single element may carry more than one.

---

## The implementation model

### 1. Start with semantic structure

- One clear page purpose and a logical heading hierarchy.
- Use landmarks intentionally: `banner`, `navigation`, `main`, `complementary`, `search`, `form`, `contentinfo` where appropriate.
- Prefer native elements over generic containers with ARIA overrides.
- DOM order matches meaningful reading order.
- For dashboards, separate summary, detail, actions, and supporting context into named regions.

### 2. Make every control understandable

- Buttons and links must answer: *what will happen if activated?*
- Accessible names include target or context when visible text is vague ("Delete" → "Delete draft: Q3 rollout notes").
- Expose action consequence for risky or irreversible behavior.
- Never rely on color, iconography, or placement alone.

### 3. Treat charts and complex visuals as first-class accessibility content

- Provide chart title, summary, and machine-readable values.
- Expose a screen-reader-friendly table or equivalent structured description.
- State what the chart measures, whether higher/lower is better, and key outliers.
- Never make a chart the only place where critical insight exists.

### 4. Add controlled announcement behavior

- `aria-live="polite"` by default for advisory or informational updates.
- Reserve assertive behavior (`role="alert"`) for truly urgent, time-sensitive states.
- Batch or coalesce rapid updates before injecting.
- Never inject interactive content into a live region without preserving semantics and follow-up navigation.

### 5. Add agent-readable metadata where meaning would otherwise be implicit

> **`spec/VOCABULARY.md` is the normative source for every `data-englyn-*`
> attribute, its permitted values, and its obligation level.** This section is
> derivative and orientation-only. Where the two differ, `VOCABULARY.md`
> governs.
>
> **Corrected 2026-08-18.** This guide previously published a table of six
> attributes as "the base six". It was wrong in both directions: it omitted
> `role`, `priority`, `consumer`, `state` and `value`, and it specified
> `confidence` and `severity`, which have **zero uses** in the reference
> implementation and are now **reserved, not specified**. `consumer` — the
> attribute that declares who an annotation is *for* — was the most
> consequential omission.

The seven **normative** attributes, in the four groupings `VOCABULARY.md` defines:

| grouping | attributes |
|---|---|
| Operation semantics | `data-englyn-primitive` · `data-englyn-consequence` · `data-englyn-receipt` |
| Document structure | `data-englyn-role` · `data-englyn-priority` |
| Annotation provenance | `data-englyn-source` |
| Routing | `data-englyn-consumer` |

`data-englyn-severity`, `data-englyn-confidence`, `data-englyn-value` and
`data-englyn-state` are **reserved** — named so no implementation invents an
incompatible meaning, but carrying no conformance requirement. Do not treat
their absence as a defect.

**This is a schema, not a convention.** A conforming page MUST NOT emit a
`data-englyn-*` value outside the published enum, and a conforming checker MUST
validate value *membership*, not merely attribute *presence*. Extend it per
domain by proposing an enum addition, never by shipping an undeclared value.

---

## ARIA/a11y best practices by output type

### General pages and documents

- Headings express information architecture, not typography.
- Lists for grouped items, not manual punctuation.
- Tables only for real tabular relationships.
- Descriptive link text.
- Focus order follows meaning.
- Keyboard-only use works end to end.

### Dashboards and data-heavy views

- Expose an executive summary before deep detail.
- Group cards into labeled regions.
- Each card has a title, purpose, status, and available actions.
- Pair visual severity with text status.
- Drill-down actions are explicit and unique.

### Forms and workflows

- Every field needs a label, description where needed, and a clear error relationship.
- Validation messages are perceivable without hunting.
- Multi-step flows expose current step, remaining path, and recovery options.
- Approval checkpoints are explicit for risky actions.

### Generated / AI-authored content

- Mark AI interaction and AI-generated content clearly and accessibly.
- Retain human-visible labels alongside machine-readable provenance.
- Log source, confidence, and revision state when the output may drive action.
- Provide human review for high-consequence output.

### Spatial canvases and 2D surfaces

- Don't expose raw geometry as the only meaning model.
- Provide group labels, reading-order hints, and a fallback linear rendering.
- Use a canvas-level envelope that declares layout strategy and composition status.
- Support group-aware y-then-x linearization for tab order.
- Use directional navigation only when predictable and testable.

---

## Canonical schema expectations

For componentized or agent-composed surfaces, treat the schema as the contract, not the JSX. Good schema-driven outputs are:

- **JSON-serializable** — no functions, framework nodes, or opaque runtime values on the wire.
- **Slot-based** — named slots like header, body, footer, actions.
- **Variant-driven** — enums, not arbitrary style strings.
- **Accessibility-annotated** — role, labels, keyboard contract, safety semantics.
- **Action-typed** — `actionId` plus an optional validated payload.

| Do | Avoid |
|---|---|
| Use a schema-first definition (Zod or equivalent) | Implicit props and prop spreading on public APIs |
| Expose structured slots | Passing framework nodes (JSX, component trees) over the wire |
| Use action registries with typed payloads | Inline callbacks in schema-carrying APIs |
| Use finite variants | Free-form style overrides for agent-selected UI |
| Encode a11y metadata explicitly | Leaving roles, focus, or labels to convention alone |

---

## Action-safety tiers

Action metadata is not optional. The system should always know whether an action is reversible, dangerous, confirmable, external-facing, or blocked.

| Tier | Meaning | Expected behavior |
|---|---|---|
| **T1 — Exception** | Read or navigate | Immediate, low-risk |
| **T2 — HITL** | Create internal artifacts or alerts | Propose or one-click confirm |
| **HOTL** | Internal auto-execute with undo | Only when strongly governed and reversible |
| **T3 — HITL-High** | Customer- or public-facing, or high-consequence | Multi-step review before execution |
| **Blocked** | Never allowed | Structurally excluded |

This maps directly onto Belief 1 — the human keeps the pen. T1/T2/HOTL are where AI accelerates; T3 and Blocked are where a human stays the author of the outcome, not just a rubber stamp on it.

---

## Reference implementation checklist

- [ ] The page has a clear purpose and heading hierarchy.
- [ ] Landmarks are present and correctly labeled where needed.
- [ ] DOM order matches meaningful reading order.
- [ ] All interactive elements have accessible names.
- [ ] Color is not the only carrier of status or urgency.
- [ ] Charts and visuals have summaries and data equivalents.
- [ ] Dynamic updates use appropriate `aria-live` behavior.
- [ ] Risky actions expose consequence and confirmation patterns.
- [ ] AI-generated or agent-authored output is visibly and programmatically labeled.
- [ ] Output includes provenance or receipt references when actions or decisions matter.
- [ ] Keyboard-only navigation works through all critical paths.
- [ ] Screen reader testing has been performed on major target flows.

*(Full test-layer detail — static lint, axe-core, keyboard flow, AT verification, the Rule-10 read-aloud gate, regression/observability KPIs — lives in the companion `testing/` workstream of this package.)*

---

## Common anti-patterns

- Generic `div` structures where semantic elements should exist.
- Exposing only visual layout with no structural or narrative equivalent.
- Adding AI labels only in hidden metadata with no human-visible disclosure.
- Color-only urgency cues.
- Charts that are visually rich but semantically empty.
- Letting agents compose arbitrary controls outside a bounded component registry.
- Encoding actions without consequence or reversibility metadata.
- Streaming rapid updates into live regions without batching.
- Treating accessibility as a QA pass instead of a schema and architecture concern.

---

## Recommended rollout path

1. **Baseline** — require semantic HTML, labels, keyboard operability, chart narration, and AI transparency labels on all new outputs.
2. **Structured metadata** — introduce consistent `data-englyn-*` semantics and receipt/provenance conventions where actions or generated insights matter.
3. **Schema-first components** — move reusable UI into slot-based, variant-driven, validated component contracts.
4. **Cross-modal expansion** — add voice summaries, haptic mapping, and spatial fallback models from the same semantic payload.
5. **Observability and policy** — measure accessibility health, hydration success, and agent composition reliability as ongoing product KPIs.

---

## FAQ

**Is ENGLYN a replacement for WCAG or ARIA?**
No. ENGLYN builds on WCAG, ARIA, and accessibility-tree semantics. It adds behavior, governance, provenance, and agent-readable meaning where current standards are thin — particularly around agent-mediated execution, delegated authority, interruption, recovery, and handback, where there's a real normative gap today.

**Do I need custom metadata on every page?**
No. Start with semantic HTML and strong accessibility basics. Add `data-englyn-*` metadata where action meaning, confidence, provenance, or behavioral phase would otherwise remain implicit.

**Can this apply to non-AI pages?**
Yes. The implementation patterns improve clarity, accessibility, and semantic quality for any digital output, even when no agent is directly in the loop.

**What's the shortest useful adoption path?**
Semantic structure, accessible names, chart summaries, live-region policy, and explicit action consequences. See `ENGLYN_QUICKSTART.md` in this directory.

---

## References

Public standards only — no internal or vendor-specific sources.

- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*
- W3C, *Accessible Rich Internet Applications (WAI-ARIA) 1.2* and the *ARIA Authoring Practices Guide (APG)*
- W3C, *Authoring Tool Accessibility Guidelines (ATAG) 2.0*
- European Union, *Artificial Intelligence Act*, Article 50 (transparency obligations for AI system providers and deployers)
- European Union, *European Accessibility Act (EAA)*, Directive (EU) 2019/882
- ETSI/CEN/CENELEC, *EN 301 549* — Accessibility requirements for ICT products and services

---

*Wax+Wires — Authored Intelligence. Companion doc: `ENGLYN_QUICKSTART.md`.*
