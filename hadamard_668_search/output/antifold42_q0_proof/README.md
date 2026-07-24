# Certified anti-fold support exclusion: long `q=0`

This directory contains a checked UNSAT certificate for one of the 30
orientation-free anti-fold support instances at special distance 41.

The claim is deliberately narrow:

```text
Eliahou seed
+ special-distance-41 repair shell
+ long reciprocal q pair with representative 0
+ arbitrary support and endpoint profile
=> no solution of the anti-fold equations.
```

It does **not** exclude the other 29 anti-fold support instances, all
distance-41 repairs, `BS(84,83)`, or a Hadamard matrix of order 668.

## Artifacts

```text
antifold_00.cnf
    39,580 variables, 127,589 clauses
    SHA-256 f3eb29b1ea9c386e53b03726349fe0c38577d7e187b56aa19f86412c8749755d

antifold_00.drat.zst
    binary DRAT, compressed with zstd
    90,490,737 bytes
    SHA-256 efd8abd9d80d50365822754f36345f368d7cff8f2740ca33b9cab7d5866aa519

decompressed DRAT
    276,262,081 bytes
    SHA-256 7ab546776c7b0c199d524a952f51015a045c4aa7433b8eaa78d471e34129a374
```

The formula includes modulo-two and modulo-four Hensel chains that are
redundant consequences of the exact integer anti-fold equations.  Therefore
UNSAT of this formula excludes the underlying support problem; it does not
depend on either adjacent-fold root profile.

`certificate.json` records the solver and checker transcript statistics.
`verify_eliahou_antifold_q0_proof.py` checks the artifact hashes, dimensions,
and metadata with the Python standard library.

## Full proof replay

The compressed proof must first be decompressed to a **regular file**.
`drat-trim` did not reliably consume this binary proof through a FIFO or
process-substitution stream.

From the repository's `hadamard_668_search` directory:

```sh
python3 verify_eliahou_antifold_q0_proof.py \
  --full \
  --drat-trim /absolute/path/to/drat-trim
```

The verifier uses `zstd`, creates a temporary regular proof file, checks its
uncompressed size and hash, runs `drat-trim`, and removes the temporary file.
The original replay completed with:

```text
s VERIFIED
75.00 seconds
471.1 MB peak resident memory
824,251 / 4,451,261 lemmas in the core
73,135,509 resolution steps
0 RAT lemmas
```

An earlier proof trace captured through a Python solver wrapper failed
independent replay and was removed.  It is not part of this certificate.
