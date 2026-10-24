# Separate audit of the new fixed-zero / low-exponent formulas

Scope added by parent after the analytic audit. This report checks the formulas in `../../../algebraic/fixed_zero_coefficients.py` and `low_exponent_coefficients.py`. It does not independently rerun the reported n=10 or n=11 vectors. Their numerical validation remains assigned to the parent.

## Verdict

Both compression formulas are correct for `n≥3`. Their signs, denominator factors, cap constraints, `a_0=0/1` restriction, and signed-permutation parity agree exactly with the general grid coefficient identity. No formula counterexample was found. All 48 coefficients in the two families for `3≤n≤6` additionally agree with an independent full-grid implementation using exact rational arithmetic.

Reviewed file hashes (SHA-256):

- `fixed_zero_coefficients.py`: `140b4f92085c9cdddbc51fd4cd69c070dd502015c94d8d8390cd77bb30e403ea`
- `low_exponent_coefficients.py`: `49392bc748ff8c0f81dce9f42898825a59b11f2dcdd5ff0d3f2d5cffd8b64410`

## General identity and exact reduction

Let `t=(t_0,...,t_(n−1))` with each `0≤t_i≤n−1` and `Σt_i=d=n(n−2)`. Put

- `M=n(n−3)/2`, the number of disjoint edge pairs;
- `H=∏_(r=1)^(n−1) r!`;
- `R(a)=∏_(i<j, edges i and j disjoint) [(a_j+a_(j+1))−(a_i+a_(i+1))]`, with cyclic indices;
- `δ_i=n−1−t_i`.

The multivariate coefficient identity on grids `{0,...,t_i}` is

`[x^t]Q_n = Σ_(0≤a_i≤t_i) Q_n(a) / ∏_i [(-1)^(t_i−a_i) a_i! (t_i−a_i)!]`.

It follows by taking the product of the univariate Lagrange leading-coefficient functionals. Because `deg Q_n=Σt_i`, any monomial other than `x^t` has some exponent smaller than `t_i` and is killed by at least one functional.

The Vandermonde in `Q_n(a)` forces all `a_i` distinct. Since each lies in `{0,...,n−1}`, the surviving tuple is a permutation of this entire set. For such a permutation,

`V(a)=sgn(a) H`, `∏a_i!=H`,

and

`Σ_i(t_i−a_i)=d−n(n−1)/2=M`.

Therefore the surviving summand is

`(-1)^M sgn(a) R(a) / ∏_i(t_i−a_i)!`.

Equivalently, extending to all permutations and using the falling factorial `(r)_δ=r(r−1)...(r−δ+1)`,

`[x^t]Q_n = ((-1)^M/H) Σ_(a permutation) sgn(a) R(a) ∏_i (n−1−a_i)_(δ_i)`.

The falling-factorial weight is automatically zero when `a_i>t_i`. This remains valid in the repeated-deficit case: if `r=0` and `δ=2`, the product `r(r−1)` is zero, rather than an invalid factorial ratio. Thus the scripts correctly include zero-weight out-of-cap permutations without evaluating factorials at negative arguments.

## Fixed-zero code

Here `t_0=0`, `t_j=n−2` for one `j>0`, and all remaining caps equal `n−1`. Their total is `d`. The deficits are `δ_0=n−1`, `δ_j=1`, with all others zero.

The weight at coordinate zero forces `a_0=0` and contributes `(n−1)!`. The only other factor is `n−1−a_j`. Thus the code's numerator

`(-1)^M (n−1)! Σ_(tail permutations of 1,...,n−1) sgn(tail) R(0,tail)(n−1−a_j)`

and denominator `H` are exact. Since `a_0=0`, the full permutation has the tail's inversion parity. The script's pair test `j−i not in (1,n−1)` is exactly disjointness of cyclic edges.

## Low-exponent code

Here `t_0=1`. The remaining total deficit is two, placed either on distinct coordinates `j<k` or twice on one coordinate `j=k`. Again the caps sum to `d` and are nonnegative for `n≥3`.

The deficit at coordinate zero is `δ_0=n−2`, so `a_0` can only be `0` or `1`. Its falling-factorial contribution is

- `(n−1)!` when `a_0=0`;
- `(n−2)!` when `a_0=1`.

This is exactly `factorials[n−1−a0]` in the code. The other factor is

`(n−1−a_j)(n−1−a_k−1_(j=k))`,

which is the code's `weight`. For the full permutation, the number of inversions involving the initial entry is exactly `a_0`, because the tail contains every other integer from `0` through `n−1`. Hence `inv=a0+inv(tail)` is correct, including the minus sign for the `a_0=1` branch. The overall sign `(-1)^M` and denominator `H` are unchanged.

The equality `num % H == 0` is mathematically required because the expression equals an integral coefficient; the assertion is a useful execution check. Python integers avoid overflow. This divisibility assertion alone would not verify a formula, but the independent derivation above does.

## Independent small tests

`check_small_formulas.py` uses the full grid expression, evaluates the original polynomial through explicit vertex-set disjointness, and divides by each signed factorial denominator using `Fraction`. It does not use the compressed denominator cancellation, falling-factorial weights, or permutation-sign reduction. It imports the two reviewed functions only to obtain their claimed values.

For `n=3,4,5,6`, it checks every fixed-zero target and every low-exponent target: 48 coefficients in total. All agree, including positive, negative, zero, repeated-deficit, and distinct-deficit cases. A nonzero distinct-deficit check is `n=4, t=(1,2,2,3)`, where both methods give `−4`. Results are recorded in `small_formula_results.json`.

Reproduce from this directory with:

`python3 check_small_formulas.py > small_formula_results.json`

## Exact remaining scope

The compression derivations apply to arbitrary `n≥3`. They justify using these algorithms to compute their restricted coefficient families. They do not establish the numerical n=10 or n=11 outputs without checking the corresponding execution results, and they do not establish nonzero content for all n. If a complete audited vector has gcd `1`, it certifies a coefficient not divisible by every prime; gcd `2` certifies that assertion for every odd prime. The parent is checking the newly reported large-n witnesses separately.
