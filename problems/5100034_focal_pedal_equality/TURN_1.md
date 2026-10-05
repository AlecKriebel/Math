# Focal-pedal ratio equality, with the phase-constancy error separated

5100034 / AMR-050-0034. 2026-10-02. One substantive author turn. Complete source-corrected candidate, independent review pending. This is a credited companion consequence of the reviewed mechanisms in [PR210](https://github.com/AlecKriebel/Math/pull/210) and [PR261](https://github.com/AlecKriebel/Math/pull/261), not a claim of independent novelty.

## 1. Exact theorem and source editions

Let the outer ellipse have semiaxes a>b>0 and foci F±=(±c,0). Fix a strictly nested nondegenerate confocal elliptical caustic with semiaxes α>β>0. Let P be a primitive billiard orbit of least period N≥3, allowing primitive star turning numbers. Let P' be its consecutive tangent-intersection polygon. For each focus let A± be the signed area of its pedal polygon on the original chord lines and B± the signed area of its pedal polygon on the sides of P', which are the tangents at the original vertices.

**Theorem.** There is a positive phase-independent real constant C, the same for the two foci, such that

    B+(w)=C A+(w),   B−(w)=C A−(w).                         (1)

For positive canonical traversal all four areas are strictly positive. Consequently, at every real phase,

    A+(w)/A−(w) = B+(w)/B−(w).                            (2)

Reversal changes the signs of the four areas and leaves these conclusions intact. Repetitions of a shorter nondegenerate orbit preserve (1)–(2), because each signed area is multiplied by the repetition count. Degenerate two-period diameters, hyperbolic/degenerate caustics and unsigned sums of lobe areas are excluded. The circular case, if added by a separate limit, is trivial because the foci coincide.

Equation(2) is arXiv2004.12497v11 Table7 k606, p9, renamed k607 in the published Table7 p349. Published k606 is a different product invariant. The imported assertion that the common ratio is itself phase-constant is false; §7 gives an exact convex counterexample. This does not refute the source equality.

## 2. Canonical coordinates and credited inputs

Uniform scaling lets us set α=1. Write k=c/α∈(0,1), k'=sqrt(1−k²), β=k'. Let K,K' be the real and complementary complete elliptic integrals, with modulus k in all Jacobi functions. For a positive primitive turning number τ with gcd(τ,N)=1 and 0<τ<N/2 put

    v=2Kτ/N,   δ=2v,   a=dn(v)/cn(v),   b=k'/cn(v).

Stachel's published Theorem4.3 and equation4.9 give

    P(u)=(-a sn u, b cn u),   P_i(w)=P(w+iδ).             (3)

The chord from P(u−v) to P(u+v) is tangent to the caustic at parameter u, with equation

    (-sn u, cn u/k') · X = 1.                            (4)

This is also immediate by the Jacobi addition identities, or Stachel's contact-midpoint description. In particular the original chord i has contact parameter w+v+iδ. The outer polygon side at original vertex i has equation

    (-sn u/a, cn u/b) · X = 1.                           (5)

The published canonical theorem and classical Jacobi identities are existing inputs, as are the campaign local trace arguments specified below. Their hypotheses are restated rather than importing an odd/even final conclusion outside its range.

## 3. The two actual focal-pedal maps

For F+=(k,0), orthogonal projection to(4) and(5) gives, respectively,

    q(u)=((k−sn u)/(1−k sn u), k' cn u/(1−k sn u)),
    Q(u)=(a(k−a sn u)/(a−k sn u), ab cn u/(a−k sn u)).    (6)

For real u their denominators exceed or equal1−k>0 and a−k>0. Both maps are actual Euclidean perpendicular feet. Complex continuation uses the bilinear dot product, not a Hermitian product.

Define the signed cyclic traces

    A(w)=1/2 Σ_i det(q(w+v+iδ),q(w+v+(i+1)δ)),
    B(w)=1/2 Σ_i det(Q(w+iδ),Q(w+(i+1)δ)).               (7)

They are exactly A+(w),B+(w), up to a harmless cyclic shift of outer side indexing. Consecutive tangents in P' have finite intersection: distinct original vertices can have parallel tangents only when antipodal, whereas0<δ<2K. All original chord lines are nondegenerate.

Central inversion changes the focus and corresponds to a2K phase shift. Directly from(6), or by projection equivariance,

    A−(w)=A(w+2K),   B−(w)=B(w+2K).                     (8)

## 4. Common meromorphic pole data for every period

Both traces have real periods4K andδ. Bezout's identity and gcd(τ,N)=1 give the common period

    L=4K/N.                                             (9)

This choice is valid in both parities. Do not replace it by an even-period reduced lattice before handling odd N. The classical imaginary shift fixes sn and negates cn, hence both maps in(6) undergo reflection in the x-axis. Thus

    A(w+2iK')=−A(w),   B(w+2iK')=−B(w).                (10)

They are meromorphic on X=C/(L Z+4iK' Z).

Put r=K+iK' and t=K−v. Their only possible poles on X are

    t+iK',   t+3iK',                                    (11)

and all have order at most one. Here is the full local justification.

### Original-pedal cancellation (credited PR261 local lemma)

At a common Jacobi pole, q has a removable singularity because numerator and denominator have at most a common simple pole with nonzero denominator leading coefficient. The other possible poles are sn u=1/k. On the sn torus with periods4K,2iK', this root is the double root r. The quarter-shift formulas

    sn(r+z)=dn z/(k cn z),
    cn(r+z)=−i k'/(k cn z)

show that q(r+z) is even in z and has pole order at most two. The neighboring maps q(r+z±δ) are holomorphic there, since0<δ<2K; a common Jacobi pole at a neighbor is removable as already noted. The two incident area terms combine into

    1/2 det(q(r+z), q(r+z+δ)−q(r+z−δ)).                 (12)

Evenness of q around r makes the second vector odd and holomorphic in z, so(12) has at most a simple pole. For a primitive orbit there is only one singular original-pedal vertex at such a phase modulo4K; other terms are holomorphic. This argument does not use even N. The shift by v in(7) moves the possible phase poles to r−v−iδ, all the first class in(11), with the imaginary translate giving the other.

### Outer-pedal cancellation (credited PR210 local lemma)

Common Jacobi poles are removable in Q by the same leading-coefficient cancellation. The other possible poles solve

    sn u=a/k=dn(v)/(k cn(v)).

The only two roots on the sn torus are r−v and r+v, using the same quarter-shift formulas and the degree-two property of sn. They are distinct and simple for0<v<K. At both roots, sn u=a/k and cn u=−ib/k, so the two numerator vectors in Q are equal; the derivatives of its denominator are opposite because dn changes sign. Hence the residues of Q at the two poles are opposite, nonzero and collinear.

Their separation isδ. Thus the cyclic area really has a term whose two endpoints are simultaneously singular. Its possible double coefficient is det(R,−R)=0. The remaining incident terms have at most one singular endpoint and at most simple poles. For primitive N≥3 exactly two adjacent vertices are singular; N=2 is excluded. Cyclic wrap-around obeys the same calculation because Nδ=4Kτ. After reduction by L these phases also give exactly(11). This local reasoning is parity-free, although PR210 used it for a final odd-period product.

This proves the common pole bound without relying on a numerical sample or on the desired equality.

## 5. Real positivity, including primitive star traversals

The focus lies strictly inside both ellipses: k<1<a. At any tangent line, the vector from the focus to its perpendicular foot is a **positive** multiple of the outward normal. The normal direction along either ellipse in the parametrization(-A sn u,B cn u) increases strictly, and advances by exactlyπ when u increases by2K. Therefore its direction change over0<δ<2K is strictly between0 andπ, at every real starting phase.

Consequently each determinant of consecutive vectors from F+ to the feet in either cyclic polygon is strictly positive. The closing edge has the same lifted direction increase, since Nδ=4Kτ. Translation of the origin to F+ does not change a shoelace area. Thus A(w)>0 and B(w)>0 for every real w, even for primitive stars. Applying(8) gives positivity at F− as well. Self-intersections of a star do not invalidate this signed-traversal argument.

This proves that none of the four real area denominators in(2) vanishes. It also shows that neither meromorphic trace is identically zero.

## 6. Residue matching gives the equality without premature division

A nonzero trace with the pole bound(11) and anti-periodicity(10) must have a genuine simple pole at both listed points. If it had no pole at the first, anti-periodicity would remove the second; then it would be holomorphic on the compact torus, hence constant, and the anti-period would force it to be zero, contradicting §5.

Let C be the ratio of the residues of B and A at the first pole. This is division only by a proved nonzero residue, not by a possibly vanishing area. The difference B−C A has no pole there. Anti-periodicity implies that its residue at the second pole also vanishes. The common simple-pole bound leaves no other possible singularity. Hence this difference is holomorphic on X and constant; its anti-period makes that constant zero:

    B=C A identically.                                  (13)

Evaluating at any real phase and using §5 proves C is real and positive. Applying(13) at w+2K and then(8) proves the same C works at the other focus. Now, and only now, divide the nonzero real denominators to obtain(2).

Thus the correct source equality is a credited consequence of the two earlier reviewed pole mechanisms on a common lattice. No independently new elliptic-function method is claimed.

## 7. Exact correction of the imported extra constancy claim

This section is separate from the proof of the source equality. Take the outer ellipse

    x²/21+y²/16=1,   F±=(±sqrt(5),0),

and the strictly nested confocal caustic with squared semiaxes189/25 and64/25. A convex primitive triangular orbit has consecutive vertices

    P=((sqrt(21),0), (-3sqrt(21)/5,16/5),
                       (-3sqrt(21)/5,−16/5)).           (14)

Each vertex is on the outer ellipse. Its side lines are x=−3sqrt(21)/5 and

    2x/sqrt(21)+y=2,   2x/sqrt(21)−y=2.

The caustic support-function test proves exact tangency: on either oblique side,
(189/25)(2/sqrt(21))²+64/25=4; the vertical side is a caustic tangent by construction. The three supporting tangents to a confocal inner ellipse give the billiard reflection law; alternatively it is checked directly by normalized incoming/outgoing vectors in the accompanying exact checker. The contacts are on the side segments. The triangle is nondegenerate, convex and has least period3.

Direct perpendicular-foot and shoelace computation gives

    A±=84(7sqrt(21)±sqrt(5))/625,
    B±=7(7sqrt(21)±sqrt(5))/10.                          (15)

These are all positive and B±/A±=125/24, consistently with(1). The common focal ratio is

    R=(7sqrt(21)+sqrt(5))/(7sqrt(21)−sqrt(5))>1.         (16)

The centrally inverted orbit −P is a different phase of the same triangular Poncelet family, preserves orientation and exchanges the foci. Its common ratio is1/R<1. Thus the common ratio is not phase-constant even in this convex, finite, nonzero-area example. This is a transcription/formulation correction to the imported extra assertion, not a refutation of the true equality or a claim to solve a different target.

## 8. Scope, checks and provenance

One substantive source-corrected proof/reconstruction turn is complete. The all-period equality and its strict real denominator positivity are universal analytic results; the exact triangle is a separate finite certificate. Modest exact algebraic controls and separately labeled high-precision diagnostics supplement but do not replace the proof.

Sources: [arXiv v11](https://arxiv.org/abs/2004.12497v11), [published edition](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), [Stachel](https://doi.org/10.1007/s40879-021-00524-2), [DLMF periods](https://dlmf.nist.gov/22.4), [DLMF addition](https://dlmf.nist.gov/22.8). Dependency proof hashes and their prior independent reviews are listed in SOURCE_HASHES.json and DEPENDENCIES.md. Upstream dataset research is credited in SOURCE_GATE.md.

No historical novelty, human peer-review, unsigned-area, hyperbolic-caustic or degenerate-diameter claim. The frozen full candidate must receive a separate source/proof audit before any campaign disposition or PR publication.
