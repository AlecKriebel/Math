# Exact Diffusion Design for Maximally Collective Stable Turing Patterns

Portable exact source, proof certificates, independent verifiers, current-profile numerical illustrations, and manuscript sources for the corrected final release.

The immutable version 1.0.4 snapshot is published at
<https://github.com/AlecKriebel/Math/releases/tag/maximally-collective-stable-turing-v1.0.4>;
archived versions share <https://doi.org/10.5281/zenodo.21753404>.

## Replay

```bash
bash replay.sh
```

The full command regenerates the current exact finite data, verifies the all-dimensional certificates, reruns mutation tests and numerical illustrations, rebuilds all four figures, and compiles the manuscript and supplement. Numerical illustrations are not used in any proof.

`verification_outputs/` records the current repair campaign, and
`sha256_manifest.txt` verifies the initially downloaded tree. Running the
replay regenerates both for the local toolchain.
