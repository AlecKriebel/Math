# Research log: hostile multi-hit collision audit

## 2026-07-28 PDT

- Frozen and hashed the candidate note and manifest before review.
- Reconstructed the used portions of accepted C-143, C-145, C-146,
  C-108, and C-064.
- Audited the six neighborhood rows, mover sets, response-list
  exclusions, and synchronous deletion-rank conventions.
- Verified the all-rank XQ0 exact drop and \(q\leftrightarrow u\), the
  all-rank XQ1 \(p\leftrightarrow r\), and every singleton reversal.
- Reconstructed the rank-one XQ0 contradiction without using the
  candidate control program.  No active-witness, occupancy, or
  one-guard-model gap was found.
- Audited every possible named collision of the private witnesses and
  reconstructed the QQ0/AQ0 ridge and XQ1 ladder.
- Found a missing explicit multi-hit hypothesis in Theorem 2.1.  The
  proof and table are sound after adding it.
- Found that equation (4.2) literally includes \(x,r\).  The
  completion-clique theorem is sound after excluding those endpoints.
- Found one short omitted self-collision line in Lemma 3.1:
  \(y_g\ne g\) follows from \(gr\in E(G)\) and
  \(y_gr\notin E(G)\).
- Wrote an independent integer-mask graph6/kernel evaluator.  It
  reproduced both fixed controls and all stated local ranks and
  activities.
- Verdict on frozen bytes: `REVISE_LOCAL_ERRATA`, not `PASS`.
- Audited revised note
  `dd90daba2f44d5dbd85b956e9c6323a44f78a2cb429bc00eb619b9fc97acb786`.
  The three requested repairs were present, but the introductory sentence
  immediately before Theorem 2.1 still stated the six-case reduction
  without the new hypothesis.  Requested one additional scope edit.
- Audited final revised note
  `acfbc262877c08f9e4b38aa38931c3b95699b50073aa9a67d8ac3f80ba9ba3fd`
  and manifest
  `a7d29adbdcd44d8a2d157a731e84fc09f7d4d2c2175be3a02eb42179cc884636`.
  The lead-in is now explicitly subject to (2.0), all three errata are
  complete, both control replays remain unchanged, and the final verdict
  is `PASS`.
