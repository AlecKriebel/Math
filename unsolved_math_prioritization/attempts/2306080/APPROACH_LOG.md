# Function Theory 6.80 research log

All timestamps are UTC on 2026-10-04. Percentages describe completion of
the target-verification task, not probabilities that a theorem is true.

## Source and status triage

- 09:50–09:52: Catalogue access failed (HTTP 403); read the full imported
  target and prior OPEN-TRIAGE report, and checked Hayman–Lingham 6.80.
  The prior report supplied no proof attempt. Located the 1981 publisher
  abstract describing exactly the requested negative answer. Estimated
  completion: 25%.
- 09:52–09:55: Compared the arXiv and published-format versions of
  Gröhn's paper. The published version has the correct real second
  exponent and the 1981 Lappan citation; the arXiv version differs on
  both points. Read and visually checked equation (12). Estimated
  completion: 50%.

## Substantive response 1 of 5

**Mechanism.** Reconstruct the explicit known counterexample using a
logarithmic change of variables. The transformed disc is a convex domain
inside a strip of width pi. An exact bound on the logarithmic derivative,
|L'−1| < 87/700, rules out both zero winding and nonzero exponential
winding in a putative collision. This proves global univalence of F'.
An exact radial zero sequence makes the hyperbolically weighted spherical
derivative of F diverge.

**Evidence.** PROOF.md includes the full strip lemma, transformed-domain
calculation, branch choices, uniform rational margin, exact zero sequence,
and normalization check. verify.py reproduces the finite algebra and
constant controls. The proof covers every analytic univalent function
quantifier required to refute the proposed universal statement, by one
explicit counterexample.

**Status.** Complete reconstruction of Lappan's known negative result.
No mathematical gap remains in the candidate proof. Independent audit
is separate from this author's verification. Completion estimate at the
author's freeze: 95% of the verification-and-publication task; mathematical
candidate complete.

**Prior-report assessment.** Its only substantive status statement was
that the 2018 compilation still listed the problem without progress.
That is not evidence that it remained open: Lappan's primary abstract and
the published Gröhn paper give earlier affirmative evidence of a negative
resolution. No earlier proof was inherited or counted as a new proof.

**Stopping rule.** Do not spend the remaining four turns searching for a
new solution to an already resolved question. No additional approach
families are claimed. No source download is a proof-attempt turn.
