# A projective obstruction for every nonsymmetric hexagonal-ring core

Third mathematical edition. [Independent acceptance](INDEPENDENT_RING_ACCEPTANCE.md) and [exact reproduction conventions](REPRODUCTION.md) accompany this proof. The distinct-vertex hypothesis inherited from a conforming realization is repeated explicitly in Lemma 2.

## Status and scope

This is one branch of the third newly documented substantive pass for row 1761 / problem 30002861 / OWR-13678-002, dated 2026-10-13 UTC. It is not an additional pass beyond that shared third pass.

**Result.** The entire twelve-vertex hexagonal-ring core used in the first two passes is excluded from cycle balance, with arbitrary coordinates and no symmetry assumptions. The proof uses exact projective incidence and strict convexity, not an optimization failure. It extends the accepted threefold alternating-radius exclusion to every admissible nonsymmetric realization of that topology, including nonconvex inner hexagons.

This does not settle other core topologies or universal quartic Hermite interpolation. No literature novelty or worldwide openness claim is made.

The fixed model is a finite conforming straight-line triangulation of a polygonal disk, with nondegenerate original triangles. The data are arbitrary vertex values and both first derivatives, and the requested interpolants are globally C1 polynomials of degree at most four on the original triangles.

### Accepted mathematical dependencies

The exact earlier proofs and independent acceptances are linked in [DEPENDENCIES.md](DEPENDENCIES.md).

The first-pass reduction and its independently accepted support theorem provide:

- A closed active component induces a convex triangulated polygon K, and every induced edge is active.
- An induced boundary vertex of even degree is a strict corner; a straight boundary vertex has odd induced degree.
- At a strict corner, the two exterior zero rays impose the exterior-attachment construction described below.
- Every closed component contains at least three original nonsingular degree-four interior mesh vertices. A degree-four vertex in such a component has its full original four-neighbor star in the component.

The independently accepted second-pass theory provides face-normalized, nonzero dependency coordinates x_v. For an edge vw with opposite original vertices u and z, they satisfy

    x_v det(z-v,u-v) = x_w det(u-w,z-w).                 (1)

Equivalently, writing V_v=(v_x,v_y,1)^T and U_v=x_v V_v,

    det(U_v+U_w,U_u,U_z)=0.                              (2)

All determinants with three columns below are homogeneous 3-by-3 determinants. Equation (2) follows from (1) without dividing by any sum of weights: the homogeneous vector U_v+U_w belongs to the projective line through the two opposite vertices. The weights x_v themselves are nonzero. The existing equivalence says that a balanced closed component would be a genuine quartic Hermite obstruction, including for a suitable pure-gradient datum.

No additional literature is used in this proof.

## 1. A boundary positivity lemma

**Lemma 1.** Suppose a side vw of the convex closed support K has no straight subdivision vertices. Its two incident triangles, including the original triangle outside K, form a strictly convex quadrilateral. In particular x_v and x_w have the same sign in any balanced closed component.

**Proof.** Let the strict corners immediately before v and after w be p and q. The accepted exterior-attachment theorem gives the common outside opposite vertex Q as

    Q=v+t(v-p)=w+s(w-q),    t,s>0.

The two lines Qv and Qw are supporting lines of K, namely the preceding and following sides. The convex polygon K lies in the closed cone from Q through the segment vw and in the half-plane beyond vw, away from Q.

Let u be the support triangle's opposite vertex. The ray Qu therefore meets vw in its closed segment. An endpoint intersection would make u collinear with Q and v or with Q and w. The corresponding determinant in (1) would vanish, contrary to the activity of that endpoint coefficient. Hence the intersection lies in the open segment vw. The opposite vertices u and Q lie on opposite sides of the line vw, so the two-triangle quadrilateral is strictly convex.

In the transverse-diagonal formula of the second pass, if this intersection is v+p_0(w-v), then

    x_w/x_v=p_0/(1-p_0),    0<p_0<1.

The ratio is strictly positive. ∎

Thus all boundary weights have one sign whenever every boundary vertex is a strict corner. This statement does not claim that each subedge of a subdivided straight side has a positive ratio; that stronger assertion is not used here.

## 2. The core topology

Use outer boundary vertices O_0,...,O_5 in counterclockwise order and inner vertices I_0,...,I_5. Subscripts on these lists are modulo six. The core consists of the twelve annulus triangles

    (O_i,O_(i+1),I_(i+1)),
    (O_i,I_(i+1),I_i),          i=0,...,5,

and the four central triangles

    (I_0,I_1,I_2), (I_2,I_3,I_4),
    (I_4,I_5,I_0), (I_0,I_2,I_4).

It has 12 vertices, 27 edges, and 16 triangles. Its six boundary vertices have induced degree four, so in a closed active realization they are all strict corners by the accepted support theorem. No straight subdivision occurs on its boundary. Lemma 1 therefore gives

    x_(O_0),...,x_(O_5) all have the same sign.            (3)

The six inner vertices are genuinely interior points of K. No convexity assumption is made about the polygon I_0...I_5 itself.

## 3. A homogeneous pencil-collapse lemma

**Lemma 2.** Suppose the twelve vertices are distinct, as required by the fixed conforming-realization model, all twelve weights are nonzero, and equation (2) holds on all 21 interior edges of the displayed core, with all its triangle triples nondegenerate. Then there is a nonzero homogeneous vector S such that

- O_0,O_3,I_2,I_5 lie on one projective line through S;
- O_1,O_4,I_0,I_3 lie on a second such line;
- O_2,O_5,I_4,I_1 lie on a third such line.

More precisely, after using the homogeneous weighted vectors

    A=U_(I_0), B=U_(I_2), C=U_(I_4)

as a basis, S=A+B+C and every vector in each of the three classes is its corresponding base vector A, B, or C plus a scalar multiple of S.

**Proof.** The central triangle is nondegenerate and the three weights are nonzero, so A,B,C are linearly independent.

Put c=U_(I_1), a=U_(I_3), b=U_(I_5). The balance equation across the central edge I_0 I_2 says that A+B,c,C are dependent. Thus

    c=alpha_c(A+B)+beta_c C.                              (4)

Both alpha_c and beta_c are nonzero. If alpha_c were zero, I_1 would be the same geometric point as I_4; if beta_c were zero, the triangle I_0 I_1 I_2 would be degenerate. Cyclically,

    a=alpha_a(B+C)+beta_a A,
    b=alpha_b(C+A)+beta_b B,                              (5)

with all six displayed alpha and beta coefficients nonzero.

Consider the four-star at I_1. The edge I_0 I_1 has opposite vertices I_2 and O_0, and I_2 I_1 has opposite vertices I_0 and O_1. Equation (2) therefore yields

    U_(O_0)=k(A+c)+l B,
    U_(O_1)=m(B+c)+n A,

where k and m are nonzero: otherwise O_0=I_2 or O_1=I_0 as projective, hence geometric, points.

The other two edges at I_1, namely O_0 I_1 and O_1 I_1, give

    det(U_(O_0)+c,A,U_(O_1))=beta_c m(k-l+1)=0,
    det(U_(O_1)+c,U_(O_0),B)=beta_c k(m-n+1)=0.

Here determinants are calculated in the basis A,B,C; in arbitrary coordinates they have the common additional nonzero factor det(A,B,C). It follows that l=k+1 and n=m+1. With Q_c=A+B+c we have

    U_(O_0)=B+k Q_c,
    U_(O_1)=A+m Q_c.                                    (6)

Also k+1 and m+1 are nonzero. For example, k=-1 would make U_(O_0)=-A-c, degenerating the required triangle O_0 I_1 I_0. The argument for m is the same using O_1 I_2 I_1.

Apply the same four-star argument at I_5. With Q_b=C+A+b it gives

    U_(O_5)=C+q Q_b,                                    (7)

where q and q+1 are nonzero.

Now use the two still-unused edges I_0 O_0 and I_0 O_5. Their opposite pairs are (I_1,O_5) and (O_0,I_5), respectively. Direct determinant expansion in A,B,C gives

    det(A+U_(O_0),c,U_(O_5))
      =beta_c q(k+1)(alpha_b-beta_b+1),                   (8)

    det(A+U_(O_5),U_(O_0),b)
      =beta_b k(q+1)(alpha_c-beta_c+1).                   (9)

Every prefactor is nonzero, as already justified. Balance forces

    beta_b=alpha_b+1,    beta_c=alpha_c+1.

The cyclic version at I_2 also yields beta_a=alpha_a+1. Hence, with S=A+B+C,

    a=A+alpha_a S,
    b=B+alpha_b S,
    c=C+alpha_c S.                                      (10)

In particular Q_c=beta_c S, and its analogues Q_a and Q_b are nonzero multiples of S. Substituting into (6), (7), and their cyclic versions yields scalars p_0,...,p_5 such that

    U_(O_0)=B+p_0 S,    U_(O_3)=B+p_3 S,
    U_(O_1)=A+p_1 S,    U_(O_4)=A+p_4 S,
    U_(O_2)=C+p_2 S,    U_(O_5)=C+p_5 S.                (11)

This is the claimed pencil collapse. The three lines are distinct: for example det(A,B,S)=det(A,B,C) is nonzero. The vector S is nonzero because A,B,C are independent. No coordinate sum has been divided by, and S has not yet been assumed finite in the original affine chart. ∎

## 4. Convexity resolves the point at infinity and gives a contradiction

**Theorem.** No closed active component with the topology in Section 2 is cycle-balanced, in any admissible realization.

**Proof.** Suppose it were balanced. By Lemma 2 its three opposite outer-vertex diagonals

    O_0 O_3,    O_1 O_4,    O_2 O_5

meet at the projective point represented by S. The boundary hexagon is strictly convex. Each pair of these diagonals has alternating endpoints around its boundary, so its two segments intersect in their relative interiors. In particular their common point is a finite point P in the interior of K. Thus the possible projective-at-infinity case has been excluded geometrically, before taking affine coordinates for P.

Translate the original affine plane so P becomes the origin. This applies a linear homogeneous transformation to every U_v and preserves all relations above. Now S=(0,0,h)^T for a nonzero h. The first two coordinates of U_(O_0) and U_(O_3) in (11) are therefore the same vector b_0, namely the first two coordinates of B. This vector is nonzero: if it vanished, B and S would be proportional, contradicting the independence of A,B,C and S=A+B+C.

By the definition U_v=x_v(v_x,v_y,1)^T, after this translation we obtain

    x_(O_0)(O_0-P)=b_0=x_(O_3)(O_3-P).                  (12)

But P lies strictly between O_0 and O_3, so the nonzero vectors O_0-P and O_3-P point in opposite directions. Equation (12) forces x_(O_0) and x_(O_3) to have opposite signs. This contradicts the boundary positivity (3). ∎

The proof is independent of radial, affine-regular, or other symmetry conditions. It also does not assume that the signed-Ceva concurrence for the central triangle lies inside that triangle. The only concurrence point shown to be interior is forced by the opposite diagonals of the strictly convex outer hexagon.

## 5. Consequence for the complete eighteen-vertex family

Consider any admissible full disk having the 28 triangles from the second-pass construction, with six exterior vertices Q_i and the two additional outer triangles

    (O_i,Q_i,O_(i+1)), (O_i,Q_(i-1),Q_i),

together with the core triangles above. Coordinates may be arbitrary, provided this is a conforming disk with nondegenerate triangles. The only original degree-four interior mesh vertices are I_1,I_3,I_5; all O_i and I_0,I_2,I_4 have original degree six, and every Q_i is a boundary vertex.

Any closed active component needs three original nonsingular degree-four vertices. If one of I_1,I_3,I_5 is singular, there are too few. Otherwise a closed component must contain all three, together with their complete original neighbor sets

    {O_0,O_1,I_0,I_2},
    {O_2,O_3,I_2,I_4},
    {O_4,O_5,I_4,I_0}.

Their union with the three degree-four vertices is all twelve interior vertices. Therefore every possible closed component must be the full core already excluded by the theorem. All other active components have a forcing one-entry column. The reduced matrix R consequently has full row rank.

**Corollary.** Every admissible nonsymmetric realization of this eighteen-vertex, twenty-eight-triangle topology admits arbitrary quartic vertex first jets. This is a whole-topology result, not merely an excluded parameter subfamily.

It does not state that every coordinate assignment is admissible, or that the twelve rows always form a closed component. Those conditions need not hold; the argument excludes balance whenever closedness does hold.

## 6. Exact checks and remaining scope

The two four-star determinant factors, the two even-vertex factors (8)-(9), and the degeneracies used to justify division admit exact symbolic verification. The general pencil form (10)-(11) satisfies all 21 interior Ceva equations of the 16 core triangles and the three outer pencil incidences. [REPRODUCTION.md](REPRODUCTION.md) specifies these checks without dependence on a particular program. These algebraic identities corroborate the argument; the strict convexity and sign contradiction are the mathematical proof above.

The remaining target is a closed balanced core of a different topology, or a theorem excluding all such topologies. More degree-six interior vertices, different arrangements of degree-four vertices, higher even degrees, and legal straight boundary subdivisions are not settled here. In particular, the pencil-collapse lemma was proved for the displayed incidence pattern; it must not be applied to an arbitrary even triangulation without a further argument.
