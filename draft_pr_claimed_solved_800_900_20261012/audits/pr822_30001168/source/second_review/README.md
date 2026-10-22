# Second review bundle

Read SECOND_REVIEW.md for the analytic acceptance and the independent
four-region all-time round bound. The two earlier frozen bundles are
identified in INPUTS.json and were not modified or repackaged here.

Run `python -I -B verify_review.py` and `python -I -B -O verify_review.py`.
The verifier checks the strict regular-file inventory, hashes, exact output,
and two mathematical negative controls. Checks remain active under -O.

The manifest authenticates bytes relative to the external receipt. Neither
hashes nor the arithmetic certificate replace the analytic proof.
