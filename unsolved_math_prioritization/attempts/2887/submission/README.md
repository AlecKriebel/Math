# KP-4.11: orientable exotic Gluck twists

**Unsolved, 5/5 attempts. No complete candidate and no novelty claim.**

The exact target is Kirby's 2026 K3 Problem 4.11, numeric record 2887. Both the single-sphere and homotopic-pair existence questions require an orientable ambient manifold. Published nonorientable examples do not settle them.

- FULL_PROOF.md: five substantive routes, proved reductions and exact gaps
- APPROACH_LOG.md / turns.jsonl: five-turn accounting and completion estimates
- SOURCE_GATE.md / SOURCE_MANIFEST.json: source/version checks, prior-work limits and provenance
- STATUS.json: requested own-row outcome and scope
- VALIDATION_LIMITS.md: what is and is not established
- verify.py / CONTROL_RESULTS.json: reproducible exact algebraic controls
- SHA256SUMS.json / verify_manifest.py: frozen-byte integrity controls

Run from this folder using Python 3.10+ with only its standard library:

    python3 verify.py
    python3 verify_manifest.py

verify.py prints deterministic results without altering the package. Compare its JSON output to CONTROL_RESULTS.json. Neither command is a proof checker for smooth four-dimensional topology.

All source PDFs, copied corpus records, source screenshots and raw API data stay outside this package. Independent audit and the campaign's publication gate are still required. No remote writes were performed while preparing it.
