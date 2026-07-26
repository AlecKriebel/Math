# Certified exclusion of the order-12 `hole9` template

## Status and exact scope

This note proves the graph-theoretic implication of the recovered
base-plus-170-cut UNSAT certificate.  It does not assert that the original
CEGAR run reached a terminal, and it does not address the `hole5` or `hole7`
templates.

Throughout, \(G\) is a finite simple graph on 12 vertices and
\(H=\overline G\).

## Theorem

There is no connected 12-vertex graph \(G\) such that
\[
  \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G)
\]
and \(H\) contains a hub-free induced \(C_9\).

Here “hub-free” means that no vertex outside the induced cycle is adjacent in
\(H\) to every cycle vertex.

## Proof

Suppose that such a graph \(G\) exists.  We show that it gives a satisfying
assignment of the exact CNF whose SHA-256 is
`2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d`.
The certified unsatisfiability of that CNF is then a contradiction.

Choose the assumed induced \(C_9\) in \(H\), orient it, and label its vertices
\(0,\ldots,8\) cyclically.  Because \(\gamma(G)=3\), no pair dominates
\(G\).  Equivalently, every pair of vertices in \(H\) has a common neighbor:
for a pair \(a,b\), a vertex outside the pair that is adjacent in \(G\) to
neither \(a\) nor \(b\) is adjacent in \(H\) to both.  Apply this to the rim
edge \(01\).  No rim vertex is a common neighbor of \(0\) and \(1\) in an
induced cycle of length at least five, so their common neighbor lies outside
the cycle.  Label one such vertex \(9\), and label the two remaining vertices
\(10,11\) arbitrarily.

Use the actual edges of \(H\) as the values of the CNF edge variables.
Since \(\alpha(G)=\omega(H)=3\), \(H\) has no \(K_4\).  The preceding
common-neighbor argument supplies every witness variable required by the
pair clauses: choose one true witness for each pair and set the unused
witness variables false.  The chosen labels satisfy the exact induced-\(C_9\) units,
the units \(09,19\in E(H)\), and every no-external-hub clause.  The
connected-cut clauses hold because \(G\) is connected.

Because \(\gamma^\infty(G)=3\), there is a nonempty eternal family of
dominating triples in the one-guard-moves model.  Set a family variable true
exactly for those triples and, for every selected triple and every
unoccupied attack, select one legal responding guard promised by the
strategy; set every unused move variable false.  Each selected successor is
again a dominating family member, so
all domination and move clauses hold.  The redundant clauses requiring every
triangle of \(H\) to be selected also hold: a triangle of \(H\) is an
independent triple of \(G\), and the maximum-independent-state theorem says
that every independent 3-set belongs to every eternal 3-family.
Consequently the complete base formula is satisfied.

It remains to check the 170 appended coloring cuts.  Each cut was constructed
from a fixed map \(c:V(H)\to\{0,1,2\}\) and is
\[
  \bigvee_{\substack{u<v\\c(u)=c(v)}} e_{uv}.
\]
But \(\theta(G)=\chi(H)>3\).  Thus \(c\) is not a proper coloring of \(H\),
so at least one same-color pair is an edge of \(H\); the corresponding
literal makes the cut true.  This argument applies independently to all 170
recorded cuts.  Hence the alleged graph and strategy satisfy the exact
base-plus-cut CNF.

The sealed recovery package reconstructs that CNF byte-for-byte as a formula
with 6,886 variables and 20,200 clauses.  Its addition-only proof has 4,705
steps, each independently verified as a reverse-unit-propagation consequence
of the preceding formula, and its final step is the empty clause.  Therefore
the CNF is unsatisfiable, contradicting the satisfying assignment above.
\(\square\)

## Corollary

By C-014, if \(\gamma^\infty(G)=3\), then \(\overline G\) has no induced odd
wheel.  Therefore every induced \(C_9\) in the complement of a putative
order-12 parameter-three counterexample would automatically be hub-free and
is excluded by the theorem.  Combining this with C-017, every survivor of
the order-12 parameter-three slice must contain a hub-free induced \(C_5\) or
\(C_7\).

## Certificate boundary

- Acceptance record:
  `results/synthesis_k3_hole9_orphan_recovery_acceptance.json`.
- Sealed package:
  `certificates/synthesis_k3_hole9_orphan_000170_recovery/`.
- Independent review and checker:
  `reviews/hole9_orphan_recovery_hostile/`.
- The original source checkpoint remains `running` with no terminal marker.
- The complete \((n,k)=(12,3)\) slice remains open until both remaining
  templates receive independently accepted negative certificates.
