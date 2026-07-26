# Order-12, parameter-four DoubleLex proof package

## Status and claim boundary

Status:
`UNSAT_LRAT_VERIFIED_PENDING_INDEPENDENT_HOSTILE_REVIEW`.

This package records a complete proof-checking chain for one exact formula:

```text
instances/order12_k4_connected_doublelex/instance.cnf
SHA-256 14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7
18,381 variables; 115,507 clauses; 1,190,774 literal occurrences
```

The package is not yet a campaign claim. A separate hostile reviewer must
rehash the frozen inputs, rerun the LRAT proof from a private copy, audit the
pipeline records, and accept the exact certificate. It does not by itself
resolve the universal γ–θ conjecture.

The mathematical transfer from this strengthened formula to the exact
anchored parent is supplied by the independently hostile-accepted DoubleLex
theorem:

```text
math/lemmas/order12_k4_doublelex.md
SHA-256 d5be9b6373d7aa7c49dec32c18c6202698b35fe05a1f58b2b97dcc98d9114a76
```

The exact theorem, generator, tests, formula manifest, hostile review, and
hostile probe are all hash-bound in `certificate.json` and
`artifact-manifest.json`.

```text
certificate.json
SHA-256 a21bd3db71fb271965859237d7665c5d0c38d32d061fdf3eda285c014e366991

artifact-manifest.json
SHA-256 846a646ba951569f50a76b562fdc8ec005dcf0f06ff57e48b4e3d4d330fbd607
```

## Decisive proof chain

The frozen solver artifacts are:

```text
results/order12_k4_doublelex_seed0/solver.result
SHA-256 bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162
exact contents: s UNSATISFIABLE

results/order12_k4_doublelex_seed0/proof.raw.bdrat
SHA-256 ed3975c5f0cfbe9475c607e440c0ddc012722d0fe68b797e693149fd6f7d5c51
32,987,136 bytes
```

No SAT solver was rerun. The raw binary DRAT stream was instead subjected to
the following fail-closed chain:

1. The pinned strict normalizer parsed the complete binary stream, required
   canonical varints, enforced the declared variable bound, required exactly
   one empty addition, rejected additions after the empty clause, and removed
   every deletion.
2. Pinned `drat-trim` checked the normalized stream in binary, forward,
   warning-fatal, RUP-only mode with `-i -f -W -U`.
3. A separate pinned `drat-trim` process checked the same stream backward in
   warning-fatal, RUP-only mode and emitted LRAT with `-i -W -U -L`.
4. The separately pinned `lrat-check` executable freshly replayed the LRAT
   file against the exact frozen formula.

All four children exited 0, emitted empty stderr, stayed below their wall,
memory, and file limits, and recorded exact executable, command, stdout, and
stderr hashes. The decisive outputs are:

```text
proof/proof.normalized.rup.bdrat
SHA-256 2741335a5ed9af769f0db4bd0c03a70e414d0568681d5b8261a5667ed30b6686
15,783,377 bytes

proof/proof.converted.lrat
SHA-256 0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263
228,381,671 bytes
```

The normalization report records:

- 1,378,975 total binary records;
- 640,854 additions;
- 738,121 deletions;
- one empty addition at final record 1,378,975;
- no post-empty deletion record;
- maximum observed variable 18,381.

The decisive checker outputs report:

```text
normalized forward: s VERIFIED; 0 RAT lemmas
backward conversion: s VERIFIED; 0 RAT lemmas
fresh LRAT replay: c VERIFIED
```

The full exact records are in `logs/`, `resources/`,
`proof/normalization-report.json`, `artifact-manifest.json`, and
`certificate.json`.

## Resource record

Each child was run under the campaign-wide heavy-child lock with:

- 3,600 seconds wall limit;
- 2,048 MiB memory limit;
- 2,048 MiB file-size limit;
- an 8 GiB free-disk reserve gate.

Observed wall time and maximum resident memory were:

| phase | wall seconds | maximum RSS MiB |
|---|---:|---:|
| strict normalization | 17.532 | 27.422 |
| normalized forward RUP | 435.571 | 129.359 |
| backward RUP/LRAT conversion | 205.258 | 278.688 |
| fresh LRAT replay | 3.393 | 47.656 |

No frozen formula, theorem, source, test, review, solver result, raw proof, or
production-run artifact was modified. The producer rehashed all frozen inputs
after the final replay and required byte-for-byte agreement with their
pre-run bindings.

## Preserved failed attempts

Two nonclaiming failed attempts are preserved, hash-bound by the artifact
manifest, and explicitly excluded from the decisive chain:

- `failed-attempt-000000`: the strict normalizer rejected an output/report
  directory-layout mistake before parsing;
- `failed-attempt-000001`: normalization succeeded, but an unnecessary
  raw-stream forward diagnostic exited 80 on the deletion-bearing stream.

The second attempt motivated the correct distinction: the decisive forward
check is performed on the strictly parsed, addition-only normalized stream,
not on the original deletion-bearing stream.

## Required hostile review

Before elevating this package to a certified finite result, a reviewer should:

1. verify every frozen input and decisive output hash;
2. independently census the exact DIMACS formula;
3. inspect the strict normalization report and full binary-stream policy;
4. verify the exact `-i -f -W -U` and `-i -W -U -L` commands and clean
   resource records;
5. rerun pinned `lrat-check` against private copies of the exact formula and
   LRAT proof;
6. confirm the generator and DoubleLex theorem hashes match their accepted
   hostile review;
7. confirm that no CaDiCaL or other SAT solver was invoked during
   certification; and
8. keep the result labeled pending until that review is recorded.
