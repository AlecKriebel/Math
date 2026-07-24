# Hadamard order 668 search

Status: active computational research; no exact matrix has been found yet.

This directory is a reproducible attack on the smallest unresolved Hadamard
order.  A result counts only when an explicit `668 x 668` sign matrix passes an
exact, dependency-free check of `H H^T = 668 I`.  Near solutions and solver
status are diagnostics, never discoveries.

`RESUME.md` is the compact handoff for restarting this project after a pause.
`PRIORITY_AUDIT.md` records the provisional novelty and publication audit for
this milestone.  `H668_72H_GATE.md` records the active sprint's success and
stop criteria; in particular, one second-digit witness is not a milestone.

## Current map

| Lane | Status | Scope / finish line |
|---|---|---|
| Eliahou seed verification | reproduced near matrix | published 64-modular matrix of order 668, not an exact Hadamard matrix |
| Repair with Eliahou's exact `q` | impossible | reduces to empty `TU(41)` |
| Repair with Eliahou's exact `s` | impossible | already contradicted by the `z=1` sum-of-two-squares norm |
| Variable `s,q` special quadruple | active | adjacent-42 forces base distance 80 and special distance 41; the anti-fold reduces the boundary to 30 support instances, with exactly case 0 certified UNSAT, case 1 unproved, and 28 UNKNOWN |
| Prime-83 oriented SDS | implemented construction lane | best verified checkpoint has quarter-energy 14 and 11 bad lags; no prime fold yet |
| Prime-83 character families | closed restricted lane | degree-two Sidelnikov products, phases, signs, and independent decimations excluded exactly |
| Common-type five-comb packing | closed restricted lane | all 48 quartets and 32 projective cores solver-excluded; no proof certificates |
| Distinct-lobe five-comb packing | active construction lane | 1,246 complementary octets; primitive-eight vertical sieves retain 140,007 inventories at core 4 and 65,868 at core 27 |
| Sextic-multiplier `LP(333)` | archival/subsumed restricted lane | our compact fixed-compression census has zero hits, but the stronger July 2026 full-family exclusion covers this paper ID8 subgroup |
| Quartic-multiplier `LP(333)` | archival/subsumed restricted lane | our compact fixed-compression census has zero hits, but the stronger July 2026 analytic full-family exclusion covers this paper ID12 subgroup |
| Order-three multiplier `LP(333)` | active 72-hour gated lane | `<112>` is closed only under the prescribed fixed compression; `<10>` has five exact `n_9=2` profile orbits, a 36-dimensional first-digit space, and an audited quadratic second digit whose six-coordinate residue layer is surjective; the finish gate now requires consecutive higher-digit contraction or exact structured-family replay, not a second-digit witness; `<121>,<211>` share a 1,296-word/108-orbit outer boundary |
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

`ELIAHOU_ADJACENT42_REPAIR.md` supplies a third exact cyclic image. Folding
all four base rows modulo `z^42-1` turns the published seed into a perfectly
flat periodic quadruple of energy 14, while every exact `BS(84,83)` must have
energy 334. Equivalently, the target needs exactly 83 equal separation-42
pairs and the seed has only three. Therefore every exact repair changes at
least 80 base-row signs. In special `(s,q)` coordinates the distance is at
least 41: equality 40 would keep `q` fixed and is already excluded by the
`TU(41)` theorem. A complete distance-41 split leaves only two reciprocal
`q` flips plus 39 `s` flips; roots `+1,-1` reduce its 80 shell-compatible
reciprocal pairs to 39, each with two joined root profiles:

```sh
python3 verify_eliahou_adjacent42_repair.py
```

`ELIAHOU_ANTIFOLD42.md` supplies the complementary reduction modulo
`z^42+1`. On the distance-41 shell, either endpoint choice in a
separation-42 pair has the same anti-fold effect, so all `2^39` endpoint
orientations disappear from the first stage. The 39 reciprocal `q` pairs
collapse to 30 orientation-free, 39-cell binary support instances. Exactly
one is now closed: canonical case 0, the long `q` representative 0, has a
standalone CaDiCaL binary-DRAT certificate that passes independent
`drat-trim` replay. Canonical case 1, the long representative 2, has one
solver-UNSAT observation but no checked proof; the other 28 instances are
`UNKNOWN`.

`ELIAHOU_ANTIFOLD_MOD2.md` gives the exact first binary lift. Pairing the two
long and two short rows produces an affine system over `F_2`; including
support-weight parity, its rank is exactly 21 in all 39 reciprocal-`q`
cases. Exact MacWilliams counts show that this layer leaves many supports,
so it is a reduction rather than another exclusion.

```sh
python3 verify_eliahou_antifold42.py
python3 verify_eliahou_antifold_mod2.py
python3 verify_eliahou_antifold_q0_proof.py
```

The proof package is in `output/antifold42_q0_proof/`. The default verifier
checks metadata, hashes, and the complete DIMACS shape. A full replay, when
`drat-trim` and `zstd` are available, is:

```sh
python3 verify_eliahou_antifold_q0_proof.py \
  --full --drat-trim /absolute/path/to/drat-trim
```

The machine-readable `ELIAHOU_ANTIFOLD42_CENSUS.json` is the authoritative
resume ledger. Rebuild deterministic formulas or resume only the unresolved
range with:

```sh
../tmp/hadamard-env/bin/python search_eliahou_antifold_sat.py \
  --ignore-profiles --start 0 --stop 30 --list-instances
../tmp/hadamard-env/bin/python search_eliahou_antifold_sat.py \
  --ignore-profiles --start 2 --stop 30 --time-limit 1800
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

`FIVE_COMB_ROOT8_VERTICAL.md` extends the narrower vertical-pair placement
through a primitive eighth root. Writing the four completed evaluations as
`E+zeta_8 O` splits the norm into an integer energy equation and an exact
`sqrt(2)`-coefficient cancellation. The retained core-4 census reduces
724,564 prior survivors to 140,007; core 27 reduces 229,408 to 65,868.
These are exact exclusions only for the vertical-pair slice and retain the
even/odd high-lag projection. The larger run used 3.87 GB maximum RSS with
zero swap:

```sh
python3 verify_five_comb_root8_vertical.py --cores 4
python3 verify_five_comb_root8_vertical.py --cores 27
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

`LP333_ORDER3_CHAR37_TRANSFER.md` gives an independent exact mixed-lag
coordinate system. In characteristic 37, `x^37-1=(x-1)^37`; the logarithmic
coordinate `x=exp(u)` and order-three invariance leave only powers of
`v=u^3`. This identifies the complete 13-dimensional invariant group ring
with `F_37[omega][v]/(v^13)`, and the six complex mixed equations become one
truncated norm identity. The transfer matrix has rank 13 and determinant 11,
so it loses no invariant information modulo 37. Direct replay matches 4,476
physical/cyclotomic equations. Explicit witnesses show all 22 aggregate
shards survive coefficients one and two together with the older local sieve,
while every pinned witness fails later coefficients:

```sh
python3 verify_lp333_order3_char37_transfer.py
```

`LP333_ORDER3_LABELED_JET.md` makes the primitive-nine layer fully labelled.
It proves the exact invariant-algebra split

```text
F_3[C_37]^H  ~=  F_3 x F_729 x F_729
```

and identifies column negation with the third Frobenius iterate in both
field factors. The lower three jet digits depend only on residue profiles;
the upper three form a linear placement lift because `pi^3 R` is
square-zero. One row-695 lift is replayed through all 222 mod-three jet
equations and four exact row-direction equations. It proves survival, not an
`LP(333)` and not a catalog exclusion.

`LP333_ORDER3_TRIT_LIFT.md` compresses the upper placement layer further.
For the pinned row-695 profiles, 54 placement trits satisfy a rank-18 affine
system over `F_3`, leaving nullity 36 before exact margin and correlation
conditions. A second fully labelled modular certificate is independently
replayed. These rank values apply only to the pinned profile tuple.

`LP333_ORDER3_INTEGRAL9.md` records the stronger exact ninth-root condition.
For each invariant column lag, vanishing at a primitive ninth root is
equivalent over the integers to

```text
c_(b,s) = c_(b,s+3) = c_(b,s+6),    s=0,1,2.
```

This gives 72 genuinely new displayed integer equations outside the zero
column. Both pinned mod-three certificates fail all 36 nonzero
column-class/residue groups. This proves strictness of the integral layer on
those witnesses, but does not exclude row 695 or any other catalog row.

`LP333_ORDER3_PROFILE9_IDEAL.md` extracts the part of that exact condition
visible before within-residue placement. For each reversal-paired nonzero
column class, the profile Fourier coefficient must lie in

```text
3(1-omega) Z[omega].
```

The six displayed tests have one global dependency, leaving five independent
finite-ideal conditions. Passing the ideal uniquely reconstructs the full
`12 x 3` table of exact periodic correlation targets. All 22 profile
assignments retained by the earlier characteristic-37 checkpoint fail this
test. `LP333_ORDER3_PROFILE9_SHARDS.md` then gives the necessary negative
control: one different exact profile assignment exists for every one of the
22 aggregate shards. Thus the ideal is a strict assignment-level filter but
does not exclude an aggregate shard.

`LP333_ORDER3_PROFILE_ZERO_GATE.md` records the stronger condition that was
missing from the continuation plan.  A full Legendre pair has adjusted
plus-support intersection 167 at every row lag, so its order-three profile
moment satisfies

```text
D_t=0
```

on all thirteen column parts.  All 22 stored ideal-compatible tuples fail:
one on ten nonzero classes and 21 on all twelve.  The original row-695
profile and stored same-shard witness both fail all twelve.  These are 22
fixed-profile exclusions and zero
aggregate-shard exclusions; only a different zero-moment profile tuple may
proceed to placement.

`LP333_ORDER3_PROFILE_CRT.md` turns that exact zero gate into a finite
local-global test.  On the energy-167 shell, every profile correlation lies
in the Cauchy disk of norm at most `167^2=27,889`.  Simultaneous membership
in the primitive-nine ideal and vanishing modulo 37 puts it in

```text
37(1-omega)^3 Z[omega],
```

whose least nonzero norm is `36,963`.  The norm gap therefore makes the
`lambda^3` and complete characteristic-37 layers equivalent to exact
`D_t=0`.  `LP333_ORDER3_PRIME167_SPLIT.md` gives an independent one-prime
version with a broader ambient theorem: on total energy 167, divisibility of
every nonzero-lag correlation by 167 already forces exact zero.  In the
order-three invariant algebra this
becomes

```text
F_167(omega)[C_37]^H = k x E x E,
k=F_(167^2),  E=F_(167^12),
```

with an explicit involution, inverse CRT, and complete finite-field
parameterization.  All 22 stored profile tuples fail both exact forms.

`LP333_ORDER3_SPECTRAL_UNITS.md` removes the boundary of that finite-field
cone on the physical profile alphabet.  Irreducibility of `Phi_37` over the
Eisenstein field makes every primitive complex Fourier value nonzero; its
twelve-factor absolute norm is strictly below `167^12`, while either
primitive residue prime has norm exactly `167^12`.  Hence both channels are
units in all three CRT factors.  The ratio `U=A B^(-1)` is well-defined and
satisfies `U U*= -1`, leaving one fixed-target primitive torus of exactly
`(167^12-1)^3` points.  This rules out the old degenerate and axis branches
but does not yet produce a small-alphabet point.

`LP333_ORDER3_PROFILE_SPARSE_SHELLS.md` excludes the two sparsest exact
profile sectors

```text
(n_9,n_3,n_0)=(5,3,16), (6,0,18).
```

The opposite-quartet condition confines the three norm-three letters in the
first sector to one quartet.  Since every norm-nine coefficient is divisible
by 3, all high-high cross terms vanish modulo 9.  This reduces the two
sectors to 552 and 288 assignments for detached exact replay, respectively;
none has all 36 nonzero physical correlations zero.  Independent enumeration,
sanitizer runs, all-37-lag replay, and external certificate hashes confirm the
exclusion.  Thus any exact profile survivor has at most four norm-nine
letters.  Five type sectors remain.

`LP333_ORDER3_PRIME163_EXTREME.md` gives an exact complementary obstruction
at the opposite rational prime 163.  In the two norm-pair `(163,4)` targets,
the extreme channel-energy allocation makes `B=2 delta_0` and would require
`A A^*=163 delta_0`.  The two degree-12 primes above 163 in
`Q(omega,zeta_37)^H` are explicitly principal, generated by
`14+3 omega` and `11-3 omega`; CM-unit rigidity then makes every nontrivial
Fourier value of `A` constant, contradicting Fourier inversion at
`A(0)=-1`.  This removes exactly 1,617,192 locally legal profile assignments
from each target, 3,234,384 total.  Nonextreme local witnesses remain, so
neither aggregate shard is excluded.

`LP333_ORDER3_SPARSE_B_NORM.md` treats the next sparse allocation in those
same two targets.  Normalized `B`-energy six and aggregate zero force

```text
B=2+z(eta_i-eta_j),       Norm(z)=3,
```

giving 396 structural words and 34 lift-safe orbits.  In the quadratic
CM extension
`Q(omega,zeta_37)^H / (Q(omega,zeta_37)^H)^star`, exact complementarity
requires `167-BB*` to be a relative norm.  Odd valuations at inert primes
above 11 and 101 exclude 13 of 17 field types: 312 words and 26 lift-safe
orbits.  PARI's guaranteed cyclic norm test confirms that four types really
are field norms, leaving 84 words and eight lift-safe orbits.  This is a
substantial exact reduction, not a closure of the energy-six sector; the
remaining norm witnesses need not have a physical `A`-profile.

`LP333_ORDER3_PROFILE_ZERO_SYMMETRY.md` certifies the formal profile group
`C6 x C2_A x C2_B`, reducing the 22 aggregate targets to seven equation
orbits.  Only `C6 x C2_B` transports the canonical labelled zero words, so a
lift-complete campaign has twelve target orbits; `A`-star images must be
lifted independently.  The verifier now checks correlation covariance
term-by-term over the complete finite profile alphabet rather than relying
on sampled assignments.

`LP333_ORDER3_PROFILE_CRT_CONSTRUCTOR.md` implements the seven formal target
orbits as a finite 24-variable discovery search.  It enforces the six
reversal-independent equations `D_j=0` directly, uses the sharp
`[-192,192]` correlation box, and replaces each opposite-pair quartet by an
exact 3,334-row/1,409-state coarse layer.  It applies the independently
verified shell theorems as the hard cut `n_9<=2`.  The model also uses the full
fixed-target stabilizer, semantic checkpoint fingerprints, persistent exact
no-goods, complete formal/lift-compatible orbit emission, and three detached
integer replays of every survivor.  Persisted survivors are replayed again
before becoming resumed no-goods, and the fingerprint covers the full
operational replay dependency closure.  CP-SAT exhaustion is not treated as
a proof certificate, and no long campaign has been run on the hardened model.

A separate prime-167 MITM audit found that the obvious balanced split would
need more than 151 GiB, while the low-memory channel-first version still
requires 6,338,555,429 degree-12 field signatures.  The hardened
checkpointed constructor is therefore the current exact profile route;
neither the obsolete first-generation workflow pilot nor the MITM count is
evidence of infeasibility.

Four exact energy-shell theorems now prune that constructor before any
solver search.  `LP333_ORDER3_PROFILE_ENDPOINT_SHELL.md` excludes
`(n_9,n_3,n_0)=(6,0,18)`, and
`LP333_ORDER3_PROFILE_PENULTIMATE_SHELL.md` excludes `(5,3,16)` after an
affine modulo-nine join reduces 34,634,136 aggregate/local assignments to
552 exact replays.  `LP333_ORDER3_PROFILE_SHELL_FOUR.md` then classifies the
six medium letters into the only possible quartet patterns `2+2+2`, `3+3`,
and `4+2`.  Its streaming verifier checks 27,468,720 oriented frames,
replays 345,984 exact-aggregate modulo-nine survivors on all 37 lags, and
finds none with `D_t=0`.  `shell_four_compressed/` independently quotients
the medium skeletons and reproduces the same survivor counts and exact
failure histogram; it is corroboration and explicitly shares the production
alphabet and transition source.

The three-high shell `(3,9,12)` is excluded independently in
`shell_three_mod27/`.  Its signed-uniformizer quotient has 38,296 canonical
skeletons.  A lossless affine modulo-nine join leaves 479,850
exact-aggregate assignments; only two survive modulo 27, and detached exact
replay rejects all 479,850.  The companion cubic characteristic-37 moment
also rejects both modulo-27 near witnesses.  Hence every exact profile
satisfies

```text
n_9 <= 2.
```

These are complete shell exclusions, not a whole-quotient obstruction.

The next shell behaves differently: it contains genuine exact profile
solutions.  `shell_two_exact/` gives a complete, symmetry-reduced
classification of

```text
(n_9,n_3,n_0)=(2,12,10).
```

There are exactly five profile-zero orbits under the order-24 formal profile
group, with orbit sizes `24,12,12,12,24`.  One lies in the medium-support
partition `222222` and four lie in `422220`; the other five possible
partitions are empty.  The exact enumerator checks 14,715,744 raw signed
skeletons, 617,788 canonical skeletons, 10,201,038 exact replays, and five
survivors.  Every representative independently passes all 37 physical
profile correlations, the characteristic-37 and prime-167 gates, exact
aggregate reconstruction, and orbit replay.  This is the first point in the
descent where exact profile solutions exist.  It is not yet an `LP(333)`:
each representative still has 54 placement trits.

For all five representatives, the first placement Hensel digit has rank 18
and nullity 36.  Their exact row-margin joins retain `72,72,72,96,93`
catalog rows, respectively.  The active problem is therefore the remaining
integral phase lift of these five finite inputs, in parallel with the
unclassified `n_9=1,0` shells.

```sh
python3 shell_two_exact/verify_shell_two_partition_theory.py
python3 shell_two_exact/verify_shell_two_exact_orbits.py
python3 -m unittest -v shell_two_exact/test_shell_two_partition.py
```

`scratch_exact_profile_lift/` preserves a secondary, resumable exact CP-SAT
lift of the first representative.  Its 72 row-margin shards are all
`UNKNOWN` after the short attempt-zero diagnostic; this is explicitly not
an exclusion.  The bounded model is retained so future algebraic cuts can be
measured against the same exact save-and-replay gate.

`phase_second_digit/` gives the complete next placement digit on all five
representatives.  The first digit leaves `F_3^36`; the next exact digit is a
system of eighteen independent quadratic forms, with two additional
structural-zero rows and no affine contradiction.  Six three-row
combinations form the residue layer of the ramified row-coordinate algebra

```text
(F_27 x F_27) tensor F_3[epsilon]/(epsilon^3).
```

An exact 729-character transform proves that their joint map
`F_3^36 -> F_3^6` is surjective for every profile, with every fiber close to
`3^30`.  Thus a second-digit witness is expected to be abundant and is not a
construction milestone.  A separate exact centroid audit proves that the
36-dimensional placement space is not a free rank-two module over the
ramified algebra: its common self-adjoint centroid has dimension one, not
eighteen.  The remaining twelve coordinates therefore require genuinely
conditional quadratic or exact finite-field methods rather than automatic
linear Hensel lifting.

`structured_phase_families/` then tests nine named algebraic placement
families on all five profiles.  The four low-period controls are entirely
contained in the already excluded order-six common-multiplier family.  Three
opposite-class-twisted families deliberately break every excluded proper
supergroup, while the final family reconstructs all 56 minimal
three-dimensional invariant submodules of the `F_27 x F_27` class algebra
and tests all `56^2` asymmetric channel pairs per profile.  Every
supergroup-free structured point fails the quadratic second digit.  The
single structured second-digit point is order-six fixed and fails digit
three, so it is a positive control rather than a viable lift.

`LP333_ORDER3_DENSE_SHELL_QUADRATIC_ALGEBRA.md` analyzes the first genuinely
quadratic uniformizer response in the remaining `n_9=1,0` shells without
enumerating phases.  Its six polar matrices commute and generate

```text
F_27 x F_27,
```

with projective rank census `rank 12: 338, rank 6: 26` and the exact radial
identity `M_0+...+M_5=2I_12`.  After the actual local and aggregate affine
rows are imposed, exact Gauss bounds prove that this universal combination
attains every right-hand side on every nonempty fiber—at least 2,025 times
for `n_9=1` and 54,675 times for `n_9=0`.  Thus no single-form anisotropy can
exclude either dense shell.  The positive consequence is a lossless next
architecture: count the full six-coordinate layer using 729 exact quadratic
Gauss sums per signed skeleton, then recover a witness by self-reduction.

`LP333_ORDER3_PHASE_FACTOR.md` turns the remaining labelled lift into
intrinsic unit phases. Splitting row `r=s+3q`, every fixed-size-one or
fixed-size-two residue fiber has a signed cube-root phase in
`Z[omega]`. The identity

```text
active(profile)=3-Norm(profile Fourier value)/3
```

shows that total profile norm 54 forces exactly 54 phase variables for every
viable profile tuple, not only row 695. After the threefold physical-column
expansion and the fixed zero column, frame energy 167 is automatic. The
complete primitive-ninth-root equation is equivalent to two group-ring
identities:

```text
K_00+K_11+K_22 = 167 e,
K_10+K_21+omega^2 K_02 = 0.
```

The first is a periodic complementary frame of six sparse Eisenstein
sequences; the formally third cubic-basis equation is the adjoint of the
second. This explains the 36 independent mixed-column integer conditions.
It is now the preferred architecture for lifting the five exact shell-two
profiles.

`LP333_ORDER3_PHASE_PRIME167.md` makes this phase architecture finite without
loss.  On the universal zero/unit support-167 shell, Cauchy equality would
force support to be a union of translation or twisted-translation orbits.
Their relevant lengths are 37, 3, and 111, none of which can sum to 167.
Consequently both phase equations are exactly equivalent to their full
reductions modulo 167.  In the existing `k x E x E` split, the three
primitive equations become the annihilator of a three-dimensional twisted
orbit plane.

Recombining the three fibers at a primitive ninth root gives the still
smaller complete algebra

```text
F_(167^6) x F_(167^12)^6.
```

Star pairs the six primitive factors into three pairs, so all 39 prime-field
component conditions are one Hermitian norm cone over
`F_(167^6)/F_(167^3)` and three bilinear cones over `F_(167^12)`.
The direct bridge
`sum_X W_X W_X^*=E0+alpha E1+alpha^2 omega^2 E1^*`, every branch,
three nondegenerate axis/generic recovery fixtures, and the rank-13 invariant
CRT are checked exactly.  The remaining problem is the sparse zero/unit
inverse-CRT intersection; no physical phase point is asserted.

`LP333_ORDER3_PHASE_FIBER_SUPPORT.md` sharply restricts that intersection
before any enumeration.  A nonzero zero/unit fiber cannot vanish at a
primitive complex character; its twelve-factor relative norm is strictly
below `167^12`, whereas vanishing in either prime-167 coordinate forces
divisibility by `167^12`.  Hence, for each of the six fibers,

```text
U_i=0  if and only if  x_i=0  if and only if  y_i=0.
```

Five fibers are forced nonzero by the fixed zero column, leaving only two
joint support strata: all six coordinates nonzero, or `B0` zero in both
primitive vectors.  This removes 4,094 of the 4,096 ambient joint
zero/nonzero patterns.  The `B0`-zero stratum also has primitive-plane rank
at least two; the dense rank-one stratum remains possible, so no rank-three
or existence claim is made.

`LP333_PHASE_CONE_TRIVIAL_BRANCH_OBSTRUCTION.md` removes the trivial zero
branch from that intersection.  If one channel's recombined trivial
coordinate vanished, its nine row margins would repeat with period three,
making their total divisible by three; the exact total is 167.  The complete
row-sum catalog sharpens the surviving branch from `167^3+1=4,657,464`
abstract projective ratios to 1,411 exact nonzero coordinate pairs.

`LP333_ORDER3_PHASE_TRACE_SIEVE.md` inverts the four cone blocks by a
three-by-three row-Galois transform and reconstructs every physical class
coefficient by factorwise traces.  It exposes twelve independent fixed-zero
linear equations and five further displayed profile-support equations after
the cone total is used.  A proposed ninth-root coefficient is physical if
and only if the nine inverse-DFT values satisfy `b^2=b`; exhaustive replay
proves this decoder for all weight-three and complementary weight-six
words.  The same analysis gives a seven-value local norm alphabet with
explicit cubic branches.

Independently, `LP333_ORDER3_PHASE_CYCLIC_DECODER.md` factors the phase
equation modulo seven into thirteen scalar equations over `F_(7^3)`.  It
gives exact local alphabets of sizes 1, 9, and 27 and a compact
11,466-row multiplication layer.  Its accompanying architecture audit rules
out the raw trellis, plain balanced MITM, additive Wagner, and
alphabet-independent one-factor BCH shortcuts; it is a necessary propagator,
not yet a practical standalone decoder.

`LP333_ORDER3_PHASE_TRANSFER.md` collapses the trivial-column character of
that phase frame to one integer energy and one Eisenstein cross term per
channel.  It proves object-by-object, including multiplicities, that this is
exactly a phase-coordinate form of the existing 1,756-word row-sum catalog,
not a new obstruction.  On the diagnostic stored tuples it reduces
`3^54` phase assignments to 22--87 transfer signatures and 45--98 compatible
catalog rows.  The architecture is retained for a future `D_t=0` profile.

`LP333_ORDER3_PHASE_HENSEL.md` gives the first placement-dependent
`(1-omega)`-adic digit as 20 affine equations over `F_3`.  On the stored
corpus, 21 tuples have rank 18 and nullity 36, while fixed-profile witness 3
has coefficient/augmented ranks `(16,17)` and an explicit contradiction.
This census is subsumed because all 22 inputs already fail `D_t=0`; only the
generic affine formulation is a forward search tool.

`LP333_ORDER3_DIAGONAL_FRAME_PREFIX.md` independently compresses the
augmentation and first characteristic-37 coefficient of the diagonal frame.
The largest one-sequence and joined tables have 444 and 666 states, and all
22 diagnostic tuples have positive exact counts.  No second coefficient or
complete diagonal-frame survivor is claimed.

Reproduce the new exact layer with:

```sh
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
python3 verify_lp333_order3_spectral_units.py
python3 verify_lp333_order3_prime163_extreme.py
python3 verify_lp333_order3_sparse_b_norm.py
gp -q verify_lp333_order3_sparse_b_norm.gp
python3 verify_lp333_order3_profile_zero_symmetry.py
python3 verify_lp333_order3_profile_endpoint_shell.py
python3 verify_lp333_order3_profile_penultimate_shell.py
c++ -std=c++20 -O3 verify_lp333_order3_profile_shell_four.cpp \
  -o /tmp/verify_lp333_order3_profile_shell_four
/tmp/verify_lp333_order3_profile_shell_four
clang++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  shell_three_mod27/verify_lp333_order3_profile_shell_three_mod27.cpp \
  -o /tmp/verify_lp333_order3_profile_shell_three_mod27
/tmp/verify_lp333_order3_profile_shell_three_mod27
python3 shell_three_character/verify_lp333_order3_shell3_cubic_character.py
python3 verify_lp333_order3_phase_factor.py
python3 verify_lp333_order3_phase_prime167.py
python3 verify_lp333_order3_phase_fiber_support.py
python3 verify_lp333_phase_cone_trivial_branch.py
python3 verify_lp333_order3_phase_trace_sieve.py
python3 verify_lp333_order3_phase_cyclic_decoder.py
python3 verify_lp333_order3_phase_transfer.py
python3 verify_lp333_order3_phase_hensel.py
python3 verify_lp333_order3_diagonal_frame_prefix.py
../.venv/bin/python search_lp333_order3_profile_crt.py \
  --self-test --max-memory-mb 512
../.venv/bin/python -m unittest -v \
  test_search_lp333_order3_profile_crt.py
../tmp/hadamard-env/bin/python verify_lp333_order3_lift_catalog.py \
  --workers 4 --time-limit 2
../tmp/hadamard-env/bin/python -m unittest -v \
  test_lp333_multiplier_row_sum.py \
  test_lp333_order3_difference_family.py \
  test_lp333_order3_mod3_sieve.py \
  test_lp333_order3_primitive9_jet.py \
  test_lp333_order3_char37_transfer.py \
  test_lp333_order3_labeled_jet.py \
  test_lp333_order3_trit_lift.py \
  test_lp333_order3_integral9.py \
  test_lp333_order3_profile9.py \
  test_lp333_order3_profile9_shards.py \
  test_lp333_order3_profile_zero_gate.py \
  test_lp333_order3_profile_crt.py \
  test_lp333_order3_prime167_split.py \
  test_lp333_order3_spectral_units.py \
  test_lp333_order3_prime163_extreme.py \
  test_lp333_order3_sparse_b_norm.py \
  test_lp333_order3_profile_zero_symmetry.py \
  test_lp333_order3_profile_endpoint_shell.py \
  test_lp333_order3_profile_penultimate_shell.py \
  test_lp333_order3_profile_shell_four.py \
  shell_three_mod27/test_lp333_order3_profile_shell_three_mod27.py \
  shell_three_character/test_lp333_order3_shell3_cubic_character.py \
  test_lp333_order3_phase_factor.py \
  test_lp333_order3_phase_prime167.py \
  test_lp333_order3_phase_fiber_support.py \
  test_lp333_phase_cone_trivial_branch.py \
  test_lp333_order3_phase_trace_sieve.py \
  test_lp333_order3_phase_cyclic_decoder.py \
  test_lp333_order3_phase_transfer.py \
  test_lp333_order3_phase_hensel.py \
  test_lp333_order3_diagonal_frame_prefix.py \
  test_lp333_order3_lift_catalog.py \
  test_lp333_order3_cp_sat.py
```

`LEGENDRE_MULTIPLIER.md` records the other order-three subgroups. The subgroup
generated by 112 is impossible under the prescribed fixed compression by a
direct lag-111 distance contradiction; the unrestricted paper ID2 family
remains open.  The `<121>` and `<211>` lanes also remain open.
`LP333_TWISTED_ORDER3.md` gives their common exact outer theorem.
Row-multiplier invariance reduces the
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
python3 verify_eliahou_adjacent42_repair.py
python3 verify_eliahou_antifold42.py
python3 verify_eliahou_antifold_mod2.py
python3 verify_eliahou_antifold_q0_proof.py
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
python3 verify_lp333_order3_char37_transfer.py
python3 verify_lp333_order3_labeled_jet.py
python3 verify_lp333_order3_trit_lift.py
python3 verify_lp333_order3_integral9.py
python3 verify_lp333_order3_profile9.py
python3 verify_lp333_order3_profile9_shards.py
python3 verify_lp333_order3_phase_factor.py
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
  test_lp333_order3_primitive9_jet.py \
  test_lp333_order3_char37_transfer.py \
  test_lp333_order3_labeled_jet.py \
  test_lp333_order3_trit_lift.py \
  test_lp333_order3_integral9.py \
  test_lp333_order3_profile9.py \
  test_lp333_order3_profile9_shards.py \
  test_lp333_order3_phase_factor.py \
  test_lp333_twisted_order3.py \
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
