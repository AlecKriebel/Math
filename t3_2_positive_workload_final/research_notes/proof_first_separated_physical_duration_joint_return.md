# Physical duration for the separated joint-return episode

**Proof-first interface lemma, 2026-08-12 PDT.**  This note proves the
physical-time estimate for the repaired separated stopping rule.  It uses
the clean completed-base Green hierarchy audited in
`proof_first_separated_clean_base_green_audit.md` (SHA-256
`96c72e11a6105013b8d7b6e2309da7c2dbebccfa0b72640bfb3cfe6cf1608b36`)
and the physical first-mark decomposition of
`proof_first_separated_first_mark_resolvent_lemma.md` (SHA-256
`d4c4baff29ffda942798f28fc69d4b30ab25ee2c8e13d1960a4ee20b6d772506`).
It does not use an unweighted terminal spectator moment.  Such a moment is
false for a critical carrier genealogy and is unnecessary for physical
time.

## 1. Stopping convention and localized domain

Put

\[
 q=A+C,\qquad
 \{q\}\subseteq {\cal C}
 \subseteq\{0,B,2B,C,2C,B+C,q\}.                    \tag{1.1}
\]

Start at a cofactor-free state \(x=(a,b,0)\).  At \(C=0\), repeat only
clean completed returns having active loss \(k=0\).  Stop a clean
completed return with \(k\ge1\) as service.  If a lower-sourced reaction
fires while \(C>0\), mark its first occurrence, retain every physical
clock thereafter, and stop at the next actual return to \(C=0\) or at an
included open boundary.  Thus the marked episode never begins another
base macro.  All boundary-causing reactions are included.
The exact invariant/no-history alternative isolated by the clean strong
cut is routed separately; the present lemma concerns the complementary
killed branch.  A frozen base is already terminal.

Let \(m(B)=1+B^p\), with the usual harmless replacement by \(1+B\) when
the largest present spectator degree is one, and put

\[
 h=\log {a\over m(b)}\longrightarrow\infty,
 \qquad \varepsilon_a=e^{-h/2}.                     \tag{1.2}
\]

Before the included open boundary assume

\[
 {a\over2}<A<2a,\qquad
 {m(B)\over A}<\varepsilon_a,\qquad
 {C\over A}<\varepsilon_a.                          \tag{1.3}
\]

The last two inequalities imply, uniformly over every lower complex
\(y\ne q\),

\[
 {\lambda_y(X)\over\lambda_q(X)}\le C\varepsilon_a. \tag{1.4}
\]

Here \(\lambda_q\) is the aggregate propensity of all nontrivial
\(q\)-sourced reactions.  Every such reaction has the same \(AC\)
factor, and strong connectivity gives it a positive fixed aggregate rate.
The comparisons for the possible lower sources are respectively
\(1/(AC),B/(AC),B^2/(AC),1/A,C/A,B/A\).  A zero-vector reaction may be
deleted because it does not change the CTMC.

## 2. Embedded length of one open excursion

Let \(\nu\) be the number of physical state-changing reactions in one
open excursion, beginning just after its launch and ending with the
included return or boundary reaction.  This excursion may be clean, may
contain the first mark and arbitrarily many later marks, and may have a
critical or supercritical carrier genealogy.

### Lemma 2.1 (active-coordinate clock)

For every fixed integer \(r\ge1\),

\[
                         \mathbb E\nu^r\le C_r a^r.          \tag{2.1}
\]

#### Proof

At every preterminal open state, (1.4) gives

\[
 \mathbb P\{\hbox{next source is }q\mid{\cal F}_n\}
       \ge {1\over1+C\varepsilon_a}.                         \tag{2.2}
\]

Every nontrivial \(q\)-sourced reaction lowers \(A\) by exactly one,
because \(q\) is the only complex in (1.1) containing \(A\).  A
lower-sourced reaction raises \(A\) by at most one, and does so only when
its target is \(q\).  Thus, for all sufficiently large \(a\),

\[
 \mathbb E[A_{n+1}-A_n\mid{\cal F}_n]\le-\kappa             \tag{2.3}
\]

with a fixed \(\kappa>0\), while \(|A_{n+1}-A_n|\le1\).
More quantitatively, for a sufficiently small fixed \(t>0\),

\[
 \mathbb E[e^{t(A_{n+1}-A_n)}\mid{\cal F}_n]
 \le {e^{-t}+C\varepsilon_a e^t\over1+C\varepsilon_a}
 \le e^{-\gamma}                                             \tag{2.4}
\]

for a fixed \(\gamma>0\).

On \(\{\nu>n\}\), the lower active boundary has not been reached, so
\(A_n>a/2\), whereas the launch has \(A_0\le a+1\).  Iterating (2.4)
up to \(n\wedge\nu\) therefore gives

\[
 \mathbb P\{\nu>n\}
       \le \min\{1,\exp(Cta-\gamma n)\}.                    \tag{2.5}
\]

Tail summation proves (2.1).  Stopping earlier at \(C=0\), at the
spectator/cofactor threshold, or at the upper active boundary can only
decrease \(\nu\).  No carrier population or terminal spectator moment
enters this argument. \(\square\)

The point of Lemma 2.1 is that carrier criticality concerns the number of
offspring before an untruncated extinction.  In the physical localized
episode, each \(q\)-reaction spends one active molecule, while the rare
lower clocks replenish at most one.  The active coordinate is therefore a
uniformly drifting reaction counter even when the carrier offspring law is
critical.

## 3. Physical time of one open excursion

Let \(T_O\) be the physical duration of the excursion in Section 2.  At
every preterminal open state, \(A\ge a/2\) and \(C\ge1\), so

\[
                       \Lambda(X)\ge cAC\ge ca.              \tag{3.1}
\]

Conditional on the embedded states and reaction labels, the holding times
are independent exponentials with their corresponding total rates.  For
an integer \(r\ge1\), Minkowski's inequality and (3.1) give

\[
 \mathbb E[T_O^r\mid X_0,\ldots,X_{\nu-1}]
       \le C_r\left({\nu\over a}\right)^r.                  \tag{3.2}
\]

Combining (3.2) with Lemma 2.1 proves

\[
                         \boxed{\mathbb E T_O^r\le C_r.}     \tag{3.3}
\]

This includes the holding time immediately preceding the reaction which
crosses a boundary.  Nothing is charged after its actual endpoint.

## 4. Repeated cofactor-free returns

Let \(N_B\) be the number of contracted clean \(k=0\) base trials before
service, the first mark, localization, or a frozen state.  At \(C=0\), a
clean \(k=0\) macro is only

\[
              cB\longrightarrow jB,
 \qquad\hbox{or}\qquad
              cB\longrightarrow q\longrightarrow jB,       \tag{4.1}
\]

with \(c,j\le d\).  Hence every such open portion contains exactly one
open reaction.  Literal population returns have the uniformly bounded
directed-cut inverse from the audited clean theorem and consequently add a
geometric block with all fixed moments.

Here the clean audit gives a direct, unweighted macro-count estimate; no
spectator endpoint estimate is being inferred from its exponential
weight.  After literal returns are contracted, a maximal \(dB\)-source
trial has a fixed probability of either being killed or strictly lowering
\(B\).  This is the directed cut from the audited proof.  A trial sourced
at \(cB\), \(c<d\), has probability
\(O((1+B)^{c-d})\), and every continuing displacement is bounded by two.
Consequently, outside a fixed compact set,

\[
 \mathbb P\{\hbox{kill or }\Delta B\le-1\mid B\}\ge\epsilon,
 \qquad
 \mathbb P\{\Delta B>0\mid B\}\le {C\over1+B}.              \tag{4.2}
\]

For a sufficiently small fixed \(t>0\), (4.2) gives a substochastic
exponential contraction

\[
 \mathbb E[e^{t(B_{n+1}-B_n)};,n+1<N_B\mid{\cal F}_n]
                         \le e^{-\gamma}                     \tag{4.3}
\]

at large \(B\).  On the remaining finite set, the same strong cut gives
the corresponding contraction after a fixed number of trials.  Grouping
those trials into blocks and iterating as in (2.5) yields

\[
                 \mathbb P\{N_B>n\}\le C e^{tb-\gamma' n},
 \qquad
                 \mathbb E N_B^r\le C_r(1+b)^r.             \tag{4.4}
\]

When \(d=0\), every continuing \(k=0\) return is literal, so (4.4)
follows directly from its geometric directed-cut inverse.  Thus (4.4)
concerns only the bounded, nonbranching \(k=0\) kernel and makes no claim
about the terminal population of a long carrier branch.

At a nonfrozen base, some nontrivial pure source is enabled.  Since the
graph and rate vector are fixed and an enabled falling factorial is at
least one,

\[
                              \Lambda(X)\ge c.                \tag{4.5}
\]

More sharply it is at least \(c(1+B)^d\) outside a fixed compact set, but
the constant lower bound suffices here.  Conditional exponential-moment
bounds, (4.2), and the geometric literal-return blocks imply, for the
total base holding time \(T_B\),

\[
 \mathbb E T_B\le C(1+b),
 \qquad
 \mathbb E T_B^r\le C_r(1+b)^r.                             \tag{4.6}
\]

The one open holding time in each preceding \(k=0\) macro has rate at
least \(ca\); its sum satisfies the same bounds and is smaller than the
base contribution.  There is at most one terminal long open excursion,
whose moments are bounded by (3.3).

## 5. Duration conclusion and Foster scale

Let \(\tau\) be the complete separated episode described in Section 1.
Equations (3.3) and (4.6) prove, for every fixed integer \(r\ge1\),

\[
 \boxed{
 \mathbb E_x\tau\le C(1+b),\qquad
 \mathbb E_x\tau^r\le C_r(1+b)^r.}                         \tag{5.1}
\]

In the separated regime, \(m(b)=o(a)\).  If \(p=1\), this gives
\(b=o(a)\); if \(p=2\), it gives \(b=o(a^{1/2})\); and if \(p=0\), the
spectator is constant after classwise reduction.  For every fixed linear
factorial correction,

\[
 G_\ell(a,b,0)\ge c a\log a
\]

for all sufficiently large entrances.  Since \(h\to\infty\), (5.1)
therefore yields

\[
                  \mathbb E_x\tau
                         =o\bigl(G_\ell(x)^3h\bigr).          \tag{5.2}
\]

Thus physical duration is strictly lower order than the separated
fourth-power service drift.  The proof remains valid for a critical
Galton--Watson clean carrier: the false unweighted terminal \(B\)-moment
is nowhere invoked.

## 6. Exact scope

This lemma proves only the duration interface for the stated joint-return
stopping rule.  It assumes the audited clean base Green hierarchy and the
open dominance localization used by the phase-resolvent theorem.  It does
not itself prove the corrected entropy transform or the weighted
probability of the included open boundary.
