# Local barriers and controlled gluing for 5/6 triangulations

Problem 30000433 / OWR-1194-002. Authored research note, 6 October 2026 UTC.
Status: partial, universal questions unresolved. Four substantive approaches.
This is an AI-assisted, unrefereed mathematical note. No priority claim is made.

## 1. Source and category

John M. Sullivan's Problem 5, printed p. 693 of *Discrete Differential Geometry*, Oberwolfach Report 12/2006, asks whether all three-manifolds admit edge degrees exclusively 5 and 6, and whether the additional TCP triangle restriction can always be imposed. TCP means that a triangle has at most one degree-6 edge. The original question does not explicitly say “closed,” “orientable,” or “simplicial complex.” The later Lutz–Sulanke–Sullivan report treats the closed case. We retain the original question without pretending its category ambiguities have been settled.

All results and certificates below concern finite abstract simplicial complexes triangulating closed PL 3-manifolds, except where a ball is explicitly specified. There are no repeated vertices in a simplex, loops, multiple edges, face-pairing tetrahedra, ideal vertices, or boundary in the closed examples. Degrees count tetrahedra incident with an edge. The elementary arguments do not require orientability; the implemented closed examples are additionally checked to be orientable. No extension to generalized triangulations, noncompact manifolds, or arbitrary boundary conditions is asserted.

Brady–McCammond–Meier's Theorem 1.2 proves the 4/5/6 bound for closed orientable 3-manifolds, not the requested 5/6 bound. Their source constructions use quotients and require separate care if strict simplicial output is desired. We do not use their theorem as a certificate for any of our complexes. Elder–McCammond–Meier's published 5/6* theorem restricts degree-5 edges, rather than degree-6 edges. It is a conditional hyperbolicity result, not a universal existence theorem. Indeed TCP and 5/6* cannot hold simultaneously in a nonempty 5/6 triangulation: a triangle would need at most one edge of each of two degrees, despite having three edges.

Primary sources are listed in SOURCE_AUDIT.md and SOURCE_METADATA.json. A current search located no full resolution, which is a bounded search result and not a proof of historical openness.

## 2. Approach 1: local curvature and TCP restrictions

Let L be the link of a vertex v in a closed simplicial 3-manifold K with every edge degree 5 or 6. L is a triangulated 2-sphere. Write n_i for its number of degree-i vertices. These are precisely the edges incident with v that have degree i in K. With N, E, F the face counts of L, the equations 3F=2E and N-E+F=2 give

    sum_w (6-deg_L(w)) = 12.

Therefore n_5=12. In particular, the degree-5 edges of K form a spanning 12-regular simple graph. Every such K has at least 13 vertices. Double counting their endpoints yields E_5=6V. For a closed 3-manifold, F=2T and Euler characteristic is zero, so E=V+T. Consequently

    T=5V+E_6.

These are necessary identities, not sufficient existence conditions.

For TCP, the degree-6 vertices of L form an independent set: two adjacent ones would correspond to two degree-6 edges in a triangle through v. Put q=n_6. Each degree-6 vertex has six degree-5 neighbors. Around any degree-5 vertex, its five neighbors form a cycle. No two degree-6 neighbors can be consecutive, so at most two of these neighbors have degree 6. Counting 5–6 edges in L in both directions gives

    6q <= 2 n_5 = 24, hence q <= 4.

Thus the degree-6 subgraph of a TCP triangulation has maximum degree four, every vertex of K has graph degree between 12 and 16, E_6<=2V, and 5V<=T<=7V. This proof does not claim that every q in {0,1,2,3,4} occurs. In particular it is not an exhaustive classification of possible links. The classical Frank–Kasper local models already motivate bounds of this kind; novelty is not claimed.

The approach supplies useful local constraints but no contradiction for an arbitrary manifold and no way to assemble compatible spherical links globally.

## 3. Approach 2: ordinary subdivision and Pachner barriers

**Proposition.** Any positive-dimensional stellar subdivision of a closed simplicial 3-manifold introduces an edge of degree at most four. Therefore a nonempty finite sequence consisting only of such subdivisions can never end with all edge degrees at least five.

**Proof.** Let x be the new vertex.

* Subdivide a tetrahedron abcd. Each edge xa has degree three.
* Subdivide a triangle abc. It has exactly two incident tetrahedra, say abcd and abce. Each edge xa, xb, xc lies in exactly four new tetrahedra.
* Subdivide an edge ab. Its link is a cycle C_d. The star is ab*C_d. For each cycle vertex w, exactly two edges of C_d contain w. Each old tetrahedron abww' becomes axww' and xbww'. Hence xw lies in four tetrahedra. The two axial edges ax and xb retain degree d.

There are no other positive-dimensional faces. For a finite sequence, apply the argument to its final move. Later vertex renamings do not change the degrees. QED.

This is a barrier to pure stellar subdivision, not a statement that every subdivision is obstructed. General replacements, stellar welds, and mixed move sequences lie outside the proposition.

A related observation is that every closed simplicial triangulation with all edge degrees at least four is isolated in the induced graph of ordinary three-dimensional Pachner moves that maintain that same lower bound at every step. A 1–4 move introduces degree-three edges; a 2–3 move introduces a degree-three edge. A 3–2 move needs a degree-three edge, and a 4–1 move needs a tetrahedral vertex link, hence incident degree-three edges. None is allowed in this induced graph. This does not obstruct paths that temporarily leave the degree-restricted class or use compound moves.

The exact controls test edge stellar subdivisions for cycle lengths 3 through 20, face and tetrahedron subdivisions, and a 2–3 move. These bounded tests supplement, rather than replace, the preceding universal proofs.

## 4. Approach 3: a minimum size for an octahedral replacement

**Proposition.** Let B be a finite simplicial 3-ball whose boundary is the unsubdivided octahedral sphere on six vertices. If every interior edge of B has degree at least five, then B has at least seven interior vertices.

**Proof.** If B has an interior vertex x, its link is a simplicial 2-sphere. Every edge from x is an interior edge, so every vertex of this link has degree at least five. If its link has n vertices, then 5n<=2(3n-6), and hence n>=12. B therefore has at least 13 vertices in total and at least seven interior vertices.

It remains to exclude the possibility of no interior vertices. The octahedral boundary graph is K_{2,2,2}; it has no four-vertex clique. Any tetrahedron of B must therefore contain an edge joining one of the three pairs of opposite boundary vertices. This edge is an interior edge. Its link is a cycle with vertices among the four remaining vertices of B, so it has degree at most four, a contradiction. QED.

A degree-four edge has an octahedral star boundary, so this lower bound applies to any attempt to replace that star by a ball without subdividing its boundary while demanding degree at least five at every new interior edge. It permits all larger replacements and all boundary refinements. It gives no guarantee that a seven-vertex interior gadget exists, no upper bound, and no solution to compatibility with the surrounding boundary-edge degrees.

## 5. Approach 4: controlled connected sums and a self-handle

### 5.1 Conditional vertex-star gluing lemma

Let K_1 and K_2 be disjoint closed simplicial 3-manifolds with only degrees 5 and 6. Select vertices v_i with isomorphic links L_i. Remove the open stars, and glue the resulting boundaries by a specified simplicial isomorphism. Require that in each punctured complex the link boundary is induced on its vertex set: every remaining simplex whose vertices lie in that set already belongs to the boundary. This sufficient condition avoids unintended simplex identifications. For oriented connected sums choose an orientation-reversing boundary map, or equivalently choose compatible opposite orientations on the two summands.

For a seam edge e, let d_i(e) be its degree before puncturing. Exactly two tetrahedra of its original star contain e, one for each of the two triangles of L_i containing e. Therefore its degree after gluing is

    d_new(e)=d_1(e)+d_2(e)-4.

Every nonseam surviving edge retains its degree. Thus this construction stays in the 5/6 class exactly when both old seam degrees are five for every seam edge; the resulting seam edges then have degree six. The topological result is the connected sum, because open vertex stars are embedded PL balls. Every seam triangle has three degree-six edges, so the construction necessarily fails TCP. The lemma is conditional: it does not assert the existence of a suitable vertex or matching link in a general manifold.

By contrast, removing only one tetrahedron from each summand produces seam degrees d_1+d_2-2>=8. The most direct facet connected sum fails even the weak 5/6 requirement.

### 5.2 Exact convex 600-cell certificate

We reconstruct a classical 600-cell boundary using scaled coordinates in the real quadratic field Q(phi), where phi=(1+sqrt(5))/2:

* all permutations of (+/-2,0,0,0), giving eight vertices;
* all sixteen sign choices of (1,1,1,1);
* all even permutations of (0,+/-1,+/-phi,+/-(phi-1)), giving 96 vertices.

Represent a+b phi by its integer pair (a,b). Join two vertices precisely when their dot product is 2 phi, and take every four-clique as a tetrahedron. The code derives 120 vertices and 600 tetrahedra without importing an external facet list.

For each tetrahedron, let s be the sum of its four vertex vectors. Each of its vertices satisfies s dot x=4+6 phi. Every other listed vertex satisfies the strict inequality s dot x<4+6 phi, checked exactly. There are 72,000 such supporting-halfspace comparisons, of which 69,600 are strict. The Gram matrix of the four tetrahedron vectors has diagonal 4 and off-diagonal 2 phi. Its eigenvalues are 4+6 phi and 4-2 phi, the latter three times, all positive. The four vertices are thus linearly, and therefore affinely, independent and form a genuine facet of the convex hull.

The hull is full-dimensional and contains the origin in its interior since it contains all eight coordinate-axis vertices. The selected facets form a closed connected simplicial pseudomanifold: the program checks that every triangular ridge has exactly two incident selected tetrahedra and that their adjacency graph is connected. A convex polytope has exactly two facets at each ridge and a connected facet-adjacency graph. Consequently this collection, already closed under adjacency across every ridge, is the whole boundary of the convex hull. It is therefore a PL 3-sphere, not merely a homology sphere inferred from local checks.

Additional independent-from-the-geometry combinatorial checks establish spherical vertex links (connected closed surfaces with Euler characteristic two and cyclic links at their vertices), cyclic edge links, coherent tetrahedron orientations, and edge degree five. The resulting f-vector is (120,720,1200,600).

### 5.3 A doubled puncture

Take two copies, delete the open star of coordinate vertex index zero, and identify their link boundaries by equal vertex labels. The induced-boundary check in the gluing lemma is verified explicitly. Assign opposite ambient orientations to make this the oriented connected sum S^3#S^3, hence S^3.

The f-vector is (226,1386,2320,1160). There are 1,356 degree-five edges and 30 degree-six seam edges. Each of the 12 seam vertices has twelve degree-five and five degree-six incident edges; the other 214 vertices have twelve degree-five and zero degree-six edges. Exactly 20 triangles violate TCP, precisely the icosahedral seam. This is a concrete control showing why the surgery lemma does not answer the stronger question.

### 5.4 A self-handle producing S^2 times S^1

In a single copy remove the open stars of the antipodal vertices (-2,0,0,0) and (2,0,0,0). The program verifies that their boundary vertex sets are disjoint and no remaining simplex meets both sets. Identify the two boundaries using the symmetry

    (x0,x1,x2,x3) -> (-x0,x1,-x2,-x3).

It permutes the full vertex set, exchanges the poles, and gives a simplicial boundary isomorphism. Its determinant is -1; its restriction to the oriented hull boundary is orientation reversing. It therefore reverses the induced orientations on the two puncture boundaries, yielding an orientable self-handle. The PL 3-sphere with two disjoint open balls removed is S^2 times an interval; identifying its ends in the orientable way gives S^2 times S^1. Equivalently, this follows from the standard classification of S^2 bundles over S^1 (an orientation-preserving sphere monodromy is isotopic to the identity). This topological fact is an explicit standard input, not something the finite checker proves.

The resulting simplicial complex has f-vector (106,666,1120,560), with 636 degree-five and 30 degree-six edges. It is independently checked to be a closed orientable combinatorial 3-manifold; 20 triangles violate TCP. S^2 times S^1 was already in the prior TCP existence families. This is a reproducible surgery control, not a new topological existence result.

## 6. Precise remaining gap and claim limits

The four approaches do not remove degree-four edges from arbitrary manifolds, construct the necessary globally compatible TCP links, or exhibit a manifold that cannot admit the desired triangulation. Stellar and small-octahedral obstructions concern particular construction methods, not the universal problem. The gluing lemma requires clean matching boundaries that have not been produced for arbitrary summands. The explicit examples have previously known manifold types and fail the stronger condition after gluing.

The retained outcome is therefore PARTIAL / UNSOLVED, four of at most five substantive approaches. There is no claimed full resolution, no claimed novel classification, no formal proof-assistant certification, and no human peer review. Finite exact controls and mutation tests are engineering evidence for the explicit certificates and calculations, not a universal mathematical proof.
