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
- a dependency-free 16-coordinate dynamic program proves that every exact
  `BS(84,83)` is at raw labelled Hamming distance at least 34 from Eliahou's
  base quadruple; the primitive-eight sphere first becomes reachable at
  distance 33, but all 66 full root-eight targets there fail the exact margin
  norms. A distance-34 witness passes roots, margins, and endpoint quads, so
  this combined relaxation is sharp;
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
- inversion-symmetric/normalized-skew `LP(333)` type pairs are impossible;
- several large, explicitly defined local neighborhoods around retained near
  misses have been independently exhausted.

The strongest new constructive reductions are:

- `NOVEL_BS84_THEORY.md`: exact equivalence of `BS(84,83)` with simultaneous
  cyclic folds at 84 and 83. The prime fold is a 41-equation oriented SDS with
  45 size profiles and a `GF(2^82)/GF(2^41)` norm parameterization. Construct
  the prime fold first, then test 564,898 finite phase/multiplier lifts.
- `NOVEL_LP333_THEORY.md`: an exact 45-phase quartic-residue QPSK quotient.
  A frozen axis-complete table leaves only 16 mixed equations.
- `LP333_SEXTIC_QUOTIENT.md`: an order-six multiplier quotient with 108 free
  binary signs after fixing its `LP(9)` core. The row-axis fiber reduces to
  298 exact meet-in-the-middle signature shards and 34 reversal-inequivalent
  quotient lag equations. The implemented default channel has 2,979
  variables and 2,923 constraints after an exact residual `C3` lex leader.
  It reduces 1,658,700 compatible signature sextuples to 552,912
  signature-level orbits.
- `NOVEL_LIFTING_64.md`: an 84-bit reciprocal `q` skeleton and finite 2-adic
  lift. The seed's first obstruction is a five-lag Frobenius square, while an
  augmented-rank certificate rules out a first-order tangent repair.
- `FIVE_COMB_SECANT.md`: the complete seed defect is one rank-one ten-sparse
  carrier. Common-factor repairs are impossible, but a minimum complementary
  octet gives 32 flat carrier channels of energy 320 that pack into the target
  lengths with exactly 14 singleton holes. Cancelling the packing cross terms
  would directly construct `BS(84,83)`.
- `FIVE_COMB_PAIRED_LOBES.md`: distinct words in the two lobes reduce exact
  self-cancellation to one complementary length-five octet. There are 1,246
  octets and 768,512 sorted directed-pair inventories; the rank-nine
  projective quotient, 1,440 row orbits, physical hole fiber, and high-lag
  boundary table all survive.
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
- the frozen table in `search_lp333_quartic_quotient.cpp`: quotient energy
  112, 14/18 remaining quotient equations bad, hence not an `LP(333)`;
- the sextic table in `check_lp333_sextic_quotient.py`: both coordinate axes
  exact, but 20/24 mixed quotient cells bad, quotient energy 784, hence not an
  `LP(333)`;
- the exact sextic CP model has 108 primary signs, 2,862 cached XORs, the
  implemented 28-signature/298-shard channel, and the exact residual `C3`
  lex leader. Its latest 20-second four-worker pilot ended `UNKNOWN`, with no
  candidate, after 711 conflicts and 149,953 branches, at 2.11 GiB maximum
  RSS and zero swaps;
- no character checkpoint survives: the independently decimated
  degree-at-most-two Sidelnikov family has zero row-admissible orientation
  matches and zero exact PAF joins.

Read `README.md` for the lane map, `RESEARCH_LOG.md` for chronology, and
`PRIORITY_AUDIT.md` before making any novelty or publication claim.
Read `VARIABLE_Q_ROOT8.md` before doing any further seed-centered search:
shells through radius 33 are now excluded without a solver.

## Theory-first continuation order

1. Solve the audited 108-sign sextic `LP(333)` quotient with the implemented
   298 row-signature shards and residual `C3` quotient. Use
   `run_lp333_sextic_signature_shards.py` for atomic resume records, and
   strictly expand every feasible quotient before any claim.
2. Build the universal four-directed-pair model from
   `FIVE_COMB_PAIRED_LOBES.md`. Filter it with the modulo-16
   meet-in-the-middle and high-lag boundary table before imposing all 83
   lags. Omit the universally impossible structural core zero, leaving 31
   cores, and prioritize the 21 genuinely nondecomposable octet profiles.
3. Continue the prime-83 oriented-SDS construction outside the exact
   neighborhood already exhausted around profile 19. Any prime fold
   automatically triggers its finite modulo-84 lift bank.
4. Keep the quartic `LP(333)` quotient as a secondary independent lane.
   Do not rerun the 48 diagonal common-type five-comb cases: the complete
   1,536-shard corpus is closed.

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

The primary exact continuation is the sequential sextic signature corpus.
Every completed shard writes one atomic JSON record under
`output/lp333_sextic_signature_shards/`; existing records are skipped, so the
command is safe to interrupt and resume:

```sh
.solver-venv/bin/python run_lp333_sextic_signature_shards.py \
  --start 0 --end 297 --time-limit 3600 \
  --workers 1 --max-memory-mb 4096
```

Use `--rerun-unknown` only when intentionally extending the time allotted to
previously unresolved shards. A reported assignment is still accepted only
after the full `LP(333)` and `H(668)` candidate gate succeeds.

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
