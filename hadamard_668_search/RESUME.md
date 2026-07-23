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
- a solver-backed exhaustive computation reports no exact `BS(84,83)`
  sequence through raw labelled Hamming distance 18 of the seed; the retained artifact
  checker verifies the decomposition and records, not the 1,296
  solver-reported UNSAT claims (1,284 root-layer and 12 compression-layer
  leaves); four representative leaves now have independently checked DRAT
  proofs and all twelve stored root witnesses pass pinned positive-CNF
  validation, leaving the full UNSAT gate incomplete;
- inversion-symmetric/normalized-skew `LP(333)` type pairs are impossible;
- several large, explicitly defined local neighborhoods around retained near
  misses have been independently exhausted.

Read `README.md` for the lane map, `RESEARCH_LOG.md` for chronology, and
`PRIORITY_AUDIT.md` before making any novelty or publication claim.

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

## Resource rules for the 16 GiB host

- Run one solver or production search at a time.
- Keep CP-SAT at one worker.
- Treat `max_memory_in_mb` as an internal solver limit, not a process limit.
- Do not enlarge the full 111,554-variable fixed-profile model here: measured
  whole-process peaks were 703 MB and 931 MB in short pilots despite lower
  internal limits.
- The C++ local engines use under 10 MB; the independent radius-two verifier
  uses about 73 MB; the outer profile sampler has used at most 117 MB.
- Record seed, command, wall time, maximum RSS, swap count, solver status, and
  output hash for every retained production result.

The next high-value step is structural mathematics or distributed exact
sharding, not indefinite repetition of the same local annealer.
