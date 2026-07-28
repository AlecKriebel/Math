# The first multi-step full-target constraint: spoke polarization

## Status and exact scope

Date: 2026-07-28 (PDT)

This note uses the standard **one-guard-moves** eternal-domination model:
attacks are made only at unoccupied vertices, and exactly one guard moves
along one edge to the attacked vertex.

The result is a short human theorem about the first two attacks from a
full-response independent triple.  It is genuinely stronger than all of
the static hypotheses in C-128.  In particular, it rejects the C-128
control immediately.

The theorem does **not** prove the complete full-list branch, the complete
\(k=3\) case, or the universal \(\gamma\)--\(\theta\) conjecture.  It
reduces the physical inactive-set obstruction to a component-palette
synchronization problem.

No literature-priority claim is made.

## 1. Setup

Let \(G\) have a one-guard eternal family \(\mathcal F\) of dominating
triples.  Put

\[
 H=\overline G.
\]

Let

\[
 S=\{s_0,s_1,s_2\}\in\mathcal F
\tag{1.1}
\]

be independent in \(G\), fix \(x\notin S\), and suppose \(x\) has a
**full family response at \(S\)**:

\[
 s_jx\in E(G)
 \quad\hbox{and}\quad
 D_j:=S-\{s_j\}+\{x\}\in\mathcal F
 \qquad(0\le j\le2).
\tag{1.2}
\]

Thus the first attack is at \(x\), and each of the three guards is a legal
possible responder.

Let

\[
 B=N_H(x).
\tag{1.3}
\]

These are the vertices at which the guard on \(x\) is physically unable
to answer a later attack.  Equation (1.2) gives \(S\cap B=\varnothing\).
For the family-relative C-108 marking one has \(B\subseteq R_x\), but the
inclusion may be strict: a \(G\)-neighbor of \(x\) can be dynamically
inactive because its successor is absent from \(\mathcal F\).  The theorem
below controls \(B\), not the residual set \(R_x-B\).  In the sharp C-128
control, \(B=R_x\).
For \(i\in\{0,1,2\}\), define the root spoke

\[
 B_i=B\cap N_H(s_i),
\tag{1.4}
\]

and, for \(b\in B\), define its retained anchor palette

\[
 P(b)=
 \{\,i:\{x,s_i,b\}\in\mathcal F\,\}.
\tag{1.5}
\]

The possible anchorless set is

\[
 B_*=
 B-(B_0\cup B_1\cup B_2).
\tag{1.6}
\]

## 2. Two-step spoke-polarization theorem

### Theorem 2.1 — PROVED

Under (1.1)--(1.5), the following hold for every \(b\in B\).

1. The vertex \(b\) sees at most one root anchor in \(H\).  Equivalently,
   the three spokes \(B_0,B_1,B_2\) are pairwise disjoint.
2. The retained palette satisfies
   \[
   |P(b)|\ge2.
   \tag{2.1}
   \]
3. If \(b\in B_q\), then
   \[
   q\in P(b).
   \tag{2.2}
   \]
4. For every \(i\in P(b)\),
   \[
   N_{H[B]}(b)\cap B_i=\varnothing.
   \tag{2.3}
   \]

Consequently:

\[
 \boxed{\text{each }B_i\text{ is independent in }H[B],}
\tag{2.4}
\]

and every vertex of \(B\) has neighbors in at most one of the three
root spokes.

### Proof

Every state \(D_j\) in (1.2) dominates \(G\).  If \(b\in B\) saw two
root anchors in \(H\), choose \(j\) so that both of those anchors remain
in \(D_j\).  Then \(b\) would be adjacent in \(H\) to \(x\) and to both
other members of \(D_j\), so \(D_j\) would miss \(b\) in \(G\).  This
proves assertion 1.

Fix \(b\in B\).  Attack \(b\) from each of the three retained states
\(D_j\).  The attack is unoccupied because \(S\cap B=\varnothing\), and
the guard at \(x\) cannot move because \(xb\notin E(G)\).

First suppose \(b\in B_q\).  For either \(j\ne q\), the state \(D_j\)
contains \(s_q\) and the third anchor \(s_t\).  The guard at \(s_q\) is
blocked from moving to \(b\), while the guard at \(s_t\) can move because
assertion 1 says that \(b\) sees no second anchor in \(H\).  Closure
therefore forces the unique successor

\[
 \{x,s_q,b\}\in\mathcal F.
\tag{2.5}
\]

Thus \(q\in P(b)\).  From \(D_q\), both remaining anchors can move to
\(b\).  Whichever guard answers, the stationary anchor has index
different from \(q\), so \(P(b)\) contains a second index.

Now suppose \(b\in B_*\).  All root anchors can move to \(b\).  If
\(P(b)\) had at most one member, say \(q\), then the attack at \(b\) from
\(D_q\) could leave only one of the two anchors with index different from
\(q\).  Neither possible successor would belong to \(\mathcal F\).
Hence (2.1) also holds in the anchorless case.  This proves assertions 2
and 3.

Finally, a triple dominates \(G\) exactly when its three vertices have no
common neighbor in \(H\).  Since every common \(H\)-neighbor of \(x\)
lies in \(B\), one has the exact equivalence

\[
 \{x,s_i,b\}\text{ dominates }G
 \quad\Longleftrightarrow\quad
 N_{H[B]}(b)\cap B_i=\varnothing.
\tag{2.6}
\]

Every retained state dominates.  Equations (1.5) and (2.6) prove (2.3).
If \(b\in B_i\), then (2.2) permits \(i\) in (2.3), proving that \(B_i\)
is independent.  Because \(P(b)\) has at least two indices, (2.3) also
shows that the neighbors of \(b\) can meet at most one root spoke.
\(\square\)

### Why this is genuinely a two-step condition

The proof uses the forced attack sequence

\[
 S
 \xrightarrow[\text{one guard}]{\text{attack }x}
 D_j
 \xrightarrow[\text{one guard}]{\text{attack }b}
 \{x,s_i,b\}.
\tag{2.7}
\]

Checking only that the three \(D_j\) dominate is a one-step static test.
The requirement that every \(D_j\) itself answer the second attack is the
first new closure layer.  C-128 checked the former and fails the latter.

## 3. Exact static form of the second-attack test

Define the dominating palette

\[
 Q(b)=
 \{\,i:\{x,s_i,b\}\text{ dominates }G\,\}.
\tag{3.1}
\]

By (2.6),

\[
 i\in Q(b)
 \quad\Longleftrightarrow\quad
 N_{H[B]}(b)\cap B_i=\varnothing.
\tag{3.2}
\]

The three first successors \(D_0,D_1,D_2\) can each answer an attack at
\(b\) by a move to a dominating state if and only if:

- \(b\in B_q\) implies \(q\in Q(b)\) and \(|Q(b)|\ge2\);
- \(b\in B_*\) implies \(|Q(b)|\ge2\).

This is an exact truth-table characterization, not merely a necessary
condition.  In an actual eternal family, \(P(b)\subseteq Q(b)\), and
Theorem 2.1 supplies the stronger retained-state statement.

## 4. Component consequence under the C-127 target condition

C-127 proves that in the equality-critical deletion branch,
\(\gamma(G-x)\ge3\) and \(\gamma(G)\ge3\) make \(B=N_H(x)\) totally
dominate \(H-x\).  In particular, \(H[B]\) has no isolated vertex.

### Corollary 4.1 (two-spoke components) — PROVED

Assume the hypotheses of Theorem 2.1, assume \(H[B]\) has no isolated
vertex, and assume there are no anchorless physical inactive vertices:

\[
 B=B_0\mathbin{\dot\cup}B_1\mathbin{\dot\cup}B_2.
\tag{4.1}
\]

Then every connected component \(C\) of \(H[B]\) has a unique unordered
two-spoke signature

\[
 \sigma(C)=\{i,j\}\subset\{0,1,2\},
\tag{4.2}
\]

such that

\[
 C=(C\cap B_i)\mathbin{\dot\cup}(C\cap B_j),
\tag{4.3}
\]

both parts are nonempty, and they are the two bipartition sides of \(C\).

#### Proof

Take an edge \(bc\) of \(C\), which exists because \(C\) is not an
isolated vertex.  By (2.4), its endpoints lie in different spokes, say
\(b\in B_i\) and \(c\in B_j\).  Theorem 2.1 says that all neighbors of
\(b\) lie in one spoke, necessarily \(B_j\), and all neighbors of \(c\)
lie in one spoke, necessarily \(B_i\).  Induction along paths from the
edge shows that every vertex of \(C\) lies in \(B_i\cup B_j\), with spoke
labels alternating along every edge.  Connectedness makes both classes
nonempty and gives uniqueness. \(\square\)

For a component of signature \(\{i,j\}\), color its \(B_i\)-side with
the color of \(s_j\) and its \(B_j\)-side with the color of \(s_i\).
Together with three distinct colors on the root triangle \(S\), this is a
proper coloring of

\[
 H[S\cup B].
\tag{4.4}
\]

Thus each physical inactive component has a canonical local two-color
palette.  The unresolved issue is to synchronize these palettes across
different components and extend the resulting precoloring through
\(H-(S\cup B\cup\{x\})\).  Different components can have different
signatures.

## 5. Exact controls and the corrected frontier

### 5.1 C-128 is rejected at the first new layer

For the C-128 target graph

```text
KxU[ISrR}NP^
```

with \(x=11\), \(S=\{0,4,8\}\), and
\(B=\{1,2,3,5\}\), the spokes are

\[
 B_0=\{3\},\qquad B_4=\{2\},\qquad B_8=\{1,5\}.
\tag{5.1}
\]

But \(15\in E(H)\).  Hence \(B_8\) is not independent, contradicting
(2.4).  More explicitly,

\[
 Q(1)=\{4\},\qquad Q(5)=\{0\}.
\tag{5.2}
\]

Both palettes have size one and omit the vertex's own spoke anchor.  For
example, after \(0\to x\) from \(048\), an attack at \(1\) from
\(\{x,4,8\}\) blocks the guard at \(8\) and forces
\(4\to1\); the resulting state \(\{x,1,8\}\) is non-dominating, with
vertex \(5\) missed.  This is exactly why that target successor has
deletion rank one.

### 5.2 The earlier C-123 control fails the same theorem

For the \(L(K_{3,3})\) control C-123, the full root is
\(\{1,5,8\}\).  Two of its spokes contain internal edges of the inactive
\(C_4\).  Hence the two-step theorem rejects it independently of its
separate domination-number failure.

### 5.3 Exact equality control

The accepted equality graph

```text
Ksv`f\knJVis
```

with target \(x=0\) and full root \(S=\{1,2,3\}\) satisfies Theorem 2.1
inside its 127-state greatest eternal triple-family.  Its physical
inactive graph has two components:

\[
 \{6,8\}\quad\text{with spoke signature }\{0,2\},
\qquad
 \{10,11\}\quad\text{with signature }\{1,2\}.
\tag{5.3}
\]

Every retained palette has exactly two anchors.  This proves that
different component signatures can occur under exact equality.  In this
control \(\gamma(G-x)=2\), and successful deletion colorings still exist;
the example neither refutes a synchronization theorem under the
equality-critical deletion condition nor supplies one.

## 6. What remains

The first missing multi-step layer is no longer merely “some successor
must survive.”  It has the explicit graph-theoretic content:

\[
 \boxed{
 \begin{array}{c}
 \text{each root spoke is independent in }H[B],\\
 \text{each }b\in B\text{ is anticomplete to at least two spokes},\\
 \text{and, without anchorless vertices, each }H[B]\text{ component}\\
 \text{uses exactly two spoke types.}
 \end{array}}
\tag{6.1}
\]

The next proof target is global and precise:

1. eliminate anchorless vertices or incorporate them into the component
   palette;
2. control the dynamically inactive residual set \(R_x-B\);
3. synchronize the two-color palettes of distinct \(H[B]\)-components
   using \(\gamma(G-x)=3\), ridge covariance, and retained states outside
   \(S\cup B\); and
4. prove that one synchronized palette extends through all of \(H-x\)
   while omitting a color on the full inactive set \(R_x\) (or, for the
   clique-cover conclusion alone, on the physical neighborhood \(B\)).

No step above assumes this remaining gluing statement.
