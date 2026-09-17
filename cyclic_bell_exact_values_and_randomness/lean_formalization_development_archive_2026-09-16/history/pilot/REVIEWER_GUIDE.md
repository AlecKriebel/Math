# Reviewer guide

## Status at a glance

**Strongest completed formal endpoint: none.** The cloud session could read
GitHub but its checkpoint write returned HTTP 403, and no usable Lean compiler
was available. No successful Lean check, clean rebuild, axiom output, or
independent-agent audit is claimed. This package is for reviewing and continuing
a precisely scoped pilot, not citing the paper as formally verified.

The strongest combined source candidate is
`CyclicBell.D4.target_measurement_package`. It concerns only the designated
measurements on a normalized four-dimensional maximally entangled state. Even
if compiled, it would not on its own prove a scalar-maximality counterexample.

## Read these files first

`STATEMENT_CONTRACT.md` fixes the physical model, dimensions, conventions,
functional normalization, source hashes, target labels, and endpoints A–F.
`COVERAGE.md` maps individual claims to source candidates and identifies all
unfinished components. `AXIOMS.md` records the absence of executed dependency
reports. Do not substitute a declaration count for proof coverage.

In `CyclicBell/Model.lean`, inspect `State`, `PVM`, `Strategy`, `tensor`,
`observable`, `born`, and `pureBorn`. The dimensions are parameters nA,nB.
Validity requires only physical positivity, trace normalization, PVM
orthogonality/idempotence/completeness. It contains no Bell bound, table, or
maximality assumption. The general candidate `pureBorn_projectors` is the
bridge from Born's rule to an amplitude square. `pureBorn_eq_born` connects
the vector expression to the positive trace-one density model.

In `CyclicBell/D4.lean`, inspect `phi`, `u`, `v`, `q`, `kappa`,
`swappedWeights`, and the two PVM constructors. `kappa_values` fixes
(0,1,3,2), `weights_are_final_swap` connects it to the algebraic root labels,
and `q_recurrence` connects it to the target basis. The state amplitude is 1/2,
not 1/4. The candidate observable-encoding theorems matter: the parity table
alone cannot expose a mistaken Bob transpose/outcome convention.

`targetBorn` is defined using the general physical Born rule, independently of
`table`. `targetBorn_eq_table` and `mixed_targetBorn_eq_table` attempt to prove
that the resulting probabilities are 1/32 for even a+b and 3/32 for odd a+b.
The marginals, total mass, largest entry, fixed-pair success, and nonuniformity
are separate declarations. No guessed pair is claimed to optimize Eve across
all realizations.

`CyclicBell/Functionals.lean` records the actual first and second functionals.
`FirstUpperBound` and `SecondUpperBound` are **unproved propositions**, not
axioms or fields in the strategy model. The definitions use arbitrary positive
local dimensions and mixed states in their intended universal statements.

## What actually ran

The standard-library-only `scripts/exact_preflight.py` passed 392 exact checks
using Fraction coefficients in Q[x]/(x^8+1), with x interpreted as exp(pi*i/8).
It reconstructs spectral projectors and checks outer-product factors, all
witness PVM identities, state normalization, the complete target table, both
attained values, Fourier compression, a 16×16 witness SOS, and a symbolic
second-family SOS in a two-party free-unitary algebra. The symbolic normal
form does not commute generators within Alice or within Bob.

The negative controls detect wrong state normalization, a changed target phase
order, a malformed polar phase, and a wrong SOS prefactor. Those exact checks
are helpful convention/arithmetic evidence, but the checker and its semantic
interpretation were not verified inside Lean. They cannot certify any Lean
endpoint or the first-family universal bound.

Ten tests of the report parser and source scanner passed. The source/import
scanner passed for all six Lean files and found all 39 axiom queries. It is a
static check, not a Lean elaborator. The full build-and-audit command exited 2
before any Lean command, as recorded in `logs/build_attempt.log`.

## Reproduction

In a checkout containing the matching canonical manuscript, place this folder
at `cyclic_bell_exact_values_and_randomness/lean_formalization/`. Do not replace
other project files. Then, with Lean/Lake, Git and Python available:

```sh
cd cyclic_bell_exact_values_and_randomness/lean_formalization
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

The runner verifies the manuscript bytes against the baseline, compiler commit,
and all dependency commits; performs a clean project build; checks physical
positive/negative controls; executes all axiom queries; and verifies source
stability. Detailed receipts are stored under `logs/runs/`. Unexpected failures,
missing reports, or nonstandard axioms stop the run. It does not silently reset
existing dependency modifications. It does not edit, commit, push, or publish.

The command is supplied for reproduction, **not asserted to pass**: the current
candidates may require actual Lean elaboration/proof repairs. A passing build
would certify the checked candidate statements, subject to a correspondence
review; it would not automatically close the remaining paper-level gaps.

## Exact remaining obstacles

Immediate execution obstacle: no Lean/Lake in the cloud runtime, with failed
supported acquisition attempts. Immediate preservation obstacle: GitHub writes
were denied; all commits in this delivery are local preservation commits only.

Mathematical/formal gaps: prove the positive-square-root/exponential phase
identification; complete all non-target Bell measurements in Lean; establish
one actual universal arbitrary-dimension bound and explicit attainment; and
perform the independent statement/dependency review. The first-family polar/
functional-calculus proof has not been attempted in Lean, so its compilation
cost or feasibility was not measured by this pilot.

Continuing is worthwhile **in a Lean-capable environment**: the exact witness
and both scalar evaluations survive independent arithmetic reconstruction,
and the second SOS survives a symbolic check without illicit same-party
commutation. The next useful checkpoint is a real clean kernel pass of the
target-only package plus its exponential-phase bridge. A subsequent complete
second-family result would require the additional gaps listed in COVERAGE.md;
it would not settle the first-family Conjecture-2 formalization by itself.
