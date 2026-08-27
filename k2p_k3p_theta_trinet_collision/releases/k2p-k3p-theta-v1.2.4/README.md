# K2P/K3P theta-trinet collision release 1.2.4

This directory contains the replay archives accompanying the bioRxiv-ready
manuscript. They were built from the annotated tag
`k2p-k3p-theta-v1.2.4`, which resolves to full commit
`87d86cf348e888b29df94681426611ac601afe62`.

## Files

- `k2p-k3p-theta-collision-87d86cf348e8.zip`
- `k2p-k3p-theta-collision-87d86cf348e8.tar.gz`
- `SHA256SUMS-87d86cf348e8`
- one SHA-256 sidecar for each archive

The archive hashes are:

```text
24a5f9cb52cdad7f10a2a3bfe33777cb81b285ca63c7fbafa1b77e0051cabbf6  k2p-k3p-theta-collision-87d86cf348e8.zip
add48903979de1784ae28e56ae88ed0bd4f52944d9b80e1df32275bf5b6b3804  k2p-k3p-theta-collision-87d86cf348e8.tar.gz
```

Each archive contains `RELEASE_PROVENANCE.txt` and `FILE_SHA256SUMS`. The
author-only `submission/biorxiv/` staging files, the legacy package, caches,
and local build debris are excluded.

## Release validation

The commit-pinned builder completed the following fail-closed gates on
27 August 2026:

- version, `CITATION.cff`, annotated tag, and commit identity;
- deterministic double builds of ZIP and tar.gz and byte-identical extracted
  contents;
- internal and canonical SHA-256 manifests with exact path-set parity;
- exact verifier replay normally and with Python optimization, with byte-exact
  transcript comparison, including the K3P semantic-mutation suite and exact
  four-leaf graft regression;
- clean reconstruction of all three PDFs, with unchanged extracted text and
  rendered pixels and no TeX warning or error.

Best-guess completion is **100% for the technical release and replay
package**. The author's bioRxiv affiliation, distribution license, portal
category, and final approval remain intentionally outside this archive.

No GitHub release, Zenodo deposit, DOI, or external communication was created
as part of this packaging step.
