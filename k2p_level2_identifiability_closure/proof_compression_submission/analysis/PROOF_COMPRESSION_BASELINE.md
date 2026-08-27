# Proof-compression baseline

Status: **PASS**.  This is a read-only measurement of frozen release lock
`30132af1b10f7aba6d49ababf14551f9f914a19dc6a0638517761b6b85cf4c8d`.  It does not replace or
modify the promoted theorem.

## Proof surface

| Role | Modules | Physical lines | Nonblank/noncomment lines |
|---|---:|---:|---:|
| Primary generation, algebra, and coverage (upper bound) | 61 | 27,943 | 25,211 |
| Explicit independent/adversarial consumers (lower bound) | 13 | 7,144 | 6,412 |
| Mutation code | 25 | 13,232 | 11,949 |
| Release, hash, and orchestration | 13 | 10,149 | 9,584 |
| **Total** | 112 | 58,468 | 53,156 |

The classification is deliberately conservative and file-level.  In
particular, cross-layer release validation is not counted as an independent
mathematical hypothesis, and the primary figure is an upper bound.

The recursively locked evidence set contains
405 files and
240 machine-readable evidence files
(476,415,795 bytes).  The promotion
manuscript has 957 lines,
4,940 words, and
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

Payload SHA-256: `6f1be0b46da897b49fc83cff5d3a909f85bd4b1eff4cb07e38a7f978edbdc92f`.
