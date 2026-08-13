# Homogeneous two-carrier and dyadic activation with every lower support

**Proof-first standalone theorem, 2026-08-12 PDT.**  This note proves the
all-clock activation-or-ledger macro for the first two symbolic kernels at a
top-dead homogeneous pure vertex.  It covers every optional top support
compatible with the rank-two hypothesis, every lower support of two or three
unaries, every strong labelled orientation, and every fixed positive rate
vector.  It does not enumerate orientations, paths, populations, or rate
regimes.

After relabelling the dead bulk vertex as \(X\), write \(Y,Z\) for the two
transverse species.  The upper support \(T\) is a strongly connected subset
of the homogeneous quadratic shell, \(2X\notin T\), and

\[
                         \dim\operatorname{span}(T-T)=2.
                                                               \tag{0.1}
\]

The two kernels are:

1. **two carrier:** \(X+Y,X+Z\in T\);
2. **dyadic:** \(T=\{X+Y,2Z\}\cup Q\), where
   \(\varnothing\ne Q\subseteq\{Y+Z,2Y\}\), and \(X+Z\notin T\).

Thus the carrier kernel has at least one vertex outside
\(\{X+Y,X+Z\}\), and the three possible dyadic supports are exactly
\(\{X+Y,2Z,Y+Z\}\), \(\{X+Y,2Z,2Y\}\), and their union.  The rank-one
support \(\{X+Y,2Z\}\) is not in the theorem.

The lower linkage is \(R=\{0\}\cup U\), where \(U\) consists of two or
three unaries and the labelled graph on \(R\) is strongly connected.

## 1. Exact theorem, disjoint wedges, and the workload ledger

Put \(H=X+Y+Z\).  Let \(B_t\) count all zero-source births and \(D_t\)
all labelled direct lower deaths after the beginning of the episode.  Every
top reaction and every nonzero lower transfer preserves \(H\), so

\[
                         H(X_t)-H(X_0)=B_t-D_t.       \tag{1.1}
\]

There are only finitely many top-dead pure vertices.  At each such vertex
\(d\), choose the positive transverse linear coordinate \(S_d\) constructed
in Section 3 or Section 4, after relabelling \(d\) as \(X\).  On the normalized
simplex \(\Delta\), \(S_d\) vanishes only at \(d\).  Hence a fixed sufficiently
small \(\varepsilon_0>0\) makes the normalized wedge neighborhoods

\[
 \widehat{\cal W}_d
   =\{u\in\Delta:S_d(u)<\varepsilon_0\}                \tag{1.2}
\]

have pairwise disjoint closures.  Let \({\cal W}_d\) be the population lift
\(\{x:x/H(x)\in\widehat{\cal W}_d\}\).  Define the single global activated
region

\[
 {\cal A}=\Delta\cap
   \left(\bigcup_d\widehat{\cal W}_d\right)^{\mathrm c}.              \tag{1.3}
\]

It is compact.  Reaction jumps are uniformly bounded.  Consequently, after
enlarging the finite set once more, the first actual jump out of
\({\cal W}_X\) cannot land in another \({\cal W}_d\); its normalized endpoint
is literally in \({\cal A}\).

> **Theorem 1.1 (activation or direct-death ledger).**  For each fixed
> network in either kernel there are \(R,C<\infty\), independent of the
> integer \(L\ge1\), such that the following holds.  From every \(x\) with
> \(H_0:=H(x)\ge R\) in \({\cal W}_X\), there is an all-clock stopping time
> \(\sigma_{x,L}\) satisfying
>
> \[
>  \mathbb E_x B_{\sigma_{x,L}}\le C,
>  \qquad \mathbb E_x\sigma_{x,L}\le C,                \tag{1.4}
> \]
>
> and one of the following *labelled* alternatives holds at its actual
> endpoint.  Labels are assigned after the terminal jump in the priority
> order \(F>D>I\):
>
> \[
> \begin{array}{ll}
> F:&H(X_{\sigma_{x,L}})\le H_0/2,\\[2mm]
> D:&H(X_{\sigma_{x,L}})>H_0/2,\quad
>       D_{\sigma_{x,L}}\ge L,\\[2mm]
> I:&H(X_{\sigma_{x,L}})>H_0/2,\quad
>       D_{\sigma_{x,L}}<L,\quad
>       X_{\sigma_{x,L}}/H(X_{\sigma_{x,L}})\in{\cal A}.
> \end{array}                                           \tag{1.5}
> \]
>
> Every episode contains at least one ordinary physical jump.  Every clock,
> including every direct death, remains present throughout the construction.

The independence of \(C\) from \(L\) is essential.  We first construct a base
time \(\sigma_\infty\), stopping only at \(F\) or at the first exit from
\({\cal W}_X\), with

\[
 \sup_{H_0\ge R}\mathbb E_x\sigma_\infty\le C,
 \qquad
 \sup_{H_0\ge R}\mathbb E_xB_{\sigma_\infty}\le C.     \tag{1.6}
\]

Deaths are not absorbing in this base construction.  If \(\rho_L\) is the
actual time of the \(L\)-th direct death, set

\[
                         \sigma_{x,L}=\sigma_\infty\wedge\rho_L.     \tag{1.7}
\]

Then (1.4) follows by monotonicity, and (1.5) is exhaustive with the stated
priority.  Thus there is no circular choice of \(L\) against an
\(L\)-dependent prelude debt.

## 2. Lower-linkage sign and literal finite establishment

Let \(\delta_X\) be the total rate coefficient of direct arrows \(X\to0\).
Inside \({\cal W}_X\), \(X\ge(1-C\varepsilon_0)H\).  If \(\delta_X>0\), then,
up to the exit of the wedge or \(F\),

\[
                         {\cal L}H\le \beta_0-cH,      \tag{2.1}
\]

where \(\beta_0\) is the total constant birth rate.  Stopped Dynkin applied
to \(H\), followed by localization, gives a uniform mean time to the exit or
\(F\), and the birth compensator gives the second bound in (1.6).  This proves
the theorem in that branch.  We may therefore assume in the hard branch that

\[
                              \delta_X=0.              \tag{2.2}
\]

If \(X\in U\), every lower arrow sourced at \(X\) is then a transfer to \(Y\)
or \(Z\).  It strictly increases the transverse height \(S\) used below.  The
only lower arrows that can decrease a transverse coordinate are sourced in
\(Y,Z\), with aggregate rate

\[
                              \lambda_{\rm adv}\le C(1+Y+Z).          \tag{2.3}
\]

Thus an order-\(H\) \(X\)-source clock is favorable and is never hidden in a
bounded error term.

Fix a sufficiently large integer \(K\).  We now prove, without a prescribed
slow reaction word, the uniform establishment estimate on \(0\le S<K\).

**Two carriers.**  Use the height \(S=v_YY+v_ZZ\) of Section 3.  At \(S=0\)
the top linkage is disabled.  If \(X\in U\), (2.2) and strong connectivity
give an \(X\to Y\) or \(X\to Z\) arrow of intensity at least \(cX\).  If
\(X\notin U\), then \(U=\{Y,Z\}\), and an arrow out of \(0\) gives a
transverse birth at a fixed positive rate.  Thus a state with
\(0<S\le C_0\) is reached in uniformly bounded mean time and birth count.

On \(0<S<K\), the exact killed-resolvent estimate (3.2), the favorable sign
of every \(X\)-source lower transfer, and (2.3) give, for large \(H_0\) and
before \(F\) or wedge exit,

\[
 {\cal L}S\ge cH_0S,\qquad
 \Gamma S\le CH_0S.                                  \tag{2.4}
\]

Indeed \(H\ge H_0/2\), \(X\ge cH\), and \(S\) is bounded.  Stop a seeded
trial at \(S=0\), \(S\ge K\), \(F\), or wedge exit.  For a fixed small
\(\theta>0\), Taylor's formula makes \(e^{-\theta S}\) a supermartingale
on the open interval.  Since a nonzero population has
\(S\ge s_*:=\min(v_Y,v_Z)>0\), optional stopping gives

\[
 \inf\mathbb P\{S\ge K,\ F,\text{ or wedge exit before }S=0\}
       \ge 1-e^{-\theta s_*}=:p_K>0.                 \tag{2.5}
\]

Stopped Dynkin applied to \(S\), whose endpoint is bounded by \(K\) plus
one jump, gives mean seeded-trial time \(O(H_0^{-1})\).  After a return to
\(S=0\), run the same all-clock seed mechanism again.  Geometric repetition
of (2.5) has uniformly bounded mean duration and birth count.  All fast
carrier firings and all deaths remain present.

**Dyadic kernel.**  Here \(S=2Y+Z\).  First suppose \(X\in U\).  By (2.2)
some \(X\to Y\) or \(X\to Z\) arrow has intensity at least \(cX\), and
every such firing raises \(S\).  While \(S<K\), all clocks capable of
lowering \(S\) are sourced in \(Y,Z\) or at an optional high top complex,
and their total intensity is \(O_K(1)\).  Neutral minimum-source firings do
not affect this race.  Before \(F\) or wedge exit, \(X\ge cH_0\).
Consequently the probability that \(K\) good \(X\)-source firings occur
before the first adverse firing is bounded below uniformly, and their mean
physical time is \(O(H_0^{-1})\).  This reaches \(S\ge K\); an adverse
firing merely restarts the trial at its actual finite transverse state.

It remains to treat \(X\notin U\), hence \(U=\{Y,Z\}\).  On \(S<K\), the
pair \((Y,Z)\) ranges over a finite set.  We quotient only the order-\(H\)
firings sourced at \(B=X+Y\).  A \(B\to A=2Z\) firing is \(S\)-neutral and
lowers \(Y\) by one; a \(B\)-firing to \(Y+Z\) or \(2Y\) raises \(S\).
Thus at most \(K\) consecutive fast neutral firings can occur before either
strict progress or a state with \(Y=0\).

At \(S=0\), a lower birth creates \(Y\) or one \(Z\) at fixed positive
rate.  A lone \(Z\) either moves to \(Y\), receives a second \(Z\) birth,
or is lost and restarts; the second-arrival-or-\(Y\) event has fixed
positive probability.  Once \(Z\ge2\), the source \(A=2Z\) has fixed
positive intensity.  Its firing either makes a strict cut or reaches \(B\).
In the latter case the order-\(H\) \(B\)-clock fires before the bounded slow
competitors with probability tending to one, and it either makes a strict
cut or returns to \(A\).  The pair \(\{A,B\}\) cannot be closed in the
strong top graph because \(Q\ne\varnothing\).  Hence at least one of
\(A,B\) has a strict outgoing label, with a fixed positive same-source
label probability.

This gives a finite quotient chain with no closed unsuccessful class:
from every \(S<K\) phase, a bounded number of slow \(A\)/lower steps and
contracted fast \(B\)-steps has a fixed positive probability of raising
\(S\), reaching \(F\), or exiting the wedge.  Concatenating at most \(K\)
such strict increments gives one uniform positive probability of reaching
\(S\ge K\).  Every wait for a slow step has total progress-or-reset
intensity bounded below by a fixed constant; fast steps only shorten it.
Geometric repetition from the actual endpoint therefore has uniformly
bounded mean physical duration.  This explicitly includes the lone-\(Z\)
resistance-two phase and the neutral \(A\leftrightarrow B\) loop.

In all cases the constant-rate birth compensator now proves

\[
 \sup_{H_0\ge R}\mathbb E_x\tau_K\le C_K,\qquad
 \sup_{H_0\ge R}\mathbb E_xB_{\tau_K}\le \beta_0 C_K.                \tag{2.6}
\]

where \(\tau_K\) stops at \(S\ge K\), wedge exit, or \(F\), but not at a
death.  This is the required literal establishment.  It uses no
population-dependent slow top word and no conditional-Poisson shortcut.

## 3. Two carriers: killed resolvent and multiplicative ascent

Kill the strong top graph when it first exits the carrier set
\(\{X+Y,X+Z\}\) to any other top complex.  The carrier subset cannot be
closed: otherwise strong connectivity would make it the whole top graph,
whose stoichiometric rank would be one rather than two.  Its killed
two-state subgenerator \(Q\) is therefore transient.  Put

\[
 g=(-Q)^{-1}{\bf1}>0,
 \qquad v_i=1-\epsilon g_i>0\quad(i=Y,Z),
 \qquad S=v_YY+v_ZZ.                                  \tag{3.1}
\]

For sufficiently small fixed \(\epsilon>0\), the rate-weighted \(S\)-reward
at each carrier source is strictly positive.  Every noncarrier source has
propensity \(O((Y+Z)^2)\) and bounded \(S\)-jump.  Exactly for
falling-factorial propensities,

\[
                       {\cal L}_TS\ge cXS-CS^2.        \tag{3.2}
\]

Every \(X\)-sourced lower transfer is favorable by Section 2.  Direct deaths
of \(Y,Z\) and all other adverse lower terms contribute only \(O(1+S)\).
Choose \(\varepsilon_0\) small and \(K\) large.  On
\(K\le S<\varepsilon_0H\), before \(F\),

\[
 {\cal L}S\ge cHS,
 \qquad
 \Gamma S:=\sum_e\lambda_e(\Delta_eS)^2
       \le CHS+CS^2\le C'HS.                          \tag{3.3}
\]

The last inequality uses \(S\le\varepsilon_0H\); the fixed and order-\(H\)
lower variances are absorbed because \(S\ge K\).  All \(S\)-jumps are
bounded.

Here are the stopped estimates used in the ascent.  Enter a band at
\(S\in[r,r+C_0]\) and stop at \(S\le r/2\), \(S\ge2r\), wedge exit, or \(F\).
Give wedge exit and \(F\) cemetery value zero.  Taylor's formula and (3.3),
with a fixed sufficiently small \(\theta>0\), give on the open band

\[
              {\cal L}^{\dagger}e^{-\theta S}
                    \le-cHS e^{-\theta S}.            \tag{3.4}
\]

Optional stopping of this nonnegative supermartingale yields

\[
 \mathbb P\{S\le r/2\text{ before the upper or favorable exits}\}
                    \le Ce^{-cr}.                     \tag{3.5}
\]

For the time estimate, do not use the killed function.  Let \(J\) bound the
absolute \(S\)-jump and take \(K>2J\).  Define a bounded function \(f_r\) that
equals \(\log S\) throughout the open band and at every state reachable from
it in one jump, and clamp it arbitrarily outside that one-jump enlargement.
Thus \({\cal L}f_r={\cal L}\log S\) before the stopping time.  The
bounded-jump Taylor formula gives

\[
 {\cal L}f_r
 \ge \frac{{\cal L}S}{S}-C\frac{\Gamma S}{S^2}
 \ge cH                                                   \tag{3.6}
\]

after increasing \(K\).  Every actual stopped endpoint has
\(r/2-J\le S\le2r+J\), so its \(f_r\)-value differs from the starting value
by at most \(\log4+O(r^{-1})\).  Before the wedge exit and \(F\), one has
\(H\ge cr\).  Dynkin's formula therefore gives

\[
                              \mathbb E t_r\le \frac C r.             \tag{3.7}
\]

No exponential holding-time claim is needed.

Sum (3.5)--(3.7) over the dyadic bands
\(K,2K,4K,\ldots\).  The error sum is at most \(Ce^{-cK}\), the physical-time
sum is at most \(C/K\), and this remains true if births move the terminal
wedge boundary outward.  Choosing \(K\) large gives a fixed positive chance
that one establishment-plus-ascent attempt exits \({\cal W}_X\) or reaches
\(F\).  A downward return simply restarts at its actual state.  Geometric
repetition with (2.6) proves (1.6) in the two-carrier kernel.  Direct deaths
have remained active throughout.

## 4. Dyadic kernel: aggregate minimum clocks and exact source balance

Put

\[
                              S=2Y+Z.                  \tag{4.1}
\]

The minimum-height sources are

\[
                         A=2Z,\qquad B=X+Y,            \tag{4.2}
\]

both of \(S\)-height two.  Optional sources \(Y+Z,2Y\) have heights three
and four.  In a band

\[
                         r/2<S<2r,
 \qquad r\le\varepsilon_0H,                            \tag{4.3}
\]

we have \(X\ge H-S\ge(1-\varepsilon_0)H\), and for large \(K\le r\)

\[
 \lambda_{\min}=a_A Z(Z-1)+a_BXY
       \ge c\{Z(Z-1)+HY\}\ge cr^2.                   \tag{4.4}
\]

Call optional high-source reactions, adverse \(Y/Z\)-sourced lower events,
and births **bad**.  Direct \(Y/Z\) deaths are included, not stopped.  Since
the optional-source propensities are \(O(YS)\), their aggregate intensity
satisfies

\[
 \frac{\lambda_{\rm bad}}{\lambda_{\min}}
       \le C(\varepsilon_0+r^{-1}).                   \tag{4.5}
\]

Lower transfers sourced at \(X\) are **good**: each increases \(S\) by one
or two.  Their intensity may be order \(H\).  They are retained in the actual
prefix and are never placed in (4.5).

Consider a reaction prefix that remains in the band.  Let \(m_A,m_B\) be the
numbers of minimum-source firings, \(e\) the number of bad firings, \(g\) the
number of good \(X\)-source firings, and \(c_*\) the number of minimum-source
firings whose target has strictly larger \(S\)-height.  Every good firing and
every strict cut increases \(S\) by at least one; a firing \(A\leftrightarrow
B\) has zero \(S\)-reward; only a bad firing can decrease \(S\), by a bounded
amount.  Hence the exact height ledger gives

\[
                              g+c_*\le Cr+Ce.          \tag{4.6}
\]

Strong connectivity supplies a direct-cut source without enumerating
orientations.  If \(B\) has no strict outgoing cut, every \(B\)-firing goes
to \(A\), consumes one \(Y\), and therefore

\[
                              m_B\le Y_0+2m_A+C(e+g).  \tag{4.7}
\]

Then \(A\) must have a strict outgoing cut.  If \(A\) has no strict outgoing
cut, every \(A\)-firing goes to \(B\), consumes two \(Z\), and

\[
                              2m_A\le Z_0+2m_B+C(e+g). \tag{4.8}
\]

Then \(B\) must have a strict outgoing cut.  If both have strict cuts, every
minimum firing is already from a direct-cut source.  Thus in all cases the
number \(q_*\) of firings from direct-cut sources obeys

\[
 q_*\ge c(m_A+m_B)-Cr-C(e+g).                         \tag{4.9}
\]

At any fixed source, all outgoing labels share the same source monomial.
Consequently a strict label has a fixed conditional probability
\(p_*>0\) at every direct-cut opportunity.

We now give the complete prefix estimate.  Inspect \(M=L_0r\) successive
actual nonterminal reactions, padding only after an exit for the probability
calculation.  At each pre-exit state the conditional chance of a bad reaction
is at most \(q=C(\varepsilon_0+r^{-1})\).  Choose \(L_0\) large, then
\(\varepsilon_0\) small and \(K\) large enough that \(qL_0\) is smaller than
all fixed fractions below.  Adaptive Chernoff gives, outside an event of
probability \(Ce^{-cr}\),

\[
                              e\le 2qM.                \tag{4.10}
\]

If the prefix stays in the band, (4.6) first gives \(g\le Cr+Ce\).  Hence all
but \(O(r+e)\) of the \(M\) reactions are minimum-source firings.  Equations
(4.9) and (4.6) then imply that a fixed fraction of \(M\) are direct-cut
opportunities, whereas the height ledger permits only \(O(r+e)\) successful
cuts.  A second adaptive Chernoff bound for the fixed label probability
\(p_*\) contradicts this when \(L_0\) is large.  A lower exit before \(M\)
requires at least \(cr\) bad negative reward and is covered by the same first
Chernoff estimate.  Therefore

\[
 \mathbb P\{\text{lower exit, or no exit by }M\}
                              \le Ce^{-cr}.            \tag{4.11}
\]

Restart \(M\)-reaction prefixes after a nonexit.  Their number is
geometrically dominated, so the expected reaction count before a band exit
is \(O(r)\).  While the prefix remains in the band, (4.4) bounds every holding
time by an exponential clock of rate \(cr^2\).  Thus

\[
                              \mathbb E t_r\le \frac C r.             \tag{4.12}
\]

Equations (4.11)--(4.12), summed over dyadic bands, give a fixed positive
chance and uniformly bounded mean time for one establishment-plus-ascent
attempt to exit \({\cal W}_X\) or reach \(F\).  The sum \(\sum_r C/r\) is
finite over doubling \(r\), even if births move the wedge boundary outward.
Failed attempts restart from their actual state.  The small-phase bound
(2.6) and geometric repetition prove (1.6) in the dyadic kernel.  In
particular, direct deaths remain live; no prefix is restarted merely because
a death occurred.

## 5. Truncation, integrability, and exact composition scope

The preceding constructions tile actual physical paths by establishment and
band stopping times.  Each tile contains a jump unless it ends at the same
terminal jump as the previous tile; such zero-length classifier handoffs are
concatenated and never counted as episodes.  The geometric attempt bounds and
(2.6), (3.7), or (4.12) give \(\mathbb E\sigma_\infty<\infty\).  The chain is
nonexplosive under binary mass action: pathwise,
\(H_t\le H_0+N_t\), where \(N\) is the constant-rate zero-source birth
Poisson process; on every bounded interval this bounds all binary hazards.
Localization and monotone convergence therefore justify all stopped Dynkin
and compensator identities.  In particular,

\[
                  \mathbb E B_{\sigma_\infty}
                        =\beta_0\mathbb E\sigma_\infty\le C,          \tag{5.1}
\]

with the same \(C\) for every later truncation \(\sigma_{x,L}\).  This proves
Theorem 1.1.

The residual support certificate identifies the homogeneous dead-ray
incidences as

\[
                         360=168+144+48,              \tag{5.2}
\]

where the first two summands are respectively the two-carrier and dyadic
kernels proved here, and the final 48 are common-catalyst kernels.  The
common-catalyst family, including all four relative lower supports, is proved
separately at exact SHA

~~~text
81a48c007e092570cd500d8f124c0546538d44f7e62599100ecf00480f401496
~~~

The present theorem deliberately stops at activation-or-ledger.  A common
deterministic top-service and stochastic compensator window can be appended
at an \(I\)-endpoint.  By (1.1), an \(F\)-endpoint already has
\(D-B\ge H_0/2\), while a \(D\)-endpoint has \(D\ge L\).  Because the birth
debt \(C\) is independent of \(L\), one may choose \(L>C\) only after the
theorem is applied.  This is the exact interface required by the
workload-only Foster composition.

The support identity is finite geometry only.  No finite stochastic
orientation, history, or population enumeration enters Sections 2--4.
