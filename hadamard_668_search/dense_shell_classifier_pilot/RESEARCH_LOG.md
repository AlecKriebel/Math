# Dense-shell classifier pilot research log

## 24 July 2026: exact bounded stream

- Created a dedicated implementation for the two remaining order-three
  profile shells `(1,15,8)` and `(0,18,6)`.
- Reused the certified ten-letter profile alphabet, 22 exact aggregate
  targets, `F_37/H` geometry, local signed-skeleton equation, and exact
  `C_6 x C_(2,A) x C_(2,B)` action from the prior shell certificates.
- Replaced the dense arithmetic benchmark's synthetic target decoration with
  direct Eisenstein aggregate and correlation equations.
- Implemented deterministic `--skip/--limit` bounded recovery over complete
  canonical decorated skeletons.  Every decoration stabilizer is evaluated
  on all 24 group elements.  Modulo-nine phase assignments are transformed
  under the full action, but the resulting ID-lex coincidence diagnostics
  are not assignment-orbit counts because ID order does not refine decoration
  order.  They are not used scientifically.  The current skip path rescans
  its prefix and is retained only for bounded pilot reproduction.
- Restored medium phases through six exact local primitive-flag tables.  The
  product is streamed without retaining a phase cube.  Added actual affine
  aggregate compatibility modulo `lambda^3`, exact target equality, modulo
  nine, the following lambda digit, modulo 27, and exact-zero gates.
- Recovered the first witness at every attained gate.  Every modulo-nine
  assignment is expanded to two physical length-37 words and replayed
  directly at all lags.  Compact and detached correlations must agree.
- Independently rederived the assignment-level characteristic-two unitary
  test in C++.  The Python verifier calls the tracked
  `char2_profile_quotient.check_eisenstein_profile` API on every emitted
  witness and checks its aggregate and shell support as well as its six
  nonzero correlation coordinates.

## 24 July 2026: pinned census and exact workload

- The first 100 canonical `h=1` decorations contain:

  ```text
  primitive-flag leaves                  7,440,174
  affine aggregate hits                  3,897,234
  exact aggregate hits                     159,116
  characteristic-two hits                       82
  modulo-nine hits                              220
  following-lambda hits                           1
  joint characteristic-two/modulo-nine hits      0
  exact profiles                                  0.
  ```

- The first 10 canonical `h=0` decorations contain:

  ```text
  primitive-flag leaves                  3,188,646
  affine aggregate hits                  3,188,646
  exact aggregate hits                     105,954
  characteristic-two hits                       50
  modulo-nine hits                              141
  following-lambda hits                           1
  joint characteristic-two/modulo-nine hits      0
  exact profiles                                  0.
  ```

- A complete streaming Burnside census, independent of phase restoration,
  gives:

  ```text
  h=1 raw skeletons                 59,743,488
  h=1 raw high-position decorations 537,691,392
  h=1 canonical decorations         22,426,752

  h=0 raw skeletons                 47,730,304
  h=0 raw decorations               47,730,304
  h=0 canonical decorations          1,999,128.
  ```

  The full fixed vectors are pinned in
  `verify_dense_shell_classifier_pilot.py`.  Their sums are exactly 24 times
  the displayed orbit counts.

- The independent verifier pins both bounded censuses, splits the first 100
  `h=1` decorations into resumable `0+40` and `40+60` shards, independently
  replays eight emitted witnesses on all 37 positions, calls the tracked
  characteristic-two API, and reruns both complete Burnside counts.

## 24 July 2026: corrected workload projection

- Three optimized repetitions gave median raw-equivalent primitive-leaf
  rates, weighted by the actual decoration orbit size, of:

  ```text
  h=1: 393,328,180 primitive leaves/s/core,
  h=0: 499,390,832 primitive leaves/s/core.
  ```

- Audit retracted the earlier 25.20-core-hour projection.  Its
  `23,926,488,518,016` numerator counted one aggregate right-hand side per
  skeleton, while the implemented affine predicate accepts the union of up
  to three target residue classes.  Observed affine hits can therefore
  exceed the alleged bound; it was not a valid runtime numerator.

- An independent exact dynamic program over
  `(quartet,n,r,alpha,beta)` pins the residue-stratified union bounds:

  ```text
  h=1: 30,006,842,465,088,
  h=0: 17,848,209,316,608,
  total: 47,855,051,781,696.
  ```

- The enumerator scans primitive-compatible leaves before applying the
  affine union.  The corresponding exact workload upper bounds are:

  ```text
  h=1: 45,036,129,993,984,
  h=0: 26,743,335,560,064,
  total: 71,779,465,554,048.
  ```

  Dividing these by the pinned primitive-leaf rates gives 31.806 and
  14.876 core-hours, or 46.681 core-hours combined.  This uses measured
  stabilizer weights, not a naive division by 24.  It remains a
  small-early-shard rate projection, not a production runtime measurement.

- The actual characteristic-two/modulo-nine intersection is empty in the
  pinned sample.  The earlier neutral planning figures `622,743` and `3,304`
  used the retracted one-right-hand-side workload and are superseded.  They
  are not replaced because neutrality between the algebraic gates is
  unproved; production will measure the intersection directly.

- The direct enumerator therefore remains computationally plausible.  The
  729-character self-reduction kernel remains a fallback if production
  timings materially exceed the corrected projection.

## 24 July 2026: production-resumable classifier

- Added 729 deterministic prefix shards per shell by fixing the first two
  legal local-state indices before canonicalization and phase restoration.
  This is a disjoint partition with no skip-prefix rescanning.
- Added `--complete-shard`.  It rejects skip/limit combinations and emits
  `shard_complete=1` only after exhaustive traversal.  Production upper
  exact correlations are evaluated only on `char2 && mod9`; this remains
  exhaustive for exact zero, and its counter scope is explicit in output.
- Any exact-zero assignment is canonicalized, detached-replayed, emitted,
  and stops the shard with `shard_complete=0` and candidate status.  It
  cannot be mislabeled as a complete exclusion.
- Added an exact partition audit.  Its 729-cell sums reproduce both raw
  skeleton totals and both raw decoration totals.  The pinned Burnside fixed
  vectors independently reproduce the canonical totals.
- Added a local runner that compiles once, pins source/binary/compiler/flag
  hashes and exact commands, runs only missing shards, writes results
  atomically, orders work by descending raw-decoration count, and cleans up
  every active child on interruption or validation error.
- Darwin `RLIMIT_AS` was tested and rejected because it prevents child
  startup at otherwise ample limits.  The production runner instead permits
  at most eight children and polls aggregate child RSS, stopping the pool
  above 3,072 MiB—below the 4 GiB workstream budget and far below the
  machine's 16 GiB physical RAM.
- Added a strict aggregator.  It rejects missing, extra, duplicate,
  hash-mismatched, command-mismatched, or census-mismatched results; sums
  counters with arbitrary-precision integers; verifies that orbit-weighted
  decorations recover the raw totals; and independently replays every
  retained joint witness.
- Only the infeasible, zero-work `h0` prefix `(13,13)` was used for the
  production smoke.  No nontrivial complete prefix and no full-shell run was
  launched.

## Validation

- Warning-clean optimized build with `-Werror`: PASS.
- AddressSanitizer and UndefinedBehaviorSanitizer on both pinned shards:
  PASS.
- Python 3.14 verifier and regression test: PASS.
- System Python 3.9 verifier and regression test: PASS.
- Production partition/runner/strict-incomplete-aggregate regression tests:
  PASS.
- Standalone optimized C++ maximum resident memory: approximately 1.5 MB.
- Full Python verification, including compilation and both Burnside
  censuses: approximately 11 seconds and below 170 MB.
- No external communication, commit, push, or unrelated scratch mutation
  occurred.
