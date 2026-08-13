# Clean completed-base Green audit for the separated carrier

**Independent hostile proof audit, 2026-08-12 PDT.**  This note audits the
clean completed-return ledger and its same-exponent killed base Green
operator.  It uses no support, orientation, or population enumeration.
Open lower-sourced firings, physical duration, localization estimates, and
the fourth-power Foster lift are outside its scope.

**Verdict: PASS, with one endpoint-moment correction.**  The ledger

\[
                        \Delta B\le pk+(d-c)                 \tag{0.1}
\]

is valid, including the exceptional case (d=0,p=1).  After literal
population self-returns are contracted, the clean (k=0) base kernel has
a same-exponent factorial Green bound.  However, a generic unweighted
scale-relative terminal moment for (B) is false because the clean carrier
genealogy may be critical.  No such moment is needed: on service paths,
(0.1) makes every polynomial divisor ratio a polynomial in (k), which is
absorbed by a small loss in the exponential service factor.

## 1. Exact completed-word balance

Use the notation

\[
 q=A+C,
 \quad
 {cal F}={\cal C}\cap\{0,B,2B\},
 \quad
 d=\max_{cB\in{cal F}}c,
 \quad
 p=\max_{y\in{cal C}\setminus\{q\}}y_B.             \tag{1.1}
\]

A clean macro starts at (C=0) with one reaction sourced at (cB\in
{cal F}), then, while (C>0), uses only (q)-sourced reactions, and
ends at the first return to (C=0).  Let (e\in\{0,1\}) indicate that
the base target is (q), let (T) be the number of subsequent
(q)-firings, and put

\[
                         k=A_0-A_\tau.                        \tag{1.2}
\]

Only the base firing can increase (A), and it does so exactly when
(e=1); every (q)-firing decreases (A) by one.  Therefore

\[
                         k=T-e\ge0.                           \tag{1.3}
\]

The inequality follows because return to (C=0) is impossible after an
entry to (q) without at least one (q)-firing.

Let the base target have (B)-degree (j_0\le p), and let the (T)
(q)-targets have (B)-degrees (j_1,\ldots,j_T\le p).  The exact
spectator balance is

\[
                   \Delta B=-c+j_0+\sum_{i=1}^Tj_i.          \tag{1.4}
\]

If (e=1), then (j_0=0), so (1.3)--(1.4) give

\[
             \Delta B\le-c+pT=pk+(p-c).                     \tag{1.5}
\]

When (p>d), necessarily (p=1,d=0): if (p=2), the only lower complex
with (B)-degree two is (2B\in{cal F}), forcing (d=2); if (p=1)
and (B\in{cal F}), then (d=1).  Thus the only (e=1,p>d) case is
(p=1,d=c=0).  Here a (B+C) target has (C)-degree one, while the
initial target (q) contributes one carrier.  Returning to (C=0)
requires that the number of (C)-free (q)-targets dominate the number
of (B+C) targets.  Since (T=1+k), at most (k) of the targets can be
(B+C), and therefore

\[
                         \Delta B\le k.                       \tag{1.6}
\]

This is exactly (0.1) for (p=1,d=c=0).

If (e=0), the base target is lower.  At (C=0) it must itself be in
({\cal F}), hence (j_0\le d).  Equations (1.3)--(1.4) then give

\[
                   \Delta B\le -c+d+pk.                      \tag{1.7}
\]

Equations (1.5)--(1.7) prove (0.1) in all cases.

## 2. The decisive (k=0) simplification

Suppose (k=0).  Then (T=e).  Carrier balance at the completed return
forces every lower target in the word to have (C)-degree zero.  Hence a
clean (k=0) macro is exactly one of

\[
              cB\longrightarrow jB,
 \qquad
              cB\longrightarrow q\longrightarrow jB,        \tag{2.1}
\]

with (c,j\le d\).  In particular,

\[
                          \Delta B=j-c,                       \tag{2.2}
\]

so its jump is bounded by two.  If (c=d), a nonself macro has (j<d)
and strictly decreases (B).  Equality (j=d) is a literal population
self-return.  If (d=0), every (k=0) return is literal self-return;
after contraction the killed kernel is identically zero.  This includes
the case (d=0,p=1), so the presence of (B+C) creates no hidden neutral
base move.

## 3. Same-exponent killed Green drift

Let (u=B) at the base and let (Q\) be the embedded clean base-return
kernel, restricted to (k=0), after literal population self-returns have
been contracted.  Service paths (k\ge1) are killing outcomes.  Use the
same-exponent weight

\[
                  \Phi_\theta(u)=\exp\{\theta u\log(u+e)\},
             \qquad 0<\theta<1.                              \tag{3.1}
\]

At a large base, a source (cB) has rate of order (u^c), whereas a
present maximal source (dB) has rate of order (u^d).  A (k=0)
macro from source (cB) has the bounded displacement (j-c\le d-c).
Consequently its embedded probability times its weight ratio is bounded
by

\[
 C u^{c-d}\,{\Phi_\theta(u+j-c)\over\Phi_\theta(u)}
       \le C u^{-(1-\theta)(d-c)}.                    \tag{3.2}
\]

For every (c<d), the right side tends to zero.  For (c=d), every
nonself surviving return strictly decreases (u), and a decrement by one
has

\[
                  {\Phi_\theta(u-1)\over\Phi_\theta(u)}
                    \le C u^{-\theta}.                       \tag{3.3}
\]

It remains to control repeated exact returns.  Consider the exact-return
block generated by (dB) and (q).  Strong connectivity supplies a first
directed edge leaving this proper block.  If its source is (dB), its
conditional probability among (dB)-sourced edges is fixed and positive.
If its source is (q), the common (q)-propensity cancels and the same is
true.  Any finite path inside the two-node block has a fixed product of
such identical-source conditional probabilities.  Hence there is a
support- and rate-dependent (\varepsilon>0) such that each contracted
maximal-source trial has probability at least (\varepsilon) of leaving
the exact-return block.  The literal-self-return diagonal inverse is thus
at most (\varepsilon^{-1}), uniformly in (u).

Upon leaving the block, a completed (k=0) outcome strictly lowers (B),
whereas every other completed outcome has (k\ge1) and is killed.  Combining
this fixed cut with (3.2)--(3.3) gives, outside a fixed compact set,

\[
                         Q\Phi_\theta(u)\le\rho\Phi_\theta(u)
 \qquad\hbox{for some }\rho<1.                       \tag{3.4}
\]

On the remaining finite set, a state with no enabled source is a frozen
singleton.  Otherwise strong connectivity gives a finite positive-
probability path to killing or to the exterior drift region.  The finite
killed Green corrector therefore yields a weight
(\widehat\Phi_\theta\asymp\Phi_\theta) satisfying

\[
                 (I-Q)^{-1}\widehat\Phi_\theta
                       \le C\widehat\Phi_\theta.              \tag{3.5}
\]

This is a same-exponent estimate; no loss from (\theta) to a smaller
exponent is needed in the base Green step.

## 4. Why an unweighted terminal ratio moment is false

The clean carrier population need not have uniform polynomial moments.
For example take

\[
             {\cal C}=\{0,2C,B+C,q\}                         \tag{4.1}
\]

and include the directed edges

\[
 0\to q,
 \qquad q\to0,\ q\to2C,\ q\to B+C,
 \qquad 2C\to q,
 \qquad B+C\to q,                                           \tag{4.2}
\]

with the three (q)-outgoing rates equal and any positive fixed rates on
the other displayed edges.  Add edges if desired to make the graph
strong; they are irrelevant to the clean (q)-only macro.  Starting from
((a,0,0)), the clean carrier genealogy generated by (q)-firings has
offspring count (0,2,1), each with probability (1/3).  It is a critical
Galton--Watson process.  Its total progeny has the classical
(n^{-3/2}) point-mass scale, and the number of unary (B+C) outcomes is
of the same order as total progeny on typical long trees.  The physical
constraint (A\ge0) merely truncates the tree at order (a).  Thus for
fixed (r>1/2),

\[
                 \mathbb E(1+B_\tau)^r
                       \gtrsim a^{r-1/2}                      \tag{4.3}
\]

along a subsequence, up to harmless constants.  In particular a bound

\[
       \mathbb E\left[{1+B_\tau\over1+B_0}\right]^r\le C_r  \tag{4.4}
\]

cannot be asserted without localization or an exponential service tilt.
This counterexample does not affect (3.5): here (d=0), so the artificial
base divisor equals one and the (k=0) nonself kernel is empty.

## 5. Joint absorption replaces the false moment

For (d>0), no standalone endpoint-ratio moment is needed either.  On a
service path, (0.1) gives

\[
 {M_{X_\tau}(dB)\over M_x(dB)}
       \le C\left(1+{pk+d\over1+u}\right)^d
       \le C(1+k)^{d}.                               \tag{5.1}
\]

Any fixed power of this ratio is polynomial in (k).  The clean service
ledger supplies an exponential factor (e^{-c\theta k h}), where the
tier gap (h\to\infty).  For every (r<\infty) and every
(0<\theta'<\theta),

\[
       (1+k)^r e^{-c\theta kh}
              \le C_{r,\theta,\theta'}
                    e^{-c\theta'kh}                         \tag{5.2}
\]

uniformly once (h\ge1).  Therefore the polynomial divisor incurred when
converting the corrected terminal transform back to the raw factorial
transform is absorbed jointly by an arbitrarily small exponent slack.

Critical or near-critical clean genealogies can also occur when (d>0),
but (5.2) controls precisely the service-weighted quantity actually used
in the terminal transform.  What fails is only the stronger, unnecessary
unweighted moment (4.4).

## 6. Strict scope boundary

This note proves the clean ledger and the killed (k=0) same-exponent base
Green estimate.  It also identifies and repairs the endpoint-moment
interface.  It does not prove the separate phase-corrected open-mark
resolvent, included-boundary estimates, duration, or the final common-
(W^4) drift.
