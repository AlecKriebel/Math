# Independent determinant identity audit

Started: 2026-10-01 14:04:10 UTC. Completed: 2026-10-01 14:08:57 UTC.

Completion estimate: **100% of this narrowly scoped identity audit**. This is not an estimate of the parent research program. No sibling material, earlier review, or candidate proof was read; no Git operation or external communication was performed.

## Verdict and exact assumptions

**Verified.** For an integer dimension `n >= 1`, suppose `Z` is an almost surely finite, real symmetric positive semidefinite random matrix and its *full matrix* Laplace transform is

\[
\mathbb E e^{-\operatorname{tr}(uZ)}=\det(I+u)^{-\alpha/2}
\qquad(u\succeq0),
\]

with real parameter `alpha`. Then, for every `s > 0`,

\[
\boxed{\mathbb E\left[\det Z\,e^{-s\operatorname{tr}Z}\right]
=2^{-n}\prod_{j=0}^{n-1}(\alpha-j)
(1+s)^{-n\alpha/2-n}.}
\]

No existence assertion for any parameter, nor any classification of ranks of arbitrary laws, is made here. A trace-only transform would be insufficient for the differential argument.

## Analytic differentiation and the symmetric normalization

Use the independent coordinates `u_ij` with `i <= j` and define a symmetric matrix of commuting differential operators by

\[
D_{ii}=\partial_{u_{ii}},\qquad
D_{ij}=D_{ji}=\tfrac12\partial_{u_{ij}}\quad(i<j).
\]

The factor `1/2` is essential: `tr(uZ)` contains `2 u_ij Z_ij` off the diagonal. Consequently

\[
\det(-D)e^{-\operatorname{tr}(uZ)}
=\det Z\,e^{-\operatorname{tr}(uZ)}.
\]

At `u=sI`, choose a symmetric open neighborhood on which `u >= (s/2)I`. Write `T=tr Z`. Positivity gives `|Z_ij| <= T`, so each derivative through order `n` is bounded in absolute value by a constant times

\[
T^r e^{-(s/2)T}\qquad(0\le r\le n),
\]

which is bounded on `T >= 0`. Differentiation under expectation therefore follows from dominated convergence; ordinary unweighted determinant moments are not required. In particular, all terms in the operator are justified separately. The tilted determinant itself is integrable, since `det Z <= (T/n)^n`.

Thus the left side equals

\[
\left.\det(-D)\det(I+u)^{-\alpha/2}\right|_{u=sI}.
\]

## Noncircular polynomial interpolation proof

Set `t=1+s`. Rescaling `I+u=t(I+v)` gives

\[
\left.\det(-D)\det(I+u)^{-\alpha/2}\right|_{u=sI}
=t^{-n\alpha/2-n}R_n(\alpha),
\]

where

\[
R_n(\alpha)=\left.\det(-D_v)\det(I+v)^{-\alpha/2}\right|_{v=0}.
\]

`R_n` is a polynomial of degree at most `n` in `alpha`. To see this without any determinant differential identity, write `det(I+v)^(-alpha/2)=exp((-alpha/2) log det(I+v))` near `v=0`. Induction on the number of partial derivatives shows that each order-`n` derivative is the same exponential times a polynomial of degree at most `n` in `alpha`. At `v=0` the exponential equals one. The determinant operator is a fixed finite linear combination of order-`n` partial derivatives.

Determine this polynomial from the explicit integer Gaussian cases. For any integer `k >= n`, let `G` be `n x k` with independent standard real normal entries, and set

\[
Z_k=\tfrac12 GG^\mathsf T.
\]

Direct Gaussian integration gives `E exp(-tr(u Z_k))=det(I+u)^(-k/2)`. Under the scalar tilt `exp(-s tr Z_k)`, all entries of `G` have variance `1/t`, and the normalizing factor is `t^(-nk/2)`. Thus

\[
\mathbb E[\det Z_k e^{-s\operatorname{tr}Z_k}]
=t^{-nk/2-n}\mathbb E\det Z_k.
\]

Cauchy–Binet gives `det(GG^T)` as the sum of squared determinants over all `n`-column subsets. For an `n x n` standard Gaussian matrix `H`, expansion by permutations and rowwise independence gives

\[
\mathbb E(\det H)^2
=\sum_{\sigma,\tau}\operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)
\prod_i\mathbb E[H_{i,\sigma(i)}H_{i,\tau(i)}]
=n!.
\]

Therefore

\[
\mathbb E\det Z_k=2^{-n}\binom{k}{n}n!
=2^{-n}k(k-1)\cdots(k-n+1).
\]

It follows that `R_n(k)=2^(-n) product_{j=0}^{n-1}(k-j)` for infinitely many integers `k`. The two sides are polynomials, so they agree identically. This proves the boxed formula.

**Circularity check:** the interpolation invokes only matrices built from finitely many independent ordinary Gaussian variables. It never presumes a noninteger-parameter law, any general existence theorem, a rank classification, or the target symmetric determinant differential identity.

## Direct low-dimensional and boundary checks

For the purely algebraic calculation write `p=-alpha/2` and evaluate at `A=tI`.

| Dimension | Direct symmetric-operator value `det(D) det(A)^p` | Final tilted determinant expectation |
|---|---|---|
| 1 | `p t^(p-1)` | `(alpha/2) t^(-alpha/2-1)` |
| 2 | `p(p+1/2) t^(2p-2)` | `alpha(alpha-1)/4 t^(-alpha-2)` |
| 3 | `p(p+1/2)(p+1) t^(3p-3)` | `alpha(alpha-1)(alpha-2)/8 t^(-3alpha/2-3)` |

For dimension two, with `A=[[a,x],[x,b]]`, the operator is `partial_a partial_b - (1/4) partial_x^2`. The two contributions at `tI` are `p^2` and `p/2`, times `t^(2p-2)`.

For dimension three, with `A=[[a,x,y],[x,b,z],[y,z,c]]`, the operator is

\[
\partial_a\partial_b\partial_c
+\tfrac14\partial_x\partial_y\partial_z
-\tfrac14(\partial_a\partial_z^2+\partial_b\partial_y^2+\partial_c\partial_x^2).
\]

At `tI` these contributions are `p^3`, `p/2`, and `3p^2/2`, times `t^(3p-3)`. Applying `det(-D)=(-1)^n det(D)` gives the table.

At `alpha=0`, the transform at `u=sI` equals one. Since `exp(-s tr Z) <= 1`, equality of its expectation to one implies `tr Z=0` almost surely, hence `Z=0`. The identity consequently gives zero, as required.

For integer Gram examples with `0 <= k < n`, the explicit matrix has at most `k` independent column directions and its determinant vanishes; the falling product also vanishes. For `k >= n`, the Cauchy–Binet computation above supplies the positive value. These are checks of the constructed Gaussian examples only.

In particular, the half-Gram normalization is required: using `GG^T` without the half would yield `det(I+2u)^(-k/2)` and a different scalar-tilt factor. With the stipulated transform, the stated `2^(-n)` and `1+s` are correct.

Because the left side is nonnegative, the identity gives the finite-dimensional necessary condition `product_{j=0}^{n-1}(alpha-j) >= 0`. No sufficiency is inferred from that condition.

## Reproducible computation and checkpoint log

`check_jets.py` independently builds `det(cI+U)` by permutation expansion, computes the generalized-binomial Taylor jet for `det(cI+U)^p / det(cI)^p`, and applies the explicitly normalized symmetric determinant operator. It uses exact `Fraction` arithmetic and no third-party package.

Run: `python3 check_jets.py`.

Observed: **144/144 exact comparisons passed**, covering dimensions `1,2,3,4`, twelve integer and noninteger rational values of `alpha` (including zero and negative values as algebraic checks), and `c=1,3/2,2`. The algebraic checks at negative parameters do not assert existence of a probability law.

| UTC timestamp | Checkpoint | Completion estimate |
|---|---|---|
| 2026-10-01 14:04:10 | Started standalone audit; fixed exact claim and symmetric-coordinate convention. | 10% |
| 2026-10-01 14:06:48 | Finished differentiation justification, noncircular interpolation, direct dimensions 1–3, boundary checks, and 144 exact rational jet comparisons. | 95% |
| 2026-10-01 14:08:57 | Recorded complete checkable derivation, scope limitations, and reproducibility instructions. | 100% |

Strongest verified result: the boxed identity follows from the exact stated full-matrix Laplace transform and PSD support, in every finite dimension and for every `s>0`. Remaining gap for this scoped identity: **none identified**.
