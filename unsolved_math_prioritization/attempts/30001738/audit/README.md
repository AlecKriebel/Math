# Independent unitary multiplicity audit

Read AUDIT_REPORT.md for the verdict, source scope, mathematical checks and limitations. The original author packet is accepted unchanged within its precise p-adic irreducible source scope. The literal catalogue assertion is false.

Files:
- AUDIT_REPORT.md: independent authored audit
- SOURCE_CHECKS.json: fresh public-source fingerprints, corpus checks and inspection history
- replay_audit.py: independent standard-library replay and corruption tests
- REPLAY_RECEIPT.json: complete results of three passing replays and 38 rejected mutations
- MANIFEST.json: SHA-256 hashes and byte counts of all other public audit files

Replay with a trusted Python 3 interpreter:

    python -I -S -B replay_audit.py AUTHOR_DIRECTORY AUTHOR_ZIP

Obtain and check the audit manifest and replay_audit.py pins independently before execution. The script pins the original author manifest, verifier and archive; it never modifies them. It creates temporary copies for mutation tests and compares the original packet again afterward. Fresh source/corpus checks are recorded separately and require independently obtaining the public sources.

No source PDFs, extracts, screenshots, dataset contents, private sources or private coordination material are included. Finite diagnostics are not a proof of the external analytic theorem.
