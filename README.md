# Englyn

**A draft specification for making digital output interpretable by two readers
at once: a person and an agent.**

The patterns that make work usable for humans across modalities are the same
ones that make it interpretable and safe for software agents. The disability
community wrote the specification for agent-reliable systems fifteen years
early and filed it under a different name.

Englyn is an attempt to write that down as something an engineer can ship and a
machine can check.

- **Canonical:** <https://waxandwires.com/englyn/>
- **Source of record:** <https://github.com/waxandwires/englyn>

Both are always referenced together. The site is where the specification is
read; the repository is where it is versioned, diffed, and argued with.

---

## Read this before anything else

**This is a draft by one author, and no disabled reviewer has read it.**

No rule here has been tested with a screen-reader user. Every rule is a
hypothesis held by its author, and the ones most likely to be noise are marked
as such. The reference implementation is the author's own site — one codebase,
one content type, one set of design decisions. **n = 1.**

`spec/UNVERIFIED.md` is the full account: every claim this specification cannot
currently check, why it cannot be checked, and what would settle it. It is not
an appendix. Read it as part of the specification, because a specification that
publishes only what it can verify is implicitly claiming the rest passed.

**Defects are wanted, including defects in that file.**

---

## The five marks

| mark | what it asks of an interface |
|---|---|
| **Observable** | Everyone extracts the same meaning — sighted reader, assistive-technology user, agent |
| **Verifiable** | Every output and action can be explained afterwards |
| **Explicit** | Actions are declared and consequence-labelled, never ambiguous |
| **Recoverable** | Partial states stay valid; the user is never trapped |
| **Typed** | Structure is machine-readable, not inferred from prose |

Beneath the marks sit six behavioural primitives — `perceive`, `act`,
`announce`, `audit`, `interrupt`, `oversee` — carried in markup as
`data-englyn-primitive`. `spec/VOCABULARY.md` is the normative source for those
attributes and their permitted values.

---

## Three verdicts, never two

**CONFORMS · FAILS · CANNOT-CHECK.**

Most conformance tooling returns two, which means an instrument that could not
run reports the same result as one that ran and found nothing. Englyn treats
those as different answers, because for a reader they are different answers.

A clean automated run is a **floor, not a certification**. Automated checks
cover 30–57% of WCAG issues depending on methodology, and **0 of the 10
narration rules** in this specification.

---

## Conformance tiers

Two are defined; one is deliberately not.

- **Bronze — structurally sound.** Static lint, schema validation, and
  automated accessibility checks all pass with zero violations.
- **Silver — operable end to end.** Bronze, plus keyboard-flow verification.
- **Gold — verified by lived experience.** A destination, not a specification.
  It requires recorded assistive-technology verification with paid community
  participation, it cannot be self-certified, and **it is published as an open
  invitation to help define it** rather than as a rule handed down.

**Tier names never appear naked** — always "Bronze — structurally sound", never
"Bronze". A bare tier name reads as a verdict on usability, and it is not one.
`spec/TIERS.md` has the full definitions and the reason that rule exists.

These are Englyn's names. **They are not a W3C claim, and no mapping to WCAG 2.2
or EN 301 549 is asserted.**

**This project's own reference implementation is currently UNKNOWN, not Bronze.**
Two of the required test layers have never run. A standard that publishes a
ladder it has not climbed should say so.

---

## What is here

| path | what it is |
|---|---|
| `spec/UNVERIFIED.md` | Every claim this specification cannot check, with what would settle each one |
| `spec/VOCABULARY.md` | The normative `data-englyn-*` attributes: names, value enums, obligations, and which reader each serves |
| `spec/TIERS.md` | Bronze, Silver, Gold — what each requires, the layer stamp, and what a tier claim is not |
| `implementation/ENGLYN_IMPLEMENTATION_GUIDE.md` | Engineer-facing: semantic model, ARIA by output type, action-safety tiers, rollout path |
| `implementation/ENGLYN_QUICKSTART.md` | The shortest adoption path, with a before/after snippet |
| `testing/ENGLYN_TESTING_PROTOCOL.md` | The six test layers, what each catches, and what each cannot |
| `testing/ENGLYN_ACCEPTANCE_CHECKLIST.md` | The runnable pre-publish gate |
| `testing/axe-integration-example/` | A worked automated-check integration |
| `measurement/ENGLYN_MEASUREMENT_SCHEMA.md` | Turning adoption into evidence: aggregate, non-fingerprinting |
| `measurement/englyn_schema.sql` | The schema behind it |
| `measurement/ENGLYN_TRANSPARENCY_REPORT_TEMPLATE.md` | Publishing that evidence, including when it is unflattering |
| `tools/spoken_number.py` | A converter for digit strings that are ambiguous to speech synthesis. Its output belongs in prose or `aria-describedby`, never in an accessible name |

`spec/SPEC.md`, a conformance checker, and a reference implementation are named
in the publication manifest and **are not written yet**. They are listed there
rather than omitted, so their absence is a declared state and not a silence.

---

## Co-review: an open invitation

**Englyn needs reviewers who use assistive technology daily, and it does not yet
have any.**

The invitation is unpaid, and that is stated plainly rather than dressed up.
There is no money coming in, so there is no money going out. **No date is set,
because a date would be a promise this project is not in a position to keep** —
and an earlier draft of this file published one, which is exactly the defect
this paragraph replaces.

What stands in place of a date is an obligation with no exit: **any rule the
first co-author calls noise is removed in the next release**, and the removal is
published under their name if they want it there.

**Gold tier keeps its paid-participation requirement.** That requirement is what
makes it honest — the tier does not exist yet, and the rate becomes a live
question when Gold moves from declared to defined, not before.

### What this author covers first-hand, and what he does not

The neurodivergent reading of the problem is **direct experience**. The case for
compressed text, variable length, and non-linear topology is written from inside
AuDHD experience. Agent-consumer needs are covered directly too.

**Screen-reader experience is not.** Englyn's testing is
assistive-technology-shaped, and that is a different lived experience.

This is stated so a blind reviewer can see exactly what they would bring that
the author cannot. Citation is not co-authorship, and this specification stands
on fifteen years of work by people who are not in the room.

---

## Reporting a defect

Open an issue on this repository. Every report is answered — here or in the
changelog — applied or refused, **with the reason given either way**.

---

## Licence

The specification text is **CC BY 4.0** (see `LICENSE`).

The conformance checker is **Apache-2.0** and lives in a separate repository.
The split is deliberate: no dual-licensing inside one tree, so nobody has to
work out which licence governs which file.

---

*The disability community solved the observation problem before the AI industry
knew the problem existed. The work now is to use what they built.*
