# An exact finite simultaneous weak amplifier

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. The graph and theorem

Let `G` have two hubs and seven internally disjoint paths of length four
between them.  On every path, give the two hub-adjacent edges weight

\[
                              x={103\over500},              \tag{1}
\]

and the two internal edges weight one.  Thus `G` has

\[
                             n=2+7\cdot3=23                \tag{2}
\]

vertices.  Its degree multiset is

\[
             2\times {721\over500},\qquad
            14\times {603\over500},\qquad 7\times2.       \tag{3}
\]

**Theorem.**  The graph `G` is a strict simultaneous weak amplifier for Bd
and dB updating under uniform initial mutation.  More exactly, if

\[
 \rho_U(G,1+\epsilon)={1\over23}+c_U(G)\epsilon
                         +O(\epsilon^2),                   \tag{4}
\]

then

\[
 c_{Bd}(G)
 ={443330487524299675208486212
   \over926460931665398277422905559},                      \tag{5}
\]

\[
 c_{dB}(G)={284789678\over623264051}.                      \tag{6}
\]

Against the complete-graph coefficients

\[
                    c_{Bd}(K_{23})={11\over23},\qquad
                    c_{dB}(K_{23})={21\over46},            \tag{7}
\]

the two exact excesses are

\[
 \boxed{
 c_{Bd}(G)-c_{Bd}(K_{23})
 ={240476727804846875792249
   \over926460931665398277422905559}>0,}                   \tag{8}
\]

\[
 \boxed{
 c_{dB}(G)-c_{dB}(K_{23})
 ={512179\over1246528102}>0.}                             \tag{9}
\]

For orientation only, these excesses are approximately
`0.000259564887828101` and `0.000410884439089846`.  The
positivity claims use only the integer signs in (8)--(9).

Finite absorbing probabilities are rational functions of fitness in a
neighborhood of one.  Equations (8)--(9) therefore imply that some
`delta>0` exists such that

\[
 \rho_{Bd}(G,r)>\rho_{Bd}(K_{23},r),\qquad
 \rho_{dB}(G,r)>\rho_{dB}(K_{23},r)                       \tag{10}
\]

simultaneously for every `1<r<1+delta`.

## 2. Exact neutral pair proof

For each rule `U`, let `h^U_ij` be the continuous-time neutral meeting time
of the two ancestral lineages.  The backward lineage rates are

\[
 a^{Bd}_{ij}={w_{ij}\over d_j},\qquad
 a^{dB}_{ij}={w_{ij}\over d_i}.                           \tag{11}
\]

On the `binom(23,2)=253` unordered distinct pair states, the exact meeting
system is

\[
 (t_i^U+t_j^U)h^U_{ij}
 =1+\sum_{k\ne j}a^U_{ik}h^U_{kj}
    +\sum_{k\ne i}a^U_{jk}h^U_{ik},                      \tag{12}
\]

with `h_ii=0`.  The graph is connected, so this rational system has a unique
solution.

Put `D=sum_i d_i` and `C=(sum_i 1/d_i)^-1`.  The exact weak coefficients are

\[
 c_{Bd}={2C\over23}\sum_{i<j}{w_{ij}\over d_id_j}h^{Bd}_{ij}, \tag{13}
\]

\[
 c_{dB}={2\over23D}\sum_{i<j}\sum_v
                    {w_{vi}w_{vj}\over d_v}h^{dB}_{ij}.   \tag{14}
\]

Substitution of the unique rational solutions of (12) into (13)--(14)
reduces to (5)--(6).  The replay constructs every rate and every equation
directly from (1), solves over `QQ`, checks the residuals, and verifies all
four rational identities (5)--(9).

There is also a compact exact classification of the endpoint-weight
parameter.  Keep seven arms and replace (1) by an arbitrary `x>0`.  The
pair states have only ten orbits under arm permutations and global
left--right reflection.  Solving the exact ten-state quotient over `Q(x)`
gives

\[
 c_{Bd}(G_x)-{11\over23}={P_B(x)\over
 23(49x^2+249x+4)Q_B(x)},                                 \tag{14a}
\]

where

\[
\begin{aligned}
 P_B(x)={}&180018405x^7+2975072149x^6+13161584556x^5\\
 &+17094630950x^4+2810292145x^3-858773619x^2\\
 &-105248866x-1878120,                                    \tag{14b}
\end{aligned}
\]

\[
 Q_B(x)=1786365x^5+15512608x^4+34819480x^3
        +14633270x^2+1659563x+52170,                       \tag{14c}
\]

and

\[
 c_{dB}(G_x)-{21\over46}
 =-{9576x^2+2473x-924\over46(672x^2+743x+252)}.            \tag{14d}
\]

Every denominator in (14a)--(14d) is positive for `x>0`.  The coefficient
list of `P_B`, read in increasing powers of `x`, has exactly one sign
change.  Since `P_B(0)<0` and its leading coefficient is positive,
Descartes' rule proves that it has a unique positive root `alpha_B`.
The quadratic in (14d) has positive root

\[
                   \alpha_D={-2473+5\sqrt{1660345}\over19152}. \tag{14e}
\]

Consequently the seven-arm theta family is a strict simultaneous weak
amplifier **if and only if**

\[
                         \boxed{\alpha_B<x<\alpha_D}.       \tag{14f}
\]

For orientation,

\[
 \alpha_B=0.205251510881545\ldots,qquad
 \alpha_D=0.207274371262138\ldots.                        \tag{14g}
\]

The rational value `103/500=0.206` lies in this interval by direct exact
substitution: `P_B(103/500)>0` and the quadratic in (14d) is negative
there.  Thus (8)--(9) are an interior exact witness, not a rounded point on
a numerically unresolved boundary.

## 3. Exact refutation of the power midpoint route

The two rules are endpoints of a natural reversible power interpolation:

\[
 a^{(\theta)}_{ij}
 =w_{ij}d_i^{-(1+\theta)/2}d_j^{-(1-\theta)/2},\qquad
 \pi_i^{(\theta)}={d_i^\theta\over Z_\theta}.              \tag{15}
\]

Indeed, `theta=-1` is Bd and `theta=1` is dB.  At `theta=0` the rates are
symmetric and the stationary law is uniform.  If

\[
 N(\theta)=2\sum_i\pi_i^{(\theta)}t_i^{(\theta)}
                          R_i^{(\theta)},                  \tag{16}
\]

then the remeeting identity gives `N(0)=n`.  Moreover,

\[
 c_{Bd}={N(-1)-1\over2n},\qquad
 c_{dB}={N(1)-2\over2n}.                                  \tag{17}
\]

There is a striking common-operator reduction.  On pair states use the
reversible measure `mu_ij=pi_i pi_j` and symmetrize the killed meeting
operator.  All off-diagonal entries become

\[
                         -{w_{ik}\over\sqrt{d_id_k}},       \tag{18}
\]

independently of `theta`; only the diagonal holding rates and source change.
Writing the symmetric operator as `H_theta`, one obtains

\[
 N(\theta)-1=k^TH_\theta^{-1}g_\theta,                    \tag{19}
\]

with the same boundary vector for every `theta`,

\[
 k_{ij}={4w_{ij}\over\sqrt{d_id_j}},\qquad
 (g_\theta)_{ij}={ (d_id_j)^{\theta/2}\over Z_\theta}.     \tag{20}
\]

This reduction suggested the midpoint inequality

\[
                         N(1)+N(-1)\leq2N(0)=2n.           \tag{21}
\]

The exact theta graph refutes it.  From (8)--(9),

\[
 \boxed{
 N(1)+N(-1)-46
 ={33664123156747757687570792981933
  \over1091549703899830447854483854239621}>0.}            \tag{22}
\]

Thus neither operator symmetrization nor the shared boundary vector implies
the needed midpoint concavity.  The obstruction is the coupled change in
the diagonal killing rates and source `g_theta`.

## 4. Consequence for the exact-threshold program

This result settles the previously open finite weak-selection question:
strict simultaneous weak amplifiers do exist.  It does **not** by itself
give an asymptotically universal family or determine `R_sim`.  The graph is
a fixed finite local mechanism, and (10) only supplies an unspecified
neighborhood of neutrality.

What it rules out is a whole class of matching-upper strategies.  No
universal inequality can force one of `N_Bd,N_dB` below `n`, and no atomic
compactness induction can demand that every finite module response vector
avoid the open positive quadrant.  A viable upper proof must retain the
fitness evolution of a positive weak atom and show that it loses one
coordinate before the proposed endpoint, or else control how such atoms
compose across scales.

## 5. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
lower_global_tradeoff/verify_weak_simultaneous_theta.py
```

The replay uses an exact `253 x 253` rational solve for each rule and an
independent symbolic ten-orbit solve for (14a)--(14f).  No floating-point
value enters the proof.
