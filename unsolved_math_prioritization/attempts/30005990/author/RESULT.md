# Boundary frequency gap: candidate sharp blow-up theorem

Problem 30005990 / OWR-14298587-002, queue rank 958.

**Disposition: UNSOLVED, 5/5 substantive mathematical approaches.** The packet proves a candidate sharp admissible-blow-up theorem and additional realization reductions, pending independent mathematical review. Actual attainment by a bounded-domain global spectral optimizer remains unproved. No publication, peer-review, or priority claim is made.

## Result

For the primary paper's class B_gamma of nonzero, nonnegative, segregated, homogeneous Dirichlet-energy minimizers on a half-space with zero flat-boundary trace, in every dimension d >= 3:

- There are no homogeneities strictly between 2 and 5/2.
- Homogeneity 5/2 occurs.
- Every 5/2-homogeneous member is, after a tangential rotation, component permutation, and multiplication by one positive constant, U(x,t) = t Y(x_1,x_2), where Y is the three-sector 3/2-homogeneous planar junction and t > 0 is the normal coordinate.

The proof divides by t and radially lifts the normal coordinate to three variables. This turns a boundary homogeneity gamma into an interior homogeneity gamma-1 in dimension d+2. The published interior gap and equality classification then apply to the exact lifted variational-inequality class. The Hardy and removable-axis steps are proved explicitly in PROOF.md.

Consequently every boundary free-interface frequency of a spectral sum-of-first-Dirichlet-eigenvalues optimizer, under the boundary hypotheses of the cited blow-up theorem, is 2 or at least 5/2. The result uses the existing spectral blow-up theorem; it does not reprove that theorem on an arbitrary C^1 domain.

## Notation correction

The OWR report prints {2} union [2+delta_d,infinity), then gives delta_d = 5/2 as its conjecture. These two uses are inconsistent with its geometric endpoint model. This packet denotes the first higher admissible frequency by beta_d and the additive gap by g_d. The proved candidate values are beta_d=5/2 and g_d=1/2. Thus the literal additive equation delta_d=5/2 is not the intended sharp-gap statement. This discrepancy was confirmed on the rendered primary PDF, printed p.2122.

## Sharpness and limits

Sharpness here means existence in the primary source's B_gamma class, the class used to determine admissible boundary frequencies, with N>=3. The explicit minimizer tY supplies this. In d=3 its interior triple-junction spine is the normal half-line. In d>3 it is that model times R^(d-3). Its interfaces meet the fixed flat boundary orthogonally, and its interior spine points have frequency 3/2.

This packet does not show that tY is the tangent of an optimizer of the unconstrained global sum-of-eigenvalues problem on some bounded smooth domain. The original attainment wording is conservatively treated as requiring that separate assertion, so the queue problem remains unsolved. It also does not prove uniqueness of blow-ups or smoothness of the actual spectral free interface near frequency-5/2 points. Cone classification alone does not imply either conclusion.

## Five substantive approaches

1. Weak radial dimension lifting: sharp exclusion, equality classification, and attainment in the half-space cone class. Full proof: PROOF.md.
2. Cartesian-product realization: a restricted exact tensorization theorem and a long-cylinder counterexample to unrestricted tensorization.
3. Angular spectral realization: exact spectral shift to a higher-dimensional sphere, and the sharp hemispherical three-cell min-max problem. The sum functional remains a separate obstacle.
4. Thin-cylinder variational limit: convergence of the original spectral sum after subtraction of the transverse ground-state energy, including compactness of minimizers.
5. Explicit spectral stationary construction: separated Bessel eigenfunctions on half-ball Y cells have the desired 5/2 asymptotics and pairwise shape-stationarity, without a global-minimum certificate.

Approaches 2-5 are proved and scoped in REALIZATION_APPROACHES.md. Source retrieval, checks, audits, and packaging are not counted as approaches.

## Sources and novelty

The interior gap is credited to Soave-Terracini and the earlier regularity theory, as restated in Ognibene-Velichkov, arXiv:2412.00781v5, Theorem 2.4. The equality classification is their Proposition 3.5, with its stated antecedent in Soave-Terracini. The characterization S=M is credited to Wang-Zhang, as explicitly stated in that paper's Section 2. Boundary blow-up compactness is Ognibene-Velichkov, arXiv:2404.05698v1, Proposition 6.13.

The argument authored here is the weak dimensional-lift reduction and its use for the boundary sharp gap and equality case. A bounded literature search did not locate this boundary deduction; this is not a novelty certificate. The 2026 survey inspected still states only an unspecified positive boundary gap.

## Verification

Run `python3 -I -B check_math.py` and `python3 -I -B verify_packet.py` from this directory, or use absolute script paths from any directory. The exact finite checks exercise differential identities, their wrong-dimension negative controls, angular/eigenvalue arithmetic, and rotation-invariant projection algebra. They do not replace the Sobolev, distributional, or imported analytic theorems. See CHECKS.md and SOURCE_AUDIT.md.
