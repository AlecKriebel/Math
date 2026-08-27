# K2P/K3P theta-trinet collision release 1.2.5

This directory contains the replay archives accompanying the bioRxiv-ready
manuscript. They were built from the annotated tag
`k2p-k3p-theta-v1.2.5`, which resolves to full commit
`9f8d2682ead74e23b7badd9d7f46869477b4e84f`.

## Files

- `k2p-k3p-theta-collision-9f8d2682ead7.zip`
- `k2p-k3p-theta-collision-9f8d2682ead7.tar.gz`
- `SHA256SUMS-9f8d2682ead7`
- one SHA-256 sidecar for each archive

The archive hashes are:

```text
bbcb8c460bc940e886c11899bba4ec674c73def0ca12955775f1a5f8ff510741  k2p-k3p-theta-collision-9f8d2682ead7.zip
6decd0b632e195870f5c25d3346cf39aa6ad8a380d838d4d58e9fb8214ffbca1  k2p-k3p-theta-collision-9f8d2682ead7.tar.gz
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
  transcript comparison, including the compact-K2P field-mutation guard, the
  expanded K3P semantic-mutation suite, and exact four-leaf graft regression;
- clean reconstruction of all three PDFs, with unchanged extracted text and
  rendered pixels and no TeX warning or error.

Best-guess completion is **100% for the technical release and replay
package**. The author's bioRxiv affiliation, distribution license, portal
category, and final approval remain intentionally outside this archive.

No GitHub release, Zenodo deposit, DOI, or external communication was created
as part of this packaging step.
