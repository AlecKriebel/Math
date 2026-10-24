# Independent audit of the reduced cycle polynomial

Opened 2026-10-24 19:40 UTC. Completion of the assigned implication and
small-coefficient audit: **100% through n=9**. This is not a completion
estimate for the full research problem.

For `n>2`, put `s_i=x_i+x_(i+1 mod n)` and

`Q_n=V(x) product_(0<=i<j<n, j-i not in {1,n-1})(s_j-s_i)`.

There are `n(n-3)/2` retained color factors, so `deg Q_n=n(n-2)`.
This definition correctly omits exactly the adjacent edge pairs, including
the wraparound pair. If `V(x)!=0`, consecutive edge sums cannot be equal,
since `s_(i+1)-s_i=x_(i+2)-x_i`, with all indices cyclic. Thus `Q_n!=0`
on `A^n` certifies the required cyclic ordering.

Let a coefficient `[x^t]Q_n` be nonzero in the field, with every
`0<=t_i<=n-1` and `sum(t_i)=deg Q_n`. Choose any `A_i subset A` with
`|A_i|=t_i+1`. The rectangular grid coefficient identity gives

`[x^t]Q_n=sum_(a in product A_i) Q_n(a)/product_i product_(b in A_i\{a_i})(a_i-b)`.

All denominators are nonzero. The total-degree condition makes this exact:
every other exponent vector has some coordinate below its corresponding
`t_i`, so its tensor interpolation functional vanishes. A nonzero
coefficient forces a nonzero evaluation in `product A_i subset A^n`.
Its coordinates are distinct by the first Vandermonde and therefore
enumerate all of `A`. There is no assumption `p>=n`.

## Independent exact coefficient checks

The self-contained `slack_coefficient_audit.py` uses weighted finite
differences, not factor multiplication. For its integer grids
`{0,...,t_i}`, all nonzero evaluations lie at permutations of
`{0,...,n-1}`. It computes

`[x^t]Q_n = sum_sigma Q_n(sigma) product_i (-1)^(t_i-sigma_i) binom(t_i,sigma_i) / product_i t_i!`,

where only permutations with `sigma_i<=t_i` are included. Division is
performed over the integers, never in a finite field. The script asserts
exact divisibility and the following witness coefficients:

| n | Independently verified coefficient values | Gcd of these values |
| --- | --- | ---: |
| 3 | 1 | 1 |
| 4 | 4 | 4 |
| 5 | 14, -24 | 2 |
| 6 | 182, -476, -520 | 2 |
| 7 | -1454, 1570 | 2 |
| 8 | -108696, -2270792 | 8 |
| 9 | -137176976, -1261141910 | 2 |

The exponent vectors are recorded directly in the script. These witness
gcds alone suffice to certify every odd characteristic for each listed
size. They do not independently establish the gcd of all coefficients;
through `n=8` they agree with the full expansion's contents. No odd-prime
obstruction appears in these checks. No all-`n` nonvanishing assertion or
extension to arbitrary finite abelian groups is proved by this audit.

The `n=9` witnesses were selected and verified while the full expansion
was still running; no full expansion is needed for their certificate.
