# Independent final-pass audit: fixed-point criteria and depth obstruction

Reviewed artifact: `pass5_audit/FIXED_POINT_CRITERION_AND_DEPTH_OBSTRUCTION.md`.
SHA256: `7f2f076348b3c51f754b045f6dd5d293d0ee1c99e68a0b909d6ab1daef5660f0`.

**Verdict: accepted without required correction.** This is an exact structural reduction and a conditional obstruction to universal fixed-depth closure, not a full-game solution or a forced losing history.

## Robust fixed-point criterion

The finite state domain retains the exact cone and every tail-age constraint. Each legal Devil update remains available at every state; the constraints are invariants of the transition, not a separate limit that grants the Devil different choices in different histories. Consequently the robust predecessor has the stated Angel-then-Devil quantifiers.

The four criteria are equivalent. A stable finite-horizon region is a closed invariant, and any closed invariant lies in every finite-horizon region. Finite stabilization by itself is automatic even when the empty state is losing. The separate requirement that the empty state still belong to the stable region is essential and is stated correctly.

## Fixed-depth carpet

For M=(2k+3)^2, the carpet's strongest tail constraint is M≤H−k. Thus H≥M+k is exactly sufficient for this particular carpet to belong to K_H. The entire terminal square lies within the relative cone.

The carpet is irrelevant for the first k death checks. Suppressing or supplying this fixed old information in a virtual history proves the exact online equivalence with empty-state survival for k moves. There is no offline path selection and no requirement that the Devil forget the old information. During the next move every possible endpoint is already carpeted, so the failure of W_(k+1) is unconditional.

The resulting dichotomy preserves the missing initialization issue: either empty∉W_k, or the full W_k family fails closure. This proves that one fixed depth cannot serve the stated universal-closure scheme for all H. It does not exclude a smaller invariant or imply that an H-dependent square-root depth suffices.

The realization uses distinct rounds H−i+1 and leads k+i≤H. Every target occurs after the H-step preparation, so the stay-put history is legal. Its cooperative path cannot be replaced by an assertion of strategic forceability.

## Negative-certificate interface

At a state of removal rank r>1, the negation of the robust predecessor says that every safe Angel move has at least one Devil reply outside W_(r−1). Such a successor has smaller positive removal rank. Rank-one states have all nine immediate moves bombed. Therefore a finite rank-decreasing certificate rooted at empty would genuinely force finite death on every Angel branch; a certificate rooted only at a preload has the weaker local scope explicitly stated in the artifact.

## Additional logical boundary

For the unrestricted game, deleting preloaded bombs cannot hurt the Angel. Hence, for any k, existence of even one W_k state implies that the empty state belongs to W_k. The strategy can internally supply the fixed deleted preload while processing every actual adaptive announcement; any real lethal pair is also present in this virtual play.

It follows that an unconditional family of W_k-but-not-W_(k+1) states for an unbounded set of k would itself establish empty-state survival to every finite horizon, and therefore an infinite strategy by the already accepted compactness argument. Such a family cannot be treated as a purely negative induction result without recognizing this affirmative consequence. The reviewed artifact avoids that issue by retaining its empty∈W_k premise and its failed-initialization alternative.

No arbitrary-H survival proof or empty-rooted Devil certificate was obtained in this lane during the final pass. The full target remains unresolved.
