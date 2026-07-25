# Hadamard 668 research log

## 23 July 2026: unrestricted projective exhaustion and two larger constructions

- Solved the complete modulo-four projective quotient for the common-type
  five-comb packing. Its 24 label bits have rank-nine syndrome; row-sign
  normalization leaves twelve free bits and exactly 4,096 label maps. Row-pair
  swaps reduce them to 1,440 representatives, partitioned by five structural
  bits into 32 exact cores.
- Derived the complete label-independent physical hole fiber: five
  equalities and one disequality form six affine relations and leave 256
  completions; lag 82 fixes the outer position-82 vector to
  `eta*V_2`, and lag 83 makes the two long tails opposite.
- Derived and dependency-free verified the exact lags-81-through-78 boundary
  equations. The physical table has 10,934 rows; its projective image has
  2,434 rows and yields the universal clause
  `beta or u7 or y1 or y7`. The checker replayed 134,872 table/sequence
  boundary cases and 13,824 general high-lag formulas.
- Integrated the physical boundary table into the exact factorized,
  pure-Boolean, and spectral models. A 32-core pilot excluded quartet zero
  completely in 193.51 seconds wall time at 473 MB maximum RSS. The full
  disjoint four-process sweep stayed around 1.4 GB aggregate memory.
- Completed all `48*32=1,536` exact common-type cores: every record is
  `INFEASIBLE`, with zero `UNKNOWN` and zero candidate. Recorded totals are
  10,768.610061 solver-seconds, 3,568,646 conflicts, and 71,107,207 branches.
  The canonical corpus digest is
  `9c1534a77319dd1b8e0a90f8fb2a620ad09499c6948e1198087bc29c967ecb45`.
  This is a solver-backed restricted-family exclusion with no independent
  UNSAT certificates.
- Proved the exact dyadic-compression theorem. Norm identities at all roots
  through order 16 are equivalent to one periodic autocorrelation identity
  for four length-16 integer compressions. The nine bucket/root bases differ
  by determinant `-256`. Physical parity gives 14 even and 50 odd cells and
  exactly 1,589 possible magnitude shells. An independent audit reproduced
  all formulas and counts; the dependency-free verifier digest is
  `f029b9690c941297b1da21286a7299ab9bf60e319306488a9e781c642ce05a51`.
- Audited the obvious odd-modulus shortcuts and stopped them: all 704
  spectral-class/core units reach full affine rank modulo 3, 5, and 7 after
  cross catalogs are included, and direct modular reachability survives in
  every class tested. The next spectral engine must retain component
  consistency or use staged cyclotomic filtering.
- Proved the same-word self-cancellation theorem: the exact extension of the
  diagonal/common-type family is an ordered pair of complementary quartets,
  2,304 cases. Then proved a strictly larger distinct-lobe theorem: four
  directed pairs used with both polarizations self-cancel exactly when their
  combined eight words form one complementary octet.
- Classified the distinct-lobe family exactly: 1,246 octets in 35 signature
  profiles and 768,512 sorted directed-pair inventories. Of these, 557 octets
  and 721,984 inventories are genuinely beyond separate lower/upper
  quartets. An exhaustive 65,536-state check proves that the rank-nine
  projective quotient, 4,096 labels, 1,440 row orbits, hole fiber, and
  physical high-lag table all carry over.
- Found a new independent `LP(333)` construction lane invariant under the
  order-six multiplier 64 modulo 333. Its sextic `9 x 7` QPSK quotient has 34
  reversal-inequivalent lag equations. Symmetry fixes the 972-element
  `LP(9)` zero-column orbit and leaves 108 Boolean signs. The other columns
  have 28 real-PAF signatures, reducing the row-axis fiber to 298 exact
  three-plus-three signature shards.
- Constructed and fully expanded a sextic axis-complete skeleton. It satisfies
  every pure row and column equation but remains a non-candidate with 20/24
  mixed quotient residuals, energy 784, and 120/144 mixed physical lags bad.
  A dependency-free checker reproduced the quotient matrices, all short-word
  counts, the full 333-cell expansion, and exact obstructions to the
  quadratic-residue and logarithmic-template subfamilies. An independent
  audit corrected the wording: the 34 equations are reversal-inequivalent;
  fixed compression leaves at most 27 linearly independent.
- Built the first exact sextic CP model with 108 primary signs, 2,862 cached
  XORs, 2,970 total variables, and 2,908 constraints. Its candidate gate
  replays all quotient/CRT equations, all 333 periodic correlations, the
  bordered construction, and the full order-668 matrix before writing. A
  300-second eight-worker pilot ended `UNKNOWN` after 145,214 conflicts and
  3,155,570 branches, at 522.8 MB maximum RSS and zero swaps. It emitted no
  candidate.
- Implemented the exact 28-signature/298-shard propagation layer. The
  unsharded model without residual symmetry has 2,977 variables and 2,916
  constraints; a fixed shard has 2,976 variables. A sequential
  atomic-record runner makes all 298 shards resumable.
- Proved and dependency-free verified the residual order-three decimation
  symmetry. The unit `226` fixes the `Z/9` row coordinate, rotates sextic
  classes by two, and has cube `64`, which is trivial on the multiplier
  quotient. The 972 zero-column cores form one free symmetry orbit, all 298
  signature shards are invariant, and the 1,658,700 compatible ordered
  signature sextuples have 18 fixed points and exactly 552,912
  signature-level `C3` orbits. The exact tie-safe lex leader gives a default
  model with 2,979 variables and 2,923 constraints.
- A 20-second four-worker pilot of that strengthened model ended `UNKNOWN`
  after 711 conflicts and 149,953 branches, at 2,263,646,208 bytes maximum
  RSS and zero swaps. It emitted no candidate and proves no infeasibility.
- Proved the universal projective-core-zero obstruction. In that core all
  carrier row sums are `(x,x,y,y)`; the physical hole fiber and the `z=1`
  norm force either 165 or 166 to be a sum of two integer squares, which is
  impossible. This removes all 128 core-zero row-orbit representatives,
  including 8/2,434 projected and 288/10,934 full high-lag rows. A
  dependency-free verifier also classifies all 768,512 paired-lobe
  inventories into four exact root-amplitude profiles.
- A broader session-only `z=1` profile audit found 3,968/4,096 projective maps
  feasible for each of the four profiles, with exactly the same 128
  core-zero maps excluded. No stronger profile-dependent root cut emerged.
  That auxiliary all-core DP is not retained by the verifier and is recorded
  only to prevent repeating the same exploratory calculation.

## 23 July 2026: constructed prime-fold lane and algebraic exclusions

- Implemented the 45-shard prime-83 oriented-SDS constructor with an
  independent verifier and automatic `82*83^2` adjacent-fold lift bank.
- Retained and replayed profile 19, sizes `(37,37,35,41)`, row sums
  `(8,10,13,1)`, quarter-energy 14, and 11 bad independent lags. Exact
  meet-in-the-middle polishing through the documented coordinated move
  families found no zero. No prime fold or lift was produced.
- Used `167=2*83+1` to derive a Sidelnikov binary/one-zero PAF identity.
  Direct endpoint completions, zero filling, and degree-two products were
  excluded exactly.
- Enlarged that character family by independent decimations. A modulo-four
  theorem forces equality of the 41 inverse-pair orientation fingerprints.
  The only catalog intersection has `U` row sum 82 and therefore violates the
  energy bound. The full 12,584,792-state signature join independently found
  zero prime folds.
- Factored all thirteen Eliahou base residuals as
  `32*N((z^42-1)(1-z^4+z^8-z^12+z^16))` above a constant 14.
  The complete literal reciprocal chord has zero modulo-32 points, and all
  80,896 endpoint pairs in the disjoint-comb constructor fail exact
  cross-orthogonality. A unit-circle root also excludes every four-sequence
  repair retaining the common comb factor.
- Found a constructive spectral escape: the alternating comb extends to a
  minimum complementary octet; opposite separation-42 polarizations and two
  copies give 32 flat channels of energy 320. Eight carrier shifts per target
  sequence occupy 80 coefficients and leave precisely the 14 singleton
  positions needed for energy 334. Only their packing cross terms remain.
- Added an axis-preserving quartic `LP(333)` constructor. Its bounded pilot
  improved quotient energy from 1536 to 112 but left 14/18 quotient
  equations nonzero. It remains a checked non-candidate.

## 23 July 2026: three theory-first construction reductions

- Proved the adjacent cyclic-fold theorem: `BS(n+1,n)` is equivalent to the
  intersection of the padded modulo-`n+1` cyclic complement and the
  endpoint-folded modulo-`n` cyclic complement.
- At `n=83`, converted the prime fold into 41 exact oriented-SDS equations,
  enumerated 45 anchored size profiles, and derived a relative norm shadow in
  `GF(2^82)/GF(2^41)`. An oriented SDS has 564,898 basic phase/multiplier
  lifts to test at modulus 84; any passing lift is already exact.
- Recast `LP(333)` as a QPSK real-autocorrelation problem. The quartic
  residues modulo 37 form a `(37,9,2)` difference set and give an exact
  45-phase, 22-equation quotient. A checked axis-complete table leaves only
  16 mixed quotient equations; it remains a strict non-candidate.
- Derived a finite 2-adic lift for the special seed. Exactness forces an
  84-bit reciprocal `q` skeleton; the next layer is linear in `s`. The
  published seed first fails at five modulo-32 lags whose syndrome is a
  Frobenius square. Exact Jacobian ranks `82,163,200,200`, with augmented rank
  201 at the next lift, rule out a first-order tangent repair.
- Added dependency-free checkers for all three reductions. No exact
  `BS(84,83)`, `LP(333)`, or `H(668)` is claimed.

## 23 July 2026: primitive-eight sphere and a distance-34 theorem

- Evaluated the `BS(84,83)` norm identity at
  `z=exp(pi*i/4)` and split it over `Q(sqrt(2))`.
- Reduced each base sequence to four signed residue sums
  `(x,y,alpha,beta)`. Every exact quadruple must satisfy a rational
  16-square equation of energy 334 and a second bilinear cancellation.
- The published seed has rational energy 1614 at this root. A
  dependency-free dynamic program over the sixteen bounded coordinates proves
  that the nearest point on the required rational sphere is at raw Hamming
  distance 33. There are 1,350 targets on this first shell; 66 satisfy the
  bilinear equation, and an exact enumeration proves that none can also meet
  both ordinary/alternating margin norm identities.
- An explicit distance-34 sign witness passes the complete primitive-eight
  equations, both margin norms, and every endpoint-quad product. Thus the
  strengthened necessary-condition bound is sharp.
- This closes the full seed ball through radius 33 without relying on CP-SAT,
  strictly superseding the earlier solver-backed radius-18 distance report as
  a local exclusion.
- Holding Eliahou's `s` fixed is independently impossible: its fixed `A,C`
  partial norm is `807+24*sqrt(2)>334`, before the nonnegative `B,D`
  contributions are added.
- Added both primitive-eight coefficient equations to the exact sharded
  CP-SAT model as redundant but strong propagation.
- The theorem and checker are in `VARIABLE_Q_ROOT8.md` and
  `variable_q_root8.py`.

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
  solver-backed computational claim. It remains an internal draft. Any
  release decision by the human user should wait for all 1,296 radius leaves,
  lawful public-source review of the inaccessible 2026 text if it becomes
  available, and independent expert review. The project will not initiate
  outreach.

## 23 July 2026: multiplier row-sum obstruction

- Summed all 37 column-lag equations in a fixed-compression, column-only
  multiplier quotient. For subgroup size `h`, transition matrices satisfy
  `D+h sum(M_j)=w w^T`; hence the complete length-nine row sum `s=x+h t`
  must have real PAF `(297,-37,-37,-37,-37)`.
- The zero-column divisibility condition leaves exactly the same 972 QPSK
  words for `h=18,9,6,3`. They form one free normalization orbit and all have
  nonzero real PAF `-1`, so the canonical zero word is fixed without loss.
- Completed the exact nonnegative integer projection. The order-18 family has
  no energy state. The order-9/quartic family has 40 canonical states and 29
  PAF profiles, none targeted; over all zero cores it has 38,880 states and
  zero hits. The order-6/sextic family has 2,376 canonical states and 971
  profiles, none targeted; the all-core replay has 2,309,472 states and zero
  hits. These are complete restricted-family obstructions, not solver
  outcomes. The former quartic and sextic searches are now historical only.
- Retained `verify_lp333_multiplier_row_sum.py`,
  `test_lp333_multiplier_row_sum.py`, and
  `LP333_MULTIPLIER_ROW_SUM.md`. Six focused tests pass, including an
  independent `Phi_3` shell derivation for the already closed sextic family.

## 23 July 2026: exact order-three boundary

- At `h=3`, the row-sum projection is viable. A warning-clean C++20
  enumerator checks exactly 46,503,026 energy-and-sum words and finds 1,756
  full row-sum PAF words. Regeneration took 8.60 seconds and 2,818,048 bytes
  maximum RSS with no swap. The emitted 1,757-line catalog has SHA-256
  `e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea`
  and reproduced byte-for-byte.
- Complementing each high-weight binary class word turns a zero-column lift
  into four groups of six triples on `Z/9`. Signed incidence equations encode
  the aggregate row sums, and the zero-column PAF equations are exactly the
  four difference totals `18,18,18,18`. A frozen 24-triple witness passes
  compression, row sums, and all zero-column equations.
- Expanded that witness through all 333 coordinates. It fails 51 of 54
  reversal-independent nonzero-column equations, with residual energy 8,320
  and maximum absolute residual 30; all six geometric column-axis equations
  fail. It is explicitly a pure-axis lift, not an `LP(333)` candidate.
- Recast the 24 labeled blocks as four 84-entry multiplicity histograms and
  audited all 1,756 catalog rows. Every row is feasible; there are zero
  infeasible and zero unresolved cases. The full independent replay took
  168.09 seconds, 114,081,792 bytes maximum RSS, and no swap, with coverage
  digest
  `b32aa9116098ea455063d256b37541033d3a9f8eb6ff5e32f57c3d7039fb1049`.
  Thus strengthening only the row-sum and zero-column layer cannot prune the
  order-three catalog.
- Implemented a dedicated exact `9 x 13` quotient and dependency-free save
  gate. The quotient has 216 primary signs and 58 reversal-independent lag
  equations. The baseline model has 11,790 variables and 11,657 constraints.
  A full lex leader for the commuting `C6 x C2` action raises this to 11,857
  variables and 11,889 constraints. The corrected B-only affine involution
  is `B'[n]=B[323n+111]`; the plausible class-fixed multiplier 260 is false,
  changing 264 PAF lags on the frozen pure-axis witness. All 26 combined
  focused tests and the dependency-free symmetry verifier pass.
- A 60-second four-worker pilot of the full corrected model ended `UNKNOWN`
  with no candidate after 32,600 conflicts and 293,875 branches. It used
  390,365,184 bytes maximum RSS with no swap. This is a bounded diagnostic
  only and makes no feasibility or infeasibility claim. Every solver
  assignment must replay all 333 correlations and the complete bordered
  `668 x 668` matrix before any candidate can be written.
- Factored the modulo-three row compression into two independent ten-state
  binary profiles per class. Their nontrivial Fourier coefficients lie in
  `Z[omega]`, with norm census `0^1,3^6,9^3`, and the full compressed system
  is exactly `a*a^*+b*b^*=167 delta_0` for two `H`-invariant Eisenstein
  sequences on `F_37`.
- Proved that seven of the 20 reversal-independent real equations are
  fixed-sum dependencies. The exact system therefore has one real origin
  equation and six complex class equations, or 13 integer conditions. The
  1,756 row-sum words collapse to 22 aggregate shards with norm-pair census
  `(19,148)^4,(28,139)^4,(64,103)^2,(91,76)^8,(100,67)^2,(163,4)^2`.
- Reduced each opposite-class block modulo the ramified prime
  `1-omega`. Its three signatures have multiplicities 34,33,33, leaving
  `34^2+33^2+33^2=3,334` of 10,000 local choices. Explicit pinned witnesses
  show all 22 aggregate shards survive after adding the origin energy, so
  the sieve is exact but nondecisive. The verifier and five tests pass below
  29 MB RSS with no swap.
- An optimized 1,344-variable, 1,287-constraint pilot of the 13-condition
  model ended `UNKNOWN` after 120.024 seconds with no assignment, 387,475
  conflicts, 708,771 branches, and 188.5 MiB maximum RSS. No mathematical
  conclusion is drawn from that bounded run.

## 23 July 2026: primitive-nine and coupled order-three boundaries

- Expanded the `<10>` quotient at the primitive ninth root in
  `F_3[pi]/(pi^6)`, `pi=1-zeta_9`. The canonical zero-column reciprocal power
  is 5 and `v_pi(167-5)=v_pi(162)=24`. This yields six exact triangular jet
  equations modulo three.
- Proved by exhaustive local replay that jet digit one is exactly the
  3,334/10,000 Eisenstein opposite-pair sieve. Digits two through five retain
  within-residue placement and introduce nonzero/nonzero class products. A
  pinned aggregate/origin/local-pair survivor has nonzero-lag residual census
  `(0,0,18,24,30,24)` and first fails digit two, proving strictness. No
  row-sum catalog exclusion is claimed. The verifier and five tests pass
  below 22 MB with no swap.
- Derived a common outer theorem for the coupled multipliers 121 and 211.
  Their invariant row sums satisfy a positive-definite five-value equation:
  36 Gaussian repeated-row pairs reduce to 12 realizable pairs, 6,048 generic
  row words, and 1,296 words compatible with the invariant zero column and
  all fixed margins.
- The 1,296-word catalog has SHA-256
  `4c03c95355e161dca2bca94c635f377f73ec069baf36aa1be8143fd351ea2965`,
  216 free row-dihedral orbits, and 108 extended equivalence classes. An exact
  21,953-state DP proves every word lifts through both zero-column-lag LP
  equations. A nonadditive column-orbit exponent reversal bijections the
  121/211 spaces through margins, row sums, and the zero-column axis only.
  The verifier and five tests pass below 94 MB with no swap.

## 23 July 2026: first paired-lobe dyadic root sieves

- Joined the even and odd carrier groups at roots `+1,-1`. In the
  arbitrary-placement relaxation, 46 new map/profile rows are impossible,
  representing 2,576,920 of 1,864,410,112 weighted inventory-map products
  (0.1382%); no whole surviving core/profile cell is removed.
- In the narrower vertical-pair slice, roots `+1,-1` reject 830,528 of
  23,823,872 inventory/core products. Adding `Phi_4` rejects 75,713 more, for
  a cumulative 906,241 products (3.8039%) and eleven complete cells. The
  3.8039% figure applies only to vertical placement.
- Both retained standard-library verifiers and focused tests pass with zero
  swap. The roots `+1,-1` replay peaked near 712 MB; the `Phi_4` replay peaked
  at 499,613,696 bytes. Work stopped before `Phi_8` and `Phi_16`.

## 23 July 2026: adjacent-42, characteristic-37, and primitive-eight lifts

- Folded all four published base rows modulo `z^42-1`. The thirteen nonzero
  seed residuals cancel in four exact triples plus the lag-42 energy term,
  leaving a periodically flat fold of energy 14. An exact `BS(84,83)` has
  folded energy 334.
- Across the four rows there are 166 separation-42 pairs and two singleton
  signs. If `E` pairs have equal endpoints, the folded energy is `2+4E`.
  The target therefore needs 83 equal pairs, while the seed has three. This
  proves an exact base-row Hamming lower bound of 80.
- Translating the bound into special `(s,q)` coordinates gives distance at
  least 40. Equality would keep `q` fixed and is excluded by the completed
  `TU(41)` reduction, so the true special-coordinate bound is 41. The
  complete distance-41 cost split has zero, one, or two `q` changes. Fixed
  `q` is closed, the unique one-`q` center case is impossible at `z=-1`, and
  the remaining case is exactly two reciprocal `q` flips plus 39 `s` flips.
- Exactly 80 reciprocal pairs are compatible with the minimum base shell.
  Roots `+1,-1` leave 39 pairs, each with two joined ordinary/alternating
  profiles. The complete base-distance-80 adjacent-42 condition is an
  80-sparse ternary group-ring equation on `C_42`. The reciprocal-skeleton
  shell coefficient is reproduced by
  `(1+12t^2+8t^4)^39(1+6t^2)(1+2t^2)(1+4t^2)`.
  The dependency-free verifier and five tests pass below 25 MB with zero
  swap.
- Reduced the order-three Eisenstein group ring modulo 37. Since
  `x^37-1=(x-1)^37`, the truncated logarithm `x=exp(u)` turns inversion into
  `u -> -u`; `H`-invariance leaves only powers of `v=u^3`. The resulting
  13-dimensional transfer matrix has rank 13 and determinant 11, making the
  degree-twelve norm identity equivalent to all invariant mixed equations
  modulo 37.
- A direct 373-fixture audit checks 4,476 physical/cyclotomic equations.
  Explicit witnesses prove that all 22 aggregate shards survive the joined
  aggregate, norm-54, local mod-three, and first two characteristic-37
  coefficients. Every pinned witness fails six, eight, or nine of the later
  coefficients, so no candidate is implied. The verifier and three tests
  pass below 28 MB with zero swap.
- Extended the distinct-lobe vertical-pair slice through a primitive eighth
  root. The completed evaluation `E+zeta_8 O` yields one rational norm and
  one exact `sqrt(2)`-coefficient equation. Independent monomial replay
  checks 2,048 carrier cases and all 512 hole evaluations. The 768,512
  inventories refine to 87,695 five-coordinate feature classes.
- At core 27, `Phi_8` cuts 229,408 prior survivors to 65,868. At core 4 it
  cuts 724,564 to 140,007. The new rejection rates are 71.2878% and
  80.6771%. Both are vertical-pair-only necessary filters. The core-27 run
  used 2.82 GB maximum RSS; the larger core-4 relation used 3.87 GB. Both
  recorded zero swap, and all four focused tests pass.

## 23 July 2026: anti-fold certificate and exact labelled order-three lifts

- Reduced the base-sequence norm modulo `z^42+1`, complementary to the
  adjacent-42 sum fold. On the special-distance-41 shell, flipping either
  endpoint of a seed-opposite separation-42 pair zeros the same anti-fold
  cell. This removes all `2^39` endpoint orientations from the first stage.
  The 39 reciprocal-`q` pairs collapse to 30 distinct binary support
  instances: 21 long and nine mirrored short instances.
- The seed anti-fold has energy 654 and the exact target has energy 334.
  After the reciprocal `q` pair and 39 support cells are removed, zero-lag
  energy is automatic and the remaining problem is exactly 20 independent
  negacyclic correlation equations.
- Pair-sum/pair-difference normalization gives an exact first affine lift
  over `F_2`. Including support-weight parity, all 39 reciprocal-`q` cases
  have rank 21: 38 systems have 78 variables and one has 79. Exact
  MacWilliams counts leave tens of quadrillions of target-weight words in
  representative affine codes, so the lift is a solver reduction rather
  than an exclusion.
- Canonical anti-fold case 0, the long `q` representative 0, is certified
  UNSAT. Its 39,580-variable, 127,589-clause CNF has SHA-256
  `f3eb29b1ea9c386e53b03726349fe0c38577d7e187b56aa19f86412c8749755d`.
  Standalone CaDiCaL 3.0.1 solved it in 200.17 seconds at 163.9 MB peak RSS.
  The 90,490,737-byte compressed binary DRAT proof has SHA-256
  `efd8abd9d80d50365822754f36345f368d7cff8f2740ca33b9cab7d5866aa519`
  and passed independent `drat-trim` replay in 75.00 seconds at 471.1 MB.
  `verify_eliahou_antifold_q0_proof.py` audits metadata, hashes, DIMACS shape,
  and optionally the full proof.
- Canonical case 1, the long representative 2, has one solver-UNSAT
  observation but no checked proof. The other 28 distinct support instances
  are `UNKNOWN`. Exactly one of 30 instances is therefore excluded; no
  complete distance-41 exclusion, `BS(84,83)`, or `H(668)` is claimed.
- Completed the fully labelled primitive-nine algebra split
  `F_3[C_37]^H ~= F_3 x F_729 x F_729`. Column negation is the third
  Frobenius iterate in both field factors. A pinned row-695 lift passes all
  222 modular jet equations and four exact row-direction equations, proving
  that the labelled modular sieve has at least one survivor and zero
  certified catalog exclusions.
- Parameterized the upper three primitive-nine digits by 54 placement trits
  for the pinned row-695 profiles. Their affine system has rank 18 and
  nullity 36 before exact margins and correlations. A reduced model produced
  a second fully labelled modular certificate, independently replayed
  through the same 226 equations. These rank values are profile-specific.
- Replaced the modular primitive-nine shadow by its exact integral criterion.
  Divisibility by `Phi_9=x^6+x^3+1` is equivalent to equality of correlation
  counts at row lags `s,s+3,s+6`. Both modular certificates fail all 36
  nonzero column-class/residue groups; their defects are divisible by three
  but not zero. This proves strictness of the integral layer on the pinned
  lifts, not infeasibility of row 695.
- These labelled and integral layers complement the already verified
  characteristic-37 logarithmic transfer. None of them currently removes a
  row-sum catalog entry or constructs an `LP(333)`.

## 23 July 2026: profile ideal and three-fiber phase factor

- Extracted the placement-independent part of exact primitive-nine
  equidistribution.  At each nonzero column class, the profile Fourier
  coefficient must lie in `3(1-omega) Z[omega]`, an Eisenstein ideal of norm
  27. Reversal gives six displayed conjugate-pair tests; the aggregate
  moment supplies one global dependency, leaving five independent ideal
  trits. Passing the ideal uniquely reconstructs the full `12 x 3` exact
  periodic-correlation target table.
- All 22 profile assignments retained by the characteristic-37
  two-coefficient checkpoint fail the new ideal test. A separate complete
  certificate corpus then found and exactly replayed one alternative passing
  profile tuple for every aggregate shard. The replay checks 132 local
  opposite-class conditions and 264 displayed ideal conditions. Thus the
  ideal is a strict assignment filter but excludes zero of the 22 shards.
  The profile corpus, correlation-table, and reconstructed-target hashes are
  respectively
  `92fbf448260334f3e4a9b7d1cfb82046d3cb5043721bd5fcb09fbcb4aeaab43f`,
  `27a3fc0c11e745e05e3da8ca273cde3535419009e78cb2ce34ca83fc074b1a78`,
  and
  `e7d395500053eeb4346260d545affbb1baea35f01a6793ef48d6b3a3ee9c8628`.
- Split each nine-row class word into three `C_3` fibers. A fiber of size one
  or two has a signed cube-root Fourier value. For every profile composition,
  `active=3-Norm/3`; summing over 24 profiles of total norm 54 proves that
  every viable tuple has exactly 54 Eisenstein unit phases. Threefold column
  expansion plus five fixed zero-column units makes frame energy 167
  automatic. Expanding in the cubic basis of
  `Q(zeta_9)/Q(omega)` reduces the remaining exact primitive-nine equation
  to two independent group-ring identities: the complementary frame and one
  directed cross-fiber equation. The third displayed component is
  `omega^2` times the adjoint of the second.
- Exact replay against both labelled modular certificates checks all 37
  physical column lags and the direct integer correlation tables. Both have
  167 active physical fibers and nonzero coefficients in all twelve
  nonzero invariant classes of all three components, so neither is an exact
  survivor. Four focused phase-factor tests pass below 17 MB RSS.
- Replayed the compressed anti-fold proof again through a regular
  decompressed binary DRAT file. `drat-trim` returned `VERIFIED` in 78.353
  seconds at 458,539,008 bytes maximum RSS. This independent rerun confirms
  the packaged case-0 theorem; it does not enlarge its one-of-30 scope.
- No exact `LP(333)`, `BS(84,83)`, or Hadamard matrix of order 668 has yet
  been constructed.

## 23 July 2026: exact full-LP profile zero gate

- Corrected the continuation scope after the primitive-nine ideal audit.
  For two length-333 sign sequences of sum one, the Legendre target `-2`
  is equivalent to combined plus-support intersection 167 at every nonzero
  lag. After the standard origin subtraction, all nine row-lag coefficients
  at every `C_37` lag are therefore 167. Their order-three Fourier moment
  is exactly zero.
- This moment is the profile correlation `D_t` already reconstructed by the
  Eisenstein channel. Thus a full `LP(333)` requires `D_t=0` on all 13
  column parts. Membership in `3(1-omega) Z[omega]` is strictly weaker: it
  only makes the primitive-nine target triple integral.
- Applied the exact zero gate to all 22 ideal-compatible profile witnesses.
  One tuple has nonzero `D_t` on ten nonzero classes and the other 21 fail
  on all twelve, for 262 nonzero class moments. The compact certificate hash
  is
  `d0e496d2a2b01ed5432e4ff89c2a306a778a52cac08cebd22aa60292588a9060`.
- Catalog row 695 lies in aggregate shard `(1,-1,2,-2)`. Its original pinned
  profile and alternative same-shard ideal-witness 8 both fail `D_t=0` on
  all twelve nonzero classes. The original-profile certificate hash is
  `e22de237bf4a6e3b61d7bd31aff2bad9d7126fd8739b5ab503f75ca52c758621`.
- These are 22 exact fixed-profile exclusions and zero aggregate-shard
  exclusions. The correct next finite search is for different profile
  tuples satisfying `D_t=0`; only such a tuple merits a 54-trit phase lift.
- Collapsed the trivial `C_37` character of the six phase sequences to
  `(energy,cross term)` per channel. A dependency-free comparison with the
  pinned 1,756-word row-sum catalog agrees object-by-object and with exact
  assignment multiplicities on all 22 diagnostic tuples and row 695. Thus
  this is a useful phase-coordinate transfer, not a new obstruction. It
  reduces the diagnostic `3^54` spaces to 22--87 transfer signatures and
  45--98 catalog rows before nontrivial column-character equations.
- Reduced the first placement-dependent `1-omega` digit of the exact phase
  equations to a 20-row affine system over `F_3`. Twenty-one diagnostic
  tuples have rank 18 and nullity 36; fixed-profile witness 3 has ranks
  `(16,17)` and an explicit two-row contradiction. The result is subsumed on
  this corpus by `D_t != 0`, but the affine formulation is reusable.
- Enumerated the diagonal-frame augmentation and first characteristic-37
  coefficient by six separable sequence summaries. The largest sequence
  table has 444 states and the largest joined table 666; all 22 diagnostic
  tuples survive, with exact pinned counts and result hash
  `443d0e733f5c383d5d5ed14d5ec98b458becf9d7dd9e64c08d9d07c2b625a81a`.
  No second coefficient or complete diagonal frame is claimed.

## 23 July 2026: exact local-global and prime-167 profile closures

- Combined the primitive-nine lambda-cube ideal with the complete
  characteristic-37 transfer.  On energy 167, every correlation has norm at
  most `167^2=27,889`, while a nonzero element of
  `37(1-omega)^3 Z[omega]` has norm at least 36,963.  The two finite modular
  layers are therefore equivalent to exact `D_t=0`.  The third lambda digit
  is the first one sufficient for this universal norm argument.
- Found a broader single-prime closure.  If an energy-167 Eisenstein
  autocorrelation is divisible by 167, equality in Cauchy would make the
  nonzero order-37 translation act by an Eisenstein unit.  The unit must be
  one, making every sequence constant and the energy divisible by 37, a
  contradiction.  Thus exact complementarity is equivalent to its complete
  reduction modulo 167.
- Factored the order-three invariant modular algebra as
  `F_(167^2) x F_(167^12) x F_(167^12)`.  The exact checker proves both
  degree-18 factors, the two six-dimensional invariant period spaces, the
  star exponents 5 and 7, inverse CRT round trips, and all four branches of a
  complete two-channel solution parameterization.  All 22 pinned profile
  tuples fail the modular equation, agreeing with exact replay.
- Proved that none of those four ambient branches can lie on the boundary
  for a physical profile-zero pair.  `Phi_37(X+1)` is Eisenstein at
  `7+3 omega`, so every primitive complex Fourier value is nonzero.  Its
  absolute norm in `Q(omega,zeta_37)^H` is a product of twelve numbers
  strictly between zero and 167, hence is a positive integer below
  `167^12`.  Each of the two primitive residue primes has norm `167^12`, so
  every channel coordinate has prime valuation zero.  The trivial
  coordinates are units as well.
- Reparameterized the surviving modular locus by the unitary ratio
  `U=A B^(-1)`, `U U*=-1`.  For a fixed aggregate target the primitive
  locus is the single torus `(x_A,x_B,tau) in (F_(167^12)^*)^3`, of size
  `(167^12-1)^3`; the removed degenerate/axis boundary has
  `(2*167^12-1)^2` points.  The dependency-free verifier also pins the seven
  exact profile type sectors coming from
  `X(X^3-27)(X^6+27)`.  Its master certificate is
  `a8f551c9c7933f17178d7f63e2df78871b393462d890ccba9753bdc74bcae6ac`.
  This is a search reduction, not a profile survivor.
- Certified the formal profile symmetry
  `C6 x C2_A x C2_B`, of order 24.  The 22 aggregate targets form seven
  formal orbits.  With the complete canonical zero words fixed, only the
  B-star is affinely transportable, so labelled lifting has twelve target
  orbits.  An exhaustive termwise checker now verifies 2,200,368 local
  correlation monomials, making the covariance certificate universal over
  the full finite profile alphabet.
- The independent audit found no blocking mathematical error.  It classed
  prime-167 exactness as the strongest new order-three theorem, retained the
  CRT, Hensel, diagonal-prefix, transfer, and symmetry packages with their
  narrower scopes, and emphasized that no package excludes a whole aggregate
  shard or constructs an `LP(333)`.
- Repository and filename searches found no draft messages, recipient lists,
  or outreach files to delete.  At that audit point this task had sent and
  pushed nothing.  A later concurrent workspace workflow pushed the shared
  branch while archiving unrelated Ramsey artifacts; this task did not
  initiate that push and did not attempt a destructive remote rewrite.
  Further H(668) work was isolated on the local, no-upstream branch
  `codex/h668-local-only`.  External contact remains prohibited.
- The first-generation resumable 24-profile constructor used aggregate,
  energy, opposite-pair, lambda-cube, and all 13 characteristic-37
  constraints.  A 45-second workflow pilot made four exact subdivisions,
  leaving 37 disjoint pending cubes, zero candidates, and zero infeasible
  cubes.  That pilot only validated resumption and has no negative meaning.
- Replaced that model by a hardened constructor enforcing the six
  reversal-independent integer equations `D_j=0` directly in the sharp
  `[-192,192]` box.  Its four-profile tables have 3,334 exact legal rows and
  1,409 coarse states; all 132 off-diagonal product tables are materialized.
  Full fixed-target stabilizers, semantic source/dependency/table
  fingerprints, persistent exact no-goods, formal and lift-compatible orbit
  output, and three independent exact survivor replays make the discovery
  workflow safely resumable.  Every loaded survivor is replayed before it can
  become a resumed no-good, closing a checkpoint-corruption hole, and the
  fingerprint includes the full operational replay dependency closure.
  Eighteen tests and the constructor self-test pass below 140 MB.  No long
  hardened solve has been run, and CP-SAT exhaustion alone is not accepted
  as an infeasibility proof.
- Audited a prime-167 meet-in-the-middle alternative before implementing it.
  The three ordered opposite-pair signature buckets have sizes `34,33,33`,
  so a legal four-profile quartet has 3,334 choices.  A balanced three-plus-
  three quartet split has `3,334^3=37,059,263,704` injective half signatures
  and would exceed 151 GiB for identifiers alone.  A channel-first split is
  low-memory—half lists at most 39,304 and collision cells at most
  2,105,586—but still requires 6,338,555,429 degree-12 field signatures
  across the seven formal targets.  The 729 local-signature patterns have
  exactly 125 `C6` orbits.  This is a rigorous fallback/barrier audit, not a
  practical primary constructor, so no speculative implementation was kept.

## 23 July 2026: lossless prime-167 full phase algebra

- Extended prime-167 exactness from ordinary complementarity to both
  independent phase-frame equations.  The diagonal Cauchy equality support
  orbits have length 37.  The directed cross operator has three-cycles at
  zero column lag and 111-cycles otherwise because its fiber twist satisfies
  `P^3=omega^2`.  Total support 167 is a multiple of none of these lengths,
  so modular vanishing is equivalent to exact vanishing coefficient by
  coefficient.
- In the existing `F_(167^2) x F_(167^12)^2` invariant split, the three
  primitive equations are exactly `x` orthogonal to the span of
  `z,bar(P)z,bar(P)^2z`.  This span has rank at most three, giving an
  explicit at-least-three-dimensional annihilator for fixed minus spectral
  data.
- Recombined the three fiber sequences at a primitive ninth root.  Since
  `ord_9(167)=6`, the coefficient field is `F_(167^6)`, and the complete
  invariant algebra is
  `F_(167^6) x F_(167^12)^6`.  The six primitive factors form three star
  pairs with Frobenius exponents 3 and 9.  All 39 prime-field component
  conditions are one Hermitian norm cone over `F_(167^6)/F_(167^3)` and
  three bilinear cones over `F_(167^12)`.
- Mechanically partitioned all 36 nonzero character exponents into six
  factor orbits, proved rank 13 on the origin plus twelve class-indicator
  basis, checked star on all 13 basis words, and pinned the exhaustive
  degenerate/nondegenerate branch counts.  The verifier now also checks the
  coefficientwise bridge
  `sum_X W_X W_X^*=E0+alpha E1+alpha^2 omega^2 E1^*` directly and exercises
  a generic recovery together with both nondegenerate axis cases.  An
  independent audit found no mathematical defect.  Both Python runtimes
  reproduce the corrected hash
  `765e4631c4142b778c4c05eb4fe4220a23f06fd2198cf05d7ac2cf8dfc0463f1`;
  verifier and six tests stay below 31 MB maximum RSS.
- This parameterizes the entire finite modular norm cone but does not solve
  its sparse zero/unit inverse-CRT intersection.  No phase assignment,
  `LP(333)`, or `H(668)` is claimed.

## 23 July 2026: primitive support of the six phase fibers

- Proved for every zero/unit phase fiber that
  `U_i=0` if and only if either prime-167 primitive coordinate is zero.
  Irreducibility of `Phi_37` over `Q(omega)` first rules out a primitive
  complex zero for a nonzero word.  The diagonal frame and five fixed
  nonzero fibers then make all twelve conjugate energy factors strictly
  smaller than 167.  Either residue-prime vanishing would make their product
  divisible by `167^12`, contradicting the strict norm gap.
- The two primitive vectors consequently have the same zero support.  Since
  `A0,A1,A2,B1,B2` are nonzero already at the fixed zero column, only two of
  the `4^6=4096` ambient joint support patterns remain: the dense pattern and
  synchronized zero at `B0`.  Rank one requires the zero set to be a union
  of the two fiber three-cycles, so the `B0`-zero branch has plane rank at
  least two.  Dense rank-one points remain algebraically possible.
- Independent mathematical and PARI audits found no defect.  The verifier
  and five tests pass under Python 3.9.6, 3.12.13, and 3.14.6 below 26 MB
  combined peak RSS, reproducing certificate
  `c15e8357dc55e49f63469888dc306113165cf39c0cfc19b66aec15c747b2669e`.
  This removes 4,094 support patterns but does not produce a physical phase
  point, `LP(333)`, or `H(668)`.

## 23 July 2026: prime-163 extreme-sector obstruction

- Isolated the extreme energy allocation in the two aggregate targets
  `(4,-1,0,0)` and `(5,1,0,0)`, whose trivial-character norm pair is
  `(163,4)`.  Zero profile energy in the second channel forces
  `B=2 delta_0`, reducing exact complementarity to
  `A A^*=163 delta_0` with `A(0)=-1`.
- Factored 163 explicitly in `Z[omega]` as
  `(14+3 omega)(11-3 omega)`.  Since `ord_37(163)=36`, both factors are
  inert through the degree-12 quotient
  `Q(omega,zeta_37)^H/Q(omega)`.  The two primes above 163 are therefore
  principal of absolute norm `163^12`; no class-group computation is
  needed.
- Ideal factorization and Kronecker's theorem force
  `A(zeta_37)` to be a sixth root of unity times one of the two displayed
  Eisenstein primes, hence to lie in `Q(omega)`.  All 36 nontrivial Fourier
  values are then constant.  Fourier inversion would require
  `S+36q=-37` with `|S|^2=|q|^2=163`, contradicting the exact inequality
  `35^2*163=199675>37^2=1369`.
- A dependency-free multiplicity DP counts 1,151,042,580 aggregate-and-
  energy profile words per target before the opposite-pair sieve and
  exactly 1,617,192 after it.  The theorem removes all 3,234,384 such local
  survivors.  Explicit nonextreme local witnesses with physical energies
  `(37,130)` remain in both targets, so no aggregate shard is excluded.
- An independent PARI/GP 2.17.4 audit reconstructs the degree-24 field,
  finds two primes with `(e,f)=(1,12)`, matches them to the explicit
  principal generators, and finds six roots of unity below 29 MB RSS.
  The dependency-free verifier and five tests reproduce master hash
  `631649252c20db62a2bd0b2200c588708b07b9eb94fa350b73cd7f3c3865f191`
  with Python 3.14.6 and the project environment's Python 3.12.13, staying
  below 35 MB RSS.

## 23 July 2026: sparse-\(B\) relative-norm screen

- In the two aggregate targets `(5,1,0,0)` and `(4,-1,0,0)`, normalized
  `B`-profile energy six and aggregate zero force exactly two opposite
  norm-three coefficients:
  `B=2+z(eta_i-eta_j)`, `Norm(z)=3`.  This gives 396 distinct words,
  partitioned into 34 lift-compatible `C6 x C2_B` orbits and 17 larger
  field-norm types.
- Proved uniformly that `gamma=167-BB*` is totally positive using
  `(2+6 sqrt(3))^2<167`.  Exact complementarity would make `gamma` a norm
  from the quadratic CM extension.  Degree-one primes of the real field
  above 11 and 101 are inert in that extension, so an odd local valuation
  is impossible for a norm.
- Exact evaluations modulo `p^2` find such a simple valuation for 13 of the
  17 field types: twelve at 11 and one additional type at 101.  They account
  for 312 raw words and 26 lift-safe orbits.  Four types remain:
  `(d,z)=(1,-1-2 omega),(3,-2-omega),(6,-2-omega),`
  and `(6,-1-2 omega)`, totaling 84 words and eight lift-safe orbits.
- An independent PARI/GP replay reconstructs the real degree-12 field,
  verifies all ideal valuations, and returns quotient one in the guaranteed
  cyclic relative-norm test for all four survivors.  The GP run uses about
  81 MB RSS with no swap.  Python 3.9.6, 3.12.13, and 3.14.6 reproduce the
  dependency-free certificate
  `6920db3a6912ad854e0af57562a0e61cd1a1966cb1ed91f8954bd520d4722f5d`.
  The 84 survivors still need a physical complementary `A`; the energy-six
  sector, both targets, `LP(333)`, and `H(668)` remain open.

## 24 July 2026: exact exclusion of the two sparse profile shells

- Partitioned the 24 profile letters by Eisenstein norm as
  `(n_9,n_3,n_0)=(h,18-3h,6+2h)`.  Exact enumeration of all 10,000 labelled
  opposite quartets leaves 3,334 legal rows and shows that a quartet contains
  `0,2,3`, or `4` norm-three letters, never exactly one.
- For `h=5`, all three norm-three letters therefore occupy one quartet.
  Every norm-nine coefficient lies in `3 Z[omega]`, so high-high cross terms
  vanish modulo 9 and the other five quartets become independent after the
  distinguished frame is fixed.  Of 34,634,136 aggregate/local candidates,
  only 552 reach detached exact replay.
- For `h=6`, modulo 9 localizes each quartet's self term to its own reversal
  pair.  Of 1,653,840 aggregate/local candidates, only 288 reach detached
  replay.  None of the 552 or 288 words has all nonzero physical
  correlations zero.  The pinned certificate hashes are
  `e917360e36cbf57b96e5f0a8d842017eaeab9a73c4cdff804bdad719d898090e`
  and
  `981f1a39c7858271e9588b7606dece1c6d408b31506381c71eecc9dbc85d410e`.
- An independent audit re-enumerated the complete quartet catalog, reproduced
  every aggregate count by a separate weighted DP, checked the 22-target
  table against its upstream catalog, replayed all 37 physical lags,
  reproduced both hashes externally, and passed warning-clean,
  ASan/UBSan, Python 3.9, and Python 3.14 runs.  Normal peak RSS was 63 MB.
- The resumable exact constructor now maps every profile ID to a norm-nine
  flag and enforces the proved cut `n_9<=4`.  Its theorem verifier is included
  in the semantic checkpoint fingerprint; 19 constructor tests pass.  Five
  profile sectors, the labelled lift, `LP(333)`, and `H(668)` remain open.

## 24 July 2026: exact profile-shell descent and physical cone decoders

- Excluded the norm-nine endpoint profile shell
  `(n_9,n_3,n_0)=(6,0,18)`.  The zero-column incidence condition reduces
  each opposite quartet from 256 high/zero states to 40.  Exact aggregate
  and count leave 288 assignments in twelve full profile-symmetry orbits;
  detached integer replay rejects every assignment, with bad-class
  histogram `10:24, 12:264`.  The pinned certificate is
  `addf4ad655ca1ca16eaef5aebf8787eb14e8a56676e73e05f68e905fc9f45b5a`.
- Excluded the adjacent shell `(5,3,16)`.  The universal quartet table has
  no state with exactly one norm-three letter, so all three such letters
  lie in one quartet.  Fixing that medium frame makes all six
  reversal-independent correlations affine in the five norm-nine letters
  modulo nine.  A complete additive join reduces 34,634,136 aggregate/local
  assignments to 552, all rejected by 20,424 detached physical-lag replays.
  The bad-class histogram is `6:24, 10:144, 12:384`; certificate
  `51c25095c92ba49c4c7c493373bb68f7d9c0c4671d65490413ae140c2b0aad69`.
- Excluded `(4,6,14)` by a new support/phase split of the affine
  modulo-nine equations.  Legal medium counts per quartet are
  `0:1, 1:0, 2:108, 3:216, 4:486`, so the six medium letters have only the
  distributions `2+2+2`, `3+3`, and `4+2`.  The coordinate sum of `D/3`
  is a phase-free local high-support flag; all high/medium terms lie in its
  one-dimensional kernel, and an occupied quartet's high phases span that
  kernel.  A streaming verifier checks 27,468,720 oriented medium frames,
  115,033,608 high-support leaves, 12,835,512 phase solutions, and 345,984
  exact-aggregate modulo-nine survivors.  Exact 37-lag replay rejects all,
  with histogram
  `4:204, 6:1860, 8:16884, 10:96192, 12:230844`.
- At this stage these three independent shell theorems strengthened the exact
  profile constructor from the energy-only bound `n_9<=6` to `n_9<=3`.
  The later shell-three theorem strengthens it again to `n_9<=2`.  The
  checkpoint and survivor schemas were advanced to `v5`,
  and all theorem sources are included in its semantic fingerprint.
- Removed the zero branch of the trivial prime-167 phase cone.  If either
  channel coordinate
  `c_X=sum_r m_(X,r) alpha^r` vanished, irreducibility of `Phi_9` would make
  the nine margins repeat with period three.  Their integer range lifts the
  congruence exactly, contradicting total plus support 167.  The complete
  1,756-row catalog maps to 1,411 distinct nonzero coordinate pairs and
  1,411 distinct norm-minus-one ratios, versus `167^3+1=4,657,464` abstract
  ratios.  Certificate
  `50f3d0f090187ded04c9bce52cfb6900c451dd005d48e4db965046c8d71edb26`.
- Built an exact row-Galois and trace inverse for the four prime-167 cone
  blocks.  Three-by-three Vandermonde transforms recover all six original
  fiber CRT triples, and weighted `E/K` traces recover every physical class
  coefficient.  Parseval supplies twelve independent fixed-zero linear
  equations and six profile support forms; after the cone-supplied total,
  five profile-resolved equations remain as displayed cuts, without a
  codimension claim on the constrained locus.
- Replaced the local sparse-alphabet lookup by an if-and-only-if decoder.
  One proposed primitive ninth-root value supplies six Frobenius DFT
  channels, while weight and residue profile supply the remaining three.
  The word is physical exactly when all nine inverse-DFT values satisfy
  `b^2=b`.  Exhaustive weight-three and weight-six checks test 820
  value/profile pairs per branch and accept exactly the 84 physical words.
  The same certificate gives seven possible local norms and the cubic
  branches `t^3-6t^2+9t-3` and `t^3-9t^2+18t-9`.  Composite trace-sieve
  certificate
  `8253d73531cfbf4d5111c211b75da5abfdd8abeb11efc47973e49daedcc9b1e1`.
- Independently reduced the phase equation modulo seven:
  `Phi_9=(X^3-2)(X^3-4)` and every component splits into thirteen scalars
  over `F_(7^3)`.  Local phase coefficients remain injective with alphabet
  sizes 1, 9, and 27, and one factor has 40,353,264 compatible quadruples
  parameterized as an affine line.  A compact CP-SAT multiplication layer
  needs only 234 scalar 49-row tables.  The accompanying audit rejects raw
  trellis, balanced MITM, additive Wagner, and alphabet-independent
  one-factor BCH architectures as primary decoders.  Corrected certificate
  `0605563ad589018e39ac73a41ecf880c678f38ad6941730b9dd7fcb2e33e84cf`.
- Independent audits and focused replays found no mathematical or
  completeness defect.  The largest new verifier used about 147 MB RSS
  (the CP-SAT constructor tests); the exhaustive shell-four theorem itself
  used under 4 MB.  No exact profile, `LP(333)`, or `H(668)` has yet been
  found.  Nothing was sent, contacted, pushed, or published.

## 24 July 2026: exact exclusion of the three-high profile shell

- Reparameterized every norm-three profile coefficient as a signed
  uniformizer `sigma*(1-omega)*omega^u`.  The opposite-quartet equation
  leaves 908,800 signed skeletons and 38,296 exact skeleton orbits in the
  shell `(n_9,n_3,n_0)=(3,9,12)`.
- For a fixed skeleton, every remaining medium-phase or high-letter
  correction is divisible by three.  Distinct correction products therefore
  disappear modulo nine, yielding a lossless additive signature join with
  exact aggregate coordinates.  Across 93,564 canonical-skeleton/target
  loops it checks 17,424,680 high supports and produces exactly 479,850
  modulo-nine/exact-aggregate survivors.
- Carrying the correction expansion one digit farther restores the quadratic
  cross terms modulo 27 and leaves exactly two near witnesses.  Their six
  independent exact correlations are nonzero multiples of 27.  A separate
  cubic characteristic-37 moment has values 33 and 23 on them, so neither
  can be exact.
- Detached integer replay was deliberately applied to all 479,850 modular
  survivors on all 37 physical lags and found zero exact profiles.  Thus
  `n_9=3` is excluded independently of the cubic moment, and the exact
  constructor may enforce `n_9<=2`.
- An independent audit recomputed the complete skeleton and target-orbit
  counts, exhaustively checked 5,514,624 locality/phase conditions, compared
  14,400 unary responses and 6,000 full flags to direct correlation, passed
  warning-clean and Python 3.9/3.14 regressions, and completed separated
  ASan/UBSan shards below 702 MB.  It found no arithmetic or completeness
  defect.
- The older `n_9=4` verifier was also replayed independently:
  27,468,720 frames, 345,984 modular survivors, zero exact profiles.  A
  compressed skeleton/MITM corroboration reproduces the same target counts
  and exact failure histogram in about 12 seconds; it is retained with an
  explicit shared-source caveat.
- Four of the seven profile-energy shells are now closed.  The exact
  mathematical frontier is `(n_9,n_3,n_0)=(2,12,10),(1,15,8),(0,18,6)`.
  No exact profile, labelled lift, `LP(333)`, or `H(668)` has yet been found.
  Nothing was sent, contacted, pushed, or published.

## 24 July 2026: five exact two-high profiles and dense quadratic algebra

- Completed the exact shell
  `(n_9,n_3,n_0)=(2,12,10)`.  Uniformizer descent leaves seven possible
  medium-support partitions.  A symmetry-reduced exact enumerator checks
  14,715,744 raw signed skeletons, 617,788 canonical skeletons, and
  10,201,038 exact replays.
- Exactly five profile-zero symmetry orbits survive, of sizes
  `24,12,12,12,24`.  One representative lies in partition `222222` and
  four lie in `422220`; `332220,333300,433200,442200,444000` are empty.
  This is the first shell in the descent with genuine exact profile
  solutions.
- Every representative passes detached all-37-lag Eisenstein replay, the
  exact aggregate and norm census, all local signatures, complete formal
  orbit reconstruction, the characteristic-37 gate, and the lossless
  prime-167 gate.  The complete semantic certificate hash is
  `36099444b32f88869557a6f510f06cfa3b6eaa7a876b26cf62a0796ca4232565`.
- All five representatives have 54 placement trits.  Their first
  placement-Hensel systems have coefficient/augmented rank `18/18` and
  nullity 36.  Exact trivial-character transfer leaves
  `72,72,72,96,93` compatible row-margin catalog rows.  They are profile
  inputs only; no labelled `LP(333)` or `H(668)` has been obtained.
- Built a secondary exact XOR/CP-SAT lift for the first representative.
  A five-minute four-worker run ended `UNKNOWN` after 1,674,513 branches,
  peaking near 604 MB with no swap.  A resumable five-second pass over all
  72 compatible row-margin shards also returned 72 `UNKNOWN`.  These runs
  establish an exact baseline and no mathematical exclusion.
- Independent Python 3.9 and 3.14 replays, warning-clean compilation, and a
  full ASan/UBSan partition replay passed.  The exact enumerator uses about
  4 MB resident memory; completeness comes from pinned finite counts, not a
  timeout.
- For the remaining `n_9=1,0` shells, reconstructed the six quadratic
  correction polar matrices over `F_3`.  They commute, generate
  `F_27 x F_27`, have projective rank census `12:338, 6:26`, and satisfy
  `M_0+...+M_5=2I_12`.
- After imposing the actual local-quartet and channel-aggregate affine
  rows, complete support-only censuses cover 510,384 masks at `n_9=1` and
  107,476 at `n_9=0`.  Exact quadratic Gauss bounds show that the radial
  combination attains every right-hand side at least 2,025 and 54,675
  times, respectively.  Thus it cannot exclude either shell.  The full
  six-coordinate layer can instead be counted by 729 exact character sums
  per skeleton and self-reduced to a witness.
- The dense verifier and independent warning-clean C++ audit passed below
  19 MB resident memory with no swap.  Nothing was sent, contacted, pushed,
  or published.

## 24 July 2026: complete second placement digit and 72-hour gate

- Reconstructed the next exact Eisenstein placement digit on all five
  shell-two profiles.  The first digit leaves an affine `F_3^36`; the next
  digit has twenty displayed quadratic rows, of which two origin rows vanish
  structurally and the remaining eighteen polar forms are independent with
  common radical zero.
- Exhausted all 3,588 projective combinations of support at most three.
  Exactly six have polar rank below 28.  They are the row-collapse forms
  `E0(b)+E1(b)+E1(27b)` for `b=1,2,4,8,16,32`, with ranks between 15 and 21.
- Identified those six forms as the residue layer of the ramified
  row-coordinate algebra
  `(F_27 x F_27) tensor F_3[epsilon]/(epsilon^3)`.  An independent
  factorization verifies the `F_27 x F_27` class algebra, the fixed-zero
  boundary terms, and explicit radical translations.
- Evaluated all 729 quadratic additive characters exactly.  On every
  profile, the six-coordinate map `F_3^36 -> F_3^6` is surjective; its
  zero-fiber sizes are
  `205891130500326,205891148037879,205891197461892,`
  `205891052378499,205891125717357`.  Hence one second-digit witness is
  expected to be abundant and is not evidence of convergence.
- Falsified the proposed free rank-two module lift over the ramified
  algebra.  The residue ranks exceed the required bound, the first
  nilpotent layer has common radical zero, odd polar ranks violate the
  unimodular norm spectrum, and the exact common self-adjoint centroid
  system has rank 1,295 in 1,296 variables on every profile.  Only scalar
  endomorphisms remain.
- The complete five-test regression passed under Python 3.9 and 3.14; the
  independent structured theorem has semantic hash
  `aa6dbb0c3272e8695e3c8beff8381702a9f7f5a2505716138086d8074aa20d5c`,
  and the module falsification has semantic hash
  `a09bcdb69480fb94c79e941db77c8081e8a5403b4472863c557db7c1f2d0ce58`.
- Began a 72-hour gated continuation.  Its required evidence is a structured
  exact family or contraction through at least two consecutive higher
  digits together with an end-to-end search estimate.  A lone
  second-digit SAT witness does not pass the gate.  No external contact,
  push, or publication occurred.

## 24 July 2026: current multiplier-literature audit

- Audited Ramos--Hulak--de Queiroz, arXiv:2607.20765, submitted 22 July
  2026, together with its public proof artifacts.  It proves that every
  fixed common-multiplier subgroup of order at least nine is impossible for
  `LP(333)` and also closes one order-four and one order-six subgroup.
- Mapped our column-only `h=18,9,6` lanes exactly to its paper IDs 20, 12,
  and 8.  Its conclusions are strictly stronger because they do not assume
  our prescribed fixed compression.  The local row-sum proofs remain useful
  as compact independent replays and as the front end of the `h=3` chain,
  but are no longer headline novelty.
- The active `<10>` subgroup is paper ID3 and remains open.  The other
  order-three subgroups `<112>,<121>,<211>` are paper IDs 2, 4, and 5 and
  also remain open in the full-family classification.  Corrected the local
  `<112>` language to claim only the fixed-compression exclusion.
- The five minimal proper common-multiplier supergroups of paper ID3 are all
  publicly excluded.  Any exact pair in our `<10>` lane must therefore have
  fixed common-multiplier stabilizer exactly `<10>`; structured searches
  must break every proper supergroup rather than adding more common
  multiplier symmetry.
- The companion mod-64 report already contains the basic Eliahou special
  lift/`BS(84,83)` equivalence and a raw-distance lower bound of 64.  The
  local distance-80 theorem remains a strict improvement, but the basic
  translation is no longer treated as new.  Generic fixed-field novelty
  language was likewise narrowed after checking the companion compression
  note.
- No second July 2026 binary-Legendre-pair or `H(668)` paper was located in
  the targeted audit.  The April 2026 Legendre-pair equivalence-group paper
  was added to the priority source ledger.  No external contact, message,
  push, or publication occurred.

## 24 July 2026: structured phase-family gate

- Exhausted four low-period placement controls on the five canonical
  shell-two orbit representatives.  Every first-digit point in them is
  fixed by the already excluded order-six common-multiplier subgroup.
- Exhausted three genuinely opposite-class-twisted families.  Their
  per-family supergroup-free first-digit counts are 2,916, 174,960, and
  1,458; none has a supergroup-free second-digit survivor.  The family sets
  overlap, so these counts are not summed.
- The sole structured second-digit control occurs in the opposite-helical
  family.  It is order-six fixed and fails five displayed equations at digit
  three.
- Independently reconstructed all 56 minimal three-dimensional invariant
  submodules of the `F_27 x F_27` class algebra.  All 3,136 asymmetric
  channel pairs per canonical representative were tested: 436 distinct
  first-digit points,
  six outside every excluded proper supergroup, and no second-digit point.
- The six-test package passed under the system Python and the pinned Python
  3.9 runtime.  A compatibility helper replaced direct `int.bit_count()`
  calls in the shared dense-shell verifier without changing its semantic
  replay.  Peak resident memory stayed below 32 MB.
- These are exact canonical-representative structured-family exclusions,
  not action-closed or whole-profile exclusions.  No external contact,
  push, or publication occurred.

## 24 July 2026: higher-digit and complete-search gate

- Certified one proper-supergroup-free placement through digits zero, one,
  and two.  The second-digit dimension heuristic predicts about `3^18`
  points per profile, so the witness is an instrument check rather than
  convergence toward `LP(333)`.
- Derived the exact coordinate identity
  `F=A+(3Q-A)omega`.  It makes exactness the signed-histogram condition
  `A=Q=0`, proves that digits zero through eight force exact zero, and
  exposes a nineteenth digit-three equation from the delayed `E1` origin
  row.
- Counted the delayed origin equation exactly: 30 admissible orientation
  histograms with total weight 596,095,200 among `3^22` orientations.
  Degree-three XL has rank 666 and produces neither a refutation nor a new
  lower-degree consequence.
- A five-profile bounded census replayed nine further digit-two points.  Two
  also satisfy the delayed nineteenth row, disproving the proposed
  implication that digit two forces that row nonzero.  They leave 11 and 16
  other digit-three rows nonzero, and all nine census points fail the exact
  row-margin join.
- Exact local analysis at the two stage-2.5 points found regular rank-18
  digit-two Jacobians, 17-dimensional tangents, zero common Hessian
  radicals, and inconsistent complete first-order cubic corrections.  The
  candidate-zero six-dimensional correction sheet contains no digit-two
  point among its 729 elements.
- Exhausted the affine Hamming ball of radius five about the better
  stage-2.5 point: 13,065,937 points contain only the center and one
  radius-five digit-two point.  Neither is row-margin compatible, and the
  second point is worse at digit three.
- Added exact row-margin membership to the sparse histogram model.  The
  candidate-zero digit-two union, eight sampled fixed targets, a
  target-preserving permutation search, and the all-target digit-three
  model all ended `UNKNOWN`.  No bounded status was promoted to an
  exclusion.
- Completed the whole-route estimate.  Generic enumeration of the five
  `3^36` shell-two charts is infeasible; the `n_9=1,0` shells still contain
  510,384 and 107,476 legal supports and 59,743,488 and 47,730,304 legal
  signed skeletons.
- Implemented the exact dense-shell 729-character kernel.  Its conservative
  single-core median is 12,668,666 evaluations/second, 718 times the
  four-week arithmetic threshold.  Independent brute force agrees on all
  1,458 character sums for two real affine cubes.  Full streaming,
  canonicalization, survivor recovery, and exact replay remain unmeasured.
- The strict higher-digit construction gate failed: no full digit-three or
  digit-four point, exact structured lift, feasible complete phase lift, or
  whole-profile exclusion was obtained.  Headline search on the five
  placement charts stops here.  The five-orbit/carry package is preserved
  for a scoped paper, while the dense profile classifier is the only
  evidence-backed bounded continuation.
- No external contact, message, push, or publication occurred.

## 24 July 2026: exact dense-shell `h=0` profile

- The first production prefix of the dense-shell classifier found the
  explicit profile
  `A=112445112445`, `B=551741551741`, target `(2,-2,-4,-2)`.
- An independent dependency-free replay gives `D_0=167` and `D_t=0` for
  all `t=1,...,36`, shell `(0,18,6)`, stabilizer order two, and orbit size
  12.
- The production prefix stopped after 3,979 canonical decorations and is
  incomplete.  The witness proves profile existence but supplies no orbit
  count for the dense shell.
- No labelled `LP(333)` or `H(668)` was obtained.

## 24 July 2026: half-turn lift and asymmetric digit-two point

- The profile half-turn splits the rank-18 first placement fiber into
  dimensions `21+15`.
- The 18 active second-digit equations become twelve even quadrics and six
  odd bilinear equations.  The six odd equations have exactly
  205,901,492,005,503 common points; this is near the generic `3^30`
  scale and is not a contraction.
- Exhausted all 36 global quotient-position fiber pairings.  Seventeen are
  first-layer inconsistent; eighteen leave dimension nine and have no
  second-digit point after all `18*3^9=354,294` points are checked; the
  identity family has dimension 21 and is the publicly excluded
  order-six multiplier ID8.
- Found and replayed a canonical asymmetric `y=e_0` point through digit
  two.  It fails the exact row-margin catalog and zero-column-lag equation,
  and leaves 13 digit-three rows nonzero.
- A 300-second exact digit-three solve on the 15-dimensional slice returned
  `UNKNOWN` after 4,340,808 branches and 177,136 conflicts, with peak RSS
  175,112,192 bytes.  No obstruction or witness is inferred.
- A separate all-target row-margin-aware digit-two solve returned `UNKNOWN`
  after 180 seconds and 2,065,449 branches.

## 24 July 2026: ternary support-and-sign filtration

- In the 27 natural opposite-class pairs, the antisymmetric translation
  space is a ternary `[27,15,4]` code.  Its complete `3^15` weight census
  has six minimum words and fourteen weight-five words.
- Exhausted all six weight-four slices: 266 digit-two points, zero exact
  row-margin points, and zero digit-three points.  The best third-digit
  defect is six rows.
- Exhausted all seven projective weight-five slices: 392 signed digit-two
  points, zero exact row-margin points, and zero digit-three points.  The
  best third-digit defect is seven rows.
- Derived an exact row-margin precursor join.  The fixed eigenspace is a
  ternary `[27,21]` code with six parity checks; the six local blocks of
  sizes `3,4,6,4,4,6` join exactly in `Z[F_3^6]`.
- Anti weight zero has no physical precursor.  Exactly one minimum
  projective direction reaches row-margin target 34, with 7,346
  first-digit placements per sign.  Its 87 digit-two placements are
  disjoint from those physical points.
- The verifier semantic hash is
  `2deaa893bb4e6e2f1afa218ae7a1ff8e6d06a036d89cbfd711fe3868bfbfaf11`.

## 24 July 2026: irreducibility of the half-turn pencils

- Tested whether the twelve even quadrics admit a common affine center,
  invariant block, simultaneous diagonalization, or ordinary field-norm
  model.
- The even `x` and `y` center systems both have coefficient/augmented ranks
  `21/22`, so neither can be homogenized by one translation.
- Relative polar operators generate the full matrix algebras
  `M_21(F_3)` and `M_15(F_3)`.
- On the canonical `y=e_0` asymmetric slice, the twelve restricted polar
  operators again generate the full `M_15(F_3)`.
- This exactly rules out the direct invariant-block and one-field
  trace/norm contractions.  It does not rule out nonlinear or global
  elimination and does not construct or exclude `LP(333)`.

## 24 July 2026: updated priority boundary

- The 2026 `p q^2` paper of Kotsireas, Gallardo-Cava, Gómez, and
  Gómez-Pérez is the source of the prescribed
  `A=[1,3 chi], B=[1,-3 chi]` compression at `(p,q)=(37,3)`.
- The checked sources do not contain the exact `h=0` profile, its `21+15`
  algebra, nonidentity global-twist census, or ternary low-weight
  filtration.  These remain plausible new restricted results inside the
  public-open order-three subgroup ID3.
- The isolated profile and family exclusions are not recommended as a
  standalone paper.  Their proper current role is within a complete
  dense-shell/order-three profile-classification paper.
- No external contact, message, push, or publication occurred.

## 24 July 2026: bounded `Phi_28` Eliahou audit

- Stopped the independent `Phi_28` lane without a witness, exclusion,
  implementation, or repository artifact.
- Corrected the proposed half-join: self-norm hashes alone lose the
  bilinear cross terms, and the mod-six removal vector must be retained
  until the full row is assembled.
- Over `F_3`, `Phi_28` splits into two degree-six Frobenius orbits and
  inversion is the third Frobenius power.  Evaluating the full joined
  element before `u -> u*u^27` gives two `F_27` norm values and a possible
  729-signature modulo-three sieve.
- This is only a prospective necessary sieve with nominal `3^6`
  selectivity.  It has no measured or publication value yet.
- No external contact, message, push, or publication occurred.

## 24 July 2026: unconditional integral closure of the sparse-B sector

- Closed the 84 field-norm survivors from the normalized `B`-energy-six
  census.  Combined with the earlier inert-prime obstruction, all 396
  structural words and all 34 lift-safe orbits are impossible in this exact
  `<10>`-invariant sector.
- Certified the real field unconditionally with `h(M)=1` and unit rank 11.
  The exact product of the twelve odd `L(0,chi)` values is 4096.
- Found the explicit `H`-fixed cyclotomic unit
  `u=product_(h in {1,10,100})(1-zeta_111^h)` with `u/u*=-1`.  This proves
  Hasse unit index `Q_L=2`, hence the CM relative class-number formula gives
  `h(L)=12`.
- Replaced an infeasible generic degree-24 class certificate with a finite
  exact theorem.  For a candidate ideal `J`, an exact generator verifies
  `J^12=(a)`.  At the split primes `1777,2221,2887,3109`, the quadratic and
  cubic unit-signature matrices each have rank 12 and augmented rank 13.
  Therefore no unit twist of `a` is a square or cube, so neither `J^6` nor
  `J^4` is principal.  It follows that `ord([J])=12`; since `h(L)=12`,
  `Cl(O_L)=<J>=C_12`.
- Authenticated every displayed prime-ideal coordinate by an exact
  generator identity for `I J^(-c)`.  Three residual field types have no
  principal integral allocation.  The fourth has four principal
  allocations.
- The full unit group is `mu_6 U_M <u>`, so its norm image is
  `U_M^2<N(u)>`.  All four principal correction units have free parity
  outside the two norm square classes and are impossible.
- The canonical PARI/GP 2.17.4 replay exits successfully in 4.78 seconds
  with 60,014,592 bytes maximum RSS.  Two independent audits replayed it in
  4.76--4.77 seconds, cross-checked every residue signature using
  `idealprimedec`/`nfmodpr`, and found no mathematical or implementation
  gap.
- A generic `bnfcertify` attempt was stopped after 3 hours 29 minutes and
  58,802,176 bytes maximum RSS.  PARI's degree-24 path uses the Minkowski
  bound `1,095,226,102,412`; measured progress projects to roughly 433 days.
  No inference was made from the interrupted run.
- The compact companion certificate is
  `ee3c525efe9b6f9c86c11960ba493159cc33c906a945c297c8676304cb934706`.
  The theorem closes one profile-energy sector, not either aggregate target,
  unrestricted `LP(333)`, or `H(668)`.
- No external contact, message, push, or publication occurred.

## 24 July 2026: connected dense-shell production audit

- Completed the first nontrivial production prefix `h0-p01-p13`: 1,296
  legal skeletons, 42 canonical decorations, 19,131,876 primitive phase
  leaves, 753 modulo-nine hits, and no characteristic-two/modulo-nine
  intersection.
- Found a production cost-model defect: 554,008 diagnostic all-37-lag
  replays ran outside the declared joint-gate scope.  Restricting marginal
  witness recovery to bounded mode changed the shard from 2.615347 to
  0.771325 seconds and leaves zero production replays, with every lower
  count unchanged.
- Connected one real canonical skeleton and target to a complete
  729-character transform.  Its actual `3^12` affine fiber has exactly 729
  modulo-nine points, 34 with the selected exact aggregate, and one that
  passes the following lambda digit.  All 729 character sums, their inverse
  transform, digest `0xc8ac157d026d3025`, and detached physical replay
  agree.
- The recovered point has nonzero exact correlations and fails
  characteristic two.  It is not an exact profile, physical placement,
  Legendre pair, or `H(668)`.
- The actual production modulo-nine polar differs in 459 of 864 entries
  from the older synthetic/theoretical benchmark family.  The old
  12.7-million-character rate is therefore not a drop-in production
  projection.  The actual fitted representative family has a three-run
  median of 15,641,863 characters/second/core.
- The corrected complete-prefix rate projects the rigorous combined
  primitive-leaf upper bound to 53.59 single-core hours.  This is a
  one-cell extrapolation, not a runtime certificate.
- No commit, push, or external communication was performed.

## 24 July 2026: dense-shell exact-orbit census upgrade

- Converted dense-shell production from stop-on-first discovery to
  exhaustive per-shard exact-profile collection.  Exact hits are now
  canonicalized under the 24-element action, keyed by canonical IDs and
  target index, deterministically deduplicated, independently replayed on
  all 37 physical lags, and retained while the shard continues.
- Preserved the original stop-on-first classifier mode for bounded
  discovery.  The resumable production runner always selects the exhaustive
  mode, and its v2 manifest pins that command and policy together with
  source and binary hashes.
- Preserved `dense_shell_classifier_pilot/output/production` unchanged as
  the v1 raw-discovery provenance line.  Its source hash is
  `cf48f07cf1c69b2df1adc9f5f48ffd96c4b3daccc747bcab5a9852d9138e2025`
  and it contains the stopped `h0-p00-p05` candidate.  A future exhaustive
  run must use a fresh `output/production-v2` directory and restart that
  prefix; v1 files are never copied into or overwritten by v2.
- Upgraded both runner and strict aggregator to reject malformed,
  noncanonical, unsorted, duplicate, target-inconsistent, digest-invalid,
  or physically invalid exact-orbit records.  The aggregate certificate now
  contains the complete distinct canonical orbit list and source-shard
  provenance instead of assuming every complete shard has zero exact hits.
- Used the certified second `h=0` profile as a bounded end-to-end fixture.
  The census path reproducibly retains its canonical target-3 orbit with
  digest `0x7395e771c01b49bf`; two runs and the independent validator agree.
  This targeted check took under one second per run and roughly 1 MB
  resident memory.
- No full shell census was launched.  No commit, push, publication, or
  external communication occurred.

## 24 July 2026: second exact dense-shell profile orbit

- The first heavy production prefix, `h0-p00-p05`, reached an exact hit
  after raw skeleton 44,172 of 110,976. The canonical compressed words are
  `A=(1,2,6,1,5,1,4,5,1,5,7,4)` and
  `B=(2,4,2,4,4,6,5,5,8,1,5,8)`, with aggregate target
  `(-3,0,0,3)`.
- Independent integer Eisenstein replay gives `D_0=167` and
  `D_t=0` for all `t=1,...,36`. The shell is `(n_9,n_3,n_0)=(0,18,6)`.
  The representative is canonical with trivial stabilizer and orbit size
  24, and its full orbit is disjoint from the previously certified size-12
  `h=0` orbit.
- Frozen v1 discovery provenance is pinned in
  `dense_shell_exact_profile_h0_orbit2/certificate.json`. The raw candidate
  hash is
  `291a1d2246ceab2b067b225e78deac0757ec47b08ee1ba973d0fbddebef10001`.
  The prefix stopped on discovery, so this is not a complete dense-shell
  census.
- The first placement digit has rank 18 and nullity 36. Its next layer
  contains eighteen active quadrics; eleven polar matrices have rank 36
  and seven have rank 35, while the eighteen polar coefficient vectors are
  independent.
- A 120-second ternary tabu run evaluated 2,841,815 updates and found a
  defect-one point. The full Jacobian has rank 18 and the satisfied
  seventeen-row subsystem has rank 17. Exact enumeration then checked all
  137,724,625 points in the ternary Hamming ball through radius six and
  found no digit-two solution. Peak memory was 539 MB. Full SAT remained
  `UNKNOWN`; no global obstruction is claimed.

## 24 July 2026: quadratic-class control-law obstruction

- Extended the first dense profile's opposite-class control from affine
  laws to arbitrary functions `f:F_3 -> F_3` independently in both
  channels. This gives 2,916 paired families, including 2,592 genuinely
  non-affine-in-class cases.
- Exactly 1,454 families are inconsistent at the first lift and 1,458
  dimension-nine families are empty at the second. One dimension-15
  exception is also empty at the second digit. Two nonidentity
  dimension-21 families each leave 24 digit-two points; all 48 fail digit
  three in between eight and sixteen displayed rows and none meets the
  exact row-margin catalog.
- Therefore all 2,915 nonidentity controls are excluded no later than digit
  three. The only retained law is the identity/identity order-six branch
  already separated by the multiplier audit.
- The dependency-free exhaustive verifier replays 57,415,311 family-point
  incidences in 166.74 seconds with maximum RSS 60,407,808 bytes and zero
  swap. Family-point incidences are not asserted to be distinct placements.
  This is a finite-family theorem for one profile, not a whole-profile or
  `LP(333)` exclusion.

## 24 July 2026: characteristic-three Eliahou anti-fold jet

- Over `F_3`, independently reconstructed
  `Phi_12=Phi_4^2`, `Phi_84=Phi_28^2`, and
  `z^42+1=(z^14+1)^3`. A primitive-28 value sieve is therefore only the
  zeroth Hasse jet; the complete characteristic-three anti-fold condition
  has three jets and twenty normalized support equations.
- Found and detached-replayed a canonical case-26 weight-39 support that
  satisfies all twenty equations modulo three. It is not a joint
  modulo-six point and not an integer repair.
- After division by the common content four, every quadratic coefficient is
  even. The normalized characteristic-two equation is exactly affine.
  Adding weight parity gives rank 21 and dimension 57 in case 26 and rank
  21/dimension 58 in case 0. Exact quotient enumeration counts
  25,941,166,955,843,488 and 51,310,052,181,007,034 fixed-weight supports,
  respectively.
- Code-preserving search reached characteristic-three defect two at lags 9
  and 11 while satisfying the full characteristic-two layer. An exact
  joint SAT check excludes its complete Hamming-radius-eight ball; the
  radius-ten run remained `UNKNOWN`. No joint modulo-six support, integer
  repair, or exclusion follows.
- Independent verifiers replayed the cyclotomic factorization, 68 physical
  support cases, all thirty canonical equation systems, the full
  characteristic-three witness, both characteristic-two code counts, and
  the pinned defect-two point.

## 24 July 2026: v2 connected-prefix provenance repair

- The connected end-to-end verifier correctly rejected the v2 classifier
  because its benchmark certificate pinned the frozen v1 post-fix source.
  No mathematical counter changed.
- Recompiled the exact v2 source hash
  `ef7c77598396c1050d13848b5fde536eba4e8b1426c6554705a1015fbc7f3404`
  and reran `h0-p01-p13` five times with the actual production flag
  `--enumerate-exact-orbits`.
- The five wall times were `0.745499,0.744369,0.742056,0.763598,0.743341`
  seconds. The median rate is 385,532,181 raw-equivalent primitive leaves
  per second per core; maximum measured RSS was 1,540,096 bytes.
- The current one-cell projections are 19.27 single-core hours for `h=0`,
  32.45 for `h=1`, and 51.72 combined, or 5.17 ideal ten-core hours.
  They remain extrapolations rather than runtime certificates.
- Bumped the connected benchmark schema to v2 while preserving the
  historical v1 before/after measurements. The verifier now pins the v2
  source, requires exact-orbit enumeration mode and the v2 shard schema,
  and passes.

## 24 July 2026: five-representative anti-tensor family

- Introduced the multiplicative class-by-row family
  `u_X(j,s)=P_X(j mod 3,s)+h_j F_X(j mod 6)G_X(s)`, with arbitrary
  quadratic background `P_X`, arbitrary six-class table `F_X`, and one of
  twelve nonconstant projective row laws `G_X` in each channel.
- The two independent row laws give 144 charts per representative and 720
  across the five shell-two representatives. Exactly 703 charts are consistent
  at the first placement digit.
- Complete affine enumeration gives 879,741 chart incidences and 517,109
  distinct first-digit placements. Only 2,197 lie in the combined union of
  the seven earlier representative-scoped feature families and every
  minimal `F_27` submodule family. The other 514,912 are also outside all five proper
  fixed common-multiplier supergroups.
- Exhaustive evaluation of all twenty exact second-digit equations leaves
  zero survivors. The best points satisfy 18 of 20 rows on two profiles.
  The verifier uses no solver statuses or timeouts and passes with semantic
  hash
  `39de8bf9d6e60ee078e7710daa81d3546e519589a769bbd2c5579693c6203bef`.
- The independent replay took 28.30 seconds and 180,355,072 bytes maximum
  RSS. A flat rank-two extension is projected at about
  327,370,313,205 chart incidences, so it is not a viable next census.
- This is a complete obstruction for one new structured family on the five
  canonical representatives.  It was already scoped that way and has not
  been action-closed.  It removes only 517,109 points from five `3^36`
  spaces and is not a whole-profile, `LP(333)`, or `H(668)` result.

## 24 July 2026: bounded `Phi_28` norm-key assessment

- Factored
  `Phi_28 mod 3=(x^6+x^5+x^3+x+1)(x^6-x^5-x^3-x+1)`.
  Both factors are degree-six Frobenius orbits, and inversion is
  Frobenius cubed because `3^3=-1 mod 28`. A completed row therefore maps
  to two norms `u*u^27` in `F_27`, a combined 729-valued signature.
- The norm must be formed only after joining row halves; half self-norms
  omit the bilinear cross terms. Modulo-six local state products are
  36,000,000 for the 40-cell `P` block and 30,720,000 for the 39-cell `Q`
  block, so the earlier collapsed `Phi_4/Phi_12` histogram cannot acquire
  this key cheaply.
- Since `z^42+1=(z^14+1)^3` in characteristic three, the norm signature is
  only Hasse jet zero. The separate full three-jet audit above supplies the
  correct stronger layer. No additional support-level sieve, pruning
  count, witness, exclusion, or construction was obtained from the
  `Phi_28` norm-key approach.

## 24 July 2026: anti-tensor correction obstruction

- Took all three `18/20` points from the five-representative anti-tensor
  census and
  allowed a second separable component
  `h_j F'_X(j mod 6)G'_X(s)` with all 13 projective row directions per
  channel, while holding each point's background and first component fixed.
- Exact first-digit elimination reduces the two relevant profiles to 175
  and 11 distinct corrections, or 361 base-correction incidences. None
  reaches `19/20` or `20/20` in the exact second-digit equations.
- The two near misses on `h2-422220-2` lie in the same unique original
  chart. Their difference is the only nonzero correction retaining
  `18/20`, and it merely swaps the two points; the third point on that line
  scores `9/20`.
- Every fixed-background Newton system is inconsistent. A broader
  rebalanced rank-two diagnostic retains 2 of 16 charts for each first
  profile point and 7 of 16 for the second profile point, but its exact
  Newton steps score at most `11/20`. This is heuristic prioritization, not
  a nonlinear full-chart exclusion.
- The independent verifier passes with semantic hash
  `ed254a1e0a884227b447d31910298ea09ef9d7080b244bce3934c459bed9c4b8`,
  in 4.37 seconds and 39,534,592 bytes maximum RSS.

## 24 July 2026: second-profile quadratic character compression

- For the second exact `h=0` profile, grouped the eighteen active quadrics
  into six triple-sums `g_i=q_i+q_(i+6)+q_(i+12)`.
- All 728 nonzero scalar combinations have singular polar rank between 19
  and 34. Exactly 722 are balanced by a radical translation; the remaining
  six vectors form three projective exceptional lines.
- Every nonzero combination of the first five `g_i` is balanced, so the map
  `F_3^36 -> F_3^5` is exactly uniform with fibers `3^31`. Exact Fourier
  inversion gives
  `#g^(-1)(0)=3^30-7*3^13=205,891,120,934,388` and a complete five-size
  histogram for all 729 fibers.
- The first four forms have a seven-dimensional common radical on which
  their linear terms have rank four. This yields an explicit quadratic
  bijection from `F_3^32` to their common zero set.
- A single 29,524-projective-character census gives exact zero-fiber counts
  after six through ten equations:
  `205891120934388,68630383210734,22876784306199,7625590635303,
  2541863158002`. Each is within roughly `10^-6` of its random-map
  expectation. The compression is structurally exact but does not indicate
  anomalous convergence toward all eighteen equations.
- The verifier passes in 16.66 seconds and 44,138,496 bytes maximum RSS.
  This is a digit-two coordinate theorem, not a placement witness or
  higher-digit lift.

## 24 July 2026: first complete mod-six anti-fold supports

- In case 26, fixed the 39 reflected-pair parities to the affine quotient
  state of the prior defect-two point. It has 23 odd pairs and 16 even
  pairs, with exactly eight full even pairs, hence
  `2^23*binom(16,8)=107,961,384,960` weight-39 supports.
- After substitution, the cross-block central pair is an articulation of
  the characteristic-three interaction graph. Conditioning it separates
  components of sizes `10,10,10,8`, permitting an exact vector-valued
  meet-in-the-middle join.
- The complete fixed-quotient census finds exactly 62 simultaneous
  normalized mod-two/mod-three supports. These are the first full mod-six
  survivors in this lane. Detached physical replay of all 62 finds zero
  exact integer supports; the minimum has 11 nonzero lags and the minimum
  `L1` residual under a separate objective is 114.
- The pinned lexicographic witness has Hamming distance 28 from the old
  center and residual
  `(6,0,0,-36,0,6,6,24,0,0,-6,-18,-6,-12,0,0,0,0,-6,-6)`.
- This covers exactly one of `2^18=262,144` quotient states, not the full
  25,941,166,955,843,488-point characteristic-two slice. The exact next
  problem is to reuse the same articulation join across the other 262,143
  quotient states.
- Independent replay passes in 3.36 seconds with 452,722,688 bytes maximum
  RSS. No integer repair or whole-case exclusion is claimed.

## 24 July 2026: complete dense `h=0` profile classification

- Finished all 729 production shards for the dense `(n_9,n_3,n_0)=(0,18,6)`
  shell.  The strict aggregate covers 47,730,304 raw decorations,
  1,999,128 canonical decorations, and
  25,368,365,895,696 weighted primitive leaves.
- The filters leave 19,986 characteristic-two/modulo-nine hits, 64
  post-modulo-nine lambda hits, and exactly 18 inequivalent canonical
  exact-zero profile orbits.  Twelve have orbit size 24 and six have orbit
  size 12; their weighted exact-zero population is 360.
- Froze the complete classification in
  `dense_shell_h0_complete_classification/`.  Its dependency-free verifier
  reconstructs all 666 exact integer-Eisenstein correlations (648
  nonzero-lag and 18 zero-lag), the faithful 24-element action, canonicality,
  stabilizers, 153 pairwise disjointness checks, and the complete 729-shard
  provenance.  It passes without the ignored production output.
- This is a complete profile-layer classification in the prescribed
  order-three `q^2`-uncompression branch.  It is not a Legendre pair or a
  physical phase-lift classification.

## 24 July 2026: all-eighteen lift geometry and complete half-turn extension

- Replayed every exact `h=0` orbit from the frozen classification
  certificate.  All eighteen first placement layers have rank/nullity
  `18/36`, every quadratic span has rank 18, and the individual polar ranks
  range from 33 through 36.
- Audited 6,552 structured characters and 6,552 hyperplanes.  Retraction
  maxima split exactly nine profiles at dimension five and nine at
  dimension four; none reaches six.  Exact transfer through every one of
  the 1,756 row-sum words leaves 45--96 compatible rows per profile.
- Exactly six profiles are half-turn fixed.  Across their complete
  anti-weight-four and anti-weight-five shells, 244 signed anti-words give
  242 consistent slices and 7,178 exact digit-two points.  None meets an
  exact row margin and none survives the full third digit; the minimum
  digit-three defect is six.
- The full one-core replay passes with semantic SHA-256
  `1e95c26f935cd6f7cfcb69044d9b97c9fdf0a0e1907b774240a0a63bd394cbea`.
  This satisfies the sprint's consecutive-higher-digit requirement on a
  rigorously delimited family, but does not exclude the remaining anti
  spaces or the twelve generic profiles.

## 24 July 2026: Witt-conic reduction and rank-one obstruction

- Derived the lossless local characteristic-three form
  `(q-t)^2=p(s)-1`, `t=-p u` for every exact `h=0` block.
- For profile `c90c`, exhaustively tested the rank-one antipodal
  quadratic-center family: 29,524 projective shapes, 78,729 canonical
  shape/amplitude centers, and 65,601 distinct physical placements.
- No placement survives the full second digit; the best satisfies 16 of 18
  equations.  A successful conic-center law in this model must have rank at
  least two or be nonquadratic.
- Independent replay passes with semantic SHA-256
  `0c68683c63f9116179530430435e9da69728e198b7e5d8a2e63d8d69c8696a3c`.

## 24 July 2026: complete case-26 Eliahou quotient exclusion

- Exhausted all 262,144 characteristic-two parity quotients in canonical
  case 26.  The complete run evaluates 412,316,860,416 principal join rows,
  obtains 10,533,216 simultaneous normalized modulo-six supports, and
  physically replays all 10,533,216 as integer polynomials.
- No exact support exists in this case.  The best quotient is 123143 with
  pair state 369546495487 and residual
  `(0,0,0,-36,0,0,0,18,6,0,0,0,0,0,-6,0,0,0,0,0)`.
- Froze an output-independent completion certificate and verifier in
  `eliahou_global_quotient_plan/`.  Strict live replay checks all 256 range
  manifests, the range digest
  `c566eef9154ebefb13bca52c5e3e931c622e7d930619e2d3f35bec09d9e27fc7`,
  aggregate SHA-256
  `268adc90d99e7a045c60879fd9367910c78a3b0b93e11aab47589e743d5a5253`,
  and zero exact supports.
- An independent reference replay of the best quotient finds 46 normalized
  survivors, zero exact supports, and the same best residual.

## 24 July 2026: all-nine short-block theorem and census launch

- Generalized the case-26 articulation join to every canonical short-block
  case 21 through 29.  Each has 78 binary variables, 39 equal-syndrome
  pairs, quotient dimension 18, the same four conditional cliques, and a
  free reflection on every quotient.
- Cases 24 and 27 alone can lack an odd long-block pair; a symmetric
  short-block fallback gauge is exact there.  The resulting total work for
  all nine cases is 3,710,853,316,608 principal join rows.
- The parameterized compiled kernel, atomic resume runner, strict
  aggregator, and independent physical replay pass controls against the
  case-26 model and exceptional gauges.
- The other eight cases were launched sequentially with eight workers and
  fixed small memory.  The prospective decision rule was to replay an exact
  survivor immediately or, on empty completion, close all nine short-block
  cases while leaving twenty long-block cases open.

## 24 July 2026: near-Williamson order-167 feasibility audit

- Derived the one-defect identity
  `d_t=b_t+c_t+x_t+x_(2t-1)+x_(2t+1) mod 2`, which eliminates one binary
  block after the other three are fixed.
- The 68 normalized row-sum profiles split into 34 Williamson and 34
  genuine one-defect profiles.  Nevertheless the 33 unique gauge-fixed
  `A,B` front-end shards contain exactly
  `5,389,321,893,816,717,644,217,498,408,040,941,405,747,563,982,000`
  states, about `10^48.73`.
- The May 2026 near-Williamson paper classifies odd orders through 35 and
  gives examples through 63, but supplies no order-167 construction.  The
  present route is not scalable without a new parametrization or spectral
  theorem and has not been authorized for production.

## 24 July 2026: complete quadratic antipodal rank-two conic family

- Selected exact `h=0` orbit 07, digest `0x86b13a0388d98a5e`, from the
  all-eighteen lift scan.  It ties the maximum 96 compatible row-sum words,
  has the second-largest raw transfer mass, and gives the smallest
  rank-two image dimension among the audited targets.
- Allowed four arbitrary degree-at-most-two center polynomials
  `P_A,P_B,Q_A,Q_B` in the antipodal Witt-conic closure.  The `2 x 10`
  coefficient matrix includes every rank-zero, rank-one, and rank-two
  opposite correction in this quadratic feature space.
- The exact linear quotient has 40 coefficients, feature rank 32,
  first-layer rank 18, solution dimension 22, and evaluation-kernel
  dimension eight.  Thus the complete physical family has exactly
  `3^14=4,782,969` distinct placements, or fraction `3^-22` of the ambient
  `F_3^36` first layer.
- Exhausted all 4,782,969 placements after restricting the eighteen
  quadrics to fourteen variables.  There are zero exact digit-two
  survivors, zero row-margin-compatible digit-two points, and zero
  two-consecutive-digit survivors.  Exactly five near misses score 17 of
  18 and fail rows 2, 3, 4, 10, and 16 once each; none meets the 1,756-row
  catalog.
- Independent replay passes in 11.80 seconds at 59,604,992 bytes maximum
  RSS with semantic SHA-256
  `cc272f74521b7cf58216b1971f8a2659b1eb1068a295b6c7552cb3c15c778dc8`.
  This closes the stated quadratic antipodal family on one orbit, not
  degree-three, non-antipodal, or unrestricted center laws.

## 24 July 2026: shell-two structured action closure

- Audited the older `structured_phase_families/` scope.  Its feature laws
  use the chosen class coordinates, while its verifier iterates only the
  five canonical shell-two representatives.  The earlier exact results
  remain valid on those representatives but were not all-action-image
  theorems.  The independent `five_orbit_family_audit/` was already
  explicitly representative scoped and is unchanged.
- Built a separate exact, resumable closure for
  `opposite_planar_c3_envelope`, `opposite_twisted_c6`,
  `opposite_helical_c4`, and the `F_27` minimal-submodule family.  The frozen
  24-element action produces exactly
  `24+12+12+12+24=84` distinct labelled images.
- Exhausted 5,900,019 attained first-digit placements across the four
  family-image audits: 72,900 planar, 3,542,940 twisted, 2,278,854
  helical, and 5,325 `F_27`.  The `F_27` total includes all `56^2=3,136`
  asymmetric submodule pairs on every image.
- Exactly five points reach digit two, all in the helical family.  They are
  five distinct classes under the common `C6` rotation, with every one of
  the six rotations directly replayed.  All five are fixed by minimal
  proper multiplier supergroup ID8; none is proper-supergroup-free.
  Their digit-three defects are `5,6,7,8,12`, and zero reach digit three.
- The action closure therefore repairs a real orbit-scope gap but fails the
  consecutive-lift gate.  The five digit-two points are not counted as
  construction progress.
- The pinned, live-output, and full 84-image recomputation verifiers all
  pass.  The certificate semantic SHA-256 is
  `e5a27d107a5e2f140feabb3a69a02c16044980a05baaa1523fafff3ef9d0d802`.
  No commit, push, or external contact occurred.

## 25 July 2026: complete all-nine Eliahou short-block exclusion

- Finished every case 21 through 29 with the exact reflection-gauged
  four-clique engine.  The complete denominator is
  3,710,853,316,608 principal join rows.
- The nine runs retain 88,927,740 joint modulo-six supports.  Every support
  was replayed through the integer equations and the independent bit-packed
  physical correlations; zero is exact.
- Froze the output-independent result in
  `eliahou_short_block_census/NINE_CASE_COMPLETION_CERTIFICATE.json`, with
  detached verification by `verify_nine_case_completion.py`.
- This closes the complete short-block boundary.  The twenty long cases
  1--20 remain open; the case-1 solver-UNSAT observation still has no checked
  proof.

## 25 July 2026: all-canonical-gauge rank-two census and action correction

- Exhausted the arbitrary-quadratic antipodal rank-two conic family on all
  eighteen frozen canonical dense-`h=0` gauges: 3,663,754,254 exact physical
  quotient states.
- Seven points survive digit two.  Their following-digit defects are
  `10,10,11,13,13,14,14`; none survives full digit three or two consecutive
  digits, and none meets an exact row margin.
- An exact action audit disproves invariance of this coordinate-dependent
  feature law.  Across all 360 distinct labelled images, the physical
  dimensions split as `14:12, 15:8, 16:56, 17:96, 18:188`.  The completed
  census covers only the eighteen frozen canonical gauges, not the other
  342 images.
- The complete action-image workload is 87,815,310,840 states.  The remaining
  342 images account for 84,151,556,586 states, projected at roughly 89
  single-core wall hours.  This is a workload sum, not a disjoint-placement
  count or an exclusion.
- Froze the canonical census and noninvariance audit in
  `h0_witt_conic_rank_two_full_18/`; the legacy
  `h0_witt_conic_rank_two_all_orbits/SCOPE_CORRECTION.json` records the
  withdrawn all-orbit interpretation.
- The bounded construction gate therefore fails.  Preserve the five-orbit
  and eighteen-orbit classifications as a scoped paper project, and stop
  headline `H(668)` work absent a genuinely new construction principle.

## 25 July 2026: semiregular \(C_{37}\) conference-lift restart

- Began a genuinely different route: construct a normalized symmetric
  conference matrix of order 334 and double it to `H(668)`.  The 333-vertex
  core is required to have only a semiregular `C37` action with nine fibers,
  so the earlier obstruction to group-developed cores of order 333 does not
  apply.
- The obvious product of normalized order-10 and order-38 conference cores
  fails exactly: its natural zero-filling tensor has residual
  `28*(I9 tensor J37-J9 tensor I37)`.  This closes that mixed Turyn-style
  repair, not all product constructions.
- Derived the exact zero-frequency equations
  `T*1=0`, `T^2=333I-37J` and constructed an explicit integral feasible
  quotient from four norm-333 planes in an `A8` Hadamard basis.  Its
  adjacency quotient is nonnegative, 166-regular, and satisfies the full
  strongly-regular orbit equation.
- Excluded the quadratic-residue three-class lift, the natural full-`S4`
  lift, every regular order-four pair translation, every simultaneous
  paired-label transposition, and every paired-label three-cycle by exact
  norm, trace, and representation-sector arguments.
- Proved a general trace law: after orientation, every nonzero quadratic
  residue appears in six diagonal blocks and every nonresidue in three.
  The complete trace-compatible fixed-margin ambient space is still between
  `2^1297` and `2^1298`.
- In characteristic 37, the full graph equation becomes
  `N(y)^2=9*y^36*J`.  Its first moment has rank 16 on 36 skew variables,
  reducing the exact ambient count by `37^16` to between `2^1214` and
  `2^1215`.  A concrete support witness passes through `y^3` and first fails
  at `y^4`; this is calibration, not convergence.
- Constructed an explicit full formal completion for every admissible first
  moment.  With `z=log(1+y)`, each is `[N0,A]` for symmetric `A`, and
  `exp(-zA)*(N0+z^18*J+19*y^36*J)*exp(zA)` satisfies the complete truncated
  equation and the correct trace branch.  This does not classify all formal
  solutions; exact binary support realization remains open.
- Excluded every constant diagonal and every constant symmetric rank-one
  generator in that exponential family.  The nonisotropic case contradicts
  six exact
  quadratic-character lag patterns; the isotropic square-zero case retains
  five nonbinary zero-lag diagonal coefficients.  Any viable constant
  generator must be genuinely nondiagonal and have rank at least two;
  higher-`y` conjugators are not excluded.
- Counted exact finite-field relaxations of the full fixed-quotient
  group-ring equation.  Characteristic three gives two Hermitian
  square-zero factors and an upper bound between `2^1141` and `2^1142`.
  Characteristic two gives a rank-four unitary projection over
  `F_(2^18)` and an exact orientation-fixed modular count between `2^719`
  and `2^720`.  Every binary lift injects into the latter set, but most
  modular points need not satisfy the integral margins or support
  conditions.
- Excluded every constant symmetric rank-two generator in the
  trace-corrected exponential family by exhausting all rational/Jordan
  types.  Independent review found two implementation defects in the
  preliminary split check; both were corrected, the result remained zero
  survivors, and a separate universal-code computation corroborates the
  split conclusion.  A viable single constant generator must now have rank
  at least three.  Higher-`y` conjugators and general lifts remain open.
- Completed the exact outer classification of the semiregular quotient:
  625 permutation classes, 314 permutation/sign classes, and 196,560,000
  labeled matrices.  No class has an all-zero diagonal, making the `6/3`
  trace law universal.  Independent orderly, canonical, automorphism, and
  modular-rank audits passed.
- The 625 integral quotients reduce to only three adjacency-quotient parity
  types, or two up to complement.  Combined with the unitary-projection
  theorem, every lift in the complete quotient lane injects modulo natural
  equivalences into an all-quotient mod-two relaxation between `2^720`
  and `2^721`.
- The exact trace-law union over all 625 canonical quotient classes has
  base-two logarithm `1307.10873431446430`; after the exact `37^16`
  first-moment reduction it is `1223.75748046440094`.
- Refined the constant-rank-two obstruction across the complete quotient
  census.  Only one quotient sign-class survives the coarse diagonal
  weight code.  For its two remaining Jordan types, restoring the fixed
  `z^18*J` coefficient yields a seven-dimensional affine code with no
  binary word at either genuine orientation `eta=+/-1`.  Therefore no
  constant symmetric rank-two generator works for any of the 625 quotient
  classes.  This still says nothing about higher-`y` conjugators.
- The literature audit confirms that orbit matrices and semiregular cyclic
  blocks are standard.  Mathon's apparently matching `p*q^2+1` construction
  requires `p=q+2` and therefore does not cover `37*3^2+1=334`; the 22 July
  2026 common-multiplier Legendre-pair paper is a separate lane.  No
  occurrence of this particular quotient or its specialized trace/moment
  results was found, but the search was not exhaustive and novelty remains
  provisional.
- Froze the derivation, machine-readable certificate, and dependency-free
  verifier in `conference_334_z37_lift/`.  No conference matrix, strongly
  regular graph, or `H(668)` is claimed, and no external communication was
  made.

## 25 July 2026: exact support and higher-layer construction gate

- Constructed one explicit semiregular `333 x 333` binary support for an
  integral quotient representative of each of the two parity types.  Each
  has exact degree 166, every prescribed integer block margin, the full
  `6/3` diagonal trace law, and all 2,997 ordered group-ring equations
  modulo two, equivalently all 110,889 scalar equations.  A third frozen
  type-1 representative retains the lower layer while reducing the
  independent next-digit carry from `722/1503` to `672/1503`.
- None of the three frozen supports reaches adjacency modulo four.  The
  exact next-digit CP-SAT model ended `UNKNOWN` in bounded runs, while
  sampled targeted derivative ranks `720/721` and affine rank 1,493 show
  why its generic relaxation is weak rather than proving infeasibility.
- Proved that an ordinary four-cycle toggle preserves the modulo-two
  equation only on an invariant pair-vector plane.  Exhausting all 55,278
  pair-vectors per frozen type gives minimum column-difference weights 136
  and 138 and zero invariant planes.  Exhausting 49,284 smallest
  semiregular Hermitian transvections per witness gives zero
  exact-margin members.
- Extended the characteristic-37 formal obstruction from constant rank two
  through rank three.  The complete projective rational over-list contains
  1,452 types; 960 survive the diagonal weight gate and every one fails
  after the fixed `J` coefficient is restored.  A viable generator in this
  single-constant family must have rank at least four.
- Derived the first-nonconstant unitary logarithm through degree two:
  `K=z*A0+z^2*A1` has a `20+20`-parameter gauge slice with `A0` symmetric
  and `A1` skew.  Pure first-higher rank two and the entire common
  nondegenerate two-plane pencil are impossible across all 625 quotients.
  Degenerate or moving support and general nonconstant generators remain
  open.
- Completed the five-profile LP333 physical-margin gate.  All 405 targets
  have a rank-six affine margin digit, the next six quadrics have zero
  common polar radical, no five-form retraction survives, and all 11,011
  four-subspaces give maximum dimensions `4,3,3,3,4`.  No physical
  consecutive higher-digit witness was found; the five-profile
  construction lane is stopped but preserved as a paper project.
- Audited arXiv `2607.20765`: its full-family results subsume the local
  multiplier-order 18, 9, and 6 exclusions.  The five-orbit and
  physical-margin results lie only in the paper's still-open subgroup ID3
  and remain novel-looking within the additional fixed-compression slice.
- The strict construction gate fails: no `H(668)`, conference graph,
  Legendre pair, modulo-four support, or two-consecutive-higher-digit
  physical lift was produced.  Headline search should pause unless a new
  theorem supplies globally coupled margin restoration or a direct
  integral construction.  All promoted replays stayed below 101 MB except
  the bounded CP-SAT diagnostic, which stayed near 2.7 GB; no external
  communication occurred.

## 25 July 2026: theory-first restart and higher Sidelnikov products

- Restarted only on structural reductions; no unrestricted brute-force
  production search was launched.
- Extended the prime-83 character-product theorem from independently
  decimated degree at most two to independently decimated degree at most
  three.  The complete quotient has 3,910,048 affine representatives and
  5,434 row-compatible endpoint states; the exact 41-coordinate integer PAF
  join has zero ordinary-block completions.
- Independently exhausted the un-decimated degree-at-most-four family:
  325,835 row-compatible endpoint states yield 179,221 required PAF vectors
  and zero decompositions.
- Frozen byte-for-byte outputs, the separate Python semantic certificate,
  release replay, ASan/UBSan, the seven-file hash manifest, and an
  independent red-team enumeration all pass.
- No prime fold, `BS(84,83)`, or `H(668)` was found.  Independently
  decimated degree four, higher products, and arbitrary character families
  remain open.

## 25 July 2026: exact Eliahou endpoint-orientation cascade

- Derived the complete positive-fold 2-adic orientation lift on all twenty
  open distance-41 long cases.
- Proved that the apparent positive-fold mod-8 obstruction is exactly
  redundant on the full anti-fold characteristic-two affine code.
- At a fixed support, replaced 39 raw endpoint choices by one fixed
  `23 x 78` mod-16/root-parity matrix restricted to the selected columns,
  four exact root cardinalities, and 21 exact mod-32 quadratics.
- Regenerated a deterministic 200-support certificate.  Its 26,607,616
  consistent mod-16 points leave 22 mod-32 points, one exact-root point, and
  zero positive-fold mod-64 points.  This excludes only the pinned supports,
  not any complete long case.
- Independent derivation reproduced the algebra on a different 200-support
  sample and replayed the lone primary root-exact point directly.
- Corrected an initially promising but false equivalence: the positive and
  anti 42-folds leave the nonzero kernel `C_1=2,C_83=-2` and prove periodic,
  not aperiodic, complementarity.  Exactness needs 41 causal equations.
- Verified in every long case that the exact ternary fold-plus-causal system
  has 5,928 quadratic products, identical to the direct aperiodic inventory.
  A bounded exact case-1 diagnostic returned `UNKNOWN`; no solver claim or
  Hadamard candidate was retained.
- Exact case-1 support-first scale is
  25,953,942,447,362,002 already at the anti-mod-2 layer.  The orientation
  cascade is meaningful local contraction, but a global support theorem is
  still required.

## 25 July 2026: exact Eliahou ternary-model diagnostic

- Built the exact case-1 fold-plus-causal model with 78 trits, 156 endpoint
  Booleans, 5,928 shared products, 6,085 proto variables, and 17,949 proto
  constraints.
- Source ternary polynomials, Boolean expansions, and direct physical
  correlations agree in 4,080 scalar checks over 24 deterministic
  assignments.
- Profile 0 remained `UNKNOWN` after 300 seconds with four workers; profile
  1 was deliberately interrupted after the gate failed and also returned
  `UNKNOWN`.  Peak RSS was 322 MB.
- No profile is excluded.  A proof-capable encoding is mechanically
  available, but the observed propagation does not justify a raw
  proof-producing run before a new mathematical contraction.

## 25 July 2026: shell-two primitive-unit theorem

- Exhausted all five canonical shell-two profiles, both channels, and all
  six primitive prime-167 factors, then audited the five additional
  `A`-star seeds needed for physical action closure: 90 exact zero-assignment
  counts, all zero.
- The largest meet-in-the-middle halves have `3^15=14,348,907` exact field
  values.  An independent pinned linear-hash replay gives a disjoint
  necessary-image certificate and passes its positive control.  Peak RSS
  was 1.86 GB.
- A detached verifier partitions the 84 formal profile images into ten
  physical lift orbits of sizes `12,6,6,6,12,12,6,6,6,12` and verifies
  their disjoint union and factor transport.
- Therefore both recombined channel words are units in all six primitive
  factors on every physical shell-two placement.  The norm cone has the
  global ratio form `R=W_B/W_A`, `R R*=-1`, with
  `R_(r+3)=(-R_r^(-1))^(167^9)`.
- The exact physical-margin plus `T1/T2` convolution excludes 0 of 405
  targets.  It leaves 1,123,966,766,238,638,605 assignments, a reduction
  essentially equal to `37^2`; this is not convergence evidence.
- No Legendre pair or `H(668)` was found.  Further work in this lane is
  justified only by a new multiplicative character, resultant, or
  local-coset obstruction on the ratio torus.
