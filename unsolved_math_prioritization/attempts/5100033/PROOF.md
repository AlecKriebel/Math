# The product of the two outer focal-pedal areas

**5100033 / AMR-050-0033 / arXiv k605,a. Complete author-turn-1 candidate; separate review pending.** No novelty or priority claim.

## 1. Exact theorem and edition mapping

Let E be an ellipse with semiaxes a>b>0 and foci f_±=(±c,0), where c²=a²−b². Fix a strictly nested, nondegenerate confocal elliptical caustic. Let P range over a Poncelet billiard family of odd least period N≥3, including primitive star orbits. Let P' be the polygon whose vertices are consecutive intersections of the tangents to E at the vertices of P. Project f_+ and f_- orthogonally onto the consecutive side lines of P', and let B_+ and B_- be the **signed** areas of the two ordered pedal polygons. Then

    B_+ B_- is constant over the family.                  (1)

This is k605,a in [arXiv2004.12497v11](https://arxiv.org/abs/2004.12497v11), Table 7, printed p. 9. The same primed-area product is renamed **k606** in the [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table 7, printed p. 349. Published k605 is the different unprimed/original-orbit product. The formula and construction, not a label carried across editions, fix the present target.

The source defines areas by signed cross-product sums. The pedal feet are on the outer polygon's side lines, which are tangents to E at the original vertices. They are not projections onto the original billiard chords. Hyperbolic or collapsed caustics and relabeling repetitions of shorter orbits are outside the restored source scope.

## 2. Canonical phase and exact outer-pedal map

Let the caustic semiaxes be α>β>0, and put k=c/α, k'=β/α. Let K,K' be the real and complementary complete elliptic integrals. Stachel's published [Theorem 4.3 and equation 4.9](https://doi.org/10.1007/s40879-021-00524-2) give canonical coordinates

    P(w)=(-a sn w, b cn w),
    a=α dn(v)/cn(v),  b=β/cn(v),
    δ=2v=4Kτ/N,  gcd(τ,N)=1,  0<τ<N/2.                  (2)

The Jacobi modulus is k∈(0,1); 0<v<K. Orientation may be reversed to arrange the displayed turning-number range without changing a product of two signed areas. Vertices occur at w+jδ.

The tangent to E at P(w) is

    n(w)·X=1,  n(w)=(-sn(w)/a, cn(w)/b).

The perpendicular foot from f_+ to that tangent is

    Q_+(w)=f_+ + [(1−n(w)·f_+)/(n(w)·n(w))] n(w).

Writing s=sn w and using cn²w=1−s² gives the explicit cancellation

    Q_+(w)= ( a(c−a sn w)/(a−c sn w),
              ab cn w/(a−c sn w) ).                     (3)

Indeed n·n=(a−cs)(a+cs)/(a²b²), and the numerator factor a+cs cancels. The real denominator is at least a−c>0. Direct algebra also gives

    Q_+(w)·Q_+(w)=a².

This is the classical auxiliary-circle property of a focal pedal of an ellipse; the calculation is included, so it is not an additional unproved input. The complex dot product in the meromorphic continuation is bilinear, not Hermitian.

The other focus satisfies

    Q_-(w)=−Q_+(w+2K).                                  (4)

Let

    T(w)=1/2 sum_(j=0)^(N−1)
       det(Q_+(w+jδ), Q_+(w+(j+1)δ)).                    (5)

The outer polygon's consecutive side lines are the tangents in this same cyclic order, up to a cyclic index shift. Therefore

    B_+(w)=T(w),  B_-(w)=T(w+2K).                        (6)

The outer intersections are finite: distinct consecutive vertices are not antipodal because 0<δ<2K. A cyclic shift of the feet has no effect on their signed area.

## 3. Poles of the focal-pedal map

Write p=iK' and r=K+iK'. The standard Jacobi periods and shifts used below are listed in [DLMF 22.4](https://dlmf.nist.gov/22.4); the canonical and addition identities are in [DLMF 22.8](https://dlmf.nist.gov/22.8).

At a common pole of sn and cn, formula (3) is removable: both its numerator and denominator have at most a simple pole, with nonzero denominator leading coefficient. Its other possible poles occur when

    sn w=a/c=dn(v)/(k cn(v)).

The quarter-period identities

    sn(r+z)=dn z/(k cn z),
    cn(r+z)=−i k'/(k cn z),
    dn(r+z)= i k' sn z/cn z

show that the two solutions on the torus with periods 4K,2iK' are

    z_-=r−v,  z_+=r+v.                                  (7)

They are distinct because 0<v<K. They are simple roots of a−c sn w: the derivative is −c cn w dn w, which is nonzero at both points. They exhaust the roots because sn has degree two on that torus. On the larger torus with periods 4K,4iK', there are also their translates by 2iK'. There are no further poles.

At z_- and z_+, sn and cn take the same respective values a/c and −ib/c. Thus the two numerator vectors of (3) are identical:

    (−ab²/c, −iab²/c).

The derivatives of the denominator are opposite, since dn changes sign between r−v and r+v. Consequently Q_+ has opposite, nonzero and **collinear** residue vectors at its two poles. Collinearity, rather than their magnitude, is the key fact below.

## 4. The cyclic area has only simple poles

Although Q_+ has simple poles, a term of (5) could a priori have a double pole when both endpoint vectors are singular. The two locations in (7) differ by δ=2v, so such simultaneous poles really occur at adjacent vertices.

Near such a phase, write the singular endpoints as

    Q_+(z_-+ε)=R/ε+A+O(ε),
    Q_+(z_++ε)=−R/ε+B+O(ε).

The coefficient of ε^(−2) in their determinant is det(R,−R)=0. Therefore this term has at most a simple pole. Every other incident area term has at most one singular endpoint and hence also has at most a simple pole. This accounts for the entire cyclic sum, including the edge that crosses the index cut: Nδ=4Kτ is a true period of Q_+.

For a fixed pole phase there are exactly two singular vertices, at adjacent indices. Primitivity makes the phase orbit have N distinct members modulo4K, so no additional pole copy is hidden at that phase. The same analysis applies to the imaginary translates. It follows that T has at most simple poles at z_−−jδ and their translates by 2iK'.

Define the reduced real period

    L=4K/N.

The function T has periods δ and4K. Since gcd(τ,N)=1, it therefore has period L. On

    X=C/(L Z+4iK' Z)

the only possible poles of T are

    b+p and b+3p,  where b=K−v.                         (8)

Indeed z_+=z_-+δ and every jδ is an integer multiple of L. Both poles have order at most one.

This cancellation differs from merely bounding the area terms separately. The adjacent two-pole term was checked explicitly; an argument that assumes every term has only one singular endpoint would be false.

## 5. Reflection character and the complementary zero divisor

The real and imaginary Jacobi shifts in (3) give

    Q_+(w+4K)=Q_+(w),
    Q_+(w+2iK')=J Q_+(w),  J=diag(1,−1).

Taking determinants gives

    T(w+2iK')=−T(w).                                    (9)

Also sn(2K−w)=sn w and cn(2K−w)=−cn w, so

    Q_+(2K−w)=J Q_+(w).

Reflection reverses the cyclic vertex order and has determinant −1. Those two signs cancel, yielding

    T(2K−w)=T(w).

Because T has period δ=2v, it is also even about b=K−v. Thus the function F(z)=T(b+z) is even, has real period L, anti-period 2iK', and at most simple poles at p and3p.

If F has no poles, it is constant on the compact torus; the anti-period then makes it zero. In that case the desired product is already constant. Otherwise the anti-period forces both possible poles to be present and simple. Their total multiplicity is two.

At p+L/2, evenness, period L and anti-period 2p give F=−F. This point is not a pole, so it is a zero. Its translate3p+L/2 is another distinct zero. The zero and pole multiplicities of a nonconstant elliptic function agree by the argument principle on a period parallelogram. Hence these two zeros exhaust its zero divisor and are simple. The product

    F(z)F(z+L/2)

has no poles, since each pole is canceled by a zero of the translated factor. It is therefore constant. Equivalently,

    T(w)T(w+L/2) is constant.                            (10)

No division by a pedal area, residue, or possibly vanishing proportionality constant occurs.

## 6. Odd-period conclusion

For odd N,

    2K=(N/2)L ≡ L/2 modulo L.

Equations (6) and (10) immediately give

    B_+(w)B_-(w)=T(w)T(w+2K)=constant,

which is the exact target (1). The proof includes every primitive star turning number because only coprimality and the canonical phase shift were used. Both areas change sign under orientation reversal, leaving their product unchanged.

For even primitive periods, switching the focus is a full reduced real-period shift, yielding equality of the two areas instead. This argument does not assert constancy of their product in that parity. The circular limit, if included separately, follows directly from rigid rotation of regular star polygons and coincident foci.

## 7. Verification and credit

The accompanying author checks verify the real projection and auxiliary-circle identities, the pole-vector cancellation, reduced-lattice multiplicities, the half-period zero-divisor argument, and direct real geometry of the actual outer tangent polygon. Numerical tests use intersections of adjacent tangents, then independent Euclidean projection onto the resulting outer side lines. They include odd primitive stars and separate even-parity controls. Complex diagnostics check the pole cancellation; they are not interval certificates or replacements for the universal proof.

The canonical theorem is credited to Stachel, the Jacobi inputs to classical elliptic-function theory, and the complex pole method to the existing billiard-invariant literature. The two-pole character/divisor organization also appeared in the neighboring k203,b and k804,a candidates reviewed during this campaign; all facts needed here are proved afresh. The present author did not coauthor those candidates. This source-specific outer-focal-pedal argument needs its own uninvolved independent review. No exhaustive novelty search or historical-first claim is made.
