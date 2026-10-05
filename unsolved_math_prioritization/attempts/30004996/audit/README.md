# Portable independent audit

Problem 30004996 / OWR-9790354-007. Verdict: pass as **unsolved**, subject to two minor source-map corrections. No full-target solution is certified.

Read `AUDIT.md` for the mathematical review and limitations. `SOURCE_CHECKS.json` records fresh source inspection and provenance boundaries. `CORRECTIONS.json`, `source_map.patch`, and `source_map.corrected.md` form a precise correction overlay; no frozen input was changed.

From this directory run:

```
python3 verify_audit_manifest.py
python3 run_audit.py
```

The second command expects `../packet/` and `../FREEZE_MANIFEST.json`. For another layout, supply `--packet-dir PATH --freeze PATH`. Both commands work offline with the Python standard library and do not write input files. The first checks audit payload integrity; the second verifies all eight frozen inputs, replays the original 19,861 assertions, replays 135,653 independently authored controls, and verifies the correction overlay. `REPLAY_RESULTS.json` is the recorded output of the second command.

The root external freeze manifest is SHA-256 `b8a4f8d40b4428baec9bdad1d74c3ab8b33c98bf73013cc5dcb4e60d749d9b4d`. The manifest checksum in `AUDIT_MANIFEST.sha256` must itself be anchored by a separately transmitted digest to detect coordinated replacement. Self-contained checksums are integrity checks, not signatures or independent timestamps.

The portable package includes only the frozen authored packet, its external freeze/checksum files, and this authored audit. It deliberately omits source PDFs, extracted source text, source screenshots, dataset records, and private coordination files. Source inspection is a recorded human-readable audit finding, not replayed by the offline finite programs. Full datasets and repository state were not independently fetched in this audit.
