# K2P/K3P theta-trinet collision release 1.2.0

This directory contains the replay archives accompanying the bioRxiv-ready
manuscript. They were built from the immutable annotated tag
`k2p-k3p-theta-v1.2.0`, which resolves to full commit
`7570a4a0f7051a607ee6eb4ef7ed43e54e805322`.

## Files

- `k2p-k3p-theta-collision-7570a4a0f705.zip`
- `k2p-k3p-theta-collision-7570a4a0f705.tar.gz`
- `SHA256SUMS-7570a4a0f705`
- one SHA-256 sidecar for each archive

The archive hashes are:

```text
0a0985adc5724392ff316f644ec80a3963b4dda194aeebc7984711f6b572b139  k2p-k3p-theta-collision-7570a4a0f705.zip
986cff9666b478bdc6f2730c3398087e6a79ad9470505848b6f012b6e59d0592  k2p-k3p-theta-collision-7570a4a0f705.tar.gz
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
package**. The author's bioRxiv account email, affiliation, distribution
license, portal category, and final approval remain intentionally outside this
archive.

No GitHub release, Zenodo deposit, DOI, or external communication was created
as part of this packaging step.
