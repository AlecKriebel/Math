# Odd-period products of the two outer focal-inverse areas

**5100063 / AMR-050-0063 / k904,a. Complete author-turn-1 candidate; independent review pending.** No historical-priority or human-peer-review claim.

## 1. Exact target and source distinction

Let E be a billiard ellipse with semiaxes a>b>0, original foci f_+=(c,0), f_-=(-c,0), c^2=a^2-b^2, and a strictly nested nondegenerate confocal elliptical caustic with semiaxes alpha>beta>0. Fix a Poncelet family of **odd least period N>=3**, with any coprime turning number, including primitive stars. Let Q_i be the outer polygon vertices obtained by intersecting consecutive tangents to E at the billiard vertices.

Invert the Q_i in unit circles centered at f_+ or f_-, and join successive inverted vertices by straight segments. Let B_+,B_- be the resulting **signed shoelace areas**. Then

    B_+ B_- is constant throughout the family.             (1)

This is k904,a in [Reznik-Garcia-Koiller arXiv2004.12497v11](https://arxiv.org/abs/2004.12497v11), Table10 printedp12, with inversion defined in Section3.9. The published *Fifty New Invariants* companion has no900-series table. The original foci must not be replaced by the foci of the outer-vertex locus: the latter choice belongs to k906. Inverting the original orbit vertices is the different k903,a target.

The source defines signed areas. This proof includes stars in the confocal-ellipse setting, not hyperbolic or collapsed caustics, and does not create a primitive parity by repeating a shorter orbit. Inversion of vertices followed by straight joining is distinct from inverting entire edges to circular arcs.

## 2. Canonical coordinates and outer vertices

Let k=c/alpha in (0,1), k'=beta/alpha, and K,K' be the real and complementary complete elliptic integrals. Every Jacobi function below has modulus k. Stachel's [published Theorem4.3 and equation4.9](https://doi.org/10.1007/s40879-021-00524-2) give

    P(w)=(-a sn w,b cn w),
    a=alpha dn(v)/cn(v),    b=beta/cn(v),
    delta=2v=4K tau/N,
    gcd(tau,N)=1,    0<tau<N/2,    0<v<K.                 (2)

Reversing the orbit does not change the area product, so this orientation is enough.

The intersection of tangents at P(u-v),P(u+v) is

    Q(u)=(-A_o sn u,B_o cn u),
    A_o=a dn(v)/cn(v),    B_o=b/cn(v).                    (3)

To verify this, the tangent at P(z) is -X sn(z)/a+Y cn(z)/b=1. Substitution of (3) and the Jacobi addition formulas satisfies both equations. Their determinant magnitude is

    2 sn(v)cn(v)dn(u) / [ab(1-k^2sn^2(u)sn^2(v))]>0

on the real line. Thus no intersection at infinity is hidden. The real outer locus is an ellipse with the positive axes in (3), without requiring A_o>B_o. It generally is not confocal with E.

Moreover A_o>a and B_o>b, since dn^2(v)-cn^2(v)=k'^2sn^2(v)>0. Its points therefore lie outside E, and cannot equal either original focus. All real inversions used in (1) are defined. Up to an irrelevant fixed starting phase, the Q_i are Q(w+j delta).

Set

    h=sn v, C=cn v, d=dn v, t=h^2, q=C^2=1-t,
    U=1-2k^2t+k^2t^2,
    V=1-2t+k^2t^2,
    W=1-k^2t^2.                                         (4)

Thus A_o=alpha d^2/q, B_o=alpha k'/q, U=dn(delta)W and V=cn(delta)W.

## 3. Exact focal-distance and inverse-edge identities

For f=f_+, direct expansion using (3) gives

    D_f(u):=(Q_x(u)-c)^2+Q_y(u)^2
           =alpha^2/q^2 (1+k sn u)(U+kV sn u).            (5)

This is a positive squared distance on the real line. Its factorization follows from

    A_o^2-B_o^2=alpha^2 k^2 V/q^2,
    B_o^2+c^2=alpha^2 U/q^2,
    U+V=2q d^2.

Translate the inverse polygon by -f, which does not affect signed area, and use

    I(u)=(Q(u)-f)/D_f(u).                                (6)

All squared norms in the complex continuation are bilinear sums of squares; no conjugation of the complex parameter is used.

Let E_+(u)=det(I(u-v),I(u+v))/2. Define

    L0=(U^2-k^2V^2t)/d,
    L1=(V^2-U^2t)/C,
    D(u)=1-k^2t sn^2u,
    C0=B_o h d q^4/(alpha^3 C)>0.                        (7)

Then

    E_+(u)=C0 dn(u)D(u)
                 /[(d+kC sn u)^2(L0+kL1 sn u)].         (8)

The following identities give a direct derivation rather than a fit to samples:

    (1+k sn(u-v))(1+k sn(u+v))
      =(d+kC sn u)^2/D(u),                               (9)

    (U+kV sn(u-v))(U+kV sn(u+v))
      =(d+kC sn u)(L0+kL1 sn u)/D(u),                    (10)

    det(Q(u-v)-f,Q(u+v)-f)/2
      =alpha B_o h d dn(u)(d+kC sn u)/(C D(u)).           (11)

Equations (9)-(10) follow by expanding products and using the Jacobi sum and product formulas for sn(u±v). For (10), the constant and quadratic coefficients are precisely the definitions of L0,L1; the remaining coefficient is the polynomial identity

    d^2(V^2-U^2t)+q(U^2-k^2V^2t)=2UV q d^2.

Equation (11) follows by expanding the determinant and using the same addition formulas. Dividing (11) by the product of the two squared distances (5) proves (8), including its q^4 normalization.

## 4. Triple-angle factors and real positivity

Put

    Z=W^2-4k^2t^2 q d^2
     =W^2[1-k^2t sn^2(delta)]>0.                         (12)

The Jacobi addition formulas give

    L0=Z dn(3v),    L1=Z cn(3v).                         (13)

For an explicit check, write D3=UW-2k^2tqV and C3=VW-2t d^2 U. Then

    U^2-k^2V^2t=d^2 D3,
    V^2-U^2t=q C3,
    dn(3v)=d D3/Z,    cn(3v)=C C3/Z.

In particular L0>0 and

    L0^2-k^2L1^2=k'^2Z^2>0.                             (14)

Also d^2-k^2C^2=k'^2>0. Thus for real u every factor d+kC sn u and L0+kL1 sn u is strictly positive, as are dn(u), D(u), and C0. Consequently

    E_+(u)>0 for every real u.                           (15)

This will ensure the cyclic area function is not identically zero.

Since N is odd, L1 is nonzero. In fact 0<3v<3K, and cn(3v)=0 would require3v=K (or the excluded endpoint3K), hence N=6tau, impossible for oddN.

## 5. Full pole list, including the N3 critical case

Set p=iK' and r0=3K+p. The meromorphic function in (8) has real period4K and imaginary anti-period2iK', hence period4iK'. We use standard Jacobi pole, zero and quarter-shift facts from [DLMF22.4](https://dlmf.nist.gov/22.4) and [22.8](https://dlmf.nist.gov/22.8), including

    sn(K+iK'+z)=dn z/(k cn z).                           (16)

On the sn torus with periods4K,2iK', the first denominator factor d+kC sn u has exactly two zeros,

    r0+v and r0-v.                                       (17)

They are distinct, finite, and simple for0<v<K. Equation (16) proves the values, and the two displayed zeros exhaust the degree-two sn fiber. They cannot be critical values±1/k because d/C>1. Squaring this factor permits double poles in (8).

By (13), the second factor L0+kL1 sn u has its zeros at

    r0+3v and r0-3v.                                     (18)

If3v is not2K these are distinct simple zeros. The possible coincidence modulo4K,2iK' would require6v=4K, and therefore3v=2K. Primitivity in (2) makes that precisely N=3,tau=1.

In that N3 case, L0=Z,L1=-Z; the linear factor is Z(1-k sn u). It has a double zero at K+p, where dn has a simple zero. The numerator dn(u) in (8) cancels one order, so (18) still produces **at most a simple pole**, not a double one. Its location is different from either point in (17). The two sets (17)-(18) cannot otherwise meet: such equality would force2v or4v to be a multiple of4K, impossible for0<v<K.

At common poles of sn,cn,dn, the numerator dn(u)D(u) has pole order3 and the denominator in (8) has pole order3, since k,C,L1 are nonzero. These singularities are removable. At every other dn zero the numerator only vanishes. We have therefore exhausted the pole list:

- at most double poles at r0±v and their2iK' translates
- at most simple poles at r0±3v and their2iK' translates, with the preceding N3 cancellation
- no other poles

## 6. Cyclic cancellation of the double terms

Define the inverse-area sum

    F(u)=sum_(j=0)^(N-1) E_+(u+j delta).                  (19)

Then B_+(w)=F(w+v), because the inverse edge centered atw+v+jdelta joins the outer vertices atw+jdelta andw+(j+1)delta.

Jacobi parity and shifts give

    sn(2r0-u)=sn u,    dn(2r0-u)=-dn u,
    E_+(2r0-u)=-E_+(u).                                  (20)

Hence the quadratic Laurent coefficients at the reflected points r0+v and r0-v are opposite. These two points differ bydelta. When (19) is formed, each possible pole receives one translated quadratic coefficient of each sign. They cancel exactly. The points from (18) already have pole order at most one and differ from r0+v bydelta or-2delta, so they add no further pole classes. If N3 identifies the two points in (18), it is the already-treated single simple pole, not two unexamined higher-order poles.

Let L=4K/N. The periodsdelta and4K, with gcd(tau,N)=1, give periodL for F. It has anti-period2iK'. On

    X=C/(L Z+4iK' Z),    R=r0+v,                          (21)

its only permitted poles are therefore simple, at R and R+2iK'.

Both actually occur. If neither occurred, F would be holomorphic on the compact torus and constant; its anti-period would force it to be zero. That contradicts the positive real sum (15). The anti-period pairs the poles, so each has order exactly one.

## 7. Half-period zeros and the opposite focus

Cyclic reindexing preserves the odd reflection in (20), so F is odd about r0. Since2v=delta is a period, it is also odd about R:

    F(2R-u)=-F(u).                                       (22)

At R+L/2 this forces F=0, because reflection sends that point to its real-period translate. The same holds at R+L/2+2iK'. These two distinct points are not poles; they exhaust the zero divisor and are simple because F has exactly two simple poles. It follows that

    F(u)F(u+L/2) is constant on X.                        (23)

This is divisor cancellation followed by compactness, not a numerical constancy inference.

Finally Q(u+2K)=-Q(u). Unit inversion about f_- is the central reflection of inversion about f_+ applied to the opposite point. Central reflection preserves signed area, so

    B_-(w)=B_+(w+2K)=F(w+v+2K).                          (24)

For oddN, 2K=N L/2 equalsL/2 moduloL. Equations (23)-(24) prove (1). Both areas are positive for the chosen orientation by (15), so the real constant is positive. Reversal changes both signs and leaves the product unchanged.

## 8. Scope, verification and credit

The result uses unit focal inversion and straight-edge signed area. No area is divided out. The positivity argument concerns this strict elliptical-caustic scope, not arbitrary inverse polygons. Primitive star turning numbers satisfy the same canonical identities. The N3 critical triple-angle case is explicitly included. A circular billiard gives the corresponding central-inversion result by rigid rotation and is separate from the k>0 proof.

Stachel's canonical parametrization and the Jacobi identities are published inputs. Complex methods for billiard invariants are classical; see [Akopyan-Schwartz-Tabachnikov](https://arxiv.org/abs/2001.02934). The outer-locus calculation and cyclic organization reuse this author's preceding [k115 work](https://github.com/AlecKriebel/Math/pull/200) and [k804,a work](https://github.com/AlecKriebel/Math/pull/207); every required identity is proved here.

The distinct [k903,a proof](https://github.com/AlecKriebel/Math/pull/206) was inspected. Its original-ellipse isotropic-contact argument was not assumed for these outer vertices, because the inversion centers here are generally not foci of their locus ellipse. A ratio transfer through the separate k806,a target is also not assumed. Shared framework and source advice are not independent verification.

Exact symbolic, lattice, pole-coefficient and exception controls accompany the proof. Separate numerical diagnostics compute actual outer tangent intersections, actual Euclidean inversions and signed areas. They support but do not replace the universal meromorphic argument. Bounded literature checks did not certify historical novelty. An uninvolved independent reviewer must audit the full candidate before a claimed-result PR.
