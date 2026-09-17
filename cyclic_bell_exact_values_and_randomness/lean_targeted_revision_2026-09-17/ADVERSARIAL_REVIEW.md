# Adversarial source review of the targeted second-family revision

Date: 2026-09-17. Completion estimate: **100% of this bounded source-level review**.
This is an independent agent review, not a human specialist endorsement. It
compares the frozen new statements and proof dependencies with the bundled
manuscript and the earlier independent review's REPAIR_PLAN.md. The reviewer
made no production source or documentation edits and ran no Lean/Lake build.
The coordinating agent owns the final integrated clean build and axiom audit.

## Verdict

No unresolved mathematical or semantic deficiency was found in the three
new proof modules. They close the three targeted omissions in manuscript
`thm:second`: the full complex first-harmonic matrix and all local first
moments, literal state-vector SOS residual annihilation, and transport to the
Bob-adjoint output convention. Their hypotheses match the intended dimensions
and physical strategies. They do not assume the target conclusions as strategy
validity conditions.

A wording error was found in an existing source-polar claim-ledger row: it
called the source Bob matrix the polar factor itself. The coordinator corrected
it to **the entrywise conjugate of the unitary polar factor**, matching
`sourceBob_canonical_polar`. The corrected wording was rechecked.

This verdict is conditional on the final integrated build/axiom checks. It does
not upgrade the companion to an exhaustive line-by-line formalization or
remove the disclosed boundaries on general polar-decomposition infrastructure,
external self-testing results, or unknown adversarial optima.

## Frozen source identities

Paths below are relative to `lean_formalization/`; SHA-256 was recomputed after
the coordinator confirmed the proof modules frozen.

| File | SHA-256 |
| --- | --- |
| `CyclicBell/GeneralSecondMoments.lean` | `b02b61335bf0b8b0cfa6cf55d6f93fd62078aaeb0537e84bc3c7f36bdbcdf8e6` |
| `CyclicBell/GeneralSecondResiduals.lean` | `2d39ed961e289683acafcdc24f557fdfee7233bd27e6c4ba0ad4f409e1c8db23` |
| `CyclicBell/GeneralOutcomeRelabeling.lean` | `5ab4f85eedffb87e9f893617dbc0f368d2e364dfa5db1e90c7c08b5739dca1a1` |
| `CyclicBell/GeneralSecondCompletionStatements.lean` | `4e1e3d8984e8e951607f546fac0dc1fc7638fd0441bae873ac24103ee79f34cf` |
| `reference/manuscript/main.tex` | `82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71` |

Primary comparison: manuscript lines 991–1092 (`thm:second` and its proof),
with coefficient/functional/SOS definitions at lines 914–990. The earlier plan
is [REPAIR_PLAN.md](../lean_independent_review_2026-09-16/REPAIR_PLAN.md), items
1–3 and the documentation boundaries in items 4–6.

## 1. Complete moments: quantifiers, phase, and Born linkage

[GeneralSecondMoments.lean](../lean_formalization/CyclicBell/GeneralSecondMoments.lean)
quantifies every `d≥2`, every permutation of `Ix d`, every Alice index `l : Ix d`,
and every Bob index `y : Option (Ix d)`. The array is therefore genuinely
`d × (d+1)`, including the alignment column; it does not reuse a `Fin 2`-Alice
endpoint as a substitute.

The reduced entries are the complex numbers `generalLambda l * chi (-(l*y))`,
not merely their real parts or a weighted Bell sum. The extra column is exactly
`if l=0 then 1 else 0`. All Alice and Bob local first moments vanish, including
the extra setting. The invariance theorem compares arbitrary permutations,
not only a selected swap or cyclic relabeling.

The proof expands the actual encodings, applies the maximally entangled trace
identity to the actual weighted cycles, removes the arbitrary permutation from
the finite sum, and uses the previously proved Fourier shift/compression and
unit-modulus prefactor. This preserves the manuscript's minus character sign.
Character orthogonality supplies the extra column; weighted-shift trace zero
supplies the local moments, with the necessary `d≥2` premise.

`secondPermutation_behavior_correlator` and the aggregate
`secondPermutation_complete_first_moments` explicitly connect the statements to
`behavior (secondPermutationStrategy ...)` via `probabilityCorrelator_behavior`.
The local statements use the strategy's actual density matrix. No synthetic
table is substituted for the Born behavior. The asserted invariance is only
of the complete first-harmonic array and local first moments, not of higher
Fourier orders or the full outcome distribution.

## 2. Literal residuals: scalar, sign, tensor convention, and state

[GeneralSecondResiduals.lean](../lean_formalization/CyclicBell/GeneralSecondResiduals.lean)
proves the vector equation for every `d≥2`, permutation, and residual index:

```
(d * lambda_l * I - A_l tensor Bhat_l) Phi_d = 0.
```

The scalar is the literal complex `d*generalLambda l`, with no conjugation,
absolute value, missing dimension factor, or sign reversal. The `secondFourier`
is the same plus-character Fourier combination used by the existing SOS.
The inlined tensor residual is exactly the tensor realization of
`secondResidual` in GeneralSecondSOS.lean; the SOS prefactor remains the
separately proved `1/(2d)`.

The proof uses exact operator compression `Bhat_l=d*lambda_l*D_l`, the actual
encoding `A_l=entryConjugate D_l`, and the vector identity
`(A tensor entryConjugate A) Phi_d=Phi_d`. It does not confuse entrywise
conjugation with adjoint, or infer vector annihilation merely from scalar
attainment. Its proof dependencies introduce no maximality premise.

The extra residual `I-A_0 tensor B_none` also kills the same state: both actual
observables are the real forward shift `X`, and `X tensor X` fixes Phi_d.
The existing universal SOS/upper-bound theorem remains responsible for global
optimality; residual annihilation is not promoted into a standalone argument
that an arbitrary candidate SOS is valid.

## 3. Output inversion and the transported functional

[GeneralOutcomeRelabeling.lean](../lean_formalization/CyclicBell/GeneralOutcomeRelabeling.lean)
uses the existing valid PVM constructor with effects `M.effect (-b)`. The
encoding theorem proves this sends the observable to its **adjoint**, using
Hermitian effects and the character identity. This is distinct from the
entrywise conjugation used in the weighted-cycle construction.

The transformed strategy keeps the original state and Alice measurements and
negates every Bob measurement's outcomes. Its complete actual behavior is
`p'(x,y,a,b)=p(x,y,a,-b)`. The construction is involutive. The explicit cyclic
endpoint `secondAdjointPermutation_bob_encoded` includes every Bob setting,
including `none`.

The alternate functional is genuinely transported: it uses adjointed encoded
Bob observables in both the Fourier terms and the aligned term. The Fourier
identity is `secondAdjointFourier B l=(secondFourier B (-l))†`, preserving the
plus character in the functional's definition. The attained-value and
maximality conclusions apply this alternate functional to both the relabeled
witness and every finite-dimensional competitor. They do not assert the false
claim that merely adjointing Bob preserves an arbitrary unchanged functional.

`observedMaxEntry` is the attained maximum of a finite observed probability
array. The range-reindexing, nonuniformity, best deterministic fixed-guess,
and quantitative-gap theorems preserve that interpretation. The physical
fixed-guess identity uses the existing actual one-dimensional Eve instrument.
Nothing equates the observed maximum with the optimum over all quantum Eve
extensions. Nonuniform swap/gap conclusions correctly require `d≥4`.

## 4. Boundary cases and adversarial checks

- The complete-moment and residual statements include `d=2` and `d=3`; neither
  silently strengthens its dimension premise to `d≥4`. Only the biased-swap
  consequences use the latter threshold.
- At `d=2`, outcome negation is the identity and order-two encoded observables
  are self-adjoint, so the generic adjoint transport is consistent.
- At `d=3`, inversion is nontrivial, but the swap-bias claim is not asserted;
  the earlier orbit-flatness result remains compatible with the new moments.
- Generic relabeling statements require only nonzero outcome dimension and
  legitimate measurements/strategies; arbitrary finite local dimensions are
  preserved in the transported upper-bound and maximality comparisons.
- A read-only `git diff --name-only ca6389e42` comparison found no changes to
  GeneralModel, GeneralBehavior, GeneralSecondWitness, GeneralSecondSOS,
  GeneralSecondBound, GeneralPhaseTables, or GeneralOperational. Thus the new
  endpoints were not obtained by redefining the underlying physical models,
  coefficients, witness, Fourier transform, or fixed-guess probability.

A separate floating-point diagnostic reconstructed matrices directly from the
manuscript formulas, using only Python's standard library. It checked every
permutation for `d=2,3,4`, plus identity/reversal/final-swap for `d=5,6`: 38
cases. Maximum discrepancies were below `1.9e-15` for complete complex
correlators, extra column, local moments, residual vectors, and the correctly
transported attained score. Deliberately leaving the original functional
unchanged after adjointing Bob gives score 0 instead of 4 in the `d=3` examples,
confirming the importance of the transported-functional distinction.

The diagnostic is **not proof evidence** and does not test all dimensions.
Its reproducible script and report are retained here:
[adversarial_numeric_crosscheck.py](adversarial_numeric_crosscheck.py),
[adversarial_numeric_crosscheck.json](adversarial_numeric_crosscheck.json).

## 5. Expanded interfaces and documentation

[GeneralSecondCompletionStatements.lean](../lean_formalization/CyclicBell/GeneralSecondCompletionStatements.lean)
contains nine expanded examples. They expose the actual Born sums, all Alice
and Bob input types, density traces, literal residual/scaling, PVM outcome
encoding, and both adjointed terms of the transported functional. None adds a
hidden equality, saturation, normalization, or target-table premise.

The new rows in [COVERAGE.md](../lean_formalization/COVERAGE.md), the
second-family paragraph in [REVIEWER_GUIDE.md](../lean_formalization/REVIEWER_GUIDE.md),
and the new entries in [paper_claim_ledger.json](../lean_formalization/reference/paper_claim_ledger.json)
match the inspected source. They distinguish full first-harmonic entries from
all Fourier orders, explain functional transport, and keep observed/fixed-guess
claims separate from worst-case Eve optimization. The corrected source-polar
ledger row now preserves its conjugation convention.

The coordinator reports successful narrow compilation of the frozen modules
and expanded statement examples. This reviewer did not rerun those builds and
does not treat that report as a substitute for the required fresh integrated
library build, complete declaration/axiom inventory, controls, and exact
archive receipt.
