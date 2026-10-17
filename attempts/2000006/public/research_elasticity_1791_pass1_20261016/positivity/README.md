# Positivity and boundary regularity lane

Pass 1 of the frozen E-6322 benchmark, 2026-10-16.

**Outcome: no proof or counterexample to E-6322.** The useful result is a precise, sharp audit of what finite inverse-square Jacobian energy can establish once extra regularity has actually been proved.

- `REGULARITY_AND_BOUNDARY.md` proves the scalar conditional positivity thresholds, supplies explicit finite-energy obstructions below them, and identifies the unproved PDE step.
- `PRESSURE_REDUCTION.md` uses justified stationarity and a global negative-norm estimate to prove the stronger conditional result for C^{1,beta} minimizers, for every beta>0, including the entire boundary.
- `check_formulas.py` independently checks the elementary determinant formulas and integrability thresholds. Its output is in `formula_checks.json`.

Main conclusions:

1. If a finite-energy deformation has `det Dy` in C^{1,1} on the entire closure, it has a positive Jacobian lower bound. The sufficient deformation regularity is C^{2,1}, **not** C^{1,1}.
2. Interior zeros are already excluded by `det Dy` in C^{1,alpha} for alpha >= 1/2. At the boundary, the energy-only threshold is stricter. The inverse-square exponent is exactly critical for quadratic tangential vanishing with linear normal vanishing.
3. For every alpha < 1, there are admissible C^{2,alpha} deformations with the identity trace, positive Jacobian everywhere inside, finite energy for every positive coefficient quadruple, and essential Jacobian infimum zero at one boundary point. A logarithmic example belongs to every C^{2,alpha}, alpha < 1, simultaneously.
4. These deformations are **not minimizers**: the identity is the unique minimizer for their boundary data. They disprove energy-only shortcuts, not E-6322.
5. For minimizers, stationarity changes the picture: if Dy is globally bounded, the inverse Jacobian has every finite moment. Therefore any global C^{1,beta} minimizer, beta>0, satisfies the desired entire-domain lower bound. Proving that extra regularity for arbitrary target minimizers remains unresolved.
6. Ordinary additive-variation arguments, scalar pressure maximum principles, and boundary Schauder bootstraps each need an additional justified step. The pressure argument uses no ordinary additive equilibrium equation and no prior determinant lower bound.

The exact first-variation identities and the admissibility of their variations are owned by the separate variations lane and are not duplicated as a claimed independent result here.
