# Independent adversarial verification of the rank-restriction extension

Scope: only the stronger rank-restriction route in diagonal_review/INDEPENDENT_DERIVATION.md. This is an additive postseal audit finding, not a sixth author turn, a novelty certification, or resolution of sharp prefix growth. The preceding 32-path probability package and both independence seals are preserved byte exact.

**Verdict: the stronger route is supported.** No unsupported central step or counterexample was found. A universal argument below proves, for independent P(i in A)=1/i and subset representations,

    log M(D) = O(log D/(log log D)^2 + (log log D)^2)

almost surely as D tends to infinity. In particular,

    log M(D) log log D / log D -> 0 almost surely.

The bound is still far above the credited polylogarithmic lower scale. It does not give a finite sharp exponent for log M(D)/log log D. Statements about priority remain outside this verification.

## 1. Universal row-restriction lemma

Let F be any finite family of k distinct subsets of a finite ground set S. For each a in S let omega_a in {0,1}^k be its incidence column across the family, let 1=(1,...,1), and set R=dim span(1,{omega_a})-1.

Choose R incidence columns completing 1 to a basis. Their R-bit row signatures must be pairwise different. If two rows had the same signature, they agree on every basis column including 1, hence on every incidence column, so the two subsets would be identical. Thus k<=2^R.

If R>=r, choose 1 and r incidence columns linearly independent over Q. Form the k by (r+1) matrix of these columns. Its column rank is r+1, so it has r+1 linearly independent rows. Restrict to those rows. The restricted columns remain independent, including the constant column, and the ambient dimension is exactly r+1. The restricted family has r+1 distinct subsets: coincident rows would contradict invertibility. If all original subsets have the same sum, so do these selected subsets. All their other restricted incidence columns lie in the same ambient Q^{r+1} and hence have quotient rank at most r; the selected independent columns force quotient rank exactly r.

Consequently, for any r>=1,

    {m(A intersect G)>2^{r-1}} subset E_r(G),

where E_r(G) means that r+1 distinct equal-sum subsets with full quotient rank r exist in A intersect G. This is deterministic event inclusion, not a union bound over rows or original families. No factor depending on k, m(A intersect G), the number of original equal-sum families, or the number of possible row selections is required. The inclusion need not be an equivalence; the fresh weighted controls exhibit that distinction.

## 2. Uniform occupancy event

Take integer T sufficiently large, 0<=u<T, G=[ceil(exp u),floor(exp T)] intersect N, epsilon=1/20, lambda=log(1+epsilon), and a positive t. Let the logarithmic endpoint grid consist of u and the integers floor(u)+1,...,T+1. Define H by

    N(G intersect [exp alpha,exp beta)) <= (1+epsilon)(beta-alpha)+t

for every alpha<=beta in this grid, together with

    N([1,exp u)) <= (1+epsilon)u+t.

Empty intervals cause no problem. For the intervals used below u tends to infinity, so all high-ground entries are at least two. For any such integer interval its harmonic mean is at most beta-alpha+C with an absolute C; truncation to G only reduces it. For the low prefix the mean is at most u+C, including the deterministic first indicator.

Independence yields E exp(lambda N)<=exp((exp lambda-1)E N)=exp(epsilon E N). Markov then bounds a failure for length L by

    exp(epsilon C-[lambda(1+epsilon)-epsilon]L-lambda t)
       <= C_0 exp(-lambda t).

The bracket is positive since (1+epsilon)log(1+epsilon)>epsilon. There are O((T+2)^2) intervals, so P(H^c)<=C_1(T+2)^2 exp(-lambda t). Take t=10log(T+2)/lambda to obtain O(T^-8). No independence between occupancy events for different T is used.

## 3. Greedy pivots and every residual column

On E_r(G), take an ordered witness of r+1 subsets and read the selected integers of S=A intersect G in decreasing order. Start with V_0=span(1), and retain a column exactly when it increases the span. The quotient rank is r, so this selects exactly r pivots x_1>...>x_r with representatives v_1,...,v_r independent modulo the diagonal. Put V_j=span(1,v_1,...,v_j), dim V_j=j+1.

For any nonpivot a>x_{j+1}, its column belongs to V_j. Above x_1 it belongs to V_0. The pivots used here are re-selected after row restriction; using only the originally chosen r independent columns without this greedy step would not justify the ordered support condition.

Put z_j=floor(log x_j). Then z_1>=...>=z_r>=floor u>=0 for all sufficiently large T and z_j<=T. For j<r assign residual entries in

    [exp(z_{j+1}+1),exp(z_j+1)) intersect G

to V_j; assign residual entries in [exp u,exp(z_r+1)) intersect G to V_r. Entries at or above exp(z_1+1) are diagonal. This enlarged partition includes every true greedy assignment because exp(z_{j+1}+1)>x_{j+1}. Tied z_j produce empty middle intervals; vectors in the resulting lowest equal-band layer are allowed in the largest corresponding V_j, which is an enlargement. Ceil/floor in G and half-open endpoints preserve the partition, including the case exp u is an integer.

## 4. Cube classes and exact reconstruction

Every d-dimensional rational subspace admits d coordinate projections that are jointly injective, because a matrix for a basis has d independent coordinate rows. Thus V_j intersect {0,1}^{r+1} has at most 2^{j+1} members. Both 0 and 1 are present and coincide modulo V_0. These are the only distinct binary vectors differing by a constant in every coordinate: a nonzero such constant must be +1 or -1, forcing the 0/1 pair. Hence the number of quotient classes is at most

    Q_j=2^{j+1}-1, h_j=log Q_j.

For a fixed ordered basis (v_j), band tuple (z_j), and residual selected set B=S minus {x_1,...,x_r}, the number of possible residual quotient sums is at most product_j Q_j^{n_j}, where n_j counts B in the enlarged j-th interval. Diagonal entries above the first band contribute the unique zero class. Choosing between common inclusion/exclusion adds no quotient-sum choice. Multiple assignments producing the same quotient sum only overcount this upper bound.

The equal-sum equation modulo V_0 is

    sum_j x_j [v_j] = -sum_{a in B} a [omega_a].

The r pivot classes are independent in an r-dimensional quotient, so each possible residual sum determines a unique rational pivot tuple. Discard any tuple whose entries are not distinct integers in G, not strictly decreasing, not in their designated bands, or intersect B. Valid tuples alone create possible selected sets S. Distinct assignments can recover the same selected set; counting all assignments remains an upper bound. No additional summation over individual root values is present.

For each valid tuple the finite Bernoulli law on G gives exactly

    P(A intersect G=S)/P(A intersect G=B)
       = product_j 1/(x_j-1) <= 2^r exp(-sum_j z_j),

because all roots are at least two and x_j>=exp z_j. Independence is used only on distinct support entries. The odds, not 1/x_j, are needed because B leaves those entries unselected.

If S obeys H, deleting the roots leaves B obeying all needed upper occupancy bounds. Summing P(A intersect G=B) over the eligible residual sets is at most one. This does not assert that greedy deletion preserves a distribution or conditions the residual Bernoulli law. It simply bounds each witness-selected set by the unconditional probability of its own residual set.

## 5. Complete uniform count, without hidden family dependence

For fixed basis and bands the preceding steps give probability on H at most exp(E), where

    E=(1+epsilon)[sum_{j<r}(z_j-z_{j+1})h_j+(z_r+1-u)h_r]
          -sum_j z_j+t sum_j h_j+r log2.

Indeed every residual interval's logarithmic length is exactly the displayed length, including zero-length tied intervals, and the H upper bound is inherited by B. Using t for every interval is a safe enlargement. Its error is O(t r^2); a sharper cumulative-count argument is unnecessary here.

Let b=(1+epsilon)log3-1>0. Telescoping yields coefficient b on z_1, and coefficient (1+epsilon)log(Q_j/Q_{j-1})-1 on z_j for j>=2. Since Q_j/Q_{j-1}<=7/3 and (21/20)log(7/3)<1, all latter coefficients are negative. Thus, using z_1<=T and z_j>=0,

    E <= bT-(1+epsilon)u h_r+(1+epsilon)h_r+t sum_j h_j+r log2.

The two strict sign claims are certified by exact rational logarithm intervals in the fresh controls; their analytic origin is the elementary atanh series.

There are at most (2^{r+1})^r=2^{r(r+1)} ordered binary bases; dependence only removes choices. There are at most (T+1)^r band tuples z_j in {0,...,T}; ordering only removes choices. These are the entire union counts. The original witness family's size and row-selection choices have already been removed by the deterministic event inclusion in Section 1.

Since h_j<=(j+1)log2, we have sum_j h_j=O(r^2). Combining everything,

    P(E_r(G) intersect H)
      <= exp[bT-(1+epsilon)u h_r+O((1+t)r^2+r log(T+1))],

with absolute constants for the fixed epsilon. This bound is universal in r,T,u,t within the stated domain. It introduces no unspecified fixed-r or fixed-family constant before choosing growing r.

## 6. Growing rank, summability, full-prefix interpolation

Set delta=1/100,

    r=floor((log T)^2),
    u=(b+delta)T/((1+epsilon)h_r),
    t=10log(T+2)/lambda.

For all sufficiently large integer T, r>=1, 0<u<T, u tends to infinity, and h_r is asymptotic to r log2. The main exponent is exactly -delta T. The error satisfies

    (1+t)r^2+r log(T+1)=O((log T)^5)=o(T).

Hence the rank-witness probability on H is eventually at most exp(-delta T/2), and the occupancy failure is O(T^-8). Both are summable in integer T. Borel-Cantelli I gives, on one probability-one event, H and absence of E_r(G) for all sufficiently large integer T. No inter-T event independence is needed.

By the row-restriction lemma, m(A intersect G)<=2^{r-1}. The low prefix [1,exp u) and G partition the selected elements up to exp T. Convolution of nonnegative subset-sum coefficients yields

    M(exp T)<=2^{N([1,exp u))}m(A intersect G),

so H gives

    log M(exp T)<=(log2)((1+epsilon)u+t+r-1)
          =O(T/(log T)^2+(log T)^2).

For arbitrary large D choose the integer T=ceil(log D). Monotonicity gives M(D)<=M(exp T); T/log D and log T/log log D tend to one. This proves the advertised bound for all real D, and its larger-normalization limit zero because log M(D)>=0. A possibly immense deterministic starting scale is harmless; no effective small-scale numerical threshold is claimed.

## 7. Adversarial outcome, recent-source comparison, exact gap

Fresh exact controls passed 42,829 assertions across 1,573 families. They independently select invertible rows, re-greedy all restricted columns, check tied-band support, all cube-section quotient classes, exact roots/odds, and weighted event inclusion without a row factor. Exact dyadic bands are used to eliminate floating-rounding error; the proof above handles natural-log bands universally. These finite checks do not establish an asymptotic theorem by themselves.

The inspected diagonal control code correctly covers its finite intended identities. Its floating log/telescoping controls are supplementary numerical checks, not exact certificates of asymptotic coefficient signs; the fresh adversary supplied rational sign certificates and the universal calculation. The replay output embeds time/runtime, so structural receipts are compared; byte-exact replay is deliberately not claimed for it.

The [Mao-Song v2](https://arxiv.org/pdf/2609.22296v2) pages 6-12 identify problems with classifying arbitrary subflags using cube intersections and with allowing unconstrained labels above the first threshold. This argument classifies no arbitrary subflags and obtains its diagonal-support restriction from decreasing greedy exposure on every selected column. It also counts quotient classes directly rather than relying on the disputed general residual lemma. Its validity uses no result from the unaudited 81-page general framework. Raw source pages remain private.

Mandatory changes to the stronger derivation: none. Keep the row-restriction existence lemma, re-greedy step, valid-root filtering, exact odds, and uniform count explicit in any promoted additive statement. Do not replace the one-way event inclusion by equality or assume a reverse multiplicative convolution inequality.

Strongest verified extension: the larger logarithmic normalization tends to zero almost surely. Exact remaining gap: the bound divided by log log D still diverges as an upper envelope, so it establishes no finite sharp leading exponent, no equality/value of the original tail liminf/sup, and no convergence in probability on that original normalization. No priority certification or new author turn is warranted merely by this audit.

Checkpoint: 2026-10-03 07:13 UTC (exact evidence time in manifest). Completion estimate: 95%; final integrity binding remains.
