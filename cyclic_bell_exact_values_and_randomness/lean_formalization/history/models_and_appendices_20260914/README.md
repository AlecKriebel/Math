# Cyclic Bell Lean companion — model-value source extension

**UNCOMPILED SOURCE. No Lean kernel check has run; no formal endpoint is certified.**
This package is intended for offline compilation, repair and independent
statement review. The proof scripts may require substantive changes; source
inventory and exact finite tests do not establish their correctness.

The new extension writes the literal finite, closure and commuting-model value
suprema for both cyclic families in every d>=2, explicit finite-to-commuting
physical embeddings, binary three-model values and actual finite-purification
privacy/setting minimality, and the nonunit weighted-cycle characteristic
polynomial. Earlier d4 and all-dimensional candidates are retained unchanged.

## Start here

- [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md): strongest candidates and the exact remaining gaps.
- [COVERAGE.md](COVERAGE.md): manuscript labels and candidate theorem names.
- [OFFLINE_HANDOFF.md](OFFLINE_HANDOFF.md): installation, repair order and controls.
- [MODEL_VALUE_SELF_AUDIT.md](MODEL_VALUE_SELF_AUDIT.md): physical/model correspondence and self-audit findings.
- [STATEMENT_CONTRACT.md](STATEMENT_CONTRACT.md), [GENERAL_STATEMENT_CONTRACT.md](GENERAL_STATEMENT_CONTRACT.md), [MODEL_VALUE_CONTRACT.md](MODEL_VALUE_CONTRACT.md): frozen and extended statement contracts.

## One offline command

From this directory, beside the matching canonical manuscript:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

The pins are Lean 4.19.0 and Mathlib
`c44e0c8ee63ca166450922a373c7409c5d26b00b`; all nine dependencies are locked.
No compiler or compiled dependency artifact is shipped. Omit `--bootstrap`
when the exact dependencies and build cache are already available.

`CyclicBell.lean` is the default target. It imports all 66 source/audit files,
including `ModelValueStatements` and 1,332 pending axiom queries. Fifteen
separate offline controls comprise three positive files and twelve deliberately
false files. False controls are not production imports and must fail for genuine
proof errors, not missing imports or unrecognized APIs.

## Status

Written: 987 named theorem candidates and 75 expanded examples. Executed:
compiler-free exact arithmetic, static source/import/pin checks and reporting
machinery tests. **Zero Lean invocations and zero actual axiom reports.**
Source-writing completion of this targeted extension is not whole-paper
completion; selected appendix and general model-inclusion claims remain open
in this source package, as listed in COVERAGE.md.

All earlier mathematical modules and dependency pins are preserved. Work was
checkpointed on a new local `main` checkout restored from the archive. There
was no remote push, manuscript/qubit edit, correspondence, release, or DOI.
