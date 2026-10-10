# Outer focal-antipedal areas: k608 with its exact quotient domain

**5100036 / AMR-050-0036. Full domain-qualified candidate, author turn 1. Awaiting independent review. No novelty or priority claim.**

## 1. Exact target and theorem

The assigned item is Reznik–Garcia–Koiller, *Eighty New Invariants in the Elliptic Billiard*, [arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), Table 7, printed p9, k608. Its ratio is the signed area of the **outer tangent polygon's antipedal about the first original billiard focus**, divided by the corresponding area about the other original focus. It asserts value 1 for even N. Section 3.5 defines antipedals by successive perpendicular-line intersections; equation (1), printed p3, specifies signed shoelace area. Neither focal pedal projections nor the outer locus's own foci are the target.

The published companion, *Fifty New Invariants*, Arnold Math. J. 7 (2021), Table 7 printed p349, has no k608 row. Its section 3.7 predicts related antipedal identities after a differently numbered table. We retain the exact arXiv target and correct the imported prior report's edition conflation.

Let E be `x²/a²+y²/b²=1`, with `a>b>0`, original foci `F±=(±c,0)`, `c²=a²-b²`, and a strictly nested nondegenerate confocal **elliptical** caustic. Let `(P_i)` be a billiard of even least period N. Put `T_i=ell_i intersect ell_(i+1)`, where ell_i is the supporting tangent to E at P_i. For any M define the antipedal line

    L_i(M): (T_i-M)·(X-T_i)=0,

and let `Q_i(M)=L_i(M) intersect L_(i+1)(M)`. Define

    B(M)=(1/2) sum_i det(Q_i(M),Q_(i+1)(M)).       (1)

### Theorem

For every orbit under these hypotheses, all T_i and Q_i(F±) are finite and uniquely defined, and

    B(F+)=B(F-).                                  (2)

Hence the source ratio is 1 wherever its denominator is nonzero. This covers all admissible primitive even star winding numbers as well as convex orbits. Repetitions of an even primitive orbit retain the equality, with both areas multiplied by the repetition count. An artificially even indexing length obtained by repeating an odd primitive orbit is not a parity hypothesis for this theorem.

The quotient qualification is necessary **even for convex primitive billiards**: section 4 constructs a convex six-orbit with `b=1, a=1+sqrt(3)`, whose two finite antipedals both have signed area zero. Thus the literal raw quotient is 0/0 there. This is not a varying defined ratio and does not refute the rational identity. The equality is global; a chosen constant extension of the ratio is a separate convention. We do not claim a nonempty defined quotient locus on every exceptional family.

## 2. Credited central symmetry and geometric regularity

The substantial classical input is Stachel, *On the motion of billiards in ellipses*, European Journal of Mathematics 8 (2022), Theorem 4.3 and equation (4.9), [DOI 10.1007/s40879-021-00524-2](https://doi.org/10.1007/s40879-021-00524-2). Its canonical parameter is

    P(u)=(-a sn(u), b cn(u)),
    u_(i+1)-u_i=4mK/N, gcd(m,N)=1,

where the Jacobi modulus is the caustic's numerical eccentricity, K its complete elliptic integral, and m is the primitive turning number. The standard real half-period identities `sn(u+2K)=-sn(u)`, `cn(u+2K)=-cn(u)` are recorded in [DLMF section 22.4](https://dlmf.nist.gov/22.4). When N is even, m is odd, so

    P_(i+N/2)=-P_i.                               (3)

The source itself credits symmetry for neighboring focal-pedal identities. Related campaign targets use this same classical mechanism. The present outer-antipedal construction and domain certificate are checked explicitly rather than counted as a new central-symmetry theorem.

The tangents at consecutive P_i cannot be parallel: for an ellipse this would mean `P_(i+1)=-P_i`; the chord would pass through O and intersect, rather than support, the strict centered caustic. Thus every T_i is finite.

Three consecutive P_i are distinct. Adjacent repetitions are not billiard chords. If `P_(i+2)=P_i`, specular reflection forces normal backtracking. At `P=(a cos theta,b sin theta)`, a normal chord has confocal tangency parameter

    lambda_normal=a² sin²(theta)+b² cos²(theta) >= b².

This follows by applying the dual-conic tangency formula to the line through P in its normal direction. A strict inner elliptical caustic has `0<lambda<b²`, excluding normal backtracking. Hence the two points `T_i,T_(i+1)` on ell_(i+1) are distinct: otherwise their common point would carry tangents to three distinct points of the strictly convex conic, impossible for a point in the plane.

Each focus lies strictly inside E, whereas ell_(i+1) is a supporting tangent. Therefore that line does not contain either focus. Since T_i and T_(i+1) are distinct on the line,

    det(T_i-F±, T_(i+1)-F±) != 0.                 (4)

Equation (4) is precisely the nonparallel-normal condition for the two adjacent antipedal lines. It establishes finiteness and uniqueness of every Q_i(F±), without an unproved convexity claim about the antipedal polygon.

## 3. Equality of the actual antipedals

Central inversion sends ell_i to ell_(i+N/2), so uniqueness of the tangent intersections gives

    T_(i+N/2)=-T_i.

If X lies on L_i(F+), then

    (-T_i-F-)·(-X+T_i)=(T_i-F+)·(X-T_i)=0.

Thus the isometry X→-X carries L_i(F+) to L_(i+N/2)(F-). Uniqueness from (4) yields

    Q_(i+N/2)(F-)=-Q_i(F+).                      (5)

This is a cyclic reindexing, not reversal. Since `det(-X,-Y)=det(X,Y)`, equation (5) proves (2) with the signed areas intact. Neither simplicity nor a positive denominator has entered the proof.

## 4. An exact convex six-orbit with a common zero

We give a one-parameter family of certified convex six-orbits, then choose the parameter where the antipedal area vanishes. This varies the ellipse/caustic while selecting the example; it is not a claim of phase variation of the ratio in one Poncelet family.

### 4.1 Orbit and caustic

Let `a>1`, `b=1`, and set

    h=sqrt(2a+1), C=a/(a+1), S=h/(a+1),
    c=sqrt(a²-1), lambda=C².

Then `C²+S²=1`, and the following vertices are in counterclockwise cyclic order on E:

    (a,0), (aC,S), (-aC,S),
    (-a,0), (-aC,-S), (aC,-S).                  (6)

They are six distinct points; the orbit is convex and primitive, with winding number 1.

At `(aC,S)`, the incoming diagonal vector is `(-C,S)`, which already has unit length, and the outgoing unit vector is `(-1,0)`. Their difference `(1-C,S)=(C/a,S)` is exactly the outward ellipse normal there. This proves the reflection law. The other three non-axial vertices follow by axial reflections. At `(±a,0)`, the incident vectors are reflections of each other about the horizontal normal. Thus all six bounces are physical billiard reflections.

The two horizontal sides are `y=±S` and support the ellipse

    x²/(a²-C²)+y²/(1-C²)=1.                     (7)

One diagonal has equation `Sx+Cy=aS`; its dual-conic tangency test is

    (a²-C²)S²+(1-C²)C²=a² S²,

using `S²=1-C²`. Symmetry handles the remaining three diagonals. Because `0<C²<1<a²`, (7) is a strictly nested nondegenerate confocal elliptical caustic.

### 4.2 Outer vertices and exact antipedal area

Intersecting the actual outer ellipse tangents at (6) gives, in cyclic order,

    (a,v), (0,w), (-a,v), (-a,-v), (0,-w), (a,-v),
    v=1/h, w=(a+1)/h.                           (8)

We compute the antipedal about `(c,0)` by the lines in section 1. Set

    d=v², D=(a+1)(1-d)/2, E=c(1+d)/2,
    Z=a(1+d), F=c d,
    Y0=w-c E/w, Y1=c D/w.

Direct intersection gives its six vertices

    (D-E,Y0+Y1), (-D-E,Y0-Y1), (-Z+F,0),
    (-D-E,-Y0+Y1), (D-E,-Y0-Y1), (Z+F,0).        (9)

For example the first two lines of (8) are

    (a-c)x+v y=a²-ac+v²,
    -c x+w y=w².

Solving them yields `x=(a+1)(a-c-d)/(a+1-c)`. Since `c²=a²-1`, the denominator product `(a+1-c)(a+1+c)=2(a+1)` reduces this to `D-E`; the second line gives `y=Y0+Y1`. The other intersections follow by the same calculation and reflection across the x-axis. All divisions are legal: `a±c>0`, `a+1±c>0`, and v,w,h are positive.

Taking the shoelace sum of (9) gives

    B(F+)=2Y0(D+Z)+2Y1(E+F)
          =2w(D+Z)+(c²/w)[2dD-a(1+d)²]
          =-4a(a+1)(a²-2a-2)/(2a+1)^(3/2).     (10)

This is an exact identity. The first equality follows by pairing opposite horizontal reflections; the second substitutes the definitions of Y0,Y1,E,F; the final one uses `d=1/(2a+1)`, `w=(a+1)/sqrt(2a+1)`, and `c²=a²-1`. The authored symbolic checker independently forms the six tangent intersections and antipedal intersections and reproduces (10).

Now choose `a=1+sqrt(3)`. Then `a²-2a-2=0`, so (10) is zero. All constructions remain finite and physical by the preceding proofs. The other focus has area zero by (2). In fact `c=h` at this parameter, so no root isolation or numerical caustic reconstruction is needed.

The original orbit (6) is convex, but its antipedal need not be. A zero signed shoelace area is therefore consistent with the six finite vertices in (9). This is distinct from the known original-polygon six-antipedal zero at aspect ratio 2 mentioned by Garcia–Reznik in their later self-intersected-billiard paper; no claim of novelty for zero-area phenomena is made.

## 5. Scope and result

The universal, everywhere-defined conclusion is equality of the two signed outer-antipedal areas. The source quotient is identically 1 on its natural nonzero-denominator domain. The exact convex six-orbit shows why the raw ratio cannot be assigned a value at every member of every admissible family without a convention. No varying defined ratio, hyperbolic-caustic theorem, unsigned-area interpretation, or repeated-odd-period extension is asserted.

Finite exact checks are controls for the formulas and degeneracy certificate; the universal proof is the credited central symmetry plus the verified geometric equivariance. Independent review is required before publication as a result.
