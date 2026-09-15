# Offline checking and repair handoff

## Installation location and safe application

The full zip places files under
`cyclic_bell_exact_values_and_randomness/lean_formalization/`. Copy that folder
into the Math checkout without touching `main.tex` or the qubit project.
A full-addition patch is appropriate only when this directory does not yet
exist. A pilot-to-current delta patch is supplied for the exact incoming pilot.
Run `git apply --check <patch>` before applying a patch, and preserve any local
changes that are not part of this source snapshot.

The package contains no compiler and no vendored Mathlib artifacts. Lean is
4.19.0, compiler commit `6caaee842e9495688c1567e78c0e68dbb96942aa`. Mathlib and all
transitive dependency commits are fixed in `lake-manifest.json`. Bootstrap
requires network access for missing pinned dependencies and the cache. With
those already present, omit `--bootstrap`.

## The one complete command

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

The command performs a clean rebuild of the companion, not a bootstrap rebuild
of Lean and all of Mathlib. It validates the canonical manuscript against its
recorded Git blob and SHA-256; refuses to reset dirty or differently pinned
dependencies; removes only this project's `.lake/build`; builds the standard
library; runs positive and five false controls; executes all axiom queries;
and rechecks protected source/dependency fingerprints. It writes receipts,
not commits or releases.

A successful result says `candidate_kernel_checks_passed_statement_review_required`.
It is not whole-paper certification. A blocked or failed result must not be
relabelled as partial kernel success. In this handoff **no Lean invocation has
been performed at all**.

## Repair order

Start with the first actual Lean error. The logical order is: Model and
Functionals; MatrixAlgebra and ScalarData; Fourier4 and the two SOS modules;
PhysicalBounds; D4 and Phases; Cycle4 and Witness; TraceCalculus and Attainment;
Guessing and Endpoints; Regression, Statements, and AxiomAudit.

The likely sensitivity points are finite-sum rewrites and scalar coercions,
PosSemidef and matrix API spelling at the pinned revision, matrix-expression
normalization, finite-index reduction, and exact real/complex arithmetic tactic
performance. These are risks inferred from the source, not observed compiler
errors. More substantive helper-proof repairs may also be necessary; no claim
is made that the source will compile after merely fixing syntax.

For matrix algebra, preserve the exact identities in `FIRST_FAMILY_SOS.md`.
Break a brittle tactic proof into explicit intermediate equalities when needed.
Do not introduce same-party commutation. `FirstSOS` requires unitarity of A,U,B_y
and U/B_y commutation only. `SecondSOS` uses Fourier orthogonality and unitarity
with the actual source coefficient normalization. The universal physical model
must retain arbitrary local dimensions and arbitrary PSD trace-one mixed states.

After editing source, refresh the inventory and run all checks:

```sh
python3 scripts/source_inventory.py --write
python3 scripts/static_audit.py --output logs/continuation_static_audit.json
python3 scripts/test_runner.py
python3 scripts/check.py --manuscript ../main.tex
```

The query inventory includes every named source declaration, not merely a
handful of endpoint names. Static counts and hashes are metadata, not theorem
verification. The false control files belong outside the production import
graph; do not make their failed proofs part of the normal library.

## Invariants not to weaken

The State/PVM/Strategy definitions must not gain a Bell bound, attainment, target
table, eigenphase restriction, or chosen-witness condition. Competitors must not
be limited to 4x4. The score definitions must keep their coefficients and
normalizations. A0/A1/B_y tensor placement must not be replaced by commuting
all same-party matrices. Source coefficients must not become arbitrary
normalized variables at the endpoint. Phase roots must remain the actual
complex exponential embedding. The designated table must stay a derived Born
formula. The trivial-Eve success must not be claimed optimal across all
realizations.

No `sorry`, `admit`, `sorryAx`, custom mathematical axiom, `native_decide`, or
unsafe proof substitution is allowed. Do not omit a troublesome endpoint or
audit import from the standard build to make it pass.

## Independent review after a genuine clean pass

A different reviewer should compare `STATEMENT_CONTRACT.md` and the expanded
statements with the pinned manuscript, inspect the two independent bound and
attainment chains, verify the mixed-state and Eve bridges, and examine all
actual axiom reports. The explicit witness removes concern about an empty
physical model. Zero-dimensional quantifiers in the stronger algebraic bound
are harmless because no trace-one zero-dimensional State exists; arbitrary
positive dimensions remain included.

Record the exact source hashes, successful run id, remaining exclusions, and
reviewer's conclusions. No autonomous contact, manuscript publication change,
GitHub release, or DOI creation is part of this checking workflow.
