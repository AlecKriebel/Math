import Bell

/-! Handoff statement contracts. These examples must be ELABORATED after the
full build. Textual existence or `#check` alone does not validate the contracts.
This file changes no physical definition and adds no theorem assumption.
It checks the concrete complex-qubit model, hull rather than raw equality,
complete-strategy mixtures, quantitative separation and boundary alphabets.
No success is claimed until the offline compiler accepts this file. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
open Bell

-- The Hilbert spaces really are complex 2 and 2-by-2 spaces.
example : Operator = Matrix (Fin 2) (Fin 2) ℂ := rfl
example : JointOperator = Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ := rfl

-- Check the measurement/state validity fields, not just a proposition's name.
example (ρ : State) : ρ.density.PosSemidef ∧ Matrix.trace ρ.density = 1 :=
  ⟨ρ.positive, ρ.normalized⟩
example {n : ℕ} (M : PVM n) :
    (∀ a, (M.effect a).PosSemidef) ∧ (∑ a, M.effect a) = 1 ∧
      (∀ a, M.effect a * M.effect a = M.effect a) ∧
      (∀ a b, a ≠ b → M.effect a * M.effect b = 0) :=
  ⟨M.positive, M.normalized, M.idempotent, M.orthogonal⟩
example (ρ : JointOperator) (M N : Operator) :
    born ρ M N =
      (Matrix.trace (ρ * (fun i j => M i.1 j.1 * N i.2 j.2))).re := rfl

-- Actual set ranges and ordinary convex hulls, with dependent finite outputs.
example (AO BO : Fin 2 → ℕ) :
    convexHull ℝ (Set.range (Strategy.behavior (A := ⟨2,2,AO,BO⟩))) =
    convexHull ℝ (Set.range (fun s : ProjectiveStrategy ⟨2,2,AO,BO⟩ =>
      s.toStrategy.behavior)) :=
  two_input_convex_equality AO BO

-- One finite random variable chooses every measurement AND the state.
example (AO BO : Fin 2 → ℕ) (s : Strategy ⟨2,2,AO,BO⟩) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → ProjectiveStrategy ⟨2,2,AO,BO⟩),
      (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
        (∑ i, w i • (t i).toStrategy.behavior) = s.behavior :=
  finite_projective_simulation AO BO s

-- No positive-output-count hypothesis was introduced into equality.
example : convexPOVM ⟨2,2,(fun _ => 0),(fun _ => 3)⟩ =
    convexPVM ⟨2,2,(fun _ => 0),(fun _ => 3)⟩ :=
  two_input_convex_equality _ _
example (AO : Fin 0 → ℕ) (BO : Fin 5 → ℕ) :
    convexPOVM ⟨0,5,AO,BO⟩ = convexPVM ⟨0,5,AO,BO⟩ :=
  one_input_equality _ (Or.inl (by decide))

-- Verify the attained-value quantifier and global physical comparison.
example : ∃ p ∈ rawPOVM separatorArchitecture,
    bellScore p = (16 + 8 * Real.sqrt 7813) / 25 := strengthened_attainment
example (s : ProjectiveStrategy separatorArchitecture) :
    bellScore s.toStrategy.behavior ≤ (289 / 10 : ℝ) :=
  projective_strategy_rational_upper s
example : StrictSeparation separatorArchitecture := three_by_two_separation
example : separatorArchitecture.aliceInputs = 3 ∧ separatorArchitecture.bobInputs = 2 :=
  ⟨rfl, rfl⟩
example (A : Architecture) (h : StrictSeparation A) :
    (3 ≤ A.aliceInputs ∧ 2 ≤ A.bobInputs) ∨
      (2 ≤ A.aliceInputs ∧ 3 ≤ A.bobInputs) := minimum_inputs A h
