# Wild-knot quadrisecants: independent audit delivery

Read `AUDIT.md` for the mathematical review and `ACCEPTANCE.json` for its exact scope. The decision is `unsolved`, `5/5`; it is not a theorem-proof or formal-certification claim.

Publishable replacement:

- `corrected/packet/`: corrected authored report, ledger, status, source metadata and checkers
- `corrected/freeze/`: regenerated manifest and externally verifiable pins
- `corrected/audit_tools/`: distributed author replay harness
- `corrected/source_free_packet.tar.gz`: corrected frozen archive
- `CORRECTED_REPLAY.json`, `EXACT_CONTROLS.json`, `SOURCE_RECHECK.json`: independent receipts
- `ORIGINAL_REPLAY.json`: historical original-archive verification metadata only
- `PATCH_NOTES.md`, `CORRECTION_PINS.json`, `LEDGER_TYPE_HARDENING.patch`: implemented corrections and their hashes

No original source-bearing archive, PDF, screenshot, source extract, corpus record, or private inspection file is included. The literal quotation-removal diff is excluded, with its digest recorded in `CORRECTION_PINS.json`.

## Reproduce the corrected archive audit

Requires Python 3.9+ standard library and a genuine non-root account. First authenticate the delivery's hashes against a separately trusted receipt; an archive cannot authenticate its own trust anchors.

Run from this directory:

    python3 -I -B independent_archive_replay.py --archive corrected/source_free_packet.tar.gz --archive-sha256 29f3c6c8c4c0fad6298263a16ab66d95cf1460854346441a6c53a8173c29a865 --manifest-sha256 9097b3da520bdee1facde8b7fdb92b7b23e974fb7cbb726c2903ccbc1965cd56 --bootstrap-sha256 4bcfe34c55a37eb7c1323a63de12e86f7060110efaf10b8237b08c974e96fcfa --verifier-sha256 4f55b4aee1cae738e45891f9ad53fe3e1c901aeef3b4b87af6669beffe3cd331 --ledger-hardened

This extracts a fresh read-only copy, executes all three optimization modes, reproduces the distributed harness, runs independent malformed/positive controls and ledger regressions, verifies write denials, and checks that the frozen files did not change. It prints a source-free JSON receipt without temporary local paths.

Run the independent mathematical finite controls separately:

    python3 -I -B independent_exact_controls.py
    python3 -I -B -O independent_exact_controls.py
    python3 -I -B -OO independent_exact_controls.py

All continuous/topological arguments require the human-readable mathematical review. Finite diagnostics and immutable-file checks do not prove the wild-knot assertion.

`PUBLIC_MANIFEST.json` inventories all public files other than itself and `DELIVERY.json`. `DELIVERY.json` pins that manifest. The outer delivery receipt pins the final source-free audit archive, avoiding any circular self-hash requirement.
