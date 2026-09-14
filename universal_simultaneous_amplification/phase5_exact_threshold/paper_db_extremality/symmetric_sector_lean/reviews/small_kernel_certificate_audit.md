# Independent audit of the optimized small-order certificate path

Timestamp: 2026-09-14 14:54 UTC. This review inspects the generated theorem
statements and their trust path, particularly the largest endpoint N=39,
after the finite-system checks were changed to `decide +kernel`.

`Small39.lean` defines an explicit rational response on exactly
`Channel 39 = Fin 38 ⊕ Fin 37`, corresponding to a ranks `1,...,38`
and b ranks `2,...,38`. No missing b rank 1 or rank 39 is inserted. Its
`equations` theorem is the actual 75-equation system

`(1 - coefficientK 39).mulVec response = source 39`.

After function extensionality, kernel reduction checks every row against
the actual matrix and the recursively defined actual gradient source.
No list of independently claimed equations is accepted as an input axiom.
The preceding gradient lemmas also evaluate the genuine recurrence and
check its terminal equation. They are supplementary; the new kernel checker
does not depend on Python's assertion of its gradient values.

The `value` theorem first uses `coefficient_system_isUnit 39` to identify
the checked response with the mathematical inverse response. That unit
theorem is proved by the actual coefficient matrix's strict absolute row
contraction. The helper `witness_eq_inverse_mulVec` cancels using its proved
unit determinant. Only after this identification does kernel reduction
check the actual signed reward dot product. The final `positive` theorem
uses the resulting rational equality and checked rational positivity.
Thus an external solver's assertion of positivity or invertibility is
never in the dependency path.

The inspected `Definitions.lean` retains K=Hᵀ, the negative a-to-b
coefficient, positive source, and negative b reward of (A.12)–(A.16).
`reducedScalar` remains the actual `gᵀ(I−K)⁻¹s`; it is not defined from
the external answer. The generator imports python-flint solely to discover
a rational solution witness. Any erroneous vector or scalar emitted by it
will fail the equation or dot-product check.

`decide +kernel` produces an ordinary Lean proof by kernel reduction.
It is distinct from `native_decide`; neither this generated source nor its
generic identification proof uses native evaluation, custom evaluators,
compiler-trust assertions, unproved axioms, or placeholders. Independent
final axiom queries should still include the quantified small-range theorem
and the endpoint equations/value, since a source audit does not replace a
successful build and transitive dependency audit.

After the endpoint module was built, I ran the separate query
`reports/SmallEndpointAxioms.lean`. The equations, exact value, strict
positivity, general coefficient-system invertibility, and witness/inverse
identification all report exactly `propext`, `Classical.choice`, and
`Quot.sound`. The full output is retained in `reports/SmallEndpointAxioms.log`.
There is no computed-answer or compiler-trust axiom in any queried dependency.

No trust-path or endpoint-statement discrepancy was found. Completion
estimate for this bounded source and statement review: 100%; full build
and axiom evidence is recorded by the project build audit, not inferred
from inspection. The general-n active-chain identification remains a
separate theorem obligation.
