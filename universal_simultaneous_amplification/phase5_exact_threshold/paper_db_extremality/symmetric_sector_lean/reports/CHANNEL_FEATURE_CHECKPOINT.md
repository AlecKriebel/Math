# Rational-channel to physical-feature checkpoint

Timestamp: 2026-09-14T14:57:11Z

Implementation report, not an independent review.

The assigned coefficient/feature linkage is complete (100% of this bounded
Stage 3 subtask). `SymmetricSector/ChannelFeatures.lean` compiles and all
principal proof dependencies are the standard foundational axioms only.

The module first derives the actual rational `coefficientK` actions from its
concrete block entries, in the physical coefficient direction. Those actions
are then transported into real coefficients using the actual `coeffA` and
`coeffB` finite-channel extensions from `PhysicalBridge`.

| Exact connection | Lean theorem |
| --- | --- |
| Actual K good row | `coefficientK_good_action` |
| Actual K bad row | `coefficientK_bad_action` |
| Real feature coefficient A equals cast of actual K action | `Active.featureCoeffA_coefficientK` |
| Real feature coefficient B equals cast of actual K action | `Active.featureCoeffB_coefficientK` |
| Actual labeled K₀ intertwines with finite K | `Active.K0_coefficientFeature` |
| Actual source is the physical perturbation of rankPotential | `Active.coefficientFeature_source` |
| Actual rational inverse solves the coefficient system | `Active.coefficientSolution_equation` |
| Its real feature solves the actual physical Poisson residual | `Active.coefficientFeature_poisson` |

The last three physical statements require `n ≥ 4` and the actual
`SymmetricBalanced δ` condition. They do not assume a feature representation
is injective. At rank one the bad feature vanishes by the proved singleton
identity. At rank `N=n−1`, both features vanish by the proved row/column
identities. All other ranks use the explicit finite row equations.

The zero extensions also prove the manuscript's coefficient conventions
directly: `coeffB_one`, `coeffA_of_le`, and `coeffB_of_le` establish
`b₁=0` and `a_N=b_N=0`, including all higher absent ranks. `coeffA_zero`
handles the extra zero lower good coordinate.

The actual coefficient solution is defined as `(1−coefficientK N)⁻¹*source N`.
Its equation uses `coefficient_system_isUnit`, already proved for the actual
finite matrix, rather than a solver assertion. The physical Poisson theorem
then follows by linearity and the kernel intertwining.

The final Green-operator normalization and physical R² identity are assembled
separately in `PhysicalIdentity`; exact reward normalization is handled in
`Reward`. This module does not itself claim the final scalar positivity or
the complete fixation-Hessian theorem.

Reproduction:

```text
lake build SymmetricSector.ChannelFeatures
lake env lean reports/ChannelFeatureAxioms.lean
```

The audit output is saved in `reports/channel_feature_axioms.log`. Its
dependencies contain only `propext`, `Classical.choice`, and `Quot.sound`;
some simple endpoint lemmas require only a subset of those axioms.
