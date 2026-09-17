# Cyclic Bell companion — complete d=4 source draft, unverified

**Source scripts are supplied for both d=4 end-to-end counterexamples. No Lean
compiler was run in this continuation. None of the new declarations is certified.**
This is an offline-checking handoff, not a claim that the entire paper has been
formalized or that the current scripts will compile without repair.

The principal source candidates are
`CyclicBell.D4.first_counterexample`, `CyclicBell.D4.second_counterexample`, and
`CyclicBell.D4.main_d4_counterexamples`. They connect arbitrary-finite-dimension
mixed-state/PVM upper bounds to explicit C⁴⊗C⁴ witnesses, actual Born probabilities,
uniform marginals, and a legal one-dimensional Eve guessing strategy.

Start with [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md),
[STATEMENT_CONTRACT.md](STATEMENT_CONTRACT.md), and [COVERAGE.md](COVERAGE.md).
The new first-family polynomial SOS is explained in
[FIRST_FAMILY_SOS.md](FIRST_FAMILY_SOS.md). Offline checking and repair instructions
are in [OFFLINE_HANDOFF.md](OFFLINE_HANDOFF.md). Axiom-query status is in
[AXIOMS.md](AXIOMS.md).

## One build-and-audit command

With this folder beside the matching canonical `main.tex`, and Lean/Lake, Git,
and Python 3.10+ available:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

The command verifies the source/compiler identities and exact dependency pins,
fetches missing locked dependencies and their cache, deletes only this project's
`.lake/build`, builds every candidate/audit module, runs positive and intentionally
failing controls, queries every named declaration's axioms, and checks source
stability. It does not edit the manuscript, reset unrelated work, change branches,
commit, push, contact anyone, or publish a release.

Bootstrap needs network access unless the compiler, exact dependencies, and cache
are already available. After prefetching them, omit `--bootstrap` for local
checking without the bootstrap downloads. The zip contains source and dependency
locks, not Lean binaries or vendored Mathlib build artifacts.

**This command has not been executed on the continuation's Lean source.** The
old failed environment attempt is retained under `history/pilot/logs/`, not
presented as a build of this version. A successful future command will produce
actual receipts under `logs/runs/`; independent statement review remains required.

## What changed from the pilot

The first-family universal proof now has a d=4 polynomial sum-of-squares route
that requires no polar decomposition or functional calculus. The physical
upper-bound import closure contains no concrete witness module. Both full PVM
families, exponential-phase bridges, source coefficient normalization, Fourier
compression, attainment, physical target tables, mixed-state positivity, and
trivial-Eve partial-trace bridges have proof scripts.

There are **321 named theorem candidates**, 113 definitions, six abbreviations,
three structures, and **27 expanded statement examples**. The standard build
reaches all **20 Lean files**, including **443 generated axiom queries**. These
counts describe source, not accepted proofs. The inventory is generated in
`reference/source_inventory.json` and checked against the query file.

## What actually ran

The compiler-free checks passed: 392 exact witness/coefficient/second-SOS checks;
12 exact first-SOS checks; eight additional checks of the first SOS with only
U/B_y commutation; 17 reporting/scanner tests; and the source/import/lock audit.
The word-algebra implementation for the weaker-commutation check is distinct,
but shares coefficient arithmetic and was written by the same assistant.
It is not an independent-agent or Lean audit.

```sh
python3 scripts/exact_preflight.py --output logs/continuation_exact_preflight.json
python3 scripts/first_sos_preflight.py logs/first_sos_preflight.json
python3 scripts/partial_commutation_preflight.py logs/partial_commutation_preflight.json
python3 scripts/static_audit.py --output logs/continuation_static_audit.json
python3 scripts/test_runner.py
```

Every supplementary receipt has `kernel_checked: false`. No numerical result,
Python verdict, or imported certificate is a premise of a Lean endpoint.

## Scope and provenance

The canonical manuscript Git blob is
`bbd0667c934d5a34dd9c8ced50df91515cb1308c`. Lean is pinned to 4.19.0 and Mathlib to
`c44e0c8ee63ca166450922a373c7409c5d26b00b`; every transitive dependency revision
is locked in `lake-manifest.json`.

All-dimensional cycle/autocorrelation results, arbitrary-Hilbert-space qc
statements, support multiplicities and cancellation, robust statements, and
optimal adversarial guessing over all realizations remain outside this draft.
The existing qubit project and published manuscript were not modified.
Checkpoints are local on `main`; there is no remote push receipt. The preceding
pilot's GitHub write was denied with HTTP 403. Historical status documents are
preserved under `history/pilot/` and do not describe current source coverage.
