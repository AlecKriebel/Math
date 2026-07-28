# Research log: remaining rank-one collision endgame

## 2026-07-28 PDT — discovery and strict proof freeze

- Reconstructed the accepted C-143, C-145, C-146, and C-150
  dependencies and the exact six-row collision table.
- Kept `probe_cases.py` unchanged.  Its UNSAT outputs remain
  discovery-only and are not used as mathematical evidence.
- Independently checked a short contradiction for the two
  \(ur=0\), \(pr=qr=1\) rows QQ0 and AQ0.
- Proved a private-witness transfer lemma.  If \(y_g\) is the private
  witness for a rank-one successor, completing \(\{u,y_g\}\), applying
  C-108, and—unless the completion is already the opposite endpoint—
  making one unique attack forces \(T-g+y_g\) into the greatest family.
- From \(M_q=\{x,p,y_q\}\), attacked \(y_p\).  The \(y_q\)-successor
  misses \(q\).  The \(p\)- and possible \(x\)-successors each fail at
  the unoccupied attack \(u\), because every possible response lands in
  \(\{u,y_p,y_q\}\), which misses \(r\).
- Audited all seven named vertices for collisions and every attacked
  target for occupancy.  The proof does not assume
  \(y_py_q\in E(G)\) and never treats a missing family transition as a
  graph nonedge.
- Wrote an independent ordinary-set checker enumerating all assignments
  to the five optional named graph pairs in both rows.
- The strict replay checked 64 optional-pair assignments, 128
  adjacency-eligible first successors, all four completion branches, and
  matched `expected_result.json` byte for byte.
- Exact scope: rank-one QQ0 and AQ0 only.  XQ0 was already eliminated by
  C-150; XQ1 is handled by a separate candidate.  QQ1, AQ1, every
  higher-rank collision, reciprocity, complete \(k=3\), and the
  gamma--theta conjecture remain open.
