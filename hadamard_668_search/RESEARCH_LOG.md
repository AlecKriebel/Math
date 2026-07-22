# Hadamard 668 research log

## 21 July 2026: exact seed recovery and fixed-q reduction

- Recovered Eliahou's length-167 sequences from the published run-length code
  and independently checked all 166 aperiodic correlation sums.
- Reconstructed the full Goethals-Seidel array and checked its row-dot-product
  distribution using only Python integer bit operations.
- Verified the 13 residual lags
  `4,8,12,16,26,30,34,38,42,46,50,54,58` with values
  `-512,384,-256,128,-64,128,-192,256,-320,256,-192,128,-64`.
- Derived the fixed-q identity

  ```text
  F_k = 4 sum_{i: same half, q_i=q_{i+k}} s_i s_{i+k}.
  ```

- For `q=(83,2,81,1)`, decomposed the active variables into `X` of length 83
  and `Y` of length 81.  The exact constraints are

  ```text
  c_k(X)+c_k(Y)=0                (1 <= k <= 80),
  x_0*x_81+x_1*x_82=0           (k=81),
  x_0*x_82+u*v=0                (k=82).
  ```

  The remaining coordinate is isolated.
- Evaluation at `+1` and `-1`, together with odd-square congruences modulo 8,
  forces `x_0*x_82=-1`, `u*v=+1`, and ordinary and alternating sums of both
  `X` and `Y` to have absolute value 9.  These invariants are included in the
  initial CP-SAT model.
- Corrected an initially over-strong symmetry break: after fixing `sum(Y)=9`,
  one cannot also assume `y_0=+1` when both endpoints of a representative are
  negative.  The model now retains both endpoint-sign classes.
- Added exact spectral propagation at primitive roots of orders 3, 4, and 6,
  where the Laurent identity reduces to quadratic integer norm equations with
  right sides 165, 166, and 165.  Added full lexicographic symmetry breaking
  against negated reversal of `X` and reversal of `Y`.
- Added an independent CNF/PySAT encoding using XNOR product literals, exact
  cardinality networks, gated alternating-sum cases, and the same safe
  involutive symmetry quotient.  Any model is rechecked from the original
  integer autocorrelation definition before being written.
- Sharpened the alternating-sum invariant: after normalizing both ordinary
  sums to `+9`, residue-block parity forces `alt(X)=-9` and `alt(Y)=+9`.
  Removed the now-unnecessary disjunction from both exact models.

## 21 July 2026: fixed-q lane closed by a Turyn obstruction

- Let `P_k` be the product of all individual terms in
  `c_k(X)+c_k(Y)`.  Exact zero correlation at lags 1 through 81 forces
  `P_k=(-1)^k`.  Telescoping consecutive products forces

  ```text
  x_(82-i)=(-1)^(i+1) x_i,
  y_(80-i)=(-1)^i y_i.
  ```

- Even/odd decimation then maps every hypothetical exact fixed-q repair to
  `(E;B;O;P) in BS(42,41)`, where `E` is skew and `O` is symmetric.  This is
  exactly a Turyn sequence in `TU(41)`.
- The standard Turyn necessary condition rules out `TU(41)` because
  `2*41+1=83` is not a sum of two squares.  The published exhaustive
  classification through long length 42 independently gives the same result.
- Added `FIXED_Q_OBSTRUCTION.md` and a pure-Python checker which verifies the
  fixed-q edge structure, product telescope, forced reversal signs, symbolic
  decimation identity, and the two-squares arithmetic.  The only imported
  fact is the cited Turyn necessary-condition theorem.
- Consequence: further SAT or local search with Eliahou's exact `q` is wasted
  computation.  This closes only that subfamily; it does not settle order 668.

## 21 July 2026: fixed-compression LP(333) model

- Implemented the factor-9 compression proposed for `p=37`, `q=3`: 74 exact
  CRT-column margins on two binary sequences of length 333.
- Encoded all 166 independent Legendre-pair equations with 110,556 native XOR
  definitions and exact cardinalities.
- Added dependency-free candidate verification, model-construction checks,
  safe shift/inversion symmetry modes, and arithmetic/encoding tests.
- Added the exact 504-case factor-111/modulo-3 compression table, the
  factor-37/modulo-9 PAF equations, and sharp per-lag distance bounds from the
  fixed 9-bit column weights.  Cyclic distances are exposed as even
  half-distances.  Per-cycle parity is available experimentally but was slower
  in short matched benchmarks, so it is not the default.
- Added a C++ margin-preserving local engine with exact incremental PAF
  residuals.  A 94.6-million-move diagnostic run reached half-PAF energy 1608
  with 126 of 166 bad lags; the independent verifier correctly rejected it.
- Added the bordered two-circulant construction and exact full-matrix checker.
- No candidate has yet been found.  The fixed compression is a motivated
  restriction, not a necessary condition for every `LP(333)`.

## 21 July 2026: exact multiplier sublane

- Imposed common order-three multiplier invariance.  The four compatible
  subgroups have representatives `10,112,121,211`.
- For representatives 121 and 211, the model has 113 sign orbits and only 56
  representative lag equations.  Reusing XOR literals by orbit pair reduces
  the exact model from roughly 111,000 to roughly 13,000 variables before
  optional symmetry breaking.
- Ruled out the subgroup `<112>={1,112,223}` exactly.  At lag 111 invariance
  permits at most 111 disagreements, while the fixed column weights require
  at least 112 in each sequence.
- Short exact searches of the other three subgroups returned `UNKNOWN`; no
  candidate was emitted.

## 21 July 2026: further exact LP(333) constraints

- Added the missing factor-3 compression to length 111.  Its two compressed
  PAFs have combined values 662 at lag zero and -6 at every nonzero lag.
  The zero-lag equation is the exact cardinality statement that 55 of the 222
  source triples are monochromatic.  CP-SAT exposes this through 222 tiny
  truth tables; a `full` experimental mode also adds all 55 nonzero PAF
  equations.  Matched short trials showed negligible overhead but no clear
  search gain, so the option remains off by default.
- Repeated the matched comparison with one worker, random seed 668, default
  dihedral symmetry, and a 10-second solver limit.  The `off`, `energy`, and
  `full` modes all returned `UNKNOWN`, with respectively 612,287, 626,498,
  and 571,036 branches.  This short noisy result does not establish a winner.
- Ruled out every `LP(333)` subfamily in which each sequence is symmetric or
  normalized skew under inversion.  Modulo-3 compression reduces the
  symmetric/symmetric, skew/skew, and mixed cases respectively to
  `x^2+y^2=668`, `x^2+y^2=222`, and `x^2+3y^2=667`, none of which has an
  integer solution.  A standard-library checker exhausts all 28,224
  admissible compressed cases.  This result does not assume the fixed
  factor-9 seed.
- Checked whether the pairwise fixed-column distance bounds conceal global
  cyclic consistency constraints.  An exact width-9 transfer DP, including
  the closing row twist, exhausts all 324 nonzero-column-offset sequence/lag
  cases.  A separate exact bitset sum covers the eight column-preserving
  cases, for 332 cases in total.  Every attainable spectrum is the full even
  interval between the existing endpoints, so the live bounds are globally
  sharp and no extra distance pruning exists at this level.

## 21 July 2026: variable-q reduction to BS(84,83)

- Proved and checked a bijection between joint `(s,q)` special quadruples and
  base sequences `(A;B;C;D) in BS(84,83)`:

  ```text
  A=s[:84], B=(s*q)[:84], C=s[84:], D=(s*q)[84:].
  ```

- Enumerated 12 canonical ordinary-sum profiles and 288 exhaustive compatible
  ordinary/alternating margin shards.
- Added a sharded CP-SAT model with 334 primary signs, 83 exact aperiodic
  correlation equations, root-of-unity norm propagation, and an endpoint
  product telescope encoded by 83 sparse XOR constraints.
- Added an independent candidate verifier that reconstructs `(s,q)`, checks
  the special Golay quadruple, expands the Goethals-Seidel array, and verifies
  all row products of the full order-668 matrix.
- Implemented a margin-preserving local engine with exact incremental
  aperiodic correlations.  Its unrestricted diagnostic reached half-energy
  156.  A second mode generates and preserves all 83 endpoint XORs using
  equal-syndrome paired swaps and zero-syndrome single swaps; its then-tracked
  shard-235 checkpoint had half-energy 232, 43 bad lags, and no odd residual.
  Both checkpoints were independently rejected as nonexact.
- Implemented the factor-14 four-sequence PAF signature join and exhaustively
  ran all 288 shards.  No shard is eliminated; each has 378--392 matching
  pair sums.  Fourier inversion shows that this compression exactly
  repackages the existing ordinary/alternating margin and primitive root-3
  and root-6 constraints.  At that stage the next unimplemented small
  compression had length seven.
- Fixed continuation semantics in the local engine so an unperturbed initial
  checkpoint can never be discarded by a shorter, worse run.  Strict-warning
  compilation, address/undefined sanitizers, per-move full validation, and
  independent Python correlation checks all pass.

## 22 July 2026: variable-q symmetries and stronger propagation

- Added the exact global coordinate-alternation equivalence
  `x_i -> (-1)^i x_i`.  It sends `R_k` to `(-1)^k R_k`, swaps ordinary and
  alternating margins, pairs 264 nominal shards into 132 two-cycles, and fixes
  24 shards.  The exact and local schedulers now search 156 representatives by
  default; fixed shards receive an internal lexicographic quotient.
- Canonicalized the parity-feasible shard-235 checkpoint to its representative
  shard 213.  `output/variable_q_parity_best_canonical.json` has ordinary
  margins `(14,4,11,1)`, alternating margins `(14,8,5,7)`, half-energy 232,
  43 bad lags, and no odd half-residual.  It remains nonexact and is rejected
  by the independent verifier.  At this snapshot its SHA-256 is
  `9c5e69534abd8db1abf69e493dbfb7640e2457b594c3a83a5c9dd0e45d39417f`.
- Replaced the default endpoint-product encoding by the equivalent standard
  base-sequence quad basis: 42 four-literal products for `(A,B)` and 41 for
  `(C,D)`.  The targets are `(-1,+1,...,+1)` and `(+1,...,+1)` respectively.
  The CP model retains `quad`, `endpoint`, and `both` modes; these are
  propagation alternatives, not different mathematical subfamilies.
- Implemented the factor-12 compression to length seven.  Twelve explicit
  compressed PAF witnesses cover the 12 ordinary profiles and lift to all 288
  nominal ordinary/alternating shards, or 156 alternation orbits.  Thus this
  relaxation eliminates no shard.  An exact algebraic primitive-seven PSD
  filter substantially reduces individual signature lists, and
  `--compression-7` exposes the four PAF equations in CP-SAT.  A short matched
  benchmark did not improve throughput, so the option remains off by default.
  The witnesses are compressed witnesses, not exact base sequences.
- Implemented Djokovic's norm-preserving short-pair quad transposition.  Its
  domain check requires every `(C,D)` endpoint quad to have product `+1`; it
  is not valid on arbitrary near candidates.  The switch is involutive and
  preserves `N_C+N_D` coefficientwise.  The switched parity-feasible
  checkpoint therefore retains half-energy 232 and 43 bad lags.  Bounded
  continuations from both it and the canonical state found no improvement,
  which is a diagnostic only.
- Exhaustively enumerated the endpoint-parity-feasible, same-margin
  neighborhood of the canonical checkpoint through three sign exchanges.
  Hamming distances 2, 4, and 6 contain respectively 34, 3,646, and 159,558
  distinct vectors, whose minimum half-energies are 272, 248, and 280.  The
  incumbent energy 232 is therefore a strict local minimum in this radius-six
  subspace, and no exact candidate occurs there.  This says nothing about
  radius eight, other margins, or parity-infeasible intermediate states.
- Added an exact Hamming-radius constraint around a same-shard hint and a flag
  disabling all lexicographic/bit symmetry quotients.  Any symmetry-off
  infeasibility result has deliberately narrow scope: raw labeled sign vectors
  with the selected ordinary and alternating margins.  It does not extend to
  different-margin neighbors or the global-alternation partner.  Runs that
  retain symmetry breaking cover only the ball's intersection with the
  canonical chamber because canonicalization need not preserve distance to
  the hint.
- Ran the corrected symmetry-off finite models at radii 4, 6, 8, 10, 12, 14,
  and 16 around the canonical checkpoint.  Every run returned `INFEASIBLE`;
  the resource-safe one-worker radius-16 model required 1,487.746
  solver-seconds, 9,725,924 conflicts, and 59,741,208 branches while remaining
  near 112 MiB RSS.  This proves only that no exact `BS(84,83)` with the fixed
  shard-213 margins occurs within raw labeled distance 16.  It does not
  cover different-margin neighbors or transfer through global alternation.
  `VARIABLE_Q_NEIGHBORHOOD.md` freezes the checksum, all run statistics, and
  the exact reproduction command.

## 22 July 2026: circulant good-matrix route

- Added a third independent route: normalized circulant good matrices of odd
  order 167.  An exact quadruple consists of one skew sequence and three
  symmetric sequences with complementary periodic autocorrelation, and its
  Goethals-Seidel array is a skew Hadamard matrix of order 668.
- The trivial-character equation leaves only two signed row-sum profiles for
  the symmetric sequences, up to permutation:

  ```text
  (-21,-1,15),   (-9,15,19).
  ```

- Encoded the Bright--Djokovic--Kotsireas--Ganesh product theorem
  `A[k]B[k]C[k]D[k]=-A[2k]`.  Doubling has order 83 modulo sign at 167, so one
  product cycle determines all 83 independent entries of `A` from `B,C,D` and
  one seed sign; the safe `A[1]=1` decimation quotient removes that seed.
- Added an exact CP-SAT model with the two row-sum profiles, 83 product XORs,
  and all 83 independent periodic-correlation equations.  Matched bounded
  order-167 runs returned `UNKNOWN`; no candidate was emitted.  The model and
  independent verifier are regression-tested on an exact good quadruple of
  order seven and its skew `H(28)`.
- Added a two-stage reducer.  For fixed `A,B`, the product theorem gives
  `D=S*C`; reducing the remaining correlation equations modulo four yields a
  sparse `GF(2)` system in the 83 independent signs of `C`.  Across 2,000
  randomly sampled `(A,B)` pairs, the observed rank was 82, 978 systems were
  inconsistent, and only 37 passed the weight filters to the exact PAF check;
  none was exact.  Rank 82 is empirical for this sample, and the scan is not
  exhaustive.
- Audited the broader cyclic-SDS and Williamson-style routes.  All ten
  trivial-character profiles survive the Williamson parity/count test.  A
  common multiplier of order 83 is impossible from block-size congruences,
  while the order-two multiplier merely recovers symmetric blocks.  These are
  subfamily reductions, not a nonexistence proof for `H(668)`.

## 22 July 2026: resource-safe search defaults

- A four-worker radius-16 continuation exhausted the practical memory budget
  of the 16 GiB host and terminated without a usable solver result.  It is not
  recorded as `UNKNOWN` or as an infeasibility result.
- Changed every live CP-SAT command to default to one worker with an explicit
  2,048 MiB solver memory limit, and forwarded the same limit through the
  sequential shard scheduler.  OR-Tools does not account for every byte of
  Python/model-construction memory, so searches are also kept nonconcurrent.
- Declined the proposed distance-eight in-memory parity meet-in-the-middle
  table.  The streaming distance-six enumerator remains the largest exact
  combinatorial neighborhood scan retained for this 16 GiB machine.

## 22 July 2026: global seed radius and new low-memory lanes

- Enumerated every raw labeled image of the 288 exact margin shards and found
  that Eliahou's published base quadruple has margin-only distance at least
  eight.  The unique minimizer is a raw image of shard 287 with margins
  `A=(-18,18), B=(0,0), C=(3,1), D=(-1,-3)`.
- Proved the unique distance-eight pattern impossible: it must flip eight
  positive odd coordinates of `A` and no others.  The seed already satisfies
  every standard base-sequence quad product, while each of those odd
  coordinates lies in a distinct long quad, so the eight flips break eight
  required products.  A standard-library checker therefore excludes every
  exact `BS(84,83)` within raw radius eight of the published seed, across all
  margin shards.  It makes no claim beyond that radius.
- Derived the joint primitive-7/primitive-14 compression.  Each residue cell
  couples its ordinary sum to its sum after `x_i -> (-1)^i x_i` by an exact
  tiny table.  A sequential 56-cell-variable CP model imposes both compressed
  PAF systems with a 256 MiB cap; its shard scan is pending.
- Added an unrestricted cyclic-SDS route at order 167 with all ten four-square
  row-sum profiles.  The single-threaded C++ annealer uses fixed-size arrays
  and exact `O(83)` swap updates.  Any zero must pass a strict verifier of all
  periodic correlations and the full `668 x 668` Goethals-Seidel matrix.  No
  candidate is claimed before compilation, self-test, and bounded execution.

## 22 July 2026: published-seed exclusion extended through radius 17

- Added `verify_variable_q_seed_quad_radius.py`, a dependency-free dynamic
  program over the 42 long and 41 short endpoint quads.  It enumerates all raw
  labeled exact margin targets near Eliahou's seed and computes the minimum
  flip distance preserving every required quad product.  It excludes radius
  13 outright: 85 raw margin targets occur, and none is quad-reachable within
  the ball.  At radius 14 exactly 18 margin-plus-quad targets first survive,
  all at exact distance 14 in shards 0, 6, and 24.
- Independently audited the raw-margin orbit and DP logic.  A separate
  enumeration recovered the same 56,448 distinct raw labeled margin tuples;
  brute-force small even/odd fixtures agree with the DP.  The audit also
  reconstructed a radius-14 relaxation witness and directly checked its
  margins and quad products.  Such witnesses are necessary-condition objects,
  not exact base sequences.
- Added `search_variable_q_seed_frontier.py`.  It fixes each surviving raw
  target, exposes exact classwise flip-direction cardinalities, and imposes
  the primitive 3rd-, 4th-, and 6th-root norm identities.  Replacing general
  multiplication constraints with exact allowed-value tables reduced the
  radius-16 two-second screen from 120 timeouts to one.  The final rigid
  shard-287 case has exactly eight positive odd `A` flips and one partner flip
  in each selected quad; exposing that consequence resolves it immediately.
- The final radius-16 artifact contains 197 `INFEASIBLE` models and no
  survivors or timeouts.  It ran sequentially with one worker, a 256 MiB
  solver cap, 148 MB peak RSS, and no swaps.
- Fixed margins determine Hamming-distance parity.  Reusing the complete
  radius-16 certificate leaves 276 models in the exact distance-17 shell and
  skips 161 parity-incompatible targets.  Compatibility-checked resume passes
  reduced 66 initial timeouts to two and then zero.  The two last shard-28
  models required 7.296 and 9.716 seconds.  The final shell artifact contains
  276 `INFEASIBLE` statuses, peaked at 164 MB RSS, and used no swaps.
  It was subsequently regenerated directly, without a resume dependency; the
  direct models used 149.806 total solver-seconds and at most 9.862 seconds
  individually.
- Therefore no exact `BS(84,83)` lies within raw labeled Hamming distance 17
  of Eliahou's published base quadruple.  This bounded theorem fixes neither
  `q` nor a margin shard, but it is not a global nonexistence result.
- The older unsharded margin-plus-quad optimizer ended `FEASIBLE` after 300
  seconds with a checked distance-14 relaxation witness and objective lower
  bound zero.  The witness fails the small-root and length-seven layers and
  is not exact.  The monolithic full-correlation radius-10 model ended
  `UNKNOWN` after 300 seconds at 251 MB peak RSS; the decomposed radius-17
  certificates supersede that undecided diagnostic.

## 22 July 2026: bounded joint-compression and cyclic-SDS runs

- The first joint primitive-7/14 compressed model for shard 213 ended
  `UNKNOWN` after 30.005 seconds and 2,640,159 branches.  It used 111 MB peak
  RSS with no swaps and produced neither a compressed witness nor an
  infeasibility result.  The all-representative scan remains pending.
- Strict warning compilation, AddressSanitizer/UndefinedBehaviorSanitizer,
  10,000 exact exchange-delta checks, and the `H(12)` verifier regression all
  pass for the unrestricted cyclic-SDS lane.
- A 60-second one-core portfolio over all ten order-167 profiles completed
  184,060,343 moves and 185 restarts at only 1.4 MB peak RSS.  Its best
  checkpoint has row sums `(3,7,9,23)`, quarter-energy 76, and 46 bad lags.
  The checkpoint kind is deliberately rejected by the strict verifier; no
  exact SDS or `H(668)` candidate was found.
