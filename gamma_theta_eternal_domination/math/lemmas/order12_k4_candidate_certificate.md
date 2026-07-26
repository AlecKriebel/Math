# Soundness of the decoded order-12, parameter-four candidate certificate

## Status

This note specifies and proves the acceptance implication of
`src/verifier_k4_candidate`.  It does not assert that an accepted candidate
exists, and it gives no finite exclusion.

## Certificate theorem

Let \(G\) be the labeled graph on \(\{0,\ldots,11\}\) encoded by a candidate
JSON file.  Suppose the independent verifier reports
`mathematical_counterexample_verified=true`.  Then

\[
  \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=4<\theta(G).
\]

In particular, an accepted file is a counterexample to the
\(\gamma\)--\(\theta\) conjecture in the one-guard-moves model.

### Proof

The verifier checks explicitly that the declared four-set dominates \(G\).
It also examines every three-set and rejects if one dominates.  Domination is
upward closed, so a dominating set of size at most three would extend to a
dominating three-set.  Hence \(\gamma(G)=4\).

The supplied eternal family is nonempty and consists of four-sets.  Every
state is checked to dominate.  For each state \(D\) and each attacked vertex
\(r\notin D\), the verifier requires a guard \(u\in D\) such that
\(ur\in E(G)\) and
\[
  (D-\{u\})\cup\{r\}
\]
is another supplied state.  Thus exactly one guard moves, it moves along one
edge, and attacks are tested only at unoccupied vertices.  The family proves
\(\gamma^\infty(G)\le4\), while
\(\gamma(G)\le\gamma^\infty(G)\) gives equality.

For completeness, the standard parameter chain is immediate here:
every maximal independent set dominates, giving
\(\gamma(G)\le i(G)\le\alpha(G)\), while the usual independent-set attack
argument gives \(\alpha(G)\le\gamma^\infty(G)\).  (Attack successively at
unoccupied vertices of a maximum independent set; guards already on that
set cannot answer another such attack, so each attack increases the number
of guards on it.)  The two endpoint equalities therefore force
\[
  i(G)=\alpha(G)=4.
\]
The checker also verifies these two values directly, but those redundant
checks are classified as consistency checks.

Because the anchor is independent in \(G\), it is a \(K_4\) in
\(\overline G\).  Every proper four-coloring of \(\overline G\) assigns four
different colors to the anchor.  Renaming colors uniquely normalizes those
colors to \(0,1,2,3\).  The verifier examines all \(4^8\) assignments on the
other eight vertices and rejects unless every row has a monochromatic edge
of \(\overline G\).  Therefore \(\overline G\) is not four-colorable and
\[
  \theta(G)=\chi(\overline G)\ge5.
\]

The same chain shows that every maximal independent set has order four:
its order is at least \(\gamma(G)=4\) and at most \(\alpha(G)=4\).
Therefore \(G\) is well-covered.
\(\square\)

## Consistency certificates

A consistency-complete report additionally confirms connectedness, a
triangle, a 4-cycle, maximum degree at least four, and an explicitly verified
induced odd hole or odd antihole.

Nonplanarity is certified without a planarity-library dependency.  The file
supplies pairwise-disjoint connected branch sets forming a \(K_5\) or
\(K_{3,3}\) minor.  The verifier checks every required adjacency between
branch sets.  By Wagner's theorem this is a rigorous certificate that \(G\)
is nonplanar.  This auxiliary consistency check is not used in the decisive
parameter proof above.

The graph6 record is recomputed from the edge list and bound by SHA-256.
This is a labeled identity check.  Canonical labeling is a packaging concern
and is intentionally not in the logical acceptance path.

The checker deliberately separates the definition-level result from these
consistency conditions.  Its mathematical status depends only on graph
identity, \(\gamma(G)=4\), a literal one-guard eternal four-family, and the
complete four-color exclusion.  If that core passes but an auxiliary
restriction fails, the checker reports
`VERIFIED_COUNTEREXAMPLE_WITH_CONSISTENCY_ALERTS`.  Such a graph remains a
definition-level counterexample and must be frozen while the contradictory
restriction or checker is audited.
