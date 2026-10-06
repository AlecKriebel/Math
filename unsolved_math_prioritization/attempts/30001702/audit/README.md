# Independent audit packet

Verdict: ACCEPTED_PARTIAL_UNRESOLVED. This packet independently audits the separately frozen seven-file author packet for problem 30001702 / OWR-4798-027. It does not solve the universal factorial facet problem.

- ADVERSARIAL_AUDIT.md: scope, findings, adversarial tests, and verdict
- EXPANDED_LEMMAS.md: independent detailed mathematical arguments
- SOURCE_AUDIT.json: public source/data hashes and inspection metadata only
- ACCEPTANCE.json: machine-readable acceptance and actual replay evidence
- INDEPENDENT_RESULTS.json and independent_check.py: independent finite diagnostics
- AUTHOR_CONTROL_RESULTS.json and audit_controls.py: anchored original-packet replay and mutation checks
- verify_audit.py: strict external-manifest verification and replay of this packet

Run the independent diagnostics with Python 3:

    python -I -B independent_check.py
    python -I -B -O independent_check.py

The audit replay verifier takes --root and an externally supplied --manifest. Optional --author-root, --author-manifest, and --author-archive rerun the original-packet adversarial controls as well. Keep the separately supplied audit manifest outside the safe directory. Pin that manifest or the audit ZIP by its independently supplied SHA-256 before trusting it. No self-generated manifest authenticates a packet by itself.

No external package, network request, or source dataset is needed for the finite replay. Mathematical acceptance rests on the prose audit and primary references, not on finite code checks alone. Downloaded sources and datasets are excluded from this public-safe payload.
