# Independent review of the delivered cyclic Bell Lean companion

Reviewed 16 September 2026 Pacific (17 September UTC).

**Disposition: substantial and apparently faithful formal coverage of the principal results, with specific omissions that should be closed or disclosed before calling this a complete formalization of the paper.** No incorrect principal mathematical endpoint was found in the independent source review. This does not establish that every manuscript assertion has a matching Lean theorem.

**Fresh machine replay: PASSED.** Clean project build, all 1,852 declaration axiom reports, five acceptance controls, twenty deliberate proof-error controls, statement compilation, and input/dependency integrity checks passed.

## Exact artifact and manuscript

- Received: `cyclic-bell-lean-review.zip`, SHA-256 `f1bcadd327b0321f4277baa8b136723da2b15bbc878ab5f9d2de3fbe949b73e9`.
- Safely extracted 225 files; all 224 entries in the included content manifest matched. Review used this extraction, not a possibly newer working directory.
- Bundled `reference/manuscript/main.tex` is byte-identical to the repository's current canonical `cyclic_bell_exact_values_and_randomness/main.tex`, SHA-256 `82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`, Git blob `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
- Bundled PDF SHA-256 is `9d0d23837aed20346f6e97234095ee146f7e7b852c7a4a4b5d646e5fa595c0f6`, the same merged v1.1 manuscript identified in the preceding website/source review.
- No mathematical source, existing manuscript, or delivered archive was changed during this review.

## Findings to address before a completeness claim

### 1. The second family's complete first-harmonic statement is not assembled

Manuscript Theorem `thm:second` explicitly says the full complex correlator matrix is permutation-independent. The required formulas are

⟨A_l B_y⟩ = λ_l ω^(−ly), and ⟨A_l B_d⟩ = δ_(l,0),

for every Alice row l and every Bob input, with vanishing local first moments.

The package proves physical second-family measurements, exact Fourier compression, attainment, and the biased target table. But it does not explicitly state and prove that full d-by-(d+1) physical matrix and all its local moments. The theorem named `linear_permutation_all_harmonics_invariant` in `GeneralCoveragePermutation.lean:160` applies to a different generic construction with `x : Fin 2`, so it cannot by itself be cited as the second family's endpoint. `secondPermutation_aligned_correlator` only supplies one real aligned entry.

Two independent source inspections confirmed this. Crucially, the generic weighted-cycle identity `GeneralCycles.first_harmonic_permutation` does apply to arbitrary weights and, together with the proved second-family encodings and Fourier compression, supplies the missing proof. This is a short missing assembly/statement bridge, not evidence that the paper's claim is false or that the existing counterexample proof is invalid. Explicit endpoint signatures and the derivation are in [permutation_review.md](permutation_review.md).

### 2. The alternate Bob-adjoint convention is not transported explicitly

The theorem also discusses the source convention that adjoints all Bob observables and inverts outcomes b↦−b. The package has a `negateMeasurement` constructor, but no theorem identifying its encoded observable with the adjoint and applying the resulting probability relabeling to the cyclic second-family strategy. The chosen main convention is consistent and correct.

Add a generic encoding/behavior transport lemma and its cyclic application. When claiming Bell-value preservation, transport the functional as well: simply adjointing Bob while keeping arbitrary coefficients fixed is not a valid invariance argument. This is a correspondence omission, not a sign error found in the delivered main construction.

### 3. Some proof infrastructure is deliberately outside scope

`GeneralCoveragePolarCanonical.lean:130` proves the arbitrary-Hilbert positive-factor identity from a supplied factor satisfying the actual polar factorization and initial-isometry equations. It does not construct the arbitrary canonical polar decomposition, prove its general uniqueness or von Neumann algebra membership, or establish the paper's strong-limit representation. That boundary is disclosed in COVERAGE and STATEMENT_REVIEW.

This does **not** leave the principal first-family bound conditional: its arbitrary-Hilbert proof constructs different functional-calculus factors and is unconditional under the stated unitarity and cross-party commutation assumptions. The source attaining matrices also have an explicit canonical-polar construction. Keep the boundary visible, or close it if the intended promise is verification of every analytic argument in the manuscript.

Similarly, all-dimensional second-family residual annihilation is not a separate endpoint, although proved scalar attainment and the independently proved positive SOS suffice for maximality. If claiming every clause of `thm:second` explicitly, expose that residual-zero consequence too.

### 4. The claim ledger retains outdated qualifications

An earlier ledger row says no Qqa⊆Qqc theorem is claimed; a later row and the actual source prove it. Another older row says no source canonical-polar identification is claimed, while the later source-canonical module supplies one. Qualify these as module-local historical descriptions or update them to describe the final package. These inconsistencies concern reviewer guidance, not mathematical correctness.

## What the substantive source review supports

Five separate AI-assisted audit tracks inspected the actual Lean definitions, assumptions, proof chains and corresponding manuscript passages; the coordinator additionally inspected the settings appendix and verification tooling. These are independent task passes, not external human peer review. Package self-reports were not used as evidence of correctness.

| Area | Source-review result |
|---|---|
| Scalar extremum and equality phases | Arbitrary unit-circle input and every d≥2; no equality premise smuggled into the bound. |
| First/second quantum values | Literal coefficients, actual arbitrary finite mixed-state strategies, arbitrary complete-Hilbert commuting bounds, and genuine q/qa/qc suprema. |
| Physical model bridges | Actual purification and behavior preservation; approximate correlations use closure; the observed Qqa⊆Qqc bridge constructs a limiting Hilbert/PVM model. |
| Biased maximizers | Physical states and PVMs, derived Born/Fourier table, all-d swap and quantitative gap, actual d=4 probabilities 1/32 and 3/32. |
| Supported rigidity | Starts from physical saturation, derives the actual reduced-state support and equal positive root multiplicities; no hidden spectral/rank assumption. |
| Literal source strategy | Correct signs/transposes, coefficient interpolation, unitarity/order, canonical source modulus, simple spectra, physical attainment. |
| Randomness | General Eve POVMs, full extended-correlation closure before the maximal-value slice, correct guessing/entropy inequality directions. No exact worst-case optimum is falsely claimed. |
| Binary/private-MUB/one-input | Actual score-to-privacy proof, supported sufficient criterion, full behavior reconstruction with perfect guessing; correct finite/purified scope. |
| Settings appendix | Actual phase-basis tables, exact peaks, entropy limit, anchored d=2 exception and coefficientwise MUB obstruction. |

## Changes of proof that are legitimate

- The rigidity proof uses purification amplitudes, a supported finite spectral pseudoinverse, and a rectangular telescoping rank argument. The final assumptions and supported multiplicity conclusion agree with the manuscript.
- The MUB obstruction uses constant diagonal plus positivity instead of the paper's Toeplitz/SVD calculation. It proves a stronger statement with the required conclusion.
- Coefficient normalization uses Fourier compression and Parseval instead of separately proving the general shifted cosecant-square identity. The needed normalization is fully derived.
- The Fourier-bias proof obtains a stronger intermediate estimate and explicitly derives the paper's stated weaker bound. This is not a changed normalization.

A formalization need not duplicate every intermediate calculation when it proves the same result from the same or weaker assumptions. These differences should be documented as alternate proofs, not treated as errors.

## Reproduction and trust boundary

The independently replayed run `20260917T040838993157Z` completed successfully in 939.8 seconds. It ran 66 recorded commands and rebuilt all 106 project Lean source files from a cleared project build directory using Lean 4.19.0, compiler commit `6caaee842e9495688c1567e78c0e68dbb96942aa`, and the pinned Mathlib commit.

All 1852 named-declaration reports were present and accepted. The only axioms used were `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx`, custom axioms or native-trust shortcuts appeared. Five acceptance controls compiled; all twenty deliberate proof-error controls failed in their designated proof bodies, rather than from imports, syntax or resource exhaustion. Such rejected proof attempts are regression checks, not independent proofs of negated propositions. The expanded Statements file compiled, and the runner confirmed protected source/manuscript hashes and dependency revisions remained unchanged.

Separately, 63 runner tests and 24 packaging tests passed. See the [replay summary](reproduction/summary.json), [full fresh receipt](reproduction/20260917T040838993157Z/run.json), and [fresh compiler/axiom output](reproduction/20260917T040838993157Z/022.log).

The initial runner command used a mistaken relative path to the external manuscript and stopped before invoking Lean; the corrected run used the absolute canonical path. Both facts are logged. The clean replay uses the pinned Lean compiler and copied upstream dependency caches with verified clean source revisions. It rebuilds the entire companion; it does not independently rebuild Lean itself or all of Mathlib from source. Successful axiom checks certify the encoded propositions within this normal Lean trust boundary, not automatically their correspondence with prose or the research's novelty.

## Recommendation

Make the focused endpoint/documentation revision in [REPAIR_PLAN.md](REPAIR_PLAN.md), then rerun verification on the new archive. The current material is a substantial formal companion and should help reviewers check the central results; it should not be introduced as an exhaustive, issue-free formalization of every assertion in the paper.

Because the requested follow-up email was conditional on full verification, this review does not supply a message claiming that condition has been met. No email was sent or external contact initiated.

Detailed evidence: [operators](operator_review.md), [permutations](permutation_review.md), [models](model_review.md), [rigidity/source strategy](rigidity_review.md), [randomness](randomness_review.md), [settings/tooling](settings_review.md).
