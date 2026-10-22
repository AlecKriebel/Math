# Turn2: affirmative result for integral root-direction zonotopes

AI-assisted mathematical proof candidate; independent review pending. Original unresolved2/5. Classical facts about zonotopes and base-polyhedron edge directions are credited; no novelty claim is made.

## 1. The structural class

Consider a zonotope

Z=t+sum_{edges ij} w_ij [0,e_i-e_j],

where the graph has no loops, parallel directions have been combined, w_ij are positive integers and t is integral. Assume0 belongs to Z and Z is contained in[-1,1]^n. Then Z has opposite vertices.

This includes every integral zonotopal base polyhedron in the original question. Indeed base-polyhedron edge directions are multiples of e_i-e_j, a classical consequence of the greedy normal fan refining into permutation chambers. Every generating direction of a zonotope occurs as an edge direction. Group parallel generators into a single positive segment. Its length in the primitive root direction is an integer because the corresponding edge joins integral vertices. Reversing generators only changes the translation; an integral vertex minus its selected integral generator endpoints then shows that translation can be chosen integral. Thus the displayed representation applies.

For clarity, the elementary normal-fan argument for base edge directions is as follows. Greedy vertices are constant on chambers of strict coordinate order. At a generic wall between two chambers only two adjacent coordinates exchange order; the two greedy outputs differ in these two coordinates alone and have the same sum, hence their difference is a multiple of e_i-e_j. Every edge's normal cone contains such a generic braid-wall piece: the base normal fan is a coarsening of the braid fan, and its codimension-one cones are unions of those walls. Coordinates fixed by decompositions can equivalently be treated in the affine span. This is the standard generalized-permutahedron characterization, used here with attribution rather than claimed as new.

## 2. Coordinate widths force graph degree at most two

The width of Z in coordinate i is d_i=sum_{j:ij edge}w_ij, since maxima/minima of a linear functional add under Minkowski sums. Therefore d_i<=2. Let c=t+(1/2)sum w_ij(e_i-e_j) be its center; its coordinate interval is [c_i-d_i/2,c_i+d_i/2].

If d_i=2, containment in[-1,1] forces c_i=0. If d_i=1, integrality of t makes c_i a half-integer, and interval containment gives c_i in{−1/2,1/2}. If d_i=0, the coordinate is fixed and0 in Z forces c_i=0.

Thus each weighted connected component is one of: an isolated coordinate; a unit-weight path; a unit-weight cycle of length at least3; or a single edge of weight2. There are no other possibilities: an edge of weight2 saturates both endpoint degrees, and otherwise the unweighted graph has maximum degree2.

## 3. Component analysis

Generators in different components use disjoint coordinates. The zonotope is their Cartesian product with the corresponding translations. On each component the sum of coordinates is constant; since0 is in Z it is zero, and equals the sum of that component's center coordinates.

- An isolated coordinate is identically zero, a one-point factor.
- A unit cycle has d_i=2 everywhere, hence center0. The factor is centrally symmetric about0. Negation takes every vertex to a vertex.
- A doubled edge also has center0 and gives the segment [−(e_i-e_j),e_i-e_j]. Its endpoints are opposite vertices.
- On a unit path label the vertices0,...,k and orient each edge i→i+1 (orientation does not affect its centered segment). Internal centers are0; endpoint centers are±1/2 with opposite signs because their total is zero. The centered representation is

c+sum_{i=0}^{k-1} alpha_i(e_i-e_{i+1}), with −1/2<=alpha_i<=1/2.

To obtain the zero point, set every alpha_i=−c_0, which is one of the two interval endpoints. The endpoint and internal coordinate equations all vanish. The path root vectors are linearly independent, so this affine image of the box is a parallelotope and that corner is a vertex. Therefore0 itself is a vertex of the path factor. Its negative is the same vertex, allowed by the exact source statement.

Choose an arbitrary opposite vertex pair in every centered cycle/doubled-edge factor and zero in every path/isolated factor. Their Cartesian products are opposite vertices of Z. This proves the theorem in every dimension.

## 4. Scope and controls

No central symmetry of the whole zonotope was assumed: translated path components need not be centered at0, but0 is their vertex. The cube and integrality hypotheses are essential to the component reduction. The result does not cover general non-zonotopal base polyhedra, whose faces can be triangles. It is separate from the source-known even-valued2-polymatroid result.

The exact checker enumerates centered cycle endpoint images and translated path corners through12 coordinates, verifying integrality, coordinate bounds, opposite cycle endpoints and the zero path corner; it checks doubled-edge factors separately. These controls do not prove the all-dimension classification, which follows from weighted degree<=2 and the component argument above. Public artifacts retain the checker and deterministic output; no general conjecture is inferred from this finite range.
