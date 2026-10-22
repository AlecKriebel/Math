# Exponential auxiliaries: scoped progress, not a resolution

**30000707 / OWR-1460-014 — UNSOLVED, 5/5 substantive approaches.**

The exact target is the pair of exponential auxiliary systems in
Steinmetz's 2007 Problem 2. This package proves:

* Common poles are simple; finite multiplicities have minimum one and
  obey an exact exponential integer-ratio condition.
* Solutions have order one or two, respectively, by an attributed
  established characteristic estimate.
* If any finite shared value is CM, the first system is exactly
  `f=b−e^(−z), g=b−e^z`; the quadratic system has no such solution.
* The first system has no other rational-in-e^z solution of degree at
  most two. The quadratic rational-in-e^(z^2) ansatz fails by parity.

The general case where all three finite values fail CM sharing remains
unresolved. A recent claimed finite-order theorem is not used to bridge
that gap: one of its printed intermediate inferences fails a canonical
control, without thereby refuting the theorem statement.

Read [PROOF.md](PROOF.md), [DEPENDENCY_CHECK.md](DEPENDENCY_CHECK.md),
[SOURCE_STATUS.md](SOURCE_STATUS.md), and [APPROACH_LOG.md](APPROACH_LOG.md).
Run from the package root:

    python controls/check_controls.py

Python 3.12.14 and SymPy 1.14.0 produced 37 passing controls. The script
writes `controls/CONTROL_RESULTS.json`. Its explicit limits are part of
the result. It performs exact symbolic algebra and a bounded illustrative
scale check; it is not a formal proof assistant or a meromorphic-function
search. No source PDFs, catalogue corpus, private coordination, or
credentials belong in the public package.

These are unrefereed, substantially AI-assisted research notes, without
novelty, priority, full-resolution, paper, or new-DOI claims.
