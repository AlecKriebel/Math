# Homogeneous carrier and dyadic activation with every lower support

**Proof-first standalone theorem, 2026-08-12 PDT.**  Fix three species
\(X,Y,Z\), put \(H=X+Y+Z\), and let

\[
 R=\{0\}\cup U,qquad
 U\in\big\{\{X,Y\},\{X,Z\},\{Y,Z\},\{X,Y,Z\}\big\}. \tag{1.1}
\]

The lower labelled graph is strongly connected and has arbitrary fixed
positive rates.  The top support lies on the quadratic shell, has affine
rank two, excludes \(2X\), and its labelled graph is strongly connected.
This note treats either of the following symbolic alternatives.

1. **Two carriers:** \(X+Y,X+Z\in T\); any subset of
   \(\{2Y,Y+Z,2Z\}\) compatible with rank two and strong connectivity may
   also occur.
2. **Dyadic carrier:** \(X+Y,2Z\in T\), while
   \(X+Z,2X\notin T\); any subset of \(\{Y+Z,2Y\}\) compatible with rank
   two and strong connectivity may also occur.

Every clock is retained.  In particular, a lower \(X\)-source may have
rate of order \(H\); it is treated by its exact sign, not put into a small
exceptional-rate class.

## 1. Statement

Let \(B_t\) count zero-source births and let \(D_t\) count all labelled
direct lower deaths.  They satisfy the exact workload identity

\[
                          H(X_t)-H(X_0)=B_t-D_t.       \tag{1.2}
\]

> **Theorem 1.1 (all-clock dormant-ray activation).**  For every fixed
> network above, every integer \(L\ge1\), and a sufficiently small fixed
> \(\varepsilon>0\), there are \(R_0,C<\infty\) and an all-clock stopping
> time \(\sigma_x\), selected from every state \(x\) with
> \(H(x)\ge R_0\) in the dormant pure-\(X\) neighborhood, such that
> \[
>             \mathbb E_x\sigma_x\le C,
>             \qquad \mathbb E_xB_{\sigma_x}\le C,   \tag{1.3}
> \]
> the endpoint is the actual physical endpoint of an ordinary jump, and
> one of the following holds there:
> \[
>          D_{\sigma_x}\ge L,qquad
>          S(X_{\sigma_x})\ge\varepsilon H(X_{\sigma_x}),qquad
>          H(X_{\sigma_x})\le R_0.                    \tag{1.4}
> \]
> Here \(S=v_YY+v_ZZ\), with fixed positive \(v_Y,v_Z\), in the
> two-carrier case, and \(S=2Y+Z\) in the dyadic case.  The activated
> alternative is separated from every dead pure-\(X\) ray by a fixed
> normalized distance.  Moreover
> \[
>                  \mathbb E_x(D_{\sigma_x}-B_{\sigma_x})^-le C.   \tag{1.5}
> \]

Equation (1.5) follows from \((D-B)^-\le B\), but is included to state the
exact interface used by the homogeneous occupation theorem.

## 2. Exact sign of every lower \(X\)-clock

Before analyzing either top kernel, isolate the lower issue which is lost if
all unary clocks are placed into one error term.  At a pure-\(X\) chart an
off-diagonal lower reaction sourced at \(X\) has only three possibilities:

\[
                       X\longrightarrow Y,qquad
                       X\longrightarrow Z,qquad
                       X\longrightarrow0.             \tag{2.1}
\]

The first two strictly increase both activation coordinates used here.  The
last is a direct death and increments \(D\).  Thus, until activation or the
next favorable death endpoint, no lower \(X\)-source contributes a negative
drift, carré-du-champ error, or exceptional hazard.  Its possibly order-
\(H\) clock is helpful.

Every adverse lower transfer is instead sourced at \(Y\) or \(Z\).  In a
region where \(Y+Z\asymp r\), its aggregate rate is \(O(r)\), and its jump
in either activation coordinate is bounded.  Constant births have rate
\(O(1)\).  Direct deaths from \(Y,Z\) are stopped and counted as favorable.
This sourcewise split is valid for all four supports in (1.1).

## 3. Uniform seeding at zero transverse mass

At \(Y=Z=0\), the top linkage is dead.  There is nevertheless a uniform
all-clock route to a transverse seed or a direct death.

If \(X\in U\), then either an \(X\to0\) label fires, which is favorable,
or strong connectivity of the lower graph supplies an outgoing path whose
first nonzero step is \(X\to Y\) or \(X\to Z\).  All \(X\)-source labels
have rates proportional to \(X\), so the first such event has mean
\(O(H^{-1})\), and every competing \(X\)-label is itself either a seed or a
death.  Constant births can only add a bounded expected charge before this
event.

If \(X\notin U\), every nonzero lower vertex is \(Y\) or \(Z\).  Select
one outgoing constant label from zero.  Its waiting time has a fixed
exponential mean and its firing creates a transverse molecule.  Competing
births also create transverse mass.  Hence there are constants \(C_s,C_b\)
such that the seed-or-death time \(\sigma_s\) obeys

\[
       \sup_{H\ge R_0}\mathbb E\sigma_s\le C_s,
       \qquad
       \sup_{H\ge R_0}\mathbb E B_{\sigma_s}\le C_b. \tag{3.1}
\]

Every endpoint above is an actual reaction endpoint.  No prescribed top
word is used.

## 4. Two-carrier Perron--Frobenius wedge

Assume \(X+Y,X+Z\in T\).  Kill the labelled top graph on first leaving the
carrier set \(\{X+Y,X+Z\}\).  Its two-state subgenerator \(Q\) is
transient: a nonempty closed carrier subset would contradict strong
connectivity of the full top graph.  Put

\[
          g=(-Q)^{-1}{\bf1},\qquad
          v_i=1-\theta_0g_i>0\quad(i=Y,Z),qquad
          S=v_YY+v_ZZ,                                \tag{4.1}
\]

with \(\theta_0>0\) sufficiently small.  At either carrier source the
rate-weighted \(S\)-reward is then strictly positive.  Reactions sourced at
a pure-mutant complex have propensity \(O((Y+Z)^2)\) and bounded reward.
Consequently, exactly for falling factorial propensities,

\[
                         {\cal L}_TS\ge cX S-CS^2.    \tag{4.2}
\]

The positive coefficients make \(S\asymp Y+Z\).  Apply the sign split of
Section 2, and send every direct death to a favorable cemetery with payoff
zero.  For sufficiently small \(\varepsilon\), all large \(H\), and
\(0<S\le\varepsilon H\), the killed generator and its quadratic variation
satisfy

\[
        {\cal L}^{\dagger}S\ge c_1HS,
        \qquad
        \Gamma S\le C_1HS.                            \tag{4.3}
\]

Here an \(X\to Y/Z\) jump is kept with its positive sign; it is not hidden
in \(C_1HS\).  Bounded jumps and Taylor expansion give, for fixed small
\(\theta>0\),

\[
                   {\cal L}^{\dagger}e^{-\theta S}
                       \le-c_2HS e^{-\theta S}.       \tag{4.4}
\]

Stop a trial at activation, a direct death, or return to \(S=0\).  Starting
from any one-molecule seed, optional stopping in (4.4), first under bounded
localization and then by monotone convergence, yields

\[
 \inf_{H\ge R_0}
 \mathbb P\{S\ge\varepsilon H\text{ or a death before }S=0\}
                         \ge p_1>0.                   \tag{4.5}
\]

To control physical time, choose a fixed \(S_0\).  On
\(S_0\le S\le\varepsilon H\), the same bounded-jump calculation gives

\[
                         {\cal L}^{\dagger}\log S\ge c_3H,          \tag{4.6}
\]

after increasing \(S_0\).  The mean time across this region is at most
\(C\log H/H\le C\).  Below \(S_0\), only finitely many transverse count
vectors occur.  A carrier source, whenever present, has rate at least
\(cH\); an \(X\)-lower event is a seed increase or a death; and at a state
with no carrier source, the enabled pure-mutant top and lower/birth clocks
have a fixed positive aggregate rate.  The killed carrier subgenerator has
no closed unsuccessful class.  Therefore the finite transverse phase,
with activation and death declared absorbing, has a uniform finite mean
exit time.  This is a finite killed-resolvent statement over transverse
count vectors, not an enumeration of orientations or a bounded reaction
word.

Combining this finite phase with (3.1), (4.5), and (4.6) gives a complete
attempt with conditional success probability at least \(p_1\) and uniform
mean duration.  A failed attempt returns to \(S=0\) and is reseeded from its
actual endpoint.

## 5. Dyadic compound ascent

Assume now that \(X+Y,2Z\in T\), while \(X+Z,2X\notin T\).  Put

\[
                              S=2Y+Z.                  \tag{5.1}
\]

The minimum-height top sources are

\[
                         A=2Z,qquad B=X+Y,            \tag{5.2}
\]

and the only possible higher sources are \(Y+Z,2Y\).  Fix a dyadic band

\[
                    K\le r/2<S<2r\le\varepsilon H.   \tag{5.3}
\]

Since \(X\ge H-S\), the aggregate minimum-source hazard satisfies

\[
 \lambda_{\min}ge c\{Z(Z-1)+XY\}\ge cr^2.          \tag{5.4}
\]

The higher-source hazard is at most \(CYS\).  If \(Y>0\), the \(XY\)
term in (5.4) bounds its ratio by \(CS/H\le C\varepsilon\); if \(Y=0\),
the higher propensity is zero.  By Section 2, every adverse lower clock is
sourced in \(Y,Z\) and has aggregate rate \(O(r)\); births have rate
\(O(1)\).  Hence, calling higher-source reactions, adverse lower transfers,
and births exceptional,

\[
              {\lambda_{\rm exceptional}\over\lambda_{\min}}
                       \le q_{\varepsilon,K}
                       :=C(\varepsilon+K^{-1}).        \tag{5.5}
\]

An \(X\to Y/Z\) reaction instead makes a strict positive jump of \(S\),
and \(X\to0\) is a favorable death endpoint.  Neither appears in (5.5).
Successive exceptional indicators are therefore adaptively dominated by
Bernoulli variables of parameter \(q_{\varepsilon,K}\).

It remains to convert aggregate minimum firings into strict height cuts.
Let \(m_A,m_B\) count reactions sourced at \(A,B\), and let \(e\) count
exceptional reactions in a reaction prefix which stays in the band.  If
\(B\) has no direct edge to a higher source, every \(B\)-reaction goes to
\(A\), lowering \(Y\) by one.  Since an \(A\)- or exceptional reaction
raises \(Y\) by at most two, nonnegativity gives

\[
                 m_B\le2r+2m_A+2e.                   \tag{5.6}
\]

If \(A\) has no direct higher edge, every \(A\)-reaction goes to \(B\),
lowering \(Z\) by two; hence

\[
                 2m_A\le2r+2m_B+2e.                  \tag{5.7}
\]

Strong connectivity ensures that at least one minimum source has a direct
strict cut, and if one lacks it the displayed zero-height edge to the other
is forced.  Conditional on a firing from a direct-cut source, its cut
probability is a fixed positive labelled-rate ratio \(q_*>0\).  Equations
(5.6)--(5.7), adaptive Bernoulli Chernoff bounds for the exceptional events,
and a second adaptive Chernoff bound for the direct-cut labels imply, after
first choosing \(K\) large and \(\varepsilon\) small,

\[
 \mathbb P\{S\text{ exits a dyadic band downward}\}\le Ce^{-cr}.    \tag{5.8}
\]

For completeness, inspect \(M=(M_0+2)r\) successive events, padding after
an exit.  Except with probability \(Ce^{-cr}\), at most \(r\) are
exceptional.  Equations (5.6)--(5.7) then make a fixed fraction of the
remaining minimum firings direct-cut opportunities; choosing \(M_0\) large
and applying the \(q_*\)-Chernoff bound gives at least \(4r\) strict cuts.
Fewer than \(r/5\) adverse exceptional jumps cannot pay the bounded
downward reward needed for a lower exit, whereas the strict cuts force an
upper exit.  This proves (5.8) without prescribing a label word.

The total hazard in the band is at least \(cr^2\).  Repeating the preceding
fixed-prefix estimate gives an exponential tail for the event count on the
scale \(r\); stochastic domination of the holding times therefore yields

\[
                     \mathbb E t_r\le {C\over r}.     \tag{5.9}
\]

Apply (5.8)--(5.9) on the bands \(K,2K,4K,\ldots\).  Since

\[
             \sum_{j\ge0}Ce^{-c2^jK}<1,qquad
             \sum_{j\ge0}{C\over2^jK}<\infty,        \tag{5.10}
\]

one dyadic attempt reaches \(S\ge\varepsilon H\) with probability at
least \(p_2>0\) and has uniform finite mean duration.  The target
\(\varepsilon H\) may move by the bounded workload change of one event;
enlarging adjacent band constants absorbs this overshoot.

Below \(K\), use Section 3 at \(S=0\).  With \(0<S<K\), there are finitely
many transverse count vectors.  An enabled \(XY\) clock has rate
\(\Theta(H)\) and its reaction is zero-height or favorable; an
\(X\)-lower clock is a strict increase or a death; all remaining top and
lower clocks have fixed rates on this finite phase.  Strong connectivity of
the top and lower graphs excludes a closed unsuccessful class.  Declaring
\(S\ge K\) and every direct death absorbing, the finite killed resolvent has
a uniform finite mean absorption time and a positive probability of reaching
\(K\).  This is the exact finite establishment lemma, including the possible
need for two \(Z\)-seeds; it uses an aggregate finite phase, not a fixed top
reaction word.

Adjoining establishment to the dyadic bands proves the claimed complete
attempt with probability \(p_2\) and uniform finite mean duration.

## 6. Compound attempts and the ledger endpoint

In either kernel let \(p=\min(p_1,p_2)>0\) for the applicable construction.
Start with Section 3 when needed, run one complete activation attempt, and
restart after a failed attempt at its actual endpoint.  Every direct death
ends the current attempt, increments the cumulative count, and restarts
unless it is the \(L\)-th death.  Conditional at every restart, the chance
of activation before another unsuccessful restart is at least \(p\).
Consequently the number of attempts before activation or the \(L\)-th death
is dominated by a finite sum of geometric variables.  The complete stopping
time has a uniform finite mean.

The aggregate birth clock has constant intensity \(\beta\).  Localizing in
time and event count and then using monotone convergence gives the exact
compensation identity

\[
                         \mathbb E B_{\sigma_x}
                              =\beta\mathbb E\sigma_x\le C.          \tag{6.1}
\]

If the finite workload threshold is crossed, record the third alternative
in (1.4).  Otherwise the process ends at activation or at the \(L\)-th
death.  Every branch ends at an actual physical jump.  Equation (1.5)
follows from \((D-B)^-\le B\), completing the proof. \(\square\)

## 7. Scope and dependency boundary

The proof is uniform only after the orientation and positive labelled rates
are fixed; no constant is claimed uniformly over rate space.  Optional pure
mutant or higher vertices are included sourcewise in (4.2) or (5.5).
Arbitrary residual lower supports are included by Sections 2--3.  The
two-carrier proof uses the killed-carrier Perron--Frobenius identity; the
dyadic proof uses aggregate minimum-source balance and adaptive Chernoff,
not orientation enumeration or a bounded reaction history.

The common-catalyst support \(\{X+Y,Y+Z,2Y\}\) is deliberately outside
this theorem and is covered by the separate all-lower-support operational
macro at SHA-256
`81a48c007e092570cd500d8f124c0546538d44f7e62599100ecf00480f401496`.
