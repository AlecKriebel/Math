# K2P/K3P theta-trinet collision release 1.2.3

This directory contains the replay archives accompanying the bioRxiv-ready
manuscript. They were built from the immutable annotated tag
`k2p-k3p-theta-v1.2.3`, which resolves to full commit
`3d3e4abee9f4dab9f5f1b3ec9f73740aa04c565c`.

## Files

- `k2p-k3p-theta-collision-3d3e4abee9f4.zip`
- `k2p-k3p-theta-collision-3d3e4abee9f4.tar.gz`
- `SHA256SUMS-3d3e4abee9f4`
- one SHA-256 sidecar for each archive

The archive hashes are:

```text
c8f1d4aadb93a5b4a39095f92a0b4b69bbc37265c7ea0165477cc7d2e4eca9d3  k2p-k3p-theta-collision-3d3e4abee9f4.zip
d2f09e150a0ca0a38224bf6070a425d4cd594a0d5b135791c39fd16797a3e6fa  k2p-k3p-theta-collision-3d3e4abee9f4.tar.gz
```

Each archive contains `RELEASE_PROVENANCE.txt` and `FILE_SHA256SUMS`. The
author-only `submission/biorxiv/` staging files, the legacy package, caches,
and local build debris are excluded.

## Release validation

The commit-pinned builder completed the following fail-closed gates on
26 August 2026:

- version, `CITATION.cff`, annotated tag, and commit identity;
- deterministic double builds of ZIP and tar.gz and byte-identical extracted
  contents;
- internal and canonical SHA-256 manifests with exact path-set parity;
- exact verifier replay normally and with Python optimization, with byte-exact
  transcript comparison, including the exact four-leaf graft regression;
- clean reconstruction of all three PDFs, with unchanged extracted text and
  rendered pixels and no TeX warning or error.

Best-guess completion is **100% for the technical release and replay
package**. The author's bioRxiv affiliation, distribution license, portal
category, and final approval remain intentionally outside this archive.

No GitHub release, Zenodo deposit, DOI, or external communication was created
as part of this packaging step.
