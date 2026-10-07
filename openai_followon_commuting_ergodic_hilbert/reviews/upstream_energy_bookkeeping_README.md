# Reproduction of the upstream energy audit's seeded bookkeeping test

The exact numerical procedure originally run inline by `upstream_energy_audit`
is now saved as `upstream_energy_bookkeeping.py`. Its arithmetic, random seed,
sample ordering, dimensions, singular-support cutoff, and number of trials
are unchanged. A new execution reproduced both reported decimal outputs
exactly; the stdout is saved in `upstream_energy_bookkeeping_output.txt`.

From the dedicated project folder, run:

```sh
/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 reviews/upstream_energy_bookkeeping.py
```

The script uses Python 3.12.14, NumPy 2.3.5, and macOS Accelerate LAPACK/BLAS
on arm64. The full environment summary is saved in
`upstream_energy_bookkeeping_environment.json`. Another NumPy or LAPACK build
may differ in the final floating-point digits. The script generates all
inputs from the fixed seed; it requires no unpublished arrays or data files.

The result is exactly:

```text
5000 random/rank-deficient cyclic tests; max mixed ratio 0.07470168193073122
15000 neighbor tests; max neighbor ratio 0.707003261832278
```

These ratios compare the sampled left sides to the stated inequality right
sides. Each cyclic sample has one comparison for mixed trace and three for
neighbor comparison. Half of the cyclic samples deliberately use edges of
rank at most one. The spectral calculation discards eigenvalues no larger
than `max(max_eigenvalue,1)*1e-12`, so this is a limited floating-point
bookkeeping test. It provides no exact certificate for singular support,
near-zero eigenvalues, all matrix dimensions, or any analytic theorem.
The audit's algebraic reconstruction is the proof evidence.

No payload archives, prior review, or upstream files were modified to save
these reproducing artifacts. This reproduces only the main reviewer's
seeded test; the independent matrix reviewer's numerical testimony has a
separate provenance and is not reproduced by this script.

SHA-256 hashes before this README was written:

| File | SHA-256 |
| --- | --- |
| `upstream_energy_bookkeeping.py` | `9ede04303dfc30bd9ca5c77e023904cdb6733ce2eb69f4a85ae7e0144f919f99` |
| `upstream_energy_bookkeeping_output.txt` | `a5dc46c6126150077482b5e35a92dfcbb81134ff19b549bf5b63dd922d67a011` |
| `upstream_energy_bookkeeping_environment.json` | `258592c84c51f3ce83f3fd02ebf4b4f272d0b0e1c748db4e25999e297573bdfb` |
