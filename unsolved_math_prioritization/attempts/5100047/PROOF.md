# The outer/original focal-inverse area ratio, in every period

**5100047 / AMR-050-0047 / arXiv k806,a. Complete author-turn-1 candidate, pending independent review.** This is a credited companion of the reviewed focal-inverse pole calculations in PRs207 and211, with their required identities reproduced and the all-period exceptional cases checked below. No novelty or historical-priority claim.

## 1. Exact statement, edition and domain

Let E have semiaxes a>b>0, original foci f_±=(±c,0), c²=a²−b², and a strictly nested nondegenerate confocal elliptical caustic with semiaxes α>β>0. Fix a billiard Poncelet family of least period N≥3, allowing every primitive star turning number. Let P_i be the ordered orbit vertices and Q_i the intersections of the tangents to E at P_i and P_(i+1). For either original focus f, invert each P_i and each Q_i in the unit circle centered at f, and join the inverted vertices in their original order by straight edges. Write A_f and B_f for these two signed shoelace areas, respectively.

**Theorem.** There is a positive constant κ, depending on the fixed family, such that

    B_f(w)=κ A_f(w)                                      (1.1)

for every phase w and either focus. Both areas are strictly positive in the positive orientation, and both reverse sign on orientation reversal. In particular B_f/A_f is a well-defined constant throughout the family. The same conclusion holds for repeated traversals, since both areas are multiplied by the repetition number.

This is the displayed ratio A'_j^†/A_j^† in arXiv2004.12497v11, Table9 printedp11, with the original-focus definition in §3.9, pp9–10. The shorter published *Fifty New Invariants* companion omits this row. The later self-intersected paper's k806 denotes a different ratio A/A_j^† and cannot be substituted.

The numerator is not inversion about a focus of the outer-vertex locus. Areas are signed traversal areas of straight-edge polygons, not unsigned lobe areas or areas bounded by inverted circular arcs. Hyperbolic or degenerate caustics are outside the original confocal-ellipse setting used here. There is no zero-area exception in this strict setting. The adjacent arXiv k806,b row prints the reciprocal of the correct N4 value for its displayed expression: §8 proves κ=1/2, not2. This does not alter k806,a's constancy assertion.

## 2. Canonical phases and the actual outer vertices

Use the Jacobi modulus k=c/α∈(0,1), complementary modulus k'=β/α, and complete integrals K,K'. Functions sn,cn,dn below have modulus k. Stachel's published Theorem4.3 and (4.9) give

    P(w)=(-a sn w,b cn w),
    a=α dn(v)/cn(v),        b=β/cn(v),
    δ=2v=4K τ/N,           gcd(τ,N)=1,
    0<τ<N/2,               0<v<K.                        (2.1)

Every allowed orientation is this one or its reverse. The original vertices are P(w+jδ), j=0,…,N−1. The tangent intersections are

    Q(u)=(-A_o sn u,B_o cn u),
    A_o=a dn(v)/cn(v),      B_o=b/cn(v),                  (2.2)

so the actual outer vertices are Q(w+v+jδ). Indeed the tangent at P(z) is

    -X sn(z)/a+Y cn(z)/b=1,

and the addition formulas verify (2.2) on both tangents z=u±v. Their determinant has magnitude

    2 sn(v)cn(v)dn(u) / [ab(1−k²sn²(v)sn²(u))]>0         (2.3)

for real u. Thus no undefined real tangent intersection is hidden. The two outer locus axes in (2.2) need not appear in decreasing order; no assumption about its own focal line is used. Both A_o>a and B_o>b, so Q(u) lies outside E. Neither P nor Q can equal an original focus.

Set

    h=sn v, C=cn v, d=dn v, t=h², q=C²=1−t,
    U=1−2k²t+k²t², V=1−2t+k²t², W=1−k²t².             (2.4)

Then cn δ=V/W, dn δ=U/W, and

    U+V=2q d², U−V=2t k'²,
    U²−k²V²=k'²W²>0.                                   (2.5)

All of α,β,h,C,d,q,W,U are positive. Complex continuation below uses bilinear squared norms, not conjugation of the parameter.

## 3. Original inverse edge function

It suffices initially to take f=f_+=(c,0). The positive distance from P(z) to f is a+c sn z. Translating every inverted point by −f does not change area, so define

    I(z)=(P(z)−f)/(a+c sn z)².

For an edge centered at u, put s=sn u and D(u)=1−k²t s². A direct calculation gives

    E(u):=det(I(u−v),I(u+v))/2
         =C_P dn(u) D(u)/[(1+ks)(U+kVs)²],
    C_P=b h d q²/α³>0.                                 (3.1)

For auditability the two identities yielding it are

    (a+c sn(u−v))(a+c sn(u+v))
       =α²(1+ks)(U+kVs)/(q D(u)),                       (3.2)

    det(P(u−v)−f,P(u+v)−f)
       =2α b h d dn(u)(1+ks)/D(u).                      (3.3)

They follow by expanding with

    sn(u−v)+sn(u+v)=2s C d/D(u),
    sn(u−v)sn(u+v)=(s²−t)/D(u).

Dividing half of (3.3) by the square of (3.2) gives (3.1). These are the original-inverse identities credited to PR207; that PR's final parity-specific product conclusion is not assumed.

For real u every factor in (3.1) is positive: dn(u)>0, D(u)>0, 1+ks≥1−k>0, and U>|kV|. Hence

    E(u)>0.                                             (3.4)

## 4. Outer inverse edge function

Translate the inversion of Q by the same original focus:

    J(z)=(Q(z)−f)/D_f(z),
    D_f(z)=(Q_x(z)−c)²+Q_y(z)².

The exact outer distance factorization is

    D_f(z)=α²/q² (1+k sn z)(U+kV sn z).                  (4.1)

It follows by expansion from

    A_o=α d²/q, B_o=α k'/q,
    A_o²−B_o²=α²k²V/q², B_o²+c²=α²U/q².

Put

    L0=(U²−k²V²t)/d,        L1=(V²−U²t)/C,
    C_Q=B_o h d q⁴/(α³ C)>0.

Then the outer inverse edge centered at u is

    G(u):=det(J(u−v),J(u+v))/2
         =C_Q dn(u)D(u)/[(d+kC sn u)²(L0+kL1 sn u)].     (4.2)

The direct component identities are

    (1+k sn(u−v))(1+k sn(u+v))
       =(d+kC sn u)²/D(u),                              (4.3)

    (U+kV sn(u−v))(U+kV sn(u+v))
       =(d+kC sn u)(L0+kL1 sn u)/D(u),                   (4.4)

    det(Q(u−v)−f,Q(u+v)−f)/2
       =α B_o h d dn(u)(d+kC sn u)/(C D(u)).             (4.5)

Expanding the same sn sum/product proves (4.3)–(4.4); the remaining coefficient in (4.4) is

    d²(V²−U²t)+q(U²−k²V²t)=2UV q d².

Equations (4.1), (4.3)–(4.5) prove (4.2). These identities are credited to PR211; its odd-period product conclusion is not assumed.

Define

    Z=W²−4k²t²q d²=W²[1−k²t sn²δ]>0.

The triple-angle addition identities give

    L0=Z dn(3v),       L1=Z cn(3v),
    L0²−k²L1²=k'²Z²>0.                                 (4.6)

For example, with D3=UW−2k²tqV and C3=VW−2t d²U, expand

    U²−k²V²t=d²D3,       V²−U²t=qC3,
    dn(3v)=d D3/Z,       cn(3v)=C C3/Z.

In particular L0>0 and L0>|kL1|. Also d²−k²C²=k'²>0. Thus every real factor in (4.2) is positive, even when L1=0, and

    G(u)>0.                                             (4.7)

## 5. Cyclic sums and the two-pole comparison principle

Set

    F(u)=Σ_(j=0)^(N−1) E(u+jδ),
    H(u)=Σ_(j=0)^(N−1) G(u+jδ),
    ℓ=4K/N,       p=iK',       r=3K+p.                  (5.1)

Both sums have real periods 4K and δ, hence ℓ by coprimality. They have imaginary anti-period 2iK' and period4iK', because sn is 2iK'-periodic and dn changes sign under that shift. They are meromorphic on the compact torus

    X=C/(ℓ Z+4iK' Z).                                   (5.2)

We will prove:

    F has at most simple poles at r,r+2iK';
    H has at most simple poles at r+v,r+v+2iK'.           (5.3)

All pole locations in (5.3) are understood modulo the lattice in (5.2). They need not be distinct before cyclic reduction, and the following analysis accounts for those identifications. The two listed points within each pair are distinct on X.

By (3.4), F is positive on the real axis and is not identically zero. If its possible poles were removable, it would be constant on X; its imaginary anti-period would then force zero. Consequently both poles in its pair actually occur and are simple, with opposite nonzero residues. The same reasoning applies to H using (4.7).

Therefore F(u) and H(u+v) have the same two possible simple poles and the same anti-period. Choose κ to match their residues at r. Anti-periodicity matches the other residue. Their difference is holomorphic on X, hence constant, and anti-periodicity makes that constant zero. Thus

    H(u+v)=κ F(u).                                      (5.4)

Both sides are positive on the real line, so κ is real and strictly positive. It remains to prove the complete pole bounds, including the exceptional periods.

## 6. Original-area poles, including N4

We use the standard Jacobi identity

    sn(K+iK'+z)=dn z/(k cn z),                           (6.1)

and the usual periods, simple poles and critical values. In the sn torus with periods4K,2iK', each noncritical finite value has two simple preimages. The critical value −1/k occurs at r and has order-two contact there, while dn has a simple zero.

First assume V≠0. The factor 1+k sn u has its only zero class at r, of order2. The numerator dn has order1 there, while U+kV sn r=U−V>0. Thus E has at most a simple pole at r and its 2iK' translate on the dn torus.

The zeros of U+kV sn u occur at r±δ by (6.1). They are finite, distinct and simple: their value is −U/(kV), and U>|V| by (2.5), excluding the critical values. The two points are distinct for 0<δ<2K; at δ=K they instead become common Jacobi poles and V=0, the separately handled case. Squaring this factor permits order-two poles at r±δ and their imaginary translates.

At a common pole of sn,cn,dn, the numerator dn D has order at most3 and the denominator in (3.1) has order3, so E is removable there. The displayed list is exhaustive.

Reflection about r gives

    sn(2r−u)=sn u,       dn(2r−u)=−dn u,
    E(2r−u)=−E(u).                                      (6.2)

The quadratic Laurent coefficients at r+δ and r−δ are opposite. These locations differ by2δ and lie in one cyclic orbit. Every quadratic contribution in F is paired with its opposite under cyclic reindexing, with equal multiplicity, so it cancels. The remaining poles have order at most1 and are all in the class of r moduloδ. This proves the first part of (5.3) when V≠0.

If V=0, then δ=K and primitivity gives N=4, τ=1. Instead of applying the preceding generic degree estimate, pair the opposite edges explicitly:

    E(u)+E(u+2K)
       =2C_P/U² [q/dn u+t dn u].                        (6.3)

This follows from (3.1), `1−k²sn²u=dn²u` and `D=q+t dn²u`. Now

    F(u)=[E(u)+E(u+2K)]+[E(u+K)+E(u+3K)].

Every pole in (6.3) is simple, at a dn pole or zero. These all differ from r by integer multiples of K or2iK'. Since ℓ=K, they give exactly the allowed pair in (5.3). The N4 case is therefore covered without an unproved generic limit argument.

## 7. Outer-area poles, including N3 and N6

The first denominator factor d+kC sn u in (4.2) has two finite simple zeros at r±v. They are noncritical because d/C>1. Its square allows order-two poles there.

### Generic triple-angle factor and N3

Assume L1≠0. By (4.6) and (6.1), the zeros of L0+kL1 sn u are r±3v. For 0<3v<3K these are distinct, finite and simple, except when 3v=2K. That exception is exactly N=3, τ=1 by primitivity. In that case the factor is Z(1−k sn u), with an order-two zero at K+iK'; dn has a simple zero there. Thus the resulting pole of G is still at most simple. The other critical possibility 3v=0 is excluded.

The r±3v zeros cannot coincide with r±v in the full sn torus: the possible real differences are2v or4v, and 0<v<K. Thus this does not create an unexamined higher-order pole. At a common Jacobi pole, numerator and denominator in (4.2) have order3, so G is removable when L1≠0.

The same reflection as (6.2) gives G(2r−u)=−G(u). Hence the order-two coefficients at r+v and r−v are opposite. They differ byδ, so their contributions to H cancel by cyclic reindexing. The simple poles at r±3v differ from r+v byδ or−2δ. This proves the second pole bound in (5.3), including the N3 critical zero.

### The exceptional vanishing coefficient L1=0

By (4.6), L1=0 means cn(3v)=0. In 0<v<K the only possibility is3v=K, so primitivity gives N=6, τ=1. Here the second factor is the positive constant L0. At a common Jacobi pole, (4.2) has numerator order3 and denominator order2, hence at most a simple pole. No order-two term is created there. The first-factor double poles at r±v still cancel exactly as above.

The new common-pole locations are p and p+2K, with their2iK' translates. With v=K/3 and ℓ=2K/3,

    (r+v)−p=10K/3=5ℓ,       2K=3ℓ.

Thus these are already the two allowed classes r+v and r+v+2iK' on X. This completes the outer pole list at N6. All periods and all exceptional coefficients have now been accounted for.

## 8. Alignment, both foci and the corrected four-period value

The original orbit edges are centered at w+v+jδ, whereas the actual outer vertices are Q(w+v+jδ). Their edges are centered at w+2v+jδ. Therefore

    A_+(w)=F(w+v),          B_+(w)=H(w+2v).

Substitute u=w+v into (5.4) to obtain (1.1). Forgetting this half-step would compare the wrong divisors; no parity shortcut is used.

Central reflection satisfies P(z+2K)=−P(z) and Q(z+2K)=−Q(z). Inverting about f_- is the central reflection of inversion about f_+ after that phase shift. Central reflection preserves signed area. Applying the already established constant ratio to the shifted phase proves the same κ for f_-. Positivity, reversal and repetition behave as stated in §1.

For N4, choose the axial orbit P=(0,b),(-a,0),(0,-b),(a,0), whose tangent intersections are (-a,b),(-a,-b),(a,-b),(a,b). Inversion about (c,0), followed by translation by −f, gives the original vertices

    (-c/a²,b/a²), (-1/(a+c),0),
    (-c/a²,-b/a²), (1/(a−c),0),

whose area is2/(ab). The outer inverse vertices simplify using

    (a±c)²+b²=2a(a±c)

to

    (-1/(2a), b/[2a(a+c)]),
    (-1/(2a),-b/[2a(a+c)]),
    ( 1/(2a),-b/[2a(a−c)]),
    ( 1/(2a), b/[2a(a−c)]).

Their area is1/(ab). Thus κ=1/2 for the exact displayed outer/original ratio. As a rational check, a=5,b=3,c=4 gives areas2/15 and1/15; its strict confocal four-caustic has axes25/√34 and9/√34. The arXiv neighboring row's value2 belongs to the reciprocal expression. The full constancy claim under review does not prescribe that erroneous neighboring value.

## 9. Attribution and verification boundary

Stachel's published canonical parametrization and classical Jacobi addition, pole and compact-torus arguments are inputs. PR207 supplies the original inverse-edge algebra, and PR211 supplies the outer inverse-edge and triple-angle algebra. Their complete proofs were read and the needed calculations are reproduced here. The new comparison is the correct phase alignment on a common cyclic torus for all periods, with N3, N4 and N6 treated explicitly. This is presented as a credited companion consequence, not a separate discovery claim.

Exact symbolic and rational controls accompany the proof. Numerical diagnostics use actual Euclidean tangent intersections and inversions and are labeled non-interval evidence. Neither finite samples nor a neighboring theorem replaces the all-period pole argument. Separate adversarial review is required before publication of a result PR.
