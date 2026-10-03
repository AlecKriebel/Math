# Fresh adversarial audit: rank 461 / problem 20002029

Date: 3 October 2026 (UTC).

## Verdict

**PASS for the five expressly scoped mathematical results and the package's partial-result status. HOLD on any claim to resolve the original problem in general even dimension.** No fatal mathematical gap was found in the frozen proofs. In particular, the dimension-six nonexistence argument passes: the source classification applies, the full ambient invariant has the stated restriction, the Weyl-cubic spanning reduction is valid, the witnesses are actual positive-definite Ricci-flat metrics, and their exact evaluation matrix is nonsingular.

One nonblocking packaging repair is needed: the last paragraph of `ATTEMPT_4.md` points to `checks/divergence_results.json`, which is absent from the frozen public package. The public result file is `checks/verify_divergence_restrictions.result.json`. Correct that reference in a later revision; do not silently alter the frozen snapshot or its manifest.

This is an independent mathematical audit, not an assertion of novelty, external peer review, or a full solution. The earlier dimension-six contributor was not used as an independent reviewer.

## 1. Snapshot and source checks

The supplied manifest SHA-256 is verified:

`f91d501b76bd6e17c15eb0317b6ad8241b6404bf684a389ff184ee77fcfb16dc`.

All 15 listed files match both their recorded byte counts and SHA-256 values. The author snapshot was not edited. The integrity results are in `manifest_verification.json` beside this report.

The original [AIM Problem 10](https://aimath.org/WWN/confstruct/articles/html/30a/) has the stated pointwise, all-metric, even-dimensional scope and records the negative answer for n=4. It is not a locally conformally flat or integrated/modulo-divergence question. The interpretation of complete contractions as metric contractions is consistent with the source and the package's declared parity convention.

The critical primary source was checked against the live [Fefferman–Graham preprint](https://arxiv.org/pdf/0710.0919), printed pages 52, 56, 77–78, and 93–94, as well as the locally cached text. Theorem 9.4 covers even scalar invariants at weight −n, including the boundary case n=6. The subsequent weight −6 discussion gives the derivative ambient invariant together with Weyl cubics as a spanning family. Equations (6.3) and (9.3) agree with the quoted formulas. Proposition 6.5 gives the stated Cotton transformation; the normalization remark after Proposition 8.4 permits Schouten normalization.

The live [Case et al. v4, equation (3.4)](https://arxiv.org/html/2404.11319v4#S3) matches both Ricci-flat restrictions in Attempt 4. Its Cotton convention differs from FG's indexing convention, but the restricted expressions do not depend on that difference. The v4 date and journal citation were corroborated by [the preprint record](https://arxiv.org/abs/2404.11319) and [the publisher](https://www.sciencedirect.com/science/article/pii/S0001870826002136). The Case–Gover journal metadata in the source gate is also consistent with [the publisher record](https://doi.org/10.1112/jlms.70375).

This audit does not independently establish the absence of all earlier literature or certify every negative repository-search statement. Those statements are already bounded in the package, and no mathematical conclusion relies on a novelty claim.

## 2. Attempt 1: undifferentiated-Schouten elimination — PASS

The conformal Hessian gauge is legitimate at an arbitrary point of an arbitrary metric. The prescribed value, gradient, and Hessian of the conformal factor are compatible finite smooth jets. Setting the value and gradient to zero and the Hessian to P makes the transformed P vanish while retaining the metric and invariant value at that point.

If every summand contains P without derivatives, every summand then vanishes regardless of higher transformed jets. This establishes the ideal-type assertion exactly as stated. The warning against deleting such summands individually from a general invariant is essential and correctly included.

The constant-rescaling count is also correct. All-covariant P and its covariant derivatives have weight zero under constant scaling; the total of 2L + Σr_s covariant slots requires L + (Σr_s)/2 inverse metrics. Thus the scalar weight is −2L − Σr_s. If no derivative order is zero, then n = 2L + Σr_s ≥ 3L. The examples for n=8,10,12 follow. None of this removes unsymmetrized higher Schouten jets or imposes conformal flatness.

## 3. Attempt 2: first-Schouten-jet vanishing — PASS

### Tensor decomposition and gauge

For T_{kij}=∇_kP_{ij}, the last two slots are symmetric. With C_{ijk}=T_{kij}−T_{jik}, its skew/cyclic/trace conditions are correct, and

T_{kij}=S_{ijk}+(C_{ijk}+C_{jik})/3

follows directly by symmetrizing T. Prescribing the Hessian fixes P; the symmetric third derivative of the conformal factor has coefficient −1 in the fully symmetric part of the transformed ∇P. Consequently P=S=0 is attainable, including when a specified first derivative v is retained. No claim that the entire ∇P can be gauged away is made.

### Actual finite-jet realization

The independence of W and C is justified by actual metric jets, rather than by pretending that arbitrary complete curvature jets are free. Starting with any quadratic metric jet realizing W, the proposed cubic correction has no effect on curvature at the origin because it vanishes to order three. Its effect on the first curvature derivative is linear: all possible quadratic/cubic interaction terms vanish at the origin when the metric's first derivatives do.

For a trace-free hook tensor T with cyclic sum zero, write h_{ij}=−b T_{kij}x^k|x|². Direct differentiation gives

∂_i∂^a h_{aj}+∂_j∂^a h_{ai}=−2b T_{kij}x^k,

Δh_{ij}=−2b(n+2)T_{kij}x^k,

tr h=0.

Therefore Ric'(h)_{ij}=b(n+1)T_{kij}x^k. Choosing b=(n−2)/(n+1) gives the claimed Schouten derivative. This calculation is dimension-independent and verifies the coefficient in (2.2). Local positive definiteness follows by shrinking the neighborhood around the Euclidean constant term. A polynomial jet with a local cutoff is a genuine smooth local metric. No Ricci-flat germ realization is being claimed here.

### Translation span

The Cotton law has the right sign in the FG convention, and at u(x)=0 no conformal density factor changes the scalar value. Because W and C are independently realizable, the identity F(C−L_vW)=F(C) holds for every triple (C,W,v), not merely a constrained subset.

The proposed R(v,C) satisfies algebraic curvature symmetries. Its Ricci tensor and scalar trace are as asserted. The two summed contractions can be checked without representation theory:

Σ_a R(e_a,C)_{ajkl}=nC_{jkl}.

The trace terms in the summed Kulkarni–Nomizu expression vanish, leaving 2C_{jkl}+C_{lkj}−C_{klj}=3C_{jkl} by the cyclic identity. Thus the Weyl-projected sum is (n−3)(n+1)/(n−2) times C, nonzero for n≥4.

The images therefore span the entire Cotton space. Successive translations are permissible since the invariance identity holds at every C. F is constant, and its value at the flat jet is zero at negative weight. This final formulation also avoids any concern about a nonhomogeneous presentation containing cancelling constant terms. The n=3 exception is correctly identified.

The author's finite tests are useful checks of formulas, not the proof of the universal statement; the symbolic argument above supplies that proof.

## 4. Attempt 3: full dimension-six result — PASS

### Classification and parity

A universal polynomial contraction of Schouten jets is a natural, orientation-even scalar curvature invariant, so it lies in the class covered by the cited classification. At n=6 and weight −6 the theorem's range condition is satisfied. No exceptional odd invariant is being smuggled into or omitted from this class.

### Weyl-cubic span

The contraction-graph argument is complete. A self-pairing on a Weyl factor vanishes. With three four-valent vertices and no loops, every pair of vertices has exactly two edges. This accounts for every metric contraction, including initially non-obvious index arrangements.

If a factor is unmixed, antisymmetrization along each incident double edge reduces a mixed neighbor to half of its unmixed form using first Bianchi. Thus this class is proportional to A. If all three factors are mixed, curvature symmetries and relabeling reduce to the two displayed forms B and U. The identities used in B−U=A/4 have the correct signs and factors: first antisymmetrize the second tensor in e,f, then the first tensor in a,c. The final three-factor contraction is A by pair exchange and dummy relabeling.

This proves the required upper bound of two Weyl-cubic generators, independently of numerical examples and without assuming their independence. The evaluation matrix later proves independence as well.

### Full ambient restriction, including 0/∞ components

The proof does not identify an ambient norm with a tangential norm by simply discarding transverse slots. The source's equation (9.3) is the expanded full ambient contraction. On a Ricci-flat metric P and C vanish as tensor fields, so their derivatives vanish as well, U_FG=0, and V=∇R. This yields precisely D=|∇R|².

For an additional independent check, I constructed the actual eight-dimensional metric

2ρ dt² + 2t dt dρ + t²g_p

for each of the three six-dimensional witnesses and computed its Christoffel symbols, complete curvature tensor, complete first covariant derivative, and full inverse-metric contraction at t=r=1, ρ=0. The calculation includes every 0/∞ slot and does not use equation (9.3) or the author's orthonormal-frame formula. Nonzero components with one 0 slot really occur: respectively 120, 200, and 300 such components. Every component with an ∞ slot vanishes. Since the inverse metric pairs 0 with ∞ on the cone, their total scalar contribution is zero. The full ambient norms are exactly 1280/81, 27, and 21504/625.

This independent computation is recorded in `independent_ambient_check.py` and its result JSON. It directly defeats the most serious potential omitted-transverse-term objection.

### Genuine Ricci-flat witnesses and exact matrix

The stated power-law metrics are smooth and positive definite for r>0. The Kasner constraints give Ricci zero identically, not merely at r=1. The orthonormal connection and curvature signs are consistent. Completeness at r=0 is irrelevant to a universal pointwise identity on metric germs.

I separately computed the metrics in the coordinate frame from g_{rr}=1 and g_{ii}=r^{2p_i}, deriving the Levi-Civita connection, curvature and covariant derivative directly. This avoids reuse of the author's sectional-curvature or derivative-norm formulas. It produces exactly the three rows

(1280/81, −256/243, −128/243),
(27, −3, −3/2),
(21504/625, −19968/3125, −6528/3125).

Their determinant is −65536/3125. The arrays in `independent_coordinate_check.result.json` document the calculation.

On each witness P and every covariant derivative vanish identically. Thus the Schouten-only invariant evaluates to zero, and the nonsingular matrix forces all three classification coefficients to vanish. This is a valid proof of the original n=6 statement. The claim of injectivity on the full three-dimensional even weight −6 conformal-invariant space also follows. The flat-product extension to weight −6 in higher dimensions is valid, but does not make those weights critical there.

## 5. Attempt 4: two dimension-eight divergence examples — PASS

The tensor contractions and −1/6 Laplacian coefficient match the precise v4 source. Cotton terms and their derivatives vanish on every Ricci-flat germ. This is an exact pointwise restriction; no integration by parts or quotient by divergences is used.

In the coordinate computation mentioned above, I also formed both cubic covariant two-tensors with all inverse metric factors, differentiated them using their coordinate Christoffel symbols, and then computed the second divergence and scalar Laplacian. In particular, this check did not assume equation (4.1), equation (4.2), or diagonal-frame derivative formulas. The two eight-dimensional values are

(0, −256/81),
(−63/4, −45/2).

The determinant is −448/9. The direct computation also confirms the needed zero off-diagonal components. Since a nonzero linear combination cannot vanish on both witnesses, none can have a Schouten-only representative. This establishes the entire claimed two-dimensional-span exclusion, not merely failure of the displayed formulas to look Schouten-only.

There is no claim or evidence here that these two invariants span all weight −8 invariants. The package explicitly preserves that distinction.

## 6. Attempt 5: diagonal-curvature blind spot — PASS

The proposed four-tensor Q is alternating: it is half the sum of the wedge squares of the two-forms W_{ab}. Its conformal weight is zero as an all-covariant four-tensor. Four inverse metrics in its squared norm give scalar weight −8. No orientation tensor is required, so H is orientation-even and belongs to the same metric-contraction parity class as the question.

For diagonal Weyl curvature, each W_{ab} is a scalar multiple of a simple two-form e^a∧e^b, whose square is zero. Thus Q vanishes identically across the entire diagonal family. If the Riemann curvature rather than W is described as diagonal, its Ricci tensor is diagonal too, and subtracting the Schouten–metric term preserves this diagonal structure; the same conclusion holds. All Ricci-flat Kasner witnesses are included.

The explicit four-coordinate tensor extended into dimension eight is an algebraic Weyl tensor. Each of the three self-dual two-forms has the same squared wedge orientation and the same Ricci contraction, so the coefficient sum 1+1−2 cancels first Bianchi and Ricci traces. Orthogonality gives Q_{1234}=4(1²+1²+(−2)²)=24; all other independent four-form components vanish. With the specified 1/4! convention, H=576. The norm normalization is correct.

Realizing this single algebraic curvature tensor at a point needs only the ordinary order-zero metric jet realization, not a Ricci-flat germ. Therefore H is genuinely nonzero on metrics. Its universal vanishing on the selected test family proves that no number of exclusively Kasner/diagonal-curvature evaluations can make restriction injective on the entire n=8 invariant space.

The package correctly does not call H a Schouten-only invariant or a counterexample. It also correctly distinguishes a hypothetical kernel for restriction to all Ricci-flat germs from a kernel for the much smaller Kasner family.

## 7. Remaining gap and exact scope of approval

The full even-dimensional problem for n≥8 remains unresolved by this package. The following steps would be needed for the proposed general restriction route and are not supplied:

1. A complete, justified spanning description at the higher critical weight.
2. Either a proof of injectivity on actual Ricci-flat metric germs, or a sufficiently rich certified full-rank evaluation family.
3. Control of differential Bianchi, nonlinear commutator, Ricci-flat compatibility and extendability constraints; slot counting in an unconstrained tensor algebra alone does not do this.

The first-jet theorem and the P-factor ideal lemma do not bridge those gaps. The explicit blind spot shows that enlarging only the Kasner sample cannot bridge them either. These are acknowledged limitations, not defects concealed by the proofs.

Accordingly: approve publication as partial results with n=6 proved and the other stated exclusion/obstruction certificates; do not approve any upgrade to a general solution, proof of all-dimensional Ricci-flat restriction injectivity, complete n=8 classification, or novelty claim.

## 8. Reproduction record and suggested small repairs

All four author scripts completed successfully under Python 3.12.14 and SymPy 1.14.0. Their fresh outputs are saved as `*.rerun.txt` in this audit directory. I additionally wrote and ran two independent exact coordinate calculations:

- `independent_coordinate_check.py`: base metrics, Ricci, covariant derivative norm, raw cubic contractions, cubic two-tensors, double divergences, Laplacian, and both determinants.
- `independent_ambient_check.py`: full ambient connection, curvature, covariant derivative, and null-slot-sensitive scalar contraction for every n=6 witness.

Both result JSON files report success. The first-jet formulas and the cubic spanning proof were audited algebraically; the finite author samples are not being promoted to exhaustive proofs.

Required nonblocking repair: fix the Attempt 4 result-file reference identified at the start.

Optional clarity improvements, neither mathematically necessary:

- Add the two-line cubic-metric Ricci calculation from §3 to make the actual-jet realization especially transparent.
- State F(0)=0 by flat-metric constant-rescaling covariance, rather than by an implicit homogeneous-monomial convention.
- Link the primary journal DOI when stating final publication metadata in the source gate.

Any revised public files need a new manifest and should be distinguished from this audited frozen snapshot.
