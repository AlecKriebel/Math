# Hadamard order 668 search

Status: active computational research; no exact matrix has been found yet.

This directory is a reproducible attack on the smallest unresolved Hadamard
order.  A result counts only when an explicit `668 x 668` sign matrix passes an
exact, dependency-free check of `H H^T = 668 I`.  Near solutions and solver
status are diagnostics, never discoveries.

`RESUME.md` is the compact handoff for restarting this project after a pause.
`PRIORITY_AUDIT.md` records the provisional novelty and publication audit for
this milestone.

## Current map

| Lane | Status | Scope / finish line |
|---|---|---|
| Eliahou seed verification | reproduced near matrix | published 64-modular matrix of order 668, not an exact Hadamard matrix |
| Repair with Eliahou's exact `q` | impossible | reduces to empty `TU(41)` |
| Repair with Eliahou's exact `s` | impossible | already contradicted by the `z=1` sum-of-two-squares norm |
| Variable `s,q` special quadruple | active | adjacent cyclic folds at 84 and prime 83; root/margins force seed distance at least 34 |
| Prime-83 oriented SDS | implemented construction lane | best verified checkpoint has quarter-energy 14 and 11 bad lags; no prime fold yet |
| Prime-83 character families | closed restricted lane | degree-two Sidelnikov products, phases, signs, and independent decimations excluded exactly |
| Common-type five-comb packing | closed restricted lane | all 48 quartets and 32 projective cores solver-excluded; no proof certificates |
| Distinct-lobe five-comb packing | active construction lane | 1,246 complementary octets; projective rank-nine and high-lag reductions survive |
| Sextic-multiplier `LP(333)` | closed restricted lane | exact row-sum obstruction; 2,309,472 projected states over all normalized zero cores, zero hits |
| Quartic-multiplier `LP(333)` | closed restricted lane | exact row-sum obstruction; 38,880 projected states over all normalized zero cores, zero hits |
| Order-three multiplier `LP(333)` | active theory-led lane | `<112>` closed; `<10>` has 1,756 row sums, 22 Eisenstein shards, and a primitive-9 jet; `<121>,<211>` share a 1,296-word/108-orbit outer boundary |
| Symmetric/skew `LP(333)` | impossible sublane | mod-3 norm obstruction |
| Circulant good matrices of order 167 | active | two row-sum profiles; an exact quadruple gives a skew `H(668)` |
| Unrestricted cyclic SDS of order 167 | active heuristic lane | ten row-sum profiles; an exact quadruple gives `H(668)` |

The published 64-modular seed is encoded exactly in `seed.py`.  Run its full
regression check with:

```sh
python3 verify_seed.py
```

The initially natural repair lane—hold Eliahou's
`q=(83,2,81,1)` fixed and change `s`—is now closed.  A parity telescope forces
any exact repair to decimate to a Turyn sequence in `TU(41)`, but `TU(41)` is
empty by the published exhaustive classification of Edmondson, Seberry, and
Anderson.  The new reduction has a dependency-free symbolic checker and a
self-contained explanation.  In addition, `tu41_certificate/` independently
reproduces the endpoint with a deterministic, low-memory enumeration:
461/461 shards, 57,543,021 nodes, and zero solutions.  This modern
reproduction supports, rather than supersedes, the 1994 theorem:

```sh
python3 verify_fixed_q_obstruction.py
python3 tu41_certificate/verify_manifest.py
python3 tu41_certificate/verify_cube_cover.py \
  tu41_certificate/cubes_depth5.txt
```

See `FIXED_Q_OBSTRUCTION.md` for the precise scope and literature dependency.
The old fixed-q CP-SAT, CNF, and local encodings are retained as regression
artifacts, not as live searches.

## Live lane 1: variable q and `BS(84,83)`

Allowing both `s` and `q` to vary is exactly the base-sequence problem
`BS(84,83)`.  `VARIABLE_Q_LANE.md` proves the bijection, derives 288 exhaustive
nominal ordinary/alternating margin shards, and quotients them to 156 search
representatives by global coordinate alternation.  It also documents the exact
CP-SAT model:

```sh
python3 -m venv .solver-venv
.solver-venv/bin/python -m pip install -r requirements.txt
python3 variable_q_base.py
.solver-venv/bin/python search_variable_q_cp_sat.py \
  --shard 0 --workers 1 --max-memory-mb 2048 --time-limit 3600
```

`VARIABLE_Q_ROOT8.md` gives a new dependency-free obstruction obtained by
evaluating the base norm at a primitive eighth root. It splits the norm over
`Q(sqrt(2))` into a 16-square equation of energy 334 and one bilinear
equation. Eliahou's seed has rational energy 1614. A complete 16-coordinate
dynamic program proves that the primitive-eight sphere begins at distance 33;
an exhaustive check of all 1,350 minimum-shell targets against the exact
ordinary/alternating margin norms raises the base-sequence lower bound to 34,
closing the complete ball through radius 33 without solver trust. An explicit
radius-34 witness also passes both root equations, both margin norms, and every
endpoint-quad product, so this combined relaxation is sharp. The same method
also proves that holding Eliahou's `s`
fixed is impossible, since the fixed `A,C` contribution is already
`807+24*sqrt(2)>334`. The root-eight equations are now included in the exact
CP-SAT model by default:

```sh
python3 variable_q_root8.py
```

`NOVEL_BS84_THEORY.md` gives a new exact construction formulation. For
general `BS(n+1,n)`, all aperiodic equations are equivalent to the
simultaneous complementarity of two adjacent cyclic folds: pad the short
sequences modulo `n+1`, and fold the long endpoints modulo `n`. At `n=83`,
the prime fold becomes 41 oriented supplementary-difference-set equations on
`Z/83`; its mod-2 shadow is a relative norm equation over
`GF(2^82)/GF(2^41)`. There are 45 anchored size profiles. Once a prime-fold
object is found, only `82*83^2=564,898` multiplier/phase lifts need be tested
against the modulo-84 fold, and any pass is an exact `BS(84,83)` by the
adjacent-fold theorem:

```sh
python3 check_bs84_cyclic_folds.py
```

`NOVEL_LIFTING_64.md` gives a complementary 2-adic formulation. Exactness
first forces an 84-parameter reciprocal skeleton for `q`; the next lift is
linear in `s` and has rank 82 at the published seed. Eliahou's point already
passes through the quartic/modulo-16 layer. Its first failed lift consists of
only five lags and is a Frobenius square, but an exact Boolean-Jacobian
certificate proves that no first-order tangent direction repairs it. The
remaining constructive proposal is therefore a nonlinear five-comb move
coupled to 42 linear causal-mate equations:

```sh
python3 verify_novel_lifting_64.py
```

`FIVE_COMB_SECANT.md` sharpens the seed identity to

```text
sum N(X) = 14 + 32*N((z^42-1)(1-z^4+z^8-z^12+z^16)).
```

The literal 30-variable reciprocal chord and every aligned orthogonally
staged disjoint five-comb completion are exactly excluded. More generally, a
unit-circle root of the common comb rules out every repair that retains that
factor in all four sequences. The checker then supplies a constructive escape:
a minimum complementary octet, polarized at separation 42 and doubled, gives
32 flat carrier channels of energy 320. Those channels pack into the target
lengths with exactly 14 singleton holes. The live finite problem is to assign
the carrier channels and hole signs so that the packing cross terms cancel:

```sh
python3 verify_five_comb_secant.py
```

`FIVE_COMB_PROJECTIVE_EXHAUSTION.md` solves the complete modulo-four
projective quotient for the common-type construction. Row-sign normalization
leaves twelve label bits and 4,096 maps; row-pair swaps reduce these to 1,440
orbits, and the physical holes form a label-independent 256-point fiber.
The exact lags-78-through-81 boundary table leaves 2,434 possible projective
parameter rows. A resume-safe exact sweep then reports `INFEASIBLE` for all
1,536 quartet/core models. This is a solver-backed exclusion of that family,
not a proof certificate and not an exclusion of arbitrary five-combs:

```sh
python3 verify_five_comb_high_lag_boundary.py
python3 verify_five_comb_unrestricted_full_corpus.py
```

`FIVE_COMB_PAIRED_LOBES.md` gives the constructive escape. Same-word carriers
form an ordered pair of complementary quartets, but allowing distinct words
in the two lobes needs only one complementary octet. There are 1,246 such
octets and 768,512 sorted directed-pair inventories; 721,984 are genuinely
beyond separate lower/upper quartets. The rank-nine projective quotient,
1,440 row orbits, physical hole fiber, and lags-78-through-81 table all remain
valid. A new universal `z=1` row-square obstruction removes structural core
zero before any carrier search: all 128 of its row-orbit representatives
would require 165 or 166 to be a sum of two squares. Thus only 31 structural
cores remain. `FIVE_COMB_DYADIC_COMPRESSION.md` replaces the root conditions
through order 16 by one exact `Z/16` compressed autocorrelation identity and
specifies a staged or meet-in-the-middle architecture whose production
implementation is not yet retained:

```sh
python3 verify_five_comb_paired_lobes.py
python3 verify_five_comb_core0_obstruction.py
python3 verify_five_comb_dyadic_compression.py
```

`BS84_ORIENTED_SDS_SEARCH.md` implements the prime-fold constructor rather
than the original 334-sign aperiodic search. The retained profile-19 state has
sizes `(37,37,35,41)`, row sums `(8,10,13,1)`, quarter-energy 14, and 11 bad
independent lags. It is a verified checkpoint, not a prime fold. Its exact
structured neighborhood—including up to three inverse-pair changes and
coordinated single/double exchanges—contains no zero. The Python constructor
is resumable across all 45 profiles and automatically tests all 564,898
modulo-84 lifts if it finds a prime fold:

```sh
python3 verify_bs84_oriented_sds.py --allow-checkpoint \
  output/bs84_oriented_sds_local_p19.json
```

The safe-prime identity `167=2*83+1` yields a further exact character
calculation. `PRIME83_SIDELNIKOV_FOLD.md` proves that a binary Sidelnikov word
and its one-zero skew companion have summed PAF `-2` at every nonzero lag.
The natural endpoint completion and its degree-two product extension fail.
`PRIME83_SIDELNIKOV_DECIMATIONS.md` then allows independent block
decimations and proves the universal orientation condition

```text
U_k U_-k = v_k v_-k,  k=1,...,41.
```

The row-admissible fingerprint catalogs are disjoint. An independent exact
join checks 12,584,792 normalized `U/V` states and finds no prime fold:

```sh
python3 check_bs84_sidelnikov_fold.py
```

`VARIABLE_Q_LOCAL_NOTES.md` documents the margin- and endpoint-parity-
preserving C++ engine and its independently rejected diagnostic checkpoints.
The tracked parity-feasible checkpoint is now in canonical shard 213; it has
half-energy 232 and 43 bad lags, so it is not a solution.  The exact CP model
uses the standard four-literal base-sequence quad parities by default; the
older endpoint telescope is an equivalent optional basis.

`VARIABLE_Q_SEED_DISTANCE.md` retains a superseded solver-backed raw-radius-18 report
around Eliahou's published base quadruple.  A dependency-free dynamic program first
enumerates every raw margin image and proves that no quad-preserving target is
reachable through radius 13.  Exact fixed-margin CP-SAT models with table-
encoded primitive 3rd-, 4th-, and 6th-root norms then report infeasibility
for all 197 margin-plus-quad targets through radius 16 and all 276 targets in
the exact distance-17 shell.  At distance 18, an exact modulo-12 endpoint-quad
quotient
classifies the recorded root frontier as 811 infeasible targets and 12
decoded witnesses.  Primitive-7 or primitive-14 models report those 12
targets infeasible.  A dependency-free artifact checker verifies all nine hashes,
selection edges, and witnesses.  The recorded runs used one worker, peaked
at 176 MB resident memory with no swaps, and make no exact-`BS(84,83)` claim
outside this finite ball.  The checker does not replay any solver
infeasibility proof: a proof-grade release still requires independent
certification of 1,284 root-layer and 12 compression-layer `INFEASIBLE`
statuses.  `proof_certificates/` is the first proof-producing upgrade: four
representative root/compression leaves regenerate to deterministic CNF and
pass independent DRAT replay.  That is 4/1,296 coverage, not a proof of the
whole radius-18 report.  All twelve stored root witnesses separately pass
exactly pinned positive-CNF validation, closing the known-feasible encoding
gate.  Hard-leaf pilots reached 1.785 GB RSS, so no
memory-risking full batch was launched; the next planned step is an exact
orbit-count CNF for the six hard root leaves.

`VARIABLE_Q_PARITY_NEIGHBORHOOD.md` gives a deterministic exact scan inside
the checkpoint's same-margin, endpoint-parity-feasible subspace.  The
checkpoint is a strict local minimum against every such change of at most six
coordinates; this bounded result says nothing about radius eight, other
margins, or parity-infeasible intermediate states.

`VARIABLE_Q_NEIGHBORHOOD.md` records a separate CP-SAT search with every
symmetry quotient disabled.  The exact finite models through raw Hamming
radius 16 are `INFEASIBLE`: no exact base sequence with the checkpoint's
shard-213 margins occurs in that ball.  This result deliberately does not
cover different-margin neighbors, the raw shard-235 partner ball, or an
unrestricted 334-sign neighborhood.

`VARIABLE_Q_COMPRESSION.md` gives an exact factor-14 signature join over all
288 nominal shards.  It eliminates no shard and proves that this compression
is Fourier-equivalent to constraints already exposed in the CP model.  The
implemented factor-12 compression to length seven adds new primitive-seventh-
root propagation relative to those exposed invariants, but it also eliminates
no shard and remained slower in a short matched benchmark, so
`--compression-7` is optional.

`VARIABLE_Q_JOINT_COMPRESSION.md` derives a bounded-memory filter that couples
the primitive-7 compression to the compression after coordinate alternation,
thereby exposing primitive-14 information.  A 30-second shard-213 run ended
`UNKNOWN` at 111 MB peak RSS; it found neither a compressed witness nor an
infeasibility result.  The all-representative scan has not been run, so no
shard-elimination claim is made.

## Live lane 2: fixed-compression `LP(333)`

`LEGENDRE_333.md` describes the exact model inside the conjecturally motivated
factor-9 compressed subfamily, its further compression constraints, local
engine, and full bordered two-circulant verification:

```sh
.solver-venv/bin/python search_legendre_333_cp_sat.py \
  --workers 1 --max-memory-mb 2048 --time-limit 3600 \
  --output output/legendre_pair_333.json
```

`NOVEL_LP333_THEORY.md` recasts the binary pair as one QPSK sequence on
`Z_9 x F_37`. The quartic residues form a cyclic `(37,9,2)` difference set,
which yields an exact multiplier quotient with 45 fourth-root phases and only
22 equations. A checked `9 x 5` phase table satisfies the prescribed
compression and both coordinate axes, but the later row-sum theorem proves
that no fixed-compression order-nine quotient can satisfy the mixed
equations. The old constructor and table are retained as exact historical
regressions:

```sh
python3 check_lp333_quartic_quotient.py
```

`LP333_MULTIPLIER_ROW_SUM.md` gives the decisive exact projection. For a
column-only multiplier subgroup of size `h`, sum all 37 column-lag equations
and write the complete row sum as `s`. Every candidate must satisfy

```text
Re PAF_s(0)=297,       Re PAF_s(a)=-37  (a=1,...,4).
```

The zero-column equations force one 972-word normalization orbit. Exact
integer enumeration then gives no target profile for `h=18`, `h=9`, or
`h=6`, closing the quadratic-residue, quartic, and sextic
fixed-compression families. Across all zero cores the `h=9` and `h=6`
replays check 38,880 and 2,309,472 projected states, respectively, with zero
hits. These are complete restricted-family obstructions, not solver
timeouts.

The sextic `9 x 7` quotient and its 108-sign CP model remain useful regression
artifacts. Its former 298 signature shards should not be resumed:

```sh
python3 check_lp333_sextic_quotient.py
python3 verify_lp333_sextic_c3.py
python3 -m unittest -v \
  test_lp333_sextic_quotient.py test_lp333_sextic_cp_sat.py
```

At the sharp viable boundary `h=3`, a dependency-free C++ enumeration checks
46,503,026 energy-and-sum states and finds exactly 1,756 row-sum words. The
catalog is byte-pinned in `output/lp333_order3_row_sum_catalog.csv`. Every one
passes the exact zero-column/signature lift, which is equivalent to choosing
24 cyclic triples in `Z/9` with four signed incidence margins and four
difference totals equal to 18. This proves that the pure-axis layer is a
reformulation, not a useful filter.

`LP333_ORDER3_DIFFERENCE_FAMILY.md` freezes one such 24-triple lift and
expands it through all 333 entries. It is deliberately a non-candidate:
51 of its 54 reversal-independent nonzero-column equations fail, including
all six geometric column-axis equations. The dedicated
`search_lp333_order3_cp_sat.py` model therefore imposes the full 58 quotient
equations on 216 primary sign bits, with the row-sum catalog as an exact
redundant channel. Its exact baseline has 11,790 variables and 11,657
constraints; the full residual `C6 x C2` lex leader gives 11,857 variables
and 11,889 constraints. The corrected involution is
`B'[n]=B[323n+111]`; the tempting class-fixed multiplier 260 is explicitly
disproved by a PAF counterexample. Any assignment must pass the full
`LP(333)` and `668 x 668` save gate before reaching disk. A 60-second
four-worker pilot ended `UNKNOWN` with no candidate; it proves nothing
negative.

`LP333_ORDER3_EISENSTEIN.md` factors the nontrivial three-row Fourier channel
exactly. Each 100-state Gaussian class catalog is a product of two ten-state
binary profiles, and the compressed problem is equivalent to two
`H`-invariant Eisenstein sequences on `F_37` satisfying

```text
a*a^* + b*b^* = 167 delta_0.
```

Seven of the former 20 real equations are dependent, leaving one energy
equation and six Eisenstein equations, or 13 integer conditions. The 1,756
row-sum words collapse to 22 aggregate shards in six norm-pair types. A
ramified-prime sieve retains exactly 3,334 of 10,000 choices on each
opposite-class pair, but explicit witnesses show that all 22 shards survive
this local sieve plus the origin energy. This is a sharp algebraic reduction,
not a construction or infeasibility proof.

`LP333_ORDER3_PRIMITIVE9_JET.md` restores placement information lost by the
three-row compression. In the exact local ring

```text
F_3[pi]/(pi^6),       pi=1-zeta_9,
```

the canonical zero-column power is 5 and
`v_pi(167-5)=v_pi(162)=24`. All six jet digits must vanish. Digit one is
exactly the 3,334/10,000 Eisenstein pair sieve; digits two through five
contain new nonzero/nonzero class products. A pinned local survivor first
fails digit two, with nonzero-lag residual census `(0,0,18,24,30,24)` across
digits zero through five. This proves strictness beyond the local pair sieve,
but no complete row-sum catalog entry is yet excluded.

Reproduce the new exact layer with:

```sh
python3 verify_lp333_multiplier_row_sum.py
python3 verify_lp333_order3_difference_family.py
python3 verify_lp333_order3_mod3_sieve.py
python3 verify_lp333_order3_primitive9_jet.py
../tmp/hadamard-env/bin/python verify_lp333_order3_lift_catalog.py \
  --workers 4 --time-limit 2
../tmp/hadamard-env/bin/python -m unittest -v \
  test_lp333_multiplier_row_sum.py \
  test_lp333_order3_difference_family.py \
  test_lp333_order3_mod3_sieve.py \
  test_lp333_order3_primitive9_jet.py \
  test_lp333_order3_lift_catalog.py \
  test_lp333_order3_cp_sat.py
```

`LEGENDRE_MULTIPLIER.md` records the other order-three subgroups. The subgroup
generated by 112 is impossible by a direct lag-111 distance contradiction;
the `<121>` and `<211>` lanes remain open. `LP333_TWISTED_ORDER3.md` gives
their common exact outer theorem. Row-multiplier invariance reduces the
Gaussian row sum through the census

```text
36 -> 12 -> 6,048 -> 1,296.
```

The 1,296 fixed-margin words form 216 free row-dihedral orbits and 108
extended equivalence classes. An exact 21,953-state dynamic program proves
that all 1,296 still lift through both zero-column-lag LP equations.
Exponent reversal gives a bijection between the 121 and 211 spaces through
fixed margins, row sums, and the complete zero-column axis, but it is
nonadditive and does not preserve mixed lags. Thus only nonzero-column
equations can now distinguish or eliminate these lanes.

An additional fixed-row-profile fiber replaces the generic modulo-9 products
by 18 exact cardinalities.  Twenty-one sampled compressed-profile orbits are
catalogued (not exhaustively).  A fixed-memory `2 x 2` checkerboard engine
reached independently verified half-PAF energy 2320 on profile 6; it remains
nonexact with 135 bad lags and is a strict local minimum against all 5,992
single switches, all 8,972,767 one-A/one-B switch pairs, and all 8,547,413
disjoint same-sequence pairs.  Including the remaining 247,533 alternating
six-cycles, an independent collision-free verifier proves no lower-energy
state among all 17,661,680 unique states in the product switch-graph ball
through radius two.  The search engine used under 5 MB RSS.  The matching
exact CP-SAT mode is `--symmetry none --mod9-profile 6`; a 15-second
one-worker pilot ended
`UNKNOWN`, not infeasible.  A second 10-second repaired-hint pilot also ended
`UNKNOWN`; no candidate was emitted.
Centered-norm sharding and exact model-level orbit exclusion added nine more
profiles beyond the initial twelve.  Profile 19 reached independently verified
energy 2336 after 60 seconds; its 17,708,876-state radius-two ball and
9,526,800 alternating-eight-cycle neighborhood contain no lower-energy state.
Profile 6 was displaced by a 60-second profile-4 run at energy 2280, with 120
bad lags.  Its independent radius-two audit covers 17,801,598 unique states
and finds no lower energy.  This is the current catalog incumbent, not an
exact Legendre pair.

A complete exact scan paired every legal alternating six-cycle in either
sequence with every legal checkerboard switch in the other.  An independent
non-KD-tree verifier evaluated all 749,359,042 states and found unique minimum
energy 2408, above the profile-4 baseline 2280.  A second independent verifier
covered all 9,549,173 connected alternating eight-cycles and found minimum
2568.  These finite local results do not rule out the rest of the profile-4
fiber.

`LEGENDRE_SYMMETRY_OBSTRUCTION.md` rules out every pair in which each sequence
is symmetric or normalized skew under inversion.  Modulo-3 compression
reduces the three symmetry-type cases to the impossible norm equations
`x^2+y^2=668`, `x^2+y^2=222`, and `x^2+3y^2=667`.  This does not use the
conjectural factor-9 seed.  The main solver also has optional exact
`--mod111-compression energy|full` propagation; short matched trials left it
off by default.  An exact transfer DP independently proves the existing
fixed-column distance bounds have no hidden endpoint improvements or gaps.

## Live lane 3: circulant good matrices of order 167

`GOOD_167.md` describes an independent route to a skew `H(668)`.  Symmetry and
the good-matrix product theorem reduce the search to two signed row-sum
profiles.  Its exact CP-SAT model pairs correlation edges and caches repeated
unordered half-bit XORs, reducing the PAF auxiliaries to 13,612, then uses a
lexicographic necklace leader for the remaining 83-fold common-decimation
symmetry.  The default model has 20,669 variables, down from 55,777 in the
original encoding.  A two-stage `GF(2)` filter is also
implemented.  Its constant-memory C++ form reparameterizes by the symmetric
product quotient `S`, factors the 83-variable system once, and reuses it for
256 fixed-weight `B` samples.  This sustained about 48,000 samples/second at
1.44 MB peak RSS.  Two 60-second shards evaluated 2,890,277 and 2,871,527
samples; the best independently replayed PAF energies were 2,752 and 3,264,
still nonzero.  A connected structured annealer then preserved the product
theorem and all row sums while reducing both profiles to independently
verified energy 752.  An exact three-coordinate triangle descent then reduced
profile 1 to energy 728 with 58 bad lags; profile 0 stayed at 752.  Complete
pair-plus-triangle scans found no further improvement.  These are local
minima, not a global lower bound.  The states canonicalize into 332-primary-bit
repair hints for the unchanged exact CP-SAT model.  Cached-model bounded runs
ended `UNKNOWN`; the profile-1 run made 168,484 branches at 279.6 MB with zero
swap.  These runs prove no nonexistence result:

```sh
.solver-venv/bin/python search_good_167_cp_sat.py \
  --profile 0 --hint output/good_167_local_steepest_profile0.json \
  --hint-conflict-limit 1000 --workers 1 --max-memory-mb 256 \
  --time-limit 3600 --output output/good_167_hint_profile0_candidate.json
python3 verify_good_167.py --self-test

clang++ -std=c++20 -O3 search_good_167_stream.cpp \
  -o ../tmp/search_good_167_stream
../tmp/search_good_167_stream --parameterization sb --profile 0 \
  --seconds 60 --trials 0 --inner-batch 256 \
  --checkpoint output/good_167_stream_sb_profile0_60s.json
python3 verify_good_167_stream.py \
  output/good_167_stream_sb_profile0_60s.json
python3 verify_good_167_local.py \
  output/good_167_local_triangle_profile1.json
```

## Live lane 4: unrestricted cyclic SDS of order 167

`CYCLIC_SDS_167.md` removes the good-matrix symmetry restriction and searches
all ten cyclic supplementary-difference-set row-sum profiles.  The local
engine is single-threaded and bounded-memory; its strict verifier checks every
periodic correlation and the full order-668 Goethals-Seidel matrix.  Strict,
sanitized compilation and the exact single/compound-delta self-tests pass.  A
600-second incumbent continuation completed 1,628,953,659 moves using 1.4 MB
peak RSS and improved the best checkpoint from quarter-energy 76 to 64, still
with 46 bad lags.  Exhaustive cross-sequence pair polish and bounded triple
polish found no further descent.  The engine now also exhausts the full
`83^3` relative independent-decimation orbit modulo common decimation and
every fixed-row-sum state through raw Hamming distance four.  The latter audit
covers 335,097,301 states and proves
the energy-64 checkpoint is the unique energy and quartic minimum in that
neighborhood.  Guided exact scans also exclude 64,899,721 single-window
states, 61,383,193 unique paired-window states (61,471,872 evaluations), and
an aligned four-window union of 8,747,201,498,101 unique states.  Allowing an
independent family choice in each sequence expands the exact mixed-window
union to 15,055,272,576,605,041 unique states; none is exact.  The mixed
meet-in-the-middle pass uses 216.3 MB peak RSS and has an independent
small-domain/full-replay audit.
The checkpoint is nonexact and is deliberately rejected by the strict
verifier; no candidate is claimed.

## Verification

Run the dependency-free arithmetic checks and the solver-backed unit suite:

```sh
python3 verify_seed.py
python3 verify_fixed_q_obstruction.py
python3 verify_legendre_symmetry_obstruction.py
python3 variable_q_base.py
python3 variable_q_compression_7.py --self-test
python3 verify_variable_q.py --self-test
python3 verify_variable_q_seed_radius.py
python3 verify_variable_q_seed_quad_radius.py
python3 verify_variable_q_seed_frontier_artifacts.py
python3 verify_variable_q_seed_shell18_artifacts.py
python3 verify_five_comb_high_lag_boundary.py
python3 verify_five_comb_dyadic_compression.py
python3 verify_five_comb_paired_lobes.py
python3 verify_five_comb_root12_sieve.py
python3 verify_five_comb_root4_vertical.py
python3 verify_five_comb_unrestricted_full_corpus.py
python3 check_lp333_sextic_quotient.py
python3 verify_lp333_multiplier_row_sum.py
python3 verify_lp333_order3_difference_family.py
python3 verify_lp333_order3_mod3_sieve.py
python3 verify_lp333_order3_primitive9_jet.py
python3 verify_lp333_twisted_order3.py
python3 verify_good_167.py --self-test
python3 verify_sds_167.py --self-test
python3 verify_sds_167_neighborhood.py \
  --engine ../tmp/search_sds_167_local
python3 verify_sds_167_windows.py \
  --engine ../tmp/search_sds_167_local
.solver-venv/bin/python -m unittest -v \
  test_construction.py test_legendre_333.py \
  test_legendre_333_eight_cycle.py \
  test_legendre_333_profile_local.py \
  test_lp333_sextic_quotient.py test_lp333_sextic_cp_sat.py \
  test_lp333_multiplier_row_sum.py \
  test_lp333_order3_difference_family.py \
  test_lp333_order3_mod3_sieve.py \
  test_lp333_order3_primitive9_jet.py test_lp333_twisted_order3.py \
  test_lp333_order3_lift_catalog.py test_lp333_order3_cp_sat.py \
  test_search_legendre_333_profile_catalog.py test_legendre_multiplier.py \
  test_legendre_column_distance_dp.py test_variable_q_base.py \
  test_variable_q_cp_sat.py test_variable_q_compression.py \
  test_variable_q_compression_7.py \
  test_variable_q_joint_compression.py test_variable_q_parity_neighborhood.py \
  test_variable_q_seed_distance.py test_variable_q_seed_quad_radius.py \
  test_variable_q_seed_frontier.py test_variable_q_seed_ball.py \
  test_good_167.py test_sds_167.py
.solver-venv/bin/python verify_legendre_333.py --self-test
```

Any future candidate from any live lane must be expanded to the full matrix
and checked exactly before it is treated as verified.

## Resource safety

This repository is currently run on a 16 GiB host. Solver jobs may use several
gigabytes when the reduction warrants it, but their measured aggregate
whole-process RSS must remain below 16 GB. The OR-Tools limit applies to the
solver, not all Python/model-construction memory, so it is a guardrail rather
than an operating-system hard limit. During the full common-type sweep, the
live session monitor observed four disjoint single-worker processes at
roughly 1.4 GB aggregate RSS; this measurement is not encoded in the corpus
records. Use disjoint resume-safe shards before introducing similar
concurrency. The exact parity-neighborhood enumerator is intentionally capped
at three exchanges;
larger meet-in-the-middle tables are not safe on this machine.
The seed-frontier models use a tighter 256 MiB solver cap and have remained
at or below 176 MB total RSS.  The cyclic-SDS annealer remained below 2 MB;
its radius-four scans used 11.5 MB and its exact four-window MITM used 24.7
MB.  The larger mixed-family MITM is explicitly capped at eight left-family
pairs per batch and used 216.3 MB peak RSS.
The reduced good-matrix CP-SAT runs also use one worker and a 256 MiB solver
cap; their measured whole-process peaks were 272.7 and 285.3 MB with zero
swap.  The fixed-array good-matrix streamer used 1.44 MB peak RSS in
production; the structured local runs used at most 1.49 MB and their
ASan/UBSan trial used 17.9 MB.  Neither program retains a
visited set or any structure that grows with elapsed time.
The exact-profile Legendre C++ search used at most 2.7 MB and its exhaustive
extended polish used 4.46 MB.  The independent collision-free radius-two
verifier used at most 73.0 MB across the retained audits.  The direct mixed
and eight-cycle verifiers used 4.03 MB and 1.89 MB respectively.  Its
fixed-profile
CP-SAT model built at 254 MB and reached 703 MB whole-process RSS in a
15-second solve under a 320 MiB solver-internal limit, with zero swap; this
measured gap is why no such solves are overlapped.  A repaired-hint pilot
reached 931 MB whole-process RSS even with a 128 MiB internal limit, so this
full model is not being lengthened on the current host.
The separate 18-variable profile sampler used at most 117 MB whole-process RSS
in recorded runs with one worker, a 128 MiB solver cap, and zero swap.
The exact order-three row-sum enumerator used 2.82 MB maximum RSS. The
all-1,756 pure-axis histogram replay used 114.1 MB in the independent run,
the Eisenstein verifier and tests stayed below 29 MB, and the corrected full
quotient pilot used 390.4 MB; all completed with zero swap. The paired-lobe
roots `+1,-1` retained replay peaked near 712 MB and
the vertical `Phi_4` replay at 499.6 MB. These measurements leave substantial
headroom, but future jobs must still account for the several gigabytes used
by the desktop and other applications rather than treating 16 GB as wholly
available to one solver.
The primitive-nine verifier stayed below 22 MB, while the coupled-order-three
verifier and tests stayed below 94 MB, again with zero swap.

Primary seed source: Shalom Eliahou, [A 64-modular Hadamard matrix of order
668](https://ajc.maths.uq.edu.au/pdf/93/ajc_v93_p422.pdf), *Australasian Journal
of Combinatorics* 93(2) (2025), 422-427.
