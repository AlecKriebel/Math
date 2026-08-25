# Proof-compression baseline

Status: **PASS**.  This is a read-only measurement of frozen release lock
`bc690c3e68a3a9d66960239ebf60a63f96da63ee5312cd2f0e8bf16d707d3ac9`.  It does not replace or
modify the promoted theorem.

## Proof surface

| Role | Modules | Physical lines | Nonblank/noncomment lines |
|---|---:|---:|---:|
| Primary generation, algebra, and coverage (upper bound) | 59 | 27,071 | 24,408 |
| Explicit independent/adversarial consumers (lower bound) | 13 | 6,775 | 6,065 |
| Mutation code | 21 | 5,521 | 4,711 |
| Release, hash, and orchestration | 13 | 8,322 | 7,786 |
| **Total** | 106 | 47,689 | 42,970 |

The classification is deliberately conservative and file-level.  In
particular, cross-layer release validation is not counted as an independent
mathematical hypothesis, and the primary figure is an upper bound.

The recursively locked evidence set contains
398 files and
239 machine-readable evidence files
(476,289,919 bytes).  The promotion
manuscript has 937 lines,
4,801 words, and
18 named lemmas or
theorems.

## Finite theorem surface

| Layer | Exact census |
|---|---:|
| Four-port raw directions | 405,216 |
| Four-port terminal presentations / canonical terminal classes | 1,472 / 934 |
| Four-port restoration presentations / canonical parents | 2,540 / 997 |
| Theta2 raw directions | 2,946,240 |
| Restoration first / second children | 36,568 / 256 |
| Restoration final leaves | 36,792 |
| Probe anchors / canonical anchor classes | 176 / 39 |
| Probe one-port / two-port rows | 29,964 / 544,571 |

Every authoritative sign row is classified by an original-full-map
`T_i` certificate.  Historical rooted `tree_sunlet` reasons are excluded
from this compression surface.

## Timing boundary

The frozen deterministic payload does not record an end-to-end quick or full
runtime.  This baseline therefore does not invent one from noncomparable
component timings.  Runtime benchmarking belongs in a separate operational
record.

Payload SHA-256: `19e1b3e455334ff43a557a09145c34432c662c7438e1bd6ef3bef462ebf4c7c9`.
