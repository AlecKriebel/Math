# Review02 independent mathematical reconstruction

This reconstructs the implication assessed in this review. The exact claim and attack plan were frozen in INDEPENDENT_SCOPE_FREEZE.json before earlier family reports or verdicts were read. I read the current manuscript and reconstructed the argument before reading those reports. No earlier PASS, Root acceptance, or review01 conclusion is a premise. The final reasoning shares the candidate's valid divisor mechanism; it is an independent audit, not a claim of a new proof method.

## Physical domain and the original construction

Write c^2=a^2-b^2=alpha^2-beta^2, with a>b>0 and 0<beta<b. Therefore k=c/alpha is strictly between zero and one. Set k'=beta/alpha. The equation cn(v,k)=beta/b has exactly one solution 0<v<K because real cn decreases from one to zero on that interval. Confocality then gives

    a=alpha dn(v)/cn(v), b=beta/cn(v).

This is a surjective normalization of every strict pair in the claim, rather than an extra restriction to specially generated ellipses. Stachel's published Theorem4.3/(4.9), printed1614, confirms that P(w)=(-a sn(w),b cn(w)) is the billiard parameter and its step is delta=2v. One can independently check the geometric identification: for s=sn(u), r=cn(u), C=cn(v), d=dn(v), the line through P(u-v), P(u+v) is

    -d s X/a + r Y/b = C,

or equivalently -s X/alpha+r Y/beta=1. Its normal is on the dual caustic because s^2+r^2=1, so it is precisely a caustic tangent. The addition-formula residuals at both chord endpoints vanish identically; this is tested exactly by the newly authored checker. The boundary normal reflection law is also tested by directly propagating physical trajectories, without generating their vertices from the asserted outer formula.

The real parameter P is injective modulo4K. Least closure gives delta=4K*tau/N and gcd(tau,N)=1. Reversal chooses 0<tau<N/2, hence v=2K*tau/N in(0,K). Thus every admitted primitive star is included. An odd total traversal of a repeated orbit has odd least period and is covered by the separate repetition argument.

The two original boundary tangents at P(u-v),P(u+v) have coefficient determinant

    2 sn(v) cn(v) dn(u) / [ab(1-k^2 sn(v)^2 sn(u)^2)] > 0

on the entire real line. Their intersection is

    Q(u)=(-A sn(u),B cn(u)),
    A=alpha d^2/C^2, B=alpha k'/C^2.

Both A>a and B>b: d^2-C^2=k'^2 sn(v)^2>0 and C<1. Consequently Q_x^2/a^2+Q_y^2/b^2>1, so Q never equals either original focus, which lies inside the billiard ellipse. This argument does not order A and B. In fact A^2-B^2=alpha^2 k^2 V/q^2 below, which is negative for v>K/2; primitive triangles have this reversed outer-axis case.

The original source defines this tangent polygon, unit vertex inversion about the original foci, and signed cross-product polygon area. Inverting whole edges, choosing the outer ellipse's own foci, or replacing signed shoelace by filled-star area changes the question. Those objects are not identified by the proof.

## Reconstructing the physical edge and its sign

Put h=sn(v), t=h^2, q=C^2=1-t and

    U=1-2k^2 t+k^2 t^2,
    V=1-2t+k^2 t^2,
    W=1-k^2 t^2.

For f+=(alpha k,0), direct expansion of (Q_x-alpha k)^2+Q_y^2 gives

    D_f(u)=alpha^2(1+k sn(u))(U+k V sn(u))/q^2.

For complex parameters the squares are bilinear; no conjugate is inserted. On the real line this is the physical Euclidean distance squared. Translating the entire inverse polygon by -f is legitimate because the additional terms in its cyclic shoelace telescope. Such a translation need not preserve an individual edge determinant, so the checker compares the full center-inclusive area with the full translated sum.

Let I(u)=(Q(u)-f)/D_f(u). Expanding the actual determinant of the two outer points and the two shifted distance products yields

    e(u)=det(I(u-v),I(u+v))/2
        =C0 dn(u)(1-k^2 t sn(u)^2)
          /[(d+k C sn(u))^2 (L0+k L1 sn(u))],

    L0=(U^2-k^2 V^2 t)/d,
    L1=(V^2-U^2 t)/C,
    C0=B h d q^4/(alpha^3 C)>0.

In particular q already means C^2; the fourth power is required. The unsimplified determinant is alpha B h d dn(u)(d+k C sn(u))/(C(1-k^2 t sn(u)^2)). Its division by the two distances supplies this normalization. This formula has inverse-length-squared units, agreeing with an area after unit inversion. The product has inverse-length-fourth units.

Triple addition gives

    Z=W^2(1-k^2 t sn(2v)^2)>0,
    L0=Z dn(3v), L1=Z cn(3v),
    L0^2-k^2 L1^2=k'^2 Z^2.

Since dn(3v)>0 on the real axis, L0>0. Also d^2-k^2 C^2=k'^2>0. Therefore both real denominator factors in e are positive, as are dn(u), C0 and 1-k^2 t sn(u)^2. Every real e is positive; no nonzero area or residue has been assumed or divided out. L1 cannot vanish for odd N: in0<3v<3K it would require3v=K, or N=6tau. The limiting possibility3v=3K is excluded byv<K.

## Complete denominator fibers and the exceptional triangle

Set p=iK', r0=3K+p. The sn torus has periods4K,2p, degree two, two simple poles, and finite critical values +/-1,+/-1/k. The edge itself has periods4K,4p and anti-period2p. Confusing these two tori would lose poles; I use the smaller torus only for fiber enumeration.

The quarter-shift identity is sn(r0+z)=-dn(z)/(k cn(z)). Thus the zeros of d+k C sn(u) are r0+v and r0-v. Their value has magnitude d/(kC)>1/k, so these are distinct noncritical simple roots. Squaring the factor permits order two.

The other factor has the complete fiber r0+3v,r0-3v because L0/L1=dn(3v)/cn(3v). Away from cn(3v)=0, the squared target value minus1/k^2 is

    [dn(3v)^2-cn(3v)^2]/[k^2 cn(3v)^2]
      = k'^2 sn(3v)^2/[k^2 cn(3v)^2].

Hence a critical value occurs only at sn(3v)=0. In0<3v<3K this is exactly3v=2K. The two root labels coincide precisely in the same case, since6v=4K. Substitution v=2Ktau/N gives N=3tau, and coprimality leaves N=3,tau=1. There is no unexamined genericity condition or other odd exceptional fiber.

Here L0=Z,L1=-Z and the factor is Z(1-k sn(u)). At u=K+p, sn=1/k and dn=0. From sn'=cn dn and dn'=-k^2 sn cn, dn has a simple zero because cn^2=-(1-k^2)/k^2 is nonzero. Also sn''=(1-k^2)/k is nonzero there, so 1-k sn has order exactly two. The remaining numerator factor is q>0 and the first denominator is d+C>0. Thus the critical edge pole is exactly simple, not double and not silently absent.

The first and second fibers are disjoint before summation. Coincidence would require2v or4v to be a multiple of4K, impossible for0<v<K. At any common Jacobi pole, the numerator has order three and denominator order three with nonzero leading coefficient because k,C,L1 are nonzero. Therefore these points are removable, not additional poles. For example at p the finite limit is i C0 t/(q L1); the new controls test this limit at two-sided displacements. The same order reasoning covers both Jacobi poles and their translates. Other numerator zeros can only reduce the pole bounds, so their exact classification is not an unproved premise of the main argument.

## Exact cancellation on the quotient, without a sampled-residue premise

Parity and the shifts imply e(2r0-u)=-e(u). Thus the quadratic Laurent coefficients at r0+v and r0-v are negatives of one another. These two poles differ by delta=2v. In

    F(u)=sum_(j=0)^(N-1) e(u+j delta),

the shift has exact order N modulo4K, by gcd(tau,N)=1. At every possible translated double pole, exactly one contribution from each first-fiber root occurs. Their quadratic coefficients cancel. All second-fiber contributions are at most simple, including the single critical triangular root, whose two labels must not be double-counted.

The second-fiber locations are R+delta and R-2delta, with R=r0+v. Thus they introduce no new cyclic pole coset. Reindexing makes delta a period and Bezout gives L=4K/N as a period. On X=C/(L Z+4p Z), the only possible poles of F are simple, at R and R+2p.

If either were absent, anti-periodicity would make both absent. F would then be holomorphic on compact X, hence constant; its anti-period would force zero. But every real summand is positive. Thus both poles occur, exactly simply. This proves the required nondegeneracy for every k and admitted turn. Numerical residues are not used to exclude an exceptional family.

Reindexing preserves odd reflection about r0; since delta is a period it also gives F(2R-u)=-F(u). The reflection has four fixed classes on X. Two are the poles R,R+2p. The remaining two, R+L/2 and R+L/2+2p, are regular distinct points and must be zeros. Equality of total zero and pole orders for a nonzero elliptic function makes them exactly simple and exhausts the divisor. Translation by L/2 exchanges zeros and poles. Consequently F(u)F(u+L/2) is holomorphic on compact X and constant. This is a classical elliptic-function consequence of the target-specific calculation, not a new general method.

The outer polygon can have vertices Q(w+j delta), with a harmless constant shift from the original billiard phase. Its positive-focus area is F(w+v). As Q(u+2K)=-Q(u), central reflection identifies the negative-focus inverse polygon with the positive-focus inverse polygon phased by2K; determinant+1 preserves signed area. For odd N,2K=NL/2 is L/2 modulo L. This proves the actual product is the constant above and positive in the chosen orientation.

Reversal negates both areas. An r-fold traversal repeats each shoelace r times, multiplying the product by r^2. Scaling the geometry by s with unit inversion multiplies the product by s^-4; changing both inversion radii to rho gives rho^8. At k=0 use a separate rotation calculation: outer radius a/cos(pi tau/N), inverse signed area N sin(2pi tau/N)/(2R_outer^2). The collapsed/hyperbolic/grazing limits are excluded; positivity bounds degenerate there, and interior numerical approaches establish no extension. A same-caustic even diagnostic varies with phase, agreeing with the proof's essential odd-half-period identification.

## Independent controls and mathematical limits

independent_checks.py was newly authored here, imports no reviewed checker, and writes only INDEPENDENT_RESULTS.json beside itself. It checks11 exact polynomial identities plus the nonzero critical second derivative, and22 physical configurations with4 phases each at135 decimal digits. The real orbits start from one canonical point and a geometrically constructed caustic tangent, then propagate through ordinary Euclidean reflection and the second ray/ellipse hit. Areas come from raw original-tangent intersections and center-inclusive Euclidean inversions. All small coprime turns atN=3,5,7,9,11 are represented, together with k=10^-15, k=1-10^-18, N41 endpoint/near-quarter-period turns and an even negative control. Reversal, repetition, scale, opposite-focus shift, kernel, complex reflection/anti-period and common-pole limit are checked. The final JSON records every case and actual errors.

These finite noninterval controls can falsify implementation errors; they are not universal certification. The universal conclusion rests on the deduction above, standard Jacobi facts and compact-torus complex analysis. No proof assistant or conventional independent human referee has verified it. No mathematical blocker was found in the precise frozen claim.
