# Independent review of relative collapse under subdivision

## Verdict and scope

**PASS for the stated partial result. No mandatory correction is required.** The local protected-boundary reduction is exact, and the constructive argument proves the prescribed-target statement for finite complexes of dimension at most two. The higher-dimensional linear-subdivision problem remains unresolved. The package makes no novelty claim, and this review does not promote it to a solution of the original problem.

Reviewed on 2026-09-30 by a separate gpt-6-astra reviewer with xhigh reasoning. The frozen artifact is PARTIAL.md, SHA-256:

1adb24c7b7d48655368bd89405bcd6c4fd6ac4a95fac574922b5e91ebeff27a9

The reviewer made no changes to the author artifact or its checks.

## Original statement and credited results

I read the complete relevant OWR contribution and visually inspected printed p.1460. The sentence immediately before Problem 2 explicitly adopts *linear triangulation* as the subdivision convention. Problem 2 asks for collapse to the induced subdivision of the **specified** target. Corollary 2 inserts a barycentric subdivision on both sides. The same page expressly warns that ordinary collapsibility of subdivisions of convex balls does not immediately settle the relative question. The candidate preserves all of these distinctions. [Original report, pp.1459–1462](https://ems.press/content/serial-article-files/46393?nt=1)

I also read the definitions, Lemma 2.3, and the complete proof of Theorem 4.3 in the published Adiprasito–Benedetti paper, and visually inspected its theorem page (PDF page 17). The theorem's conclusion is precisely sd(D) collapsing to sd(D′). Its proof reduces to an elementary original collapse and uses the derived-subdivision endo-collapsibility result. It does not furnish an unsubdivided sequence on D. The source's geometric-complex and restriction conventions match those used in the partial result. [Published article, DOI 10.1007/s00454-019-00137-3](https://doi.org/10.1007/s00454-019-00137-3), [accessible full text](https://par.nsf.gov/servlets/purl/10169029)

As additional prior-art context, Adiprasito–Benedetti's earlier paper states that a planar complex collapses to any subcomplex whose realization is a deformation retract: Lemma 2.5 in [arXiv:1202.3390v2](https://arxiv.org/abs/1202.3390v2). The lemma there has its proof left to the reader. It is broader corroborating context for the elementary planar case, not a substitute for auditing the submitted constructive proof.

The bounded source check supplies no new full resolution of Hudson's question. The package's explicitly partial disposition is appropriate.

## Exact local reduction

Proposition 1 has both directions, with the target retained.

For necessity, the face complex of a simplex collapses by deleting the simplex and the chosen free facet. Removing that facet from the boundary face set retains all its proper faces. Consequently the target is a subcomplex, not the set-theoretic complement of the closed facet. This matters at the endpoints and lower-dimensional boundary intersections.

For sufficiency, at an original elementary step, the realization of the removed region consists of the simplex interior and the relative interior of its free facet. Every other part lies in the next original subcomplex. Because the subdivision respects the original faces, restricting it gives both asserted identities:
\[
D_i=T\cup D_{i+1},\qquad T\cap D_{i+1}=K.
\]
The intersection is exactly the prescribed subdivided protected boundary part.

Consider any pair removed by a relative collapse of T to K. Neither member lies in K, since collapses delete faces without subsequently restoring them. If an additional coface of the pair's lower face lay in the adjoined complex \(D_{i+1}\), closure under faces would put that lower face in \(D_{i+1}\), hence in \(T\cap D_{i+1}=K\), a contradiction. This also excludes an outside coface of the upper simplex, since such a coface would contain the lower face. Thus maximality and freeness survive gluing, not merely the homotopy type.

Applying these sequences along the finite original collapse ends at the restriction to the original prescribed target, exactly D′. No compatibility of arbitrarily chosen local sequences beyond this fixed overlap condition is required.

The dimension-zero convention is coherent: a vertex cannot be deleted using the empty face, so no nontrivial elementary step arises there.

## Disk certificate

Proposition 2 is valid for every finite triangulated closed disk with a nonempty connected proper boundary subcomplex K. Such a subcomplex is a path or a vertex. Since it is proper, some boundary edge is outside it.

The key points were checked individually:

1. The triangle dual graph using interior edges is connected. A path between triangle interiors can be chosen in the disk interior, avoiding the finite vertex set and meeting edges transversely.
2. The chosen outside boundary edge has exactly one incident triangle, so the initial edge-triangle pair is free and does not meet the target.
3. At a later triangle, its parent triangle has already been removed. The shared interior edge originally has exactly two incident triangles; therefore only the current triangle still contains it.
4. That shared edge has not previously been deleted. Earlier moves delete only their selected edge and their triangle. In a simplicial disk, the edge joining a triangle to its parent cannot simultaneously be another triangle's selected parent edge.
5. All subsequent paired edges are interior. Hence no boundary face of K is deleted.
6. After the triangles are removed, the remainder is a connected contractible finite graph. A connected graph is contractible only if it is a tree; contractibility here follows from genuine elementary collapses of the disk.
7. K is a connected subtree of that tree. If anything remains outside K, there is an outside vertex: an additional edge between vertices of K would create a cycle. A vertex of greatest distance from K is a leaf, because every edge other than its unique edge toward K would increase the distance in a tree.
8. Deleting this leaf with its sole incident edge preserves K. Iteration terminates at K exactly, including when K is a single vertex.

The proof does not assume a shelling. Its triangle order is a parent-first order in a spanning tree, and the final pruning is a separate one-dimensional procedure.

For a subdivided original triangle, the protected part consists of the two retained original sides and their subdivisions, a connected proper boundary path. For an interval it is the prescribed retained endpoint. These facts justify Corollary 3 from the local reduction.

## Why the higher-dimensional gap is real

The disk proof uses the implication that a connected contractible graph is a tree. After top-dimensional peeling in higher dimensions, the residual complex can have dimension at least two. Contractibility alone no longer provides the required free-face sequence relative to its protected subcomplex.

The candidate stops at this exact gap. In particular, it does not infer relative collapsibility from absolute collapsibility, use shellability and collapsibility interchangeably, remove a barycentric subdivision from a known theorem, or treat an arbitrary PL ball as a linear triangulation of a simplex. No statement beyond the verified low-dimensional scope follows from the finite controls below.

## Reproduction and independent controls

The submitted checker was copied into an isolated replay directory before execution. It passes all **4,200** assertions for **27** rational disk triangulations and **6** glued-region cases. Both regenerated files, verification.json and sample_certificate.json, are byte-identical to the submitted versions.

I inspected its pair predicate, construction, and output. It requires exactly one proper coface of the lower face, codimension one, and exclusion of both deleted faces from the target. The regular triangular grids and interior stellar insertions construct genuine planar subdivisions. Its negative control rejects a topologically free pair when that pair would delete a protected target face.

The separate checker passes **59,718** assertions. Its inputs and checks include:

- Thirteen rational disk meshes constructed with boundary-edge splits and weighted interior stellar insertions
- All singleton targets and all proper connected boundary arcs of those meshes, giving **387** disk-target cases
- A cone over each protected target, joined using a new vertex, giving **387** external-gluing cases with intersection exactly equal to the protected target
- **30** interval cases testing both prescribed endpoints
- Independent replay of the explicitly listed submitted sample certificate
- Negative controls for deleting a protected face, introducing an obstructing outside coface, retaining the entire disk boundary, and deleting the empty face

For each emitted move, the independent checker tests the full proper-coface set, preservation of every protected face, downward closure of the remaining face set, and final equality with the specified target. Empty faces are uniformly omitted from the computational encoding and are never collapsed. All coordinates used to generate the planar meshes are rational.

These assertion counts include repeated invariants at successive moves; they are not counts of independent theorems or high-dimensional examples. The finite checks support the algorithms and edge cases. The general propositions rest on the arguments audited above.

## Disposition and publication files

Retain **unsolved, one substantive route used**, with no novelty claim. The proven partial scope is the local equivalence and the exact relative statement in dimensions zero, one, and two.

The six publication files are:

- REVIEW.md
- review_summary.json
- independent_checks.py
- independent_results.json
- submitted_verification.json
- submitted_sample_certificate.json

The independent checker uses only the Python standard library and the accompanying submitted sample certificate. Source PDFs, page images, and the isolated author replay directory are local review materials, not part of the publication package.

## Final administrative hash addendum

At 06:47 UTC on 2026-09-30, I verified that the only artifact change replaces the pending-review sentence with a passed-review sentence linking this report. Reversing that exact replacement recovers the original frozen bytes. The final artifact SHA-256 is 2d8b599378ff784446a35ec84a28bbd2555f67b2da7f11853eb7d775ac61c6a8. The verifier and sample certificate are unchanged; the final author receipt differs only in its artifact-hash field. The archived submitted receipt retains the original audited hash. Mathematical content and the PASS_PARTIAL verdict are unchanged, and this review covers the final artifact.
