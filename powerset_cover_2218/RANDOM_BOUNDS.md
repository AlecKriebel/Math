# Explicit random-coloring bounds for principal ideals

## Scope and status

This note gives self-contained probabilistic **upper bounds**, with finite sufficient conditions and explicit constants. It does not establish a growing lower-order gap above the elementary lower bound. In particular, it does **not** solve the conjecture that the unrestricted covering threshold minus `log_2 n` tends to infinity.

The coefficient 2 in the logarithmic correction is **not claimed as new**. Erdős and Hajnal's 1968 paper displays a coefficient-3 upper bound and explicitly states a coefficient-`2+epsilon` refinement on printed page 347. The arguments below supply direct finite proofs rather than reproducing the source's text or proof.

Public primary reference: P. Erdős and A. Hajnal, *On a combinatorial problem* (1968), [public PDF](https://users.renyi.hu/~p_erdos/1968-01.pdf). This historical comparison is not a claim about the problem's current solved/unsolved status.

## 1. Definitions and conventions

Let `[n]={1,...,n}`. The principal ideal `P(Y)` is the entire power set of `Y`, **including both the empty set and Y itself**. We seek a function such that

\[
\{f(A):A\subseteq Y\}=[n]
\qquad\text{for every }Y\in\binom{[n]}h.
\]

The unrestricted model allows every function `f:P([n])->[n]`. Its least feasible threshold is denoted `H_u(n)`.

The exterior model additionally requires `f(A) notin A` whenever `A` is a proper subset of `[n]`. The value at `[n]` is arbitrary, since an exterior value there cannot exist. Its least feasible threshold is denoted `H_e(n)`. Equivalently, one may define the exterior function only on proper subsets and make any extension at `[n]`.

A covering property at size `h` implies the same property for every larger tested size: a larger set contains an `h`-set, and its principal ideal contains that smaller principal ideal. Thus `H_u(n)<=H_e(n)`.

Throughout, `ln` is the natural logarithm, `log_2` is base two, and `L=log_2 n`.

## 2. Unrestricted finite bound

Independently for every `A subseteq [n]`, choose `f(A)` uniformly from `[n]`. Fix `Y` of size `h` and a color `i in [n]`. The `2^h` values indexed by `A subseteq Y` are independent. Therefore

\[
\Pr\bigl(i\notin f(\mathcal P(Y))\bigr)
=\left(1-\frac1n\right)^{2^h}
\le \exp\left(-\frac{2^h}{n}\right).
\]

There are `n binom(n,h)` pairs `(Y,i)`. The union bound gives

\[
\Pr(\text{some ideal misses some color})
\le n\binom nh\left(1-\frac1n\right)^{2^h}
\le n\binom nh\exp\left(-\frac{2^h}{n}\right).
\tag{U}
\]

Consequently, for integers `n>=2` and `1<=h<=n`, either of the following is a sufficient condition for `H_u(n)<=h`:

\[
n\binom nh\left(1-\frac1n\right)^{2^h}<1,
\tag{U-exact}
\]

or the simpler, stronger condition

\[
2^h>n\left(\ln n+\ln\binom nh\right).
\tag{U-simple}
\]

Only independence within each fixed missing-color event was used. The events for different pairs `(Y,i)` need not be independent.

## 3. Exterior finite bound and exact products

For every proper `A subsetneq [n]`, independently choose `f(A)` uniformly from `[n] minus A`. For now let `1<=h<n`, so all subsets of a tested `h`-set are proper.

Fix `Y` of size `h` and a color `i`. A subset `A subseteq Y` can receive color `i` precisely when `i notin A`, and then its probability of doing so is `1/(n-|A|)`.

If `i in Y`, the eligible subsets are exactly the subsets of `Y minus {i}`, hence there are `2^(h-1)` eligible inputs. If `i notin Y`, every subset of `Y` is eligible, giving `2^h` inputs.

For `0<=m<=n-1`, define

\[
Q_m(n)=\prod_{k=0}^{m}
\left(1-\frac1{n-k}\right)^{\binom mk}.
\]

Grouping eligible subsets according to cardinality gives the exact probabilities

\[
\Pr\bigl(i\notin f(\mathcal P(Y))\bigr)
=
\begin{cases}
Q_{h-1}(n),&i\in Y,\\
Q_h(n),&i\notin Y.
\end{cases}
\]

Thus the following is a sufficient finite condition for `H_e(n)<=h`:

\[
\binom nh\bigl[hQ_{h-1}(n)+(n-h)Q_h(n)\bigr]<1.
\tag{E-exact}
\]

Because each eligible input has probability at least `1/n` of receiving `i`, we also have

\[
Q_m(n)\le\exp\left(-\frac{2^m}{n}\right).
\]

This yields the simpler sufficient condition

\[
\binom nh\left[
h\exp\left(-\frac{2^{h-1}}n\right)
+(n-h)\exp\left(-\frac{2^h}n\right)
\right]<1.
\tag{E-split}
\]

Bounding both types of event by the larger probability gives

\[
\Pr(\text{some ideal misses some color})
\le n\binom nh\exp\left(-\frac{2^{h-1}}n\right).
\tag{E}
\]

In particular, the convenient finite condition

\[
2^{h-1}>n\left(\ln n+\ln\binom nh\right)
\tag{E-simple}
\]

suffices. Again, no independence between different missing-color events is assumed.

At the endpoint `h=n`, exterior coverage is automatic: for each color `i`, the forced value at `[n] minus {i}` is `i`. The product formula is therefore only needed for `h<n`; there is no need to define `Q_n(n)`.

## 4. Explicit constants valid for every n >= 32

**Proposition.** For every integer `n>=32`, with `L=log_2 n`,

\[
H_u(n)\le
\left\lceil L+2\log_2 L+1\right\rceil,
\tag{4.1}
\]

and

\[
H_e(n)\le
\left\lceil L+2\log_2 L+2\right\rceil.
\tag{4.2}
\]

**Proof.** Write the two displayed candidate thresholds as `h_u` and `h_e`, respectively. Since `L>=5`, the inequality `2 log_2 L<=L` gives

\[
h_u\le h_e\le L+2\log_2 L+3\le 2L+3<2^L=n.
\]

Here `2 log_2 L<=L` holds for `L>=4`: there is equality at 4 and the derivative of `L-2 log_2 L` is positive thereafter. Likewise, `2^L-2L-3` is positive at 5 and has positive derivative for `L>=5`. Thus both candidate thresholds are legitimate and the exterior estimates for `h<n` apply.

By the definitions of the ceilings,

\[
\frac{2^{h_u}}n\ge 2L^2,
\qquad
\frac{2^{h_e-1}}n\ge 2L^2.
\]

For either candidate `h`, using `binom(n,h)<=n^h` gives

\[
\ln\left(n\binom nh\right)
\le(h+1)\ln n
\le\bigl(L+2\log_2 L+4\bigr)L\ln2.
\]

To estimate the final expression, set

\[
r(L)=\frac{2\log_2 L+4}{L}.
\]

Its derivative is

\[
r'(L)=\frac{2/\ln2-2\log_2 L-4}{L^2}<0
\qquad(L\ge5).
\]

Moreover, `log_2 5<5/2`, so `r(5)<9/5`. Consequently,

\[
\bigl(L+2\log_2 L+4\bigr)L\ln2
<\frac{14}5(\ln2)L^2
<2L^2.
\]

For completeness, `ln2<5/7` proves the last strict inequality; one elementary verification is `exp(5/7)>1+5/7+(5/7)^2/2+(5/7)^3/6=4178/2058>2`.

The strict finite conditions (U-simple) and (E-simple) now hold, proving both assertions. ∎

## 5. The coefficient-2 asymptotic statement

The explicit bounds give, in both models,

\[
H(n)\le\log_2 n+2\log_2\log_2 n+O(1).
\]

More quantitatively, for every `epsilon>0`, the exterior estimate implies

\[
H_e(n)\le
\left\lceil L+(2+\varepsilon)\log_2 L\right\rceil
\]

whenever

\[
L\ge\max\{5,\,2^{2/\varepsilon}\}.
\]

Indeed, this condition implies `epsilon log_2 L>=2`, so the candidate threshold here is at least that of (4.2). For the unrestricted model, the sufficient condition is instead

\[
L\ge\max\{5,\,2^{1/\varepsilon}\}.
\]

Changing the base of the inner logarithm changes only an additive constant. In particular,

\[
2\log_2\log_2 n
=2\log_2\ln n-2\log_2\ln2.
\]

Thus the coefficient 2 agrees with the natural-log normalization in the historical source.

## 6. Why a middle-layer argument can display coefficient 3

The exterior constraint itself costs at most a factor of two in the number of usable inputs, not a power of `log n`. It therefore affects the additive constant in these upper bounds, not the coefficient of `log log n`.

For comparison, restrict the random choices used in the proof to `t`-element inputs, and test a set `Y` of size `h=2t+1<n`. A color inside `Y` has exactly `binom(2t,t)` eligible `t`-subsets. A color outside `Y` has at least as many. Each eligible input assigns that color with probability `1/(n-t)>=1/n`.

The largest binomial coefficient in row `2t` is the central one. Since the row has `2t+1` entries summing to `4^t`,

\[
\binom{2t}t\ge\frac{4^t}{2t+1}.
\]

Consequently,

\[
\Pr(\text{some failure})
\le n\binom n{2t+1}
\exp\left(-\frac{4^t}{n(2t+1)}\right)
\le\exp\left((2t+2)\ln n-
\frac{4^t}{n(2t+1)}\right).
\]

The sufficient condition

\[
4^t>n(2t+1)(2t+2)\ln n
\]

has a right-hand side of order `n (ln n)^3` when `t` is of logarithmic order, explaining a coefficient-3 logarithmic correction in this coarse one-layer proof. Using every subset size removes the layer loss and yields the coefficient-2 bounds above.

This comparison explains the two upper-bound coefficients. It does not supply a lower bound of either logarithmic order, and no matching asymptotic gap is asserted.
