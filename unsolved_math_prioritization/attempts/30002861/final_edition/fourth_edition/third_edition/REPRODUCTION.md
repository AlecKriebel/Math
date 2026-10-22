# Exact reproduction conventions for the third edition

The general theorems are proved in the authored manuscripts and their independent mathematical audits. The finite and symbolic checks below reconstruct their algebra, incidences, and explicit examples. A finite list of ring counts is not a proof for every count. A hash is not a mathematical certificate, and a floating rank or drawing is unnecessary.

## 1. Arithmetic and geometry

All integer and fraction strings in [THIRD_PASS_CERTIFICATES.json](THIRD_PASS_CERTIFICATES.json) denote exact rational numbers. A fraction p/q has integer numerator and positive nonzero denominator. Indices are zero-based. Every coordinate, determinant, polynomial coefficient, and inequality in the finite controls is evaluated exactly.

Use det(a,b)=a_x b_y-a_y b_x. A counterclockwise triangle (v,w,u) has positive doubled area det(w-v,u-v). A homogeneous determinant det(A,B,C) has the displayed vectors as columns. Cyclic rotations of a face preserve orientation; swapping two entries changes its sign. When an identity is verified only up to determinant-order sign, both sides must receive the same global nonzero sign. Never replace a relative minus sign by this convention.

A conforming realization has pairwise distinct vertices and nondegenerate triangles meeting only in their common listed simplices. Positive triangle areas alone do not certify those intersection or full-fan conditions.

## 2. The first ring and full disk incidences

For the twelve-vertex calculation number O_0,...,O_5 by 0,...,5 and I_0,...,I_5 by 6,...,11, with cyclic subscripts modulo six. Form twelve annulus faces

    (O_i,O_(i+1),I_(i+1)), (O_i,I_(i+1),I_i),

and four central faces

    (I_0,I_1,I_2), (I_2,I_3,I_4),
    (I_4,I_5,I_0), (I_0,I_2,I_4).

An undirected edge is its sorted endpoint pair. Enumerate all such pairs lexicographically and attach, for each incident face, its third vertex. This gives 27 edges, 21 with two opposite vertices and six boundary edges. The six O vertices each have induced degree four.

For the full topology number Q_0,...,Q_5 by 12,...,17 and add

    (O_i,Q_i,O_(i+1)), (O_i,Q_(i-1),Q_i).

The result has 18 vertices, 45 edges, and 28 faces, with boundary exactly the six Q vertices. Only I_1,I_3,I_5 are original interior degree-four vertices. Every other original interior vertex has degree six. The union of those three four-star centers and their neighbor sets is all twelve interior vertices. These are incidence facts independent of coordinate choices, subject to admissibility of the chosen geometric realization.

## 3. Normalized homogeneous balance and pencil elimination

Take the accepted face-normalized weights x_v from [second-pass theory](second_edition/SECOND_PASS_THEORY.md), rather than an independently rescaled set of vertex weights. Write V_v=(v_x,v_y,1)^T and U_v=x_v V_v. All weights of a putative closed balanced component are nonzero. For edge vw with opposite vertices u,z, define

    D_v=det(z-v,u-v), D_w=det(u-w,z-w).

Direct expansion gives

    det(U_v+U_w,U_u,U_z)
       =-x_u x_z (x_v D_v-x_w D_w).

No division by x_v+x_w is permitted or needed. A boundary equation uses its actual exterior opposite vertex, whose homogeneous representative may be scaled arbitrarily by a nonzero factor; no exterior dependency coordinate is being asserted.

Use A=U_(I_0), B=U_(I_2), C=U_(I_4) as basis. Their determinant is nonzero. In that basis take A=(1,0,0)^T, B=(0,1,0)^T, C=(0,0,1)^T; every computed determinant in original coordinates has the additional common factor det(A,B,C). Set

    c=alpha_c(A+B)+beta_c C,
    a=alpha_a(B+C)+beta_a A,
    b=alpha_b(C+A)+beta_b B.

The first star equations give

    U_(O_0)=k(A+c)+lB, U_(O_1)=m(B+c)+nA,
    beta_c m(k-l+1)=0, beta_c k(m-n+1)=0.

The required distinctness and triangle determinants rule out beta_c,k,m=0, giving l=k+1 and n=m+1. The triangle determinants also rule out k+1=m+1=0. The analogous I_5 star gives U_(O_5)=C+q(C+A+b), with q and q+1 nonzero. Reconstruct the opposite vertices from the face list before expanding the remaining two equations:

    det(A+U_(O_0),c,U_(O_5))
      =beta_c q(k+1)(alpha_b-beta_b+1),
    det(A+U_(O_5),U_(O_0),b)
      =beta_b k(q+1)(alpha_c-beta_c+1).

Their canceled factors must be justified individually, as in the proof. The cyclic counterpart forces beta_a=alpha_a+1. The resulting forms, with S=A+B+C, are

    a=A+alpha_a S, b=B+alpha_b S, c=C+alpha_c S,
    O_0,O_3: B+p_i S;
    O_1,O_4: A+p_i S;
    O_2,O_5: C+p_i S.

Substitute into all 21 raw interior-edge determinants. All vanish identically. This is a consistency check; the elimination, together with the justified nonzero factors, proves necessity. The base coefficient is exactly one in the already normalized weighted vectors. Merely lying on the same projective line does not imply the sign contradiction.

## 4. Boundary positivity and the finite concurrence

For a terminal boundary edge use affine coordinates

    v=(0,0), w=(h,0), Q=(r,-t), u=(p,q), h,t,q>0.

Here Q is the actual exterior opposite vertex and u the actual interior opposite vertex. There is no restriction that r or p lie between 0 and h. The supporting half-planes give

    D_v=tp+rq>=0,
    D_w=t(h-p)+(h-r)q>=0,
    D_v+D_w=h(t+q).

Activity makes both inequalities strict. The line Qu meets vw at horizontal coordinate D_v/(t+q), strictly between 0 and h. Hence x_w/x_v=D_v/D_w>0.

All six terminal vertices have induced degree four; the accepted support theorem makes them strict corners of a convex hexagon. This sign proof is not a claim for each subedge of an arbitrary subdivided straight side.

The opposite diagonals of the strictly convex terminal hexagon have alternating endpoints and intersect in their relative interiors. Their projective concurrence S is therefore finite and interior before division by any affine last coordinate. Translate it to P=0. The same-color weighted endpoints have the same nonzero planar numerator but oppositely directed geometric positions, so their weights have opposite signs. This contradicts boundary positivity. No numerical coordinate search is part of this argument.

## 5. Propagation through every ring

For a separate convenient labeling start with I_i=i for i=0,...,5 and ring j with vertices 6j+i, where j=1,...,n. The initial central faces are unchanged as cyclic triples. Between V_i on the old ring and W_i on the new ring use one orientation uniformly on that annulus:

    Forward: (W_i,W_(i+1),V_(i+1)), (W_i,V_(i+1),V_i).
    Reverse: (W_i,W_(i+1),V_i), (W_(i+1),V_(i+1),V_i).

Different annuli may choose independently. This does not allow independent diagonal flips within one annulus. The resulting counts are V=6(n+1), E=18n+9, T=12n+4. There are exactly six terminal boundary edges and all terminal induced degrees are four.

Give the initial I vertices colors A,C,B,A,C,B and extend by giving the vertex opposite an old edge its missing color. Every face has three colors, every ring is three-periodic, and opposite terminal vertices have the same color. Reversing i to -i preserves the central face set and exchanges the two first-annulus orientations.

For the local induction take S=A+B+C and known vectors A+aS, B+bS, C+cS. In the A,B,C basis verify

    det(A+aS,B+bS,C+cS)=1+a+b+c,
    det(A+aS+B+bS,C+cS,(u,v,w)^T)
      =(u-v)(1+a+b+c).

The first factor is nonzero by the actual old triangle's nondegeneracy. The new opposite vector is therefore Z=gamma C+pS. After all six line constraints are imposed, the next annulus equation is

    det(gamma C+pS+B+bS,A+aS,delta A+qS)
      =(gamma-1)(q-a delta).

The cross product of the two opposite vectors is (0,a delta-q,q-a delta). Distinct geometric vertices with nonzero weights force q-a delta nonzero; hence gamma=1. This includes delta=0 and rules out provisional gamma=0 by the same equation. No division by gamma, delta, or the last coordinate of S occurs.

Reconstruct the six old-edge constraints and twelve radial equations in each orientation. The same local argument applies at every added layer; this proves induction for arbitrary positive finite n. Checking all 62 orientation sequences for n=1,...,5 is an additional incidence regression, not an upper bound on the theorem. The complete-core theorem does not decide irregular proper components in larger full meshes.

## 6. Local cofactor and polynomial conventions

At a vertex v use the actual full counterclockwise even fan d_0,...,d_(m-1). For the finite examples, sort directions by exact polar order: the upper half-plane, including the positive horizontal ray, comes first; within a half-plane use the sign of the determinant. Ensure that the result winds once around v and that each consecutive determinant is positive. Set s_i=(-1)^i, a_i=det(d_i,d_(i+1)), and

    L_i(X)=det(d_i,X-v),
    rho_i=s_i det(d_(i-1),d_(i+1))/(a_(i-1)a_i),
    F_i=s_i L_i L_(i+1)/a_i.

Then F_i-F_(i-1)=rho_i L_i². Expanding polynomial coefficients verifies every jump without dividing by rho_i, so zero row entries are retained. Subtraction of x_v F_i from q_i gives the common p_v exactly when the stated cofactor span holds. Uniqueness is claimed only for a nonzero row.

Use J=[[0,-1],[1,0]], n_i=Jd_i and

    S_i=(n_i n_(i+1)^T+n_(i+1)n_i^T)/a_i.

Verify det S_i=-1, S_i d_i=-Jd_i, S_i d_(i+1)=Jd_(i+1), and the sum identity in the proof. These yield D²q_i=B_v+x_v s_i S_i and the stated edge-gradient formula. The determinant of S_i is not the determinant of D²q_i.

Polynomials in the certificate use monomial order (1,x,y,x²,xy,y²). Their Hessian is [[2c_xx,c_xy],[c_xy,2c_yy]]. Coefficients are in the global affine coordinates unless explicitly described as local about v. To compare two quadratics, compare all six exact coefficients. Expressions and rational coefficients describe mathematical objects, not a required implementation.

The four-star derivative example uses v=0 and the displayed B. Build p=(1/2)X^T B X and q_i=p+F_i. Compare all four rho values and all four values of partial_x q at d_i with the certificate. The derivative is continuous and affine on each triangle, so its strict negativity away from v follows from barycentric interpolation of the three vertex values. The triangle fan contains a neighborhood of v; no compact extension is claimed.

## 7. Exact compact patch geometry and continuity

Use vertex order A,B,C,a,b,c and the seven face triples in the certificate. Each face is counterclockwise. Verify doubled areas (5,3,5,3,5,3,1), sum of areas 25/2, and containment in the outer triangle ABC.

For each pair of triangles intersect their six closed left half-planes. One exact procedure enumerates intersections of every pair of nonparallel boundary lines, retains points satisfying all six nonnegative half-plane inequalities, and takes their convex hull. Each bounded polygonal intersection is determined by these vertices; keep the lower-dimensional cases of a point or segment. The result must equal the convex hull of the listed common vertices, or be empty if there are none. There are 21 pairs: three empty, nine common-vertex, and nine common-edge intersections. Boundary coverage and total area show that the nonoverlapping triangles fill ABC.

Reconstruct edges and vertex links. Exactly AB, AC, BC have one incident triangle; each other edge has two. Boundary links are connected paths, and interior links are connected four-cycles. This confirms a conforming disk, not merely a list of positive triangles.

Orient each edge from lower to higher vertex index. The face on its geometric left has positive determinant against its third vertex. Set the right or left exterior polynomial to zero if absent. Reconstruct the scalar a_e by comparing coefficients in

    q_left-q_right=a_e det(v_j-v_i,X-v_i)².

Compare all six coefficients, not values at a few sample points. The twelve a_e are listed in lexicographic edge order in the certificate and are all nonzero. Square divisibility proves equality of value and both first derivatives along every edge, including extension by zero across the outer boundary.

At each interior vertex use the polar-order neighbor list in the certificate and s_0=1. An outgoing cofactor equals a_e if the center has the lower index and -a_e otherwise. Divide one nonzero outgoing cofactor by its rho_i to obtain x_v; check all four coefficients and subtract x_v F_i from each incident polynomial. The four remainders must match the displayed common p_v, with scales 15/2,15/2,-15/2 in the specified orders. A different starting ray may change a local sign; it is not a new global dependency.

Compute the Hessian determinant in each face and multiply by its exact area. The sum is 3(3/2)(-12)+(1/2)(108)=0. The vanishing uses genuine cancellation, so a nonpositive-energy argument cannot be inferred from the bubble determinant alone. Finally solve A+t(A-C)=B+s(B-C): t=s=-1, contrary to the required t,s>0. This is why the compact patch is not a closed quartic active support.

## 8. Corrected segment statement and assembly

For the derivative four-star evaluate q-p at (-t,0), using the triangle with rays d_1,d_2, for 0<t<1. The exact result is 5t²/14. Its incident positive horizontal ray has zero q-p, so whole-line agreement of the piecewise function fails.

For the eight-ray control use the certificate directions, p=0, x_v=1, and q_i=F_i. Verify positive consecutive areas and the full polar order. Both rays of x=0, y=0 and y=x are incident, so q vanishes on the portions of those three lines inside the fan. Nevertheless (-2t,t), for 0<t<1/2, lies in the triangle with rays (-1,1),(-1,0), and q=t². It lies on the supporting line of the incident ray (2,-1), disproving the old full-line conclusion.

The corrected proof uses only incident nondegenerate segments. Three distinct supporting lines force the homogeneous quadratic p_v to vanish because the determinant of their quadratic evaluation rows is det(u,v)det(u,w)det(v,w), which is nonzero. This gives zero on all incident segments, not on arbitrary opposite rays. The macro-patch conclusion then uses the two adjacent micro-vertex values, both 3 times their incident patch amplitude, and requires an actual full even fan with the quartic proportionality imposed.

## 9. Evidence limits

The audits' finite checks corroborate exact algebra and incidence. Strict convexity, the geometric significance of canceled factors, arbitrary-n induction, all-fan equivalence, and the restricted universal assembly conclusion are proved arguments. The compact example and local controls do not produce an admissible quartic obstruction. No unaudited nonconvex seed is used. The full eighteen-vertex component theorem must not be transferred to arbitrary larger full triangulations without a separate proper-component argument.
