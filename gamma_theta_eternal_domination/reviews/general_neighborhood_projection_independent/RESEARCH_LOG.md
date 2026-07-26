# Research log: independent-antineighborhood projection audit

## 2026-07-26 06:20--07:10 PDT

- Froze
  `math/lemmas/independent_antineighborhood_projection.md` at SHA-256
  `543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620`.
- Reproved the arbitrary-vertex statement directly, then the stronger
  independent-set form.  No game-quantifier or static-parameter gap was
  found.
- Observed that the \(A\)-form follows by iterating the arbitrary-vertex
  theorem.  Its direct restricted-slice proof remains cleaner and explicitly
  projects every eternal family.
- Proved that, in the complement of a minimum counterexample, all
  higher-clique common-neighborhood conclusions follow from the vertex
  condition plus the fact that every maximal clique has size \(k\).
- Compared the \(k=3\) specialization with the accepted odd-wheel theorem.
  The vertex condition is exactly local bipartiteness, while the remaining
  common-neighborhood facts are automatic.  It supplies no new \(k=3\)
  pruning.
- Implemented a clean-room probe with no campaign evaluator imports.
  Exhausted all 13,598 nonempty unlabeled graphs through order eight, all 694
  graphs satisfying \(\gamma=\gamma^\infty\), and all 14,421 eligible
  independent sets.  Checked 32,059 projected states and 56,166 attack
  obligations.  All checks passed.
- Found decisive accessible prior-art overlap in Taletskii,
  arXiv:2412.20120v2, Lemma 13: the minimum-planar-counterexample parameter
  and \(\theta\) conclusion is already stated there for every independent
  set.  Reclassified the reviewed theorem as an unrestricted and
  family-level generalization, not a wholly new antineighborhood idea.
- Confirmed the classical static overlap in Randerath--Vestergaard,
  DOI `10.1016/j.dam.2005.05.041`, Observation 2.
- Narrow searches found no exact unrestricted arbitrary-family statement in
  accessible one-guard sources.  Novelty remains unresolved because the 2018
  Klostermeyer--Krop--MacGillivray manuscript could not be inspected.
- Removed the generated Python bytecode cache.  All retained artifacts are
  source, result, review, and log files in this review directory.
