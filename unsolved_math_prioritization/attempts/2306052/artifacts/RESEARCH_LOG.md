# Five substantive analytical attempts

Problem 2306052 / AMR-022-6052, rank 528. Investigation on 2026-10-03 UTC. This log records five distinct mathematical routes, not five literature queries or five successful solutions. The checkpoint estimates concern progress toward resolving the original universal question; they are subjective planning estimates, not mathematical probabilities. The record was assembled after the derivations, with the time ranges below identifying their investigation order.

## Attempt 1: compact-target perturbation and exhaustion

Investigated 19:39–19:41 UTC. Checkpoint estimate: 10% toward the general goal.

Start with f(D)=C and preserve zeros by local Rouché contours. Derived a fully uniform perturbation allowance for any fixed compact target set by a finite cover of target disks. In particular, each finite target disk survives some bounded univalent linear perturbation.

Result: Lemma 1 in PROOF.md, proved for every compact K⊂f(D).

Exact gap: the allowance depends on K. Passing to larger and larger compact disks supplies a sequence of possible coefficients, but no single nonzero coefficient. This route is blocked without a genuine uniform estimate; no limiting coefficient is asserted to remain nonzero.

## Attempt 2: uniform contour margins and annular escape

Investigated 19:41–19:42 UTC. Checkpoint estimate: 10%.

Strengthened the contour hypothesis to one common margin for every target. Then tested a geometric source of arbitrarily large margins: contours with min|f|→∞. Used two applications of Rouché, first to guarantee a zero of f and then to guarantee a zero of f+h−w. This works for every bounded perturbation, with no smallness assumption.

Result: Proposition 2 and Corollary 2.1. Strong annularity is sufficient.

Exact gap: surjectivity alone has not been shown to provide these contours. The rational example later constructed is surjective but not strongly annular, and it admits a bounded affine perturbation that destroys surjectivity. Therefore the unrestricted “every bounded perturbation” claim is actually false.

## Attempt 3: inverse branches over uniform target disks

Investigated 19:42–19:43 UTC. Checkpoint estimate: 10%.

Recast the desired equation in a target disk through a holomorphic right inverse. Applied Rouché to ξ−w+h(φ_w(ξ)) on a smaller target circle. This yields a uniform norm criterion without needing estimates on inverse derivatives.

Result: Proposition 3, with the full inverse-branch hypothesis and a strict perturbation bound.

Exact gap: the inverse branches are an additional global requirement. In the final rational example the target −1/4 has only one disk preimage, which is critical, so even a local holomorphic right inverse fails there. The example nevertheless has uniform small-bounded-perturbation stability. The stronger inverse-branch assumption is therefore not a necessary replacement for the contour method.

## Attempt 4: affine-parameter topology and omitted-value selection

Investigated 19:43–19:45 UTC. Checkpoint estimate: 15%.

Established that coefficients preserving each compact target disk form an open neighborhood of 0 and that globally surjective coefficients form the intersection of these open sets. Identified the failure of an unsupported Baire argument. Proved that omitted targets must escape to infinity as the coefficient tends to 0.

Then assumed a holomorphic omitted-value selection on a punctured parameter disk. Escape to infinity forces a pole; the meromorphic argument principle, using the uniform boundedness of the perturbing function, then gives a contradiction. This produces a substantive no-selection theorem, Proposition 5.

Checked the complete relevant proof of Eremenko's entire-source exceptional-value theorem to investigate whether it supplied the missing selection. It does not apply to a disk-source family. Its Picard uniqueness and entire-source pluripolarity hypotheses are unavailable here.

Result: Propositions 4 and 5.

Exact gap: no theorem constructs a holomorphic omitted-value selection from failure of surjectivity of every small nonzero f+az. Nor has the nonzero intersection of the parameter neighborhoods been established by another argument.

## Attempt 5: exact rational family, boundary cases, and global norm control

Investigated 19:45–19:52 UTC. Checkpoint estimate: 15% toward the general goal; the stated special-family classification is complete.

Selected the Cayley transform T:D→H and P(t)=t²−t. Root sums immediately prove that f_0=P∘T is surjective. For f_0+az, clearing the denominator produces a cubic with zero t² coefficient. If it has no root in H, all three roots must be imaginary. Coefficient comparison pins down the sole possible omitted value, and the real cubic's extrema give the exact discriminant cusp.

Result: Theorem 6 completely classifies all complex affine coefficients. The bad locus is (2 Re a−1)^3≥27(Im a)^2; on it the unique omitted value is −conj(a). This includes repeated-root boundary cases. The explicit failure a=1/2 is checked by a separate factorization. Every nonzero |a|<1/2 is good.

A separate two-case contour construction, depending on the separation of the quadratic roots, proves that every bounded holomorphic h with ||h||∞<3/64 preserves surjectivity. This is Theorem 7; the constant is not claimed optimal.

Exact gap: the zero-sum cubic mechanism belongs to the selected rational function. No extension to arbitrary surjective f is proved. An example that admits both good and bad perturbations is not a counterexample to Rubel's existential question.

## Verification and final scope

At 19:52 UTC, the standard-library exact verifier passed 1,021 assertions, including six formal polynomial identities, boundary-cusp factorizations, rational test cases, and contour-margin constants. Those computations support the explicit algebra; the analytic arguments remain written proofs rather than formalized theorems.

Original problem: unresolved in this investigation. Proposed queue status: `unsolved`, `5/5`. No claim of a new solution, novelty, exhaustive current-open status, or human peer review. No remote writes were made. All included mathematical claims are limited to the statements proved in PROOF.md.
