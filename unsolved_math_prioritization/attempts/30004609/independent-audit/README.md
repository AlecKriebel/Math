# Portable independent audit

Mathematical verdict: **PASS within the stated characteristic-zero scope**. No required mathematical correction was found. Novelty remains unestablished.

- `AUDIT.md`: complete claim-by-claim adversarial review and limits.
- `CORRECTIONS.md`: optional explanatory improvements; no blocking corrections.
- `AUDIT_RESULT.json`: machine-readable decision and coverage.
- `AUDIT_SOURCE_METADATA.json`: source URLs, checks, and bounded search disclosure; no source text.
- `AUDITED_INPUTS.json`: exact unchanged frozen author manifest.
- `inputs/author.zip`: exact unchanged frozen author packet, containing only its eight original deliverables.
- `AUTHOR_CHECK_RERUN.json`: byte-identical replay of the author's entire checker.
- `independent_checks.py` and `INDEPENDENT_CHECKS.json`: separate exact diagnostics, including a negative control and non-Fano Saito certificate.
- `AUDIT_MANIFEST.json`: hashes of every preceding audit file and binding to the frozen author packet.
- `verify_audit.py`: portable offline integrity and reproduction verifier.

Run `python verify_audit.py` from any working directory with Python 3 and SymPy 1.14.0 installed. The verifier extracts the frozen author packet only into a temporary directory, checks every input hash, reruns both suites, and compares outputs byte-for-byte. It neither contacts the network nor modifies the reviewed inputs.

The manifest excludes itself to avoid a self-hash cycle. The enclosing ZIP/manifest hashes should be checked against the independent delivery record. These diagnostic programs are not a proof assistant and do not replace the universal argument reviewed in `AUDIT.md`.

No scholarly PDF/full text, dataset contents, private sources, or coordination files are included.
