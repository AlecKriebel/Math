# Fast basis-bracket evaluator

## Mechanism

`Kourovka/Ambient/FastBasis.lean` defines an integer-only evaluator `coeff ts i j o` for arbitrary lists of sparse skew-half terms. Each contribution checks the forward/reversed input pair and output coordinate and adds/subtracts the displayed integer coefficient. It preserves duplicate contributions, permits arbitrary natural indices, and retains the original zero-extension behavior.

The generic proofs establish equality with the actual `Sparse.entry` and `Sparse.fromTerms` applied to coordinate vectors. `bracket_sound` specializes this to the frozen ambient table. `termCheck_of_coeff` derives the original complete vector-valued TermCheck, without weakening its quantified input coverage.

`cast_fromTerms_sound` transports the integer computation to every commutative coefficient ring through the existing `mapVec_terms` and `mapVec_unit` theorems. Thus it can be instantiated with `scaledTerms` over the rationals for inner-column checks or with integers for lattice embedding checks. It does not introduce a replacement bracket, accept externally computed values, or claim that any concrete certificate passes.

## Validation

The helper, including its generic cast theorem, compiles under the pinned Lean 4.19.0 with exit status zero and no warnings/errors using `lake env lean -j1 -s65536 -o ... Kourovka/Ambient/FastBasis.lean`.

The scratch `FastBasisShard30.lean` proves the original TermCheck30 via the integer evaluator and the original JacobiCheck30 via existing integer computation. Both use kernel reduction. It passed in 48.90 seconds wall time (47.88 seconds user CPU), recorded in `fast_basis_shard30.log`. This is one end-to-end shard measurement under concurrent host load, not a clean speed ratio benchmark. Existing ambient check shards were left unchanged at the parent's request because their original repaired build was already progressing.

No admissions, custom axioms, native computation proof mechanisms, or theorem weakening were added. Generic cast-theorem compilation is checked; downstream integration and performance are owned by the embedding/certificate reviewers.

Checkpoint: 2026-09-19T04:03:31.598843+00:00. Assigned helper implementation and compilation: 100% complete; no claim of complete problem formalization.

Source SHA256: `53d7861d0a22222c75472cef995d88fbf600f6a3a623ce2e8b5fea67a5aa3c4a`.
