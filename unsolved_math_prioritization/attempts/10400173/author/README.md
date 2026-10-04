# Rank 637: Sato's subfactor lens-space question

Status: **unsolved**, five approach families completed. The literal lens-space clause has an explicit, exactly checked A6 Jones-subfactor specialization. The bundled request for optimal three-manifold classification remains unformalized and unresolved; complete classification is obstructed by published work.

Start with [RESEARCH_NOTE.md](RESEARCH_NOTE.md). This packet is an authored research note and reproducible algebraic certificate, not a novelty claim or a certified solution of the complete source problem.

## Reproduce

Requires Python 3.8 or later and only its standard library. No network, source PDFs, raw datasets, or credentials are needed.

    python3 verify_manifest.py
    python3 verify.py > /tmp/rank637-replay.json
    diff -u CONTROL_RESULTS.json /tmp/rank637-replay.json
    python3 -O verify.py > /tmp/rank637-optimized.json
    diff -u CONTROL_RESULTS.json /tmp/rank637-optimized.json

The expected result is 283 passing exact checks. All checks are explicit runtime checks and remain active under Python optimization. The matrix certificate is algebraic; subfactor realizability, the TV/center identification, and Funar's universal theorem are stated literature dependencies. Finite congruence checks do not prove an all-moduli statement.

## Files

- RESEARCH_NOTE.md: construction, proof, five approach families, limitations and references
- SOURCE_GATE.md / SOURCE_MANIFEST.json: identity, scope and inspected-source provenance
- STATUS.json / readiness.json: target coverage and current source binding
- RESEARCH_LOG.md / turns.jsonl: checkpointed research history and completion estimates
- verify.py / CONTROL_RESULTS.json: dependency-free exact controls
- verify_manifest.py / SHA256SUMS.json: authored-file integrity

Source PDFs, their extracted text, raw dataset records and coordination material are excluded. Public source hashes and sizes allow authorized inspection without republishing source content.
