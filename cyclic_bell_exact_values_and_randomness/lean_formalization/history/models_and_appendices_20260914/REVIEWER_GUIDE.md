# Reviewer guide — model values, binary certification and appendices

## Trust boundary first

This is a **source-only continuation**. No Lean process was invoked. Every
mathematical declaration is an uncompiled candidate and may require substantial
proof repair. No actual axiom reports, clean-build receipt or independent-agent
review exists for this source. A final kernel pass must still be followed by
independent manuscript-statement validation.

Canonical manuscript Git blob: `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
Its SHA-256 in the repository manifest is
`82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
Raw canonical bytes were not re-hashed here; the offline command requires both
hashes to match the local `main.tex` before issuing any success receipt.

## Most useful new endpoints

`GeneralCorrelationValues.lean` defines the actual real correlation models and
writes these four literal supremum equalities for every d>=2:

```lean
CyclicBell.General.first_reduced_values_q_qa_qc
CyclicBell.General.first_augmented_values_q_qa_qc
CyclicBell.General.second_reduced_values_q_qa_qc
CyclicBell.General.second_augmented_values_q_qa_qc
```

The first two values are `2/sin(pi/(2*d))` and that number plus one. The second
family values are d and d+1. `ModelValueStatements.lean` expands the actual
`bellSupremum` and `closure` statements, not just the theorem names.

`GeneralModelCounterexamples.lean` attaches the same concrete final-two-swap
strategy to all three maxima and its nonuniform Born table. The physical
trivial-Eve success is explicitly identified, without assuming a worst possible
Eve or maximizing over all compatible realizations.

## Read the physical model before its value assembly

1. `GeneralBehavior.lean` uses a real array `p x y a b`; observable correlations
   are derived as `sum chi(a+b) * p x y a b`. No optimum is a definition of score.
   Reduced Bob settings use `Ix d`; augmented settings use `Option (Ix d)`.
2. `GeneralCommutingModel.lean` defines a unit vector and actual PVMs on any
   complete complex Hilbert space. Cross-party effect commutation is its physical
   hypothesis. Same-party commutation and finite dimension are not assumed.
3. `GeneralHilbertBridge.lean` maps finite matrices to operators on Euclidean
   Hilbert space, not the ordinary sup-norm function space. It vectorizes the
   positive square root of an arbitrary mixed density matrix and lets both
   parties act trivially on the added environment. Adjoint, tensor placement,
   normalization, PVM validity and full Born equality are written separately.
4. `Qq_subset_Qqc` uses that construction. `Qqa` is literally `closure Qq`.
   Continuous sublevel sets carry each scalar bound to Qqa. Supremum proofs
   exhibit a member and an upper bound before using real `sSup`.

The proof does **not** assume or prove general Qqa-subset-Qqc or closedness of
Qqc. Those general facts are unnecessary for these value equalities. Do not
claim them merely because the three particular suprema agree.

## Binary certification: validity is not privacy

`GeneralBinaryModels.lean` writes the two-square C-star identity and a separate
arbitrary-Hilbert upper bound. Binary PVM encodings are proved to be Hermitian
involutions. The literal source qubit witness gives a nonempty attaining model,
and `binary_values_q_qa_qc` assembles its three model suprema.

`GeneralBinaryCertification.lean` adds actual finite purified strategies. Their
fields contain only an amplitude matrix, its normalization and PVMs.
`binary_purified_saturation` connects the earlier matrix privacy proof to those
physical fields and true post-measurement conditional states. Eve's finite
dimension is arbitrary.

`BinaryPrivacyAt` quantifies over **every compatible finite purification** of a
behavior. It is a property proved or refuted, never a strategy-validity field.
The achievable behavior is physically constructed; `purifyStrategy` separately
ensures that every finite mixed strategy has a compatible purification.

The new `binary_componentwise_minimality` combines this achievable private
2x2 binary behavior with actual success-one one-input constructions in both
party orientations. It is not a classification of higher-dimensional setting
complexity and makes no arbitrary-Hilbert Eve privacy claim.

## Appendix additions

`GeneralExactValues.lean` derives all five entries d=2,3,4,5,6 of the manuscript's
exact-value table from the literal sine expression. The values are
`2 sqrt 2`, `4`, `2 sqrt(4+2 sqrt 2)`, `2(1+sqrt 5)`, and `2(sqrt 6+sqrt 2)`.

`GeneralCycleCharpoly.lean` proves the written candidate
`charpoly(weightedCycle w) = X^d - C(product w)` for arbitrary nonzero complex
weights. It expands the actual Mathlib Cayley-Hamilton theorem, uses the d
successive first-column supports, and cancels nonzero prefix products to find
every lower coefficient. No unit-modulus or product-one hypothesis is hidden
in that theorem. The d=1 boundary is included.

## Self-audit and test evidence

Read `MODEL_VALUE_SELF_AUDIT.md` for the inspection checklist, repairs and
remaining API risks. No separate agent participated. The new Gaussian-rational
finite tests passed 9,906 assertions and 37 controls, including unequal local
dimensions, rank-deficient densities, zero PVM effects and a uniform observed
behavior that is perfectly guessable by Eve. A separate determinant expansion
passed 175 assertions and 19 controls in d=1..7. It shares Gaussian arithmetic
but not the written Cayley-Hamilton argument.

All retained exact regressions also reran. The 34 audit-machinery tests check
receipt parsing and control registration, not Lean mathematics. None of these
results proves model closure, suprema or a universal theorem.

## What is still genuinely missing

The full general Qqa-subset-Qqc inclusion; source-Z/qutrit strategy identification;
standard Fourier-phase and anchored target formulas/asymptotics; and full
adversarial tripartite guessing-model suprema remain outside the source endpoints.
The canonical polar and Toeplitz/SVD intermediate routes were replaced, not
individually translated. Open questions and bibliography are not theorem claims.

Most importantly, **the entire accumulated source still needs Lean compilation
and independent statement review**. The offline repair order is in
`OFFLINE_HANDOFF.md`. Do not turn a difficult helper into a new physical-model
assumption, drop a troublesome audit import, or advertise static counts as
formal verification.
