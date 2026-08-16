# Version 1.1.1 release notes

Date: 16 August 2026.

This is a submission-readiness and verifier-hardening patch. It does not alter
the stated construction, theorem, proof scope, or novelty claim.

## Changes

- Hardened every supported scientific verifier against optimized-Python
  false passes and replaced scientific assertions with explicit checks.
- Retained the original supplied SymPy attachment byte for byte under the
  unambiguous archival name `verify_supplied_original.py`.
- Added independent literal checks of the active operator, active Hecke
  relation, both obstruction norms, far commutativity, and every generic
  converse branch.
- Added mutation/negative tests and a portable, path-safe checksum verifier.
- Made the internal checksum manifest self-contained and removed website
  files from the curated source archive boundary.
- Made the deterministic source ZIP an exact manifest allowlist, with a hard
  failure on unexpected submission-directory contents.
- Locked Python dependencies by wheel hash and pinned the Tectonic version,
  resource bundle, and deterministic build epoch.
- Added explicit manuscript/code licenses, citation metadata, Zenodo/arXiv
  metadata, journal highlights, and submission checklists.
- Corrected Wenzl's official title, printed the Markov normalization used in
  the GHR identification, and refreshed every priority/reference check through
  16 August 2026.
- Added the title-page metadata and declarations required for the planned
  journal workflow, including a transparent generative-AI declaration.
- Added commit-pinned continuous-integration gates for clean-environment
  verification, mutation tests, PDF reproduction, and isolated archive checks.

No DOI is claimed in this version. A fresh manual Zenodo record must be used;
the unrelated monorepo concept DOI must not be reused.
