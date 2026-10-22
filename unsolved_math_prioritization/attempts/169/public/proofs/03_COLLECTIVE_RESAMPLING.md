# Stage 3: collective nonmonotone resampling and its limits

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 3. Exact target remains uniform A of size k=floor(sqrt(p)) in F_p, with cap c=floor(100 sqrt(p)).

## Results

- An exact identity describes every equal-budget collective exchange, including exchanges that temporarily lose previously covered points.
- Every global optimum satisfies the resulting all-exchange-size inequalities. A positive-hole fractional histogram satisfies all of them with equality exactly, so these linear histogram conditions alone do not force a cover.
- For a fixed low-energy A, complete uniform resampling of the centre set has variance O(p), considerably sharper than a direct swap-bound estimate. The cancellation is exact at first order and does not assume independent coverage indicators.
- A small exact example disproves the universal claim that a noncover can always be strictly improved by one equal-budget swap whenever a cover at that budget exists. Plateau paths remain possible.

No genuinely collective affirmative construction closing the fixed-100 budget was obtained.

## 1. Exact identity for arbitrary-size exchanges

Fix A,T subset F_p, with |A|=k and |T|=m. For each x put

`d_x=|(x-A) intersection T|`, and `N_d=#{x:d_x=d}`.

Thus N_0 is the current number of holes, `sum_d N_d=p`, and `sum_d d N_d=km`.

For an integer `0<=q<=min(m,p-m)`, choose a uniform q-subset D of T to delete and, independently, a uniform q-subset B of F_p\T to add. Set `T'=(T\D) union B`. The new centre set still has size m. No coverage-preservation condition is imposed.

For x with d_x=d, it is uncovered after the exchange exactly when all d old centres covering it are deleted and none of its k-d outside neighbours is added. Therefore

`E[holes(T') | A,T] = sum_{d=0}^q N_d a_d(q) b_d(q)`,

where

`a_d(q)=(q)_d/(m)_d`,

`b_d(q)=binom(p-m-k+d,q)/binom(p-m,q)`.

A falling factorial is `(z)_d=z(z-1)...(z-d+1)`, with `(z)_0=1`. Impossible binomial selections have value zero. The identity also follows directly by counting the deletion/addition pairs.

### Necessary condition at a global optimum

If T minimizes the number of holes among all m-centre sets, every outcome T' has at least N_0 holes. Hence for every allowed q,

`N_0 <= sum_{d=0}^q N_d a_d(q)b_d(q)`,

or equivalently,

`N_0[1-b_0(q)] <= sum_{d=1}^q N_d a_d(q)b_d(q)`.

The d=0 term must not be omitted from the first formula.

For q=1, assuming `p-m-k+1>0` as holds eventually in the target regime,

`N_1 >= [mk/(p-m-k+1)] N_0`.

For m~Ck this says asymptotically that the number of singly covered points must be at least C times the number of holes. It is a necessary condition, not a sufficient characterization of local or global optimality.

If N_0=0, every displayed inequality is automatically satisfied. Thus these inequalities alone cannot rule out a zero-hole optimum.

## 2. Exact positive-hole fractional stationary profile

There is also a positive-hole profile satisfying every exchange equality, not just the one-centre relation.

Let T be uniform among all m-subsets, with A fixed. Its expected multiplicity histogram is

`n_d = p * binom(k,d)binom(p-k,m-d)/binom(p,m)`.

This follows because each x has exactly k potential covering centres. The histogram satisfies

`sum_d n_d=p`, `sum_d d n_d=km`, and

`n_0=p binom(p-k,m)/binom(p,m)>0` when `m+k<=p`.

The q-exchange Markov kernel on m-subsets is symmetric: for any two states differing by exactly q deletions and q additions, the transition probability is the same constant

`1/[binom(m,q)binom(p-m,q)]`.

Consequently the uniform distribution on m-subsets is stationary. Averaging Section 1 over uniform T and using the linearity of its formula gives, exactly for every q,

`n_0=sum_{d=0}^q n_d a_d(q)b_d(q)`.

This is a feasible fractional histogram for all the linear optimum inequalities and the elementary total-count constraints. It is not a claim that a particular T, much less an optimum, has this exact generally nonintegral histogram.

The obstruction is precise: a proof that uses only these linear histogram inequalities cannot eliminate all positive-hole profiles. Additional joint information about A, T, correlations of potential gains, or cover-specific structure is necessary.

### Poisson limit, with its proper scope

If m/k->C and k^2/p->1, the normalized stationary histogram tends to Poisson(C). More generally, suppose a sequence of actual histograms satisfies `N_d/p -> exp(-C)C^d/d!` for every fixed d and `sum dN_d/p -> C`. If q/m->theta in [0,1], then Section 1 gives

`E[holes(T')]/p -> exp(-C theta) sum_d exp(-C)C^d theta^d/d! = exp(-C)`.

The bounded first moment controls the histogram tail, so the termwise limit is justified. Thus the leading-order expected number of holes has no contraction at a Poisson profile. This does not establish exact finite-p stationarity for an actual T, forbid lower-order improvements, or exclude improvements accumulated over many adaptive rounds.

## 3. Exact variance for full uniform resampling

Fix A and sample T uniformly among all m-subsets, where `m<=C sqrt(p)` for fixed C. Define

`Q_s=binom(p-s,m)/binom(p,m)`, `a=Q_k`,

`r_A(d)=|A intersection (A+d)|`, and `E(A)=sum_d r_A(d)^2`.

Let U be the number of holes. Translation invariance gives

`E U=p a`.

For x!=y, their forbidden centre sets have union size `2k-r_A(y-x)`. Consequently the exact variance is

`Var U = p a(1-a) + p sum_{d!=0}[Q_(2k-r_A(d))-a^2]`.

No coverage-indicator independence is asserted.

### Cancellation and energy bound

Uniformly for integers 0<=s<=2k, expansion of the exact product for Q_s yields

`log Q_s = -ms/p - [m(m-1)s+ms^2]/(2p^2) + O_C(k^(-2))`.

Indeed `log Q_s=sum_{j=0}^{m-1}log(1-s/(p-j))`; the cubic logarithm remainder and the next terms in the two reciprocal sums are all O_C(k^(-2)), since p~k^2.

Subtracting twice the s=k expansion from the s=2k-r expansion, and exponentiating, gives uniformly for 0<=r<=k,

`Q_(2k-r)-a^2 = a^2 { (m/p)(r-k^2/p) + O_C((r^2+1)/k^2) }`.

The estimate remains valid when r is large: the logarithmic ratio is bounded by a constant depending only on C, and its quadratic exponential remainder is bounded by a constant times `(r^2+1)/k^2`.

Now the identity

`sum_{d!=0}(r_A(d)-k^2/p) = -k+k^2/p <= 0`

cancels the apparent order-p^(3/2) contribution. Substituting in the exact variance formula gives

`Var U <= O_C(p + E(A))`.

In particular, whenever `E(A)<=Kk^2` for a fixed K,

`Var U = O_(C,K)(p)`.

This requires no maximum-codegree condition. Under the typical exact-model energy bounds established earlier, it applies with high probability to the sampled A. It also applies to some exceptional coverable A, so it is not itself a noncoverage criterion.

The mean has the uniform form

`E U = p exp(-mk/p)+O_C(k)`.

For m=floor(Ck), or for the operational m=c with C=100, this is `p exp(-C)+O_C(k)` after accounting for floor errors.

### Complete resampling outside the current centre set

The same order of mean and variance holds if an arbitrary current m-set T_0 is excluded and the restart is uniform among m-subsets of F_p\T_0, provided 2m<=p.

To see this, start with a uniform m-subset B of the whole group. Let L=|B intersection T_0| and replace its L forbidden centres by a uniform L-subset outside T_0 union B. The output B' is uniform among m-subsets outside T_0 by permutation symmetry. Also

`E L=m^2/p=O_C(1)`, `E L^2=O_C(1)`.

The two hole counts differ by at most kL. Their means therefore differ by O_C(k), and

`Var U(B') <= 2 Var U(B) + 2 k^2 E L^2 = O_C(p+E(A))`.

This allows the current T_0 to be any function of A: the assertion conditions on the full fixed A,T_0 before performing the fresh restart. It does not treat partial q-exchanges as independent full restarts.

### What the variance does not supply

The standard deviation is O(sqrt(p))=O(k), whereas the expected holes are asymptotic to exp(-C)p. Chebyshev consequently makes a full cover rare under a single uniform restart. It supplies no exponentially strong lower-tail bound over all potential centre sets.

There are `exp(Theta(k log p))` candidate m-sets. An exceptionally small fraction can contain a genuine cover without materially changing either the first or second moment. Neither a sub-Gaussian tail nor a conclusion about the minimum is inferred from the variance bound. The unproved expectation gap for the unrestricted optimal residual remains open.

## 4. Exact one-swap plateau counterexample

Take p=11, A={0,1,2}, m=4 and T={0,1,4,8}. Then A+T misses exactly 7.

The private points of the four old translates are, respectively,

`{0}`, `{3}`, `{4,5,6}`, `{8,9,10}`.

An added centre can cover the hole 7 only if it is 5, 6, or 7. None of those three translates contains the entire private set of any old translate. Thus every one-centre deletion/addition leaves at least one hole: no one-swap move strictly improves the current coverage.

Nevertheless, a four-centre cover exists. There is even a plateau escape followed by a strict improvement:

`{0,1,4,8} -> {0,2,4,8} -> {0,2,5,8}`.

The first move preserves ten covered points; the second covers all eleven. This refutes an always-strict-one-swap repair lemma, not a method allowing plateau or temporary-loss moves. Fixed-cardinality subset space is connected under swaps, so an unlimited nonmonotone path to any existing cover always exists; proving that the cover exists is the substantive missing part.

## 5. Sharpened unrestricted expectation bridge

Let `R_c(A)=min_{|T|<=c}|F_p\(A+T)|` and `mu_p=E R_c(A)`. The unrestricted optimum concentration proved in Stage 2 gives

`Pr(R_c=0) <= exp(-mu_p^2/(8kc^2))`.

Consequently the exact negative acceptance condition needs much less than a positive-density mean: if there is a fixed a>0 and arbitrarily large primes with

`mu_p >= a c sqrt(k)`,

then on those primes the covering probability is at most `exp(-a^2/8)<1`. This supplies a fixed positive failure probability along an infinite prime sequence, exactly the required negation of convergence to one. The scale `c sqrt(k)` is asymptotic to `100 p^(3/4)`.

If `mu_p/(c sqrt(k)) -> infinity`, the same inequality yields noncoverage with high probability. If the affirmative probability limit holds, necessarily `mu_p=o(c sqrt(k))`. These are implications, not proved lower or upper estimates for mu_p; small expected residual alone still does not imply exact coverage.

## 6. Disposition and the unrestricted gap

The exact all-q exchange identities are genuinely collective and fully adaptive necessary conditions. Their stationary fractional profile prevents a proof based only on leading expected gain or the listed linear histogram constraints. The energy-based variance theorem makes full random restarts sharply concentrated on the k scale but does not locate the extreme lower tail among all possible T.

A complete affirmative argument still needs a demonstrated mechanism selecting those extreme configurations, with a proof of reaching zero holes and exact budget control. A complete negative argument still needs a lower bound on the unrestricted optimum's expectation, or comparable control of all potential witnesses. No such mechanism or bound was established in this shared pass.

