# Hilbert-space dimension and basis correspondence

2026-09-21, implementation checkpoint (85% of this bridge complete).

The independent source model is now compiled in `Bell/HilbertCorrespondence.lean`:
local spaces are arbitrary finite-dimensional complex inner-product spaces;
effects are actual linear endomorphisms; the density is an endomorphism of their
algebraic tensor product; positivity and self-adjointness use source inner
products; normalization and Born probabilities use `LinearMap.trace` and
`TensorProduct.map`. These definitions do not refer to the fixed-qubit embedding.

Mathlib 4.19 does not provide the needed Hilbert tensor-product instance. Instead,
`Bell/HilbertCoordinates.lean` constructs its canonical Hermitian form in arbitrary
source orthonormal bases and proves sesquilinearity, positive definiteness, the
pure-tensor product formula, and independence of both chosen bases. Positivity
of source endomorphisms is equivalent to PSD of their source coordinate matrix.
This finite-dimensional construction requires no new analytic assumptions.

The forward representation has compiled for arbitrary complex Hilbert spaces
with each local finrank at most two. It chooses source ONBs, uses explicit local
linear isometries into complex C², embeds the joint density by the tensor of their
coordinate matrices, and assigns the unused orthogonal complement to one selected
outcome in each measurement. Joint trace and all Born probabilities are preserved.
POVM normalization/positivity and PVM idempotence/orthogonality are proved.
`State.alice_finrank_pos` and `State.bob_finrank_pos` exclude zero-dimensional
states directly from trace one. Outcome nonemptiness is derived from source
normalization after those facts; it is not an extra endpoint premise.

The matrix and actual Hilbert-isometry helpers were independently implemented
and compiled in `Bell/IsometricCompression.lean` and `Bell/HilbertIsometry.lean`.
The explicit rectangular matrix tests include dimensions zero, one, and two.
No raw equality for a fixed one-dimensional source is claimed. Still to finish:
reverse realization of fixed matrices as actual Hilbert operators, composition
with the complete-strategy finite-mixture theorem, and independent contracts.
No axioms or sorry are used.

2026-09-21 07:31 PDT, completed checkpoint (100% of the assigned Hilbert bridge).

The reverse realization compiled in `Bell/HilbertReverse.lean`: every fixed-qubit
state and POVM/PVM strategy becomes a source operator strategy on actual complex
Euclidean C² spaces, with identical complete behavior. `Bell/HilbertSimulation.lean`
then defines the independent physical raw sets as a union over local `Space`
carriers of dimension at most two and proves exact equality with the matrix raw
sets for both measurement classes. The hull equality follows through this genuine
two-sided correspondence. The theorem
`Bell.Hilbert.Strategy.finite_projective_simulation` takes an arbitrary source
Hilbert strategy with two inputs and returns an actual finite family of source
Hilbert PVM strategies on C², nonnegative common weights summing to one, and a
whole-behavior equality. Both parties and the joint state are selected together
in each branch; there is no per-entry choice or fixed-dimension-one raw equality.

Verification receipts:

- `bell_lean/local_verification/hilbert_simulation_build.log`: successful production
  build of the full new bridge and its existing main-theorem dependencies.
- `bell_lean/validation/HilbertContracts.lean`: compiled successfully (exit 0;
  `local_verification/hilbert_contracts.log` is empty because there are no errors
  or warnings). These anonymous contracts expand operator-source trace/positivity,
  arbitrary local isometry, both-party embedding validity, complete behavior
  preservation, projectivity, reverse realization, raw-set equality, and the
  finite projective-mixture endpoint. They explicitly prove zero-dimensional
  state impossibility, impossible empty measurement outputs, and existence of
  a genuine normalized one-dimensional source state as a nonvacuity check.
- `bell_lean/local_verification/HilbertAxiomCheck.lean` and `hilbert_axioms.log`:
  eight core bridge/end-to-end statements depend only on `propext`,
  `Classical.choice`, and `Quot.sound`; no custom axiom or admitted proof occurs.
- Production source scan of the three directly owned modules contains no
  `sorry` or `axiom` declarations.

Independent semantic review accepted the source/target separation, canonical
tensor form, dimension-zero boundary, complement-padding construction, exact
joint Born transfer, and use of the main theorem. Final repository-wide rebuild,
all-declaration audit, arbitrary finite-label composition, package checks and
committing/pushing remain the coordinating agent's separate integration scope.
