# The mixed three-color \(P_4\): exact boundary

## Status

Date: 2026-07-26 (PDT)

This note studies the smallest residual list-critical tree left by the
frozen-color projection.  It does **not** resolve the \(k=3\) slice.  The
finite census statements below are labeled **OBSERVED**.  The explicit
seven-vertex near-realization is checked directly from the definition and is
an exact counterexample to several tempting intermediate claims, but it is
not a counterexample to the gamma--theta conjecture because its domination
number is two.

## 1. The target pattern and its forced states

Let

\[
 S=\{a,b,c\}
\]

be an independent state in an eternal three-family \(\mathcal F\).  Suppose
that \(x_0x_1x_2x_3\) is an induced path in
\(H=\overline G\), and that the exact family-response lists are

\[
 L(x_0)=\{a\},\quad
 L(x_1)=\{a,c\},\quad
 L(x_2)=\{b,c\},\quad
 L(x_3)=\{b\}.
\tag{1.1}
\]

The two end edges are Hall-tight.  Lemma 8 of
`math/working/k3_cross_state_attack.md` therefore puts

\[
 \{b,x_0,x_1\},\qquad \{a,x_2,x_3\}
\tag{1.2}
\]

in \(\mathcal F\).  All six one-swap states named by (1.1) also belong to
\(\mathcal F\).  Restoration rules out any state whose missing reference
positions are not contained in the union of the lists of its outside
positions.

These facts do not immediately contradict closure.  For example, from
\(\{b,x_0,x_1\}\) an attack at \(x_2\) can move either \(b\) or \(x_0\);
both successor shapes pass restoration.  The symmetric ambiguity remains
on the other end.  Ridge covariance does not apply to (1.2), since these
forced states need not be independent and do not share a two-vertex ridge
with \(S\).

### Lemma 1 (the domination witness creates a second independent state) — PROVED

Assume in addition that

\[
 \gamma(G)=\alpha(G)=3.
\]

Then there is a vertex

\[
 w\notin S\cup\{x_0,x_1,x_2,x_3\}
\tag{1.3}
\]

which is nonadjacent in \(G\) to both \(x_1\) and \(x_2\).  Consequently,

\[
 T=\{w,x_1,x_2\}
\tag{1.4}
\]

is a maximum independent set and belongs to every eternal three-family.

#### Proof

The pair \(\{x_1,x_2\}\) dominates all seven displayed vertices.  Indeed,
\(a,c\) are adjacent to \(x_1\), while \(b,c\) are adjacent to \(x_2\), by
the positive list entries in (1.1).  The vertices \(x_1,x_2\) dominate
themselves.  Since the path is induced in \(H\), the nonconsecutive pairs
\(x_0x_2\) and \(x_1x_3\) are edges of \(G\), so the pair also dominates
\(x_0,x_3\).

But \(\gamma(G)=3\), so \(\{x_1,x_2\}\) cannot dominate \(G\).  A vertex
\(w\) missed by this pair is outside the seven displayed vertices and is
nonadjacent to both members.  The middle path edge \(x_1x_2\) is also a
nonedge of \(G\), so (1.4) is independent.  It has maximum size because
\(\alpha(G)=3\).  The independent-state forcing lemma now puts \(T\) in
every eternal three-family. \(\square\)

Lemma 1 is the first place where \(\gamma=3\), rather than merely
\(\alpha=\gamma^\infty=3\), enters the mixed-core analysis.  The
adversarial two-state exchange theorem applies to the disjoint independent
states \(S\) and \(T\): every ordering of \(w,x_1,x_2\) has a
family-supported monotone path from \(S\) to \(T\), and every restoration
ordering has a path back.  No contradiction from those paths is presently
proved.

### Lemma 2 (the middle-pair witnesses form a covariant ridge clique) — PROVED

Under Lemma 1, put

\[
 W=N_H(x_1)\cap N_H(x_2).
\tag{1.5}
\]

Then \(W\) is nonempty, lies outside the seven displayed vertices, and
\(G[W]\) is a clique.  For every \(w\in W\),

\[
 T_w=\{w,x_1,x_2\}
\tag{1.6}
\]

is an independent family state.  From \(T_w\), an attack at any
\(z\in W-\{w\}\) has the unique response \(w\to z\), producing \(T_z\).
Moreover, ridge covariance transports the complete response-incidence
system at \(T_w\) to that at \(T_z\) by the transposition \((w\ z)\).

#### Proof

Nonemptiness and separation from the named vertices follow from the proof
of Lemma 1.  If distinct \(w,z\in W\) were nonadjacent in \(G\), then

\[
 \{x_1,x_2,w,z\}
\]

would be an independent four-set, contrary to \(\alpha(G)=3\).  Hence
\(G[W]\) is a clique.  Each \(T_w\) is an independent triple, so the
independent-state forcing lemma puts it in \(\mathcal F\).

At \(T_w\), neither \(x_1\) nor \(x_2\) is adjacent to \(z\), by the
definition of \(W\), whereas \(wz\in E(G)\).  Thus \(w\to z\) is the unique
legal response, and its successor is \(T_z\).  Finally, \(T_w,T_z\) are
independent states sharing the ridge \(\{x_1,x_2\}\), so ridge
response-covariance applies with the transposition \((w\ z)\). \(\square\)

The mixed core therefore forces not just one new state but a whole
interchangeable ridge of witness states.  The current gap is to turn this
covariance back into an additional allowed color, or a coloring, on the
original four path vertices.

## 2. A genuine eternal near-realization — PROVED/CHECKED

The graph

\[
 G=\texttt{FDzro}
\]

on labels

\[
 a=0,\ b=1,\ c=2,\ x_0=3,\ x_1=4,\ x_2=5,\ x_3=6
\]

has edge set

\[
\begin{split}
&03,04,05,\quad 14,15,16,\quad
23,24,25,26,\\
&35,36,46.
\end{split}
\tag{2.1}
\]

The complement induced by \(3,4,5,6\) is exactly the path
\(3\,4\,5\,6\).  The 21 triples recorded in
`results/k3_mixed_p4_probe.json` form an eternal dominating family in the
standard one-guard model.  This is a proper subfamily of the 33-state
greatest eternal three-family.  The separately structured verifier B accepts
the displayed family directly.  Relative to \(S=\{0,1,2\}\), its exact
family-response lists are

\[
 L(3)=\{0\},\quad L(4)=\{0,2\},\quad
 L(5)=\{1,2\},\quad L(6)=\{1\}.
\tag{2.2}
\]

Exact evaluation gives

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\tag{2.3}
\]

Thus the mixed \(P_4\) is compatible, inside a specified eternal subfamily,
with all of the following at once:

1. \(\alpha=3\);
2. a genuine closed one-guard eternal family of three-sets;
3. arbitrary-state restoration;
4. the two Hall-tight forced states;
5. the co-occupied-ridge common-neighborhood lemma; and
6. ridge covariance wherever its independent-state hypothesis applies.

It follows rigorously that these ingredients alone cannot eliminate (1.1).
Any contradiction in an equality graph must use the missing hypothesis
\(\gamma=3\), or a consequence which genuinely depends on it.

## 3. Named-vertex partial closure — OBSERVED

There are six unspecified adjacencies between \(S\) and the four path
vertices after the positive list edges are fixed.  The probe enumerates
them, requires every path vertex to be shared, imposes the inherited
condition \(\alpha(G[\{S,x_0,x_1,x_2,x_3\}])\leq3\), removes exactly the
six forbidden direct-swap states, and computes the greatest family closed
under attacks at the seven displayed vertices.

Of 36 masks surviving the inherited static filters, four admit all required
states.  Every surviving local model contains the additional graph edges

\[
 cx_0,\qquad bx_1,\qquad ax_2,\qquad cx_3.
\tag{3.1}
\]

Each resulting seven-vertex graph has a dominating pair.  This calculation
is a transparent finite diagnostic, not a theorem: no independent coverage
checker or proof log has been packaged for the 36-mask case split.

The exact near-realization in Section 2 is the first of these four local
models.  It shows that the local survivors are mathematically real rather
than artifacts of a transition abstraction.

## 4. Complete small census — OBSERVED

Using `nauty` 2.9.3 `geng -c`, the probe examined every connected unlabeled
graph of orders seven, eight, and nine.  It retained graphs satisfying

\[
 \gamma=\alpha=\gamma^\infty=3
\]

and searched every independent state in the greatest eternal three-family
for (1.1) on an induced complement \(P_4\).

\[
\begin{array}{c|r|r|r}
n&\text{connected graphs}&
\gamma=\alpha=\gamma^\infty=3&\text{realizations}\\ \hline
7&853&16&0\\
8&11\,117&140&0\\
9&261\,080&1\,380&0
\end{array}
\tag{4.1}
\]

The aggregate is 273,050 graphs, 1,536 equality graphs, and zero
realizations.  Source, hashes, commands, and literal output are frozen in
`results/k3_mixed_p4_probe.json` and
`results/k3_mixed_p4_probe.log`.

This is not promoted to a certified exclusion: it has one probe and no
separate coverage audit.  It is also weaker than the campaign's already
known no-counterexample census, because it concerns one exact response-list
pattern.

## 5. Exact stopping boundary

The smallest mixed tree is not refuted by the present universal transition
lemmas.  A seven-vertex eternal realization exists, and it fails the target
hypothesis in exactly one decisive place:

\[
 \gamma=2<\alpha=\gamma^\infty=3.
\]

Conversely, no realization in the **greatest** eternal family of an equality
graph occurs through order nine.  This does not exclude the pattern in a
proper eternal subfamily of one of those graphs.  The next proof step should
therefore exploit the witnesses forced by the absence of dominating pairs.
Lemma 1 already turns the witness missed by \(\{x_1,x_2\}\) into the second
independent family state \(\{w,x_1,x_2\}\).  Closure and two-state exchange
at that state are information absent from the seven-vertex local model and
are the first mechanism not already refuted by \(\texttt{FDzro}\).
