# Trace and geometry independent audit

Read `AUDIT.md` for verdict and proof boundaries. `literal_source_record.json` and `independence_seal.json` pin the source-first and before-history phases. `read_ledger.json` states the exact full/partial read extent. `close_pin.json` records the frozen original head and retained hold.

The two scripts in `originals/` are unchanged frozen originals, with byte-identical 30/72 stdout in `streams/`. `mutants/` contains five actual code corruptions; their full expected failure streams are preserved. `geometry_controls.py` gives 25 supplemental exact controls. `replay_and_corruption_receipts.json` records actual interfaces and hashes. These controls do not solve the full mathematical target.

`authored_manifest.json` excludes only itself and `tmp/`, and covers all other files recursively. Run `/usr/bin/python3 verify_manifest.py` from this folder to verify exact path coverage, hashes and sizes. The actual manifest corruption controls and full streams are recorded in `manifest_control_receipts.json`. `build_manifest.py` regenerates the manifest only when intentionally revising this audit.

Foreign PDFs, extracted raw text, rendered source pages and disposable manifest test copies stay in ignored `tmp/`; they are not published. Root owns final acceptance and remote head checks. No new substantive attempt turn, solved claim, canonical edit or remote mutation occurred here.
