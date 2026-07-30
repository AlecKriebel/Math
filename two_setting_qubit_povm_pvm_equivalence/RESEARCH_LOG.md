# Research log: Two-setting fixed-qubit POVM–PVM equivalence

## 2026-07-30T00:53:28Z (2026-07-29 17:53:28 PDT)

- Recorded the theorem that, for every bipartite Bell scenario with two
  measurement inputs per party and arbitrary finite output sets,
  \(\mathcal Q^{\mathrm{POVM}}_2(2,2)=
  \mathcal Q^{\mathrm{PVM}}_2(2,2)\), with arbitrary shared classical
  randomness included on both sides.
- Recorded the resulting setting-minimality classification: combined with the
  frozen exact \(3\times2\) separation, fixed-qubit POVM–PVM separation first
  occurs at \(3\times2\) inputs, up to exchanging the parties.
- Imported the supplied proof dossier, dependency graph, adversarial audit,
  failed-approach record, exact symbolic verifier, constructive rank-zero
  simulator, machine-readable formulas, reports, and hash manifests.
- Preserved every supplied artifact byte-for-byte. The source archive has
  SHA-256
  `1263676974401159079e0faf8926aaee5430a2edeb1f7bcc843e938b6294a23d`.
- Verified every supplied artifact against `SHA256SUMS.txt`.
- Ran `verify_exact.py` with Python 3 and SymPy 1.14.0: all exact algebraic
  closure checks passed.
- Ran `rank_zero_simulator.py` with exact rational arithmetic: the symmetric
  trine instance and its deterministic local decomposition passed.

The closure proof imports the frozen dependencies D1–D3 (the exact
\(3\times2\) separation, the one-binary-party theorem, and the arbitrary-output
residual reduction). Their hashes are preserved in
`INHERITED_CHECKPOINT_SHA256SUMS.txt`, but their proof files were not included
in the supplied archive. Thus this bundle independently documents the closure
of the final residual \((2,3)\)-by-\((2,3)\) architecture; the universal
classification uses those inherited results. The full closure argument is in
`FINAL_RESEARCH_DOSSIER.md`.
