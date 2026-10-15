# The inner focal-inversion area identity, with its exact quotient domain

**5100064 / AMR-050-0064 / arXiv k905. Complete first-turn candidate; separate review pending.** This is a credited consequence of classical central symmetry, not a novelty claim.

## 1. Exact source target and theorem

The target is arXiv:2004.12497v11 (29 October 2020), Table 10, printed p.12: the two focal-inversion areas of the **inner caustic-contact polygon** have ratio 1 for even N. The published companion *Fifty New Invariants*, Arnold Mathematical Journal 7 (2021), 341–355, omits this row and the 900-series table. Its last mathematical table, Table 9 on p.350, is not a second edition of k905. The pinned desk report's apparent claim to have verified k905 in both editions must not be repeated.

Let the billiard ellipse be

    E: x²/a²+y²/b²=1,  a>b>0,

and let C be its strictly nested nondegenerate confocal elliptical caustic. The shared foci are F+=(c,0), F−=(−c,0), c²=a²−b². Let P_i, i modulo N, be an orbit of **least even period N≥4**, with primitive star winding allowed. Write T_i for the unique tangency point of the side P_iP_(i+1) with C, in orbit traversal order. These T_i are the source's P''_i.

Ordinary unit-circle inversion about F is

    I_F(X)=F+(X−F)/|X−F|².                         (1)

Define V_i^±=I_(F±)(T_i), and join these vertices with **straight polygon edges** in the same cyclic order. The source's signed area convention is

    B_±=1/2 sum_i det(V_i^±,V_(i+1)^±).             (2)

**Theorem.** All vertices V_i^± are finite and distinct, and

    B_+=B_−.                                       (3)

Consequently k905 is exactly

    B_+/B_−=1 on the locus B_−≠0.                  (4)

The cross-multiplied identity (3) holds at common zeros as well. One may extend the rational invariant by the constant 1 there, but the raw expression is 0/0. Section 4 gives an admissible primitive N=4 orbit with both areas zero. No assertion that every fixed family contains a nonzero-area configuration is needed or made.

This uses ordinary focal **vertex inversion of the inner polygon**. It is not elliptic inversion, inversion of whole boundary arcs, inversion of the original or outer polygon, or inversion about a focus of an outer vertex locus.

## 2. Classical central pairing passes to contact points

Stachel, *The geometry of billiards in ellipses and their Poncelet grids*, Journal of Geometry 112, article 40 (2021), Corollary 4.2(i), pp.22–23, states central symmetry for even period and odd turning number with an **ellipse** as caustic. The preceding splitting discussion separates nonprimitive repetitions. In canonical rotation coordinates, least period N means gcd(N,τ)=1; even N therefore forces odd τ. Thus

    P_(i+N/2)=−P_i.                                 (5)

The canonical parametrization in Stachel, *On the Motion of Billiards in Ellipses*, European Journal of Mathematics 8 (2022), Theorem 4.3 and (4.9), gives the same half-turn by the 2K Jacobi shift and includes primitive stars. We credit these established inputs rather than claim a new integrability theorem. Reversing traversal, if needed to match the source's orientation convention, changes the signs of both signed areas and leaves their equality and defined ratio unchanged.

Negation sends the chord P_iP_(i+1) to its index-shifted chord. The caustic is invariant under negation and a tangent line to its strictly convex ellipse has a unique contact point. Therefore

    T_(i+N/2)=−T_i.                                 (6)

The contact points are distinct. For example, in the cited canonical coordinates they advance by the same primitive rotation as the vertices, offset by half a step. Equivalently, a repeated tangent line would repeat the oriented chord and the deterministic billiard orbit, contradicting least period. No repeated odd list is used as an even orbit.

Each focus lies strictly inside C: if its semiaxes are α>β>0, then c²=α²−β²<α². It cannot be any T_i on the boundary. Thus every denominator in (1) is strictly positive. Inversion is injective away from its center, so the distinct T_i give distinct finite inverted vertices. This is independent of whether their signed polygon area vanishes.

## 3. Inversion equivariance and signed area

A direct substitution in (1) gives

    I_(−F)(−X)=−I_F(X).                             (7)

Combining (6) and (7) yields

    V_(i+N/2)^−=−V_i^+.                            (8)

The index map is a cyclic shift, not a traversal reversal. Also det(−X,−Y)=det(X,Y) in the plane. Substitute (8) into the full sum (2) and relabel indices to obtain (3). The signed convention is essential for faithfully matching the source, although no division is used to prove equality.

For B_−≠0, (4) follows. At B_−=0, (3) gives B_+=0; ordinary real division is undefined. Cancellation of the common rational factor gives a constant extension, not a value of the original quotient at that point. These statements resolve the intended ratio invariant on its natural domain without adding an unsupported universal nonvanishing hypothesis.

## 4. An exact admissible four-orbit with zero denominator

Take

    a=√2, b=1, F±=(±1,0),
    P_0=(√2,0), P_1=(0,1),
    P_2=(−√2,0), P_3=(0,−1).                      (9)

This is a strictly convex primitive four-period billiard. At P_0 the incoming and outgoing unit velocities are (√2,1)/√3 and (−√2,1)/√3; their difference is parallel to the outward normal. The other axis vertices satisfy the reflection law by the axis symmetries. All sides have length √3 and all turning angles are nonzero.

Its caustic is

    C: x²/(4/3)+y²/(1/3)=1.                        (10)

Indeed it is confocal with E, with λ=2/3 subtracted from both squared semiaxes. It is strictly nested and nondegenerate. The first chord has equation x/√2+y=1; the dual-conic tangency condition is

    (4/3)(1/√2)²+(1/3)·1²=1.

The tangency point is T_0=(2√2/3,1/3). Reflecting the chord and its contact point in the axes gives, in traversal order,

    T_0=( 2√2/3, 1/3), T_1=(−2√2/3, 1/3),
    T_2=(−2√2/3,−1/3), T_3=( 2√2/3,−1/3).        (11)

Each contact point lies on its chord segment (parameter 1/3 or 2/3, according to direction). In particular these are actual contact points, not arbitrary centrally symmetric points on C.

The four T_i lie on the unit circle centered at O, which passes through both foci. None equals a focus. For any such T=(x,y), inversion about F+=(1,0) has

    |T−F+|²=2(1−x),
    [I_(F+)(T)]_x=1+(x−1)/[2(1−x)]=1/2.

For completeness their y-coordinates in order are

    3/2+√2, 3/2−√2, −3/2+√2, −3/2−√2.             (12)

They are all finite and distinct. Thus this inverse **vertex polygon** is collinear and has signed area zero. Inversion about F− similarly gives the line x=−1/2 and signed area zero. All original billiard and caustic data remain strict and nondegenerate; only the derived polygon's area degenerates. Its raw area ratio is therefore genuinely 0/0 in the stated even-period class.

A useful independent algebra check is available for the full axis four-orbit at arbitrary a>b>0. Its contact rectangle has half-width u=a³/(a²+b²), half-height v=b³/(a²+b²), and c²=a²−b². If r²=u²+v², direct inversion and shoelace summation give

    B_+=4uv(r²−c²)(r²+c²)/[(r²+c²)²−4c²u²]²
       =4(2b²−a²)(2a²−b²)/(a³b³).                 (13)

Thus a²=2b² is exactly the zero within this axis-orbit subclass. Equation (13) is a direct calculation, not an assertion about every phase of the fixed four-period family. The proof of equality (3) and the explicit zero (9)–(12) do not depend on (13).

## 5. Scope, checks, and credit

The exact source k905 is a classical central-symmetry consequence, just as neighboring arXiv rows k903,b and k904,b already credit symmetry for original and outer focal inversions. The present proof checks the contact-point construction and its actual denominator domain separately. Related campaign k406,a and k607 use the same elementary symmetry mechanism for different antipedal objects; they are not new inputs or duplicate claims of this target.

The checker provides exact rational contact-polygon algebra controls, exact four-orbit admissibility and inversion/area checks, and separately labeled high-precision diagnostics for actual primitive elliptical billiards. Finite controls do not establish a universal theorem by sampling. No source code from external authors is executed, no source PDFs are redistributed, and no novelty is asserted.

Hyperbolic or collapsed caustics, repeated odd lists, two-bounce degeneracies, unsigned area of regions, and inverted circular-arc boundaries are outside this statement. The constant extension at a common zero remains separate from the raw quotient. Independent source-and-proof review is required before any final promotion.
