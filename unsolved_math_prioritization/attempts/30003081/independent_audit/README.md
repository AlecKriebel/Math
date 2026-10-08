# Independent audit packet

Read REPORT.md and ACCEPTANCE.json first. This packet audits the exact author manifest pinned in ACCEPTANCE.json. The five scoped mathematical results are accepted; the original broad target remains unresolved by the work. No mathematical patch is required. HARDENING.patch is an optional one-line diagnostic improvement and has not been applied to the author originals.

All files here are authored audit material, public source metadata or verification results. Source PDFs, excerpts, screenshots, corpus records and private coordination material are absent.

## Replay

Authenticate this audit's MANIFEST.json and executable members using its separately supplied freeze receipt before executing them. A self-authenticating manifest is not an external trust anchor. The audit's scripts require only Python 3's standard library.

Verify the authenticated audit manifest and replay its independent mathematics:

    python3 -I -B verify_audit.py --manifest-sha256 EXTERNAL_AUDIT_MANIFEST_SHA256
    python3 -O -I -B verify_audit.py --manifest-sha256 EXTERNAL_AUDIT_MANIFEST_SHA256
    python3 -OO -I -B verify_audit.py --manifest-sha256 EXTERNAL_AUDIT_MANIFEST_SHA256

Run the independent mathematics directly:

    python3 -I -B independent_math.py
    python3 -O -I -B independent_math.py
    python3 -OO -I -B independent_math.py

The output should match INDEPENDENT_MATH_RESULTS.json. Run expanded integrity and mathematical controls against the unchanged author packet:

    python3 -I -B independent_controls.py --author-root /path/to/authenticated/author/public

That script internally exercises normal, -O and -OO modes. It requires the original manifest and verifier hashes and never changes the author packet. Results are recorded in EXPANDED_CONTROLS.json. AUTHOR_CONTROLS_RERUN.json records a separate rerun of the author's own controls.

Source bytes are deliberately optional and absent. Without supplied inputs this reports NOT_RUN:

    python3 -I -B verify_sources.py

To verify separately obtained bytes whose expected names, sizes and hashes are in SOURCE_METADATA.json:

    python3 -I -B verify_sources.py --pdf-dir /path/to/pdfs --corpus-dir /path/to/corpora

A requested missing, changed or nonregular file is rejected. SOURCE_CHECKS.json records the actual original-input checks. SOURCE_AND_HARDENING_CONTROLS.json records three-mode source omission/corruption controls and the separately patched-verifier smoke tests. The optional source and hardening controls can be repeated with source_controls.py, supplying --author-root, --pdf-dir and --corpus-dir. These source checks authenticate exact bytes and parse the corpora, while source-content inspection and the written mathematical audit remain distinct.

These finite controls do not formally prove the universal geometric claims, guarantee complete literature coverage, or provide a general security certification. See REPORT.md for the exact accepted scope and remaining limitations.
