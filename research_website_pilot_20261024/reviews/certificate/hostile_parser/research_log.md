# Hostile parser review research log

Scope: deposited `verify_currents.py` and real `square_flow_certificate.json.gz`, without modifying source, accessing prior review artifacts, network, Git, or external contact.

## 2026-10-24T22:50:32.560224+00:00 — Initial checkpoint

Completion estimate: **75%** toward the assigned finite input-validation audit. Status: **HOLD pending runnable mutation results**.

Static review confirms that `main()` first SHA256-pins compressed bytes, then decompresses and parses. `check(data)` independently regenerates ordered graph edges and validates all integer currents, divergences, individual energies, and the fixed total. Ordinary JSON duplicate-key resolution, floating-point `vertices=3070.0`, and unused metadata are candidate permissive cases; their mathematical impact must be separated from malformed input handling. The unchanged source and certificate have been copied locally and hash-checked. A full-certificate mutation suite is running; no reduced graph or mocked checker is used.

Exact claim under review: no tested malformed mathematical content is accepted as a certificate by the deposited pinned entry point; for the direct checker, acceptance must imply the fixed graph and integer-flow constraints despite JSON/schema leniencies. Falsification criterion: any parsed JSON object accepted with a wrong source, invalid graph/edge set, nonintegral or infeasible current, incorrect energy, or denominator inconsistent with the claimed bound. This does not audit the manuscript's infinite-volume transfer or novelty.

## 2026-10-24T22:52:12.934873+00:00 — Final checkpoint

Completion estimate: **100%** of the assigned finite input-validation audit. Status: **PASS with API/schema limits**.

The full unchanged-checker mutation suite completed 161/161 expected outcomes: 145 rejections and 16 accepted genuine or intentionally permissive cases. All 20 altered-file main-entry subprocess cases failed the compressed SHA256 pin; genuine ordinary and optimized runs passed. Wrong current/source/edge/energy/denominator cases failed direct validation. A divergence-preserving triangle circulation with recomputed energies failed the fixed total. Duplicate-key last-wins semantics, float vertices, ignored metadata, and unchecked helper-denominator arguments are documented bounded leniencies, not demonstrated false-math certification. The actual deposited JSON has no duplicate keys or nonstandard numeric constants. Artifacts: REPORT.md, test_hostile_parser.py, test_results.json, genuine_json_structure.json, and unchanged checker/certificate copies. No source changes, network, Git, or external contact. Exact remaining gap: this review does not independently verify graph identification, infinite-volume transfer, or novelty.
