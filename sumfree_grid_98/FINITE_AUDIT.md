# Independent adversarial finite-grid audit

Date: 2026-10-20. Scope: the positive-grid finite claims in EXACT_ATTEMPT_1.md and EXACT_ATTEMPT_2.md, the twelve branching certificates, the N=3 reduction, and the computed value f_6(3)=706. No remote publication actions were taken.

## Verdict

**PASS for the stated partial results, not a solution of the general finite-grid problem.** All twelve certified exact maxima survive independent constraint reconstruction, certificate replay, mutation rejection, and Python optimization flags. The N=3 reduction and upward-compression argument are correct. A separately authored exhaustive upset enumerator confirms M_6=41 and hence **f_6(3)=706**. The maximum coordinate-sum slice has 700 points, so global slice extremality is false.

## 1. Branching-certificate audit

`audit_finite_independent.py` does not call the search instance generator to reconstruct constraints. It enumerates each possible target z, then all coordinatewise positive decompositions z=x+y. Edges are frozensets of point indices, rather than the producer's bit-mask accumulation. Repeated summands yield two-element edges and are explicitly retained. The replay is iterative, reconstructs every required branch, checks each packing's pairwise disjointness and avoidance of deleted vertices, and checks the required deletion threshold. Strictly increasing deletion sets make the proof acyclic. An actual lower-bound slice is separately checked against every reconstructed edge.

Verified exact values and numbers of distinct repeated-summand constraints:

| d | N | exact maximum | repeated-summand constraints | visited certificate nodes |
|---|---|---|---|---|
| 2 | 2 | 3 | 1 | 1 |
| 2 | 3 | 7 | 1 | 1 |
| 2 | 4 | 12 | 4 | 1 |
| 2 | 5 | 18 | 4 | 25 |
| 2 | 6 | 25 | 9 | 64 |
| 2 | 7 | 33 | 9 | 6258 |
| 2 | 8 | 43 | 16 | 25114 |
| 3 | 2 | 7 | 1 | 1 |
| 3 | 3 | 23 | 1 | 14 |
| 3 | 4 | 53 | 8 | 20 |
| 3 | 5 | 101 | 8 | 59007 |
| 4 | 3 | 75 | 1 | 14 |

For every certificate, both the original checker and independent replay reject each of: K decreased by one, K increased by one, a zero/nonedge substituted for a packing edge, and a duplicated overlapping packing edge. For every certificate with branching, deleting a required child is also rejected. The complete test suite passed in normal Python, `python -O`, and `python -OO`; output files are FINITE_AUDIT_RESULTS.json, FINITE_AUDIT_RESULTS_O.json, and FINITE_AUDIT_RESULTS_OO.json. Validation is explicit and not assert-dependent.

Caveat: `exact_finite_search.py` still uses an assert for its final witness self-check, which disappears under optimization. This does not invalidate the certified results: their separate certificate/lower-witness replay uses explicit exceptions, and the audit directly checks feasibility. The search script alone should not be described as an optimization-resistant witness validator.

## 2. Exact reduction and compression

The isolated points have both a 1 and a 3 coordinate, and cannot occur in any sum relation. The remaining lower and upper Boolean cubes overlap exactly at the all-2 vector. All relations have disjoint lower index sets, including the repeated empty-set summands. The empty-set-present case has active size at most 2^d; in the empty-set-absent case the center can safely be included and must be counted only once. This validates

f_d(3)=3^d−2^d+max_F(|F|−|D(F)|), with ∅ excluded and [d] included.

For a coordinate compression, any newly created disjoint pair has exactly one shifted member A∪{i}. Its other member B survived in the lower half, so B∪{i} was already present. The old disjoint pair A, B∪{i} has the same union. Therefore D(new F)⊆D(old F); cardinality is preserved. The sum of member sizes increases under every nontrivial compression, proving termination at an upset. No unproved assertion that arbitrary families are already upsets is needed. As a separate finite stress test, audit_compression_independent.py checks every family and every coordinate in dimensions 1 through 4, including all 65,536 families in dimension four; every cardinality and D-inclusion check passes under -OO (FINITE_AUDIT_COMPRESSION.json).

## 3. Independent verification of the 706 optimum

The original comparable-pair recurrence and its upper-union formula are correct. The Python verifier's early stopping is safe: it stops only after exhibiting enough actual distinct unions to prove the desired upper bound, not after assuming an optimizer's answer. I reran it under -OO; FINITE_AUDIT_UPSET_REPLAY.json records all 7,828,354 upsets and all 7,828,352 admissible ones.

For a genuinely different enumeration route, `audit_upsets_independent.cpp` visits subsets in descending integer order. At each subset it branches on exclusion, and permits inclusion only if every immediate strict superset has already been included. This uniquely generates every upset without generating comparable pairs of smaller upsets. It maintains D incrementally by taking disjoint unions of the newly included member with earlier members; the empty member's self-union is included explicitly. No floating-point bound or assert is used.

The output FINITE_AUDIT_UPSETS.txt gives counts 3, 6, 20, 168, 7581, 7828354 and maximum deficiencies 1, 2, 4, 10, 20, 41 in dimensions 1 through 6. Thus the f_d(3) values 2, 7, 23, 75, 231, 706 are independently verified. The simple threshold |A|≥3 attains deficiency 42−1=41 in dimension six, matching the exhaustive upper bound.

Separately, the finite audit script reconstructs the 700-point slice and the six added permutations of (3,1,1,1,1,1). It verifies all 498,436 ordered pairs, including equal points, against the 706-point set. It also checks every integer slice threshold, whose maximum is 700. Real endpoints cannot improve that maximum because rounding a lower endpoint upward produces a containing integer-threshold slice. Hence this is a counterexample to finite coordinate-sum slice extremality, not merely a solver anomaly.

## 4. Source-hypothesis audit

The primary source [Frankl–Kupavskii, Partition-free families of sets, arXiv:1706.00215v1](https://arxiv.org/html/1706.00215v1), Introduction, Theorems 1 and 2, was inspected directly. Theorem 1 requires d=3m+1 with positive integer m. Theorem 2 requires m≥6 for d=3m or 3m+2. Its abstract alone does not supply the small cases. These yield the report's claimed ranges d≡1 modulo 3 with d≥4, and all d≥18. The set-family upper bound applies because F\D(F) is partition-free and |F|−|D(F)|≤|F\D(F)|. The rank-threshold lower bound matches it. This audit checks the theorem statement and application, not every proof line of the cited paper.

## 5. Limits and remaining gaps

- The exact result 706 supersedes EXACT_ATTEMPT_1.md's chronological statement that its upper optimality was not yet established; that file should retain its attempt-specific scope or link to attempt 2 to avoid confusion.
- The N=3 dimensions 8,9,11,12,14,15,17 remain outside the theorem and computations used here. No inference from the source abstract closes them.
- The generic finite problem for N≥4 is unresolved by these arguments. Small certified cases are not a general structural theorem.
- No novelty claim is established, and no claim of an absence of other literature is warranted.
- This audit does not certify the separate asymptotic manuscript or its repairs.
- C++ enumeration uses 64-bit masks and is designed only through dimension six. Extending its loop to dimension seven without changing representation would be invalid.

## 6. Extension audit: attempts 3 and 4

**PASS with the corrected threshold hypotheses.** The isolated-point characterization for N≥2 is exact. A point with no N coordinate is a summand with the all-1 vector, and a point with no 1 coordinate is a target of the all-1 vector plus a positive vector. The inclusion-exclusion count and cumulative J(s) correctly treat the shifted inner cube. These are counting translations, not translations of a sum-free set.

The outer-shell identity is valid: no shell point can be a summand, so after fixing a sum-free interior F the only forbidden shell points are exactly (F+F)∩T. Thus all other shell points can be added simultaneously. This identity does not reduce to a recurrence in the scalar f_d(N−1), and does not prove a universal optimum for completed slices.

The construction B_t is sum-free, including all new-new cases. Its low added points can never be summands and have too low a rank to be targets of slice/high points. Its high added points cannot be targets and have too high a rank to create slice targets. The exact displayed B_t count follows by separately counting the three disjoint pieces.

`audit_boundary_independent.py` reconstructs every forbidden edge for d=1,…,4 and N=2,…,6, then checks every threshold t for B_t sum-freeness, the isolated classification, and the isolated-completion count. For each threshold satisfying d≤t, 2t≤dN+1, and dN≤4t−2, it checks that every omitted point completes a forbidden edge with points already in B_t. All checks passed under -OO; output is FINITE_AUDIT_BOUNDARY.json.

The corrected maximality proof is sound: for an omitted low point of rank r, the available coordinate box for y has ranks d,…,dN−r and contains t under 2t≤dN+1. Then y,w+y lie in the slice. For an omitted high point, positive coordinate splits realize all possible ranks d,…,r−d, and 2t≤r≤4t−2 guarantees both summands can lie in the slice. Repeated summands are allowed. Without the second threshold condition the earlier claim was false: d=1,N=3,t=3 gives B_t={3}, to which 2 can safely be added. Inclusion-maximality must never be substituted for maximum cardinality.

Independent convolution of the coordinate rank distributions, without the binomial inclusion-exclusion formula, verifies every numerical comparison in attempts 3 and 4. The code audit_boundary_counts.py and FINITE_AUDIT_BOUNDARY_COUNTS.json confirm in particular [11]^3: plain 991 versus isolated-completed 992; [29]^3: isolated 17420 versus B_t 17423; and [100]^3: isolated 699658 versus B_t 699788.

The asymptotic obstruction also passes. For d≥3 the derivative computation gives strictly increasing slice volume through u=1 and positive derivative there, so all continuum maximizers are separated from [0,1]. Uniform lattice error bounds transfer this separation to all largest integer slices. The fixed face x_1=N with every other coordinate between 2 and floor(εN) then supplies Ω_d(N^(d−1)) omitted low points, all simultaneously addable and non-isolated. Since there are only O_d(N^(d−2)) isolated points in total, the improved family eventually beats every isolated-completed slice as well. This proves a boundary-scale lower-bound improvement, not an exact optimum or a changed leading density.

## 7. Extension audit: attempt 5

**PASS as a negative/local-search report, not as a global upper bound.** The shell-profile inequality is precisely the missing statement needed for the proposed boundary candidate to be universally optimal. The zero-based-cube slice interpretation is a counting identity and is correctly not promoted into a structural equivalence.

Both obstruction examples are valid. The maximum sum-free sets {2,3} and {3,4} in [4] have different extension scores at shell {5}. Simultaneous successor compression of the sum-free {1,3,5} gives {2,4,5}, which contains 2+2=4. These disprove the proposed shortcuts, not every possible refined induction or compression.

The three blocker classes in search_boundary_trades.py are exhaustive: an omitted w can occur twice as a summand, once as a summand with an old point, or as the target of two old points (possibly equal). A deletion makes w admissible exactly when it hits every blocker. For a pair of individually admissible additions, the code checks their sum, both differences against the remaining set, and both repeated-new-summand relations, then revalidates any positive witness. The implementation is logically sound for this move class.

For additional independence, audit_trades_independent.py reconstructs all edges target-first and groups those having exactly one omitted vertex. It intersects their old-vertex subsets for each omitted point, rather than using the original per-point blocker formulas. All twelve reported instances independently have empty blocker intersections at every omitted point. The -OO results are FINITE_AUDIT_TRADES.json. Thus no single deletion permits even one omitted point in these selected sets; in particular no one-deletion/two-addition improvement exists.

This is only local stability. It neither excludes multi-deletion trades nor certifies the global optimality of B_t. The broader floating-point MILP exploration and non-exported integer searches are outside this audit's certified exact-value bundle and are omitted from this publication package. The unrestricted finite problem is still unresolved by these five attempts.
