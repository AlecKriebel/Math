# k906: equal own-focus inverse areas, and the quotient's domain

**5100065 / AMR-050-0065. Complete author-turn-1 candidate; independent review pending.**

## 1. Exact conclusion

Let a noncircular ellipse E have a strictly nested, nondegenerate confocal elliptical caustic. Fix a Poncelet billiard family of **even least period N>=4**. Its outer polygon Q is formed by consecutive tangent intersections to E. Let f'_+, f'_- be the two foci of the centered ellipse traced by Q's vertices. Invert the outer vertices in unit circles about these foci and join successive images by straight segments. Write B_+, B_- for the signed shoelace areas.

Then, throughout the family,

    B_+ = B_-.                                             (1)

Consequently B_+/B_-=1 at every configuration where B_- is nonzero. For the simple winding-one family, neither area vanishes, so the ratio is defined and equal to 1 everywhere. These statements prove the usual simple-family k906 invariant.

For the broader reading allowing primitive stars, the denominator qualification cannot be removed: Section 5 gives an exact fixed 8/3-star family with both areas zero at some phase. Thus an unqualified everywhere-defined ratio is false on that broader domain; the equality (1) is its valid division-free version.

This is arXiv:2004.12497v11, Section 3.9 and Table 10 k906. The centers here are the **outer locus's own foci**, not the original billiard foci (k904), and the inverted vertices are outer vertices, not original vertices (k903). The source uses signed cross-product areas. The published *Fifty New Invariants* companion omits the 900-series table. No different row is substituted for k906.

No hyperbolic or collapsed caustic is included. Parity refers to least period, not an even multiple of a smaller odd orbit. Reversal changes both signed areas by the same sign. A circular outer locus is allowed, with coincident foci.

## 2. Credited canonical parametrization and the outer locus

Let the caustic semiaxes be alpha>beta>0, put k²=1−beta²/alpha² in (0,1), and let K be the real complete elliptic integral. Jacobi functions below use modulus k. Stachel's published Theorem 4.3 and (4.9), [On the motion of billiards in ellipses](https://doi.org/10.1007/s40879-021-00524-2), give the canonical parametrization

    P(u)=(-a sn u, b cn u),
    v=2K tau/N,     delta=2v=4K tau/N,
    a=alpha dn(v)/cn(v),     b=beta/cn(v),               (2)

where gcd(tau,N)=1 and 0<tau<N/2. Opposite orientation may be reversed to arrange this inequality. This includes primitive stars, not just tau=1.

The intersection of the tangents at P(u−v),P(u+v) is

    Q(u)=(-A sn u, B cn u),
    A=a dn(v)/cn(v),     B=b/cn(v).                     (3)

Indeed the tangent at P(z) has equation −X sn(z)/a+Y cn(z)/b=1. Substitution of (3), followed by the Jacobi addition formulas, satisfies both tangent equations. Their determinant is

    2 sn(v)cn(v)dn(u) / {ab[1−k² sn²(u)sn²(v)]},        (4)

which is strictly positive on the real line. Thus every outer vertex is finite and (3) describes its actual locus. Its axes A,B are positive; they need not be ordered the same way as a,b. All Q(u) lie on this nondegenerate ellipse. Its own foci lie strictly inside it, so no real Q(u) equals an inversion center. Unit vertex inversion is everywhere finite in the stated domain.

The outer polygon has vertices Q(w+j delta), j=0,...,N−1, up to a choice of starting phase. Formula (3) and the elementary symmetry argument below do not assume that its foci equal those of E. This is exactly the distinction needed in k906.

The outer-locus computation is also present in the author's earlier [k115 work](https://github.com/AlecKriebel/Math/pull/200) and [k904,a work](https://github.com/AlecKriebel/Math/pull/211). It is reproduced and credited here, not counted as a second discovery.

## 3. The half-turn proof

Because N is even and gcd(tau,N)=1, tau is odd. The standard real half-period identities sn(u+2K)=−sn(u) and cn(u+2K)=−cn(u) imply

    Q_(j+N/2)=Q(w+j delta+2K tau)=−Q_j.                 (5)

Alternatively the same relation holds for the original billiard vertices, and central reflection takes each tangent intersection to the opposite tangent intersection. The two foci of a centered ellipse are f'_- = −f'_+, even when both are zero.

For unit inversion I_f(x)=f+(x−f)/|x−f|²,

    I_(-f)(-x)=−I_f(x).                                (6)

Combining (5) and (6), the minus-focus inverse polygon is the central reflection of the plus-focus inverse polygon with its cyclic indexing shifted by N/2. Central reflection in the plane has determinant +1. Its signed shoelace area is unchanged, as is area under cyclic relabeling. This proves (1) without dividing by an area or assuming any inverse polygon is simple.

The mechanism is elementary and already credited as “symmetry” for neighboring rows k903,b and k904,b of the source table. The present application to the own-focus outer-locus object is not a claim to invent that mechanism or certify historical priority.

## 4. The quotient is everywhere defined for winding one

Here is a separate proof, because symmetry alone cannot show nonvanishing.

Put t=sn²(v), q=1−t=cn²(v), d²=1−k²t and

    V=1−2t+k²t².

From (2)–(3),

    A=alpha d²/q,       B=alpha sqrt(1−k²)/q,
    A²−B²=alpha² k² V/q².                              (7)

The double-angle formula gives V=cn(2v)[1−k²t²]. If delta=2v<=K, this is nonnegative. The outer foci are consequently on the x-axis or coincide. For c_o²=A²−B²,

    a²−c_o²
      = alpha² [q d²−k²V]/q²
      = alpha²(1−k²)(q+k²t²)/q² > 0.                  (8)

Thus both own foci lie strictly inside the original billiard ellipse E.

For real u, the eccentric angle of Q(u)=(-A sn u,B cn u) increases strictly with u and increases by pi over a 2K interval. Since 0<delta<2K, consecutive Q_i,Q_(i+1) have a positive determinant about the origin. Their joining line is the shared tangent to E at P(w+(2i+1)v). It does not pass through O. Since f'_+ and f'_- lie inside E, each is strictly on the same side of this tangent as O. Hence

    det(Q_i−f, Q_(i+1)−f)>0

for each f=f'_+,f'_- and every edge. Translating an inverse polygon by −f does not change its area, and its edge determinant becomes the displayed positive determinant divided by the positive number |Q_i−f|²|Q_(i+1)−f|². Every term in twice its signed area is therefore positive. Both B_+ and B_- are positive in the chosen orientation.

For winding one and even N>=4, delta=4K/N<=K, so this proof applies throughout every such family. More generally it applies to every primitive turning number tau/N<=1/4. At N=4, delta=K, A=B and the outer locus is a circle; coincident-focus inversion causes no exceptional denominator problem.

## 5. Exact primitive-star zero-area witness

We now prove that a broader all-stars everywhere-defined quotient would overstate the conclusion.

Fix caustic semiaxes

    alpha=1, beta=25/144,
    k²=20111/20736,

and take N=8,tau=3. Let h=K/4; then v=3h and delta=6h=3K/2. The positive quarter-period data are

    sn(h)=4 sqrt(1326)/221,
    cn(h)=5 sqrt(1105)/221,
    dn(h)=5 sqrt(30)/36,
    sn(3h)=6 sqrt(1326)/221,
    cn(3h)=sqrt(1105)/221.                              (9)

These can be verified exactly from sn²(h)=96/221 and the Jacobi double-angle formulas: the doubled values are sn(2h)=12/13, cn(2h)=5/13 and dn(2h)=5/12. A further doubling gives cn(4h)=0 with positive sn, so h is the real first-quarter K/4. Equivalently these are the standard positive real half-period values and the K−h shift formulas.

Equations (2)–(3) give

    a²=221/96,        b²=27625/20736,
    A=221/96,         B=1105/144,
    f'_+=(0,221 sqrt(91)/288),  f'_- = −f'_+.           (10)

These are a fixed genuine nondegenerate confocal ellipse pair: a²−b²=alpha²−beta²=k² and a>alpha,b>beta>0. Equation (2), with gcd(8,3)=1, gives least period eight.

Let S(w) be the signed area after inversion of Q(w+j delta) about f'_+. It is continuous in w because the center lies strictly inside the vertex-locus ellipse and hence no vertex meets it. Direct exact shoelace evaluation gives

    S(0) = 1473536/30525625 > 0,
    S(h) = −51985629184 sqrt(30)/12455533443925 < 0.     (11)

For independent reproduction, the (sn,cn) pairs in orbit order at w=0 are

    (0,1), (12/13,−5/13), (−1,0), (12/13,5/13),
    (0,−1), (−12/13,5/13), (1,0), (−12/13,−5/13).

At w=h, write x=sn(h), y=cn(h), z=sn(3h), r=cn(3h). The pairs are

    (x,y), (x,−y), (−z,r), (z,r),
    (−x,−y), (−x,y), (z,−r), (−z,−r).

Map each pair (s,c) to Q=(-A s,B c), then to (Q−f'_+)/|Q−f'_+|². Sum consecutive determinants and divide by two. Translation by f'_+ is irrelevant to the result. The exact symbolic checker reproduces (9)–(11), rather than inferring signs from floating-point sampling.

By the intermediate value theorem S(w*)=0 for some w* in (0,h). Equation (1) gives B_-(w*)=0 as well. All original billiard, outer-intersection and inversion objects remain finite there. The ratio is 0/0 and is undefined at that configuration. This is a domain obstruction within one fixed primitive elliptical-caustic star family, not a degenerating caustic or an even repetition of an odd orbit.

## 6. Status, sources and validation limits

The universal division-free equality and simple-family ratio are proved. The primitive-star construction proves the need for the quotient qualification when the dataset statement is read broadly. No claim of two individually constant inverse areas is made; only their equality and ratio on its domain are at issue.

Published inputs are Stachel's canonical parametrization and the standard Jacobi real/addition formulas ([DLMF 22.4](https://dlmf.nist.gov/22.4), [22.8](https://dlmf.nist.gov/22.8)). Symmetry and the preceding campaign's outer-locus calculation are credited. Bounded literature searches did not locate a separate exact k906 proof, but do not certify novelty.

This complete candidate was reached in one substantive author turn. Exact algebra, independently constructed numerical tangent-intersection diagnostics, and a separate adversarial review are required before promotion. Numerical checks are not the proof of the all-N statement, nonvanishing, or the exact star zero.
