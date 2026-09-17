# Axiom audit — pending, no executed Lean reports

**Actual Lean invocations in this continuation: 0.**
**Actual successful clean Lean builds: 0.**
**Actual endpoint axiom reports: 0.**

`CyclicBell/AxiomAudit.lean` contains **1,146 generated queries**, not output.
They cover all 851 explicitly named theorem candidates plus definitions,
abbreviations, structures, proof-bearing constructors and two named spectrum
instances found by the source inventory. Anonymous expanded-statement examples
are checked by their importing build, not counted as named axiom reports.

Every explicitly named declaration is listed in
`reference/expected_theorems.json` (historical filename, now broader than theorems).
`reference/source_inventory.json` associates names with source locations.
`CyclicBell.lean` reaches `Statements`, `GeneralStatements`, and `AxiomAudit`.
The import graph has 55 source files and excludes no claimed candidate module.

## Allowed transitive axioms

Only subsets of these standard foundations are permitted:

```text
propext
Classical.choice
Quot.sound
```

There are no executed dependency reports from which to assert that any present
endpoint meets this requirement. Absence of forbidden source tokens is not
absence of transitive unproved assumptions. The offline runner parses actual
`#print axioms` output and rejects missing reports, duplicate reports, custom
axioms, `sorryAx`, and native-evaluation trust axioms such as `Lean.ofReduceBool`.

No sorry/admit/custom mathematical axiom/native_decide/unsafe proof escape was
found by the source scanner. That scanner masks comments and strings and checks
approved compiler options, but it is not a Lean parser or kernel. All imports
outside this companion are Mathlib modules at the pinned revision.

## Run and inspect

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Actual run receipts will be written under `logs/runs/<timestamp>/`. They must
include the successful clean build, controls, axiom reports and protected-input
fingerprints. The script deliberately leaves `formal_endpoint_certified=false`
even after kernel acceptance, pending independent manuscript correspondence
review. Never edit a cloud receipt to imply a run happened.

Lean/compiler/runtime and the provenance of dependency build caches remain
ordinary software trust assumptions. This command rebuilds the companion, not
the compiler or all third-party software from bootstrap sources.

Historical logs and d=4 reports remain clearly historical. No old blocked run
or Python success has been substituted for a new successful formal audit.
