import Bell.Assembly

/-!
# Complete-strategy simulation and operational corollaries

These statements distinguish hull equality from raw equality. The finite
mixture may change the shared state in every branch. It selects a complete
projective strategy simultaneously, not an independent mixture for each entry.
Verification scope and current receipts are documented in CERTIFICATION.md.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators
namespace Bell

/-- Every raw two-input behavior belongs to the genuine qubit PVM hull. -/
theorem two_input_strategy_simulable (AO BO : Fin 2 → ℕ)
    (s : Strategy ⟨2,2,AO,BO⟩) :
    s.behavior ∈ convexPVM ⟨2,2,AO,BO⟩ := by
  rw [← two_input_convex_equality]
  exact subset_convexHull ℝ _ ⟨s,rfl⟩

/-- Explicit finite-mixture quantifiers for the common-randomness conclusion.
No state, outcome label, or measurement input is dropped from a branch. -/
theorem finite_projective_simulation (AO BO : Fin 2 → ℕ)
    (s : Strategy ⟨2,2,AO,BO⟩) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → ProjectiveStrategy ⟨2,2,AO,BO⟩),
      (∀ i, 0 ≤ w i) ∧ ∑ i, w i=1 ∧
      (∑ i, w i • (t i).toStrategy.behavior)=s.behavior := by
  classical
  have hp := two_input_strategy_simulable AO BO s
  change s.behavior ∈ convexHull ℝ (rawPVM ⟨2,2,AO,BO⟩) at hp
  obtain ⟨ι,hi,w,p,hw,hn,hp,he⟩ := mem_convexHull_iff_exists_fintype.mp hp
  letI : Fintype ι := hi
  choose t ht using hp
  refine ⟨ι,hi,w,t,hw,hn,?_⟩
  simpa only [ht] using he

/-- The paper's one-binary-party assertion follows, in particular, from the
arbitrary-output equality. The earlier BinaryParty module supplies the
independent binary-PVM case actually used inside the main proof. -/
theorem one_binary_party_simulation (AO : Fin 2 → ℕ)
    (s : Strategy ⟨2,2,AO,fun _ => 2⟩) :
    s.behavior ∈ convexPVM ⟨2,2,AO,fun _ => 2⟩ :=
  two_input_strategy_simulable AO (fun _ => 2) s

/-- An upper bound valid for every physical projective strategy is already
valid for every physical two-input POVM strategy. -/
theorem two_input_linear_bound_transfer (AO BO : Fin 2 → ℕ)
    (f : Behavior ⟨2,2,AO,BO⟩ →ₗ[ℝ] ℝ) (U : ℝ)
    (h : ∀ t : ProjectiveStrategy ⟨2,2,AO,BO⟩, f t.toStrategy.behavior ≤ U)
    (s : Strategy ⟨2,2,AO,BO⟩) : f s.behavior ≤ U := by
  apply linear_bound_on_convexHull f (rawPVM ⟨2,2,AO,BO⟩) U
    (by rintro p ⟨t,rfl⟩; exact h t)
  exact two_input_strategy_simulable AO BO s

/-- Equality of support-bound predicates, without introducing an unbounded
supremum or claiming equality of raw nonconvex images. -/
theorem two_input_linear_bound_iff (AO BO : Fin 2 → ℕ)
    (f : Behavior ⟨2,2,AO,BO⟩ →ₗ[ℝ] ℝ) (U : ℝ) :
    (∀ s : Strategy ⟨2,2,AO,BO⟩, f s.behavior ≤ U) ↔
      (∀ t : ProjectiveStrategy ⟨2,2,AO,BO⟩, f t.toStrategy.behavior ≤ U) := by
  constructor
  · intro h t
    exact h t.toStrategy
  · intro h s
    exact two_input_linear_bound_transfer AO BO f U h s

end Bell
