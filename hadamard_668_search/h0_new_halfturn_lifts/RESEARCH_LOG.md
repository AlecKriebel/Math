# Research log

## 2026-07-24 19:31 PDT

- Consumed the final strict aggregate: 729 completed `h=0` shards and 18
  distinct exact canonical profile orbits.
- Added automatic all-37 replay and stabilizer discovery rather than
  extending a hard-coded profile list.  Exactly six profiles are fixed by
  the class half-turn; all have stabilizer `{0,12}`, orbit size 12, and
  first-lift split `36=21+15`.
- Identified two half-turn profiles absent from the v1 certificate:
  `0x86b13a0388d98a5e` and `0xaa1c4c148acc5b86`.
- Their anti codes are `[27,15,4]`.  Their first two positive shells have
  sizes `8,6` and `2,6`, respectively.
- Exhausted all 22 new signed slices, producing 752 exact digit-two points.
  None reaches any of the 96 row-margin fibers or full digit three; the best
  digit-three defect is seven.
- Froze `final_certificate_v2.json` with explicit nonoverlapping coverage
  classes: original baseline, prior three-profile v1, and two-new final
  extension.  Combined totals are six profiles, 244 signed words, 242
  consistent slices, and 7,178 digit-two points, with zero row-margin and
  zero full digit-three points.
- Lightweight final catalog/artifact-chain verifier passed with semantic
  hash `9745f32ab864df7c34de70fab72da9002c173d2d84dab8443189c662037bac86`.
- Prepared but did not launch the one-core `--full-extension` replay while
  the independent eight-worker Eliahou census is active.

## 2026-07-24 19:01 PDT

- Pinned the three exact half-turn profiles emitted by completed production
  shard `h0-p00-p02`.
- Certified that all three first placement lifts have the same
  `36=21+15` half-turn eigenspace split.
- Exhausted each natural ternary `[27,15]` antisymmetric code.  The priority
  digest `0xfdb6a5c865468e1f` is structurally different from the other two:
  it has minimum distance five, rather than four.
- Exhausted both lowest positive anti-weight shells for every profile:
  202 signed anti words and 200 consistent symmetric slices in total.
- Replayed 5,768 exact digit-two points.  None lies in an exact row-margin
  fiber and none reaches digit three.  The global best digit-three defect is
  six, attained in the priority profile's weight-six shell.
- Added a compact certificate and a detached verifier.  The verifier also
  checks every full anti-code weight enumerator independently through the
  ternary MacWilliams transform of the enumerated dual code.
- Honest boundary: only two local anti shells per profile are excluded.  No
  Legendre pair or Hadamard matrix of order 668 was found.
