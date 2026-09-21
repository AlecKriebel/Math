import Bell.HilbertReverse
import Bell.SimulationCorollaries

/-! # The physical dimension-at-most-two model and the main simulation theorem

The union below allows arbitrary complex finite-dimensional Hilbert carriers,
including zero-dimensional carriers (which admit no normalized states). Its raw
sets coincide with the fixed-qubit matrix model. This is a union over local
spaces, not raw equality for a fixed one-dimensional carrier.
-/
noncomputable section
open scoped BigOperators TensorProduct
namespace Bell.Hilbert

/-- A local physical Hilbert space with the stated dimension upper bound. -/
structure Space where
  carrier : Type
  [normed : NormedAddCommGroup carrier]
  [inner : InnerProductSpace ℂ carrier]
  [finite : FiniteDimensional ℂ carrier]
  dimension : Module.finrank ℂ carrier ≤ 2

attribute [instance] Space.normed Space.inner Space.finite
instance : CoeSort Space Type := ⟨Space.carrier⟩

def qubitSpace : Space where
  carrier := QubitSpace
  dimension := qubitSpace_finrank.le

/-- Raw behaviors from independent operator strategies on arbitrary allowed
local Hilbert spaces, with no convexification in this definition. -/
def rawPOVM (A : Architecture) : Set (Behavior A) :=
  {p | ∃ (E F : Space) (s : Strategy E F A), s.behavior = p}

def rawPVM (A : Architecture) : Set (Behavior A) :=
  {p | ∃ (E F : Space) (s : ProjectiveStrategy E F A), s.toStrategy.behavior = p}

def convexPOVM (A : Architecture) : Set (Behavior A) := convexHull ℝ (rawPOVM A)
def convexPVM (A : Architecture) : Set (Behavior A) := convexHull ℝ (rawPVM A)

theorem rawPOVM_eq_matrix (A : Architecture) : rawPOVM A = Bell.rawPOVM A := by
  ext p
  constructor
  · rintro ⟨E, F, s, rfl⟩
    exact s.behavior_mem_rawPOVM E.dimension F.dimension
  · rintro ⟨s, rfl⟩
    exact ⟨qubitSpace, qubitSpace, ofQubitStrategy s, ofQubitStrategy_behavior s⟩

theorem rawPVM_eq_matrix (A : Architecture) : rawPVM A = Bell.rawPVM A := by
  ext p
  constructor
  · rintro ⟨E, F, s, rfl⟩
    exact s.behavior_mem_rawPVM E.dimension F.dimension
  · rintro ⟨s, rfl⟩
    exact ⟨qubitSpace, qubitSpace, ofQubitProjectiveStrategy s,
      ofQubitProjectiveStrategy_behavior s⟩

theorem convexPOVM_eq_matrix (A : Architecture) : convexPOVM A = Bell.convexPOVM A := by
  rw [convexPOVM, rawPOVM_eq_matrix]
  rfl

theorem convexPVM_eq_matrix (A : Architecture) : convexPVM A = Bell.convexPVM A := by
  rw [convexPVM, rawPVM_eq_matrix]
  rfl

/-- The two-input equality for the independent physical Hilbert-space model. -/
theorem two_input_convex_equality (AO BO : Fin 2 → ℕ) :
    convexPOVM ⟨2, 2, AO, BO⟩ = convexPVM ⟨2, 2, AO, BO⟩ := by
  rw [convexPOVM_eq_matrix, convexPVM_eq_matrix]
  exact Bell.two_input_convex_equality AO BO

variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]

/-- Complete-strategy finite simulation consumed through the new source model.
Every branch is an actual projective Hilbert-space strategy on complex C²;
one shared random index selects both parties and the joint state together. -/
theorem Strategy.finite_projective_simulation (AO BO : Fin 2 → ℕ)
    (s : Strategy E F ⟨2, 2, AO, BO⟩)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → ProjectiveStrategy QubitSpace QubitSpace ⟨2, 2, AO, BO⟩),
      (∀ i, 0 ≤ w i) ∧ ∑ i, w i = 1 ∧
      (∑ i, w i • (t i).toStrategy.behavior) = s.behavior := by
  obtain ⟨ι, hi, w, t, hw, hn, he⟩ :=
    Bell.finite_projective_simulation AO BO (s.toQubit hE hF)
  letI : Fintype ι := hi
  refine ⟨ι, hi, w, fun i => ofQubitProjectiveStrategy (t i), hw, hn, ?_⟩
  simpa only [ofQubitProjectiveStrategy_behavior, s.toQubit_behavior hE hF] using he

end Bell.Hilbert
