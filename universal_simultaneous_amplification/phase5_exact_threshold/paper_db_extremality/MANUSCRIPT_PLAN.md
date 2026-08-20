# Manuscript plan and theorem ledger

## Headline theorem suite

1. **Fitness-two full local optimality.** For every `n >= 3`, the uniform
   complete loopless kernel is a strict nondegenerate local maximizer of
   uniformly initialized dB fixation over the full positive loopless
   row-stochastic kernel polytope.
2. **Fixed-graph strong-selection rigidity.** No fixed finite loopless
   directed weighting strictly amplifies dB fixation for every beneficial
   fitness.  Complete support has an explicit incoming-column sum-of-squares
   deficit; the equality class is dynamically complete.
3. **Global low-order slices.** Every nonuniform positive weighted triangle
   is a strict suppressor at every beneficial fitness; the same holds in the
   two displayed maximally symmetric weighted `K_4` families.

## Exact dependencies

- coverage dual and active collision:
  `../r2_coverage_submodular/` and `../r2_determinant/ACTIVE_R2_DETERMINANT.md`;
- complete-refresh expansion and antisymmetric sector:
  `../r2_determinant/COMPLETE_REFRESH_FOREST.md`;
- physical standard column-imbalance sector:
  `../r2_standard_physical_phase/PHYSICAL_STANDARD_PHASE_THEOREM.md`;
- symmetric sector:
  `../r2_determinant/TRUE_INVERSE_RANK_SYMMETRIC_PHASE_CONTRACTION.md`;
- independent regular-undirected Hessian check: `../r2_regular_sector/`;
- strong-selection, triangle, and symmetric-`K_4` proofs:
  `../../../paper/` and the root verification packages.

## Scope exclusions

- no global all-kernel maximality theorem at fitness two;
- no population-uniform neighborhood around the complete kernel;
- no upper bound on the simultaneous-amplification threshold;
- no claim that finite exact verification replaces the displayed universal
  analytic certificates.
