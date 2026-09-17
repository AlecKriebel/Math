# Reviewer package tooling checkpoint

Timestamp: 2026-09-17T03:39:56.149188+00:00

Implementation and synthetic verification completion: 100%. Actual release archive creation remains pending the parent's fresh clean-build receipt.

Owned additions only:

- `scripts/package.py` — SHA-256 `447e206f8a715ebdbeb6b4cb448569059b268326da3f5700e8a6616b0039b365`
- `scripts/test_package.py` — SHA-256 `fb6865c010dca29f0968dbb6a259905de7024ecc5a95840319e724a8d99089ca`

The CLI accepts only `--output`; there is no unverified packaging option and it invokes no Lean command. Payload selection uses the explicit reviewer-file allowlist, flat production/validation Lean sources, and exactly the numbered command logs referenced by `verification/recorded/run.json`. The current runner defines no separate success-summary files. Root/source/script/reference protected files outside the share allowlist cause refusal; transient verification runs and unrelated research folders are never selected.

A package requires a passed kernel-checked receipt, matching current protected fingerprints, the pinned compiler/manuscript, 1,852 unique inventoried declaration names, source-inventory file digests, and axiom reports matching both the receipt and actual fresh build log. Only the standard three axioms are allowed. Every command is checked against the full ordered runner contract, including bootstrap when present, compiler checks, dependency checks before/after, the build, all registered controls, optional repeated axiom audit, and final expanded statements. Log digests and exact expected exit codes must match. Negative control errors must occur inside the control proof, not an import or statement; their rejection remains a smoke test rather than an independent proof of falsity.

The packaged TeX and PDF have independently fixed hashes. All selected text must decode as UTF-8 and is scanned for private machine home-path prefixes. Required files and protected tree symlinks are rejected. Archive output stays outside the companion. Each entry has a fixed timestamp, Unix regular-file mode, stable sorted name, and stored compression mode. `SHA256SUMS` covers every payload byte except itself; a sidecar records the complete ZIP digest.

Validation: `python3 -B scripts/test_package.py` passed all 24 tests in under one second. Tests cover deterministic bytes and manifest completeness; missing required files/logs/axiom source; altered log contents; stale fingerprints and source inventory; source/directory/output symlinks; private text; unexpected protected files; missing commands, log traversal, wrong return codes and false success flags; missing/nonstandard axiom reports; manuscript corruption; resource failure; unrelated negative-control errors; and the quiet-bootstrap command contract. See `package_tests.log`.

A read-only check against the actual current source confirmed that the packager's root-parameterized fingerprint enumeration equals `check.protected_fingerprints()`. The two new scripts pass their own private-path scan. These tests use small synthetic temporary fixtures and do not execute Lean, copy dependency trees, or claim a successful production archive before the final receipt exists.

2026-09-17T03:41:27.896599+00:00 — Bootstrap portability repair synchronized: the ordered receipt contract now requires `lake build Cache.Main` and then `lake env lean --run .lake/packages/mathlib/Cache/Main.lean get`. This avoids relying on the platform-linked cache executable while preserving pinned source/toolchain checks. All 24 packaging tests pass again; script hashes above updated. Tooling completion remains 100%, production archive still awaits the fresh passing receipt.
