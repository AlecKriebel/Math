# Independent acceptance of the exact increasing-pair target

Shared PASS4, 14 October 2026.

Reviewed artifact: `pass4_two_sided_mark/POINT_PAIR_TARGET.md`, 5477 bytes, SHA-256 `e5161b6e84679b9a04c00dd64a7796ff8066c578c5fff37bdfa0d7f375411087`.

**Accepted as an exact criterion and counting identity.** No asymptotic estimate of either weighted term is proved.

## Metric and exact-law criterion

Sorting into decreasing order by adjacent swaps uses exactly Inc(pi) swaps. Swapping adjacent positions changes the footrule distance to the decreasing target by at most two: each moved value changes its target position by one. Thus D(pi)<=2Inc(pi).

For a square-spread point in the i-th occupied square, the discrepancy from(X,1-X) is at most |i+pi(i)-(n+1)|/n+1/n. The first coordinate is uniform, so this is a valid coupling to the anti-diagonal permuton. Averaging proves the displayed bounded-Lipschitz upper bound.

Consequently E Inc=o(n^2) implies weak convergence in probability by Markov's inequality. Conversely, the two-point increasing event has a boundary only at equal x or equal y coordinates. Independent samples from any permuton give that boundary probability zero because its marginals are uniform. Hence its density is weakly continuous. The finite pattern density differs from the square-spread density by O(1/n), and all these variables are bounded. Convergence in probability to the deterministic anti-diagonal therefore implies convergence of the expected normalized increasing-pair count to zero. The criterion is genuinely necessary and sufficient for the stated exact-uniform convergence.

## Exact weighted decomposition

The normalization S preserves increasing-pair counts. Nonadjacent canonical cells are in skew order, so every increasing pair is either internal to one cell or crosses exactly one adjacent edge.

Marking an internal pair yields z^|A|ell_A h_A inc(A). Marking a cross-cell pair on an edge yields z^(|A|+|C|)ell_A h_C K_inc(A,C). Each state weight occurs once, the prefix ends before A, and the suffix starts after C. The edge kernel sums the actual allowed-shuffle increasing-pair counts, retaining both avoidance and greedy constraints. No unconditioned interleaving average is substituted.

Summing these disjoint contributions gives the exact coefficient identity. All coefficients are finite. For real z<rho, convergence follows from the coefficient bound binom(n,2)a_n, so nonnegative rearrangements are justified.

## Local geometry and scope

A decreasing pair inside the open position/value rectangle of an increasing pair would form1324 with its endpoints. Hence that interior is increasing. The caution about empty rectangles is also valid: two decreasing blocks in direct sum have many increasing cross-pairs but none of those rectangles need contain points. This is a deterministic observation, not a probability bound.

The exact target is coefficientwise o(n^2 a_n) for the displayed sum. A whole-state exponential mark would suffice but is stronger than necessary. The pointwise incoming lift preserves an inverse-pattern padding in the paired outgoing term and gives no estimate by itself. The note correctly leaves both the internal-pair and cross-edge weighted bounds open.
