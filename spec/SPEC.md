---
title: "Englyn"
subtitle: "A conformance standard for interfaces read by people and by agents"
version: 0.1.0-draft
status: DRAFT ... awaiting the author's final pass
author: Micah Eberman
license: CC-BY-4.0
canonical: https://waxandwires.com/englyn/
source: https://github.com/waxandwires/englyn
created: 2026-08-18
---

# Englyn

## §0: Why this exists

Anyone handed meaning they did not author gets the receipt and keeps the pen.

A blind reader. Deskless hands. An agent acting for you. None of them wrote the
page. All of them are being asked to act on it. Every one of them deserves to know
what they are looking at, what will happen if they act, and whether the thing that
told them is telling the truth.

That is the whole argument. The rest of this document is what it takes to keep it.

### The uphill part

For twenty-five years the case for accessibility has been made on the right
grounds and moved at the wrong speed. It is a moral argument, it is correct, and
it has been losing on schedule. Ship dates win. Accessibility gets a ticket, the
ticket gets a sprint, the sprint gets cut, and the person who cannot use your
product is still not using your product.

Nobody reading this needs another appeal to conscience. You have heard it. You
probably agree with it. It has not been enough on its own.

**But it was never nothing, and that matters to what comes next.** Twenty-five
years of that argument built the accessibility tree, ARIA, the semantics in your
framework, and the standard we are about to credit. The floor exists. It was laid
by people who kept arguing while they were losing, and **the reason this
specification can be short is that they already did the long part.**

What has been missing is not the case. It is the momentum.

### What changed

Software is now being used by things that cannot see.

An agent hitting your interface has the same problem a screen reader user has had
since 1999. It cannot see your layout. It cannot infer meaning from position. It
cannot tell that the red button is dangerous because the red is a color and the
color is a pixel. It needs the structure stated, not implied.

That is not a coincidence and it is not a metaphor. **It is the same requirement,
arriving with a budget attached.**

The disability community solved this problem fifteen years early and filed it
under a different name. Semantic structure. Stated relationships. Announced
consequences. Predictable order. Every technique the agent era is now inventing
under new branding was built by people who needed it to get through a Tuesday.

So this specification is not a favor to anyone, and it is not a scolding either.
**It is the observation that the thing you now need commercially is the thing they
needed all along, and that building it once serves both.**

That is a rare thing and worth naming as good news. Most of the time doing right
by people costs you something and you do it anyway. **This is the other kind: the
work that makes your product survive contact with an agent is the same work that
makes it usable by someone who cannot see it.** You do not have to choose. You
were probably going to build half of it regardless.

**So take the ride, and take the credit for showing up.** Then find out who was
already here, because they left you notes.

### POUR already covers most of this, and it should be said plainly

If you have not met it: **POUR** is the organizing principle underneath the Web
Content Accessibility Guidelines, the W3C standard the world already uses. Four
words. Content must be **Perceivable**, **Operable**, **Understandable**, and
**Robust**. It has been the floor since 1999, it is a genuine achievement, and it
was written by people who did the work before any of this was fashionable.

Englyn has five marks. **Four of them are POUR, restated for a consumer POUR was
not written for.**

| Englyn | POUR ancestor | the question, asked about an agent |
|---|---|---|
| **Observable** | Perceivable | can it find the thing at all |
| **Recoverable** | Operable | can it interrupt, undo, or back out |
| **Explicit** | Understandable | can it tell why that happened |
| **Typed** | Robust | does it work with what the consumer actually runs |

**We are not claiming those four.** They are POUR's, they hold, and a page that
satisfies WCAG has most of Englyn already. If you have done accessibility work,
you are further along here than you expect.

### The fifth mark, which is the reason this document exists

**Verifiable.** A consumer must be able to check a claim, not merely receive it.

POUR has no verification principle, and that is not an oversight. **POUR was
written for documents, and documents make no claims.** A page that says "Contact
Us" is not asserting anything you could be wrong about. It is text. You read it or
you do not.

An interface an agent acts on is not a document. It is a **transaction**. When
markup says an action is safe, reversible, complete, or finished, that is a claim
with consequences, and the consumer needs a way to check it rather than trust it.

The field has largely missed this, and the miss has a name: it **conflates
descriptive user-interface markup with actionable, verifiable transaction
semantics.** Accessibility trees were built so a screen reader could describe a
screen to a person who would then decide. They were never built to let an
autonomous consumer confirm that what it was told is true. A description is
adequate when a human is in the loop to catch the lie. It is not adequate when
nothing is.

**That is the gap Englyn is for. One mark, not five.**

And it appears to be open. Two independent research passes, one of them
adversarially prompted to prove the opposite, both concluded that **no existing
work makes consumer-side agent standardization redundant**: ARIA, the
Accessibility Object Model, Web MCP, C2PA, and W3C PROV each address a different
layer. Plenty of work is happening on the **producer** side, where the agent is
being built. This is the other end, where the agent has to read something somebody
else made.

### Why an unverified marker is worse than no marker

In 2002 the W3C published P3P, a privacy specification. Internet Explorer checked
that a policy string was **present**. It never checked that the policy was
**true**. So sites shipped a string, the check passed, and the behaviour never
changed. Google's read, in production, for years:

```
P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
```

The check passed. P3P was formally obsoleted in 2018.

**Presence is not conformance.** Any standard that can be satisfied by declaring
something will be, and the declaration will be false, and the tooling will report
success. This specification is built to be checkable for that reason and no other.

### One example, from this site, measured

Every heading on this page was written in sentence case: `What this buys us`. CSS
made them display as capitals. Correct source, correct rendering, and a defect:

**WebKit hands the style-transformed text to the accessibility tree.** So VoiceOver
received `US` and read the country. *"What this buys U-S."*

The automated checks at the time: **axe reported zero failures. html-validate
passed. Englyn's own checker passed. The DOM was impeccable.** Four layers of
automated testing, all green, on a page a screen reader was mispronouncing.

**It was found by listening.** By running a screen reader against the site for the
first time and writing down what it actually said.

That is the argument for Verifiable in one concrete case, on our own work, and it
is why the tiers in this specification are honest about which of them a machine can
grant and which it cannot.

### What is wrong with this specification, on the first screen

This is version 0.1.0 and it has not earned your trust yet. The limits ship in the
same release as the claims, because a standard about verifiable claims that hid its
own would be self-refuting.

- **No external review.** No standards body, no working group, no independent
  audit.
- **No disabled reviewer has read this.** The neurodivergent reading of the problem
  is first-hand, written from inside AuDHD experience. **Screen-reader experience
  is not.** That is a different life and this document does not speak for it.
- **The reference implementation does not reach the top tier**, and cannot, by
  design. See §Tiers.
- **Disability Justice is a framework this specification set out to be answerable
  to, and does not satisfy.** It is answerable to Disability Justice; it does not
  speak for it.
- **Every unverified assumption is enumerated**, with what would settle each one,
  in `spec/UNVERIFIED.md`. Read it before you rely on anything here.

**If you are looking for a reason to dismiss this, that file is the shortest route
and we wrote it ourselves.** We would rather you find the gap there than in
production.

### What this specification is, and is not

**It is** a set of properties a conforming interface must have, stated
independently of how anyone builds one, so that a stranger can conform without
adopting our process.

**It is not** a replacement for WCAG. It is not a certification. It is not a
product. There is nothing to buy, and the validator is open.

**And it is not finished.** The top tier is deliberately unspecified: reaching it
requires recorded verification with paid participation from disabled reviewers, and
that cannot be defined without them. **That section is an invitation, not a
specification.** If you do this work, it is yours to help write.

Nothing about us without us is a demand, not a courtesy. This document is written
by someone inside one part of that "us" and outside most of it. **The correct
response to that is not to claim more, it is to leave the door open and say which
side of it you are standing on.**

---

## §1: Vocabulary

> Normative. See `spec/VOCABULARY.md` ... eleven attributes, value spaces, marks
> carried, and obligations. To be folded in from the extraction and the register.

## §2: The five marks

> Normative. Written from `spec/EXTRACTION-2026-08-17.md` and the decision register, with
> obligations ruled by Micah on 2026-08-19 (`spec/BALLOT-MUSTSHOULD-125-ROWS.md`).

### How to read this section, and what is deliberately not in it

**This section is short on purpose.** One hundred and twenty-five requirements were
extracted from this project's own working documents. Fourteen are here. The rest were ruled
out, and where they went matters more than the count:

**Requirements that restate WCAG, WAI-ARIA or the APG are cited, never renumbered.** Colour
not being the sole carrier of meaning, keyboard reachability, a visible focus ring, `alt`
attributes, contrast floors, `<label for>`, Escape closing a modal: **those are WCAG and APG
requirements and they already have a standards body, an enforcement ecosystem, and
twenty-five years of tooling behind them.** Renumbering them here would claim credit for a
floor other people built. A conforming page satisfies them **as WCAG**, cited to the
specific success criterion.

**Requirements on the conformance instrument are in §4**, not here. §2 governs what a page
must do. What a *checker* must do is a separate contract.

**Attribute value spaces are in `spec/VOCABULARY.md`**, which is normative and already
carries its own obligations. They are cited here, never restated. A requirement duplicated
across two files is two contracts that will disagree.

**And the reference implementation's house rules are not requirements.** Essay structure,
metadata conventions, and this project's internal naming discipline are enforced in its own
repository. **A standard that requires your document structure is not a standard.**

---

### 2.1 The floor: no tooling is required

**A conforming page MUST be achievable by hand-authored markup.** No build step, no design
system, no framework, and no dependency on this project's validator or on any other.

This is first because it is the difference between a standard and a product. Every
requirement below is satisfiable by typing attributes into HTML in a text editor. If a
requirement in a future version cannot be met that way, **the requirement is wrong.**

### 2.2 Observable

**A conforming page MUST carry `data-englyn-role` and `data-englyn-primitive` on every
meaningful region.** Value spaces: `spec/VOCABULARY.md`. A region is meaningful if a
briefing of the page would name it.

**A conforming page MUST order its DOM and reading order independently of its visual
order:** title, then narration, then highest-priority content, then supporting detail, then
actions. Visual arrangement is a rendering; reading order is the payload.

**A conforming page SHOULD be comprehensible to someone who cannot see it.** Specifically:
a person who hears the page rather than seeing it can tell what it is, what matters most,
and what to do next.

**This is the only requirement in this specification that no instrument can settle**, and it
is stated as SHOULD for that reason rather than softened. It is also what every other
requirement here is for. A page satisfying all the others and failing this one has satisfied
the letter of a standard whose point it missed.

### 2.3 Explicit

**A conforming page MUST NOT state a control's consequence only in that control's visible
text.** The consequence MUST also be present in the control's accessible name or
description. Visible text is one rendering of the page; it is not the page.

**A conforming page MUST carry a non-empty `data-englyn-consequence` on every control whose
activation changes state, and that value MUST be mirrored in the text of the control's
`aria-describedby` target.** A consequence declared only in an attribute is available to an
agent and withheld from the person using a screen reader, which inverts this
specification's purpose.

### 2.4 Recoverable

**A conforming page MUST record whether an action is reversible rather than leaving it to be
inferred.** Reversibility is carried by `data-englyn-primitive="interrupt"` and, where a tier
is declared, by the declared tier.

The reason this is a MUST and not a SHOULD is mechanical. **A consumer that infers
reversibility from prose is parsing English to decide whether something is safe**, and a
prose pattern can be accidentally wrong: correct wording, wrong pattern, wrong answer.
**Nobody accidentally declares an action reversible.** Declaring it moves the failure from
the instrument to the claimant, which is the trade a conformance standard should always want.

**A conforming page MUST declare an action-safety tier on every interactive control whose
activation is not read-only.**

### 2.5 Typed

**A conforming page MUST emit only values inside the published value space for each
`data-englyn-*` attribute**, per `spec/VOCABULARY.md`, and **a conforming checker MUST
validate value membership rather than attribute presence alone.**

Presence-only validation is the failure this specification was built against. A marker
nobody checks will be shipped, it will be wrong, and the tooling will report success.

**A conforming page MUST carry its `data-englyn-*` attributes in the live DOM after
hydration, not only in pre-hydration source.** A framework that renders the attributes away
has produced a page that passes a source reader and fails every consumer.

**A conforming page MUST NOT use a live region as its narration block.** The narration
region is a heading. It carries no `aria-live` and no landmark role, because content present
at load is not an update and announcing it as one interrupts the reader it was written for.

### 2.6 Verifiable

**A conforming page MUST carry `data-englyn-receipt` with a durable identifier on every
action that writes to an external system.**

**Where any `data-englyn-*` value carries meaning for a person, that meaning MUST also be
present in the node's accessible name or description.**

This is the load-bearing requirement in the whole specification, and it is the one most
easily lost. **Every attribute this standard adds is invisible to a screen reader by
default.** An implementation that puts operation semantics in attributes and stops has built
a channel for agents and left the person using assistive technology with the worse page.
**Then the standard has made things worse for the people it was written for**, which is not
a hypothetical failure mode: it is the obvious one.

**Wherever `data-englyn-source`, `data-englyn-confidence` or `data-englyn-receipt` are
described, in specification text, documentation, or user-facing copy, they MUST be described
as self-asserted and unsigned.** They are not provenance. They are not attestation. They are
not signed, and nothing in this specification verifies them cryptographically.

**A receipt in this specification is a claim by whoever wrote the page.** It is checkable in
the sense that a reader can go and look; it is not checkable in the sense that a signature
is. **Allowing these attributes to be read as attestation would build the exact trap this
specification exists to name**, and it would be worse than P3P, because P3P at least never
claimed to be signed.

---

### What §2 does not cover, stated here rather than left to be discovered

**Voice and spoken agents.** Turn-taking and idle-timeout requirements are unowned by this
version. The research is clear that typical five-to-ten-second cutoffs truncate stuttered,
Parkinson's, ALS and older speech, and that AAC users need longer. **This specification does
not yet govern a spoken agent, and it should not be cited as though it does.**

**A confirmation ceiling for Explicit.** Requiring per-action confirmation can itself be an
accessibility failure, and this specification currently requires consequence declaration
without bounding how often a consumer should ask. **The contradiction is disclosed in
`spec/UNVERIFIED.md` and not resolved.** Deferring the solution is legitimate. Deferring the
disclosure would not have been.

**CLI, TUI, and any surface without an accessibility tree.** Every requirement above assumes
a document with an accessibility tree. **On surfaces without one, this specification is
unproven and possibly wrong.**

## §3: Conformance and tiers

> See `spec/TIERS.md`. Bronze and Silver defined; Gold declared, not defined.

## §4: What a CONFORMS warrants

> DRAFT, from the liability ruling of 2026-08-17, awaiting a final pass. This
> section is not legal advice and its author is not a lawyer.

**"When a receipt says CONFORMS and it doesn't, who is liable?"**

That is the first question a careful buyer or practitioner asks, and a
specification that leaves it implicit has left its sharpest reader to write the
answer for us. So it is written here.

### A conformance verdict is a claim by a person, not a fact about a page

**Englyn does not certify anything.** There is no certifying body, no registry, no
audit, and no badge anyone issues. **Every verdict in this specification is
asserted by whoever ran the instrument**, and the specification's job is to make
that assertion precise enough to be checked by someone else.

So a verdict always names three things, and a verdict missing any of them warrants
nothing:

**Who is claiming.** An implementer self-asserting about their own work, or a
third party attesting about someone else's. Those carry different weight and must
never be reported in the same form.

**At which layer.** L1 static markup · L2 schema · L3 automated audit · L4 keyboard
flow · L5 observed assistive technology. **A claim is bounded by the layer that
produced it and says nothing about the layers above it.**

**On what date, against which build.** A conformance run measures the artefact in
front of it. It expires the moment the artefact changes, and a verdict without a
build identifier is a verdict about nothing.

### What CONFORMS does warrant

**That a named instrument ran, on a stated date, against a stated build, and found
no violations of the requirements at that layer, and that everything it could not
determine is published alongside.**

That is a narrow claim and it is deliberately narrow. It is also checkable: a
stranger can re-run the instrument and get the same answer, which is the only
property that makes a conformance claim worth anything.

### What CONFORMS does not warrant

- **Not that the interface is usable.** Bronze and Silver are claims *about
  testing*, not about experience. **Only Gold claims a human found it usable**, and
  Gold cannot be self-certified.
- **Not that it is accessible to any particular person.** No instrument in this
  specification, and no combination of them, can establish that.
- **Not WCAG conformance.** Englyn is not a WCAG conformance mechanism. A page can
  satisfy Englyn and fail WCAG, and the reverse.
- **Not legal compliance**, in any jurisdiction, under any statute. If you need
  that, you need counsel and an audit, and this specification is neither.
- **Not that the layers above the claimed one would pass.** A Bronze page has not
  been near a screen reader.

### The asymmetry that keeps this honest

**A CONFORMS is a weak claim. A FAILS is a strong one.**

An instrument that finds a violation has found something real: it can point at the
element and the requirement. An instrument that finds nothing has only established
that *it* found nothing, which is a fact about the instrument as much as the page.

**This specification was written because four instruments reported clean on a page
a screen reader was mispronouncing.** `text-transform: uppercase` reached WebKit's
accessibility tree, and *"What this buys us"* was spoken *"What this buys U-S."*
axe: zero violations. `html-validate`: pass. Englyn's own checker: pass. The DOM:
correct. **It was found by listening, and by nothing else.**

Treat every CONFORMS in this specification with that example in mind.

### Where the liability actually sits

**With whoever made the claim.** If an implementer self-asserts Bronze and the
page has a defect at that layer, the implementer asserted something false. If a
verifier attests and is wrong, the verifier is wrong. **The specification asserts
nothing on anyone's behalf and cannot be cited as a warranty by either party.**

And the corollary, which is the reason `UNVERIFIED.md` exists: **an instrument's
published scope limits are its liability limits.** A verdict that hides what it
could not check has widened its own exposure, not narrowed it.

## §5: Limitations

> See `spec/UNVERIFIED.md`. Referenced from §0 deliberately, not deferred to the
> end.
