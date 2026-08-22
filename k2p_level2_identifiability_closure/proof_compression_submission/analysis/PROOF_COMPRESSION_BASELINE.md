# Proof-compression baseline

Status: **PASS**.  This is a read-only measurement of frozen release lock
`0c17eeaa3344f0982998ea694c1eb92f72f5ced0841e2acad0d39566e2ec71c3`.  It does not replace or
modify the promoted theorem.

## Proof surface

| Role | Modules | Physical lines | Nonblank/noncomment lines |
|---|---:|---:|---:|
| Primary generation, algebra, and coverage (upper bound) | 54 | 23,896 | 21,544 |
| Explicit independent/adversarial consumers (lower bound) | 11 | 6,317 | 5,675 |
| Mutation code | 17 | 4,506 | 3,819 |
| Release, hash, and orchestration | 13 | 7,567 | 7,055 |
| **Total** | 95 | 42,286 | 38,093 |

The classification is deliberately conservative and file-level.  In
particular, cross-layer release validation is not counted as an independent
mathematical hypothesis, and the primary figure is an upper bound.

The recursively locked evidence set contains
369 files and
226 machine-readable evidence files
(432,456,552 bytes).  The promotion
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

Payload SHA-256: `9a467e69fe97ee0f155429430d3848ce7b983f81c5ed426cd6506ad29c9d2347`.
