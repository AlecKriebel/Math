# Independent probability and entropy acceptance: rectangle route

Final shared PASS5, 14 October 2026.

Reviewed final proof pins:

- `pass5_pair_rectangles/RECTANGLE_DELETION_AND_ENTROPY.md`: `990442ebcdd9866c6df9f1ddd127bfa36a31a399c5ddd965a1020ebfdab7a373`.
- `pass5_pair_rectangles/COMB_RECTANGLE_OBSTRUCTION.md`: `cabf1788cc22562cc3ba8ffb3feaf81298c9fc1b89db99d76d321e4b8714cea3`.
- `pass5_pair_rectangles/COARSE_RECTANGLE_DICHOTOMY.md`: `489d88735bac14ca612105f8e34682dbdfabd7fc554d4251b213d6f31b4dda2b`.

**Accepted with the stated restricted scope.** The first note proves an actual uniform tail for favorable deletion scores. The other two identify exact deterministic coverage and an actual-class obstruction to forcing that score. No global pair-density estimate follows.

## Exact reconstruction and allocation entropy

The interior of an increasing-pair rectangle in a 1324-avoider is increasing. Deleting its m entries preserves avoidance, produces an empty marked rectangle, and leaves exactly p positions and q values between the endpoints. Choosing which m of the m+p interior positions and m of the m+q interior values were deleted, then matching them increasingly, reconstructs at most one original permutation. Order-preserving insertion keeps all surviving entries outside the open rectangle. Thus the exact sum over empty skeletons with an avoidance indicator is valid.

The full product of binomial coefficients counts allocation records before avoidance is imposed. It is only an upper bound. The displayed counterexample checks: the empty rectangle in 31524 gives 314625 after insertion, and entries 1,4,2,5 witness 1324 in the latter. This verifies that the indicator cannot be discarded in an equality or sampling law.

There are at most (n-m)^2 marked skeleton pairs and at most (n+1)^3 statistic triples. The entropy upper bound on each binomial is exact, with the conventional zero terms. If m log lambda-E(m,p,q)>=c*n, each summand is at most n^2*lambda^n*exp(-c*n). Dividing by the actual a_n and summing proves exp(-c*n+o(n)); the o(n) includes the exact normalization defect. The bound is uniform over all locations, sizes and marked pairs because no limit depending on those choices is used.

For p+q<=m, concavity gives E<=2e(m,m/2)=m log(27/4). The strict inequality lambda>27/4 is a proven input. Consequently the dense-interior corollary has precisely the claimed exponential rate. The skeleton may still have exponentially many completions with unfavorable allocation data; no independent conditional law is introduced.

## Comb contamination and exact constants

A comb's earlier high teeth exceed every later point, so its southwest predecessors are low anchors. All but possibly the final relevant anchor contribute their full following tooth blocks as contaminants. The same-cell argument compensates for an incomplete final block with the block following the first endpoint. Under the staircase normalization reflection, the position and value strips exchange roles. Combining the two adjacent cells therefore gives p+q>=L(m-2)_+ with no double counting of teeth.

The entropy function satisfies H(x)+H(y)>=H(x+y), where H(t)=e(1,t), by concavity and H(0)=0. Hence E>=e(m,p+q). With L=5 and m>=20, the contamination ratio is at least 9/2. The strict comparison is exact:

    2[H(9/2)-log(27/2)]=log(11^11/3^24)>0.

The stated integers 11^11 and 3^24 verify this close inequality. The credited upper bound lambda<=27/2 then makes every such rectangle's raw score negative. This covers all rectangles simultaneously, rather than a bounded predetermined selection.

The central comb has inc=(6k^2+4k)/2 at L=5, while n=6(3k-4); the limiting pair-count lower bound is 1/108 and the LIS lower bound is 1/18. These are genuine deterministic weak-deviation witnesses. They have no asserted nonvanishing weight in the uniform class. The obstruction applies to treating all allocation records as admissible; it does not refute a sharper estimate using the exact indicator.

## Coarse-grid constants and complete branches

With the stated Q, excluding pairs whose position or value differences are at most 2n/Q removes at most 4n^2/Q<=epsilon*n^2/2 pairs. Pigeonholing over at most Q^4 cell pairs gives beta*n^2 retained pairs. Every pair across the chosen separated cells is increasing.

The half-open core is strictly between all endpoints: its lower boundary is above the southwest cell's excluded upper edge, and its excluded upper edge is at or below the northeast cell's lower edge. Points of any selected open rectangle outside that core belong to two endpoint columns or two endpoint rows. Their number is at most 4ceil(n/Q)<=theta*n under n>=8/theta and Q>=8/theta. Thus the occupied and sparse branches, including their uniform assertion for every pair in the chosen product set, are exhaustive and have the stated constants. Q is fixed before n.

An occupied core need not have low strip contamination, as the comb witnesses show. The sparse branch includes the decreasing-block direct sum, with quadratically many empty increasing-pair rectangles. Merely obtaining a fixed finite family of endpoint regions suppresses neither branch. The exact empty-skeleton incidence and admissibility-weighted reconstruction remain the missing probabilistic estimates.
