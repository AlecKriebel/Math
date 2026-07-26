# Hole9 orphan-recovery hostile-audit log

## 2026-07-25 18:52 PDT — audit opened (10%)

- Scope fixed to the sealed recovery package, the frozen `hole9` run tree,
  exact 170-cut chronology, deterministic deletion stripping, and a fresh
  deletion-free RUP replay.
- Reviewed artifacts will not be edited.  New work is isolated in this
  directory.
- Initial package hashes agree with the author handoff.

## 2026-07-25 18:59 PDT — provenance defect found (35%)

- The frozen ART-115 incident JSON records the `cuts.json` SHA-256 with 63
  hexadecimal characters, omitting the final `b`.
- The live cut payload, packaged copy, checkpoint, orphan generator, and new
  certificate all agree on the correct digest
  `a3c7bd3591b71c310cfe0bd5711b8e672b75136f3598bb1505ae11cda3c2193b`.
- This makes the published statement that ART-115 binds every decisive
  orphan hash literally false.  Root and the recovery author were notified.
  The package remains pending; no frozen evidence or claim registry was
  changed.

## 2026-07-25 19:06 PDT — two non-destructive corrections received (45%)

- The recovery author issued an explicit ART-115 erratum at
  `results/logs/synthesis-k3-hole9-batch-004-checker-incident-erratum.json`;
  SHA-256
  `6bfb1cc799977d96fe5058b13c1dd08e8c0cbb8b86c3a58a30c3c9a6233ee135`.
- A second erratum corrects the soundness note's imprecise statement that the
  runner generated the CNF twice.  It generated one CNF and ran two CaDiCaL
  passes against the same path.  Erratum SHA-256:
  `f6135a4121cafaca5275d1f1f707e7c82626d61caec94d908704aaec92400e90`.
- Both errata preserve the frozen incident and sealed package bytes.  Their
  complete cross-bindings are now part of the standalone probe.

## 2026-07-25 19:10 PDT — standalone replay complete (90%)

- Isolated standard-library probe reconstructed the exact 6,886-variable,
  20,200-clause CNF.
- All 170 history links, 170 cuts, and 2,210 present-artifact bindings passed.
- Strict parsing removed exactly 11,683 deletion lines and reproduced the
  exact 65,906-byte addition-only proof.
- Fresh watched-literal propagation validated all 4,705 additions, including
  the final empty clause.  RUP replay took 2.879 seconds; full audit took
  4.412 seconds with 74,285,056-byte maximum RSS.
- Eleven hostile mutations were rejected.

## 2026-07-25 19:14 PDT — verdict issued (100%)

- Verdict: **ACCEPT WITH TWO VALIDATED ERRATA** for the exact narrow
  hole9-CNF UNSAT claim.
- No unresolved mathematical, reconstruction, proof, or package defect
  remains.
- Integration must publication-bind the two errata, outer certificate,
  hostile review, and probe while leaving frozen source evidence and sealed
  package bytes unchanged.
