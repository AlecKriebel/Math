# Exact coefficient extension through cardinality eleven

2026-10-24. Both `n=10` and `n=11` witnesses independently reproduced by the original grid method. The formal-group proof in `FORMAL_GROUP_TRANSFER.md` is frozen separately. No statement for all cardinalities or mixed-prime groups is claimed.

Use the reduced polynomial `Q_n=V(x)F_n(x)` defined in `FORMAL_GROUP_TRANSFER.md`, with `V(x)=prod_(i<j)(x_j−x_i)` and `F_n` the product of differences of sums on disjoint cycle edges. Write

`m=n(n−3)/2`, `d=n(n−2)`, `N=n(n−1)/2`, `H=prod_(k=1)^(n−1)k!`.

## Formula and exact integer implementation

For the exponent tuple `t_0=0`, `t_j=n−2`, `t_i=n−1` for `i≠0,j`, Lagrange interpolation on the integer grids `{0,...,t_i}` gives

`[x^t]Q_n = ((−1)^m (n−1)! / H) sum_a sign(a) (n−1−a_j) F_n(a)`.

The sum is over all permutations `a=(0,a_1,...,a_(n−1))` of `{0,...,n−1}` with first value zero. `sign(a)` is the permutation sign.

To verify the formula, the grid coefficient identity has denominators `prod_i a_i! (−1)^(t_i−a_i) (t_i−a_i)!`. The Vandermonde makes every tuple with repeated coordinates vanish, leaving full permutations. Their total sign denominator is `(−1)^(d−N)=(−1)^m`, and their Vandermonde is `sign(a)H`. Relative to the uniform grids `{0,...,n−1}`, whose factorial denominator is `H^2`, changing the first cap to zero and the `j`th cap to `n−2` contributes the factor `(n−1)!(n−1−a_j)`. The latter also vanishes on the excluded value `a_j=n−1`.

For `t_0=1` and additional deficits of two, indexed by `j,k≥1` (possibly equal), the analogous formula sums full permutations with `a_0∈{0,1}`, with weight

`(n−1−a_0)! (n−1−a_j) [n−1−a_k−1_(j=k)]`

and the prefactor `(−1)^m/H`. The weight vanishes on all excluded values of the capped grids.

`fixed_zero_coefficients.py` and `low_exponent_coefficients.py` implement these formulas with exact Python integers and assert every final denominator divides its numerator. No fixed-width arithmetic is used. `verify_extension_consistency.py` independently compared all 151 computed coefficient values at `n=3,...,9` against complete sparse polynomial expansions; all matched, including zero coefficients and every deficit location.

## Small exact witnesses

At `n=10`, the following three coefficient witnesses from the signed-permutation implementation have gcd `2`:

| Exponents | Coefficient |
|---|---:|
| `(1,7,9,9,9,9,9,9,9,9)` | `−299280689184` |
| `(1,8,8,9,9,9,9,9,9,9)` | `−600114405460` |
| `(1,8,9,8,9,9,9,9,9,9)` | `−643745163834` |

The independent actual-polynomial grid verifier checked an even smaller `n=10` certificate: `(0,8,9,9,9,9,9,9,9,9)` has coefficient `−30955393332`, and `(1,9,8,8,9,9,9,9,9,9)` has coefficient `−125404419790`; their gcd is `2`. See `polynomial/n10_combined_verification.txt`.

At `n=11`, two witnesses have gcd `1`:

| Exponents | Coefficient |
|---|---:|
| `(0,9,10,10,10,10,10,10,10,10,10)` | `11098103614834` |
| `(0,10,9,10,10,10,10,10,10,10,10)` | `189427196282499` |

The independent verifier `polynomial/fixed_zero_audit.py` evaluates the actual polynomial `V*F` with binomial-grid weights, rather than the simplified signed-permutation identity. It reproduced both `n=11` integers exactly; see `polynomial/fixed_zero_n11_verification.txt`.

Following the separate coefficient audits, these witnesses and the already verified `n=3,...,9` witnesses give nonzero reduced polynomial modulo every odd prime for `3≤n≤11`. Applying the formal-group transfer gives the required cycles for subsets of those cardinalities in **every finite abelian group of odd prime-power order**. At `n=11`, the same conclusion also holds for abelian `2`-groups, because the two witness coefficients are relatively prime.

These calculations do not establish a content formula for arbitrary `n`. In particular, the fixed-zero vector alone already has odd factors in its coefficient gcd at `n=6,8,10` (respectively `10,504,6`), although other coefficients remove them. No universal nonvanishing follows from the fixed-zero vector.
