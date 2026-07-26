# Hub constraints for the surviving order-12, parameter-four templates

**Status:** `PROPOSED_PROOF_PENDING_ADVERSARIAL_REVIEW`.

**Claim boundary.**  This note does not exclude any of the surviving
\(C_5,C_7,\overline{C_7}\) branches and does not prove a finite or universal
nonexistence result.  It derives cheap necessary conditions from accepted
one-guard monotonicity and component additivity.

Let \(G\) satisfy \(\gamma^\infty(G)=4\), put \(H=\overline G\), and let
\(C\) be an induced odd hole in \(H\).  A vertex outside \(C\) is a **hub**
if it is adjacent in \(H\) to every rim vertex.

## 1. The one-guard value one

**Lemma 1.**  A nonempty graph \(J\) has
\(\gamma^\infty(J)=1\) if and only if \(J\) is complete.

**Proof.**  If \(J\) is complete, the family of all singleton configurations
is an eternal family: every singleton dominates, and the sole guard can move
along an edge to any attacked vertex.

Conversely, let \(\mathcal F\) be an eternal family of singleton
configurations and choose \(\{u\}\in\mathcal F\).  For every \(r\ne u\), an
attack at \(r\) forces \(ur\in E(J)\) and \(\{r\}\in\mathcal F\).  Applying
the family condition from each resulting singleton \(\{r\}\) shows that
\(r\) is adjacent to every other vertex.  Hence every vertex is universal
and \(J\) is complete. \(\square\)

## 2. Hubs of an odd hole

**Theorem 2.**  The hubs of \(C\) form an independent set in \(H\).

**Proof.**  Let \(X\) be the hub set.  There is nothing to prove if
\(X=\varnothing\).  Every hub is nonadjacent in \(G\) to every rim vertex,
while \(G[V(C)]=\overline C\).  Therefore

\[
 G[V(C)\cup X]=\overline C\mathbin{\dot\cup}G[X].
\]

The accepted odd-antihole value is
\(\gamma^\infty(\overline C)=3\).  Induced-subgraph monotonicity and
component additivity give

\[
 3+\gamma^\infty(G[X])
 =\gamma^\infty\!\left(G[V(C)\cup X]\right)
 \leq\gamma^\infty(G)=4.
\]

Since \(X\) is nonempty, \(\gamma^\infty(G[X])\geq1\), so equality holds and
\(\gamma^\infty(G[X])=1\).  Lemma 1 makes \(G[X]\) complete.  Equivalently,
\(H[X]\) is edgeless. \(\square\)

This argument is explicitly one-guard: it uses the accepted one-guard values,
induced-subgraph monotonicity, and component additivity, not an
all-guards-move result.

## 3. The antihole branch has no hub

**Theorem 3.**  If \(H\) contains an induced \(\overline{C_7}\) on a vertex
set \(A\), no vertex outside \(A\) is adjacent in \(H\) to every vertex of
\(A\).

**Proof.**  Suppose \(x\) were such a vertex.  Then
\(G[A]=C_7\), and \(x\) has no \(G\)-neighbor in \(A\).  The induced
subgraph on \(A\cup\{x\}\) is consequently

\[
 K_1\mathbin{\dot\cup}C_7.
\]

The accepted one-guard odd-cycle value gives
\(\gamma^\infty(C_7)=4\).  Component additivity and induced-subgraph
monotonicity would imply

\[
 5=1+\gamma^\infty(C_7)
 =\gamma^\infty(K_1\mathbin{\dot\cup}C_7)
 \leq\gamma^\infty(G)=4,
\]

a contradiction. \(\square\)

## 4. P3 bounds the number of hole hubs

Now assume additionally that \(H\) satisfies

\[
 \tag{P3}
 \forall A\in{V(H)\choose3}\quad
 \exists x\notin A\quad A\subseteq N_H(x),
\]

as it must when \(\gamma(G)=4\).  Let \(R=V(C)\), let
\(Y=V(H)\setminus R\), and write \(r=|Y|\) and \(t\) for the number of hubs
in \(Y\).

**Theorem 4.**  If \(r\geq2\), then \(t\leq r-2\).

**Proof.**  By Theorem 2, distinct hubs are nonadjacent in \(H\).

If \(t=r\), choose a hub \(a\) and a rim edge \(uv\).  No rim vertex is
adjacent in the induced cycle to both endpoints of a rim edge.  No other
outside vertex can witness (P3) for \(\{a,u,v\}\), because every such vertex
is a hub and hence is nonadjacent to \(a\).  This contradicts (P3).

If \(t=r-1\), write \(Y\setminus X=\{y\}\), where \(X\) is the hub set.
Fix \(a\in X\).  For every rim edge \(uv\), the preceding argument eliminates
every rim vertex and every hub other than \(a\) as a witness for
\(\{a,u,v\}\).  Thus (P3) forces \(y\) to be adjacent in \(H\) to \(a,u,v\).
As this holds for every rim edge, \(y\) is adjacent to every rim vertex and
is itself a hub, contradicting \(y\notin X\).

Both \(t=r\) and \(t=r-1\) are impossible, so \(t\leq r-2\). \(\square\)

## 5. Order-12 search consequences

For a connected order-12 parameter-four target, the accepted structural
split now has the following necessary hub conditions.

1. An induced \(C_5\) has seven outside vertices and at most five hubs; those
   hubs are pairwise nonadjacent in \(H\).
2. An induced \(C_7\) has five outside vertices and at most three hubs; those
   hubs are pairwise nonadjacent in \(H\).
3. An induced \(\overline{C_7}\) is hub-free in the stronger antihole sense
   of Theorem 3.

These restrictions may be added as redundant search checks after independent
review.  They do not justify fixing a template and the anchored
\(H\)-\(K_4\) on unrelated labels without an orbit-complete placement
argument.
