# Independent acceptance of the fixed greedy staircase-prefix theorem

Date: 14 October 2026. This review concerns exact uniform Av_n(1324), whose proposed anti-diagonal limit is equivalent by reversal to the diagonal target for alpha=312, forbidden pattern 4231.

## Verdict and pin

Accepted within its stated restricted scope: FIXED_STAIRCASE_PREFIX_THEOREM.md, 13295 bytes, SHA-256 1049ab2c021a6398831e8251d0a07cd03b1db98d9a88d64e4faa3660cb1a2037.

For each fixed positive integer K and fixed epsilon>0, the total mass in the first K canonical greedy staircase cells exceeds epsilon with exponentially small probability. Consequently the canonical at-most-K-cell subfamily has a strict exponential growth gap. The proof does not establish maximal-cell concentration or the anti-diagonal limit for uniform 1324-avoiders. No correction to the frozen proof was required.

## 1. Exact source geometry

Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Proposition 1, pp.3-4, was inspected directly, including the full proof and the rendered p.4 diagram and text. Source: https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf . PDF pin: 627368 bytes, SHA-256 1264749e17f01005277e8acf1a7782e6c4e448fe1733ac6fbb29ec8bd125f26d.

The first row divider is determined by the highest value serving as the minimum of a 213. The values above it form the largest 213-free top interval. The next column divider is determined by the earliest endpoint of a 132 in the remainder, so the points before it are the largest 132-free initial positional interval. The source's 1324-exclusion argument ensures that forbidden off-staircase cells are empty. Repeating these operations on the standardized remainder therefore does give the source's canonical greedy cells; this is not an arbitrary color partition or an unproved alternative gridding.

Nonadjacent cells are strictly ordered northwest to southeast. The source's construction also makes all prior deletion rules deterministic. Thus their use in an injective reconstruction upper bound is legitimate.

## 2. Uniformity-preserving symmetry maps

For the top interval, reverse(inverse(sigma)) maps the complete Av_q(1324) bijectively to Av_q(4231). The selected original values q,q-1,... become the initial positions after the two symmetries. Pattern 213 becomes 312, so the cell-size statistic is exactly one less than the 312-frontier label in that image.

For the positional interval, complement maps Av_q(1324) bijectively to Av_q(4231), preserves prefixes, and maps 132 to 312. The same frontier lemma applies.

Both are bijections on full finite classes. Hence their input law is exactly uniform, and their common growth constant lambda agrees with that of Av(1324). The existing frontier estimate requires no ratio limit or exact numerical value of lambda.

## 3. Uniform errors and actual completion weights

The claimed uniform tail estimate over all k<=delta n is valid. If it failed, a maximizing subsequence could be chosen with (n-k_n)/n converging to theta in a compact interval bounded away from zero. The accepted variable-threshold frontier theorem would then apply at lengths q_n=n-k_n, with threshold-to-length ratio converging to eta/theta. Multiplication by q_n/n recovers the rate -eta gamma and contradicts failure. Impossible events are safely discarded. This establishes uniform control rather than assuming it from a separate estimate at each k.

For a fixed remainder of size n-k, an original permutation can be encoded by the k removed positions, the k removed values and the removed entries' standardized pattern. The last belongs to Av_k(1324) by heredity. Thus the reconstruction bound is exactly at most binom(n,k)^2 a_k. These data plus the remainder determine every entry of the original permutation, so the encoding cannot undercount. Extra invalid encodings only enlarge the upper bound.

Skew-sum closure gives a_k a_(n-k)<=a_n because 1324 is skew indecomposable. After normalization, the remaining probability comparison costs binom(n,k)^2. The proof retains this factor and never calls the actual remainder law uniform.

Summing over all possible k<=delta n introduces at most n+1 terms. Since delta<1/2, the uniform binomial entropy upper bound is exp(2n h(delta)+o(n)). Combined with the uniform frontier tail, this proves the displayed deletion estimate with exponent 2h(delta)-eta gamma. There is no missing allocation, denominator, or deletion-size factor.

## 4. Fixed-K induction and its exact consequence

For K=1 the appropriate uniform frontier bound gives rate epsilon gamma. For the inductive step choose delta<epsilon/2 with 2h(delta)<epsilon gamma/4. On the event that the first K cells have total size at least epsilon n, either the first K-1 already have more than delta n points or the next frontier has at least (epsilon-delta)n points after a deletion of at most delta n entries.

The first event has a strictly negative exponential rate by induction; the second has rate below -epsilon gamma/4. Taking the smaller positive rate yields the claimed r_K(epsilon). This argument applies separately to each fixed K. It supplies no lower bound uniform in growing K.

If the canonical greedy gridding has at most K nonempty cells, its first K cells contain all n points. Multiplying the resulting probability bound by a_n and taking nth roots gives a rate at most lambda exp(-r_K(1)), strictly below lambda. This corollary does not require that the subfamily be hereditary. The frozen statement correctly avoids any claim about minimum cell count over arbitrary alternative griddings.

## 5. Geometry and deterministic nonimplication

For a point in cell j, let a and b count points in earlier and later nonadjacent cells, and let q_j count the three cells j-1,j,j+1. The source geometry gives

    a+1<=i<=n-b,   b+1<=pi(i)<=n-a,   a+b+q_j=n.

These imply |i+pi(i)-(n+1)|<=q_j-1. The extra within-square error is exactly at most 1/n, giving |x+y-1|<=q_j/n<=3M/n. Coupling to (X,1-X) proves the stated d_BL bound under the square-spread convention, with no additional asymptotic boundary term required. The alternative increasing-pair upper bound follows because only the same or adjacent cells can contribute such a pair.

The skew-sum construction using r copies of 2413, then I_N, then another r copies of 2413 is valid. All its blocks avoid 1324, and skew closure preserves avoidance. Each outer 2413 block contributes three entries to one greedy cell and leaves a singleton for the next. Because 132 and 213 are themselves skew indecomposable, no occurrence straddles its skew blocks. This establishes the exact sequence

    3, (r-1 copies of 4), N+4, (r-1 copies of 4), 1.

Its entries sum to N+8r. With r increasing sublinearly in n, each fixed cell index at either end has bounded size, while the middle increasing block has mass tending to one. Its normalized plot tends to the diagonal, not the anti-diagonal. This correctly disproves only the deterministic implication from bounded-index control to maximal-cell control. It is not sampled uniformly and therefore gives no counterexample to the target.

## 6. Source-status and final scope

The separately recorded Brignall manuscript, *Shuffle automata and the growth of 1324-avoiding permutations*, arXiv:2610.02535v1, was checked against its retained PDF introduction. Its inspected statement is an upper growth bound, not a permuton limit theorem. Source: https://arxiv.org/abs/2610.02535v1 . PDF pin: 298584 bytes, SHA-256 eb0aeebef5214af3a6b2390c698f93eb2350c84a2cb2815e7d7a26ed09735cf7. None of its numerical bounds is required by the accepted probability argument.

The open step remains a bound on a cell whose greedy index can escape to infinity, or a direct bound on positive anti-diagonal crossing mass/increasing-pair density. Replacing fixed K by K_n, discarding a macroscopic completion bias, or treating this restricted theorem as the full 1324 limit would be invalid. The universal fixed-alpha target remains unresolved by this candidate.
