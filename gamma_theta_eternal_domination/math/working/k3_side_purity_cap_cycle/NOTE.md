# Side-pure physical ports and a finite cap-cycle control at \(k=3\)

## Status and exact scope

Date: 2026-07-27 (PDT)

All graph statements use the standard one-guard-moves eternal domination
model.  Attacks are made only at unoccupied vertices, exactly one adjacent
guard moves, and every retained state dominates.

This note has two outcomes.

1. **PROVED:** the accepted odd fan-path theorem C-079 has an exact
   side-purity consequence.  If a physical hub has a complement neighbor
   whose response list contains \(a\), then all of the hub's neighbors in
   any one component of the \(a\)-omitting projection lie on one
   bipartition side.
2. **EXACT POSITIVE CONTROL:** the connected graph `GCXfVG` has
   \[
     (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3),
   \]
   and its greatest eternal triple-family realizes a single positive cap
   repeated around an entire \(a\)-omitting complement \(C_4\).  There is
   no C-079 fan, no complement \(K_4\), and no dominating pair.

The control is colorable and is **not** a gamma--theta counterexample.  Its
response-list formula is satisfiable.  It refutes only the following naive
recurrence principle:

> Under equality, the first repeated positive cap in a finite connector
> iteration must itself create a C-079 fan, a complement \(K_4\), or a
> dominating pair.

Therefore a proof for an arbitrary two-unit chain or unit-free bicycle must
use the actual cross-clause ports, terminal units, or additional
arbitrary-family dynamics.  Cap roles, finiteness, and first repetition
alone do not suffice.

No argument below interprets omission from a family-response list as a
graph nonedge.

## 1. Response notation and accepted input

Let \(\mathcal F\) be an arbitrary eternal family of triples in \(G\), let

\[
  S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(t\notin S\), write

\[
  L(t)=\{u\in S:S-u+t\in\mathcal F\}.
\tag{1.1}
\]

Membership \(u\in L(t)\) implies \(ut\in E(G)\): the retained state
\(S-u+t\) must dominate the omitted anchor \(u\), and neither member of
\(S-\{u\}\) sees \(u\).  The converse is not asserted.

Fix \(a\in S\), and put

\[
  P_a=\{t\notin S:a\in L(t)\},
  \qquad
  W_a=\{t\notin S:a\notin L(t)\}.
\tag{1.2}
\]

The accepted frozen-projection theorem makes every component of
\(H[W_a]\) bipartite.  We also use C-079 in precisely its physical form:
there are no distinct outside vertices

\[
  p,q,v_0,\ldots,v_m
\]

with \(m\geq1\) odd, \(a\in L(p)\), every \(v_i\in W_a\), and literal
complement edges

\[
  pq,\ qv_0,\ qv_m,\ v_0v_1,\ldots,v_{m-1}v_m.
\tag{1.3}
\]

## 2. Side-purity

### Theorem 2.1 (C-079 side-purity) — PROVED

Let \(K\) be a connected component of \(H[W_a]\), with bipartition

\[
  U_K\mid V_K.
\]

Let \(q\notin S\).  If there is a vertex

\[
  p\in P_a-\{q\}
  \qquad\text{with}\qquad
  pq\in E(H),
\tag{2.1}
\]

then

\[
  N_H(q)\cap K\subseteq U_K
  \quad\text{or}\quad
  N_H(q)\cap K\subseteq V_K.
\tag{2.2}
\]

Thus an \(a\)-positive complement neighbor exposes \(q\) and makes every
one of its \(W_a\)-component neighborhoods side-pure.

#### Proof

Suppose instead that there are

\[
  x\in N_H(q)\cap U_K,
  \qquad
  y\in N_H(q)\cap V_K.
\]

Choose a shortest \(x\)--\(y\) path

\[
  x=v_0,v_1,\ldots,v_m=y
\]

in \(K\).  It is vertex-distinct, and \(m\) is odd because its endpoints
lie on opposite bipartition sides.  Every path vertex lies in \(W_a\).

The path avoids \(p\), since \(p\in P_a\) and \(P_a\cap W_a=\varnothing\).
It also avoids \(q\).  Indeed, if \(q\in W_a\), then the edge \(qx\)
puts \(q\) in \(K\), and both \(x\) and \(y\), as neighbors of \(q\) in
the bipartite graph \(K\), must lie on the side opposite \(q\).  That
contradicts their placement on opposite sides.  Hence \(q\notin K\).

The vertices \(p,q,v_0,\ldots,v_m\) are therefore distinct.  Equation
(2.1), the two chosen hub edges \(qv_0,qv_m\), and the literal path edges
give exactly the forbidden physical odd fan (1.3), with positive vertex
\(p\).  This contradicts C-079. \(\square\)

### Equivalent forbidden-neighborhood form

The contrapositive is often the useful version.  If \(q\) has neighbors on
both sides of one component of \(H[W_a]\), then

\[
  N_H(q)\cap P_a=\varnothing.
\tag{2.3}
\]

Here \(q\) itself may lie in \(P_a\); equation (2.3) concerns its open
complement neighborhood and does not include \(q\).

## 3. The singleton-buffer boundary for logical ports

### Corollary 3.1 (opposite-side port implies singleton buffer) — PROVED

Assume every outside response list is nonempty.  Let \(v\in S-\{a\}\),
let \(d\) be the third member of \(S-\{a,v\}\), and suppose

\[
  L(q)=S-\{v\}.
\tag{3.1}
\]

Suppose \(q\) has two complement neighbors \(x,y\) on opposite sides of
one component of \(H[W_a]\).  Then:

1. \(N_H(q)\cap P_a=\varnothing\);
2. every outside vertex \(r\) satisfying
   \[
     qr\in E(H),\qquad v\notin L(r)
   \tag{3.2}
   \]
   has
   \[
     L(r)=\{d\}.
   \tag{3.3}
   \]

In particular, suppose \(q\) is a port in a non-anchor flip component of
the \(v\)-projection and a positive-length physical connector leaves
\(q\).  Its first connector vertex is outside \(S\), so (3.3) says that
it is a singleton marker.  That marker fixes the orientation of the
component by the usual singleton parity equation.

#### Proof

Equation (3.1) gives \(a\in L(q)\), but this fact does not provide an
edge from \(q\) to another member of \(P_a\).  If such an edge existed,
Theorem 2.1 would put all of \(q\)'s neighbors in the chosen
\(W_a\)-component on one side, contrary to the hypotheses on \(x,y\).
This proves item 1.

Now take \(r\) as in (3.2).  If \(a\in L(r)\), then
\(r\in N_H(q)\cap P_a\), contradicting item 1.  Thus \(a\notin L(r)\).
The other hypothesis in (3.2) gives \(v\notin L(r)\).  Since
\(L(r)\) is a nonempty subset of the three-element set
\(\{a,v,d\}\), it follows that \(L(r)=\{d\}\).

A non-anchor flip component is disjoint from the anchor component
containing \(S-\{v\}\).  Hence the first vertex of an internal connector
from \(q\) is outside \(S\), and item 2 applies. \(\square\)

### Corollary 3.2 (cap continuation dichotomy) — PROVED

Let \(xy\in E(H[W_a])\), and let \(z\notin S\) satisfy

\[
  zx,zy\in E(H),
  \qquad
  a\in L(z).
\tag{3.4}
\]

Then

\[
  N_H(z)\cap P_a=\varnothing.
\tag{3.5}
\]

If in addition \(L(z)=S-\{v\}\) for \(v\ne a\), every outside
\(H\)-neighbor of \(z\) in \(W_v\) is the singleton in the third color.

#### Proof

The endpoints of the edge \(xy\) lie on opposite sides of their
\(H[W_a]\)-component.  Apply (2.3) with \(q=z\), and then apply
Corollary 3.1. \(\square\)

This is the exact obstruction to a purely physical contraction.  A hub
touching opposite logical signs either creates the accepted odd fan, or it
is isolated in \(H\) from every \(a\)-positive vertex.  If it is itself a
two-list port, ordinary same-type continuation is replaced by a singleton
buffer.  Logical identity of variables does not identify physical ports,
and list omission has not been converted into nonadjacency.

## 4. A connected equality cap cycle

Let

\[
  V(G)=\{a,b,c,z,x_0,x_1,x_2,x_3\}.
\]

The graph \(G\) has exactly the edges

\[
\begin{split}
 E(G)=\{&
 az,\ ax_2,\ ax_3,\\
 &bx_i,\ cx_i\quad(0\leq i\leq3),\\
 &x_0x_2,\ x_1x_3\}.
\end{split}
\tag{4.1}
\]

With the vertex order

\[
 (a,b,c,z,x_0,x_1,x_2,x_3)=(0,1,2,3,4,5,6,7),
\]

its graph6 record is

```text
GCXfVG
```

Equivalently, \(H=\overline G\) consists of:

- the anchor triangle \(ab,ac,bc\);
- the edges \(bz,cz\);
- all four edges \(zx_i\);
- the two edges \(ax_0,ax_1\); and
- the rim cycle
  \[
    x_0x_1x_2x_3x_0.
  \tag{4.2}
  \]

In particular, \(G\) is connected.

### The 26-state greatest eternal family

Put

\[
  R=\{b,c,x_0,x_1,x_2,x_3\}
\]

and let

\[
  \mathcal D=
  \binom R2-\bigl\{\{x_0,x_2\},\{x_1,x_3\}\bigr\}.
\tag{4.3}
\]

Define

\[
  \mathcal F=
  \bigl\{\{t\}\cup D:
  t\in\{a,z\},\ D\in\mathcal D\bigr\}.
\tag{4.4}
\]

Thus \(|\mathcal F|=2(15-2)=26\).

The graph \(G[R]\) is \(K_{2,4}\), with part
\(\{b,c\}\) joined to every \(x_i\), together with the matching
\(x_0x_2,x_1x_3\).  Its dominating pairs are exactly \(\mathcal D\).
Every state in (4.4) therefore dominates: \(t\) dominates the edge
\(\{a,z\}\), and \(D\) dominates \(R\).

The family \(\mathcal D\) is an eternal two-family in \(G[R]\).

- From \(\{b,c\}\), answer an attack at \(x_i\) by either anchor.
- From \(\{h,x_i\}\), answer an attack at the other anchor by \(x_i\).
  For an attack at the matching partner of \(x_i\), move \(x_i\);
  for an attack at either other \(x_j\), move \(h\).
- A pair of rim vertices in \(\mathcal D\) is a rim edge of (4.2).
  Each unoccupied rim vertex is the \(G\)-matching partner of one
  occupied endpoint; attacks at \(b\) or \(c\) are answered by either
  endpoint.

Every listed successor remains in \(\mathcal D\).  An attack exchanging
\(a\) and \(z\) is answered along the edge \(az\), without changing
\(D\).  This proves that \(\mathcal F\) is eternal.

Conversely, every dominating triple must contain at least one of
\(\{a,z\}\), because \(z\) is a leaf with unique neighbor \(a\).  No
triple containing both \(a,z\) dominates.  With exactly one of them, the
remaining pair must lie in \(\mathcal D\); the two excluded matching pairs
miss the opposite matching pair.  Hence (4.4) is the set of all dominating
triples and therefore the greatest eternal triple-family.

### Parameters

The state \(S=\{a,b,c\}\) dominates \(G\).  Every vertex pair has a common
neighbor in \(H\):

- \(a,z\) have the common neighbors \(b,c,x_0,x_1\);
- a pair involving \(b\) or \(c\) is completed inside
  \(\{a,b,c,z\}\) or by \(z\);
- every pair of rim vertices has common neighbor \(z\);
- \(z,x_i\) have a rim neighbor in common; and
- \(a,x_i\) have \(x_0\) or \(x_1\), as appropriate, in common.

Thus no singleton or pair dominates \(G\), and

\[
  \gamma(G)=3.
\tag{4.5}
\]

The anchor triangle gives \(\alpha(G)\geq3\).  There is no \(K_4\) in
\(H\): the rim is triangle-free, \(az\notin E(H)\), and no rim vertex is
an \(H\)-neighbor of \(b\) or \(c\).  Hence

\[
  \alpha(G)=3.
\tag{4.6}
\]

The eternal family (4.4) and the standard lower bound
\(\alpha\leq\gamma^\infty\) give

\[
  \gamma^\infty(G)=3.
\tag{4.7}
\]

Finally,

\[
  \{a,z\}\mid
  \{b,x_0,x_2\}\mid
  \{c,x_1,x_3\}
\tag{4.8}
\]

is a partition into three \(G\)-cliques.  Together with
\(\alpha=3\), this proves

\[
  \theta(G)=3.
\tag{4.9}
\]

### Exact response lists and colorability

At \(S=\{a,b,c\}\), the family (4.4) gives

\[
  L(z)=\{a\},
  \qquad
  L(x_i)=\{b,c\}\quad(0\leq i\leq3).
\tag{4.10}
\]

Replacing \(a\) by \(z\) gives a state in (4.4).  Replacing \(b\) or
\(c\) by any \(x_i\) also gives a state in (4.4).  Replacing \(a\) by an
\(x_i\) leaves the leaf \(z\) undominated, so it is not a family state.

The response-list instance is colorable in exactly two ways: color \(z\)
by \(a\), and alternate \(b,c\) around the rim \(C_4\).  The control is
therefore positive and does not obstruct \(\theta=3\).

## 5. What first repetition does and does not imply

For the omitted color \(a\),

\[
  P_a=\{z\},
  \qquad
  W_a=\{x_0,x_1,x_2,x_3\},
\tag{5.1}
\]

and \(H[W_a]\) is the cycle (4.2).  The same positive vertex \(z\) is a
common complement neighbor, hence a cap, of every rim edge.  The edge
\(x_2x_3\) is fully dynamic relative to \(a\):

\[
  ax_2,ax_3\in E(G),
\]

and its unique common complement neighbor is \(z\).

There is nevertheless no C-079 fan for any anchor.

- For \(a\), the only positive vertex is \(z\).  A possible hub \(x_i\)
  sees the two rim neighbors \(x_{i-1},x_{i+1}\), which lie on the same
  side of the rim bipartition.  Every path between them in the rim is
  even.
- For \(b\) and \(c\), the corresponding omitting set is the singleton
  \(\{z\}\), so it contains no path of positive length.

There is no complement \(K_4\) and no dominating pair by
(4.5)--(4.6).  Thus the first repeated cap can close around a finite even
connector cycle without producing any of the three hoped-for exits.

What the control lacks is equally important: it has no unsatisfiable
two-unit chain or unit-free bicycle.  In particular, \(P_a-\{z\}\) is
empty, so there are no separated \(a\)-positive cross ports for the cap to
interact with.  A future global proof can still succeed by exploiting
those logical incidences.  It cannot treat repeated cap identity alone as
the contradiction.

## 6. Reproduction

Run

```text
python3 -I -B -W error \
  math/working/k3_side_purity_cap_cycle/verify.py \
  --check math/working/k3_side_purity_cap_cycle/result.json
```

The verifier independently:

- decodes `GCXfVG` and compares its edge set with (4.1);
- computes all four parameters;
- reconstructs the greatest safe families for one, two, and three guards;
- checks all \(26(8-3)=130\) unoccupied state/attack obligations;
- reconstructs the exact lists (4.10) and their two colorings;
- checks the repeated cap on all four rim edges, including the fully
  dynamic edge \(x_2x_3\);
- enumerates all physical C-079 embeddings for all three anchors; and
- confirms the absence of a complement \(K_4\) and of a dominating pair.

The deterministic output is `result.json`.
