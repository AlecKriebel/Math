# K3 Problem 3.45: support genus

Status: **unresolved after five mathematical approaches**.

Read `REPORT.md` for the complete authored analysis, proofs, imports, and exact gaps. `TURN_LEDGER.md` distinguishes the five approaches from zero-count source/audit work. `SOURCE_METADATA.json` contains bibliographic, version, inspection, and file-hash metadata only. No source PDF, copied source text, corpus record, or dataset is included in this packet.

The most concrete partial calculation is for the boundary-twist open books (S_{g,1},t_boundary^n): H_1 is Z^(2g), connected-binding support genus is g, and support norm is 2g-1. These facts leave unrestricted support genus unresolved because the binding component count is unbounded in its definition.

A current-literature correction is important: Orbegozo Rodriguez and Stenhede's July 2026 preprint proves that contact connected sum has support genus at most the larger summand's. Thus connected sums of genus-one examples do not answer the problem.

## Reproduction

Requires Python 3.10 or newer; standard library only; no network or external data.

- `python check_math.py` prints the exact regression-check results.
- `python verify_packet.py` verifies the frozen file list, byte counts, hashes, and reproducibility of the saved results.

The checks exercise word abelianizations, surface arithmetic, the conformal Reeb equation, characteristic numbers, finite U-modules, and capping-vector constraints. They are regression tests for the displayed algebra, not proof of contact realization, imported theorems, or exclusion of all genus-one books. `REPORT.md` contains the proofs and limitations.

Publication classification: source-free authored partial report and verification metadata. No novelty or problem-solved claim.
