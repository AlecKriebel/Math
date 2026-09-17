# Axiom audit status

**No actual `#print axioms` output was produced.** Lean was not available and
no Lean process was started. The axiom inventory below is a request inventory,
not a successful dependency report. There is no evidence here that any named
endpoint has passed a kernel check.

`CyclicBell/AxiomAudit.lean` requests reports for all 34 authored theorem
candidates and five proof-bearing constructors:

- `CyclicBell.pvmOfBasis`, `CyclicBell.stateOfPure`;
- `CyclicBell.D4.aliceTargetPVM`, `bobTargetPVM`, `targetState`.

The complete 39-name machine-readable inventory is
`reference/expected_theorems.json`. The audit file and expanded statement checks
are imported by the standard `CyclicBell` target.

## Allowed foundations in a future executed report

Only subsets of the standard axioms `propext`, `Classical.choice`, and
`Quot.sound` are accepted by `scripts/check.py`. This is an **allowlist**, not
an assertion that these are the actual transitive dependencies of the current
source. Missing, duplicate, or unexpected reports are failures. `sorryAx`,
custom axioms, and compiler-trust axioms are not allowed.

The source scanner found no prohibited code tokens in the candidate library.
It also checks the standard import graph and resource-only compiler options.
Static scanning does not prove dependency safety or replace type checking.
The ordinary `decide` in the finite permutation candidate is not
`native_decide`; its proof would still have to be accepted by the Lean kernel.

## Build/evidence trust boundary

The planned clean build removes this project's `.lake/build`, not all upstream
Mathlib caches. All dependency Git commits are locked and their tracked source
cleanliness is checked. A successful future run would rely on the pinned Lean
binary/kernel/runtime and imported dependency artifacts, as ordinary Lean
projects do; it would not bootstrap or independently rebuild every component
of the trusted computing base.

The Python cyclotomic/SOS computation and Python audit-parser tests are
supplementary, explicitly carry `kernel_checked: false`, and are not imported
as theorem evidence. No external solver verdict is accepted by any Lean theorem.

Current actual run evidence: `logs/build_attempt.log` and `logs/latest_run.json`,
with zero Lean commands and status `blocked_or_failed_NOT_CERTIFIED`.
