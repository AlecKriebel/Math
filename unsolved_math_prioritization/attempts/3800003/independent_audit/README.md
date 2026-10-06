# Independent audit package

Problem 3800003 / AMR-037-0003, queue rank 927. Read `AUDIT_REPORT.md`, `MATH_SOURCE_REVIEW.md` and `EXACT_ACCEPTANCE.json`. The original safe author ZIP and its external manifest are included unchanged. Source PDFs, HTML and complete dataset files are not included.

Authenticate this audit archive and `AUDIT_MANIFEST.json` against the separately supplied external manifest before using the scripts. To check the extracted audit inventory:

    python -I -B verify_audit.py --root AUDIT_DIRECTORY --manifest-sha256 EXTERNAL_DIGEST
    python -I -B -O verify_audit.py --root AUDIT_DIRECTORY --manifest-sha256 EXTERNAL_DIGEST

To reproduce the full independent artifact audit, supply the exact complete corpus files and the four successfully retrieved source files listed in the metadata:

    python -I -B replay_audit.py --author-zip DEGENERATE_POLYTOPE_3800003_AUTHOR_SAFE_FREEZE.zip --author-external DEGENERATE_POLYTOPE_3800003_AUTHOR_EXTERNAL_MANIFEST.json --catalog CATALOG_PATH --problems PROBLEMS_PATH --reports REPORTS_PATH --sources SOURCE_DIRECTORY

Repeat with `-O`. The driver runs author scripts and controlled mutations in both modes internally; running the driver twice additionally checks that the audit logic does not rely on assertions. It makes no network requests and prints verification metadata only. The expected full JSON output is `AUDIT_REPLAY_RESULTS.json`.

The independently held hashes are the trust anchor. A manifest that an attacker may replace along with its members cannot authenticate its own replacement. These checks address a static artifact handoff, not concurrent hostile filesystem replacement. Mathematical/source review is separate from integrity verification.
