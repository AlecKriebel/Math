# Reviewer guide

The most useful review has two parts: compare the Lean definitions and endpoint statements with the manuscript, then reproduce the compiler and axiom checks. [Verification status](verification/README.md) records the latter; [COVERAGE.md](COVERAGE.md) records the intended correspondence. Neither file substitutes for inspecting the mathematical statements.

Most all-dimensional declarations use the namespace `CyclicBell.General`; generic analytic helpers may use `CyclicBell.General.Coverage`. The earlier explicit four-dimensional calculations use `CyclicBell.D4`. The [library entry point](CyclicBell.lean) lists the imported modules.

## 1. Check the source conventions first

Read manuscript `app:attainment` beside these files. This route is useful for checking that the companion treats the same observables and coefficients as the paper.

| Check | Source and entry points |
| --- | --- |
| Positive clock `Z`, forward shift `X`, triangular exponent and cosecant coefficients | [GeneralSourceFourier.lean](CyclicBell/GeneralSourceFourier.lean): `sourceClock`, `sourceCoeff`, `sourceBob`, `source_coefficient_DFT` |
| The two source Fourier sums and explicit qutrit signs | Same file: `source_fourier_zero`, `source_fourier_one`, `source_qutrit_operator` |
| Transpose and complex conjugation in the maximally entangled trace identity | [GeneralWitness.lean](CyclicBell/GeneralWitness.lean): `phi_trace`; [GeneralCoverageSourceWeyl.lean](CyclicBell/GeneralCoverageSourceWeyl.lean): `sourceBob_transpose_polynomial` |
| Literal coefficients equal the polar function on the actual spectrum | [GeneralCoverageSourceFactors.lean](CyclicBell/GeneralCoverageSourceFactors.lean): `sourceBob_transpose_finiteCalc`, `sourceBob_unitary` |
| Actual positive modulus, its inverse, and `Q_y=H_y⁻¹(1+W_y†)Z†` | [GeneralCoverageSourceCanonical.lean](CyclicBell/GeneralCoverageSourceCanonical.lean): `sourceModulus_eq_relative_modulus`, `sourceModulus_inverse`, `sourceBob_transpose_inverse_formula`, `sourceBob_canonical_polar` |
| Measurement order and full simple spectra | [GeneralCoverageSourceOrder.lean](CyclicBell/GeneralCoverageSourceOrder.lean): `sourceBob_order`; [GeneralCoverageSourceSpectrum.lean](CyclicBell/GeneralCoverageSourceSpectrum.lean): `source_relative_full_simple_spectrum`, `sourceBob_full_simple_spectrum` |
| Actual source PVMs, state, and attained Bell value | [GeneralCoverageSourceStrategy.lean](CyclicBell/GeneralCoverageSourceStrategy.lean): `sourcePhysicalStrategy_encodings`, `sourcePhysicalStrategy_attains` |

Unitarity and measurement order are proved from the literal coefficients and functional calculus before constructing the source strategy. They are not inferred merely from the two Fourier sums reaching the desired score.

## 2. Inspect the physical models and exact values

Start with [GeneralModel.lean](CyclicBell/GeneralModel.lean): `StateOn`, `Measurement`, `StrategyOn`, `encoded`, and the Born-probability definitions. The finite models allow arbitrary finite local dimensions and mixed states; the number of outcomes is `d`, not a restriction on local dimension.

[GeneralCommutingModel.lean](CyclicBell/GeneralCommutingModel.lean) supplies complete-Hilbert commuting PVM models. [GeneralCorrelationValues.lean](CyclicBell/GeneralCorrelationValues.lean) defines the actual behavior sets `Qq`, `Qqa`, `Qqc` and their Bell suprema. Its four `*_values_q_qa_qc` endpoints state the reduced and augmented values for both families. `Qqa` is the topological closure of `Qq`.

For the first family, follow [GeneralScalar.lean](CyclicBell/GeneralScalar.lean), [GeneralFirstBound.lean](CyclicBell/GeneralFirstBound.lean), and [GeneralCommuting.lean](CyclicBell/GeneralCommuting.lean). They separate the scalar extremum, finite mixed-state bound, and arbitrary-Hilbert bound. [GeneralCoveragePolarCanonical.lean](CyclicBell/GeneralCoveragePolarCanonical.lean) states the manuscript's general polar identity using actual nested positive square roots.

For the second family, read [GeneralSecondCoefficients.lean](CyclicBell/GeneralSecondCoefficients.lean), [GeneralSecondBound.lean](CyclicBell/GeneralSecondBound.lean), [GeneralSecondWitness.lean](CyclicBell/GeneralSecondWitness.lean), and [GeneralSecondCommuting.lean](CyclicBell/GeneralSecondCommuting.lean). Check the literal coefficients and normalization before the SOS and value endpoints.

The separate [GeneralCoverageClosureContainment.lean](CyclicBell/GeneralCoverageClosureContainment.lean) proves `Qqa_subset_Qqc` for finite input alphabets through an actual limiting Hilbert-space construction. The specific Bell-value proofs do not assume this inclusion.

## 3. Review permutation blindness and support rigidity

[GeneralPermutation.lean](CyclicBell/GeneralPermutation.lean) states the conditional phase-permutation theorem. Its scalar cap, phase alignment, and cyclic-product hypotheses are part of the manuscript theorem. [GeneralCoveragePermutation.lean](CyclicBell/GeneralCoveragePermutation.lean) adds arbitrary-Hilbert bounds, local moments, and all first-harmonic invariances; [GeneralCoverageWitness.lean](CyclicBell/GeneralCoverageWitness.lean) exposes the simple-spectrum and complete-moment packages.

For the explicit biased maximizers, follow [GeneralChirp.lean](CyclicBell/GeneralChirp.lean), [GeneralSwap.lean](CyclicBell/GeneralSwap.lean), [GeneralGuessing.lean](CyclicBell/GeneralGuessing.lean), and [GeneralFirstWitness.lean](CyclicBell/GeneralFirstWitness.lean). The all-dimensional nonuniform witnesses require `d≥4`; the separate `d=2,3` statements concern the specified permutation orbit.

[GeneralRigidity.lean](CyclicBell/GeneralRigidity.lean) derives `supported_multiplicity_rigidity` and `supported_dimension_divisible` from physical maximality on the range of the actual reduced state. Inspect the support and saturation modules it imports to check how invariance, kernel-safe cancellation, and adjacent reflections are derived. The result does not classify the whole maximizing face or constrain an unused ambient complement.

## 4. Separate observed tables from adversarial guessing

[GeneralTripartite.lean](CyclicBell/GeneralTripartite.lean) uses actual finite ABE states, AB PVMs, and general Eve POVMs. [GeneralAdversarialValues.lean](CyclicBell/GeneralAdversarialValues.lean) defines the three value-conditioned guessing quantities. In the approximate model, closure is taken over full extended correlations **before** imposing the exact Bell-score constraint.

The first/second guessing endpoints give quantitative lower bounds witnessed by valid strategies, together with the upper bound one. They do not identify an exact worst-case optimum. [GeneralPOVMMaximum.lean](CyclicBell/GeneralPOVMMaximum.lean) and [GeneralNestedGuessing.lean](CyclicBell/GeneralNestedGuessing.lean) separately prove attainment of each finite-Eve fixed-realization POVM maximum and its connection to the outer supremum.

For the binary benchmark and settings minimality, read [GeneralBinaryCertification.lean](CyclicBell/GeneralBinaryCertification.lean), [GeneralBinaryWitness.lean](CyclicBell/GeneralBinaryWitness.lean), and [GeneralOneInput.lean](CyclicBell/GeneralOneInput.lean). Binary privacy quantifies over compatible finite purifications; the Hilbert-space Bell upper bound is a separate result.

## 5. Review the settings appendix independently

Read [GeneralPhaseTables.lean](CyclicBell/GeneralPhaseTables.lean), [GeneralPhaseBounds.lean](CyclicBell/GeneralPhaseBounds.lean), [GeneralAnchoredTables.lean](CyclicBell/GeneralAnchoredTables.lean), and [GeneralPhaseEntropy.lean](CyclicBell/GeneralPhaseEntropy.lean). These construct the actual phase PVMs, prove their tables and peaks, cover the qubit anchor exception, and derive the observed entropy asymptotic. They do not formalize the external self-testing theorem cited by the manuscript.

[GeneralCoverageExposure.lean](CyclicBell/GeneralCoverageExposure.lean) gives the computational-MUB operator-space and coefficientwise exposure obstruction. Its scope is coefficientwise saturation, not a universal obstruction to additional measurements or joint Bell certificates.

## Reproduce and inspect evidence

Run `python3 scripts/check.py --bootstrap` from the package directory. For a preliminary scan use `--static-only`; for the library alone use `lake build`. Full instructions and trust boundaries are in [AXIOMS.md](AXIOMS.md).

The [claim ledger](reference/paper_claim_ledger.json) and [declaration inventory](reference/source_inventory.json) support targeted inspection. Expanded statement examples and the [validation controls](validation/) help detect changed normalizations, coefficients, conjugations, or model domains. A designated proof rejection is a regression check, not by itself a proof that the target proposition is false.
