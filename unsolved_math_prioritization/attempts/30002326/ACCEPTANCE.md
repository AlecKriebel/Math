# Acceptance of the homometric flower partial result

Problem 30002326 / OWR-12481-016. Edition dated 10 October 2026.

## Verdict

Accepted as a partial result under the operational convention: h(G) is the largest common size of two disjoint sets with identical multisets of ambient pairwise distances, and h(n) is the minimum of h(G) over connected n-vertex finite simple unweighted graphs. No mathematical correction to the original report is required. The differently quantified universal exact-size convention is not presumed equivalent.

For every integer n >= 20736, the explicitly constructed flower G_n satisfies

h(G_n) = floor((n - floor(log_2(log_12 n)) + 3)/4).

The proof checks every integer order, parity, the enlarged final clique, both root states in the cone, the j=0 boundary, path vertex counting and every residue modulo four. The exact cone formula requires k >= 2. Flower localization holds for pairs of size at least four; the size-three P_3 exception is retained. Threshold four was already corrected in the revised Axenovich–Özkahya manuscript.

Uniformly over flowers with nonempty core H and tail order m >= 2, writing q = |V(H)| and n = q + m, one has h(F(H,m)) = max(q,m)/2 + o(n). Their minimum ratio tends to 1/4. This conclusion relies explicitly on the graph-uniform equal-order/equal-edge-count theorem of Bollobás–Kittipassorn–Narayanan–Scott. The audit checks that theorem's statement and application, not an independent proof of the entire published theorem.

The necessary maximum-degree o(n), diameter o(n), and absence of linearly large two-distance subsets for a hypothetical sublinear sequence are also accepted. The eight-vertex example establishes noninheritance within specified pairs only; other homometric triples exist in that graph.

## Limits and credit

Neither a proof nor a disproof of h(n) = o(n) is supplied. The flower obstruction is not a global positive linear lower bound. The cone formula is not extended to k = 1, and the arbitrary-multicolour theorem is not assumed. No equivalence or inequivalence of the global extremal conventions, novelty, priority, or exhaustive current-literature conclusion is certified.

Albertson–Pach–Young receive credit for the connected question and kite mechanism; Axenovich–Özkahya for flower localization and rapidly growing odd-clique cores, with their credit to Caro–Yuster preserved in the audit; Bollobás–Kittipassorn–Narayanan–Scott for the theorem used in the flower obstruction; and Alon for the compatible polylogarithmic lower bound. Full public citations and version distinctions appear in the report, audit and source metadata.

This is an independent internal AI mathematical and source-credit audit of an AI-assisted research note. These authored documents are unrefereed. Acceptance here is not external human peer review, journal acceptance, or formal proof-assistant certification. Finite diagnostics supplement the proof and are not a hidden proof dependency.

The original report's 16,408 bytes were recovered exactly. The original full bundle and complete historical verification record were not restored. The separately inventoried independent audit records recovered public-source identities and fresh diagnostics. Publication preparation retains those limits and makes no new source-inspection claim.
