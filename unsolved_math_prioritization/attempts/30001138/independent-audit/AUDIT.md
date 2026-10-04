# Independent adversarial audit: linked skeletons of convex four-polytopes

Target: rank 666, ID 30001138, OWR-3385-009. Audit date: 2026-10-04 UTC.

## Verdict

**ACCEPT AS UNRESOLVED AFTER FIVE APPROACHES.** The packet does not resolve the original existence problem. Its exclusions of simplicial four-polytopes, pyramids, four-polytopes with at most six vertices, all products of two polygons, and the completely vertex-truncated four-simplex withstand this audit. No mandatory mathematical correction was found. No full-resolution, novelty, or exhaustive current-literature-open claim is endorsed.

The reviewed input is exactly `rank666-30001138-authored-packet.zip`, 26,737 bytes, 16 regular files, SHA-256 `78cdf14fddfa360a5cbb27d1b571e88bd4eed6e7410c6296de628b19f9770719`. All 15 manifest-listed member hashes and sizes match. The input was preserved. This supplement contains authored audit material and public verification metadata only.

## 1. Target identity and terminology

The published original is Ivan Izmestiev's Problem 7 on printed page 108, not Problem 9. It asks about two disjoint spatially linked cycles in the specified boundary embedding of a convex four-polytope, while the abstract graph admits a nonlinked embedding. It imposes no simplicity or simpliciality restriction. The original page was freshly retrieved, text inspected, and visually checked. The packet correctly avoids the unrelated disjoint-terminal-path notion of graph k-linkedness. [Original report](https://ems.press/content/serial-article-files/46203)

The audit follows the packet's nonsplit-pair convention. A facet disk yields an actual separating sphere; no positive splitness conclusion rests merely on a zero linking number. A Petersen-family obstruction supplies a stronger obstruction, including nonzero mod-two linking in some pair in every embedding, so the differing terminology in older papers does not weaken the exclusions.

## 2. Geometric proof audit

### Facet disk and pyramids

A skeleton cycle contained in a three-dimensional facet is a simple polygon on that facet's boundary two-sphere. The Jordan disk can be pushed inward through a collar with its boundary fixed. Its interior is then in the facet's relative interior, which contains no skeleton edges. A small regular neighborhood of the disk, chosen disjoint from the other cycle, is a three-ball giving a separating sphere. This proves splitness, not just a homological statement.

For a pyramid, at most one member of a vertex-disjoint cycle pair visits the apex. The other is entirely in the base facet. Therefore the lemma applies without additional assumptions. These deductions are valid for the natural boundary embedding.

### Stacking and simplicial polytopes

The stacking step replaces a tetrahedral facet by a cone over its boundary, a three-ball. Its piecewise-linear identification with the original tetrahedron can place the new vertex in the interior and its four edges as radial segments, fixing the tetrahedral boundary. This extends by the identity to the rest of the boundary sphere. If a cycle uses the new vertex, shortcutting its two incident edges across the corresponding triangle avoids the other cycle. The triangle-cycle case must be removed using its disk, as the packet does. Otherwise the shortcut is a simple old cycle. The induction is sound.

A homeomorphism of the boundary spheres is enough to preserve splitness; the argument does not require a continuous path through convex realizations. Thus the equality theorem's combinatorial stacked conclusion is sufficient.

The two edge inequalities have precisely the required hypotheses. Theorem 1.2 in Chudnovsky–Scott–Seymour–Spirkl states Mader's bound for arbitrary finite graphs with at least four vertices, despite the paper's bipartite title. The lower bound is applied only to simplicial polytopes. Kalai's Sections 3.4–3.5, especially Theorems 3.3 and 3.4 on internal page 12, give the equality characterization in dimension four. This page was visually checked to distinguish d>3, d≥4, and the separate d>4 statement. Consequently linkless embeddability forces m≤4n−10, simpliciality forces m≥4n−10, and equality implies stacked. [Mader bound](https://arxiv.org/abs/2204.10119), [Kalai exposition](https://math.huji.ac.il/~kalai/aspects.pdf)

The underlying deep lower-bound and excluded-minor theorems are accepted as established cited inputs, not claimed to have been re-proved by this audit.

### At most six vertices

The augmented coordinate matrix has rank five and a one-dimensional affine-dependency kernel. Both sign supports have at least two members by extremality. If a coefficient is zero, the other five vertices span exactly a hyperplane: their span is at most three-dimensional by dependence and at least three-dimensional because adding the last vertex raises dimension by at most one. The remaining vertex is strictly on one side, giving a pyramid.

With all coefficients nonzero, the two sign types are (2,4) and (3,3), up to reversal. The affine evaluation space is the dependency's orthogonal complement. A functional zero on a proposed edge and strictly positive elsewhere exists exactly when both signs remain outside that pair. This proves the edge criterion rather than assuming general position. The resulting graphs have 14 and 15 edges respectively. No facet can have five vertices when the unique dependency has full support. Thus the (2,4) case is simplicial, while the (3,3) graph is K6. Both exclusions are valid. Independent arithmetic also reproduces 14,15,14 for positive support sizes 2,3,4.

## 3. Independent finite verification

The supplied verifier and manifest verifier were first replayed in an isolated extraction. Parsed output agrees exactly with `verification_results.json`.

A separate standard-library verifier was then written without importing or executing packet code. It constructs polygon-product edges from coordinate comparisons. It counts Hamilton paths in layered `(vertex subset, final vertex)` states, closes them into oriented cycles, and divides by two. It then directly tests every pair of distinct cycle masks for disjointness. This differs from the author's recursive cycle enumeration and subset-zeta coverage test.

Independent results:

- C3×C3: 111 cycles, 99 masks, 78 disjoint cycle pairs, zero uncovered pairs.
- C3×C4: 733 cycles, 510 masks, 723 disjoint cycle pairs, zero uncovered pairs.
- C3×C5: 4,448 cycles, 2,666 masks, 5,023 disjoint cycle pairs, zero uncovered pairs.
- C4×C4 negative control: 7,984 cycles, 2,840 masks, 156 uncovered disjoint mask pairs.

All length distributions and nonfacial-mask counts agree with the packet. Cycles longer than N−3 cannot belong to a pair of disjoint cycles in a simple N-vertex graph, so the truncation is exhaustive for the stated purpose. Mask compression preserves both tested predicates. An uncovered pair remains only a failure of a sufficient criterion.

The independent verifier reconstructs all seven stored family derivations by edge-set transformations. It verifies minor branch connectivity with union-find, constructs the quotient graph, and emits spanning-tree and adjacency witnesses. All three minor models pass. It independently identifies the ten-vertex target with the standard Petersen graph by an explicit isomorphism. The used targets employ only Delta-Y moves from K6: four for Petersen and three for the nine-vertex truncated-simplex obstruction. It rejects empty, overlapping, out-of-range, disconnected, missing-adjacency, and damaged-family controls.

For the truncated simplex, the verifier independently enumerates the vertices of `sum x_i=3, 0≤x_i≤2` by active bounds. It derives adjacency from the common active face, confirming 20 vertices, 40 edges, and degree four everywhere, with exactly the stated clique-plus-reversal graph.

Minor obstructions are applicable at the abstract graph level. The classic Petersen-family result and minor closure rule out a linkless embedding of each obstruction-containing graph. No reverse-Y preservation principle for arbitrary intrinsically linked graphs is assumed. [Robertson–Seymour–Thomas](https://arxiv.org/abs/math/9301216)

The infinite extension for polygon products is sound: partition a cycle factor into consecutive connected blocks and contract each block in every fiber. Products of the block branch sets are connected and disjoint, with all required product edges. For m,n≥4 this gives C4×C4; for one factor C3 and the other at least six it gives C3×C6. Together with the three exact facet-cover cases, this exhausts all polygon side counts. Face-lattice isomorphisms induce boundary-sphere homeomorphisms, so the argument is independent of polygon metric shape.

## 4. Spectral and later-literature safeguards

Izmestiev's Theorem 2.4 has the general-polytope scope claimed. Applying it to the polar with original vertices as facet normals gives a corank-four Colin de Verdière matrix whose kernel coordinates are the original vertices up to basis. Radial projection is a homeomorphism from a convex boundary with interior origin to S3; every edge lies in a positive supporting halfspace and projects to the short great-circle arc. Combining the established mu≤4 characterization of linkless graphs with the polytopal lower bound therefore yields the necessary equality mu=4. It does not prove flatness of that embedding. [Izmestiev](https://arxiv.org/abs/0704.0349)

The 1999 Remark 2 explicitly proposes the corank-four, 4-connected linkless-graph nullspace extension. The 2015 preprint of the 2017 Strong Arnold paper still asks whether normalized nullspace representations are flat. Its proved statement is algebraic and does not supply the missing complementary disks. The packet makes no invalid promotion from Strong Arnold, Balinski connectivity, or existence of some flat embedding to flatness of the specified natural embedding. [Lovász–Schrijver](https://doi.org/10.5802/aif.1703), [Schrijver–Sevenster](https://arxiv.org/abs/1512.03200)

The two-by-two interpolation countercontrol is arithmetically correct. Its endpoint determinants are −11, while the midpoint eigenvalues are −11/2 and −7/2. It refutes general convexity of the one-negative-eigenvalue condition. The packet correctly does not claim a corank-four example or disconnected admissible space from it.

Stanfield's 2025 article claims that every flat embedding can be linearized in R3. The published page 4594 passage was visually inspected. Naimi's March 2026 note attacks a specific disk-disjointness step, and explicitly does not assert that the constructed embedding refutes linearizability. The packet accurately treats this as a gap report and does not rely on the disputed proof. Even a correct linearization theorem for a chosen flat embedding would not identify it with the natural boundary embedding under investigation. [Stanfield article](https://doi.org/10.2140/agt.2025.25.4585), [Naimi note](https://arxiv.org/abs/2603.10066)

Fresh retrieval of all 13 public source files reproduced every reported size and SHA-256. Targeted current web checks did not produce a verified full resolution or correction resolving this target. That search result is bounded evidence, not proof of global open status. No novelty is asserted; in particular the pyramid and stacking observations already appear in Eppstein's 2014 exposition. [Eppstein](https://11011110.github.io/blog/2014/12/13/links-and-knots.html)

## 5. Scope of acceptance

The five approaches are distinguishable investigations: spectral/nullspace constraints, simplicial edge rigidity, facet/apex topology, products/truncations with explicit minors, and low-order affine dependency. Their overlap does not convert them into five solutions. Random negative minor searches are inconclusive and were not used to accept any exclusion. Their exact search history was not independently reconstructed.

Remaining mathematical task: handle nonsimplicial, nonpyramidal four-polytopes on at least seven vertices outside the excluded classes, or construct a verified witness there. The packet does neither. Its correct status remains unresolved after five approaches.

The audit did not independently re-download or re-parse the external corpus files listed in `DATA_PROVENANCE.json`; target identity instead rests on the primary report. That limitation does not affect the exclusion proofs. No repository, branch, PR, or external document was modified.
