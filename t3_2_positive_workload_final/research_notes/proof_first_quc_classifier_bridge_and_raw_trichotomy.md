# The exact Q/U/C classifier bridge and raw AA/mixed/SS trichotomy

**Proof-first analytic bridge, 2026-08-12 PDT.**  This note proves that the
ordered Q/U/C output of the inherited two-active top-complex classifier
implies the available-target hypothesis in Section 2 of
proof_first_both_available_current_target_theorem.md, frozen at SHA-256

    157e94cd035dec9a41947129dfcbbab0ebc6e72c01abde6bcf6626052954f1ed.

It also records the exact raw partition of two-linkage chart incidences into
available/available (AA), one available and one shielded (mixed), and
shielded/shielded (SS).  The bridge is symbolic.  The displayed counts are
finite support identities only; they prove no stochastic estimate.

## 1. Exact ordered classifier

Let

\[
 {\cal C}_2=\{0,A,B,C,2A,2B,2C,A+B,A+C,B+C\},
 \qquad h=(h_A,h_B,0),\quad h_A,h_B>0,                 \tag{1.1}
\]

and let \(L\subseteq{\cal C}_2\) be a nontrivial linkage support.  Put

\[
 T=T_h(L)=\{y\in L:h\cdot y=\max_{z\in L}h\cdot z\}.  \tag{1.2}
\]

The classifier applies the following tests in order.

1. If \(T=L\), return **S** (shielded).
2. If \(T\) contains a complex with two active particles, return **Q**.
3. Let
   \[
       I_T=\{i\in\{A,B\}:y_i>0\text{ for some }y\in T\}.
   \]
   If
   \[
             \sum_{i\in I_T}y_i=1\qquad(y\in L),       \tag{1.3}
   \]
   return **S**.
4. If \(T\) contains a unary complex, return **U**.
5. If a member of \(T\) contains \(C\) and a member of \(L\setminus T\)
   also contains \(C\), return **C**.
6. Otherwise return **S**.

The available label is

\[
                         {\rm A}=\{{\rm Q},{\rm U},{\rm C}\}. \tag{1.4}
\]

The tests are ordered, so Q, U, C, and S are disjoint and exhaustive.  This
is the literal mathematical content of top_kind in the independent
clean-room atlas replay; no orientation enters it.

## 2. Faster source and lower terminal in each available type

For every available linkage choose \(q\in T\) and \(c\in L\setminus T\)
as follows.

### Q: quadratic active top

Choose \(q\in T\) with \(q_A+q_B=2\), and choose any \(c\in L\setminus T\).
Binaryity forces \(q_C=0\), and

\[
                         q_C=0\le c_C,\qquad
                         h\cdot q>h\cdot c.            \tag{2.1}
\]

### U: unary top

Choose a unary \(q\in T\), and choose any \(c\in L\setminus T\).  The unary
top cannot be \(C\): if \(q=C\), then the maximum in (1.2) is zero, while
all weights in (1.1) are nonnegative, so every member of \(L\) has weight
zero and \(T=L\), contrary to the first classifier test.  Hence
\(q\in\{A,B\}\), and again

\[
                         q_C=0\le c_C,\qquad
                         h\cdot q>h\cdot c.            \tag{2.2}
\]

### C: bounded-cofactor carrier

Choose a top complex \(q\in T\) containing \(C\), and a lower complex
\(c\in L\setminus T\) containing \(C\).  This test occurs only after Q.
Thus \(q\) cannot contain two active particles; since it is nonflat and has
positive \(h\)-weight, binaryity gives

\[
 q\in\{A+C,B+C\},\qquad q_C=1\le c_C\in\{1,2\},
 \qquad h\cdot q>h\cdot c.                            \tag{2.3}
\]

Equations (2.1)--(2.3) give one common conclusion:

\[
       q_C\le c_C,\qquad h\cdot q>h\cdot c.            \tag{2.4}
\]

The inequality in the bounded coordinate is the exact activation fact
needed below.  It is not a probability estimate.

## 3. From every actual target to a rare terminal

Fix an arbitrary strongly connected orientation of \(L\), arbitrary
positive labelled rates, and an escaping sequence of marked states

\[
                         (x_n,t),\qquad x_n\ge t,\quad t\in L, \tag{3.1}
\]

in a fixed two-active chart.  Both \(A_n\) and \(B_n\) diverge, while \(C_n\)
lies in the chart's bounded phase.  The complete source-order flag is
scalarized by \(h\): whenever \(h\cdot u>h\cdot v\), the corresponding
enabled source propensities satisfy

\[
                         {\lambda_v(x_n)\over\lambda_u(x_n)}
                              \longrightarrow0.          \tag{3.2}
\]

Strong connectivity supplies a directed path from the actual target \(t\)
to the chosen lower complex \(c\).  Delete loops to make it simple:

\[
                         t=y_0\longrightarrow y_1
                          \longrightarrow\cdots\longrightarrow y_m=c.
                                                               \tag{3.3}
\]

It is a physical word.  At its first step \(t\) is enabled because it is the
actual carried target; after every prescribed firing, its actual target
creates the next prescribed source.  No future activation is conditioned
upon.

On designated success, populations telescope to

\[
                         z_n=x_n-t+c\ge c.               \tag{3.4}
\]

If an intermediate firing changes the bounded phase, enabled-source support,
active set, shell, or source-order chart, retain the causing reaction as a
physical structural exit.  Otherwise all \(z_n\) remain in the same padded
chart.  Their active coordinates differ from those of \(x_n\) by a fixed
bounded vector, so the strict source comparison (3.2) is unchanged.

At \(z_n\), the faster source \(q\) is enabled.  In Q and U this follows
from \(q_C=0\) and divergence of both active coordinates.  In C, (3.4) and
(2.3) give

\[
                         (z_n)_C\ge c_C\ge q_C=1,        \tag{3.5}
\]

while the active particle of \(q\) is present for all large \(n\).
Therefore

\[
 \begin{aligned}
 p_c(z_n)
   &={\lambda_c(z_n)\over\Lambda(z_n)}
     \le{\lambda_c(z_n)\over\lambda_q(z_n)}\\
   &={K_c(z_n)_c\over K_q(z_n)_q}
     \longrightarrow0.
 \end{aligned}                                          \tag{3.6}
\]

The last limit is exactly \(h\cdot q>h\cdot c\) in the fixed source-order
chart, preserved under bounded displacement.  Fixed positive rate constants
only multiply the ratio by \(K_c/K_q\).

Thus, for **every** actual carried target \(t\in L\), one fixed simple
same-linkage path either records a physical structural exit or reaches a
complex \(c\) whose source probability tends to zero.  This is precisely the
available-target hypothesis of the frozen both-available theorem.

Notice what has disappeared: a C-type source may be disabled at the episode
start, but the rule does not wait for it.  It starts at the already enabled
actual target \(t\), travels to \(c\), and (2.4) makes \(q\) enabled at the
success endpoint.  The terminal rarity in (3.6) is therefore proved without
conditioning on an activation jump.

## 4. Raw AA/mixed/SS trichotomy

After fixed-class projection and linkage merging, a two-linkage chart has two
disjoint supports \(L_1,L_2\subseteq{\cal C}_2\), each with at least two
vertices.  Apply the ordered classifier of Section 1 independently to each
support.  Exactly one of the following occurs.

1. **AA:** both outputs lie in \(\{{\rm Q},{\rm U},{\rm C}\}\).
   Section 3 proves the available-target hypothesis for both linkages, from
   every actual target.  The frozen both-available all-clock theorem applies.
2. **Mixed:** exactly one output lies in
   \(\{{\rm Q},{\rm U},{\rm C}\}\), and the other is S.  Section 3 proves
   the bridge only for the available side.  The both-available theorem is
   deliberately not invoked; these are the shielded/available interfaces
   passed to the pair-specific physical-time reduction.
3. **SS:** both outputs are S.  These are exactly the incidences passed to
   the common-invariant/deficiency-zero/service atlas.

This is a disjoint exhaustive trichotomy because (1.4) and S partition the
output of each linkage classifier.  It involves no stochastic inference.

For orientation only, the raw finite incidence identity is

\[
\begin{array}{c|r}
\text{ordered status}&\text{support--workload incidences}\\ \hline
{\rm AA}&163{,}612\\
{\rm A}{\rm S}&11{,}715\\
{\rm S}{\rm A}&11{,}715\\
{\rm SS}&446\\ \hline
\text{total}&187{,}488 .
\end{array}                                                \tag{4.1}
\]

Indeed, for one workload representative the number of ordered assignments
of ten complexes to \(L_1,L_2\), or neither, with both supports of size at
least two is

\[
 3^{10}-2(2^{10}+10\,2^9)+(1+10+10+90)=46{,}872.       \tag{4.2}
\]

The four exact workload representatives give \(4\cdot46{,}872=187{,}488\).
The four rows of (4.1) are the exact replay of the ordered classifier and
sum to this analytic universe count.  Their individual values are regression
evidence for the finite partition; the proof of the bridge is Sections 2--3.
Combining the two middle rows gives \(23{,}430\) raw mixed incidences.

## 5. Durable scope

The result proved here is:

> **Classifier bridge theorem.**  In a two-active binary chart, every Q-, U-,
> or C-classified linkage satisfies the frozen theorem's available-target
> path hypothesis from every actual target, for every strongly connected
> orientation and every positive fixed rate vector.  Hence every raw AA
> incidence is covered by the both-available all-clock theorem.  Raw mixed
> and SS incidences remain in their separate analytic pipelines.

The bridge does not assert recurrence for a generic mixed incidence, does
not delete a shielded linkage, and does not infer recurrence from support
inclusion.  Its only stochastic handoff is the exact hypothesis of the
already frozen both-available theorem.
