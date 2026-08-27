# K2P/K3P theta-trinet collision release 1.2.6

This directory contains the replay archives accompanying the bioRxiv-ready
manuscript. They were built from the annotated tag
`k2p-k3p-theta-v1.2.6`, which resolves to full commit
`672d96a08be174cd6b67762a6907dfbdcd926b9b`.

## Files

- `k2p-k3p-theta-collision-672d96a08be1.zip`
- `k2p-k3p-theta-collision-672d96a08be1.tar.gz`
- `SHA256SUMS-672d96a08be1`
- one SHA-256 sidecar for each archive

The archive hashes are:

```text
e0200c66b87c373fb718553ea2b9d8bbaa70c98bd78772ad1874cb9ccd47db12  k2p-k3p-theta-collision-672d96a08be1.zip
7b2ef2796353cf60633333ea0ac8296029a3a764422c39ac9ce98fb528c73d99  k2p-k3p-theta-collision-672d96a08be1.tar.gz
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
  transcript comparison, including duplicate-key and closed-schema hostile
  tests, the compact-K2P field-mutation guard, the expanded K3P semantic suite,
  and the exact four-leaf graft regression;
- clean reconstruction of all three PDFs, with unchanged extracted text and
  rendered pixels and no TeX warning or error.

Best-guess completion is **100% for the technical release and replay
package**. The author's bioRxiv affiliation, distribution license, portal
category, and final approval remain intentionally outside this archive.

No GitHub release, Zenodo deposit, DOI, or external communication was created
as part of this packaging step.
