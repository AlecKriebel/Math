# Revision log

## Version 0.3 - 9 August 2026

### Proof precision and exposition

- Preserved the marked-target proof architecture after a fresh adversarial
  reconstruction found no theorem-breaking defect.
- Made the CTMC positive-return convention, stopped episode chain, finite-index
  integrability, trace-excursion conditioning, population projection, uniform
  lower rate bound, and class-wise nonexplosion statements explicit.
- Rewrote the abstract for the Applied Probability journals, added a worked
  trigger-and-drain calculation and proof schematic, clarified the central
  bimolecular alternative, and moved the bibliography to the end.

### Literature, declarations, and submission metadata

- Added the announced two-dimensional recurrence result to the priority audit
  with scope explicitly distinguished from the arbitrary-dimensional
  bimolecular single-linkage theorem.
- Added the author-supplied ORCID `0009-0001-9320-500X` and repository citation
  metadata; no DOI is claimed.
- Reconciled the manuscript and supplement AI declarations with the current
  Cambridge policy and the actual ChatGPT, Claude, Claude Code, and Codex uses.
- Updated the cover letter, code-availability statement, and journal wrapper.

### Verification and release integrity

- Replaced incidental recursive source hashing with an explicit verifier input
  set and separated stable mathematical output from environment provenance.
- Replaced vacuous or mislabeled tests with exact entropy checks, episode and
  boundary checks, and independently validated top-complex witnesses.
- Made the standalone reproducer installation-free and portable, and made it
  compare two fresh runs with the committed golden report without overwriting
  that report.
- Removed elapsed-time noise from the Phase-V certificate, repaired archived
  runners and instructions, and regenerated all affected certificates.
- Replaced the stale partial release manifest with a portable complete-tree
  writer/verifier and added clean-environment continuous-integration checks.
- Clarified that archived Phases II--IV are superseded research history and
  that internal adversarial reconstruction is not independent expert review.

## Version 0.2 - 6 August 2026

### Historical preservation intent

- Retained the discovery manuscript and Phase-I--V development files in the
  repository. A later release audit found that the v0.2 manifest referred to a
  separate `discovery_version/` distribution that was not present in the Git
  tree; Version 0.3 replaces that unverifiable claim with Git-tree provenance.

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
- No ORCID was recorded in Version 0.2. Version 0.3 adds the identifier later
  supplied by the author.
- Added a detailed AI-use declaration consistent with current arXiv and Cambridge guidance.

### Reproducibility

- Replaced the project-dependent verifier with a minimal standalone package having no imports outside the archive and no runtime third-party dependencies.
- Added a dependency-free editable-install backend, deterministic tests, fixed random seeds, canonical JSON output, and a one-command reproducer.
- Required two consecutive verifier runs to produce byte-identical reports.
  Version 0.3 additionally compares their stable content with the committed
  golden report and excludes incidental transcripts and environment metadata.
- Added deterministic LaTeX metadata controls and tested PDF reproducibility under the released toolchain.
