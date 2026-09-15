# Cyclic Bell Lean companion

This is the locally repaired Lean companion to the merged paper. The downloaded handoff was entirely uncompiled. Repairs retain the original mathematical statements and add missing source-strategy, polar, spectral and closure constructions. Read `COVERAGE.md` for exact claim correspondence and proof boundaries. The reproducible frozen clean-build outcome is `logs/latest_run.json`; independent reviews and retained evidence are in `repair_audit_2026-09-14/`.

The canonical manuscript is `../main.tex`, SHA-256 `82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`. The original download remains untouched. The received handoff, `history/`, and retained uncompiled-status comments in original source headers describe the incoming snapshots, not current compiler results. Current status comes from the actual receipt and the local evaluation.

## Reproduction

With Lean 4.19.0 available, from this directory:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Omit `--bootstrap` if all exact pinned dependencies and their cache are already installed. This checks dependency identities, builds the complete imported library, runs positive and negative contracts, obtains actual axiom reports, and verifies protected source fingerprints. Regenerate the declaration inventory with `python3 scripts/source_inventory.py --write` after legitimate source changes, then freeze those inputs throughout the final run.

A successful compiler build verifies the encoded statements. The accompanying semantic audits separately check their match to physical states, PVMs, arbitrary Eve POVMs, correlation models, and the manuscript. Failed candidate proofs in negative contracts are interface/regression checks; their failure alone is not a proof of the negation of every displayed target.

The settings entropy concerns observed tables; adversarial entropy is treated separately. Guessing lower bounds do not assert an exact globally optimized adversary. All literal mathematical coverage gaps must be disclosed even if every imported source file compiles.
