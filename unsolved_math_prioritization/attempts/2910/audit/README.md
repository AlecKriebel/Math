# Independent acceptance packet: Problem 2910

Read `AUDIT.md` for the mathematical and source review and `ACCEPTANCE.json` for exact accepted bytes. The result remains an unresolved, scoped partial audit, three of five approaches. No full solution, refutation, or novelty is claimed.

`AUTHOR_SAFE_FREEZE.zip` and its manifest preserve the ten-file original exactly. `CLARIFIED_SAFE.zip` and its manifest contain the accepted ten-file derivative. `CLARIFICATION.patch` records the three changed files. No third-party source document or corpus content is included.

With Python 3 and its standard library, run:

    python3 replay.py AUDIT_DIRECTORY AUDIT_EXTERNAL_MANIFEST AUDIT_ZIP
    python3 -O replay.py AUDIT_DIRECTORY AUDIT_EXTERNAL_MANIFEST AUDIT_ZIP

The external manifest and ZIP belong outside the extracted audit directory. Verify their receipt digests before trusting the replay. The checker runs from any working directory and does not fetch sources.

`verify_sources.py` separately verifies the complete original corpus files and four exact PDFs when those authorized inputs are available. Its positional inputs are the catalog, problems file, reports file, and PDF directory. It emits hashes and match metadata only. Missing private inputs are not silently counted as reverified; source receipt checks within `replay.py` are distinguished from fresh source-byte verification.

The computational tests do not decide smooth standardness or surface isotopy. No publication was performed as part of this review.
