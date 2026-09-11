> **Historical cloud-stage document.** Statements below about missing compilation or unfinished targets describe the incoming archive. Current local verification and the precise certified scope are recorded in [CERTIFICATION.md](CERTIFICATION.md); this document is retained as research provenance.

# End-to-end Lean source draft — 10 September 2026

**Status: source written; NOT compiled or kernel-verified.**

The user requested the remaining Lean source first and deferred the compiler run.
No Lean or Lake command was run during this source-writing phase. No successful
build, theorem verification, or formal-completion certification is claimed.

## What changed

The source now contains an end-to-end draft for the arbitrary-finite-output,
two-input convexified equality, the minimum-setting conclusion, the explicit
3×2 separation, and Appendix B's strengthened physical attainment. The final
Assembly declarations do not take `UniversalTwoInputEquality`, a residual
closure oracle, or the main theorem as arguments.

The inventory contains **58 mathematical modules**, excluding the aggregate
`Bell.lean` and generated `Bell/Audit.lean`. It contains **681 theorem/lemma
proof-attempt declarations**: 672 public declarations and 9 private helpers.
There are **10,375 lines in those mathematical modules**. These are static text
counts, not declarations accepted by Lean.

Compared with the incoming continuation archive, 34 mathematical modules were
added. Of the 24 incoming mathematical modules, 21 are byte-identical; Scalars
and Targets have updated scope comments, and UphillDirection has a pinned-API
finrank proof edit. The complete incoming archive is retained byte-for-byte in
`preservation/input_before_source_completion.zip`.

## Main declarations

`Bell/Assembly.lean` now contains source attempts for:

- `two_input_convex_equality (AO BO : Fin 2 → ℕ)`;
- `universal_two_input_equality : UniversalTwoInputEquality`;
- `at_most_two_input_equality` and `main_claims : MainClaims`;
- `minimum_inputs`, `minimum_inputs_attained`, and `no_two_input_strict_separation`.

`Bell/StrengthenedWitness.lean` contains the explicit complex-qubit construction,
`strengthened_attainment : StrengthenedAttainment`, and
`main_claims_with_strengthening : MainClaims ∧ StrengthenedAttainment`.

`Bell/SimulationCorollaries.lean` explicitly exposes a finite mixture of complete
projective strategies. It does not replace convexified equality by raw equality.

## Proof architecture now written

The source derives compact strategy/hull sets; an extreme maximizing behavior;
a full-Schmidt-rank pure realization of any nonlocal behavior; independent,
rank-one active effects; the common-span dimension bound; and binary/ternary
support reduction with exact input/output recoding. The independent binary-PVM
case is settled by a balanced three-dimensional cone, sparse extreme circuits,
and actual qubit purification. General binary-POVM simulation is also a final
corollary of the arbitrary-output equality.

For genuine residual frames, the source constructs a local physical chart,
proves the six-constraint Jacobian surjective by an explicit right inverse,
derives Lagrange stationarity, obtains strict multipliers from deterministic
physical score gaps, and assembles the rank-zero, rank-one and rank-at-least-two
cases. The high-rank argument uses an exact finite score identity and a C¹
implicit feasible curve instead of differentiating matrix inverses twice.

This is an alternative source proof route for the principal results, not a
line-for-line formal transcription of every independently stated appendix lemma
or explanatory remark. In particular, separate finite-POVM SDP duality is not
needed by the new multiplier-positivity route.

## Executed checks — narrow scope

The new exact checker passed **69 symbolic identity checks**, **474 rational
regression checks**, and one negative control that rejects omitting Bob's
transpose. Matrix-valued checks are counted as checks, not as a inflated count
of every scalar entry. The checks cover Pauli/trace/Born identities, frame
probabilities, derivative formulas and seed identities, exact finite gap
residuals, cone splitting, physical right-inverse fixtures, whitening, and the
strengthened strategy's value.

A Python dependency-log parser passed 10 unit tests using **mock text**. Those
are tests of the parser, not actual Lean dependency reports. The generated
future axiom audit queries all 672 public theorem declarations; private helper
dependencies are traversed through their public clients.

The source-token scan and import graph checks passed. All local imports resolve,
the import graph is acyclic, and the aggregate imports all mathematical modules.
Selected top-level declaration headers match the intended unconditional source
interfaces. No `sorry`, `admit`, custom `axiom`, or prohibited proof-escape token
was detected outside comments/strings by the static scan.

**None of these checks establishes Lean elaboration, proof correctness, the
analytic claims, or faithful source-to-manuscript correspondence.** Historical
reports elsewhere in the package are retained as provenance; they are not fresh
verification of the expanded source.

## What remains unverified

The entire expanded draft must be elaborated by the pinned compiler. Large
proofs involving finite dependent alphabets, matrix coercions, spectral data,
continuous linear maps, and implicit-function APIs can still contain errors.
Some proof tactics may fail, and a compiler/referee audit may expose mathematical
issues as well as API mismatches. It would be premature to call the formalization
complete or publication-ready.

There is no deliberately unfilled main-theorem premise in the final interfaces,
but absence of a placeholder is NOT evidence that the bodies work. The first
unverified task is the actual build, followed by repair and the dependency audit.

## Later run

With Lean 4.19.0 available and the pinned Mathlib dependency obtainable:

```bash
bash scripts/check.sh --bootstrap
```

The wrapper builds all imported source, invokes Lean on `Bell/Audit.lean`, and
fails if a required public theorem lacks a recognized dependency report or uses
an unapproved axiom. Its reports are reset at the start of a run. A successful
future run would check the formal statements; a separate review of the model and
statement correspondence remains necessary.

No repository files, branches, pull requests, or remote workflows were changed
in this source-writing phase.
