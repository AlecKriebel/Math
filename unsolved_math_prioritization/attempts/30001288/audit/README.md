# Independent audit deliverable

Problem 30001288 / OWR-3481-005 / rank 973.

**Verdict: accept the source-free investigation with the verifier correction; retain unsolved, 5/5.** No general connected rational comparison is proved. The literal full-sheaf formula has a separate projective-line defect.

## Files

- `AUDIT_REPORT.md`: complete mathematical, source-hypothesis, and implementation audit.
- `ACCEPTANCE.json`: exact scoped verdict and original/corrected snapshot pins.
- `GAPS.md`: unresolved mathematics and prohibited shortcuts.
- `SOURCE_AUDIT_METADATA.json`: public source citations, inspected locations, authenticated PDF hashes and sizes, and audit limits.
- `CORRECTION.patch`: minimal explicit-exception verifier correction and corresponding candidate manifest update.
- `corrected_checks.py`, `CORRECTED_AUTHOR_MANIFEST.json`: exact corrected files for comparison or reconstruction. In a copied author packet their names must be `checks.py` and `AUTHOR_MANIFEST.json`.
- `audit_checks.py`: independent exact controls and executable corruption tests.
- `AUDIT_CHECK_RESULTS_NORMAL.json`, `AUDIT_CHECK_RESULTS_OPTIMIZED.json`: results for both wrapper modes. Each wrapper explicitly tests both child interpreter modes.
- `AUDIT_MANIFEST.json`: hashes of this audit deliverable, excluding itself.

Preserve the original author packet. Apply the patch to a separate copy, then run:

```text
python3 audit_checks.py --packet ORIGINAL --corrected-packet CORRECTED
python3 -O audit_checks.py --packet ORIGINAL --corrected-packet CORRECTED
```

Each run records 57,135 audit checks and 56 verifier/invalid-input regression cases. The corrected script preserves all 73,323 deterministic author controls. The tests prove the original optimized hash-verification bypass and verify its correction. They separately show why manifest authentication and inventory validation require more than the minimal patch.

The deliverable contains authored analysis, code, and public verification metadata only. It contains no copied scholarly PDFs or source text, dataset contents, or private coordination material. No publication was performed.
