# A complement-side dictionary for the \(k=3\) slice

## Status

Proved directly on 2026-07-25 and accepted by
`reviews/complement_k3_hostile_review.md`. This note is a search reduction,
not a resolution of the \(k=3\) slice.

Let \(G\) be a finite simple graph and put \(H=\overline G\). All
neighborhoods in the statements below are taken in the indicated graph.

## 1. Static parameters

**Proposition 1.** The following statements hold.

1. \(\alpha(G)=\omega(H)\) and \(\theta(G)=\chi(H)\).
2. A set \(D\subseteq V(G)\) dominates \(G\) if and only if there is no
   vertex \(x\notin D\) such that \(D\subseteq N_H(x)\).
3. A pair \(\{u,v\}\) dominates \(G\) if and only if \(u\) and \(v\) have no
   common neighbor in \(H\) outside the pair.
4. If \(\omega(H)=3\), then \(\gamma(G)=3\) if and only if every pair of
   vertices of \(H\) has a common neighbor.
5. If \(\omega(H)=3\), then \(G\) is well-covered if and only if every
   maximal clique of \(H\) is a triangle.

**Proof.** Independent sets in \(G\) are precisely cliques in \(H\), while
clique partitions of \(G\) are precisely proper colorings of \(H\); this
proves (1).

A vertex \(x\notin D\) is undominated by \(D\) in \(G\) exactly when it is
nonadjacent in \(G\) to every member of \(D\). Complementing adjacency, this
is exactly \(D\subseteq N_H(x)\), proving (2). Specializing to a pair gives
(3); a common neighbor cannot equal either endpoint in a simple graph.

If \(\omega(H)=3\), a triangle of \(H\) is a maximum clique and hence a
maximal clique. The corresponding independent triple in \(G\) is maximal
independent and therefore dominates, so \(\gamma(G)\leq3\). By (3), every
pair has a common neighbor exactly when no pair dominates \(G\). This also
rules out a dominating singleton, and proves (4).

Finally, maximal independent sets in \(G\) are precisely maximal cliques in
\(H\). Under \(\omega(H)=3\), all of them have size three exactly when every
maximal clique of \(H\) is a triangle. This proves (5). \(\square\)

## 2. The one-guard game in the complement

Call a set \(D\subseteq V(H)\) **externally uncontained** if

\[
  D\not\subseteq N_H(x)\qquad\text{for every }x\notin D.
\]

By Proposition 1(2), these are exactly the dominating configurations of
\(G\).

**Proposition 2.** A family \(\mathcal F\) of \(k\)-subsets is a one-guard
eternal dominating family in \(G\) if and only if:

1. \(\mathcal F\) is nonempty and every member is externally uncontained in
   \(H\); and
2. for every \(D\in\mathcal F\) and every \(r\notin D\), there is a vertex
   \(u\in D\) with \(ur\notin E(H)\) such that
   \((D-\{u\})\cup\{r\}\in\mathcal F\).

**Proof.** The first condition is Proposition 1(2). An edge \(ur\) of \(G\)
is a nonedge of \(H\), so the second condition is exactly the requirement
that one guard move along one edge of \(G\) to the unoccupied attacked
vertex, with the successor remaining in the family. \(\square\)

When \(k=\alpha(G)=3\), every triangle of \(H\) belongs to every eternal
three-guard family: triangles of \(H\) are independent triples of \(G\), so
this is Lemma 1 of `maximum_independent_states.md`.

## 3. Exact complement target for a \(k=3\) counterexample

By Corollaries 6 and 11 of `math/reductions.md`, every parameter-three
counterexample is connected: its counterexample component already has
domination number at least three, which exhausts the total domination number.

Consequently, a \(k=3\) counterexample \(G\) would yield a graph
\(H=\overline G\) satisfying all of the following:

1. \(\omega(H)=3<\chi(H)\);
2. every pair of vertices of \(H\) has a common neighbor;
3. every maximal clique of \(H\) is a triangle;
4. \(\overline H\) is connected; and
5. there is a nonempty closed family of externally uncontained triples under
   the nonedge moves in Proposition 2, necessarily containing every triangle
   of \(H\).

Conversely, any \(H\) with (1), (2), (4), and (5) has
\[
 \gamma(\overline H)=\alpha(\overline H)
 =\gamma^\infty(\overline H)=3<\theta(\overline H).
\]
Condition (3) then follows automatically from the equality collapse, but it
is retained as a cheap independently checkable generation filter.

This dictionary supplies direct constraints for the \((n,k)=(12,3)\)
synthesis lane. It does not replace the eternal-family condition with a
static graph property.
