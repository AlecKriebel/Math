# Independent audit: problem 30005024

**PASS for scoped results; general problem UNSOLVED after 5/5 approaches.**

Read `AUDIT.md` for the independent mathematical audit and `CORRECTIONS.md` for the provenance addition and scope clarifications. The original author freeze is preserved unchanged under `author/`.

Run with Python 3.10 or newer and the standard library only:

    python verify_audit_manifest.py
    python author/verify_manifest.py
    python author/verify.py
    python verify_independent.py

The author diagnostics have 9,093 assertions. The independent program reconstructs all 9,093 cases and runs 3,787 additional exact checks. Tests are finite diagnostics, not formal verification or a solution certificate.

`SOURCE_AUDIT.json` records current source checks, fresh PDF hashes, full-corpus pins, the reconstructed review hash and bounded prior-attempt searches. `PROVENANCE_RESULTS.json` is the recorded external-input verification. To repeat those input checks, run `verify_provenance.py --help` and supply the separately held complete corpora, source PDFs, pinned repository queue script and author ZIP. Those inputs are deliberately not bundled. Offline arithmetic replay does not itself refetch sources or rerun repository searches.

No source PDFs, text extracts, screenshots, raw corpus records or private coordination files are included. No remote writes were performed by this audit.
