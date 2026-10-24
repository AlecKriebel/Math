# 21.124 tubular approach research log

## 2026-10-24T22:15:48Z — independent start

Target: an explicit CAT(0) free-by-cyclic tubular group with no finite-index RAAG embedding, or a complete positive mechanism. This family investigates multi-vertex, overlapping-cycle graphs, independently of the other current 21.124 families. Discovery completion estimate: **1%**; no result or publication claim.

Read the project policy and the authoritative priority/source contracts. Read the primary Euclidean-by-finite criterion in Merladet Urigüen–Minasyan 2505.18054v3, Theorem 1.6, and the cycle-disjoint positive theorem in 2511.21293v1, Corollary 1.4. Single-vertex CAT(0) free-by-cyclic groups are prior positive results by Wu–Ye 2504.14192v2, Theorem 4.5. Neither an infinite planar holonomy calculation nor failure of cocompact cubulation is enough for our target: finite holonomy can act in a larger Euclidean dimension, and noncompact special models are allowed.

Initial mechanisms:

1. Exact height-compatible Gram matrices on theta and denser two-vertex tubular graphs; determine which candidate constraints really permit a geometric CAT(0) action and a finite-rank free kernel.
2. Nonquadratic finite-orbit obstructions to the Euclidean-by-finite criterion, retaining arbitrary representation dimension and arbitrary finite covers.
3. A positive common-height construction, if CAT(0) forces compatible horizontal data. Its exact potential gap is whether quadratic metric compatibility can produce a finite orbit of wall directions, rather than merely an infinite orthogonal representation.

No outreach, git operations, or publication occurred in this subtask.

## 2026-10-24T22:26:43.892087+00:00 — theta positive partial and Pell obstruction

Discovery estimate toward a complete21.124 resolution: **6%** (high uncertainty). The research has produced checkable partial mechanisms, not a full solution.

- THETA_SUBCLASS.md proves an explicit R²⋊C₂ vertex-injective representation for every CAT(0) two-vertex/three-edge tubular theta admitting an edge-nonzero height. A rational sign lemma handles every degeneration except the three-equal-length collinear configuration excluded by CAT(0). check_theta.py passed50,625 rational grid cases. Root assigned a fresh nonauthor adversary; these mathematical files are frozen for review.
- PELL_CANDIDATE.md gives an exact eligible CAT(0) F₅-by-Z group on a two-vertex/four-edge graph, using the correct pairs(3,2),(20,14),(119,84). The initially typed pairs did not satisfy the equation; the checker caught this and the correction was immediately sent to root before promotion.
- The candidate excludes elementary abelian2 linear holonomy in every dimension. A separate new ABELIAN_HOLONOMY_DELTA.md extends this to every finite abelian linear holonomy using a six-term determinant, a proved Mann bound, and216,000 exact cyclotomic tests. This extension awaits fresh review.
- An exhaustive finite-permutation search up to simultaneous conjugacy found no witness in transitive permutation degree≤5 (counts1,7,94,2598,92672). Modular full rank at prime65521 proves absence in each enumerated case overQ; neither the search nor the abelian theorem covers arbitrary nonabelian finite holonomy.

Precise central gap: excluding nonabelian finite holonomy for the candidate, or constructing one such witness. A route that merely assumes the remaining Euclidean-by-finite nonexistence is **blocked** as a transfer of the central difficulty. Infinite planar holonomy and bounded-index failures are also blocked as full negative mechanisms. Further work must add a new unbounded group/representation argument or an exact positive witness.

Source provenance: primary2505.18054v3 Theorem1.6/Proposition1.10,2511.21293v1 Corollary1.4,2504.14192v2 Theorem4.5 and§2; Mann1965 DOI10.1112/S0025579300005210 bibliographic metadata verified at the publisher. The needed Mann bound is proved in the note, not inferred from an inaccessible theorem page. No originality, human-review, or publication claim.
