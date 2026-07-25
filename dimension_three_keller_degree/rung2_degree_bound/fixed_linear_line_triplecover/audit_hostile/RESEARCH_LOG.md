# Hostile audit log: transverse fixed-linear line triple cover

**2026-07-25T05:52Z — Audit opened**

- Confirmed the worktree is on `main`.
- Baseline SHA-256 hashes:
  - theorem:
    `99ec31535d5b2c0602ca2b42273b39210b2b32eec8e6ed937dc58e09bcbe142d`;
  - SymPy:
    `54fb2d4ff4f4c521edeb2a1f30fa2b3a8e55b738d7ab3768c3a706e3881ab930`;
  - PARI/GP:
    `395899524357e670adf3e40161877a03accfb46cf974a2655dea499b25331958`;
  - strict wrapper:
    `08c918007529f776a3e8e4b7a0c11c828dcabb6d29feb9437436539dfd841eda`.
- Both supplied verifier commands pass.
- Initial hand reconstruction confirms the cross-product sign and the
  exponent \(p^6\).

**Checkpoint estimate:** 30% complete.

**2026-07-25T06:00Z — Audit complete**

- Proved that the general pair of coprime binary cubics is the exhaustive
  left-right form; no false normalization to a power map is used.
- Independently confirmed
  \(D=p^6sw(-1,-t,3s)\) and
  \(D(G)=p^{d+5}sw(4sg_s-dg)\).
- Verified that cancellation uses only the domain property and
  \(w\ne0\), not invertibility of \(w\).
- Reconstructed both determinant polarizations with independent matrix
  entries and checked the arbitrary-form eigenvalue kernels.
- Audited the plane-field descent and the exact transverse-only scope.
- Optimized Python fails closed.  Fault injection confirmed that the
  supplied GP wrapper rejects diagnostics, extra output, and nonzero exits.
- Final verdict: **PASS**, with exposition clarifications in `REPORT.md`.

**Checkpoint estimate:** 100% complete.
