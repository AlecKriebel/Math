# Research log

## 2026-07-24 PDT

- Selected `h0-p01-p13` as a bounded, positive-work production prefix.  It
  has one unsigned support, 1,296 legal signed skeletons, 42 canonical
  decorations, and raw-equivalent orbit weight 600.
- Completed the unmodified prefix in 2.615347 seconds.  It performed
  554,008 detached all-37-lag replays despite having zero
  characteristic-two/modulo-nine intersections.
- Located the cause: the bounded diagnostic witness-recovery fallback
  remained active in complete-production mode, but production deliberately
  never stores those marginal witnesses.  Restricted the fallback to
  bounded mode.  The same complete prefix now performs zero detached
  replays and completes in 0.771325 seconds with all lower counters
  unchanged.
- Added a regression pinning the complete nontrivial prefix and its exact
  replay scope.
- Built a connected C++ oracle around a real canonical skeleton and target.
  Exhaustive exact correlations over its `3^12=531,441` affine points agree
  with all 729 factorized character sums and their complete inverse
  transform.
- Counted 729 modulo-nine points, 34 that also have the exact selected
  aggregate, and one that passes the following lambda digit.  Recovered
  digest `0xc8ac157d026d3025` and replayed all 37 physical lags.
- The recovered point is not an exact profile and fails the independent
  characteristic-two gate.  It is not a physical placement, a Legendre
  pair, or `H(668)`.
- Found that 459 of 864 restricted polar entries differ between the actual
  production modulo-nine family and the older synthetic-target benchmark
  family.  Narrowed the old throughput claim accordingly.
- Three runs of 11,943,936 evaluations on the actual fitted representative
  family gave a median 15,641,863 characters/second/core.
- The corrected representative-prefix direct-stream rate projects the
  rigorous combined primitive-leaf upper bound to 53.59 single-core hours.
  This is a one-cell extrapolation, not a runtime certificate.
- No commit, push, or external communication was performed.

## 2026-07-24 PDT: v2 enumeration replay

- The exhaustive classifier upgrade changed the source hash, so the audit
  failed closed instead of silently applying the v1 timing certificate to
  new code.
- Replayed the exact v2 source with
  `--complete-shard --enumerate-exact-orbits` on the same prefix in five
  trials. Median wall time is 0.744369 seconds and the median
  raw-equivalent rate is 385,532,181 primitive leaves/second/core.
- The current one-cell projection is 51.72 single-core hours combined, or
  5.17 hours under ideal ten-core scaling. Maximum measured RSS was
  1,540,096 bytes.
- Preserved all historical v1 measurements, added separate v2 source and
  binary hashes, bumped the benchmark schema, and made the verifier require
  the v2 enumeration mode and shard schema.
