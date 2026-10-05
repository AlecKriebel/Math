# Independent audit: roots-of-unity lower bounds

Verdict: **PASS for scoped results and an unresolved disposition. Full target unsolved, 5/5 approaches used.**

- `AUDIT.md`: mathematical proof audit, target binding, source quantifiers and limitations
- `BINDING.json`: exact author ZIP and member hashes
- `independent_exact_controls.py` and `INDEPENDENT_RESULTS.json`: independent exact finite checks, standard library only
- `NEGATIVE_CONTROLS.json`: semantic and quantifier controls with interpretation limits
- `AUTHOR_REPLAY.json`: byte-identical author replays and nine corruption controls
- `SOURCE_SCOPE.json`: independently inspected source locations and eight fresh public PDF hash matches
- `REPRODUCIBILITY.json`: normal, optimized and relocated independent-run equality
- `STATUS.json`: explicitly unresolved research status
- `verify_audit.py`, `test_audit_integrity.py`, `AUDIT_INTEGRITY_RESULTS.json` and `MANIFEST.json`: externally anchored file verification and corruption controls

The author freeze is a separate input, not modified or duplicated in this package. Its expected name is `ROOTS_UNITY_30002178_AUTHOR_FREEZE.zip`, with SHA-256 `24f88fd09d1f753306be377bcb96e17a0dd85d2ccb674975873a6046ddcbe02d`.

Run, replacing paths as needed:

    python independent_exact_controls.py /path/to/ROOTS_UNITY_30002178_AUTHOR_FREEZE.zip --output /tmp/independent.json
    python -O independent_exact_controls.py /path/to/ROOTS_UNITY_30002178_AUTHOR_FREEZE.zip --output /tmp/independent-optimized.json
    cmp INDEPENDENT_RESULTS.json /tmp/independent.json
    cmp INDEPENDENT_RESULTS.json /tmp/independent-optimized.json
    python verify_audit.py . /path/to/ROOTS_UNITY_30002178_AUTHOR_FREEZE.zip AUDIT_MANIFEST_SHA256
    python test_audit_integrity.py

Use the externally delivered SHA-256 of `MANIFEST.json` for `AUDIT_MANIFEST_SHA256`; computing a hash from an untrusted replacement alone is not an identity check. The independent exact checker uses Python's standard library. The optional author replay needs SymPy, as documented in the author package. All mathematical checks remain active under Python -O.

The release excludes scholarly PDFs, extracts, page images, raw datasets and prior AI reports. Finite checks do not establish the infinite conjecture. No novelty, complete prior resolution or global-openness claim is made.
