import Bell.HilbertFiniteLabels

/- Anonymous contracts for the composed source model, rather than two
independent bridges that are never applied to the same physical strategy. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder TensorProduct InnerProductSpace
open Bell

universe u v
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]
variable {m n : ℕ} (AO : Fin m → Type u) (BO : Fin n → Type v)
  [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]

example {α : Type u} [Fintype α] (M : HilbertFiniteLabels.POVM E α) :
    (∀ a, Hilbert.PositiveFor (fun x y : E => ⟪x, y⟫_ℂ) (M.effect a)) ∧
      (∑ a, M.effect a) = 1 := ⟨M.positive, M.normalized⟩

example {α : Type u} [Fintype α] (M : HilbertFiniteLabels.PVM E α) :
    (∀ a, M.effect a * M.effect a = M.effect a) ∧
      (∀ a b, a ≠ b → M.effect a * M.effect b = 0) := ⟨M.idempotent, M.orthogonal⟩

example (s : HilbertFiniteLabels.Strategy E F AO BO) (x y a b) :
    s.behavior AO BO x y a b =
      (LinearMap.trace ℂ (E ⊗[ℂ] F)
        (s.state.density * TensorProduct.map ((s.alice x).effect a) ((s.bob y).effect b))).re := rfl

example (s : HilbertFiniteLabels.Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    ∃ t : FiniteLabels.Strategy AO BO,
      t.behavior AO BO = s.behavior AO BO ∧
      t.state.density.PosSemidef ∧ Matrix.trace t.state.density = 1 ∧
      (∀ x, (∑ a, (t.alice x).effect a) = 1) ∧
      (∀ y, (∑ b, (t.bob y).effect b) = 1) := by
  let t := s.toQubit AO BO hE hF
  exact ⟨t, s.toQubit_behavior AO BO hE hF, t.state.positive, t.state.normalized,
    fun x => (t.alice x).normalized, fun y => (t.bob y).normalized⟩

example (s : HilbertFiniteLabels.ProjectiveStrategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    ∃ t : FiniteLabels.ProjectiveStrategy AO BO,
      (t.toStrategy AO BO).behavior AO BO = (s.toStrategy AO BO).behavior AO BO :=
  ⟨s.toQubit AO BO hE hF, s.toQubit_behavior AO BO hE hF⟩

example (s : FiniteLabels.Strategy AO BO) :
    ∃ t : HilbertFiniteLabels.Strategy Hilbert.QubitSpace Hilbert.QubitSpace AO BO,
      t.behavior AO BO = s.behavior AO BO :=
  ⟨HilbertFiniteLabels.ofQubitStrategy AO BO s, HilbertFiniteLabels.ofQubitStrategy_behavior AO BO s⟩

example : HilbertFiniteLabels.rawPOVM AO BO = FiniteLabels.rawPOVM AO BO :=
  HilbertFiniteLabels.rawPOVM_eq_fixed AO BO
example : HilbertFiniteLabels.rawPVM AO BO = FiniteLabels.rawPVM AO BO :=
  HilbertFiniteLabels.rawPVM_eq_fixed AO BO

example (hm : m ≤ 2) (hn : n ≤ 2) :
    convexHull ℝ (HilbertFiniteLabels.rawPOVM AO BO) =
      convexHull ℝ (HilbertFiniteLabels.rawPVM AO BO) :=
  HilbertFiniteLabels.at_most_two_input_equality AO BO hm hn

example (s : HilbertFiniteLabels.Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2)
    (hm : m ≤ 2) (hn : n ≤ 2) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → HilbertFiniteLabels.ProjectiveStrategy Hilbert.QubitSpace Hilbert.QubitSpace AO BO),
      (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
        (∑ i, w i • ((t i).toStrategy AO BO).behavior AO BO) = s.behavior AO BO :=
  HilbertFiniteLabels.finite_source_projective_simulation AO BO s hE hF hm hn

example (x : Fin m) [IsEmpty (AO x)] : IsEmpty (HilbertFiniteLabels.Strategy E F AO BO) :=
  HilbertFiniteLabels.no_strategy_of_empty_alice AO BO x
example (y : Fin n) [IsEmpty (BO y)] : IsEmpty (HilbertFiniteLabels.Strategy E F AO BO) :=
  HilbertFiniteLabels.no_strategy_of_empty_bob AO BO y

example (s : HilbertFiniteLabels.Strategy E F AO BO) (h : Module.finrank ℂ E = 0) : False := by
  have := s.state.alice_finrank_pos
  omega
