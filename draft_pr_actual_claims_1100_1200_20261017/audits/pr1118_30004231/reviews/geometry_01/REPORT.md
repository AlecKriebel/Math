# Independent geometry and canonical-summand audit — PR1118 / problem30004231

Audited head: `8592fb7297d3c4973f2778c47cfa8972cba896a6`.
Review date: 2026-10-17.
Reviewer shard: `reviews/geometry_01`.

**Verdict: PASS** for the geometry, canonical summands, dimensions, inclusion structure, product-interval classification, and numerical claims in scope. No defect found. This is an independent research audit, not external peer review or formal certification.

## Scope and independence

I read only `audit/input/PROOF.md` among the pinned manuscript/audit files, plus the primary EMS report. I did not read the historical MATHEMATICAL_AUDIT, acceptance/source reviews, or other new reviewers. The input PROOF.md SHA256 is `b6e32c893f45447951cf920777adaaf012b1eb5a9e5a8072a8822fc8fcf2ff28`.

The exact verifier starts with coordinates and reconstructs supporting facets and their full intersection lattice; it does not construct the lattice by assuming the manuscript's ordered index-pair formulas. Those formulas are compared afterward. A separate exhaustive enumeration of every pair of summand faces challenges noncanonical decompositions.

No Git refs, pinned inputs, PR, or other shards were changed. After local ENOSPC, the coordinator narrowly authorized preservation of this report, SOURCE_LEDGER.json and RESEARCH_LOG.md as unreferenced Git-data blobs; no ref, tree, commit or PR mutation was authorized or performed by this reviewer. No individual was contacted.

## Claim and success criteria

Let D=conv(0,e1,e2,e3,e4), I=[0,1], P1=D×I and P2=(−D)×I in R5. For each exposed face F of S=P1+P2, take its canonical summand faces G1,G2 exposed by the same functional. Retain exactly those with dim(G1),dim(G2)>0 and dim(F)=dim(G1)+dim(G2).

The claim in scope is that every retained face is an endpoint copy of a mixed face of D−D; there are 100 retained faces and 120 strict comparabilities, with two connected graph components each having 50 vertices and 60 edges. Success requires an exhaustive exposed-face classification, exact dimensions, uniqueness of summands, all inclusion relations, and treatment of t=0, u=0, empty and whole faces. Shellability and the source's homology target are audited separately by the coordinator; the graph census here provides independent input.

## Primary-source check

The primary source is [Oberwolfach Report 39/2019](https://ems.press/content/serial-article-files/46818), DOI 10.4171/OWR/2019/39, physical PDF page 70 (zero-based69), printed 2464, section 3, attributed to Sam Payne. It defines the class by positive summand dimensions and additive dimension, then asks about shellability and rational homology of a wedge of n−2 spheres. Neither that problem nor its immediate context states a general-position or transversality hypothesis. The example lies within the printed scope. No inference is made about unprinted intentions or generic variants.

## Independent H-representation and analytic exhaustiveness

Put Q=D−D. For x∈R4 let x+ and x− be its coordinatewise positive and negative parts. Then

Q={x: sum_i x_i+≤1 and sum_i x_i−≤1}.

Indeed, if x=p−q with p,q∈D, every positive coordinate of x is bounded by the corresponding coordinate of p, and every negative part by q. Conversely, the bounds put x+,x− in D and give x=x+−x−. Equivalently, for every nonempty J⊆{1,2,3,4},

−1≤sum_{j∈J}x_j≤1.

These 30 inequalities are an exact H-representation independent of ordered A,B face formulas. Each is a facet: for a positive subset J, the support face has roots vi−vj with i∈J and j∈{0,1,2,3,4}\J. Fixing one root, differences obtained by varying its first endpoint within J and its second endpoint in the complement give 3 linearly independent directions, by affine independence of the simplex vertices. The negative inequalities follow by symmetry. Thus all 30 inequalities are irredundant facets, with no missing facet.

Every nonzero root vi−vj, i≠j, is a vertex because a functional can uniquely maximize vi and uniquely minimize vj. The remaining input difference0 is the midpoint of opposite roots and is not a vertex.

Every polytope face is the intersection of its containing facets. Thus closing the exact facet list under intersection is analytically exhaustive, rather than an inference from finite search alone. The coordinate program independently rediscovers all 30 facets by testing every 4-point candidate hyperplane among the 20 roots, retaining actual supporting hyperplanes of affine rank3. It then closes their vertex sets under intersection. Every facet contains4 affinely independent vertices, so candidate enumeration cannot miss a facet.

For a nonempty intersection F, a positive sum of all containing outward facet normals exposes exactly F: each support deficit is nonnegative, and their sum vanishes exactly where every deficit vanishes. The program uses this normal and a differently weighted positive sum to recover canonical summands and challenge dependence on the exposing functional. The final tested code does not separately compare reconstructed facet normals to the explicit subset-sum H-list; that additional check was proposed but could not be written after ENOSPC and is not claimed.

## Canonical summands and all base dimensions

For any proper nonempty exposed face of Q choose nonzero u, write a_i=u(vi), and let A,B index the maximum and minimum values. Because the simplex affinely spans R4 and u≠0, those extrema differ, so A,B are nonempty and disjoint. Maximizing u(p−q) independently forces p∈conv{vi:i∈A} and q∈conv{vj:j∈B}. Hence the face is

F(A,B)=conv{vi−vj:i∈A,j∈B}.

Conversely, assign values 1 on A, −1 on B and 0 elsewhere and subtract the value at v0 to get a linear functional exposing precisely that pair. This post-hoc classification is exhaustive.

The summand dimensions are |A|−1 and |B|−1. Their direction spaces have zero intersection: an equality between zero-sum affine combinations on the disjoint index sets would be an affine dependence among the 5 simplex vertices. Therefore

dim F(A,B)=|A|+|B|−2.

All proper base faces are dimension-additive, whereas the whole base has dimensions(4,4,4) and is not. Qualifying cardinality pairs are exactly(2,2),(2,3),(3,2).

Canonical summands are unique even if the decomposition notation allowed arbitrary nonempty compact convex subpolytopes of the summands. If F=H1+H2 is exposed on P1+P2 by u, every point of either Hi must maximize u on Pi; otherwise a sum point would fail the exposed equality. Thus Hi⊆Gi=Pi^u. Since H1+H2=G1+G2, for every direction v the nonnegative support-function deficits h_Gi(v)−h_Hi(v) sum to 0. Both vanish in every direction, forcing Hi=Gi. No alternate pair of smaller faces can rescue a failed additive-dimension test.

The program separately enumerates every nonempty summand-face pair. Each Pi has 93 nonempty faces, giving 8649 pairs. A pair's sum lies in the intersection of all sum facets whose canonical summands contain the selected faces. This is its smallest containing sum face. Equality holds precisely when the pair-sum point set contains every extreme vertex of that face: all pair sums lie in the face, and an extreme vertex of S contained in their convex hull must itself occur among them. Exactly 543 pairs reproduce faces of S, each agreeing with its unique canonical pair; the other 8106 do not produce a face of S.

## Inclusion and the shared interval

For nonempty base faces F(A,B)⊆F(C,E), a functional exposing the latter must maximize on every vi−vj of the former. Equality of the difference of two scores with the global range forces i∈C,j∈E. Thus inclusion is equivalent to A⊆C and B⊆E. Conversely those index inclusions imply convex-hull inclusion. This proves uniqueness of indexing and excludes hidden identifications. The verifier checks all 32400 ordered pairs of proper nonempty base faces against this formula, not merely mixed faces or covers.

From Cartesian products, S=Q×[0,2]. Its exact H-representation has the 30 vertical lifts of Q's facet inequalities and two height inequalities. A functional(u,t) exposes Q^u×J with J={2} if t>0, J={0} if t<0, and J=[0,2] if t=0. This proves exhaustive product classification and excludes missing facet types. The program constructs the full 32-facet intersection lattice, then verifies afterward that every nonempty face is exactly a Cartesian product. All 294849 ordered pairs of nonempty sum faces satisfy product inclusion, including endpoint/vertical/whole interactions. Additionally, 129600 ordered pairs of proper endpoint faces satisfy the ordered index-pair inclusion formula.

At an endpoint the canonical faces are the base canonical faces times the corresponding endpoint of I, so all three dimensions are unchanged. For t=0 let the base dimensions be(c,a,b). The sum face has dimension c+1, while the summand dimensions are a+1,b+1. Since c≤a+b, their sum is at least c+2, so additivity is impossible. This excludes every full-interval face, including base-vertex cases, without assuming positive base dimensions.

For u=0,t≠0 the two end faces have dimensions(4,4,4), so fail additivity. For u=t=0 the whole sum has dimensions(5,5,5), so fails. The empty face has no positive-dimensional summands. Allowing or omitting the genuine whole face leaves the qualifying poset unchanged. No artificial bounds are appended.

## Census and graph structure

| Object | Vertices | Facets | Nonempty faces by dimension, starting at 0 | Faces including empty and whole |
|---|---:|---:|---|---:|
| Q=D4−D4 |20|30|20,60,70,30,1|182|
| Each Pi |10|7|93 nonempty total|94|
| S=Q×[0,2] |40|32|40,140,200,130,32,1|544|

The543 nonempty sum faces split into 181 lower endpoint faces,181 upper endpoint faces and 181 full-interval faces. Proper nonempty sum faces number 542. The mixed subset has 60 faces of geometric dimension2 and 40 of dimension3.

For a single endpoint, there are 30 minimal(2,2) faces and 20 maximal(2,3)/(3,2) faces. Each minimal element has two strict upper neighbors, and each maximal element has three lower neighbors. There are no chains of three elements. Therefore the order complex is a pure graph with 50 vertices and 60 edges; its degrees are 2 at 30 vertices and 3 at 20 vertices. Endpoint heights preclude cross-component comparisons.

Here is an analytic connectivity proof distinct from the manuscript's odd-cycle/double-cover argument. Suppress every degree-two minimal vertex. The remaining signed vertices are two-element subsets A+ and B−, adjacent exactly when A∩B is empty. If distinct same-sign two-subsets A,C intersect, the two-element complement of A∪C is an opposite-sign common neighbor. If A,C are disjoint, choose a two-subset R containing one element of each; it intersects both, so the preceding construction supplies a path from A to R and from R to C. Thus all same-sign vertices connect, and every opposite-sign vertex has neighbors. Suppression preserves connectivity. Each endpoint graph is connected.

A connected graph with 50 vertices and 60 edges has cycle rank 60−50+1=11. Thus the two components together have beta0=2,beta1=22 and no higher graph homology. This agrees with the numerical claim; no numerical boundary matrix calculation is substituted for this graph argument.

## Repeatability and adverse controls

Run from this review directory:

    python3 verifier.py
    python3 -O verifier.py

Both final runs passed and their JSON outputs were byte-identical. All checks use explicit exceptions, not assertions removable by optimization. The implementation uses integer Bareiss determinants and Fraction Gaussian elimination; no installation or third-party library is needed.

Saved artifact SHA256 values:

- verifier.py:4785407e1f5fc842cfa71593b00aee485deff20a67d2aba618e06573d3efd02e
- results.normal.json:d3f510f119525a1e85d8bb1421a9257e8bdff07d05d3e5f41a8b76c87d789283
- results.optimized.json:d3f510f119525a1e85d8bb1421a9257e8bdff07d05d3e5f41a8b76c87d789283

The verifier checks determinant row swaps, singularity, and rational rank. It also:

1. Reconstructs D3−D3 from coordinates, finding 12 vertices,14 facets,52 faces including empty/whole, and exactly6 incomparable mixed faces.
2. Takes perpendicular line segments in R2. Their whole rectangle has dimensions(2,1,1) and must qualify; it is the unique qualifying face. This prevents an accidental convention banning every whole face or requiring full-dimensional summands.
3. Applies an invertible rational shear/rescaling and independent rational translations to P1,P2, rechecks all 543 face dimensions and canonical summands, and verifies the transformed supports retain the same face vertex sets.
4. Deliberately rejects omission of the whole face from the complete census, counting the shared interval direction incorrectly, dropping positive dimensions, reversing inclusion, and deleting one supporting facet.
5. Checks empty exclusion, both nonqualifying end faces, all full-interval faces, and the nonqualifying whole sum.

## Strongest verified result and remaining gap

The exposed-face geometry and every numerical claim in this shard are established both analytically and by an independent exact coordinate reconstruction. The dimension-additive, positive-dimensional canonical faces are precisely the two endpoint copies; no alternate summand decomposition changes that conclusion. There is no remaining geometry gap for the stated example.

This audit does not establish novelty, examine unprinted intended hypotheses, or settle a modified generic problem. It does not rely on the historical audit. The coordinator is independently checking the precise source/realization and shellability/homology interpretation.

Final completion estimate for this geometry/canonical-summand audit:100%. Discovery of a novel result is not being claimed.
