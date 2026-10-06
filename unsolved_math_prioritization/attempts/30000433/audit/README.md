# Independent audit and correction supplement

Problem 30000433 / OWR-1194-002, rank 812.

Verdict: accepted as partial/unsolved with the narrow A1 quotient-certificate supplement. Four substantive approaches remain used. Read AUDIT_REPORT.md and CORRECTION.md.

The original author ZIP is preserved and is a separate input. Python 3 standard library suffices:

    python3 audit_replay.py /path/to/EDGE_DEGREE_30000433_AUTHOR_SAFE_FREEZE.zip
    python3 -O audit_replay.py /path/to/EDGE_DEGREE_30000433_AUTHOR_SAFE_FREEZE.zip

To run only the independent checker against an extracted original author package:

    python3 independent_audit.py /path/to/extracted-author-package

The original ZIP SHA-256 is b64c3b92a96f180b51d22ddd343e9458fc7181f7d8117d5117a4b6a7215dcdf7. The harness validates this before extraction. It reconstructs the mathematics, verifies the supplementary quotient conditions, and tests the patch in temporary copies. It does not change the input archive.

MANIFEST.json records this audit package's member hashes. Keep its hash or the archive hash outside the package as the trust anchor. No manifest authenticates itself.

The package contains authored audit mathematics, code, results, correction patches, and public verification/source metadata only. It excludes corpus records, source PDFs and extracts, and private coordination material. No human peer review, formal proof-assistant certification, novel topological existence family, or universal resolution is claimed.
