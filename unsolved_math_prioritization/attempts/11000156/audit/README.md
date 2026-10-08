# Independent audit deliverables

Read AUDIT.md for the mathematical verdict and source limitations.

- citation_correction.patch is the actual source-attribution correction.
- corrected_source_free_packet.tar.gz is the final corrected publication unit.
- CORRECTED_DELIVERY.json pins that archive, its manifest, and its bootstrap.
- CORRECTED_ARCHIVE_REPLAY.json records a fresh non-root read-only replay of that final archive under ordinary Python, -O, and -OO.
- AUDIT_RECEIPT.json records independent finite mathematics and 186 malformed-input rejections across the original and corrected freezes.
- SOURCE_INSPECTION.json contains public source metadata only.

The corrected archive includes six packet files, the external manifest/bootstrap/pins, and its acceptance receipt. Original inputs were preserved. Neither the audit nor the checks resolve the literal commutation-only problem.

Run `python3 -B independent_checks.py` and repeat with `-O` and `-OO` for the additional finite tests. `test_distribution.py` expects the original source-free distribution in a sibling `boundary_twist_11000156` directory and the corrected distribution here. It creates temporary mutation copies and never edits the original packet. `archive_corrected.py` deterministically builds and freshly replays the corrected archive.
