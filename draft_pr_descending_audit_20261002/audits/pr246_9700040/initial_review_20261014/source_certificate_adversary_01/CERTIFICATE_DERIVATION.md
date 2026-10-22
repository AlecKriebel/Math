# Independent rational certificate derivation

Written 2026-10-15 before inherited review verdicts. Assume a correct positive raw series with total raw coefficient `a_n=x^n/n!`, `x>0`. Let the constrained coefficient `w_n` satisfy `0<=w_n<=a_n`. Define `W=sum_{n<=N}w_n`, `T=sum_{n<=N}a_n`, `E=sum_{n>N}a_n`, and `F=sum_{n>N}w_n`. Then

`P=(W+F)/(T+E)`, `0<=W<=T`, and `0<=F<=E`.

## Tail and worst-case normalization

For `N+2>x`, the ratios of successive terms after the first omitted term are at most `q=x/(N+2)<1`. Hence

`0<E<=R=a_(N+1)/(1-q)`.

For a fixed `E`, the numerator is least at `F=0` and greatest at `F=E`. Thus

`W/(T+E)<=P<=1-(T-W)/(T+E)`.

The left expression decreases in `E`; the right increases in `E` since `T-W>=0`. Maximizing the admissible `E` gives

`W/(T+R)<=P<=(W+R)/(T+R)`.

The width is exactly `R/(T+R)`, lies strictly between zero and one, and neither endpoint leaves `[0,1]`. This remains valid at `W=0` and `W=T`. It is optimal over the information class `0<=F<=E<=R`: the lower endpoint occurs at `(E,F)=(R,0)` and the upper at `(R,R)`. For the actual exponential series `E` is fixed and generally smaller than `R`, so these information-class extrema need not be attained by a particular query.

Using `(W+R)/T` is a valid but weaker upper bound that can exceed one. Using `W/T` as the lower endpoint is generally false because excluded tail mass changes the denominator. Replacing `R` by the first omitted term is generally false. The submitted expression uses the correct shared denominator.

## Monotonicity, including both endpoints

Write `a=a_(N+1)` and `k=N+2>x`. Then

`R_N=a k/(k-x)`,

`R_(N+1)/R_N = x(k+1)(k-x)/(k^2(k+1-x)) < x/k < 1`.

Also `Sbar_N=T_N+R_N` satisfies

`Sbar_N-Sbar_(N+1) = a x^2/[k(k-x)(k+1-x)] >0`.

Consequently the width strictly decreases: `T_N` increases and `R_N` decreases. The lower endpoint is nondecreasing because `W_N` increases and `Sbar_N` decreases. For the upper endpoint use `1-(T_N-W_N)/Sbar_N`: `T_N-W_N` is nondecreasing because `a_n-w_n>=0`, and `Sbar_N` decreases. Thus the upper endpoint is nonincreasing. This proves nested certificates, stronger than the submitted width-only claim. The reasoning requires the same event and consistent truncated coefficients when `N` varies.

## Effective cutoff and arbitrary rational precision

For rational `x>0` and rational `epsilon>0`, start at any integer `N` satisfying `N+2>x`, compute rational `T_N,R_N`, and increment `N` until `R_N/(T_N+R_N)<=epsilon`. This stops. For example, after `N+2>=2x` the successive tail-term ratio is at most `1/2`, so `R_N<=2a_(N+1)` and the latter tends to zero geometrically; also `T_N>=1`. All comparisons are integer/rational comparisons. At the chosen finite `N`, only finitely many partitions of size at most `N` and finitely many finite determinants occur. Thus no runtime efficiency theorem or inaccessible real-number oracle is required.

To compute a joint CDF involving `q` coordinates by inclusion–exclusion, enclose each needed survival probability to width at most `epsilon/2^q`, sum intervals with their signs reversed where needed, and intersect with `[0,1]`. This yields an enclosure of width at most `epsilon`. The cost may be exponential in query length. For arbitrary real thresholds the formula still defines a law; effective evaluation requires appropriate input access (rational inputs suffice here). A noncomputable unspecified real is not a finite executable query.

## Boundary and presentation distinctions

`N` must be a nonnegative integer. The strict tail condition `N+2>x` cannot be weakened to equality. If a finite query reduces to no positive thresholds, return probability one without using the series. Repeated/nonpositive thresholds can be normalized as described in `INDEPENDENT_RECONSTRUCTION.md`; positive integer indices remain required. The mathematical interval's exact rational endpoints are certified. Ordinary binary64/decimal conversion can round endpoints inward or collapse their displayed difference; such displays are not certified unless rounded outward. The submitted CLI labels them `display_only`, so exact-fraction output is the actual certificate.
