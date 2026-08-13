# Independent hostile audit of the single-linkage level trace

**Audit date:** 2026-08-12 PDT  
**Frozen target:** `proof_first_single_linkage_level_trace_completion.md`  
**Audited SHA-256:**
`08c216dcf5926484e39edcab22df9ab119cd45f63f3f605154d6193a01c9f558`  
**Verdict:** **STRICT FAIL**

This is a proof audit, not an orientation or population enumeration.  The
target file was not edited.  Two explicit histories disprove its
load-bearing stopped inequalities.  There are also independent definition,
localization, handoff, and scope gaps.  No recurrence counterexample was
found; the corrected full-kernel theorem remains analytically plausible,
but it requires a different physical stop.

## 1. A full-rank deficiency-one test network

Use the five-complex support

\[
             {\cal C}=\{0,C,2C,A+C,B+C\}                       \tag{1.1}
\]

with unit-rate directed cycle

\[
  r_1:0\longrightarrow B+C,quad
  r_2:B+C\longrightarrow A+C,quad
  r_3:A+C\longrightarrow C,quad
  r_4:C\longrightarrow2C,quad
  r_5:2C\longrightarrow0.                                     \tag{1.2}
\]

It is binary, one-linkage, and strongly connected.  Relative to zero, the
complex vectors have rank three, so its deficiency is
\(5-1-3=1\).  The physical chain is irreducible on
\(\mathbb Z_{\ge0}^3\).  The following executable words generate the six
signed coordinate moves:

\[
\begin{array}{c|c}
r_1r_2r_4r_5&+A\\
r_1r_4r_5&+B\\
r_1r_2r_3&+C\\
r_1r_2r_3^2r_4r_5&-A\quad(A>0)\\
r_1r_2^2r_3^2r_4r_5&-B\quad(B>0)\\
r_4r_5&-C\quad(C>0).
\end{array}                                                    \tag{1.3}
\]

Thus the entrances below lie in one fixed closed irreducible class, not in
unrelated artificial classes.

At

\[
                    x_a=(a,b,0),                               \tag{1.4}
\]

the deterministic monomials of \(0,C,2C,A+C,B+C\) are
\(1,1,1,a,b\).  Whenever \(b=o(a)\), \(q=A+C\) is the unique disabled
top deterministic complex and zero is the only enabled source.  Since
\(2B\) is absent and \(B+C\) is present, the target note's scale is
\(m(b)=1+b=o(a)\).  Hence this is exactly its separated scope.

## 2. Fatal counterexample to Lemma 3.2

Take

\[
                         b=\lfloor a/\log a\rfloor             \tag{2.1}
\]

and \(\ell=0\).  At (1.4), the clean trace necessarily fires
\(r_1:0\to B+C\); this is its first \({\cal P}\)-target.  During the
subsequent cleanup Lemma 3.2 suppresses all \({\cal P}\)-source clocks.
The remaining clocks are further zero-source openings and
\(r_3:q\to C\).  The first \(r_3\)-firing completes the claimed old-
\(A\) service.  Its actual endpoint always satisfies

\[
                         A_D=a-1,\qquad B_D\ge b+1.             \tag{2.2}
\]

The carrier factorial and every further zero opening are nonnegative costs.
Consequently

\[
 G_0(X_D)-G_0(x_a)
       \ge-\log a+\log(b+1).                                  \tag{2.3}
\]

Because \(\log(b+1)\to\infty\), (2.3) contradicts (3.9) of the target,
which asserts the upper bound \(-\log a+C\).  It also directly contradicts
the claimed spectator estimate (3.11).

Put

\[
             \delta_a=\log{a\over b+1}\sim\log\log a.         \tag{2.4}
\]

Equation (2.3) gives \(G_0(X_D)\ge G_0(x_a)-\delta_a\).  Therefore

\[
 \mathbb E[W_0(X_D)-W_0(x_a)]
   \ge (G_0(x_a)-\delta_a)^4-G_0(x_a)^4
   \ge-4G_0(x_a)^3\delta_a.                                  \tag{2.5}
\]

Since \(\delta_a/\log a\to0\), (2.5) is incompatible with (3.10) for
every fixed positive \(c\).  The inference

\[
                       \log(b!)=o(\log(a!))                    \tag{2.6}
\]

does not repair the issue: (2.6) is a bulk comparison, while one newly
created spectator costs \(\log b\), which can be asymptotic to
\(\log a\).  On this history the clean reward is
\(-\log(a/b)+O(1)\), not \(-\log a+O(1)\).

There is a still sharper structural warning.  If a zero-source launch and
a \(q\)-exit both target \(B+C\), stopping after the first old-
\(A\) decrement can create two spectators.  Its raw factorial reward is
\(-\log a+2\log b+O(1)\), which can be positive under the allowed
condition \(b=o(a)\).  A correct episode must retain the physical carrier
closure or promotion rather than treating the first \(A\)-decrement as an
automatically good endpoint.

## 3. Fatal counterexample to the paid-stop estimate

The first-\({\cal P}\)-source stop in Lemma 4.1 also fails independently of
the clean estimate.  Keep (1.1)--(1.2), take

\[
                    b=\left\lfloor {a\over\sqrt{\log a}}\right\rfloor,
                    \qquad \ell=0.                             \tag{3.1}
\]

After the forced launch \(r_1\), the state is \((a,b+1,1)\).  The two
load-bearing clocks are

\[
 \begin{array}{c|c|c}
 hbox{reaction}&hbox{rate}&G_0hbox{-increment}\ \hline
 r_3:q\to C&a&-\log a+\log(b+1),\\
 r_2:B+C\to q&b+1&+\log(a+1).
 \end{array}                                                   \tag{3.2}
\]

The first line is the target's clean service and the second is its included
paid endpoint \(E\).  The other immediately enabled clocks have total rate
two.  Let

\[
                 \delta_a=\log{a\over b+1}
                         ={1\over2}\log\log a+o(1).            \tag{3.3}
\]

Every possible terminal history after this launch has
\(G_0(X_\tau)\ge G_0(x_a)-\delta_a\): a direct service attains the lower
scale, an extra zero launch adds a spectator and carrier, and each paid
endpoint has no larger negative factorial loss.  On the immediate
\(r_2\)-event, whose probability is

\[
                 {b+1\over a+b+3}\sim {1\over\sqrt{\log a}},  \tag{3.4}
\]

the increment is \(+\log(a+1)\).  The fourth-power finite difference
therefore gives, for large \(a\),

\[
 \mathbb E[W_0(X_{\tau_0})-W_0(x_a)]
 \ge cG_0(x_a)^3{\log a\over\sqrt{\log a}}
       -C G_0(x_a)^3\log\log a>0.                             \tag{3.5}
\]

This contradicts (4.4), not merely its claimed \(\log a\) magnitude.
The mechanism is exact: stopping a rare reverse carrier clock at its raw
positive endpoint pays probability \((b/a)\) times cost \(\log a\).  When
\(a/b\to\infty\) arbitrarily slowly, that can dominate the true clean gap.

If the process is continued instead, \(r_2\) is a neutral retry: it creates
a paired \(A+C\), and subsequent fast \(q\)-firings cancel that pair before
servicing old \(A\).  Thus (3.5) indicts the stopping rule, not recurrence.

## 4. Independent proof gaps

The counterexamples already decide the verdict.  The following gaps would
remain even after changing the drift scale.

### 4.1 The clean macro is not defined precisely enough

The target calls \(Q_a\) an embedded clean kernel obtained by deleting
exact population self returns.  Under the literal reaction-jump
interpretation, (3.7) is false.  For example, on the strong cycle

\[
                  0\to q\to C\to2C\to B+C\to0,               \tag{4.1}
\]

we have \(d=0,J=B\), and the nonself reaction \(0\to q\) neither kills nor
decreases \(J\).  If a macro instead means the full first return to
\(C=0\) or first \({\cal P}\)-target, that stopping time, state space,
diagonal inverse, and treatment of nested openings must be stated.

The displayed bound \(|J'-J|\le2\) is also not valid for such a collapsed
macro once nested zero-level insertions are retained.  What is plausible is
a uniform exponential increment moment below localization, not a
deterministic jump bound.

### 4.2 Lemma 3.1 uses the desired tail before localization

Only \(m(b)=o(a)\) is assumed at the entrance.  The proof controls nested
carrier progeny by asserting \(m(B)/a=o(1)\) along the trace, before the
Green tail controlling \(B\) has been established.  The moving level
\(L_a\) which would make this true is introduced only later in Section 4.
The noncircular order is: stop first below explicit \(B\)- and
\(C\)-localizations, prove the subcritical carrier and killed-Green bounds
there, and only then estimate the included boundary.

### 4.3 The endpoint estimate in Lemma 4.1 is not a kernel inequality

Equation (4.3) bounds only the terminal positive part at the first paid
clock.  The subsequent claim that the same bracket has a fixed negative
coefficient is false by Sections 2--3.  More generally, it does not state a
pointwise full-kernel supermartingale or Feynman--Kac inequality, so it does
not control cumulative interlacing of clean descents, neutral reverse
clocks, and nested carrier insertions.  The exact full all-clock kernel is
load-bearing here.

### 4.4 Localization and promotion are ordered inconsistently

Section 4 says to stop first at \(B=L_a\), including its crossing reaction.
Under the separated assumptions,

\[
 {L_a\over\sqrt a}\to0\quad(2B\hbox{ present}),\qquad
 {L_a\over a}\to0\quad(2B\hbox{ absent}).                    \tag{4.2}
\]

The promotion threshold in Section 5 is respectively of order
\(B\asymp\sqrt a\) or \(B\asymp a\).  A path stopped at \(L_a\) cannot
later reach that threshold.  The proof must either pay the included
\(L_a\)-endpoint and stop, or restart through explicit shells until
promotion; it cannot do both implicitly.

There is a second handoff problem.  A promotion can be crossed with
\(C>0\).  The balanced theorem cited in Section 5 starts at the physical
cofactor-free face \(C=0\), so it is not an immediate handoff for that
endpoint.  An open promotion needs its own cleanup or an all-active
generator/episode theorem.

### 4.5 Section 7 is a sketch, not the claimed remaining theorem

The two-disabled-top one-active case asserts bounded inactive population,
a geometric inverse, physical duration, and fourth-power drift in one
paragraph.  Arbitrary strong graphs can have repeated zero-level nested
openings, so these conclusions do not follow merely from the displayed
linear functional.  That scope needs an explicit stopped kernel with the
same endpoint and time estimates as the main case.

## 5. What the correct scale and local algebra say

The counterexamples rule out the frozen stopping rule, but they do not
produce a recurrence obstruction.  The natural local scale is the exact
deterministic monomial gap, not \(\log a\).  Write, at a localized open
state,

\[
 u=\log(A+e),\qquad v=\log(B+e),\qquad w=\log(C+e).            \tag{5.1}
\]

Up to a support- and \(\ell\)-dependent \(O(1)\), the factorial increments
of a \(q=A+C\)-sourced reaction are

\[
\begin{array}{c|rrrrrr}
q\to z&0&B&2B&C&2C&B+C\\ \hline
\Delta G_ell&-u-w&-u+v-w&-u+2v-w&-u&-u+w&-u+v.
\end{array}                                                    \tag{5.2}
\]

Before an exact open promotion, every displayed quantity is negative.
Its least magnitude is the actual source/target gap

\[
 h_q(A,B,C)=min_{q\to z}
     \log{(A+e)(C+e)\over (A+e)^{z_A}(B+e)^{z_B}(C+e)^{z_C}}, \tag{5.3}
\]

with harmless bounded corrections.  A correct chart stops or hands off
before \(h_q\) ceases to diverge.

The potentially positive \({\cal P}\)-source increments have much more
structure than the crude \(O(\log a+\log b)\) charge in (4.5):

\[
\begin{array}{c|c|c}
hbox{source}&hbox{source rate scale}&hbox{largest relevant positive costs}\\ \hline
C&C&u,\ v,\ 2v,\ w\\
2C&C^2&u-w,\ v-2w,\ 2v-2w\\
B+C&BC&u-v,\ v-w,\ w-v.
\end{array}                                                    \tag{5.4}
\]

In particular, the dangerous reverse \(B+C\to q\) costs only
\(u-v=\log(A/B)+O(1)\), not \(u=\log A+O(1)\).  If \(2B\) is absent, its
rate-times-cost divided by the corresponding \(q\)-scale is suppressed by
\(B/A\to0\).  If \(2B\) is present, put

\[
        g_2=\log{A+e\over(B+e)^2}\longrightarrow\infty.       \tag{5.5}
\]

Then \(B^2/A\to0\) implies

\[
 {B\over A}{\log(A+e)\over g_2}longrightarrow0,              \tag{5.6}
\]

because eventually \(B\le\sqrt A\) and
\(\log A/(\sqrt A,g_2)\to0\).  Thus even
\(B+C\to q\) or \(B+C\to2B\) cannot overwhelm an
\(AC\,g_2\) descending clock.  The pure-carrier sources are likewise
lower order after a carrier cutoff satisfying

\[
             {(1+C)\log(A+e)\over A h_q(A,B,C)}\longrightarrow0. \tag{5.7}
\]

Equations (5.2)--(5.7) are the rate-times-entropy comparison which the
frozen proof needs but does not use.  They show why an arbitrarily slow
tier gap is not itself an obstruction: the apparently dangerous reverse
clock carries either the same logarithmic gap at the smaller rate \(BC\),
or a larger raw logarithm multiplied by a source rate which is smaller by
at least a power allowed by (1.5).

## 6. Minimal analytic repair and outlook

A viable repair cannot merely replace every \(\log a\) in the frozen note
by \(\log(a/m(b))\).  Sections 2--3 show that the first-service and
first-paid-clock endpoints themselves can have the wrong sign.  The repair
must instead:

1. localize \(B\) and \(C\) before invoking subcritical nested-carrier
   bounds;
2. define the clean macro exactly as a first-return/first-level-change
   trace and prove an exponential, rather than bounded, nested increment
   estimate;
3. retain \({\cal P}\)-source reactions inside the physical regenerative
   kernel—especially neutral reversals such as \(B+C\to q\)—instead of
   stopping at their raw positive endpoints;
4. prove a pointwise full-kernel Lyapunov/Feynman--Kac inequality using the
   exact gaps (5.2)--(5.4);
5. stop only at a completed cofactor-free return with negative factorial
   reward, an included localization endpoint, or an actual open promotion
   with a proved same-\(W_\ell\) handoff; and
6. lift the resulting one-sided \(-h_q\) drift directly through the exact
   fourth-power identity.  Since \(G_\ell\asymp A\log A\), the quadratic
   remainder \(G_ell^2(\log A)^2\) is
   \(o(G_ell^3h_q)\) for every \(h_q\to\infty\); no gap comparable to
   \(\log A\) is required.

No rate-times-entropy reversal was found after making these corrections.
The full all-clock common-\(W_\ell\) theorem therefore remains plausible,
including when the deterministic gap tends to infinity arbitrarily slowly.
But the frozen SHA does not prove it, and its stated stopping time is
explicitly false on (1.1)--(1.2).

