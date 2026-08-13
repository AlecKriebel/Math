# Root termination versus diffuse adjoint branching

Date: 2026-08-13 (America/Los_Angeles)

No graph search, literature search, or external communication was used.

## 1. Status

**PROVED CONDITIONAL REDUCTION AND PRECISE OBSTRUCTION.**  Let

\[
 r=R_{\rm hyb},\qquad a=r-1,\qquad p_0={r-1\over r}.
\]

Assume a hypothetical endpoint sequence, with `n_k->infinity`, has
normalized gains

\[
 \Delta_{B,k}>0,\qquad \Delta_{D,k}>0,\qquad
 \epsilon_k=\max\{\Delta_{B,k},\Delta_{D,k}\}.
 \tag{1}
\]

The paired Schur-trace theorem says that every physical peeling which
reaches the nonseparated root leaves `D+aB` charge at least
`(r-1)epsilon_k-o(epsilon_k)` in its controlled-error form.  The theorem
below identifies exactly what that root can be.

For each population cutoff `2<=K<=n`, couple the finite Moran process to its
whole-graph linear branching process until extinction, population `K`, or
the first collision/nonlinear event.  There are two exact nonnegative
errors:

1. `chi_U(K)`, the probability of a collision/nonlinear coupling failure;
2. `theta_U(K)`, the probability that the branching process reaches `K`
   and nevertheless later becomes extinct.

The resulting aggregate cutoff implication is the following.  If some
cutoff sequence makes

\[
 {1\over n_k}+\sum_{U\in\{B,D\}}
       \{\chi_{U,k}(K_k)+\theta_{U,k}(K_k)\}
 =o(\epsilon_k),                                        \tag{2}
\]

then the finite reversible adjoint branching kernels of the graphs satisfy

\[
 \boxed{
 \left(\bar s_k-p_0\right)
   +(r-1)\left(\bar b_k-p_0\right)>0}                    \tag{3}
\]

and, eventually, the left side of (3) is at least

\[
                         { (r-1)p_0\over4}\epsilon_k.     \tag{3a}
\]

Here `bar b_k` and `bar s_k` are the uniformly averaged Bd and dB branching
survival probabilities.  If no cutoff sequence makes (2) hold, the
three-term aggregate obstruction remains.  These conclusions are not
asserted to be mutually exclusive.

Consequently the one diffuse inequality

\[
 \boxed{
 \left(\bar s-p_0\right)
   +(r-1)\left(\bar b-p_0\right)\leq0}                   \tag{DA}
\]

for every finite undirected-realizable adjoint branching kernel at
`r=R_hyb` closes the root branch whenever (2) holds.  The exact support
identity already stored in
`lower_global_tradeoff/R_DEPENDENT_DIFFUSE_SUPPORT_IDENTITY.md` reduces
`(DA)` to one constrained ground-energy sign plus a manifest square.

Thus average diffuseness and average isothermality do not by themselves
prove root exhaustion.  The precise missing uniformity is the ability to
make the aggregate in (2) little-oh of the response: it contains a
response-weighted killed-Green collision/metastability budget together with
the finite-population `1/n` layer.  This is a theorem-level obstruction, not
a request for a larger graph search.

## 2. Whole-graph adjoint branching pair

Let `G` be a connected loopless undirected weighted graph of order `n`,
with

\[
 d_i=\sum_jw_{ij},\qquad P_{ij}={w_{ij}\over d_i},\qquad
 t_i=\sum_jP_{ji}.                                      \tag{4}
\]

The Bd branching process is the continuous-time particle process in which
a particle at `i`

\[
 i\longrightarrow i+j\quad\hbox{at rate }rP_{ij},
 \qquad i\longrightarrow\varnothing\quad\hbox{at rate }t_i. \tag{5}
\]

Here `i -> i+j` means that the parent at `i` remains and one child of type
`j` is added.  The clock normalization is the exact Bd Moran
state-time normalization: every resident has a reproduction clock of rate
one and every mutant a clock of rate `r`, after which its target is sampled
from its row of `P`.  Dividing all outgoing rates at a mutant set `S` by
`n+(r-1)|S|` recovers the usual discrete-time Bd transition probabilities,
so this Poissonization preserves every hitting probability.

The dB branching process has

\[
 i\longrightarrow i+j\quad\hbox{at rate }rP_{ji},
 \qquad i\longrightarrow\varnothing\quad\hbox{at rate }1.   \tag{6}
\]

For dB, every target has a death clock of rate one.  The two rules therefore
use their own standard state-time normalizations; no comparison of their
absolute clock speeds is used.

Their survival vectors are the unique strictly positive solutions

\[
 t_i b_i=r(1-b_i)(Pb)_i,\qquad
 s_i=r(1-s_i)(P^Ts)_i.                                  \tag{7}
\]

Put

\[
                         \bar b={1\over n}\sum_i b_i,
 \qquad                  \bar s={1\over n}\sum_i s_i.   \tag{8}
\]

This pair is not an ansatz.  It is the exact linearization of the two Moran
generators at the all-resident state.

It is also exactly the undirected-realizable normal form used in `(DA)`.
Indeed, `P` is reversible with respect to

\[
 \pi_i={d_i\over\sum_jd_j}.
\]

Set

\[
 \alpha_i={\sum_jd_j\over nd_i},\qquad
 p_i=\pi_i\alpha_i={1\over n}.
\]

Then

\[
 D_\alpha^{-1}PD_\alpha=P^T,qquad
 {P\alpha\over\alpha}=t.                               \tag{9}
\]

Thus (7) is precisely the reversible-kernel/adjoint pair with uniform
physical initialization.  No compactness or fixed type number is required:
the desired inequality `(DA)` can be applied stage by stage.

## 3. Exact collision and nonlinear defect rates

For a simple particle configuration `S`, write

\[
 x_j(S)=\sum_{i\in S}P_{ji},\qquad
 I(S)=\sum_{i,j\in S}P_{ij}.                             \tag{10}
\]

For Bd, couple every birth onto a resident vertex and every death caused by
a resident parent.  The unmatched branching clocks are births onto an
occupied vertex and deaths suppressed by a mutant parent.  Their total rate
is exactly

\[
                         \delta_B(S)=(r+1)I(S).          \tag{11}
\]

For dB, the physical addition and loss rates are

\[
 q_j^+(S)={r x_j(S)\over1+(r-1)x_j(S)}\quad(j\notin S),
\]

\[
 q_i^-(S)={1-x_i(S)\over1+(r-1)x_i(S)}\quad(i\in S).    \tag{12}
\]

Both are at most their branching counterparts `r x_j(S)` and `1`.
Maximal thinning therefore gives the exact unmatched rate

\[
\begin{aligned}
 \delta_D(S)
 &=rI(S)
   +\sum_{i\in S}{r x_i(S)\over1+(r-1)x_i(S)}\\
 &\quad+
   \sum_{j\notin S}{r(r-1)x_j(S)^2\over1+(r-1)x_j(S)}.  \tag{13}
\end{aligned}
\]

In particular,

\[
 \delta_D(S)\leq2rI(S)+r(r-1)\sum_jx_j(S)^2.            \tag{14}
\]

Equations (11)--(13) contain every same-site collision and every nonlinear
fitness denominator; no informal independence approximation is being made.

Let `C_U^(K)` be the substochastic generator on simple sets
`1<=|S|<=K-1` obtained from the common clocks in the maximal coupling,
killing on extinction, arrival at `K`, or an unmatched clock.  Let

\[
 G_U^{(K)}=(-C_U^{(K)})^{-1}                             \tag{15}
\]

be its killed Green kernel and let `ell` put mass `1/n` on every singleton.
Standard absorption accounting gives the exact formula

\[
 \boxed{
 \chi_U(K)=\ell^TG_U^{(K)}\delta_U.}                    \tag{16}
\]

This is the response-weighted quantity which a valid diffuse reduction has
to control.  It is the whole-graph analogue of `incoming load x killed
Green x exit rate` in the paired Schur trace.

If `H_U^{phys}(K)` and `H_U^{br}(K)` are the uniform probabilities of
hitting population `K` before zero, then the coupling gives

\[
             |H_U^{phys}(K)-H_U^{br}(K)|\leq\chi_U(K).  \tag{17}
\]

Let

\[
 \theta_U(K)=H_U^{br}(K)-\bar u_U\geq0,
 \qquad \bar u_B=\bar b,\quad\bar u_D=\bar s.           \tag{18}
\]

The equality between survival and the decreasing limit of hitting
probabilities uses two facts.  The finite-type linear branching process is
nonexplosive, and, for every fixed `K`, its count chain killed on total
population zero or `K` has a finite interior state space.  From every
interior state a finite sequence of deaths reaches zero with positive
probability, uniformly over that finite state space.  Hence the killed chain
hits zero or `K` almost surely.  It follows that a nonextinct trajectory
cannot remain forever in a finite population band: survival is exactly
unbounded growth, equivalently the intersection over `K` of the events of
hitting `K`.  Therefore `H_U^{br}(K)` decreases to `bar u_U`.  Since
fixation must hit every `K`, (17)--(18) imply

\[
 \boxed{
 \rho_U(G,r)\leq \bar u_U+\theta_U(K)+\chi_U(K).}        \tag{19}
\]

## 4. Quantitative root-to-diffuse theorem

Write the two complete-graph baselines as

\[
 \kappa_B(n)={p_0\over1-r^{-n}},
 \qquad
 \kappa_D(n)=p_0{n-1\over n}{1\over1-r^{-(n-1)}}.      \tag{20}
\]

Suppose

\[
 \rho_B(G_k,r)=\kappa_B(n_k)(1+\Delta_{B,k}),\qquad
 \rho_D(G_k,r)=\kappa_D(n_k)(1+\Delta_{D,k}),           \tag{21}
\]

with (1).  Put

\[
 e_{U,k}(K)=\theta_{U,k}(K)+\chi_{U,k}(K).              \tag{22}
\]

Equation (19) gives

\[
\begin{aligned}
 &(\bar s_k-p_0)+a(\bar b_k-p_0)\\
 &\quad\geq
   \kappa_D\Delta_{D,k}+a\kappa_B\Delta_{B,k}
  +(\kappa_D-p_0)+a(\kappa_B-p_0)
  -e_{D,k}(K)-a e_{B,k}(K).                             \tag{23}
\end{aligned}
\]

For all sufficiently large `n`,

\[
 \kappa_D\Delta_D+a\kappa_B\Delta_B
 \geq {ap_0\over2}\epsilon,                            \tag{24}
\]

because at least one of the two gains equals `epsilon`.  Also

\[
 (\kappa_D-p_0)+a(\kappa_B-p_0)
 \geq-{2p_0\over n}.                                   \tag{25}
\]

Combining (23)--(25) proves

\[
 \boxed{
 (\bar s_k-p_0)+a(\bar b_k-p_0)
 \geq {ap_0\over2}\epsilon_k-{2p_0\over n_k}
      -e_{D,k}(K)-ae_{B,k}(K).}                         \tag{26}
\]

Therefore, if some cutoffs `K_k` satisfy

\[
 {1\over n_k}+e_{D,k}(K_k)+e_{B,k}(K_k)
                         =o(\epsilon_k),                \tag{27}
\]

the root forces the strict diffuse support violation (3).  Conversely, if
`(DA)` is true, (26) supplies the quantitative obstruction

\[
 e_{D,k}(K)+a e_{B,k}(K)+{2p_0\over n_k}
                         \geq {ap_0\over2}\epsilon_k    \tag{28}
\]

for every cutoff `K` and all sufficiently large `k`.

This proves the aggregate cutoff implication without taking a limit of
graph kernels or trace measures.  It is not a mutually exclusive
trichotomy: a positive diffuse charge and a response-scale cutoff error may
coexist.

## 5. What `c(G)->0` and `t->1` do, and do not, supply

Put

\[
 C(G)={1\over n}\sum_{i,j}P_{ji}^2,
 \qquad
 \eta(G)={1\over n}\sum_i|t_i-1|.                      \tag{29}
\]

The inherited all-fitness theorem gives `C(G_k)->0` and `eta(G_k)->0`.
At a uniformly sampled singleton, (13) gives the sharp local estimate

\[
 {1\over n}\sum_i\delta_D(\{i\})
 ={1\over n}\sum_{i,j}
 {r(r-1)P_{ji}^2\over1+(r-1)P_{ji}}
 \leq r(r-1)C(G),                                      \tag{30}
\]

whereas

\[
                         \delta_B(\{i\})=0.             \tag{31}
\]

There is no duplicated defect term in this equality.  For `S={i}`, the
loopless hypothesis gives `I(S)=P_ii=0` and `x_i=P_ii=0`, so the first two
terms of (13) vanish; only its resident nonlinear term remains.  Averaging
that term over `i` gives exactly the double sum in (30).

The temperature conclusion has an equally exact one-generation meaning.
The aggregate Bd child-birth flow generated by a uniform singleton source
has law `t_j/n`, whose total-variation distance from uniform is
`eta(G)/2`.  For dB the aggregate child-birth flow from a uniform source is
exactly uniform, while its parent flow is biased by `t_i`.

These are source-local statements.  Formula (16), not (30), is the error
that matters at the first response scale.  A vanishing hazard can be
multiplied by a diverging killed occupation time, and the occupation law can
concentrate on the `o(n)` temperature outliers.  If one wants to replace
the exact `t` in (7) by the regular value one, the additional necessary
quantity is the response-weighted exposure

\[
 \mathfrak T_U(K)=
 \ell^TG_U^{(K)}\left[S\mapsto
                  \sum_{i\in S}|t_i-1|\right],           \tag{32}
\]

not the unweighted average `eta(G)`.  The adjoint inequality `(DA)` avoids
that unsafe replacement by retaining `t` exactly.

There is also an unavoidable finite-population layer.  Since every row of
a loopless stochastic `P` has at most `n-1` entries,

\[
                         C(G)\geq{1\over n-1}.            \tag{33}
\]

Thus a response with `epsilon=O(1/n)` occurs at the same scale as the first
collision correction and the complete-graph dB finite-size deficit.  A
pure branching limit cannot decide strict amplification on that scale.
The stored balanced sharp-cut example realizes exactly this phenomenon:
`C(G)=Theta(1/n)`, `eta(G)=o(n^{-M})` for every `M`, and its fixation-sum
correction is `Theta(1/n)`.  The example is not a simultaneous amplifier,
but it rigorously proves that the local hypotheses cannot yield
`o(epsilon)` control by themselves.

Accordingly the three-term aggregate obstruction within this reduction is:

1. **atomic scale:** `1/n` is comparable with the response;
2. **Green-amplified collision/nonlinearity:** `chi_U(K)` is comparable
   with the response;
3. **metastable false establishment:** `theta_U(K)` is comparable with the
   response for every collision-safe cutoff.

The last two are the branching-language form of nonseparated root
termination.

## 6. The single diffuse inequality that remains

For the reversible parametrization (9), put

\[
 q=1-b,\quad h=1-s,\quad
 x=b-p_0,\quad u=s-p_0.
\]

The exact identity already proved in
`R_DEPENDENT_DIFFUSE_SUPPORT_IDENTITY.md` is

\[
 T_r:=-\{(\bar s-p_0)+(r-1)(\bar b-p_0)\}
 ={r(r-1)\over4}K_r
 +{r\over r-1}E_p\!\left[
 h\left\{{u\over h}-{r-1\over2}
       \left(Px-{x\over h}\right)\right\}^{\!2}\right], \tag{34}
\]

where

\[
 K_r={4\over r-1}E_p\!\left[{t x^2\over q}\right]
      -E_p\!\left[h\left(Px-{x\over h}\right)^2\right]. \tag{35}
\]

Thus `(DA)` is exactly `T_r>=0`.  Proving the stronger constrained
ground-energy inequality

\[
                             K_{R_{\rm hyb}}\geq0         \tag{36}
\]

for every finite reversible datum is sufficient to close the diffuse branch
of root termination.  If (36) is false but the full right side of (34)
remains nonnegative, `(DA)` still suffices; the true minimal target is the
sign of `T_r`, not the stronger sign of `K_r`.

Combining (28) and (34) leaves a sharply stated global task.  Prove
`T_{R_hyb}>=0` and then rule out the three-term response-scale aggregate in
Section 5, or prove a direct physical inequality charging that aggregate.
No exhaustion of graph spaces is relevant to either step.

## 7. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_bulk_diffuse_reduction/verify_root_to_diffuse_reduction.py
```

The replay uses exact rational arithmetic on both a genuinely nonregular
undirected kernel and a nonuniform weighted-regular kernel.  It independently
reconstructs the two physical subset chains, the two multitype branching
chains, and the killed common-clock Green system; verifies every defect-rate
orientation in (11)--(13), the coupling bound (17), the complete-graph
baselines (20), and the elementary response inequalities (24)--(25).
