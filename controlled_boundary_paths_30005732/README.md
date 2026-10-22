# Controlled boundary paths: partial results and scope audit

Problem ID 30005732 (OWR-14298011-003), ordered row 1845.
Disposition: **UNSOLVED**, five research approaches completed, frozen 2026-10-21.

This authored package contains complete conditional normal-flow constructions, a weak finite-perimeter area comparison with explicit hypotheses, optimal critical-budget disk examples, and admissible nonuniqueness/topology tests. It does not solve the general existence of optimal AC boundary trajectories or of regular optimal selections.

The strongest optimal example has continuous normal speed at every time and a joint C1 normal parametrization, but no joint C1,1 normal parametrization. The kink example only applies in the a.e.-time weak class and has no joint C1 parametrization. Both retain unique AC normal paths and a stationary smooth optimizer for the same data. Local graph nonuniqueness and annulus topology examples are only admissible, not established optimal. Extinction paths are AC up to their limit, without a nondegenerate endpoint parametrization.

## Contents and verification

- RESEARCH.md: complete authored proofs and five approaches.
- AUDIT_CONTROLLED_BOUNDARY_PATHS.md: independent mathematical audit, including BV balance and comparison proof.
- SOURCE_GATE.md: primary-source identification and carefully bounded literature status.
- SOURCE_METADATA.json and DATASET_METADATA.json: public URLs, retrieval/inspection history, hashes, byte counts and match counts, not copied documents or dataset contents.
- CLAIM_LEDGER.json: accepted claims and excluded interpretations.
- SANITIZATION.md: transformation provenance and exclusions.
- PACKAGE_AUDIT.md: independent review of the sanitized package.
- verify_integrity.py and MANIFEST.json: exact inventory, byte-count and SHA-256 checks.

Run from this directory:

    python3 verify_integrity.py
    python3 -O verify_integrity.py

These commands verify artifact integrity only. They are not numerical experiments, theorem provers, source re-retrievals, or independent mathematical certification. No computational proof claim is made. The manifest does not hash itself and is not a cryptographic signature; its externally recorded digest pins the frozen inventory.
