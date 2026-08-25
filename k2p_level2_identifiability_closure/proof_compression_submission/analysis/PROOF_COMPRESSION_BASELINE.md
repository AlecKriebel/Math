# Proof-compression baseline

Status: **PASS**.  This is a read-only measurement of frozen release lock
`7113b1c52d577858ec20ef83cd87c870242c8ddc96018036b5c073229821eec9`.  It does not replace or
modify the promoted theorem.

## Proof surface

| Role | Modules | Physical lines | Nonblank/noncomment lines |
|---|---:|---:|---:|
| Primary generation, algebra, and coverage (upper bound) | 59 | 27,291 | 24,612 |
| Explicit independent/adversarial consumers (lower bound) | 13 | 6,781 | 6,071 |
| Mutation code | 21 | 5,545 | 4,731 |
| Release, hash, and orchestration | 13 | 8,322 | 7,786 |
| **Total** | 106 | 47,939 | 43,200 |

The classification is deliberately conservative and file-level.  In
particular, cross-layer release validation is not counted as an independent
mathematical hypothesis, and the primary figure is an upper bound.

The recursively locked evidence set contains
398 files and
239 machine-readable evidence files
(476,289,997 bytes).  The promotion
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

Payload SHA-256: `8944cc91a0d70f42a60ad04becdb7311c76875ec51e956d0856fa747ef650150`.
