# Independent audit: OPG-605 / problem 3075 / rank 925

Audit date: 2026-10-06 UTC. Disposition: **accept the mathematics as a partial, unsolved result at 3/5 approaches; accept the repaired derivative for reproducible replay.** No full solution, original-conjecture counterexample, suitable-deletion obstruction, minimality result, or novelty claim is certified.

## 1. Exact objects accepted and original preserved

The incoming author ZIP is 17,362 bytes, SHA-256 `f3cb16cc91789f6577849ddc1091bd29f67a600b711bcd2eacf56658626100f0`. Its external manifest is 1,927 bytes, SHA-256 `f45a494556b383263eea83bf788ca69618194bf259f0edb7bdf258ce7b65602e`. Both exact pins matched. All eleven ZIP members, byte counts, and member hashes matched the external manifest. The original archive was not changed.

The mathematical report, both authored geometry implementations, complete witness, identity record, source pins, external-input verifier, and historical author-check log are byte-identical in the repaired derivative. Only `verify.py`, its usage paragraph in `VERIFYING.md`, and the affected entries in `MANIFEST.json` change. The exact change is `ISOLATED_LOADING.patch`. `ACCEPTANCE.json` and the derivative's external manifest identify the accepted ZIP and member bytes. This audit does not silently endorse arbitrary later edits or a different archive.

## 2. Target, hypotheses, and identity

The target is the average **vertex-edge graph diameter** of the bounded chambers of a real, simple affine hyperplane arrangement. The parameters are dimension d and n >= d+1 hyperplanes. Every d normal vectors are independent, and the intersections determined by different d-element subsets are distinct. These assumptions rule out parallels in dimension two and all d+1-fold concurrence. They also imply each full-dimensional chamber has a pointed recession cone and each bounded chamber is a simple polytope.

The exact-ID entry 3075 is unique in both complete input lists. Its problem number is OPG-605 and its catalog rank and one-based position are both 925. The full, unprojected `[problem_record, reports.get(problem_number,{})]` pair, serialized with Python's stated default JSON convention, has SHA-256 `f428e5123afd638179df90386db49bc7566befb56776e5f3f9af51bd99aa18c0`. This agrees with both the packet and the catalog review hash. The report key is absent and its default object is empty. The inherited record contains source notes and dated literature triage, not an existing mathematical solution. No claim that all possible unindexed repository work is absent is independently certified here; the author's repository-search history remains provenance, not an exhaustive theorem about prior work.

The three entire corpus snapshots were independently read and hashed, not replaced by extracted or reconstructed small records:

- `catalog.json`: 21,735,099 bytes; SHA-256 `891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566`
- `problems.json`: 68,931,837 bytes; SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
- `research_results.json`: 80,334,822 bytes; SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`

`CORPUS_AUDIT.json` records only identifiers, hashes, sizes, and match results. No corpus content is distributed.

## 3. Proposition 1: exact defect identity

Write I = C(n-1,d), B = C(n-2,d-1), S = sum diam(G(P)), D = dI-S, and sigma = sum(f(P)-d-diam(G(P))). Let F count bounded arrangement facets and E those adjacent to exactly one bounded chamber.

The supporting-hyperplane restriction is a simple (d-1)-dimensional arrangement, so F = nB. The subtle incidence assertion is valid under the stated spanning hypotheses: a bounded facet is adjacent to at least one bounded chamber. Indeed, fix the signs of all other hyperplanes and their recession cone K. Boundedness of the facet implies K intersects the supporting hyperplane's direction space only in zero. If both adjacent chambers were unbounded, K would contain directions of opposite strict normal signs. A positive combination has zero normal component, hence must vanish. The two directions would then generate a line in K, contradicting the fact that the other n-1 normals span the full space. An unbounded arrangement facet cannot be a facet of a bounded chamber. Therefore sum f(P) = 2F-E.

Using dI = (n-1)B gives

    S = 2nB - E - dI - sigma = dI + 2B - E - sigma,
    D = E + sigma - 2B.

This is the claimed identity, with the signs and constants correct. Crucially, sigma is **signed** in unrestricted dimension. Neither this proof nor the accepted code assumes the false general Hirsch bound. The statement is an exact reformulation, not an inequality that settles the problem. Dimension one is also consistent: E=2 and sigma=D=0; the supplied geometry program deliberately supports d>=2.

## 4. Proposition 2: the three-dimensional criterion

A bounded chamber in dimension three is a simple 3-polytope. Euler's formula and degree three imply v=2f-4, and its graph is 3-connected. For nonadjacent vertices at distance ell, three internally vertex-disjoint paths each have at least ell edges, so v >= 2+3(ell-1). Consequently ell <= floor((v+1)/3) = floor(2f/3)-1. For adjacent vertices the same bound follows from f>=4.

Thus r(P)=2f(P) mod 3 lies in {0,1,2}, and t(P)=floor(2f(P)/3)-1-diam(G(P)) is nonnegative. Summation yields 3S=2 sum f(P)-R-3I-3T. Substituting sum f(P)=2F-E, F=n(n-2)(n-3)/2, and I=(n-1)(n-2)(n-3)/6 gives exactly

    3D = 2E + R + 3T - 2(n-2)(n-3).

Both nonnegative terms and all factors check. The criterion 2E+R+3T >= 2(n-2)(n-3) is necessary and sufficient for that arrangement. The simpler E >= (n-2)(n-3) is sufficient, not asserted universal. No unproved global control of E, R, or T has been smuggled in. The local bound and incidence framework are already present in the cited literature; no literature novelty is certified.

## 5. Proposition 3: independent exact witness verification

The fixed eight rows `(a,b,c)` mean a*x+b*y=c:

    (1,1,5), (1,2,-1), (1,4,2), (1,5,-2),
    (1,7,2), (1,8,-5), (1,9,-1), (1,10,-2).

The deleted row is zero-based index 5, namely x+8y=-5. The independently written `independent_verifier.py` imports neither authored geometry implementation. It enumerates every pair intersection with exact fractions, checks every other line at that intersection to exclude triple concurrence, and then enumerates every sign vector. For each vector, it finds precisely the feasible pair-intersection vertices. Nonempty vertex sets represent full-dimensional chambers: at any such vertex the two independent active inequalities have a nonempty open local sector, and all other inequalities are strict.

Boundedness is tested by a different mechanism from either authored algorithm. The homogeneous recession cone is pointed. If it is nonzero, an extreme ray lies on one of its defining homogeneous lines, so one of the two exact directions perpendicular to a line normal satisfies all homogeneous signed inequalities. Conversely any such direction certifies unboundedness. Bounded-cell edges are reconstructed from their supporting lines and all graph distances are computed by BFS. This construction uses no floating-point decisions and no box clipping.

The independent recomputation agrees with **every** authored bounded-cell sign vector, vertex basis, edge, diameter, and rational polygon coordinate, not only the aggregate sums:

- Eight lines: 37 chambers, 16 unbounded, 21 bounded; 8 triangles, 11 quadrilaterals, 2 hexagons; S=36, average 12/7, D=6, E=16, sigma=2.
- After deletion: 29 chambers, 14 unbounded, 15 bounded; 7 triangles, 7 quadrilaterals, 1 pentagon; S=23, average 23/15, D=7, E=16, sigma=1.

Thus the insertion raises S by 13 while 2 times the increase of I is 12. It disproves the proposed bound for **every** deletion, since D drops from 7 to 6 under that insertion. The two averages remain strictly below 2. It does not refute the original conjecture.

Recomputing all eight one-line deletions gives D values `[6,5,5,6,6,7,6,6]`. Several deletions satisfy the monotonicity needed by a suitably chosen deletion step, so this is not a suitable-deletion obstruction either. No minimality assertion is made.

The two authored algorithms also have valid completeness arguments: the vertex/ridge method enumerates all chambers and detects unbounded chambers from extreme edges, while the exact clipping method uses a square containing every arrangement vertex strictly inside it. A bounded chamber stays inside that square; an unbounded chamber with a vertex inside has a ray crossing its boundary. The coordinate/graph certificate is exhaustive for these fixed rows only.

## 6. Primary-source audit and literature boundary

All six listed public sources were freshly retrieved during this audit. Every fetched byte count and SHA-256 matched the author's source pin. Relevant sections were inspected in the pinned PDFs/HTML; no copied source document or extracted text is included. `SOURCE_RETRIEVAL_AUDIT.json` records titles, public URLs, times, sizes, hashes, and match results.

- [Open Problem Garden](https://www.openproblemgarden.org/op/average_diameter_of_a_bounded_cell_of_a_simple_arrangement): identifies the bounded-cell average-diameter conjecture, its authors, and the chamber count.
- [Deza–Terlaky–Zinchenko, Polytopes and Arrangements: Diameter and Curvature](https://www.cas.mcmaster.ca/~deza/orl2008.pdf): Section 2, Conjecture 2.1, is the graph-diameter target. Its conditional Hirsch discussion does not provide an unconditional solution.
- [Deza–Xie, Hyperplane Arrangements with Large Average Diameter](https://arxiv.org/abs/0710.0328): introduction, planar result, small regimes, Proposition 6, and fixed-dimensional asymptotic lower constructions agree with the report. Proposition 6 uses the same local 3-polytope bound and incidence accounting.
- [Deza–Miyata–Moriyama–Xie, computational approach](https://www.cas.mcmaster.ca/~deza/aspm2012.pdf): Sections 1.2 and 5 distinguish the average-diameter conjecture from the external-facet lower-bound hypothesis. Proposition 7 establishes 44<45 for the latter at (d,n)=(3,8). Section 5 explicitly checks realizability of maximizing/minimizing oriented matroids. It does not identify every abstract oriented matroid with a real arrangement.
- [Selected publications, Antoine Deza](https://www.cas.mcmaster.ca/~deza/pub.html): confirms the 2009 and 2012 publication metadata and provides the recent facial-distance item.
- [Facial distance and diameter, arXiv:2609.32440v1](https://arxiv.org/abs/2609.32440): Section 1 defines diameter using Euclidean distance, so its resolved facial-distance conjecture is different.

Direct retrieval of the UnsolvedMath page again returned HTTP 403; exact imported identity was established through the full pinned corpus instead. The alternate 2026 McMaster PDF URL again returned HTTP 404; the arXiv PDF was accessible and matched. A targeted public literature search located no general resolution. This is limited search evidence, not proof of unresolved status or novelty.

## 7. Artifact defect, repair, and acceptance tests

Original normal and optimized replay pass in relocated directories. Original isolated Python replay fails in both `-I` and `-I -O` because Python excludes the script directory from module search and the bare `from arrangement import ...` fails. The original documentation did not explicitly promise `-I` support; this is a portability limitation found by the expanded audit, not a mathematical invalidation.

The derivative stores each already hash-checked file's bytes and compiles the two geometry implementations directly from those bytes into fresh module namespaces. It neither relies on sys.path nor consumes unpinned `.pyc` caches. The patch changes no mathematics, witness, or geometry algorithm.

The published audit driver reproduced 88 checks with fresh relocated packets, an unrelated working directory, a reduced environment, and explicit normal/optimized/isolated/isolated-optimized modes. The two original isolated failures are recorded as expected findings, not silently relabeled successful executions. The derivative passes all four replay modes. Negative tests reject raw witness changes, re-pinned coefficient/sum/coordinate changes, missing members, manifest-file-set changes, manuscript or implementation byte changes, corpus-byte changes, a wrong complete-pair digest, duplicated exact-ID records, and a corrupted scholarly PDF. Optimized negative tests remain failures. A deliberately poisoned bytecode cache is ignored by the derivative. AST inspection finds zero assertion statements in the authored, derivative, and independent validation code. Full details appear in `ARTIFACT_AUDIT_RESULTS.json`.

The manifests provide integrity relative to the externally frozen hash, not code trust by themselves. A malicious party that changes the entire package and its external trust anchor can create a different package; that is outside this acceptance. The proof audit and independently written exact enumerator are the substantive basis for accepting the mathematical claim.

## 8. Final scope and remaining task

The accepted partial consists of two exact identities and a finite counterexample to a stronger, arbitrarily chosen deletion induction. It establishes neither a new universal positive regime nor a genuine arrangement with average graph diameter above the dimension. Finishing the original problem still requires a universal bound E+sigma >= 2 C(n-2,d-1), another valid argument, or a true counterexample. The recorded outcome should remain **unsolved / partial stalled, 3/5**. The three approaches are documented; the remaining two are not represented as spent.

No GitHub writes were performed. The distributable audit contains authored mathematics, correction code, finite authored witness data, verification scripts, acceptance records, and public-source/corpus verification metadata only. It excludes corpus contents, third-party PDFs/HTML/text, private sources, and private coordination material.
