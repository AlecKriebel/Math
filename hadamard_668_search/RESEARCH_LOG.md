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
- Edmondson, Seberry, and Anderson's published exhaustive classification of
  Turyn sequences below long length 43 contains no sequence of long length 42,
  excluding `TU(41)`.
- Added `FIXED_Q_OBSTRUCTION.md` and a pure-Python checker which verifies the
  fixed-q edge structure, product telescope, forced reversal signs, symbolic
  decimation identity.  The only imported nonexistence fact is the cited
  exhaustive Turyn classification.
- A subsequent priority audit removed an invalid shortcut that had applied a
  `2n+1` two-squares statement at odd `n=41`.  The correct zero-lag identity is
  `C^2+D^2=162`, and `162=9^2+9^2`, so that shortcut supplies no obstruction.
  The fixed-q reduction remains valid, and its final contradiction now rests
  solely on the exhaustive classification.
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
- Replaced each good-matrix PAF equation's 668 directed-edge XORs by an exact
  reflection quotient with 331 representatives.  The skew distance is
  `2+2*sum(82 XORs)` and each symmetric distance is `2*sum(83 XORs)`, so the
  reduced cardinality target is 166.  This cuts the PAF auxiliaries from
  55,444 to 27,473.  Direct order-7/order-167 distance regressions and the
  exact `H(28)` construction test pass.
- Added the remaining exact common-decimation quotient.  The unique row-sum-
  15 symmetric sequence has a nonconstant 83-bit doubling-cycle word; making
  it lexicographically maximal among all rotations removes a factor of 83
  after the state-dependent multiplier sign restores `A[1]=1`.  Exhaustive
  short-word truth tables validate the reified lex encoding.  The default
  model now has 34,530 variables and 67,987 constraints versus 55,777 and
  55,614 in the old full-edge model.
- Sequential 60-second searches of the two reduced order-167 profiles ended
  `UNKNOWN`, with 2,121,259 and 2,256,669 branches.  Whole-process peaks were
  272.7 and 285.3 MB under a one-worker, 256 MiB solver cap; both used zero
  swap.  No candidate was emitted, and these bounded outcomes prove no
  nonexistence result.
- Implemented a fixed-array C++ form of the exact `A,B -> GF(2) -> C,D`
  reducer.  Its self-test exhausts the order-7 `(A,B)` domain and agrees with
  brute force on all nine extendible pairs; 16 order-167 fixtures give the
  same result under direct elimination and transformed-RHS factor reuse.
  ASan/UBSan passed 10,000 order-167 trials.
- Derived the bijective `(S,B)` parameterization.  With `A[1]=1` and
  half-weight 38 for `B`, the doubling recurrence closes exactly when the
  half-weight of `S` is odd.  The two exact `C,D` profiles restrict this to
  `5..77` or `7..81` by twos.  A lex-max doubling necklace removes the exact
  83-fold common-decimation action.  Fixing `S` also fixes the GF(2) matrix,
  allowing one row-transform factorization to serve 256 `B` samples.
- Direct 60-second streams evaluated 442,374 and 441,506 samples and reached
  PAF energies 3,200 and 3,296.  Factored `(S,B)` streams evaluated 2,890,277
  and 2,871,527 samples, reaching energies 2,752 and 3,264.  All four best
  checkpoints pass the independent Python replay; none is exact.  The
  factored runs used at most 1.44 MB RSS and zero swap.  Checkpoint writes are
  checked and atomic, and high-nullity systems are deferred rather than
  treated as rejections.
- Added the full structured `(B,C,D)` local parameterization with
  `S=C xor D` and `A` recovered by the doubling recurrence.  Atomic exchanges
  in each mask make the fixed-weight state graph connected; three coupled
  exchanges leave `A` unchanged.  A 96-step invariant test covers each move
  family, and ASan/UBSan passed a 10,000-move shard.  The separate verifier
  checks all structure and PAFs and explicitly reports `NOT H(668)`.
- Profile 0 fell from energy 2,752 to 808 in 1,659,072 production moves and
  then to 752 under cold reheating.  Profile 1 independently reached 752 in
  1,657,915 moves.  Complete scans of 7,742 and 7,682 valid two-coordinate
  neighbors found no improvement, so both are local minima for the stated
  move union.  Hot reheating, compound moves, and soft GF-shadow penalties
  did not pass this floor.  These results imply no global lower bound.
- On the exact GF surface, complete scans of every one-exchange `B` neighbor
  and two-toggle `S` neighbor evaluated 5,113 states per profile.  Including
  the centers, only 64 and 65 recovered an exact-weight affine survivor; none
  improved energies 2,752 and 3,264.  This is another finite local-minimum
  result, not an exhaustive good-matrix search.
- Added an exact CP-SAT bridge from the two energy-752 local checkpoints.  The
  loader strictly verifies each nonexact state, reorders the symmetric
  sequences by sorted row sum, selects the lexicographically maximal doubling
  rotation of the unique row-sum-15 anchor, and chooses the multiplier sign
  that restores `A[1]=1`.  Fixed regression masks, residual-multiset checks,
  orbit-invariance checks, and the model proto confirm exactly 332 distinct
  primary hints; no PAF auxiliary is hinted or fixed.
- Sequential one-worker, 256 MiB repaired-hint runs of 60 seconds per profile
  returned `UNKNOWN`.  Profiles 0 and 1 made 1,024,840 and 1,572,158 branches
  with 1,429 and 1,241 conflicts; whole-process peaks were 337.4 and 339.0 MB,
  with zero swap.  No candidate was emitted.  OR-Tools' hint repair preserves
  every exact constraint, but these time-bounded outcomes prove neither
  existence nor infeasibility.
- Reused one PAF XOR auxiliary per sequence and unordered half-index pair.
  Every pair occurs exactly twice across all 83 lags; skew occurrences have
  opposite polarity, while each symmetric sequence contributes 83 direct
  singleton literals.  This exact cache cuts PAF auxiliaries from 27,473 to
  13,612 and the default necklace model from 34,530 variables / 67,987
  constraints to 20,669 / 54,126.  Exhaustive order-7 assignments, all
  order-167 multiplicities, proto counts, and the exact `H(28)` regression
  pass.
- Added exhaustive fixed-`A` triangle trades to the structured local descent.
  Alternating all pair moves with all six triangle assignments left profile 0
  at energy 752 after 77,144 evaluations.  Profile 1 improved from 752 to 728
  at evaluation 73,261 and then exhausted a second round at 155,008 total.
  The independently verified state has 58 bad lags and maximum absolute
  quarter residual 6.  The 5.60-second run used 1.47 MB RSS and zero swap.
  This proves only local minimality for the stated pair-plus-triangle union.
- Cached-model repaired-hint runs emitted no candidate.  Profile 0, with a
  10,000-conflict repair allowance, returned `UNKNOWN` after 39,844 branches
  and 77.591 seconds at 287.0 MB peak RSS.  Profile 1 started from energy 728
  and returned `UNKNOWN` after 168,484 branches and 3,539 conflicts in 60.004
  seconds at 279.6 MB.  Both used one worker and zero swap.  A 30-second exact
  CP-SAT ball of symmetric exchange radius one around the E728 state also
  returned `UNKNOWN` at 537.4 MB, so that memory-heavier formulation was not
  enlarged; the direct pair scan already exhausts that radius cheaply.

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
- Added strict checkpoint loading, incumbent perturb-and-restart, exact
  compound exchanges across up to four distinct sequences, and a mixed
  single/compound move probability.  Loaded residuals and energy are always
  recomputed.  The self-test now covers 10,000 single and 1,000 compound
  deltas; strict compilation and a sanitized mixed-continuation smoke test
  pass.
- Six 10-second incumbent continuations, four 10-second pure-compound runs,
  three 20-second mixed schedules, and a 10-second-per-profile screen did not
  beat quarter-energy 76.  These bounded failures are search diagnostics, not
  evidence against a cyclic SDS.
- A later 600-second continuation with seed 12668 and a 5% three-sequence
  compound mixture finally improved the profile-5 incumbent to quarter-energy
  64 after roughly 360 seconds.  The complete run evaluated 1,628,953,659
  exact moves over 1,629 restart basins at 1.4 MB peak RSS and zero swaps.
  Independent arithmetic matches all stored correlations, 46 bad lags, raw
  maximum residual 8, and quarter-residual histogram
  `{-2:2,-1:22,0:37,1:18,2:4}`.  The checkpoint remains nonexact.
- Added bounded deterministic compound polish.  An 8192-entry pool contains
  every opposite-sign exchange and proves that the energy-64 checkpoint has
  no improving single exchange or pair of exchanges in distinct sequences.
  A 1,024-entry-per-sequence scan found no improving triple.  The exhaustive
  pair scan took 14.28 seconds; the bounded triple scan took 219.57 seconds;
  both used 11.5 MB peak RSS and zero swaps.  The triple result is not an
  exhaustive all-triples statement.

## 22 July 2026: published-seed exclusion extended through radius 18

- Enumerated the exact distance-18 margin-plus-quad frontier: 823 targets are
  parity-compatible, while 276 raw targets have the wrong fixed-distance
  parity.  A first half-second root screen proved 525 targets infeasible,
  decoded 7 root witnesses, and left 291 timeouts.
- Added compatibility-checked survivor and timeout selection to the frontier
  driver, together with exact long/short quad-distance lower bounds.  A
  2-second pass on the 298 live targets proved 209 more infeasible and exposed
  11 root witnesses; a 5-second pass on its 78 timeouts proved 37 more and
  exposed one additional witness.
- Identified the exact modulo-12 symmetry of the root relaxation.  Endpoint
  quads with equal oriented seed signs and equal endpoint residues are
  interchangeable.  Bit-level orbit ordering proved 2 more targets
  infeasible.  Replacing each orbit by counts of its eight even-flip patterns
  gives an exact quotient with 60 quad orbits, 512 small integer variables,
  and 111 constraints before presolve.
- The quotient proved 32 of 38 hard targets infeasible at a 5-second cap and
  the remaining 6 in 6.229--11.302 seconds each.  It was independently
  checked in both directions: all 18 radius-14 targets remain infeasible, and
  a known shell-18 witness decodes to 334 signs whose margins, distance, quad
  products, and primitive-root norms verify exactly.
- The complete root classification is therefore 811 infeasible targets and
  12 verified root witnesses.  Primitive-7 compression eliminates 9 witness
  targets.  Primitive-14 compression eliminates the remaining 3 in 5.077,
  12.913, and 29.017 seconds.
- Added `verify_variable_q_seed_shell18_artifacts.py`.  With standard-library
  integer arithmetic it reconstructs all 823 targets, pins nine SHA-256
  artifacts and every parent-selection edge, independently verifies all 12
  witnesses, and checks that the compression eliminations cover exactly the
  witness set.  It passed at 39 MB peak RSS.  The largest recorded solver run
  in this chain used 176 MB peak RSS; every run used one worker, a 256 MiB
  solver cap, and zero swaps.
- The stored CP-SAT results consequently report no exact `BS(84,83)` within
  raw labeled Hamming distance 18 of Eliahou's published base quadruple.  The
  publication-audit correction below records the remaining proof boundary.

### Publication-audit correction

The artifact checker independently validates the twelve decoded
primitive-root witnesses, but it does not independently prove that their
whole target models become infeasible after primitive-7/14 compression.
Those twelve eliminations are CP-SAT `INFEASIBLE` statuses, just like the
1,284 primitive-root eliminations.  A proof-grade radius-18 release therefore
has 1,296 solver leaves to certify, not 1,284.  Until those certificates or a
structurally independent enumeration exist, the radius-18 statement is a
strongly audited solver-backed computational claim rather than a
proof-assistant-level theorem.

## 22 July 2026: cyclic-SDS decimation and complete radius-four audit

- Added a shaped annealing score `E + pB`, while keeping exactness tied only
  to raw energy `E=0`.  Strict and sanitized delta tests pass, checkpoint
  metadata records the penalty and score, and raw-energy pair polish is
  rejected when a nonzero penalty is active.  Sixty-second screens at
  penalties 2, 4, and 16 evaluated 156,994,182, 151,691,146, and 151,667,228
  proposals, respectively, without displacing the energy-64 incumbent.  Each
  used 1.4 MB peak RSS and zero swaps.  Bad-lag shaping remains diagnostic
  because a strong penalty can concentrate residual mass.
- Exhausted the complete relative independent-decimation orbit.  PAF symmetry
  quotients each multiplier by sign, and a common multiplier only permutes
  lags, leaving `83^3 = 571,787` normalized tuples.  The identity tuple wins
  the invariant energy, quartic, and maximum-residual rankings at
  `(E,Q,B,max)=(64,136,46,2)`.  The C++ scan took 0.33 seconds at 1.4 MB peak
  RSS.  An independently written standard-library Python enumeration checked
  all 571,787 tuples in 20.08 seconds at 16.8 MB peak RSS and reproduced the
  winner.
- Added exact same-sequence four-flip deltas, including the cross interaction
  omitted by naive delta addition.  One hundred randomized incremental cases
  match full recomputation.  The exhaustive scan covered 46,884,138
  two-in/two-out states in 6.34 seconds at 3.9 MB peak RSS.
- Rescored all 27,722 single exchanges and all 288,185,440 pairs of exchanges
  in distinct sequences for energy, quartic score, and maximum residual.  The
  optimized scan took 11.88 seconds at 11.5 MB peak RSS.  Full sanitized
  repetitions of the same- and cross-sequence scans took 15.13 and 28.09
  seconds and stayed below 29 MB peak RSS; all runs used one core and zero
  swaps.
- Together with the identity, these disjoint classes are exactly all
  335,097,301 states preserving the four row sums at raw labeled Hamming
  distance at most four.  Only the incumbent attains energy 64, and only it
  attains quartic score 136.  The minimum maximum quarter-residual is 2,
  attained by 5,442 states.  Hence no exact cyclic SDS occurs in this complete
  neighborhood.  This is a finite local theorem around the stored profile-5
  checkpoint, not a global cyclic-SDS obstruction.
- Added `verify_sds_167_neighborhood.py`.  It pins the incumbent checkpoint
  hash, independently recomputes the row sums, correlations, metrics, and all
  four combinatorial class counts, independently exhausts the normalized
  decimation orbit, replays both C++ radius-four scans, and checks that their
  disjoint tie counts combine to the documented totals.  The complete replay
  passed in 28.96 seconds at 25.5 MB peak RSS with zero swaps.

## 22 July 2026: cyclic-SDS quartic and guided-window lanes

- Generalized the annealing objective to `w_E E + w_Q Q + w_B B`, while
  retaining `E=0` as the only exactness test.  Added exact random
  two-plus/two-minus moves within one sequence, including every autocorrelation
  interaction term.  A 60-second pure-quartic run evaluated 152,303,355
  proposals; a 120-second run with 30% same-sequence moves evaluated
  237,719,274 proposals over 1,189 basins.  Neither lowered the incumbent's
  `(E,Q)=(64,136)`; both used under 1.5 MB peak RSS and zero swaps.
- Exhausted six disjoint guided `H=12` single-sequence window families.  The
  union contains 64,899,721 unique fixed-profile states.  An exact paired
  `H=6` scan then made 61,471,872 evaluations across twelve families and all
  six sequence pairs, representing 61,383,193 unique states.  Neither scan
  found an exact SDS or improved energy, quartic score, or maximum residual.
  The paired evaluation count includes overlaps between its sequence-pair
  domains; its printed ties are evaluation multiplicities.
- Added an exact four-block `H=6` meet-in-the-middle scan.  Each aligned family
  enumerates `924^4=728,933,458,176` assignments using 853,776 stored left
  pairs.  Two linear 64-bit fingerprints admit no false negatives, and every
  match is checked over all 83 residuals.  Twelve support-disjoint aligned
  families have a union of 8,747,201,498,101 unique states; none is exact.
  The complete optimized pass took 2.36 seconds at 24.7 MB peak RSS with zero
  swaps.  A one-family ASan/UBSan pass used 44.2 MB and reported no issue.
- Added `verify_sds_167_windows.py`.  It independently reconstructs every
  correlation in a direct `6^4=1,296` regression, replays the full twelve-
  family aligned MITM, validates sign-balanced disjoint supports, and checks
  all counts and unchanged output.
- Extended the MITM to all `12^4` mixed family choices.  Deduplicating the
  repeated identity assignment leaves `11,077` configurations per sequence
  and exactly 15,055,272,576,605,041 unique states.  Eight left-family pairs
  per batch use 6,830,208 records plus a 32 MiB no-false-negative Bloom
  filter.  All 18 batches completed 2,212,987,392 right probes in 39.92
  seconds at 216.3 MB peak RSS and zero swaps.  There were 877,347 Bloom
  positives, no exact fingerprint matches, and no exact SDS.  A full-size
  one-batch ASan/UBSan replay passed at 279.0 MB peak RSS with zero swaps.
- The window verifier now independently enumerates the 14,641 canonical
  states at `H=2,F=2`, then replays both large aligned and mixed scans and
  checks their exact counts.  It passed in 39.21 seconds at 216.2 MB peak RSS
  with zero swaps.  The mixed result still covers at most one guided window
  per sequence, not arbitrary cyclic SDS quadruples or multiple windows in a
  single sequence.

## 22 July 2026: exact modulo-9 Legendre profile fibers

- Derived the exact row-compression equations.  For row sums `alpha,beta`,
  the shifted vectors `z=(alpha-1)/2`, `w=(beta-1)/2` have sums `-4`, combined
  squared norm 152, and combined cyclic correlations `-15` at lags 1 through
  4.  Equivalently the row sums have combined PAF
  `(594,-74,...,-74)`.  Every such profile is automatically Gale--Ryser
  compatible with the fixed 37 column margins.
- Catalogued an initial 12 exact, pairwise orbit-distinct sampled profiles
  under the 1,944-element compressed symmetry.  The catalog at that stage was
  deliberately not called exhaustive.  Added a single-threaded C++ fiber
  engine whose `2 x 2` CRT
  checkerboard switches preserve all 18 row and 74 column margins.  Exact
  delta/full-recompute self-tests cover all profiles and compound A/B moves.
- Added a reproducible 18-variable exact profile sampler.  It canonicalizes
  every output orbit, streams atomic JSON with explicit non-certificate flags,
  and defaults to one worker with a 128 MiB solver cap.  Its smoke test used
  93.2 MB whole-process RSS and zero swap.
- Partitioned the exact outer model by the invariant centered norm
  `max(sum(z_i^2),sum(w_i^2))`.  The 37 even shards from 76 through 148 are
  disjoint and exhaustive.  Sequential 1.5-second screens of the 25 shards
  absent from the original catalog found four new orbit classes, at norms 82,
  116, 130, and 134; the other 21 runs were `UNKNOWN`, not infeasible.  A
  second three-second pass over five balanced missing shards found a fifth
  class at norm 86, while norms 76, 84, 92, and 94 stayed `UNKNOWN`.  The
  catalog and fixed-memory engine then validated 17 profiles.
- Ten-second local screens of new profiles 12 through 16 reached energies
  2528, 2400, 2488, 2560, and 2480.  Deepening profile 13 for 60 seconds reached
  E2344 with 133 bad lags, maximum raw residual 20, and L1 residual 984.  A
  complete engine scan of its single, cross-pair, disjoint-pair, and six-cycle
  neighborhoods found no improvement.  The generalized independent verifier
  confirms all 17,676,364 unique states in that radius-two ball have energy at
  least 2344; it used 72.6 MB RSS and zero swap.  The searches used at most
  2.12 MB RSS; profile 6 at E2320 was the catalog incumbent at that stage.
- A separate 60-second profile-1 depth run evaluated 219,985,355 proposals
  and retained E2360.  Its complete engine radius-two polish also found no
  improvement.  The disposable checkpoint passed strict replay; this bounded
  result does not justify retaining another near-miss artifact.
- A 60-second profile-4 depth run evaluated 221,282,503 proposals and improved
  the global catalog incumbent from E2320 to E2280, with 120 bad lags, maximum
  raw residual 20, and L1 residual 928.  Complete single, cross-pair,
  disjoint-pair, and six-cycle polish found no descent.  The independent
  verifier enumerated all 17,801,598 unique radius-two states and confirmed no
  lower energy.  The search used 2.12 MB RSS and the independent audit 73.0
  MB; both used zero swap.  E2280 remains nonexact and is not an H(668).
- Completed the larger exact mixed neighborhood at the profile-4 E2280
  incumbent.  Pairing every legal alternating six-cycle in either sequence
  with every legal checkerboard switch in the other gives 749,359,042
  possible pair distances.  The exact bounding-box search evaluated
  486,717,630 point distances after safe pruning and found no descent.  The
  complete pass took 285.28 seconds at 8.52 MB RSS with zero swap; strict
  replay confirms that its center is unchanged and nonexact.  This is only a
  finite local theorem, not a profile-fiber or Legendre-pair impossibility.
- Four-second sequential screens used about 2 MB RSS and zero swap.  Profile
  6 led at half-PAF energy 2352; a 60-second run improved it to 2320 with 135
  bad lags, maximum raw PAF residual 20, and L1 residual 976.  The strict
  verifier recomputes all correlations, compression lifts, margins, and
  redundant count metadata, then explicitly reports `NOT H(668)`.
- Exhaustively rescored the profile-6 one-switch neighborhood: 2,939 legal A
  switches and 3,053 legal B switches.  None ties or improves the incumbent;
  the least uphill move reaches energy 2400.  This is a finite local result,
  not a bound on the whole fiber.  A fixed-memory exact polish then scored the
  complete A-by-B two-switch neighborhood of 8,972,767 states and found no
  improvement.  The same run scored 4,109,262 disjoint A-switch pairs and
  4,438,151 disjoint B-switch pairs, again with no improvement.  The combined
  replay also scored 120,553 valid A and 126,980 valid B alternating
  six-cycles.  It took 1.38 seconds at 4.42 MB RSS with zero swap; the output
  signs are byte-identical to the independently verified E2320 checkpoint.
- Added an independent collision-free radius-two verifier.  It classifies
  every overlap of two same-sequence switches, combinadically deduplicates
  their resulting eight-cell supports, and directly recomputes all residual
  energies.  The complete product switch-graph ball contains 17,661,680
  unique states including the center.  None has energy below 2320.  The
  independent replay took 0.92 seconds at 72.4 MB RSS with zero swap.  This is
  a finite local theorem only, not a global lower bound for the fiber.
- A 60-second incumbent continuation with a 5% coordinated A/B proposal
  mixture evaluated 213,783,033 exact moves over 855 restart basins.  It
  retained E2320 unchanged, used 2.44 MB peak RSS and zero swap, and passed
  strict replay.  This is a bounded heuristic result only.
- Added an exact CP-SAT profile option.  Fixing one catalog entry replaces the
  generic modulo-3 table and 90 nonlinear products with 18 row cardinalities;
  `--symmetry none` is required because row symmetries change the chosen
  orientation.  Profile-checkpoint hints now pass the strict verifier and can
  request CP-SAT hint repair without fixing any sign.
- The full profile-6 model has 111,554 variables and 110,556 Boolean XORs.
  A 15-second one-worker pilot returned `UNKNOWN` after 493,894 branches and
  155 conflicts.  Model construction peaked at 254 MB; the solve peaked at
  703 MB total RSS with zero swap even under a 320 MiB solver limit, confirming
  that the solver cap does not account for all process memory.
- A second 10-second profile-6 run enabled repaired-hint search with a tighter
  128 MiB solver limit.  It returned `UNKNOWN` after 222,444 branches and no
  conflicts, emitted no candidate, and nevertheless reached 931 MB total RSS
  with zero swap.  Hint repair and presolve storage are not bounded by the
  internal limit, so this full-model experiment is not being enlarged on the
  current 16 GiB host.
- Added exact model-level exclusion of every oriented image of already
  catalogued compressed profiles.  A constructive subgroup symmetry chooses
  independent dihedral maxima and orders the two vectors, reducing each
  1,944-element orbit by a sound 648-element subgroup while leaving the common
  multiplier for output canonicalization.  Independent tests prove that every
  full orbit retains a representative and that each exclusion table is exactly
  the selected catalog-orbit union.
- The improved outer sampler found four more orbit-distinct profiles: profile
  17 in centered-norm shard 82, profile 18 in shard 102, profile 19 in shard
  108, and profile 20 in shard 130.  The catalog and both engines now validate
  21 exact compressed profiles.  Their ten-second fixed-margin screens reached
  E2480, E2544, E2336, and E2408 respectively; none is exact.
- A 60-second continuation from profile 19 evaluated 214,957,700 proposals and
  retained E2336 with 133 bad lags.  Complete cross-pair, same-sequence-pair,
  six-cycle, and connected-eight-cycle engine scans found no descent.  The
  independent radius-two verifier enumerated 17,708,876 states including the
  center and found none below 2336.  The independent eight-cycle replay
  covered 9,526,800 moves and found exact minimum 2448.
- Added an exact connected alternating-eight-cycle polish.  At the profile-4
  E2280 incumbent the engine evaluates 9,549,173 legal cycles in fixed memory
  and finds no descent.  A structurally independent DFS verifier finds exact
  minimum 2568 with multiplicity two and replays its witness with every margin
  unchanged.  Independent exhaustive `4 x 4` tests prove that the canonical
  generator equals all 72 connected two-regular supports and that its sign
  buckets cover all 65,536 signings.
- Replaced reliance on the mixed-neighborhood KD-tree claim with a direct
  independent verifier.  It evaluates all 749,359,042 cycle/opposite-checker
  states, finds unique minimum 2408, and reports no state tying or improving
  the E2280 center.  The full replay took 8.51 seconds at 4.03 MB RSS with zero
  swap.  This remains a finite local theorem, not a profile-fiber lower bound.

## 22 July 2026: milestone freeze and priority audit

- Added `RESUME.md` with authoritative checkpoints, hashes, low-memory restart
  commands, and an explicit full-matrix finish line.
- Re-ran the complete 116-test Python suite, strict replay of every retained
  Legendre checkpoint, the independent radius-two/mixed/eight-cycle
  verifiers, seed and obstruction checkers, and the radius-16/17/18 frontier
  artifact checkers.  Release builds were warning-clean and stayed well below
  the 16 GiB host limit.
- Corrected the exposition of the fixed-`q` theorem.  The parity telescope and
  reduction to `TU(41)` remain valid, but a previously stated odd-`n`
  two-squares shortcut does not: `162=9^2+9^2`.  Emptiness of `TU(41)` rests
  on the exhaustive 1994 classification by Edmondson, Seberry, and Anderson.
- The provisional audit initially ranked the raw-radius-18 seed exclusion as
  the strongest likely-new result, with the fixed-`q` reduction as a theorem
  component.  The certificate audit below reverses that publication order:
  fixed-`q` is the strongest theorem-sized result, while radius 18 remains a
  solver-backed claim.  CP-SAT `INFEASIBLE` records are reproducible solver
  results, not independently replayable proof transcripts.

## 22 July 2026: publication-certificate audit

- Corrected the radius-18 proof gate from 1,284 to 1,296 leaves.  The twelve
  primitive-7/14 eliminations are solver-reported infeasibility decisions too;
  decoding their parent witnesses does not independently prove those final
  models empty.
- Added an OR-Tools-independent deterministic CNF exporter and four pinned
  DRAT proofs: one radius-16 root, one shell-17 root, one shell-18 root, and
  one shell-18 primitive-7 leaf.  Regeneration plus `drat-trim` replay passed
  4/4 in 34.62 seconds at 250 MB peak RSS.  A known feasible shell-18 root
  also passed an independent SAT-model and clause checker with the symmetry
  quotient enabled.  All twelve stored root witnesses then passed exactly
  pinned, unquotiented v2 CNFs, every DIMACS clause, and independent margin,
  distance, quad, pair-bound, and primitive-root checks.  A fourth exhaustive
  regression independently reconstructs the complete contribution signature
  of all 83 endpoint quads for every even mask and matches the exporter's
  global root-orbit partition and comparison forest.
- Stopped the hard-leaf pilots rather than scaling them.  A raw-bit hard
  trace reached 388 MB without completing; combined z7/z14 reached 1.785 GB
  RSS and timed out.  The next proof task is an exact orbit-count CNF for the
  six hard root leaves, followed by a size audit before any full corpus.
- Independently reproduced `TU(41)=empty` with a dependency-free outside-in
  enumerator: 461/461 canonical shards, 57,543,021 nodes, zero solutions,
  362.92 seconds summed serial time, and 1.38 MB peak RSS on the slowest
  shard.  A separate Python exhaustion verifies the exact `2^19` depth-five
  cube cover, and sanitizer regressions reproduce the known small cases.
- Completed a primary-source priority audit.  The open 2025 Eliahou paper and
  conference slides do not contain either repair result.  The body of the
  June 2026 update remains paywalled, so its overlap status is unresolved.
  Project policy prohibits external outreach; no contact drafts or recipient
  lists are retained.
- Drafted `local_obstructions_668.tex` as one theorem plus one explicitly
  solver-backed computational claim.  Public theorem-level release remains
  gated on all 1,296 radius leaves, the inaccessible 2026 text or author
  response, and expert review.
