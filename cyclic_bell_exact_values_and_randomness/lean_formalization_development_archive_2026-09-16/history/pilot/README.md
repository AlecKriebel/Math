# Cyclic Bell Lean companion — unverified pilot

**No Lean kernel check completed in this cloud session. None of endpoints A–F
is certified. This is a preserved source-candidate package, not a verification
certificate for the paper or either Bell counterexample.**

The canonical manuscript is `../main.tex`, Git blob
`bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
The attempted remote checkpoint returned HTTP 403. These files were preserved
in a new local repository on `main`, not pushed to AlecKriebel/Math.

Start with [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md),
[STATEMENT_CONTRACT.md](STATEMENT_CONTRACT.md), and [COVERAGE.md](COVERAGE.md).
[AXIOMS.md](AXIOMS.md) explicitly distinguishes requested reports from executed
reports. The exact source and evidence hashes are in `SOURCE_HASHES.sha256`.

## Reproduce the attempted build and audit

Place this folder beside the matching canonical `main.tex`, with Lean/Lake,
Git, and Python 3.10 or later available, and run from this folder:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

This fetches exact locked dependency commits (without resetting existing
modifications), checks source/compiler identities, removes only this project's
`.lake/build`, builds the standard target including its statement/axiom audits,
runs positive and intentionally false physical controls, and rejects unapproved
or missing axiom reports. It logs all executed commands and fingerprints.
It never changes branches, edits the manuscript, commits, or pushes.

The command was actually attempted in the cloud. It exited 2 **before any Lean
command ran**, because Lean/Lake was unavailable. See `logs/build_attempt.log`
and `logs/latest_run.json`. A local run may also reveal elaboration or proof
errors: the candidates have not yet passed a compiler. The runner does not
turn a successful candidate build into whole-paper certification.

To run only the supplementary exact arithmetic and reporting tests:

```sh
python3 scripts/exact_preflight.py --output logs/exact_preflight.json
python3 scripts/static_audit.py --output logs/static_audit.json
python3 scripts/test_runner.py
```

These passed in the cloud: 392 exact-arithmetic checks, static checks for six
candidate/import/audit modules, and ten reporting-tool tests. **None invokes
Lean or establishes a formal theorem.**

## What the source candidates contain

`CyclicBell/Model.lean` defines arbitrary-coordinate-dimension states, PVMs,
tensor products, observable encodings, and Born probabilities. It includes
proof candidates for the rank-one Born reduction and the pure/mixed trace
bridge. Strategy validity does not include a Bell value or a target table.

`CyclicBell/D4.lean` gives the target-only four-dimensional construction with
the literal final-two permutation, explicit Fourier bases, projectors, Phi4,
observable encodings, and a candidate derivation of the nonuniform Born table.
The largest combined target-only candidate is
`CyclicBell.D4.target_measurement_package`.

`CyclicBell/Functionals.lean` defines both actual manuscript functionals and
states their universal target propositions. **It does not prove the bounds.**

There are 34 theorem candidates and 39 axiom-report requests, counting five
proof-bearing constructors. All are included in the default build. The
unfinished routes in `experiments/` are outside that import graph.

## Checkpoint scope

Completed: source/statement audit, source candidates, exact Python preflight,
reporting checks, and local preservation.

Not completed: an executed Lean proof, the exponential-phase bridge, the full
Bell witness in Lean, either universal Bell bound, formal attainment, or the
scalar-maximality counterexample. No independent-agent audit was available.
