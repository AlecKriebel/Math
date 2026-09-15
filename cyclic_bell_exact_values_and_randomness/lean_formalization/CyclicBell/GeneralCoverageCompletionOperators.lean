import Mathlib.Analysis.InnerProductSpace.Completion
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
import Mathlib.Analysis.NormedSpace.OperatorNorm.Completeness
import Mathlib.Tactic

/-! Bounded operators on a complex seminormed pre-Hilbert space extend to its
actual uniform completion. Algebraic relations and inner symmetry are preserved
by equality on the dense embedded pre-space. No quantum-model closure premise
is involved in this infrastructure. -/
noncomputable section
open scoped BigOperators InnerProductSpace
namespace CyclicBell.General.Coverage
open UniformSpace
variable {E : Type*} [SeminormedAddCommGroup E]
section Normed
variable [NormedSpace ℂ E]

/-- The actual completion functor applied to a uniformly continuous linear map.
Linearity passes through the dense embedding even for a seminormed pre-space. -/
def completionOperator (A : E →L[ℂ] E) : Completion E →L[ℂ] Completion E where
  toFun := Completion.map A
  map_add' := by
    intro x y
    refine Completion.induction_on₂ x y
      (isClosed_eq (Completion.continuous_map.comp continuous_add)
        ((Completion.continuous_map.comp continuous_fst).add
          (Completion.continuous_map.comp continuous_snd))) ?_
    intro u v
    rw [← Completion.coe_add, Completion.map_coe A.uniformContinuous,
      Completion.map_coe A.uniformContinuous, Completion.map_coe A.uniformContinuous,
      map_add, Completion.coe_add]
  map_smul' := by
    intro z x
    refine Completion.induction_on x (isClosed_eq
      (Completion.continuous_map.comp (continuous_const_smul z))
      (Completion.continuous_map.const_smul z)) ?_
    intro u
    rw [← Completion.coe_smul, Completion.map_coe A.uniformContinuous,
      Completion.map_coe A.uniformContinuous, map_smul, Completion.coe_smul]
    rfl
  cont := Completion.continuous_map

@[simp] theorem completionOperator_coe (A : E →L[ℂ] E) (x : E) :
    completionOperator A (x : Completion E) = (A x : Completion E) := by
  exact Completion.map_coe A.uniformContinuous x

/-- Equality of continuous operators can be checked on the dense pre-space. -/
theorem completionOperator_ext (A B : Completion E →L[ℂ] Completion E)
    (h : ∀ x : E, A (x : Completion E) = B (x : Completion E)) : A = B := by
  apply ContinuousLinearMap.ext
  intro x
  exact Completion.induction_on x (isClosed_eq A.continuous B.continuous) h

@[simp] theorem completionOperator_zero :
    completionOperator (0 : E →L[ℂ] E) = 0 := by
  apply completionOperator_ext
  intro x
  simpa using (Completion.toComplL : E →L[ℂ] Completion E).map_zero

@[simp] theorem completionOperator_one :
    completionOperator (1 : E →L[ℂ] E) = 1 := by
  apply completionOperator_ext
  intro x
  simp

@[simp] theorem completionOperator_mul (A B : E →L[ℂ] E) :
    completionOperator (A * B) = completionOperator A * completionOperator B := by
  apply completionOperator_ext
  intro x
  simp

@[simp] theorem completionOperator_comp (A B : E →L[ℂ] E) :
    completionOperator (A.comp B) = (completionOperator A).comp (completionOperator B) :=
  completionOperator_mul A B

@[simp] theorem completionOperator_add (A B : E →L[ℂ] E) :
    completionOperator (A + B) = completionOperator A + completionOperator B := by
  apply completionOperator_ext
  intro x
  simp [Completion.coe_add]

@[simp] theorem completionOperator_smul (z : ℂ) (A : E →L[ℂ] E) :
    completionOperator (z • A) = z • completionOperator A := by
  apply completionOperator_ext
  intro x
  simp [Completion.coe_smul]

@[simp] theorem completionOperator_sum {J : Type*} (s : Finset J) (A : J → E →L[ℂ] E) :
    completionOperator (∑ j ∈ s, A j) = ∑ j ∈ s, completionOperator (A j) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert j s hj ih => simp [Finset.sum_insert, hj, ih]

/-- Any norm bound of the pre-space operator remains valid on the completion. -/
theorem completionOperator_bound (A : E →L[ℂ] E) (C : ℝ)
    (h : ∀ x : E, ‖A x‖ ≤ C * ‖x‖) (x : Completion E) :
    ‖completionOperator A x‖ ≤ C * ‖x‖ := by
  refine Completion.induction_on x (isClosed_le (by fun_prop) (by fun_prop)) ?_
  intro y
  simpa using h y

/-- A bare bounded linear map supplies the required continuous operator. -/
def completionOfBounded (A : E →ₗ[ℂ] E) (C : ℝ)
    (h : ∀ x : E, ‖A x‖ ≤ C * ‖x‖) : Completion E →L[ℂ] Completion E :=
  completionOperator (A.mkContinuous C h)

@[simp] theorem completionOfBounded_coe (A : E →ₗ[ℂ] E) (C : ℝ)
    (h : ∀ x : E, ‖A x‖ ≤ C * ‖x‖) (x : E) :
    completionOfBounded A C h (x : Completion E) = (A x : Completion E) := by
  simp [completionOfBounded]

/-- Idempotence and commutation are transferred as algebraic identities. -/
theorem completionOperator_idempotent (A : E →L[ℂ] E) (h : A * A = A) :
    completionOperator A * completionOperator A = completionOperator A := by
  rw [← completionOperator_mul, h]

theorem completionOperator_commute (A B : E →L[ℂ] E) (h : A * B = B * A) :
    completionOperator A * completionOperator B = completionOperator B * completionOperator A := by
  rw [← completionOperator_mul, ← completionOperator_mul, h]

theorem completionOperator_orthogonal (A B : E →L[ℂ] E) (h : A * B = 0) :
    completionOperator A * completionOperator B = 0 := by
  rw [← completionOperator_mul, h, completionOperator_zero]

theorem completionOperator_complete {J : Type*} [Fintype J] (A : J → E →L[ℂ] E)
    (h : ∑ j, A j = 1) : ∑ j, completionOperator (A j) = 1 := by
  rw [← completionOperator_sum, h, completionOperator_one]

end Normed

section Inner
variable [InnerProductSpace ℂ E]

/-- Inner symmetry on the pre-space passes to arbitrary vectors by density in
both variables; this does not require positive definiteness before completion. -/
theorem completionOperator_inner_symmetry (A : E →L[ℂ] E)
    (h : ∀ x y : E, ⟪A x, y⟫_ℂ = ⟪x, A y⟫_ℂ) (x y : Completion E) :
    ⟪completionOperator A x, y⟫_ℂ = ⟪x, completionOperator A y⟫_ℂ := by
  refine Completion.induction_on₂ x y (isClosed_eq (by fun_prop) (by fun_prop)) ?_
  intro u v
  simpa using h u v

/-- The completed symmetric bounded operator is selfadjoint. -/
theorem completionOperator_selfadjoint (A : E →L[ℂ] E)
    (h : ∀ x y : E, ⟪A x, y⟫_ℂ = ⟪x, A y⟫_ℂ) :
    star (completionOperator A) = completionOperator A := by
  apply ContinuousLinearMap.ext
  intro x
  apply ext_inner_right ℂ
  intro y
  change ⟪(completionOperator A).adjoint x, y⟫_ℂ = ⟪completionOperator A x, y⟫_ℂ
  rw [ContinuousLinearMap.adjoint_inner_left]
  exact (completionOperator_inner_symmetry A h x y).symm

end Inner
end CyclicBell.General.Coverage
