# Stage 2: unrestricted adaptive residuals

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 2. Exact model: p prime, k=floor(sqrt(p)), A uniform among k-subsets of F_p, and cap c=floor(100 sqrt(p)).

## Findings

1. A proposed residual estimate uniform over every adaptive centre sequence is false, with high probability, by a fully collective protected-translate construction. This is not another small-menu restriction.
2. The globally optimal residual already has a direct bounded-differences concentration theorem. The unresolved part is a lower bound on its expectation, rather than taking a union bound over all centre sets.
3. A cumulative-gain condition, explicitly left unproved, would suffice for a global negative answer while allowing the counterexample in item 1. An estimate restricted to the actual greedy algorithm would only show failure of that algorithm.

No full collective affirmative construction was obtained.

## 1. Protected translates refute pointwise residual mixing

For any nonempty A of size k, define

`D={t in F_p : (A+t) intersection A is empty}`, and `d=|D|`.

Assume d>=k. Choose centres one at a time by maximizing the newly covered points among the allowed centres D. Let T_i be the first i centres and let `s_i=|A+T_i|`.

### Exact incidence bound

For every current covered set S,

`sum_{t in D}|(A+t)\S| = dk - sum_{x in S} deg_D(x) >= dk-k|S|`,

because every point belongs to exactly k translates from the full family, and hence to at most k translates indexed by D. Averaging gives an available translate with at least

`k(1-|S|/d)`

new points whenever this right-hand side is positive. Previously selected translates have zero marginal gain, so a positive-gain choice is automatically new. When the right-hand side is nonpositive, monotonicity of coverage is sufficient. Therefore

`s_{i+1} >= s_i + k(1-s_i/d)`

holds, and induction gives

`s_i >= d[1-(1-k/d)^i]`.

Every selected translate avoids A, so A itself remains entirely uncovered throughout the construction.

### Typical A supplies linearly many allowed centres

`D=F_p\(A-A)`. The exact-model elementwise-map theorem proved in Stage 1, applied to the single map phi(a)=-a, gives with high probability

`d >= p/(2e)`.

This invocation uses the theorem's established uniform-k proof, not an untransferred Bernoulli assertion.

Take i=k. Since d<=p and `k^2/p -> 1`,

`s_k >= d[1-exp(-k^2/d)] >= p/(4e)`

for all sufficiently large p on the displayed event. Let `U=F_p\(A+T_k)`. Then

`A subset U`, `|U|/p <= 1-1/(4e)`, and

`max_t |(A+t) intersection U| = k`.

Consequently

`max_t |(A+t) intersection U| - k|U|/p >= k/(4e)`.

This is much larger than `O(sqrt(k log p))`. Thus a statement asserting

`max_t |(A+t) intersection U_T| <= k|U_T|/p + O(sqrt((k|U_T|/p) log p))`

uniformly over all adaptively chosen T of size at most k is false with high probability.

### Scope

The construction uses all of A collectively in defining D and choosing the centres. It protects only one translate A, and adding centre 0 covers that protected translate at once. The remaining uncovered set can still be large; no claim of full coverage after that addition is made.

This refutes an overly strong pointwise residual-mixing lemma. It does not refute a global covering obstruction. It also does not describe the unrestricted greedy algorithm: once the protected translate has larger marginal gain than the best centre in D, unrestricted greedy can select it. Any valid proof must allow or account for such exceptional translates rather than treating every residual as an independent random subset.

## 2. Optimal residual concentration needs no centre-set union bound

For a fixed integer m, define the unrestricted optimal residual

`R_m(A)=min_{T subset F_p, |T|<=m} |F_p\(A+T)|`.

For every fixed T, swapping one element of A changes its residual count by at most 2m. The minimum of a family of functions with the same Lipschitz constant retains that constant: use a minimizing T for one input to bound the change in one direction, and reverse the roles for the other direction. Thus R_m is swap-Lipschitz with constant 2m, even though a minimizing T may change completely after the swap.

Uniform-subset martingale exposure, as proved in Stage 1 Section 1, therefore gives the exact finite bound

`Pr(R_m(A) <= E R_m(A)-u) <= exp(-u^2/(8km^2))`,

and the analogous upper-tail bound.

In particular, for `m=c=floor(100 sqrt(p))`, any fixed eta>0 such that

`E R_c(A) >= eta p`

for all sufficiently large primes would imply

`Pr(R_c(A)=0) <= exp(-Omega_eta(sqrt(p))) -> 0`.

The same assertion along arbitrarily large primes gives a stronger-than-required negative subsequence result. This route is fully adaptive and requires no entropy union bound. It has not been completed: the expectation is an expectation of the minimum, and fixed-T expectation lower bounds do not lower-bound it.

### A useful converse necessary condition

Let `P_p=Pr(R_c(A)=0)` and `mu_p=E R_c(A)`. The preceding inequality implies

`P_p <= exp(-mu_p^2/(8kc^2))`.

Hence if P_p>=delta>0 along a sequence of primes, then

`mu_p <= sqrt(8kc^2 log(1/delta)) = O_delta(p^(3/4))`.

If P_p tends to one, the bound strengthens to `mu_p=o(p^(3/4))`.

Conversely, `mu_p=o(p)` or even a much smaller expected residual does not establish exact coverage or the required probability limit. Repairing a sublinear residual can still exceed the remaining translate budget.

## 3. Exact cumulative-gain identity

Consider any ordered sequence of distinct centres `t_1,...,t_m`, chosen with arbitrary dependence on A. Set

`T_i={t_1,...,t_i}`, `U_i=F_p\(A+T_i)`, `u_i=|U_i|`,

`g_i=|(A+t_i) intersection U_{i-1}|`,

`e_i=g_i-(k/p)u_{i-1}`, and `q=1-k/p`.

The recurrence is exact:

`u_i=q u_{i-1}-e_i`.

Unrolling gives

`u_m=p q^m - sum_{i=1}^m q^(m-i)e_i`.

At the operational cap, `q^c -> exp(-100)`. Therefore any covering sequence with m<=c must achieve weighted cumulative excess

`sum_{i=1}^m q^(m-i)e_i = p q^m >= (exp(-100)-o(1))p`.

Since all weights lie in [0,1], a necessary condition for such a cover is

`sum_{i=1}^m max(e_i,0) >= (exp(-100)-o(1))p`.

This is a quantitative requirement on unrestricted adaptive success. The protected-translate example can generate a single excess of order k, but that is o(p) and so does not invalidate an aggregate excess bound.

## 4. A precise unproved full-route lemma

The following statement would settle the original target negatively, but is NOT proved here:

> There is a fixed b<exp(-100) such that, with probability tending to one, every ordered sequence of at most c distinct centres satisfies `sum_i max(e_i,0)<=bp`.

A stronger, more natural-looking version is an o(p) upper bound. Neither version follows from the results established in these passes.

One sufficient exceptional-step formulation is also precise. Put `gamma=exp(-100)/404`. Suppose, with high probability, every sequence of at most c centres has at most gamma k steps satisfying `e_i>gamma k`. Since `e_i<=k`, its total positive excess would then be at most

`c gamma k + gamma k^2 <= (101 gamma+o(1))p < exp(-100)p`.

The exact identity would rule out every legal cover. This condition tolerates a sublinear number of protected-translate-type anomalies, unlike the false pointwise estimate. Establishing it requires new control of collective adaptivity; it is not an established probabilistic theorem.

The constants are chosen only to verify the exact cap reduction. No effectiveness claim is made for any finite prime.

## 5. Why familiar conditioning shortcuts do not establish the missing lemma

- Observing one whole translate A+t with its centre already reveals all of A. There is no independent collection of unexposed translate edges left afterward. Deferred-exposure arguments for independent random hypergraphs cannot be transferred by merely replacing the edges with translates.
- Conditioning only on a coarser greedy history does leave randomness, but the conditional distribution of A is constrained by all previous gain comparisons. It is not the original uniform-subset law. No valid bound on that conditional law was supplied here.
- Direct concentration of each fixed-T residual has an exponent of order sqrt(p) for a constant-density deviation, whereas the family of all legal T has logarithmic size of order sqrt(p)log(p). That standard union bound fails.
- The globally optimal residual has concentration despite this entropy issue, but its expectation remains uncontrolled. Interchanging a minimum and expectation in the favorable direction would be invalid.
- Showing that the unrestricted greedy algorithm needs logarithmically many rounds would be only an algorithmic lower bound. The target allows other collective choices and does not require an efficient algorithm.

## Disposition

The protected-translate construction is a proved counterexample to an intended universal pointwise residual lemma. Optimal-residual concentration and the weighted-excess identity are valid unrestricted reductions. The expectation lower bound or cumulative-excess theorem needed for a full negative answer remains unproved, and no full affirmative construction was obtained.

