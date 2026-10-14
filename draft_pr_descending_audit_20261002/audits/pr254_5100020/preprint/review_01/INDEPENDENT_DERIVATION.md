# Independent reconstruction before reading PR254 audit conclusions

Recorded 2026-10-13 UTC. Scope: the five-page frozen note with TeX SHA256 e2f115f1eee7489a9d888b9d1b639ac851e5442402fd453556612c1f39e3e8fd.

The manuscript, original primary-source definitions, Stachel's canonical theorem, DLMF, and the nine checkset programs were read first. No earlier PR254 mathematical acceptance or priority verdict was consulted while reaching the mathematical conclusion below. Finite numerical checks are diagnostics. The universal proof is reconstructed here.

## Domain and canonical arithmetic

Set alpha > beta > 0, k' = beta/alpha, k^2 = 1-k'^2. A noncircular strict confocal family has 0 < k < 1. Put v = 2K tau/N, delta = 2v, with N odd >= 3, gcd(tau,N)=1, and 0 < tau < N/2. Then 0 < v < K, so s=sn(v), c=cn(v), d=dn(v) are positive and nonzero. Stachel Theorem 4.3/(4.9) gives a=alpha d/c, b=beta/c, P(w)=(-a sn w,b cn w), and every phase is an actual reflected billiard orbit with this caustic. The source's modulus m is the manuscript's k, rather than the numerical library parameter k^2.

Confocality and strict nesting are checked directly:

    a^2-b^2 = alpha^2(d^2-k'^2)/c^2 = alpha^2 k^2 = alpha^2-beta^2;
    b^2-beta^2 = beta^2 s^2/c^2 > 0;
    (b^2-beta^2)/b^2 = s^2 < 1.

The real P parameter is injective modulo 4K. Since delta/(4K)=tau/N, gcd(tau,N)=1 makes the least period exactly N. Stars with admitted coprime tau are therefore covered, and no convexity assertion is needed. At fixed outer ellipse and caustic the rotation number is fixed; the theorem does not assert that all tau share one fixed caustic.

Let ell=2K/N. Modulo 2K the increments delta/ell=2tau generate all N real classes, because gcd(2tau,N)=1. A function with real periods 2K and delta has ell as a period (Bezout). A pole vertex at p-jdelta and an opposite chord midpoint at p-v-jdelta both reduce to p modulo ell because v=tau ell. At N=3 the opposite edge is precisely the edge between the two finite neighbors of the pole vertex; for larger odd N it is another edge. Exactly one opposite midpoint occurs at a vertex-pole phase: solving tau(2j+1)=0 mod N gives j=(N-1)/2. This is an actual overlap of singularity classes, not evidence that the opposite endpoint singularity is removable.

## Real intersections, the actual construction, and equation (6)

The Jacobi addition formulas give

    det(P(u-v),P(u+v)) = 2absc dn(u)/(1-k^2 s^2 sn^2(u)).

For real u the numerator is positive and the denominator is at least 1-k^2s^2 > 0. Thus every pair of consecutive radial normals is linearly independent, including in stars. The antipedal is built from the original vertices' lines P_i dot X=P_i dot P_i, not from outer ellipse tangent normals or from a pedal of the outer polygon.

For independent real or complex P,Q, solving those two lines gives

    R(P,Q) = ((H(P) Q_y-H(Q) P_y), (P_x H(Q)-Q_x H(P)))/det(P,Q).

Equivalently, with J(x,y)=(-y,x),

    R_i = P_i + t_i J P_i,
    R_(i-1) = P_i - u_i J P_i,
    t_i=(H(P_(i+1))-P_i dot P_(i+1))/det(P_i,P_(i+1)),
    u_i=(H(P_(i-1))-P_(i-1) dot P_i)/det(P_(i-1),P_i).

Since det(P,JP)=H(P) even for isotropic complex P, the local area contribution is H(P_i)(t_i+u_i)/2. Grouping by the original edge (P,Q) produces exactly

    F(P,Q)=[H(P)H(Q)-(H(P)+H(Q))(P dot Q)/2]/det(P,Q).

This establishes the original antipedal signed shoelace identity U=sum F. It holds for arbitrary polygons with nonzero consecutive determinants, with no convexity or positive-norm hypothesis. The meromorphic continuation uses the bilinear dot product; inserting conjugation would invalidate it.

## Complete chord divisor and finite endpoint types

Write p=iK', r=K+p and D=1-k^2s^2sn^2u. The squared sine is elliptic on the 2K by 2p cell and has one double pole at p. A nonzero meromorphic function has equal total zero and pole orders. D therefore has two zeros counting order. The p-shift identities locate them at p+v and p-v. Their derivatives are +/-2cd/s, nonzero. They are distinct since 0<v<K. dn there is -/+ i c/s, nonzero. Thus B=det(P(u-v),P(u+v)) has simple poles at p+/-v, each with exactly one pole endpoint. Their residue is -i absc/d, nonzero.

At p, dn has a simple pole and D a double pole, giving B a simple zero with coefficient 2i ab c/s. The endpoints are finite and opposite because P(p-z)=-P(p+z).

At r, dn has a simple zero, sn(r)=1/k, cn(r)=-i k'/k, and D(r)=c^2. The zero coefficient of B is 2i ab s k'/c, nonzero. The endpoints are finite and coincident because P(2r-z)=P(z).

These lists exhaust B's support: every possible zero is a dn zero or the result of the dn/D orders at their common pole; every possible pole is a D zero. No additional finite determinant zero or endpoint pole was discarded.

The numerator factorization

    N(P,Q)=((H(P)+H(Q))H(P-Q)-(H(P)-H(Q))^2)/4

shows N=O(z^2) at coincident finite endpoints, regardless of H(P)=0, while B has a simple zero. This removes that F singularity. At opposite endpoints the numerator equals 2H(P)^2; regularity alone gives at most a simple pole, and in this strict domain it is genuinely nonzero. Indeed

    H(P(p+v)) = (a^2-b^2 d^2)/(k^2 s^2)
                 = alpha^2 d^2/(c^2 s^2) > 0.

Consequently the opposite-midpoint F residue is

    2 H(P(p+v))^2/(2i ab c/s)
      = H(P(p+v))^2 s/(i ab c) != 0.

This independently falsifies any attempt to classify both finite endpoint types as removable. The manuscript correctly retains the opposite pole.

## Incident cancellation at vertices

Each pole vertex has simple coordinate poles; H(P) has order at most two, P dot Q order at most one for a regular neighbor Q, and hence the F numerator has order at most three. The chord determinant has a simple pole with a nonzero coefficient, so each incident F has pole order at most two. No incident edge has two pole endpoints since 0<delta<2K.

For G(z)=F(P(p+z),P(p+delta+z)), the backward term is exactly -G(-z): use P(p-z)=-P(p+z), the same identity at delta-z, antisymmetry F(Q,P)=-F(P,Q), and F(-P,-Q)=F(P,Q). Thus their sum is G(z)-G(-z). A Laurent series bounded by order two loses its z^-2 coefficient and retains at most z^-1. The argument includes N=3; its third edge has the already-classified opposite-endpoint simple pole and cannot raise the order. Possible overlaps for larger N likewise only add simple poles.

The real period 2K is inherited from simultaneous endpoint negation, the real period delta from cyclic reindexing, and the 2p shift reflects y while preserving bilinear norms and dots and negating the determinant. Thus U is ell-periodic and 2p-antiperiodic. The full previous pole list leaves only possible simple poles at p and 3p on X=C/(ell Z+4p Z).

## The trace divisor and uniqueness are universal, not sampled

For S(w)=sum_j dn(w+jdelta), the same real arithmetic makes S ell-periodic; dn is even, so reindexing makes S even; its imaginary antiperiod is 2p. At p only j=0 contributes a pole modulo 2K. Its residue is -i from dn(p+z)=-i cn(z)/sn(z). Therefore it cannot cancel. The second pole at 3p has residue +i, and these are the entire simple pole divisor on X.

The map w -> -w+ell+2p fixes p+ell/2 and negates S. Hence that nonpole is a zero. The corresponding point 3p+ell/2 is another distinct zero. S is nonzero (and positive on the real axis); equality of total orders on a compact torus forces exactly these two zeros, both simple. The half-real-period translate exchanges poles and zeros, so S(w)S(w+ell/2) is pole-free and thus constant. No division by S or a derived area at a zero is made in this reasoning.

Any meromorphic antiperiodic function with only possible simple poles at p,3p has opposite residues there. Subtracting the scalar multiple of S matching the first residue removes both poles. The difference is constant on the compact torus; the antiperiod forces that constant to vanish. This also handles the identically zero function. Consequently U=c_* S, and real phase values make c_* real. This is the familiar simple-pole cyclic-trace mechanism, not a novel general method.

## Pedal construction and the required shift

The chord at midpoint u has caustic-normal equation n dot X=1 with n=(-sn u/alpha,cn u/beta). Both endpoints satisfy it by the addition formulas. Moreover

    n dot n = dn^2(u)/beta^2,
    Q(u)=n/(n dot n)=(-alpha k'^2 sn(u)/dn^2(u), beta cn(u)/dn^2(u)).

Thus Q is the actual original-side foot, and A_O(w)=T(w+v) with T the signed area of the Q polygon.

At common Jacobi poles Q is holomorphic and vanishes, since its numerators have order one and denominator order two. At dn zeros r and translates its coordinate poles have order at most two. The same reflection P(2r-z)=P(z) and dn^2(2r-z)=dn^2(z) gives Q(2r-z)=Q(z). Equivalently the local chart is

    Q(r+z)=(alpha dn(z)cn(z)/(k sn^2(z)),
            i beta cn(z)/(k k' sn^2(z))),

an even Laurent series. Its regular neighbors satisfy Q(r-delta+z)=Q(r+delta-z). Their difference is O(z), so the two incident determinants together have pole order at most one. The Q shifts give real period 2K and imaginary character diag(1,-1); the T area is ell-periodic and 2p-antiperiodic. Its only possible poles on X are r,r+2p, precisely those of S(u+K). The previous uniqueness proof gives T=c_p S(u+K), with real c_p.

Therefore

    A_O(w) A_O^*(w)=c_p c_* S(w+v+K)S(w),
    (v+K)/ell=tau+N/2=tau+(N-1)/2+1/2.

This is the constant complementary-divisor product. Even when one area is identically zero the identity remains valid; there is no ratio by an area anywhere in the universal argument. Reversal changes the sign of both shoelace areas. An r-fold repeated list repeats every derived edge r times, scaling each area by r and their product by r^2; it does not create a new primitive least period.

## Circular, even, dimensional and limiting controls

For a circle, theta=2pi tau/N in (0,pi). An actual chord's origin foot and the consecutive radial-line intersection lie on the midpoint ray at respective radii R cos(theta/2) and R/cos(theta/2). Their ordered stars both have step theta, so areas are (N/2) times radius squared times sin(theta), giving N^2 R^4 sin^2(theta)/4. Intersections are finite since theta<pi. A degenerate torus at k=0 is unnecessary.

The N4 diamond and rectangle in the manuscript are genuine strict common-caustic trajectories, not arbitrary inscribed quadrilaterals: alpha^2=25/8, beta^2=9/8, a^2=5, b^2=3 have common gap 15/8. The diamond sides satisfy alpha^2/a^2+beta^2/b^2=1; its axis-vertex reflection follows symmetry. The rectangle is on the outer ellipse, its sides are caustic tangents, and alpha/a^2=beta/b^2 ensures its Cartesian reflection. Both have four distinct vertices. Actual foot projections and named-line intersections yield 225/4 and 289/4. This refutes unrestricted even-period invariance, but does not claim every even family is noninvariant.

Every length coordinate scales by h under a homothety. Both areas scale by h^2 and the product by h^4. F has degree four numerator divided by a degree two determinant, Q has length units, and the circle expression has units R^4. No dimensional mismatch occurs. k tending to 0 or 1, v tending to 0 or K, and collapsed or hyperbolic caustics are not smuggled into the strict domain. Circles are explicitly treated. Numerical extreme interior moduli do not establish excluded limiting cases.

## Independent mathematical conclusion

All twelve numbered equations, the signed-construction identification, the pole support/orders, the odd-period arithmetic, the shifted pedal trace, and the boundary controls are correct as written. I found no mathematical gap or counterexample in the admitted domain. This conclusion was recorded before reading the prior PR254 audit verdicts; source credit, bounded priority, archive provenance and submission metadata were then audited separately.
