# Catalog k=1 replay-safe proof-bundle sample

Date: 2026-07-23 (America/Los_Angeles)

## Certified result and scope

**CERTIFIED, fixed-core scope only.** All 64 preregistered stratified
`(catalog line, deleted vertex)` pairs have complete `CORE2DP2` UNSAT trees
that were independently replayed. Exact sample coverage, artifact hashes,
producer/checker agreement, and status semantics all passed.

This certifies only those 64 induced 41-vertex fixed cores. It leaves 13,712
catalog/deletion pairs uncertified and does not imply global `(5,5;43)`
nonexistence or change any Ramsey bound.

## Replay-safe bundle

The compact `C2DPB001` binary bundle binds:

- its exact record count;
- the catalog SHA-256;
- the ordered pair-list SHA-256;
- each record's catalog line and deletion label; and
- each embedded proof's input order, line, deletion, variable count, and
  independently reconstructed clause count.

The checker is a separate C++ implementation with its own graph6 decoder,
graph validation, clause representation, formula reconstruction, unit
propagation, bundle parser, and exhaustive-tree traversal. It requires exact
pair order, no trailing bytes, and promotes its transcript only after every
proof passes.

Five targeted tests pass. They include deliberate tree corruption, pair-order
corruption, hash-binding corruption, and a bundle-size cap; all invalid
artifacts fail closed.

## Sample measurements

The immutable plan was written before execution:

```text
results/benchmark_plans/core_completion_catalog_k1_proof_bundle_sample_v1.json
SHA-256 e7ec1712ec6a79ea353a6a8867f7014df1d673878f95a1f25fd2eb2c929ae682
```

The selection uses 16 evenly spaced catalog lines and four cyclically shifted
deletion-label quartiles per line.

| measure | value |
|---|---:|
| independently replayed pairs | 64 |
| proof bytes total | 13,004 |
| compact bundle bytes | 13,656 |
| proof bytes minimum / median / mean / maximum | 138 / 210 / 203.1875 / 278 |
| producer internal seconds sum | 0.504401 |
| producer wall seconds | 70.048232 |
| checker wall seconds | 0.600800 |

The producer wall time includes an approximately 69-second process-start
delay. The immutable estimator deliberately scales the observed wall time
with a 4x factor rather than subtracting that delay.

Full-catalog projections fixed by the plan were:

| projection | value |
|---|---:|
| mean bundle | 2,923,703 bytes |
| conservative bundle using sample maximum | 3,954,320 bytes |
| all persistent artifacts, including result JSON | 23,266,120 bytes |
| conservative eight-worker wall | 7,723.602 seconds |

## Stop-rule application

No production bundle was started.

The frozen wall projection exceeds the 1,800-second gate, permitting at most
one whole 41-line/1,722-pair shard if every other gate passed. Disk space then
fell below both the frozen 3 GiB preproduction floor and the requested 2 GiB
absolute reserve: the minimum observed availability was 1,585,292 KiB.
Accordingly, no production pair list was preregistered and no partial
production result is claimed.

The maximum auditable result completed in this track is therefore the
64-pair certified sample. The machine-readable stop record is:

```text
results/core_completion_catalog_k1_proof_bundle_sample_v1/STOP_NO_PRODUCTION.json
```

## Persistent artifacts

| artifact | SHA-256 |
|---|---|
| sample result | `80a05d1b04f7ad3307e7fa12c4495e9995f89e8db89dd6a4f24464f4bb79b544` |
| exact coverage audit | `22caa7c90bf7b2dcf6823bd218d61417d02e1474999dde6acb3a4571817bb9f2` |
| proof bundle | `7c3d41898f437f571e07612e88e84342467fdde82d6dcdfe49bde227659a7c1f` |
| producer transcript | `256401e4d631b19103a62645ce48f72c4ae4dbad5c936a403bc48b24031b10fd` |
| checker transcript | `6ed92503e95b7c42b259d395267bdadd4198ae47043e6bafed2fb4a50fabfbda` |

The exact sample producer/checker binaries and sources are preserved beside
the bundle because the later unexecuted producer revision adds an explicit
bundle-byte cap.
