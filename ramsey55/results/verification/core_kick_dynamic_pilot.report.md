# Dynamic core-kick constructive pilot

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and claim boundary

**REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the preregistered
three-seed, 36,000-step pilot did not find a \((5,5;43)\)-graph. Its best
retained candidate has

```text
seed       C5   I5   E   changed core   changed boundary
20260731    2    0   2        12                5
20260732    1    2   3         7                4
20260733    2    2   4        12                4
```

Here \(E=C_5+I_5\). Because every retained objective is nonzero, none of
these artifacts is a valid Ramsey construction. This bounded outcome does
not establish nonexistence or local optimality.

## Search region and policy

The search made all 237 edges incident to
\(\{3,4,7,38,41,42\}\) mutable. It also maintained a core Hamming distance
between 7 and 12 among the other 666 edges, so accepted search states lay
outside the certified aggregate core-radius-six region.

Restart zero began with proof-core ranks 1--7 flipped. The second restart
used a seeded mixture of four distinct ranks from the top 64 and three
distinct ranks from all 666 core edges. Search moves included unrestricted
boundary flips, admissible core flips, and changed/unchanged core swaps that
dynamically moved between distinct core cuts.

The implementation self-check exhaustively compared the incremental raw and
weighted deltas for all 903 single-edge flips against full enumeration. It
also checked 100 seeded dynamic core swaps, including objective, weighted
objective, and tracked core distance. The result was `PASS`; its retained
JSON record has SHA-256
`2b2ef3f0959aaa13006230099678be60a8ac0aa89a408fb7cc59d5da5084df6e`.

## Preregistration

The plan was written before the three production runs:

```text
results/benchmark_plans/core_kick_dynamic_pilot_v1.json
SHA-256 9eb107020d23b4af9e68f7efc41332f6793bbc411a9b2a53d615b86e319873ef
created_utc 2026-07-24T00:07:16Z
status PREREGISTERED_BEFORE_PRODUCTION_RUNS
seeds 20260731, 20260732, 20260733
2 restarts x 6,000 steps/seed = 36,000 total registered steps
180 seconds maximum wall time/seed
```

The plan pins the search source, reused incremental kernel, runner,
independent structural verifier, both graph verifiers, binary, base graph,
boundary metadata, and proof-core ranking by SHA-256.

## Exact commands

Compilation and preflight self-check:

```sh
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  src/search43_core_kick_lns.cpp \
  -o build/search43_core_kick_lns

build/search43_core_kick_lns \
  --seed-graph results/best_candidates/exoo_seed_20260724.g6 \
  --metadata certificates/residual_lns_incident_six.metadata.json \
  --ranking results/verification/residual_lns_incident_six_proof_core_edge_rank.json \
  --seed 20260731 \
  --initial-core-distance 7 \
  --min-core-distance 7 \
  --max-core-distance 12 \
  --guided-initial-edges 4 \
  --guided-pool 64 \
  --self-check \
  --self-check-random-swaps 100
```

Preregistered production run:

```sh
python3 src/run_core_kick_pilot.py \
  --plan results/benchmark_plans/core_kick_dynamic_pilot_v1.json
```

For each seed the runner executed the pinned binary with the exact options
in the plan, then independently ran:

```sh
python3 verify/exhaustive_verify.py \
  results/best_candidates/core_kick_seed_${seed}.g6

build/bitset_verify \
  results/best_candidates/core_kick_seed_${seed}.g6

python3 verify/core_kick_candidate_check.py \
  results/best_candidates/core_kick_seed_${seed}.g6 \
  --base results/best_candidates/exoo_seed_20260724.g6 \
  --metadata certificates/residual_lns_incident_six.metadata.json \
  --search-json results/verification/core_kick_seed_${seed}_search.json \
  --incident-vertices 3,4,7,38,41,42 \
  --min-core-distance 7 \
  --max-core-distance 12 \
  --output results/verification/core_kick_seed_${seed}_audit.json
```

The literal values substituted for `${seed}` were exactly `20260731`,
`20260732`, and `20260733`.

## Independent verification

For every retained candidate:

- direct Python enumeration of all \(\binom{43}{5}=962{,}598\) five-subsets
  reproduced the reported \(C_5\), \(I_5\), and \(E\);
- the independent C++ recursive-bitset verifier agreed on whether a
  5-clique and a 5-independent set exist;
- the independent structural audit validated the base and metadata hashes,
  the exact 237-edge boundary, all changed-edge counts and lists, core
  distance, graph6 payload, degrees, and objective.

All three structural audits returned `structural_valid=true`. They correctly
returned `accepted=false` and `ramsey_valid=false`, because each candidate
has \(E>0\). The preregistered E=0-only canonical export and adversarial
artifact-audit branch was therefore not invoked.

## Pinned implementation hashes

```text
search source
3af7168a8f90197a3286126a774f8aef5c5bae42d3c8f8fd14276e0ec8657fb0

incremental kernel source
556f5550f74b5d835b79646d888979177b710bda7ef5a9b83f4b30fb7fead3fe

pilot runner
a2233a8095d74e2dd46c81f68d79ff18eb626378846bd93ba1b67d5088a77a33

independent structural verifier
736d520de764fa6e7da614ab014a7447730c1604e12e9b5c5680a2bbe9e226cc

Python exhaustive verifier
fb8f5bee76f98a37a080970cd0548b88825f6f0f49f1144db20a3524ce5878b5

C++ recursive-bitset verifier
2ba9e189bc56b4d7c439b26317ade8eec60589c58e294bd26d7f35f4bd631f89

core-kick binary
8698ec5a69fd000949af75aef59c3c1277486f608298b5dee6f4fa9d5c56db04
```

## Result artifact hashes

```text
seed 20260731 candidate
64d2362eb9fac1ed2bf387578e92f3fc3bbdbe6655b38fa65329f737ee40bff6
search / Python / C++ / structural records
2a7c53b6ad90d4d5aba0670086c3a9c76288cec10bf8c6e05c42205228384f98
7d1d7942024d894da801261ceb9af19f95cefa6974eac850d7ebf798a7bc8d8f
898a0b3ec075f337bcbbf51f6bda9f048446d9932c5219dae2494cc049eed216
2b41d11b575eb7fe83a634c51391ea24bc66d8deb5f1668604658fd0102d3285

seed 20260732 candidate
e63c8890420eee6a8d1e8fa1a494cce3246e4e85b1769ed748a4fa74704b89d8
search / Python / C++ / structural records
ef8058634871be0b3e7aa6a272371b077fa14befda0b30238b9c555d97a937ac
5184d1b5b1f6d76025cc314cbe397406e75038e0ce5e3812b71159d33e53b3fd
07cb65b5936694d8d016f0c33fc2bf4b9084fd73b00a2569746b791c5e0b3f78
40d925daa3dfdb364fa312a58d88b8e3da4bbe55bba612466a61a8c26d3e11f1

seed 20260733 candidate
1128609d3a66f6b9c523544f634fdfdea87687acb5d5f3d9a3ba6811568b7cf7
search / Python / C++ / structural records
515ea6707fac9920ef304245e94a6ef6011a2525d7e20a41f0c655d9410054e5
5730b5c31835aa734506075a9530da77245f96efc703eff1753b18eaa15518bd
ec304564c7a87d6367b57f90b3ee99f72656b4ca7c03bbfc3b425929bc0cf292
d1de03d7ac84d6fd28c60b7a17f0c0a9d1917adee1e90341ed9dcd191f7af092

aggregate summary
7a587b2955817e79d33b74fcba4865f7b5f44dd376202d03982cf1f055c29753
```
