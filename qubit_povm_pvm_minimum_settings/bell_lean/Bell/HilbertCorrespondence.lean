import Bell.HilbertCoordinates
import Bell.HilbertIsometry

/-! # Arbitrary complex Hilbert spaces of local dimension at most two

The source model uses endomorphisms of the actual local spaces and their
algebraic tensor product. Positivity uses the source Hilbert inner products and
the basis-independent tensor inner product; normalization and Born probabilities
use the basis-independent linear-map trace. Fixed-qubit matrices enter only in
the representation theorem, not these physical definitions.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder TensorProduct InnerProductSpace
namespace Bell.Hilbert

variable (E F : Type*) [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]

/-- The canonical source tensor Hermitian form, using an arbitrary standard ONB
only to construct it. `tensorInner_basis_independent` removes that choice. -/
def jointInner : (E ⊗[ℂ] F) → (E ⊗[ℂ] F) → ℂ :=
  tensorInner (stdOrthonormalBasis ℂ E) (stdOrthonormalBasis ℂ F)

structure State where
  density : (E ⊗[ℂ] F) →ₗ[ℂ] (E ⊗[ℂ] F)
  positive : PositiveFor (jointInner E F) density
  normalized : LinearMap.trace ℂ (E ⊗[ℂ] F) density = 1

structure POVM (n : ℕ) where
  effect : Fin n → E →ₗ[ℂ] E
  positive : ∀ a, PositiveOperator (effect a)
  normalized : ∑ a, effect a = 1

structure PVM (n : ℕ) extends POVM E n where
  idempotent : ∀ a, effect a * effect a = effect a
  orthogonal : ∀ a b, a ≠ b → effect a * effect b = 0

variable {E F}

def born (ρ : (E ⊗[ℂ] F) →ₗ[ℂ] (E ⊗[ℂ] F))
    (M : E →ₗ[ℂ] E) (N : F →ₗ[ℂ] F) : ℝ :=
  (LinearMap.trace ℂ (E ⊗[ℂ] F) (ρ * TensorProduct.map M N)).re

variable (E F)
structure Strategy (A : Architecture) where
  state : State E F
  alice : (x : Fin A.aliceInputs) → POVM E (A.aliceOutputs x)
  bob : (y : Fin A.bobInputs) → POVM F (A.bobOutputs y)

structure ProjectiveStrategy (A : Architecture) where
  state : State E F
  alice : (x : Fin A.aliceInputs) → PVM E (A.aliceOutputs x)
  bob : (y : Fin A.bobInputs) → PVM F (A.bobOutputs y)

variable {E F}
def Strategy.behavior {A : Architecture} (s : Strategy E F A) : Behavior A :=
  fun x y a b => born s.state.density ((s.alice x).effect a) ((s.bob y).effect b)

def ProjectiveStrategy.toStrategy {A : Architecture}
    (s : ProjectiveStrategy E F A) : Strategy E F A where
  state := s.state
  alice := fun x => (s.alice x).toPOVM
  bob := fun y => (s.bob y).toPOVM

section Coordinates
variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]
variable (b : OrthonormalBasis ι ℂ E) (c : OrthonormalBasis κ ℂ F)

def State.coordinates (ρ : State E F) : Matrix (ι × κ) (ι × κ) ℂ :=
  LinearMap.toMatrix (b.toBasis.tensorProduct c.toBasis)
    (b.toBasis.tensorProduct c.toBasis) ρ.density

theorem State.coordinates_positive (ρ : State E F) : (ρ.coordinates b c).PosSemidef := by
  apply basisMatrix_positive
  have hi : basisInner (b.toBasis.tensorProduct c.toBasis) = jointInner E F := by
    funext x y
    exact tensorInner_basis_independent b c (stdOrthonormalBasis ℂ E)
      (stdOrthonormalBasis ℂ F) x y
  rw [hi]
  exact ρ.positive

theorem State.coordinates_trace (ρ : State E F) : (ρ.coordinates b c).trace = 1 := by
  rw [State.coordinates, ← LinearMap.trace_eq_matrix_trace]
  exact ρ.normalized

def POVM.coordinates {n : ℕ} (M : POVM E n) (a : Fin n) : Matrix ι ι ℂ :=
  LinearMap.toMatrix b.toBasis b.toBasis (M.effect a)

theorem POVM.coordinates_positive {n : ℕ} (M : POVM E n) (a : Fin n) :
    (M.coordinates b a).PosSemidef := operatorMatrix_positive b _ (M.positive a)

theorem POVM.coordinates_sum {n : ℕ} (M : POVM E n) :
    ∑ a, M.coordinates b a = 1 := by
  simp only [POVM.coordinates, ← map_sum]
  rw [M.normalized, LinearMap.toMatrix_one]

theorem PVM.coordinates_idempotent {n : ℕ} (M : PVM E n) (a : Fin n) :
    M.toPOVM.coordinates b a * M.toPOVM.coordinates b a = M.toPOVM.coordinates b a := by
  simp only [POVM.coordinates, ← LinearMap.toMatrix_mul, M.idempotent]

theorem PVM.coordinates_orthogonal {n : ℕ} (M : PVM E n) (a a' : Fin n) (h : a ≠ a') :
    M.toPOVM.coordinates b a * M.toPOVM.coordinates b a' = 0 := by
  simp only [POVM.coordinates, ← LinearMap.toMatrix_mul, M.orthogonal a a' h, map_zero]

open scoped Kronecker in
/-- Both local basis changes and the joint trace are accounted for in this
identity for arbitrary states and arbitrary complex endomorphisms. -/
theorem born_coordinates (ρ : State E F) (M : E →ₗ[ℂ] E) (N : F →ₗ[ℂ] F) :
    born ρ.density M N =
      (ρ.coordinates b c *
        (LinearMap.toMatrix b.toBasis b.toBasis M ⊗ₖ
          LinearMap.toMatrix c.toBasis c.toBasis N)).trace.re := by
  rw [born, LinearMap.trace_eq_matrix_trace ℂ (b.toBasis.tensorProduct c.toBasis),
    LinearMap.toMatrix_mul, TensorProduct.toMatrix_map]
  rfl

end Coordinates

/-- A zero-dimensional local side forces zero-dimensional joint trace; it
cannot carry a normalized density operator. No nonzero-space premise is hidden. -/
theorem State.alice_finrank_pos (ρ : State E F) : 0 < Module.finrank ℂ E := by
  by_contra h
  have hz : Module.finrank ℂ E = 0 := Nat.eq_zero_of_not_pos h
  letI : IsEmpty (Fin (Module.finrank ℂ E)) := by rw [hz]; infer_instance
  have ht := ρ.coordinates_trace (stdOrthonormalBasis ℂ E) (stdOrthonormalBasis ℂ F)
  simp [Matrix.trace] at ht

theorem State.bob_finrank_pos (ρ : State E F) : 0 < Module.finrank ℂ F := by
  by_contra h
  have hz : Module.finrank ℂ F = 0 := Nat.eq_zero_of_not_pos h
  letI : IsEmpty (Fin (Module.finrank ℂ F)) := by rw [hz]; infer_instance
  have ht := ρ.coordinates_trace (stdOrthonormalBasis ℂ E) (stdOrthonormalBasis ℂ F)
  simp [Matrix.trace] at ht

theorem POVM.outcomes_pos [Nontrivial E] {n : ℕ} (M : POVM E n) : 0 < n := by
  by_contra h
  have hz : n = 0 := Nat.eq_zero_of_not_pos h
  subst n
  have ht := M.normalized
  simp at ht


/-- Each nonempty local measurement receives the unused orthogonal complement
at the selected label. This preserves the complete outcome alphabet. -/
def POVM.toQubit {n : ℕ} (M : POVM E n) (hE : Module.finrank ℂ E ≤ 2)
    (selected : Fin n) : Bell.POVM n :=
  IsometricCompression.povm (IsometricCompression.canonicalEmbedding hE)
    (IsometricCompression.canonicalEmbedding_isometry hE)
    (M.coordinates (stdOrthonormalBasis ℂ E)) selected
    (M.coordinates_positive _) (M.coordinates_sum _)

def PVM.toQubit {n : ℕ} (M : PVM E n) (hE : Module.finrank ℂ E ≤ 2)
    (selected : Fin n) : Bell.PVM n :=
  IsometricCompression.pvm (IsometricCompression.canonicalEmbedding hE)
    (IsometricCompression.canonicalEmbedding_isometry hE)
    (M.toPOVM.coordinates (stdOrthonormalBasis ℂ E)) selected
    (M.toPOVM.coordinates_positive _) (M.toPOVM.coordinates_sum _)
    (M.coordinates_idempotent _) (M.coordinates_orthogonal _)

def State.toQubit (ρ : State E F) (hE : Module.finrank ℂ E ≤ 2)
    (hF : Module.finrank ℂ F ≤ 2) : Bell.State :=
  IsometricCompression.state (IsometricCompression.canonicalEmbedding hE)
    (IsometricCompression.canonicalEmbedding hF)
    (IsometricCompression.canonicalEmbedding_isometry hE)
    (IsometricCompression.canonicalEmbedding_isometry hF)
    (ρ.coordinates (stdOrthonormalBasis ℂ E) (stdOrthonormalBasis ℂ F))
    (ρ.coordinates_positive _ _) (ρ.coordinates_trace _ _)

/-- Empty outcome alphabets are excluded by the source state and operator
normalization, rather than by adding alphabet assumptions to the endpoint. -/
def Strategy.aliceSelected {A : Architecture} (s : Strategy E F A)
    (x : Fin A.aliceInputs) : Fin (A.aliceOutputs x) := by
  letI : Nontrivial E := Module.nontrivial_of_finrank_pos s.state.alice_finrank_pos
  exact ⟨0, (s.alice x).outcomes_pos⟩

def Strategy.bobSelected {A : Architecture} (s : Strategy E F A)
    (y : Fin A.bobInputs) : Fin (A.bobOutputs y) := by
  letI : Nontrivial F := Module.nontrivial_of_finrank_pos s.state.bob_finrank_pos
  exact ⟨0, (s.bob y).outcomes_pos⟩

def Strategy.toQubit {A : Architecture} (s : Strategy E F A)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) : Bell.Strategy A where
  state := s.state.toQubit hE hF
  alice := fun x => (s.alice x).toQubit hE (s.aliceSelected x)
  bob := fun y => (s.bob y).toQubit hF (s.bobSelected y)

def ProjectiveStrategy.toQubit {A : Architecture} (s : ProjectiveStrategy E F A)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) : Bell.ProjectiveStrategy A where
  state := s.state.toQubit hE hF
  alice := fun x => (s.alice x).toQubit hE (s.toStrategy.aliceSelected x)
  bob := fun y => (s.bob y).toQubit hF (s.toStrategy.bobSelected y)

/-- Joint Born probabilities are preserved for both parties simultaneously. -/
theorem Strategy.toQubit_behavior {A : Architecture} (s : Strategy E F A)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    (s.toQubit hE hF).behavior = s.behavior := by
  funext x y a b
  change Bell.born _ _ _ = born _ _ _
  rw [born_coordinates (stdOrthonormalBasis ℂ E) (stdOrthonormalBasis ℂ F)]
  exact IsometricCompression.born_padded _ _
    (IsometricCompression.canonicalEmbedding_isometry hE)
    (IsometricCompression.canonicalEmbedding_isometry hF) _ _ _ _ _ _ _

theorem ProjectiveStrategy.toQubit_behavior {A : Architecture} (s : ProjectiveStrategy E F A)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    (s.toQubit hE hF).toStrategy.behavior = s.toStrategy.behavior := by
  exact s.toStrategy.toQubit_behavior hE hF

theorem Strategy.behavior_mem_rawPOVM {A : Architecture} (s : Strategy E F A)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    s.behavior ∈ Bell.rawPOVM A := ⟨s.toQubit hE hF, s.toQubit_behavior hE hF⟩

theorem ProjectiveStrategy.behavior_mem_rawPVM {A : Architecture} (s : ProjectiveStrategy E F A)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    s.toStrategy.behavior ∈ Bell.rawPVM A := ⟨s.toQubit hE hF, s.toQubit_behavior hE hF⟩

end Bell.Hilbert
