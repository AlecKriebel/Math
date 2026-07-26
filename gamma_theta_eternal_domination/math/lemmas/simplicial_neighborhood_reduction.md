# Simplicial closed-neighborhood reduction

## Status and claim boundary

**Draft pending independent adversarial review.**

This note generalizes the leaf--support reduction.  It is written entirely
for the standard one-guard-moves eternal domination model: attacks occur
only at unoccupied vertices, and exactly one guard moves along one graph
edge to the attacked vertex.

The claim is a reduction, not a resolution of the universal
\(\gamma\)--\(\theta\) conjecture.  No novelty claim is made until the
literature and adversarial audits are complete.

## 1. Exact reduction

A vertex \(v\) is **simplicial** when its closed neighborhood \(N[v]\) is a
clique.

### Theorem 1

Let \(G\) be a finite simple graph with

\[
 \gamma(G)=\gamma^\infty(G)=k,
\]

let \(v\) be simplicial, and suppose

\[
 Q=G-N[v]
\]

is nonempty.  Then

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=k-1,
\tag{1.1}
\]

\(Q\) is well-covered, and

\[
 \theta(G)=\theta(Q)+1.
\tag{1.2}
\]

#### Proof

The parameter chain gives

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=k,
\]

so every maximal independent set of \(G\) has size \(k\).

Let \(I\) be any maximal independent set of \(Q\).  Then
\(I\cup\{v\}\) is independent and maximal in \(G\): the guard position
\(v\) blocks every vertex of \(N(v)\), while maximality of \(I\) inside
\(Q\) blocks every vertex of \(Q-I\).  Therefore

\[
 |I|=k-1.
\]

This holds for every maximal independent set of \(Q\).  Hence \(Q\) is
well-covered and

\[
 i(Q)=\alpha(Q)=k-1.
\tag{1.3}
\]

In particular, \(\gamma(Q)\leq k-1\).  If \(A\) dominated \(Q\) with
\(|A|\leq k-2\), then \(A\cup\{v\}\) would dominate \(G\), because \(v\)
dominates all of \(N[v]\).  This would contradict \(\gamma(G)=k\).
Consequently

\[
 \gamma(Q)=k-1.
\tag{1.4}
\]

Fix an eternal dominating family \(\mathcal D\) of \(k\)-sets in \(G\).
Every independent \(k\)-set belongs to every eternal \(k\)-family: starting
from an arbitrary family state, attack its unoccupied target-set vertices
one by one; independence prevents a guard already on the target set from
responding, so each one-guard response increases target occupancy by one.

Choose a maximum independent set \(I\) of \(Q\).  The independent
\(k\)-set \(I\cup\{v\}\) therefore belongs to \(\mathcal D\).  Define

\[
 \mathcal E=
 \{D-\{v\}:D\in\mathcal D,\ v\in D\}.
\tag{1.5}
\]

This family is nonempty.  Moreover, no state \(D\in\mathcal D\) containing
\(v\) can contain a second vertex \(u\in N(v)\).  If it did, then
\(D-\{v\}\) would still dominate \(G\).  Indeed, because \(N[v]\) is a
clique, \(u\) dominates every vertex that \(v\) can dominate; vertices in
\(Q\) are not adjacent to \(v\) and were already dominated by other guards.
This would contradict \(\gamma(G)=k\).

It follows that every member of \(\mathcal E\) is a \((k-1)\)-subset of
\(Q\).  If \(B=D-\{v\}\in\mathcal E\), then \(B\) dominates \(Q\), since
\(D\) dominates \(G\) and \(v\) has no neighbor in \(Q\).

Let \(r\in V(Q)-B\) be attacked.  This attack is unoccupied in
\(D=B\cup\{v\}\).  Eternal closure supplies a guard

\[
 u\in D\cap N_G(r)
\]

such that

\[
 D'=(D-\{u\})\cup\{r\}\in\mathcal D.
\]

The vertex \(v\) has no neighbor in \(Q\), so \(u\neq v\).  Hence \(D'\)
still contains \(v\), and

\[
 D'-\{v\}=(B-\{u\})\cup\{r\}\in\mathcal E.
\]

Thus \(\mathcal E\) is a nonempty family of dominating \((k-1)\)-sets of
\(Q\), closed against every unoccupied attack by one guard moving along one
edge.  Therefore

\[
 \gamma^\infty(Q)\leq k-1.
\]

Equation (1.3) and the general lower bound
\(\alpha(Q)\leq\gamma^\infty(Q)\) give equality and complete (1.1).

For the clique-cover identity, the clique \(N[v]\), together with a minimum
clique partition of \(Q\), gives

\[
 \theta(G)\leq\theta(Q)+1.
\tag{1.6}
\]

Conversely, let \(\mathcal P\) be a minimum clique partition of \(G\), and
consider all parts that intersect \(N[v]\).  The part containing \(v\) lies
entirely in \(N[v]\), because \(v\) has no neighbor in \(Q\).  Replace all
parts meeting \(N[v]\) by the single clique \(N[v]\) and by the nonempty
remainders obtained after deleting \(N[v]\) from those parts.  Every
remainder is still a clique.  Since the old part containing \(v\) has empty
remainder, this replacement does not increase the number of parts.
Minimality of \(\mathcal P\) means that the resulting partition is also
minimum.  It has \(N[v]\) as one part, so deleting that part gives a clique
partition of \(Q\) with \(\theta(G)-1\) parts.  Hence

\[
 \theta(Q)\leq\theta(G)-1.
\tag{1.7}
\]

Equations (1.6)--(1.7) prove (1.2). \(\square\)

If \(Q\) is empty, then \(N[v]=V(G)\) is a clique and \(G\) is complete, so
it cannot be a counterexample.  The nonempty-\(Q\) hypothesis only avoids
empty-graph parameter conventions.

## 2. Consequences for a counterexample

### Corollary 2

If, under the hypotheses of Theorem 1,

\[
 \gamma(G)=\gamma^\infty(G)=k<\theta(G),
\]

then \(Q=G-N[v]\) is a smaller counterexample with

\[
 \gamma(Q)=\gamma^\infty(Q)=k-1<\theta(Q).
\]

#### Proof

Theorem 1 gives
\(\gamma(Q)=\gamma^\infty(Q)=k-1\) and
\(\theta(Q)=\theta(G)-1\).  Since \(\theta(G)\geq k+1\),
\(\theta(Q)\geq k>k-1\). \(\square\)

### Corollary 3

Every minimum-order counterexample to the \(\gamma\)--\(\theta\) conjecture
is connected and has no simplicial vertex.  In particular, it has minimum
degree at least two, and the two neighbors of every degree-two vertex are
nonadjacent.

#### Proof

The accepted component-additivity reduction makes every minimum-order
counterexample connected.  If it had a simplicial vertex \(v\), then either
\(G-N[v]\) would be a smaller counterexample by Corollary 2 or it would be
empty, in which case \(G\) would be complete and not a counterexample.
Thus no vertex is simplicial.

A connected graph of order at least two with a leaf has a simplicial leaf,
so the minimum degree is at least two.  A degree-two vertex with adjacent
neighbors is simplicial, proving the final statement. \(\square\)

## 3. Exact scope

Theorem 1 preserves the equality \(\gamma=\gamma^\infty\) and the strict
gap to \(\theta\), but it does not say that arbitrary vertex deletion or
arbitrary closed-neighborhood deletion has this behavior.  Simpliciality is
used twice: to make one neighboring guard render \(v\) redundant in a
minimum dominating state, and to consolidate a minimum clique partition
around \(N[v]\).

The result supplies a structural condition on a minimum counterexample.  It
does not exclude nonsimplicial graphs, prove a universal minimum-order
bound by itself, or resolve the conjecture.
