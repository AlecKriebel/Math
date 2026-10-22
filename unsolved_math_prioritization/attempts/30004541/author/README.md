# Derrida–Retaux extinction: author checkpoint

Exact target: 30004541 / OWR-2654828-006.

**NO RESOLUTION.** General initial-law classification and zero-energy extinction remain unproved here. This package contains five approaches, complete partial proofs, exact controls, and an explicit obstruction to a proposed moment shortcut. No novelty is claimed. Independent audit is pending.

- REPORT.md: exact model, scope, literature, five approaches, disposition
- PROOFS.md: complete retained partial arguments
- SOURCE_VERIFICATION.json: public source identities, PDF/corpus hashes and sizes, inspection limits, prior-work checks
- RESEARCH_LOG.md: checkpoints and five-approach ledger
- readiness.json: scope and success test; current source-hash verification still required before queue writes
- verify_controls.py and EXACT_CHECKS.json: 27 exact symbolic/rational controls, not a proof checker
- verify_manifest.py and AUTHOR_MANIFEST.json: byte-level artifact integrity

Run `python verify_controls.py` with Python 3 and SymPy 1.14.0, then `python verify_manifest.py`. The first script prints its results and does not modify files. The manifest validator rejects unexpected files and subdirectories in this package.

The release contains authored text/code and source-verification metadata only. Source PDF bytes, text extracts, dataset records, and private coordination are excluded. No remote write was made during preparation.
