import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Finite product response distributions

A common random variable assigns an output to *every* input simultaneously.
The lemmas quantify over arbitrary finite, dependent output alphabets. Zero
marginal weights are handled without assuming they are positive.

Verification evidence: see CERTIFICATION.md and reports/kernel_report.json.
-/
noncomputable section
open scoped BigOperators
namespace Bell.ClassicalProduct

variable {X : Type*} [Fintype X] [DecidableEq X]
variable {O : X → Type*} [∀ x, Fintype (O x)] [∀ x, DecidableEq (O x)]

abbrev Assignment (O : X → Type*) := (x : X) → O x

def mass (r : (x : X) → O x → ℝ) (α : Assignment O) : ℝ := ∏ x, r x (α x)

/-- The finite distributive law, including dependent finite alphabets. -/
theorem total_mass (r : (x : X) → O x → ℝ) :
    (∑ α : Assignment O, mass r α) = ∏ x, ∑ a, r x a := by
  classical
  simpa [mass] using
    (Finset.prod_univ_sum (fun x => (Finset.univ : Finset (O x))) r).symm

theorem total_mass_one (r : (x : X) → O x → ℝ)
    (hn : ∀ x, ∑ a, r x a = 1) : (∑ α : Assignment O, mass r α) = 1 := by
  rw [total_mass]
  simp [hn]

/-- Pin one output while leaving all other response distributions unchanged. -/
def pin (r : (x : X) → O x → ℝ) (x : X) (a : O x) : (y : X) → O y → ℝ :=
  Function.update r x (fun b => if b = a then r x b else 0)

theorem pin_mass (r : (x : X) → O x → ℝ) (x : X) (a : O x)
    (α : Assignment O) :
    mass (pin r x a) α = mass r α * (if α x = a then 1 else 0) := by
  classical
  unfold mass
  rw [Fintype.prod_eq_mul_prod_subtype_ne (fun y => pin r x a y (α y)) x,
    Fintype.prod_eq_mul_prod_subtype_ne (fun y => r y (α y)) x]
  have htail :
      (∏ y : {y // y ≠ x}, pin r x a y.1 (α y.1)) =
      ∏ y : {y // y ≠ x}, r y.1 (α y.1) := by
    apply Finset.prod_congr rfl
    intro y _
    simp [pin, y.property]
  rw [htail]
  by_cases h : α x = a <;> simp [pin, h]

/-- Each one-coordinate marginal of the product assignment equals its input row. -/
theorem marginal (r : (x : X) → O x → ℝ)
    (hn : ∀ x, ∑ a, r x a = 1) (x : X) (a : O x) :
    (∑ α : Assignment O, mass r α * (if a = α x then 1 else 0)) = r x a := by
  classical
  calc
    (∑ α : Assignment O, mass r α * (if a = α x then 1 else 0)) =
        ∑ α : Assignment O, mass (pin r x a) α := by
      apply Finset.sum_congr rfl
      intro α _
      simpa only [eq_comm] using (pin_mass r x a α).symm
    _ = ∏ y, ∑ b, pin r x a y b := total_mass _
    _ = r x a := by
      rw [Fintype.prod_eq_mul_prod_subtype_ne (fun y => ∑ b, pin r x a y b) x]
      have htail : ∀ y : {y // y ≠ x}, (∑ b, pin r x a y.1 b) = 1 := by
        intro y
        simpa [pin, y.property] using hn y.1
      simp only [htail, Finset.prod_const_one, mul_one]
      simp [pin]

variable {B : Type*} [Fintype B] [DecidableEq B]

/-- A table with a single input on the B party. -/
abbrev Table (O : X → Type*) (B : Type*) := (x : X) → O x → B → ℝ

def conditional (p : Table O B) (q : B → ℝ) (b : B) : (x : X) → O x → ℝ :=
  fun x a => p x a b / q b

def weight (p : Table O B) (q : B → ℝ) (k : B × Assignment O) : ℝ :=
  q k.1 * mass (conditional p q k.1) k.2

theorem conditional_normalized (p : Table O B) (q : B → ℝ)
    (hrow : ∀ x b, ∑ a, p x a b = q b) (b : B) (hb : q b ≠ 0) :
    ∀ x, ∑ a, conditional p q b x a = 1 := by
  intro x
  simp only [conditional, ← Finset.sum_div, hrow, div_self hb]

theorem weight_nonnegative (p : Table O B) (q : B → ℝ)
    (hp : ∀ x a b, 0 ≤ p x a b) (hq : ∀ b, 0 ≤ q b)
    (k : B × Assignment O) : 0 ≤ weight p q k := by
  apply mul_nonneg (hq k.1)
  exact Finset.prod_nonneg (fun x _ => div_nonneg (hp x (k.2 x) k.1) (hq k.1))

/-- One common distribution of complete deterministic response assignments. -/
theorem weight_normalized (p : Table O B) (q : B → ℝ)
    (hrow : ∀ x b, ∑ a, p x a b = q b) (hqsum : ∑ b, q b = 1) :
    (∑ k : B × Assignment O, weight p q k) = 1 := by
  classical
  rw [Fintype.sum_prod_type]
  calc
    (∑ b, ∑ α : Assignment O, weight p q (b,α)) = ∑ b, q b := by
      apply Finset.sum_congr rfl
      intro b _
      by_cases hb : q b = 0
      · simp [weight, hb]
      · change (∑ α : Assignment O, q b * mass (conditional p q b) α) = q b
        rw [← Finset.mul_sum,
          total_mass_one _ (conditional_normalized p q hrow b hb), mul_one]
    _ = 1 := hqsum

/-- A zero marginal annihilates all its nonnegative joint probabilities. -/
theorem entry_zero_of_marginal_zero (p : Table O B) (q : B → ℝ)
    (hp : ∀ x a b, 0 ≤ p x a b)
    (hrow : ∀ x b, ∑ a, p x a b = q b)
    (x : X) (a : O x) (b : B) (hb : q b = 0) : p x a b = 0 := by
  have hu : p x a b ≤ ∑ a', p x a' b :=
    Finset.single_le_sum (fun a' _ => hp x a' b) (Finset.mem_univ a)
  rw [hrow, hb] at hu
  exact le_antisymm hu (hp x a b)

/-- Simultaneous reconstruction of every table entry, with no positive-marginal
assumption in the final statement. -/
theorem reconstruction (p : Table O B) (q : B → ℝ)
    (hp : ∀ x a b, 0 ≤ p x a b)
    (hrow : ∀ x b, ∑ a, p x a b = q b)
    (x : X) (a : O x) (b : B) :
    (∑ k : B × Assignment O,
      weight p q k * (if a = k.2 x ∧ b = k.1 then 1 else 0)) = p x a b := by
  classical
  rw [Fintype.sum_prod_type]
  have hslice :
      (∑ b', ∑ α : Assignment O,
        weight p q (b',α) * (if a = α x ∧ b = b' then 1 else 0)) =
      ∑ α : Assignment O,
        weight p q (b,α) * (if a = α x ∧ b = b then 1 else 0) := by
    apply Finset.sum_eq_single b
    · intro b' _ hne
      simp [Ne.symm hne]
    · intro h
      exact (h (Finset.mem_univ b)).elim
  rw [hslice]
  simp only [and_true]
  by_cases hb : q b = 0
  · have he := entry_zero_of_marginal_zero p q hp hrow x a b hb
    simp [weight, hb, he]
  · change (∑ α : Assignment O,
      (q b * mass (conditional p q b) α) * (if a = α x then 1 else 0)) = p x a b
    simp only [mul_assoc]
    rw [← Finset.mul_sum, marginal _ (conditional_normalized p q hrow b hb)]
    unfold conditional
    field_simp [hb]

end Bell.ClassicalProduct
