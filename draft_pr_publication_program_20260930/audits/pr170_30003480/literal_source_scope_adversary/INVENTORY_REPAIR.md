# Inventory repair and public reproduction controls

Repair UTC: 2026-10-12T11:58:33.314724+00:00

The scientific source/math verdict and all first assessment/identity/seal files are unchanged. This is an inventory and artifact-handling repair requested by ROOT. Audit completion estimate remains100%.

The former FILE_MANIFEST.json, created at 2026-10-12T11:55:07.783503+00:00, had SHA256 7e95b1081364d7c8c3c83c84252646a8130be42800f0edf6664898332c2e22d3 and excluded itself plus FINAL_INVENTORY.sha256. Its exact bytes are preserved at HISTORICAL_FILE_MANIFEST_20261012T115507Z.json (mode0444).

The existing FINAL_INVENTORY.sha256 is retained byte-for-byte as a historical receipt of that former manifest. Its85 bytes contain the former manifest digest and the historical logical label FILE_MANIFEST.json. Its own SHA256 is 9de51cb1e2950ca834d7cda5664cb22202a781bae77aa8081a9aa180319cb34e and its mode is0444. The old digest authenticates the preserved HISTORICAL_FILE_MANIFEST_20261012T115507Z.json contents. It does **not** authenticate the newly replaced FILE_MANIFEST.json. No sidecar has been generated for the new manifest; the new digest is returned directly to ROOT outside the inventory.

The new complete FILE_MANIFEST.json includes the historical receipt, historical manifest snapshot, this note, updated RESULT.json and RESEARCH_LOG.md, public exact checker/results, every other retained file, and all four consumed external documentary inputs. It excludes only itself, avoiding self-reference.

EXACT_CHECKS.py and EXACT_CHECKS_RESULT.json are public own-output copies of this reviewer's independently written standard-library checker and retained successful result. The public checker was rerun successfully; its stdout exactly equals the public result file. Both public copies have exactly the same bytes as their retained private-scratch originals. Checker SHA256: 55bb58ed44a81888236fa2d0ebfd509c5d80f34e3c9456604bd46b04dcf55aa0. Result SHA256: bcd3eb37d3d78827bdceb3f58967b67aac5ce3d3d04fbcbcceb1c26063914582.

Reproduction command from this directory: python3 EXACT_CHECKS.py. Only fractions, itertools, math and json from the Python standard library are needed. The exact arithmetic and finite boundary controls corroborate the written derivation; they do not replace the universal polynomial-multiplicity proof.

The expanded explicit public own-output whitelist in RESULT.json authorizes these two mathematical controls plus this explanatory note and the historical inventory snapshot. Source bodies, full extractions, metadata and renders remain private. No source/private-render bodies were promoted. No mathematical or historical-priority reassessment occurred.
