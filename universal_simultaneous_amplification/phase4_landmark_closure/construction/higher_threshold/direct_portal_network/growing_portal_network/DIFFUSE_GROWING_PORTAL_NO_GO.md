# Diffuse growing portal networks: an exact mean-field obstruction

Date: 2026-08-08 (America/Los_Angeles)

Status: **PROVED for exchangeable blade incidence and a growing diffuse
regular portal network.  This includes complete portal graphs and
degree-diverging regular expanders.  Fixed-degree portal networks and
portal-dependent incidence remain open.**

No literature search or external contact was used.  The limit below is
derived from the exact labelled portal-subset trace.  Establishment is used
only as an upper bound on fixation.

## 1. Family and scaling

For each `s`, take `s` disjoint unit-weight blade edges and `Q_s` portals,
where

\[
 Q_s\longrightarrow\infty,\qquad {Q_s\over s}\longrightarrow0.   \tag{1}
\]

The portals carry a symmetric weighted graph `h^(Q)` satisfying

\[
 \sum_{b\ne a}h^{(Q)}_{ab}=H>0,
 \qquad
 \epsilon_Q:=\max_{a\ne b}h^{(Q)}_{ab}\longrightarrow0.           \tag{2}
\]

Thus every portal has the same portal-network load `H`, while every
individual portal edge is diffuse.  The complete graph with edge weight
`H/(Q-1)` is the canonical example.  A regular expander of degree
`D_Q->infinity`, with edge weight `H/D_Q`, is another example.

There may be `T_s` blade types.  A type-`t` blade endpoint is joined to
every portal with weight `lambda_t/s`; the incidence is exchangeable across
portal identities.  Let `pi_t` be the blade-type proportions and assume

\[
 B:=2\sum_t\pi_t\lambda_t>0                         \tag{3}
\]

is fixed.  All graph data are independent of fitness.  For a growing number
of types, the usual no-concentration condition
`max_t lambda_t=o(s)` ensures that one portal birth cannot target one blade
with nonvanishing probability.  Put

\[
 d=B+H,qquad f_t={2\pi_t\lambda_t\over B}.            \tag{4}
\]

The `f_t` form the child-type distribution.  The graph is connected when
every represented type has positive incidence.

## 2. Exact complete-portal count chain

For the complete portal graph, the exact labelled subset chain lumps by the
number `k` of mutant portals.  Write `e_Q=H/(Q-1)`.  From the atomic Bd rules,

\[
 L^B_{Q,k}=k\left[B+{(Q-k)e_Q\over d}\right],\qquad
 U^B_{Q,k}=(Q-k){rk e_Q\over d}.                       \tag{5}
\]

Here `L` and `U` are the total rates `k->k-1` and `k->k+1`.  A mutant
portal creates successful blade children at total rate

\[
 \beta_B={r^2B\over(r+1)d}.                            \tag{6}
\]

For dB the exact rates are

\[
L^D_{Q,k}=k\,{B+(Q-k)e_Q\over
                   B+(Q-k)e_Q+r(k-1)e_Q},              \tag{7}
\]

\[
U^D_{Q,k}=(Q-k)\,{rk e_Q\over
                   B+(Q-k-1)e_Q+rk e_Q},               \tag{8}
\]

and each mutant portal creates successful blade children at rate

\[
 \beta_D={rB\over2}.                                  \tag{9}
\]

If `F^U_{Q,k}(z)` is the PGF of the total number of successful blade children
before the portal count next reaches zero, then `F_{Q,0}=1` and

\[
 \{L^U_{Q,k}+U^U_{Q,k}+k\beta_U(1-z)\}F^U_{Q,k}
 =L^U_{Q,k}F^U_{Q,k-1}+U^U_{Q,k}F^U_{Q,k+1}.          \tag{10}
\]

Equation (10) is exact for every finite `Q`; it is not a branching
approximation.

## 3. The correct `Q -> infinity` portal episode

For every fixed `k`, (5), (7), and (8) converge to

\[
 L^B_k=k\delta_B,qquad L^D_k=k\delta_D,qquad
 U^B_k=U^D_k=ku,                                      \tag{11}
\]

where

\[
 \delta_B=B+{H\over d},\qquad \delta_D=1,qquad
 u={rH\over d}.                                       \tag{12}
\]

Thus a portal episode converges to a linear birth--death branching process,
but its two death rates and child-export rates remain update-rule specific.
For a general diffuse regular portal graph, if a mutant set has at most `K`
vertices, its internal portal weight is at most `K^2 epsilon_Q`.  Substitution
in the exact labelled-subset rates gives (11) uniformly below every fixed
portal cutoff.  Hence the same limit holds for all families satisfying (2),
not only complete graphs.

Let `F_U(z)` be the limiting episode PGF begun from one mutant portal.  The
branching first-event equation is

\[
 \{\delta_U+u+\beta_U(1-z)\}F_U(z)
 =\delta_U+uF_U(z)^2,                                 \tag{13}
\]

where the minimal solution in `[0,1]` is selected.  The `F^2` term is
essential: one portal reproduction event leaves two descendant portal
lineages.  A linear establishment or single-portal approximation would give
the wrong limit.

The parent clean blade's death and portal-seeding rates give the exact
limiting lifetime PGFs

\[
 D_B(z)={1\over1+r(r+1)d\{1-F_B(z)\}},                \tag{14}
\]

\[
 D_D(z)={1\over1+{2r^2\over d}\{1-F_D(z)\}}.          \tag{15}
\]

Multiple exchangeable blade types do not change (13)--(15).  Every parent
type has the same lifetime law after cancellation of its factor `lambda_t`,
and every child type is sampled from `f`.  Therefore all coordinates of the
largest survival fixed point are equal, so `sum_t f_t s_t=s`.  This proves
an exact scalar collapse even when `T_s` grows.

### Simultaneous-limit justification

Fix clean-blade and portal cutoffs `K,L`.  Below them, the difference between
the labelled portal rates and (11) is `O(L^2 epsilon_Q)`.  An overlapping
episode occurs at rate `O(KQ_s/s)`, and external intervention during a fast
heterotypic-blade resolution is also `O(Q_s/s)`.  Child collisions are
`O(K max_t lambda_t/s)` under the no-concentration assumption.  The cutoff
chain has finite mean event count, so these errors vanish using (1)--(2).
Letting first `s`, then `L`, and then `K` tend to infinity gives the same
stopped-trace upper bound as in the fixed-portal derivation.  If the limiting
portal branching process survives, it accumulates infinitely many child
marks; this is exactly the minimal-root branch of (13), not a missing mass
term.

Consequently, with `q_U` the smallest fixed point of `D_U`,

\[
 \limsup_{s\to\infty}\rho_B(G_s,r)
 \le {r\over r+1}(1-q_B),\qquad
 \limsup_{s\to\infty}\rho_D(G_s,r)
 \le {1\over2}(1-q_D).                                \tag{16}
\]

## 4. Exact no-overlap theorem

Put `p=1-1/r`.  For `1<r<2`, establishment exceeds `p` precisely when the
extinction root lies below

\[
 q_B^0={1\over r^2},\qquad q_D^0={2-r\over r}.         \tag{17}
\]

Write `X_U=1-F_U(q_U^0)`.  Substituting (17) into (13) shows that `X_U` is
the unique positive root of

\[
 \Phi_U(X)=uX^2+(\delta_U+k_U-u)X-k_U,                \tag{18}
\]

where

\[
 k_B={(r-1)B\over d},\qquad k_D=(r-1)B.              \tag{19}
\]

Equations (14)--(15) say that Bd establishment exceeds `p` exactly when

\[
 X_B>{r-1\over rd},                                   \tag{20}
\]

and dB establishment exceeds `p` exactly when

\[
 X_D>{d(r-1)\over r^2(2-r)}.                          \tag{21}
\]

Direct exact substitution into (18) yields

\[
 \Phi_B\left({r-1\over rd}\right)
 =-{(r-1)^2(d-1)(B^2+BH+H)\over rd^3}.               \tag{22}
\]

Because `Phi_B(0)<0` and it has one positive root, (22) proves

\[
 \text{Bd establishment exceeds }p
 \quad\Longleftrightarrow\quad d>1.                  \tag{23}
\]

For dB, write `x=d-1` and `B=1+x-H`.  The second threshold substitution is

\[
 \Phi_D\left({d(r-1)\over r^2(2-r)}\right)
 ={(r-1)^2P(r,x,H)\over r^3(2-r)^2},                 \tag{24}
\]

where `P` is affine in `H` and has endpoint values

\[
 P(r,x,0)=r(2-r)(1+x)(r^2-r+x),                      \tag{25}
\]

\[
 P(r,x,1+x)=(1+x)\{(r-1)^2+x\}.                     \tag{26}
\]

If `d>=1`, then `x>=0` and positivity of `B` gives `0<H<1+x`.  Both
endpoint values are positive for `1<r<2`; hence the affine interpolation
`P(r,x,H)` is strictly positive.  Therefore dB establishment is strictly
below `p` whenever `d>=1`.

**Theorem (growing diffuse portal no-go).**  Every family satisfying
(1)--(4), with exchangeable incidence across portals, fails simultaneous
amplification for every fixed `r>1`:

- if `d<1`, Bd establishment is strictly below `p`;
- if `d=1`, Bd is at its limiting threshold and dB is strictly below `p`;
- if `d>1`, Bd can exceed `p` but dB is strictly below `p`.

For `r=2`, dB's entrance factor equals `p` but its positive extinction
probability makes its establishment bound strict.  For `r>2`, the entrance
factor `1/2` is already below `p`.

Thus complete portal networks, degree-diverging regular expanders, and an
arbitrary growing collection of exchangeable blade types do not furnish an
Outcome-C construction at `r=31/20`, at `r=3/2`, or at any other beneficial
fitness.

## 5. What remains open

**PROVED:** the exact finite complete-portal count chain, the diffuse
`Q->infinity` episode map, its simultaneous `Q_s=o(s)` stopped-trace limit,
the growing-type scalar collapse, and the no-overlap theorem for every
`r>1`.

**EXACTLY COMPUTED:** the factor (22) and the affine endpoint certificate
(25)--(26).

**FALSIFIED AS A CONSTRUCTION ROUTE:** complete or degree-diverging diffuse
regular portal networks with portal-exchangeable blade incidence.

**OPEN:** fixed-degree portal expanders (where parent and child portals retain
an order-one shared edge), portal-dependent incidence, multiple mesoscopic
portal classes, `Q_s` comparable to `s`, and singular `B,H` scaling.  No
post-establishment fixation theorem was pursued because this bounded cycle
produced no positive establishment lead.
