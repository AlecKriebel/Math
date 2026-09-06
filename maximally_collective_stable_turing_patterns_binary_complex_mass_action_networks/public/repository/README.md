# Exact Diffusion Design for Maximally Collective Stable Turing Patterns

Portable exact source, proof certificates, independent verifiers, current-profile numerical illustrations, and manuscript sources for the corrected final release.

This package targets the immutable version 1.0.10 snapshot at
<https://github.com/AlecKriebel/Math/releases/tag/maximally-collective-stable-turing-v1.0.10>.
Archived versions share <https://doi.org/10.5281/zenodo.21753404>. The exact
preceding version 1.0.9 snapshot has DOI <https://doi.org/10.5281/zenodo.22478273>.

## Replay

```bash
bash replay.sh
```

The full command regenerates the current exact finite data, verifies the all-dimensional certificates, reruns mutation tests and numerical illustrations, rebuilds all four figures, and compiles the manuscript and supplement. Numerical illustrations are not used in any proof.

`verification_outputs/` records the command, scope, evidence class, and release
version of stored evidence. `sha256_manifest.txt` verifies the initially
downloaded tree and is never rewritten by replay. Deterministic regenerated
artifacts are compared with that baseline; the replay writes its local tree to
`verification_outputs/replay_self_consistency_manifest.txt` instead.

Release qualification uses the exact Python and TinyTeX 2022.04 environment in
`environment/TESTED_ENVIRONMENT.md`; `requirements.txt` remains a compatibility
minimum for exploratory use.
