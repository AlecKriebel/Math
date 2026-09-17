# Independent review: scalar, operator bounds, and source polar correspondence

Review checkpoint: 2026-09-17T04:08:27Z / 2026-09-16 Pacific. Completion estimate: 100% of this bounded source-correspondence audit. Clean compilation and dependency verification are owned by the coordinating reviewer and are not claimed here.

## Verdict

**No blocking mathematical or statement-correspondence issue found in the assigned scope.** The delivered sources genuinely derive the all-dimensional scalar bound and its equality set, first-family bounds for arbitrary complete complex Hilbert spaces, the literal second-family SOS with proved coefficient normalization, and the actual source coefficient observables' canonical polar interpretation and attainment. The physical upper bounds do not assume an optimal value, a chosen spectrum, a preexisting SOS, or an equality witness.

The important qualification is the general polar-decomposition boundary: the general identity takes a supplied factor satisfying factorization and initial-isometry equations. It does not construct arbitrary canonical polar decompositions or prove their strong-limit representation. This is accurately disclosed in `COVERAGE.md`, and the main commuting bound uses independently constructed continuous half-polar factors, so this omission does **not** leave that bound conditional on an unproved existence statement. For the explicit source pencils, the package does construct the factor and modulus inverse.

I reviewed the extracted delivered package at `package/lean_formalization`, against its own `reference/manuscript/main.tex`; I did not use the historical live Lean version, earlier verdicts, or package execution reports as evidence of correctness. The package was not edited, and no build was run by this reviewer.

## Correspondence and proof audit

All source references below are relative to `package/lean_formalization/`.

| Manuscript target | Actual delivered statement and evidence | Assessment |
| --- | --- | --- |
| `lem:scalar`, manuscript lines 406–420 | `CyclicBell/GeneralScalar.lean:256`, `scalar_bound`; line 341, `scalar_equality_iff`. Both quantify arbitrary `z : ℂ` with `‖z‖=1` and all `d≥2`. | Full scalar statement, not only sampled dimensions or selected equality roots. |
| First global upper bound, `thm:exact`, manuscript line 326 | `CyclicBell/GeneralCommuting.lean:96`, `first_cstar_sos`; line 160, `first_commuting_hilbert_bound`. | A genuine SOS in an arbitrary C*-algebra, followed by the normalized-vector bound on an arbitrary complete complex Hilbert space. |
| Finite-dimensional mixed-state first bound | `CyclicBell/GeneralFirstBound.lean:79`, `first_matrix_upper`; line 103, `first_physical_upper`; line 141, expanded physical statement. | Arbitrary finite local coordinate types, d outcomes, positive trace-one mixed state. Local dimension is not silently fixed to d. |
| First augmented upper bound | `CyclicBell/GeneralCommuting.lean:183`, `first_augmented_commuting_hilbert_bound`. | Adds the actual aligned term with upper bound one. The endpoint is even valid without cross-commutation for the added product, since a product of unitaries is unitary. This is stronger, not a missing physical hypothesis. |
| General polar identity, `lem:polar`, manuscript line 345 | `CyclicBell/GeneralCoveragePolarCanonical.lean:77`, `canonical_polar_positive_factor_identity`; line 108, Hilbert specialization. | Literal CFC positive square roots and half-powers, including singular operators; supplied-factor boundary described below. |
| Literal second coefficients and `lem:lambda-normalization`, manuscript lines 920–968 | `CyclicBell/GeneralSecondCoefficients.lean:14`, actual coefficients; line 36, `generalLambda_literal`; line 203, `generalLambda_normalization`. | Sign, phase, denominator, exceptional l=0 exponent, and normalization are proved. Normalization is not just a premise at the physical endpoint. |
| `eq:second-sos`, manuscript lines 974–981 | `CyclicBell/GeneralSecondCommuting.lean:55`, `second_cstar_sos`; line 93, `second_commuting_hilbert_bound`; line 108, augmented bound. | Correct residual `d λ_l I − A_l Bhat_l`, conjugation of λ in the functional, positive prefactor `1/(2d)`, and bounds d and d+1. |
| Canonical source strategy, `app:attainment`, manuscript line 1632 onward | `CyclicBell/GeneralSourceFourier.lean:29–38`, literal coefficients/modes/Bob matrix; `GeneralCoverageSourceCanonical.lean:77`, actual modulus; line 121, literal inverse formula; line 137, `sourceBob_canonical_polar`; `GeneralCoverageSourceStrategy.lean:91`, `sourcePhysicalStrategy_attains`. | Identifies and validates the literal source matrices, not merely an unrelated strategy with the same value. |

### Scalar proof and all-dimension quantifiers

The scalar definitions at `GeneralScalar.lean:12–17` are the manuscript quantities: `2/sin(π/(2d))` and the sum of `‖1+chi(y)z‖`. The `chi` phase matches the positive exponential via `GeneralPhases.lean:60–68`; the shifted equality roots match the manuscript formula via `GeneralPhases.lean:112`.

I followed the proof through the centered-grid calculation (`GeneralScalar.lean:86–154`), actual floor-based sector reduction (`156–180`), unit-circle parameterization (`256–262`), and power/equality equivalence (`308–348`). Positivity of the sine denominator is proved before division, the angular domain is bounded before uniqueness of the cosine maximum is invoked, and the argument of an arbitrary unit-circle complex number is used at the endpoint. Neither the scalar maximum nor its equality set is assumed. The centered-grid proof is a legitimate alternative to the manuscript's parity-split exposition.

### First-family operator proof and kernels

`GeneralFunctionalCalculus.lean:19–20` defines `h(z)=sqrt(‖z‖)` and `k(z)=z/h(z)`. Lean's total division at zero is not relied on as an inverse: lines 49–61 explicitly prove continuity at zero from `‖k(z)‖=sqrt(‖z‖)`, and lines 63–77 prove `h* k=z` and `k* k=‖z‖`, splitting or handling zero explicitly.

The CFC commutation step at lines 109–126 is proved from unitary conjugation and uniqueness of continuous functional calculus. The spectrum's unit modulus is derived at lines 129–146. Thus the arbitrary-Hilbert proof does not borrow a finite-matrix spectral theorem or assume all spectral values have the equality form.

`GeneralCommuting.lean:46–78` constructs all factors and the scalar gap from CFC. The existential certificate at line 96 is the theorem's conclusion; it is not part of admissibility. The Hilbert endpoint has only a complete complex inner-product space, bounded operators, normalized state vector, unitarity, cross-party commutation, and d≥2. There is no finite-dimension typeclass, full-rank condition, fixed eigenbasis, or maximality assumption.

The residual is expressed as `H_y A0* − K_y B_y`. This is an alternative continuous factorization; it need not first introduce the discontinuous canonical phase at zero. Mathematically the manuscript residual is its left multiplication by A0, which preserves its adjoint-square because A0 is unitary. The final gap has the same three nonnegative contributions and correct factors of one half. The finite-state version separately proves the trace bound and tensor-lifts actual encoded PVMs.

### General polar identity: exact scope

The assumptions at `GeneralCoveragePolarCanonical.lean:78–80` are

1. `C = V sqrt(C* C)`;
2. `(V* V) sqrt(C* C) = sqrt(C* C)`;
3. B unitary and C commuting with B.

These are sufficient polar-factor premises, not the desired residual identity in disguise. They are weaker than demanding a globally unitary V. The square-root support-isometry transfer at lines 33–43 uses a C*-zero-product argument, not an inverse or closed-range premise. Left modulus and left half-modulus are proved by positive-square-root uniqueness at lines 46–72. Commutation of B with the required modulus is derived at lines 90–95; it is not passed in as a stronger unexplained premise. The final residual is exactly the manuscript's expression in actual positive square roots.

There is no separate theorem constructing an arbitrary Hilbert-space canonical V, proving its uniqueness, or deriving V's strong-limit formula. Therefore “every derivation in the polar-decomposition discussion is formalized” would overstate the delivered artifact. The narrower documented claim—identity for a supplied polar factor, plus an unconditional independently proved commuting upper bound—is supported. No repair is necessary for that documented scope.

### Second-family coefficients and bound

The delivered coefficient formula uses `(-1)^(l.val+1)`. The explicit integer-exponent bridge at `GeneralSecondCoefficients.lean:24–41` establishes equivalence to `(-1)^(l−1)`, including l=0. The phase is the actual complex exponential, and nonzero sine denominators are proved at lines 56–74.

Normalization is deduced from signed geometric sums, the exact compression `S_l=d λ_l r_l` at line 197, unit modulus of `r_l`, and Parseval at lines 203–226. This replaces the manuscript's differentiated sine-product proof; it establishes the same coefficient normalization. The general cosecant-square identity for an arbitrary nonpole shift x is not independently formalized by this coefficient theorem. That displayed intermediate identity should not be advertised as an additional checked endpoint.

The SOS expansion at `GeneralSecondCommuting.lean:46–89` has the correct complex conjugations and dimension factors. The generic algebraic theorem assumes coefficient normalization, as it should, but `second_commuting_hilbert_bound` discharges it with `generalLambda_normalization hd`. No same-party commutation is required; indeed the algebraic SOS does not require cross-party commutation either. This stronger validity does not weaken its application to Bell strategies. The actual PVM endpoint is at lines 189–197.

### Source polar correspondence and attainment

The definition `sourceCanonicalPolar := ((sourceBob)^T)*` at `GeneralCoverageSourceCanonical.lean:16` could look circular if one checked only its name. It is not sufficient by itself, and I traced the additional proof chain:

- `GeneralSourceFourier.lean:29–38` defines `sourceBob` independently as the literal cosecant-coefficient sum of `X^(k+1) Z^k`, retaining the order of the two matrices.
- `GeneralCoverageSourceWeyl.lean:25–91` derives the transpose/relative-unitary polynomial identity with the triangular phase.
- `GeneralCoverageSourceLiteralInterpolation.lean:48–88` handles the k=d−1 wrap term and identifies that polynomial on every equality root with the actual inverse polar phase.
- `GeneralCoverageSourceFactors.lean:12–62` transfers the literal polynomial through the real finite spectral calculus and proves unitarity. The finite-spectrum restriction is explicit and appropriate here because this strategy is on ℂ^d.
- `GeneralCoverageSourceCanonical.lean:30–83` proves positivity, actual factorization, and equality of the constructed modulus to `CFC.sqrt(C* C)`. Thus “canonical” is supported by more than a naming choice.
- Lines 85–105 construct a two-sided modulus inverse using proved spectral nonvanishing. Lines 121–132 prove `B_y^T=H_y^−1(1+W_y*)Z*` with that inverse.
- `GeneralCoverageSourceOrder.lean:51–66` proves order d from the twisted product and the scalar orbit product. `GeneralCoverageSourceSpectrum.lean:210–235` proves full simple spectra; it is not just checking order d.
- `GeneralCoverageSourceStrategy.lean:13–42` builds actual PVMs and a positive normalized maximally entangled state, with the extra Bob observable Z*. Lines 80–104 derive the exact reduced expectation and augmented attainment from those actual matrices.

The transpose and adjoint conventions match the bundled manuscript. I found no assumed coefficient-to-polar equivalence, circular validity assumption, or hidden d=prime restriction.

## Limits and recommended public description

This is a semantic/source audit, not an independent compiler run. The source proof chains appear complete, and the statements match the assigned manuscript targets at their advertised scopes; the coordinator's clean build and axiom/dependency audit must supply the executable verification receipt. The broader package's closure, adversarial, rigidity, permutation, and privacy endpoints have separate reviewers and are not certified by this report.

An accurate public description for this scope is: “The companion formalizes the scalar maximum and equality set, both families' finite and commuting-operator upper bounds, the literal second-family coefficient normalization and SOS, and canonical source-strategy correspondence and attainment. The general polar identity assumes a supplied polar factor; arbitrary polar-decomposition existence and the strong-limit construction are outside scope.”

No external communication occurred. No manuscript or package source was modified.
