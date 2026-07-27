# Research log: hostile review of the \(k=3\) 2-SAT-bicycle lane

## 2026-07-26 19:19 PDT

- Froze the four target artifacts and read the note, evidence source,
  evidence JSON, and research log in full.
- Re-read the directly used frozen-projection, projection-gluing,
  ridge-covariance, mixed-\(P_4\), and mixed-witness prerequisites together
  with their accepted hostile reviews.  Checked the concurrent
  forced-\(C_5\) statement used only for narrative comparison.
- Re-derived the normalized minimal-unsatisfiable 2-CNF trichotomy.  The
  implication-closure extension step, clause-covering minimality, unit
  count, and trivial-path boundary all check.
- Audited the port-event signs and all internal/singleton connector
  parities algebraically and by an independent truth table.
- Reconstructed every attack-tree branch in Theorems 4.1 and 5.1 from the
  one-guard definition.  No occupied attack or unclassified responder was
  found.
- Exhausted 512 graph completions of the lollipop hypotheses, with no
  condition on \(L(q)\), and 256 completions of the two-variable bicycle
  hypotheses.  The reference state survived in none, even after relaxing
  positive list membership.
- Independently decoded `GFznc{`, verified its graph/complement edge sets,
  all 35 family states, all 175 unoccupied attacks, both response-list
  tables, five covariance identities, two independent triples, zero direct
  list colorings at each ridge end, and parameters \((2,3,3,3)\).
- Confirmed with pinned nauty that `GFznc{` is a valid labelled record but
  not canonical (`shortg` gives `G@~~fc`).  The source makes no canonicality
  claim and the graph is not a conjecture candidate.
- Reran the target generator.  After deleting elapsed time, its output is
  byte-identical to the frozen evidence payload.
- Independently reproduced all order-eight scan counts, including 11,117
  connected graphs, 18,985 exact two-list restrictions, 14,372 surviving
  restricted families, and zero uncolorable instances.
- Verdict: `PASS`.  No correction is required for mathematical acceptance;
  two nonblocking explanatory clarifications are recorded in `REVIEW.md`.

Frozen review artifacts:

| artifact | SHA-256 |
|---|---|
| `independent_audit.py` | `0806fc076c0e2485ebbece7dd8474b018a0234d4d8e103914bb05d2d24dd96ac` |
| `independent_result.json` | `6de1f254a1c306aef2713a51927baef0fb606feb73eb03af9c9a1b3bc5217640` |
| `generator_rerun.json` | `fe47bbca42458aa7fc578a2789c843650e7eb5180496d94ab9c12d94b65a3822` |
