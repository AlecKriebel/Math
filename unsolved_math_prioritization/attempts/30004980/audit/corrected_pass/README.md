# Corrected maximum twin width audit packet

FULL PASS for corrected release v1 as a scoped partial research record. The exact maximum problem remains unsolved after five attempts. The historical original freeze retains its HOLD; H1 is repaired only in the separate corrected release.

Read PUBLIC_AUDIT_REPORT.md for the complete mathematical, source, implementation, and correction review. MANIFEST.json records hashes of all supplied audit files. Source PDFs and private records are excluded.

Using Python 3.10+ with its standard library, run:

```text
python verify_readme.py /path/to/corrected_release_v1
python independent_verify.py /path/to/corrected_release_v1 --full
python independent_conference.py
```

The first command runs all four author commands in a temporary copy and compares output bytes. The second independently computes and compares every exact value through six vertices, verifies all certificates and the source manifest, and confirms source preservation. Its original-definition K2 witness is retained as a regression demonstration of the repaired historical defect. The third checks conference controls including Paley(9). No network or remote writes are needed. Run without Python optimization flags. Result JSON files are written beside the audit scripts.
