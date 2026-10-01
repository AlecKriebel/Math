# Focal-inversion area products for elliptic billiards

**5100044 / AMR-050-0044 / arXiv k804,a. Complete author-turn-1 candidate; independent review pending.** No novelty or human-peer-review claim.

## 1. Target, edition and normalization

Fix a billiard ellipse E with semiaxes a>b>0 and foci f_+=(c,0), f_-=(-c,0), c^2=a^2-b^2, and a nondegenerate strictly nested confocal elliptical caustic with semiaxes alpha>beta>0. Suppose the billiard family has **least period N divisible by4**, with any admissible coprime turning number, including primitive stars. Let A be the signed area of the ordered orbit polygon. Invert its vertices in a unit circle about f_j, and join consecutive inverted vertices by straight segments; let A_j^dagger be that polygon's signed area. Then

    A A_j^dagger is constant over the family.              (1)

The two choices of focus have equal inverse areas. No hyperbolic/degenerate caustic or parity obtained by repeating a shorter orbit is included. The inverted polygon consists of straight chords between inverted vertices, not the circular images of complete original sides.

This is **k804,a in arXiv2004.12497v11, Table9 printedp11**, not the published companion's k804, which is a different cosine-sum assertion. The source defines signed areas and unit-radius focal inversion. In Garcia-Reznik's later [Exploring self-intersected N-periodics](https://doi.org/10.33039/ami.2022.02.001), the corresponding area-product label is k805,a; Proposition4.9 already gives the simpleN4 value4. That special case is credited, not presented as new.

## 2. Canonical coordinates and the cyclic area sum

Let k=c/alpha in (0,1), k'=beta/alpha, and K,K' be the real and complementary complete elliptic integrals. Jacobi functions below have modulus k. Stachel's published [Theorem4.3 and equation4.9](https://doi.org/10.1007/s40879-021-00524-2) give

    P(w)=(-a sn w,b cn w),
    a=alpha dn(v)/cn(v),    b=beta/cn(v),
    delta=2v=4K tau/N,    gcd(tau,N)=1,    0<tau<N/2.       (2)

Write N=4n and m=N/2=2n. Thus tau is odd and the half orbit is antipodal. Put ell=2K/m and

    S(w)=sum_(j=0)^(m-1) dn(w+j delta).                    (3)

The signed area is

    A(w)=2C_A S(w),    C_A=ab sn(v)cn(v)/dn(v)>0.          (4)

For completeness, the cross product of P(u-v),P(u+v) is

    2ab sn(v)cn(v)dn(u)/(1-k^2sn^2(v)sn^2(u)).

The dn addition formula expresses its half as
C_A[dn(u-v)+dn(u+v)]/2. Summing over N sides gives C_A times the N-term dn sum, which equals2S. This proves (4) for signed star-polygon areas as well as simple ones.

We will use the following elementary cyclic-sum fact, with its proof included rather than assumed from a neighboring candidate:

    S(w)S(w+ell/2) is a positive constant.                 (5)

Indeed S has periods ell and4iK', anti-period2iK', and is even. Period ell follows from periodsdelta,2K and gcd(tau,m)=1; evenness follows by reindexing the orbit. On X=C/(ell Z+4iK' Z), its only poles are simple poles at p=iK' and3p. Their residues are nonzero: each real-period translate of a Jacobi dn pole has the same residue, and the summands contributing to an identified pole add rather than cancel. Evenness plus the anti-period forces zeros at p+ell/2 and3p+ell/2. They are finite distinct points, exhaust the two-zero divisor and are simple. The half-shift product has no divisor and is holomorphic on a compact torus, proving (5). Positivity follows from dn>0 on the real line.

These Jacobi periods, poles, zeros and shifts are standard: [DLMF22.4](https://dlmf.nist.gov/22.4); addition identities are in [DLMF22.8](https://dlmf.nist.gov/22.8).

## 3. Exact focal-inverse edge-area formula

For f=f_+, the ordinary focal distance of P(w) is

    d(w)=a+c sn(w)>0.                                    (6)

Squaring verifies this from the ellipse equation, and its lower bound a-c>0 fixes the positive sign. Translating the inverted polygon by -f does not affect area, so we use vertices

    I(w)=(P(w)-f)/d(w)^2.                                 (7)

Set h=sn v, t=h^2, q=cn^2 v=1-t, and

    U=1-2k^2t+k^2t^2,
    V=1-2t+k^2t^2,
    W=1-k^2t^2,
    C=b h dn(v) q^2/alpha^3>0.                            (8)

Then

    cn(delta)=V/W, dn(delta)=U/W,
    U+V=2q dn^2(v), U^2-k^2V^2=k'^2 W^2>0.              (9)

For a side centered at phase u, write s=sn u, d_u=dn u and D(u)=1-k^2t s^2. The half-cross-product of its two inverted endpoints is

    E_+(u)=1/2 det(I(u-v),I(u+v))
          =C d_u D(u)/[(1+ks)(U+kVs)^2].                 (10)

Here are explicit algebraic steps. The Jacobi addition identities give

    d(u-v)d(u+v)
      =alpha^2(1+ks)(U+kVs)/(q D(u)),                    (11)

and

    det(P(u-v)-f,P(u+v)-f)
      =2alpha b h dn(v)d_u(1+ks)/D(u).                  (12)

Divide (12)/2 by the square of (11) to obtain (10). Equation (11) follows by expanding the product of a+c sn(u±v), using

    sn(u-v)+sn(u+v)=2s cn(v)dn(v)/D(u),
    sn(u-v)sn(u+v)=(s^2-t)/D(u).

This calculation uses no numerical reconstruction or complex conjugate. It gives meromorphic identities extending the real signed areas. All denominators in the original real inversion are nonzero; equivalently U>|kV| and1+ks>0 on the real line.

## 4. Antipodal pairing

Because N is even with tau odd, P(w+m delta)=-P(w). Pairing opposite sides gives

    A_+^dagger(w)=R(w+v),
    R(u)=sum_(j=0)^(m-1) B(u+j delta),
    B(u)=E_+(u)+E_+(u+2K).                               (13)

Since sn(u+2K)=-sn u and dn has period2K, elementary fraction addition yields

    B(u)=2C D(u)[U^2+k^2 V(V+2U)sn^2 u]
          /{dn u [U^2-k^2 V^2 sn^2 u]^2}.                (14)

We next show

    R(u)=C_R S(u+K)                                      (15)

for a real constant C_R. The important point is cancellation of opposite double-pole coefficients in the **cyclic sum**, not boundedness of each summand.

## 5. Generic pole analysis and cancellation

Suppose V is nonzero. In the base torus with periods2K,4iK', let r=K+iK' and p=iK'. Formula (14) has possible poles only at

    r, r+2iK';
    r±delta, r±delta+2iK'.                               (16)

At r and its imaginary translate, dn has a simple zero, while
U^2-k^2V^2sn^2r=U^2-V^2 is nonzero. Indeed U-V=2t k'^2>0 and U+V>0. Thus these are at most simple poles.

The other denominator factor is W^2 times

    dn^2(delta)-k^2cn^2(delta)sn^2u.

It has a double pole at p on the smaller sn^2 torus and zeros at r±delta, by

    sn(z+K+iK')=dn(z)/(k cn(z)).                          (17)

Those two zeros are distinct modulo2K,2iK': otherwise delta=K within0<delta<2K, contradicting V nonzero. They are neither p nor r and exhaust the degree-two zero divisor, hence are simple. Squaring this factor permits at most double poles of B at r±delta. A numerator cancellation can only lower the order.

At a common pole of sn,cn,dn, the expression (14) is removable: sn^2 has order-2, dn order-1, the numerator has order at worst-4 and the denominator order-5, giving a zero of at least order1. This accounts for every possible pole; none at infinity or elsewhere is omitted on the torus.

The standard Jacobi reflection about r is

    sn(2r-u)=sn u,    dn(2r-u)=-dn u.

Equation (14) therefore gives

    B(2r-u)=-B(u).                                       (18)

If the Laurent expansion at r+delta begins b_-2 epsilon^-2+b_-1 epsilon^-1, then the expansion at r-delta begins

    -b_-2 epsilon^-2+b_-1 epsilon^-1.

The two order-two coefficients are opposite. In R, the locations r+delta and r-delta are in the same cyclicdelta orbit. For each possible pole of R, one translate from each of these locations contributes its double coefficient, which cancels exactly. There is one such contribution of each type per cyclic orbit modulo2K. The remaining r-family contributes only simple poles. Thus R has at most simple poles at r and r+2iK' moduloell,4iK'.

This argument allows vanishing leading coefficients. It does not require the generic double poles actually to occur, only the stated order bound and reflection relation.

## 6. The N4 exception

If V=0, then cn(delta)=0, so delta=K. Primitivity in (2) forces N=4 andtau=1. The generic pole-order argument is not used in this case. Formula (14) becomes

    B(u)=2C/U^2 [q/dn u+t dn u].                          (19)

All poles are simple. They occur at r andp with their imaginary translates. Now m=2 andell=K, so r=p+K andp are the same reduced real class. Hence R still has at most the same two simple poles on X.

## 7. Residue matching, parity and completion

In both cases B has real period2K and anti-period2iK': sn^2 is unchanged by these shifts and dn changes sign under2iK'. The cyclic sum R is also periodicdelta, hence periodicell. It is meromorphic on X, with possible simple poles at r and r+2iK'.

The function S(u+K) has exactly the same pole locations and character, and has a nonzero residue at r. Choose C_R to cancel the residue there. Anti-periodicity cancels the other residue. The difference is holomorphic on the compact torus and therefore constant; the anti-period forces that constant to vanish. This proves (15). For realu, both R andS(u+K) are real and the latter is positive, so C_R is real. No complex branch is selected.

Combining (4), (13) and (15),

    A(w)A_+^dagger(w)=2C_A C_R S(w)S(w+K+v).             (20)

Because N=4n, m=2n andtau is odd,

    (K+v)/ell=(m+tau)/2 is a half-integer.

The phase shift in (20) is ell/2 moduloell, so (5) proves constancy. Central symmetry sends the ordered orbit to its negative by a cyclic shift; inversion about f_- followed by central reflection equals inversion of the opposite vertices about f_+. Central reflection preserves signed area. Thus A_-^dagger=A_+^dagger, proving the claim for both foci.

The product is unaffected by reversing the ordering, since both signed areas change sign. A circular billiard is immediate from rigidly rotating regular star polygons and central inversion, and is separate from the k>0 proof.

## 8. The credited N4 value and limits

For the axial N4 orbit with vertices (0,b),(-a,0),(0,-b),(a,0), its area is2ab. After inversion about(c,0), translating the focus to the origin gives vertices

    (-c/a^2,b/a^2), (-1/(a+c),0),
    (-c/a^2,-b/a^2), (1/(a-c),0).

Their signed area is2/(ab), since a^2-c^2=b^2. Thus the invariant is4. This confirms the previously published special case; it is not an independent novelty claim.

Exact algebraic, lattice, pole-coefficient and N4 controls accompany the proof. Separate numerical checks use direct Euclidean inversion and signed shoelace areas, including primitive stars and wrong-parity controls. They are diagnostics, not interval certificates or substitutes for the universal argument.

Stachel's canonical theorem, standard Jacobi identities and the classical complex-pole method are credited. The two-pole cyclic-sum organization also reuses the current author's neighboring k203,b work; its needed facts are proved here, not assumed from an unreviewed result. No exhaustive novelty claim, hyperbolic extension, merge, release or external communication is made. A separate uninvolved adversary must review this candidate before a claimed-result PR.
