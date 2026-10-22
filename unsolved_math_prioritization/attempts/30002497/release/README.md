# Corrected partial-results release: irrational autocorrelation maxima

Problem 30002497 / OWR-12866-004. **Unsolved after five approaches.**

The independent audit accepted the partial mathematics and required one
correction to numerical endpoint export. The analytic proof is unchanged:
any irrational local maximum must be a stationary Wilton point, and an
explicit quadratic family and its reciprocals are excluded. Neither result
settles existence of an irrational strict local maximum. No novelty claim
is made.

## Which files to use

- `current/`: corrected working packet, including outward-rounded decimal
  endpoints and its verifier. Use these numerical files as the current
  certificate outputs.
- `original-author/`: all nine frozen original author files, preserved
  byte-for-byte. Their saved interval strings are historical nearest-rounded
  displays, not directed decimal endpoint certificates. In-memory sign
  assertions were unaffected by the export defect.
- `audit/`: the complete independent audit, preserved byte-for-byte, including
  its standard-library integer-interval engine and original-input binding.
- `CORRECTION_LEDGER.json` and `CORRECTION.diff`: exact changes and provenance.
- `RELEASE_CHECKS.py` and `verification_results.json`: preservation, replays,
  exact serializer tests, nesting/sign comparisons, and independent backend
  rerun.
- `MANIFEST.json` and `SHA256SUMS`: binding of the safe release contents.

Sign assertions are performed on in-memory interval values. In the corrected
packet, exported decimal endpoints are separately rounded outward by exact
rational arithmetic: lower endpoints use floor and upper endpoints use
ceiling. The export implementation is pinned to mpmath 1.3.0.

The correction changes neither the integration engine nor any derivative
sign, analytic theorem, target status, or five-approach budget. The missing
argument remains strict two-sided increment control at stationary Wilton
points.

## Reproduce the entire verification

With Python 3 and mpmath 1.3.0, from this directory:

    python RELEASE_CHECKS.py --output rerun_verification.json

This reruns both original parameter sets, requiring byte-for-byte equality
with their historical outputs; reruns both corrected parameter sets; checks
that corrected high-precision intervals nest inside the lower-precision ones;
and reruns the independent integer backend. Temporary replay files are
removed automatically. Use a new output filename to preserve the supplied
verification record.

To run the standalone independent backend, Python's standard library alone
suffices:

    python audit/independent_controls.py --cutoff 256 --output rerun_independent.json

To run the preserved audit against its original input binding:

    python audit/verify_audit.py --author original-author --rerun --output rerun_audit.json

No network calls or remote writes are performed. This release does not contain
source PDFs, full texts, raw catalogues, or private coordination inventories.
