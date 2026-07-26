# Alignment of near-hubs in the order-12 anti-\(C_7\) branch

**Status:** `PROVED_ACCEPTED_BY_INDEPENDENT_HOSTILE_REVIEW`.

**Claim boundary.**  This note gives a necessary condition for the surviving
induced-\(\overline{C_7}\) template and excludes its subbranch with at least
four near-hubs.  It does not exclude the full template, the connected
order-12 parameter-four slice, or any larger class.  No novelty claim is
made; this observation has not received a literature audit.

The eternal-domination parameter is the one-guard-moves parameter: attacks
occur only at unoccupied vertices, and one guard moves along one edge to the
attacked vertex.

## 1. Statement in \(G\)

The following local statement is slightly more general than the campaign
application.

**Theorem 1 (two-spoke alignment).**  Let \(G\) be a finite simple graph with
\(\gamma^\infty(G)\leq4\).  Suppose that \(A\subseteq V(G)\) induces a
seven-cycle, and let \(x,y\notin A\) be distinct.  If

\[
 N_G(x)\cap A=\{a\},
 \qquad
 N_G(y)\cap A=\{b\},
\]

then

\[
 xy\in E(G)
 \qquad\text{and}\qquad
 a=b.
\]

Thus two vertices having exactly one neighbor each on an induced \(C_7\)
must be adjacent and must use the same cycle neighbor.

The condition is sharp on the induced nine-vertex graph.  If \(xy\in E(G)\)
and \(a=b\), then the graph induced by \(A\cup\{x,y\}\) has one-guard eternal
domination number exactly four.

## 2. Definition-level forcing fact

We use the following elementary consequence of the exact one-guard
definition.

**Lemma 2 (independent-set forcing).**  Let \(\mathcal F\) be an eternal
family of \(k\)-guard configurations in a graph \(J\), and let \(I\) be an
independent \(k\)-set.  Then \(I\in\mathcal F\).  In particular,
\(\alpha(J)\leq\gamma^\infty(J)\).

**Proof.**  Starting from any member of \(\mathcal F\), attack unoccupied
vertices of \(I\).  A guard that moves to a vertex of \(I\) cannot come from
another vertex of \(I\), since \(I\) is independent.  Each response therefore
increases the number of guards on \(I\) by one.  With \(k\) guards, this
process reaches \(I\), and every reached configuration belongs to
\(\mathcal F\).

If an independent set has more than \(k\) vertices, the same process first
puts all \(k\) guards on it.  Attacking one of its remaining unoccupied
vertices then has no legal response.  Hence an eternal \(k\)-guard family
requires \(\alpha(J)\leq k\). \(\square\)

## 3. Proof of Theorem 1

Let

\[
 J=G[A\cup\{x,y\}].
\]

Accepted induced-subgraph monotonicity for the one-guard parameter gives

\[
 \gamma^\infty(J)\leq\gamma^\infty(G)\leq4.
\]

We prove that either failure of the claimed alignment forces
\(\gamma^\infty(J)\geq5\).

First suppose that \(xy\notin E(G)\).  After deleting any prescribed one or
two vertices from \(C_7\), three pairwise nonadjacent cycle vertices remain.
For completeness, label the cycle \(0,1,\ldots,6,0\), put \(a=0\), and use a
reflection if necessary.  If the cyclic distance from \(a\) to \(b\) is
\(0,1,2,\) or \(3\), respectively, one may take

\[
 \{1,3,5\},\quad
 \{2,4,6\},\quad
 \{1,3,5\},\quad
 \{1,4,6\}.
\]

Each displayed triple avoids both \(a\) and \(b\).  Its union with
\(\{x,y\}\) is therefore an independent five-set in \(J\), contrary to
Lemma 2 and \(\gamma^\infty(J)\leq4\).  Hence \(xy\in E(G)\).

It remains to rule out \(a\ne b\).  Relabel and reflect the cycle so that
\(a=0\), \(b=d\), and \(d\in\{1,2,3\}\).  Write \(C_7\) with edges between
consecutive residues, let \(x\) be adjacent on the cycle only to \(0\), let
\(y\) be adjacent on the cycle only to \(d\), and recall that \(xy\) is an
edge.

For each of the three possible values of \(d\), the displayed set \(D\) in
the following table is an independent four-set.  Lemma 2 therefore gives
\(\gamma^\infty(J)\geq4\); together with
\(\gamma^\infty(J)\leq4\), this gives equality and hence an eternal family
of four-sets.  Fix such a family.  Lemma 2 forces the displayed \(D\) into
it.  The first attack has only one response that is still a dominating set;
call it \(E\).  The listed second attack from \(E\) has no response that is
a dominating set.

| \(d\) | forced \(D\) | first attack and responses | second attack from \(E\) |
|---:|---|---|---|
| \(1\) | \(\{1,3,6,x\}\) | attack \(2\): \(1\to2\) gives \(E=\{2,3,6,x\}\); \(3\to2\) leaves \(4\) undominated | attack \(0\): \(6\to0\) leaves \(5\) undominated, while \(x\to0\) leaves \(y\) undominated |
| \(2\) | \(\{1,3,6,x\}\) | attack \(0\): \(1\to0\) gives \(E=\{0,3,6,x\}\); \(6\to0\) leaves \(5\) undominated, while \(x\to0\) leaves \(y\) undominated | attack \(2\): the sole move \(3\to2\) leaves \(4\) undominated |
| \(3\) | \(\{1,4,6,x\}\) | attack \(0\): \(6\to0\) gives \(E=\{0,1,4,x\}\); \(1\to0\) leaves \(2\) undominated, while \(x\to0\) leaves \(y\) undominated | attack \(3\): the sole move \(4\to3\) leaves \(5\) undominated |

All attacks in the table are at unoccupied vertices.  Every response listed
is exactly one guard move along an edge to the attacked vertex.  The
non-dominating successors cannot belong to an eternal family.  Consequently
the unique possible first successor \(E\) cannot belong to the family
either, because the displayed second attack defeats it.  The forced
configuration \(D\) therefore has no legal response within the family, a
contradiction.  This proves \(a=b\).

Finally suppose \(xy\in E(G)\) and \(a=b\).  On
\(J=G[A\cup\{x,y\}]\), the set \(\{a,x,y\}\) is a clique.  The remaining six
cycle vertices split into three consecutive cycle edges, so \(J\) has a
four-clique partition.  Placing one guard in each clique gives
\(\gamma^\infty(J)\leq4\) directly in the one-guard model.  The independent
set consisting of \(x\) and alternating vertices of the six-vertex path
\(A-\{a\}\) has size four, so Lemma 2 gives the reverse inequality.  Hence
\(\gamma^\infty(J)=4\), proving the stated sharpness. \(\square\)

## 4. Complement translation for the surviving template

Return to the connected order-12 parameter-four target and put
\(H=\overline G\).  Suppose \(H[A]\cong\overline{C_7}\).  Call
\(z\in V(H)\setminus A\) an **\(A\)-near-hub** if it is adjacent in \(H\) to
exactly six vertices of \(A\).  Equivalently, \(z\) has exactly one neighbor
on the induced cycle \(G[A]\).

**Corollary 3 (anti-\(C_7\) near-hub constraint).**  Any two
\(A\)-near-hubs are nonadjacent in \(H\), and they have the same unique
\(H\)-nonneighbor in \(A\).

**Proof.**  The target has \(\gamma^\infty(G)=4\), so Theorem 1 applies to
every pair of \(A\)-near-hubs.  Adjacency of the pair in \(G\) becomes
nonadjacency in \(H\), and their common unique cycle neighbor in \(G[A]\)
becomes their common unique nonneighbor in \(H[A]\). \(\square\)

The previously accepted hub constraint says that no outside vertex is
complete in \(H\) to \(A\).  Corollary 3 is strictly stronger information
at the next incidence layer: vertices missing only one antihole adjacency
cannot choose different gaps, and they form an independent set in \(H\).
This is a redundant necessary filter for the anti-\(C_7\) search branch.

## 5. An order-12 cap from P3

The pairwise alignment combines with the accepted property

\[
 \tag{P3}
 \forall T\in {V(H)\choose3}\quad
 \exists w\in V(H)\setminus T\quad T\subseteq N_H(w)
\]

and the accepted absence of an outside \(H\)-hub for an induced
\(\overline{C_7}\).

**Theorem 4 (at most three anti-\(C_7\) near-hubs).**  In a connected
order-12 parameter-four target, an induced \(\overline{C_7}\) in \(H\) has at
most three \(A\)-near-hubs among its five outside vertices.

**Proof.**  Label the underlying cyclic order on \(A\) as
\(0,1,\ldots,6,0\).  Suppose there are at least four near-hubs.  By
Corollary 3 they all have the same unique \(H\)-nonneighbor in \(A\); rotate
the labels so that this common gap is \(0\).

Consider the three rim triples

\[
 T_1=\{0,1,4\},\qquad
 T_2=\{0,2,5\},\qquad
 T_3=\{0,3,6\}.
\]

No vertex of \(A\) is a common \(H\)-neighbor of any \(T_i\).  Indeed, a
vertex of \(A\) is \(H\)-adjacent to every member of \(T_i\) exactly when its
closed neighborhood in the underlying \(C_7\) avoids \(T_i\).  For the
displayed triples, the unions of the corresponding closed cycle
neighborhoods are

\[
\begin{aligned}
 N_{C_7}[0]\cup N_{C_7}[1]\cup N_{C_7}[4]&=A,\\
 N_{C_7}[0]\cup N_{C_7}[2]\cup N_{C_7}[5]&=A,\\
 N_{C_7}[0]\cup N_{C_7}[3]\cup N_{C_7}[6]&=A.
\end{aligned}
\]

Thus P3 requires an outside common neighbor for each \(T_i\).  None of the
near-hubs can serve, because every one of them misses \(0\).  If all five
outside vertices were near-hubs, P3 would already fail for \(T_1\).  Hence
exactly four are near-hubs and there is a unique remaining outside vertex
\(z\).  P3 forces that same \(z\) to witness all three triples.  Since

\[
 T_1\cup T_2\cup T_3=A,
\]

the vertex \(z\) is adjacent in \(H\) to all of \(A\).  This is an outside
hub for the induced \(\overline{C_7}\), contradicting the accepted no-hub
theorem.  Hence there are at most three near-hubs. \(\square\)

Consequently the anti-\(C_7\) subbranch with four or five outside vertices of
\(H\)-degree six into \(A\) is empty.  This is a branch exclusion only at
that precisely stated incidence layer.

## 6. Dependencies and scope

The proof uses only:

1. the exact one-guard definition, from which Lemma 2 and the attack table are
   proved here; and
2. induced-subgraph monotonicity for one-guard eternal domination, proved in
   `math/reductions.md` and accepted in
   `reviews/reductions_hostile_review.md`;
3. for Theorem 4 only, property P3 from
   `math/lemmas/order12_k4_synthesis_target.md` and the anti-\(C_7\) no-hub
   theorem from `math/lemmas/order12_k4_hub_constraints.md`, both already
   adversarially accepted.

It does not use component additivity, the Strong Perfect Graph Theorem,
or an unproved placement symmetry.  Order twelve and P3 enter only in
Theorem 4; Theorem 1 and Corollary 3 do not need them.  Connectedness is a
standing target hypothesis in Theorem 4 but is not used by its proof.
