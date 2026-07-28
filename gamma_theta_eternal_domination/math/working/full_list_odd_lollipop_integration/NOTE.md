# Integrating the odd fan-path theorem into the single-full slice

## Status and verdict

Date: 2026-07-27 (PDT)

The odd fan-path exclusion in
`math/working/k3_long_bicycle_connectors/NOTE.md` and its hostile PASS
review were read in full.

**REFUTED as an automatic local implication:** an
augmentation-sensitive one-unit lollipop at a unique full vertex need not
realize the odd fan-path geometry.  One explicit obstruction is
**terminal-port separation**: the outgoing and returning clauses can use
different physical vertices of the unit's frozen component.

This note gives an exact nine-vertex, 65-state eternal-family control
realizing that obstruction.  It has \(\gamma=2\), so it does not refute a
future theorem using the full minimum-counterexample hypothesis
\(\gamma=3\).  It proves that any such theorem must use genuinely
\(\gamma=3\)-sensitive dynamics; the 2-SAT expansion and single-full
hypothesis alone do not identify the ports.

## 1. Why the lift can fail

Let the full vertex be \(x\), and prescribe color \(a\) for \(x\).  An
augmented unit is supported at some \(r\in R_x=N_H(x)\) and fixes the
orientation of an entire frozen component \(K\).  A one-unit implication
path can leave \(K\) through a port \(q_0\), traverse other components, and
return through a different port \(q_1\).

The fan theorem requires one physical vertex \(q\) satisfying

\[
 xq,\ qv_0,\ qv_m\in E(H).
\tag{1.1}
\]

The Boolean identity of \(q_0,q_1,r\) as literals of the same component
variable does not imply any equality among these vertices and does not
imply the missing complement edges in (1.1).  Contracting the component
paths would be unsound.

## 2. Smallest separated-port pattern

Use anchors \(S=\{a,b,c\}=\{0,1,2\}\), full target \(x=3\), and outside
vertices

\[
 r=4,\quad t=5,\quad q=6,\quad v_0=7,\quad v_1=8.
\]

The complement edges are

\[
\begin{split}
E(H)=\{&
01,02,12,\ 34,\\
&45,56,68,78,47\}.
\end{split}
\tag{2.1}
\]

Thus the nonanchor complement is a \(C_5\)

\[
 r-t-q-v_1-v_0-r
\tag{2.2}
\]

with the unit tail \(x-r\).

There is an eternal family \(\mathcal F\) whose exact lists at \(S\) are

\[
\begin{array}{c|cccccc}
y&x&r&t&q&v_0&v_1\\ \hline
L(y)&
\{a,b,c\}&\{a,b\}&\{a,b\}&\{a,b\}&\{b,c\}&\{b,c\}.
\end{array}
\tag{2.3}
\]

In particular, \(F_3(S)=\{x\}\).  The family is defined reproducibly as
the greatest safe kernel of all dominating triples after banning exactly
the direct swaps excluded by (2.3).  It has 65 states, deletion-round
sizes \(8,1,4\), and satisfies all \(65(9-3)=390\) unoccupied-attack
obligations.

The two frozen components are

\[
 r-t-q\subseteq W_c,\qquad v_0-v_1\subseteq W_a.
\tag{2.4}
\]

Let their orientation variables be \(X,Y\).  Up to complementing the
coordinates, the cross edges \(rv_0,qv_1\) give

\[
 (\neg X\lor Y),\qquad(\neg X\lor\neg Y).
\tag{2.5}
\]

The base formula is satisfiable exactly at

\[
 (X,Y)=(0,0),(0,1).
\tag{2.6}
\]

Coloring the full target \(x\) with \(a\) adds the unit \(X\), making
(2.5) inclusion-minimally unsatisfiable.  This is a genuine one-unit,
two-binary-clause lollipop.

There is no embedding of the odd fan-path theorem for any anchor color.
For the intended color \(a\), the unit edge is \(xr\), but only the first
cross clause uses \(r\); the returning clause uses \(q\).  The even
connector \(r-t-q\) makes the two ports the same Boolean orientation
without making them the same vertex.  All five nonfull vertices are
adjacent in \(G\) to all three anchors: every omitted response in (2.3) is
dynamic, not a graph nonedge.

The labeled graph6 record is

```text
HFzvvn{
```

and its canonical graph6 record is

```text
Hvzax|~
```

Its parameters are

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\tag{2.7}
\]

The ordinary-set verifier is `verify.py`.

### Minimality of the port obstruction

Within the two-clause subclass in which the outgoing terminal port is the
unit-support vertex \(r\in R_x\), terminal-port separation is the smallest
way to avoid the fan while keeping vertex-distinct simple connectors:

1. avoiding the fan requires distinct terminal ports;
2. the two ports must represent the same starting orientation, so their
   shortest nontrivial connector has even length at least two, requiring
   the intermediate vertex \(t\);
3. the repeated other component has odd connector length at least one,
   requiring distinct vertices \(v_0,v_1\).

Hence \(r,t,q,v_0,v_1\) are the smallest separated-port expansion in this
subclass.  The control realizes this five-vertex minimum.

Without the outgoing-port condition, separation is only one obstruction:
the two clauses may share a physical port \(q\notin R_x\), in which case
\(xq\notin E(H)\) and the fan hypothesis still fails.

## 3. Exact extra condition that makes the fan theorem apply

For an augmentation-sensitive two-clause lollipop, the odd fan theorem
does apply if the following **physical hub condition** is added:

1. the two terminal cross clauses use the same physical port \(q\);
2. \(q\in R_x\), so \(xq\in E(H)\);
3. after those clauses are removed, the repeated component has a
   vertex-distinct connector \(v_0\ldots v_m\) contained in \(W_a\).

The connector parity law then makes \(m\) odd: both terminal clauses have
the same collision color.  Taking a shortest connector makes its vertices
distinct.  The fan theorem applies with

\[
 p=x,\quad q=q,\quad v_0,\ldots,v_m,
\]

because \(a\in L(x)\), every \(v_i\) omits \(a\), and all required
complement edges are literal.

If the lollipop has three or more binary clauses, an additional reduction
is needed: the implication walk must first be reduced to two terminal
clauses around one repeated \(W_a\)-component.  The fan theorem does not
perform that reduction.

## 4. Consequence for the \(\gamma=3\) proof lane

The new theorem eliminates the **hub-recurrent** subcase, not every
augmentation-sensitive one-unit lollipop.  The remaining exact branch is:

- terminal ports are separated as above; or
- the terminal port is shared but lies outside \(R_x\), so the required
  complement edge from \(x\) is absent; or
- the implication walk uses more than two binary clauses/components.

The control fails the equality hypothesis precisely at \(\gamma=2\).
Therefore a viable next lemma must show that \(\gamma=3\), together with
the full-vertex spoke/covariance geometry, forces hub recurrence or
otherwise kills the separated-port cycle.  Merely interpreting
\(a\notin L(y)\) as \(ay\in E(H)\) is refuted literally by (2.1)--(2.3).

No such \(\gamma=3\)-sensitive port-identification lemma is proved here.
