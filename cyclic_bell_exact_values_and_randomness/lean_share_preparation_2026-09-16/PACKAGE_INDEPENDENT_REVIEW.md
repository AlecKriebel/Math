# Independent reviewer-package review

Date: 2026-09-16. Bounded review complete: 100%. Reviewed `scripts/package.py`, `scripts/check.py`, `scripts/test_package.py`, the static-audit interfaces, package configuration, and reviewer-document links while the clean Lean run was in progress. No protected file was edited and no Lean/Lake command was run. Python checks used disabled bytecode writes; synthetic adverse cases ran in temporary directories.

## Result

No blocking omission, stale-source acceptance, or portability defect was found for the current export. Export remains contingent on installing the completed clean receipt and its exact numbered logs in `verification/recorded/`, then successfully running the exporter. This review is not that pending compiler receipt or a verification of an archive not yet produced.

The runner and packager compute the same protected fingerprints: 152 files in the reviewed tree. Every protected file is in the export allowlist. All 106 production/root Lean files (including the generated axiom audit), all 25 validation controls, the required scripts, configurations, reference inventories, and bundled TeX/PDF are included. The manuscript source and PDF match their pinned SHA-256 values. The TeX does not reference an omitted local `input`, `include`, graphics, or bibliography file. The export deliberately excludes dependencies, caches, transient runs, and private repair records; reproduction uses the locked dependency bootstrap.

Checked 146 local links in README, REVIEWER_GUIDE, COVERAGE, AXIOMS, and the verification/review documents. Every target is inside the package and present or allowlisted, except the expected pending `verification/recorded/run.json` and `verification/recorded/` targets. These must exist before delivery. No current allowlisted text matched the private `/Users/` or `/home/` path scan.

## Receipt and export checks

The exporter requires a passed, kernel-checked receipt with current protected hashes, pinned compiler identity, the exact declaration set, matching per-source inventory hashes, approved reported axioms, and fresh clean-build axiom provenance. It reconstructs the complete command sequence including dependency bootstrap/cache commands when present, acceptance and rejection controls, optional repeated axiom audit, and both dependency-integrity passes. It verifies each numbered log's digest and exit status, compiler/revision outputs, empty dependency status logs, actual build axiom reports, and source-located negative proof diagnostics. Missing, stale, malformed, or incomplete evidence fails closed in the examined paths.

The cache bootstrap command contract matches the final runner: `lake build Cache.Main`, followed by the interpreted `lake env lean --run .lake/packages/mathlib/Cache/Main.lean get`. This review inspected that contract; it did not run those commands or independently test platform cache execution.

Archive inputs reject symlinks and unsafe paths. The protected-file subset check prevents a nested new Lean file from being silently omitted by the flat source glob. The exporter checks protected hashes again after collection. Archive entry order, timestamps, permissions, encoding, and storage mode are fixed; the internal file manifest and external archive checksum cover the exported bytes. The existing deterministic-archive test passed.

## Executed checks

All 24 `test_package.py` tests passed. Six additional independent temporary-fixture mutations were rejected as intended:

| Mutation | Rejection |
| --- | --- |
| Alter bundled PDF and refresh source fingerprints | Pinned manuscript digest mismatch |
| Add a nested Lean source absent from the flat allowlist | Protected input outside allowlist |
| Insert a dirty dependency status with a matching log hash | Recorded dependency modifications |
| Move a negative proof diagnostic to another source file | Different-source diagnostic |
| Add a private root Markdown document and refresh fingerprints | Protected input outside allowlist |
| Replace a numbered command log with a symlink | Symlinked archive input |

## Boundaries and final handoff

Checksums and internally consistent logs do not authenticate a maliciously fabricated receipt. The verification documentation correctly states that checksums do not authenticate an author, and reviewers can rerun Lean. Upstream dependency artifacts and the pinned compiler remain in the documented trust base. The private-path filter is a targeted text check, not a general personal-information detector; its PDF exclusion is paired with an exact canonical PDF hash pin. Verification narratives and source-preservation records are included as review evidence rather than compiler-generated proof of correspondence.

After the clean run finishes, copy its receipt and numbered logs unchanged, run the real exporter, inspect/extract the resulting archive, and recheck the recorded links and manifest. Those release steps belong to the integration owner. No source or packaging repair is requested by this bounded review.
