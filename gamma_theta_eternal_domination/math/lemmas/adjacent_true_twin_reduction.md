# Adjacent true-twin reduction

## Status and scope

`PROVED`, subject to independent review.

This note uses the standard one-guard-moves eternal domination model.  It
proves a reduction for adjacent true twins and, in particular, a necessary
condition on a minimum-order counterexample to the gamma--theta conjecture.
It does not resolve the conjecture.

Two distinct vertices \(u,v\) are **adjacent true twins** when
\[
  N_G[u]=N_G[v].
\]

## Static parameters

**Lemma 1.**  Let \(u,v\) be adjacent true twins in \(G\), and put
\(Q=G-v\).  Then
\[
  \gamma(Q)=\gamma(G),\qquad
  \alpha(Q)=\alpha(G),\qquad
  \theta(Q)=\theta(G).
\]

**Proof.**
For domination, first take a dominating set \(D\) of \(G\).  If \(v\notin
D\), then \(D\) dominates \(Q\).  If \(v\in D\) and \(u\notin D\), replace
\(v\) by \(u\); the closed-neighborhood equality preserves everything
dominated.  If \(u,v\in D\), delete \(v\), whose closed neighborhood is
already supplied by \(u\).  Thus \(\gamma(Q)\leq\gamma(G)\).

Conversely, every dominating set \(D\) of \(Q\) dominates \(G\).  Indeed,
if \(u\in D\), then \(u\) dominates \(v\).  If \(u\notin D\), some member
of \(D\) adjacent to \(u\) dominates \(u\), and that same member is
adjacent to \(v\).  Hence \(\gamma(G)\leq\gamma(Q)\).

Every independent set of \(Q\) is independent in \(G\), so
\(\alpha(Q)\leq\alpha(G)\).  Conversely, an independent set of \(G\)
contains at most one of \(u,v\).  If it contains \(v\), replacing \(v\) by
\(u\) preserves independence because \(u\) and \(v\) have identical
adjacency to every other vertex.  The resulting set lies in \(Q\), proving
\(\alpha(G)\leq\alpha(Q)\).

Deleting \(v\) from every part of a clique partition of \(G\), and
discarding an empty part if necessary, gives a clique partition of \(Q\).
Thus \(\theta(Q)\leq\theta(G)\).  In the other direction, take a clique
partition of \(Q\) and add \(v\) to the part containing \(u\).  Every
vertex in that part adjacent to \(u\) is also adjacent to \(v\), so the
enlarged part is a clique.  Hence \(\theta(G)\leq\theta(Q)\). \(\square\)

## Eternal domination

We use the following elementary consequence of the one-guard rules.

**Lemma 2 (maximum independent states are forced).**  Suppose
\(\mathcal F\) is an eternal family of \(k\)-sets and \(S\) is an
independent \(k\)-set.  Then \(S\in\mathcal F\).

**Proof.**
Start from any \(D\in\mathcal F\).  If \(S-D\) is nonempty, attack a vertex
\(s\in S-D\).  No guard already in \(S\) can respond because \(S\) is
independent.  Therefore a legal response moves a guard from \(D-S\) to
\(s\), increasing the intersection with \(S\) by one.  Repeating reaches
\(S\), and every intermediate state belongs to \(\mathcal F\). \(\square\)

This is included only to make the reduction self-contained; it is also the
accepted campaign result C-010.

**Theorem 3.**  Suppose
\[
  \gamma(G)=\gamma^\infty(G)=k
\]
and \(u,v\) are adjacent true twins.  For \(Q=G-v\),
\[
  \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=k,
  \qquad
  \theta(Q)=\theta(G).
\]

**Proof.**
Equality collapse gives \(\alpha(G)=k\).  Lemma 1 gives
\[
  \gamma(Q)=\alpha(Q)=k
  \quad\text{and}\quad
  \theta(Q)=\theta(G).
\]

Let \(\mathcal F\) be an eternal \(k\)-family in \(G\), and define
\[
  \mathcal F_Q=\{D\in\mathcal F:v\notin D\}.
\]
This restricted family is nonempty.  Indeed, \(Q\) has an independent
\(k\)-set \(S\), and Lemma 2 puts \(S\) in \(\mathcal F\).

Every member of \(\mathcal F_Q\) dominates \(Q\).  If
\(D\in\mathcal F_Q\) and an unoccupied vertex \(r\in V(Q)-D\) is attacked,
closure of \(\mathcal F\) supplies a legal one-guard successor
\[
  D'=D-\{w\}+\{r\}\in\mathcal F.
\]
Neither \(D\) nor the attacked vertex contains \(v\), so \(v\notin D'\).
Thus \(D'\in\mathcal F_Q\).  Consequently \(\mathcal F_Q\) is an eternal
\(k\)-family in \(Q\), and
\[
  \gamma^\infty(Q)\leq k.
\]
The general lower bound
\(\gamma(Q)\leq\gamma^\infty(Q)\), together with
\(\gamma(Q)=k\), proves equality. \(\square\)

**Corollary 4.**  A minimum-order counterexample to the gamma--theta
conjecture has no adjacent true twins.

**Proof.**
If a minimum-order counterexample \(G\) had adjacent true twins, Theorem 3
would make \(Q=G-v\) a smaller graph satisfying
\[
  \gamma(Q)=\gamma^\infty(Q)=k<\theta(Q),
\]
contradicting minimum order. \(\square\)

## Boundary checks

1. Adjacency of the twins is essential to the clique-partition argument.
   The theorem makes no claim about nonadjacent false twins.
2. The nonempty-family step is essential: simply intersecting an arbitrary
   family with the configurations avoiding a vertex could otherwise
   produce the empty set.  Lemma 2 supplies a surviving state here.
3. The attack in \(Q\) is unoccupied in exactly the same state in \(G\),
   and the successor changes exactly one guard along one graph edge.
4. The conclusion concerns a minimum-order counterexample.  It does not say
   that every equality graph is twin-free; rather, an adjacent true twin
   can be deleted while preserving the relevant parameters.
