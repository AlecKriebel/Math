# Reproduction scope, finite counts, and negative controls

## What this edition supports

The complete mathematical proofs, dependency/application reasoning, and small authored examples are distributed. They can be read without the original computation or any earlier-round packet. Independent implementations can construct the specified cube, grid maps, high-degree graph, sharp switching example, sealed core, and additional small examples directly from this prose.

The original generator implementations, random seeds, large retained authored sample collections, programs, logs, and runtime/control artifacts are not distributed, nor are their names, sizes, hashes, or operational identifiers. This edition alone therefore cannot reproduce the exact original seeded streams or replay all 33,400 original records. It reports previously audited finite evidence and complete scope honestly; it does not present aggregate counts as a replacement for missing input records. Public dataset URLs and identity metadata are separately available in SOURCES.md without their contents.

For an independent implementation, use explicit runtime failures rather than assertions; reject missing inputs, unexpected inventory, malformed graphs, invalid label types, false flags, and incorrect witnesses. Verify every claimed source identity against the actual bytes before and after replay. Hash agreement establishes input identity, not mathematical truth. Optimization-mode success without actively failing negative controls does not establish semantic checking.

## Small-complement finite experiments

The universal claims rest on the written proofs. Computational corroboration used the following exact scopes.

- The cube has 186 same-parity subsets of size at most three, of which 130 have a common neighbor; the antipodal-pair neighborhood identity holds at all 16 cube vertices.
- Exhaustive bipartite edge subsets for same-side disjoint demands on side sizes (4,4): 65,536 subsets, 6,561 triangle-free valid cases, maximum degree seen 5.
- Opposite-side disjoint demands on side sizes (4,4): 65,536 subsets, 9,072 valid cases, maximum degree seen 4.
- Shared-endpoint demands on side sizes (3,3): 512 subsets, 125 valid cases, maximum degree seen 5.
- Total valid degree-free two-demand instances: 15,758. An additional 81 zero-/one-demand cases included long paths and swapped sides.
- Independent grid coverage: 600 compatible authored cases over six rectangle shapes, every case including a terminal-free component. Folding adjacency was checked 4,020 times for dimensions 1 through 20 and integer inputs −100 through 100. Negative fold arguments were explicitly tested; generated compatible envelopes did not happen to produce negative final coordinates.
- Mixed three-demand exhaustive checks: all 256 bipartite edge subsets at side sizes (4,2), with 49 valid cases; all 32,768 subsets at side sizes (5,3), with 2,070 valid cases. Every valid case also had a side-swapped witness.
- Signed algebra: 256 palette/cube equivalences, all eight negative triangle sign-product identities, and targeted same-sign duplicate and opposite-sign parallel fixtures.

### Seeded mixed three-demand cases

All four groups use side distribution 2+1 and 1,000 cases each. Regenerated streams matched the retained references. The edge-count histograms (edge count: number of cases) are:

- Order 10: 11: 1, 12: 25, 13: 219, 14: 755.
- Order 14: 17: 1, 18: 22, 19: 210, 20: 767.
- Order 20: 27: 11, 28: 157, 29: 832.
- Order 40: 57: 14, 58: 109, 59: 877.

### Supplied catalog checks

Every normalized cut of the exact 141 supplied public records was examined: 949,536 cuts in total. A normalized cut keeps one fixed vertex outside the chosen side. The small-complement and one-sided counts below may overlap; they are not summed as distinct cases.

- Order 6: 1 supplied records; 32 normalized cuts; 1 matching complements of size at most three and 1 one-sided matching complements verified. Maximum signed-search nodes: 4.
- Order 8: 2 supplied records; 256 normalized cuts; 5 matching complements of size at most three and 1 one-sided matching complements verified. Maximum signed-search nodes: 5.
- Order 10: 6 supplied records; 3,072 normalized cuts; 19 matching complements of size at most three and 9 one-sided matching complements verified. Maximum signed-search nodes: 6.
- Order 12: 22 supplied records; 45,056 normalized cuts; 57 matching complements of size at most three and 17 one-sided matching complements verified. Maximum signed-search nodes: 7.
- Order 14: 110 supplied records; 901,120 normalized cuts; 290 matching complements of size at most three and 108 one-sided matching complements verified. Maximum signed-search nodes: 8.

The totals are 372 small matching complements and 136 one-sided matching complements. Catalog generation completeness and nonisomorphism were not audited. The original checker's optional missing-input branch was not accepted as completion of these advertised checks.

### Larger authored one-sided cases

There were 50 cases for each of the following six (order, demand-count) pairs, for 300 total. Every group attained reduced signed degree eight, and independently regenerated streams matched their retained references. The following duplicate and opposite-sign counts describe the aggregate constraints across each 50-case group:

- (20, 6): 260 same-sign duplicate constraints removed; 221 opposite-sign parallel pairs retained; maximum signed-search nodes 7.
- (30, 9): 225 same-sign duplicate constraints removed; 217 opposite-sign parallel pairs retained; maximum signed-search nodes 10.
- (40, 12): 241 same-sign duplicate constraints removed; 204 opposite-sign parallel pairs retained; maximum signed-search nodes 13.
- (50, 15): 206 same-sign duplicate constraints removed; 186 opposite-sign parallel pairs retained; maximum signed-search nodes 16.
- (60, 18): 246 same-sign duplicate constraints removed; 226 opposite-sign parallel pairs retained; maximum signed-search nodes 19.
- (100, 30): 202 same-sign duplicate constraints removed; 196 opposite-sign parallel pairs retained; maximum signed-search nodes 31.

### High-degree graph and terminal checks

All 16,384 normalized cuts of the 15-vertex, 35-edge graph were examined. The unique normalized maximum has mask 127 and size 32. The bipartite edge connectivity is four; all 16,383 nontrivial normalized switching inequalities are strict. Its degree sequence has eight fours, six fives, and one eight.

All 512 normalized even-terminal assignments were tested. None supports all eight transversals; the maximum supported is four. The support histogram is: one supported transversal for 8 assignments, two for 168 assignments, and four for 336 assignments. Exactly 48 assignments meet all pairwise non-antipodality restrictions. All 28 pair-separation witnesses for the unrestricted addendum and the Clebsch target's degree-five, loopless, triangle-free properties were checked.

### Thirty-two active negative controls

The independent small-complement suite rejected all of the following in normal, -O, and -OO modes, and accepted restored positive inputs:

1. Wrong expected input byte count
2. Wrong expected input digest
3. Missing required input
4. Graph loop
5. Duplicate edge
6. Out-of-range endpoint
7. Triangle
8. Invalid cut label
9. Boolean masquerading as a cut label
10. Subcubic degree overflow
11. Nonmatching one-sided demands
12. Demand on the wrong cut side
13. Invalid unit-edge witness
14. Invalid antipodal-edge witness
15. Boolean masquerading as a cube label
16. Incompatible grid terminal parity
17. Incompatible grid terminal distances
18. Terminal outside the rectangle
19. Zero grid dimension
20. Cut graph inconsistent with cut labels
21. Empty graph6 record
22. Non-ASCII graph6 bytes
23. Unsupported extended graph6 order
24. Short graph6 payload
25. Extra graph6 payload
26. Nonzero graph6 padding
27. Missing declared integrity metadata
28. Tampered declared integrity metadata
29. Tampered addendum content
30. Tampered main content
31. Unexpected inventory entry
32. Missing required addendum content

An AST inspection found no assertion statements in the independent checker. Its outcomes agreed byte-for-byte across all three modes. By contrast, the original assert-based symbolic checker rejected an invalid cube witness normally but accepted it under both optimization flags; those optimized original runs receive no semantic-validation credit. The original normal parser also lacked the strict graph6 padding/byte checks and mandatory input pins of the independent checker.

## Switching finite evidence

The complete family parameter lists, within-family and cross-family duplicate counts, all 33,400/33,386 totals, and the distinction between 1,600 globally certified cuts and 31,800 other records are in SWITCHING_AUDIT.md. These are deterministic constructed samples, not exhaustive or uniform random samples or nonisomorphic catalogs. The interrupted next rejection-based group was excluded in full and supplies no coverage or negative result.

The abstract induced-pattern calculation used every internally feasible pattern with cubic boundary stubs and matching saturation, including patterns possibly lacking a global completion. For sizes one through four, the total feasible counts were 2, 13, 128, 1,816; counts satisfying the endpoint cut-degree condition were 2, 13, 125, 1,681, with maximum gains −1, 0, −1, 0. The finite superset check supplements the universal written proof.

The sharp graph's 32,768 normalized cuts gave maximum 22 and the sole maximizing mask 26982. The core normalization was checked in all 384 translation/direction cases. A separate normalized finite backtracking check tried 304 candidate labels and found no fixed-class extension; the hand proof already establishes nonexistence, without a solver-exhaustion assumption.

All original constructed witnesses were checked edge by edge. Full deterministic generation reproduced all four complete outputs and corresponding search logs on the tested compiler/runtime, with no compiler diagnostics. This establishes the reported local reproduction, not cross-platform identity of standard-library shuffling. No interruption, partial group, timeout, or unretained sample was treated as unsatisfiability.

### Eighteen active switching negative controls

The independent switching suite rejected: wrong witness; out-of-domain label; false extension flag; duplicated edge; missing edge; loop; changed cut side; wrong pentagon count; changed stability flag; wrong defect; changed cut breakpoint; missing declared input; extra file; extra empty directory; changed payload bytes; altered declared inventory count; truncated certificate input; and symlink substitution. Restored positive controls passed. All controls remained active under normal, -O, and -OO modes, with byte-identical outcomes.

The original switching verifier checked mathematics and record counts but did not itself enforce the original complete inventory or integrity metadata. An independent fail-closed wrapper supplied that boundary. Original mathematical replay, independent integrity checks, deterministic sample generation, hand proofs, and source-lineage checks remain distinct kinds of evidence.

### Small-defect group stability counts

Of the 18,000 small-defect records, 9,184 satisfy the exact three/four-stability invariant. Each following group has 1,000 records; the listed number is the count satisfying that invariant:

- (n,m)=(14,4): 212.
- (n,m)=(14,5): 0.
- (n,m)=(16,4): 346.
- (n,m)=(16,5): 0.
- (n,m)=(18,4): 518.
- (n,m)=(18,5): 141.
- (n,m)=(20,4): 570.
- (n,m)=(20,5): 290.
- (n,m)=(22,4): 640.
- (n,m)=(22,5): 410.
- (n,m)=(24,4): 726.
- (n,m)=(24,5): 514.
- (n,m)=(28,4): 807.
- (n,m)=(28,5): 657.
- (n,m)=(32,4): 854.
- (n,m)=(32,5): 745.
- (n,m)=(40,4): 898.
- (n,m)=(40,5): 856.

All 1,600 pentagon-family, 9,000 rejection-based stable, and 4,800 direct stable records satisfy that invariant. Local stability does not imply global optimality.
