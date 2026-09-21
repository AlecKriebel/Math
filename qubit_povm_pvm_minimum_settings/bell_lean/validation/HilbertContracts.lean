import Bell.HilbertSimulation

/- Independent semantic contracts for arbitrary complex Hilbert spaces.
No named result is introduced in this validation file. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder TensorProduct InnerProductSpace
open Bell

variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]

-- The state is an actual endomorphism of the source tensor product, not a
-- target matrix under a new name. Both trace and positivity are source predicates.
example (ρ : Hilbert.State E F) :
    Hilbert.PositiveFor (Hilbert.jointInner E F) ρ.density ∧
      LinearMap.trace ℂ (E ⊗[ℂ] F) ρ.density = 1 := ⟨ρ.positive, ρ.normalized⟩

example (h : Module.finrank ℂ E = 0) (ρ : Hilbert.State E F) : False := by
  have := ρ.alice_finrank_pos
  omega
example (h : Module.finrank ℂ F = 0) (ρ : Hilbert.State E F) : False := by
  have := ρ.bob_finrank_pos
  omega
example {A : Architecture} (s : Hilbert.Strategy E F A) (x : Fin A.aliceInputs)
    (h : A.aliceOutputs x = 0) : False := by
  have := (s.aliceSelected x).isLt
  omega
example {A : Architecture} (s : Hilbert.Strategy E F A) (y : Fin A.bobInputs)
    (h : A.bobOutputs y = 0) : False := by
  have := (s.bobSelected y).isLt
  omega

example (hd : Module.finrank ℂ E ≤ 2) :
    ∃ V : E →ₗᵢ[ℂ] EuclideanSpace ℂ (Fin 2), ∀ x y, ⟪V x, V y⟫_ℂ = ⟪x, y⟫_ℂ :=
  ⟨Hilbert.linearIsometry (stdOrthonormalBasis ℂ E) hd,
    Hilbert.linearIsometry_inner (stdOrthonormalBasis ℂ E) hd⟩

example {A : Architecture} (s : Hilbert.Strategy E F A)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    ∃ t : Bell.Strategy A, t.behavior = s.behavior ∧
      t.state.density.PosSemidef ∧ Matrix.trace t.state.density = 1 ∧
      (∀ x, (∀ a, ((t.alice x).effect a).PosSemidef) ∧
        (∑ a, (t.alice x).effect a) = 1) ∧
      (∀ y, (∀ b, ((t.bob y).effect b).PosSemidef) ∧
        (∑ b, (t.bob y).effect b) = 1) := by
  let t := s.toQubit hE hF
  exact ⟨t, s.toQubit_behavior hE hF, t.state.positive, t.state.normalized,
    fun x => ⟨(t.alice x).positive, (t.alice x).normalized⟩,
    fun y => ⟨(t.bob y).positive, (t.bob y).normalized⟩⟩

example {A : Architecture} (s : Hilbert.ProjectiveStrategy E F A)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    ∃ t : Bell.ProjectiveStrategy A, t.toStrategy.behavior = s.toStrategy.behavior ∧
      (∀ x a, (t.alice x).effect a * (t.alice x).effect a = (t.alice x).effect a) ∧
      (∀ y b, (t.bob y).effect b * (t.bob y).effect b = (t.bob y).effect b) := by
  let t := s.toQubit hE hF
  exact ⟨t, s.toQubit_behavior hE hF, fun x => (t.alice x).idempotent,
    fun y => (t.bob y).idempotent⟩

example {A : Architecture} (s : Bell.Strategy A) :
    ∃ t : Hilbert.Strategy Hilbert.QubitSpace Hilbert.QubitSpace A,
      t.behavior = s.behavior := ⟨Hilbert.ofQubitStrategy s, Hilbert.ofQubitStrategy_behavior s⟩

example (A : Architecture) : Hilbert.rawPOVM A = Bell.rawPOVM A :=
  Hilbert.rawPOVM_eq_matrix A
example (A : Architecture) : Hilbert.rawPVM A = Bell.rawPVM A :=
  Hilbert.rawPVM_eq_matrix A

-- The new source model is consumed by the complete-strategy simulation theorem.
example (AO BO : Fin 2 → ℕ) (s : Hilbert.Strategy E F ⟨2, 2, AO, BO⟩)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → Hilbert.ProjectiveStrategy Hilbert.QubitSpace Hilbert.QubitSpace ⟨2, 2, AO, BO⟩),
      (∀ i, 0 ≤ w i) ∧ ∑ i, w i = 1 ∧
      (∑ i, w i • (t i).toStrategy.behavior) = s.behavior :=
  s.finite_projective_simulation AO BO hE hF

-- A concrete normalized one-dimensional source state exists. This checks that
-- the arbitrary dimension≤2 source endpoint is nonvacuous below dimension two.
example : Nonempty (Hilbert.State (EuclideanSpace ℂ (Fin 1)) (EuclideanSpace ℂ (Fin 1))) := by
  refine ⟨{ density := 1, positive := ?_, normalized := ?_ }⟩
  · constructor
    · intro x y
      rfl
    · intro x
      exact Hilbert.basisInner_self_nonneg _ x
  · rw [LinearMap.trace_eq_matrix_trace ℂ
      ((EuclideanSpace.basisFun (Fin 1) ℂ).toBasis.tensorProduct
        (EuclideanSpace.basisFun (Fin 1) ℂ).toBasis), LinearMap.toMatrix_one]
    norm_num [Matrix.trace, Matrix.one_apply, Fintype.sum_prod_type, Fin.sum_univ_succ]
