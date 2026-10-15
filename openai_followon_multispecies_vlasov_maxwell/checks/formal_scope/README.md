# Pinned formal-scope audit

See `../../agent_notes/formal_scope/REPORT.md` for the actual scope and limitations. No proof certificate was reproduced.

- `lean/OAI/Analysis/VlasovMaxwell/`: exact commit-pinned source subtree, 207 files.
- `source_inventory.json`: hashes and sizes of copied files.
- `static_scan.json`: complete local import closure and preliminary admission/axiom screen.
- `build_receipt.json`: exact compiler/package versions, attempted checks, failures, and owned cleanup.
- `lean/lakefile.upstream.lean`, `lean/lake-manifest.upstream.json`: unchanged original full configurations.
- `lean/lakefile.lean`, `lean/lake-manifest.json`: minimal Mathlib-only audit configuration and resolved dependency pins.
- `lean/Audit.lean`: declaration/axiom inspection request; not run successfully.
- `reproduce.sh`: intended build and axiom inspection when adequate disk is available.

Generated `.lake` dependencies and compressed caches were deleted after the receipt was recorded because shared disk was low. Do not infer a successful build from the existence of source files, a manifest, or cache-download logs.
