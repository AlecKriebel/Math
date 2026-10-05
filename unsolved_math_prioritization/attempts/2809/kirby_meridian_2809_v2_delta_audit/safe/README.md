# C1 v2 delta acceptance

The exact pinned v2 package passes C1 correction review. The original meridian conjecture remains unresolved, 5/5. This packet supplements, and does not replace or modify, the original full audit.

- `DELTA_REVIEW.md`: in-context acceptance and limits
- `ACCEPTANCE.json`: machine-readable exact-version acceptance
- `DELTA_RESULTS.json`: executed replay and mutation results
- `verify_delta.py`: reproducible input-pin, delta, patch, replay, and mutation checks
- `verify_package.py` and `MANIFEST.json`: mandatory recursive integrity check

Run `python3 verify_package.py` or `python3 -O verify_package.py` to validate this packet. Run `python3 verify_delta.py INPUT_DIRECTORY` (also under `-O`) to reproduce the delta results. The input directory needs the six named pinned files listed in the script, the original author safe directory, the v2 safe directory, and the original audit safe directory in their documented relative layout. Python standard library and the system `patch` command are required. All mutation execution uses temporary copies.

No source PDFs, extracts, images, raw datasets, or private coordination files are included. Acceptance is AI-assisted mathematical/artifact review, not human peer review or editorial approval.
