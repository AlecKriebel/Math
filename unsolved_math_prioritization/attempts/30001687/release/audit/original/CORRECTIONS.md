# Scope corrections and elementary clarifications

These corrections apply to the author packet whose manifest SHA-256 is `2d657668c7f2b47f4429714e3e597baee441f32f58f262dc7bfb9d62dc5b4d8d`. They preserve its unsolved disposition. They are elementary audit clarifications, not new spectral claims or a sixth proof-search route.

## Required replacement for the finite-gap lemma statement

Let `m>=1` be finite. Let all functions `a,b,u_i,v_i`, for `1<=i<=m`, be C1 on a one-sided neighborhood `[0,epsilon)` of zero. Put `I_t=[a(t),b(t)]`, `G_i(t)=(u_i(t),v_i(t))`, and `g_i(t)=v_i(t)-u_i(t)`. Assume:

1. `a(0)<b(0)` and `u_i(0)=v_i(0)=c_i`, with the `c_i` pairwise distinct and strictly inside `(a(0),b(0))`.
2. `g_i'(0)>0` for every i.
3. For sufficiently small positive t the gaps lie in the hull and are pairwise disjoint.

Then `Phi(I_t minus union_i G_i(t))` is strictly decreasing for all sufficiently small positive t. The interval may depend on the full finite collection.

**Proof.** Label the gaps in their fixed spatial order. For any fixed presentation and endpoint, the bridge length `B(t)` is the difference of two of the listed C1 endpoints. Distinct interior collapsed centers imply `B(0)>0`. Positivity of `g_i'(0)` ensures `g_i(t)>0` for small positive t. The numerator of the derivative of `B(t)/g_i(t)` tends to `-B(0)g_i'(0)<0`. Take the minimum of the finitely many valid intervals for all `2m*m!` ratios. On that common interval every ratio strictly decreases. For finitely many strictly decreasing functions, their minimum is strictly decreasing by choosing a minimizer at the earlier argument; their maximum is strictly decreasing by choosing a maximizer at the later argument. Applying these two observations proves the claim.

The `m>=1` condition is necessary: with no gaps, the standard convention is `Phi(I_t)=infinity`, a constant.

## Why hull regularity must be explicit

For `t>0` small, take the single gap `(-t/2,t/2)` and hull `[-B(t),2]`, where `B(t)=1+t^2*sin(1/t^2)` and `B(0)=1`. Every gap endpoint is smooth through zero, and the left hull endpoint is differentiable at zero. The left bridge is shorter for small t, so

`Phi(t)=1/t+t*sin(1/t^2)-1/2`.

At `t_n=((2n+1)*pi)^(-1/2)`, its derivative is `1/t_n^2>0`. The hull function is not C1 at zero. Thus a reading of the original lemma imposing C1 only on the gap endpoints is insufficient.

Likewise, smoothness for positive t and linear opening alone are weaker than the corrected hypothesis. In the fixed hull `[-1,1]`, use the symmetric gap of length `g(t)=t+t^3*sin(1/t^2)` for small positive t. Although `g(t)/t->1` and the positive-t endpoints are smooth, at `t_n=(2*pi*n)^(-1/2)` one has `g'(t_n)=-1`, so `Phi(t)=1/g(t)-1/2` has positive derivative. This is a general countercontrol, not a spectral example.

## Explicit failure of a uniform interval

For each integer `n>=3`, let the hull be `[-1,1]` and the sole gap be symmetric with length

`g_n(t)=t/(1+n^2*t^2)`.

Every member separately satisfies the corrected C1 assumptions, with `g_n'(0)=1` and the same collapsed center. Its finite-gap quantity is

`Phi_n(t)=1/t+n^2*t-1/2`.

The derivative is negative on `(0,1/n)` and positive on `(1/n,infinity)`. In particular it is positive at `t=2/n`. Therefore no interval of decrease common to this family follows from the qualitative hypotheses alone. This illustrates dependence on the data; it does not claim these different one-gap sets are truncations of one Cantor family.

## Exact treatment of equal-size blockers

For a compact Cantor set with a nondegenerate bounded hull, or for a finite union of nondegenerate intervals, let a gap `G=(u,v)` have length g. On each side, measure the distance from the corresponding endpoint of G to the nearest gap of length at least g, stopping instead at the hull boundary if there is no such gap. Divide these distances by g and let S be the infimum of all such ratios.

For any presentation, a hull-boundary candidate bounds its corresponding endpoint ratio from above. For a gap-blocker candidate, let H be the blocking gap and M the intervening distance. Whichever of G and H is removed later has an endpoint bridge toward the earlier gap of length at most M. Its denominator is at least g, so some presentation ratio is at most `M/g`. Hence the infimum for any presentation is at most every candidate, and thickness is at most S.

In a decreasing-length presentation, every previously removed gap has length at least that of the current gap. A bridge cannot be shorter than the distance to the nearest gap of at least that length. Thus every ratio is at least S, proving equality. A tied blocker removed later may make an individual bridge longer; the preceding upper-bound argument assigns its candidate to the gap removed later and resolves the apparent inconsistency. For a Cantor set, the decreasing-length enumeration exists because there are only finitely many gaps above each positive length threshold.

## What exact true-gap exhaustion would establish

Let K be a compact Cantor set and `F_N` an increasing sequence of finite sets of its actual bounded gaps that exhausts all of them. Preserve K's exact hull and put `K_N=I minus union_{G in F_N} G`. Then

`Phi(K_N)` decreases to `tau(K)`.

Filling-gap monotonicity proves that these quantities decrease and stay at least `tau(K)`. Conversely, use any candidate ratio in the exact blocker formula just proved. Its gap and, if present, its blocking gap both lie in `F_N` for large N. No missing gap of length at least the selected gap lies closer than its nearest blocker in K. Thus the same candidate occurs in `K_N`, so the limit of `Phi(K_N)` is at most every candidate. Taking their infimum gives the opposite inequality and proves equality.

This establishes an elementary generic limit identity under precise true-gap exhaustion hypotheses. It does not identify the author's periodic covers with those `K_N`, certify their endpoints, or prove uniformity in coupling. If all exact true-gap truncations were nonincreasing on one common coupling interval, their pointwise limit would be nonincreasing there. Having a different interval for every N is inadequate, as is knowing merely that each truncation is an upper bound. Strict decrease need not survive an infinite limit.

## Precise replacement for the sufficient presentation comparison

Fix `0<lambda_1<lambda_2`. Suppose there is a bijection between the bounded gaps of the two spectra, with a consistent correspondence of their endpoints. Transporting the ordered gap labels then gives a bijection between all presentations. Assume that for every presentation P at `lambda_1` and every gap endpoint e, the ratio for the corresponding endpoint in the transported presentation at `lambda_2` is at most the ratio at `(P,e)`.

Taking the infimum over the corresponding endpoints first gives the inequality for each presentation. Taking the supremum over all presentations, using surjectivity of the induced presentation map, then gives

`tau(Sigma_(lambda_2)) <= tau(Sigma_(lambda_1))`.

This is a sufficient conditional criterion only. The required inequalities have not been proved for the Fibonacci spectra. A map whose image omits presentations at the second coupling is insufficient for this supremum argument.
