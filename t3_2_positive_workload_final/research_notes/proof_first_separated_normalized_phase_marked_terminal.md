# Normalized-phase marked-terminal lemma

**Proof-first interface lemma, 2026-08-12 PDT.**  This note proves raw
factorial-exponential control of the first marked separated excursion at
its next completed cofactor-free return.  It also controls the included
boundary on which \(q=A+C\) ceases to dominate because \(A\), \(B\), or
\(C\) leaves its moving tube.  No unweighted spectator moment is used.

The inputs are the clean completed-base Green theorem and the sourcewise
phase table.  Duration, the completed-base spectator cutoff, and the final
fourth-power lift are outside the strict conclusion.

## 1. Normalized phase weight

At an open state (x=(A,B,C)), (C>0), attach the target phase (s) as
in the phase-corrector construction: a lower target (z) sets (s=z),
and a lower-to-(q) entry sets (s=q).  Put

\[
 M_x(y)=\prod_i(x_i+1)^{y_i},
 \qquad
 {\cal M}(x)=M_x(dB)=(1+B)^d,                              \tag{1.1}
\]

where (d) is the maximal cofactor-free (B)-degree.  For fixed
(0<\theta<1/2), define

\[
 V_\theta(x,s)=e^{\theta G_\ell(x)}
                 \left({{\cal M}(x)\over M_x(s)}\right)^\theta
       \quad(C>0),
 \qquad
 V_\theta(x)=e^{\theta G_\ell(x)}\quad(C=0).                \tag{1.2}
\]

Thus the corrected weight agrees **exactly** with the raw exponential on
every completed base return.  This is the only normalization change from
the earlier phase weight (e^{\theta G}/M(s)^\theta).

One reaction changes (B) by at most two, so

\[
                        {{\cal M}(x')\over{\cal M}(x)}\le C \tag{1.3}
\]

uniformly for every reaction endpoint (x').  Consequently multiplying
the old phase weight by ({\cal M}(x)^\theta) changes every one-step
comparison by only a fixed constant.

## 2. The phase table is unchanged

Work in a localized open tube where

\[
 A\asymp a,
 \qquad
 \delta=\sup_{x,y\ne q}{M_x(y)\over M_x(q)}=o(1).            \tag{2.1}
\]

Write (r_y=M_x(y)/M_x(q)).  If (y\to z) is an enabled reaction and
(x'=x+z-y), bounded-degree factorial comparison gives

\[
 {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
 e^{\theta(G_\ell(x')-G_\ell(x))}
       \le C r_y^{1-\theta}r_z^\theta                       \tag{2.2}
\]

for (y\ne q), while the same expression for (y=q) is at most
(Cr_z^\theta).  The target divisor cancels (r_z^\theta), and (1.3)
controls the new numerator.  Therefore

\[
 {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
 {V_\theta(x',s')\over V_\theta(x,s)}
 \le
 \begin{cases}
 C r_y^{1-\theta}r_s^\theta,&y\ne q,\\
 C r_s^\theta,&y=q.
 \end{cases}                                                \tag{2.3}
\]

If (x') is a base, its target is (jB) with (j\le d); resetting from
the target phase to the raw base weight removes the factor
\({\cal M}(x')/M_{x'}(jB)\ge1\).  Hence (2.3) remains an upper bound at the
completed endpoint.

From a lower phase, the corrected one-step open row has mass
(O(\delta^\theta)).  From phase (q), one (q)-exit may have order-one
mass, but it sets a lower phase; recurrent lower-to-(q) competitors cost
(O(\delta^{1-\theta})).  Thus the open Green bridge has uniformly
bounded (V_\theta)-norm.

## 3. Moving dominance tube

At an entrance (x=(a,b,0)), put

\[
 \varepsilon_a={1+b^p\over a}=e^{-h_a},
 \qquad h_a\longrightarrow\infty,
 \qquad \bar\delta_a=\sqrt{\varepsilon_a}=e^{-h_a/2}.       \tag{3.1}
\]

For (p=0), interpret the spectator condition below as vacuous.  Stop and
include the first reaction crossing

\[
 A\notin[a/2,2a],\qquad
 C\ge c_0\bar\delta_a a,
 \qquad\hbox{or}\qquad
 1+B^p\ge c_0\bar\delta_a a,                                \tag{3.2}
\]

where the fixed (c_0>0) is chosen small enough for the (q)-clock to
dominate throughout the pre-jump tube.  There

\[
 \max_{y\ne q}{M_x(y)\over M_x(q)}\le C\bar\delta_a,
 \qquad C\bar\delta_a^\eta<\tfrac14,
 \qquad \eta=\min\{\theta,1-\theta\},                       \tag{3.3}
\]

for all large (a).  The first inequality follows by checking the six
possible lower monomial scales

\[
 {1\over AC},\quad {B\over AC},\quad {B^2\over AC},
 \quad {1\over A},\quad {C\over A},\quad {B\over A}.         \tag{3.4}
\]

The moving tube is strictly wider than the entrance scale because
\(\varepsilon_a/\bar\delta_a=\sqrt{\varepsilon_a}\to0\).  It also remains
macroscopic enough for a long-path boundary estimate: since
\(\varepsilon_a\ge a^{-1}\),

\[
 \bar\delta_a a\ge a^{1/2},
 \qquad
 (\bar\delta_a a)^{1/p}\ge a^{1/(2p)}\quad(p=1,2).           \tag{3.5}
\]

When \(p\ge1\), also stop at a completed \(C=0\) return if

\[
                  1+B^p\ge {c_0\over2}\bar\delta_a a.        \tag{3.6}
\]

This completed-base guard ensures that every subsequently opened excursion
starts a fixed distance below the open spectator boundary in (3.2).

## 4. Exact first-mark episode

At a cofactor-free base, repeat clean completed returns with active loss
(k=0).  A clean completion with (k\ge1) is terminal service (S).
If, while (C>0), the first reaction sourced below (q) fires, mark that
physical reaction but do not stop.  Continue the full physical open chain,
including every later lower-sourced firing, until its next (C=0) return
or the included boundary (3.2).  Call a completed marked return (E).

Let (Q) be the localized clean substochastic kernel and (R) the first
open lower-source operator.  The clean completed-base theorem and the open
phase bridge give

\[
                  \|(I-Q)^{-1}\|_{V_\theta}\le C.           \tag{4.1}
\]

Here the base restriction of \(V_\theta\) is the raw exponential.  The
clean \(k=0\) base proof applies at that weight without a divisor:
maximal-source nonself returns decrease \(B\), while a positive move from
source degree \(c<d\) has probability \(O(B^{c-d})\), which pays its raw
factorial tilt.  Literal self-returns have the uniform strong-cut inverse.

At the first mark, (2.3) gives

\[
                  \|R\|_{V_\theta}
                    \le C\bar\delta_a^{1-\theta}.            \tag{4.2}
\]

After the mark, let (K_{OO}) be the full physical open kernel, containing
both (q)- and lower-sourced reactions and killed at the first base return
or boundary.  From a lower phase its row norm is
(O(\bar\delta_a^\theta)).  From phase (q), one (q)-exit may be free,
but it sets a lower phase, while a recurrent lower-to-(q) step costs
(O(\bar\delta_a^{1-\theta})).  Therefore

\[
              \|K_{OO}^{\,2}\|_{V_\theta}
                    \le C\bar\delta_a^\eta,
 \qquad
              \|(I-K_{OO})^{-1}\|_{V_\theta}\le C.         \tag{4.3}
\]

The strong Markov decomposition at the first mark is thus

\[
 (\hbox{clean pre-mark Green})\;R\;(I-K_{OO})^{-1}.
                                                                    \tag{4.4}
\]

This is the exact stopping rule: after the mark, the operator terminates at
the next (C=0) return and does not continue through another base episode.
There is no bound on the number or nesting depth of later open marks.

Both the entrance and every endpoint in (E) have (C=0), so (1.2) and
(4.1)--(4.4) give the raw terminal estimate

\[
 \boxed{
   \mathbb E_x\!\left[e^{\theta(G_\ell(X_\tau)-G_\ell(x))};E\right]
       \le C\bar\delta_a^\eta
       =C e^{-\eta h_a/2}.}                                  \tag{4.5}
\]

No terminal spectator moment is used.  A critical carrier genealogy is
already summed inside the open resolvent.

A clean service requires one nonfree (q)-step: if the base target is
lower, its first (q)-step starts in a lower phase; if the base target is
(q), active loss (k\ge1) requires a second (q)-step after the free
exit.  Hence the same argument gives

\[
 \boxed{
   \mathbb E_x\!\left[e^{\theta\Delta G};S\right]
       \le C\bar\delta_a^\theta
       =C e^{-\theta h_a/2}.}                                \tag{4.6}
\]

## 5. Included dominance boundary

Let

\[
 L_a=\min\left\{a,\ \bar\delta_a a,\
          (\bar\delta_a a)^{1/p}:p\ge1\right\}.             \tag{5.1}
\]

A base launch changes every coordinate by at most two.  The entrance is
an \(o(1)\) fraction of the completed-base guard (3.6).  After literal
self-returns are contracted, every clean \(k=0\) base continuation changes
\(B\) by at most two.  The same-exponent raw base kernel has contraction
\(\rho<1\).  Reaching (3.6) therefore requires \(\Omega(L_a)\) contracted
base moves and has raw endpoint-weighted mass at most
\(C\rho^{cL_a}\).

If the process opens before hitting (3.6), its spectator coordinate starts
below half the open threshold in (3.2).  Every later reaction again has
bounded displacement.  Reaching any boundary in (3.2) then requires at
least \(cL_a\) open transitions.  By (3.5),

\[
                         L_a\ge c a^{1/4}.                   \tag{5.2}
\]

Grouping the open path in pairs and using (4.3), then summing the bounded
pre-opening base Green, bounds the corrected mass of an included open
boundary path by

\[
                   C(C\bar\delta_a^\eta)^{cL_a/2}.           \tag{5.3}
\]

At its first crossing endpoint all coordinates are (O(a)).  Moreover

\[
 {e^{\theta G_\ell(X_\tau)}\over V_\theta(X_\tau,s_\tau)}
 =\left({M_{X_\tau}(s_\tau)\over{\cal M}(X_\tau)}\right)^\theta
 \le Ca^{2\theta}.                                          \tag{5.4}
\]

The same ratio equals one at the completed-base guard and if an open
crossing reaction lands at \(C=0\).  Any
fixed polynomial endpoint mark costs only another fixed power of (a).
Equations (5.2)--(5.4) therefore imply, for every fixed (N) and fixed
polynomial (P),

\[
 \boxed{
 \mathbb E_x\!\left[e^{\theta\Delta G}P(X_\tau);
             \text{included dominance boundary}\right]
       \le C_Na^{-N}.}                                      \tag{5.5}
\]

This includes a (q\to2B) crossing which lands directly at (C=0): it
is either a completed service/marked endpoint or a literal return, and a
crossing far from the entrance still requires the preceding
(\Omega(L_a)) bounded jumps.

Thus (5.5) includes both the completed-base guard (3.6) and the open
dominance boundary (3.2).  No open phase-divisor conversion and no
unweighted \(B\)-moment enter.

## 6. Scope boundary

Equations (4.5)--(4.6) prove the raw exponential interface for completed
marked and clean-service endpoints.  Equation (5.5) proves the weighted
included dominance-boundary estimate.  The physical-time marked Green
recursion and the one-sided lift to the common (G_\ell^4) workload remain
separate interfaces.
