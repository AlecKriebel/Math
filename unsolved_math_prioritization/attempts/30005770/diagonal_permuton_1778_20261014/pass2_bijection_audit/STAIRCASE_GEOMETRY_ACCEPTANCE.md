# Cross-review of the 1324 staircase geometry

Same PASS 2 continuation,14 October2026. Reviewed artifact: `pass2_1324_shape/FIXED_STAIRCASE_PREFIX_THEOREM.md`,13295 bytes, SHA-256 `1049ab2c021a6398831e8251d0a07cd03b1db98d9a88d64e4faa3660cb1a2037`.

## Verdict and review boundary

**Sections1,2,5,6 pass the requested structural cross-review without correction.** The canonical gridding, symmetry transfer, deterministic3M/n bound, and escaping-cell-index example are valid. I also checked the injective deletion multiplicity used in Section3. The separate concentration reviewer owns the frontier amplification input and full probability/rate argument in Sections3–4; this report does not substitute a new review of that external input.

The draft correctly restricts its consequence to a fixed initial number of greedy cells. It does not equate this with the largest cell, the minimum possible gridding cell count, or an arbitrary K-cell grid class. It supplies no counterexample under the uniform1324 law and no resolution of its anti-diagonal limit.

## Canonical greedy peeling

The primary staircase proof chooses, in turn, the highest value serving as1 in213 and the earliest last position serving as2 in132. These are exactly the first excluded value or position in the maximal top213-free band and maximal left132-free prefix.

For an actual1324-avoider, the source's forbidden-crossing argument ensures that after each cut no previously removed point remains in the next permitted half-plane. Therefore applying the source rule to that half-plane agrees with applying the next rule to the standardized remainder. This is the required canonical continuation property; it is not assumed for arbitrary permutations.

The designated sequence of extreme cuts is an exact deterministic gridding. Results about its first K cells and its total greedy-cell count do not automatically apply to a different, more economical gridding of the same permutation. The draft preserves this distinction.

## Frontier symmetry and deletion convention

For T, inversion fixes1324 and reversal maps it to4231. Under reverse-after-inverse, the largest-value band becomes the initial position segment, while213 becomes312. For P, complementation sends1324 to4231 and132 to312 without changing positions. Thus both relevant frontiers equal the312-free initial-prefix length of an exact uniformly distributed4231-avoider; the insertion label is that length plus one. The additive correction cannot affect a fixed-positive linear threshold rate, but the convention is explicitly stated.

The deletion step is also an upper count with its weights retained: deleted positions, deleted values, their standardized pattern, and the remainder reconstruct the original permutation. Heredity bounds the deleted pattern count by a_k. The actual remainder is never assumed uniform; its completion bias is handled by the displayed multiplicity. Skew closure makes a_k*a_(n-k)<=a_n. This structural/probability normalization step is sound.

## Largest-cell geometry

Nonadjacent cells of the descending staircase are strictly northwest/southeast ordered. For a point in cell j, all earlier nonadjacent points precede it in position and exceed it in value; all later nonadjacent points do the reverse. Writing q_j for the total sizes of cells j-1,j,j+1 gives exactly

`|i+pi(i)-n-1| <= q_j-1`.

The square-spread perturbation adds at most1/n, so `|x+y-1|<=q_j/n<=3M/n`. The explicit anti-diagonal coupling therefore proves the stated d_BL bound. This holds for any such staircase gridding; no probabilistic cell independence or internal cell limit is used.

The increasing-pair alternative is also correct: only pairs within one cell or in adjacent cells can increase. The bounds `sum binom(m_j,2)<=sum m_j^2/2` and `sum m_j*m_(j+1)<=sum m_j^2` imply the claimed upper bound `(3/2)nM`.

## Escaping-index example

The patterns132,213,1324 are skew-indecomposable. Hence their occurrences in the proposed skew sum must lie in individual blocks. The block G=2413 has a maximal top213-free band of size3 and a maximal initial132-free segment of size3.

Each peel leaves one point of its active G block. The next peel includes that singleton and three allowable points from the following G block. The central increasing block avoids both triples and is absorbed completely at the transition. This proves the exact sequence

`3, 4 repeated(r-1) times, N+4, 4 repeated(r-1) times, 1`.

Because the two flanks each have size4r, every point of the central I_N actually satisfies pi(i)=i. If r tends to infinity but r/n tends to zero, its mass tends to one and the permuton tends to the diagonal. Any fixed number of cells at either end still has bounded size. The specified bounded1-Lipschitz test function distinguishes this limit from the anti-diagonal by1/(2sqrt2).

This is a precise deterministic failure of the proposed implication from bounded-index cell control to largest-cell control. It says nothing about the probability of this family under uniform1324 avoidance, as the draft correctly emphasizes.

## Independent finite regressions

`check_staircase_geometry.py` checks every1324-avoider through n=7. It independently verifies agreement of the global source half-plane rule with remainder peeling, strict ordering of every nonadjacent pair of cells, and each pointwise q_j-1 geometry bound. It also checks the exact escape-family cell sizes for all1<=r<=5 and1<=N<=20, and verifies that the central increasing block is fixed pointwise. All checks pass; `STAIRCASE_FINITE_CHECKS.json` records the results. These finite checks support implementation and indexing, not the asymptotic theorem.

Earlier PASS1 files and the already frozen PASS2 merge/countermodel acceptances remain unchanged.
