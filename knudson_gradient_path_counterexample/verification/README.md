# Exact verification

Requires Python 3.9 or later, standard library only. From the project folder:

```sh
python3 verification/verify.py
python3 verification/independent_check.py
```

Both scripts use explicit exceptions, so their checks remain active with `-O`.
Expected output is in `expected_output.txt` and `independent_output.txt`.

`verify.py` is the supplied program, unchanged. It validates every face before
its coface, reduces the F2 boundary matrix, independently computes H0 pairs
using union-find, constructs the incident matching, checks acyclicity, and
enumerates paths. Its result matches the original supplied output exactly.

`independent_check.py` reconstructs connected components at every filtration
stage by graph traversal, calculates H0 inclusion-map ranks, and
recovers finite barcode intervals by mixed differences. It then independently
reduces signed boundaries over Q and F2, F3, F5, F7, F101, and checks the original
and modified matching paths. It also checks label invariance of the zero-path
obstruction under all 24 vertex permutations. These finite field executions are
checks, not an exhaustive proof over all fields; the signed identities in the
paper provide that proof.

These are tiny exact computations; no randomization, numerical tolerances,
third-party packages, or downloaded data are needed. The short mathematical
proof remains the primary certificate. Neither script is a proof-assistant
formalization or a test of historical priority.
