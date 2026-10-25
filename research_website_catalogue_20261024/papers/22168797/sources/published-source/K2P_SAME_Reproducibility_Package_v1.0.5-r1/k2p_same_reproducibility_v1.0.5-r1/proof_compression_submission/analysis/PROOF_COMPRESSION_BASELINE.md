# Proof-compression baseline

Status: **PASS**.  This is a read-only measurement of frozen release lock
`bbb411dde4a13f001d9c2b5fac97722a54bb6ce604b6aff476de44f7ce4b8f53`.  It does not replace or
modify the promoted theorem.

## Proof surface

| Role | Modules | Physical lines | Nonblank/noncomment lines |
|---|---:|---:|---:|
| Primary generation, algebra, and coverage (upper bound) | 63 | 29,045 | 26,170 |
| Explicit independent/adversarial consumers (lower bound) | 13 | 7,258 | 6,510 |
| Mutation code | 25 | 13,536 | 12,207 |
| Release, hash, and orchestration | 13 | 10,227 | 9,643 |
| **Total** | 114 | 60,066 | 54,530 |

The classification is deliberately conservative and file-level.  In
particular, cross-layer release validation is not counted as an independent
mathematical hypothesis, and the primary figure is an upper bound.

The recursively locked evidence set contains
407 files and
240 machine-readable evidence files
(476,418,048 bytes).  The promotion
manuscript has 960 lines,
4,972 words, and
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

Payload SHA-256: `a2f858d5b09ed15e098605a169bbd37aad83243a8d49cef07d681a03a8c6588b`.
