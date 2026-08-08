# Symmetric-flow and circulation reduction at dB fitness two

Date: 2026-08-07 (America/Los_Angeles)

## Status

This note gives two **PROVED exact identities** which refine the open
Green--collision inequality.  They expose the auxiliary sufficient split

\[
   \mathcal L\le \mathcal S\le \mathcal V.                 \tag{1}
\]

The first inequality in (1) is **EXACTLY FALSE**, even for a positive
complete-support undirected six-vertex graph; an explicit integer witness is
given below.  The second inequality remains **OPEN**, but is no longer being
used as an intermediate target because it cannot imply the desired sign by
itself.  The exact identities and counterexamples are retained to prevent
this attractive but invalid split from being revived.

## 1. Directed complete flow

Let `Q=Q_K` be the generator of the complete geometric-union dual on the
nonempty proper subsets, and let

\[
 \pi_K(A)={|A^c|\over n(2^{n-1}-1)},\qquad
 c_{AB}=\pi_K(A)Q(A,B)\quad(A\ne B).              \tag{2}
\]

Stationarity of `pi_K` says that `c` is a balanced directed flow.  It is not
reversible.  In one update a target `v in A` is removed and the distinct
sites in a geometric number of uniform samples from `V\{v}` are inserted.
Consequently, every off-diagonal transition satisfies

\[
 A\setminus B=\{v\}.                              \tag{3}
\]

Put `a=|A|` and `j=|B\setminus A|`.  The transition rate for a prescribed
target and a prescribed `j`-set of newly hit holes is

\[
 \gamma_{a,j}
 =\sum_{\ell=0}^j(-1)^{j-\ell}{a-1+\ell\over
                       2(n-1)-(a-1+\ell)}.        \tag{4}
\]

Formula (4) is inclusion--exclusion applied to the probability generating
function `x/(2-x)` of a geometric number of samples.  A reverse transition
can exist only when `j=1`, in which case `A` and `B` are a same-rank swap.
The reverse swap has the same rate and the same `pi_K` mass.  Thus:

* every same-rank current is reversible;
* every rank-changing edge is one-way;
* the rank-changing current is divergence-free and hence decomposes into
  nonnegative directed cycle flows.

This also gives a short exact disproof of reversibility of `Q_K`.  For
example, on three vertices the transition from a two-set to either of its
singletons has positive rate, whereas the reverse transition is impossible.

## 2. The symmetric pairing

Let `pi` be the stationary law for the actual dual, put

\[
 g={\pi\over\pi_K},
\]

and solve the already verified complete Poisson equation

\[
 Q\psi=F,\qquad F(A)=U_{|A^c|}Z(A).               \tag{5}
\]

Then

\[
 \mathcal L=\langle g,Q\psi\rangle_{\pi_K}.       \tag{6}
\]

Let `Q*` be the adjoint in `L^2(pi_K)`, and set

\[
 Q_s={Q+Q^*\over2},\qquad Q_a={Q-Q^*\over2}.      \tag{7}
\]

Define

\[
 \boxed{
 \mathcal S:=\langle g,Q_s\psi\rangle_{\pi_K}
 =-{1\over2}\sum_{A\ne B}c_{AB}
      (g(B)-g(A))(\psi(B)-\psi(A)).}              \tag{8}
\]

No reversibility assumption is used in (8): the product of the two
increments is symmetric, so the antisymmetric part of `c` cancels.
Equations (6)--(8) give the exact two-part reduction

\[
 \mathcal L-\mathcal S=\langle g,Q_a\psi\rangle_{\pi_K},
 \qquad
 \mathcal V-\mathcal S
 =\mathcal V+{1\over2}\sum_{A\ne B}c_{AB}\Delta g_{AB}\Delta\psi_{AB}.
                                                               \tag{9}
\]

Thus the two open signs in (1) are precisely:

1. an antisymmetric-current sign;
2. a symmetric Dirichlet absorption by the exact tangent remainder.

They do not presently reduce to the same inequality.

## 3. Exact cycle-area form of the first sign

Same-rank swaps contribute equally to `L` and `S`.  On a one-way
rank-changing edge `A -> B`, its contribution to `L-S` is

\[
 {c_{AB}\over2}\{g(A)+g(B)\}\{\psi(B)-\psi(A)\}. \tag{10}
\]

Decompose the balanced rank-changing current into directed cycles `C`, with
cycle weights `theta_C>=0`.  If a cycle has successive states
`A_0,...,A_{m-1},A_m=A_0`, then

\[
 \boxed{
 \mathcal L-\mathcal S
 ={1\over2}\sum_C\theta_C\sum_{i=0}^{m-1}
   \{g(A_i)\psi(A_{i+1})-g(A_{i+1})\psi(A_i)\}.}  \tag{11}
\]

The inner sum is twice the oriented polygonal area of the cycle in the
`(g,psi)` plane.  Therefore `L<=S` would be exactly a weighted
nonpositive-area theorem.  It is false.  A positive-support directed
five-vertex row kernel first shows that stationarity alone cannot fix the
orientation.  More decisively, take the complete undirected graph on six
vertices with integer edge weights, in lexicographic order

```text
01,02,03,04,05,12,13,14,15,23,24,25,34,35,45
 = 3,300,2,5,1,3,3,1,300,1,1,1,20,1,1.
```

The exact 62-state rational calculation gives

\[
 \mathcal L\simeq0.1390362328011658,
 \quad\mathcal S\simeq0.1384866253193488,
 \quad\mathcal V\simeq0.2474805282884134,          \tag{11a}
\]

with `L-S>0` certified by its exact positive rational numerator.  At the
same time `L-V<0`, so this refutes only the auxiliary split, not complete-
graph maximality at fitness two.

There is also an exact expansion over the original undirected vertex pairs.
Put

\[
 b_{uv}={2\over n-1}-P_{uv}-P_{vu},\qquad
 \sum_{u<v}b_{uv}=0,                              \tag{12}
\]

and define the level-centered pair forcing

\[
 f_{uv}(A)=U_{|A^c|}\left\{
 1_{\{u,v\}\subseteq A}-{ |A|(|A|-1)\over n(n-1)}\right\}.
                                                               \tag{13}
\]

It has zero `pi_K` mean.  If `Q eta_uv=f_uv`, then linearity and (12) give

\[
 \psi=\sum_{u<v}b_{uv}\eta_{uv}+\hbox{constant},\qquad
 \boxed{\mathcal L-\mathcal S
 =\sum_{u<v}b_{uv}E_\pi[Q_a\eta_{uv}].}           \tag{14}
\]

Even away from the six-vertex refutation, (14) is not a termwise square
decomposition.  On the undirected three-path
with consecutive edge weights `(1,4)`, the contribution of the vertex pair
`{0,1}` in (14) is exactly

\[
 {4\over13365}>0,                                 \tag{15}
\]

while the three pair contributions sum to `-8/891`.  Any proof must use
cross-pair cancellation, not a separate sign for every original edge.

## 4. Why the second sign is still global

Since the actual stationary law annihilates its generator `Q_P`,

\[
 \mathcal S=E_\pi[(Q_s-Q_P)\psi].                 \tag{16}
\]

A pointwise proof of `v(A)>=(Q_s-Q_P)psi(A)` is false.  On the weighted path
with consecutive weights `(1,2)`, the exact residuals include

\[
 v(\{1\})-(Q_s-Q_P)\psi(\{1\})=-{13\over990},
\qquad
 v(\{0,1\})-(Q_s-Q_P)\psi(\{0,1\})=-{4\over495}.
                                                               \tag{17}
\]

Hence `S<=V`, if true, remains a genuinely stationary symmetric-flow
inequality, not a repaired statewise Poisson comparison.  Since `L<=S` is
false, this sign is not sufficient for the target `L<=V` and is recorded
only as part of the exact cancellation anatomy.

On the two frozen rational witnesses,

\[
\begin{array}{c|ccc}
 &\mathcal L&\mathcal S&\mathcal V\\ \hline
\text{path }(1,2)&2/135&1/45&8/135\\
\text{regular weighted }K_4&207/22960&207/22960&247/22960.
\end{array}                                                     \tag{18}
\]

## 5. Likelihood/Fisher identity and the nonclosing scalar bound

Although `Q` is nonreversible, its balanced directed flow gives the exact
nonnegative entropy dissipation

\[
 I_K(g):=-\langle g,Q\log g\rangle_{\pi_K}
 =\sum_{A\ne B}c_{AB}
 \left[g(A)\log{g(A)\over g(B)}-g(A)+g(B)\right]\ge0.          \tag{19}
\]

Stationarity under `Q_P` gives independently

\[
 I_K(g)=E_\pi[(Q_P-Q)\log g].                    \tag{20}
\]

The sharp scalar edgewise Fenchel inequality yields, for every `lambda>0`,

\[
 \mathcal L\le {1\over\lambda}\left\{
 I_K(g)+\sum_{A\ne B}c_{AB}g(B)
 (e^{\lambda(\psi(B)-\psi(A))}-1)\right\}.       \tag{21}
\]

This is the direct relative-entropy/Fisher route.  High-precision
minimization on the path gives a best ratio of approximately `1.01745`
between the right side of (17) and `V`; the regular weighted `K_4` gives
approximately `0.84554`.  Thus the scalar bound does not close even on the
path.  These two minimizations are marked **NUMERICALLY OBSERVED**; all
Markov, Poisson, and rational identities surrounding them are exact.

## 6. Verification

Run

```text
python3 verify_fisher_route.py
```

The verifier independently constructs both subset generators and stationary
laws over exact rationals, checks (5)--(9), checks the exact entries in
(15), (17), and (18), verifies the entropy identities to 65 decimal places, and
screens the scalar Fenchel bound.  `search_symmetric_split.py` is explicitly
a floating-point hostile-search program and is not a proof certificate.
