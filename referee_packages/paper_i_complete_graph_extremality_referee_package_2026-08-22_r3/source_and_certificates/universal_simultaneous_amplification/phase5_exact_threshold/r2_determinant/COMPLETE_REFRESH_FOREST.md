# Complete-refresh forests for the true fitness-two sign

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note introduces a forest interpolation that targets the true collision
coefficient, rather than the stronger promotion coefficient.

It proves three new facts.

1. The complete-to-actual active-tree numerator has zero constant and linear
   terms for every loopless row-stochastic kernel.
2. On every weighted triangle, every Bernstein coefficient of that
   interpolation has an explicit centered positive certificate.  Thus the
   true tree numerator is positive along the entire interpolation, not only
   at its endpoint.
3. For every population order, the quadratic coefficient is strictly
   positive on the full antisymmetric row-balanced perturbation sector.  The
   proof is an explicit two-tree/rank-recursion certificate.

The corresponding all-order statement for the standard and symmetric
balanced sectors, and positivity of every higher forest coefficient, remain
**OPEN**.  Exact hostile screens through order five support them but are not
a universal proof.

## 1. The interpolation and its exact endpoint

Let

\[
 \mathcal Y=\{(B,v):\varnothing\ne B\subseteq V\setminus\{v\}\}
\]

and let `K(P)` be the active kernel.  From `y=(B,v)`, `k=|B|`, it makes one
of the following two moves with probability one half.

* Sample `i` from row `P_v` and output `(B union {i},v)`.
* Choose `w` uniformly from `B`, sample `i` from row `P_w`, and output
  `((B minus {w}) union {i},w)`.

Let `P_0` be the uniform off-diagonal kernel, put

\[
 K_0=K(P_0),\qquad \Delta=K(P)-K_0,
 \qquad K_\alpha=K_0+\alpha\Delta,\quad0\le\alpha\le1.             \tag{1}
\]

The active kernel is linear in `P`, so `K_alpha=K(P_0+alpha(P-P_0))`.
For `N=n-1`, define

\[
 H(B,v)={1\over|B|},\qquad
 c_0={2^N-1\over N2^{N-1}},                         \tag{2}
\]

and the complete stationary row

\[
 \nu_0(B,v)={|B|\over nN2^{N-1}}.                  \tag{3}
\]

Thus `nu_0 H=c_0=1/m_K`.  The complete-refresh determinant is

\[
 \boxed{
 \mathcal F_P(\alpha)=
 \det\left[I-K_\alpha+(H-c_0\mathbf1)\nu_0\right].}               \tag{4}
\]

If `tau_y(alpha)` is the directed in-tree weight rooted at `y`, the matrix
tree theorem and `nu_0 1=1` give

\[
 \boxed{
 \mathcal F_P(\alpha)=
 \sum_{y\in\mathcal Y}\tau_y(\alpha)\{H(y)-c_0\}.}                \tag{5}
\]

Consequently `(4)` is exactly the true collision tree numerator at
`alpha=1`.  No promotion threshold appears.

## 2. Why the first two coefficients vanish

Let `S` average active states uniformly within each rank.  Permutation
symmetry of `K_0` gives `SK_0=K_0S`, while direct averaging of the two active
moves gives

\[
 \boxed{S\Delta S=0.}                               \tag{6}
\]

Indeed, a uniform `k`-subset of `V minus {v}` contains a sample from any row
with mean probability `k/N`; after retargeting, the corresponding mean is
`(k-1)/N`.  These are exactly the complete rank-transition probabilities.

Put

\[
 G=(I-K_0+\mathbf1\nu_0)^{-1},qquad q=H-c_0\mathbf1.              \tag{7}
\]

Both `q` and `Gq` are rank functions.  Since `nu_0=nu_0S`, `(6)` yields

\[
 \nu_0\Delta Gq=\nu_0S\Delta SGq=0.               \tag{8}
\]

Equivalently, if `nu_alpha` is stationary for `K_alpha`,

\[
 \nu_\alpha q
 =\alpha^2\nu_0\Delta G\Delta Gq+O(\alpha^3).      \tag{9}
\]

Since the total tree weight is positive, `(8)` proves

\[
 \boxed{\mathcal F_P(0)=\mathcal F_P'(0)=0.}        \tag{10}
\]

There is also a literal forest interpretation.  Expanding every tree edge
as `(1-alpha)K_0+alpha K(P)` writes `(5)` in the Bernstein basis.  Its
coefficient at order `j` is the signed root sum over active in-trees having
exactly `j` actual-colored edges and all other edges complete-colored.
Equation `(10)` cancels the zero- and one-colored tree packets globally.

## 3. A full Bernstein certificate on a triangle

Let `n=3` and put

\[
 w_{01}=a,qquad w_{02}=b,qquad w_{12}=c,qquad a,b,c>0.
\]

Direct expansion of the nine-state determinant gives

\[
 65536(a+b)^2(a+c)^2(b+c)^2\mathcal F_P(\alpha)
 =\sum_{j=2}^{6}\binom6j b_j\alpha^j(1-\alpha)^{6-j}.              \tag{11}
\]

Every coefficient has the centered form

\[
 b_j=\sum_{\rm cyc}(a-b)^2Q_j(a,b,c),               \tag{12}
\]

where

\[
 Q_j(x,y,z)=A_jx^2y^2+B_jxy(x+y)z+C_jxyz^2
             +D_j(x+y)z^3+E_jz^4                  \tag{13}
\]

and the nonnegative coefficients are

| `j` | `A_j` | `B_j` | `C_j` | `D_j` | `E_j` |
|---:|---:|---:|---:|---:|---:|
| 2 | `0` | `396/5` | `913/15` | `55/3` | `913/15` |
| 3 | `0` | `1332/5` | `913/5` | `131/5` | `913/5` |
| 4 | `0` | `588` | `5468/15` | `8/3` | `5324/15` |
| 5 | `196/3` | `3008/3` | `1816/3` | `0` | `492` |
| 6 | `192` | `1536` | `912` | `0` | `576` |

Every `Q_j` is strictly positive on the positive orthant.  Therefore

\[
 \mathcal F_P(\alpha)>0\quad(0<\alpha\le1)
\]

unless `a=b=c`, when the polynomial vanishes identically.  Formula `(11)`
is an actual coefficientwise forest certificate for the true sign.

## 4. The invariant quadratic coefficient

Write

\[
 \delta=P-P_0,qquad \sum_j\delta_{ij}=0,qquad\delta_{ii}=0.       \tag{14}
\]

The coefficient in `(9)` is

\[
 \mathcal R_2(\delta)=\nu_0\Delta G\Delta Gq.       \tag{15}
\]

It is an `S_n`-invariant quadratic form on the row-zero off-diagonal
matrices.  For `n>=4`, that representation splits without multiplicity into
the standard, symmetric row/column-balanced, and antisymmetric balanced
sectors.  Hence there are scalars `a_n,b_n,c_n` such that

\[
 \mathcal R_2
 =a_nA+b_nB+c_nC,                                  \tag{16}
\]

where

\[
 A=\sum_{i,j}\delta_{ij}^2,qquad
 B=\sum_{i,j}\delta_{ij}\delta_{ji},\qquad
 C=\sum_j\left(\sum_i\delta_{ij}\right)^2.         \tag{17}
\]

The three sector eigenvalues are

\[
 \lambda_{\rm sym}=a_n+b_n,qquad
 \lambda_{\rm anti}=a_n-b_n,qquad
 \lambda_{\rm std}={ (n-1)a_n+b_n\over n(n-2)}+c_n.              \tag{18}
\]

For the standard formula, if `s` has coordinate sum zero, its canonical
embedding is

\[
 E(s)_{ij}={s_i+(n-1)s_j\over n(n-2)},\qquad i\ne j.               \tag{19}
\]

It has column sum `s`, squared norm
`(n-1)||s||^2/[n(n-2)]`, and transpose pairing
`||s||^2/[n(n-2)]`, which proves `(18)`.

Exact orbit reductions give the following values.

| `n` | `lambda_std` | `lambda_sym` | `lambda_anti` |
|---:|---:|---:|---:|
| 3 | `2/33` | — | `1/9` |
| 4 | `261/5120` | `3/208` | `57/640` |
| 5 | `3434/85971` | `359/26660` | `143/2100` |
| 6 | `2268275/73893888` | `176345/14823936` | `1435/27648` |
| 7 | `117521693/4968964480` | `7823511/760600064` | `207131/5174400` |

The independent orbit verifier finds all three values strictly positive
through `n=12`.  This is exact finite computation.  The next section proves
the antisymmetric column for every `n`.

## 5. All-order antisymmetric two-tree theorem

### Theorem

For every `n>=3` and every nonzero antisymmetric row-zero perturbation
`delta`,

\[
 \boxed{\mathcal R_2(\delta)>0.}                   \tag{20}
\]

Thus the complete kernel is a strict local maximizer of the stationary dual
mean, equivalently a strict local minimizer of inverse mean, throughout the
entire antisymmetric balanced sector.

### Proof

Put `N=n-1`.  Under `nu_0`, the active rank has law

\[
 \pi_k={\binom{N-1}{k-1}\over2^{N-1}},qquad1\le k\le N.          \tag{21}
\]

The complete rank chain is the lazy heat-bath chain on `N-1` fair bits:

\[
 R_{k,k+1}={N-k\over2N},\qquad
 R_{k,k-1}={k-1\over2N}.                           \tag{22}
\]

Let `h_k` solve `(I-R)h=1/k-c_0`, with arbitrary additive normalization,
and put

\[
 d_k=h_k-h_{k+1},\qquad1\le k<N.                  \tag{23}
\]

Then

\[
 d_1>d_2>\cdots>d_{N-1}>0.                         \tag{24}
\]

To see this without an algebraic ansatz, couple adjacent heat-bath chains
using the same updated bit and the same fair replacement.  Until their one
distinguished unequal bit is updated, their forcing difference is

\[
 {1\over X+1}-{1\over X+2}>0,
\]

where `X` is the number of ones among the shared bits.  Starting the shared
bits with one additional one makes `X` stochastically larger at every time,
so the forcing difference is smaller.  Summing the convergent Poisson
series proves positivity and monotonicity in `(24)`.

For an antisymmetric `delta`, define

\[
 x(B,v)=\sum_{i\in B}\delta_{vi}.                  \tag{25}
\]

The internal ordered sum over `B` cancels, and direct use of the two active
moves gives

\[
 \Delta h(B,v)={d_k\over2}x(B,v),\qquad k=|B|.      \tag{26}
\]

Moreover, for an arbitrary rank sequence `f_k`,

\[
 K_0\{f_kx(B,v)\}
 ={kf_k+(N-k-1)f_{k+1}\over2N}x(B,v).              \tag{27}
\]

It follows that `G Delta h=r_kx`, where `r_N=0` and

\[
 \boxed{
 (2N-k)r_k-(N-k-1)r_{k+1}=Nd_k,
 \qquad1\le k<N.}                                 \tag{28}
\]

Backward induction using `(24)` proves

\[
 0\le r_{k+1}<r_k\le {N\over N+1}d_k.              \tag{29}
\]

Indeed, the upper bound at `k+1`, together with `d_{k+1}<d_k`, makes
`Nd_k-(N+1)r_{k+1}>0`, which is exactly the numerator of
`r_k-r_{k+1}`; substituting the same bound in `(28)` proves the upper bound
at `k`.

It remains to evaluate the second application of `Delta`.  Put
`T=sum_(i,j)delta_ij^2`.  Uniformly conditional on active rank `k`, simple
sampling without replacement gives

\[
\begin{aligned}
 E x^2&={k(N-k)\over nN(N-1)}T,\\
 E\sum_{i\notin B}\delta_{vi}^2&={N-k\over nN}T,\\
 E\sum_{w\in B}\left(\sum_{i\in B\setminus\{w\}}\delta_{wi}\right)^2
 &= {k(k-1)(N-k+1)\over nN(N-1)}T,\\
 E\sum_{w\in B}\sum_{i\notin B}\delta_{wi}^2
 &= {k(N-k+1)\over nN}T.                           \tag{30}
\end{aligned}
\]

Expanding the two active moves once more and using `(30)` yields

\[
\begin{aligned}
 E_k[\Delta(r_kx)]={T\over2nN}\Bigg[&
 {k(N-k)\over N-1}(r_k-r_{k+1})+(N-k)r_{k+1}\\
 &+{(k-1)(N-k+1)\over N-1}(r_{k-1}-r_k)
 +(N-k+1)r_k\Bigg].                                \tag{31}
\end{aligned}
\]

At the boundary take `r_N=0`; the coefficient multiplying `r_0-r_1`
vanishes.  Every displayed term is nonnegative by `(29)`, and the total is
strictly positive when `T>0`.  Finally,

\[
 \mathcal R_2(\delta)=\sum_{k=1}^N\pi_k
 E_k[\Delta(r_kx)]>0,
\]

which proves `(20)`.  QED.

## 6. What remains

The all-order target would follow from either of the following stronger
statements.

1. Every Bernstein forest coefficient in `(5)` is nonnegative.
2. The two remaining quadratic eigenvalues in `(18)` are positive for all
   `n`, followed by a higher-colored-tree extension.

The exact screens support both statements, including kernels outside the
reversible graph class.  They are nevertheless **OPEN**.  The present
advance is the first global cancellation (`(10)`), a complete all-alpha
forest certificate at order three (`(11)`--`(13)`), and one full all-order
two-tree sector theorem (`(20)`).
