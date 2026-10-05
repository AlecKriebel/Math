# Linked skeletons of convex four-polytopes: exclusions and exact controls

Target: 30001138 / OWR-3385-009. Research date: 2026-10-04.

## 1. Exact question and outcome

For a convex four-dimensional polytope P, let G be its vertex-edge graph, embedded naturally in the three-sphere boundary of P. Can this particular embedding contain a nonsplit pair of vertex-disjoint cycles while the same abstract graph admits another embedding in the three-sphere in which every pair of disjoint cycles is split?

The existence question is **unresolved in this investigation**. This document proves exclusions, not a solution. It excludes pyramids, simplicial four-polytopes, all four-polytopes with at most six vertices, every Cartesian product of two polygons, and the completely vertex-truncated four-simplex. A nonexistence proof for arbitrary nonsimplicial, nonpyramidal four-polytopes has not been obtained. Novelty of the individual exclusions is not asserted.

The source is Ivan Izmestiev's Problem 7 in the open-problems section of *Discrete Differential Geometry*, Oberwolfach Reports 6 (2009), printed p.108, DOI 10.4171/OWR/2009/02. The numerical suffix 009 in the imported identifier is not the source's problem number.

Here linked means a nonsplit two-component spatial link. An integer or mod-two linking number can detect some links, but zero linking number does not prove a pair split. We do not substitute that weaker test. Neither graph k-linkedness (disjoint paths between specified terminals) nor k-vertex-connectivity is the target property. No simplicity, simpliciality, generic-coordinate, or rational-coordinate restriction appears in the exact question.

## 2. Spectral route and its exact gap

Put the origin in the interior of P. Izmestiev's Theorem 2.4 constructs a Colin de Verdiere matrix M for G of corank four whose kernel coordinates give the vertices of P, up to choice of basis. The construction uses minus the support-parameter Hessian of the volume of the polar polytope. The theorem is for arbitrary convex polytopes; it is not limited to simple or simplicial ones. In particular, mu(G) >= 4. If G has a linkless embedding then mu(G) <= 4 by the Lovasz-Schrijver characterization, so any desired example has mu(G)=4.

Radial projection of the natural skeleton into S^3 is well defined because the origin is interior. Edges become short geodesic arcs: the segment between adjacent vertices lies in a proper supporting hyperplane, so its positive cone does not contain a line. Radial projection on the whole boundary is a homeomorphism. Thus a desired example would give a corank-four nullspace representation which is linked even though G admits a linkless embedding.

This reduction does not show that the natural embedding is linkless. Schrijver and Sevenster's 2015 preprint / 2017 paper establishes the Strong Arnold Property for the relevant well-signed matrices of 4-connected flat graphs. Its introduction explicitly retains the question whether their normalized nullspace representations are flat. Strong Arnold is an algebraic nondegeneracy condition, not a disk-complement theorem. A matrix with the required signature cannot be promoted to a certificate for the particular embedding's linklessness.

A direct deformation attempt also fails at a concrete algebraic step. One might interpolate two well-signed matrices and hope that their one-negative-eigenvalue condition persists, then transport a flat embedding along the resulting nullspaces. This condition is not convex even for a single edge: A=[[-10,-1],[-1,1]] and B=[[1,-1],[-1,-10]] each have determinant -11, hence one negative eigenvalue, but (A+B)/2=[[-9/2,-1],[-1,-9/2]] has eigenvalues -11/2 and -7/2. Both endpoint sign patterns are correct for K2. This is not a counterexample in corank four or for a polytope; it is an exact negative control rejecting the proposed general convex-interpolation inference. In the target situation corank four, noncollision, and preservation of embedding type would also require proof. We have not proved that the relevant admissible space is disconnected, only that naive linear interpolation is unjustified.

Exact missing step: either find a polytope with mu(G)=4 and a verified nonsplit pair in its boundary, or prove that every such polytopal nullspace embedding is linkless. The general nullspace conjecture is stronger and was not assumed. Balinski connectivity supplies a necessary hypothesis, not this missing conclusion.

## 3. Two elementary geometric lemmas

**Facet-disk lemma.** If a cycle C of G is contained in a proper three-dimensional facet F of P, then C bounds an embedded disk in F whose interior avoids the entire skeleton. Consequently C is split from every disjoint cycle of G.

**Proof.** Each edge of G lying in F is an edge of F and lies on its boundary two-sphere. The simple closed curve C bounds a disk on this two-sphere. Use a collar of the sphere inside the three-ball F to push the interior of this disk slightly inward while fixing its boundary. The disk interior then lies in relint(F), disjoint from G. A sufficiently small closed regular neighborhood of the disk is a three-ball disjoint from the other cycle and with C in its interior; its boundary separates the components. This is a topological split-link argument and does not rely merely on linking numbers. QED.

**Stacking lemma.** The natural skeleton of a stacked four-polytope contains no linked pair of disjoint cycles.

**Proof.** Start with the four-simplex, whose five vertices cannot support two disjoint cycles. Adding one stack replaces a tetrahedral boundary facet T by the other facets of a four-simplex glued onto T. Topologically identify the replacement three-ball with T, fixing its boundary, with the new vertex w inside T and its four incident graph edges the radial cone to the four vertices of T. This gives the usual subdivision picture, without changing any link type in the boundary three-sphere.

For any pair of disjoint cycles, at most one uses w. If neither does, induction applies. Otherwise the cycle using w has a consecutive subpath a-w-b with a,b distinct vertices of T. The triangle a-w-b in T has interior disjoint from the old skeleton. Replace this subpath by the edge a-b. The isotopy across that triangle avoids the other cycle because its vertices exclude a,b,w and all its edges lie outside int(T). If the original cycle was the triangle a-w-b-a, it already bounds a disk disjoint from the other cycle and is split. Otherwise the shortcut yields a simple old cycle, and induction applies. QED.

## 4. Exclusion of every simplicial four-polytope

**Theorem.** A simplicial convex four-polytope cannot answer the target question positively.

**Proof.** Write n=f_0(P), m=f_1(P), with n>=5. If G has a linkless embedding, G has no K6 minor. Mader's bound yields m<=4n-10. The lower-bound theorem for simplicial four-polytopes yields m>=4n-10. Hence equality holds. The equality characterization in dimension at least four says that a simplicial polytope with g_2=m-4n+10=0 is stacked. The stacking lemma shows that the natural embedding is linkless. QED.

Alternatively, if the simplicial polytope is not stacked, then m>4n-10 and its graph contains a K6 minor, so no alternative linkless embedding exists.

Dependencies and scope: Kalai's author-hosted *Some aspects of the combinatorial theory of convex polytopes*, Sections 3.4-3.5, states the lower bound and equality characterization with the necessary d>3 condition; the relevant page was inspected visually. Mader's bound is explicitly stated as Theorem 1.2 in Chudnovsky-Scott-Seymour-Spirkl, *Bipartite graphs with no K6 minor*, arXiv:2204.10119. The bound itself is for all finite simple graphs, not just bipartite graphs. This argument fails for a general nonsimplicial polytope because the simplicial lower bound cannot be applied to its graph.

## 5. Exclusion of every pyramid

**Theorem.** The natural skeleton of a four-dimensional pyramid over any convex three-polytope is linkless.

**Proof.** Call its apex v and base facet Q. Among two disjoint cycles, at least one avoids v. Every other vertex and every edge not incident with v is in Q, so this cycle is contained in Q. The facet-disk lemma makes the pair split. QED.

No simpliciality or simplicity assumption is used. Pyramids and stacked polytopes were already discussed as unlinked classes by David Eppstein in his 2014 research exposition; these are not claimed as new discoveries.

## 6. Exclusion through six vertices by affine dependencies

**Theorem.** Every positive example has at least seven vertices.

**Proof.** A four-polytope has at least five vertices. At five it is a simplex, with no two disjoint cycles. Suppose there are six vertices v_1,...,v_6. The augmented 5-by-6 coordinate matrix with columns (v_i,1) has rank five. Its affine-dependency space is one-dimensional; choose a nonzero vector lambda with sum lambda_i v_i=0 and sum lambda_i=0. Both its positive and negative supports have size at least two: a support of size one would express one vertex as a convex combination of others, contradicting extremality.

If lambda_z=0, the other five points are affinely dependent and span dimension at most three. They actually span dimension three, because adding v_z increases dimension by at most one and all six span dimension four. The hyperplane through the other five has v_z strictly on one side, so their convex hull is a facet and P is a pyramid. Section 5 applies.

Assume now that lambda has no zero entries. Up to reversing its sign, the support sizes are (2,4) or (3,3). A pair {a,b} is an edge precisely when the remaining four coefficients contain both signs. To verify this criterion, the space of value vectors of affine functions on the six vertices is exactly lambda-perp. An affine functional exposing exactly {a,b} exists precisely when it can have value zero on a,b and strictly positive values elsewhere. Such positive values can satisfy the single relation sum lambda_i t_i=0 exactly when both signs occur outside the pair. A functional of this kind exposes an edge, and conversely every edge has such an exposing functional.

For (3,3), every pair is an edge and G=K6. K6 is intrinsically linked, so it has no linkless embedding. For (2,4), G=K6 with just the edge between the two positive-support vertices omitted. Moreover P is simplicial: a facet with five or more vertices would produce an affine dependence supported on at most five vertices, impossible when the unique dependence has no zero entry. Thus Section 4 excludes this case. These cases exhaust six vertices. QED.

The verifier independently enumerates the edge criterion for support sizes 2,3,4 and obtains 14,15,14 edges. This is only a control for the combinatorial arithmetic; the proof above handles arbitrary real coordinates, including zero-coefficient cases.

## 7. Complete exclusion of polygon products

For integers m,n>=3 let P be the Cartesian product of a convex m-gon and a convex n-gon. Its skeleton is C_m square C_n. These are simple four-polytopes, generally not simplicial. Label vertices (i,j) by in+j. Its facets have vertex sets consisting of two consecutive rows or two consecutive columns.

**Theorem (with finite exact certificates).** No product of two polygons answers the target question positively.

**Proof.** Reorder factors so m<=n. There are three cases.

1. m>=4. Contract consecutive edges in each cycle factor until both factors have four vertices. Performing a factor contraction in every row/column gives a graph minor C4 square C4, the graph of the four-cube. The supplied branch sets certify that this graph has the Petersen graph as a minor. Thus the original graph is intrinsically linked and has no alternative linkless embedding.
2. m=3 and n>=6. The same factor-contraction argument produces C3 square C6 as a minor. Supplied branch sets again certify a Petersen minor, so this case is intrinsically linked.
3. m=3 and n=3,4,5. The exact exhaustive verifier checks every pair of vertex-disjoint simple cycles and proves that at least one member lies in a facet. The facet-disk lemma therefore shows that the natural embedding is linkless.

For case 3 the program enumerates unoriented simple cycles of lengths 3 through N-3, where N=3n. Every member of a disjoint pair has such a length. Start each cycle at its least-labelled vertex and retain just the orientation with second vertex smaller than last vertex. This produces every relevant cycle once. Membership in a facet and disjointness depend only on the vertex set, so cycle masks may be combined without losing information. After retaining masks of cycles contained in no facet, a subset dynamic program tests whether one such mask is contained in the complement of another. It finds none. The totals of enumerated cycles are respectively 111, 733 and 4448; the full length distributions appear in verification_results.json. This is finite exhaustive verification for exactly these three graphs, not sampling.

The same calculation on C4 square C4 finds an uncovered disjoint pair, a negative control. Failure of this sufficient facet criterion is not asserted to prove that this particular pair is linked. Intrinsic linking of that graph comes instead from its explicit forbidden minor. QED.

All these graph/facet properties depend only on the combinatorial type. Products of convex polygons with the same side counts have isomorphic boundary cell complexes, inducing homeomorphisms of their boundary spheres. Coordinates and metric shapes need not be specified.

## 8. Why truncating the simplex is not a counterexample

Take the four-simplex in barycentric coordinates x_0+...+x_4=3, x_i>=0, and truncate all five vertices by x_i<=2. Its 20 vertices are 2e_i+e_j for i!=j. The graph has labels (i,j), i!=j; vertices with common first label form a K4, and each (i,j) is also adjacent to (j,i). There are no other edges, by the face constraints of the truncated simplex.

The supplied minor model has nine branch sets and a target obtained by three Delta-Y moves from K6. Each move, every branch set's connectivity, pairwise branch disjointness, and all target adjacencies are checked exactly. This graph is intrinsically linked. It therefore cannot have the alternative linkless embedding the question requires. The mere appearance of linked cycles in its natural embedding is not sufficient.

This also prevents a tempting invalid induction: linklessness does not in general survive arbitrary simple-vertex truncation. Beginning with an unlinked simplex and successively truncating its original vertices can end with this intrinsically linked graph. No claim is made that the first, or every, individual truncation creates a link.

For our three obstruction models, the target families have explicit Delta-Y derivations from K6. Their intrinsic linking follows from the standard Conway-Gordon-Sachs theorem and preservation under Delta-Y moves (or directly from the Petersen-family theorem). We do not need to assume the disputed recent straight-line embedding result.

## 9. Literature safeguards and remaining question

The 2009 problem and the 2015/2017 nullspace discussion are compatible with all exclusions above. A 2025 paper by Lynn Stanfield claims that flat graph embeddings can be linearized in ordinary three-space. Ramin Naimi's March 2026 preprint identifies a gap in the argument; his example is explicitly not a disproof of the theorem. Neither the claim nor its criticism settles the present question, which fixes the natural boundary embedding of a convex four-polytope. The 2025 claim is not used anywhere in our deductions.

Neither the existence of a linkless abstract embedding, the existence of some linear embedding, the Strong Arnold Property, nor zero pairwise linking numbers alone proves linklessness of the specified boundary embedding. Conversely, one linked boundary pair is not enough without verifying abstract linkless embeddability.

After five distinct approaches the exact target remains open in this work. The residual class consists of nonsimplicial, nonpyramidal four-polytopes on at least seven vertices, excluding polygon products and the completely truncated simplex. No certified candidate witness was found. The exclusions above do not establish that this residual class is empty.

## References used

- Oberwolfach primary report, https://doi.org/10.4171/OWR/2009/02 ; Problem 7, p.108. Public PDF: https://ems.press/content/serial-article-files/46203
- I. Izmestiev, *The Colin de Verdiere number and graphs of polytopes*, https://arxiv.org/abs/0704.0349 ; Theorem 2.4 and its proof, Appendix A signature argument.
- L. Lovasz and A. Schrijver, *On the null space of a Colin de Verdiere matrix*, https://doi.org/10.5802/aif.1703 ; 1999, p.1019, Remark 2.
- A. Schrijver and B. Sevenster, *The Strong Arnold Property for 4-connected flat graphs*, https://arxiv.org/abs/1512.03200 ; introduction and main proof.
- G. Kalai, *Some aspects of the combinatorial theory of convex polytopes*, https://math.huji.ac.il/~kalai/aspects.pdf ; Theorem 1.2, Sections 3.4-3.5. The equality theorem is from his 1987 *Rigidity and the lower bound theorem I*, DOI 10.1007/BF01405094.
- M. Chudnovsky, A. Scott, P. Seymour, S. Spirkl, *Bipartite graphs with no K6 minor*, https://arxiv.org/abs/2204.10119 ; Theorem 1.2 restates Mader's general edge bound.
- N. Robertson, P. Seymour, R. Thomas, *Linkless embeddings of graphs in 3-space*, https://arxiv.org/abs/math/9301216 ; and *Sachs' Linkless Embedding Conjecture*, https://doi.org/10.1006/jctb.1995.1032 .
- D. Eppstein, *Links and knots in the graphs of four-dimensional polytopes*, 2014, https://11011110.github.io/blog/2014/12/13/links-and-knots.html .
- L. Stanfield, *Linear linkless embeddings: proof of a conjecture by Sachs*, 2025, https://doi.org/10.2140/agt.2025.25.4585 ; not used as a theorem.
- R. Naimi, *A Gap in Stanfield's Proof of Sachs' Linear Linkless Embedding Conjecture*, 2026, https://arxiv.org/abs/2603.10066 ; a gap report, not a counterexample to linearizability.
