# Incident-six constructive LNS, seed 20260726

Date: 2026-07-23

## Outcome and scope

**REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the deterministic restricted
search completed 300,000 moves and retained objective `E=2`. It did not find
a `(5,5;43)` graph and does not improve a Ramsey-number bound.

The retained candidate has two 5-cliques and zero independent 5-sets. It is a
distinct, complement-side `E=2` assignment 135 free-edge flips from the
input candidate. All 666 fixed edges were preserved exactly.

## Evidence controls

The standalone source is `src/search43_incident_lns.cpp`. Before search it:

1. compares all 237 recorded metadata edge pairs with the exact set of edges
   incident to `{3,4,7,38,41,42}`;
2. requires the seed graph to equal the metadata `base_graph6`, thereby
   pinning all 666 fixed edges and all 237 initial free values;
3. checks the metadata `base_true_variables` against the decoded seed;
4. emits JSON-escaped graph6 and path strings.

The final-source self-check compared every one of the 237 free-edge
incremental deltas against full 5-subset enumeration. It repeated all 237
checks with deterministic nonuniform forbidden-set weights, then checked
100 sequential random free-edge flips in both objectives. All 674 comparisons
passed, and fixed edges remained unchanged.

An altered graph is rejected with
`seed graph does not equal metadata base_graph6`; the older 19-edge metadata
is rejected with
`metadata free_edges does not equal the incident-six edge set`. The complete
search stdout was parsed successfully as JSON.

## Commands

Compilation:

```sh
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  src/search43_incident_lns.cpp \
  -o build/search43_incident_lns
```

Self-check:

```sh
build/search43_incident_lns \
  --seed-graph results/best_candidates/exoo_seed_20260724.g6 \
  --metadata certificates/residual_lns_incident_six.metadata.json \
  --seed 20260726 \
  --self-check \
  --self-check-random-flips 100
```

Production search:

```sh
/usr/bin/time -p build/search43_incident_lns \
  --seed-graph results/best_candidates/exoo_seed_20260724.g6 \
  --metadata certificates/residual_lns_incident_six.metadata.json \
  --seed 20260726 \
  --steps 75000 \
  --restarts 4 \
  --tabu 9 \
  --random-walk 0.04 \
  --breakout-interval 250 \
  --restart-perturbation 12 \
  --output results/best_candidates/incident_lns_seed_20260726.g6
```

The run executed 300,000 moves and 1,528,975 delta evaluations in 27.084184
internal seconds (27.15 wall seconds). It performed 1,197 breakout-weight
updates and 13 equal-objective diversity updates.

Independent verification:

```sh
python3 verify/exhaustive_verify.py \
  results/best_candidates/incident_lns_seed_20260726.g6

build/bitset_verify \
  results/best_candidates/incident_lns_seed_20260726.g6
```

The direct Python every-5-subset verifier reports `C5=2`, `I5=0`, `E=2`.
The independent C++ recursive-bitset verifier reports a 5-clique and no
independent 5-set. Both reject the graph as a valid `(5,5;43)` graph.

## Artifacts and hashes

```text
source
556f5550f74b5d835b79646d888979177b710bda7ef5a9b83f4b30fb7fead3fe

compiled binary
19855fef431a03ae5a2d45a159b51a0c94e8e49aaaf9a64be81799852901ae46

candidate graph6
c0a8d2de5e7efa1abc6848c71e61019579ff31d8958fcce70f257d725792c337

canonical candidate JSON
51dc724e2ab82293bf604e3d45d0c23b7c7e9984641f8b9e274afaa7e77fff3d
```

Machine-readable search, self-check, and verifier outputs are retained beside
this report in `results/verification/`.
