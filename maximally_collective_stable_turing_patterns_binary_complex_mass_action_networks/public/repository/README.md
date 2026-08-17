# Exact Diffusion Design for Maximally Collective Stable Turing Patterns

Portable exact source, proof certificates, independent verifiers, current-profile numerical illustrations, and manuscript sources for the corrected final release.

## Replay

```bash
bash replay.sh
```

The full command regenerates the current exact finite data, verifies the all-dimensional certificates, reruns mutation tests and numerical illustrations, rebuilds all four figures, and compiles the manuscript and supplement. Numerical illustrations are not used in any proof.

`verification_outputs/` records the current repair campaign, and
`sha256_manifest.txt` verifies the initially downloaded tree. Running the
replay regenerates both for the local toolchain.
