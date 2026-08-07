# Revision log

## Version 0.2 - 6 August 2026

### Preservation

- Preserved the discovery manuscript, Phase-V package, and their recorded hashes without overwriting the original project.
- Kept the full Phase-I-V development archive outside the clean first-contact archive; its hash is recorded separately.

### Mathematical audit

- Reconstructed the final proof from the marked-target manuscript alone, without using the discarded Phase-III or Phase-IV hierarchy arguments.
- Completed Gates A1-A12, including marked-channel irreducibility, properness of the residual factorial potential, the exact one-jump entropy identity, the full scalar-envelope branches, the exhaustive bimolecular top-complex split, finiteness and nonemptiness of the exceptional set, finite trace-chain closure, and direct nonexplosion.
- Tested all fifteen mandatory adversarial examples.
- Found no substantive theorem defect.

### Formal repairs

- Defined the augmented chain using the actual sampled reaction channel rather than the population displacement.
- Restricted one-jump sums explicitly to enabled source complexes.
- Stated the finite-class reduction before fixing an infinite class.
- Treated the zero-length path \(c=t\) explicitly.
- Proved that the exceptional set is nonempty using a global minimizer of the proper potential.
- Reserved “conservation law” for nonnegative invariants and called the service-species functional a signed linear stoichiometric invariant.
- Added the full finite trace-chain and embedded-chain-to-CTMC arguments.

### Literature and claim positioning

- Checked the 2018 Anderson-Kim paper, the 2020 Anderson-Cappelletti-Kim theorem, the Anderson-Kurtz stochastic-network reference, the May 2026 Xu revision, and later neighboring work through 6 August 2026.
- Calibrated the claim to: “This resolves the binary single-linkage case without the pure-species-complex hypothesis.”
- Added explicit disclaimers for multiple linkage classes, molecularity above two, the full conjecture, product forms, and quantitative convergence rates.

### Manuscript and metadata

- Rewrote the discovery note as a self-contained archival article with abstract, keywords, verified MSC2020 codes, definitions, proof, scope, declarations, references, and audit appendices.
- Prepared arXiv and Journal of Applied Probability initial-submission wrappers with identical mathematical content.
- Used the affiliation “Independent researcher” and did not imply a current UCI affiliation.
- No verified ORCID was supplied or located, so none was invented.
- Added a detailed AI-use declaration consistent with current arXiv and Cambridge guidance.

### Reproducibility

- Replaced the project-dependent verifier with a minimal standalone package having no imports outside the archive and no runtime third-party dependencies.
- Added a dependency-free editable-install backend, deterministic tests, fixed random seeds, canonical JSON output, and a one-command reproducer.
- Required two consecutive verifier runs to produce byte-identical reports.
- Added deterministic LaTeX metadata controls and tested PDF reproducibility under the released toolchain.
