# Frozen local package: row 1874, ID 30006595

Status: **partial/scoped all-orders result**, not a general resolution. Local only; no repository publication or QUEUE modification is part of this package.

The five approaches and complete proof are in `authored/FIXED_MODULAR_ALPHABET.md`. Its exact gauge equation is δ²U = −t²fU. The kernel f is a noncuspidal holomorphic weight-4 form on Γ0(4), with trivial character and cusp orders (1,1,0). The fixed alphabet {1,f}, cusp-normalized convergent words and analytic majorant establish the stated all-orders coefficient identity. They do not establish scalar modularity, reduction to single ordinary primitives, reconstruction of the full R(k,1) generator, or higher-depth resolution. No novelty is claimed.

## Evidence and reproducibility

- `SOURCE_STATUS_GATE.md`: bounded primary-source/status and formulation audit, preserving the scope distinction.
- `public_sources.json`, `dataset_verification.json`: only public source metadata, hashes, byte counts and match results. No copied external documents, dataset contents, private sources or coordination files are included.
- `authored/ADVERSARIAL_AUDIT.md`: mathematical audit.
- `authored/check_fixed_alphabet.py`: exact rational direct hypergeometric versus fixed-alphabet comparison through q^13 and t^12; independent eta/Eisenstein check.
- `verification/original_check_fixed_alphabet.py.txt` and `assert_provenance.json`: complete original authored checker plus whole-module AST assert census and replacement provenance. All original asserts were mechanically converted to explicit RuntimeErrors; no mathematical AST changed. The archived `.txt` is evidence, not an executable checker.
- `verification/test_package.py`: verifies provenance; runs baseline normal and optimized checks; exercises six mathematical mutations in both modes. Sign, normalization, integration exponent, modular substitution, original hypergeometric parameter sign and Eisenstein coefficient changes must all fail at actual exact checks.
- `outputs/test_normal.json`, `outputs/test_optimized.json`: full stdout, stderr and exit statuses for all mathematical runs, plus inventory negative controls. Finite checks corroborate normalization, not the all-orders proof.

Run `python -B verification/test_package.py` and `python -B -O verification/test_package.py`. The outer optimized run separately proves that the test harness itself does not rely on asserts.

## Frozen inventory

The external sibling `frozen_modularity_1874_20261021_RECEIPT.json` records every file and directory, including byte counts and SHA-256 hashes. It is intentionally outside the frozen tree. Verify using:

`python -B verification/inventory.py . ../frozen_modularity_1874_20261021_RECEIPT.json`

The inventory performs a complete recursive lstat-style type census before reading any content. It rejects symlinks, FIFOs, sockets and devices. Descriptor-relative no-follow opens and identity checks defend against entry replacement; a final census rejects tree changes. Extra files and empty directories are covered. Tests create only temporary ordinary files, directories, a symlink and FIFO; socket/device modes are synthetic classifier tests, with no socket or device creation. Nested symlink/FIFO tests forbid all content reads and verify rejection first. Concurrent hostile changes after verification remain outside a static receipt's assurance; consumers should replay immediately before use.

No copied third-party sources are present. Public mathematical source citations appear in the theorem and gate. Preserve all scope caveats in any later authorized use.
