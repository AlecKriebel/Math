# Research log: hostile side-purity and cap-cycle audit

## 2026-07-27 22:36 PDT

- Froze and hashed all four target artifacts in
  `math/working/k3_side_purity_cap_cycle/`.
- Read the current accepted C-079 proof, the frozen-color projection proof,
  and the accepted parameter-two reduction on which projection
  bipartiteness rests.
- Reconstructed the side-purity proof quantifier by quantifier.  Checked
  explicitly that when \(q\in W_a\), the edge \(qx\) puts \(q\) in \(K\)
  and forces both endpoint neighbors onto the same bipartition side.
  Therefore the mixed-side case forces \(q\notin K\), and all vertices in
  the C-079 invocation are distinct.
- Checked the open-neighborhood contrapositive when \(q\in P_a\):
  simplicity gives \(q\notin N_H(q)\), so removing \(\{q\}\) from \(P_a\)
  does not change its intersection with \(N_H(q)\).
- Audited the singleton-buffer scope.  The singleton conclusion applies
  only to outside \(H\)-neighbors omitting \(v\).  A nonanchor internal
  connector in the \(v\)-projection has precisely this property; an
  arbitrary cross-projection continuation does not inherit the conclusion.
- Audited cap continuation.  The two endpoints of an
  \(H[W_a]\)-edge are opposite-side witnesses, and the further singleton
  statement remains restricted to outside neighbors in \(W_v\).
- Ran the working verifier with `--check`; its output was byte-identical to
  the frozen `result.json`, with SHA-256
  `f9dd30333986b0c984910fe3e13464c28bd64a98d85932c8e2df14f805fb1998`.
- Wrote `independent_checker.py` without importing `verify.py` or any
  campaign graph/search helper.  It uses a separate integer-bit-mask
  representation, decodes `GCXfVG`, exhaustively computes graph
  parameters and greatest eternal kernels, reconstructs lists and
  colorings, checks the complement \(C_4\) and repeated caps, and enumerates
  all physical C-079 embeddings.
- The independent checker reproduced its frozen JSON byte-for-byte and
  returned `PASS`.  Artifact hashes at this checkpoint:
  - `independent_checker.py`:
    `af67c3e27e60767701139a039974793087c41748b806e28130aecd827a270946`;
  - `independent_result.json`:
    `9f3285541225a7bd495811853cfbd5a65dce6171fd46cbac6b7fa1f6c5ff90cb`.
- Final verdict: **PASS**.  No mathematical or scope defect was found.
