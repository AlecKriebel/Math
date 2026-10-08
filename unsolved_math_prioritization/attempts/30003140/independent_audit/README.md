# Independent audit of problem 30003140

Read FULL_AUDIT.md for the complete mathematical review and ACCEPTANCE.md for the decision. ACCEPTANCE.json records the machine-readable result. No source documents or datasets are distributed here, and no original author files are modified.

## Replay

Use Python 3.10+ and an unchanged copy of the author's public packet. The audit's independent programs require only the standard library.

    python -B independent_exact.py /path/to/author/public
    python -B -O independent_exact.py /path/to/author/public
    python -B -OO independent_exact.py /path/to/author/public
    python -B test_independent_controls.py /path/to/author/public

The original manifest is pinned directly in independent_exact.py. The --certificate option tests a separate claim file while retaining the unchanged source packet as the identity anchor. It never alters or repins the author's frozen packet. Negative tests use temporary files.

The arithmetic checker does not prove the truth of imported theorems or of arbitrary prose. Mathematical review remains in FULL_AUDIT.md. Passing replay means bounded arithmetic acceptance, never global modularity.

MANIFEST.json lists this audit's public files and excludes itself. Its external SHA-256 and archive identity are recorded in the separate AUDIT_RECEIPT.json. Neither receipt nor archive is placed inside the manifested directory.
