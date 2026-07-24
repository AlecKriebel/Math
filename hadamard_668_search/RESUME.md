# Resuming the Hadamard order-668 search

## Status at this milestone

No Hadamard matrix of order 668 has been found.  No tracked JSON file is an
exact candidate.  Exact success means producing explicit signs and passing the
full `668 x 668` verification path; energy zero in a search engine is not
sufficient by itself.

The closest published structured object remains Eliahou's 64-modular seed.
The strongest results in this repository are negative or local:

- fixing Eliahou's `q` reduces an exact repair to `TU(41)`, whose emptiness is
  supplied by a published exhaustive classification and independently
  reproduced here by a 461-shard, 57,543,021-node exact enumeration;
- fixing Eliahou's `s` is impossible already at `z=1`, where the remaining
  two row sums would have to represent `321` as two squares; the
  primitive-eighth-root partial norm gives an independent obstruction;
- the adjacent-42 fold proves that every exact `BS(84,83)` changes at least
  80 of Eliahou's 334 base-row signs and at least 41 special `(s,q)` signs.
  The only open distance-41 type is two reciprocal `q` flips plus 39 `s`
  flips; roots `+1,-1` reduce it to 39 reciprocal pairs and two joined
  profiles per pair;
- the complementary anti-fold removes all endpoint orientations from the
  first distance-41 stage and collapses the 39 reciprocal pairs to 30
  distinct support instances. Canonical case 0, long `q` representative 0,
  is certified UNSAT by a checked binary DRAT proof. Canonical case 1, long
  representative 2, has one unproved solver-UNSAT observation; the other 28
  instances are `UNKNOWN`. Exactly one of 30 is closed;
- the older primitive-eight 16-coordinate dynamic program gives a sharp
  necessary-condition boundary at distance 34: its sphere first becomes
  reachable at distance 33, all 66 full targets there fail exact margins,
  and a distance-34 witness passes roots, margins, and endpoint quads. The
  adjacent-42 theorem now supplies the stronger true repair-distance bound;
- a solver-backed exhaustive computation reports no exact `BS(84,83)`
  sequence through raw labelled Hamming distance 18 of the seed; the retained artifact
  checker verifies the decomposition and records, not the 1,296
  solver-reported UNSAT claims (1,284 root-layer and 12 compression-layer
  leaves); four representative leaves now have independently checked DRAT
  proofs and all twelve stored root witnesses pass pinned positive-CNF
  validation, leaving the full UNSAT gate incomplete;
- the unrestricted-projective common-type five-comb family is solver-excluded
  for all 48 complementary quartets and all 32 structural label cores:
  1,536/1,536 models are `INFEASIBLE`, with no timeout or candidate. The
  corpus verifier attests records and source state, not independent UNSAT
  proofs;
- the fixed-compression column-only `LP(333)` multiplier families of orders
  18, 9, and 6 are empty by an exact row-sum PAF obstruction. The all-core
  replays check 38,880 quartic and 2,309,472 sextic projected states with
  zero hits; no solver status is used.  The July 2026 full multiplier
  classification now subsumes these conclusions for paper IDs 20, 12, and
  8, so retain them as independent compact proofs rather than novelty claims;
- inversion-symmetric/normalized-skew `LP(333)` type pairs are impossible;
- several large, explicitly defined local neighborhoods around retained near
  misses have been independently exhausted.

The strongest new constructive reductions are:

- `NOVEL_BS84_THEORY.md`: exact equivalence of `BS(84,83)` with simultaneous
  cyclic folds at 84 and 83. The prime fold is a 41-equation oriented SDS with
  45 size profiles and a `GF(2^82)/GF(2^41)` norm parameterization. Construct
  the prime fold first, then test 564,898 finite phase/multiplier lifts.
- `LP333_MULTIPLIER_ROW_SUM.md`: an exact compact row-sum identity for the
  now-subsumed order-18, quartic, and sextic fixed-compression quotients,
  plus the 1,756-word front end of the still-open paper ID3 order-three lane.
- `LP333_ORDER3_DIFFERENCE_FAMILY.md`: the viable order-three boundary has
  exactly 1,756 row-sum PAF words. Their zero-column/signature lift is
  equivalent to 24 cyclic triples on `Z/9`; all 1,756 words lift in that
  projection, so the remaining obstruction is genuinely mixed cyclotomic
  geometry.
- `LP333_ORDER3_EISENSTEIN.md`: the nontrivial three-row Fourier channel is
  exactly two complementary `H`-invariant Eisenstein sequences of energy
  167. The direct 20 equations reduce to 13 independent integer conditions,
  and the row-sum catalog collapses to 22 norm-pair shards.
- `LP333_ORDER3_PRIMITIVE9_JET.md`: six exact ramified digits restore
  within-residue placement information. Digit one is the Eisenstein pair
  sieve; digits two through five contain genuinely new mixed class products.
- `LP333_ORDER3_CHAR37_TRANSFER.md`: the complete mixed system modulo 37 is
  one invertible 13-dimensional logarithmic norm transfer. The first two
  coefficients leave all 22 shards alive, while the later coefficients are
  nonredundant on every retained partial witness.
- `LP333_ORDER3_LABELED_JET.md`: the invariant column algebra splits exactly
  as `F_3 x F_729 x F_729`; a fully labelled row-695 lift passes all 222
  modular jet equations and four exact row-direction equations.
- `LP333_ORDER3_TRIT_LIFT.md`: the pinned row-695 profile tuple has 54 upper
  placement trits cut by a rank-18 affine system, leaving nullity 36 before
  exact margins and correlations. A second modular certificate is replayed.
- `LP333_ORDER3_INTEGRAL9.md`: exact primitive-ninth-root vanishing is triple
  equality of integer correlation counts at row lags separated by three.
  Both modular certificates fail all 36 nonzero class/residue groups, proving
  strictness but not excluding row 695.
- `LP333_ORDER3_PROFILE9_IDEAL.md`: profile data alone must satisfy six
  displayed Eisenstein ideal tests with one global dependency, hence five
  independent conditions. Passing fixes the complete `12 x 3` exact target
  table.
- `LP333_ORDER3_PROFILE9_SHARDS.md`: all 22 aggregate shards have explicit
  alternative profile tuples passing the ideal. The ideal eliminates the 22
  old witnesses but no whole shard. The later exact zero-moment gate excludes
  all 22 of these alternative fixed tuples as full-LP inputs, again without
  excluding a whole shard.
- `LP333_ORDER3_PROFILE_ZERO_GATE.md`: a full `LP(333)` requires the
  order-three profile correlation `D_t` to vanish exactly on all 13 column
  parts. All 22 ideal-compatible tuples fail: one on 10 nonzero classes and
  21 on all 12. The original row-695 profile and stored same-shard witness
  both fail on all 12 classes.
- `LP333_ORDER3_PROFILE_CRT.md`: on energy 167, the lambda-cube ideal plus
  all 13 characteristic-37 transfer coefficients is equivalent to exact
  `D_t=0`; the least nonzero CRT norm is 36,963, above the Cauchy bound
  27,889.
- `LP333_ORDER3_PRIME167_SPLIT.md`: reduction modulo 167 alone is lossless
  on the energy-167 shell.  The invariant algebra is
  `F_(167^2) x F_(167^12) x F_(167^12)` with checked star, inverse CRT, and
  complete two-channel solution parameterization.  All 22 stored tuples
  fail.
- `LP333_ORDER3_SPECTRAL_UNITS.md`: on the physical ten-value profile
  alphabet, both channels are units in every prime-167 CRT factor.  A
  twelve-factor number-field norm below `167^12` cannot meet either residue
  prime of norm `167^12`.  Thus `U=A B^(-1)` satisfies `U U*=-1`, and a
  fixed target has only the single primitive torus `(167^12-1)^3`; the old
  degenerate and both axis branches are impossible for a profile survivor.
- `LP333_ORDER3_PROFILE_SPARSE_SHELLS.md`: the two sparsest type sectors
  `(n_9,n_3,n_0)=(5,3,16),(6,0,18)` are exactly empty.  Opposite-quartet
  geometry plus modulo-nine linearization leaves only 552 and 288 words for
  detached all-37-lag replay, with zero exact survivors.  Independent
  enumeration and external hashes confirm the theorem, so every future
  exact profile has `n_9<=4`.
- `LP333_ORDER3_PRIME163_EXTREME.md`: in targets `(4,-1,0,0)` and
  `(5,1,0,0)`, the extreme energy split `(163,4)` would give
  `B=2 delta_0` and `A A^*=163 delta_0`.  Explicit principal degree-12
  primes above 163 plus CM-unit rigidity and Fourier inversion rule this
  out.  Exactly 1,617,192 local-sieve assignments per target are removed;
  nonextreme sectors remain, so zero whole shards are excluded.
- `LP333_ORDER3_SPARSE_B_NORM.md`: in the same two targets, normalized
  `B`-energy six gives exactly 396 two-orbit words.  Relative-norm
  obstructions at inert primes above 11 and 101 exclude 312 words and 26 of
  34 lift-safe orbits.  Four field-norm types remain, comprising 84 words
  and eight lift-safe orbits, so the sector is reduced but not closed.
- `LP333_ORDER3_PROFILE_ZERO_SYMMETRY.md`: the formal profile group
  `C6 x C2_A x C2_B` reduces 22 targets to seven.  Only `C6 x C2_B`
  transports the canonical labelled zero words, giving twelve
  lift-compatible target orbits.
- `LP333_ORDER3_PROFILE_CRT_CONSTRUCTOR.md`: the exact 24-profile discovery
  search directly enforces six reversal-independent `D_j=0` equations.  It
  uses 3,334-row quartet tables, 1,409 coarse states, full fixed-target
  stabilizers, semantically pinned atomic checkpoints, persistent no-goods,
  orbit-complete survivor emission, and three solver-free integer replays.
  Loaded survivors are replayed before being restored as no-goods, and the
  replay dependency closure is fingerprinted. Exact shell certificates now
  impose `n_9<=2`; the earlier bounded pilot found no candidate and has no
  exclusionary force.
- `LP333_ORDER3_PROFILE_ENDPOINT_SHELL.md`,
  `LP333_ORDER3_PROFILE_PENULTIMATE_SHELL.md`, and
  `LP333_ORDER3_PROFILE_SHELL_FOUR.md`: complete affine modulo-nine
  certificates exclude `n_9=6,5,4`.  The last checks 27,468,720 oriented
  medium frames and exactly replays 345,984 modular survivors.
- `shell_three_mod27/` and `shell_three_character/`: a signed-uniformizer
  skeleton quotient excludes `n_9=3`.  It exactly replays all 479,850
  modulo-nine/aggregate survivors, finds only two modulo-27 near witnesses,
  and rejects both exactly and by an independent cubic characteristic-37
  moment.
- `shell_two_exact/`: the complete `n_9=2` census is not empty.  It checks
  14,715,744 raw signed skeletons and 10,201,038 exact replays and proves
  that precisely five profile-zero symmetry orbits survive, with orbit sizes
  `24,12,12,12,24`.  All five pass detached all-37-lag, characteristic-37,
  prime-167, aggregate, and orbit replay.  Each has 54 placement trits and
  first Hensel rank/nullity `18/36`; compatible row-margin counts are
  `72,72,72,96,93`.  These are profile inputs, not `LP(333)` objects.
- `scratch_exact_profile_lift/`: a secondary exact XOR/CP-SAT model fixes the
  first shell-two representative and splits its 72 compatible row margins.
  Attempt zero is fully resumable and records 72 `UNKNOWN` statuses; it is a
  performance baseline, not an exclusion.  A five-minute union run peaked
  near 604 MB with no swap and also returned `UNKNOWN`.
- `phase_second_digit/`: all five shell-two profiles survive the complete
  quadratic next digit.  Six structured row-collapse coordinates are the
  residue layer of
  `(F_27 x F_27) tensor F_3[epsilon]/(epsilon^3)` and their exact joint map
  `F_3^36 -> F_3^6` is surjective, with fibers near `3^30`.  The full
  eighteen polar forms have scalar common centroid, which falsifies the
  proposed free rank-two ramified-module/Hensel shortcut.  A second-digit
  witness is therefore diagnostic, not a milestone.
- `structured_phase_families/`: exact solver-free tests of nine named phase
  families.  Three opposite-class-twisted families have respectively
  `2,916`, `174,960`, and `1,458` supergroup-free digit-one points, with no
  such digit-two survivor; these per-family sets may overlap.  The
  complete `F_27 x F_27` minimal-submodule family tests all 3,136 asymmetric
  channel pairs per profile, leaving six supergroup-free digit-one points
  and no digit-two point.  Its sole structured digit-two control is
  order-six fixed and fails digit three.
- `LP333_ORDER3_DENSE_SHELL_QUADRATIC_ALGEBRA.md`: the six quadratic
  correction forms relevant to `n_9=1,0` generate `F_27 x F_27` and sum to
  `2I`.  Exact affine restriction and Gauss bounds prove this universal
  form attains every right-hand side, so it cannot exclude either shell.
  The full six-coordinate layer can instead be counted with 729 exact
  quadratic character sums per skeleton and self-reduced to a witness.
- `LP333_ORDER3_PHASE_FACTOR.md`: profile norm 54 universally forces exactly
  54 signed Eisenstein unit phases and automatic physical frame energy 167.
  Exact primitive-nine lifting is one six-sequence complementary-frame
  identity plus one independent cross-fiber identity.
- `LP333_ORDER3_PHASE_PRIME167.md`: both phase equations are losslessly
  reduced modulo 167 by the `37/3/111` equality-orbit obstruction.  The
  primitive equations form a three-plane annihilator, and ninth-root
  recombination gives one Hermitian plus three bilinear cones in
  `F_(167^6) x F_(167^12)^6`.  The remaining gate is the sparse physical
  inverse-CRT intersection.
- `LP333_ORDER3_PHASE_FIBER_SUPPORT.md`: every nonzero zero/unit phase fiber
  is nonzero in both primitive prime-167 coordinates.  The two primitive
  vectors therefore have identical zero support, and the fixed zero column
  leaves only the dense stratum or the synchronized `B0`-zero stratum.
  Exactly 4,094 of 4,096 ambient joint support patterns are removed; the
  `B0`-zero primitive plane has rank at least two.
- `LP333_PHASE_CONE_TRIVIAL_BRANCH_OBSTRUCTION.md`: each channel's trivial
  coordinate is nonzero by the period-three margin kernel and total 167.
  The complete row catalog leaves exactly 1,411 nonzero coordinate pairs.
- `LP333_ORDER3_PHASE_TRACE_SIEVE.md`: row-Galois inversion and factorwise
  traces recover all physical coefficients; twelve fixed-origin equations,
  five displayed profile-support equations, and the inverse-DFT
  idempotence test are exact necessary constraints.
- `LP333_ORDER3_PHASE_CYCLIC_DECODER.md`: modulo seven gives thirteen scalar
  factors over `F_(7^3)`, exact local alphabets of size 1/9/27, and a compact
  nonlinear propagator.  The raw trellis/MITM/Wagner/BCH shortcuts audited
  there are not viable standalone decoders.
- `LP333_ORDER3_PHASE_TRANSFER.md`: the trivial-column character collapses
  to one integer energy and one Eisenstein cross term per channel and is
  exactly equivalent, with multiplicity, to the existing row-sum catalog.
  Use it only after finding a `D_t=0` profile; the current fixture counts are
  diagnostic.
- `LP333_ORDER3_PHASE_HENSEL.md`: the first `1-omega` placement digit is an
  affine `F_3` system. The diagnostic census has 21 rank-18 systems and one
  exact `(16,17)` contradiction, but every input already fails `D_t=0`.
- `LP333_ORDER3_DIAGONAL_FRAME_PREFIX.md`: augmentation plus the first
  characteristic-37 diagonal coefficient collapse to one-sequence tables of
  at most 444 states and joined tables of at most 666. All 22 diagnostic
  inputs survive; no second coefficient or full frame is claimed.
- `LP333_TWISTED_ORDER3.md`: the `<121>` and `<211>` lanes share an exact
  1,296-word, 108-orbit outer boundary and a complete row-axis lift.
- `NOVEL_LIFTING_64.md`: an 84-bit reciprocal `q` skeleton and finite 2-adic
  lift. The seed's first obstruction is a five-lag Frobenius square, while an
  augmented-rank certificate rules out a first-order tangent repair.
- `ELIAHOU_ADJACENT42_REPAIR.md`: the seed's 13 residuals cancel in an exact
  flat energy-14 fold modulo 42. The target energy 334 forces 80 new equal
  separation-42 pairs, an 80-sparse ternary group-ring shell, and the
  distance-41 reciprocal-pair frontier above.
- `ELIAHOU_ANTIFOLD42.md` and `ELIAHOU_ANTIFOLD_MOD2.md`: the complementary
  negacyclic fold turns the distance-41 frontier into 30 orientation-free
  support instances. Its first binary lift has rank exactly 21 in every
  reciprocal-`q` case. The binary lift leaves many supports and is not itself
  an exclusion.
- `FIVE_COMB_SECANT.md`: the complete seed defect is one rank-one ten-sparse
  carrier. Common-factor repairs are impossible, but a minimum complementary
  octet gives 32 flat carrier channels of energy 320 that pack into the target
  lengths with exactly 14 singleton holes. Cancelling the packing cross terms
  would directly construct `BS(84,83)`.
- `FIVE_COMB_PAIRED_LOBES.md`: distinct words in the two lobes reduce exact
  self-cancellation to one complementary length-five octet. There are 1,246
  octets and 768,512 sorted directed-pair inventories; the rank-nine
  projective quotient, 1,440 row orbits, physical hole fiber, and high-lag
  boundary table all survive. The first dyadic root sieves remove 0.1382% of
  the arbitrary-placement relaxation and 3.8039% of the narrower
  vertical-pair slice; the latter percentage must not be generalized.
- `FIVE_COMB_ROOT8_VERTICAL.md`: the primitive-eight rational/irrational join
  further cuts core 4 from 724,564 to 140,007 inventories and core 27 from
  229,408 to 65,868, still only in the vertical-pair slice.
- `FIVE_COMB_DYADIC_COMPRESSION.md`: every norm equation through order 16 is
  one exact periodic-autocorrelation identity on four `Z/16` compressions.
  A staged cyclotomic or meet-in-the-middle architecture is specified, but
  no production implementation is retained yet. Session sizing estimates
  put those designs below the host memory limit; a naive final-state DP does
  not fit.

The strongest current construction checkpoints are:

- `output/bs84_oriented_sds_local_p19.json`: verified prime-fold near state,
  profile `(37,37,35,41)`, quarter-energy 14, 11 bad lags, SHA-256
  `432b9708d77c7c45001265ad5ed0938e527af08a20782f0044d14a0ad65cc39c`;
- `output/lp333_order3_row_sum_catalog.csv`: exactly 1,756 order-three
  row-sum words, SHA-256
  `e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea`;
- the pure-axis order-three witness in
  `LP333_ORDER3_DIFFERENCE_FAMILY.md`: exact compression, row-sum PAF, and
  zero-column equations, but 51/54 independent nonzero-column equations bad,
  residual energy 8,320 and maximum residual 30, hence not an `LP(333)`;
- the dedicated order-three model: 11,790 variables/11,657 constraints
  before residual symmetry and 11,857/11,889 with the complete corrected
  `C6 x C2` lex leader. The valid B-only affine involution uses multiplier
  323; multiplier 260 is a checked counterexample, not a symmetry. A
  60-second pilot was `UNKNOWN` with no candidate;
- the Eisenstein local sieve: exactly 3,334/10,000 choices survive on each
  opposite-class pair, but pinned witnesses show all 22 aggregate shards
  survive after adding the origin energy. It is a factor-729 local reduction,
  not an elimination;
- the primitive-nine jet: a pinned local survivor passes digits zero and one
  but first fails digit two, proving the higher digits are nonredundant. No
  1,756-word catalog exclusion has yet been performed;
- the characteristic-37 transfer: rank 13, determinant 11, and 4,476 direct
  physical/cyclotomic equation checks. All 22 shards survive the joined first
  two coefficients, but none of their pinned witnesses passes all thirteen;
- the two fully labelled row-695 modular certificates: each passes 222
  primitive-nine equations and four exact row-direction equations; the trit
  certificate uses the pinned rank-18/nullity-36 upper lift. Both fail the
  stronger integral primitive-nine criterion in all 36 nonzero groups;
- the primitive-nine profile ideal: six displayed conjugate-pair tests but
  only five independent conditions; all 22 aggregate shards survive through
  pinned alternative profile tuples, each with a uniquely reconstructed
  exact target table. None of those 22 tuples survives the stronger full-LP
  zero-moment gate, so they are not phase-lift inputs;
- the full-LP profile zero gate: 22/22 fixed ideal-compatible tuples are
  excluded, with nonzero-class histogram `10:1, 12:21`; this is zero
  profile-tuple survival in the audited corpus but zero whole-shard
  exclusions;
- the exact finite zero detectors: lambda-cube plus all 13
  characteristic-37 coefficients, or the independent single-prime-167
  split.  Both are equivalent to exact zero on the shared profile domain;
  the prime-167 invariant algebra has dimensions `1+6+6` over
  `F_(167^2)`;
- the spectral-unit refinement: every physical profile-zero channel is a
  unit in that `1+6+6` algebra, so the modular intersection has no
  degenerate or axis branch and may be written as one unitary-ratio torus;
- the shell descent: `h=3,4,5,6` are empty, while `h=2` has exactly five
  profile-zero symmetry orbits.  The constructor enforces `n_9<=2`, but the
  five explicit `h=2` representatives are now the primary phase-lift inputs;
- the shell-two placement digit: all five first-digit affine spaces have
  dimension 36; the six structured second-digit coordinates are exactly
  surjective with fibers near `3^30`, while the full polar centroid is only
  the scalar algebra.  Do not treat one second-digit point or an automatic
  module lift as evidence of convergence;
- the dense-shell quadratic algebra: the six correction matrices form
  `F_27 x F_27`, their sum is radial, and exact Gauss bounds rule out a
  one-form anisotropy shortcut in `h=1,0`.  Use the 729-character full-map
  count instead of enumerating a phase cube;
- the sparse-`B` relative-norm screen: only four of 17 algebraic norm types
  remain in the normalized energy-six allocation for the two `(163,4)`
  targets.  Continue only from those 84 words/eight lift-safe orbits;
- the exact profile symmetry and hardened constructor: seven formal target
  orbits, twelve lift-compatible target orbits, a 3,334-to-1,409 quartet
  layer, direct exact-zero equations, and a deterministic semantically pinned
  checkpoint queue.  No hardened-model campaign or negative result exists;
- do not build the obvious balanced prime-167 profile MITM: its
  `3,334^3=37,059,263,704` injective half list requires more than 151 GiB
  before field data.  The exact channel-first fallback uses little RAM but
  still needs 6,338,555,429 degree-12 signatures across the seven targets;
- the three-fiber phase factor: every norm-54 tuple has 54 signed unit
  phases, automatic diagonal frame energy 167, and exactly two independent
  Eisenstein group-ring equations;
- the full phase prime-167 theorem: both equations are exact modulo 167; the
  39 prime-field component conditions recombine into one Hermitian cone and
  three bilinear cones with complete branch parameterizations.  The direct
  ninth-root bridge and generic/both-axis recovery cases are pinned.  No
  sparse physical point is known;
- the phase-fiber support theorem: only the dense and synchronized
  `B0`-zero support strata can be physical.  It removes all one-sided and
  other coordinate-degenerate branches but leaves both surviving strata
  large;
- the prime-167 physical-intersection refinements: the trivial zero branch is
  impossible; row-Galois and factorwise trace inversion expose fixed-origin
  and profile-support equations; inverse-DFT idempotence exactly recognizes
  physical local words; the independent mod-seven split supplies thirteen
  scalar propagation factors;
- the phase refinements are reusable but diagnostic on the present corpus:
  the trivial-character transfer equals the row-sum catalog, the first
  Eisenstein-adic digit has one fixed-profile contradiction, and the
  augmentation-plus-`T_1` diagonal prefix leaves all 22 tuples;
- `output/antifold42_q0_proof/`: the only certified anti-fold exclusion,
  containing the 39,580-variable CNF, compressed binary DRAT proof,
  `certificate.json`, and narrow-scope README. The default verifier checks
  metadata, hashes, and DIMACS shape; full `drat-trim` replay is optional;
- the coupled `<121>/<211>` boundary: `36 -> 12 -> 6,048 -> 1,296` row
  states, 216 row-dihedral orbits, 108 extended classes, and all 1,296
  feasible on the zero-column axis. Only nonzero-column lags remain useful;
- the old quartic energy-112 and sextic energy-784 tables remain verified
  non-candidates in families now proved empty; their search programs are
  historical regressions, not continuation points;
- no character checkpoint survives: the independently decimated
  degree-at-most-two Sidelnikov family has zero row-admissible orientation
  matches and zero exact PAF joins.

Read `README.md` for the lane map, `RESEARCH_LOG.md` for chronology, and
`PRIORITY_AUDIT.md` before making any novelty or publication claim.
Read `ELIAHOU_ADJACENT42_REPAIR.md` before doing any further seed-centered
search: base-row shells through radius 79 and special-coordinate shells
through radius 40 are now excluded. Then read `ELIAHOU_ANTIFOLD42.md`,
`ELIAHOU_ANTIFOLD_MOD2.md`, and `ELIAHOU_ANTIFOLD42_CENSUS.json`: case 0 is
certified closed, case 1 is unproved, and cases 2-29 are `UNKNOWN`.
`VARIABLE_Q_ROOT8.md` remains the sharp primitive-eight necessary-condition
audit.

## Theory-first continuation order

1. Attack the full mixed equations of the order-three `<10>` quotient through
   new algebraic invariants. Start from the exact 1,756-word row-sum catalog,
   the 24-triple formulation, the 13-condition Eisenstein identity, the
   six-digit primitive-nine jet, invertible characteristic-37 transfer,
   labelled `F_729` split, pinned trit linearization, exact integral
   primitive-nine criterion, profile ideal, three-fiber phase factor, and the
   audited `9 x 13` quotient. Do not
   spend more time strengthening only the pure-axis or first mod-three layer:
   all 1,756 rows and all 22 Eisenstein shards already pass those tests. The
   next exact task is to test structured phase families on all five
   `n_9=2` orbits and to lift through at least two consecutive digits beyond
   the quadratic layer, while estimating the complete exact replay cost.
   A point satisfying only the quadratic second digit is not a progress
   gate: the structured six-coordinate subsystem alone leaves about `3^30`
   points per profile.  Work on `n_9=1,0` should use the `F_27 x F_27`
   729-character compression rather than phase enumeration.  The general
   seven-target CRT constructor remains the fallback for discovering dense
   profile inputs.  The prime-167 channel-first MITM is a low-memory
   fallback, not the primary route at its current 6.34-billion-signature
   cost.  Any new spectral constructor should use the unitary ratio
   `U=A B^(-1)` and the single nonzero torus, never the now-excluded
   degenerate or axis branches. Do not phase-lift the 22 pinned
   ideal-compatible tuples: the exact zero-moment audit already excludes
   every one as a full-LP input. The five certified shell-two zero-moment
   survivors should proceed through the nonzero trivial-coordinate catalog,
   row-Galois trace
   inverse, local idempotence decoder, mod-seven factors, exact margins, and
   full replay. A fixed-profile exclusion is not a
   whole-shard exclusion. Strictly expand and verify any full quotient before
   any claim.
2. Build the universal four-directed-pair model from
   `FIVE_COMB_PAIRED_LOBES.md`. Filter it with the modulo-16
   meet-in-the-middle, the retained roots `+1,-1,i,zeta_8`, and the high-lag
   boundary table before imposing all 83 lags. Omit the universally
   impossible structural core zero, leaving 31 cores, and prioritize the 21
   genuinely nondecomposable octet profiles.
3. Continue the prime-83 oriented-SDS construction outside the exact
   neighborhood already exhausted around profile 19. Any prime fold
   automatically triggers its finite modulo-84 lift bank.
4. Continue the 30 orientation-free anti-fold support instances before any
   wider seed-centered search. Case 0 is certified closed. Case 1 requires a
   fresh proof-producing run before its solver observation becomes a theorem;
   cases 2 through 29 are `UNKNOWN`. Only a surviving support proceeds to
   the adjacent-fold endpoint-orientation lift.
5. Treat the `<121>` and `<211>` order-three multiplier subgroups as coupled
   secondary lanes, starting after their shared 1,296-word row-axis theorem.
   Do not duplicate that completed outer work. Do not resume the quartic,
   sextic, or 48 diagonal common-type five-comb searches: those restricted
   families are closed.

These lanes may use several gigabytes when needed, but keep total machine RSS
below 16 GB. Do not resume the old radius-18 shell expansion or the generic
666-bit Legendre model as the primary strategy.

For the publication snapshot, also read `MANIFEST.md`,
`proof_certificates/README.md`, and `tu41_certificate/README.md`.  The exact
next certification task is an orbit-count CNF for the six hard radius-18 root
leaves.  Do not resume the tested raw-bit or combined z7/z14 hard pilots
unchanged: one reached 1.785 GB RSS without finishing, and scaling it to a
corpus would waste both memory and disk.

## Authoritative Legendre checkpoints

The current sampled modulo-9 catalog has 21 orbit-distinct profiles in
`legendre_333_profile_catalog.py`.  It is not exhaustive.

- `output/legendre_333_profile4_local_60s.json`: catalog incumbent, E2280.
- `output/legendre_333_profile4_radius2.json`: unchanged signs after engine
  radius-two polish.
- `output/legendre_333_profile4_mixed.json`: unchanged signs after the complete
  mixed six-cycle/opposite-checker scan.
- `output/legendre_333_profile4_eight.json`: unchanged signs after the complete
  connected alternating-eight-cycle scan.
- `output/legendre_333_profile19_local_60s.json`: secondary E2336 checkpoint.
- `output/legendre_333_profile19_extended.json`: unchanged profile-19 signs
  after pair, six-cycle, and eight-cycle polish.

All are verified nonexact checkpoints.  Profile 4 has 120 bad independent
lags.  Its independently verified local results are:

- product switch-graph radius-two ball: 17,801,598 states, no descent;
- mixed six-cycle/opposite-checker neighborhood: 749,359,042 states, unique
  minimum E2408;
- connected alternating-eight-cycle neighborhood: 9,549,173 states, minimum
  E2568 with multiplicity two.

These statements do not cover the whole fixed-margin fiber.

SHA-256 provenance for the six principal files:

```text
b060fce197ed2346e0c350350a634d53a6753640cecccd3f262bf87832dba270  output/legendre_333_profile4_local_60s.json
d9805de89ab5a558aba23ab122667bbde47ad92de87e840737d4d16c8dcbc18a  output/legendre_333_profile4_radius2.json
9d10e3aabab0f933b81b2f706a973dd17c5d747de2498882fa59cf669668b0cf  output/legendre_333_profile4_mixed.json
658c9bb02549da8042e00d074a8c3c88cff4f23789a9b936b48bb5b8750d906b  output/legendre_333_profile4_eight.json
0807e0bd4a1a4756c1e289fee05ccf47610ac4e240795507998f6fde1a43307e  output/legendre_333_profile19_local_60s.json
591baeb68e55be17f661c6c572c6b190cfa226b52c7bd7ca99b2dcf537924bc5  output/legendre_333_profile19_extended.json
```

## Rebuild and verify

Create the solver environment if needed:

```sh
python3 -m venv .solver-venv
.solver-venv/bin/python -m pip install -r requirements.txt
```

Run the complete Python suite:

```sh
.solver-venv/bin/python -m unittest discover -v
```

Build the fixed-memory engine and independent verifiers:

```sh
clang++ -std=c++17 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  search_legendre_333_profile_local.cpp \
  -o ../tmp/search_legendre_333_profile_local
clang++ -std=c++17 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  verify_legendre_333_profile_radius2.cpp \
  -o ../tmp/verify_legendre_333_profile_radius2
clang++ -std=c++17 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  verify_legendre_333_profile_mixed.cpp \
  -o ../tmp/verify_legendre_333_profile_mixed
```

Replay the retained center and finite-neighborhood certificates:

```sh
../tmp/search_legendre_333_profile_local --self-test
python3 verify_legendre_333_profile_local.py \
  output/legendre_333_profile4_eight.json
../tmp/verify_legendre_333_profile_radius2 \
  output/legendre_333_profile4_radius2.json
../tmp/verify_legendre_333_profile_mixed \
  output/legendre_333_profile4_mixed.json
../tmp/verify_legendre_333_profile_mixed --eight \
  output/legendre_333_profile4_eight.json
```

If any search ever reports energy zero, do not edit the checkpoint.  Run:

```sh
python3 verify_legendre_333.py PATH_TO_CANDIDATE.json
```

Only a successful full-matrix check permits an `H(668)` claim.

## Safe continuation points

Audit the complete distance-41 reduction and the one certified leaf before
continuing its census:

```sh
python3 verify_eliahou_adjacent42_repair.py
python3 verify_eliahou_antifold42.py
../tmp/hadamard-env/bin/python verify_eliahou_antifold_mod2.py
python3 verify_eliahou_antifold_q0_proof.py
../tmp/hadamard-env/bin/python search_eliahou_antifold_sat.py \
  --ignore-profiles --start 0 --stop 30 --list-instances
../tmp/hadamard-env/bin/python search_eliahou_antifold_sat.py \
  --ignore-profiles --start 2 --stop 30 --time-limit 1800
```

The last command records timeout or interruption as `UNKNOWN`; it never
turns either into an exclusion. Canonical case 1 still needs an independently
checked proof-producing run. Do not use the earlier Python-wrapper proof
capture as evidence: it failed replay and was removed. To replay the retained
case-0 proof itself:

```sh
python3 verify_eliahou_antifold_q0_proof.py \
  --full --drat-trim /absolute/path/to/drat-trim
```

The primary exact continuation is the order-three quotient. Rebuild and
audit its finite front end before changing the model:

```sh
clang++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  enumerate_lp333_order3_row_sums.cpp \
  -o ../tmp/hadamard_668_build/enumerate_lp333_order3_row_sums
../tmp/hadamard_668_build/enumerate_lp333_order3_row_sums \
  --emit-words output/lp333_order3_row_sum_catalog.csv
python3 verify_lp333_multiplier_row_sum.py
python3 verify_lp333_order3_difference_family.py
python3 verify_lp333_order3_mod3_sieve.py
python3 verify_lp333_order3_primitive9_jet.py
python3 verify_lp333_order3_char37_transfer.py
python3 verify_lp333_order3_labeled_jet.py
python3 verify_lp333_order3_trit_lift.py
python3 verify_lp333_order3_integral9.py
python3 verify_lp333_order3_profile9.py
python3 verify_lp333_order3_profile9_shards.py
python3 verify_lp333_order3_profile_zero_gate.py
python3 verify_lp333_order3_profile_crt.py
python3 verify_lp333_order3_prime167_split.py
python3 verify_lp333_order3_profile_zero_symmetry.py
python3 verify_lp333_order3_phase_factor.py
python3 verify_lp333_order3_phase_transfer.py
python3 verify_lp333_order3_phase_hensel.py
python3 verify_lp333_order3_diagonal_frame_prefix.py
python3 verify_lp333_twisted_order3.py
../tmp/hadamard-env/bin/python verify_lp333_order3_lift_catalog.py \
  --workers 4 --time-limit 2
```

The exact quotient constructor may fix one catalog row with
`--row-sum-index`. An `UNKNOWN` status eliminates nothing, and repeating
unstructured bounded solves is not the research priority. A reported
assignment is accepted only after the full `LP(333)` and `H(668)` candidate
gate succeeds. The old sequential sextic signature corpus must not be
resumed; the row-sum theorem proves that family empty.

The best low-memory continuation command is reproducible but has low expected
value after the closed local neighborhoods:

```sh
../tmp/search_legendre_333_profile_local \
  --initial-checkpoint output/legendre_333_profile4_eight.json \
  --seconds 3600 --seed NEW_INTEGER_SEED \
  --output output/legendre_333_profile4_continued.json
```

New compressed profiles can be sought one centered-norm shard at a time:

```sh
.solver-venv/bin/python search_legendre_333_profile_catalog.py \
  --count 1 --time-limit 60 --max-memory-mb 128 \
  --centered-norm-shard EVEN_INTEGER_76_TO_148 \
  --exclude-catalog --profile-symmetry basic \
  --output output/legendre_333_profile_sample.json
```

An `UNKNOWN` status proves nothing.  A new compressed profile is only a new
restricted fiber and must be added to both the Python catalog and C++ table
before screening.

For the unrestricted special-Golay route, the live exact search is the 156
canonical `BS(84,83)` representative shards documented in
`VARIABLE_Q_LANE.md`.  The radius-18 result excludes only the raw labelled ball
around Eliahou's seed.

For the structured five-comb route, do not resume
`output/five_comb_unrestricted_core_cp_v2`: it is complete. Start from the
distinct-lobe universal model specified in `FIVE_COMB_PAIRED_LOBES.md`.

## Resource rules for the 16 GiB host

- Keep combined resident memory below roughly 14 GB so the OS and verifier
  retain headroom. Multi-gigabyte exact joins are allowed.
- Multi-process sharding is allowed when ranges are disjoint and measured
  aggregate RSS stays below the limit. During the completed common-type
  sweep, the live session monitor observed four processes at roughly 1.4 GB
  aggregate RSS; that measurement is not encoded in the shard records.
- Keep the oriented-SDS CP-SAT constructor at one worker; its model and
  checkpoint format assume that reproducible mode.
- Treat `max_memory_in_mb` as an internal solver limit, not a process limit.
- The new order-three front end is small: 2.82 MB for the C++ catalog,
  below 29 MB for the Eisenstein replay/tests, 114.1 MB for the complete
  histogram replay, and 390.4 MB for the latest full quotient pilot, all with
  zero swap. The primitive-nine replay stayed below 22 MB and the
  labelled-jet tests below 30 MB; the pinned trit reconstruction stayed below
  100 MB. The twisted-lane verifier/tests stayed below 94 MB. The anti-fold
  case-0 solve used 163.9 MB and full DRAT replay used 471.1 MB. The
  paired-lobe root replays used at most about 712 MB.
- Do not enlarge the full 111,554-variable fixed-profile model here: measured
  whole-process peaks were 703 MB and 931 MB in short pilots despite lower
  internal limits.
- The quartic LP constructor uses about 6 MB. The dependency-free sextic and
  dyadic checkers use only tens of megabytes. The deepest oriented-SDS exact
  polish used 927 MB RSS; the independent Sidelnikov-decimation join used
  about 137 MB.
- Record seed, command, wall time, maximum RSS, swap count, solver status, and
  output hash for every retained production result.

The next high-value step is structural mathematics or distributed exact
sharding, not indefinite repetition of the same local annealer.
