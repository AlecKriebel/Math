# Independent real-projective construction

Written before reading the PR source or another reviewer’s conclusions. This is a proof of existence and ambient openness, not a novelty assertion or a historical attribution.

## Exact claim and success criterion

For every integer d >= 2, the real coefficient space Rat_d(R) of degree-d rational maps of the complex projective line contains a nonempty open subset, in its ordinary real topology and full dimension 2d+1, such that every periodic point (for every positive period, including infinity) belongs to RP^1. Points and multiplicities are understood on the complex projective line.

Rat_d(R) is the open resultant-nonzero locus of pairs of real homogeneous degree-d binary forms (P,Q), modulo simultaneous nonzero scalar multiplication. Its real dimension is 2(d+1)-1 = 2d+1.

## Explicit algebraic seed and all-period exclusion

Choose real A>1, B, distinct real numbers p_1,...,p_(d-1), and positive real c_1,...,c_(d-1). Put

    f(z) = A z + B - sum_j c_j/(z-p_j).

The denominator q(z)=product_j(z-p_j) has degree d-1. Its numerator is

    P(z) = (Az+B)q(z) - sum_j c_j product_(k != j)(z-p_k).

At each p_j the numerator equals -c_j product_(k != j)(p_j-p_k), which is nonzero. Its leading coefficient is A and its degree is d. Thus P and q are coprime and f has exact degree d. In homogeneous coordinates the denominator is Y product_j(X-p_jY); the numerator at [1:0] is A != 0, so there is no hidden common zero at infinity.

For z=x+iy with y != 0, direct calculation gives

    Im f(z) = y [ A + sum_j c_j / ((x-p_j)^2+y^2) ].

The bracket is strictly greater than A>1. Hence f preserves each open half-plane and |Im f(z)| > A |Im z|. A nonreal orbit never reaches a pole or infinity (those preimages are real), and induction gives |Im f^n(z)| > A^n |Im z|. It follows that f^n(z) != z for every n>=1. This single inequality excludes every nonreal periodic point uniformly in the period; finite-period numerical checks are not the proof.

Infinity is a fixed point. In local coordinate w=1/z its multiplier is 1/A in (0,1). A finite pole maps to infinity and cannot be periodic, since infinity is fixed. At a finite real periodic point, every orbit value is finite and avoids the poles, and

    f'(x) = A + sum_j c_j/(x-p_j)^2 > A.

Thus the multiplier of a finite period-n point exceeds A^n>1. Infinity has multiplier A^(-n) for f^n. All fixed points of every iterate are therefore simple as fixed-point solutions. Since a degree-d^n projective rational map has d^n+1 fixed points with multiplicity, the iterate has precisely d^n finite real fixed points and infinity. The exclusion argument itself does not depend on this counting statement.

## Why this is open in full Rat_d(R)

The fixed-infinity displayed family alone has dimension 2d, so it is insufficient by itself. The following normalization supplies an open full-dimensional neighborhood.

Fix one seed f. In the coefficient topology, let F be a nearby real degree-d map. Near infinity write H_F(w)=Q_F(1,w)/P_F(1,w); this is well-defined near w=0 because P_f(1,0)=A != 0. At the seed, H_f(0)=0 and the derivative of H_f(w)-w at zero is 1/A-1 != 0. The real implicit function theorem supplies a unique nearby real root r(F) of H_F(w)-w, continuously (indeed analytically) depending on F. This is a distinguished real attracting fixed point of F. Its multiplier remains in (0,1) after shrinking the neighborhood.

The real projective transformation T_r(z)=z/(1-rz), equivalently [X:Y] -> [X:Y-rX], carries that point [1:r] to infinity and tends to the identity as r -> 0. Conjugate to g=T_r F T_r^(-1). Then g fixes infinity, its multiplier at infinity is in (0,1), and g is close to f in projective coefficient topology. Because this multiplier is nonzero, the numerator degree is d and the affine denominator degree is exactly d-1. (In reciprocal coordinate, the denominator has a simple zero at zero.)

The d-1 finite simple real poles of f continue to d-1 finite simple real poles of g: apply the real implicit function theorem at each simple root, and retain the denominator’s nonzero leading coefficient. These roots exhaust its degree. The normalized partial-fraction expression for g is therefore

    g(z) = A_g z + B_g + sum_j R_j(g)/(z-p_j(g)).

All quantities are real and continuous. The affine slope is A_g=1/(multiplier at infinity)>1. The residue R_j=P_g(p_j)/q_g'(p_j) remains negative because its seed value is -c_j<0. Thus g has exactly the above seed form with c_j(g)>0. The all-period imaginary-part proof applies to g. Real projective conjugacy preserves RP^1 and its complement, so it applies to F as well.

This proves that an entire neighborhood of the seed in Rat_d(R), rather than just the fixed-infinity or polynomial locus, has the claimed property. The construction works already for d=2 with a single pole, and for all higher d without a change in mechanism.

## Boundary and falsifiability checks

* A=1 destroys the strict slope margin and the attracting fixed-point normalization used above; the proof claims only A>1.
* A negative c_j (a positive partial-fraction residue), c_j=0, coincident poles, or a zero local multiplier can invalidate this neighborhood argument. These are excluded by strict inequalities and simplicity.
* Complex perturbations are outside Rat_d(R); the claim concerns real coefficients and real topology.
* The full ambient topology is a coefficient/projective topology on resultant-nonzero pairs, not the topology of polynomials or of rational maps constrained to fix infinity.
* The all-period argument is the growth inequality. Checking finitely many iterates cannot establish the theorem.
* Real Möbius conjugation can interchange the half-planes, but it preserves the nonreal complement; the exclusion proof is made in the normalized coordinate.
* Iteration retains degree d^n since rational maps are morphisms of CP^1 with multiplicative topological degree. A finite pole of an iterate may be a preimage of infinity; it is never a finite periodic point.

Strongest independently proved result: the full stated existence/open-set conclusion, with an explicit family and a full ambient normalization argument. Remaining historical gap at this stage: determine whether the exact PR assertion cites, reproduces, or incorrectly strengthens an existing result; no source has yet been read.
