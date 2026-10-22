# Affine–Virasoro blowup normalization audit

Problem 30005075, OWR-9790367-005. Queue rank 483.

## Finding

The exact source question is a **surface-defect** blowup identity. A 2025 paper of Bershtein–Feigin–Trufanov supplies the relevant generic-parameter coset coefficient theorem. Its published Appendix B contains a directly checkable mismatch between the displayed normalization characters and their stated splitting identity. A local repair and an all-integer finite-product calculation recover the intended coefficient-free conformal-block sewing relation.

This packet is **partial progress / full target not certified**, pending independent review. It does not conclude that the underlying 2025 theorem is false or that the original mathematical problem remains open in the literature. It does not claim a novel solution. The remaining exact-target check is the convention-specific AGT/surface-defect identification, including abelian factors and mass shifts, for the gauge functions in the original equation.

## Contents

- `NORMALIZATION.md`: all-integer algebraic proof, explicit correction proposals, exact scope boundary
- `ATTEMPTS.md`: five substantive approaches and their outcomes
- `SOURCES.md`: primary-source provenance and precise pointers
- `checks/verify.py`, `checks/normalization.py`: standalone exact rational/symbolic verification
- `checks/results.json`: captured successful run

Run from this directory:

```sh
python checks/verify.py
```

Requires Python 3 and SymPy (tested with Python 3.12.14 and SymPy 1.14.0). No network, corpus files, or scholarly PDFs are needed to run the verifier. Its finite checks corroborate the derivation; the proof of arbitrary integer shifts is in the note. PDF sources are intentionally excluded from this public packet.

## Review priorities

1. Verify the ordered three-point arguments and the sign/norm correspondence in Eq. (16).
2. Check that the two sewn prefactors reproduce the exact Eq. (4.59) coefficient for every integer flux.
3. Decide whether the paper's AGT identifications, combined with the repaired full normalizers, justify classifying the intended source question as previously solved, or whether the explicit gauge-convention bridge must still be completed.
4. Do not treat the printed auxiliary residual as a disproof of the underlying blowup formula.
5. Keep generic meromorphic/formal scope distinct from singular levels or analytic convergence claims.

Prepared 2026-10-03. All results are local; no repository or website status was changed by this investigation.
