# 5300071: Uniform access to roots for relaxed Newton maps

**Status: unsolved.** This five-approach research packet establishes elementary
local and two-root special-case results, records an exact obstruction to one
nesting direction, and isolates the missing simultaneous common-arc estimate.
It is not a solution paper.

- `RESULT.md`: precise target, proofs, logical obstructions and remaining gap.
- `APPROACHES.md` and `turns.jsonl`: all five substantive attempts.
- `SOURCE_GATE.md` and `SOURCE_MANIFEST.json`: inspected sources and limitations.
- `verify.py` / `CONTROL_RESULTS.json`: reproducible controls.
- `VALIDATION_LIMITS.md`: what the evidence does not establish.
- `SHA256SUMS.json` / `verify_manifest.py`: frozen authored-file integrity.

Reproduce with Python 3.10 or newer, no third-party packages or network:

    python verify.py > replay.json
    python -c "import json; assert json.load(open('replay.json')) == json.load(open('CONTROL_RESULTS.json'))"
    python verify_manifest.py

Write a replay output outside this directory when verifying the frozen file
allowlist. Source PDFs, full text, source corpora and private coordination
records are intentionally excluded from the authored packet. Source hashes,
byte counts, public URLs, and inspection history provide retrieval provenance.

No merge, release, DOI, external outreach, or queue.py operation is part of this
packet. Final remote collision checks and fresh audit remain separate gates.
