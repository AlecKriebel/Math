# Known order-42 catalog: fixed one-vertex extension certificates

## Result

**CERTIFIED, WITH FIXED-CORE SCOPE:** none of the 328 distinct
\((5,5;42)\)-graphs in `data/r55_42some.g6` has a one-vertex extension to a
\((5,5;43)\)-graph.

The source data page states that the other 328 historically known graphs are
the complements of these entries. Complementing the 42-vertex core and
negating all 42 new-vertex adjacency variables swaps the clique-prevention
and independent-set-prevention clauses. Consequently, fixed-extension
satisfiability is invariant under complementation, so the same conclusion
covers all 656 historically known graphs.

This is **not** a classification of all \((5,5;42)\)-graphs and is **not** a
global order-43 nonexistence proof. The source explicitly says that further
42-vertex graphs, and even larger graphs, may exist.

## Imported-catalog verification

- Source:
  `https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6`
- Retrieved bytes: 47,888
- Catalog SHA-256:
  `067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`
- Exact non-comment line count: 328
- Distinct graph6 line count: 328
- Exhaustive Python verifier passes: 328
- Independent C++ bitset verifier passes: 328
- Dual-verification result SHA-256:
  `6fe9186d25b16efe98029f60b11f4a5f5f8559c7150380cb3dc45b09833c0931`

The two verifier programs have separate graph6 decoding and forbidden-set
enumeration paths.

## Extension proof batch

The production C++ solver rebuilt the exact fixed-extension CNF for every
catalog line. For each core, its 42 Boolean variables are the adjacencies of
the new vertex. A negative clause forbids the new vertex from completing a
core \(K_4\) to a \(K_5\); a positive clause forbids it from completing a
core independent four-set to an independent five-set.

- Exact covered lines: 1 through 328
- SAT: 0
- UNSAT: 328
- limits: 0
- independently checked UNSAT proofs: 328
- total proof bytes: 17,246
- proof-bundle SHA-256:
  `79f5e8bb5c2373aea2b162159c20b8960b2250a532793cdfc0af8f4b2c33aa92`
- total DPLL tree nodes: 12,982
- total DPLL leaves: 6,655
- total unit assignments: 157,095
- producer elapsed-time sum: 0.312007 seconds
- checker elapsed-time sum: 93.792287 seconds
- recovered-batch wall time at eight jobs: 16.650744 seconds
- consolidated result SHA-256:
  `5c9ce7bd1789e2496a6bcb0ad7521712a721b99b4154ed1f5f861921cca7a81d`

The independent checker has its own graph6 decoder, reconstructs all clauses
directly from four-subsets, repeats unit propagation, and traverses the
complete proof tree. It matched the producer's clause, tree-node, and
tree-leaf counts for every instance.

## Fail-closed recovery note

The preregistered first orchestration attempt stopped after all 328 producer
proof files had been written because the wrapper incorrectly treated the
solver's conventional UNSAT process exit code 20 as an infrastructure error.
No mathematical result was recorded by that failed wrapper.

The retained first-run proofs were not deleted or overwritten. The wrapper
was corrected to accept only the documented exit codes 2, 10, and 20 and to
support a recovery mode that:

1. requires exactly the 328 expected retained filenames and no extras,
2. reruns every producer into a distinct temporary replay file,
3. requires every replay to be byte-for-byte identical to its retained
   first-run proof,
4. removes only the temporary replay after a successful comparison, and
5. independently checks the retained proof.

All 328 replays were byte-identical. The recovery-mode count in the
consolidated result is 328.

The immutable preregistration records the original wrapper SHA-256
`77d4c40b4d85e73cb8ac53109e19cd7072b1961a16fd784c4995e69986baf69d`.
The recovery wrapper SHA-256 is
`13cb02a12ec306dcaa71eb723b5152f85a1aa3bbaad570b02604617fcb4109a8`.
The mathematical producer and independent checker remained pinned at:

- solver executable:
  `5c52f4e24b5770e01cef36320e9699d31884caa3db2b830a29475689bf877fd6`
- checker source:
  `abd751b8635c03423736e7f66e0a2b33ce86b639a4d6ac23310dc83330fd7a9b`

## Reproduction

The immutable plan is
`results/benchmark_plans/catalog42_extension_all328_v1.json`, SHA-256
`80b137339d5ff26ad81c987c33e0d4f6b1959f126ffda95ebf9f918debe280e8`.
The recovered command is:

```text
python3 src/catalog42_extension_batch.py data/r55_42some.g6 \
  --proof-dir certificates/catalog42_extensions_v1 \
  --result certificates/catalog42_extensions_v1.result.json \
  --expected-count 328 \
  --expected-sha256 067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb \
  --jobs 8 --seconds-limit 60 --reuse-existing-proofs
```

The recovery flag is appropriate only when the directory already contains
the exact first-run proof set. A fresh run must use an empty output
directory and omit that flag.
