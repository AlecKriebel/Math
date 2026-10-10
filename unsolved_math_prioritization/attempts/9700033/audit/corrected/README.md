# Problem 9700033: unbounded components of a SIRSN

Read RESULT.md for the complete authored partial theorem, proof, countermodel scope, source dependencies, three approaches, and remaining uniqueness gap. The target remains unsolved.

Run `python -B verify.py` from any directory. `python -O -B verify.py` is also supported; validation uses explicit checks, not assertions. The program verifies package integrity and finite diagnostics, not the continuum proof.

SOURCE_MANIFEST.json contains public bibliographic and byte-verification metadata only. CERTIFICATE.json binds every other safe file. An external manifest independently binds the certificate, all files, and the final ZIP. Neither the certificate nor the verifier is a trust anchor against deliberate simultaneous rewriting; compare the external manifest from the author handoff.

The directory is deliberately strict: unlisted files, nested manifests, symlinks, changed bytes, and missing files are errors. Use `-B` to avoid generating a cache directory.

This is the separately identified corrected derivative. Section 2 now constructs a measurable witness count H_r; it asserts a covering family of at most H_r distinct unbounded components with E[H_r]<=8p(1), without asserting measurability of their exact number. The original author files are preserved separately. The independent audit is AI review, not human peer review, formal verification, or a novelty certificate.
