# Certified full Hamming-ball exclusion through radius nine

Date: 2026-07-23 (America/Los_Angeles)

## Result

**CERTIFIED UNSAT, LOCAL SCOPE.** There is no Ramsey(5,5;43) graph at
labeled edge-Hamming distance at most 9 from
`results/best_candidates/core_kick_seed_20260731.g6` (SHA-256
`64d2362eb9fac1ed2bf387578e92f3fc3bbdbe6655b38fa65329f737ee40bff6`).
Consequently, any valid labeled order-43 graph differs from this candidate
in at least 10 of the 903 edge positions.

This is not a global nonexistence theorem and does not change the public
bound \(43\le R(5,5)\le46\).

## Formula and independent reconstruction

The exact radius-nine formula has:

- 903 primary edge variables;
- 8,985 sequential-counter auxiliary variables;
- 9,888 variables in total;
- 1,925,196 Ramsey clauses;
- 17,961 Hamming-counter clauses; and
- 1,943,157 clauses in total.

CNF SHA-256:
`68f1b6dc8713d3bf303b5d07a57327b7536ef72fc943af381ead995049239896`.
The independent checker reconstructed every expected Ramsey and counter
clause and reported zero missing clauses, `valid: true`. Its result SHA-256
is
`776afcd3d539d1927e49e20c83691501e1f28bcfb0e01ee1e89ec4345b408993`.

## Checked proof

Pinned Glucose3 returned UNSAT after 760,743 conflicts and 140.080 solver
CPU seconds. The raw DRAT has SHA-256
`ef375d06a9e4497c7b45d9bf8f71b07e96349d6609fdfe0f74775ddc8543fc90`.

`drat-trim` accepted the proof and generated a 2,441,593,384-byte LRAT
stream. That exact stream has SHA-256
`b72d222fb62e5c523e80c874a3e434815e1c8a66f4f736a92ce55c94d9d52a86`;
`lrat-check` replayed it and returned `VERIFIED`. The streaming pipeline
retained the LRAT only as a 519,855,968-byte Zstandard archive, avoiding an
uncompressed multi-gigabyte file.

Solver-result SHA-256:
`f9db1488a3c72f6e62cea2be89074cc05091208f5e0c57f6d939a7bcf335be7b`.

## Lossless archival

The CNF, DRAT, and LRAT archives all passed `zstd -t`. Streaming
decompression reproduced the exact uncompressed byte counts and SHA-256
values recorded by the generator and proof pipeline. Archive identities and
all checks are bound in
`certificates/core_kick_full_hamming_radius9.archive.json`.

The raw CNF and DRAT are therefore exactly recoverable and need not be
retained alongside their archives.
