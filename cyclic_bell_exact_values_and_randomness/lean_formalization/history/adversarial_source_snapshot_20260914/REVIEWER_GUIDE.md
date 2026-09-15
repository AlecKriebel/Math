# Reviewer guide — uncompiled research companion

**There are no kernel-verified endpoints in this package.** It is Lean proof
source for offline checking and repair, not a formal-verification certificate.
No Lean invocation, successful clean build or actual axiom output occurred in
this continuation. The same assistant authored the source, tests and self-audit.

## What to read first

Read `STATEMENT_CONTRACT.md`, `GENERAL_STATEMENT_CONTRACT.md`,
`MODEL_VALUE_CONTRACT.md` and `ADVERSARIAL_STATEMENT_CONTRACT.md` for the physical
model, conventions, quantifiers and manuscript labels. `COVERAGE.md` maps claims
to declarations and separates remaining gaps. The manuscript Git blob is
`bbd0667c934d5a34dd9c8ced50df91515cb1308c`; the expected SHA-256 is inherited from
the repository manifest and must be checked against local raw manuscript bytes.

The retained core is the d=4 counterexample, all-dimensional cyclic values and
permutation witnesses, actual reduced-state supported multiplicities, separate
arbitrary-Hilbert upper bounds, the binary value/privacy/minimality endpoints,
and selected appendix identities. Every one remains an uncompiled candidate.

## New strongest endpoints

`first_value_conditioned_guessing_bounds` and
`second_value_conditioned_guessing_bounds` establish the source form of the
paper's quantitative lower bound, plus upper bound one, for the actual GvalQ,
GvalQa and GvalQc definitions. `first_four_Gval_three32` and its second-family
analogue strengthen the d=4 lower bound to 3/32. The entropy endpoints give
upper bound `5-log(3)/log(2)`, not equality to an optimal worst-case entropy.

The dependency chain is:

    PSD state + AB PVMs + general Eve POVM
      -> full tripartite Born array and sandwich/partial-trace pairing
      -> physical finite-to-three-party-commuting embedding
      -> actual q/qa/qc extended correlation domains
      -> Bell-equality subsets + normalized success in [0,1]
      -> literal real suprema + explicit common finite witness.

`GuessQa` is closure of the full extended behavior set BEFORE intersecting with
Bell equality. No arbitrary extension of a Qqa marginal is allowed. No model
validity field assumes maximality, an equality spectrum or a target table.
No Eve POVM is assumed projective, and no same-party commutation is imposed.

`fixed_realization_guessing_maximum` separately proves existence of an optimal
POVM for any fixed finite realization. Its Gram-factor argument includes ALL
positive effects via their positive square roots, derives an entry bound from
normalization in arbitrary dimension, and applies compactness to the actual
continuous objective. `first_GvalQ_nested` and `second_GvalQ_nested` connect the
flattened finite-q optimization to the outer supremum of these attained maxima.
There is no claim that a worst-case realizing state exists.

## Source Fourier appendix

`source_coefficient_DFT`, `source_fourier_zero`, `source_fourier_one` and
`source_qutrit_operator` use the literal triangular-exponent coefficients,
positive clock Z and forward shift X. They retain the phase and matrix order.
They do not by themselves prove source Bob PVM validity or the full canonical
polar identification. The independently supplied physical cycle witnesses
remain the attaining strategies used in the value proofs.

## Incoming defect and its repair

`dimension_pos` was in a witness file that the scalar-bound file did not import.
Its unchanged declaration was moved to `GeneralFourier.lean`, an existing shared
ancestor. Four formerly unresolved project references are recorded in
`logs/adversarial_incoming_reference_error.json`. No witness import was added
to a universal bound. A new conservative reference scanner catches this error
and selected forward/missing-import errors; it is NOT Lean name resolution.

## Reproduce

From the companion directory, with Lean/Lake installed:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

The normal build reaches all 76 Lean modules/audits, with 1,479 pending axiom
queries and 21 registered offline controls (four accept, seventeen reject).
The allowed standard foundations are `propext`, `Classical.choice`, `Quot.sound`.
The runner rejects any other transitive axiom, missing report, false accepted
control, dirty dependency reset or unexpected compiler identity. It never
changes the manuscript, creates a release, contacts anyone or publishes.

Offline source repairs must preserve the statement contracts. After a genuine
clean pass, an independent reviewer should check the complete physical and
manuscript bridge, especially Gram compactness, dependent model existentials,
partial traces, CFC/support interfaces and all supremum nonemptiness arguments.
No assurance that remaining repairs are only syntactic is justified.
