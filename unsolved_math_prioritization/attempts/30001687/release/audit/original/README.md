# Fibonacci spectral thickness audit package

The independent review accepts the **unsolved 5/5** disposition with a minor required finite-gap statement correction and explicit regularity/presentation-coverage clarifications. No infinite-spectrum numerical certificate or new spectral theorem is supplied.

- `AUDIT.md`: full review, source checks, limitations, and results
- `CORRECTIONS.md`: precise replacement statements and proofs
- `AUDIT.json`: machine-readable verdict and bound author hashes
- `replay_results.json`: exact replay output from the frozen author script
- `independent_controls.py`: independent exact and floating-point controls
- `independent_results.json`: recorded independent output
- `SHA256SUMS`: hashes of this audit package's seven files

Keep this directory next to the frozen `author` directory. Requires Python 3, NumPy, SciPy for the author replay, and SymPy for the independent symbolic check.

```sh
cd author
sha256sum -c SHA256SUMS
cd ../audit
sha256sum -c SHA256SUMS
OPENBLAS_NUM_THREADS=1 python ../author/compute_controls.py --output /tmp/fibonacci-author-replay.json
cmp ../author/control_results.json /tmp/fibonacci-author-replay.json
OPENBLAS_NUM_THREADS=1 python independent_controls.py --author ../author --output /tmp/fibonacci-independent-replay.json
```

The independent script checks the frozen author manifest hash before examining author inputs and verifies all input hashes again at completion. Its combinatorial optimizer uses first-removal dynamic programming rather than importing the author's routines. Floating-point replay differences may vary across numerical-library versions; their agreement is not interval certification.

The frozen author's manifest SHA-256 is `2d657668c7f2b47f4429714e3e597baee441f32f58f262dc7bfb9d62dc5b4d8d`. Corrections are separate; applying them to an author packet creates a new subject that should receive a new manifest and an explicit reconciliation record. Source PDFs and private research materials are deliberately excluded.
