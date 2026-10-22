# Bounded polynomial partial-sum audit

Disposition: **partial progress, not a solution of the full term-count problem**.

Read REPORT.md for definitions, five distinct approaches, complete partial-result proofs, and the exact unresolved obstruction. sources.json contains public provenance metadata only. No source PDFs, extracted text, original question record, dataset contents, or private coordination material are included.

The exact checker requires Python 3.10 or newer and no third-party packages:

    python3 -I -B verify.py fixtures.json
    python3 -I -B -O verify.py fixtures.json
    python3 -I -B -OO verify.py fixtures.json

It writes only a JSON report to standard output. Failure gives a nonzero exit code. It also accepts --stdin for externally verified fixture bytes. For a frozen audit, authenticate the separate external manifest and bootstrap using independently supplied pins before running their command. See the external AUDIT_INSTRUCTIONS.md.

No repository state or external service was changed in preparing this packet. Independent mathematical review is still required before treating any result as accepted.
