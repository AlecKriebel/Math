# Reviewer guide — settings and audit continuation

**No Lean source in this package has been certified here.** The new results are
proof-script candidates; they may need substantial repair. The earlier d=4,
all-dimensional, rigidity, commuting/model and adversarial candidates remain
uncompiled. No independent agent reviewed this work.

## New focused extension

Read `SETTINGS_STATEMENT_CONTRACT.md` alongside manuscript `app:settings` and
`eq:standard-tables`. The main namespace is `CyclicBell.General`.

| Source module | What to inspect |
|---|---|
| `GeneralPhaseTables.lean` | Actual phase PVMs, Bob outcome inversion, rank-one trace Born reduction, division-free geometric identity, normalization and uniform marginals. |
| `GeneralPhaseBounds.lean` | Literal delta matrix, exact folded-denominator lower bound, all-entry upper bound plus explicit attaining pairs, and the strict standard-table gap for d>=2. |
| `GeneralAnchoredTables.lean` | Third input actually appended without changing the original tables; perfect matching; cross maximum and nonuniformity for d>=3; uniform qubit exception. |
| `GeneralPhaseEntropy.lean` | Peak-to-observed-entropy connection and the actual difference-limit formulation of o(1). No conditional Eve entropy is claimed. |
| `PhaseTableStatements.lean` | Eight expanded statement examples, imported by the normal build. |

The principal candidates are `standard_tables_nonuniform`,
`anchored_cross_nonuniform`, `anchored_qubit_cross_uniform`, and
`standard_entropy_asymptotic`. Their new import closure deliberately does not
use the Bell upper bounds, scalar extremum, rigidity, or cyclic maximizer
endpoints. The full final audit nevertheless includes every accumulated module.

## Audit-runner defect fixed

Read `SETTINGS_SELF_AUDIT.md` and `logs/phase_incoming_runner_defects.json`.
The previous expected-failure handler could accept simulated process kills or
resource exhaustion if a proof-error string was also present. The repaired
runner rejects these, preserves logs/exit codes, and still accepts an ordinary
exit-1 proof rejection. The regression tests use mocks, not Lean executions.

## Retained companion

The original `STATEMENT_CONTRACT.md`, `GENERAL_STATEMENT_CONTRACT.md`,
`MODEL_VALUE_CONTRACT.md`, and `ADVERSARIAL_STATEMENT_CONTRACT.md` still govern
physical validity, arbitrary dimensions, source coefficients, actual reduced
supports, Hilbert conventions and guessing-model domains. `COVERAGE.md` and
`reference/paper_claim_ledger.json` map all written claims. The previous guide
is preserved in `history/adversarial_source_snapshot_20260914/`.

## Unfinished obligations

Every claimed theorem needs actual elaboration and kernel checking; every
transitive axiom set needs inspection. A separate specialist must validate the
accepted statements against the manuscript. This pass does not establish that
all old or new mathematics is correct. Selected old delicate proofs were only
spot-checked and no new mathematical defect was established in that sample.

Remaining unwritten source: the general Qqa-subset-Qqc/closedness construction,
and the complete source-Z/coefficient/polar strategy identification with PVM
validity. Intermediate canonical-polar/von-Neumann or Toeplitz/SVD identities
replaced by other routes are not claimed individually checked. Open maximizing-
face or adversarial-optimizer questions are not claimed solved.

## Reproduce

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

See `OFFLINE_HANDOFF.md` for safe installation and repair order. A successful
script result is still conditional on independent manuscript correspondence.
