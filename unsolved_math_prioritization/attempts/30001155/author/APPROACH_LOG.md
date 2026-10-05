# Five substantive approaches

Research date 2026-10-04, UTC. Completion percentages are subjective estimates toward the **entire original conjecture**, not confidence levels or fractions of a formal proof. The full target was not replaced by a special case.

## 1. Normalize the inequality and compare quantitative gap mechanisms

Checkpoint 18:34 UTC; completion estimate 10%.

Mechanism: encode the area through q=4A/(πd²), identify F(q), derive its positive quadratic small-area correction, and attempt to obtain it from diameter-only log-concavity estimates or the latest geometric quantitative refinement.

Result: exact scale-invariant reduction; all constants and disk equality verified. Andrews–Clutterbuck supplies the baseline only. Amato–Bucur–Fragalà supplies a sixth-power width remainder and strictness of the baseline. We derived its A⁶/d¹⁴ consequence and contrasted it with the target's A²/d⁶ correction.

Blocker: a sixth-power lower remainder cannot dominate the required second-power correction on arbitrarily thin rectangles for any fixed comparison constant. A sharper geometric/eigenfunction mechanism is missing. No general proof follows from strictness alone.

## 2. Separate product spectra and optimize the rectangle parameter

Checkpoint 18:35 UTC; completion estimate 15%.

Mechanism: use the full exact rectangular spectrum, reduce to an aspect-ratio inequality, and prove it uniformly by θ<1/2 and π²>8.

Result: every rectangle satisfies the proposed inequality strictly, including the square's second-eigenvalue multiplicity. The ratio to the proposed bound tends to one as aspect ratio tends to zero. The proof treats all positive aspect ratios analytically.

Blocker: general convex domains have no product decomposition. Inclusion monotonicity of individual eigenvalues cannot simply be subtracted to obtain monotonicity of their gap. This route alone does not extend to arbitrary quadrilaterals or curved domains.

## 3. Use a stronger shape-class theorem and test its transfer

Checkpoint 18:36 UTC; completion estimate 20%.

Mechanism: compare the published optimal triangle gap, 64π²/(9d²), against the maximum value of the area-refined right side over all q.

Result: the target holds strictly for every triangle, directly from Lu–Rowlett Theorem 3 and an exact certified constant comparison. Equilateral triangles do not create a new equality case here.

Blocker: the theorem is restricted to triangles; cutting a convex body into triangles changes the spectral problem, and individual Dirichlet eigenvalue bracketing does not control a difference in the needed direction. The original theorem's computer-assisted component is credited rather than newly certified.

## 4. Affine min–max comparison around the disk

Checkpoint 18:37 UTC; completion estimate 25%.

Mechanism: pull an ellipse back to the disk, bracket each eigenvalue by the anisotropic quadratic form, subtract in the valid lower-bound direction, and compare the resulting expression with F(q).

Result: a positive explicit quadratic P(u), u=√(1−(b/a)²), proves the bound for b/a≥√15/4. Exact alternating-series and Bernstein-polynomial Bessel controls identify the correct first zeros and certify a rational margin 273124119/3618160000. Equality occurs only at the disk in this range.

Blocker: the min–max subtraction becomes too crude as the ellipse flattens. Even an all-ellipse proof would not settle arbitrary convex domains. No shape derivative or affine-invariance argument transfers this certificate to general shapes.

## 5. Challenge nonseparable domains and examine singular limits

Checkpoint 18:42 UTC; completion estimate 25%; final full-target status unresolved, five approaches exhausted.

Mechanism: deterministic P1 finite-element counterexample diagnostics for 13 convex shape/parameter cases at two resolutions, plus two additional high-resolution long-stadium runs. Independently examine the interpretation of the source's strip limit using an exact convex profile and Friedlander–Solomyak's thin-domain theorem.

Result: all 28 computed Ritz-gap margins are positive. This is not a proof because differences of Ritz upper bounds are not gap lower bounds. A long-stadium normalized gap changes from about 132.02 to 63.56, 41.25 and 33.66 under refinement, displaying severe underresolution. No certified counterexample is found. The convex family K_L={|X|<L, 0<Y<2−(X/L)²} converges locally to a strip, but d_L²γ(K_L)~4πL, so local strip convergence is insufficient for normalized saturation.

Blocker: no verified lower/upper eigenvalue enclosure, exhaustive shape search, or universal geometric localization estimate was obtained. The strip example only rejects an overstrong interpretation of informal limit language; it is not a counterexample to the inequality.

## Final gate

Do not label the original conjecture solved, already solved, disproved, or independently verified. Any publication should describe an exhausted five-approach partial investigation and preserve the distinction between analytic deductions, existing theorem dependencies and exploratory numerics. A fresh independent audit remains necessary.
