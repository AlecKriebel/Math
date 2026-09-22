import Bell.HilbertFiniteLabels

noncomputable section
open scoped BigOperators TensorProduct
namespace IndependentHilbertProbe

variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]

theorem no_zero_alice_state (hE : Module.finrank ℂ E = 0) :
    IsEmpty (Bell.Hilbert.State E F) := by
  refine ⟨fun s => ?_⟩
  have h := s.alice_finrank_pos
  omega

theorem no_zero_bob_state (hF : Module.finrank ℂ F = 0) :
    IsEmpty (Bell.Hilbert.State E F) := by
  refine ⟨fun s => ?_⟩
  have h := s.bob_finrank_pos
  omega

universe u v
variable {m n : ℕ} (AO : Fin m → Type u) (BO : Fin n → Type v)
  [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]

theorem actual_trace_mixture
    (s : Bell.HilbertFiniteLabels.Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2)
    (hm : m ≤ 2) (hn : n ≤ 2) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → Bell.HilbertFiniteLabels.ProjectiveStrategy
        Bell.Hilbert.QubitSpace Bell.Hilbert.QubitSpace AO BO),
      (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
      ∀ x y a b,
        (∑ i, w i * (LinearMap.trace ℂ
          (Bell.Hilbert.QubitSpace ⊗[ℂ] Bell.Hilbert.QubitSpace)
          ((t i).state.density * TensorProduct.map
            (((t i).alice x).effect a) (((t i).bob y).effect b))).re) =
        (LinearMap.trace ℂ (E ⊗[ℂ] F)
          (s.state.density * TensorProduct.map
            ((s.alice x).effect a) ((s.bob y).effect b))).re := by
  obtain ⟨ι, hi, w, t, hw, hsum, he⟩ :=
    Bell.HilbertFiniteLabels.finite_source_projective_simulation AO BO s hE hF hm hn
  letI : Fintype ι := hi
  refine ⟨ι, hi, w, t, hw, hsum, ?_⟩
  intro x y a b
  have h := congrArg (fun p => p x y a b) he
  simpa [Bell.HilbertFiniteLabels.Strategy.behavior,
    Bell.HilbertFiniteLabels.ProjectiveStrategy.toStrategy, Bell.Hilbert.born] using h

#print axioms no_zero_alice_state
#print axioms no_zero_bob_state
#print axioms actual_trace_mixture
end IndependentHilbertProbe
