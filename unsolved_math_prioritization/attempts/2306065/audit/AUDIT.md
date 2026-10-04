# Independent adversarial audit: rank 586 / problem 2306065

Audit date: 2026-10-04 UTC. Target: AMR-022-6065, Hayman–Lingham Problem 6.65.

## Verdict

**PASS for the explicitly limited partial results and the classification `unsolved`, 5/5.** No mathematical blocker was found in the frozen package. This is not a solution of the sharp extremal problem and is not a formal verification of the cited complex-analysis theorems.

The audited statements are

- `1134162229/1250000000 <= B(3) < 957/1000`, i.e. `0.9073297832 <= B(3) < 0.957`;
- `B(M) < 2(1-1/M)` for every `e < M < 5`;
- the simple Pick/square-root envelope fails at `M=3`, a phenomenon already known from Pearce's 1991 paper.

The full sharp value remains unproved even at `M=3`. The approximate slit-search value `0.9141951229` is not certified as a lower bound, upper bound, or global maximum. None of the optimizer success flags is used as mathematical evidence in this audit.

## Frozen artifact and independent execution

Audited manifest SHA-256:

`2e460367412073ef24a4c39137fb0851123b0765f086d5e662ae2d31cdee4a6c`

All 24 payload file hashes match the manifest. There are 25 top-level files when `SHA256SUMS.json` itself is counted. The existing `__pycache__/` directory is outside this inventory and must not be published accidentally.

The frozen directory was read only. The author's aggregate verifier and manifest verifier were rerun with bytecode creation disabled; the aggregate result exactly equals the stored `CHECKS.json`. The independent program in this audit directory imports no author verifier code. It independently constructs Chebyshev coefficients from the finite closed-form power formula, recomputes Bernstein coefficients directly on each rational dyadic interval rather than using de Casteljau subdivision, checks the interval partition explicitly, and rebuilds every upper-bound dual calculation. It uses exact `Fraction` arithmetic. It also reruns seven mutated-fixture rejection checks in temporary directories.

Inventory hashes were checked again after all numerical audit work. They still match the author freeze.

## Mathematical review

### Exact analytic formulation and real reduction

The logarithm of `f(z)/z` exists because a normalized univalent function has no nonzero zero and the disk is simply connected. Schwarz's lemma applied to `f/M` gives `|f(z)/z| <= M`, so `Re g <= log M`. Conversely the two stated real-part constraints imply normalized starlike univalence and `|z exp g(z)| < M` on the disk. These are exact constraints rather than a finite-dimensional relaxation.

The coefficient identity `a3=c2+c1^2/2` is correct. The Herglotz bounds `|c_n| <= 2/n` are correct with the displayed normalization. A positive atomic mass forces the logarithmic potential to diverge on its radial approach; contributions from the other masses cannot cancel this because their negative parts are bounded below. Thus finite atomic Herglotz extremizers cannot be substituted into the bounded problem.

Rotation makes `a3` real and nonnegative. Taking the real part of the logarithmic coefficients preserves both real-part constraints. If `c1=x+iy`, the new third coefficient is the old real third coefficient plus `y^2/2`. The sign change `z -> -z` then allows `c1 >= 0`. Consequently the real-coefficient upper certificate controls the original complex class.

The compactness argument is valid: bounded holomorphic functions form a normal family; normalization rules out a constant limit; injectivity is retained under local-uniform convergence to a nonconstant limit; and `p(0)=1` upgrades the limiting nonnegative real part to strict positivity. The modulus bound passes to the limit. Coefficients are continuous, so the supremum is attained.

### Competitor formulas and strict general bound

Expanding the Pick relation gives exactly `A2=2-2/M` and `A3=3-8/M+5/M^2`. The square-root transform is holomorphic with its normalized branch, satisfies the positive-real-part criterion, and has third coefficient `1-M^-2`. Their difference and the `M=3` tie are as stated.

The required Barnard–Lewis logarithmic subordination is explicitly stated as Theorem A on printed p.326 of the 1975 coefficient article. It applies to the package's class because its boundedness condition is equivalent to the article's condition for `t>1`. Exponentiating the subordination is legitimate and yields `a3=A2 v+A3 u^2`, with `|v|<=1-|u|^2`.

For the target interval, `0<A3<A2`, so equality at `A2` forces `u=0`, `|v|=1`, and therefore `omega(z)=eta z^2`. This equality map has logarithmic derivative `2 p_M(eta z^2)-1`. Differentiating the Pick relation also gives

`p_M(w) = ((1+w)/(1-w))*((1-F_M(w)/M)/(1+F_M(w)/M))`.

Along `w=-r`, the first factor tends to zero while the second tends to a positive finite value, since `F_M(-1)/M` lies strictly between `-1` and `0`. Thus the equality map fails starlikeness near those points. Compactness is essential and correctly supplied: excluding equality for every individual function alone would not establish a strict supremum bound. Here attainment closes that step.

### Upper certificate: direction, coverage, and rounding

Fejér convolution of each nonnegative harmonic function on radius `r`, followed by `r -> 1`, gives the displayed finite necessary inequalities without assuming continuous boundary values. Sampling them at 201 rational cosine coordinates weakens the feasible conditions and therefore is valid for an **upper** bound. The inequalities are never treated as sufficient.

The positive Taylor sum through degree 30 at `U=1098613/1000000` exceeds 3, proving `U>log 3`. Replacing `log 3` by this larger rational number weakens the boundedness inequalities in the correct direction.

The `c1` bound is `0<=c1<=4/3`. The 64 slabs are exactly `[k/48,(k+1)/48]`, `k=0,...,63`, cover that interval with no gap, and include both endpoints. The secant inequality for `c1^2/2` has the correct direction because `(c1-l)(c1-h)<=0` on a slab.

Every multiplier is nonnegative. A lower coordinate multiplier contributes `-y*c_n` to the left and `-y*lower_n` to the right; the author implementation uses this sign correctly, including the special `c1` slab endpoints. The exact residual correction is valid because

`(t-d) dot c <= sum_n (2/n)*abs(t_n-d_n)`.

All 40 residual coordinates are included, so the rounded dual does not need exact feasibility. All 64 independently rebuilt bounds are strictly below `957/1000`. The largest is on slab 49, `[49/48,25/24]`, and equals approximately `0.9562404840378954`; its residual correction is approximately `4.3297963382e-11`. The margin to `0.957` is approximately `0.0007595159621046384`.

The independent result contains each exact rational slab bound and correction. No finite-angle test of admissibility and no floating-point solver output is being used as an upper-bound proof.

### Witness: complete disk rather than a grid

The exact polynomial has degree 40. The independent direct-affine Bernstein calculation reproduces the author's 14 `P` cells of maximum depth 8 and 7 `Q` cells of maximum depth 4. Their rational endpoints explicitly partition `[-1,1]` without gaps. Every Bernstein coefficient on every leaf is positive.

Certified minima are approximately `0.00024206500722906584` for `P` and `0.0000444726140904868` for `Q`. Thus the boundary inequalities hold at every angle, and the harmonic principles propagate them throughout the disk. The resulting function is normalized, starlike, and injective on the unit disk. Its extension is entire; global entire-plane univalence is neither claimed nor implied by this proof.

The Taylor tail estimate for `exp(549/500)` has the correct direction. The first omitted term is order 31, and each succeeding term has ratio at most `(549/500)/32`; its geometric majorant is below 3. The witness therefore has the required strict modulus bound. Exact coefficient arithmetic gives `a3=1134162229/1250000000 > 9/10 > 8/9`.

### Remaining slit formulation and five approaches

Barnard's Theorem 1 supports the reduction to at most two real-axis-symmetric radial slits, with the equal-length conclusion explained in the proof and the adjacent Barnard–Lewis discussion. The interior square-root formula and the expansions for `q1` and `q2` agree with Barnard and Pearce. The two real integral conditions identify equal outer radii for the interior two-arc case. They are not asserted to settle all endpoint degeneracies.

The preserved numerical probe visibly falls below the explicit Pick competitor at sufficiently large `M`, consistently with its artificial `c >= -0.999999` cutoff. This is a valid failure control, not a global optimization certificate. The five attempt families are distinct substantive approaches; certificate validation does not claim a sixth proof-search turn.

## Rejection controls

The author's zero-witness and missing-slab controls pass. Seven additional temporary mutations are rejected:

1. A negative upper-inequality multiplier.
2. A duplicate slab index replacing the last slab.
3. An out-of-range inequality index.
4. All upper multipliers removed.
5. A witness violating only the logarithmic boundedness condition: `c1=6/5`, `c2=3/10`, all others zero. Its starlike polynomial is `6/5*(x+1/2)^2+1/10>0`, but its logarithm at 1 is `3/2>L0`.
6. A witness violating only starlikeness: `c1=0`, `c2=1`, all others zero. It has `Re g<=1<L0` but `P(0)=-1`.
7. An invalid exponential cap `L=2`.

The independently written checker uses explicit exceptions rather than removable Python `assert` statements. The author's documented normal `python verify.py` invocation is valid; optimized `python -O` should not be used with its assert-based verifier.

## Source and provenance review

All five privately retained source PDF byte counts and hashes match `SOURCE_MANIFEST.json`. No PDF, extracted text, or rendered page is included in this audit deliverable.

- Hayman–Lingham printed p.141 was visually checked: the exact target is the third-coefficient supremum throughout `e<M<5`.
- Barnard–Lewis printed p.326 was visually checked for the actual subordination theorem, the `a2` consequence, the missing interval, and the two-slit reduction reference.
- Barnard's printed pp.340–343 support the parameter formula, real-coefficient reduction, and extremal-domain reduction.
- Pearce's author-manuscript pp.21–23 explicitly identify Problem 6.65 and refute the endpoint conjecture numerically. Page 23 reports a partial analytic disproof without supplying the full long calculus argument. It does not give a complete sharp formula for the missing interval. The package does not misclassify this as an already-solved target.

**Additional provenance established during this audit:** an accessible local copy of the pinned problems corpus has exactly 68,931,837 bytes and SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`. Its entire selected JSON record for 2306065 equals the author's selected record. The research-results copy also matches the pinned 80,334,822-byte hash. Thus the selected target has now been independently checked against the pinned snapshot. This supplements rather than silently edits the frozen author's truthful description of the snapshot it originally recovered. `PINNED_TARGET_CROSSCHECK.json` records the comparison without redistributing any corpus record.

The literature search remains bounded. This audit does not assert present-day exhaustive open status, priority, or novelty. It also does not refresh the author's live repository observations; a current duplicate/state/PR check is still required before publication.

## Corrections, scope, and publication recommendation

No mandatory mathematical correction is required. A separate addendum may report the newly completed pinned-corpus comparison. Optional wording clarification: replace “this entire starlike function” in verifier descriptive text with “this entire function, starlike on the unit disk” if that text is revised in a later version; the current context already defines the disk domain.

Maintain `unsolved`, `turns_used=5`, and `full_resolution=false`. Do not promote the witness, the relaxed upper bound, the known endpoint-conjecture counterexample, or the numerical slit maximum into a sharp solution.

If publication is separately authorized, use an exact file allowlist: the 24 manifest payload files and the manifest itself, plus any explicitly approved audit addendum. Exclude all private sources, corpus data, coordination receipts, and bytecode caches. The independent gate can be recorded with this separate report while leaving the author freeze untouched. Recheck current repository state first. The queue scope remains the selected row's `Status=unsolved` and `Turns=5/5`; this audit does not authorize a Findings edit or any remote write.
