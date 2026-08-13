# Rejected separated repair and bounded two-top lemma

**Rejected separated repair; bounded two-top candidate, 2026-08-12 PDT.**
This note audits two seams
in *proof_first_single_linkage_level_trace_completion.md*, frozen at
SHA-256
08c216dcf5926484e39edcab22df9ab119cd45f63f3f605154d6193a01c9f558.

The frozen file is not edited here. **The separated Theorem 1.1 below is
false with its stop-at-first-paid-source rule.** The counter-race is
recorded in Section 1.1. Sections 3--7, the bounded two-disabled-top
theorem, do not use that estimate and remain a separate candidate.

1. its moving localization must be a terminal, already-paid endpoint of the
   current episode; the later fixed-scale promotion is a **router
   classification**, not a continuation after that stopping time;
2. its claimed \(-\log a\) clean margin is false at mesoscopic spectator
   scales and must be replaced by the exact logarithmic monomial gap; and
3. its two-disabled-top paragraph is replaced below by a complete
   arbitrary-orientation bounded-carrier theorem.

The cutoff issue is a logical seam. The entropy scale and first-paid-source
rule are genuine failed claims. The two-top paragraph is a genuine missing
proof. No flag is changed.

## 1. The corrected separated scale

At a cofactor-free entrance \((a,b,0)\), put

\[
 m(b)=
 \begin{cases}
  1+b^2,&2B\in{\cal C},\\
  1+b,&2B\notin{\cal C},\
        {\cal C}\cap\{B,B+C\}\ne\varnothing,\\
  1,&B,2B,B+C\notin{\cal C},
 \end{cases}
 \qquad
 h(a,b)=\log{a\over m(b)}.                                    \tag{1.1}
\]

The separated tier premise is \(h(a,b)\to\infty\).

The full \(-\log a\) margin in the frozen Lemma 3.2 is false. On the strong
cycle

\[
                  0\to B+C\to A+C\to C\to2C\to0              \tag{1.2}
\]

with \(b=a/\log a\), a clean service can add one spectator molecule. Its
factorial entropy decrement is

\[
                        -\log a+\log b+O(1)
                           =-\log\log a+O(1).                  \tag{1.3}
\]

Thus the correct uniform quantity is \(h\), or the sharper
reaction-specific source/target monomial gap. No proof can replace \(h\)
by \(\log a\) at arbitrary separated scales.

### Rejected Theorem 1.1 (first-paid-source stopping)

Fix the separated support

\[
 \{A+C\}\subseteq{\cal C}
 \subseteq\{0,B,2B,C,2C,B+C,A+C\},                            \tag{1.4}
\]

an arbitrary strong orientation, positive rates, a closed irreducible
class, and fixed \(\ell\). Along every cofactor-free sequence
\((a,b,0)\) with \(h(a,b)\to\infty\), there is an included all-reaction
stopping time \(\sigma\) such that

\[
 \mathbb E_{(a,b,0)}[
 W_\ell(X_\sigma)-W_\ell(a,b,0)+\sigma]
       \le-cG_\ell(a,b,0)^3h(a,b).                            \tag{1.5}
\]

Its terminal partition is clean service, included cofactor-source firing,
or included moving localization. The latter is returned to the global
router. Invariant and frozen alternatives are unchanged.

### Proof

Use the frozen exact level \(H=A-C\) and maximal-source trace
\(J=B+dC\), but replace its clean entropy lemma as follows. Pair every
zero-level lower-to-\(A+C\) entry with its first \(A+C\)-exit. These pairs
telescope. The first unpaired exit has a lower target of spectator degree
at most \(d\), so its factorial increment is

\[
                  -\log a+\log m(k)+O(1)                     \tag{1.6}
\]

at the actual spectator level \(k\). A dominant \(J\)-decrease contributes
\(-c\log(k+e)\); a positive move loses one source degree and has normalized
probability \(O(k^{-1})\).

Apply the fourth power **macro by macro**, not once to the terminal
increment. At a decrease macro the actual \(W_\ell\)-loss is
\(-cG_\ell^3\log(k+e)\). Its positive lower-degree alternatives have
conditional expectation at most
\(CG_\ell^3\log(k+e)/k\), plus lower fourth-power remainders. Thus they are
absorbed locally for large \(k\); the finite levels are handled by the
compact Green corrector. At a killing macro, (1.6) gives
\[
 \mathbb E[\Delta W_\ell\mid\mathcal F_\nu,\hbox{killing macro}]
       \le-cG_\ell^3\log{a\over m(k)}.                         \tag{1.7}
\]
If the trace has reached \(k<b\), this gap is at least \(h(a,b)\). Positive
upcrossings are retained in their own macro estimates or stopped at the
moving boundary. Telescoping the actual \(W_\ell\)-increments over the
killed Green trace therefore preserves both the service gap and every
large favorable spectator decrease.

Now restore the cofactor-bearing sources \(C,2C,B+C\). At level \(k\),
their ordered race against \(A+C\) is \(C(1+k)/a\). A paid positive jump
has entropy cost at most

\[
             C\{\log a+\log(k+e)\}.                           \tag{1.8}
\]

If the clean macro has a killing probability bounded below, its margin is
the reaction-specific gap
\(\log(a/m(k))\). The paid ratio times that same gap is
\[
 {1+k\over a}\log{a\over m(k)}
       =o\!\left(\log{a\over m(k)}\right).                    \tag{1.9}
\]
If the macro instead has a fixed \(J\)-decrease probability, its clean
margin is \(\log(k+e)\). Below the moving localization,
\[
 {\,k\log a\,\over a\log(k+e)}\longrightarrow0.               \tag{1.10}
\]
Ordered Green summation of (1.8)--(1.10) therefore preserves a fixed
fraction of the macrowise killing/decrease bracket. The quadratic and
higher positive fourth-power remainders at a bounded reaction jump are
smaller by \(O(\log(a+k)/G_\ell)=o(1)\) on each macro. Carrier families
have the Green moments, so the same conclusion holds after their exact
return inverse. Telescoping the macro increments proves (1.5), apart from
the moving endpoint, which is paid by the exponential Green tail exactly
as in the frozen proof. \(\square\)

### 1.1 Counter-race to the proposed payment

The preceding proof incorrectly treats a cofactor-source entry as a
one-jump paid error. In the cycle (1.2), after the launch
\(0\to B+C\), the reaction \(B+C\to A+C\) races the \(A+C\)-clock. Its
probability is

\[
                         r\asymp {b\over a}=e^{-h}.             \tag{1.11}
\]

If it is stopped and charged at its post-jump endpoint, it has just raised
\(A\) by one and costs \(+\log a+O(\log b)\). Take

\[
                b={a\over\sqrt{\log a}},\qquad
                h={1\over2}\log\log a.                        \tag{1.12}
\]

Then

\[
                         r\log a\asymp\sqrt{\log a}\gg h.       \tag{1.13}
\]

Thus (1.9) multiplies the race probability by the wrong jump cost. A
positive entry costs \(\log a\), not the eventual entry-exit gap. The
proposed Theorem 1.1 is false with this stopping rule.

The necessary repair is structural. A
\({\cal P}\to A+C\) reaction must be retained as a nested carrier entry,
assigned one pending allowance, and paired with its first subsequent
\(A+C\)-exit. Only the completed pair may be cancelled. The full all-clock
carrier genealogy must be resummed before any residual endpoint is charged.
A first-insertion Feynman--Kac estimate cannot prove the
arbitrary-slow-\(h\) theorem.

## 2. Audit of the moving-cutoff/promotion seam

The frozen proof localizes at the included crossing

\[
 L_a=
 \begin{cases}
 a^{1/4}\sqrt{b+1},&2B\in{\cal C},\\
 \sqrt{a(b+1)},&2B\notin{\cal C}.
 \end{cases}                                                  \tag{1.1}
\]

It then begins Section 5 with “After the moving localization” and speaks
of continuing to

\[
                         m(B)\ge\varepsilon A.                 \tag{1.2}
\]

Taken literally as one physical episode, these instructions are
incompatible: an included first crossing of \(L_a\) has already stopped
the episode, and \(L_a\) remains strictly inside the separated scale.

There is no reason to continue within that episode. The frozen Green bound
already proves

\[
 \mathbb E_x[
   (W_\ell(X_\sigma)-W_\ell(x))^+;\ B_\sigma\ge L_a]
       =o\!\left(G_\ell(x)^3h(a,b)\right),                    \tag{2.3}
\]

where the crossing reaction is included. Combined with the clean service
and ordered paid-source estimates, (1.3) gives the full stopped inequality

\[
 \mathbb E_x[
 W_\ell(X_\sigma)-W_\ell(x)+\sigma]
       \le-cG_\ell(x)^3h(a,b)                                 \tag{2.4}
\]

for the episode which terminates at service, paid source, or moving
boundary. Thus the moving boundary is already paid and should simply be
returned to the global physical router.

### Lemma 2.1 (the moving endpoint is routable)

Let \(Y\) be an actual post-reaction endpoint at (1.1).

1. If \(C(Y)>0\), every divergent endpoint sequence has an enabled
   top-D source. In particular \(A+C\) is enabled, and any pure or
   cofactor source which dominates it is enabled as well. The ordinary
   generator-good rule applies.
2. If \(C(Y)=0\), then \(A(Y)=a+O(1)\), \(B(Y)=L_a+O(1)\), and the endpoint
   is another separated entrance:
   \[
   {B(Y)^2\over A(Y)}\longrightarrow0
       \quad(2B\in{\cal C}),\qquad
   {B(Y)\over A(Y)}\longrightarrow0
       \quad(2B\notin{\cal C}).                               \tag{1.5}
   \]
   The same stopped theorem may therefore be applied anew from the actual
   endpoint.
3. If a later router state satisfies (1.2), independently of how many
   earlier episodes occurred, it is classified directly as an
   enabled-pure-top or balanced-two-top state.

#### Proof

At an open endpoint, all top candidates in the separated support are
enabled except a \(B+C\) source when \(B=0\); in that case its monomial is
only \(C\), while \((A+C)\)'s is \(AC\). Hence the deterministic top meets
the enabled set.

At a cofactor-free clean crossing, the exact level \(A-C=a\) gives
\(A(Y)=a\), up to the bounded causing jump. From (1.1),

\[
 {L_a^2\over a}={b+1\over\sqrt a}\to0
       \quad\hbox{when }b^2/a\to0,                            \tag{1.6}
\]

and

\[
 {L_a\over a}=\sqrt{(b+1)/a}\to0
       \quad\hbox{when }b/a\to0.                              \tag{1.7}
\]

This proves (1.5). At (1.2), a present \(B\) or \(2B\) is enabled at the
top scale. If neither supplies the scale, the definition of the separated
scale forces \(B+C\) to be present and \(B\asymp A\), which is the balanced
chart. \(\square\)

### Proposed textual repair

The publishable version should:

* define the local terminal partition as service, paid
  \({\cal P}\)-source, or included moving boundary;
* remove promotion from the same stopping time;
* replace frozen Section 5 by Lemma 1.1; and
* leave fixed-scale promotion to the global post-endpoint router.

No recursive continuation has to be hidden inside one stopping time.
Successive moving-boundary episodes are handled by the strong Markov
composition. Nonexplosion and the common-\(W_\ell\) decrement rule out
finite-time accumulation.

## 3. The two-disabled-top setting

Let

\[
                    q_B=A+B,\qquad q_C=A+C,\qquad
 {\cal P}=\{B,C,2B,2C,B+C\}.                                 \tag{2.1}
\]

Fix a one-linkage support

\[
 \{q_B,q_C\}\subseteq{\cal C}
      \subseteq\{0,q_B,q_C\}\cup{\cal P},                    \tag{2.2}
\]

an arbitrary strong directed graph, and arbitrary positive rates. Start
from the exact no-fast face

\[
                              x_n=(n,0,0).                     \tag{2.3}
\]

The linear level

\[
                              H=A-B-C                         \tag{2.4}
\]

has complex weight zero on \(0,q_B,q_C\), weight \(-1\) on \(B,C\), and
weight \(-2\) on \(2B,2C,B+C\).

> **Theorem 3.1 (bounded two-top all-clock service).** In one fixed closed
> irreducible class, exactly one of the following holds.
>
> 1. If \(0\notin{\cal C}\), the state (2.3) is absorbing. Its class is a
>    singleton.
> 2. If \({\cal C}\cap{\cal P}=\varnothing\), \(H\) is invariant. The
>    cofactor-free part of a fixed class contains at most one state
>    \((n,0,0)\).
> 3. If \(0\in{\cal C}\) and
>    \({\cal C}\cap{\cal P}\ne\varnothing\), there is an included
>    all-reaction stopping time \(\tau_n\) such that, for every fixed
>    \(p\),
>    \[
>    \begin{aligned}
>     \mathbb P(E_n)&\le C/n,\\
>     \mathbb E[(1+|X_{\tau_n}-x_n|+\tau_n)^p;E_n]&\le C_p/n,\\
>     \mathbb E(1+\tau_n)^p&\le C_p,                          \tag{2.5}\\
>     A_{\tau_n}&=n-1,\quad B_{\tau_n}+C_{\tau_n}\le3
>          \quad\hbox{on }E_n^c.
>    \end{aligned}
>    \]
>    Here \(E_n\) is the included first non-designated lower-source
>    competitor during an open carrier window. For every fixed
>    \(\ell\in\mathbb R^3\),
>    \[
>     \mathbb E_{x_n}[
>       W_\ell(X_{\tau_n})-W_\ell(x_n)+\tau_n]
>        \le-cG_\ell(x_n)^3\log n                             \tag{2.6}
>    \]
>    for all large \(n\).

The theorem is uniform over \(n\), not over graphs or rate vectors; its
constants may depend on the fixed graph and rates.

## 4. Clean attempt kernel

Assume item 3 of Theorem 3.1. At the empty face, the only enabled source is
\(0\). Let

\[
 \lambda_0=\sum_{0\to z}\kappa_{0z}>0.                        \tag{3.1}
\]

Choose a simple directed path in the complex graph from \(0\) to its first
vertex in \({\cal P}\). Before its terminal vertex, the path lies in

\[
                              \{0,q_B,q_C\}.                   \tag{3.2}
\]

Simplicity prevents a return to \(0\), so after the initial edge every
intermediate source is \(q_B\) or \(q_C\). Starting with one carrier, this
path is physical: after a reaction \(y\to z\), the next source \(z\) is
present with the same residual population.

Temporarily suppress new \(0\)-firings while a top carrier is open. A
single carrier moves on the finite transient graph
\(\{q_B,q_C\}\), with absorption in \(0\) or \({\cal P}\). Conditional on
the current top source, its outgoing probabilities are independent of
\(n\), because all outgoing clocks share the same falling-factorial source.
The chosen simple path therefore has probability at least

\[
                               p_*>0                           \tag{3.3}
\]

in each attempt. The number of internal top reactions has a phase-type
law with every moment. Its physical duration has moments \(O(n^{-p})\).

An attempt which absorbs at \(0\) has returned to the exact population
\((n,0,0)\). Repeat attempts until a target in \({\cal P}\) occurs. Exact
neutral attempts are summed by a geometric inverse with parameter at least
\(p_*\). Each visit to the empty face waits an exponential time of rate
\(\lambda_0\). Consequently the attempt count and total clean duration
have every fixed moment.

Strong connectivity is used here only through the simple path and the
finite directed cut. No orientation list is inspected.

## 5. Physical competitors and old-cloud service

Assume item 3 of Theorem 3.1. At the empty face, the only enabled source is
\(0\). Let

\[
 \lambda_0=\sum_{0\to z}\kappa_{0z}>0.                        \tag{4.1}
\]

Restore the \(0\)-clock during an open top phase. Its rate is
\(\lambda_0\), whereas a one-carrier top clock has rate at least \(cn\).
For a phase-type number of top events,

\[
 \mathbb P\{\hbox{a new \(0\)-firing before clean absorption}\}
       \le C/n.                                               \tag{4.2}
\]

Stop at and include that firing.

At a clean \({\cal P}\)-target, the inactive population has molecularity
one or two and the old \(A\)-population equals \(n\). At least one of
\(q_B,q_C\) is enabled. Follow the physical top carrier until its first
exit to a lower complex. Top-to-top conversions preserve \(A\); the first
top-to-lower exit lowers \(A\) by exactly one. Its conditional event count
is phase type and its duration has moments \(O(n^{-p})\).

During this cleanup, every non-top source belongs to
\(\{0\}\cup{\cal P}\). The inactive population before the first top exit
is at most two, so its aggregate rate is bounded. Against the \(cn\) top
rate, the competitor probability is \(O(n^{-1})\). Stop at and include its
actual firing. A causing binary jump leaves a bounded inactive endpoint
and changes \(A\) by at most one.

Summing (4.2) and the cleanup estimate over the geometric attempts proves
(2.5). On the clean event, a possible initial \(0\to q\) entry and its
first exit cancel in \(A\); the unpaired carrier supplied by the first
\({\cal P}\)-target then exits. Hence

\[
                   A_{\tau_n}=n-1,\qquad
                   B_{\tau_n}+C_{\tau_n}\le3.                 \tag{4.3}
\]

Every physical clock has either been retained as a designated clock or
has caused the included endpoint \(E_n\).

## 6. Entropy and common fourth power

Let

\[
 G_\ell(x)=K_\ell+\sum_{i=A,B,C}\log(x_i!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4.                                     \tag{5.1}
\]

On the clean event, (4.3) gives

\[
                     G_\ell(X_{\tau_n})-G_\ell(x_n)
                          \le-\log n+C_\ell.                  \tag{5.2}
\]

At the included competitor endpoint, populations differ from the current
clean phase by a bounded jump, and the number of preceding neutral attempts
has geometric moments. Thus

\[
 \mathbb E[
   |G_\ell(X_{\tau_n})-G_\ell(x_n)|^p;E_n]
       \le {C_{p,\ell}(\log(n+e))^p\over n}.                  \tag{5.3}
\]

Equations (2.5), (5.2), and (5.3) imply

\[
 \mathbb E[
 G_\ell(X_{\tau_n})-G_\ell(x_n)+\tau_n]
       \le-\tfrac12\log n                                    \tag{5.4}
\]

for all large \(n\).

Since \(G_\ell(x_n)\asymp n\log n\), the exact fourth-power identity gives

\[
 \begin{aligned}
 \mathbb E[W_\ell(X_{\tau_n})-W_\ell(x_n)]
 &=4G_\ell(x_n)^3\,\mathbb E\Delta G_\ell\\
 &\quad+6G_\ell(x_n)^2\,\mathbb E(\Delta G_\ell)^2
   +4G_\ell(x_n)\,\mathbb E(\Delta G_\ell)^3
   +\mathbb E(\Delta G_\ell)^4.                              \tag{5.5}
 \end{aligned}
\]

The last three terms are
\(O(G_\ell(x_n)^2(\log n)^2)\), lower order than
\(G_\ell(x_n)^3\log n\). The duration moments are lower order as well.
This proves (2.6). \(\square\)

## 7. Exact replacement scope

Theorem 3.1 replaces the frozen paragraph beginning “If both \(A+B\) and
\(A+C\) are disabled top complexes.” It proves the required alternatives
without support or orientation enumeration:

* absent \(0\): frozen face;
* absent lower target: exact \(A-B-C\) invariant on the no-fast face;
* present \(0\) and lower target: geometric bounded carrier service with
  included \(O(n^{-1})\) competitors and common-fourth-power drift.

Together with the terminal moving-boundary repair in Section 1, it supplies
a logically consistent patch for both audited seams. The frozen 08c file
should not be called publication-ready until these replacements are applied
and replayed.
