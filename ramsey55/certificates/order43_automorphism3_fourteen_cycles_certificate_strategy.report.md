# Exact certificate strategy for cycle type \(3^{14}1\)

## Result and claim boundary

The orbit formula, root-neighborhood reduction, degree strengthening, and a
full greedy normalizer quotient have been generated and independently checked
clause by clause.

**No UNSAT proof has been obtained.** The cycle type \(3^{14}1\) therefore
remains unresolved. Nothing here excludes all order-three automorphisms,
excludes arbitrary order-43 graphs, or changes a Ramsey bound.

## Exact structural reduction

Let the prescribed automorphism be

\[
(0\,1\,2)(3\,4\,5)\cdots(39\,40\,41)(42).
\]

Every invariant graph is represented exactly by one Boolean variable for each
edge orbit. There are 301 orbits, all of size three. Exhaustive enumeration of
the 962,598 five-sets gives 320,593 distinct edge-orbit signatures and 641,186
Ramsey clauses. The canonical unsymmetrized DIMACS stream has SHA-256
`2cb249c2d09d00bd199be27711fc344873785b9e9756dc1cafad8f756084a5e5`.

Every vertex in a \((5,5;43)\)-graph has degree between 18 and 24. Indeed, a
neighborhood has neither a \(K_4\) nor an independent 5-set, and a
nonneighborhood has neither a \(K_5\) nor an independent 4-set. The equality
\(R(4,5)=R(5,4)=25\) gives

\[
d(v)\le 24,\qquad 42-d(v)\le24.
\]

The unique fixed vertex sees each moved 3-cycle either completely or not at
all. If it sees \(m\) cycles, its degree is \(3m\), so

\[
m\in\{6,7,8\}.
\]

Graph complementation preserves the cycle type and maps \(m\) to \(14-m\);
it exchanges 6 and 8. Permuting the fourteen 3-cycle blocks centralizes the
prescribed automorphism, so the root incidences can be sorted into a true
prefix. Consequently the two prefix lengths 6 and 7 cover the complete
cycle type. The independent checker enumerated all

\[
\binom{14}{6}+\binom{14}{7}+\binom{14}{8}=9,438
\]

degree-allowed labeled root neighborhoods and verified this reduction.

The single cover CNF has 301 variables and 641,201 clauses. Its SHA-256 is
`513b922ae8d7f4ec5fc68f7bac63d7d8c81ffb681c6d4e5a9cc5bba3abcff946`.
It adds thirteen prefix-order clauses and the two units selecting prefix
length 6 or 7. The independent checker reconstructed and matched every clause;
its result SHA-256 is
`b78826f4bf0b7637b41de5be085d24c13ebaed66ce9d48473f3c59cfdd39ad77`.

## Case formulas and exact degree layer

Fixing each prefix separately permits exact unit simplification:

| Root cycles | Variables | Clauses | CNF SHA-256 |
|---:|---:|---:|---|
| 6 | 301 | 571,377 | `ed307aeb8a96f95eed2763fa127cd23465355e4850e232ccccdaaf6ada09159b` |
| 7 | 301 | 570,808 | `bfa8b38569c7d1a9554787b36cf64f8eb54dea7ee06ff3e7a36fb571278b8272` |

For each moved vertex orbit, its degree is a weighted sum of 41 primary
variables: forty terms of weight one and one term of weight two. Fourteen
independent cumulative-threshold encodings enforce degree 18--24. They add
14,350 auxiliary variables and 56,155 clauses. The independent checker
reconstructed every weighted expression and every threshold recurrence.

| Root cycles | Variables | Clauses | CNF SHA-256 |
|---:|---:|---:|---|
| 6 | 14,651 | 627,532 | `e71953484d6d1e8bd42b4a1105391e4fd59b568818fb2f2430bd54cdbba4b8ff` |
| 7 | 14,651 | 626,963 | `4ac33e50340bf4f023a8d8c1096e73105c476fc0f4578687ce20e949bc4f4122` |

Checker-result SHA-256 values are
`aafb18faed58e1ba5447755a05d157785d547d5cdaad375234f1e93198d0906a`
and
`281dddd8e4061f6468339edbfd7e5bd645e113c6abfd45dcd72f8883bf9d2f8f`.

## Full greedy normalizer quotient

After the root partition is fixed, the block/phase subgroup
\(C_3^{14}\rtimes S_{14}\) remains available subject to preserving root
incidence. The preferred formulas select a representative constructively:

1. choose cycle zero among the root-neighbor cycles with maximal internal-edge
   bit;
2. regard a simultaneous phase shift as the prescribed automorphism itself,
   so the reference phase is immaterial;
3. at every subsequent position, compare every remaining block in all three
   phases by its full edge profile to the already fixed prefix;
4. move a lexicographically maximal oriented block to that position and
   continue.

A maximum always exists at each finite step, so these clauses retain at least
one representative of every orbit. Exact prefix-equality variables encode
each lexicographic comparison. Producer and independently written checker
agree on every profile, phase rotation, auxiliary variable, and clause.

| Root cycles | Profile comparisons | Variables | Clauses | CNF SHA-256 |
|---:|---:|---:|---:|---|
| 6 | 140 | 17,393 | 643,989 | `7f5ee1c01793a7bfe3d4f8bca19e4e4f8f002eaf940a3d4815bb50e8f9cfecd9` |
| 7 | 134 | 17,150 | 641,963 | `1ca75cb8c35155952c9c13c4fccb62dadd5d5e4f80139d25fd8583bad7142405` |

Checker-result SHA-256 values are
`b41133e37e379b6704c44c6b557172e13d1c384eac3a552d1c7350525192b8d8`
and
`f3389eea4bae08af01ce911416d770ca4bd58259831cd011c77333ac706463e8`.
Sixteen focused structural tests pass.

## Solver and proof status

The formula-matched completed negative runs used in this report are
reproducible observations, not proofs:

| Formula | Solver | Outcome | Conflicts |
|---|---|---|---:|
| combined prefix cover | Glucose3 | budget exhausted | 2,006,143 |
| reduced root-6 | Glucose3 | budget exhausted | 2,005,117 |
| reduced root-7 | Glucose3 | budget exhausted | 2,000,037 |
| degree root-6 | CaDiCaL 1.9.5 | budget exhausted | 1,000,001 |
| intermediate normalizer root-6 | Glucose3 | budget exhausted | 2,012,390 |
| greedy root-6 | Glucose3 | budget exhausted | 2,251,748 |

The serialized greedy CaDiCaL run and a subsequent 63-case internal-triangle
count split were both terminated externally by signal 15 before writing
result JSON. They imply nothing about satisfiability. Their interruption
manifest has SHA-256
`ffe59f528eedf1a9024aa41d4283a32c9b42b99de362be5c6d5fa9b824af00bc`.

An earlier normalizer diagnostic refers to a superseded CNF fingerprint whose
materialized file was replaced during refinement. It is deliberately omitted
from the evidence table and no inference relies on it.

Because no complete run returned UNSAT, there was no valid terminal result to
feed into the DRAT-to-LRAT certification stage. No DRAT or LRAT proof is
claimed or retained for this class.

## Reproduction

```sh
python3 src/automorphism3_fourteen_cycle_certificate.py \
  --mode cover \
  --cnf certificates/order43_automorphism3_fourteen_cycles_symmetry_cover.cnf \
  --metadata certificates/order43_automorphism3_fourteen_cycles_symmetry_cover.metadata.json

python3 verify/automorphism3_fourteen_cycle_symmetry_cnf_check.py \
  certificates/order43_automorphism3_fourteen_cycles_symmetry_cover.cnf \
  --metadata certificates/order43_automorphism3_fourteen_cycles_symmetry_cover.metadata.json \
  --result results/verification/order43_automorphism3_fourteen_cycles_symmetry_cover_check.json

python3 src/automorphism3_fourteen_cycle_greedy_certificate.py \
  --root-cycles 6 \
  --cnf certificates/order43_automorphism3_fourteen_cycles_root6_greedy.cnf \
  --metadata certificates/order43_automorphism3_fourteen_cycles_root6_greedy.metadata.json

python3 verify/automorphism3_fourteen_cycle_greedy_cnf_check.py \
  certificates/order43_automorphism3_fourteen_cycles_root6_greedy.cnf \
  --metadata certificates/order43_automorphism3_fourteen_cycles_root6_greedy.metadata.json \
  --result results/verification/order43_automorphism3_fourteen_cycles_root6_greedy_check.json

python3 -m unittest -v \
  tests/automorphism3_fourteen_cycle_tests.py \
  tests/automorphism3_fourteen_cycle_degree_tests.py \
  tests/automorphism3_fourteen_cycle_normalizer_tests.py \
  tests/automorphism3_fourteen_cycle_greedy_tests.py
```
