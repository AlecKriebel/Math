# Independent bounds audit: Erdős #734

Date: 2026-10-21 UTC. Scope: elementary lower bounds and dense projective-plane restrictions. These results do not solve the requested every-sufficiently-large-n O(sqrt(n)) upper bound. No novelty claim is made.

## Definitions and validity gate

A design has n points, blocks of sizes 2 through n−1, and each unordered pair in exactly one block. Write b for its number of blocks and M for its largest size multiplicity. A full-point block plus singleton blocks is excluded. The de Bruijn–Erdős theorem gives b ≥ n under these hypotheses.

Primary reference: N. G. de Bruijn and P. Erdős, On a combinatorial problem (1948), Theorem 1, https://www.renyi.hu/~p_erdos/1948-01.pdf . Its theorem and proof were inspected through the public PDF text on the audit date.

## Pair-budget lower bound

Sort the block sizes s_1 ≤ ... ≤ s_b. Since no size occurs more than M times and all sizes are at least 2,

s_i ≥ 1 + ceil(i/M).

The unique-pair property therefore gives

n(n−1)/2 = Σ_i binom(s_i,2) ≥ (1/(2M²)) Σ_i i²
             = b(b+1)(2b+1)/(12M²).

Consequently

M² ≥ b(b+1)(2b+1)/(6n(n−1))
   ≥ (n+1)(2n+1)/(6(n−1)).

This supplies an explicit sqrt(n)-order obstruction using only pair counting and b ≥ n. The inequality is a deliberately elementary necessary condition, not a claim to an optimal constant or a new literature result.

For comparison, Gyárfás (2002), Theorem 1 and Corollary 2, obtains M > sqrt(n)/2 from the upper bound on distinct block sizes and b ≥ n. Its corrected distinct-size upper formula is 2k−2 for k² ≤ n < k²+k and 2k−1 for k²+k ≤ n < (k+1)². The upper-bound argument follows by selecting t blocks of strictly increasing sizes starting at size a: each subsequent block meets the preceding union in at most its index minus one points, so their union has at least at points. The source was inspected at https://www.renyi.hu/~gyarfas/Cikkek/101_Gyarfas_ErdosProblemsOnIrregularitiesOfLineSizesAndPointDegrees.pdf .

## Deterministic dense-truncation barrier

Let a projective plane of order q have v=q²+q+1 points and v lines. For any fixed subset S of n points, put p=n/v and s_L=|S∩L|. Average over a uniformly chosen line L, not over random choices of S. Incidence counting gives

Σ_L s_L = n(q+1),
Σ_L s_L(s_L−1) = n(n−1).

Thus the exact mean and variance are

μ=(q+1)p,
Var(s_L)=q p(1−p) ≤ q/4.

Chebyshev implies at least 3v/4 lines satisfy |s_L−μ| < sqrt(q). The number of possible integer sizes in this interval is at most 2sqrt(q)+1. Some size therefore occurs at least

3v / (4(2sqrt(q)+1)) ≥ q^(3/2)/4

times. If p ≥ δ > 0 and q ≥ 4/δ², then μ−sqrt(q)>1, so this repeated size is at least 2. Also n>q+1, hence all resulting block sizes are at most n−1.

Restrict all plane lines to S and remove intersections of size zero or one. The remaining intersections form a valid pairwise design: every pair of S has its unique original line, and distinct original lines cannot yield equal intersections of size at least two. The repeated central size above is consequently a genuine block multiplicity after deletion, not an artifact of empty or singleton intersections.

Since n ≤ v ≤ 3q², the multiplicity is also at least n^(3/4)/(4·3^(3/4)). The density lower bound controls the threshold at which the counted sizes are nontrivial. This excludes an O(sqrt(n)) bound for plain fixed-positive-density restrictions of projective planes, even if the subset is chosen deterministically or optimally. It does not exclude sparser restrictions, modifications replacing blocks, or unrelated constructions.

A sharper density-sensitive statement, when 0<p<1 and μ−2sqrt(qp(1−p))>1, is that some nontrivial size occurs at least

(3v/4)/(4sqrt(qp(1−p))+1).

The p=1 case is separately immediate: all v blocks have size q+1. No use is made of an ambiguous printed/OCR exponent in the 2002 account of a related limitation.

## Historical upper-bound gate

Erdős–Purdy, Some Combinatorial Problems in the Plane (1978), Theorem 2, states F(n)=O(n^(3/4)) and expressly provides only an outline while omitting probability calculations. Its primary PDF at https://renyi.hu/~p_erdos/1978-42.pdf was inspected, especially printed page 208. The source claim is established as a historical published statement, not by that inspection alone as a fully reconstructed proof. Any separate reconstruction must verify simultaneous control of every size, exact n, nontriviality, existence of the ambient planes for every large n, and every probabilistic estimate. A valid reconstruction would still recover this partial bound, not solve #734.
