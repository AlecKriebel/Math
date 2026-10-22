# Degeneracy-aware elementary bounds

All results concern a finite set X of n >= 2 distinct points in R^2. For a determined line ell, d_X(ell) is the absolute difference of its two open-half-plane counts. D(X) is the minimum of these discrepancies. Put e = n mod 2.

## 1. Exact angular-block lemma

An exposed vertex p means that there is a vector u such that u dot (q-p) > 0 for every q in X other than p. Such a point exists: choose a linear functional taking distinct values at all points and take its unique minimizer. The argument also applies to every point satisfying this definition.

All vectors q-p are in one open half-plane. Their directions can therefore be assigned angles in one interval of length pi. Group equal angles into blocks B_1,...,B_t in increasing order. Let r_i = |B_i| and N = n-1. Distinct angle blocks correspond to distinct lines through p: opposite rays cannot occur because u dot (q-p) is strictly positive.

For block B_i, let s_i = r_1+...+r_(i-1), and let ell_i be the line through p with this block's direction. It contains exactly r_i+1 points of X. Every earlier block is strictly on one side, and every later block strictly on the other. This follows because the difference of any two angles is strictly between -pi and pi, so the sign of their determinant is the sign of their angular difference. Consequently,

    d_X(ell_i) = |N - r_i - 2 s_i|.                         (1)

This equation counts an entire collinear block as on-line. It never allocates the block arbitrarily between the two sides.

### Even n

Let n=2h, so N=2h-1. Choose the unique block containing position h in the expanded angle list. Thus s_i <= h-1 and s_i+r_i >= h. Define

    a = h-1-s_i >= 0,        b = s_i+r_i-h >= 0.

Then a+b=r_i-1 and N-r_i-2s_i=a-b. Equation (1) gives

    d_X(ell_i) <= r_i-1 = |X intersect ell_i|-2.

### Odd n

Let n=2h+1, where h>=1, so N=2h. Choose the block containing position h. Set

    a = h-s_i >= 1,          b = s_i+r_i-h >= 0.

Then a+b=r_i and N-r_i-2s_i=a-b. Hence

    d_X(ell_i) <= r_i = |X intersect ell_i|-1.

### Conclusion

For each exposed vertex p, if m_p is the maximum collinearity on any line through p, the line selected above satisfies

    d_X(ell_i) <= m_p - 2 + e.                             (2)

In particular, if m is maximum collinearity over all lines,

    D(X) <= min over exposed p of (m_p-2+e) <= m-2+e.

This includes n=2 and the fully collinear case. In the latter case an endpoint is exposed, the angle list has a single block, and equation (1) gives discrepancy 0 exactly. No compactness assumption, perturbation, genericity of X, or finite experiment is used.

## 2. Independent limiting check, and why perturbation does not give a constant

One can perturb the labelled points arbitrarily little into general position while keeping all points distinct. To see existence, choose the perturbed points one at a time inside pairwise disjoint small neighborhoods, avoiding the finitely many lines through previously chosen pairs.

For a general-position configuration, (2) with m_p=2 produces a two-point line of discrepancy at most e. In a sequence of such perturbations converging to X, one fixed pair of point labels determines the selected line along an infinite subsequence. The limiting two original points are distinct, so their line ell is well defined, and these lines converge to ell.

Suppose k original points lie on ell. The signs of all other points relative to the oriented pair stabilize to their original signs, by continuity of a nonzero determinant. The two selected endpoints are always on-line. The remaining k-2 points on the limiting line may each contribute either +1 or -1 before the limit. If S is the stabilized signed sum for the off-line points and C_j is the sum of these k-2 boundary-point contributions, then

    |S+C_j| <= e,             |C_j| <= k-2.

Therefore |S| <= e+k-2. This independently recovers the global bound, not a constant independent of k.

The lost boundary contribution can be arbitrarily large for a chosen sequence of bisectors. For example, fix endpoints (0,0),(1,0), choose M further points above the x-axis which converge to M distinct additional points on that axis, and keep M distinct points below it. The x-axis has discrepancy 0 before the limit and M afterward. The above-axis points can be chosen with positive heights tending to zero. If general position is wanted before the limit, choose their positions and the negative-side positions generically, avoiding the finitely many unwanted collinearities while retaining the strict side signs. This example invalidates a proposed inference that a chosen balanced line keeps its discrepancy in a degenerate limit. It does not claim that the limiting set lacks some other balanced determined line.

## 3. Other exact subclasses and scope controls

### A rich line

If ell contains m points, then its open-half-plane counts add up to n-m. Thus d_X(ell) <= n-m. A line containing at least n-100 points proves the requested bound immediately. Combining with (2) gives the sufficient global estimate

    D(X) <= min(m-2+e, n-m).

This estimate is not asserted to improve known general bounds.

### Central symmetry

Suppose X is invariant under x -> 2c-x. Since X has at least two distinct points, some x differs from c. Both x and its distinct antipode belong to X, so the line through them and c is determined. Every off-line point is paired with its antipode in the other open half-plane. On-line pairs, and c itself if present, are excluded. Therefore the discrepancy is 0. No upper bound on collinearity is needed.

### General-position exact values

When m=2, (2) gives discrepancy at most e. If n is odd, every determined line contains exactly two points, leaving an odd number n-2 off-line; its discrepancy is odd and therefore at least 1. Hence D(X)=e in general position.

### Necessary conditions for a counterexample to 100

Discrepancy is integral. If D(X)>100, then D(X)>=101. Equation (2) forces m_p>=102 for every exposed vertex when n is odd, and m_p>=103 for every exposed vertex when n is even. The rich-line observation forces n-|X intersect ell|>=101 for every determined ell. These conditions are necessary, not sufficient.

### Multiplicities and weights

Distinctness is an essential part of the target. If one changes the model to weighted points at three noncollinear locations, all with weight M, and requires a line through two distinct locations, every admissible line has weighted discrepancy M. That altered problem has no universal constant. Allowing two coincident copies to fulfill the incidence condition changes the model again. Neither convention is substituted for the stated finite-set problem.

## Limits of the result

All statements above are elementary analytic proofs or explicit scope counterexamples. They do not prove D(X)<=100 without additional hypotheses and do not construct a counterexample to it. They are presented as self-contained exposition, without priority or novelty claims. No empirical search is being used to infer a universal theorem.
