# Contributing to Englyn

**The most useful thing you can send is a failure.**

A FAILS from a page you own is worth more to this project than a hundred passes on ours.
Our own conformance report publishes fifteen failures and a layer we cannot yet run. That
is the honest state, and the fastest way to improve it is somebody else's evidence.

## What we most want, in order

**1. A conformance report from a page you own, especially a failing one.**

```
git clone https://github.com/waxandwires/wax-and-wires-site
npm ci
npm run englyn:selftest      # controls first. if these do not fire, stop and tell us.
npm run build                # L1
npm run englyn:schema        # L2
npm run a11y:axe             # L3
npm run l4:keyboard          # L4
```

Send the output. **If your numbers differ from `reference/CONFORMANCE-REPORT.md`, that is a
finding and we want it**, including the case where our numbers do not reproduce on your
machine.

**2. A verdict from an assistive technology we have not tested.**

We have run VoiceOver on WebKit. **NVDA, JAWS, TalkBack, Narrator, and every braille display
are untested.** If you use one daily and something in this specification is wrong, that
outranks our reasoning and we will change it.

Two open questions where a screen reader user's answer settles it and ours does not:

- Our theme picker is an ARIA combobox pattern. A linter says it should be a native
  `<select>`. **Which actually serves you better?**
- A heading with decorated text carries an `aria-label` to keep its name clean. **Is that the
  right repair, or should the heading be restructured so it needs no label?**

**3. Help defining Gold.**

**Gold is deliberately unwritten.** It requires recorded assistive-technology verification
with paid community participation, and it cannot be self-certified by anyone including this
project's author. **Writing the tier that governs disabled reviewers, without disabled
reviewers, would be the original problem in a new document.**

There is no rate set yet and no budget in place, and we will not pretend otherwise. **The
invitation is currently unpaid and honestly framed as such.** Paid review arrives when Gold
is real. If that makes this the wrong ask for you right now, that is a completely reasonable
answer and we would rather you said so than felt obliged.

## What a good report looks like

State what you ran, on what, and what happened. **Print the denominator** ... how many files or
pages were examined, not only how many failed. A count without its denominator is not a
measurement, and we learned that the hard way: one of our checkers reported CONFORMS while
scanning zero files.

Include your environment. Interpreter, browser, and tool versions. **An unpinned interpreter
has already produced a pass in this project that did not reproduce.**

## How to disagree with a requirement

**File against it.** The decision register is public, every ruling names its source, and two
of the author's own recommendations were withdrawn in the week before first release because
somebody found the evidence against them.

If a requirement cannot be met by hand-authored markup in a text editor, **the requirement is
wrong** and we want to hear about it. That is §2.1 and it is not negotiable.

## What we will not do

**We will not tune a checker until it passes.** If a check fails, the check reports it. This
project is named after that discipline and it applies to us first.

**We will not accept a requirement that restates WCAG, WAI-ARIA, or the APG as new.** Those
are cited to their source. Renumbering them here claims credit for a floor other people
built.

## Licences

Specification text is **CC-BY-4.0**. The conformance tooling is **Apache-2.0**, in its own
repository, because a patent grant is what a stranger's legal review needs before running
somebody else's code in their CI.

By contributing you agree your contribution ships under those terms.

## Conduct

Be straight with each other. Assume the person on the other side is competent and busy.

**And a specific one, because this project is about disability and most of it was not written
by someone using assistive technology daily:** if a disabled contributor tells you a
requirement is wrong, the burden of proof is on the requirement.
