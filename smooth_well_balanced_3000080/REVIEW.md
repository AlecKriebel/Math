# Independent scope and reduction review

Reviewed 2026-10-19. Read-only research; no remote publication.

## Scope verdict

**Resolved previously, NP-complete; not a new solution.** The [primary EGRES problem](https://oldlemon.cs.elte.hu/egres/open/Smooth_well-balanced_orientations_with_prescribed_in-degrees), revision 2474, expressly credits Hörsch–Szigeti. Its question requires smoothness, well-balancedness, and indegree strictly below outdegree on a specified subset T of odd-degree vertices. It does not require prescribing either sign outside T. The page records modification on 12 June 2022.

## Proof inspection

Read the [author-hosted published paper](https://pagesperso.g-scop.grenoble-inp.fr/~szigetiz/articles/CFWBOWUB_HSz.pdf), DOI [10.1007/s10878-022-00962-y](https://doi.org/10.1007/s10878-022-00962-y), through §3.7. Theorem 6 concerns upper-bounded best-balanced orientations. Its cubic-vertex-cover reduction normalizes orientations using Eulerian reversals, extracts selected vertex gadgets, and enforces the budget at hub a. Section 3.6 adds 2k leaves at a; only degree-three vertices Z retain nontrivial outdegree bounds, namely one.

The normalization checks out: the disjoint b-to-a paths saturate all 6n possible Z exits, enabling the first circuit reversals; the second reversal is Eulerian because its opposite path families have equal cardinalities. Degree saturation forces the remaining convenient directions. The hub count is 8n+|U|. Leaf balancing makes its final outdegree 8n+k without changing old-pair connectivity.

Lemma 1 contains apparent path-label slips: use q_j^v rather than q_i^v for v's incidence; the u-side path to y^e traverses q_i^u,x^e,y^e. These repairs follow existing edges and preserve arc-disjointness. No substantive gap found. For polynomial size, dispose of k≥|V(H)| as trivial before adding 2k leaves.

## Exact sign bridge

Independently checking the interpretation: reverse every arc of the constructed orientation. A degree-three z with outdegree 1 then has indegree 1 and outdegree 2. Set T=Z. Smoothness is unchanged. For every ordered pair (u,v), connectivity after reversal equals the former connectivity from v to u, while undirected connectivity is symmetric. Thus well-balancedness is unchanged, and the transformation is an involution. This gives exactly the original EGRES requirement, not its opposite.

Verification level: full extracted proof inspected and critical algebra/sign mapping reconstructed. Not a formal proof-assistant verification or exhaustive computational test. PDF screenshot requests failed with a cache-miss error; visual verification was not claimed. Standard Menger and cubic-vertex-cover hardness remain cited foundations.
