# Turn 1: an exact envelope for Δ_h and an honest thinning-oracle inequality

**Scoped partial, pending independent review. Original selector/regret question remains unresolved at 1/5.** This turn proves a samplewise bound for the actual three-step source estimator, without clipping or replacing its isotonic projection by a different ERM. It then gives a finite-sample comparison for the source's single-thinning validation score. The comparison is for the fitted thinned-data loss, not a rate-sharp full-data-refit theorem.

## 1. The source family is uniformly bounded by the sample maximum

Fix a nonempty observed sample of nonnegative integers. Let its empirical distribution be π_t, with finite support, minimum l and maximum m. The symbol π here denotes the **empirical distribution of observed counts**, not the unknown prior on Poisson means. For h>0 set

k_h(j)=e^(−h)h^j/j! for j≥0, and k_h(j)=0 for j<0,

q_h(z)=sum_t π_t k_h(z−t).

The source's first two steps are

a_h(z)=(z+1)q_h(z+1)/q_h(z)−h when q_h(z)>0, and 0 otherwise,

b_h(y)=sum_(j≥0)k_h(j)a_h(y+j).

Let Δ_h be the empirical-multiplicity-weighted least-squares projection of b_h on the nondecreasing functions of the observed count values, exactly as specified in Brown–Greenshtein–Ritov §2.3. Define Δ_0 separately by isotonic projection of the ordinary Robbins values at observed counts.

**Theorem 1. For every sample and every h≥0,**

0 ≤ Δ_h(y) ≤ m for every observed y.                (1)

The assertion includes the all-zero sample, where every fitted value is zero. There is no lower bound on positive h, and (1) does not infer continuity at h=0.

### 1.1 Positivity, finiteness and the exact shifted convolution identity

For z≥l the denominator q_h(z) is positive. The Poisson recurrence gives

(z+1)q_h(z+1)−h q_h(z)
     = sum_t t π_t k_h(z+1−t).                     (2)

This is valid for the full convolution with the convention k_h(j)=0 for j<0. Therefore a_h(z)≥0 on its positive-denominator domain, and by definition elsewhere. For z≥m,

0≤a_h(z)≤mh/(z+1−m),                              (3)

because k_h(z+1−t)=h k_h(z−t)/(z+1−t). Thus b_h(y) is finite: it has only finitely many initial terms and an absolutely convergent nonnegative Poisson tail bounded using (3). Positivity alone is not enough to prove the upper bound (1); individual unsorted b_h values can be large.

### 1.2 A posterior tail that is monotone in the corrupted count

For a threshold v among the observed values, put

W_v(z)= [sum_(t≥v)π_t k_h(z−t)]/q_h(z) for z≥l,

and W_v(z)=0 for z<l. It is the tail probability for an auxiliary empirical count T~π given Z=T+N=z, N~Poisson(h). This auxiliary construction is an exact identity for a fixed empirical histogram.

The sequence W_v(z) is nondecreasing. Indeed, for s<t the kernel has the total-positivity inequality

k_h(z+1−t)k_h(z−s) ≥ k_h(z−t)k_h(z+1−s).          (4)

When the four factors have nonnegative indices, (4) follows by comparing h/(z+1−t) with h/(z+1−s). The zero-index boundary cases satisfy the same inequality directly. Cross-multiplication of W_v(z+1)−W_v(z) reduces its numerator to a sum of (4) over s<v≤t, with coefficients π_sπ_t≥0. The initial zero branch preserves monotonicity.

### 1.3 Exact suffix identity and bound

Let expectation in this paragraph refer only to T~π and its independent Poisson N. Tonelli and (2) give

sum_(y≥v)π_y b_h(y)
 = sum_z W_v(z)[sum_t tπ_t k_h(z+1−t)]
 = E[T W_v(T+N−1)].                              (5)

The convention W_v(z)=0 below l is important. It handles the case q_h(l−1)=0 while q_h(l)>0; no division by that zero denominator is used. Since 0≤T≤m and W_v is nondecreasing,

sum_(y≥v)π_y b_h(y)
 ≤ m E[W_v(T+N−1)]
 ≤ m E[W_v(T+N)]
 = m sum_(y≥v)π_y.                               (6)

Thus every weighted suffix mean of the unprojected values is at most m.

For reference, the all-support instance of (5) also gives the exact mean identity

sum_y π_y b_h(y)=sum_y yπ_y−lπ_l e^(−h).           (7)

It follows because W_l(z)=1 for z≥l and zero below; the only lost term is T=l,N=0. This identity is for h>0 and must not be extended to the separately defined h=0 by continuity.

### 1.4 Isotonic projection and the h=0 endpoint

For sorted distinct observed values x_1<...<x_J with positive weights w_j, the final value of the nondecreasing weighted least-squares projection is

Δ_h(x_J)=max_(1≤i≤J) [sum_(j=i)^J w_j b_h(x_j)]/[sum_(j=i)^J w_j].       (8)

To check (8) directly, increasing any fitted suffix by a small positive constant is feasible. The one-sided first-order optimality condition therefore gives sum_(j≥i)w_j b_h(x_j)≤sum_(j≥i)w_j Δ_h(x_j)≤Δ_h(x_J)sum_(j≥i)w_j. Conversely, on the maximal final constant block, variation in both directions is feasible for a sufficiently small amount, so that block level equals its weighted input mean. These two facts prove (8). Every maximal constant block similarly has its input mean, and the fitted values are consequently nonnegative. Equation (6) bounds every candidate in (8) by m. Monotonicity then proves (1).

For h=0, the raw observed-count value is a_0(y)=(y+1)π_(y+1)/π_y. For every observed threshold v,

sum_(y≥v, π_y>0)π_y a_0(y)
 = sum_(t≥v+1, π_(t−1)>0)tπ_t
 ≤ m sum_(t≥v)π_t.

The same projection argument gives (1) at the endpoint directly. This proof neither ignores missing bins nor identifies h→0+ with h=0.

The weighted isotonic projection preserves the weighted mean, so (7) also holds for Δ_h when h>0. The envelope (1), not a claim of equality with ERM, is what will be used below.

## 2. The actual single-thinning validation experiment

Fix n≥1, a deterministic mean vector 0≤λ_i≤M, and α∈(0,1). Set η=1−α. Split the original independent Poisson observations by U_i|Y_i~Binomial(Y_i,α), V_i=Y_i−U_i. Conditional on λ, U and V are independent, with means αλ and ηλ.

Let H be a finite nonempty candidate set of h≥0, of cardinality K. It may be chosen measurably from U, but not from V. Fix a deterministic tie rule. Fit the entire source procedure on U and write

g_(h,i)=Δ_h^U(U_i),  B=max_i U_i.

Theorem 1 gives 0≤g_(h,i)≤B simultaneously for all h. Define the realized thinned-mean loss and validation score

L_h=n^(-1)sum_i(g_(h,i)−αλ_i)²,

ρ_h=n^(-1)sum_i(g_(h,i)−αV_i/η)².

Let h_hat minimize ρ_h over H and let h_* minimize L_h over H. The second choice is a theoretical oracle, not a data-driven rule.

**Theorem 2.** For any ε∈(0,1) and δ∈(0,1), conditional on U and λ, with probability at least 1−δ over V,

L_(h_hat) ≤ [(1+ε)/(1−ε)] L_(h_*)
 + [4α²M/ε + 2αB/3] log(2K/δ) / [(1−ε)η n].       (9)

If all λ_i=0, every fitted value and loss is zero, and the assertion is immediate. Otherwise no lower bound on individual λ_i is needed. The displayed bound is nonasymptotic and holds for the unmodified source family: there is no clipping at M and no substitution of a different monotone estimator.

### 2.1 Score differences retain the correct centering

Let E_i=V_i−ηλ_i. For any h,k, the h-independent squared-noise term cancels exactly, giving

ρ_h−ρ_k=L_h−L_k−Z_(h,k),

Z_(h,k)=[2α/(η n)]sum_i(g_(h,i)−g_(k,i))E_i.       (10)

In particular, score minimization gives L_(h_hat)−L_(h_*)≤Z_(h_hat,h_*). This avoids interpreting the raw validation score as an unbiased estimate of loss without its h-independent offset.

### 2.2 Conditional Poisson concentration

Given U, the coefficients in Z_(h,h_*) are deterministic. A centered Poisson variable of mean μ has log moment generating function μ(e^t−1−t). The elementary bound

e^t−1−t≤t²/[2(1−|t|/3)], |t|<3,

follows by the Taylor series and k!≥2·3^(k−2) for k≥2. Thus a sum of independent centered Poisson variables with real coefficients a_i has the Bernstein bound

P(|sum_i a_i(V_i−ηλ_i)| > sqrt(2vx)+cx) ≤ 2e^(−x),

where v=sum_i ηλ_i a_i² and c=max_i|a_i|/3. This is obtained directly by the exponential Markov inequality with the preceding moment bound; it is valid for either sign of the coefficients.

Here |a_i|≤2αB/(η n) and

v≤[4α²M/(η n²)]sum_i(g_(h,i)−g_(h_*,i))²
 ≤[8α²M/(η n)](L_h+L_(h_*)).                     (11)

The last step uses |x−y|²≤2|x−t|²+2|y−t|² with t=αλ_i. Union bounding over h∈H with x=log(2K/δ) gives simultaneously

|Z_(h,h_*)|≤sqrt([16α²Mx/(η n)](L_h+L_(h_*))) + 2αBx/(3η n).           (12)

There is no union bound over an uncountable tuning continuum and no independence assumption among the fitted candidate vectors.

### 2.3 Finish the oracle comparison

Apply sqrt(ab)≤εb+a/(4ε) to the first term of (12), insert h=h_hat in (10), and rearrange:

(1−ε)L_(h_hat)≤(1+ε)L_(h_*)+4α²Mx/(εη n)+2αBx/(3η n).

This is (9). The proof is conditional on U, so the random envelope B and a U-measurable finite grid cause no difficulty.

## 3. What this proves, and the original remaining gap

Equation (9) rigorously controls the source's single-split selection step for the **realized loss of the U-trained estimates of αλ**. Dividing both sides by α² gives the corresponding bound for the rescaled estimates g_h/α of λ, still trained on U. This is a precise version of an oracle comparison, not an assertion about refitting the chosen h on Y.

There are two reasons it does not answer the original rate question:

1. It is multiplicative in the full training loss. If the Bayes risk is bounded away from zero, the ε multiplier has a cost of order ε, not automatically the much smaller bounded-prior regret r_n=(log n/log log n)²/n. Optimizing a generic loss bound is not the same as proving a sharp excess-over-Bayes bound.
2. The original proposal chooses h using U,V and may then refit on Y, or conditionally average its criterion over repeated splits. Neither transfer is covered by the conditional single-split calculation. Taking α→1 without a quantitative stability argument is insufficient; shrinking η simultaneously enlarges the validation term in (9).

The exact family envelope and suffix identity are useful inputs for those sharper questions. They do not supply the required uniform approximation of the positive-h family to its Bayesian oracle, and the published h→0 discontinuity remains relevant. The separately defined h=0 monotone-Robbins guarantee is credited prior theory and does not by itself validate an adaptive positive-h selector.

This completes substantive turn 1. Original status remains unresolved, with four author turns available. All nontrivial deductions await independent review before any result PR; no novelty is asserted.

## Certificate scope

The certificate checks finite convolution identities, total-positivity minors, shifted suffix identities, exact isotonic block/suffix formulas, Poisson thinning coefficients and score-difference algebra. Infinite Poisson summation, closed-form projection facts and concentration are justified in the written proof. Finite controls are not numerical evidence of regret optimality or an exhaustive search for a selector.
