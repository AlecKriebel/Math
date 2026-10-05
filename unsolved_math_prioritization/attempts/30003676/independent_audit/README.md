# Independent SIS audit: 30003676

Read AUDIT.md for the scoped verdict. The frozen author package by itself is REVISE_REQUIRED. Read together with AUTHORITATIVE_CORRECTIONS.md, it passes this audit as a partial investigation whose mathematical outcome is NO RESOLUTION. Do not describe the conjecture as solved.

- AUTHORITATIVE_CORRECTIONS.md: mandatory interpretation/replacement text for the frozen report
- AUDIT_RESULT.json: machine-readable verdict, limitations, and correction gate
- source_verification.json: public source metadata and independently checked inspection history
- independent_checks.py / independent_results.json: 1,407 exact assertions, eight wrong-model controls, and separately labeled floating diagnostics
- verify_frozen.py / frozen_replay.json: original hashes, exact author replay, archive membership, and integrity mutation tests
- verify_audit_manifest.py / MANIFEST.json: this audit's closed safe payload

Reproduce using Python 3.10 or later, standard library only:

    python3 independent_checks.py > /tmp/sis-independent-results.json
    python3 verify_frozen.py /path/to/original/sis_30003676 > /tmp/sis-frozen-replay.json
    python3 verify_audit_manifest.py

Exact result counts are deterministic. Last digits of floating diagnostics may vary across platforms; they are not exact tests or asymptotic proof certificates. Compare the exact result fields and use the stated tolerance/envelope checks for diagnostics.

Original source PDFs, screenshots, source extracts, raw datasets, and private coordination are excluded. The author freeze is external and unmodified. No remote publication was performed by this audit.
