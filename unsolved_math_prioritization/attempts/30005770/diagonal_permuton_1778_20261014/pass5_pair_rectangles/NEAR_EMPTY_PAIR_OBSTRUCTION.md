# Sublinear chains and few empty rectangles do not control near-empty pair mass

Final shared PASS5, row1778 /30005770, 14 October2026. This completes the sparse-rectangle branch analysis. It is a deterministic obstruction to combining two weaker estimates, not a uniform-probability counterexample. No further variant or mathematical pass is opened.

For a permutation pi, let Z_t(pi) be the number of increasing pairs whose open rectangle has at most t interior entries. Thus Z_0 counts exactly empty increasing rectangles. Let Inc(pi) count all increasing pairs.

## 1. A simple example explaining the issue

Let J_a be decreasing, I_b increasing, and define

    Q_k=I_k skew-sum ... skew-sum I_k     (k blocks),
    sigma_k=J_(k^2) direct-sum Q_k.                         (1)

An increasing pair either lies in one I_k block or runs from J_(k^2) into one such block. Its open rectangle contains only an increasing segment of that I_k block. Therefore sigma_k avoids1324. It has

    n=2k^2,
    LIS=k+1,
    Z_0=k^3+k(k-1),
    Inc=k^4+k binom(k,2).                                  (2)

The cross-pair rectangle is empty exactly when its upper endpoint is the first entry of its I_k block; the internal empty pairs are consecutive chain entries. Every pair has at most k-1 interior entries. Hence LIS=o(n), Z_0=o(n^2), but Inc/n^2 tends to1/4. The increasing-pair mass consists of near-empty rather than exactly empty rectangles.

This simple example has a large initial canonical cell. The next construction makes the same obstruction compatible with negligible fixed initial and terminal canonical cell prefixes.

## 2. Normalized states and genuine canonical edges

For a>=2 put

    D_a=12 skew-sum J_(a-2).

It has only one increasing pair, namely its first two entries, is fixed by S, and belongs to Av(213). For k=2^s, s>=1, put

    A_k=1 direct-sum Q_k.                                  (3)

This is in Av(213): Q_k is a skew sum of increasing blocks and contains no213; its new first minimum cannot participate in213. The first entry of A_k is its unique minimal point in the increasing-point partial order. It has

    |A_k|=k^2+1,
    LIS(A_k)=k+1,
    Z_0(A_k)=k^2,
    inc(A_k)=(k^3+k^2)/2.                                  (4)

The Z_0 count consists of k covers from the first minimum to the first point in each Q_k block, together with k(k-1) consecutive pairs inside those blocks.

Use the following normalized state sequence:

    D_2,D_4,...,D_(k^2), A_k,
          D_(k^2),D_(k^2/2),...,D_2.                      (5)

There are4s D states and one A state. Join ordinary D_a -> D_b edges by the accepted deterministic ascent bridge. In normalized vertical orientation, its binary word is

    U L L U^(a-1) L^(b-2),                                (6)

because the maximum of the lower D_b is its second entry. Join D_(k^2) -> A_k by the same bridge. The maximum of S(A_k) is last, so its word is

    U L^(k^2+1) U^(k^2-1).                                (7)

For the special A_k -> D_(k^2) edge use instead

    U L^(k^2) U^(k^2).                                    (8)

This is an allowed kernel edge. Its lower maximum is between the first two increasing upper entries, so the greedy witness holds. A mixed1324 using two lower and two upper points would need the color order lower,upper,lower,upper, impossible because all lower points are consecutive. Occurrences with one lower point would require213 in A_k; those with three lower points would require132 in D_(k^2). Both are excluded by the cell classes.

The accepted exact homogeneous kernel therefore reconstructs one actual1324-avoider pi_s with precisely the canonical states(5) and these edge words. Its total size is

    n_s=(2k^2-2)+(k^2+1)+(2k^2-2)=5k^2-3.                 (9)

Every fixed number of initial or terminal cells has bounded total size as s grows, hence negligible mass. The central cell has mass tending to1/5. Neighbor sizes grow or shrink geometrically outside the central three comparable-size cells. The construction is not an arbitrary noncanonical gridding.

## 3. Exact local empty-pair counts

In a two-cell edge whose word is U L^b U^(a-1), all cross increasing pairs run from a lower point to an upper point after the first upper point. Such a rectangle is empty exactly when:

- the lower endpoint has no later larger lower point; and
- the upper endpoint has no earlier smaller point in the upper suffix after the first point.

These are respectively maximal points of the lower pattern and left-to-right minima of that upper suffix. Accepted pair-local rectangle geometry ensures that other staircase cells cannot contribute interior points to these rectangles.

Apply this observation to the two special edges:

- In(7), S(A_k) has exactly one maximal point, since A_k has exactly one minimal point. The upper D suffix is decreasing. Thus this edge has exactly k^2-1 empty cross pairs and (k^2+1)(k^2-1) cross increasing pairs.
- In(8), the lower D has k^2-1 maximal points. The upper suffix is Q_k and has exactly k left-to-right minima. Thus this edge has exactly k(k^2-1) empty cross pairs and k^4 cross increasing pairs.

For an ordinary edge(6), only the first two lower points precede upper points. They yield2(a-1) cross increasing pairs. Pairs starting at the first lower point have the second lower point in their interiors, whereas those starting at the second lower point have empty interiors because the upper suffix is decreasing. Thus(6) has exactly a-1 empty cross pairs.

Each D state contributes one internal increasing pair, which is empty. Equation(4) supplies the counts for A_k. Nonadjacent cells contribute no increasing pair, so these counts exhaust the permutation.

## 4. Exact totals and sublinear interior sizes

The sum of a-1 over all ordinary D_a -> D_b edges in(5) is

    3k^2-4s-4.

Consequently,

    Z_0(pi_s)=k^3+5k^2-k-5,
    Inc(pi_s)=2k^4+(k^3+13k^2)/2-4s-9.                    (10)

In particular,

    Z_0(pi_s)/n_s^2 ->0,
    Inc(pi_s)/n_s^2 ->2/25.                               (11)

An increasing subsequence can meet at most two adjacent canonical cells: points in nonadjacent cells are northwest/southeast ordered. Every D state has LIS2, while A_k has LISk+1. Hence

    LIS(pi_s)<=k+3=o(n_s).                                (12)

Every open increasing-pair rectangle is itself increasing, and adjoining its two endpoints gives an increasing subsequence. Therefore its interior has at most k+1 points. Thus

    Z_(k+1)(pi_s)=Inc(pi_s),
    (k+1)/n_s ->0.                                        (13)

These are simultaneous properties of actual canonically gridded1324-avoiders with escaping-index macroscopic cells.

## 5. The three thresholds must remain distinct

The construction establishes all of the following:

- Exactly empty rectangles have vanishing normalized count: Z_0/n^2 ->0.
- Rectangles with at most k+1=o(n) interior points carry a positive normalized count: Z_(k+1)/n^2 ->2/25.
- For every fixed theta>0, eventually k+1<=theta*n, so Z_(floor(theta*n))/n^2 ->2/25. Letting theta decrease to zero only after this n-limit does not remove that mass.

Thus neither LIS=o(n) nor Z_0=o(n^2), nor their conjunction, implies Inc=o(n^2). A proof of the sparse branch needs control uniform for a small positive interior threshold, or an equivalent direct bound on the complete near-empty allocation sum. An estimate only at m=0 leaves a genuine gap.

Nothing here asserts that pi_s, its size profile, or any related set has nonnegligible probability under the uniform avoidance law. Those examples may be exponentially rare. The result identifies insufficiency of the stated geometric/counting conditions, not a failure of the conjectured limit.

## Inputs and completion scope

The canonical kernel, nonadjacent-cell order and rectangle locality are the accepted PASS2 exact transfer. The direct bridge is the accepted PASS3 ascent bridge. All additional edge words, local cover counts and asymptotic comparisons are proved above and are independently finite-checkable. No external source retrieval, publication, remote edit, or further pass is involved.
