# Regular weighted graphs at death--birth fitness two

## Status

- **PROVED:** among connected regular undirected weighted graphs on four
  vertices, `K_4` uniquely maximizes uniformly initialized dB fixation at
  fitness two.
- **EXACTLY COMPUTED:** the labelled fourteen-state equations and the positive
  rational-square comparison certificate for that theorem.
- **NUMERICALLY OBSERVED:** no regular counterexample through order nine; local
  optimization from interior and near-boundary starts always returned the
  complete kernel.
- **EXACTLY FALSIFIED:** global concavity of fixation on the regular-kernel
  polytope.  A positive rational order-seven counterexample is certified by
  three independent 126-state labelled solves.
- **OPEN:** the universal regular-graph maximizer theorem for arbitrary order.

Nothing in this folder proves the unrestricted obstruction required by the
main program.

## 1. Exact four-vertex theorem

To see the parameterization, compare an edge `ij` with its opposite edge
`kl`.  The sum of the weighted degrees of `i,j` is twice `w_ij` plus the four
cross-edge weights.  The degree sum of `k,l` is twice `w_kl` plus those same
four cross-edge weights.  Regularity therefore gives `w_ij=w_kl`.  After
scaling the common weighted degree to one, every regular four-vertex kernel
is consequently, up to labels,

\[
 P=\begin{pmatrix}
 0&a&b&c\\ a&0&c&b\\ b&c&0&a\\ c&b&a&0
 \end{pmatrix},\qquad a+b+c=1.
\]

Put

\[
 A=\sum_{x\in\{a,b,c\}}{4x\over4+x}.
\]

Direct solution of the dB equations at `r=2` gives

\[
 \rho_{\rm dB}(P,2)={4A\over4+5A}.                    \tag{1}
\]

Here is a short derivation.  Let `f_1,f_3` be the common fixation values of a
singleton and a triple.  For a mutant pair whose internal edge has weight
`x`, its probability of moving upward at the next type-changing event is

\[
 q_x={2(1+x)\over4+x}.
\]

The singleton-to-pair rate is `2x/(1+x)` and the complementary
triple-to-pair rate is `x/(2-x)`.  Substitution of
`f_{2,x}=q_xf_3+(1-q_x)f_1` in the singleton and triple equations gives

\[
 f_1={A\over1+A+B},\qquad
 B=\sum_x{x\over4+x}={A\over4},
\]

which is (1).

The comparison is an exact tangent-square identity:

\[
 A={12\over13}-{16\over169}
 \sum_x{(3x-1)^2\over4+x}.                             \tag{2}
\]

Since (1) is strictly increasing in `A`, equations (1)--(2) imply

\[
 \rho_{\rm dB}(P,2)\le {3\over7}
 =\rho_{\rm dB}(K_4,2),
\]

with equality only at `a=b=c=1/3`.  More explicitly,

\[
 {3\over7}-\rho_{\rm dB}(P,2)
 ={16\over91(4+5A)}\sum_x{(3x-1)^2\over4+x}.          \tag{3}
\]

The proof extends by continuity to zero edge weights whenever the support is
connected.

`verify_regular_k4.py` builds every labelled transition rate directly from
the dB rule, checks all fourteen transient harmonic equations, and checks
(2)--(3) symbolically.

## 2. Higher-order discovery

For order `n`, let `B` be the unsigned vertex--edge incidence matrix of
`K_n`.  The regular-kernel polytope is

\[
 p={1\over n-1}{\bf1}+Zx\ge0,
\]

where the columns of `Z` span `ker B`.  Its dimension is
`n(n-3)/2`.  `search_regular_db.py` uses this parameterization, exact row-sum
constraints, hit-and-run starts, and constrained local optimization.  The
search is cancellation-safe but floating point, so its output is not proof.

The initially most promising conjecture was

\[
 \rho_{\rm dB}(\lambda P+(1-\lambda)Q,2)
 \ge \lambda\rho_{\rm dB}(P,2)
 +(1-\lambda)\rho_{\rm dB}(Q,2).                      \tag{C}
\]

for symmetric stochastic zero-diagonal `P,Q`.  Had (C) held, averaging all
permutation conjugates of `P` gives `K_n`, proving the desired regular-graph
maximizer theorem immediately.  It is false even within the positive regular
polytope.

The exact counterexample uses two boundary kernels on seven vertices.  `E`
is a seven-cycle with edge weights `1/2`; `F` is the disjoint union of a
three-cycle with edge weights `1/2` and two unit-weight pairs.  Put

\[
 \epsilon={1\over200000},\quad
 P=(1-\epsilon)E+\epsilon K_7,\quad
 Q=(1-\epsilon)F+\epsilon K_7,\quad
 \lambda={1\over2000}.
\]

All off-diagonal entries of `P,Q` and
`M=lambda P+(1-lambda)Q` are positive.  Exact labelled-chain solution gives

\[
 \begin{aligned}
 \rho(P,2)&=0.402516099397341564\ldots,\\
 \rho(Q,2)&=0.384445451454253552\ldots,\\
 \rho(M,2)&=0.384364425692329774\ldots,
 \end{aligned}
\]

and

\[
 \rho(M,2)-\lambda\rho(P,2)-(1-\lambda)\rho(Q,2)
 =-0.0000900610858953220657\ldots<0.                 \tag{4}
\]

The exact reduced numerator and denominator have 6,857 and 6,871 bits.
`verify_concavity_counterexample.py` reconstructs the three chains over
`QQ`, checks positivity and regularity, and certifies the sign.  Every graph
in this counterexample is dB-suppressing relative to `K_7`, so it closes the
concavity route but does not refute complete-graph maximization.

The numerical interior evidence had a genuine structural motivation special
to `r=2`.  Along
every adjacent pair of mutant sets `S` and `S+v`, write
`x=P_{vS}`.  The opposing continuous-time changing rates are

\[
 q(S,S+v)={2x\over1+x},\qquad
 q(S+v,S)={1-x\over1+x},
\]

and hence sum exactly to one.  Thus every admissible kernel has the same
unweighted edge-rate sum on the configuration hypercube.  The exact
counterexample proves that this identity does not make the absorption
functional concave; any nonreversible-capacity argument needs an additional
monotone quantity.

An equivalent-looking regular-only marginal target also survived the
screens.  If `p_i` is the stationary dB-dual occupancy marginal and

\[
 c_n={n(2^{n-1}-1)\over (n+1)2^{n-2}-n}
 ={1\over1-\rho_{\rm dB}(K_n,2)},
\]

then numerically

\[
 \sum_i{p_i\over1-p_i}\le c_n\sum_i p_i.              \tag{5}
\]

Jensen would turn (5) into the exact complete-graph mean bound.  The tempting
termwise odds bound
`p_i/(1-p_i)<=c_n sum_j P_ji p_j` is false from order five onward, while the
aggregate statement (5) remains open.

There is an exact flux reformulation.  Write `q_i=1-p_i`, let
`eta_ij=Pr(i notin A,j in A)` in the stationary dB dual, and set

\[
 H_{ij}={2P_{ij}\over1+P_{ij}}.
\]

Stationary balance of the indicator of `i` gives

\[
 p_i=\sum_jH_{ij}\eta_{ij}.                            \tag{6}
\]

Consequently

\[
 \sum_i{p_i\over q_i}
 =\sum_{i,j}H_{ij}{\eta_{ij}\over q_i},\qquad
 \sum_i p_i=\sum_{i,j}H_{ij}\eta_{ij}.                \tag{7}
\]

Thus (5) says that the hole-to-particle stationary flux sees a weighted mean
of `1/q_i` no larger than its complete-graph value.  A sufficient, stronger
target is the component bound

\[
 p_i\le\rho_{\rm dB}(K_n,2)\quad\hbox{for every }i.   \tag{8}
\]

No counterexample to (8) was found in the regular-polytope searches, but no
proof is known.  Pointwise complete-cardinality bounds for mutant sets of
size two and above are false, so a direct induction on set size cannot prove
(8).

For completeness, if `m=n^{-1}sum_i p_i`, Jensen and (5) give

\[
 {m\over1-m}\le {1\over n}\sum_i{p_i\over1-p_i}
 \le c_nm,
\]

and hence `m<=1-1/c_n=rho_dB(K_n,2)`.  This reaches the finite baseline; the
ordinary coefficient-two odds inequality reaches only `m<=1/2`.

## 3. Reproduction

Use a single BLAS thread to avoid oversubscription on the exact-state solves:

```text
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python search_regular_db.py --n 7 --starts 80 --seed 17

OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python screen_regular_concavity.py --max-n 8 --pairs 250

python verify_regular_k4.py

python verify_concavity_counterexample.py
```

The last two commands are exact verifiers: respectively a positive theorem
and a route-falsifying counterexample.
