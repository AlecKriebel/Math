# Orientation-compatible integer multicover: frozen partial-results package

Row 1872; ID 3000062; AMR-029-0062. Disposition: **NOT SOLVED**. This is a local-only authored audit package, not a claim of a general binary-input polynomial solver or an exact hardness classification.

## Contents and scope

- `source_gate.md` and `source_metadata.json`: authored source/scope gate and public verification metadata. No source PDFs, extracted source text, HTML, corpus contents, or private coordination files are included.
- `algorithmic_audit.md`: all five approaches, including the exact epsilon < 1/n approximate-fixed-point-to-integer reduction. Computing the requisite approximate fixed point in polynomial binary-input time is still missing. The normalized tolerance depends on maximum weight M. Existence and the indegree-one algorithm are prior Király–Pap results, not new solutions. The submitted-manuscript minimum/maximum and factor-two issues remain attributed corrections, not changes to the original question.
- `independent_review.md`: the accepted independent mathematical review, preserved unchanged. This package adds reproducibility checks; those checks are not a new independent mathematical review.
- `originals/`: exact original authored check scripts. Their Python assertions disappear under optimization; use the root hardened scripts for replay.
- Root check scripts: original whole-module AST transformed only by replacing assertions with explicit failure guards; formatting is normalized by ast.unparse. `provenance/` contains complete original and hardened ASTs, hashes and assertion locations.
- `check_results.json` and `robust_check_results.json`: original results, unchanged. `REPLAY_RESULTS.json` records complete stdout, stderr, exit status and semantic JSON equality for both hardened scripts in normal and optimized Python.
- `negative_controls.py`: exact mathematical counterexample and mutation controls, whole-module hardening provenance, guard controls, and fail-closed filesystem tests. Both normal and optimized outputs are supplied.
- `verify_inventory.py`: recursively lstat every entry before reading the manifest; reject links, FIFOs, sockets and devices, including unsafe root and manifest. Exact path inventory and bytes/SHA-256 must match `MANIFEST.json`.

Run from any directory with Python 3 and the standard library:

    python -B verify_inventory.py
    python -B replay.py
    python -B negative_controls.py
    python -O -B negative_controls.py

The original exhaustive check covers 729 loopless three-vertex weighted digraphs and 2,241 half-grid fixed points, with 679 scalar identities. The seeded robust check covers 30,000 trials with 624 eligible approximate fixed points. Finite tests support implementation consistency, not general proof or polynomial complexity. The robust test helper scans integers only on coordinate intervals already restricted to length < 1/n; it is not advertised as a generic wide-interval routine.

## Freeze boundary

The manifest covers every regular file except itself; an external receipt anchors the manifest digest and package-tree digest. A manifest cannot authenticate itself. Freeze is a recorded byte-level snapshot, not a filesystem immutability or adversarial concurrent-write guarantee. Symlink/FIFO/device checks protect the static inventory being validated, not races from a concurrent malicious writer.

No GitHub, QUEUE, or source input was modified. No socket was created. Socket and device rejection controls use synthetic lstat modes only. The external receipt is deliberately outside this package.
