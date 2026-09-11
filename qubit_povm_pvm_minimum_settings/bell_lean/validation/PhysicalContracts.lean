import Bell

/- Independent supplementary semantic contracts. Run only after the production
umbrella builds. These statements expose the physical and numerical predicates
behind the public proposition aliases; they do not modify any definition. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
open Bell

example {n : ℕ} (M : POVM n) :
    (∀ a, (M.effect a).PosSemidef) ∧ (∑ a, M.effect a) = 1 :=
  ⟨M.positive, M.normalized⟩

example {A : Architecture} (s : Strategy A) (x y a b) :
    0 ≤ s.behavior x y a b := strategy_behavior_nonnegative s x y a b
example {A : Architecture} (s : Strategy A) (x y) :
    (∑ a, ∑ b, s.behavior x y a b) = 1 := strategy_behavior_normalization s x y
example {A : Architecture} (s : Strategy A) (x y y' a) :
    (∑ b, s.behavior x y a b) = ∑ b, s.behavior x y' a b :=
  strategy_no_signaling_to_alice s x y y' a
example {A : Architecture} (s : Strategy A) (x x' y b) :
    (∑ a, s.behavior x y a b) = ∑ a, s.behavior x' y a b :=
  strategy_no_signaling_to_bob s x x' y b

-- MainClaims expanded through every proposition alias and scalar constant.
example :
    (∀ A : Architecture, A.aliceInputs = 2 → A.bobInputs = 2 →
      convexPOVM A = convexPVM A) ∧
    (∀ A : Architecture, (A.aliceInputs ≤ 1 ∨ A.bobInputs ≤ 1) →
      convexPOVM A = convexPVM A) ∧
    (∀ p ∈ rawPVM separatorArchitecture,
      bellScore p ≤ 20 * Real.sqrt 2 + 3 / 5 + (4 + 3 * Real.sqrt 2) / 250) ∧
    (∃ (f : Behavior separatorArchitecture →ₗ[ℝ] ℝ)
      (p : Behavior separatorArchitecture),
      p ∈ convexPOVM separatorArchitecture ∧
      ∀ q ∈ convexPVM separatorArchitecture, f q < f p) := main_claims

example : witnessBehavior ∈ rawPOVM separatorArchitecture ∧
    bellScore witnessBehavior = 20 * Real.sqrt 2 + 16 / 25 :=
  ⟨witness_mem_raw, witness_value⟩
example :
    (∀ p ∈ convexPVM separatorArchitecture, bellScore p ≤ (289 / 10 : ℝ)) :=
  convex_projective_rational_upper
example :
    (20 * Real.sqrt 2 + 16 / 25) -
      (20 * Real.sqrt 2 + 3 / 5 + (4 + 3 * Real.sqrt 2) / 250) =
      3 * (2 - Real.sqrt 2) / 250 := gap_identity

example (A : Architecture) (ha : A.aliceInputs ≤ 2) (hb : A.bobInputs ≤ 2) :
    convexPOVM A = convexPVM A := at_most_two_input_equality A ha hb
example : MainClaims ∧
    (∃ p ∈ rawPOVM separatorArchitecture,
      bellScore p = (16 + 8 * Real.sqrt 7813) / 25) := main_claims_with_strengthening
