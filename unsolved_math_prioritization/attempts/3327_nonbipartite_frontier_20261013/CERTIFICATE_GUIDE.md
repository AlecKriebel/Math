# Independent checking guide: complete order-15 exclusion

The [full finite report](FINITE_REPORT.md) gives the complete mathematical generation argument. The [full structural report](STRUCTURAL_REPORT.md) gives the unbounded combinatorial proofs. This guide specifies the certificate semantics and separates them from enumeration completeness.

## Generate every rooted labeled completion

Choose the root 0 and its independent neighbors 1,2,3,4. The pair-label graph is one of C4, K4 minus an edge, or K4. In these patterns use respectively the pairs (1,2),(2,3),(3,4),(1,4); all six pairs except (1,2); or all six pairs. Add exactly 3−deg(i) singleton labels {i}, and then n+p−17 separately labeled empty labels. An impossible negative empty-label count rules out the pattern. Add the prescribed root and label edges.

Every unknown edge lies between remaining vertices, whose required residual degrees are 4 minus their label sizes. Process those vertices in order, visiting every subset of later candidates of the required size. Forbid intersecting endpoint labels, triangles, and codegrees above two. Test triangle and codegree restrictions after every added edge. A necessary available-neighbor bound may prune only when too few individually permissible remaining neighbors exist. It may be omitted in an independent replay. There is no unproved isomorphism reduction.

At each degree-four leaf enumerate all unoriented squares, and retain exactly those with two or three squares per edge. Compare the full adjacency lists for every survivor, not merely their number or hashes. Per order and root pattern, the completion and square-survivor counts must be exactly the table in the report and [certificate](ENUMERATION_CERTIFICATE.json). The total is 3,354 completions and 37 square-rich survivors. Certificate adjacency objects prove the stated surfaces or exclusions; completeness additionally requires the generation argument and exhaustive replay.

## Check every exact graph certificate

Check n vertices, symmetric adjacency, no self-loops or repeated neighbors, degree four, connectivity, no triangles, and at most two common neighbors for every distinct vertex pair. Enumerate squares and pentagons independently using subsets and permutations, and compare all reported counts and the full edge list failing the pentagon condition.

For each nonnull omitted-square list, check that its distinct entries are actual graph squares and cover every three-square edge exactly once and no two-square edge. Attach disks to all other graph squares. Every edge must meet exactly two distinct square boundaries. At each vertex construct the link on its four incident ends, and require a connected simple C4. Verify that the number of retained squares equals n, giving Euler characteristic zero for the connected closed surface. The quartic triangle-free density lower bound gives E≥2, and the surface gives E≤2.

The surface is orientable exactly when its square orientations can be assigned consistently with opposite traversal directions across every shared edge. This produces 19 torus certificates and 12 Klein-bottle certificates. Those labels concern the supplied surfaces, not minimum nonorientable genus.

Each of the six null-cover graphs must have an independently recovered bipartition and no pentagon. Those facts exclude the required pentagon condition without any need to trust a failed exact-cover search or identify the graph by name. All 31 covering survivors pass the numerical pentagon filter.

## Exact controls and scope

Certificate checks must reject duplicate adjacency, a missing omitted square, a false pentagon count, and a duplicated omitted square even when all byte-level hash checks are bypassed. Generation must reject missing or duplicated survivors and altered completion counts. Essential tests use explicit failures and must still run under normal Python, -O, and -OO.

The structural proof establishes the pentagon restriction, independence of full-link vertices, exactly two complementary edges, forced square decomposition, and residual cycle divisibility. Finite endpoint-link and radial controls corroborate the proof; they do not enumerate arbitrary graphs. A residual six-cycle is not separately excluded: divisibility applies to the sum of residual cycle lengths. Nothing here decides existence at order 16 or above, higher-genus targets, or the orientably simple Euler-critical route.
