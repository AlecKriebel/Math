# Maximum independent states and private-neighborhood obstructions

## Status

Proved from the one-guard family definition on 2026-07-25 and accepted by an
independent hostile review. The audit and its exhaustive computational checks
are recorded in `reviews/private_lemma_hostile_review.md`.

Throughout, attacks are only at unoccupied vertices and exactly one guard
moves along one edge.

## 1. Every maximum independent set is forced into the family

**Lemma 1.** Let \(\mathcal F\) be an eternal dominating family of \(k\)-sets
in \(G\). If \(S\) is an independent set of cardinality \(k\), then
\(S\in\mathcal F\).

**Proof.** Start with any \(D\in\mathcal F\). While some vertex
\(s\in S-D\) is unoccupied, attack \(s\). A defending guard adjacent to \(s\)
cannot occupy another vertex of \(S\), because \(S\) is independent.
Therefore each response increases \(|D\cap S|\) by exactly one. Closure of
\(\mathcal F\) keeps every resulting configuration in the family. After
\(k-|D\cap S|\) attacks, all \(k\) guards occupy \(S\), so the resulting
configuration is \(S\in\mathcal F\). \(\square\)

**Corollary 2.** If \(\gamma^\infty(G)=\alpha(G)=k\), then every maximum
independent set of \(G\) belongs to every eternal family of \(k\)-sets.

This is stronger than the existence of one strategically useful maximum
independent set: the attacker may choose any maximum independent set before
starting the forcing sequence.

## 2. Exact one-step swap criterion

For a dominating set \(D\) and \(u\in D\), define the closed private
neighborhood of \(u\) relative to \(D\) by

\[
 P_D(u)=\{x\in V(G):N[x]\cap D=\{u\}\}.
\]

Thus \(P_D(u)\) is the set of vertices whose unique dominator in \(D\) is
\(u\).

**Lemma 3 (swap criterion).** Let \(D\) dominate \(G\), let \(r\notin D\),
and let \(u\in D\cap N(r)\). Put

\[
 D'=(D-\{u\})\cup\{r\}.
\]

Then \(D'\) dominates \(G\) if and only if

\[
 P_D(u)\subseteq N[r].
\]

**Proof.** Every vertex outside \(P_D(u)\) has a dominator in
\(D-\{u\}\), so it remains dominated after the swap. A vertex in \(P_D(u)\)
loses its unique old dominator and is dominated by \(D'\) exactly when it
lies in the closed neighborhood of the new guard \(r\). \(\square\)

When \(D=S\) is independent, \(u\in P_S(u)\), so the containment itself
implies \(ur\in E(G)\).

## 3. A local obstruction to equality

**Theorem 4 (private-neighborhood obstruction).** Suppose
\(\alpha(G)=k\). If \(\gamma^\infty(G)=k\), then for every maximum
independent set \(S\), and every \(r\in V(G)-S\), there exists \(u\in S\)
such that

\[
 P_S(u)\subseteq N[r].
\]

Equivalently, every maximum independent set is a secure dominating set.

**Proof.** By Corollary 2, \(S\) belongs to every eternal \(k\)-family.
Attack \(r\). Closure supplies a one-guard response
\(S'=(S-\{u\})\cup\{r\}\) that remains in the family and hence dominates.
Lemma 3 gives the displayed containment. \(\square\)

The contrapositive is a short, independently checkable lower-bound
certificate:

**Corollary 5.** If some maximum independent set \(S\) and
\(r\notin S\) satisfy

\[
 \text{for every }u\in S\cap N(r),\qquad
 P_S(u)-N[r]\ne\varnothing,
\]

then \(\gamma^\infty(G)\geq\alpha(G)+1\).

For each possible defending guard, one may certify failure by naming one
vertex \(x_u\in P_S(u)-N[r]\) that becomes undominated after the swap.
Indeed, Theorem 4 first gives
\(\gamma^\infty(G)\ne\alpha(G)\); the general bound
\(\alpha(G)\leq\gamma^\infty(G)\) and integrality then give the stated
inequality.

## 4. Search use and limits

The obstruction is safe as a fast rejection test for the equality
\(\alpha=\gamma^\infty\), and its failure has a compact human-readable
certificate. It is not sufficient for eternal domination: passing every
one-step test at every maximum independent set does not establish closure
after non-independent configurations are reached.

This failure of sufficiency already occurs for \(C_7\): the local test finds
no obstruction, while exact one-guard evaluation gives
\(\alpha(C_7)=3<4=\gamma^\infty(C_7)\).

For a conjectural counterexample, the equality collapse additionally gives
\(\gamma=\alpha\) and well-coveredness. Those separate requirements must not
be inferred from Theorem 4.
