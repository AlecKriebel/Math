# High Influence Small Sets in Boolean Functions

- Numeric ID: 30001672
- Source code: OWR-4791-032
- Disposition: **already_solved**, negatively
- Contribution: source verification and correction of the catalogue's open-status assessment
- New mathematical discovery claimed: none

The 2013 Kahn–Kalai counterexample theorem, also published in Bourgain–Kahn–Kalai (2024), supplies exactly balanced Boolean functions for which every coalition of at most n/3 variables misses output 1 on at least an inverse-polynomial fraction of outside assignments. Such fibers are determined, so the requested exponentially small determination probability is impossible.

See [PROOF.md](PROOF.md) for the exact implication, [SOURCES.md](SOURCES.md) for primary-source locations, and [RESEARCH_LOG.md](RESEARCH_LOG.md) for the bounded investigation.

## Reproduce the finite controls

Run `python3 verify_bridge.py` using Python 3.10 or later; no third-party packages or network are needed. It recreates `control_results.json` and checks 1,050,698 function–coalition pairs, comprising every Boolean function on up to four variables and every coalition. These controls establish neither the published infinite construction nor optimality.

`SHA256SUMS` binds the safe author packet. No source PDFs, source-text extracts, or dataset corpora are included. Independent adversarial review is required before remote publication.
