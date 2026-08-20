# UNVERIFIED

**What this file is.** Every claim this specification cannot currently check,
named, with the reason it cannot be checked and what would settle it. It is
not a backlog and not an apology. It is the instrument declaring its own
scope.

**Why it exists.** Englyn returns three verdicts, never two: CONFORMS, FAILS,
CANNOT-CHECK. A specification that publishes only what it can verify is
implicitly claiming the rest passed. This file is where CANNOT-CHECK lives, so
that claim is never made by omission.

**How to read an entry.** Each one answers three questions and nothing else:
what has not been verified, why that matters to an implementer, and what would
settle it. A verdict carries the layer it was earned at; a pass at one layer
says nothing about the layer above it.

**Status:** created 2026-08-13, updated 2026-08-17. Applies to v0.1.0-draft.

---

## 1. No external review has been done, and no disabled reviewer has read this specification

**What is not verified.** Nothing in this specification has been reviewed
outside the group that wrote it. No disabled reviewer has read it. No rule in
it has been tested with a screen-reader user. Every rule is a hypothesis held
by its authors.

**Why this matters to an implementer.** If you adopt a rule here, you are
adopting an untested design decision, not a validated one. Rules that read as
settled practice are not settled practice. Where a rule turns out to be wrong,
the cost lands on your users before it lands on us.

**What would settle it.** A daily screen-reader user with authority over this
specification's text, credited on it, reads it and disagrees with it in
writing. No date is set for that, because a date would be a promise this
project is not yet in a position to keep. What stands in place of a date is an
obligation with no exit: any rule the first co-author calls noise is removed in
the next release, and the removal is published under their name if they want it
there.

*Recorded 2026-08-17.*

---

## 2. Assistive-technology verification (L5) covers one platform pair and only the pages actually run

**What is not verified.** L5 is the manual assistive-technology layer. It has
been run against one pair — VoiceOver on macOS with Safari — and only on the
pages named in the published run records. Five further consumers are
unverified: NVDA with Firefox on Windows, JAWS with Chrome on Windows,
Narrator with Edge on Windows, TalkBack with Chrome on Android, and a
refreshable braille display, which is not in the L5 matrix at all. This draft
has not been run against any of them.

**Why this matters to an implementer.** These are not six implementations of
one behaviour; they are four architecturally distinct consumers. NVDA and JAWS
build an off-screen virtual buffer and navigate that, with a browse mode and a
focus mode. VoiceOver has no decoupled buffer and works the live accessibility
tree directly. TalkBack traverses a node tree by touch. A braille display
reads a forty- to eighty-cell tactile window with no audio channel at all.
Virtual-buffer desync and browse-versus-focus-mode confusion are common failure
classes on the two screen readers with the largest desktop share, and they
**cannot occur on the one platform that has been tested**. The pair that has
been run is the architectural outlier, so the pass transfers to the others far
less than a six-row matrix of equal-weight rows implies.

**What would settle it.** A recorded run of each pair on its own platform, by
someone who uses that assistive technology daily and is compensated for the
expertise, with the failures published alongside the passes. Any claim made
before then carries the stamp `L-AT (VoiceOver on macOS)` and nothing broader.

*Recorded 2026-08-13, updated 2026-08-17.*

---

## 3. A failure that occurs only on an untested platform is structurally invisible to this project's test rig

**What is not verified.** That the absence of reported failures means the
absence of failures. The rig can only observe the platforms it can reach, and
per entry 2 that is one of six.

**Why this matters to an implementer.** The worked example is the WAI-ARIA 1.3
`ariaNotify` imperative notification API. Verified 2026-08-13: it ships in
Chrome, Edge, and Android; on Safari and iOS VoiceOver the announcement is
**not spoken at all**, with no error and no warning. One major browser engine's
published standards position is *defer*; another gave no signal. Independent
screen-reader testing published June 2026 concludes it is not production ready.
Three separate research documents in this project's own corpus recommended it,
without reservation, as the settled replacement for `aria-live`. Had it been
adopted, the notification layer would have been silent for every VoiceOver
user, and the L5 run would still have come back clean, because the declarative
fallback fires on the one platform that can be reached. The specific API is not
the finding. The general form is: this rig cannot detect a failure whose
distribution excludes the platforms it can test.

**What would settle it, for `ariaNotify` specifically.** WebKit shipping the
API, plus an independent screen-reader test confirming that the announcement is
actually spoken on Safari and iOS. Until then it is not adopted here, and the
live-region queue discipline documented in the implementation guide stands.
For the general form, entry 2 is the settlement.

*Recorded 2026-08-13.*

---

## 4. The L5 release gate is unmanned, not failing

**What is not verified.** Any self-certified verdict on the spoken experience
of a surface. An L5 VoiceOver run was performed on the reference implementation
on or about 2026-08-11. The outcome was that the reviewer could not reliably
distinguish good output from bad, and concluded he was the wrong person to be
judging it.

**Why this matters to an implementer.** L5 is a release gate and its verdict is
a human judgement. If the human making that judgement cannot make it reliably,
the gate is not failing — **it is unmanned**, and every surface that previously
passed it passed on an unqualified read. Treat prior L5 passes in this project
as unstamped.

**What would settle it.** A co-reviewer who uses the assistive technology daily
making the call, and scripted, research-based interactions recorded across
multiple platforms, locally and via hosted testing services, as a first pass
for obvious errors only. That first pass is not multi-audience testing and does
not stand in for it. Nothing about us without us.

*Recorded 2026-08-13.*

---

## 5. Test layers L2 and L4 have not run; L3 has run once and is advisory

**What is not verified.** Of the six declared test layers, only L1 (static
structure and semantic lint) actually blocks a build today. **L2 (schema
validation) and L4 (keyboard flow) are CANNOT-CHECK — they are declared, not
enforced, and have not run.** The only keyboard evidence in existence is a
modelled tab-order journey from the harness, which is a model, not an observed
run. L3 (automated accessibility checks) has been machine-tested once, on
2026-08-17, over localhost: **0 FAILS, 29 CANNOT-CHECK, 534 CONFORMS across 15
pages.** It is advisory and not wired into the build. An earlier run of the
same tool against a local file rather than a served page reported 18 FAILS;
that run audited an unstyled page and was retracted — recorded here so the retraction is as visible as the claim.

**Why this matters to an implementer.** A merge gate that says "blocks merge:
yes" in the protocol table is true only for L1 today. Automated checks cover
the WCAG floor and, depending on methodology, 30–57% of WCAG issues; they cover
**0 of the 10 narration rules** in this specification. The narration rules —
the part of Englyn that is not already WCAG — have no machine check at all and
cannot acquire one.

**What would settle it.** L2 and L4 wired into continuous integration and run,
with the records published; L3 gating rather than advising; and, for the
narration rules, entry 2 — there is no automated substitute.

*Recorded 2026-08-17.*

---

## 6. Named rules carry an untested status inside the specification itself

**What is not verified.** Individual rules are marked in place, and the marks
are load-bearing. Rule 1 (numbers, currency, and percentages) is a **design
hypothesis** with no user testing behind it. Rule 7's narration is **untested
with screen-reader users and may read as noise at power listening rates**. The
`Section N of M` progress markers are **untested**. The listening-rate figures
used to size the narration length are drawn from published medians, not from
observed sessions with this content.

**Why this matters to an implementer.** These are the rules most likely to
change or be removed. Implement them if you want the whole draft, but do not
build a product surface that breaks if one of them is withdrawn, and do not
cite them as established practice.

**What would settle it.** Sessions with screen-reader users at their own
listening rates, recorded, with the rule kept, revised, or removed on the
evidence and the outcome published either way.

*Recorded 2026-08-17.*

---

## 7. The provenance attributes are self-asserted and unsigned

**What is not verified.** That a `data-englyn-source`, `data-englyn-confidence`,
or `data-englyn-receipt` value is true. Nothing in this specification verifies
them. They are declarations made by the page author, carried in the markup,
with no signature, no countersignature, and no mechanism by which a consumer
can detect a false one.

**Why this matters to an implementer.** If you consume these attributes —
particularly as an agent — you are trusting the publisher, not the format. Do
not treat a confidence value as measured, or a receipt as proof. The attributes
make a claim legible and checkable by a human; they do not make it true.

**What would settle it.** A signing and verification mechanism, plus a defined
consumer behaviour for a signature that fails. Neither exists in v0.1.0-draft,
and until one does, every attribute value is testimony.

*Recorded 2026-08-17.*

---

## 8. Bronze, Silver, and Gold are Englyn's names, not a W3C claim

**What is not verified.** Any equivalence between these tier names and a
standards-body conformance level. Bronze / Silver / Gold here are
**Englyn-defined and WCAG-3-inspired. They are not a W3C claim.** Measured
2026-08-17: the WCAG 3.0 Working Drafts have used, dropped, and re-used these
names across 2021–2026, so the names in any given draft are not stable ground
to stand on. No W3C Recommendation is expected before roughly 2028.

**Why this matters to an implementer.** If you report an Englyn tier to a
customer, a procurement process, or a regulator, you are reporting this
specification's tier and nothing else. **No mapping to WCAG 2.2 or EN 301 549
is claimed** — that mapping waits until the L1–L5 layers have actually run.
Anyone reading a tier as a legal or regulatory conformance level is reading
something that was never asserted.

**What would settle it.** W3C ratification of the names, at which point this
entry is updated to say so; and, separately, a published mapping produced after
the test layers have run, not before.

*Recorded 2026-08-17.*

---

## 9. Gold cannot be self-certified

**What is not verified.** Any Gold claim made by the party that built the
surface, including this project's own reference implementation. Gold requires
verification the builder structurally cannot supply about their own work: the
observed assistive-technology record of entry 2 and the human judgement of
entry 4, neither of which is available to a self-assessment. Silver and Bronze
are self-assessable against the published checklist. **Gold is not.**

**Why this matters to an implementer.** A self-declared Gold badge is not a
conformance statement under this specification, whoever issues it. If you see
one, ask for the assistive-technology record it rests on. If there is no
record, the correct verdict is CANNOT-CHECK, and this specification says so
rather than letting the omission read as a pass.

**What would settle it.** An external verification path — an independent
reviewer, using the assistive technology daily, with the run record published
and attributable. That path does not exist yet, so **no Gold claim exists
either, including ours.**

*Recorded 2026-08-17.*

---

## 10. The reference implementation is n = 1

**What is not verified.** That any rule here generalises beyond the site it was
written against. The reference implementation is the author's own site. One
codebase, one content type, one author, one set of design decisions. Fifteen
pages have been machine-checked, once.

**Why this matters to an implementer.** Rules extracted from one site tend to
encode that site's shape. Anything here concerning content density, section
structure, or narration length may be an artefact of long-form editorial
writing rather than a property of accessible interfaces. Applied to an
application shell, a data table, or a transactional flow, some of it will be
wrong.

**What would settle it.** Independent implementations, by other people, on
other content types, reporting back what broke — and the report published
whether it flatters this specification or not.

*Recorded 2026-08-17.*

---

## 11. The disability model this specification operationalizes is unverified by the people it describes

**What is not verified.** Where the problem definition came from. Everything
here concerning blindness, low vision, deafness, and motor disability was
**inferred by the authors from the disability community's published work** —
curb-cut, POUR, ARIA and the authoring practices around it, and practitioner
writing in the research corpus. It did not originate with disabled
practitioners inside this project. The single exception is the neurodivergent
reading of the problem, which is first-hand: the case for compressed text,
variable length, and non-linear topology is written from inside AuDHD
experience, and is still untested with any other neurodivergent reader. Citation
is not co-authorship, and this entry exists so the two are not mistaken for each
other.

Two further limits belong here rather than in a footnote. **Disability Justice
is a framework this specification set out to be answerable to, and does not
satisfy. It is answerable to Disability Justice; it does not speak for it.** Its
ten principles include an explicit anti-capitalist commitment;
Englyn's public argument is a reliability-and-market argument. Those are in
tension, the tension is not resolved here, and claiming the framework while
making that argument would be exactly the appropriation this entry exists to
prevent. And **the social model does not account for everything this
specification touches** — pain, fatigue, and cognitive impairment are not
resolved by removing environmental barriers. You cannot ramp your way out of
chronic fatigue, and several cognitive-accessibility requirements sit awkwardly
inside a purely social account. Englyn operationalizes the social model and
inherits that limit. It does not resolve it and does not claim to.

**Why this matters to an implementer.** The five marks this specification is
built on — Observable, Verifiable, Explicit, Recoverable, Typed — are
properties of the interface, never of a person. There is no user profile here,
no assessment of capability, no adaptation keyed to a named impairment. That is
deliberate, and it is also a design bet: the second reader Englyn is written
for is an AI agent, which has no body and no impairment but does have an access
need, and is served by the identical five properties that serve a blind power
user at five hundred words per minute, a reader with a cognitive disability,
and a braille user working forty cells at a time. If one set of properties
serves all four, those properties are not adaptations to bodily deficit; they
are properties of well-built interfaces. **That is the argument, and it is an
argument, not a result.** The disability-dongle critique is acknowledged here
as a live risk to this specification, not answered by it.

**What would settle it.** Disabled practitioners with authority over the text
rather than acknowledgement in it — see entry 1 — and their assessment
published whether or not it agrees with the framing above.

*Recorded 2026-08-17.*

---

## Reporting a defect

Defects in this specification are wanted, including defects in this file. Open
an issue on the specification's public repository, or use the contact address
published in the README. Every report is answered — here or in the changelog —
applied or refused, with the reason given either way.

---

## Adding an entry

Six fields, all required. An entry missing any of them is not yet an entry.

1. **Claim affected.** What a reader might otherwise reasonably assume.
2. **What can be checked.** The verified boundary, stated positively first.
3. **What cannot be checked, and why.** Mechanism, not apology.
4. **Scope of any claim made.** The layer stamp, where one applies.
5. **What would settle it.** If nothing would, say so and say why.
6. **Recorded date and source.**

**A correction stands beside a claim, never over it.** When an entry is
resolved it stays in this file, marked resolved, with the date and the
evidence. This file only ever grows.
