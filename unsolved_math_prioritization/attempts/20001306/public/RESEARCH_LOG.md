# Research log: five substantive approaches

3 October 2026. Full target: for every fixed n >= 3, prove that the origin-symmetric convex K with IK not a polar zonoid form a residual set. Completion percentages below are subjective estimates toward this full target, not correctness probabilities.

## Source checkpoint, 17:42–17:47 UTC

Recovered AIM Problem 10, inspected the older report and primary papers, corrected the missing dimension/topology, and checked for same-target repository work. No duplicate attempt was found within the inspected sources. The 2026 Ryabogin–Zvavitch paper concerns a different problem. Estimate toward the full target: 5%.

## Attempt 1: topology and quantitative separation

Mechanism: use central-section monotonicity and homogeneity to bound the reciprocal Radon transform under Hausdorff perturbations. Derived the explicit estimate (2), closedness and the exact density reduction; checked the affine quotient rather than assuming arbitrary pullbacks preserve genericity.

Outcome: rigorous quantitative openness and boundary clarification. Closedness and the qualitative reduction are already in Schneider's work and the older report. Exact gap: no reason E_n has empty interior. Estimate: 7%.

## Attempt 2: finite rational certificates

Mechanism: approximate a Hahn–Banach signed-measure witness by finitely supported rational functionals. Add a small rational multiple of the coordinate absolute-value sum to obtain strict global positivity of the cosine polynomial while preserving a negative evaluation. Piecewise linearity turns positivity into a finite exact polyhedral test.

Outcome: Proposition 1 and the neighborhood bound (5). Exact gap: there is no bound or construction producing a certificate near every exceptional input. A decision framework is not a density proof. Estimate: 9%.

## Attempt 3: cube/sign-vector obstruction

Mechanism: use the permutation-symmetric convex inequality (6), together with the exact central diagonal cube-section formula. Compute the certificate using integer and rational arithmetic, and independently verify the three-dimensional piecewise linear polynomial on all 27 arrangement vertices in the cube.

Outcome: W_3=-1/3; W_4=0; strict negative values for dimensions 5 through 64. These instantiate Schneider's obstruction. Exact gap: the witness family is concentrated near cubes and does not perturb general bodies; the exact zero in dimension four provides no conclusion there. No finite computation is promoted to an all-dimensional theorem. Estimate: 10%.

## Attempt 4: harmonic/Fourier perturbation

Mechanism: derive the normalization-sensitive identity (Delta+n-1)C=2R from the equatorial derivative jump; compute the first variation of C^(-1)[(n-1)/R(rho^(n-1))] and the corresponding convexity Hessian. Compare fixed harmonics with increasing frequency.

Outcome: formulas (10)–(12), and a precise explanation of why a fixed small smooth perturbation preserves positive generating density. For general K a variable reciprocal-square multiplier prevents the simple operator cancellation. Exact gap: frequency-uniform nonlinear control and a convexity-preserving negative perturbation near every K. Estimate: 10%.

## Attempt 5: cap surgery and local inverse-transform sign

Mechanism: restrict to a fixed, explicitly separate space Y_4 of bodies of revolution. Truncate the two axial caps. The resulting radial function equals b/t near the pole, so the inverse-cosine generating distribution has the exact negative value -9b^6/(16pi^2 H(1)^3). Derive the density result in Y_4 by convergence of truncations. Test the higher-dimensional extension using the six-dimensional flat-top moment condition.

Outcome: Theorem 2, an open-dense statement in Y_4, derived from Alfonseca's criterion with its own normalized sign verification. The six-dimensional cylinder has h=5/4, k=5/6 and hr(1)-2k^2=-5/36, so the same sufficient cap test cannot cover every revolution body. Exact gap: Y_4 is symmetry constrained and not the original ambient space; there is no reduction of arbitrary bodies to this class and no general-dimensional cap proof. Estimate: 15%.

## Author checkpoint, 17:54 UTC

All five approaches have substantive proof/obstruction artifacts in PROOF.md. The exact standard-library verifier passes. Strongest new-to-this-attempt deduction: restricted four-dimensional genericity and finite rational witness availability. Full genericity remains unresolved, so the bounded attempt is exhausted with partial progress. No first-solution or absolute novelty claim is warranted. A fresh independent reviewer should especially challenge the truncation's smoothness near the pole, distributional inversion and constants, certificate rationalization, six-dimensional integrals, and the non-transfer from the restricted class.
