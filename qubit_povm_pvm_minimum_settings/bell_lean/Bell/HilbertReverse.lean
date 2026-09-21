import Bell.HilbertCorrespondence

/-! The reverse correspondence places each fixed-qubit matrix strategy on actual
complex Euclidean Hilbert spaces and their algebraic Hilbert tensor product.
This is a dimension-two source strategy; it makes no assertion that a fixed
one-dimensional carrier realizes every qubit behavior. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder TensorProduct InnerProductSpace
namespace Bell.Hilbert

abbrev QubitSpace := EuclideanSpace ℂ Qubit

def qubitBasis : OrthonormalBasis Qubit ℂ QubitSpace := EuclideanSpace.basisFun Qubit ℂ

def jointQubitBasis : Basis Joint ℂ (QubitSpace ⊗[ℂ] QubitSpace) :=
  qubitBasis.toBasis.tensorProduct qubitBasis.toBasis

def ofQubitOperator (A : Operator) : QubitSpace →ₗ[ℂ] QubitSpace :=
  (LinearMap.toMatrix qubitBasis.toBasis qubitBasis.toBasis).symm A

@[simp]
theorem ofQubitOperator_matrix (A : Operator) :
    LinearMap.toMatrix qubitBasis.toBasis qubitBasis.toBasis (ofQubitOperator A) = A :=
  (LinearMap.toMatrix _ _).apply_symm_apply A

theorem ofQubitOperator_positive (A : Operator) (hA : A.PosSemidef) :
    PositiveOperator (ofQubitOperator A) := by
  have hp := (basisMatrix_positive_iff qubitBasis.toBasis (ofQubitOperator A)).mp
    (by simpa only [ofQubitOperator_matrix] using hA)
  simpa only [PositiveOperator, PositiveFor, orthonormal_basisInner] using hp

def ofQubitDensity (A : JointOperator) :
    (QubitSpace ⊗[ℂ] QubitSpace) →ₗ[ℂ] (QubitSpace ⊗[ℂ] QubitSpace) :=
  (LinearMap.toMatrix jointQubitBasis jointQubitBasis).symm A

@[simp]
theorem ofQubitDensity_matrix (A : JointOperator) :
    LinearMap.toMatrix jointQubitBasis jointQubitBasis (ofQubitDensity A) = A :=
  (LinearMap.toMatrix _ _).apply_symm_apply A

theorem jointInner_qubitBasis : jointInner QubitSpace QubitSpace = basisInner jointQubitBasis := by
  funext x y
  exact (tensorInner_basis_independent qubitBasis qubitBasis
    (stdOrthonormalBasis ℂ QubitSpace) (stdOrthonormalBasis ℂ QubitSpace) x y).symm

def ofQubitState (ρ : Bell.State) : State QubitSpace QubitSpace where
  density := ofQubitDensity ρ.density
  positive := by
    rw [jointInner_qubitBasis]
    apply (basisMatrix_positive_iff jointQubitBasis _).mp
    simpa only [ofQubitDensity_matrix] using ρ.positive
  normalized := by
    rw [LinearMap.trace_eq_matrix_trace ℂ jointQubitBasis, ofQubitDensity_matrix]
    exact ρ.normalized

def ofQubitPOVM {n : ℕ} (M : Bell.POVM n) : POVM QubitSpace n where
  effect := fun a => ofQubitOperator (M.effect a)
  positive := fun a => ofQubitOperator_positive _ (M.positive a)
  normalized := by
    apply (LinearMap.toMatrix qubitBasis.toBasis qubitBasis.toBasis).injective
    simp only [map_sum, ofQubitOperator_matrix, LinearMap.toMatrix_one, M.normalized]

def ofQubitPVM {n : ℕ} (M : Bell.PVM n) : PVM QubitSpace n where
  toPOVM := ofQubitPOVM M.toPOVM
  idempotent := by
    intro a
    apply (LinearMap.toMatrix qubitBasis.toBasis qubitBasis.toBasis).injective
    change LinearMap.toMatrix _ _ (ofQubitOperator (M.effect a) * ofQubitOperator (M.effect a)) =
      LinearMap.toMatrix _ _ (ofQubitOperator (M.effect a))
    rw [LinearMap.toMatrix_mul, ofQubitOperator_matrix, M.idempotent]
  orthogonal := by
    intro a b hab
    apply (LinearMap.toMatrix qubitBasis.toBasis qubitBasis.toBasis).injective
    change LinearMap.toMatrix _ _ (ofQubitOperator (M.effect a) * ofQubitOperator (M.effect b)) = _
    rw [LinearMap.toMatrix_mul, ofQubitOperator_matrix, ofQubitOperator_matrix, M.orthogonal a b hab,
      map_zero]

def ofQubitStrategy {A : Architecture} (s : Bell.Strategy A) : Strategy QubitSpace QubitSpace A where
  state := ofQubitState s.state
  alice := fun x => ofQubitPOVM (s.alice x)
  bob := fun y => ofQubitPOVM (s.bob y)

def ofQubitProjectiveStrategy {A : Architecture} (s : Bell.ProjectiveStrategy A) :
    ProjectiveStrategy QubitSpace QubitSpace A where
  state := ofQubitState s.state
  alice := fun x => ofQubitPVM (s.alice x)
  bob := fun y => ofQubitPVM (s.bob y)

set_option maxRecDepth 10000 in
@[simp]
theorem ofQubitState_coordinates (ρ : Bell.State) :
    (ofQubitState ρ).coordinates qubitBasis qubitBasis = ρ.density :=
  ofQubitDensity_matrix ρ.density

theorem ofQubit_born (ρ : Bell.State) (M N : Operator) :
    born (ofQubitState ρ).density (ofQubitOperator M) (ofQubitOperator N) =
      Bell.born ρ.density M N := by
  rw [born_coordinates qubitBasis qubitBasis (ofQubitState ρ),
    ofQubitState_coordinates, ofQubitOperator_matrix, ofQubitOperator_matrix]
  rfl

theorem ofQubitStrategy_behavior {A : Architecture} (s : Bell.Strategy A) :
    (ofQubitStrategy s).behavior = s.behavior := by
  funext x y a b
  exact ofQubit_born s.state ((s.alice x).effect a) ((s.bob y).effect b)

theorem ofQubitProjectiveStrategy_behavior {A : Architecture} (s : Bell.ProjectiveStrategy A) :
    (ofQubitProjectiveStrategy s).toStrategy.behavior = s.toStrategy.behavior := by
  exact ofQubitStrategy_behavior s.toStrategy

theorem qubitSpace_finrank : Module.finrank ℂ QubitSpace = 2 := by
  simp [QubitSpace, Qubit]

end Bell.Hilbert
