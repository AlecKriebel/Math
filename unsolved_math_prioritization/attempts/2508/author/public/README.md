# Robust polynomial interpolation prior solution audit

Problem 2508 / EP-1133, rank 1037. The April 29, 2026 prior argument checks out relative to the declared Bernstein-density theorem and standard analytic imports. New approaches: zero. Read REPORT.md for the complete authored verification and its limits.

This directory is source-free. External source identities are recorded in SOURCES.json, without source text or dataset contents. Nothing in the Python checks replaces the analytic proof or establishes community acceptance.

Obtain the expected MANIFEST.json and verify.py SHA256 digests from an independent trusted receipt. Do not trust a digest freshly computed from an unknown or modified bundle. Using Python 3 with only the standard library:

    python -B verify.py --root . --manifest-sha256 TRUSTED_MANIFEST_SHA256

For whole-source replay, additionally supply --problems, --research, --candidate-pdf, --density-pdf, and --original-pdf with independently obtained local files matching the public metadata. Either supply all five or none. The output explicitly states whether source replay was performed.

    python -B controls.py --root . --manifest-sha256 TRUSTED_MANIFEST_SHA256 --verifier-sha256 TRUSTED_VERIFIER_SHA256

Controls execute normal, -O and -OO modes, reject malformed and adversarial bundles using the pinned trusted verifier, and replay a relocated genuinely nonroot read-only copy. The read-only test intentionally fails under root or when write probes are not denied. Temporary copies are outside the bundle. Neither program changes the verified directory.

The finite parameter and angular examples are authored test fixtures. They are not empirical evidence sufficient to settle the general statement. The mathematical conclusion depends on the proof in REPORT.md and its declared imports.
