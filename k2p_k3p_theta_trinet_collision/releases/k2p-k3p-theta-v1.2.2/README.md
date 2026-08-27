# K2P/K3P theta-trinet collision release 1.2.2

This directory contains the replay archives accompanying the bioRxiv-ready
manuscript. They were built from the immutable annotated tag
`k2p-k3p-theta-v1.2.2`, which resolves to full commit
`6d3f202f9018f13fca2494c5cbb411da4ab43a8a`.

## Files

- `k2p-k3p-theta-collision-6d3f202f9018.zip`
- `k2p-k3p-theta-collision-6d3f202f9018.tar.gz`
- `SHA256SUMS-6d3f202f9018`
- one SHA-256 sidecar for each archive

The archive hashes are:

```text
8352bc2e8458fa9ff993d69db3f643f1e586104b967d0de34758925b25c57d2a  k2p-k3p-theta-collision-6d3f202f9018.zip
ecbc7d4cc903836075ba9d247108467a67266bf2e8145d04eb283e091f686d76  k2p-k3p-theta-collision-6d3f202f9018.tar.gz
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
