import Bell.ClassicalProduct
import Bell.Expectation
import Bell.Targets

/-!
# One-input equality in the actual complex-qubit behavior model

The product-response construction uses one common hidden variable selecting all
measurement outputs. Its weights are nonnegative and normalized, including zero
marginal probabilities. The final mixture consists of the actual identity/zero
qubit PVM strategies in `LocalSimulation`.

Zero-input architectures and empty declared output alphabets are not discarded:
a physical POVM supplies a positive output count, and a zero-input behavior has
no entries on which it can differ from the displayed deterministic strategy.

STATUS: uncompiled proof source.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

/-- A normalized finite POVM cannot have no declared outputs. -/
theorem povm_output_positive {n : ℕ} (M : POVM n) : 0 < n := by
  by_contra hn
  have hz : n = 0 := by omega
  subst n
  have h := congrArg (fun X : Operator => X 0 0) M.normalized
  norm_num [Matrix.one_apply] at h

def defaultOutput {n : ℕ} (M : POVM n) : Fin n := ⟨0,povm_output_positive M⟩

/-- Transport of a label to the unique input of a dependent singleton family. -/
def singleOutput (O : Fin 1 → ℕ) (a : Fin (O 0)) : (x : Fin 1) → Fin (O x) :=
  fun x => Fin.cast (congrArg O (Subsingleton.elim (0 : Fin 1) x)) a

@[simp]
theorem singleOutput_zero (O : Fin 1 → ℕ) (a : Fin (O 0)) : singleOutput O a 0 = a := rfl

theorem strategy_no_inputs {A : Architecture} (s : Strategy A)
    (hz : A.aliceInputs = 0 ∨ A.bobInputs = 0) : s.behavior ∈ convexPVM A := by
  let α := fun x => defaultOutput (s.alice x)
  let β := fun y => defaultOutput (s.bob y)
  have hd : deterministicTable A α β ∈ convexPVM A :=
    subset_convexHull ℝ (rawPVM A) (deterministic_mem_rawPVM A α β)
  have heq : s.behavior = deterministicTable A α β := by
    funext x y a b
    rcases hz with ha | hb
    · have hx := x.isLt
      have hf : False := by omega
      exact hf.elim
    · have hy := y.isLt
      have hf : False := by omega
      exact hf.elim
  rw [heq]
  exact hd

/-- Arbitrary Alice inputs and arbitrary dependent finite alphabets, one Bob input. -/
theorem strategy_single_bob {n : ℕ} (AO : Fin n → ℕ) (BO : Fin 1 → ℕ)
    (s : Strategy ⟨n,1,AO,BO⟩) : s.behavior ∈ convexPVM ⟨n,1,AO,BO⟩ := by
  classical
  let p : ClassicalProduct.Table (fun x : Fin n => Fin (AO x)) (Fin (BO 0)) :=
    fun x a b => s.behavior x 0 a b
  let q : Fin (BO 0) → ℝ :=
    fun b => expectation s.state.density (tensor 1 ((s.bob 0).effect b))
  have hp : ∀ x a b, 0 ≤ p x a b := fun x a b => strategy_behavior_nonnegative s x 0 a b
  have hq : ∀ b, 0 ≤ q b := by
    intro b
    exact state_expectation_positive s.state
      (tensor_positive (Matrix.PosSemidef.one : (1 : Operator).PosSemidef)
        ((s.bob 0).positive b))
  have hrow : ∀ x b, ∑ a, p x a b = q b := by
    intro x b
    exact born_sum_alice s.state (s.alice x) ((s.bob 0).effect b)
  have hqsum : ∑ b, q b = 1 := by
    change (∑ b, expectation s.state.density (tensor 1 ((s.bob 0).effect b))) = 1
    rw [← map_sum, ← tensor_sum_right, (s.bob 0).normalized,
      tensor_one_one, state_expectation_one]
  let w := ClassicalProduct.weight p q
  let α := fun k : Fin (BO 0) × ((x : Fin n) → Fin (AO x)) => k.2
  let β := fun k : Fin (BO 0) × ((x : Fin n) → Fin (AO x)) => singleOutput BO k.1
  have hc := finite_local_mixture_mem_convexPVM (⟨n,1,AO,BO⟩ : Architecture)
    w α β (ClassicalProduct.weight_nonnegative p q hp hq)
    (ClassicalProduct.weight_normalized p q hrow hqsum)
  have heq : (∑ k, w k • deterministicTable ⟨n,1,AO,BO⟩ (α k) (β k)) = s.behavior := by
    funext x y a b
    have hy : y = 0 := Subsingleton.elim _ _
    subst y
    simpa only [α, β, w, deterministicTable, singleOutput_zero,
      Finset.sum_apply, Pi.smul_apply, smul_eq_mul, p] using
      (ClassicalProduct.reconstruction p q hp hrow x a b)
  rw [heq] at hc
  exact hc

/-- The symmetric construction does not require a state-swap lemma or a real-qubit restriction. -/
theorem strategy_single_alice {n : ℕ} (AO : Fin 1 → ℕ) (BO : Fin n → ℕ)
    (s : Strategy ⟨1,n,AO,BO⟩) : s.behavior ∈ convexPVM ⟨1,n,AO,BO⟩ := by
  classical
  let p : ClassicalProduct.Table (fun y : Fin n => Fin (BO y)) (Fin (AO 0)) :=
    fun y b a => s.behavior 0 y a b
  let q : Fin (AO 0) → ℝ :=
    fun a => expectation s.state.density (tensor ((s.alice 0).effect a) 1)
  have hp : ∀ y b a, 0 ≤ p y b a := fun y b a => strategy_behavior_nonnegative s 0 y a b
  have hq : ∀ a, 0 ≤ q a := by
    intro a
    exact state_expectation_positive s.state
      (tensor_positive ((s.alice 0).positive a)
        (Matrix.PosSemidef.one : (1 : Operator).PosSemidef))
  have hrow : ∀ y a, ∑ b, p y b a = q a := by
    intro y a
    exact born_sum_bob s.state ((s.alice 0).effect a) (s.bob y)
  have hqsum : ∑ a, q a = 1 := by
    change (∑ a, expectation s.state.density (tensor ((s.alice 0).effect a) 1)) = 1
    rw [← map_sum, ← tensor_sum_left, (s.alice 0).normalized,
      tensor_one_one, state_expectation_one]
  let w := ClassicalProduct.weight p q
  let α := fun k : Fin (AO 0) × ((y : Fin n) → Fin (BO y)) => singleOutput AO k.1
  let β := fun k : Fin (AO 0) × ((y : Fin n) → Fin (BO y)) => k.2
  have hc := finite_local_mixture_mem_convexPVM (⟨1,n,AO,BO⟩ : Architecture)
    w α β (ClassicalProduct.weight_nonnegative p q hp hq)
    (ClassicalProduct.weight_normalized p q hrow hqsum)
  have heq : (∑ k, w k • deterministicTable ⟨1,n,AO,BO⟩ (α k) (β k)) = s.behavior := by
    funext x y a b
    have hx : x = 0 := Subsingleton.elim _ _
    subst x
    simpa only [α, β, w, deterministicTable, singleOutput_zero,
      Finset.sum_apply, Pi.smul_apply, smul_eq_mul, p, and_comm] using
      (ClassicalProduct.reconstruction p q hp hrow y b a)
  rw [heq] at hc
  exact hc

/-- Complete finite-input case split, with both zero-input degeneracies retained. -/
theorem strategy_one_input {A : Architecture} (s : Strategy A)
    (h : A.aliceInputs ≤ 1 ∨ A.bobInputs ≤ 1) : s.behavior ∈ convexPVM A := by
  rcases h with ha | hb
  · by_cases hz : A.aliceInputs = 0
    · exact strategy_no_inputs s (Or.inl hz)
    have hone : A.aliceInputs = 1 := by omega
    rcases A with ⟨na,nb,AO,BO⟩
    change na = 1 at hone
    subst na
    exact strategy_single_alice AO BO s
  · by_cases hz : A.bobInputs = 0
    · exact strategy_no_inputs s (Or.inr hz)
    have hone : A.bobInputs = 1 := by omega
    rcases A with ⟨na,nb,AO,BO⟩
    change nb = 1 at hone
    subst nb
    exact strategy_single_bob AO BO s

/-- The previously missing one-input target, stated over the actual convex hulls. -/
theorem one_input_equality : OneInputEquality := by
  intro A h
  apply Set.Subset.antisymm
  · change convexHull ℝ (rawPOVM A) ⊆ convexHull ℝ (rawPVM A)
    apply convexHull_min
    · rintro p ⟨s,rfl⟩
      exact strategy_one_input s h
    · exact convex_convexHull ℝ (rawPVM A)
  · exact convexPVM_subset_convexPOVM A

end Bell
