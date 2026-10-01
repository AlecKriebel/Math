# Turn 4: the positive-sum root is well conditioned, but rational separation remains

**Active partial, author turn 4/5, 2026-10-01.** This turn addresses the original positive unit-coefficient base 2/3 directly. It does not supply the requested polynomial-time comparison algorithm.

After the elementary cases from Turn 1, assume n≥2 and all r_i≥1. Define

    f(x)=sum_i x^(r_i)−1,   rho=2/3.

Repeated exponents are allowed. The parameter n counts terms with multiplicity.

## 1. A unique simple positive root

f(0)=−1, f(1)=n−1>0, and f is strictly increasing on (0,infinity). Therefore it has exactly one positive root ξ∈(0,1), and

    sum_i (2/3)^(r_i)>1  if and only if  ξ<2/3.

At that root,

    f'(ξ)=sum_i r_i ξ^(r_i−1) ≥ 1/ξ > 1.

The positive root cannot become a multiple root. The degree may still be exponentially large in the binary input size.

If |f(rho)|≤1/16, then ξ lies in (1/2,3/4). Indeed,

    sum_i (1/2)^(r_i) ≤ (3/4) sum_i rho^(r_i) ≤ 51/64<1,
    sum_i (3/4)^(r_i) ≥ (9/8) sum_i rho^(r_i) ≥135/128>1.

Along the interval between ξ and rho, the sum is at least 15/16 and x≤3/4, so f'(x)≥5/4. Also

    r (3/4)^(r−1) ≤27/16  for every integer r≥1.

The latter follows by taking ratios of successive terms: the maximum occurs at r=3 and r=4. Thus f'(x)≤27n/16 on the interval, and the mean value theorem gives

    (5/4)|ξ−rho| ≤ |f(rho)| ≤ (27n/16)|ξ−rho|.           (1)

Hence the sign margin and the distance of the unique root from the fixed rational comparison point differ by at most a polynomial factor in n. This reduction does not by itself bound either quantity from below.

## 2. Degree-independent local complex isolation

For any |z|≤R<1 and integer k≥1,

    |f^(k)(z)| ≤ n k!/(1−R)^(k+1).

To prove this, bound each monomial derivative by k! times one term of the positive series

    sum_(r≥k) binom(r,k) R^(r−k) = (1−R)^(−k−1).

In particular |f''(z)|≤1024n on |z|≤7/8. When ξ∈(1/2,3/4), take the circle |z−ξ|=1/(1024n), which lies in that larger disk. Taylor's theorem bounds its nonlinear remainder by

    512n |z−ξ|² = |z−ξ|/2,

while its linear term has magnitude at least (4/3)|z−ξ|. Rouché's theorem therefore shows that this small disk contains exactly one root of f, counted with multiplicity, namely ξ. There is no second complex root within this explicit inverse-polynomial radius.

Thus these hard-looking positive comparison instances do not require a nearly multiple or locally crowded positive root. Sparse-root algorithms with a precision parameter still need to determine on which side of rho that isolated root lies. Replacing that sign-separation task by local conditioning or root counting leaves the central issue unresolved.

## 3. A precise warning about conditioning versus comparison precision

For N≥3, the related polynomial

    g_N(x)=2x+x^N−1

has a unique well-conditioned positive root ξ_N just below 1/2. At x=1/2 its value is 2^(−N), and on the interval from ξ_N to 1/2 its derivative lies between 2 and 11/4. Hence

    (4/11)2^(−N) ≤ 1/2−ξ_N ≤ (1/2)2^(−N).

Its input length is O(log N), so ordinary approximation may need exponentially many bits to resolve this particular rational comparison despite excellent conditioning. This is not an instance of the noninteger-base 2/3 question: it is the easy reciprocal-integer case, and the exact prefix 2x−1 settles the sign immediately.

At the base 2/3, the general signed-coefficient task has the equally explicit example 3x+x^N−2. It has exponentially small positive value at 2/3, again explained by an exactly zero lower-degree block. Turn 3 removes that block symbolically. These examples only refute the inference “well-conditioned root implies low comparison precision”; they are not lower bounds for exact sign computation, and are not claimed to defeat the parity-protected original unit-coefficient case.

## 4. A positive gap for fixed term count, and its current quantitative limit

For fixed n define

    delta_n = inf |sum_(i=1)^k rho^(r_i)−1|,
              0≤k≤n, r_i positive integers.

Then delta_n>0. One proof compactifies the exponent set by adding infinity and setting rho^infinity=0. A convergent subsequence of each of the finitely many exponent coordinates either stabilizes at a finite exponent or tends to infinity. A zero limit would therefore express one as a sum of at most n positive powers of 2/3. This is impossible: after clearing the largest power of three, the sum's numerator is even while the threshold numerator is odd. Compactness gives a positive minimum.

The Turn 1 algorithm gives an explicit, much weaker-than-polynomial quantitative bound. For n≥2, set k=ceil(log_2 n) and

    M_n=(3k/2)(3^n−1).

Use n as an upper bound on the number of terms in the pruning rule, so the estimate covers every k≤n in the definition of delta_n. Every processed exponent is below M_n. At a pruning step, the remaining tail is at most

    (16/27) 3^(−R),

using n≤2^k, k≥1 and the same cutoff as Turn 1. A below-one prefix has deficit at least 3^(−R), so the final gap is at least (11/27)3^(−R). If a processed prefix is above one, or all terms are processed, parity gives a gap of at least 3^(−R). Consequently

    delta_n ≥ (11/27) 3^(−M_n).                         (2)

This bound is doubly exponential in n when expressed as a reciprocal gap, and only recovers a fixed-parameter algorithm. It is not evidence that the true delta_n has that size.

A bound delta_n≥2^(−poly(n)) would be sufficient to make certified truncation polynomial-time for the original positive problem. Neither compactness, parity, derivative bounds nor the local root-isolation estimate proves such a bound. Conversely, failure of that particular lower bound would not by itself rule out a symbolic polynomial-time algorithm.

## 5. Outcome and final route

The new proved reduction is that the nontrivial positive task is an exact comparison with a unique, simple, locally polynomially isolated root. The obstruction in the present analytic route is rational-point separation, rather than root count or local conditioning. Existing precision-dependent sparse-root theorems cannot be invoked with their precision/separation dependence silently dropped.

The final substantive turn will examine the rational-base carry/normal-form structure of the positive sums and test whether it supplies an order certificate avoiding that separation parameter. No universal polynomial bound, hardness theorem or final unsolved disposition is claimed in this fourth turn.
