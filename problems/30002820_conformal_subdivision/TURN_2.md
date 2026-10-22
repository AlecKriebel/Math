# Turn 2: no proper fixed affine face refinement preserves all conformal classes

Problem 30002820. Second substantive author turn. **Original unresolved, 2/5.** This rules out a broad precise class of isometric schemes: fixed subdivisions in barycentric coordinates of the old faces. It allows arbitrary fixed rational or real insertion positions and arbitrary finite subdivision patterns. It does not cover metric-dependent positions or non-isometric subdivision rules.

## 1. The fixed-affine class and theorem

Fix a finite simplicial subdivision T′ of a triangulated surface T. In each old reference triangle, every new vertex has fixed barycentric coordinates, independent of the input edge-length metric. The face patterns agree on shared edges. For each valid Euclidean input metric, realize these points affinely in every old triangle and assign the actual Euclidean lengths to all refined edges. This is an induced isometric metric on the proper geometric subdivision. The refinement is called proper here when at least one old triangle is split into more than one triangle.

**Theorem.** No proper scheme in this fixed-affine class preserves discrete conformal equivalence for all input metrics. More strongly, at every nondegenerate input metric on a fixed finite triangulated surface, there are arbitrarily small valid vertex rescalings for which the refined metrics are not discretely conformally equivalent.

In particular this excludes every proper barycentric-coordinate pattern, including standard barycentric subdivision, midpoint refinement, fixed interior stellar centers, and fixed-fraction edge insertions with straight triangulation. It does not exclude insertion positions which depend on the metric.

## 2. A local two-triangle invariant

Consider two nondegenerate adjacent triangles with common edge ab and opposite vertices c,d in a single old reference face. Their four vertices are distinct. Write their reference-plane positions as a,b,c,d∈R², retaining these letters for points. Under a Euclidean affine realization with positive-definite Gram matrix G, every squared edge length is

    L_xy(G)=(x−y)^T G(x−y).                                 (1)

This is a nonzero linear polynomial in the three independent entries G_11,G_12,G_22. The squared length-cross-ratio

    R(G) = L_ac(G)L_bd(G) / [L_bc(G)L_ad(G)]                 (2)

is invariant under any refined vertex scaling. This follows from direct cancellation of the four endpoint factors, independent of orientation or any cross-ratio characterization theorem.

**Lemma.** R(G) is not constant on any nonempty open subset of the cone of positive-definite 2×2 matrices.

### Proof

If R were constant C>0 on such an open set, the polynomial

    L_ac L_bd − C L_bc L_ad

would vanish on a nonempty real open set and hence identically. Nonzero linear polynomials are irreducible in R[G_11,G_12,G_22]. Unique factorization would pair the two numerator factors with the two denominator factors, up to nonzero scalars.

For nonzero reference vectors v,w, the forms v^T Gv and w^T Gw are proportional exactly when v and w are parallel. Indeed equality up to a scalar for every symmetric G says vv^T is proportional to ww^T; their one-dimensional images are then equal. The converse is immediate. The proportionality scalar is positive by evaluating at the identity matrix.

There are only two possible factor pairings. Pairing ac with bc makes a,b,c collinear, contradicting the first triangle's nondegeneracy. The other pairing requires ac parallel ad and bd parallel bc. Since c≠d, the first parallelism puts a on the line cd and the second puts b on that same line. Again a,b,c are collinear. Both possibilities contradict nondegeneracy. This proves the lemma, including possible repeated factors; unique factorization still gives one of those two pairings.

The lemma does not require the union quadrilateral to be convex. It only uses nondegenerate adjacent triangles with distinct opposite vertices.

## 3. A proper face subdivision supplies the obstruction

Any finite proper triangulation of a nondegenerate triangle has an interior edge with two incident triangles. One elementary reason is that the dual adjacency graph of its triangles is connected: a generic path between face-interior points crosses edges rather than vertices. With more than one triangle this graph has an edge, corresponding to an edge in the interior of the old face. Both incident triangles are nondegenerate in the reference realization.

Apply the lemma to that edge. As the old triangle shape varies through all Euclidean triangles, its Gram matrix varies through the full positive-definite cone. Its refined length-cross-ratio therefore cannot remain constant. Yet any two metrics on a single original triangle are discretely conformally equivalent, as the three endpoint-scaling equations always have a unique solution. Thus already on the triangle domain this fixed scheme fails to preserve the relation for all pairs.

## 4. Arbitrarily small conformal perturbations on any finite surface

The stronger statement does not require that the surface consist of one triangle. Choose an old face ijk in which the subdivision is proper and fix any valid input metric. Vary the three vertex parameters u_i,u_j,u_k near zero, leaving every other old-vertex parameter zero. On that face the logarithmic squared edge-length changes are

    (u_i+u_j, u_j+u_k, u_k+u_i).

This linear map R³→R³ is invertible, with determinant2 up to sign. Hence these vertex rescalings let the three local edge lengths vary through an open neighborhood. Passing between squared side lengths and the Gram entries is an invertible linear change: with reference vertices(0,0),(1,0),(0,1), the squared side lengths are G_11,G_22,G_11+G_22−2G_12.

Because the whole triangulation is finite and all input faces satisfy strict triangle inequalities, every sufficiently small choice of the three parameters leaves every old face valid, including adjacent faces outside the chosen one. The refined realizations remain valid because an invertible affine map preserves the fixed reference subdivision.

If all sufficiently small such conformal perturbations preserved refined conformal equivalence, ratio (2) would be constant on a Gram-matrix neighborhood. The lemma excludes this. Every neighborhood of the input therefore contains a valid conformally equivalent input with a different refined invariant. This proves the theorem on closed surfaces as well as surfaces with boundary. No global planar embedding is assumed.

## 5. Scope, dependencies and what remains

This is a nonexistence theorem for **metric-independent barycentric positions with the induced metric**, not for every map allowed by the source's broad wording. Standard smooth subdivision schemes which move old vertices or change the intrinsic metric are outside the stated class; so are metric-dependent refinement positions. A proof that one invariant varies does not establish nonexistence beyond these hypotheses.

The argument is elementary: squared lengths are linear in a Gram matrix, and factorization prevents a conformal cross-ratio from being affine-shape invariant. The input equivalence and length-cross-ratio framework are credited to Luo and Bobenko–Pinkall–Springborn, https://arxiv.org/abs/1005.2698 , Sections 2.1–2.3. Bauer's exact problem is https://ems.press/content/serial-article-files/46561 , printed 721–722. Source-formulation uncertainty remains as in SOURCE_GATE.md. No historical novelty claim is made.

The exact checker avoids logarithms and tests coefficient-factor pairings for a grid of rational adjacent triangles and constructs explicit changing Gram matrices for several proper face patterns. It does not use a finite scan to prove the universal lemma or general nonexistence statement.

Subjective completion estimate toward the intended unrestricted subdivision question: 10%. Author turns completed: 2/5. The next route is metric-dependent placement, where this fixed-affine obstruction no longer applies.
