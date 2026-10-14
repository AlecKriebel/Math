# Proof 13  A uniform center dominant coefficient region

This earlier coefficient region and its numerical gap constant are retained. The stronger all-p radial-cone center conditions are proved in [Proof 40](40_strong_center_green_cone.md).

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Theorem

Let `2<p<=3`, `q=p/2`, and `a_j,b_j>=0`, `c>0`. Suppose

`sum_j(a_j+b_j) <= c/3`.

For any subset `S` of endpoint pairs whose second endpoint sign is reversed, put

`P_+(z)=c+sum_j(a_j z_j+b_j z_j^(-1))`,

`P_S(z)=c+sum_j(a_j z_j+sigma_j b_j z_j^(-1))`,

where `sigma_j=-1` precisely on `S`, and integration is normalized Haar measure on the product torus. Then

`integral |P_+|^p - integral |P_S|^p`

`>= (7/8) q(q-1) c^(p-2) sum_(j in S) a_j b_j >=0`.                (1)

This estimate is dimension-uniform. In particular, the coefficient box with center magnitude `c` and endpoint bounds `a_j,b_j` has the full real majorant inequality. This is a coefficient-dependent sufficient condition, not an assertion that all centered-cross sets have the property.

## Normalization and convergent expansion

Divide the polynomials by `c`; it suffices to prove the claim at `c=1`. Write

`rho=sum_j(a_j+b_j)<=1/3`, `a=q(q-1)>0`, and `f=sum_j(a_j z_j+b_j z_j^(-1))`.

Since `|f|<=rho<1`, the binomial product

`|1+f|^(2q)=(1+f)^q(1+conjugate(f))^q`

has its usual absolutely and uniformly convergent double series. Both factors use the analytic branch on the disk `|f|<1`; their product is the displayed positive real power. We may extract the constant Laurent coefficient and group by total degree.

For each coordinate, a constant Laurent monomial has the same parity for its total occurrences of `a_j` and `b_j`: if their occurrences in `f` and `conjugate(f)` are denoted by `A_f,B_f,A_bar,B_bar`, the constant-exponent equation is

`A_f+B_bar=B_f+A_bar`.

In particular, its total degree is even. A monomial whose sign changes when the `b_j`, `j in S`, are negated must have an odd occurrence of at least one such `b_j`, and therefore an odd occurrence of the corresponding `a_j`. It is divisible by `a_j b_j`.

## The degree-two contribution

The `f conjugate(f)` term is sign-insensitive. The `f^2` and `conjugate(f)^2` terms give the exact difference

`4 q(q-1) sum_(j in S) a_j b_j = 4a sum_(j in S) a_j b_j`.        (2)

There is no odd-degree constant term.

## A coefficientwise bound for every higher degree

Let `b_k=|binom(q,k)|` and

`C_m=sum_(k=0)^m b_k b_(m-k)`.

The absolute coefficients of the degree-`m` integrated polynomial are bounded coefficientwise by those of `C_m rho^m`, before integration. For every sign-sensitive monomial, choose a flipped pair dividing it. More formally, multiplying the mixed derivative in `a_j,b_j` by `a_j b_j` multiplies each such monomial by the product of its two positive exponents, which is at least one. Taking the union bound over `j in S`, the absolute sign difference at degree `m` is therefore at most

`2 sum_(j in S) a_j b_j * m(m-1) C_m rho^(m-2)`.                (3)

This remains valid if some endpoint coefficients vanish, by polynomial continuity. Terms counted more than once only enlarge the upper bound.

For `1<q<=3/2` and `k>=2`,

`b_k <= a/[k(k-1)]`.                                         (4)

Indeed, after the initial factor `q(q-1)`, every factor `r-q` for `r>=2` is nonnegative and at most `r-1`. Also `q<=3/2` and `a<=3/4`.

For `m>=4`, separate the `k=0,1,m-1,m` terms from the convolution. Equations (4) give

`m(m-1) C_m/a`

`<= 2 + 2q m/(m-2)`

`   + a sum_(k=2)^(m-2) m(m-1)/[k(k-1)(m-k)(m-k-1)]`.

For `u,v>=2` with `u+v=m`,

`m(m-1) <=3[u(u-1)+v(v-1)]`.

To check it, the difference between right and left sides is

`2[u^2+v^2-uv-u-v] >= 2[m^2/4-m] >=0`.

Thus the last sum is at most

`6 sum_(k=2)^(m-2) 1/[k(k-1)] <=6`.

Since `m/(m-2)<=2`, we obtain the simple uniform bound

`m(m-1) C_m <= (25/2) a`, for every `m>=4`.                   (5)

## Exact remainder and conclusion

Only even degrees survive integration. Summing (3) using (5), the entire degree-at-least-four remainder has absolute value at most

`25 a sum_(j in S) a_j b_j * rho^2/(1-rho^2)`.

For `rho<=1/3`, this is at most

`(25/8) a sum_(j in S) a_j b_j`.

Subtracting this certified remainder from (2) proves the normalized lower bound

`(4-25/8) a sum_(j in S) a_j b_j`

`= (7/8) a sum_(j in S) a_j b_j`.

Restoring the factor `c^p` gives (1).

## Arbitrary signs and arbitrary real majorants in the stated box

An overall sign makes the center coefficient positive. Independently replacing `z_j` by `-z_j` removes a common sign on either endpoint pair, leaving exactly one of the above subsets `S`. These transformations preserve Haar measure and the absolute moment, so (1) compares every sign vertex of the specified coefficient box with its all-positive vertex.

For `p>=1` the `p`th absolute moment is convex in the real coefficient vector. Every coefficient vector in that box is a convex combination of its sign vertices. Jensen's inequality gives the full real arbitrary-majorant assertion for that box. No dominance condition is imposed on an individual interior vector; it is the nonnegative comparison vector that satisfies the hypothesis.

## Scope

This rules out every centered-cross counterexample whose center is at least three times the sum of all endpoint magnitudes, uniformly over dimension and all `2<p<=3`. It supplies an explicit bound rather than treating a leading Taylor coefficient as a proof. It does not cover a dominant endpoint, a small center, or intermediate-amplitude cancellations. It does not establish robust radial-noise comparison or arbitrary affine-join permanence for the unresolved centered-cross blocks.
