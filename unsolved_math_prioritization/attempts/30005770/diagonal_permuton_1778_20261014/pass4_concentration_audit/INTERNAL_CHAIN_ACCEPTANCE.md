# Independent acceptance of the internal-chain reduction

Shared PASS4, 14 October 2026.

Reviewed artifact: `pass4_two_sided_mark/INTERNAL_CHAIN_REDUCTION.md`, SHA-256 `c7f2967998cf51bf70fb52a2bf9694d7e59e4114cbcb3a0c123eddc5fe20f71c`.

**Accepted as a deterministic refinement of the pair criterion.** It supplies no uniform-law estimate.

For an Av(213) permutation written L,1,R, a left value below a right value would form213 with the minimum. Thus L>R, and the displayed identities for increasing pairs and increasing-subsequence length are exact. For a nonempty R, induction gives inc(R)+|R|<=|R|ell(R)<=|R|(ell(A)-1). If R is empty the term is zero; the same convention handles L. The resulting bound (|A|-1)(ell(A)-1) implies the stated weaker |A|(ell(A)-1), including a singleton.

The normalization symmetry preserves both statistics. Summing over cells gives n(L_max-1). The accepted staircase skew order between nonadjacent cells forces every increasing subsequence to use at most two adjacent cells, so L_max<=LIS(pi)<=2L_max. This uses actual canonical cells and no sampling assertion.

If LIS(Pi_n)/n tends to zero in probability, the within-cell increasing-pair count divided by n^2 does too. These normalized counts are uniformly bounded, so the expectation tends to zero. This implication does not control the adjacent-cell term in the exact pair generating function.

The example J_m direct-sum J_m has LIS2 and m^2 increasing pairs and avoids1324, whose LIS is3. It verifies precisely that the missing term remains essential. Its existence alone gives no lower probability under exact uniform sampling.
