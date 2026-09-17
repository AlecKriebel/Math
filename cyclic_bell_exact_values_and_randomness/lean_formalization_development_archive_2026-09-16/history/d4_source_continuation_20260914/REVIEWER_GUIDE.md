# Reviewer guide

## What this package is

A complete **source draft for the two d=4 finite-dimensional counterexamples**,
prepared for offline Lean checking. **No theorem in this continuation has been
kernel-checked.** Every claimed endpoint has a proof script, but the scripts
may require elaboration repairs, rewritten tactic proofs, or additional helper
lemmas. There is no claim that only cosmetic fixes remain.

The strongest written endpoints are `CyclicBell.D4.first_counterexample`,
`second_counterexample`, and `main_d4_counterexamples`. They are substantially
stronger than the old target-only pilot: the universal bounds, complete
measurement families, source conventions, attainment, and physical randomness
obstruction all now have source chains. Whole-paper claims remain excluded.

## The fastest mathematical inspection

Read `Model.lean` first. `State nA nB` is an actual complex PSD trace-one matrix;
`PVM n` has four positive orthogonal idempotents summing to identity; `Strategy`
contains only state and measurements. The dimensions are parameters. There is
no score, maximality, table, or equality-phase hypothesis in strategy validity.
`born` is the usual trace formula, and `TraceCalculus.lean` supplies generic
nonnegativity/normalization scripts.

Read the two functional definitions in `Functionals.lean`. The first augmented
functional has no factor 1/4. The second uses the source's actual trigonometric
`sourceLambda`, including the integer exponent (-1)^(-1) at l=0, and a positive
Fourier exponent. Target settings are the manuscript's zero-based Alice 1,
Bob 4. Outcomes are Fin 4.

Next inspect `PhysicalBounds.lean` and the proof route in `FIRST_FAMILY_SOS.md`.
The arbitrary-dimensional first bound is supplied by an exact polynomial SOS,
not by assuming the witness spectrum or by leaving the polar bound as a
hypothesis. Both bounds handle arbitrary mixed states directly through positive
trace expectations. The static audit checks that this entire import closure
contains no concrete-witness module. The second source SOS retains its 1/8
prefactor; its coefficient normalization is proved from `sourceLambda`.

For the witness, `ScalarData.lean` defines ζ as the actual exp(πi/8), rather than
an unspecified algebraic root. `D4.lean` contains Phi4, its 1/2 amplitudes,
Fourier vectors, the literal final-two permutation, and the designated PVMs.
`Phases.lean` identifies those coordinates with the manuscript's exponent list.
`Cycle4.lean` constructs the other rank-one PVMs from unimodular cycle-prefix
bases and proves their observable encodings. `Witness.lean` supplies all Alice
and Bob settings and fixes conjugation versus transpose versus adjoint.

`Attainment.lean` derives Fourier compression with the actual source coefficients
and D_l, evaluates the first score to 2/sin(π/8)+1 and the second to 5, and gives
second-residual annihilation scripts. It does not call the universal bounds.
The target PVM pair in both strategies is literally the pair used by the earlier
Born calculation, not an independently asserted table.

Finally read `Endpoints.lean`. `IsFirstMaximizer` compares the witness against
EVERY finite-dimensional competitor. It is a proved conclusion of the separate
bound/attainment chains, not a premise. The designated Born table is 1/32 or
3/32 by parity, has total mass 1 and uniform 1/4 marginals, and has maximum
entry 3/32 at (0,1). `Guessing.lean` constructs a complete positive scalar-matrix
POVM on C¹ that always guesses (0,1), and connects its conditional states to
an actual sandwich and partial trace. The AB witness is pure, so this really
is a trivial purifying Eve. No supremum over all realizations is optimized.

## Statement validation and controls

`Statements.lean` contains 27 expanded examples, including universal bounds
written out in density/projector terms, all witness measurements, actual
coefficient and phase conventions, Born tables, and the Eve bridge. It is a
separate self-audit source module, not a report from an independent agent.

`Regression.lean` checks the canonical-versus-swapped target, wrong Bob
conjugation/adjoint, and extra normalization factor. It proves true negative
control statements in the standard build. Five deliberately false files under
`validation/Reject*.lean` must fail with recognized proof errors; a positive
control exercises both complete endpoints. None of those Lean controls has yet
been executed.

## What actually passed, and what did not run

Compiler-free checks: 392 exact witness/coefficient/second-SOS checks, 12 first-SOS
checks, eight weaker-commutation first-SOS checks, 17 reporting/scanner tests,
and the import/lock/declaration audit. All 20 Lean files are in the standard
import closure. All 443 named declarations have axiom queries. A delimiter
check caught and repaired two extra parentheses during source inspection.
These checks are not Lean parsing, type checking, or proof verification.

No Lean command, clean Lean rebuild, actual axiom report, or independent-agent
review occurred in this continuation. The old blocked build log under
`history/pilot/` belongs to the earlier smaller source. Do not cite it as a
build of this version. The new receipt is `logs/EXECUTION_STATUS.json` and
`CONTINUATION_REPORT.json`, both explicitly unverified.

## Reproduce and assess

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

The precise repair workflow and invariants are in `OFFLINE_HANDOFF.md`.
The command is intended to be run, not asserted to pass. After any source
repairs, regenerate the declaration queries using
`python3 scripts/source_inventory.py --write`, then run the full audit again.
Do not remove a failed endpoint, weaken its hypotheses, or replace its proof
with a placeholder to obtain a green build.

The immediate remaining work is genuine elaboration/kernel checking and any
repairs it reveals, followed by independent statement correspondence review.
Continuing is worthwhile on demonstrated evidence: both witness evaluations and
both SOS mechanisms survive exact algebraic checks, and every required d=4
physical bridge now has a source implementation. All-dimensional, support-level,
and arbitrary-Hilbert-space claims are expressly outside this handoff.
