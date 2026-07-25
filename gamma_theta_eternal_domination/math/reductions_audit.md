# Hostile self-audit of the core reductions

## Review status

This is the author's hostile pass, not the required independent review.  An
independent reviewer should recheck `reductions.md` before its claims are
promoted in `CLAIMS.md`.

## Dependency ledger

| Result | Nondefinitional dependency | Current proof status |
|---|---|---|
| Parameter chain | None | Complete |
| Equality collapse and well-coveredness | Parameter chain | Complete |
| Component additivity | None | Complete |
| Connected reduction | Component additivity and the parameter chain | Complete |
| Imperfection obstruction | Equality collapse and Strong Perfect Graph Theorem | Complete relative to SPGT |
| Induced-subgraph monotonicity of \(\gamma^\infty\) | None | Complete |
| \(\gamma^\infty(\overline{C_{2q+1}})=3\) | Parameter chain only for the upper bound | Complete |
| \(\alpha=\gamma^\infty=2\Rightarrow\theta=2\) | SPGT and the two preceding lemmas | Complete relative to SPGT |
| Minimum counterexample parameter \(k\geq3\) | Equality collapse and the \(\alpha=2\) theorem | Complete relative to SPGT |
| Published graph-class restrictions | Primary literature not yet fully audited | Deliberately pending |

## Failure-mode checks

### \(\alpha\leq\gamma^\infty\)

- Attacks are only on currently unoccupied vertices.
- Once a guard enters the attacked independent set, it cannot be the guard
  moved to a later attacked vertex of that same independent set.
- Exactly one guard moves, so the number of guards in the independent set
  rises by one per attack.
- If the independent set is larger than the guard set, the next unoccupied
  independent vertex has no adjacent guard.  The proof does not merely stop
  after placing all guards.

### Component additivity

- A global eternal family can contain multiple invariant component-count
  sectors; the proof does not assume a single global count vector.
- It selects one nonempty count-vector slice, which is closed because an edge
  never crosses components.
- Projection from that slice dominates each component because there are no
  cross-component edges.
- Both directions are proved; the product-family construction establishes only
  the upper bound.

### Induced-subgraph monotonicity

- Naively projecting a global configuration can fail to dominate the induced
  subgraph.
- The proof instead chooses configurations maximizing the number of guards in
  the induced vertex set.
- Any response from outside that set would increase the maximum; therefore a
  response from inside exists for every local attack.
- That same response proves local domination as well as transition closure.

### Odd-antihole attack sequence

- In \(\overline{C_n}\), a two-set is nondominating exactly when its vertices
  have cyclic distance \(2\) in \(C_n\).
- The initial pair \(\{0,1\}\) is forced into every two-guard family by the
  independent-set lemma.
- At each intermediate attack \(d+2\), moving the guard at \(0\) gives a
  nondominating distance-\(2\) pair, so closure forces the other move.
- At the final attack \(n-2\), both possible resulting pairs have cyclic
  distance \(2\).
- The \(n=5\) endpoint is covered separately by the same final step; there is
  no empty induction hidden in the proof.

### Complement and coloring conventions

- \(\alpha(G)=\omega(\overline G)\).
- \(\theta(G)=\chi(\overline G)\), with \(\theta\) a partition into cliques.
- Complementing an induced odd hole gives an induced odd antihole on the same
  vertex set, and conversely.
- No all-guards-move parameter occurs in a proof.

## Counterexamples guarding against overstatement

- \(K_{3,3}\): well-covered but \(\gamma<\alpha\).
- \(C_5\): well-covered with \(\gamma=\alpha\), but
  \(\gamma^\infty=3>\gamma=2\).
- \(K_2\mathbin{\dot\cup}K_2\) with three guards: an eternal family can be a
  union of closed sectors with distinct component count vectors.
- \(C_5\): having an induced odd hole/antihole is not sufficient for the
  conjecture's target equalities.

## Open audit items

1. Obtain an independent line-by-line review of Lemmas 1, 8, and 9 and
   Proposition 5.
2. Add exact primary citations for SPGT and for historical attribution of the
   \(\alpha=2\) theorem.  The proof itself does not depend on the latter.
3. Resolve every row in `class_restrictions_pending.md` before enabling those
   restrictions in a certified generator or coverage proof.
