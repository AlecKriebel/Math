# Cyclic Bell Lean companion — extended uncompiled source

**Status: SOURCE CANDIDATES, NOT KERNEL-CHECKED.**

This continues the 14 September 2026 d=4 source package toward the mathematics
of “Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell
Inequalities.” It adds all-dimensional cyclic bounds and physical counterexamples,
the full written finite-dimensional support-rigidity chain, separate
arbitrary-Hilbert commuting upper bounds, and operational/low-setting results.
It is not a formalization of every paper claim, and no Lean proof has been
accepted in this cloud continuation.

Start with [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md), then
[COVERAGE.md](COVERAGE.md), [GENERAL_STATEMENT_CONTRACT.md](GENERAL_STATEMENT_CONTRACT.md)
and [OFFLINE_HANDOFF.md](OFFLINE_HANDOFF.md).
The original [STATEMENT_CONTRACT.md](STATEMENT_CONTRACT.md) preserves the d=4
pilot's physical conventions and target milestones.

## Reproducible formal check, to run offline

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

The source uses Lean 4.19.0 and the exact Mathlib/dependency revisions in the
lockfiles. The default build reaches all 55 Lean source files, 50 expanded
statement examples, and 1,146 generated axiom queries. These are pending queries,
not audit output. There are 851 explicitly named theorem candidates; the count
measures source scope, not correctness or successful proof checking.

## What ran in the cloud

3,040 distinct new exact-arithmetic assertions and 38 negative controls passed
in dimension batches covering d=2,...,12. The retained d=4 392-check suite,
12-check first SOS suite, 8-check alternate word-reduction suite, and 26 Python
audit-machinery tests were rerun successfully. Static import, pin and declaration
checks passed. None of these tests invokes Lean or proves a universal theorem.
No exact certificate is imported as a substitute for proof evidence.

## Source organization

`CyclicBell/General*.lean` is the new general extension. The prior d=4 modules
remain available and are included in the standard umbrella. Universal-bound
modules are separated from witness modules. `GeneralStatements.lean` expands
the actual physical and mathematical endpoint contracts.

[ALL_DIMENSION_ROUTES.md](ALL_DIMENSION_ROUTES.md) explains the continuous-factor
upper-bound route and the support chain. [FIRST_FAMILY_SOS.md](FIRST_FAMILY_SOS.md)
retains the separate polynomial d=4 SOS route. Historical d=4 documentation and
old blocked build attempts are preserved under `history/` and their original
logs; they must not be read as current successful certification.

No manuscript, existing qubit project, release, DOI, or correspondence was
modified or created. Local checkpoints are on `main`. No remote push occurred;
use the separately supplied patch after checking local work for conflicts.
