# Independent audit of 30003114

Verdict: **PASS FOR SCOPED PARTIALS; target unresolved.** No mandatory correction was found. The author freeze remains unchanged.

Files:
- AUDIT.md: complete mathematical, source, quantifier and integrity audit.
- SOURCE_AUDIT.json: independently corroborated public source identities and inspection limits.
- independent_verify.py: standalone exact verifier, standard library only, no network.
- INDEPENDENT_RESULTS.json: deterministic output with the frozen packet supplied.
- AUTHOR_REPLAY.json: byte-identical assertion-enabled author replay.
- EXECUTION_CONTROLS.json: expected rejection of disabled assertions and one intentionally failed assertion mutant.
- AUDIT_STATUS.json: scoped machine-readable verdict.
- INTEGRITY.json: binding to the original author freeze and safe-file boundary.
- MANIFEST.json: hashes and byte counts of this audit's deliverables, excluding itself.

To run the independent finite mathematical controls alone:

    python3 independent_verify.py

To additionally check the author freeze, replay its tests, and run temporary-copy integrity mutations:

    python3 independent_verify.py --safe /path/to/author/safe --archive /path/to/LITTLEWOOD_30003114_SAFE_PACKET.zip

The latter deterministic JSON must match INDEPENDENT_RESULTS.json. Use Python 3.9 or newer with assertions enabled. Optimized invocations are rejected and do not constitute verification. No source PDFs or raw dataset records are needed for the executable controls. Public source metadata was separately checked; the verifier does not re-download sources.

Mathematical proofs establish the scoped all-degree partial results. Finite controls provide falsification checks and reproducibility, never an all-degree or all-denominator proof of the target.
