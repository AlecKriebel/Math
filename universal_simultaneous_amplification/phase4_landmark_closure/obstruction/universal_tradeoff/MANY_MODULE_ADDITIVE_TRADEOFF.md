# Additive `1/n` budgets for many weak complete modules

Date: 2026-08-02 (America/Los_Angeles)

## Status and scope

The results below are **PROVED**.

* For an arbitrary number of weakly coupled complete modules on any connected
  weighted macrograph, there is an exact additive local-budget / global-charge
  identity.  It excludes dB amplification whenever every module size
  diverges.
* For a star macrograph with one growing core and arbitrarily many
  heterogeneous satellites, a new scalar tradeoff makes the argument fully
  additive: at every fixed `r>sqrt(2)`, eventual dB amplification forces a Bd
  deficit of order at least `q_n/n`, where `q_n` is the number of satellites.

This is a broad **class obstruction**, not a universal obstruction.  It does
not by itself improve the known universal upper bound on `R_sim`.  The exact
nonadditive obstacle for general macrographs is stated in Section 7.

## 1. Arbitrary weighted macrograph

Let modules `H_1,...,H_q` be complete graphs of sizes `m_1,...,m_q>=2`,
with

\[
 n=\sum_{j=1}^q m_j.
 \tag{1}
\]

Every internal edge of module `j` has weight
`alpha_j/(m_j-1)`, so its internal weighted degree is the arbitrary positive
number `alpha_j`.
Between modules `i,j`, distribute a symmetric positive total conductance
`epsilon*c_ij` over all cross edges, where `(c_ij)` is any connected weighted
macrograph.  Take a separated weak-cut limit: every module absorbs internally
before another cross event.  Let `p_(U,j)` be the fixation probability of the
resulting homogeneous-module macro chain when only module `j` is mutant.

For fixed `r>1`, put `a_r=1-1/r` and

\[
 \mathcal B_k=\frac{k}{1-r^{-k}},\qquad
 \mathcal D_k=\frac{k-1}{1-r^{1-k}}.
 \tag{2}
\]

Uniform singleton initialization first fixes locally in module `j`, then
fixes in the macro chain with probability `p_(U,j)`.  Therefore

\[
 \rho_{\rm Bd}^0(G,r)=\frac{a_r}{n}
 \sum_j\mathcal B_{m_j}p_{{\rm B},j},
 \qquad
 \rho_{\rm dB}^0(G,r)=\frac{a_r}{n}
 \sum_j\mathcal D_{m_j}p_{{\rm D},j}.
 \tag{3}
\]

Define

\[
 E_U=\sum_j\mathcal U_{m_j}-\mathcal U_n,
 \qquad
 L_U=\sum_j\mathcal U_{m_j}(1-p_{U,j}),
 \tag{4}
\]

where `U=B,D`.  Then exactly

\[
 \boxed{
 \frac n{a_r}\{\rho_U^0(G,r)-\rho_U(K_n,r)\}=E_U-L_U,}
 \tag{5}
\]

with `L_U>=0`.  Thus the local budget is additive, while every difficulty is
concentrated in the macro failure charge.

For dB, write

\[
 e_k=\frac{k-1}{r^{k-1}-1},\qquad
 \mathcal D_k=(k-1)+e_k.
 \tag{6}
\]

The dB budget has the particularly transparent form

\[
 \boxed{E_D=1-q+\sum_{j=1}^qe_{m_j}-e_n.}
 \tag{7}
\]

This is the exact finite-size tax: every additional internally equilibrated
module costs one unit, before macro failures are charged.

## 2. Arbitrarily many mesoscopic modules

### Theorem 1

Suppose `q_n>=2`, the separated weak-cut description above applies, and

\[
 s_n:=\min_jm_{n,j}\longrightarrow\infty.
 \tag{8}
\]

On any connected weighted macrograph and with arbitrary internal degree
scales, the exact separated-limit probabilities satisfy

\[
 \boxed{
 \rho_{\rm dB}^0(G_n,r)-\rho_{\rm dB}(K_n,r)
 \le-\frac{a_r}{n}\{q_n-1-o(q_n)\}.}
 \tag{9}
\]

Hence an all-mesoscopic weak-module decomposition is eventually
dB-suppressing.

#### Proof

For fixed `r>1`, `sup_(k>=s)e_k->0` as `s->infinity`.  Equation (7) gives

\[
 E_D\le1-q_n+q_n\sup_{k\ge s_n}e_k
 =-(q_n-1)+o(q_n).
\]

Now use `L_D>=0` in (5).  For actual positive cross weights, the same
conclusion holds provided

\[
 \rho_{\rm dB}(G_n,r)-\rho_{\rm dB}^0(G_n,r)=o(q_n/n).
\]

Such a positive diagonal can always be chosen after the finite parameters at
stage `n` are fixed.  QED.

This theorem allows `q_n` to grow and imposes no module-proportion condition.

## 3. Star macrographs and the unique-gate bound

Now take a star.  Its core `C` is a complete module of size `M`; satellite
`j` is a complete module of size `k_j>=2`.  There are no satellite--satellite
edges.  Let

\[
 \sigma_j=\frac{\alpha_C}{\alpha_j}
 \tag{10}
\]

be the core-to-satellite internal degree ratio.  Assume

\[
 M\longrightarrow\infty,\qquad
 \max_j\frac{k_j}{M}\longrightarrow0.
 \tag{11}
\]

The satellite count `q=q_n` and the total satellite population may be
arbitrary.  We require the positive cross weights to be separated enough
that the fixation error is `o(q/n)`; this can always be achieved after the
finite module parameters are fixed.

If satellite `j` is the only mutant module, global fixation must first pass
through the unique gate in which that satellite establishes a mutant core
before being lost.  Thus its global macro success probability is at most the
two-module gate probability.

Put

\[
 C_{k,r}=\frac{k}{k-1}r(r^{k-1}-1),
 \qquad
 s_{k,r}=\frac{r(k-r^{k-1})}{k-1}.
 \tag{12}
\]

Here are the gate odds directly from the update rules.  With a mutant
satellite of size `k` and a resident core of size `M`, the Bd ratio of raw
favorable to adverse introductions is `r*sigma`: the common total cross
conductance cancels, and the two dispersal denominators tend to `alpha_j`
and `alpha_C`.  The dB raw ratio is `r^2/sigma`: in the favorable event the
mutant competes through the core denominator `alpha_C`, whereas in the
adverse event a resident competes through the mutant-satellite denominator
`r*alpha_j`.  Multiplying these raw ratios by the respective probabilities
that the introduced type fixes locally gives the exact finite-`M` odds

\[
 Z_{\rm B}^{(M,k)}
 =\sigma r^M\frac{r^k-1}{r^M-1},
 \tag{13a}
\]

\[
 Z_{\rm D}^{(M,k)}
 =\frac1\sigma\frac{k(M-1)}{M(k-1)}
 r^M\frac{r^{k-1}-1}{r^{M-1}-1}.
 \tag{13b}
\]

These formulas use only the one-dimensional internal clique chains: after a
favorable introduction the success factors are `rho_U(K_M,r)`, and after an
adverse introduction they are `rho_U(K_k,1/r)`.  Thus the successful
favorable-to-adverse gate odds are, uniformly in every positive `sigma` under
(11),

\[
 Z_{{\rm B},j}=\sigma_j(r^{k_j}-1)\{1+o(1)\},
 \qquad
 Z_{{\rm D},j}=\frac{C_{k_j,r}}{\sigma_j}\{1+o(1)\}.
 \tag{13c}
\]

Allowing fixation with probability one after the core gate can only increase
the true fixation probability.  Allowing a locally mutant core to fix
globally with probability one is also an upper bound.  After subtracting the
complete baseline, the resulting satellite contributions are

\[
 \boxed{
 b_{k,r}(\sigma)
 =\frac{k(\sigma-1)}{1+\sigma(r^k-1)},}
 \tag{14}
\]

\[
 \boxed{
 d_{k,r}(\sigma)
 =\frac{k(s_{k,r}-\sigma)}{\sigma+C_{k,r}}.}
 \tag{15}
\]

More precisely, for a positive diagonal coupling satisfying

\[
 \rho_U(G_n,r)-\rho_U^0(G_n,r)=o(q_n/n),
 \qquad U\in\{{\rm Bd},{\rm dB}\},
 \tag{15a}
\]

we have

\[
 \frac n{a_r}\{\rho_{\rm Bd}(G_n,r)-\rho_{\rm Bd}(K_n,r)\}
 \le\sum_{j=1}^{q_n}b_{k_j,r}(\sigma_j)+o(q_n),
 \tag{16}
\]

\[
 \frac n{a_r}\{\rho_{\rm dB}(G_n,r)-\rho_{\rm dB}(K_n,r)\}
 \le\sum_{j=1}^{q_n}d_{k_j,r}(\sigma_j)+o(q_n).
 \tag{17}
\]

To see the bookkeeping, the core contribution is bounded by
`U_M`, while the complete baseline is `U_n`.  Their linear parts differ by
`-sum_j k_j`.  Adding the gate-bounded satellite terms produces (14)--(15).
The exponentially small remainders from `U_M-U_n`, the uniform estimate
`Z_B^(M,k)/Z_B=1+O(r^-M)`, and
`Z_D^(M,k)/Z_D=1+O(M^-1+r^(1-M))` give an aggregate
`O(sum_j k_j/M)=o(q_n)` gate error.  Together with (15a), these give the
displayed remainders.

For completeness, the uniformity in `k` and `sigma` is as follows.  If
`p(z)=z/(1+z)`, then for every multiplier `c` in a fixed neighborhood of
one,

\[
 \sup_{z>0}|p(cz)-p(z)|=O(|c-1|).
 \tag{17a}
\]

The two exact-to-limit odds multipliers are

\[
 c_B(M)=\frac1{1-r^{-M}},\qquad
 c_D(M)=\frac{1-M^{-1}}{1-r^{1-M}},
 \tag{17b}
\]

which are independent of `k` and `sigma`.  Also, uniformly for `k>=2`,

\[
 \mathcal B_k\le \frac{k}{1-r^{-2}},\qquad
 \mathcal D_k\le \frac{k}{1-r^{-1}}.
 \tag{17c}
\]

Hence the total gate-probability error after multiplication by the local
budgets is

\[
 O_r\!\left((M^{-1}+r^{1-M})\sum_jk_j\right)
 =O_r\!\left(\sum_j\frac{k_j}{M}\right)
 \le O_r\!\left(q_n\max_j\frac{k_j}{M}\right)
 =o(q_n).
 \tag{17d}
\]

Finally, writing `B_s=s+g_s` and `D_s=s-1+e_s`, both `g_s,e_s` tend to
zero exponentially.  Thus the non-linear remainder in `U_M-U_n` is `o(1)`,
hence `o(q_n)` because `q_n>=1`.  This proves the claimed remainder even
when `q_n` stays bounded and when the satellite sizes vary with `n`.

## 4. Sharp additive scalar lemma

### Lemma 2

For every `r>sqrt(2)`, every integer `k>=2`, and every `sigma>0`,

\[
 \boxed{b_{k,r}(\sigma)+d_{k,r}(\sigma)<0.}
 \tag{18}
\]

Moreover there is a constant `delta_r>0`, depending only on `r`, such that

\[
 b_{k,r}(\sigma)+d_{k,r}(\sigma)\le-\delta_r
 \tag{19}
\]

uniformly in `k>=2` and `sigma>0`.

#### Proof

Write `t=r^k`, `D=t-1`, `C=C_(k,r)`, and `s=s_(k,r)`.  Two direct identities
are

\[
 C+s=t,
 \qquad
 1-s=\frac{r^k-kr+k-1}{k-1}>0,
 \tag{20}
\]

where the last inequality is strict convexity of `r^k` at `r=1`.
Differentiating the sum `f=b+d` gives

\[
 f'(\sigma)=kt\left{
 \frac1{(1+D\sigma)^2}-\frac1{(\sigma+C)^2}
 \right}.
 \tag{21}
\]

Since `r>sqrt(2)` and `k>=2`, `t>2`.  Also `C>1`: for `k=2` this follows
from `2r(r-1)>1`, while for `k>=3` we have `r^(k-1)>2` and hence
`C>r>1`.  Therefore `f` has a unique maximum at

\[
 \sigma_0=\frac{C-1}{t-2}>0,
 \]

where `1+D*sigma_0=sigma_0+C`.  At that point

\[
 f(\sigma_0)
 =\frac{k(s-1)}{1+D\sigma_0}<0.
 \tag{22}
\]

This proves (18).  Its positive deficit is explicitly

\[
 \delta_{k,r}
 =\frac{k(1-s_{k,r})(r^k-2)}
 {(r^k-1)C_{k,r}-1}.
 \tag{23}
\]

For fixed `r`, `delta_(k,r)->1` as `k->infinity`.  Every finite term is
positive, so

\[
 \delta_r:=\inf_{k\ge2}\delta_{k,r}>0.
 \]

This proves (19).  QED.

The threshold is sharp for this coefficient-one scalar lemma.  If
`1<r<sqrt(2)`, then at `k=2`

\[
 \lim_{\sigma\to\infty}\{b_{2,r}(\sigma)+d_{2,r}(\sigma)\}
 =\frac{2(2-r^2)}{r^2-1}>0.
\]

At `r=sqrt(2)` the limit is zero, so no positive uniform `delta_r` exists.
This sharpness statement concerns Lemma 2, not the full star-amplification
question with other possible multipliers or arguments.

## 5. Additive star obstruction

### Theorem 3

Under the star hypotheses (10)--(11) and (15a), fix `r>sqrt(2)`.  If

\[
 \rho_{\rm dB}(G_n,r)>\rho_{\rm dB}(K_n,r),
 \tag{24}
\]

then

\[
 \boxed{
 \rho_{\rm Bd}(G_n,r)-\rho_{\rm Bd}(K_n,r)
 \le-\frac{a_r\delta_rq_n}{n}+o(q_n/n)<0.}
 \tag{25}
\]

Thus no such star family can simultaneously amplify Bd and dB at that
fitness.

#### Proof

By (17) and strict dB amplification,

\[
 \sum_jd_{k_j,r}(\sigma_j)\ge-o(q_n).
 \]

Summing (19) gives

\[
 \sum_jb_{k_j,r}(\sigma_j)
 \le-\sum_jd_{k_j,r}(\sigma_j)-\delta_rq_n
 \le-\delta_rq_n+o(q_n).
\]

Equation (16) proves (25).  QED.

The theorem allows bounded, growing, and mutually heterogeneous satellites,
provided each remains `o(M)`; their number and total proportion are
unrestricted.

## 6. Consequence for the asymptotic-amplification program

Theorems 1 and 3 exclude two broad multiscale regimes:

1. arbitrary macrographs all of whose modules are mesoscopic;
2. star hierarchies with one asymptotically larger core and any number of
   smaller complete satellites.

The star conclusion uses the actual strict dB-amplification hypothesis and
produces an explicit additive Bd deficit.  Nevertheless it is a class
obstruction only.  Since arbitrary noncomplete modules and general
macrographs remain untreated, it yields **no new universal upper bound on
`R_sim`**.

## 7. Precise nonadditive obstacle beyond stars

Identity (5) holds on every weighted macrograph, but its charge

\[
 L_U=\sum_j\mathcal U_{m_j}(1-p_{U,j})
 \]

contains global fixation probabilities of a `2^q`-state macro chain.  On a
star, a mutant satellite must cross one unique core gate, giving the
modulewise upper bound used in (13)--(17).  On a general tree, and especially
on a graph with cycles, a mutant module may establish along several routes,
return through an already mutant intermediate module, or bypass a locally
adverse edge.  The failure events attached to different cuts are therefore
neither disjoint nor independent.  Summing edgewise product bounds double
counts shared extinction events, while multiplying them undercounts recovery
paths.

Equivalently: the local budgets `E_U` are additive in modules, but the
charges `L_U` are harmonic functions of the entire macro chain and have no
known edge-additive representation.  A full macrograph theorem needs either
a recursive cut decomposition with nonoverlapping stopping events or a
global comparison of the two macro-chain harmonic measures.  The statewise
bound `R_Bd(S)R_dB(S)<=r^3` alone does not supply either property.

## 8. Independent exact certificate

The companion script `verify_many_module_additive_tradeoff.py` uses rational
arithmetic throughout.  It independently:

1. checks (5) for heterogeneous module lists and arbitrary rational macro
   fixation probabilities;
2. reconstructs (13a)--(13b) from the raw Bd and dB introduction rates and
   the internal clique fixation chains;
3. builds the full homogeneous-module macro chain for a core with two
   heterogeneous satellites, checks every successful transition rate, solves
   its absorbing equations by exact Gaussian elimination, and verifies both
   the budget identity and the unique-gate bounds;
4. checks the exact satellite reductions (14)--(15), the maximizing scale
   `sigma_0`, and the deficit formula (23) over a finite exact audit suite;
5. checks representative mesoscopic dB budgets before any macro failure
   charge is subtracted.

Its saved output is `many_module_additive_verification_output.txt`.  The
script is an independent finite symbolic audit; the uniform quantifiers in
Theorems 1 and 3 are proved analytically above, not inferred from the audit.
