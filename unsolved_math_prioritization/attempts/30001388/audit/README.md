# Independent audit of OWR 4137 004

The verdict is **accept as an unsolved five-approach investigation**. No substantive mathematical correction was found at the frozen packet's expressly limited scope. This is not a solution or novelty certificate.

Files:

- `AUDIT.md`: full mathematical audit, source hypotheses, proof checks, clarifications, and recommendation
- `input-verification.json`: exact input-release and source-file bindings
- `original-controls-replayed.json`: byte-identical replay of the author's controls
- `audit_controls.py` and `audit-controls.json`: independent exact, discriminating controls and their output
- `verify_release.py`: read-only checker for the frozen input, this audit, and both control replays
- `review.json`: machine-readable verdict and scope
- `MANIFEST.json`: hashes and lengths of this audit's files

To replay the independent controls with Python 3.10 or newer:

    python3 audit_controls.py > /tmp/baker-audit-controls.json
    cmp /tmp/baker-audit-controls.json audit-controls.json

To verify the complete release when the original packet is available:

    python3 verify_release.py /path/to/original/public

The source PDFs were read privately and are intentionally absent. No external dependencies, network access, source redistribution, or remote writes are needed to replay the controls. Mathematical proofs remain in the report; finite tests do not prove the general conjecture.
