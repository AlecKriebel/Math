# 30003741: a sharp four-site bound and the higher-N gap

The higher-multiplicity question remains unresolved in the source's agonist-only setting. This package proves an exact scalar reduction, a parity-dependent upper bound for every chain length, and a sharp three-equilibrium result for four sites.

- [Partial theorem and rational witness](PARTIAL.md)
- [Source and literature audit](SOURCE_AUDIT.md)
- [Exact verifier](verify.py) and [receipt](verification.json)
- [Exploratory scan](exploratory_scan.py) and [limited numerical observations](turning_scan.json)
- [Readiness evidence](readiness.json) and [research log](RESEARCH_LOG.md)

The exact verifier requires Python and SymPy 1.14.0; all 1,543 assertions pass. The separate exploratory scan uses NumPy, is not proof, and is unnecessary to reproduce the mathematical certificate. Both scripts write their receipts beside themselves.

Status: unsolved, 2/5; separate adversarial review pending. No dynamical stability, physiological relevance or historical novelty is asserted. The externally announced two-ligand five-state candidate is explicitly distinguished from the narrower target.
