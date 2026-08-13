# Localization and physical-time lift for the separated resolvent

**Proof-only interface lemma, 2026-08-12 PDT.**  This note records the
localization and holding-time consequences of the full phase-corrected
Green kernel.  It assumes the same-exponent, move-marked Green estimates
supplied by the completed-return/maximal-source proof.  It does not prove
that underlying clean Green theorem or the terminal entropy service
factor.  No certification flag is changed.

## 1. Green hypotheses and notation

Let (K=Q+R) be the localized augmented embedded kernel from
*proof_first_separated_first_mark_resolvent_lemma.md*.  It is killed at
service and at the included localization-causing reactions.  At an open
state its phase-corrected weight is

\[
       w_\theta(x,s)={e^{\theta G_\ell(x)}\over M_x(s)^\theta},
       \qquad 0<\theta<\tfrac12,                              \tag{1.1}
\]

and at a cofactor-free base the phase is (dB).  Put

\[
 F_\vartheta(k)=
       \exp\{\vartheta k\log(k+e)\},\qquad \vartheta>0.       \tag{1.2}
\]

The phrase **full same-exponent Green bound** below means that the Green
operator and its endpoint-marked version obey

\[
 (I-K)^{-1}w_\theta\le Cw_\theta,qquad
 \mathbb E_x\left[{F_\vartheta(B_\tau)\over F_\vartheta(b)}
                    \right]\le C,                            \tag{1.3}
\]

uniformly in the separated parameter.  The second estimate is the
spectator marginal of the first, with the bounded phase divisor and the
maximal-source corrector retained.  It must include the causing endpoint;
an occupation estimate stopping immediately before the crossing would not
suffice.

At every localized open state put

\[
 \delta_a=max_{y\ne q}{M_x(y)\over M_x(q)}=o(1),qquad
 \eta=\min\{\theta,1-\theta\}.                               \tag{1.4}
\]

The first-mark phase calculation gives

\[
 \|K_{OO}\|_{w_\theta}\le C,qquad
 \|K_{OO}^{,2}\|_{w_\theta}\le C\delta_a^\eta.             \tag{1.5}
\]

Indeed a phase-(q) sourced firing can be free once, but it sets a lower
phase.  From a lower phase, a (q)-firing costs (O(\delta_a^\theta)),
while a lower-source mark costs (O(\delta_a^{1-\theta})).

## 2. Spectator localization and relative divisor moments

Fix (M>0).  Stop at and include the first reaction for which

\[
                  {F_\vartheta(B)\over F_\vartheta(b)}
                              \ge a^M.                        \tag{2.1}
\]

Call this endpoint event \({\cal B}_B\).

### Lemma 2.1 (exponent-slack boundary estimate)

For every (0<\alpha<1),

\[
 \mathbb E_x\left[
   \left({F_\vartheta(B_\tau)\over F_\vartheta(b)}\right)^\alpha;
       {\cal B}_B\right]
       \le C a^{-M(1-\alpha)}.                               \tag{2.2}
\]

The same estimate holds with any fixed polynomial in
((1+B_\tau)/(1+b)) inserted, after replacing (1-\alpha) by a smaller
positive number.

#### Proof

On \({\cal B}_B\), writing
(Z=F_\vartheta(B_\tau)/F_\vartheta(b)), one has

\[
                         Z^\alpha\le a^{-M(1-\alpha)}Z.       \tag{2.3}
\]

Take expectations and use the endpoint-marked estimate (1.3).  For a
fixed (r) and every \(\beta>0\), convex growth of
(k\log(k+e)) gives

\[
 \left({1+k\over1+b}\right)^r
       \le C_{r,\beta}
       \left\{1+left({F_\vartheta(k)\over
                            F_\vartheta(b)}\right)^\beta\right\}.
                                                                    \tag{2.4}
\]

Choose \(\beta<1-\alpha\) and repeat (2.3) with
\(\alpha+\beta\). \(\square\)

The same pointwise comparison without the boundary indicator proves the
scale-relative endpoint moments

\[
 \mathbb E_x\left[
       \left({1+B_\tau\over1+b}\right)^r\right]\le C_r.      \tag{2.5}
\]

In particular, for the base divisor
({\cal M}(z)=(1+z_B)^d),

\[
 \mathbb E_x\left[
       \left({{cal M}(X_\tau)\over{cal M}(x)}\right)^r
                 \right]\le C_r.                             \tag{2.6}
\]

This is exactly the relative moment required by the corrected-to-raw
Hölder transform; no power of the initial scale is lost.

## 3. Cofactor localization

Fix (0<\varepsilon<1), put

\[
                             L_C=\lceil a^\varepsilon\rceil, \tag{3.1}
\]

and stop at and include the first reaction for which (C\ge L_C).  Call
this event \({\cal B}_C\).

### Lemma 3.1 (superpolynomial corrected (C)-boundary)

For every fixed (N),

\[
 \mathbb E_x\left[
   {w_\theta(X_\tau,s_\tau)\over w_\theta(x,dB)};
        {\cal B}_C\right]\le C_Na^{-N}.                      \tag{3.2}
\]

#### Proof

A base launch creates at most two cofactor molecules.  Each later reaction
changes (C) by at most two.  Thus an excursion reaching (L_C) before a
cofactor-free return contains at least

\[
                         n_C=\left\lceil{L_C-2\over2}\right\rceil
                                                                    \tag{3.3}
\]

open transitions.  By (1.5), grouping them in pairs gives corrected weight
at most

\[
 C\sum_{n\ge n_C}
       (C\delta_a^\eta)^{\lfloor n/2\rfloor}
 \le C(C\delta_a^\eta)^{n_C/2}.                              \tag{3.4}
\]

For all large (a), (C\delta_a^\eta<1/2); since
(n_C\asymp a^\varepsilon), (3.4) is smaller than (a^{-N}) for every
fixed (N).  The causing transition is one of the counted transitions,
so its actual endpoint is included.  Summing over arbitrarily many prior
completed base excursions multiplies (3.4) by the bounded full base Green
factor in (1.3), and proves (3.2). \(\square\)

Lemma 3.1 does not claim that \(\mathbb P({\cal B}_C)\) is small.  For
example, a clean supercritical (q\)-branch may reach the cutoff with high
probability while making a very favorable active-factorial decrement.
What is superpolynomially small is its **corrected endpoint weight**, which
is the quantity needed for the subsequent raw positive-endpoint bound.

Suppose, as in the full polynomial endpoint hierarchy, that every fixed
polynomial in the remaining localized coordinates has at most a fixed
power of (a) as its endpoint moment.  Combining (2.2), (3.2), the
relative moment (2.6), and Hölder at a smaller exponent then gives, for
either boundary and every fixed polynomial endpoint mark (P),

\[
 \mathbb E_x[e^{\theta'\Delta G}P(X_\tau);{cal B}_B\cup{cal B}_C]
       =O(a^{-N'})                                            \tag{3.5}
\]

after choosing (M) sufficiently large and (0<\theta'<\theta).  On the
(B)-boundary, (2.2) supplies an arbitrarily large inverse power against
those fixed polynomial moments.  On the (C)-boundary, (3.2) already
supplies every inverse power.  A boundary outcome with
\(G_\ell(X_\tau)\le G_\ell(x)\) has no positive (W_\ell)-cost and may be
discarded before applying this estimate.
Consequently the positive (W_\ell)-weighted boundary error is
(o(G_\ell(x)^3h)).

## 4. Physical holding times

Let \(\xi_n\) be the augmented embedded chain before killing, (N) its
number of transitions, (H_n) the physical holding time before transition
(n), and

\[
                              T=\sum_{n<N}H_n.                 \tag{4.1}
\]

At a nonfrozen cofactor-free base, maximal source degree (d) gives

\[
 \Lambda(\xi)\ge
 \begin{cases}
  c(1+B)^d,&d\ge1,\\
  c,&d=0,
 \end{cases}                                                  \tag{4.2}
\]

after the finite compact states are absorbed into the strong-cut
corrector.  At an open state, localization keeps (A\asymp a), and the
(q)-clock gives

\[
                             \Lambda(\xi)\ge caC.             \tag{4.3}
\]

All other clocks only shorten the holding time.  Conditional on the
current state and the chosen reaction, (H_n) is exponential with rate
\(\Lambda(\xi_n)\) and is independent of the reaction label.  Hence

\[
 h_j(\xi):=\mathbb E_\xi H_n^j={j!\over\Lambda(\xi)^j}
 \le C_j\begin{cases}
 (1+B)^{-dj},&\xi\hbox{ base},\ d\ge1,\\
 1,&\xi\hbox{ base},\ d=0,\\
 (aC)^{-j},&\xi\hbox{ open}.
 \end{cases}                                                  \tag{4.4}
\]

### Lemma 4.1 (time-marked Green recursion)

Let

\[
                         U_p(\xi)=\mathbb E_\xi T^p,
                         \qquad U_0\equiv1.                  \tag{4.5}
\]

Then

\[
 U_p=(I-K)^{-1}\left[
 h_p+\sum_{j=1}^{p-1}{p\choose j}h_{p-j}KU_j
                         \right].                            \tag{4.6}
\]

Consequently every polynomial or scale-relative additive-functional Green
bound for (K) propagates inductively to the same class of fixed moments
of physical duration.

#### Proof

At the first embedded transition, write

\[
              T=H_0+\mathbf1_{\{\text{continuation}\}}T'     \tag{4.7}
\]

and expand the (p)-th power.  The term containing ((T')^p) is (KU_p).
Independence of the exponential holding time and the reaction label makes
the remaining terms (h_p) and
({p\choose j}h_{p-j}KU_j).  Move (KU_p) to the left and apply the
killed resolvent.  Equation (4.4) and induction in (p) prove the final
claim. \(\square\)

For the present maximal-source trace, its polynomial Green hierarchy and
the first-mark resolvent identity give, for every fixed (p),

\[
 \mathbb E_xT^p\le C_p(1+b)^{c_p}.                            \tag{4.8}
\]

The sharper additive rewards in (4.4) retain the scale improvement:
base time is charged by ((1+B)^{-d}) (or by a bounded reward when
(d=0)), and every open transition is charged by at most (a^{-1}).
Thus any scale-relative version of the polynomial Green hierarchy gives
the corresponding scale-relative duration moments without an additional
power of (a).

## 5. Exact scope and necessary qualification

A single inequality ((I-K)^{-1}w_\theta\le Cw_\theta), by itself, does
not imply all moments of the killing time: a family of killed kernels can
have uniformly bounded first Green mass but unbounded higher lifetime
moments.  The duration conclusion uses the **time-marked/polynomial Green
hierarchy** through (4.6).  In the separated proof this hierarchy comes
from the maximal-source descent, the compact strong-cut inverse, and the
same first-mark Neumann contraction; it must not be replaced by the lone
zeroth-order corrected estimate.

Subject to that necessary interpretation of “full corrected Green,”
Sections 2--4 prove the scale-relative divisor moments, included weighted
boundary estimates, and physical-duration moment lift required by the
terminal common-(W_\ell) argument.
