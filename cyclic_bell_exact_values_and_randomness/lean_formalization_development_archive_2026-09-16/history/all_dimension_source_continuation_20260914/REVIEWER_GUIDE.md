# Reviewer guide — cyclic Bell companion, extended source

## Status first

This package contains **uncompiled Lean 4 source**, not a certification.
No Lean process ran in this continuation. No generated dependency query has
been converted into an actual axiom report. Some proofs may require substantive
repair, additional lemmas or different library implementations.

The source grows the previous d=4 package into all-dimensional cyclic values,
phase-permutation witnesses, support rigidity, commuting-operator upper bounds,
and several physical-randomness and low-setting results. It does **not** cover
every mathematical statement in the manuscript: see `COVERAGE.md`.

## Fast inspection path

Start with `CyclicBell/GeneralStatements.lean`: it expands the physical
quantifiers, the actual lambda formula, Born probabilities, Hilbert-space bound,
and the supported eigenspaces. Then inspect these candidate endpoints:

```lean
CyclicBell.General.first_all_dimension_counterexample
CyclicBell.General.second_all_dimension_counterexample
CyclicBell.General.supported_multiplicity_rigidity
CyclicBell.General.supported_dimension_divisible
CyclicBell.General.first_commuting_PVM_upper
CyclicBell.General.second_commuting_PVM_upper
```

For operational statements inspect:

```lean
CyclicBell.General.first_all_dimension_physical_Eve_gap
CyclicBell.General.second_all_dimension_physical_Eve_gap
CyclicBell.General.binary_saturation_privacy
CyclicBell.General.binary_private_guess_success
CyclicBell.General.one_input_pure_projective_perfect_guess
CyclicBell.General.privateMUB_composition
CyclicBell.General.physical_private_iff_fourier
```

## Physical definitions, not result-assuming interfaces

`GeneralModel.lean` uses complex matrices on arbitrary finite local index types.
A state is PSD and trace one. A measurement has PSD, pairwise orthogonal
idempotents summing to identity. Zero outcomes are allowed. None of these
structures contains a Bell bound, equality spectrum or maximizing condition.

The tensor product has entries A(i,k) B(j,l). Adjoint means conjugate transpose;
ordinary transpose has no conjugation. The observable is the positive-character
encoding sum_a exp(2*pi*i*a/d) M_a. General PVM unitarity/order and inverse
encoding have their own source proofs. The correlator has an explicit bridge
to the actual real Born probabilities, not only to complex trace expressions.

General indices are `ZMod d`. The additional Bob input is `none`; reduced
inputs are `some y`. Thus `(1, none)` is manuscript target `(1,d)`, not a
renumbered reduced input. The phase sequence's Fourier transform uses a plus
sign, while Mathlib's dft uses a minus sign. The bridge is explicit, and the
physical target uses frequency `-(a+b)` and normalization `d^(-3)`.

## Core proof routes

The scalar result is `GeneralScalar.scalar_bound` with equality characterized
by `scalar_equality_iff`. Its sector/floor trigonometry is a particularly
important offline review target. The matrix and arbitrary-Hilbert proofs lift
continuous half-polar factors, rather than assuming an invertible polar unitary.
The functions are zero-safe; `ALL_DIMENSION_ROUTES.md` gives the algebra.

`GeneralFirstBound` and `GeneralCommuting` have statically inspected import
closures free of the concrete cycle/permutation witness modules. Attainment and
probabilities are later, separate dependencies. The second family uses the
actual signed/exponential lambda formula, its derived normalization, and the
source prefactor 1/(2d), not an arbitrary normalized vector fitted to the witness.

The supported-multiplicity chain is more than the last rank inequality:

    actual state and maximal scalar value
    -> PSD square-root purification and zero SOS residuals
    -> cancellation on the actual reduced-state support
    -> equality-root support and finite-spectrum zero transfer
    -> supported polar routing and invariance
    -> adjacent reflections and powers from Bob's PVM order
    -> relative rank inequality and direct-sum dimension accounting
    -> equal positive supported eigenspace multiplicities, d | dim(support)

Read `GeneralSupportSaturation`, `GeneralSupportedPhases`, `GeneralReflectionRank`
and `GeneralRigidity` in that order. The ambient complement is intentionally
unconstrained. Exact finite examples include unused ambient phase/kernel blocks
as negative controls against a false global-phase upgrade.

## Randomness and supplementary results

The explicit one-dimensional Eve instrument is linked to an actual adjoined
state, sandwich and partial trace. The general biased constructions only give
witness lower bounds; no supremal guessing optimizer is asserted.

Binary saturation privacy is operator-valued, with arbitrary finite purifying
Eve; it is not merely a uniform scalar table. The one-input construction stores
a full hidden-variable table in a normalized pure tripartite state and uses
grouping PVMs, including a correctly handled zero-probability conditioning case.
The private-MUB result preserves the manuscript's sufficient hypotheses.

The computational-MUB exposure obstruction has a shorter constant-diagonal
positivity proof. It rules out the stated coefficientwise spectral route, not
all possible low-setting Bell designs.

## Evidence and trust boundary

The 3,040 distinct new exact-arithmetic regression checks and 38 negative
controls cover selected dimensions 2 through 12, not universal quantifiers.
The original d=4 392-check suite and two distinct word-reduction SOS suites were
rerun. No certificate is imported by the Lean proof scripts. All code and
review were authored by the same assistant; this is **not** an independent-agent
or external specialist review.

The 26 Python reporting/scanner tests are tests of the audit machinery, not
Lean proof tests. Standard build/import coverage and pending axiom queries are
mechanically checked. In the offline build every axiom report must contain only
some subset of `propext`, `Classical.choice`, `Quot.sound`.

## Reproduce the actual formal check offline

With the matching manuscript beside this directory:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

This command has **not** been run in this continuation. It checks exact pins,
cleans only this project's build outputs, imports all candidates and audits,
executes positive/false controls, and checks actual axiom reports. It never
commits, pushes, resets source, modifies the manuscript, or creates a release.
A successful run still requires independent statement-correspondence review.
See `OFFLINE_HANDOFF.md` for staged repair instructions.
