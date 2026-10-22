# Five substantive attempts

Problem 2306063, rank 585. Research date: 2026-10-04 UTC.

These are five mathematical approach families, not five tool calls. The source-gate work and prior-result checks did not yield an exact resolution eligible for an early 1/5 stop. All five have been completed and the mathematical search stops here. The independent review may check these artifacts; it is not an extra search turn.

## Source checkpoint, 09:25–09:31 UTC

- Started at the specified catalogue URL; direct request returned 403 and web retrieval failed.
- Recovered the selected record and complete prior report; verified the statement against the original source, including epsilon as a positive continuous function.
- Read the live queue, state, attempt-directory listing, related-target groups, and selected-ID PR search. Queue: queued 0/5; no selected-ID existing attempt, state entry, related group, or PR match. Live main: df9f2c05f61cad48f851c2d2ba7a63611a0acfa0.
- Read primary mathematical sources by Jenkins, Huber, Vainio, and Bishop. Found no exact later solution in the targeted searches. This is not an exhaustive literature proof of openness.
- Goal completion estimate: 0% toward a full answer. Scope is established; the recovered prior report used an incorrect constant-tolerance abbreviation.

## Attempt 1: explicit affine uniformization

Mechanism: solve the affine identification by exponential coordinates in the translation case and logarithmic-periodic coordinates in the dilation case.

Result: Theorem 1 in `PROOF.md` proves complete end classification for alpha(x)=a x+b, including a<1, a=1, a>1, and b=0. The hyperbolic parameter subset is open within the affine family.

Exact gap: the target quantifies over every admissible nearby homeomorphism, not just the two-parameter affine family.

Checkpoint: recorded in the proof before its 09:35 UTC draft completion. Full-target completion estimate: 10%, subjective and non-calibrated.

## Attempt 2: quasiconformal transport

Mechanism: descend an explicit strip interpolation F fixing the bottom edge and applying beta composed with alpha^{-1} to the top edge; control its singular-value ratio and transport extremal length.

Result: Theorem 2 proves same type under stated local sewing regularity, positive upper/lower derivative bounds, and bounded displacement. Lemma 2A constructs locally bi-Lipschitz, admissible perturbations in every fine tube with unbounded adjacent-interval distortion and unbounded distortion for that interpolation.

Exact gap: value-only closeness gives none of the uniform derivative estimates. No type change, and no impossibility of every alternative comparison, is inferred from the obstruction.

Checkpoint: recorded by 09:35 UTC. Full-target completion estimate: 10%.

## Attempt 3: invariant one-forms / Jenkins-type criterion

Mechanism: transport a unit-mass density along iterates of an expanding sewing. It yields a circle-valued degree-one function and a finite-area admissible core-loop metric.

Result: Theorem 3 proves hyperbolicity for eventually uniformly expanding real-analytic sewings, and for the explicitly chart-regular summable derivative-product variant. The affine energy bound is explicit. This mechanism has classical priority, with Jenkins 1959 credited.

Exact gap: general homeomorphic sewings need not have derivative products or the boundary-chart regularity assumed in this route. There is no value-only robustness estimate for the infinite energy sum.

Checkpoint: recorded by 09:35 UTC; chart-regularity wording tightened at the 09:38 UTC author check. Full-target completion estimate: 15%.

## Attempt 4: compact-open parabolic tail surgery

Mechanism: keep a hyperbolic affine sewing unchanged on a long initial interval and change its far tail to a translation.

Result: Theorem 4 proves convergence of parabolic sewings to a hyperbolic sewing in compact-open topology. Every example is locally bi-Lipschitz and its type is established from an exact tail uniformization.

Exact gap: the tail error grows without bound. The constant tolerance epsilon=1 rejects every constructed example, so this cannot refute the actual fine-topology statement or even constant-uniform stability.

Checkpoint: recorded by 09:35 UTC. Full-target completion estimate: 10%.

## Attempt 5: singular welding after compactification

Mechanism: split the strip and use exp(-2 pi z). Apply fine log-singular approximation on the positive side, then test the precise hypotheses of Bishop's welding theorem.

Result: Lemmas 5A–5C prove the exact fixed-negative-side reduction, the multiplicative tolerance conversion, fine positive-side log-singular homeomorphic approximation, and the capacity obstruction to global log-singularity when a nondegenerate interval is fixed. Huber's approximation theorem was checked to be in the opposite, hyperbolicity-forcing direction.

Exact gap: a globally coherent parabolic sewing through zero has not been constructed. A locally singular homeomorphism is not automatically an admissible sewing with a specified type; the whole-circle theorem cannot simply be substituted.

Checkpoint: complete by the 09:38 UTC author check. Full-target completion estimate: 10%.

## Frozen disposition

Unsolved, 5/5. Five distinct mechanisms have checkable artifacts. The principal target remains unanswered. All theorem dependencies and scope restrictions are retained. Finite controls are diagnostics, not infinite-type tests. No additional mathematical exploration is hidden after turn five.
