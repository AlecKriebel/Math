# Independent acceptance: near-empty pairs versus exact emptiness

Final shared PASS5, 14 October 2026.

Reviewed: `pass5_pair_rectangles/NEAR_EMPTY_PAIR_OBSTRUCTION.md`, SHA-256 `5b226d59b9d751ff1923c1957187c523d5425e2f1f224432c0ddf918e121da0c`.

**Accepted as an actual canonical deterministic obstruction.** No uniform probability lower bound is supplied.

In the simple example J_(k^2) direct-sum Q_k, every increasing-pair interior lies in one increasing block of Q_k. The cross rectangle is empty exactly at the first point of that block, giving k^3 empty cross pairs. Consecutive pairs within its k blocks add k(k-1). The LIS and total increasing-pair formulas follow, and show the distinction before imposing the endpoint-prefix condition.

For the canonical refinement, D_a has only its first increasing pair, and A_k=1 direct-sum Q_k has the displayed LIS and pair statistics. Its first minimum covers the first entry in each of the k blocks; the internal covers in those blocks contribute k(k-1), giving Z_0(A_k)=k^2. The special all-lower-middle edge has the greedy witness and excludes the interlocked two-color pattern; the remaining color distributions are excluded by the actual state classes.

For an edge U L^b U^(a-1), an empty cross rectangle requires a maximal lower endpoint and a left-to-right-minimal upper endpoint in the suffix. This follows by inspecting the possible interior points separately in each cell, with the accepted rectangle locality excluding all other cells. In the first special edge, S(A_k) has exactly one maximal point and the upper D suffix is decreasing, giving k^2-1 empty cross pairs. In the second, D has k^2-1 maximal points and Q_k has k left-to-right minima, giving k(k^2-1). The total cross-pair counts are k^4-1 and k^4 respectively.

For each ordinary edge the second of its first two lower points gives a-1 empty cross pairs, while the first has that second point inside its rectangle. Its total increasing cross count is 2(a-1). Summing a-1 on the ascending and descending ordinary edges gives 3k^2-4s-4. Adding the 4s internal D pairs and the A contribution recovers both exact totals in the note. Division by n=5k^2-3 gives Z_0/n^2 tending to zero and Inc/n^2 tending to 2/25.

Nonadjacent canonical cells cannot meet an increasing chain, so LIS is at most k+3. Every increasing-pair interior is itself increasing and, together with its two endpoints, is an increasing chain. Its size is therefore at most k+1=o(n). Consequently Z_(k+1)=Inc, and for every fixed theta>0 the same normalized 2/25 limit holds for Z_floor(theta*n). The order of limits is essential: taking theta to zero after the n-limit does not reduce this mass.

The fixed initial and terminal cell prefixes have bounded total size as s grows, so the example retains the escaping-index endpoint conditions. It demonstrates that small LIS and few exactly empty rectangles together do not imply small total increasing-pair count. The still-needed sparse-branch estimate must control near-empty rectangles uniformly at a small positive mass threshold, or directly control the full weighted pair count. The example's own exact-uniform probability can be negligible.
