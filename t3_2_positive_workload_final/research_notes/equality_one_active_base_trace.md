# The exact base trace for the relative-resistance equality chain

## 1. Scope

Consider the stochastic mass-action network

\[
 0\mathrel{\mathop{\rightleftarrows}^{\alpha}_{\beta}}B+C,
 \qquad
 B\mathop{\longrightarrow}^{\kappa _1}A
 \mathop{\longrightarrow}^{\kappa _2}A+B
 \mathop{\longrightarrow}^{\kappa _3}2B
 \mathop{\longrightarrow}^{\kappa _4}B,               \tag{1.1}
\]

where all six constants are strictly positive and falling-factorial
propensities are used.  The active coordinate in the disputed flag is
\(C\), and its inactive cap is \(A=B=0\).

This note audits that exact directed network.  It does not infer a theorem
for another orientation or support.  The local analytic and recurrence
flags in the companion executable remain false until the argument receives
an independent replay.

Put

\[
 z_N=(0,0,N),\qquad
 {\cal B}=\{(0,0,n):n\geq0\}.                          \tag{1.2}
\]

Starting from \(z_N\), wait for the first \(0\to B+C\) reaction and let
\(\tau_N\) be the subsequent first hit of \({\cal B}\).  Thus the initial
\({\rm Exp}(\alpha)\) holding time is included.  The central conclusion is
that a rare activation of probability order \(N^{-1}\), not an adverse
order-\(N^{-2}\) return, produces a macroscopic loss of \(C\).

## 2. Two exact identities

Let \(J_i(t)\) count the four reactions in the directed second linkage,
in the order displayed in (1.1).  Define

\[
 Q=C-A-B.                                              \tag{2.1}
\]

Every reaction except \(A\to A+B\) and \(2B\to B\)
preserves \(Q\), and those two reactions change it by \(-1\) and \(+1\),
respectively.  Pathwise,

\[
 Q_t-Q_0=-J_2(t)+J_4(t).                              \tag{2.2}
\]

In particular, at two base endpoints,

\[
 C_{\tau_N}-N=J_4(\tau_N)-J_2(\tau_N).               \tag{2.3}
\]

This identity retains every reaction.  It shows exactly what must be
estimated: \(A\to A+B\) is the macroscopic negative flux, whereas
\(2B\to B\) is the only positive flux.

There is also an exact countable-phase reduction.  Set

\[
 u(t)=\int_0^t B_s\,ds.                               \tag{2.4}
\]

On the \(u\)-clock the coordinate \(A\), until it first hits zero, is the
birth--death chain \(Y\) with generator

\[
 {\cal G}f(a)=\kappa _1\{f(a+1)-f(a)\}
 +\kappa _3a\{f(a-1)-f(a)\}.                         \tag{2.5}
\]

Indeed, the only two reactions changing \(A\) have physical intensities
\(\kappa _1B\) and \(\kappa _3AB\), so their common factor \(B\) is
removed by (2.4).  This is an exact random-time identity, not a stationary
approximation.

Let

\[
 T_0=\inf\{u:Y_u=0\},\qquad Y_0=1.                   \tag{2.6}
\]

The chain (2.5) is an immigration--death chain killed at zero.  It has
finite exponential moments of \(T_0\) for a sufficiently small positive
exponent.  Its promotion probability has the exact formula

\[
 {\mathbb P}_1\{T_K<T_0\}
 =\left\{\sum_{j=0}^{K-1}
       \left({\kappa _3\over\kappa _1}\right)^j j!
   \right\}^{-1}
 \le { (\kappa _1/\kappa _3)^{K-1}\over (K-1)!}.     \tag{2.7}
\]

Thus the apparently two-active \(A\)-excursion has a factorial, rather
than merely polynomial, boundary tail.  It must be retained as the
countable phase; replacing it by a fixed box would be invalid.

## 3. The first activation

Immediately after the primary zero-source reaction the state is

\[
 (A,B,C)=(0,1,N+1).                                   \tag{3.1}
\]

Before the first \(B\to A\) reaction, \(A=0\).  The \(B\)-population has
constant immigration \(\alpha\), death at least \(\beta NB\), the
quadratic removal \(\kappa _4(B)_2\), and killing intensity
\(\kappa _1B\).  Standard stopped immigration--death estimates give

\[
 \begin{aligned}
  {\mathbb E}\int_0^{\sigma_N}B_s\,ds
    &={1\over\beta N}+O(N^{-2}),\\
  {\mathbb E}\int_0^{\sigma_N}(B_s)_2\,ds
    &=O(N^{-2}),                                      \tag{3.2}
 \end{aligned}
\]

where \(\sigma_N\) is the first return to \(B=0\) or the first
\(B\to A\) firing.  The same bounds hold for each fixed moment of the
stopped occupation.  The killing compensator and the second-order
remainder in \(1-e^{-x}\) therefore yield

\[
 {\mathbb P}_{z_N}(E_N)
 ={\kappa _1\over\beta N}+O(N^{-2}),                 \tag{3.3}
\]

where \(E_N\) is the event that \(B\to A\) fires before the base return.
Conditional on \(E_N\), its firing state is

\[
 (1,0,N+1)+o_{\mathbb P}(1).                          \tag{3.4}
\]

The error includes every extra zero-source birth and every
\(2B\to B\) firing.  Their aggregate contribution is one order smaller;
it is not obtained by selecting only a preferred reaction word.

On \(E_N^c\), (2.3) reduces to \(C_{\tau_N}-N=J_4\), and (3.2) gives,
for each fixed integer \(p\geq1\),

\[
 {\mathbb E}[J_4^p;E_N^c]=O(N^{-2}).                 \tag{3.5}
\]

This is the complete positive endpoint contribution of the neutral
base-return block.

## 4. Candidate full activated-excursion limit

This section derives the only possible localized slow limit.  Removing all
localizations at the literal first return to \({\cal B}\) requires a
global restart and stopped-uniform-integrability lemma which is not proved
in this note.  Accordingly (4.9) and the conclusions in Sections 5--6 are
conditional calculations.  The shorter episode in Section 7 does not use
that missing lemma.

Write physical time as \(t=Ns\), put \(y_N(s)=C_{Ns}/N\), and set

\[
 \lambda(a)=\alpha+\kappa _2a.                       \tag{4.1}
\]

First stop with \(A\le K\), \(\varepsilon\le y_N\le2\), and with the
usual fast-\(B\) localization.  The \(B\)-balance martingale and the
quadratic factorial equation give, in \(L^1\),

\[
 \begin{aligned}
 \int_0^T\left\{NB_{Ns}
       -{\lambda(A_{Ns})\over\beta y_N(s)}\right\}ds&\longrightarrow0,\\
 \int_0^T N(B_{Ns})_2\,ds&\longrightarrow0.          \tag{4.2}
 \end{aligned}
\]

The martingale quadratic variations are bounded at precisely the required
orders: after division by \(N\), the linear balance has quadratic variation
\(O(N^{-1})\), and the stopped factorial balance is uniformly integrable.
Consequently \(A_{Ns}\) converges to the jump process with rates

\[
 a\longrightarrow a+1:
 {\kappa _1\lambda(a)\over\beta y},
 \qquad
 a\longrightarrow a-1:
 {\kappa _3a\lambda(a)\over\beta y}.                 \tag{4.3}
\]

Equation (2.2), divided by \(N\), gives simultaneously

\[
 {dy\over ds}=-\kappa _2Y_s.                          \tag{4.4}
\]

The positive term \(J_4/N\) vanishes by the second line of (4.2).

Use the exact chain clock in (2.5).  Equations (4.3)--(4.4) become

\[
 {du\over ds}={\lambda(Y_u)\over\beta y(u)},
 \qquad
 {d\over du}\log y(u)
 =-{\beta\kappa _2Y_u\over\alpha+\kappa _2Y_u}.     \tag{4.5}
\]

Therefore the activated endpoint fraction is

\[
 R=\exp\left\{-\int_0^{T_0}
 {\beta\kappa _2Y_u\over\alpha+\kappa _2Y_u}\,du
 \right\}.                                           \tag{4.6}
\]

For every positive rate vector,

\[
 0<R<1\quad\hbox{almost surely}.                      \tag{4.7}
\]

The corresponding scaled physical duration is

\[
 {\cal T}=\int_0^{T_0}
 {\beta R(u)\over\alpha+\kappa _2Y_u}\,du
 \le {\beta\over\alpha}T_0.                         \tag{4.8}
\]

The intended localization removal is as follows.  Formula (2.7) handles
\(A\); while
\(C\ge\varepsilon N\) and \(A\le K\), the \(B\)-coordinate is dominated
by an immigration--linear-birth--death chain whose death coefficient is
at least \(\beta\varepsilon N\), giving factorial boundary tails and
all stopped occupation moments.  Finally let \(K\to\infty\) and then
\(\varepsilon\downarrow0\).  Since (4.7) is strictly positive and
\(T_0\) has an exponential moment, the two discarded probabilities vanish
with the endpoint powers uniformly integrable.  The clearance after
\(Y\) hits zero changes only \(o(N)\) particles; reactivation during that
clearance is \(o(1)\).  If the restarted exceptional paths have the
asserted uniform moments, then, conditional on \(E_N\),

\[
 {C_{\tau_N}\over N}\Longrightarrow R,\qquad
 {\tau_N\over N}\Longrightarrow{\cal T},            \tag{4.9}
\]

The desired conclusion also requires uniform integrability of every fixed
endpoint power and of the first duration moment.  These are precisely the
uncertified restart estimates, not consequences of the displayed weak
convergence alone.

This is the source-rate promotion estimate: a divergent \(A\)-cofactor is
not called a finite-box failure.  It is controlled by (2.7), and the full
physical chain is followed back to \(A=B=0\).

## 5. Conditional leading base-return coefficients

Put

\[
 \gamma={\kappa _1\over\beta},\qquad
 \phi_r={\mathbb E}R^r\quad(r>0).                    \tag{5.1}
\]

Then \(0<\phi_r<1\).  Conditional on (4.9) and its stated uniform
integrability, combining (3.3), (3.5), and (4.9) gives, for every
fixed positive integer \(r\),

\[
 {\mathbb E}_{z_N}\{C_{\tau_N}^r-N^r\}
 =\gamma N^{r-1}(\phi_r-1)+o(N^{r-1}).               \tag{5.2}
\]

In particular,

\[
 \begin{aligned}
 {\mathbb E}\Delta C
   &=\gamma(\phi_1-1)+o(1)<0,\\
 {\mathbb E}(\Delta C)^2
   &=\gamma N\,{\mathbb E}(1-R)^2+o(N),\\
 {\mathbb E}\{C_{\tau_N}^2-N^2\}
   &=\gamma N(\phi_2-1)+o(N)<0.                      \tag{5.3}
 \end{aligned}
\]

The Feynman--Kac coefficient is also characterized without simulation.
If \(\varphi_r(a)={\mathbb E}_aR^r\), it is the minimal bounded solution
of

\[
 \kappa _1(\varphi_r(a+1)-\varphi_r(a))
 +\kappa _3a(\varphi_r(a-1)-\varphi_r(a))
 -r{\beta\kappa _2a\over\alpha+\kappa _2a}
   \varphi_r(a)=0,
 \quad \varphi_r(0)=1,                               \tag{5.4}
\]

and \(\phi_r=\varphi_r(1)\).  The pathwise inequality (4.7), rather than
a numerical solution of (5.4), proves the strict sign for every positive
choice of rates.  The coefficient can approach zero when rates approach
the boundary, but it cannot change sign at an interior rate vector.

Under the same condition, the physical duration would have the expansion

\[
 {\mathbb E}_{z_N}\tau_N
 ={1\over\alpha}+\gamma{\mathbb E}{\cal T}+o(1).      \tag{5.5}
\]

The first term is the initial zero-source wait.  A neutral post-birth
excursion is \(O(N^{-1})\); an activated excursion is \(O(N)\) but occurs
with probability \(\gamma/N+O(N^{-2})\).

## 6. Conditional literal-base-return drift

Let

\[
 {\cal F}_{\ell}(a,b,c)
 =K+\log(a!)+\log(b!)+\log(c!)+\ell_Aa+\ell_Bb+\ell_Cc
                                                               \tag{6.1}
\]

with \(K\) chosen so that \({\cal F}_{\ell}\ge1\).  The vector \(\ell\)
is arbitrary and fixed; in particular it may be the common rate correction
selected by another atlas region.  Both trace endpoints have \(A=B=0\).
Conditional on the full base-return limit, Stirling's formula and (5.2)
give

\[
 {\mathbb E}\{ {\cal F}_{\ell}(X_{\tau_N})
                 -{\cal F}_{\ell}(z_N)\}
 =\gamma(\phi_1-1)\log N+o(\log N).                  \tag{6.2}
\]

More generally, for each fixed integer \(p\ge1\),

\[
 \begin{split}
 {\mathbb E}\big[ {\cal F}_{\ell}(X_{\tau_N})^p
                  -{\cal F}_{\ell}(z_N)^p\big]
 ={}&\gamma N^{p-1}(\log N)^p(\phi_p-1)\\
 &+o\{N^{p-1}(\log N)^p\}.                           \tag{6.3}
 \end{split}
\]

Thus the literal base-return calculation predicts that the proposed common
choice \((1+{\cal F})^4\) has drift

\[
 -cN^3(\log N)^4                                      \tag{6.4}
\]

for all sufficiently large \(N\), with a rate-dependent \(c>0\).  This
conditional conclusion is not used below; Section 7 proves the needed local
drift by a shorter stopping rule.

Equation (3.5) is load-bearing here.  With probability \(1-O(N^{-1})\)
the neutral block returns to the exact same population state, so it has
zero powered curvature.  Its exceptional positive endpoint is a
\(J_4\)-event of resistance two; its contribution to (6.3) is lower by
two powers of \(N\).  Merely knowing that a neutral endpoint has bounded,
mean-zero \({\cal F}\)-increment would not suffice after taking the fourth
power.

Temporary transfer of reflected debt from \(C\) to \(A\) causes no hidden
endpoint cost.  At the return to \({\cal B}\), both \(A\) and \(B\), and
hence their reflected debts, are zero.  The factorial promotion tail in
(2.7) supplies the stopped uniform integrability needed before that return.

## 7. A shorter stopped common-potential episode

There is a shorter stopped episode which avoids making the all-\(N\)
base-return lemma load-bearing for the local drift.  Fix
\(\varepsilon\in(0,1/4)\), and after the primary zero-source reaction do
the following.

1. Retain the complete \(A=0\) fast excursion until either it returns to
   \(B=0\) or \(B\to A\) fires.  A return without activation is exactly
   neutral except for the \(J_4\) endpoint in (3.5).  If activation fires
   from a nonleading state with \(B>1\), stop immediately.
2. If activation occurs at the leading state \((1,0,N+1)\), start a clean
   stage at \(A=1,B=0\).  The next launch is either \(0\to B+C\) or
   \(A\to A+B\).  Require the immediately following reaction to be
   \(B+C\to0\); otherwise stop at that first competing physical reaction.
3. Repeat clean stages until \(L_N=\lfloor\varepsilon N\rfloor\)
   \(A\)-launched stages have occurred.  Zero-launched clean stages are
   neutral and may be interspersed arbitrarily.

At every clean stage \(C\ge(1-\varepsilon)N\).  The probability that the
launch is the \(A\)-source is

\[
 q={\kappa _2\over\alpha+\kappa _2}>0,               \tag{7.1}
\]

and the probability of a competing reaction before the fast return is
\(O(N^{-1})\), uniformly in the stage.  A negative-binomial Chernoff
bound gives a constant \(K\) for which at most \(KN\) total launches are
needed to see \(L_N\) \(A\)-launches with probability bounded away from
zero.  Conditional on that event, all \(KN\) fast returns are clean with
probability at least

\[
 (1-c/N)^{KN}\ge p_0>0.                               \tag{7.2}
\]

Together with (3.3), the successful stopped event therefore has
probability at least \(c_0/N\).  Its endpoint is

\[
 (A,B,C)=(1,0,N-L_N+O(1)),                            \tag{7.3}
\]

and its conditional expected duration is \(O(N)\).  Since the trigger
probability is \(O(N^{-1})\), the unconditional mean duration is bounded.

All clocks are retained.  If a clean stage fails, the stopping reaction
starts from \(A=1,B=1\); hence its endpoint has \(A,B\le2\) and its
upward \(C\)-overshoot is bounded by a fixed constant (at most three
relative to the original \(N\) in this construction).  More precisely,
after \(j\) completed \(A\)-launched stages it satisfies
\(C_{\tau}\le N+3-j\).  The exceptional
nonleading trigger has the
occupation bound from (3.2).  More explicitly, for every fixed integer
\(r\ge1\), the stopped fast-phase moment equations give

\[
 {\mathbb E}\left[(1+B_\tau+J_4(\tau))^r;
   \begin{array}{c}
   \text{nonleading activation, or a pretrigger}\\[-2mm]
   \text{positive }J_4\text{ endpoint}
   \end{array}\right]=O(N^{-2}).                     \tag{7.3a}
\]

Indeed, either event needs an additional zero-source birth to beat the
order-\(N\) death clock and then a second bounded-rate clock to beat the
same fast clearance; the intervening immigration--death population has
geometric factorial moments.  This upgrades the probability estimate to
the powered endpoint uniform integrability.  Thus, for
\(W=(1+{\cal F}_{\ell})^4\),

\[
 \begin{aligned}
 {\mathbb E}[W(X_\tau)-W(z_N);\text{success}]
   &\le-cN^3(\log N)^4,\\
 {\mathbb E}[(W(X_\tau)-W(z_N))^+;\text{failure}]
   &=O\{N^2(\log N)^4\}.                              \tag{7.4}
 \end{aligned}
\]

The first line is a fixed-fraction endpoint loss multiplied by the
order-\(N^{-1}\) trigger probability.  The second is a bounded endpoint
overshoot, hence one finite difference of the fourth power, multiplied by
the same trigger probability.  The pretrigger \(J_4\) contribution has
the still smaller resistance-two bound (3.5).  Consequently the stopped
episode has strict common-\(W\) physical drift and pays its mean duration.

This argument also handles the temporary transfer of reflected
\(C\)-debt to \(A\): either the episode obtains the macroscopic \(C\)
loss, or it stops at a bounded cofactor endpoint whose full powered cost is
already present in (7.4).  It does not silently project a promoted state
back into the tube.

## 8. Base-trace recurrence interface and present claim boundary

Conditional on the all-\(N\) return lemma isolated below, the base-trace
calculation would supply all of the large-shell Foster data:

1. strict drift of the proper base potential, by (6.2) or (6.3);
2. integrable endpoint powers;
3. bounded mean physical cycle duration, by (5.5); and
4. an exact countable-phase promotion bound, by (2.7).

Nonexplosion is immediate.  Total population can increase only through
the constant-rate zero source and the linear \(A\to A+B\) channel; all
other reactions preserve or lower molecular count.  It is therefore
dominated by a linear pure-birth process.

Every population state has an enabled finite path to \({\cal B}\): use
\(A\to A+B\to2B\) to lower \(A\), use \(2B\to B\) to lower \(B\), and,
if the last \(B\) has \(C=0\), use
\(0\to B+C\), \(2B\to B\), and \(B+C\to0\).  Thus every closed class
meets \({\cal B}\).

The stopped construction in Section 7 proves the local common-potential
episode without this next step.  What is not being promoted in this note
is a support-pair recurrence flag.
For that final lift one must independently replay the all-\(N\) base-return
lemma implicit in the localization removal in Section 4: \(\tau_N<\infty\)
almost surely, \({\mathbb E}\tau_N<\infty\) for each \(N\), and the
large-\(N\) bound (5.5), with no stopped exceptional path omitted.  The
exact \(A\)-clock, factorial ceiling bound, and fast-\(B\) Lyapunov estimate
give the standard geometric restart proof, but that global restart has not
yet received an independent audit.  Conditional on this lemma, the
physical return-trace Foster theorem proves positive recurrence of every
closed class.  No positive-drift or transient rate regime survives the
base-return asymptotic itself.

The companion regression is
`src/equality_one_active_base_trace_certificate.py`, with focused tests in
`tests/test_equality_one_active_base_trace_certificate.py`.  It freezes the
two exact identities and the factorial promotion tail; it does not replace
the analytic argument by simulation.
