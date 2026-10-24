# Finite-search research log

## 2026-10-24T19:32:00Z — bounded exact-search contract

Best-guess overall discovery completion: **10%** (universal claim unresolved).

Approach family: exact rainbow Hamilton-cycle search. For each finite group, vertices are group elements and edge color of {u,v} is u+v. A successful witness is one Hamilton cycle through the target subset with pairwise distinct colors. Group operations are exact integers modulo the cyclic factors.

Initial domain: C3, C5, C7, C9, C3 x C3, C11, C13, C15, all subsets of cardinality greater than two. Enumerate every subset containing 0. This is exhaustive up to translation because A-a contains 0 for a in A; translating a cycle shifts every adjacent sum by -2a and preserves distinctness. For a zero-containing subset, fix the first vertex at 0 and remove reversal symmetry by requiring the second vertex to have smaller encoded ID than the final vertex. These are complete reductions, not empirical assumptions.

Success criterion: one explicit witness per covered subset, and a separate verifier that checks both witness validity and exhaustive domain coverage. Failure criterion: DFS exhaustion for a subset; any candidate obstruction requires separate exact confirmation. No absence of counterexamples in this bounded domain establishes the full conjecture.

Implementation: `search.py`, exhaustive depth-first search with color bits and no unproved pruning. Each output line gives the subset bitmask and complete cyclic ordering. Independent checking remains pending.

## 2026-10-24T19:35:01.452388+00:00 — first exhaustive checkpoint

Best-guess overall discovery completion: **15%** (universal claim unresolved).

Complete DFS found a witness for all **22,028** zero-containing subsets in the eight listed groups of odd order at most 15. Search elapsed 5.825 seconds in total (per-group times retained in `exhaustive_order15/summary.json`). Certificate files record every mask and complete cycle. The standalone nonsearch checker `verify.py` independently computes addition from cyclic factors and checks exact mask coverage, cycle permutations, all adjacent sums including closure, and file SHA-256 hashes. All 22,028 passed; report `exhaustive_order15/verification.json`. Root-agent independent audit is pending.

Hardest DFS case: C15 with A={0,1,2,3,4,5,6,7,9,10,11,12,13,14}=C15 minus {8}. Its witness is (0,2,1,3,4,5,7,6,9,11,10,13,12,14), found after 6,015,923 recursive calls. This cost is sensitive to lexicographic branch ordering and does not measure mathematical obstruction. No counterexample appeared.

A larger finite experiment now targets C3^3, C5^2, C3 x C9, C7^2, C3^4, C5^3 with whole groups, all single omissions, all two-element omissions when order<=27, coordinate boxes, coordinate-subgroup coset unions, centrally symmetric samples, and fixed-seed samples in every size. The local-search method is bounded; any unsuccessful run will be labelled UNKNOWN and excluded from witness counts.

## 2026-10-24T19:41:47.417917+00:00 — larger domains and structured construction

Best-guess overall discovery completion: **20%** (universal arbitrary-subset claim unresolved; novelty of elementary construction unassessed).

Exhaustive size-bounded DFS found and the standalone checker validated **313,885** zero-containing subsets of C3³ and **190,026** of C5² in every cardinality 3 through 7, total **503,911**. Exact domains and counts by cardinality are in `exhaustive_sizes7/verification.json`; the generation run took 3.006 seconds in total, and witness checking took approximately 3 seconds. The hardest instances required only 33 and 52 recursive calls respectively; this is branch-order evidence, not an invariant of the subsets.

The larger fixed-seed experiment attempted 4,311 unique group-subset pairs across six group models. Bounded 2-opt local search and an additional bounded conflict-focused-swap rescue were supplemented by exact group translations, natural whole-group cycles, and the exact row-path lifting construction. Every successful cycle was checked by `verify.py` after construction. Final counts are C3³ 806/806, C5² 513/513, C3 x C9 810/810, C7² 431/431, C3⁴ 861/861, C5³ 873/890: **4,294** valid certificates; **17** UNKNOWN cases in C5³. All remaining UNKNOWN cases are full-affine-rank dense random samples, with complement sizes 4 through 9; bounded heuristic failure supplies no evidence of nonexistence. The exact remaining masks and search budgets are retained in `larger_samples/final_summary.json`. The initial search and rescue histories are preserved in `summary.json` and `rescue_summary.json`. Initial per-group local-search times ranged from 0.98 seconds (C5²) to 75.06 seconds (C5³); the conflict-swap rescue took 36.29 seconds for C5³.

An exact construction, `PRODUCT_LIFTING.md`, proves a shared-edge fiber lemma: cut rainbow cycles with the same edge {u,v} to Hamilton paths; place them in group rows; concatenate along a rainbow cycle of row indices. Internal colors have distinct second coordinates 2h and avoid first color u+v; joining edges have that first color and distinct second colors. This proves Cartesian-product closure and the punctured-fiber family (G x H) minus ({0} x D) whenever whole/punctured G cycles share an edge. Explicit bases C5 and C3² suffice for all nearfull F5³/F3⁴ samples with complement size at most three. `product_constructions.py` saved explicit cycles and exact affine-coordinate maps, all checked separately. Novelty is unassessed and root independent adversarial audit is pending.

Checkpoint artifact total: **530,233** checked certificate rows representing **530,155 distinct group-subset pairs** (78 duplicate samples overlap the exhaustive size domains). Strongest verified computational statement is the exact bounded-domain result, plus the separately proved structured product family. No universal proof or counterexample was obtained.

## 2026-10-24T19:43:36.999157+00:00 — computational family handoff

Best-guess overall discovery completion: **20%**. Final structured report `REPORT.md`, exact 17 UNKNOWN masks/complements, reproduction commands, and 16-file certificate manifests are complete. Final all-domain standalone pass checked **530,233 certificate rows** and every manifest SHA-256 hash; report `combined_verification.json`. All processes have completed; no live handles or runaway computation remains. No novelty claim is made for bounded confirmations or elementary product lifting, and no universal resolution is claimed. The parent priority investigation reports earlier bounded checks below 30, so these finite results are reproducibility artifacts rather than first evidence. Root is independently auditing the certificates and mathematical partials.
