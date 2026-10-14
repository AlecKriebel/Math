# Internal increasing pairs reduce to increasing-chain height

Shared PASS4. This is a deterministic refinement of the exact pair target, not a uniform-law tail estimate.

For a nonempty Av(213) state A let ell(A) be its longest increasing subsequence length, and inc(A) its number of increasing pairs. Then

    inc(A)<=|A|[ell(A)-1].                                  (1)

Proof: decompose A around its minimum as L,1,R, standardizing the two sides when evaluating their statistics. Every L value exceeds every R value; otherwise l,1,r would be213. Hence

    inc(A)=inc(L)+inc(R)+|R|,
    ell(A)=max(ell(L),1+ell(R)),

with empty-side subsequence length zero. Induction gives inc(L)<=|L|[ell(A)-1] and inc(R)+|R|<=|R|[ell(A)-1]. The sum is at most (|A|-1)[ell(A)-1], which proves (1). Empty sides contribute zero and cause no exception. The normalization involution S preserves increasing chains and pairs, so the same bound applies to each actual staircase cell.

For a canonical1324 staircase with cell sizes a_j and normalized states A_j, put L_max=max_j ell(A_j). The total number of within-cell increasing pairs is at most

    sum_j inc(A_j)<=n[L_max-1].                              (2)

Moreover,

    L_max<=LIS(pi)<=2 L_max.                                (3)

The lower bound is immediate. An increasing chain cannot meet two nonadjacent cells because those cells are northwest/southeast ordered. All its points therefore lie in one cell or two adjacent cells, proving the upper bound.

Consequently, proving LIS(Pi_n)=o(n) in probability would make the within-cell contribution to the exact pair criterion o(n²), in probability and expectation. It would leave the cross-cell term involving K_inc. A large cell whose own increasing-chain height is small need not be discarded by this route.

That remaining term is essential. The permutation J_m direct-sum J_m avoids1324 because its longest increasing subsequence has length2 whereas1324 has one of length3. Nevertheless it has exactly m² increasing pairs, all between the two decreasing blocks. Thus LIS=o(n), even bounded LIS, cannot by itself imply the desired anti-diagonal limit. This is a deterministic nonimplication with no uniform-probability lower bound.

The identities above use only the accepted staircase geometry and the elementary minimum decomposition of Av(213). No new counting theorem, sampling model, or asymptotic estimate is asserted.
