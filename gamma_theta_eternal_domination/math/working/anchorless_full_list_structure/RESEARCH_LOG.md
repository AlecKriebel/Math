# Research log: anchorless full-list structure

- **2026-07-28 PDT.** Read accepted C-073, C-089, C-127, C-132, the
  full-list multi-step hostile audit, and the open greatest-family
  reciprocity checkpoint.  Kept arbitrary-family and greatest-family
  statements separate.
- **2026-07-28 PDT.** Exhaustive connected-unlabeled discovery scan
  through order 9 found no equality-three greatest-family full root with
  an anchorless physical-inactive vertex.  Counts at orders
  \(6,7,8,9\) were respectively \(2,16,140,1380\) equality-three graphs
  among \(112,853,11117,261080\) connected graphs.
- **2026-07-28 PDT.** Stopped an initial unsplit order-10 exploratory run
  after approximately nine minutes because its static filter was
  inefficient and the run was not partition-checkpointed.  No result was
  retained from that interrupted run.
- **2026-07-28 PDT.** Replaced the static filter by the exact complement
  test: for a generated \(K_4\)-free \(H\), \(\gamma(\overline H)=
  \alpha(\overline H)=3\) exactly when \(H\) contains a triangle and
  every vertex pair has a common \(H\)-neighbor.  Split the order-10
  scan into 16 nauty residue classes.  All 2,894,632 unlabeled
  \(K_4\)-free complements were processed; 18,777 passed the static and
  eternal-three filters and zero had an anchorless greatest-family full
  root.  This remains `OBSERVED`, not a promoted certified finite result.
- **2026-07-28 PDT.** Derived componentwise palette rigidity by combining
  C-073 response-role covariance with C-132's domination/palette
  equivalence.  The key exact identity is that the opposite-side guard's
  response role on an edge \(bc\) is present precisely when the retained
  palette at \(b\) contains the attacked anchor.
- **2026-07-28 PDT.** Derived the zero/one/two-spoke component
  classification and the forced reverse role when both side palettes
  omit the same anchor.
- **2026-07-28 PDT.** Corrected an invalid early witness idea: a common
  complement neighbor of an anchorless \(b\) and an anchor \(s_i\) does
  not make \(\{b,s_i,y\}\) independent, because \(bs_i\in E(G)\).
  The valid mechanism is instead a unique third attack from the retained
  palette state \(\{x,s_i,b\}\), which forces
  \(x\to y\) and installs \(\{b,s_i,y\}\) in the family.
- **2026-07-28 PDT.** The installed-state domination condition proves
  that each external common-neighbor layer \(Y_i(b)\) is a \(G\)-clique.
  C-089 gives the conditional count \(|V(G)|\ge |B_*|+10\).
- **2026-07-28 PDT.** Replayed the equality two-spoke control
  `Ksv`f\knJVis`, the one-spoke anchorless gamma-two control `EEz_`, and
  the anchorless-only gamma-two control `EFz_`.  Candidate package is
  frozen for hostile review; no claim has been promoted.
- **2026-07-28 PDT.** A bounded local repair probe added one missing
  root--spoke graph edge to the 12-vertex equality control and toggled up
  to two further arbitrary edges.  None of the 8,584 labelled edits
  retained \(\gamma=\alpha=\gamma^\infty=3\), the full root, and a
  nonempty anchorless set.  This is only a failed-search observation.
