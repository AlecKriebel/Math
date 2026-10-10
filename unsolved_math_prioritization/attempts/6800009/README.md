# Bi-invariant metrics and conjugate multiplicity

Problem 6800009 / AMR-067-0009 has a negative answer under its printed, fixed-group-structure formulation. This packet gives a credited consequence of prior constructions and a direct proof for SU(2) × SU(2).

The construction is already represented in Fusi–Lafuente–Stanfield, arXiv:2608.25619v1, Proposition 7.3. Older compact-connected examples appear in Barbaro, arXiv:2307.10207v2, Example 4.1. No new-construction or first-resolution claim is made.

- [SOURCE_CERTIFICATE.md](SOURCE_CERTIFICATE.md): exact scope, prior credit, explicit metric, and full index calculation
- [GATE_REPORT.md](GATE_REPORT.md): provenance, literature/prior-work checks, and access limitations
- [RESEARCH_LOG.md](RESEARCH_LOG.md): chronology and honest turn accounting
- [source_record.json](source_record.json): machine-readable identifiers and sources
- [verify.py](verify.py): exact finite algebra diagnostics using the Python standard library
- [verify_results.json](verify_results.json): expected diagnostic results
- [MANIFEST.json](MANIFEST.json): hashes of public packet files

Run `python3 verify.py` from this directory. The script checks the metric and coordinate conversion, non-invariance witness, rational-quaternion action identities, and strict endpoint counting. These checks supplement the full proof; they do not replace it.

This source-resolution packet passed a fresh independent adversarial audit for the literal fixed-group-law question. The outcome is already_solved with 1/5 investigative turns used. Third-party papers, screenshots, raw corpus files, and private coordination are excluded.

## Independent review

[AUDIT_REPORT.md](AUDIT_REPORT.md) records the scope-qualified PASS. Run `python3 independent_controls.py` for portable controls deriving the Levi-Civita curvature and geodesic equations independently. The [change map](CHANGE_MAP.md) identifies all packaging edits since the reviewed freeze.
