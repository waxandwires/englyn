# VOCABULARY

**The single normative source for `data-englyn-*` attributes.** Where any other
document in this specification names an attribute, a value, or an enum, this
file governs and that document is derivative.

**Status:** created 2026-08-18. Applies to v0.1.0-draft. Normative except where
an entry is explicitly marked *reserved* or *proposed*.

---

## Why this file exists

Before it, three documents defined **six** attributes between them, the
reference implementation emitted **eight**, and the only document defining all
**eleven** with value sets was a skill reference that no published manifest
listed. A *published* test asserted an attribute that no published document
named.

That is not a documentation gap. It is a **truth defect that no leakage gate can
see**, because every attribute in every one of those files is spelled correctly.
A checker that validates presence and not membership cannot see it either. This
file and the membership criterion below are the two halves of the fix.

---

## The membership criterion

> **A conforming page MUST NOT emit a `data-englyn-*` value outside the
> published enum, and a conforming checker MUST validate value *membership*, not
> merely attribute *presence*.**

An attribute whose values are unconstrained is a free-text field wearing a
schema's clothes. Presence-only validation is how `orientation` reached a
selftest fixture and how `operate` reached an essay: nothing was ever going to
object.

Free-text attributes — `consequence`, `receipt` — are exempt **by declaration**,
not by omission. Their entries below say so, and a checker must treat "free
text" as a declared value space, never as an absent one.

---

## The four groupings

The eleven attributes are not one flat set. Three of them describe an
**operation**, two describe **document structure**, two describe **annotation
provenance** — and one belongs to none of those, because it does something none
of them do.

| grouping | attributes | what it describes |
|---|---|---|
| **Operation semantics** | `primitive` · `consequence` · `receipt` | what the region *does*, what happens if you act on it, and what trace that leaves |
| **Document structure** | `role` · `priority` | what kind of region it is and where it sits in the briefing order |
| **Annotation provenance** | `source` · `state` | where the annotation came from and how current it is |
| **Routing** | `consumer` | who the annotation is *for* |

**`consumer` is the load-bearing one.** It is the two-reader thesis made
machine-readable: it is the only attribute that declares an annotation's
audience rather than its content, and it is the only mechanism by which a page
can say *this text is for the agent, not for the person listening.* Without it,
every agent-facing annotation is either spoken to a human who did not ask for it
or hidden from an agent that needed it. The rest of the vocabulary describes the
page. `consumer` describes the contract.

The remaining three — `severity`, `confidence`, `value` — are **reserved** and
are not grouped, because a grouping is a claim about a thing's role, and these
have not earned one. See *Reserved*.

---

## Normative attributes

Each entry gives: **value space · mark carried · obligation · consumer served ·
measured use.** "Measured use" is the count in the reference implementation's
source at 2026-08-18, with its denominator: **56 of 56 text files under
`site/src` scanned**, one binary (`.DS_Store`) excluded and declared.

### `data-englyn-role`

- **Values (CLOSED, ruled by Micah 2026-08-18 — amended, see below):**
  `narration` · `section` · `action` · `status` · `citations` · `run-out` ·
  `media` · `collection` · `disclosure` · `hero` · `banner` · `bio` · `card`
- **Reserved, not specified:** `alert` · `stat` · `chart` — named so nobody else
  claims them; **zero uses, so not shipped contracts.**
- **Mark:** Observable
- **Obligation:** SHOULD on any region a briefing would name. MUST on the
  narration block (Rule 7) and on any region carrying `priority`.
- **Consumer:** agent, primarily. It is a *region taxonomy*, deliberately not a
  widget taxonomy — that is what ARIA `role` already is, and duplicating it
  would be the worst kind of extension.
- **Measured, 2026-08-18, all 17 values in use:** `section` 63 · `action` 18 ·
  `narration` 16 · `citations` 3 · `status` 2 · `run-out` 2 · `media` 2 ·
  then eleven singletons: `receipt` `profile` `log` `hero` `error` `disclosure`
  `collection` `card` `bio` `banner`.

> ### ⚠ AMENDED 2026-08-18 — the enum was both too wide and too narrow
>
> **The ruling stands: `role` is CLOSED.** The deciding rule settles it —
> *closed when a consumer branches on it* — and agents route on `role`. An open
> region taxonomy is not a taxonomy, it is a comment field. The earlier OPEN
> call is retracted, for the right reason: *a value used once is not a shipped
> contract, it is unreviewed accretion.*
>
> **But the first enum was not built from measurement.** Measured against
> `site/src`: **seventeen values are in use, not ten.** The original enum
> **specified three values nothing emits** (`alert`, `stat`, `chart`) — which is
> the exact `severity`/`confidence` defect ruled against one attribute over,
> *never publish vocabulary whose only demonstration is absent* — while
> **excluding ten values the site ships today.**
>
> **The ten exclusions are three different kinds of thing, which is why one enum
> could not hold them:**
>
> | | values | ruling |
> |---|---|---|
> | **Genuine regions** — what a briefing would name | `media` `collection` `disclosure` `hero` `banner` `bio` `card` | **admitted to the enum** |
> | **Content types, not regions** | `receipt` `log` `profile` | **misuse — correct the markup.** `receipt` also collides with the `data-englyn-receipt` attribute |
> | **A state, not a region** | `error` | **misuse — belongs with `status`, or in `state`** |
>
> Thirteen values, every one measured and shipping. **A closed enum should fail
> only genuine mistakes** — this one now does, and the four misuse values are
> markup defects the checker surfaces rather than vocabulary the spec absorbs.
>
> **Second correction, same day, caught by running the checker rather than
> reasoning about it.** `card` was first placed in *Reserved* on the argument that
> a single use is not a shipped contract. **That was wrong: it ships on the
> homepage** (`src/pages/index.astro`), and Reserved means *named, not specified*,
> which makes a live value FAIL. A value cannot be both reserved and in
> production. **Admitted.** The rule holds — one use is not a contract — but it
> decides whether a value is *reviewed*, never whether it is *live*.


> **Singleton values are a finding, not a specification.** A value used once is
> indistinguishable from a typo, and a checker enforcing membership now says so.
> **But the fix is a decision per value, not a blanket fail** — the amendment above
> rules each of the eleven: **seven were genuine regions and are admitted**
> (including `card`, corrected on the second pass), and four were misuse and stay
> out so the checker surfaces them as markup defects. **A singleton outside the
> enum FAILS, which is the
> correct outcome** — it forces a decision rather than letting vocabulary accrete
> silently. What it must not do is let the enum accrete either: three values
> nothing emits were specified before anyone counted.

### `data-englyn-primitive`

- **Values:** `perceive` · `act` · `announce` · `audit` · `interrupt` ·
  `oversee` — **exactly six, closed.**
- **Mark:** all five. This attribute is how the marks reach the markup.
- **Obligation:** MUST on any region carrying `role`.
- **Consumer:** author discipline first, agent second.
- **Measured:** 113 uses. `perceive` 80 · `act` 20 · `audit` 7 · `announce` 2 ·
  two bare · one template expression.

> **`interrupt` carries Recoverable, and it has been emitted zero times.**
> That is the whole of Recoverable's evidence in the reference implementation.
> Zero uses on n=1 is **UNKNOWN** — it is not evidence that the mark is
> unnecessary and it is not evidence that the standard is incomplete. It is one
> site, of one content type, that happens to have no interruptible flow.
> `spec/UNVERIFIED.md` must carry this as an entry; a mark whose only carrier
> has never fired is exactly the kind of claim that reads as verified by
> omission.
>
> Matching this token MUST be exact. `interact` and `react` both contain
> `act`, and a substring match makes them actions.

### `data-englyn-priority`

- **Values:** positive integers, 1 = highest. Within a `role` group, the
  sequence MUST be `1..n` with no gaps and no repeats.
- **Mark:** Observable
- **Obligation:** SHOULD generally; MUST on essay `<h2>` sections.
- **Consumer:** agent (briefing order), and the human via the Rule 7 narration
  prose that reads from it.
- **Measured:** 73 uses.

### `data-englyn-consequence`

- **Values:** **free text, by declaration.** A plain-language statement of what
  acting on this region does.
- **Mark:** Explicit
- **Obligation:** MUST on any region whose `primitive` is `act`.
- **Consumer:** the AT user via `aria-describedby`, and the agent.
- **Measured:** 20 uses.

> The consequence text MUST be reachable by the human, not only by the agent —
> mirrored into the region's own text, its accessible name, or an
> `aria-describedby` target. An agent-only consequence is a two-track page, and
> a two-track page fails Observable for the reader who cannot see the second
> track. The one exemption is a named link whose consequence is plainly
> navigational and read-only: its accessible name already carries the
> destination, and mirroring it into every navigation link is the speech noise
> this rule exists to prevent.

### `data-englyn-consumer`

- **Values:** `assistive-technology` · `agent` · `both`
- **Mark:** Explicit
- **Obligation:** MUST on any annotation whose intended audience is not both.
  An annotation with no `consumer` is `both` by default, and a page that means
  "agent only" and does not say so has published to the wrong reader.
- **Consumer:** the routing layer itself.
- **Measured:** 19 uses. `assistive-technology` 17 · `both` 2.

> `agent` is in the enum and has **zero measured uses.** Same verdict as
> `interrupt`: UNKNOWN on n=1, not absent. It is retained because the value
> space must be symmetric — a router that can say "AT only" and "both" but not
> "agent only" cannot express the case the thesis is built on.

### `data-englyn-source`

- **Values:** `manual` · `generated` · `llm-draft` · `research-pipeline` ·
  `analytics` · `build-script`
- **`generated` added 2026-08-18.** The TTS pipeline
  (`DEC-WW-ENGLYN-TTS-VOICE-001`) stamps it on every synthesised reading, and it
  was **shipping in code before the enum carried it** — the code-ahead-of-spec
  divergence that produced blocker B3, recurring one day after B3 was ruled.
  Found by the membership check on its first real run, which is the check working.
- **Mark:** Verifiable
- **Obligation:** SHOULD on any region whose content was not hand-written.
- **Consumer:** agent and downstream trust systems.
- **Measured:** 5 uses. `manual` 4 (one via a ternary defaulting to `manual`) ·
  `build-script` 1.

> `build-script` was measured in the reference implementation and is **admitted
> here rather than quietly tolerated.** It was not in any prior enum. This is
> what membership validation is for: the value existed, nothing objected, and
> the only way it becomes legitimate is by being written down.
>
> A `source` value is **self-asserted and unsigned** — see `spec/UNVERIFIED.md`
> §7. It makes a claim legible; it does not make it true.

### `data-englyn-receipt`

- **Values:** **free text, by declaration** — a UUID or other durable
  identifier resolvable by the publisher.
- **Mark:** Verifiable
- **Obligation:** MUST on any `act` region whose `severity` is `high` or
  `critical`. Not required on T1 read-only regions.
- **Consumer:** auditor and agent.
- **Measured:** 1 use.

> **One use is the floor, not a shortfall.** Verifiable cannot exist without a
> receipt; an attribute at exactly one use is the minimum demonstration that the
> mark is carried at all. Recorded here so nobody reads the count as a defect
> and "fixes" it by sprinkling receipts onto regions that do not write anything.
>
> Self-asserted and unsigned, per `spec/UNVERIFIED.md` §7.

---

## Reserved

**A reserved attribute is named, not specified.** The name is claimed so that no
implementation invents an incompatible meaning for it; no conformance
requirement attaches, and a checker MUST NOT fail a page for omitting one. A
reserved attribute becomes normative only by being defined in this file.

| attribute | proposed value space | measured | why reserved |
|---|---|---|---|
| `data-englyn-severity` | `low` · `medium` · `high` · `critical` | **0** | Zero uses in the reference implementation. It is load-bearing in the measurement scanner's typed tier logic (see *Proposed*), so it is expected to become normative — but it is not specified on zero demonstrations. |
| `data-englyn-confidence` | `high` · `medium` · `low` · `unknown` | **0** | Zero uses **anywhere** — not in source, not in the build, and not in any fixture. It is named in six documents and instantiated in none. |
| `data-englyn-value` | number or string | **0 live** | Appears only in two example fixtures (`testing/axe-integration-example/fixture.html:11`, `skills/englyn-accessible-page/examples/before-after-snippet.html:46`). |
| `data-englyn-state` | `present` · `gap` · `partial` · `unknown` · `at-risk` | **1** (`at-risk`) | One use, one value, and the value space has never been exercised. See *Proposed* — `state` is where freshness belongs, and that is not yet ruled. |

> **Never publish vocabulary whose only demonstration is a test fixture.** That
> is the rule `value` is reserved under. A fixture demonstrates that a parser
> accepts a string; it demonstrates nothing about whether the attribute earns
> its place on a real page. `confidence` does not even have that — it is
> documented in six places and has never been written once.

---

## Two invented values, reported not admitted

Both were flagged for a rename-or-admit ruling. **Measurement changes one of
them**, so only one ruling is actually owed.

| value | attribute | status | evidence |
|---|---|---|---|
| `operate` | `primitive` | **NOT LIVE — no ruling needed** | Survives only inside an MDX build comment at `site/src/content/essays/nothing-found.mdx:320`, documenting a fix that was **already applied**. The rendered element emits `act`. Zero occurrences across 66 of 66 text files in the build output. |
| `orientation` | `primitive` | **LIVE in an unpublished fixture — ruling owed** | `testing/harness/selftest.py:26`. Not on the publication manifest, so it cannot leak; but the harness's own selftest demonstrates a value the standard does not define. |

**Recommendation for `orientation`:** rename to `perceive`. The fixture is a
narration block, and narration is the canonical `perceive` region — the value
was invented to name something the enum already covers. This is Micah's call;
it is recorded here so it is not re-derived a fourth time.

---

## Proposed — drafted, not ruled

Each of the following came from an instrument, not from reasoning. **MUST or
SHOULD is Micah's ruling; none is normative until he makes it.** A conforming
checker MUST return CANNOT-CHECK on these, never a pass and never a fail.

### `data-englyn-tier` — the reversibility carrier

- **Proposed values:** `T1` · `T2` · `T3`
- **Grouping:** operation semantics

Action tier is currently decided **two different ways by two instruments.** The
JavaScript checker infers it by regexing English prose
(`englyn-check.mjs:416`: `/read-only|nothing is (saved|sent)/i`); the Python
measurement scanner already decides it **the typed way**, from
`data-englyn-severity` (`englyn_baseline_scan.py:241-255`).

Align to the typed path. Do not invent `tier` from scratch — `severity` already
carries the signal, and a second mechanism for the same decision is how the two
instruments came to disagree in the first place.

> Carried verbatim, because the reasoning is the point: *a prose regex can be
> accidentally wrong — correct prose, wrong pattern. **Nobody accidentally
> declares T1.** The attribute moves the failure from the instrument to the
> claimant* — which is the trade a conformance standard should always want.

A checker implementing this MUST return **CANNOT-CHECK when `tier` and
`severity` disagree.** A conflict between two typed declarations is not a pass
and not a fail; it is an unanswerable question, and answering it either way
would be the false-pass shape this specification exists to refuse.

### `data-englyn-layer` — the density switch, made declarative

- **Proposed values:** `orienting` · `expert`
- **Grouping:** document structure

The mechanism the neurodivergent-access argument needs, and **the only honest
way to test it**: two renderings of one source, so a co-author can say which one
works for them. An argument for compressed text and variable length that ships
as a single fixed rendering has no way to be wrong, and a claim that cannot be
wrong is not a finding.

### Freshness in `state`

The receipt-currency law is a page-level property that was never written into
the vocabulary. **A stale receipt read as current is the false-pass shape one
level down** — the page is honest, the receipt is real, and the reader draws a
wrong conclusion anyway. It fired twice on 2026-08-18, across six essays.

Proposed: `state` gains a currency dimension, so a receipt can declare itself
stale rather than relying on a reader to check a date. Value space unruled.

---

## Notes for implementers

**`spoken_number.py` is deliberately not in the reading pipeline.** It was
rescoped, not abolished: it converts a digit string to spoken English for the
rare TTS-ambiguous case (a year read as a quantity, a phone number), and its
output goes into prose or `aria-describedby` — **never into an accessible name,
and never beside the digits.**

It is not wired into the text-to-speech reading pipeline, and it must not be.
Kokoro reads digits correctly in prose, so wiring it in would create **a second,
silently different number rule** — one governing accessible names and one
governing speech, diverging the first time either changed. Recorded here rather
than in a commit message so nobody re-wires it on the reasonable-sounding
grounds that a number tool belongs in a speech pipeline.

**Attribute values are testimony.** No attribute in this vocabulary is verified
by anything. `source`, `confidence` and `receipt` are self-asserted, unsigned,
and carry no mechanism by which a consumer can detect a false one. If you
consume them — particularly as an agent — you are trusting the publisher, not
the format.

---

## What this file governs

| document | relationship |
|---|---|
| `skills/englyn-accessible-page/references/englyn-narration-reference.md` | **Derivative.** It held the only complete enum table and was never on the publication manifest. Its table is superseded by this file. |
| `implementation/ENGLYN_IMPLEMENTATION_GUIDE.md` | **`pending` until it cites this file.** It publishes six of eleven attributes and omits `role`, `priority`, `value`, `state` and `consumer` — a smaller, contradicting set. |
| `measurement/ENGLYN_MEASUREMENT_SCHEMA.md` | **`pending` until it cites this file.** Same defect. |
| `measurement/englyn_schema.sql` | Derivative. Columns are boolean/count aggregates and define no enum. |
| `testing/ENGLYN_TESTING_PROTOCOL.md` | Its L2 schema fixture asserts `role` as `z.string().min(1)` — a shape constraint, not membership. Reconcile to the membership criterion. |
