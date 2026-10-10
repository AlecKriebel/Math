# SIRSN exterior covering independent audit

Decision: accept the corrected scoped partial result; the uniqueness problem remains unsolved, with 3/5 approaches used. This is independent AI review, not human peer review, formal verification, or a novelty certificate.

Read AUDIT.md for the full audit and corrected/RESULT.md for the complete corrected mathematical result. The correction uses a measurable witness count H_r with E[H_r]<=8p(1), without asserting measurability of the exact number of distinct topological components.

original/ and AUTHOR_SAFE_FREEZE.zip preserve the exact frozen author packet. MEASURABILITY_CORRECTION.patch transforms its five-file directory into corrected/. ACCEPTANCE.json binds the exact corrected derivative and patch. Source documents, copied source text, dataset contents, and private coordination files are excluded.

To replay the 21 author controls and 17 fresh adversarial controls, run:

    python -I -B replay_author_controls.py

For full audit integrity, use the external manifest and its SHA-256 from the independently delivered audit handoff:

    python -I -B verify_audit.py /path/to/SIRSN_UNBOUNDED_9700033_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json EXPECTED_MANIFEST_SHA256

The manifest binds every safe file and the final ZIP. Keep its hash independently. No self-contained program can authenticate a package after an adversary replaces both the program and its external trust anchor.
