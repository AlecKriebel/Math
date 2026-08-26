# K2P/K3P theta-trinet collision release 1.1.0

This directory contains the replay archives accompanying the bioRxiv-ready
manuscript. They were built from the immutable annotated tag
`k2p-k3p-theta-v1.1.0`, which resolves to full commit
`d71493d1c188cc78ede27fed1744373272ffb220`.

## Files

- `k2p-k3p-theta-collision-d71493d1c188.zip`
- `k2p-k3p-theta-collision-d71493d1c188.tar.gz`
- `SHA256SUMS-d71493d1c188`
- one SHA-256 sidecar for each archive

Each archive contains `RELEASE_PROVENANCE.txt` and `FILE_SHA256SUMS`. The
author-only `submission/biorxiv/` staging files, the legacy package, caches,
and local build debris are excluded.

## Release validation

The commit-pinned builder completed the following fail-closed gates on
25 August 2026:

- version, `CITATION.cff`, tag, and commit identity;
- deterministic double builds of ZIP and tar.gz and byte-identical extracted
  contents;
- internal and canonical SHA-256 manifests with exact path-set parity;
- exact verifier replay normally and with Python optimization, with byte-exact
  transcript comparison;
- clean reconstruction of all three PDFs, with unchanged extracted text and
  rendered pixels and no TeX warning or error.

Best-guess completion is **100% for the technical release and replay
package**. The author's bioRxiv account email, distribution license, portal
category, and final approval remain intentionally outside this archive.

No GitHub release, Zenodo deposit, DOI, or external communication was created
as part of this packaging step.
