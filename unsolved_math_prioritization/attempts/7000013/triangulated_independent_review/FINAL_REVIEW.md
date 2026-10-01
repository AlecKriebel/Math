# Independent audit of the 7000013 PL counterexample

**Mathematical verdict: PASS for the explicitly stated finite triangulated-PL category allowing coplanar adjacent faces. Source-category verdict: qualified; the unrestricted intended Ghomi problem is not certified resolved.**

Reviewed on 2026-10-01. Exact candidate SHA-256: `a4d4369cacfa4859cb35164562c75ef4a69c43ab020d958cb70aaeadf8f32685`. Frozen manifest SHA-256: `78c82fd638e974f8f7abe2686bb2c7beaa6dd1aa275286a6c2986032e2cde63a`. All ten frozen artifacts were verified unchanged. The reviewer did not contribute to the construction. No mathematical correction is required within its stated category; the source convention must remain an unresolved qualification.

## 1. Exact source and the unresolved convention

I independently read and visually inspected [Ghomi's survey](https://people.math.gatech.edu/~ghomi/Papers/op.pdf), p.10, Section2.3 and Problems2.3–2.4. The displayed discrete question does not explicitly require noncoplanar adjacent faces, maximal planar facets, distinct normals, convexity, or a combinatorial matching. The submitted example satisfies much more than an arbitrary matching: it gives an incidence-preserving correspondence of closed embedded triangular spheres, with identical oriented area vectors.

Nevertheless the survey does not formally define its polyhedral-surface category there. The use of the word faces does not by itself prove that arbitrary coplanar triangulation cells are the intended faces. The same survey's later discussion, p.11, distinguishes a geometric edge graph from other geodesic graphs with convex faces. That is contextual evidence that the category deserves caution, not a proof that Problem2.4 imposes a nonflatness restriction.

[V. Alexandrov's 2002 primary paper](https://arxiv.org/abs/math/0211286), Section3.1, explicitly defines polyhedral surfaces by sphere-homeomorphic cell complexes whose cell images are convex polytopes. It does not impose noncoplanarity on adjacent two-cells. The submitted triangulated spheres satisfy this legitimate convention. That separate author's definition cannot establish an unstated convention in Ghomi's problem.

Accordingly the artifact proves a complete counterexample to the **broad triangulated-PL formulation** and supplies a valid source-scope warning. It does not warrant an unqualified statement that every intended form of Ghomi Problem2.4 is settled. A maximal-facet/nonflat version remains outside the proof. Under the campaign's five-turn policy, this qualified first-turn result does not by itself close an unresolved original-scope gate or permit moving on after one turn. The parent has retained that gate.

## 2. The compact shear map

The functions h and v are continuous piecewise linear with finitely many breakpoints. Each shear is a global homeomorphism with its explicitly stated inverse. Every affine piece has determinant1, so their commutator is an orientation-preserving PL homeomorphism, area-preserving on each affine piece.

The support bounds are correct, including their endpoints. If x≥6, then v(x)=0 and x-h(y)≥5, so the second vertical shear also vanishes; the horizontal shears cancel. If x≤-6, subtracting h only moves farther left. If y≥6, then y-v(x)≥2 and both h evaluations vanish; if y≤-2, the first vertical subtraction keeps y at most-2. Thus the map fixes the complement of the indicated interior rectangle and maps D onto itself.

In an open neighborhood of B, both relevant v values are4, the first h evaluation is0, and the last is1. The commutator is therefore exactly translation by(1,0) there. This is sufficient for all bump-wall and bump-top seams, not just for the four footprint corners.

## 3. Finite common triangulation and equal face data

The sequential affine-piece refinement can be obtained by finitely many half-plane cuts on each current cell. The resulting cells are convex and the map is affine with determinant1 on each. Conforming subdivision of shared edges and centroid fans give nondegenerate triangular cells. The refinement along the bump and outer boundaries agrees with the vertical-wall triangulations; the map is already the appropriate rigid map near those seams.

On the top annulus, an affine determinant-one planar map preserves the oriented area of each triangle. Those triangles stay horizontal, so the full three-dimensional oriented area vectors agree. Every other triangle is fixed or translated. Their vectors agree as well. Taking norms and then dividing by the positive area gives equal Euclidean areas and equal outward unit normals face by face. There is no hidden reversal of selected normals and no area cancellation between faces.

The correspondences preserve the entire finite abstract triangular complex. They need not preserve triangle edge lengths, nor does the claimed equal-area/parallel-normal statement require that.

## 4. Closedness, embedding, and topology

The two solids are a rectangular box with one rectangular raised box attached along a full interior face patch. Each is homeomorphic to a closed ball. Its boundary is an embedded closed orientable PL sphere. The top annulus, outer walls/bottom, and raised walls/top meet only along their prescribed seams; the planar homeomorphism and local translation make the surface map continuous and injective there.

I independently checked the frozen rational witness without importing the author's generator. The checks include distinct vertices in both realizations, nondegenerate triangles, every oriented area vector, all795 edge pairings with opposite orientations, and a single cyclic link at every vertex. The shared finite complex has267 vertices and530 triangles, Euler characteristic2.

For additional geometric validation, each triangle was independently classified into a specific axis-aligned boundary patch of the claimed solid, with exact coordinate inequalities. Top-annulus triangles were clipped against the bump interior and have zero overlapping area with it. Every pair of coplanar triangles was checked for disjoint interiors by rational separating-axis tests: **94,713 pairs per surface**, all pass. Patch-area totals are exactly the claimed320,319,1;20,20,16,16; and four2s. Thus the finite triangulations cover their prescribed boundary patches without interior overlaps. These checks are separate from, and reinforce, the topological construction proof.

## 5. Noncongruence under every rigid motion

The bottom rectangle is indeed the unique connected maximal planar two-dimensional boundary patch of largest area320. The annulus has area319; all other patches are smaller and meet it noncoplanarly. This characterization is geometric and survives erasing every subdivision edge. Therefore any global Euclidean isometry between the boundary sets maps bottom to bottom and fixes its center at the origin.

Such an isometry also maps the bounded complementary component to the bounded complementary component, hence maps the volume centroid. I independently computed volume and moments using the divergence fields(0,0,z), (0,0,xz), (0,0,yz), and(0,0,z²/2), so only horizontal face integrals are needed. This differs from the author's tetrahedral signed-volume implementation. Both volumes are322; centroids are(0,0,82/161) and(1/161,0,82/161). Their squared distances to the distinguished bottom center are6724/25921 and6725/25921. They differ. Reflections and orientation-reversing isometries are excluded by the same distance invariant.

The unique-largest-patch observation is used only to prove noncongruence; it does not covertly reinterpret the candidate's specified triangular faces as maximal facets for the theorem hypothesis.

## 6. Validation receipts and disposition

The independent checker passed **200,121 exact assertions**, including the geometric nonoverlap tests. The author's3,514-control generator was read and replayed in an isolated copy; both witness and verification receipt reproduced byte-for-byte. No floating-point geometric tolerance, downloaded executable, or numerical-only proof is used. The independent checker initially had a lexical spacing typo, corrected before it ran; no mathematical test failed.

The construction has no demonstrated historical novelty. It does not refute convex Minkowski uniqueness, the herisson theorem with its extra spherical-image conditions, or the adjacent smooth question. Its coplanar cells are essential and disclosed.

**Recommended checkpoint:** preserve the first-turn qualified broad-PL result and this audit. Do not promote an unqualified original claimed_solved status while the intended-face convention remains unresolved. Continue substantive work or source-definition resolution within the remaining author budget, and obtain a new review for any enlarged claim. No public PR or status change is performed by this reviewer.
