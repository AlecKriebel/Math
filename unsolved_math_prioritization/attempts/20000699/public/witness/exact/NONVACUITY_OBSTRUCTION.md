# Why the unchanged cumulative profile forces psi <= phi

This is an unconditional inconsistency test on the **hypothesis**, not a disproof of a prime-pair conjecture. It uses only exact reweighting and complex-uniform Cauchy differentiation. The original source-preparation gate allowed `psi>phi`; the corrected contract explicitly removes that range.

Assume the original arithmetic hypothesis on the radius `rho=c/log N` polydisc centered at zero, which is among the required centers because `a=0` is allowed. Its error is `O(x^phi)`, uniformly for `h<=x^psi` and `x<=N`, and is holomorphic near the polydisc. Let `b=rho/2>0`. Both collisions `Delta_0` and `Delta_b` belong to this polydisc, with Cauchy circles of radii `rho` and `rho/2`, respectively.

By the independently proved coefficient and profile derivative identities, uniformly on the stated arithmetic range,

`F_h(x):=sum_(n<=x) Lambda(n)Lambda(n+h) = S(h)x + O(x^phi rho^(−2))`,

and

`G_h(x):=sum_(n<=x) Lambda(n)Lambda(n+h)n^(−b)(n+h)^(−b)`

`= S(h)x^(1−2b)/(1−2b) + O(x^phi rho^(−2))`.

The second error may have an extra constant 4 from its smaller Cauchy circles. This changes no exponent. These statements hold even if the originally prescribed center range has `a0=0`: the second collision lies inside the complex polydisc about zero, so no new center is being assumed.

Put `M=N/2` and choose the positive even integer

`h=2 floor(min(M^psi,M)/2)`.

For sufficiently large `N`, it is comparable to `N^min(psi,1)`. For every real `x` in `[M,N]`, we have `h<=x^psi`, and also `h/x<=1`. Thus both displayed estimates hold throughout this whole interval. This interval restriction is important: using the unweighted estimate at arbitrarily small `x` for a fixed large `h` would be unjustified.

Let `g(x)=x^(−b)(x+h)^(−b)`. It is nonnegative, decreasing, and at most 1 on `[M,N]`. Exact Stieltjes partial summation of `F_h(x)=S(h)x+E_h(x)` gives

`G_h(N)−G_h(M) = S(h) integral_M^N g(x) dx + O(N^phi rho^(−2))`.

Indeed the two endpoint errors and the error integrated against `g'` are at most three times `sup_[M,N]|E_h|`, since the total variation of `g` is at most 1. The interval convention is `(M,N]`, so any integer atom at `M` is treated consistently.

On the other hand, subtracting the two asserted weighted cumulative main terms gives

`G_h(N)−G_h(M) = S(h) integral_M^N x^(−2b) dx + O(N^phi rho^(−2))`.

Consequently the hypothesis forces

`S(h) integral_M^N x^(−2b)[1−(1+h/x)^(−b)] dx = O(N^phi (log N)^2)`.

The left side has a uniform positive lower bound of order `h/log N`. For `x in [M,N]`, `x^(−2b)>=N^(−2b)=exp(−c)`. Because `0<=h/x<=1` and `b log2<=1` for large `N`,

`log(1+h/x)>=h/(2x)` and `1−exp(−b log(1+h/x))>=b h/(4x)`.

Hence the integral is at least `exp(−c)b h/8`. The even-gap singular series satisfies `S(h)>=2 C2>0`, so the asserted upper bound would imply

`h/log N << N^phi (log N)^2`.

If `psi>phi`, then `min(psi,1)>phi` because `phi<1`. Our choice `h asymp N^min(psi,1)` contradicts this last inequality as `N` tends to infinity.

Therefore the unchanged complex-uniform cumulative profile cannot satisfy the original hypothesis whenever `psi>phi`. This includes `psi>=1`, all `c>0`, and `a0=0`; no PNT, RH, GRH, or assumed prime-pair asymptotic was used outside the hypothesis being tested.

The necessary restriction `0<psi<=phi<1` removes this specific contradiction and preserves a nonempty admissible length interval. It does **not** establish the truth or full consistency of the remaining arithmetic conjecture. A different repair could change the density or the arithmetic range, but would have to be specified and audited explicitly. The adopted repair leaves the profile and prime benchmark unchanged and narrows only this exponent range.
