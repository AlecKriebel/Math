# Current-byte addendum: adjacent true-twin reduction

**Review date:** 2026-07-27 (PDT)
**Target:** `math/lemmas/adjacent_true_twin_reduction.md`
**Target SHA-256:** `5a342d37a5d03622f7542cec17a02d84d9e052bc8884c626e18916aae83daac6`
**Verdict:** **PASS**

This addendum independently reconstructs the current target bytes because
the earlier hostile review was bound to a prior version.  No computation is
used.

## Lemma 1: static identities

Let \(u,v\) be adjacent true twins and \(Q=G-v\).

- **Domination from \(G\) to \(Q\).**  A dominating set avoiding \(v\)
  already dominates \(Q\).  If it contains \(v\) but not \(u\), replacing
  \(v\) by \(u\) preserves the union of closed neighborhoods.  If it
  contains both, deleting \(v\) is safe because \(u\) supplies the same
  closed neighborhood.  Hence \(\gamma(Q)\leq\gamma(G)\).
- **Domination from \(Q\) to \(G\).**  If a dominating set of \(Q\)
  contains \(u\), it dominates the adjacent twin \(v\).  Otherwise a guard
  adjacent to \(u\) dominates \(u\), and closed-neighborhood equality makes
  that guard adjacent to \(v\) as well.  Hence \(\gamma(G)\leq\gamma(Q)\).
- **Independence.**  An independent set contains at most one of the
  adjacent twins.  Replacing \(v\), when present, by \(u\) preserves every
  nonadjacency to the remaining vertices.  Therefore
  \(\alpha(Q)=\alpha(G)\).
- **Clique partition.**  Restriction of a clique partition gives
  \(\theta(Q)\leq\theta(G)\).  Conversely, add \(v\) to the part containing
  \(u\).  Adjacency \(uv\) and identical adjacency to every third vertex
  make the enlarged part a clique.  Thus
  \(\theta(G)\leq\theta(Q)\).

All three identities in Lemma 1 are correct.  Adjacency of the twins is
used essentially in both the independence and clique-partition arguments.

## Theorem 3: eternal-family restriction

From

\[
 \gamma(G)=\gamma^\infty(G)=k
\]

the standard parameter chain gives \(\alpha(G)=k\).  Lemma 1 therefore
gives

\[
 \gamma(Q)=\alpha(Q)=k,\qquad \theta(Q)=\theta(G).
\]

Take an arbitrary eternal \(k\)-family \(\mathcal F\) in \(G\), and retain
only states avoiding \(v\):

\[
 \mathcal F_Q=\{D\in\mathcal F:v\notin D\}.
\]

This slice is nonempty for a valid reason.  Since \(\alpha(Q)=k\), there is
an independent \(k\)-set \(S\subseteq V(Q)\).  The maximum-independent-state
forcing argument puts \(S\) in every eternal \(k\)-family, so
\(S\in\mathcal F_Q\).

Every retained state dominates \(Q\).  For
\(D\in\mathcal F_Q\) and an unoccupied attack
\(r\in V(Q)-D\), the same attack is unoccupied in \(G\).  Closure of
\(\mathcal F\) supplies one guard

\[
 w\in D\cap N_G(r)
\]

and successor

\[
 D'=(D-\{w\})\cup\{r\}\in\mathcal F.
\]

Because \(D\) avoids \(v\), the responding guard cannot be \(v\); because
the attack lies in \(Q\), the successor also avoids \(v\).  Both \(w,r\)
lie in \(Q\), so their move edge in \(G\) is the same edge in the induced
graph \(Q\).  Hence \(D'\in\mathcal F_Q\), proving literal one-guard
closure in \(Q\).

Thus \(\gamma^\infty(Q)\leq k\), while
\(\gamma(Q)\leq\gamma^\infty(Q)\) and \(\gamma(Q)=k\) give

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=k.
\]

There is no occupied attack, no all-guards move, and no hidden requirement
to replace a guard at the deleted vertex.

## Corollary 4: minimum counterexample

If a minimum-order counterexample \(G\) contained adjacent true twins,
Theorem 3 and Lemma 1 would give the strictly smaller graph \(Q=G-v\) with

\[
 \gamma(Q)=\gamma^\infty(Q)=k<\theta(Q)=\theta(G).
\]

This is itself a counterexample, regardless of whether \(Q\) is connected,
contradicting minimum order.  Therefore the corollary is correct.

## Conclusion

The current target bytes pass.  No static lifting gap, nonempty-family gap,
quantifier reversal, or one-guard-model error was found in Lemma 1,
Theorem 3, or Corollary 4.
