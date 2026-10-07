# Independent audit packet

Problem 10000051 / AMR-099-0051. Verdict: accept corrected partial work; not solved.

- `AUDIT.md`: complete independent mathematical, source-scope and integrity audit.
- `CORRECTION.patch`: three focused repairs, applied relative to the original public-packet root.
- `CANDIDATE_CORRECTED.md`: full authored candidate after the two mathematical-text repairs.
- `AUDIT_SOURCE_METADATA.json`: public source provenance and inspection scope.
- `checks/independent_audit.py`: exact read-only verification, with validations active under Python optimization.
- `checks/independent_results.json`: verified results from the frozen original packet.
- `checks/patch_and_integrity_results.json`: patch application, fail-closed guards and corruption controls.
- `AUDIT_MANIFEST.json`: hashes and sizes for this packet; excludes itself.

Run the independent check with Python 3, giving the original frozen public directory as its sole argument. Running with `-O` is supported. Applying the correction patch changes original hashes, so the independent frozen-input check should continue to target the preserved original, not a patched replacement. Any adopted corrected packet requires its own fresh manifest.

The original source packet was not modified. No publication or remote write was performed. Source PDFs and extracted third-party source text are excluded.
