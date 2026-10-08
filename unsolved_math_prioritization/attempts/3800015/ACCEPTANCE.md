# Acceptance of public partial results

## Decision

Accept the five independently audited partial routes, with the source/output clarification mandatory in this public delivery. The general problem remains unresolved: no exact subquadratic algorithm from implicit line equations and no quadratic lower bound for unrestricted algorithms has been proved. Disposition: exhausted, 5/5. No additional proof-search route is introduced by publication or regression verification.

## Accepted mathematical scope

The setting is distinct complete affine lines with equal Euclidean travel cost and no deleted portions. Parallelism and concurrence are allowed; coincident descriptions must first be merged. Endpoints are finite arrangement vertices. The operation model is exact real RAM, explicitly including square roots and comparison of accumulated lengths, not polynomial-bit computation for arbitrary sums of radicals.

1. Every geodesic has connected intersection with each input line. For distinct endpoints, its fully expanded edge count q satisfies q <= n - |I(s)| - |I(t)| + 2 <= n - 2. This applies to every shortest path and is sharp, including straight-through intermediate vertices. A short output is not a method for finding it in subquadratic time.
2. Common-side half-plane and optimum-ellipse restrictions can retain quadratically many grid vertices. Ordinary minimum-priority vertex-expanding A* with the Euclidean heuristic must expand quadratically many strict-priority vertices in the specified family. These are limitations of those particular methods, not lower bounds on unrestricted algorithms.
3. The direction-only relaxation has exact value 91/5 in the five-line fixture; the true optimum is 21; the best one-bend route costs 65/3. The two-edge hop witness passes through C intersect D = (79/7, 209/21). The other one-bend route through A intersect B crosses the horizontal line twice and expands to four edges. author/CORRECTIONS.md and adjacency regressions preserve this distinction. Two-direction distance/compressed paths admit a linear scan, while expanded ordered output may require sorting.
4. Exact labels on one line form a lower envelope of V-functions and are 1-Lipschitz, but need not be convex: the fixture has values 5, 6, 5. The recurrence assumes global entry-site distance labels already known; it is not by itself a new global shortest-path algorithm.
5. The comparison-sorting lower bound applies to fully expanded ordered edge output on the stated unsorted-input family. It does not apply to that family's distance or compressed answer, and path-counting alone is not a general algebraic decision-tree lower bound.

## Sources and unresolved conventions

The 2003 grid-like two-pencil results are attributed to Hart and Kavitha–Varadarajan. Their exact hypotheses and opposite-corner endpoints matter. The imported general quadratic upper bound is neither reproved nor implemented here. Hart summarizes the orientation-sensitive 1999 result as O(n log k+k²), while Kavitha–Varadarajan and Eppstein's bibliography state O(n+k²). The full 1999 paper was not inspected, so its input grouping and output conventions remain unverified. Input orientation grouping and sorting expanded output are separate issues. SOURCE_OUTPUT_CLARIFICATION.md is part of the accepted report.

The 2020 thesis identity and deposited abstract were inspected, not its full PDF. No thesis-PDF hash, size, theorem, or approximation guarantee is certified. Historical pages and bounded searches do not prove present-day openness. These restrictions are preserved in both inventories and the independent audit.

## Execution and negative controls

The native suite checks 6,531 ordered distance queries, seven grid cases, and 120 sorting permutations. The independent suite reconstructs geometry by substitution and pairwise no-interior-vertex adjacency, uses layered Bellman–Ford, checks 7,828 ordered distances across 36 arrangements, verifies 300 metamorphic queries, and enumerates 890 shortest-path DAG paths across six small tie fixtures (including trivial paths).

Six deliberate semantic corruptions fail the original positive suite in normal, -O, and -OO modes: taxicab metric, skipped intermediate vertices, hop weights, missing reverse adjacency, obsolete hop witness, and an overstrong edge bound. Disabling the edge-bound or connected-intersection guard survives the original suite; both weakened guards are detected by the added adversarial fixtures. We do not claim eight original-suite rejections. The full-stream driver checks exact expected rejection causes and captures complete subprocess outputs; the missing-reverse-adjacency corruption produces the documented KeyError from malformed directed adjacency, rather than a dedicated geometric exception. Other mutants have the explicit documented RuntimeError causes. Neither arbitrary crashes nor an unqualified nonzero exit count as a substitute for those pinned outcomes.

Fresh normal/-O/-OO execution requires actual/effective UID 1000 and performs existing-file/new-file probes in the author directory, audit directory, delivery root, and working directory. Isolated subprocesses disable site imports and bytecode. The entire observed mathematical output and full normalized mutation streams are compared against fixed expected bytes/objects; outer stdout is also compared byte-for-byte. The hostile test suite targets every public member (including acceptance and receipts), queue tampering, inventories, symlinks and special files, manifest type substitutions, duplicate keys, nonfinite numbers, and weakened output comparisons.

Finite rational checks are evidence only. They neither enumerate arbitrary real arrangements nor provide a formal proof or novelty certificate. Source and corpus bytes are not bundled; absent optional checks, fresh retrieval, fresh source inspection, and fresh record joins remain NOT_RUN.

## Provenance and exact public boundary

The author manifest SHA-256 is 72d1f923599313b4f16be9505587277ac47aa232293972a7ef9737f99b82c23c; the audit manifest is 821347924d6ef299cdb84be9a7acbf5f28def364ad6b367898988c0b43860435. All original entries are present and unchanged. The report SHA-256 is bcd9f1b7e1db3e5add9db270adba50fc68fac1f94dc032979d6172b690f8dde7; native verifier SHA-256 is 842c4114b5440b68a11a6f948f3662aaedea9acde903c6814e6aeddc6d857903. Public additions are authored acceptance, mandatory clarification, reproducibility code, expected outputs, and verification metadata only. This does not authenticate omitted source documents or any private working collection.

The draft-PR change is restricted to this target directory and the current problem's QUEUE Status, Turns, and Findings cells. All other queue bytes, existing links, notes, and the initial literal SHA line are preserved. Publication creates no release, DOI, merge, or external outreach.
