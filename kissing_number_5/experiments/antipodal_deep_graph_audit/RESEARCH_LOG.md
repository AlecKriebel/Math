# Research log

## 2026-07-24 00:42 PDT

- Reconstructed every algebraic step in the odd triangle-free deficit
  proof.  The identities for \(m,D_A,D_B,D\), the use of a degree-\(a\)
  vertex, and the final incident-edge contradiction are all correct.
- Exhaustively inspected all 1,024 labeled graphs for \(a=2\) and all
  2,097,152 for \(a=3\).  The feasible maxima are 5 and 10, attaining
  \(a^2+1\).
- Reduced a possible \(a=4\) violation to the only handshake-compatible
  case: a 4-regular triangle-free graph on nine vertices.  After safely
  fixing one neighborhood, checked 983,040 finite incidence cases.  Of 216
  degree-feasible cases, none is triangle-free.
- Added a structurally different independent verifier: recursive
  triangle-free graph generation for \(a=2,3\), exact independent-set
  decisions, and a missing-neighbor count for \(a=4\).
- Found no mathematical objection.  Recorded only a minor exposition
  suggestion: exclude \(r=19,20\) before applying the \(a\geq2\) lemma.
