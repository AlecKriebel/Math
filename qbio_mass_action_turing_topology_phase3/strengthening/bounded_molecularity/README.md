# Route A - bounded molecularity reconnaissance

**Status:** killed without a theorem.

The validated reduction realizes a rational row by clearing denominators and placing the resulting signed row coefficients into source complexes. In the `PARTITION` family, entries of `Q=I+aa^T` and the denominator of `beta` grow with the binary input. The resulting source and target molecularities are therefore not bounded by a universal constant.

Three exact replacement ideas were checked conceptually:

1. **Parallel unit reactions.** Replacing a coefficient of magnitude `M` by `M` bounded reactions is exact but pseudo-polynomial in a binary input, so it does not preserve polynomial reduction size.
2. **Reaction splitting through intermediates.** At finite positive rates, added intermediates contribute new Jacobian rows/columns and new positive steady-flux constraints. The desired row image is not preserved exactly; only singular limits recover a Schur complement, which is forbidden here.
3. **Binary catalytic copying.** A polynomial-size binary coefficient gadget would need to impose exact multiplicative/copy constraints at every positive equilibrium while preventing extra stabilizing right scalings. No such classical-mass-action gadget was completed.

Accordingly the manuscript states prominently that the hardness construction uses unbounded molecularity. No bimolecular or fixed-molecularity claim is retained.
