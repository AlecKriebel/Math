# Root verification of the additive rank-restriction deduction

2026-10-03: checkpoint80%, original sharp-prefix resolution0%. This is an audit deduction, not a sixth author turn, replacement of frozen history, priority certification or complete solution. Root independently read the full candidate-free diagonal derivation, the separate universal adversarial proof and every associated control source, and privately reproduced their complete control outputs with only explicitly identified UTC/runtime exceptions. A fresh whole-package reviewer separately scrutinizes the extension after sealing its own source-first original mathematical verdict.

For independent P(n in A)=1/n and distinct finite subset representations, the supported stronger partial conclusion is, almost surely,

    log M(D)=O(log D/(log log D)^2+(log log D)^2).

Consequently log M(D) log log D/log D tends to0. The original sharp exponent log M(D)/log log D remains unresolved. The implied upper envelope on that original scale still diverges. No conclusion about finite/equal tail constants, an in-probability sharp exponent or novelty follows.

## Deterministic compression of the witness

For a family F of k distinct equal-sum subsets, let omega_n be its binary membership columns and let R be the rank of these columns modulo the all-one vector. Choose R columns completing the diagonal vector to a basis. Two equal R-bit row signatures would agree on the whole basis, hence on every membership column, making the corresponding subsets identical. Therefore k<=2^R.

If R>=r, choose r independent quotient columns. The matrix formed by these columns and the all-one column has rank r+1, so some r+1 rows form an invertible square matrix. Restrict to those rows. Their subsets remain distinct and equal-sum, and their quotient rank is exactly r, since the ambient dimension is r+1. Thus a fiber with more than2^(r-1) subsets implies existence of an r+1-member full-rank witness. This is a deterministic inclusion of events. Counting every possible original family and row choice would insert an unnecessary huge factor: we count only arbitrary resulting witnesses. Re-greedy the entire restricted incidence system; the originally chosen columns alone need not have the descending support property.

## Independent occupancy control

Fix epsilon=1/20, lambda=log(1+epsilon), b=(1+epsilon)log3-1 and delta=1/100. For integer T tending to infinity let

    r=floor((log T)^2), h_j=log(2^(j+1)-1),
    u=(b+delta)T/((1+epsilon)h_r),
    t=10log(T+2)/lambda, G=[ceil(exp u),floor(exp T)].

Eventually r>=1 and0<u<T, and u tends to infinity. Use all half-open logarithmic intervals with endpoints u and floor(u)+1,...,T+1, intersected with G, and also the low prefix[1,exp u). Each mean is at most its logarithmic length plus an absolute constant. The independent Bernoulli moment-generating function is bounded by exp(epsilon times mean), including deterministic1 in the low prefix. A count exceeding(1+epsilon)length+t has probability at most

    exp(epsilon C-[lambda(1+epsilon)-epsilon]length-lambda t)
       <= C' exp(-lambda t).

The bracket is positive, and the grid has O(T^2) intervals. The joint failure probability is O(T^-8), summable in integer T. Deleting pivots reduces every count, so all high-window occupancy bounds transfer to residual selected sets. No conditional-distribution or independence-of-deletions claim is needed.

## Exhaustive witness count

Scan a full-rank r+1-member witness's selected entries downward, recording each column that increases the span modulo the diagonal. This gives r distinct pivots x_1>...>x_r and an ordered binary basis v_1,...,v_r. Above the next pivot, every unrecorded column is in the earlier span; above the first pivot all are diagonal. Let z_j=floor(log x_j), with0<=z_r<=...<=z_1<=T.

For j<r, enlarge the residual j-th region to[exp(z_(j+1)+1),exp(z_j+1)); use[exp u,exp(z_r+1)) for the final region. This is a partition after intersecting G, with diagonal-only entries above exp(z_1+1). Rounded equal pivot bands cause empty middle regions and a safely enlarged span in their bottom region. Every endpoint is in the occupancy grid. Strict/half-open and ceiling conventions cover an integral exp u without omission.

The span of the diagonal and the first j pivots has dimension j+1. Some j+1 coordinate projections are injective on it, so its cube section has at most2^(j+1) points. Quotienting identifies only the zero/all-one pair, hence at mostQ_j=2^(j+1)-1 classes. Choosing between common inclusion/exclusion contributes no quotient choice.

For a fixed residual selected set B, basis and band tuple, enumerate every permissible residual quotient assignment. Each determines a residual vector sum. The r independent quotient pivot columns determine at most one rational root tuple x. Discard nonintegral, repeated, wrongly ordered, wrongly banded or residual-overlapping roots. Every actual witness survives this enumeration; repeated assignment descriptions merely overcount. There is no remaining sum over individual pivot values.

For each valid tuple, the exact product Bernoulli law on G gives

    P(A intersect G=B union{x_j})
       =P(A intersect G=B) product_j 1/(x_j-1)
       <=P(A intersect G=B)2^r exp(-sum_j z_j).

This uses distinct coordinates at least2. The residual-set probability is its unconditional Bernoulli mass; deletion is not asserted to preserve its law. Summing those masses gives at most1. The low-prefix occupancy event can be dropped during this high-window union bound, so no illicit conditioning on it appears.

On the occupancy event, a fixed basis and band tuple therefore costs at most exp(E), with

    E=(1+epsilon)[sum_(j<r)(z_j-z_(j+1))h_j
                   +(z_r+1-u)h_r]
      -sum_j z_j+t sum_j h_j+r log2.

Telescoping gives b z_1 and coefficients(1+epsilon)log(Q_j/Q_(j-1))-1 on later z_j. These are all negative because Q_j/Q_(j-1)<=7/3 and(21/20)log(7/3)<1. An exact certificate is exp(20/21)>sum_(m=0)^4(20/21)^m/m!>7/3; the exponential series remainder is positive. Also b>0. Hence

    E<=bT-(1+epsilon)u h_r+(1+epsilon)h_r
        +t sum_j h_j+r log2.

There are at most2^(r(r+1)) ordered binary bases and(T+1)^r band tuples. These counts already encode every ordered restricted witness; no original-family or row-selection multiplicity is needed. Since h_j<=(j+1)log2, the complete union exponent is

    -delta T+O((1+t)r^2+r log(T+1))
       =-delta T+O((log T)^5).

All constants are absolute after fixing epsilon/delta; no constant depending on an earlier fixed r is silently applied to growing r. The error is o(T), giving an eventually summable exp(-delta T/2) witness probability.

## Almost-sure full-prefix bound

First Borel–Cantelli, with no inter-scale independence, makes the occupancy bounds and absence of rank-r witnesses hold eventually on one probability-one event. The high-window maximum is then at most2^(r-1). The disjoint low prefix and high window partition A intersect[1,exp T]. Nonnegative coefficient convolution bounds the full maximum by2^(low count) times the high maximum, so

    log M(exp T)<=(log2)((1+epsilon)u+t+r-1)
                =O(T/(log T)^2+(log T)^2).

For real D choose T=ceil(log D) and use monotonicity. The normalization is comparable because T/log D and log T/log log D tend to1. The nonnegative normalized logarithm therefore tends to0.

## Checkable evidence and limits

Root's private reproduction verified all100 hash-bound members across the four distinct packages, plus their manifests, and21 seal-member instances. It reran the source-first probability controls, separate probability cross-controls, exact moments controls, diagonal rank/root controls, exact insertion kernel, separate extension controls and two integrity verifiers. Stable full outputs are byte-exact; the two diagonal programs differ only in their declared UTC/runtime fields. The entire moment report matches except two UTC fields. Original sealed moment mathematics is unchanged despite its explicitly documented opening metadata correction. Every preserved family author/historical output equals root's already reproduced full stream.

The extension adversary's42,829 exact controls and diagonal rank/root/insertion controls corroborate finite mechanisms; the universal argument above supplies the infinite result. It relies on no general weak/strict entropy equality, disputed arbitrary-subflag classification, unaudited recent full framework, divisor transference or numerical simulation. The five original author turns remain immutable. Their weaker bounds remain valid, and historical pending statements remain historical. Promotion records this stronger deduction separately and retains **unsolved,5/5**.
