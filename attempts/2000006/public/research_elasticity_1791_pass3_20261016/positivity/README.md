# Positivity and constitutive structure: shared pass 3

Frozen benchmark: E-6322, arbitrary positive a,b,c,d, arbitrary permitted smooth full diffeomorphic trace, complete finite-energy W^{1,6} class, whole-domain essential Jacobian lower bound.

## Results

- `COMPONENTWISE_COMPARISONS.md`: a new exact minimizer-specific inequality. Competitors differing from a minimizer in one fixed target direction have admissible straight interpolation, and their energy gap controls the L^6 gradient, L^3 cofactor, L^2 determinant, and L^2 reciprocal-determinant differences. The proof uses finite midpoint competitors only. It also identifies the exact cofactor-row transport constraint that prevents ordinary cutoff localization.
- `COERCIVITY_AND_ELLIPTICITY.md`: the original minimizer problem is exactly equivalent to minimizing a nonnegative relative-minor excess around any fixed positive-determinant matrix. Strong quasiconvex lower coercivity is proved directly. Exact rank-one stiffness calculations show shear stiffness tending to zero and the ellipticity ratio growing as t^{-12} at F=tI. The actual stress spectrum controls strain anisotropy; an inner-stationary deformation that is conformal almost everywhere has constant positive Jacobian, without extra regularity.
- `REFERENCE_TRUNCATION.md`: an unconditional boundary-preserving maximal-function truncation around the allowed smooth extension gives a genuine uniformly positive-determinant competitor and a bad-set energy estimate. Its admissibility ceiling is at small truncation levels, so no high-level tail or higher-integrability estimate follows.
- `verify_constitutive.py` and `CONSTITUTIVE_CHECKS.json`: reproducible algebraic checks supplementing the written proofs.

## Boundary of the result

All comparisons stated for a minimizer are in the original full class. No ordinary Piola Euler equation, injective minimizer, derivative trace, or regularity premise is silently added. The conformal consequence is expressly restricted and does not replace arbitrary boundary data. No unconditional higher-integrability or essential-lower-bound theorem was obtained, and no compliant counterexample was constructed.

The pass-1 pressure reduction and pass-2 Dini criterion remain valid conditional tools. This pass does not repackage them as an unconditional bootstrap. The variations lane separately treats the energy threshold for recovering ordinary Piola equilibrium; the literature lane treats the exact inverse comparison class.

Status: partial results; E-6322 unresolved.
