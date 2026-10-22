# Independent exact-target, combinatorics, shellability, and homology audit

**Verdict: PASS for both universal assertions exactly as printed, using the standard order-complex realization.** The five-dimensional construction refutes shellability and the specified rational homology. No required mathematical repair was found in this audit's scope. This is an independent AI-assisted mathematical review, not human peer review, formal certification, or novelty/priority clearance.

Pinned input: PR1118 head `8592fb7297d3c4973f2778c47cfa8972cba896a6`, problem 30004231 / OWR-17135-028. PROOF.md has 14,824 bytes, SHA256 `b6e32c893f45447951cf920777adaaf012b1eb5a9e5a8072a8822fc8fcf2ff28`, matching the frozen manifest. No historical audit, other new review, candidate checker, or geometry-family conclusion was consulted.

## Exact printed target

The [publisher report](https://ems.press/content/serial-article-files/46818), printed p.2464 / physical p.70, was freshly fetched, read, and visually inspected in memory. Problem 3 is Sam Payne's question. It explicitly requires positive summand dimensions and dimension additivity, and asks poset shellability and rational homology of a wedge of (n-2)-spheres. No general-position assumption appears. The complete-intersection motivation does not supply an additional printed hypothesis.

The standard realization is the order complex, with poset elements as vertices and strict chains as simplices. Wachs's primary [Poset Topology notes](https://arxiv.org/pdf/math/0602226), pp.6-7 and 44, expressly state this convention and define poset shellability through its order complex. The candidate applies it consistently. Reversing order leaves chains unchanged. Adjoining a new maximum would cone off the realization and change its homology; boundedization followed by taking the proper part instead recovers the original poset.

Empty faces fail positivity. Allowing the improper whole sum does not affect either example because its dimension is less than the sum of the full summand dimensions. Neither empty realizations nor exceptional sphere-dimension conventions are used.

The definition on p.3 of [arXiv:1607.00347](https://arxiv.org/pdf/1607.00347) uses summand facets for its totally mixed faces. This differs from the explicitly printed OWR definition and cannot silently replace it. The present verdict does not address a generic-position or differently defined variant.

## Canonical summands and the face classification

Let F be exposed in P1+P2 by u, with canonical summands C_i=P_i^u. Suppose nonempty faces G_i of P_i also satisfy G1+G2=F. For every pair g_i in G_i, u(g1)+u(g2)=h_P1(u)+h_P2(u). Each separate term is bounded above by its own support value, so both bounds are attained and G_i is contained in C_i. For every other functional w, the two nonnegative deficits h_Ci(w)-h_Gi(w) sum to zero because the Minkowski sums are equal. Thus both support functions agree individually and G_i=C_i. Alternate smaller summand faces cannot rescue a rejected face. This argument even tolerates an initially existential reading of the decomposition.

For D_m=conv(v0,...,vm), v0=0 and vi=e_i, a nonzero functional gives nonempty disjoint maximum/minimum vertex sets A,B. The exposed difference face is conv{vi-vj : i in A,j in B}. Conversely every disjoint nonempty pair occurs by assigning heights 1,-1,0 on A,B,the remainder and taking functional coordinates h_i-h_0. Thus three-level height enumeration is exhaustive, not random directional sampling.

The two direction spaces have zero intersection: an equality of their zero-sum affine combinations would be an affine dependence among disjoint subsets of the simplex's affinely independent vertices. Hence dim F(A,B)=|A|+|B|-2; positivity is exactly |A|,|B|>=2.

Inclusion is coordinatewise inclusion of A and B. For the forward direction, a functional exposing F(C,D) attains its maximum difference on every vi-vj in F(A,B), forcing i in C and j in D. Nonempty A,B give both inclusions. This also proves unique index pairs.

## Independent exact reconstruction

The independently authored standard-library verifier uses integer coordinates, all three-level simplex-height patterns, and all three interval signs. It forms summand support point sets, forms all sums, deduplicates by the actual sum-point sets, and computes all affine dimensions by exact rational elimination. Qualification is determined by these computed dimensions rather than by the candidate's count formula. Every resulting face inclusion, including every nonincidence, is compared with the index-pair prediction.

Point-set inclusion is valid here even when a stored sum point is a nonvertex. The full generating set consists of all sums of summand vertices. The generating points on an exposed face are exactly those maximizing its exposing functional. Containment of faces therefore implies containment of their complete support-generator sets; the converse follows by convex hulls.

| Case | All nonempty faces | Qualifying elements | Strict comparisons | Order-complex f-vector |
| --- | ---: | ---: | ---: | --- |
| D4-D4 in R4 | 181 | 50 | 60 | (50,60) |
| (D4-D4) x [0,2] in R5 | 543 | 100 | 120 | (100,120) |
| D3-D3 in R3 | 51 | 6 | 0 | (6) |

All 2,500, 10,000, and 36 ordered qualifying-element pairs respectively were checked. No qualifying whole sum occurs. Exactly 50 R5 qualifiers are at each endpoint; none spans the interval. There are 60 degree-two vertices and 40 degree-three vertices overall. All 120 order-complex facets are edges.

The interval-spanning exclusion is also direct. If the interval coefficient vanishes, the two summand-face dimensions are a+1,b+1 while the sum dimension is c+1 with c<=a+b, so additivity is impossible. If it is nonzero, the interval faces are endpoints and the test is exactly the base test. At base functional zero the full base dimensions are 4,4 with sum dimension 4, which excludes the additional end faces. The zero functional exposing the whole sum is covered too. Both P1=D4 x I and P2=(-D4) x I are full-dimensional lattice polytopes in R5.

## Connectivity and exact topology

For the five-index base, only cardinalities (2,2),(2,3),(3,2) qualify. There are 30 minima and 20 maxima. Each minimum has two upper maxima, obtained by assigning its one unused index to either side; each maximum has three lower minima. No chains of length three exist.

Suppress the degree-two minima. The resulting graph consists of signed copies of the ten two-subsets, with A+ adjacent to B- iff A and B are disjoint. The unsigned disjointness graph is connected: distinct intersecting two-subsets have the two-element complement of their union as a common neighbor. Its odd cycle is 01,23,04,12,34,01. A lifted walk flips sign at each step; a detour to this odd cycle and back adjusts parity. Therefore the signed double cover and its subdivision K are connected. Independent exact graph traversal confirms this.

In R5 there are two copies of K, since endpoints differ and no spanning qualifier supplies a comparison. Each component has 50 vertices and 60 edges. Contracting a spanning tree leaves eleven loops, proving each component is homotopy equivalent to a wedge of eleven circles.

The verifier generates every strict chain, constructs its signed alternating boundary and augmentation, checks boundary compositions, and computes ranks over Q with exact Fractions. For the main example C0 has dimension 100, C1 dimension 120, higher groups vanish, and rank(d1)=98. Hence H0=Q^2, H1=Q^22, Hk=0 for k>=2. Reduced beta0=1. The base ranks give Betti numbers (1,11). The tetrahedral control has six isolated order vertices and reduced beta0=5.

For n=5 the printed target is a wedge of three-spheres. Every such wedge, including the zero-fold point, is connected and has zero H1, contradicting both computed groups. Replacing n-2 by n-3 still gives connected wedges of two-spheres with zero H1 and does not repair this example. No genericity modification is settled. For n=3 the six-point control contradicts the printed wedge-of-circles target by disconnectedness.

## Shellability and the zero-dimensional control

Bjorner-Wachs's primary [Shellable Nonpure Complexes and Posets I](https://www.math.miami.edu/~wachs/papers/nonpure1.pdf), Definition 2.1 at printed p.1302 / physical p.4, was freshly read and visually inspected with its empty-face convention. Each new facet must intersect the earlier union in a pure subcomplex of dimension dim(new facet)-1. On the pure graphs here, pure and standard nonpure shellability agree.

A new edge therefore requires a nonempty vertex intersection. In any ordering of the main graph's edges, the first edge in the component different from the initial edge has no vertex intersection with all preceding edges. Its intersection has only the empty face and dimension -1 instead of zero. Thus no ordering can shell the main complex. This is not merely failure of a greedy test.

For a new singleton vertex the required intersection has dimension -1; its intersection with preceding distinct vertices is exactly the empty-face complex and meets this requirement. Thus six isolated points are shellable. The candidate correctly treats the R3 example as refuting homology only.

## Reproducibility, controls, and remaining scope

Both normal and optimized (-O) Python runs completed with exit code zero and byte-identical output. Validation uses explicit exceptions, so optimization cannot remove it. Semantic result SHA256: 7ec6034145d9726a4572683990e10cacc053c1d2e2d02c096a986447b9c203e6.

Controls reject every ordering of two disjoint edges, accept a triangle graph and the six isolated points, verify nonvacuous d1*d2=0 for a filled triangle, and detect an unsigned-boundary mutation. Adjoining an artificial maximum yields f-vector (101,220,120), augmented boundary ranks (1,100,120), and Betti numbers (1,0,0), explicitly testing the cone-realization ambiguity. This does not claim that a cone over a nonshellable complex becomes shellable.

No blocking mathematical gap or required repair remains for the literal printed assertions. This review supplies no novelty/priority conclusion. Source bodies were retained only in memory, and no other individual was contacted. Local report/source-ledger writes encountered ENOSPC after the checker/results/log were saved. The parent explicitly authorized recovery of this report, source ledger, and final log as unreferenced Git-data blobs only; no refs, trees, commits, or PRs are changed by that recovery.
