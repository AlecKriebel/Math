# Focal-distance products of outer elliptic-billiard polygons

**5100007 / AMR-050-0007 / k115. Complete proof candidate, author turn 1. Independent review pending.** No historical-priority or human-peer-review claim.

## 1. Exact statement and scope

Let E be the ellipse x^2/a^2+y^2/b^2=1, a>b>0, with foci f_+=(c,0), f_-=(-c,0), c^2=a^2-b^2. Fix a strictly nested nondegenerate confocal elliptical caustic with semiaxes alpha>beta>0, alpha^2-beta^2=c^2. Suppose its billiard family has **least period N divisible by 4**. For consecutive billiard vertices P_i,P_(i+1), let Q_i be the intersection of their tangents to E. Then

    product_(i=0)^(N-1) |Q_i-f_+|

is constant over the family. The same holds for f_-, with the same value.

The Q_i are precisely the outer polygon vertices P'_i in k115. The theorem includes primitive star polygons, not just simple trajectories. It follows the source's confocal-ellipse setting, not hyperbolic caustics, separatrix limits or collapsed caustics. A repeated traversal of an admissible primitive polygon preserves its already constant product by taking a power; an odd or 2-mod-4 primitive orbit is not relabeled as a 0-mod-4 orbit merely by repetition.

The [arXiv v11 source](https://arxiv.org/abs/2004.12497v11), Table 2 p.5, and [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table 2 p.345, both use k115 for this same outer-vertex product and N=0 modulo4. The nearby k111-k113 labels changed, but k114 and k115 did not. Area and angle conventions play no role in the present identity; all factors here are ordinary positive Euclidean distances.

## 2. Credited canonical parametrization

Use Stachel's canonical parametrization, Theorem 2 and equation (4.10) of [the author preprint](https://arxiv.org/abs/2105.03624v2), corresponding to Theorem 4.3 and equation (4.9) in the [published paper](https://doi.org/10.1007/s40879-021-00524-2). Put k=c/alpha in (0,1), k'=sqrt(1-k^2), and let K,K' be the real and complementary complete elliptic integrals. All Jacobi functions below have **modulus k**, not parameter k.

There is v in (0,K) such that

    P(u)=(-a sn u, b cn u),
    a=alpha dn v/cn v,    b=beta/cn v,
    billiard step: u -> u+delta,    delta=2v.                (1)

For least period N and a counterclockwise orientation,

    v=2K tau/N,    gcd(tau,N)=1,    0<tau<N/2.               (2)

Reversal does not affect the product. Write N=4n, m=N/2=2n. Then tau is odd, and

    m delta=2K tau,    n delta=K tau = K modulo 2K.          (3)

In particular, Q vertices will pair antipodally after m steps. The real billiard period is 4K, while the paired meromorphic functions used below have period 2K. Keeping these two lattices distinct is essential.

## 3. Tangent intersections

Let Q(u) be the intersection of the tangents to E at P(u-v), P(u+v). Direct substitution of the Jacobi addition formulas gives

    Q(u)=(-A_o sn u, B_o cn u),
    A_o=a dn v/cn v,    B_o=b/cn v.                         (4)

Here is a derivation. The tangent at P(w) has equation

    -X sn(w)/a + Y cn(w)/b = 1.

Write s=sn u, z=cn u, d_u=dn u and h=sn v, C=cn v, D=dn v. The addition formulas have common denominator D_0=1-k^2 s^2 h^2. Adding and subtracting the two tangent equations gives

    -X s C D/a + Y z C/b = D_0,
    -X z/a - Y s D/b = 0.

The second equation follows after dividing by h d_u, which is nonzero on the real line. Solving yields X=-a sD/C and Y=bz/C, proving (4). The solution is unique: the two tangent normals have determinant, up to sign,

    2h C d_u/(ab D_0) > 0.

Thus no tangent intersection is at infinity. Its coordinates satisfy

    (Q_x/a)^2+(Q_y/b)^2
      = (1-k^2 h^2 sn^2 u)/cn^2 v > 1,                    (5)

because the numerator minus cn^2 v is h^2 dn^2 u>0. All Q lie outside E and hence differ from its foci. Their two distances to the foci are positive. Formula (4), with positive A_o,B_o, also parametrizes an injective ellipse over one real period, so its primitive N vertices are distinct.

The actual outer sequence is Q(u_0+v+j delta); the fixed offset v is absorbed into the arbitrary starting phase below. Standard real shifts give Q(u+2K)=-Q(u).

## 4. The paired squared distance and its factorization

Define the elliptic function

    H(u)=[(Q_x-c)^2+Q_y^2][(Q_x+c)^2+Q_y^2].              (6)

On real u this equals (|Q(u)-f_+| |Q(u)-f_-|)^2>0. To factor it, put

    t=sn^2 v, q=1-t=cn^2 v, kappa=k^2,
    U=1-2 kappa t+kappa t^2,
    V=1-2t+kappa t^2,
    W=1-kappa t^2.

Then q,W,U are strictly positive. From (1) and (4),

    A_o=alpha(1-kappa t)/q,    B_o=alpha k'/q,
    A_o^2-B_o^2=alpha^2 kappa V/q^2,
    B_o^2+c^2=alpha^2 U/q^2.                               (7)

Writing S=sn^2 u, formula (6) becomes

    H(u)=alpha^4/q^4 [(U+kappa V S)^2
                         -4 kappa(1-kappa t)^2 q^2 S].    (8)

The elementary identity U+V=2q(1-kappa t) turns this into

    H(u)=alpha^4/q^4 (1-kappa S)(U^2-kappa V^2 S).          (9)

The double-angle identities are

    cn(delta)=V/W,    dn(delta)=U/W.

Consequently

    H(u)=C_v dn^2 u [dn^2(delta)-k^2 cn^2(delta) sn^2 u],
    C_v=alpha^4 W^2/q^4>0.                                (10)

This factorization is an identity, not a numerical fit. Equation (9) also gives a proof of it using only coefficient expansion after the canonical and addition identities.

## 5. Exact divisor, including the exceptional four-periodic case

Work on the complex torus

    T=C/(2K Z+2iK' Z),    p=iK'.

The relevant standard periods, poles and quarter shifts are recorded in [NIST DLMF 22.4](https://dlmf.nist.gov/22.4), especially Tables 22.4.1 and 22.4.3. The function sn^2 has exactly one double pole on T, at p. Also

    dn^2 u=1-k^2 sn^2 u,
    sn(z+K+iK')=dn z/[k cn z].                             (11)

It follows that dn^2 has a double pole at p and a double zero at p+K. The zero multiplicity can also be checked from dn'(u)=-k^2 sn u cn u: dn has a simple zero at p+K, since sn there is 1/k up to sign and cn there is nonzero.

First suppose cn(delta) is nonzero. The factor

    J(u)=dn^2(delta)-k^2 cn^2(delta) sn^2 u                 (12)

has one double pole at p. Equation (11) shows its zeros at

    p+K+delta,    p+K-delta.

They are distinct modulo the lattice: otherwise 2delta would be a multiple of 2K, and 0<delta<2K would force delta=K, contrary to cn(delta) nonzero. Neither zero is p, and neither equals p+K. Two distinct zeros exhaust the zero divisor of this degree-two elliptic function and are simple. Thus

    div(H)=2[p+K]+[p+K+delta]+[p+K-delta]-4[p].             (13)

There is one exceptional possibility. On the given real interval cn(delta)=0 if and only if delta=K. By (2), tau=n, and gcd(tau,4n)=1 forces n=1, hence N=4. In this case J(u)=dn^2 K=k'^2 is a positive constant, so

    div(H)=2[p+K]-2[p].                                   (14)

We do not apply the generic four-pole-order formula to N=4. It is precisely the case where the outer locus in (4) is a circle and the degree drops.

## 6. Cyclic norm and return to ordinary distances

On T, the translation by delta has exact order m, because

    delta/(2K)=tau/m,    gcd(tau,m)=1.

Its orbit through p is {p-j delta: 0<=j<m}. Equation (3) says K=n delta on T. Therefore each translated zero family in (13) permutes that same pole orbit:

    p+K-j delta       = p+(n-j)delta,
    p+K+delta-j delta = p+(n+1-j)delta,
    p+K-delta-j delta = p+(n-1-j)delta.

For the cyclic norm

    F(u)=product_(j=0)^(m-1) H(u+j delta),                 (15)

every order-four pole cancels with a double zero and two simple zeros. In the exceptional N=4 case, the order-two poles cancel with the double-zero orbit in (14). Hence div(F)=0 in every case covered by the theorem. The function F is holomorphic on the compact connected torus T and is therefore constant. Since H is positive on the real line, this constant is finite and positive.

Now pair Q(u+j delta) with Q(u+(j+m)delta)=-Q(u+j delta). For the ordinary one-focus product R_+(u),

    R_+(u)
      = product_(j=0)^(m-1) |Q(u+j delta)-f_+| |Q(u+j delta)-f_-|,
    R_+(u)^2=F(u).                                        (16)

Thus R_+(u) is the positive square root of a fixed positive number and is constant. The same paired expression proves R_-(u)=R_+(u). This proves k115 for every primitive period divisible by4 and every allowed turning number. No choice of a complex square-root branch is used.

## 7. Boundary cases, checks and credit

- For a circle, both foci coincide at its center and each outer vertex has fixed radius a/cos(pi tau/N); constancy is immediate. This is a separate k=0 observation, not a limit taken through the divisor proof.
- The proof assumes a nondegenerate elliptical caustic. It does not silently include a hyperbola or a focal segment.
- Source polygon areas are signed; source theta denotes internal polygon angles. Stachel uses an exterior-angle convention elsewhere. Neither angles nor areas enter this proof, and no convention substitution is needed.
- Finite exact checks verify the algebraic factorization, lattice permutations, multiplicities, exceptional N4 behavior, and negative parity controls. Separate high-precision numerical computations check direct tangent intersections and distance products. Numerical agreement is not the proof.
- Stachel's canonical parametrization is a published input. Jacobi analytic facts are standard and credited to DLMF. The pole-cancellation method is classical; see Akopyan-Schwartz-Tabachnikov, [Billiards in ellipses revisited](https://arxiv.org/abs/2001.02934).
- The previous campaign [k114 proof, PR149](https://github.com/AlecKriebel/Math/pull/149), suggested the cyclic-norm organization. Its claim concerns original orbit vertices and N=2 modulo4; it is not k115 and is not used as a black-box theorem here. The new work required the tangent-intersection formula and the paired fourth-degree factorization (9), with a different parity and exceptional case.

A bounded literature check did not locate an exact prior general-k115 proof; that is not evidence of historical novelty. Separate adversarial review is required before any claimed-result PR.
