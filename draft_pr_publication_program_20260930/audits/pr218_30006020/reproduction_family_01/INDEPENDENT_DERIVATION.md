# Independent finite mechanisms

These checks are model/algebra checks. They are not new mathematics, a proof of the asymptotic theorem, an independent derivation of the geometric correspondence, or a priority finding.

## Shifted-simplex computation

Let `X` have an integer-shape Dirichlet law with total shape `A`. Select `r` coordinates of shapes `alpha_i`, and require `X_i >= t_i`. Put `L = sum t_i`. For nonnegative thresholds with `L <= 1`, translation of the selected coordinates in the simplex and expansion of each translated power gives

\[
 \Pr(X_i\ge t_i,\ i\le r)
 = (A-1)!\sum_{0\le d_i<\alpha_i}
   \left(\prod_i\frac{t_i^{d_i}}{d_i!}\right)
   \frac{(1-L)^{A-1-\sum_i d_i}}{(A-1-\sum_i d_i)!}.
\]

For `L > 1`, the probability is zero. One way to verify the formula is to expand `(u_i+t_i)^(alpha_i-1)` with `u_i=X_i-t_i` and apply the elementary Dirichlet monomial integral to each term. The unselected coordinates may be aggregated into a single residual shape. The same calculation works when every coordinate is selected and the residual shape is zero: the integration is then over the original codimension-one simplex. The smallest exponent in that case is `r-1`, so no negative factorial occurs. The one-coordinate total atom is handled explicitly when converting to inclusive rectangle events.

For a rectangle, inclusion-exclusion changes selected thresholds from lower to upper endpoints. Unlike the archived direct rectangle expansion, this formula also handles rectangles cut by `sum X_i=1` without splitting their boundary geometry. The independent program checks integer Beta marginals against the binomial/order-statistics expression and checks the explicit singular examples

\[
 \Pr_{\operatorname{Dir}(2,2)}(X_1,X_2\in[1/4,1/2])=0,
 \qquad
 \Pr_{\operatorname{Dir}(2,2)}(X_1,X_2\in[1/4,3/4])=11/16.
\]

The first example would fail if normalized coordinates were incorrectly marked independently. The reviewed manuscript independently marks the unnormalized Gamma variables and subsequently treats the shared total, so it does not make that error.

The program derives the exact common-pi-stripped assembly weights from `S(z)=sin(sqrt(z))/sqrt(z)` and `log H(z)=-log S(z)/2`. If `S(z)=sum s_n z^n` and `log H(z)=sum a_n z^n`, differentiation gives

\[
 a_n=-\frac{n s_n+2\sum_{j=1}^{n-1}j a_j s_{n-j}}{2n}.
\]

It literally enumerates integer partitions at total size one through eight. Within each partition it selects every subset of components and applies the shifted-simplex probability. This gives every factorial moment of the normalized count in each of `[1/4,1/2]` and `[1/6,2/3]`, including repeated sizes and selections of every component. If `f_r=E[(M)_r]`, the complete finite distribution is recovered by

\[
 \Pr(M=k)=\frac1{k!}\sum_{r=k}^{n}\frac{(-1)^{r-k}}{(r-k)!}f_r.
\]

This follows by expanding `E[z^M]=sum f_r(z-1)^r/r!`. Each resulting probability is nonnegative and the total is exactly one; the first and second moments agree with the distribution. Separately formed ordered selected-assembly sums agree through order three. These latter checks share the shifted-simplex probability kernel, so they test enumeration and selection factors rather than provide a second probability oracle. The Beta/order-statistics comparison and explicit singular examples separately check that kernel.

## KdV intersection-number oracle

The independent evaluator uses the genus-zero formula

\[
 \langle\tau_{d_1}\cdots\tau_{d_n}\rangle_0
 =\frac{(n-3)!}{\prod_i d_i!}
\]

in the stable, dimension-correct range, the string equation, and the first KdV equation

\[
\begin{aligned}
 &(2g+n-1)\langle\tau_0\prod_{i=1}^n\tau_{d_i}\rangle_g\\
 &\quad=\frac1{12}\langle\tau_0^4\prod_{i=1}^n\tau_{d_i}\rangle_{g-1}
 +\frac12\sum_{h=0}^g\sum_{S\subseteq\{1,\ldots,n\}}
 \langle\tau_0^2\prod_{i\in S}\tau_{d_i}\rangle_h
 \langle\tau_0^2\prod_{i\notin S}\tau_{d_i}\rangle_{g-h}.
\end{aligned}
\]

Unstable and dimension-incorrect terms are zero. To obtain a target correlator with no zero degree, increase its largest degree by one and apply this equation. The string equation isolates the target; its correction terms have the largest degree increased by one, so they terminate when another degree reaches zero. Same-genus terms in a nonzero split have fewer original insertions, while the nonsplit term lowers genus. A suitable induction is genus, then number of nonzero insertions, then decreasing largest degree at fixed total degree. No published DVV factorial coefficient or intersection value is used to compute this oracle.

Only after computing this independently defined oracle does the program load the function definitions of the pinned published DVV evaluator for comparison. Its top-level loops, assertions and output writes are excluded. The two recursions agree on all 244 sorted, dimension-correct stable degree tuples in these finite ranges:

| Genus | Maximum marked points | Degree multisets |
|---|---:|---:|
| 0 | 10 | 45 |
| 1 | 8 | 66 |
| 2 | 6 | 66 |
| 3 | 4 | 41 |
| 4 | 3 | 26 |

The KdV evaluator also agrees with `1/(24^g g!)` for the one-point correlators in genus one through ten. This is a separate finite anchor. Agreement between these standard recursions does not establish the published large-genus uniform intersection estimates or their geometric application.

## Exact scope of the additional count

The current result is 1,158 successful rational checks, including 244 comparison checks and 244 separate positivity checks for the same intersection tuples. The number is an assertion count, not a count of independent theorems. It includes 398 cached rectangle-probability bound checks, 144 marginal comparisons, 16 full count-distribution mass checks and 16 full count-distribution positivity checks. The exact family counts and all 16 rational count distributions are in `INDEPENDENT_CONTROLS_RECEIPT_01.json`.
