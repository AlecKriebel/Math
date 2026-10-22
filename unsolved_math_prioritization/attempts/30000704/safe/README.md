# Boundary regularity for complete conformal metrics

Research target: 30000704 / OWR-1460-010, ranked 660.

Outcome: **partial, full target unresolved after five substantive approaches**.
The authored note proves a no-differentiability sufficient theorem for
explicit one-sided free Jordan arcs, plus a more general forward implication
under local componentwise regular-openness. Constant-curvature counterexamples
exclude punctures and arbitrary distinguished subsets of smooth boundaries.
Neither a weakest general boundary criterion nor novelty is established.

Files:
- ANALYSIS.md: complete proof, assumptions, counterexamples, unresolved scope
- APPROACH_LOG.md and turns.jsonl: five approach families and their results
- SOURCE_GATE.md and SOURCE_MANIFEST.json: source verification and limits
- controls/verify.py and CONTROL_RESULTS.json: exact reproducible controls
- STATUS.json: machine-readable claim and audit boundary
- SHA256SUMS.json and verify_manifest.py: frozen safe-file inventory

Run from this directory:

    python3 controls/verify.py
    python3 verify_manifest.py

Controls require Python 3.10+ and SymPy (author run: 1.14.0). No network
is used. The default run prints results without modifying the frozen files.

This directory contains authored mathematics/code and public source metadata.
It contains no source PDF, extracted scholarly text, dataset contents,
private coordination records, or credentials. Source inspection evidence is
kept separately. An independent audit is required before any promotion.
