# Parallel equal-area triangular faces do not determine a polyhedral surface

**7000013 / Ghomi Problem 2.4. Complete counterexample candidate in the standard triangulated-polyhedral-surface category, author turn 1; independent review pending.** No historical novelty is claimed. Coplanar adjacent triangles are essential to this example and are explicitly permitted in the category used here. A stricter version requiring every listed face to be a maximal planar facet, or forbidding flat subdivision edges, is not declared settled.

## 1. Source and category boundary

The primary statement is [Ghomi, Open Problems in Geometry of Curves and Surfaces, revised September 2, 2019, p.10, Problem 2.4](https://people.math.gatech.edu/~ghomi/Papers/op.pdf). It follows the smooth nonconvex Minkowski question and asks about parallel equal-area faces of polyhedral surfaces. It does not impose convexity, distinct adjacent face planes, genericity, or maximality of every face. The source also does not supply a formal definition of polyhedral surface there.

We use the usual PL interpretation: a finite triangulated closed surface embedded in R³, each two-simplex realized as a nondegenerate planar triangle. Adjacent triangles may be coplanar. This is consistent with the primary definition in [V. Alexandrov (2002), Section 3.1](https://arxiv.org/abs/math/0211286), which calls images of two-cells faces and requires each cell image to be a convex polytope, without a noncoplanarity condition. That separate definition does not prove what unstated restriction Ghomi may have intended. Our category and its limitation must remain visible.

The example below is connected, embedded, orientable, and homeomorphic to a sphere. It has an incidence-preserving simplicial correspondence, and corresponding oriented face-area vectors are exactly equal. Thus it does not rely on disconnectedness, self-intersection, reversing selected normals, an arbitrary permutation of faces, or faces with holes. All its specified faces are ordinary nondegenerate triangles.

## 2. The two solids

Let

D=[−10,10]×[−8,8], B=[−1/2,1/2]², and B'=B+(1,0).

Define the closed solids

K=(D×[0,1]) ∪ (B×[1,3]),
K'=(D×[0,1]) ∪ (B'×[1,3]).

They are boxes with a unit-square raised box of height two on top. Their boundaries P and P' are embedded PL two-spheres. We next supply compatible finite triangulations with equal oriented area vectors face by face. Merely declaring the top annulus a face would not meet our triangular-face convention, so that shortcut is not used.

## 3. A compactly supported area-preserving PL map

For a real number t define

h(t)=max(0,min(1,2−|t|)),
v(t)=4 max(0,min(1,5−|t|)).

The planar shears H(x,y)=(x+h(y),y) and V(x,y)=(x,y+v(x)) are piecewise-affine homeomorphisms. Their inverses subtract the same function, and each affine piece has determinant one. Set

F=H ∘ V ∘ H⁻¹ ∘ V⁻¹.

This is a piecewise-affine, orientation- and area-preserving homeomorphism of the plane, with finitely many affine pieces.

It is the identity when x≥6 or x≤−6. Indeed v(x)=0, and after subtracting h(y)∈[0,1], the x-coordinate still lies outside the open interval (−5,5); the two vertical shears vanish and the horizontal shears cancel. It is also the identity when y≥6 or y≤−2: after the first vertical subtraction, both relevant arguments of h lie outside (−2,2), so the horizontal shears vanish and the vertical ones cancel. Hence F is supported in [−6,6]×[−2,6], strictly inside D. Being a homeomorphism fixed outside D, it maps D onto D.

On a neighborhood of B, v(x)=4 and h(y−4)=0, whereas h(y)=1. The four operations therefore give

(x,y) → (x,y−4) → (x,y−4) → (x,y) → (x+1,y).

Thus F agrees with translation by (1,0) near B and maps B to B'. It maps the annulus D\int(B) homeomorphically to D\int(B').

## 4. A finite face-preserving surface correspondence

Partition D by the affine-piece boundaries of F and by the four boundary lines of B. A common refinement is a finite polygonal cell decomposition whose cells are convex polygons on each of which F is affine with determinant one. Triangulate this decomposition, subdividing shared edges consistently. Every resulting triangle is carried to a nondegenerate triangle with the same oriented planar area.

On the base top at height one outside B, use this triangulation and send (x,y,1) to (F(x,y),1). On the outer vertical walls and the bottom use the identity map, with compatible subdivisions; F is already the identity near the outer boundary. On the raised box's four walls and top use translation by (1,0,0), with compatible subdivisions; F is already this translation near B. These maps agree on every common edge and produce a PL homeomorphism P→P'. All maps are affine on the chosen triangles.

For top-annulus triangles, their oriented area vectors point upward and are preserved because det(DF)=1. All other triangles are fixed or translated, so their oriented area vectors are preserved as well. Consequently every pair of corresponding triangles has the same positive Euclidean area and identical unit normal; in particular their supporting planes are parallel. This is stronger than unoriented parallelism plus equal area.

An explicit rational instance is supplied in witness.json: 267 vertices and 530 triangular faces, with corresponding source and image vertex lists. The generator uses only rational half-plane clipping of affine pieces and a conforming centroid-fan triangulation. No existence theorem for an unspecified triangulation is needed to verify this instance.

The exact checker verifies every oriented area vector, all 795 edges with opposite paired orientations, connectedness, every vertex link being one cycle, and Euler characteristic two. The construction independently proves embeddedness: each boundary is the indicated box-with-raised-box boundary, the top annuli are related by a planar homeomorphism, and the other pieces are fixed or translated without crossing. The combinatorial checks are supplementary, not a substitute for this embedding argument.

## 5. The surfaces are not congruent

Each boundary has a unique maximal planar connected patch of greatest area: the bottom rectangle, of area 320, centered at o=(0,0,0). The top annulus has area 319, the raised top area 1, the outer vertical walls areas 20 or 16, and the raised walls area 2. These are geometric planar patches, independent of how they were triangulated. No adjacent nonhorizontal pieces merge into a larger planar patch. A rigid motion taking P to P' must therefore take the bottom rectangle to the bottom rectangle and its center o to o.

A rigid motion between these embedded boundaries also takes their bounded complementary regions, K and K', to one another. It consequently takes their volume centroids to one another. Both volumes equal 320+2=322. Direct box integration gives

centroid(K)=(0,0,82/161),
centroid(K')=(1/161,0,82/161).

Their squared distances from the distinguished bottom center are 6724/25921 and 6725/25921, respectively. They differ, so no such rigid motion exists. This includes reflections as well as orientation-preserving congruences. The exact oriented-triangle volume and centroid calculation independently reproduces these values.

## 6. Conclusion and limits

For triangulated polyhedral surfaces allowing coplanar adjacent faces, the printed parallel/equal-area implication is false, even for embedded closed spheres and an incidence-preserving correspondence preserving oriented face-area vectors. The finite construction is checkable by 3,514 exact rational assertions.

This answers the literal broad formulation under the stated standard PL convention. It is an elementary relocation construction and not a historical novelty claim. It does not settle an additional nonflatness or maximal-facet restriction absent from the displayed source statement. It also does not assert a result about Ghomi's adjacent smooth problem. The convex Minkowski uniqueness theorem is not contradicted: these surfaces are nonconvex. Alexandrov's more restrictive herisson uniqueness theorem assumes additional spherical-image structure which this repeated-normal, flat-subdivision example does not have.

Independent source-category and mathematical review is required before any result PR or full-status promotion.
