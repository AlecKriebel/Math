# Certificate-first research on \(R(5,5)\)

Retrieval and first execution date: **2026-07-23**.

This repository separates three evidence categories:

- **CERTIFIED:** checked by a small independent verifier, proof checker, or a
  complete elementary proof recorded here.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** backed by source, configuration,
  seed, environment, runtime, and an artifact, but not a theorem.
- **CONJECTURE OR HEURISTIC:** search guidance or interpretation only.

## Current result

**CERTIFIED:** the reconstructed Exoo graph in
`data/exoo42_constructed.canonical.json` is a \((5,5;42)\)-graph. The exhaustive
Python verifier finds \(C_5=I_5=0\), and the independent C++ recursive bitset
verifier finds neither a 5-clique nor an independent 5-set. This proves
\(R(5,5)\geq 43\).

**CERTIFIED:** this particular fixed 42-vertex graph has no one-vertex
extension. Its 42-variable, 2,318-clause CNF is UNSAT, as checked by two small
exhaustive DPLL-tree proof paths. This result is scoped to the fixed core and
does not prove that arbitrary \((5,5;43)\)-graphs do not exist.

**CERTIFIED:** deleting any one of the 42 vertices of this Exoo graph and
introducing two new vertices also yields no completion when the remaining
41-vertex induced core is fixed. All 42 separately labeled 83-variable CNFs
are UNSAT; an independent checker accepted all 42 proof trees. This is still a
family of fixed-core results, not global nonexistence at order 43.

**CERTIFIED:** for the first bounded \(k=2\) benchmark, deleting original
vertices 0 and 1, fixing the remaining 40-vertex induced core, and adding
three new vertices gives a 123-variable, 13,338-clause UNSAT instance. An
independent direct five-subset reconstruction matched every clause, and a
small proof checker accepted all 19,734 records. This covers exactly one of
861 two-vertex deletion pairs, not arbitrary order-43 graphs.

**CERTIFIED:** four exact large-neighborhood completions around the current
\(E=2\) candidate are UNSAT under their stated fixed boundaries. The free-edge
sets have 19, 66, 80, and 86 variables; the latter two progressively release
cycle-cut and proof-trace-selected boundary edges. Every CNF was independently
reconstructed and every exhaustive tree proof checked. These results rule out
only those four neighborhoods; they do not establish global or unrestricted
local nonexistence.

**REPRODUCIBLE COMPUTATIONAL OBSERVATION:** freeing all 237 edges incident to
the six residual-conflict vertices produced an exact 49,461-clause formula,
but the bounded solver timed out at 60.003 s. This is neither SAT nor UNSAT
and supports no existence or nonexistence conclusion.

**CERTIFIED:** the unrestricted direct \(n=43\) CNF encoding was generated and
independently reconstructed clause-by-clause: 65,403 variables and 2,052,132
clauses, including the sound degree bounds \(18\le d(v)\le24\). This certifies
the encoding identity only. No global solve was launched.

**REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the best 43-vertex candidate has
\(C_5=0\), \(I_5=2\), \(E=2\). It is **not** a Ramsey graph and proves no new
bound.

Current primary sources report \(43\leq R(5,5)\leq46\). The upper-bound
computation has not been replayed or certificate-checked in this repository;
see `literature.md`.

## Reproduce

The implementation has no third-party runtime dependencies.

```sh
make test

python3 src/construct_exoo42.py \
  --graph6 data/exoo42_constructed.g6 \
  --artifact data/exoo42_constructed.canonical.json

python3 verify/exhaustive_verify.py data/exoo42_constructed.g6 --k 5
build/bitset_verify data/exoo42_constructed.g6 --k 5

python3 verify/canonical_artifact_check.py \
  data/exoo42_constructed.canonical.json

python3 verify/extension_sat_proof_check.py \
  --graph data/exoo42_constructed.g6 \
  --proof certificates/exoo42_extension_sat_proof.bin

python3 verify/core_completion_batch_check.py \
  --input-dir certificates/core_completion_all42 \
  --expect-all-42 \
  --output /tmp/core_completion_batch_recheck.json

python3 verify/core_completion_k2_cnf_check.py \
  --graph data/exoo42_constructed.g6 \
  --cnf certificates/core_completion_k2_delete_00_01.cnf

python3 verify/extension_sat_check.py \
  certificates/core_completion_k2_delete_00_01.cnf \
  certificates/core_completion_k2_delete_00_01.tree

python3 verify/residual_lns_cnf_check.py \
  --graph results/best_candidates/exoo_seed_20260724.g6 \
  --cnf certificates/residual_lns_twelve_vertex.cnf \
  --free-vertices 3,4,7,10,21,22,30,31,32,38,41,42

python3 verify/extension_sat_check.py \
  certificates/residual_lns_twelve_vertex.cnf \
  certificates/residual_lns_twelve_vertex.tree

python3 verify/direct_ramsey_cnf_check.py \
  certificates/direct_ramsey43.cnf \
  --order 43

build/search43 --benchmark --n 43 --seed 20260723

build/search43 \
  --n 43 \
  --seed 20260724 \
  --steps 50000 \
  --restarts 4 \
  --tabu 11 \
  --random-walk 0.02 \
  --seed-graph data/exoo42_constructed.g6 \
  --output /tmp/exoo_seed_20260724_reproduction.g6
```

The search command is deterministic on this recorded compiler/runtime and
reproduces the saved \(E=2\) graph byte-for-byte. The temporary output avoids
overwriting the retained artifact. A later audit replayed all four recorded
search configurations from current source SHA-256
`2f0a1fba656b7550124f2a213a046c5ace42742d4d8e3c36967eefabe16e3674`;
all outputs were byte-identical, with raw stdout, environment, exit status,
and verifier reports retained under `results/reproductions/`.

## Independent verification paths

1. `verify/exhaustive_verify.py` iterates over every 5-subset and directly
   tests its ten pairs. It returns exact \(C_5\) and \(I_5\) counts.
2. `verify/bitset_verify.cpp` has a separate graph6 parser and recursively
   searches adjacency bitsets for a clique in the graph and its complement.
   It does not call the search kernel or the Python subset counter.

In addition, `verify/canonical_artifact_check.py` independently decodes
graph6 and cross-checks the adjacency list, edge list, adjacency matrix, edge
count, degree sequence, JSON schema, and byte-level deterministic
serialization. Its adversarial tests tamper with each representation
separately.

The test suite includes complete and empty graphs, deterministic random graphs
and complements, \(C_5\) as a \((3,3;5)\) construction, and the Paley-17
\((4,4;17)\) graph. The flip identity is exhaustively checked on all 32,768
labeled graphs of order 6 and all 491,520 possible flips.

The files named `*.canonical.json` are deterministic multi-representation
artifact serializations, not canonical graph labelings under isomorphism.
No isomorphism-deduplication claim is made without a canonical-labeling tool.

## Layout

- `STATE.md`: live research state and next experiment.
- `CLAIMS.md`: publishable claims and exact supporting artifacts.
- `RESEARCH_LOG.md`: append-only narrative of executed research cycles.
- `literature.md`: actionable source extraction.
- `environment.md`: machine and solver audit.
- `src/`: construction, graph I/O, analysis, and search code.
- `verify/`: independent verifier and adversarial audit paths.
- `tests/`: deterministic correctness tests.
- `data/`: reconstructed or imported input graphs with provenance.
- `results/experiments.csv`: append-only experiment ledger.
- `results/README.md`: experiment-field semantics.
- `results/best_candidates/`: immutable candidate snapshots.
- `certificates/`: SAT/proof-certificate work.
- `notebooks/`: optional exploratory work; authoritative checks live in source.
