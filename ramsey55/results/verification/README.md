# Recorded verification outputs

Commands:

```sh
python3 verify/exhaustive_verify.py data/exoo42_constructed.g6 --k 5
build/bitset_verify data/exoo42_constructed.g6 --k 5

python3 verify/exhaustive_verify.py \
  results/best_candidates/exoo_seed_20260724.canonical.json --k 5
build/bitset_verify results/best_candidates/exoo_seed_20260724.g6 --k 5

python3 verify/canonical_artifact_check.py \
  data/exoo42_constructed.canonical.json \
  --output results/verification/exoo42_canonical_artifact_check.json

python3 verify/canonical_artifact_check.py \
  results/best_candidates/exoo_seed_20260724.canonical.json \
  --output results/verification/best43_canonical_artifact_check.json
```

`exoo42_python.json` and `exoo42_cpp.json` are the two successful independent
outputs for the 42-vertex witness.

`best43_python.json` and `best43_cpp.json` both reject the current 43-vertex
candidate. A nonzero verifier exit for this candidate is expected and is not a
tool failure.

The two `*_canonical_artifact_check.json` reports come from an independent
strict JSON/graph6 implementation. They validate every stored representation,
including the adjacency list, edge list, matrix, edge count, and degree
sequence.
