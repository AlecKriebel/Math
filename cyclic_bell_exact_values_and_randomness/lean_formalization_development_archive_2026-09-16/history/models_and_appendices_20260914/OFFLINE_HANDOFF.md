# Offline build and repair handoff — model-value extension

## Source status and safe installation

**No Lean invocation has run on this package.** Every mathematical declaration
is an uncompiled proof-script candidate. Some repairs may be substantive.

The complete zip has root
`cyclic_bell_exact_values_and_randomness/lean_formalization/`. Put it at that
location in `Math`, preserving unrelated work. The delta patch is for the exact
previous all-dimensional archive, SHA-256
`093043d7db11aea7d45c5896c4d16ae071184c92d4085757ef1d552b3c6f9255`.
The full additive patch is only for a checkout where this companion directory
does not exist. Always run `git apply --check` first; neither patch should be
used to overwrite offline repairs without reconciliation.

The original manuscript and qubit project were not changed. No external
correspondence, GitHub release or DOI is authorized by this workflow.

## One command

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Lean: `leanprover/lean4:v4.19.0`, compiler
`6caaee842e9495688c1567e78c0e68dbb96942aa`. Mathlib:
`c44e0c8ee63ca166450922a373c7409c5d26b00b`; all nine dependencies are locked.
Omit `--bootstrap` when the pinned packages and cache already exist.

The command requires the canonical manuscript Git blob
`bbd0667c934d5a34dd9c8ced50df91515cb1308c` and SHA-256
`82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
The latter was read from the repository manifest, not recomputed from canonical
raw bytes in this continuation. Reconcile a mismatch explicitly rather than
loosening the hash check to certify a different manuscript silently.

The runner refuses dirty/wrong-revision dependency resets and symlinked build
locations, removes only this companion's `.lake/build`, builds the default
umbrella, tests all 15 registered controls, executes all 1,332 axiom requests
and expanded statements, and rechecks protected hashes. It writes a receipt,
not a commit, publication or release. It does not bootstrap the compiler or
rebuild every upstream dependency from source; the usual compiler/cache trust
boundary remains.

## Repair order

First repair the retained d4 path and its existing audits. Then repair the earlier
all-dimensional path in the order recorded in the historical handoff and
`ALL_DIMENSION_ROUTES.md`. Do not hide an earlier failure by dropping its import.

For the new extension, proceed in dependency order:

1. `GeneralBehavior`: real Born correlators, score bridges, continuity and
   conditionally complete supremum lemmas.
2. `GeneralCommutingModel`: actual PVM vector behavior and its scalar/operator
   bridges on arbitrary complete Hilbert spaces.
3. `GeneralHilbertBridge`: Euclidean matrix action, conjugate transpose/adjoint,
   actual positive-square-root purification and full behavior equality.
4. `GeneralCorrelationValues`: actual Qq/Qqa/Qqc membership, arbitrary competitors,
   separate reduced/augmented settings and four model supremum theorems.
5. `GeneralBinaryModels`, `GeneralModelCounterexamples`, `GeneralPartySwap` and
   `GeneralExactValues`.
6. `GeneralBinaryCertification`: actual finite purified PVM strategies,
   outcome-by-outcome binary encoding, conditional-state privacy and setting
   minimality. `GeneralCycleCharpoly`: prefix products and actual characteristic
   polynomial coefficient extraction.
7. `ModelValueStatements`, all other statement audits, `AxiomAudit` and separate
   positive/negative control files.

Large `simp`/`module`/noncommutative blocks and dependent typeclass projections
may require explicit intermediate lemmas. Do not assume that all errors are
mere library name changes. The final acceptance command must build every claimed
endpoint and audit from a clean companion build directory.

## Invariants not to weaken

No score/maximality/privacy restriction belongs in a physical strategy definition.
Keep arbitrary finite local dimensions, arbitrary PSD trace-one mixed states,
zero measurement effects, and genuinely arbitrary complete Hilbert spaces for
commuting upper bounds. Do not add same-party commutation.

The behavior is REAL Born probabilities. Keep `chi(a+b)`, Bob's entrywise
conjugation, literal signed lambda coefficients and the target `(1,none)`.
Reduced Bob input sets must remain truly reduced, not renamed augmented sets.
Qqa is actual topological closure; suprema are actual `sSup` with nonemptiness
and bounds proved. Do not assume general Qqa-subset-Qqc merely to simplify a
particular Bell-value theorem.

Purifications use the actual density square root. Physical Eve states are
post-measurement sandwiches and partial traces. Binary privacy quantifies over
all finite compatible purifications and is not inferred from uniform scalar
probabilities. The swapped cyclic witness is not asserted to be an adversarial
optimizer. The nonunit characteristic-polynomial theorem must not gain an
unannounced unit-modulus hypothesis.

No `sorry`, `admit`, `sorryAx`, custom mathematical axiom, `native_decide`, unsafe
evaluation, external solver verdict or omitted endpoint is allowed as a repair.

## Compiler-free checks and registered controls

```sh
python3 scripts/source_inventory.py --write
python3 scripts/static_audit.py --output logs/local_static.json
python3 scripts/test_runner.py
python3 scripts/model_bridge_preflight.py --output logs/local_model_bridges.json
python3 scripts/cycle_charpoly_preflight.py --output logs/local_cycle_charpoly.json
```

These commands never run Lean. The separate offline Lean runner has three
positive controls and twelve intentionally false controls. New false statements
concern the reduced second-family value, closure-model augmented value, actual
purification normalization and the sign in a nonunit cycle characteristic polynomial. A false file must fail for a genuine proof
error, not an unrecognized identifier, missing import or syntax failure.
The new static registry verifies that every control is registered with its
correct expected outcome; mocked unit tests check the reporting behavior.

Regenerate inventories after every source repair, then freeze them during the
actual formal audit. Do not rename a failing negative test into an unregistered
file or import it into the normal library.

## Independent review and remaining gaps

Read `COVERAGE.md` and `MODEL_VALUE_SELF_AUDIT.md`. A separate reviewer should
check the manuscript labels, all physical definitions and the complete bound /
attainment / probability / privacy dependency paths after a genuine kernel pass.
The current source is not whole-paper complete: general Qqa-subset-Qqc,
source-Z/qutrit identification, selected standard/anchored probability and
asymptotic calculations, and full adversarial guessing-model supremum assembly
remain outside its endpoints. Replaced proof routes are identified explicitly.

Kernel acceptance alone must not automatically set
`formal_endpoint_certified` or `whole_paper_source_complete` to true.
