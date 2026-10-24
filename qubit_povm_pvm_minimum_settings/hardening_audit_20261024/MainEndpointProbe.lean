import Bell.HilbertFiniteLabels

/- Fresh independent endpoint contract: actual source tensor traces and actual
projective endomorphisms, with one common finite branch distribution. -/
noncomputable section
open scoped BigOperators TensorProduct InnerProductSpace
open Bell
universe u v
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]
variable (AO : Fin 2 → Type u) (BO : Fin 2 → Type v)
  [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]

example (s : HilbertFiniteLabels.Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → HilbertFiniteLabels.ProjectiveStrategy Hilbert.QubitSpace Hilbert.QubitSpace AO BO),
      (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
      (∀ i x a, ((t i).alice x).effect a * ((t i).alice x).effect a = ((t i).alice x).effect a) ∧
      (∀ i y b, ((t i).bob y).effect b * ((t i).bob y).effect b = ((t i).bob y).effect b) ∧
      (∀ x y a b,
        (∑ i, w i *
          (LinearMap.trace ℂ (Hilbert.QubitSpace ⊗[ℂ] Hilbert.QubitSpace)
            ((t i).state.density * TensorProduct.map
              (((t i).alice x).effect a) (((t i).bob y).effect b))).re) =
        (LinearMap.trace ℂ (E ⊗[ℂ] F)
          (s.state.density * TensorProduct.map ((s.alice x).effect a) ((s.bob y).effect b))).re) := by
  obtain ⟨ι, hi, w, t, hw, hsum, he⟩ :=
    HilbertFiniteLabels.finite_source_projective_simulation AO BO s hE hF (by omega) (by omega)
  letI : Fintype ι := hi
  refine ⟨ι, hi, w, t, hw, hsum, ?_, ?_, ?_⟩
  · intro i x a
    exact ((t i).alice x).idempotent a
  · intro i y b
    exact ((t i).bob y).idempotent b
  · intro x y a b
    have h := congrFun (congrFun (congrFun (congrFun he x) y) a) b
    simpa [HilbertFiniteLabels.Strategy.behavior,
      HilbertFiniteLabels.ProjectiveStrategy.toStrategy, Hilbert.born] using h

#print axioms Bell.two_input_convex_equality
#print axioms Bell.HilbertFiniteLabels.finite_source_projective_simulation
#print axioms Bell.HilbertFiniteLabels.at_most_two_input_equality
