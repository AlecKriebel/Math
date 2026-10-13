# Independent acceptance of the nonsymmetric hexagonal-ring exclusion

## Decision and scope

**Accepted without a substantive mathematical correction.** The proof excludes every closed balanced realization of the specified twelve-vertex hexagonal-ring core. It consequently proves arbitrary quartic vertex-first-jet interpolation on every admissible eighteen-vertex, twenty-eight-triangle realization of the stated full topology, with no symmetry assumption and no convexity assumption on the inner hexagon.

The mathematical proof is reproduced in [THIRD_PASS_CEVA_OBSTRUCTION.md](THIRD_PASS_CEVA_OBSTRUCTION.md), with the inherited distinctness hypothesis explicitly repeated in Lemma 2. This is an audit of one branch of the already documented third substantive pass for row 1761 / problem 30002861 / OWR-13678-002, not another counted pass.

The fixed model is a finite conforming straight-line triangulation of a polygonal disk with nondegenerate original triangles. Vertices of that realization are distinct. Prescribed scalar values and both first derivatives are arbitrary at every original vertex, including boundary vertices. Interpolants are globally C1 and of total degree at most four on each original triangle. There is no refinement, moved vertex, extra smoothness, or boundary condition.

The mathematical dependencies are explicitly the accepted first-pass reduction and convex induced-support theorem, the accepted second-pass face-normalized balance equation, and the accepted exterior-attachment classification, all linked in [DEPENDENCIES.md](DEPENDENCIES.md). This audit independently checks their use here; it does not replace those earlier proofs. No additional literature claim is involved.

The result is specific to this topology. It is neither a universal quartic interpolation theorem nor a quartic counterexample. Separate additive extensions require their own scope and audit.

## 1. The homogeneous balance equation has no missing affine exception

For two incident triangles with edge endpoints v,w and opposite vertices u,z, put V_y=(y_x,y_y,1)^T and U_y=x_y V_y. With D_v=det(z-v,u-v) and D_w=det(u-w,z-w), direct expansion gives

    det(U_v+U_w,U_u,U_z) = -x_u x_z (x_v D_v-x_w D_w).

All weights in the interior-core calculation are nonzero. Thus the two balance formulations are equivalent, including when x_v+x_w=0. No affine division by that sum is made. Distinct v,w also prevent U_v+U_w=0: such a vector equality would make their homogeneous points equal.

For a boundary edge, the geometric determinant equation still uses its actual exterior opposite vertex. One may scale that exterior homogeneous vector by any nonzero scalar; this does not require an exterior dependency coordinate. The boundary sign argument in the reviewed manuscript directly uses D_v/D_w and therefore makes no such artificial extension of the dependency.

## 2. Independent reconstruction of the forced pencil

I rebuilt all sixteen core faces, the twenty-seven edges, and their opposite-vertex incidences before computing any edge equation. The exact reconstruction confirms twenty-one interior edges. It does not import the authoring verifier or its result files.

The weighted central vertices A=U_(I_0), B=U_(I_2), C=U_(I_4) are independent. Across the three central edges, the raw determinant equations force

    c=alpha_c(A+B)+beta_c C,
    a=alpha_a(B+C)+beta_a A,
    b=alpha_b(C+A)+beta_b B.

Here c,a,b represent I_1,I_3,I_5. Each beta is nonzero because otherwise its central ear triangle is degenerate. Each alpha is nonzero because otherwise two distinct mesh vertices would have the same homogeneous point: respectively I_1=I_4, I_3=I_0, or I_5=I_2.

For the I_1 star, independently solving the raw linear equations across I_0 I_1 and I_2 I_1 gives

    U_(O_0)=k(A+c)+l B,
    U_(O_1)=m(B+c)+n A.

The other two raw edge equations give factors beta_c m(k-l+1) and beta_c k(m-n+1), with harmless determinant-order signs when opposite vertices are enumerated in a different order. The factors k,m are nonzero: their vanishing would identify O_0 with I_2 or O_1 with I_0. Therefore

    l=k+1, n=m+1,
    U_(O_0)=B+k(A+B+c),
    U_(O_1)=A+m(A+B+c).

The factors k+1,m+1 also cannot vanish. In the basis A,B,C, the required annulus triangle determinants are, up to orientation, beta_c(k+1) and beta_c(m+1). Their zeros are genuine forbidden triangle degeneracies, not excluded generic parameter cases.

Applying the same derivation at I_5 gives U_(O_5)=C+q(C+A+b), where q is nonzero by distinctness of O_5,I_4 and q+1 is nonzero by the annulus triangle determinant beta_b(q+1).

The independently reconstructed equations on I_0 O_0 and I_0 O_5 are precisely

    beta_c q(k+1)(alpha_b-beta_b+1)=0,
    beta_b k(q+1)(alpha_c-beta_c+1)=0.

Every canceled factor has now been accounted for. They force beta_b=alpha_b+1 and beta_c=alpha_c+1. The reconstructed cyclic equation at I_2 has factor beta_c r(m+1)(alpha_a-beta_a+1), where r is the analogous nonzero outer coefficient, so it forces beta_a=alpha_a+1. There is no unexamined exceptional zero factor.

Consequently S=A+B+C is nonzero and

    a=A+alpha_a S, b=B+alpha_b S, c=C+alpha_c S.

All outer weighted vectors have base coefficient exactly one on their respective color lines:

    O_0,O_3: B+pS;
    O_1,O_4: A+pS;
    O_2,O_5: C+pS.

The coefficient-one statement matters: mere collinearity would not by itself supply the subsequent weight-sign contradiction. It follows from the four-star normalization above, and has not been imposed by independent rescaling of already normalized vertex weights.

The three projective lines are distinct because det(A,B,S), det(B,C,S), and det(C,A,S) all equal the nonzero determinant det(A,B,C). S cannot be proportional to any of A,B,C for the same independence reason.

As an independent consistency check, every one of the twenty-one edge equations vanishes identically for this general pencil parameterization. Its conceptual explanation is the three-coloring of the core: the two vertices opposite any interior edge have one color, while the endpoints have the other two. The sum of the endpoint vectors belongs to the missing color's plane spanned by its base vector and S. This check is a sufficiency identity; necessity is supplied by the elimination and nondegeneracy arguments, not inferred from that identity alone.

### Hypothesis precision

Lemma 2 is correct within the manuscript's globally fixed conforming-realization model. Its standalone wording mentions nondegenerate triangle triples without repeating distinctness of all twelve vertices. Distinctness is used at the alpha=0 and k=0 exclusions. The third-edition proof includes the optional one-sentence clarification making that inherited assumption locally explicit. It changes neither the model nor the result. The theorem is not accepted as a claim about abstract homogeneous assignments allowing coincident nonadjacent vertices.

## 3. Boundary positivity uses actual exterior triangles

The support theorem makes the core boundary convex. Its six induced boundary degrees are four, so each boundary vertex is a strict corner. In particular there are no straight subdivisions on any of its six sides.

For a boundary edge vw, the exterior-attachment theorem applies to its actual original exterior triangle. Its opposite vertex Q lies on the outward continuations of the preceding side at v and the following side at w. Those two supporting lines bound a wedge containing the whole convex support. The interior opposite vertex u lies in that wedge and on the other side of vw from Q.

An independent affine calculation makes the sign reasoning explicit. Set

    v=(0,0), w=(h,0), Q=(r,-t), u=(p,q),
    h,t,q>0,

with no restriction on the real horizontal coordinates r,p. The two inward supporting half-planes yield

    D_v=tp+rq >= 0,
    D_w=t(h-p)+(h-r)q >= 0.

Closed activity excludes zero at either endpoint, hence both are strictly positive. The transverse line Qu meets vw at affine coordinate D_v/(t+q); the identity

    D_v+D_w=h(t+q)

places that intersection strictly between 0 and h. This independently verifies both strict convexity of the two-triangle quadrilateral and x_w/x_v=D_v/D_w>0. The argument does not require Q to project between v and w, and does not replace Q by a chosen auxiliary intersection unrelated to the mesh.

Positivity propagates around all six boundary edges. This is not a claim about every subedge of an arbitrary straight subdivided boundary side; such a claim is unnecessary here and remains excluded from the accepted scope.

## 4. The concurrence is finite and interior before any affine normalization

The forced outer color lines are the lines of O_0 O_3, O_1 O_4, and O_2 O_5. Strict convexity puts the endpoints of any two of these diagonals in alternating boundary order. Their segments therefore intersect in both relative interiors. The projective concurrence S is exactly that intersection, so it is a finite point P in the interior of the support.

This order of argument excludes the point at infinity geometrically; finiteness is not assumed through division by the last coordinate of S. It also does not say that the original central-triangle Ceva concurrence lies inside that triangle.

Translate P to the affine origin. Then S=(0,0,h)^T with h nonzero. The first two coordinates of both U_(O_0) and U_(O_3) equal the same vector b_0, those of B. This b_0 is nonzero, since otherwise B would be proportional to S. Thus

    x_(O_0)(O_0-P) = b_0 = x_(O_3)(O_3-P).

P is strictly between O_0 and O_3. The two geometric displacement vectors point in opposite directions, forcing their nonzero weights to have opposite signs. This directly contradicts the established same sign of all boundary weights. Neither the sign of h nor the signs of the inner weights enter this contradiction.

## 5. All proper closed components and singular four-stars are covered

The full eighteen-vertex face list independently reconstructs forty-five edges and twenty-eight triangles. Its only boundary cycle consists of the six Q vertices. The only original interior vertices of degree four are I_1,I_3,I_5; the other nine interior vertices have original degree six.

The accepted support theorem requires at least three original nonsingular degree-four interior vertices in every closed component. If any one of the three candidate stars is singular, that count is impossible. Singular rows cannot secretly produce another component because those are precisely the rows discarded by the accepted reduction.

Otherwise any closed component must contain all three four-stars. Convex support rules out their two-opposite-zero line-star case, so each retains every one of its four original neighbors. The three complete neighbor sets, together with their centers, cover exactly all twelve original interior vertices. Thus there is no proper closed component to escape the full-core obstruction.

Components that are not closed have an incident one-entry column, which forces a left-null coordinate to zero and propagates zero throughout the connected active component. The remaining possibility, a full closed balanced core, has already been excluded. Hence the reduced matrix has full row rank and the accepted interpolation reduction proves arbitrary quartic first-jet interpolation on every admissible realization of this complete topology.

This final component argument uses the precise eighteen-vertex topology. It must not be transferred without proof to a larger mesh containing this core.

## 6. Reproducibility and limits

The independent exact calculation reconstructs both face lists and opposite-vertex incidences, derives the relevant linear constraints and determinant factors, verifies every excluded algebraic factor, checks all twenty-one pencil edge identities and three outer incidences, and establishes the exact homogeneous normalization and affine boundary identities. The mathematical conventions are stated in [REPRODUCTION.md](REPRODUCTION.md).

Negative controls distinguish a wrong four-star elimination sign, a wrong even-star constant, a wrong propagation sign, unequal same-color base normalization, an incorrect opposite color line, and a wrong exterior-side sign.

These checks corroborate algebra and combinatorics. The geometric implications, strict inequalities, and completeness of the component argument are the proofs above, not consequences of finite symbolic testing. No claim about another topology, worldwide openness, or historical novelty is accepted here.
