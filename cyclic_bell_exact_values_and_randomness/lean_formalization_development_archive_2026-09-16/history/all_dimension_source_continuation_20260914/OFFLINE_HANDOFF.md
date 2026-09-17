# Offline build and repair handoff

## Input status and non-negotiable contract

This is a source-writing handoff. **Do not initially describe it as formalized
or checked.** There were zero Lean invocations and zero actual axiom reports in
the cloud continuation. Python/static tests are supplementary only. Many tactics,
coercions and library interfaces have not been tested and some proofs may need
substantive mathematical repair rather than a spelling correction.

Canonical source Git blob: `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
Expected SHA-256 recorded in the repository manifest:
`82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
The cloud did not independently recompute the latter from raw canonical bytes.
The runner checks both against the actual local manuscript before certification.

The exact previous d=4 input archive has SHA-256
`12fbcb1179f32b5ac1f3cdc2d0b59f2c76a3abf4da5d9022e5018973ed949d85`.
Use the delta patch only on that exact source state. Use the full additive patch
only where the companion directory is absent. Never overwrite local repairs or
parallel work merely to make a patch apply.

## Build command

From `Math/cyclic_bell_exact_values_and_randomness/lean_formalization/`:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Lean must be `leanprover/lean4:v4.19.0`, compiler commit
`6caaee842e9495688c1567e78c0e68dbb96942aa`; Mathlib must be
`c44e0c8ee63ca166450922a373c7409c5d26b00b`. All nine dependencies are locked.
With dependencies already present, omit `--bootstrap`.

The command verifies pins and manuscript identity, refuses dirty dependency
resets and symlinked build locations, removes only this companion's `.lake/build`,
builds the default umbrella, checks physical positive/negative controls, runs
all 1,146 axiom queries, and checks protected files did not change during the run.
It never edits manuscript or unrelated source, sends correspondence, publishes,
commits or pushes. No GitHub release or DOI should be created.

## Repair order

First make the existing d=4 path compile; it is retained and remains useful
independently of the general extension. Then progress along this order:

1. `GeneralFourier`, `GeneralModel`, `GeneralPhases`, `GeneralWitness`,
   `GeneralCycles`, `GeneralChirp`, `GeneralScalar`, `GeneralSwap`, `GeneralGuessing`.
   Check every Fourier sign and d/sqrt(d) normalization before advancing.
2. `GeneralFunctionalCalculus`, `GeneralFirstBound`, `GeneralPolarPhases`,
   `GeneralFirstWitness`; then second coefficients/SOS/bound/witness.
   The CStarMatrix type-copy bridge and CFC continuity/evaluation APIs are
   particularly likely to need pinned-library adjustments.
3. `GeneralFiniteSpectrum`, `GeneralSupportAlgebra`, `GeneralSupportSaturation`,
   `GeneralEqualityPhases`, `GeneralSupportedPhases`, `GeneralReflectionRank`,
   `GeneralRigidity`. Verify the cancellation works on the actual support and
   does not become an unjustified full-space inverse argument.
4. `GeneralCommuting`, `GeneralSecondCommuting`: actual complete-Hilbert
   continuous-linear-map and PVM encodings, without adding finite dimension.
5. `GeneralOperational`, `GeneralBinary`, `GeneralOneInput`,
   `GeneralConsequences`, `GeneralExposure`, `GeneralBinaryWitness`,
   `GeneralOrbitConsequences`; finally both statement audits and `AxiomAudit`.

A module-by-module repair session is appropriate, but the final certification
command must build **all** claimed endpoints and audits from a clean companion
build directory. Temporarily omitting a difficult module is not completion.

## Conditions that must not be weakened

Keep arbitrary finite local dimensions and arbitrary PSD trace-one mixed states
in finite universal bounds. Keep all d-outcome PVMs, including zero effects.
Do not assume the equality phase spectrum, explicit witness, or maximality in
valid-strategy definitions. Do not add same-party commutation. For commuting
bounds, do not add a finite-dimensional or tensor-product hypothesis.

Keep the actual signed source lambda coefficients, target input `(1,none)`,
positive-character observable encoding, Bob entrywise conjugation and the
Born d^(-3) Fourier normalization. Keep equality multiplicity on the actual
reduced-state support, not an arbitrarily supplied faithful subspace. Do not
assume the reflection-rank premises in the advertised rigidity endpoint.

Keep Eve conditional states as true post-measurement sandwiches and partial
traces. Uniform observed probabilities alone are not operator privacy. The
constructed nonuniform witness does not establish a worst-case adversarial
optimizer. The private-MUB and polar-linear permutation results retain their
explicit sufficient hypotheses and are labeled conditional accordingly.

## Controls and evidence

`validation/AcceptPhysical.lean` and `AcceptGeneral.lean` must compile. The
`Reject*.lean` files must fail for a mathematical type mismatch or unsolved
proof, not because an import is missing. New controls reject a d=5 Born table
summing to two, squared coefficient norm two, and a falsely uniform swapped
table. They have not been run in Lean yet.

Compiler-free checks may be rerun independently:

```sh
python3 scripts/source_inventory.py --write
python3 scripts/static_audit.py --output logs/local_static.json
python3 scripts/test_runner.py
python3 scripts/exact_preflight.py --output logs/local_d4_exact.json
python3 scripts/first_sos_preflight.py logs/local_first_sos.json
python3 scripts/partial_commutation_preflight.py logs/local_partial_sos.json
python3 scripts/general_exact_preflight.py --help
```

The last command documents dimension-batch options; do not pass `--help` to
the two older positional-output SOS scripts. Recompute source hashes and
generated query lists after repairs, then freeze them during the formal audit.

## Review and remaining source gaps

After a successful build, an independent specialist should inspect the expanded
statements, the original manuscript labels and the entire dependency chain.
In particular review sector/floor equality cases, zero-safe functional calculus,
rank telescoping, binary on-state identities, and physical Eve interfaces.
The fact that a tactic now elaborates does not itself establish manuscript
correspondence. Do not convert `formal_endpoint_certified` to true automatically.

`COVERAGE.md` lists mathematical statements still lacking source endpoints,
including q/qa/qc set/embedding/closure/supremum assembly and selected appendix
calculations. A successful current build is not a whole-paper certification.
