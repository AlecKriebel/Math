# K2P/K3P theta-trinet collision release 1.2.1

This directory contains the replay archives accompanying the bioRxiv-ready
manuscript. They were built from the immutable annotated tag
`k2p-k3p-theta-v1.2.1`, which resolves to full commit
`45bedb7e76e2e314b2a8b986f822ed283fd96651`.

## Files

- `k2p-k3p-theta-collision-45bedb7e76e2.zip`
- `k2p-k3p-theta-collision-45bedb7e76e2.tar.gz`
- `SHA256SUMS-45bedb7e76e2`
- one SHA-256 sidecar for each archive

The archive hashes are:

```text
79df3ac662287c30c3d3f3a2c2b2e2176b66dba1dbbd13a768df503ba6e00e68  k2p-k3p-theta-collision-45bedb7e76e2.zip
3098e3a680e87d8fd2f5e1ff723575de82703855bd41b0e3f0ca0186d80d54f7  k2p-k3p-theta-collision-45bedb7e76e2.tar.gz
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
