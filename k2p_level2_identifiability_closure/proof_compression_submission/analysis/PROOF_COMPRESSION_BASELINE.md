# Proof-compression baseline

Status: **PASS**.  This is a read-only measurement of frozen release lock
`8456344d649641eb1622f474e8144ef4193bbfa87e2c5fea14e6dafb15e6f0a6`.  It does not replace or
modify the promoted theorem.

## Proof surface

| Role | Modules | Physical lines | Nonblank/noncomment lines |
|---|---:|---:|---:|
| Primary generation, algebra, and coverage (upper bound) | 60 | 27,547 | 24,852 |
| Explicit independent/adversarial consumers (lower bound) | 13 | 6,781 | 6,071 |
| Mutation code | 24 | 7,148 | 6,210 |
| Release, hash, and orchestration | 13 | 8,478 | 7,942 |
| **Total** | 110 | 49,954 | 45,075 |

The classification is deliberately conservative and file-level.  In
particular, cross-layer release validation is not counted as an independent
mathematical hypothesis, and the primary figure is an upper bound.

The recursively locked evidence set contains
402 files and
239 machine-readable evidence files
(476,313,915 bytes).  The promotion
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

Payload SHA-256: `cac8186363802b68c419874eb67543699dc3f71345228c068f89a31bd74de674`.
