# A dilute pair--pendant hybrid crosses fitness three halves

## 1. Result and exact status

Put

\[
 P(R)=R^6-8R^5+22R^4-30R^3+21R^2-6R+1.
\]

The polynomial has a unique root

\[
 R_*=1.5028569127905696267\ldots
\]

in `(3/2,151/100)`.  Define the fixed algebraic constants

\[
 \sigma_*={-R_*^3+4R_*^2-3R_*-1\over2(R_*-1)},
 \qquad
 \lambda_*={2(R_*-1)(1-\sigma_*)
  \over1+\sigma_*(R_*^2-1)}.                       \tag{1}
\]

Numerically these are

\[
 \sigma_*=0.13067728228704837\ldots,
 \qquad \lambda_*=0.75080648303188049\ldots .      \tag{2}
\]

**Theorem.**  There is one fitness-independent family of finite connected
undirected weighted graphs which eventually amplifies every fixed
`1<r<R_*` under both Bd and dB updating.  Consequently

\[
                         R_{\rm sim}\ge R_*>\frac32. \tag{3}
\]

Within the two-parameter dilute hybrid family below, `R_*` is the exact
largest open fitness threshold.  This does not determine the global value of
`R_sim`.

The exact orbit lumping, finite positive-coupling chain, rare trace,
coefficient identities, and algebraic optimization were independently
reconstructed in this folder.  The only limiting input is the elementary
clique--pendant estimate proved in Section 4 from the displayed transition
rates; the proof controls the post-establishment route to fixation.

## 2. Explicit graph family

For an integer `t>=2`, set

\[
 q_t=t,\qquad m_t=\lfloor\lambda_*t\rfloor,
 \qquad C_t=t^4,
 \qquad n_t=C_t+m_t+2q_t.                              \tag{4}
\]

The graph contains:

1. a unit-weight clique on `C_t` vertices, with one distinguished hub;
2. `m_t` unit-weight pendant vertices adjacent only to the hub;
3. `q_t` disjoint two-vertex satellites;
4. an internal edge of weight `C_t/sigma_*` in every satellite;
5. an edge of weight

   \[
       \epsilon_t=2^{-2^{n_t^4}}                       \tag{5}
   \]

   from every satellite vertex to every clique vertex.

There are no other edges.  Every displayed weight is positive algebraic and
independent of fitness.  The weak bundles make the graph connected.  Notice
that the degree-one population has proportion `m_t/n_t -> 0`, while every
satellite has clique support degree `C_t`; this is not a repeated
bounded-support construction.

For a completely rational, slightly weaker statement one may instead use

\[
 \sigma={19\over137},\qquad q_t=27t,\qquad m_t=20t.    \tag{6}
\]

That family has exact threshold

\[
 R_{\mathbb Q}={5069+12\sqrt{147001}\over6439}
 =1.50176815223369\ldots>\frac32.                       \tag{7}
\]

## 3. Exact finite lumping

At positive `epsilon_t`, a mutant configuration has orbit label

\[
 (h,i,u,v,l).                                           \tag{8}
\]

Here `h` is the hub bit, `i` is the number of mutant ordinary clique
vertices, `u,v` count mixed and all-mutant satellite pairs, and `l` is the
mutant pendant count.  The acting group is

\[
 S_{C_t-1}\times(S_2\wr S_{q_t})\times S_{m_t}.
\]

Both update kernels commute with this action, so (8) is a strong orbit
lumping.  `hybrid_pair_pendant_search.py` lists the ten possible coordinate
changes directly from the update rules.  `verify_hybrid_lumping.py` is an
independent exact audit: on a nine-vertex instance it enumerates every one
of the 512 labelled configurations, aggregates every Bd source--target and
dB death--parent event over `QQ`, and matches all 108 orbit fibres.

## 4. The center-module estimates

Let `H_(C,m)` be the unit clique `K_C` with `m` unit hub pendants.  Assume

\[
             m\longrightarrow\infty,qquad m/C\longrightarrow0,             \tag{9}
\]

and fix `r>1`.  Write `p=1-1/r`.  Directly from the three-coordinate
`(h,i,l)` rates one obtains, for either rule,

\[
 u_{\rm core}(r)=p+O_r(C^{-1}),                          \tag{10}
\]

uniformly for a hub or ordinary clique start after averaging over the
`C` clique vertices.  For a pendant start,

\[
 u_{\rm leaf}^{Bd}(r)=1-O_r(m/C+m^{-1}),
 \qquad
 u_{\rm leaf}^{dB}(r)=O_r(C^{-1}).                       \tag{11}
\]

Consequently the uniformly initialized center-module probabilities satisfy

\[
 a_H^{Bd}(r)
 ={Cp+m\over C+m}+o_r(m/C),
 \qquad
 a_H^{dB}(r)
 ={Cp\over C+m}+o_r(m/C).                               \tag{12}
\]

The portal quantities, where only clique vertices are incident with weak
satellite edges, are

\[
 I_{\rm core}=1+{1\over C-1+m}=1+o(1),                  \tag{13}
\]

and

\[
 J_{\rm core}(r)=p+o(1).                                \tag{14}
\]

At reciprocal fitness, both the portal-uniform fixation probability and
`J_core(1/r)` are `exp(-Omega_r(C))`.

Here is a proof that includes the establishment-to-fixation step.  Stop the
ordinary clique mutant count on first reaching zero or a cutoff `K` with
`K->infinity`, `K=o(C)`.  Until this time the two opposing clique-change
rates, under either update rule, are

\[
                  ri\{1+O_r(K/C)\},\qquad
                  i\{1+O_r(K/C)\}.                       \tag{15}
\]

Hub excursions contribute only `O_r(K/C)` to a stopped finite family; a
pendant created during such an excursion returns through the same hub and
does not change the limiting offspring law.  Truncate first at fixed `K`
and then let `K` grow.  The linear birth--death extinction calculation gives
`p`, with an `O_r(C^-1)` averaged error.  Starting from `K` core mutants, the
same rate ratio is bounded above one until a fixed positive core density is
reached.  In the upper strip the resident deficit is dominated by a
subcritical linear birth--death chain.  Recurrent mutant-hub intervals then
fill all pendants: under dB every pendant copies the hub at its next death;
under Bd the hub-occupation renewal ratio for mutant versus resident pendant
changes tends to `r^2>1`.  Thus reaching `K` leads to full fixation with
probability `1-o(1)`, not merely to branching survival.

For a single Bd mutant pendant, hub activations occur at order-one rate.
During each short activated excursion, a successful clique family is marked
at order `1/m`, whereas pendant extinction is at order `1/C`; the ratio is
`C/m->infinity`.  Multiple productive events in one excursion and the
finite-family return time contribute `O_r(m/C+m^-1)`.  This proves the first
part of (11).  Under dB the mutant pendant dies at rate one after the common
death-clock time change, while hub activation is `O_r(C^-1)`, proving the
second part.  Reversing fitness makes (15) uniformly subcritical; reaching a
positive core density, necessary for fixation, has probability
`exp(-Omega_r(C))`.  This proves (10)--(14).

These estimates are also the dilute limit of the independently audited
clique--pendant calculation in `threshold/clique_pendant_asymptotic/`.

## 5. Rare migration and the complete post-establishment trace

First fix `C,m,q` and send the common satellite--clique weight `epsilon` to
zero.  Before another cross event, an invaded module returns to a monomorphic
state with probability tending to one.  The trace state is

\[
 (h,k)\in\{0,1\}\times\{0,\ldots,q\},                   \tag{16}
\]

where `h` is the center-module type and `k` counts mutant satellites.
Failed invasions are self-loops.

For one specified satellite let `A,D,B,C'` denote, respectively, mutant
satellite invasion of a resident center, resident-center recovery of that
satellite, mutant-center invasion of a resident satellite, and
resident-satellite recovery of the center.  The direct update-rule sums are

\[
\begin{array}{c|cccc}
 &A&D&B&C'\\ \hline
 Bd&C r I_P a_{\rm core}(r)
   &2 I_{\rm core}a_P(1/r)
   &2rI_{\rm core}a_P(r)
   &C I_Pa_{\rm core}(1/r)\\[2mm]
 dB&2rJ_{\rm core}(r)
   &{C\over r}J_P(1/r)
   &CrJ_P(r)
   &{2\over r}J_{\rm core}(1/r).
\end{array}                                               \tag{17}
\]

The isolated K2 satellite has internal degree `C/sigma`, hence

\[
 I_P={2\sigma\over C},\quad
 a_P^{Bd}(r)={r\over r+1},\quad
 a_P^{Bd}(1/r)={1\over r+1},\quad
 J_P(r)=J_P(1/r)={\sigma\over C},                         \tag{18}
\]

and its dB singleton establishment is `1/2`.

In (16), the nonzero rates are

\[
 (0,k)\to(1,k):kA,quad (0,k)\to(0,k-1):kD,
\]

\[
 (1,k)\to(1,k+1):(q-k)B,quad
 (1,k)\to(0,k):(q-k)C'.                                  \tag{19}
\]

Equations (17)--(19) control the entire path to absorption.  By (10)--(14),
`qC'/B->0`.  Therefore a mutant center fixes all satellites with probability
`1-o(1)`, and a single established mutant satellite fixes globally with
probability

\[
 \pi_B={\sigma(r^2-1)\over1+\sigma(r^2-1)}+o(1),
 \qquad
 \pi_D={2r(r-1)\over\sigma+2r(r-1)}+o(1).                \tag{20}
\]

This proves post-establishment fixation through the exact absorbing trace;
no independent-genealogy assumption is used.

`hybrid_trace_search.py` solves the center module and (19) independently.
For small instances its answers agree with the full positive-epsilon
five-coordinate chain to between `10^-9` and `10^-13` as epsilon decreases.

## 6. The two simultaneous correction coefficients

Let `eta=q/C` and suppose

\[
 q\to\infty,\qquad q/C\to0,qquad m/q\to\lambda.          \tag{21}
\]

Using (12), (18), and (20), and noting that the finite complete-graph
baseline differs from `p` by `o(eta)`, uniform initialization gives

\[
 {\rho_{Bd}(G,r)\over\rho_{Bd}(K_n,r)}
 =1+\eta\left\{
 {2(\sigma-1)\over1+\sigma(r^2-1)}
 +{\lambda\over r-1}\right\}+o_r(\eta),                 \tag{22}
\]

\[
 {\rho_{dB}(G,r)\over\rho_{dB}(K_n,r)}
 =1+\eta\left\{
 {2\{r(2-r)-\sigma\}\over\sigma+2r(r-1)}
 -\lambda\right\}+o_r(\eta).                           \tag{23}
\]

For example, the pair part of (22) is

\[
 -2+{2\over p}{r\over r+1}\pi_B
 ={2(\sigma-1)\over1+\sigma(r^2-1)},                    \tag{24}
\]

and the pair part of (23) is `-2+pi_D/p`.  The pendant
corrections are `lambda/(r-1)` and `-lambda`.  The exact symbolic verifier
reconstructs (20)--(24).

The explicit diagonal (5) preserves (22)--(23).  Indeed, fixation is a ratio
of nonnegative directed-forest sums in `epsilon`.  After the common lowest
power is removed, coefficient-height and forest-count bounds are at most

\[
 \exp\{2^{O(n_t\log n_t)}\}.
\]

On the compact interval `[1+1/t,t]`, (5) makes the full-chain/trace error
smaller than `o(q_t/C_t)`.  Every fixed `r>1` lies in these compact intervals
eventually.  This is the same cancellation-free diagonal argument used for
the earlier center--triangle construction.

## 7. Exact interval and optimization

Define

\[
 L(r,\sigma)={2(r-1)(1-\sigma)\over1+\sigma(r^2-1)},
 \qquad
 U(r,\sigma)={2\{r(2-r)-\sigma\}\over
                    \sigma+2r(r-1)}.                     \tag{25}
\]

Both leading corrections are positive exactly when

\[
                 L(r,\sigma)<\lambda<U(r,\sigma).          \tag{26}
\]

For fixed `0<sigma<1`, `L` is increasing as long as
`sigma(r-1)^2<1`, while

\[
 {\partial U\over\partial r}
 ={4r(\sigma-r)\over(2r^2-2r+\sigma)^2}<0.               \tag{27}
\]

At the algebraic constants (1), `L(R_*,sigma_*)` and
`U(R_*,sigma_*)` both equal `lambda_*`.  Hence (26) holds strictly for every
`1<r<R_*`; equations (22)--(23) prove eventual strict simultaneous
amplification.

For class-optimality, the numerator of `L-U` is quadratic in `sigma`, with
discriminant

\[
 4r^2P(r).                                                \tag{28}
\]

At `R_*` the two admissible roots merge at `sigma_*`; immediately above it
the discriminant is negative and (26) is impossible for any positive
`sigma,lambda`.  Thus `R_*` is the exact threshold of this dilute hybrid
ansatz.  For the fixed optimized family, `U(r,sigma_*)<lambda_*` for every
`r>R_*`, so it is eventually dB-suppressing there.

The rational parameters (6) give, exactly at `r=3/2`,

\[
 G_B={232\over17361}>0,
 \qquad G_D={65\over12123}>0.                             \tag{29}
\]

Their dB coefficient first vanishes at (7), while the Bd coefficient remains
positive, proving the stated rational-family threshold.

## 8. Verification

From the repository root:

```text
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_construction_v2/verify_hybrid_lumping.py
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_construction_v2/verify_hybrid_coefficients.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_construction_v2/hybrid_trace_search.py --core 1000 --pairs 27 --pendants 20 --sigma 0.1386861313868613
```

The first two commands are exact certificates.  The final command is a
finite trace diagnostic and is not used as proof.
