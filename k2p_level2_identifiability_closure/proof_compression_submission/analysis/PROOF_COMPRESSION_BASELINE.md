# Proof-compression baseline

Status: **PASS**.  This is a read-only measurement of frozen release lock
`fb8a6ef3470cb53518dd485fd98030ce5809695e3f2166dbba553dd86324f703`.  It does not replace or
modify the promoted theorem.

## Proof surface

| Role | Modules | Physical lines | Nonblank/noncomment lines |
|---|---:|---:|---:|
| Primary generation, algebra, and coverage (upper bound) | 61 | 27,943 | 25,211 |
| Explicit independent/adversarial consumers (lower bound) | 13 | 7,144 | 6,412 |
| Mutation code | 25 | 13,162 | 11,884 |
| Release, hash, and orchestration | 13 | 10,142 | 9,577 |
| **Total** | 112 | 58,391 | 53,084 |

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

Payload SHA-256: `d72f69d6163e52bbdbe818278d02a3d9b6c63ab5a453b2718aecdcd7fc63b4b1`.
