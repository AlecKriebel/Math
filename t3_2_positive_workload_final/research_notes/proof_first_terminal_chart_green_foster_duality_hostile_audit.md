# Hostile audit: terminal-chart Green/Foster duality

**Proof-only audit, 2026-08-12 PDT.**  This note tests the proposed use of
the certified fixed-state killed reaction-count Green occupation to compose
different local Foster potentials.  It does not change any finite atlas or
network classification.

## 1. Exact verdict

There are two inequivalent meanings of “uniformly integrable positive
endpoints.”

1. Uniform moments of the **positive local episode increment**
   \((V(X_\tau)-V(x))^+\), together with uniform duration moments, do **not**
   suffice.  Even after adding properness, a uniform negative all-clock
   episode drift, positive terminal-chart occupation, and zero normalized
   structural-exit flux, the claimed contradiction is false.
2. Uniform integrability of the value of the incoming local potential on
   the **chart-entry and defect endpoints**, with respect to their normalized
   boundary subprobability measures, does suffice.  This is a strictly
   stronger cross-chart hypothesis.  It is exactly the condition that makes
   the weighted boundary toll vanish.

The existing both-available and Bellman/Flat0 estimates prove the first
notion.  The certified killed Green theorem and finite-chart circulation
prove only that the unweighted boundary mass tends to zero.  Neither result
proves the second notion.  Thus the proposed terminal-chart composition,
without a global common potential or a new weighted-boundary estimate, has
a load-bearing gap.

## 2. A fixed-state killed-Green counterexample

Consider the discrete-time chain on

\[
 E=\{o\}\mathbin\cup\{U_n,D_n:n\ge1\}
\]

with transitions

\[
 \begin{split}
 o&\longrightarrow U_1,\\
 U_n&\longrightarrow U_{n+1}\quad\hbox{with probability }{n\over n+1},\\
 U_n&\longrightarrow D_n\quad\hbox{with probability }{1\over n+1},\\
 D_n&\longrightarrow D_{n-1}\quad(n\ge2),\\
 D_1&\longrightarrow o.
 \end{split}                                                    \tag{2.1}
\]

All displayed transitions have bounded displacement in the level
coordinate.  The chain is irreducible.  It may also be made a nonexplosive
CTMC by giving every state total rate one and using (2.1) as its embedded
kernel.

Let \(H\) be the height at which the up phase switches to the down phase.
The probability of reaching \(U_n\) is

\[
       \prod_{j=1}^{n-1}{j\over j+1}={1\over n},
\]

and hence

\[
               \mathbb P(H=n)={1\over n(n+1)}.             \tag{2.2}
\]

The positive return time is \(1+2H\).  It is finite almost surely but has
infinite mean.  This is therefore a literal fixed-state infinite-mean-return
chain of the kind to which the certified killed Green construction applies.

Take the exhaustion

\[
 D_M=\{o\}\mathbin\cup\{U_n,D_n:1\le n\le M\}
\]

and kill at return to \(o\) or exit from \(D_M\).  Write
\(\mathsf H_M=\sum_{n=1}^M1/n\).  The expected transition counts before
killing are

\[
 \begin{array}{c|c}
 \hbox{source type}&\hbox{expected count}\\ \hline
 o&1\\
 U&\mathsf H_M\\
 D&\displaystyle\sum_{n=1}^M{n\over n(n+1)}
       =\mathsf H_{M+1}-1.
 \end{array}                                                 \tag{2.3}
\]

Consequently the Green normalizer is

\[
                 t_M=\mathsf H_M+\mathsf H_{M+1}\longrightarrow\infty,
                                                                  \tag{2.4}
\]

and the down chart carries nonzero limiting transition occupation:

\[
 {\mathsf H_{M+1}-1\over t_M}\longrightarrow{1\over2}.       \tag{2.5}
\]

The entry count \(U_n\to D_n\), summed over \(n\le M\), has expectation
\(M/(M+1)\).  The only outgoing chart transition is \(D_1\to o\), with
the same expectation.  Both counts divided by \(t_M\) tend to zero.  Thus
the down-phase node is a positive-mass terminal strongly connected
component of the limiting finite phase graph with zero unweighted entry
and exit flux.  Its occupation also escapes every finite subset because
the expected count at each fixed \(D_j\) is bounded while \(t_M\to\infty\).

## 3. A perfect local Foster episode still does not contradict it

On the down chart put

\[
                         V(D_n)=n,
 \qquad V(o)=V(U_n)=0.                                  \tag{3.1}
\]

Restricted to the down chart, \(V\) is nonnegative and proper.  Use one
ordinary jump as the episode.  At every down-chart start,

\[
                 V(X_1)-V(X_0)=-1                         \tag{3.2}
\]

including \(D_1\to o\).  In the rate-one CTMC version, if \(\tau\) is
the next holding time, then

\[
       \mathbb E_{D_n}[V(X_\tau)-V(D_n)+\tfrac12\tau]
                         =-\tfrac12.                      \tag{3.3}
\]

The episode has all physical clocks, one embedded jump, all duration
moments, and

\[
                 (V(X_\tau)-V(D_n))^+=0.                  \tag{3.4}
\]

Thus its positive endpoint increment is uniformly integrable in the
strongest possible way.  Replacing \(V(n)=n\) by \(V(n)=n^2\) even makes
the negative drift tend to minus infinity; the same obstruction remains.

The missing quantity is the value of the newly selected potential at a
rare entry.  Its normalized expectation is

\[
 \begin{aligned}
 {1\over t_M}\mathbb E\sum_{U_n\to D_n}V(D_n)
 &= {1\over t_M}\sum_{n=1}^M{n\over n(n+1)}\\
 &= {\mathsf H_{M+1}-1\over t_M}
   \longrightarrow {1\over2}.                            \tag{3.5}
 \end{aligned}
\]

This is exactly the toll which pays for the normalized down-chart drift
\(-1/2\).  A vanishing number of entries can carry a nonvanishing, or even
diverging, amount of an unbounded local potential.

This also exhibits the Banach-limit/downward-shift obstruction directly.
For fixed \(R\), let \(V_R=V\wedge R\).  The bounded-test Green identity
sees only the finitely many down levels at which \(V_R\) changes, so

\[
        \lim_{M\to\infty}\sum\nu_M\,\Delta V_R=0.          \tag{3.6}
\]

Taking \(R\to\infty\) afterwards still gives zero, whereas integrating the
untruncated one-step drift first gives \(-1/2\).  Uniform integrability of
the **positive increments** does not justify interchanging these limits;
the lost term is the starting-value tail in (3.5).

The example also refutes the assertion that every positive-mass terminal
chart separately inherits nonnegative physical workload flux from the
global killed endpoint balance.  Here the down chart has level flux
\(-1/2\), the up chart has the compensating positive flux, and the phase
switches have zero normalized count.  Endpoint nonnegativity constrains the
sum over the whole killed path, not each zero-count-separated terminal
component.

## 4. The exact corrected boundary-toll lemma

The valid abstract statement is elementary once its missing hypothesis is
made explicit.

> **Lemma 4.1 (terminal episode runs with weighted boundary control).**
> For each \(M\), let
> \(Y^M_0,Y^M_1,\ldots,Y^M_{N_M}\) be a finite adapted macroepisode path,
> where \(N_M\) is a stopping index for the macroepisode filtration, and
> let \(a_M\to\infty\) be its normalization.  Fix a chart
> \(C\), a function \(V:E\to[0,\infty)\) which is proper on \(C\), and let
> \[
> I_M=\{0\le k<N_M:Y^M_k\in C\}
> \]
> be the good episode starts.  Suppose every such episode has an
> integrable actual endpoint and, conditionally on its start,
> \[
> \mathbb E\!\left[V(Y^M_{k+1})-V(Y^M_k)+c^M_k
>                    \mid\mathcal F^M_k\right]\le-\delta   \tag{4.1}
> \]
> for a fixed \(\delta>0\) and nonnegative costs \(c^M_k\).
> Let \(B_M\subset I_M\) contain the first index of every consecutive run
> of indices in \(I_M\).  If
> \[
> \liminf_M {\mathbb E|I_M|\over a_M}=\alpha>0             \tag{4.2}
> \]
> and
> \[
> {1\over a_M}\mathbb E\sum_{k\in B_M}V(Y^M_k)
>                       \longrightarrow0,                  \tag{4.3}
> \]
> then these paths cannot exist.

### Proof

Group the good indices pathwise into their maximal consecutive runs
\([r,s]\).  Exact telescoping and \(V\ge0\) give

\[
 \begin{aligned}
 \sum_{k\in I_M}\{V(Y^M_{k+1})-V(Y^M_k)\}
 &=\sum_{[r,s]}\{V(Y^M_{s+1})-V(Y^M_r)\}\\
 &\ge-\sum_{r\in B_M}V(Y^M_r).                         \tag{4.4}
 \end{aligned}
\]

For a deterministic \(m\), truncate the displayed sums to \(k<m\).  Since
\(N_M\) is a stopping index, the good-start indicator is measurable at the
episode start.  Endpoint integrability permits conditional summation of
(4.1).  Combining that finite conditional sum directly with the pathwise
run inequality gives

\[
 \delta\,\mathbb E|I_M\cap\{0,\ldots,m-1\}|
 \le \mathbb E\sum_{r\in B_M,\ r<m}V(Y^M_r).           \tag{4.5}
\]

Letting \(m\to\infty\) uses monotone convergence on both nonnegative sides.
Dividing by \(a_M\) and using (4.2)--(4.3) yields
\(0\ge\delta\alpha>0\), a contradiction.
\(\square\)

The same proof allows an \(o(a_M)\) family of bad, exit, or cut episodes:
break a run at each such index and include the value at the following good
start in the boundary sum (4.3).  A fixed finite exceptional set contributes
only \(o(a_M)\) provided its one-episode successors have bounded expected
\(V\)-value.  Completing the single episode which straddles a killed-path
cut contributes another \(o(a_M)\) term when its positive endpoint increment
is uniformly integrable.  These are cut-overshoot controls; they do not
imply (4.3).

## 5. Precisely sufficient endpoint uniform integrability

Define the normalized chart-boundary subprobability measure

\[
 \beta_M(A)={1\over a_M}\mathbb E
        \sum_{k\in B_M}{\bf1}\{Y^M_k\in A\}.              \tag{5.1}
\]

Finite-chart circulation and zero structural-exit flux can prove
\(\beta_M(E)\to0\).  The additional condition actually needed is

\[
 \lim_{R\to\infty}\limsup_{M\to\infty}
       \int_{\{V>R\}}V\,d\beta_M=0.                       \tag{5.2}
\]

Indeed,

\[
       \int V\,d\beta_M
       \le R\beta_M(E)+\int_{\{V>R\}}V\,d\beta_M,         \tag{5.3}
\]

so (5.2) and \(\beta_M(E)\to0\) imply (4.3).  A convenient stronger
condition is

\[
             \sup_M\int V^{1+\epsilon}\,d\beta_M<\infty
             \quad\hbox{for some }\epsilon>0.              \tag{5.4}
\]

This is the rigorous meaning under which “uniformly integrable positive
boundary endpoints” closes the lemma.  It concerns the value of the **new
chart's** potential at rare entries and after defects.  It is not a moment
bound for \((\Delta V)^+\) on episodes already running in that chart.

## 6. Consequence for the proposed T3-2 composition

The certified fixed-state killed Green construction supplies the diverging
normalization, finite-set escape, and exact bounded-test balance.  The
finite chart localization can supply a positive local episode-start mass
and zero **unweighted** exit/entry count.  The both-available and
Bellman/Flat0 theorems supply a proper marked factorial potential, negative
all-clock drift, actual endpoints, duration moments, and positive
episode-increment moments.  These inputs control (4.1), the episode cut,
and ordinary endpoint overshoot.

They do not control (5.2) for entries from a chart using a different local
potential, nor do they turn global nonnegative linear endpoint balance into
nonnegative flux on every terminal component.  Therefore Lemma 4.1 cannot
yet be invoked.  A publication-safe closure must add one of the following:

1. one global common proper potential, so all cross-chart values telescope;
2. an explicit proof of (5.2) for every selected terminal chart and every
   defect/entry boundary; or
3. a different global flow/separation argument which keeps the compensating
   chart flux instead of discarding its zero-count but high-value entries.

**Audit verdict:** the proposed local-potential terminal-Green implication
is **STRICT FAIL** under the hypotheses currently proved.  The corrected
weighted-boundary Lemma 4.1 is **PASS**, but its load-bearing hypothesis
(5.2) is not presently supplied by the cited components.
