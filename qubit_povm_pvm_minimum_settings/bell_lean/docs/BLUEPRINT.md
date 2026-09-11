> **Historical cloud-stage document.** Statements below about missing compilation or unfinished targets describe the incoming archive. Current local verification and the precise certified scope are recorded in [CERTIFICATION.md](../CERTIFICATION.md); this document is retained as research provenance.

# Resume blueprint — continuation v0.2.0

## First unfinished computation: compile the existing source

```bash
cd bell_lean
bash scripts/check.sh --bootstrap
```

The saved wrapper exits 127 before any Lean build because `lake` is absent.
No source error has yet been observed by Lean. A working toolchain is required
before proof status can advance beyond “source attempt.” Do not interpret the
absence of compiler diagnostics as an absence of errors.

Retain the pinned Lean/Mathlib pair for the first replay. Validate the reconstructed
Lake manifest, obtain dependencies, and repair parsing/API/tactic errors. Then run
the generated all-declaration axiom audit; only standard `propext`,
`Classical.choice`, and `Quot.sound` are accepted. Any deliberate toolchain update
must be recorded and all proofs rechecked; a published release also merits an
up-to-date kernel/toolchain review rather than relying only on an old pin.

## Preserve the completed exact stages

```bash
python3 -m pip install -r requirements.txt
bash scripts/replay_exact.sh
```

This replay does not generate the expensive numerical SOS search. Preserve
`certificates/binary_pair_sos.json`: it already passes two independent exact
positivity calculations and a universal word-identity checker. The floating-point
search is retained for provenance, not required for reproduction.

Likewise retain the projective-fiber maps and successful rational reconstruction
reports. There is no need to regenerate the earlier resultant computation.
The current finite grid checks, permutation checks and checksums are in `reports/`.
Do not count them as general Lean proofs.

## Stage 1 — get the explicit separation branch through Lean

The previous checkpoint's Schmidt-state/deficit route is no longer the preferred
implementation. A shorter, stronger rational SOS route is already written:

```text
Quantum / Expectation / ProjectionSupport
                  ↓
SOSAlgebra / SOSCertificate / ProjectiveSOS
                  ↓
ProjectiveBound.projective_strategy_rational_upper
                  ↓
projective_global_upper_bound / three_by_two_separation
```

It includes the physical zero-effect PVM reduction, arbitrary complex mixed-state
positive expectation, all three auxiliary support pairs, the exact witness, and
convexification. Compile and repair these modules instead of introducing another
upper-bound assumption. If the big numeric proof is slow, split the 144 LDL entry
proofs or use a verified reflection tactic; do not replace them by an asserted
Boolean or an axiom.

Success is an **unconditional kernel-checked physical separation theorem**, not
just a checked Gram matrix. Keep the explicit definition-fidelity review. The
new bound is not asserted to be optimal.

## Stage 2 — compile the one-input and algebraic rank modules

`OneInput` now contains the actual complete-strategy mixture for one setting on
either side, with zero input/marginal cases and dependent alphabets. Compile its
classical product and Born-law dependencies. This is distinct from the missing
one-binary-party theorem with *two* inputs.

For the residual geometry, compile:

```text
Lorentz → ProjectiveFiber → RankOne
Lorentz → RankZero → RankZeroSimulation
LocalSimulation + Relabeling ────────↑
Lorentz → UphillDirection
```

The projective-fiber source covers all generic/exceptional cases. Rank zero
retains the actual output permutation. The high-rank shortcut uses four rank-one
directions and at most three compatibility equations, not a full inertia
classification. The source statements make their algebraic hypotheses explicit.

## Stage 3 — supply the missing physical/analytic layer

This remains substantial work; the compiled algebraic modules will not replace it.

### 3a. Compactness and residual reduction

Prove compactness of the actual finite-dimensional strategy images/hulls, convex
separation and exposed extreme maximizer selection. Formalize arbitrary
stochastic postprocessing through deterministic PVM maps.

Prove the three-dimensional pointed-cone circuit decomposition and the physical
one-binary-party simulation, including scalar and parallel observables, zero
rays, rank-deficient circuit sums, and one common hidden variable. Formalize
physical common-span filtering and the extremal qubit POVM rank-square argument
needed to reduce a strict maximizer to the genuine binary/ternary residual class.

### 3b. Actual incidence coordinates and physical curves

Prove the complex Pauli trace/determinant pairings, pure steering representation,
all factors of 2 and determinants, invertibility, strict inequalities, and
Lorentz signature. Then construct nearby physical strategies from normalized
incidence data and prove that every incidence tangent integrates to a two-sided
physical curve. Zero *joint* probabilities must not be excluded by treating
nonnegativity as an extra strict hypothesis.

One possible simplification to investigate is an explicit frame instead of
abstract Gram–Schmidt. In the paper's Pauli coordinates set

```text
E1 = (1/2, 0, 0, 1/2)
E2 = (1/2, 0, 0,-1/2)
E3 = (a+c, 2 sqrt(ac), 0, c-a)
f  = 2(ad+bc) - (a+b+c+d-1/2)
E4 = (b+d, f/(2 sqrt(ac)), sqrt(4bd-f²/(4ac)), d-b).
```

The positivity of the last radicand, frame identities, and smoothness must be
proved from the actual physical-domain assumptions. These formulas are
**continuation notes, not an implemented theorem**. An explicit positive 2×2
square root `(ρ + sqrt(det ρ) I) / sqrt(tr ρ + 2 sqrt(det ρ))` may similarly
simplify smooth reconstruction once its hypotheses are established.

### 3c. Strict multipliers and Hessian/compatibility bridge

Prove finite POVM strong duality with attainment and complementary slackness.
Derive the determinant pullback and identify its normalization multiplier with
the dual operator. When a multiplier vanishes, deterministic replacement must
preserve the score and yield a local behavior. This forces strict positivity at
a hypothetical strict non-PVM maximum.

Differentiate the inverse-metric incidence equations, identify the weighted
second form, and derive the Fredholm compatibility conditions. For rank D≥2,
produce a basis of at most three compatibility coefficients and show λ lies in
its span. A positive vector for S=Pᵀg⁻¹P can be chosen as v=P⁻¹gu, with value 1;
this observation still needs its matrix/physical formal proof. Then instantiate
`normalized_uphill_of_three_compatibilities`, integrate the physical tangent, and
contradict local maximality.

For rank one, instantiate `RankOne` from the actual metric differential, distinct
source rays, and positive multipliers. For rank zero, instantiate
`rank_zero_transformed_table_mem` from the physical null/base/future/normalization
conditions and return through the original output relabeling/embedding.

## Stage 4 — finish the universal theorem, not just its wrapper

Prove `UniversalTwoInputEquality` without additional assumptions for every
finite input-dependent two-input output architecture. Only then supply it to
`main_claims_of_two_input_equality` and `minimum_inputs_of_two_input_equality`.
The wrappers are intentionally conditional until this stage is complete.

Rebuild every module and audit every declaration. Review the model statement
against the paper, especially dimension, finite alphabets, zero projectors,
postprocessing, and shared randomness. There is no theorem-count threshold or
finite test count that substitutes for these end-to-end obligations.

## Separate remaining Appendix B stage

`StrengthenedAttainment` still requires the nonmaximally entangled physical state,
observables, and ternary POVM construction. The scalar strengthened bound and
family comparison already written do not imply that physical attainment. Keep
this auxiliary target separate from the minimum-setting theorem.

## Ongoing checkpoint discipline

After a completed stage, update source hashes, actual build/axiom logs, claim
coverage, and `reports/status.json`. Then package outside the source root:

```bash
python3 scripts/package.py ../bell_setting_lean_continued.zip
```

Never promote an uncompiled source attempt to a proof, an assumed physical bridge
to a proved one, a finite benchmark to a universal result, or a subset build to
full-paper certification. No remote branch or manuscript was changed during the
present continuation.
