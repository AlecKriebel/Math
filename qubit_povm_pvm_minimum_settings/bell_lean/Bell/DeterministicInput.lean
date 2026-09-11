import Bell.OneInput

/-!
# Complete physical deterministic-input replacement

One common random variable specifies every Alice output and both Bob outputs.
The output alphabet is the padded binary/ternary architecture, so unused labels
and zero marginal probabilities are included. The conclusion concerns the
actual complex-qubit PVM convex hull, not a coefficient-space surrogate.

This is proof source for subsequent compilation; no build is claimed here.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder

namespace Bell.ClassicalProduct

variable {X : Type*} [Fintype X] [DecidableEq X]
variable {O : X → Type*} [∀ x, Fintype (O x)] [∀ x, DecidableEq (O x)]
variable {B : Type*} [Fintype B] [DecidableEq B]

theorem reconstruction_alice_marginal (p : Table O B) (q : B → ℝ)
    (hp : ∀ x a b, 0 ≤ p x a b)
    (hrow : ∀ x b, ∑ a, p x a b = q b)
    (x : X) (a : O x) :
    (∑ k : B × Assignment O,
      weight p q k * (if a = k.2 x then 1 else 0)) = ∑ b, p x a b := by
  calc
    (∑ k : B × Assignment O, weight p q k * (if a = k.2 x then 1 else 0)) =
        ∑ b, ∑ k : B × Assignment O,
          weight p q k * (if a = k.2 x ∧ b = k.1 then 1 else 0) := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro k _
      by_cases ha : a = k.2 x
      · simp [ha, ← Finset.mul_sum]
      · simp [ha]
    _ = ∑ b, p x a b := by
      apply Finset.sum_congr rfl
      intro b _
      exact reconstruction p q hp hrow x a b

theorem reconstruction_with_deterministic_input (p : Table O B) (q : B → ℝ)
    (hp : ∀ x a b, 0 ≤ p x a b)
    (hrow : ∀ x b, ∑ a, p x a b = q b)
    (d : Fin 2) (label : B) (x : X) (y : Fin 2) (a : O x) (b : B) :
    (∑ k : B × Assignment O,
      weight p q k *
        (if a = k.2 x ∧ b = (if y = d then label else k.1) then 1 else 0)) =
      if y = d then (∑ c, p x a c) * (if b = label then 1 else 0)
      else p x a b := by
  by_cases hy : y = d
  · by_cases hb : b = label
    · simpa only [if_pos hy, hb, and_true, if_pos rfl, ite_true, mul_one] using
        reconstruction_alice_marginal p q hp hrow x a
    · simp [hy, hb]
  · simpa only [if_neg hy] using reconstruction p q hp hrow x a b

end Bell.ClassicalProduct

namespace Bell

def otherInput (d : Fin 2) : Fin 2 := if d = 0 then 1 else 0

@[simp]
theorem otherInput_ne (d : Fin 2) : otherInput d ≠ d := by
  fin_cases d <;> norm_num [otherInput]

theorem eq_otherInput_of_ne (d y : Fin 2) (hy : y ≠ d) : y = otherInput d := by
  fin_cases d <;> fin_cases y <;> norm_num [otherInput] at hy ⊢

def replaceBobInput (s : Strategy binaryTernaryArchitecture)
    (d : Fin 2) (label : Fin 3) : Strategy binaryTernaryArchitecture where
  state := s.state
  alice := s.alice
  bob := fun y => if y = d then (deterministicPVM 3 label).toPOVM else s.bob y

theorem born_deterministic (ρ : JointOperator) (M : Operator) (label b : Fin 3) :
    born ρ M ((deterministicPVM 3 label).effect b) =
      born ρ M 1 * (if b = label then 1 else 0) := by
  by_cases hb : b = label
  · simp [deterministicPVM, hb]
  · simp [deterministicPVM, hb, born, tensor_zero_right]

theorem replacement_behavior (s : Strategy binaryTernaryArchitecture)
    (d : Fin 2) (label : Fin 3) (x y : Fin 2) (a b : Fin 3) :
    (replaceBobInput s d label).behavior x y a b =
      if y = d then
        (∑ c : Fin 3, s.behavior x (otherInput d) a c) *
          (if b = label then 1 else 0)
      else s.behavior x (otherInput d) a b := by
  by_cases hy : y = d
  · subst y
    simp only [replaceBobInput, Strategy.behavior, if_pos rfl, ite_true]
    rw [born_deterministic, born_sum_bob]
    rfl
  · have ho := eq_otherInput_of_ne d y hy
    subst y
    simp [replaceBobInput, Strategy.behavior, otherInput_ne]

/-- Physical membership after replacing either entire Bob input. -/
theorem replaceBobInput_mem_convexPVM (s : Strategy binaryTernaryArchitecture)
    (d : Fin 2) (label : Fin 3) :
    (replaceBobInput s d label).behavior ∈ convexPVM binaryTernaryArchitecture := by
  classical
  let p : ClassicalProduct.Table (fun _ : Fin 2 => Fin 3) (Fin 3) :=
    fun x a b => s.behavior x (otherInput d) a b
  let q : Fin 3 → ℝ := fun b =>
    expectation s.state.density (tensor 1 ((s.bob (otherInput d)).effect b))
  have hp : ∀ x a b, 0 ≤ p x a b :=
    fun x a b => strategy_behavior_nonnegative s x (otherInput d) a b
  have hq : ∀ b, 0 ≤ q b := by
    intro b
    exact state_expectation_positive s.state
      (tensor_positive (Matrix.PosSemidef.one : (1 : Operator).PosSemidef)
        ((s.bob (otherInput d)).positive b))
  have hrow : ∀ x b, ∑ a, p x a b = q b := by
    intro x b
    exact born_sum_alice s.state (s.alice x) ((s.bob (otherInput d)).effect b)
  have hqsum : ∑ b, q b = 1 := by
    change (∑ b, expectation s.state.density
      (tensor 1 ((s.bob (otherInput d)).effect b))) = 1
    rw [← map_sum, ← tensor_sum_right, (s.bob (otherInput d)).normalized,
      tensor_one_one, state_expectation_one]
  let w := ClassicalProduct.weight p q
  let α := fun k : Fin 3 × (Fin 2 → Fin 3) => k.2
  let β := fun k : Fin 3 × (Fin 2 → Fin 3) =>
    fun y : Fin 2 => if y = d then label else k.1
  have hc := finite_local_mixture_mem_convexPVM binaryTernaryArchitecture
    w α β (ClassicalProduct.weight_nonnegative p q hp hq)
    (ClassicalProduct.weight_normalized p q hrow hqsum)
  have heq : (∑ k, w k • deterministicTable binaryTernaryArchitecture (α k) (β k)) =
      (replaceBobInput s d label).behavior := by
    funext x y a b
    rw [replacement_behavior]
    simpa only [w, α, β, deterministicTable, Finset.sum_apply,
      Pi.smul_apply, smul_eq_mul, p] using
      ClassicalProduct.reconstruction_with_deterministic_input p q hp hrow
        d label x y a b
  rw [heq] at hc
  exact hc

def rayInput (j : Fin 5) : Fin 2 := if j.val < 2 then 0 else 1

def rayLabel (j : Fin 5) : Fin 3 :=
  if h : j.val < 2 then ⟨j.val, by omega⟩
  else ⟨j.val - 2, by have hj := j.isLt; omega⟩

def replaceBobRay (s : Strategy binaryTernaryArchitecture) (j : Fin 5) :
    Strategy binaryTernaryArchitecture := replaceBobInput s (rayInput j) (rayLabel j)

theorem replaceBobRay_mem_convexPVM (s : Strategy binaryTernaryArchitecture) (j : Fin 5) :
    (replaceBobRay s j).behavior ∈ convexPVM binaryTernaryArchitecture :=
  replaceBobInput_mem_convexPVM s (rayInput j) (rayLabel j)

theorem strict_gap_to_deterministic_replacements
    (s : Strategy binaryTernaryArchitecture)
    (f : Behavior binaryTernaryArchitecture →ₗ[ℝ] ℝ)
    (hstrict : ∀ p ∈ convexPVM binaryTernaryArchitecture, f p < f s.behavior) :
    ∀ j, f (replaceBobRay s j).behavior < f s.behavior := by
  intro j
  exact hstrict _ (replaceBobRay_mem_convexPVM s j)

end Bell
