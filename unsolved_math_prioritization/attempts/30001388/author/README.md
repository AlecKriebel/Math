# Escaping Boundary Points of Baker Domains

ID 30001388 · OWR-4137-004 · 4 October 2026

**Unsolved after five substantive approaches.** No general proof, counterexample, or novelty claim is made.

- `RESULT.md`: exact target, proofs of the reductions and controls, five routes, and remaining gaps.
- `APPROACH_LOG.md` and `turns.json`: approach-level accounting and completion estimates.
- `SOURCES.json`: primary-source identifiers, theorem locators, and consulted-file hashes.
- `readiness.json`: scope, prior-work and related-target checks.
- `verification/check.py`: deterministic exact controls using only Python's standard library.
- `verification/result.json`: checked output.
- `MANIFEST.json`: SHA-256 manifest of the author-created packet.

Reproduce from this directory:

    python3 verification/check.py > /tmp/baker-check.json
    cmp /tmp/baker-check.json verification/result.json

The code is a control against incorrect arguments, not a computer-assisted solution of the general problem. Source PDFs and extracted source text are not included.
