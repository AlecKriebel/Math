# Independent-antineighborhood projection

## Status and claim boundary

**Draft pending independent adversarial review.**

This note concerns the standard one-guard-moves eternal domination model:
attacks occur only at unoccupied vertices, exactly one adjacent guard moves
to the attacked vertex, and every resulting configuration dominates.

The theorem projects an arbitrary eternal family after fixing any independent
set of guards.  It does not assert a clique-cover identity for the original
graph.  The clique-cover conclusion below uses minimum-counterexample
minimality, not an unproved monotonicity rule.

No novelty claim is made pending a dedicated literature audit.

## 1. Exact projection theorem

For \(A\subseteq V(G)\), write

\[
 N[A]=\bigcup_{a\in A}N[a].
\]

### Theorem 1

Let \(G\) be a finite simple graph with

\[
 \gamma(G)=\gamma^\infty(G)=k,
\tag{1.1}
\]

let \(A\) be an independent set of size \(t<k\), and put

\[
 Q=G-N[A].
\tag{1.2}
\]

Then \(Q\) is nonempty and well-covered, and

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=k-t.
\tag{1.3}
\]

#### Proof

The accepted parameter chain first gives

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=k.
\tag{1.4}
\]

Thus every maximal independent set of \(G\) has size \(k\).

Let \(I\) be any maximal independent set of \(Q\).  The set \(I\cup A\)
is independent in \(G\).  It is maximal there: every vertex of
\(N[A]-A\) is adjacent to a vertex of \(A\), and every vertex of \(Q-I\)
is adjacent to a vertex of \(I\) by maximality inside \(Q\).  Equation
(1.4) therefore gives

\[
 |I|=k-t.
\tag{1.5}
\]

This holds for every maximal independent set of \(Q\).  Consequently \(Q\)
is well-covered and

\[
 i(Q)=\alpha(Q)=k-t.
\tag{1.6}
\]

In particular \(Q\) is nonempty because \(t<k\), and
\(\gamma(Q)\leq k-t\).

Conversely, suppose that \(B\) dominates \(Q\) with
\(|B|\leq k-t-1\).  The set \(A\) dominates all of \(N[A]\), while \(B\)
dominates \(Q\).  Hence \(A\cup B\) dominates \(G\) with at most \(k-1\)
vertices, contrary to \(\gamma(G)=k\).  Thus

\[
 \gamma(Q)=k-t.
\tag{1.7}
\]

It remains to prove the eternal equality with the exact online
quantifiers.  Fix an arbitrary eternal dominating family \(\mathcal D\) of
\(k\)-sets in \(G\).  We use the accepted independent-set forcing fact:
every independent \(k\)-set belongs to every eternal \(k\)-family.  Indeed,
attack its unoccupied vertices one at a time.  Independence prevents a
guard already on the target set from responding, so every response
increases target occupancy by one.

Choose a maximum independent set \(I\) of \(Q\).  Equations (1.5)--(1.6)
show that \(A\cup I\) is an independent \(k\)-set, so
\(A\cup I\in\mathcal D\).  Define the restricted slice

\[
 \mathcal E=
 \{D-A:D\in\mathcal D,\ A\subseteq D,\ D-A\subseteq V(Q)\}.
\tag{1.8}
\]

This family is nonempty and every member has size \(k-t\).

Let \(C\in\mathcal E\), so \(D=A\cup C\in\mathcal D\).  The guards in
\(C\) dominate \(Q\): the state \(D\) dominates \(G\), while no vertex of
\(A\) has a neighbor in \(Q\) by (1.2).

Now fix an arbitrary unoccupied attack

\[
 r\in V(Q)-C.
\]

It is also unoccupied in \(D\).  Eternal closure supplies a guard

\[
 u\in D\cap N_G(r)
\]

such that

\[
 D'=(D-\{u\})\cup\{r\}\in\mathcal D.
\tag{1.9}
\]

No vertex of \(A\) is adjacent to \(r\), so \(u\notin A\).  Since every
other guard of \(D\) lies in \(Q\), we have \(u\in C\).  The successor
therefore still contains all of \(A\), all its remaining guards lie in
\(Q\), and

\[
 D'-A=(C-\{u\})\cup\{r\}\in\mathcal E.
\tag{1.10}
\]

Thus, for every \(C\in\mathcal E\) and every \(r\in V(Q)-C\), there exists
one adjacent guard \(u\in C\) whose single move to \(r\) remains in
\(\mathcal E\).  Every state of \(\mathcal E\) dominates \(Q\), so
\(\mathcal E\) is an eternal dominating family of \((k-t)\)-sets in \(Q\).
Hence

\[
 \gamma^\infty(Q)\leq k-t.
\]

The general lower bound
\(\alpha(Q)\leq\gamma^\infty(Q)\), together with (1.6), proves equality
and completes (1.3). \(\square\)

## 2. Minimum-counterexample consequence

### Corollary 2

Let \(G\) be a minimum-order counterexample to the
\(\gamma\)--\(\theta\) conjecture, with

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=k<\theta(G).
\]

For every nonempty independent set \(A\) of size \(t<k\), the proper
induced graph

\[
 Q=G-N[A]
\]

satisfies

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=\theta(Q)=k-t.
\tag{2.1}
\]

#### Proof

Theorem 1 gives every equality in (2.1) except the one involving
\(\theta(Q)\).  The general chain gives

\[
 \theta(Q)\geq\gamma^\infty(Q)=k-t.
\]

If \(\theta(Q)>k-t\), then \(Q\) would itself be a smaller counterexample,
contrary to the choice of \(G\).  Thus equality holds. \(\square\)

This argument does not claim that
\(\theta(G)=\theta(Q)+t\).  Such an identity is generally unavailable;
minimum-counterexample minimality is exactly what supplies \(\theta(Q)\).

## 3. Complement formulation

Put \(H=\overline G\).  An independent set \(A\) of \(G\) is a clique of
\(H\), and

\[
 V(G)-N_G[A]
 =
 \bigcap_{a\in A}N_H(a).
\tag{3.1}
\]

Write the right side as \(N_H(A)\), the common open neighborhood of \(A\).
For the induced graph \(Q=G-N_G[A]\),

\[
 \alpha(Q)=\omega(H[N_H(A)]),\qquad
 \theta(Q)=\chi(H[N_H(A)]).
\tag{3.2}
\]

Corollary 2 therefore becomes the following exact local condition.

### Corollary 3

If \(G\) is a minimum-order counterexample with common parameter \(k\) and
\(H=\overline G\), then every nonempty clique \(A\) of \(H\), of size
\(t<k\), has nonempty common neighborhood and

\[
 \chi(H[N_H(A)])
 =
 \omega(H[N_H(A)])
 =
 k-t.
\tag{3.3}
\]

In particular:

1. every vertex neighborhood in \(H\) has chromatic and clique number
   \(k-1\);
2. the common neighborhood of every \((k-1)\)-clique is nonempty and
   independent; and
3. for \(k\geq3\), the common neighborhood of every
   \((k-2)\)-clique is bipartite and contains an edge.

Consequently no odd cycle of \(H\) is complete to a
\((k-2)\)-clique.  For \(k=3\), this is the odd-wheel obstruction: every
open neighborhood in \(H\) is bipartite.  The earlier induced-odd-wheel
formulation is equivalent, because every non-bipartite graph contains a
shortest odd cycle, and such a shortest odd cycle is induced.

## 4. Exact scope

Theorem 1 applies to every graph satisfying
\(\gamma=\gamma^\infty\), not only to counterexamples and not only to
simplicial vertices.  It preserves \(\gamma=\alpha=\gamma^\infty\) after
deleting the closed neighborhood of an independent set.

It does not by itself preserve a strict gap to \(\theta\).  Corollaries
2--3 require a minimum-order counterexample so that the conjecture is
already valid on every proper induced graph.  No universal resolution
follows merely from the local equalities.
