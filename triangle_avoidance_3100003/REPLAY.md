# Replay and package integrity

Executed 2026-10-20 with Python 3, standard library only, from the package directory.

- `python3 stripe_exact.py`: exit code 0; all five expected rational fixed-width checks passed. The output matches the supplied result JSON, both as bytes and parsed values.
- `python3 check_square_grid.py`: exit code 0; PASS: 41616 pairs; 134 distinct squared distances; 289 points.

The stripe checks include an equality-boundary success, a success below the simpler sufficient threshold, an explicit flat-triangle failure at its specified width, a 3–4–5 success, and failure at a width exceeding the minimum altitude. These are sanity checks, not an all-width execution or a proof of the unrestricted conjecture.

## Reviewed versions and packaged versions

`AUDIT.md` retains the SHA-256 hashes of the four proof documents as originally reviewed. The mathematical proofs are unchanged in this package. Presentation-only edits replace source-gate references with the self-contained `SCOPE.md`, make the script command package-relative, and remove one nonmathematical introductory sentence before the stripe cutoff proof. Consequently, the historical reviewed-version hashes in the audit are not the packaged-file integrity hashes. `MANIFEST.json` and `SHA256SUMS` describe the packaged versions.

The Python scripts are unchanged. The grid output was captured during replay, and the stripe result was regenerated and checked against the supplied output. The package contains only authored mathematical notes, the audit, code, results, public-source references, and integrity metadata.

`MANIFEST.json` lists every payload file with its byte count and SHA-256 digest, excluding itself and `SHA256SUMS`. `SHA256SUMS` additionally seals `MANIFEST.json` and excludes only itself. As usual, this detects changes against the supplied manifest but is not an external signature or attestation.
