import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic

/-! Actual labeled active-chain definitions from (3.10), (3.17), and (4.2)–(4.6).

The Green matrix below is mathlib's nonsingular inverse. No theorem in this
module asserts its invertibility. Establishing that fact, and identifying the
general symmetric coefficient resolvent with this physical one, remain explicit
proof obligations. In particular R2 is not defined using the reduced scalar.
-/

namespace SymmetricSector.Active

noncomputable section

open scoped BigOperators

abbrev State (n : ℕ) :=
  { p : Finset (Fin n) × Fin n // p.1.Nonempty ∧ p.2 ∉ p.1 }

abbrev State.cache {n : ℕ} (y : State n) := y.val.1
abbrev State.target {n : ℕ} (y : State n) := y.val.2
abbrev State.rank {n : ℕ} (y : State n) := y.cache.card

def sampled {n : ℕ} (C : Finset (Fin n)) (v i : Fin n)
    (hv : v ∉ C) (hi : i ≠ v) : State n :=
  ⟨(insert i C, v), Finset.insert_nonempty i C, by simp [hv, hi.symm]⟩

theorem sampled_rank {n : ℕ} (C : Finset (Fin n)) (v i : Fin n)
    (hv : v ∉ C) (hi : i ≠ v) :
    (sampled C v i hv hi).rank = if i ∈ C then C.card else C.card + 1 := by
  simp only [sampled, State.rank, State.cache]
  split_ifs with h
  · exact Finset.card_insert_of_mem h
  · exact Finset.card_insert_of_not_mem h

theorem sum_state_event {n : ℕ} (C : Finset (Fin n)) (v : Fin n)
    (hC : C.Nonempty) (hv : v ∉ C) (r : ℝ) (f : State n → ℝ) :
    (∑ y : State n, (if y.cache = C ∧ y.target = v then r else 0) * f y) =
      r * f ⟨(C, v), hC, hv⟩ := by
  have heq (y : State n) :
      (y.cache = C ∧ y.target = v) ↔ y = ⟨(C, v), hC, hv⟩ := by
    constructor
    · intro h
      apply Subtype.ext
      exact Prod.ext h.1 h.2
    · intro h
      subst y
      exact ⟨rfl, rfl⟩
  simp_rw [heq]
  simp

theorem sum_sample_event {n : ℕ} (C : Finset (Fin n)) (v i : Fin n)
    (hv : v ∉ C) (r : ℝ) (f : State n → ℝ) :
    (∑ y : State n,
      (if i ≠ v ∧ y.cache = insert i C ∧ y.target = v then r else 0) * f y) =
      if hi : i ≠ v then r * f (sampled C v i hv hi) else 0 := by
  by_cases hi : i ≠ v
  · rw [dif_pos hi]
    have hp (y : State n) :
        (i ≠ v ∧ y.cache = insert i C ∧ y.target = v) =
          (y.cache = insert i C ∧ y.target = v) :=
      propext (and_iff_right hi)
    simp_rw [hp]
    exact sum_state_event (insert i C) v (Finset.insert_nonempty i C)
      (by simp [hv, hi.symm]) r f
  · simp [hi]

/-- Section 3's two actual labeled moves: continue, or uniformly retarget
within the nonempty cache before sampling. Diagonal sources are excluded. -/
def kernel {n : ℕ} (P : Matrix (Fin n) (Fin n) ℝ) :
    Matrix (State n) (State n) ℝ := fun y z =>
  (1 / 2 : ℝ) * (∑ i : Fin n,
    if i ≠ y.target ∧ z.cache = insert i y.cache ∧ z.target = y.target
    then P y.target i else 0) +
  (1 / (2 * (y.rank : ℝ))) * (∑ w ∈ y.cache, ∑ i : Fin n,
    if i ≠ w ∧ z.cache = insert i (y.cache.erase w) ∧ z.target = w
    then P w i else 0)

/-- Kernel action obtained from exactly the two moves, with valid successor
states. This lemma removes the labeled output-state sum without assuming a
rank quotient or feature formula. -/
theorem kernel_action {n : ℕ} (P : Matrix (Fin n) (Fin n) ℝ)
    (f : State n → ℝ) (y : State n) :
    (kernel P).mulVec f y =
      (1 / 2 : ℝ) * (∑ i : Fin n,
        if hi : i ≠ y.target then
          P y.target i * f (sampled y.cache y.target i y.property.2 hi) else 0) +
      (1 / (2 * (y.rank : ℝ))) * (∑ w ∈ y.cache, ∑ i : Fin n,
        if hi : i ≠ w then
          P w i * f (sampled (y.cache.erase w) w i (Finset.not_mem_erase w _) hi)
        else 0) := by
  simp only [Matrix.mulVec, dotProduct, kernel, add_mul, Finset.sum_add_distrib]
  congr 1
  · simp_rw [mul_assoc, Finset.sum_mul]
    rw [← Finset.mul_sum, Finset.sum_comm]
    congr 1
    apply Finset.sum_congr rfl
    intro i hi
    exact sum_sample_event y.cache y.target i y.property.2 (P y.target i) f
  · simp_rw [mul_assoc, Finset.sum_mul]
    rw [← Finset.mul_sum, Finset.sum_comm]
    congr 1
    apply Finset.sum_congr rfl
    intro w hw
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i hi
    exact sum_sample_event (y.cache.erase w) w i (Finset.not_mem_erase w _)
      (P w i) f

/-- A single actual source draw acting on a rank function, for a zero-row-sum
perturbation. The proof accounts for an empty pre-sampling cache as well. -/
theorem rank_sample_balance {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (hdiag : ∀ v, δ v v = 0) (hrow : ∀ v, ∑ i, δ v i = 0)
    (C : Finset (Fin n)) (v : Fin n) (hv : v ∉ C) (h : ℕ → ℝ) :
    (∑ i : Fin n, if hi : i ≠ v then
      δ v i * h (sampled C v i hv hi).rank else 0) =
      (h C.card - h (C.card + 1)) * ∑ i ∈ C, δ v i := by
  have hterm (i : Fin n) :
      (if hi : i ≠ v then δ v i * h (sampled C v i hv hi).rank else 0) =
        (if i ∈ C then δ v i else 0) * (h C.card - h (C.card + 1)) +
          δ v i * h (C.card + 1) := by
    by_cases hi : i ≠ v
    · rw [dif_pos hi, sampled_rank]
      split_ifs <;> ring
    · have heq : i = v := not_ne_iff.mp hi
      subst i
      simp [hdiag, hv]
  simp_rw [hterm, Finset.sum_add_distrib, ← Finset.sum_mul, hrow, zero_mul, add_zero]
  have hset : Finset.univ.filter (fun i => i ∈ C) = C := by ext i; simp
  rw [← Finset.sum_filter, hset]
  ring

theorem rank_sample_formula {n : ℕ} (P : Matrix (Fin n) (Fin n) ℝ)
    (hdiag : ∀ v, P v v = 0) (C : Finset (Fin n)) (v : Fin n)
    (hv : v ∉ C) (h : ℕ → ℝ) :
    (∑ i : Fin n, if hi : i ≠ v then
      P v i * h (sampled C v i hv hi).rank else 0) =
      (h C.card - h (C.card + 1)) * (∑ i ∈ C, P v i) +
        h (C.card + 1) * ∑ i, P v i := by
  have hterm (i : Fin n) :
      (if hi : i ≠ v then P v i * h (sampled C v i hv hi).rank else 0) =
        (if i ∈ C then P v i else 0) * (h C.card - h (C.card + 1)) +
          P v i * h (C.card + 1) := by
    by_cases hi : i ≠ v
    · rw [dif_pos hi, sampled_rank]
      split_ifs <;> ring
    · have heq : i = v := not_ne_iff.mp hi
      subst i
      simp [hdiag, hv]
  simp_rw [hterm, Finset.sum_add_distrib, ← Finset.sum_mul]
  have hset : Finset.univ.filter (fun i => i ∈ C) = C := by ext i; simp
  rw [← Finset.sum_filter, hset]
  ring

/-- Complete loopless sampling kernel. Statements using it substantively
must restrict to n≥2. Natural subtraction is intentional in N=n−1. -/
def complete (n : ℕ) : Matrix (Fin n) (Fin n) ℝ :=
  fun i j => if i = j then 0 else 1 / ((n - 1 : ℕ) : ℝ)

@[simp] theorem complete_diagonal (n : ℕ) (v : Fin n) : complete n v v = 0 := by
  simp [complete]

theorem complete_subset_sum {n : ℕ} (C : Finset (Fin n)) (v : Fin n) (hv : v ∉ C) :
    (∑ i ∈ C, complete n v i) = (C.card : ℝ) / ((n - 1 : ℕ) : ℝ) := by
  have hterm (i : Fin n) (hi : i ∈ C) :
      complete n v i = 1 / ((n - 1 : ℕ) : ℝ) := by
    unfold complete
    rw [if_neg]
    intro heq
    exact hv (heq ▸ hi)
  rw [Finset.sum_congr rfl hterm]
  simp [nsmul_eq_mul, div_eq_mul_inv]

theorem complete_row_sum {n : ℕ} (hn : 2 ≤ n) (v : Fin n) :
    ∑ i, complete n v i = 1 := by
  have hN : (((n - 1 : ℕ) : ℝ)) ≠ 0 := by exact_mod_cast (show n - 1 ≠ 0 by omega)
  have hsum := Finset.sum_erase_add (s := Finset.univ) (f := complete n v)
    (Finset.mem_univ v)
  rw [complete_diagonal, add_zero] at hsum
  rw [← hsum, complete_subset_sum _ _ (Finset.not_mem_erase _ _)]
  simp [hN]

theorem rank_sample_complete {n : ℕ} (hn : 2 ≤ n)
    (C : Finset (Fin n)) (v : Fin n) (hv : v ∉ C) (h : ℕ → ℝ) :
    (∑ i : Fin n, if hi : i ≠ v then
      complete n v i * h (sampled C v i hv hi).rank else 0) =
      ((C.card : ℝ) * h C.card +
        ((((n - 1 : ℕ) : ℝ)) - C.card) * h (C.card + 1)) /
          ((n - 1 : ℕ) : ℝ) := by
  rw [rank_sample_formula _ (complete_diagonal n), complete_subset_sum C v hv,
    complete_row_sum hn, mul_one]
  have hN : (((n - 1 : ℕ) : ℝ)) ≠ 0 := by exact_mod_cast (show n - 1 ≠ 0 by omega)
  generalize (((n - 1 : ℕ) : ℝ)) = N at *
  field_simp [hN]
  ring

def K0 (n : ℕ) := kernel (complete n)

/-- The actual complete active chain has exactly the rank transition rates
in (A.2), including both physical boundary ranks. -/
theorem K0_rank {n : ℕ} (hn : 2 ≤ n) (h : ℕ → ℝ) (y : State n) :
    (K0 n).mulVec (fun y => h y.rank) y =
      h y.rank +
        ((((n - 1 : ℕ) : ℝ)) - y.rank) / (2 * ((n - 1 : ℕ) : ℝ)) *
          (h (y.rank + 1) - h y.rank) +
        ((y.rank : ℝ) - 1) / (2 * ((n - 1 : ℕ) : ℝ)) *
          (h (y.rank - 1) - h y.rank) := by
  rw [K0, kernel_action,
    rank_sample_complete hn y.cache y.target y.property.2 h]
  have hk : 0 < y.rank := Finset.card_pos.mpr y.property.1
  have hkR : (y.rank : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hk
  have hN : (((n - 1 : ℕ) : ℝ)) ≠ 0 := by exact_mod_cast (show n - 1 ≠ 0 by omega)
  have hstop :
      (∑ w ∈ y.cache, ∑ i : Fin n, if hi : i ≠ w then
        complete n w i *
          h (sampled (y.cache.erase w) w i (Finset.not_mem_erase w _) hi).rank else 0) =
        (y.rank : ℝ) *
          (((y.rank : ℝ) - 1) * h (y.rank - 1) +
            ((((n - 1 : ℕ) : ℝ)) - y.rank + 1) * h y.rank) /
          ((n - 1 : ℕ) : ℝ) := by
    simp_rw [rank_sample_complete hn]
    have hentry (w : Fin n) (hw : w ∈ y.cache) :
        (((y.cache.erase w).card : ℝ) * h (y.cache.erase w).card +
          ((((n - 1 : ℕ) : ℝ)) - (y.cache.erase w).card) *
            h ((y.cache.erase w).card + 1)) / ((n - 1 : ℕ) : ℝ) =
          (((y.rank : ℝ) - 1) * h (y.rank - 1) +
            ((((n - 1 : ℕ) : ℝ)) - y.rank + 1) * h y.rank) /
              ((n - 1 : ℕ) : ℝ) := by
      have hcard : (y.cache.erase w).card = y.rank - 1 :=
        Finset.card_erase_of_mem hw
      have hidx : y.rank - 1 + 1 = y.rank := Nat.sub_add_cancel (by omega)
      have hcast : (((y.rank - 1 : ℕ) : ℝ)) = (y.rank : ℝ) - 1 := by
        rw [Nat.cast_sub (by omega : 1 ≤ y.rank), Nat.cast_one]
      rw [hcard, hidx, hcast]
      ring
    rw [Finset.sum_congr rfl hentry]
    simp only [Finset.sum_const, nsmul_eq_mul]
    change (y.rank : ℝ) * _ = _
    ring
  rw [hstop]
  change (1 / 2 : ℝ) * (((y.rank : ℝ) * h y.rank +
    ((((n - 1 : ℕ) : ℝ)) - y.rank) * h (y.rank + 1)) /
    ((n - 1 : ℕ) : ℝ)) + _ = _
  generalize (((n - 1 : ℕ) : ℝ)) = N at *
  field_simp [hN, hkR]
  ring

/-- Because the active kernel is linear, this is its exact first derivative. -/
def perturbation {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ) := kernel δ

def nu0 {n : ℕ} (y : State n) : ℝ :=
  (y.rank : ℝ) / ((n : ℝ) * ((n - 1 : ℕ) : ℝ) * 2 ^ (n - 2))

def observable {n : ℕ} (y : State n) : ℝ := 1 / (y.rank : ℝ)

noncomputable def center (n : ℕ) : ℝ := ∑ y : State n, nu0 y * observable y

noncomputable def q (n : ℕ) : State n → ℝ := fun y => observable y - center n

noncomputable def centeredMatrix (n : ℕ) : Matrix (State n) (State n) ℝ :=
  1 - K0 n + Matrix.of (fun (_ : State n) (y : State n) => nu0 y)

noncomputable def green (n : ℕ) : Matrix (State n) (State n) ℝ :=
  (centeredMatrix n)⁻¹

/-- The physical active-chain expression ν₀ Δ G Δ G q in (4.6). -/
noncomputable def R2 {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ) : ℝ :=
  dotProduct nu0 ((perturbation δ).mulVec
    ((green n).mulVec ((perturbation δ).mulVec ((green n).mulVec (q n)))))

def SymmetricBalanced {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ) : Prop :=
  (∀ i, δ i i = 0) ∧ (∀ i j, δ i j = δ j i) ∧ (∀ i, ∑ j, δ i j = 0)

def x {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ) (y : State n) : ℝ :=
  ∑ i ∈ y.cache, δ y.target i

/-- The diagonal terms vanish for admissible matrices, so this equals the
ordered off-diagonal sum in (A.11). -/
def z {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ) (y : State n) : ℝ :=
  ∑ w ∈ y.cache, ∑ i ∈ y.cache, δ w i

def feature {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (a b : ℕ → ℝ) (y : State n) : ℝ :=
  a y.rank * x δ y + b y.rank * z δ y

/-- The first physical perturbation formula (A.15), before introducing any
Poisson solution. It applies to every actual rank function h. -/
theorem perturbation_rank {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (hδ : SymmetricBalanced δ) (h : ℕ → ℝ) (y : State n) :
    (perturbation δ).mulVec (fun y => h y.rank) y =
      (h y.rank - h (y.rank + 1)) / 2 * x δ y +
      (h (y.rank - 1) - h y.rank) / (2 * (y.rank : ℝ)) * z δ y := by
  rw [perturbation, kernel_action,
    rank_sample_balance δ hδ.1 hδ.2.2 y.cache y.target y.property.2 h]
  have hstop :
      (∑ w ∈ y.cache, ∑ i : Fin n, if hi : i ≠ w then
        δ w i * h (sampled (y.cache.erase w) w i (Finset.not_mem_erase w _) hi).rank
        else 0) = (h (y.rank - 1) - h y.rank) * z δ y := by
    simp_rw [rank_sample_balance δ hδ.1 hδ.2.2]
    have hentry (w : Fin n) (hw : w ∈ y.cache) :
        (h (y.cache.erase w).card - h ((y.cache.erase w).card + 1)) *
            ∑ i ∈ y.cache.erase w, δ w i =
          (h (y.rank - 1) - h y.rank) * ∑ i ∈ y.cache, δ w i := by
      have hk : 0 < y.rank := Finset.card_pos.mpr y.property.1
      have hcard := Finset.card_erase_of_mem hw
      have hsum := Finset.sum_erase_add (s := y.cache) (f := δ w) hw
      rw [hδ.1, add_zero] at hsum
      rw [hcard, hsum]
      have hidx : y.cache.card - 1 + 1 = y.rank := by
        change y.cache.card - 1 + 1 = y.cache.card
        change 0 < y.cache.card at hk
        omega
      rw [hidx]
    rw [Finset.sum_congr rfl hentry, ← Finset.mul_sum]
    rfl
  rw [hstop]
  unfold x
  ring

theorem rank_pos {n : ℕ} (y : State n) : 0 < y.rank :=
  Finset.card_pos.mpr y.property.1

theorem cache_subset {n : ℕ} (y : State n) :
    y.cache ⊆ Finset.univ.erase y.target := by
  intro i hi
  simp only [Finset.mem_erase, Finset.mem_univ, and_true]
  intro heq
  rw [heq] at hi
  exact y.property.2 hi

theorem rank_le {n : ℕ} (y : State n) : y.rank ≤ n - 1 := by
  have h := Finset.card_le_card (cache_subset y)
  simpa using h

theorem full_rank_cache {n : ℕ} (y : State n) (hk : y.rank = n - 1) :
    y.cache = Finset.univ.erase y.target := by
  apply Finset.eq_of_subset_of_card_le (cache_subset y)
  simp [hk, State.rank]

theorem x_full_rank {n : ℕ} {δ : Matrix (Fin n) (Fin n) ℝ}
    (hδ : SymmetricBalanced δ) (y : State n) (hk : y.rank = n - 1) : x δ y = 0 := by
  unfold x
  rw [full_rank_cache y hk]
  have h := Finset.sum_erase_add (s := Finset.univ) (f := δ y.target)
    (Finset.mem_univ y.target)
  rw [hδ.1, hδ.2.2, add_zero] at h
  exact h

theorem z_singleton_rank {n : ℕ} {δ : Matrix (Fin n) (Fin n) ℝ}
    (hδ : SymmetricBalanced δ) (y : State n) (hk : y.rank = 1) : z δ y = 0 := by
  obtain ⟨w, hw⟩ := Finset.card_eq_one.mp hk
  simp [z, hw, hδ.1]

theorem z_full_rank {n : ℕ} {δ : Matrix (Fin n) (Fin n) ℝ}
    (hδ : SymmetricBalanced δ) (y : State n) (hk : y.rank = n - 1) : z δ y = 0 := by
  have hrow (w : Fin n) :
      ∑ i ∈ Finset.univ.erase y.target, δ w i = -δ y.target w := by
    have h := Finset.sum_erase_add (s := Finset.univ) (f := δ w)
      (Finset.mem_univ y.target)
    rw [hδ.2.2, hδ.2.1 w y.target] at h
    linarith
  unfold z
  rw [full_rank_cache y hk]
  simp_rw [hrow, Finset.sum_neg_distrib]
  have hx := x_full_rank hδ y hk
  unfold x at hx
  rw [full_rank_cache y hk] at hx
  rw [hx, neg_zero]

theorem retarget_denominator_pos {n : ℕ} (y : State n) :
    0 < 2 * (y.rank : ℝ) := by
  exact mul_pos (by norm_num) (by exact_mod_cast rank_pos y)

theorem complete_denominator_pos {n : ℕ} (hn : 2 ≤ n) :
    0 < ((n - 1 : ℕ) : ℝ) := by
  exact_mod_cast (show 0 < n - 1 by omega)

theorem nu0_denominator_pos {n : ℕ} (hn : 2 ≤ n) :
    0 < (n : ℝ) * ((n - 1 : ℕ) : ℝ) * 2 ^ (n - 2) := by
  exact mul_pos (mul_pos (by exact_mod_cast (show 0 < n by omega))
    (complete_denominator_pos hn)) (by positivity)

@[simp] theorem kernel_zero (n : ℕ) : kernel (0 : Matrix (Fin n) (Fin n) ℝ) = 0 := by
  ext y z
  simp [kernel]

theorem kernel_add {n : ℕ} (P Q : Matrix (Fin n) (Fin n) ℝ) :
    kernel (P + Q) = kernel P + kernel Q := by
  ext y z
  simp only [kernel, Matrix.add_apply]
  simp_rw [ite_add_zero, Finset.sum_add_distrib]
  ring

theorem kernel_smul {n : ℕ} (t : ℝ) (P : Matrix (Fin n) (Fin n) ℝ) :
    kernel (t • P) = t • kernel P := by
  ext y z
  simp only [kernel, Matrix.smul_apply, smul_eq_mul]
  have aux : ∀ (p : Prop) [Decidable p] (a : ℝ),
      (if p then t * a else 0) = t * (if p then a else 0) := by
    intro p _ a
    split_ifs <;> simp
  simp_rw [aux, ← Finset.mul_sum]
  ring

theorem kernel_affine {n : ℕ} (t : ℝ) (δ : Matrix (Fin n) (Fin n) ℝ) :
    kernel (complete n + t • δ) = K0 n + t • perturbation δ := by
  rw [kernel_add, kernel_smul]
  rfl

/-- Checked uniqueness infrastructure. The invertibility and concrete Poisson
residual hypotheses must themselves be supplied by downstream proofs. -/
theorem green_eq_solution {n : ℕ} (hinv : IsUnit (centeredMatrix n).det)
    (f b : State n → ℝ) (hf : (centeredMatrix n).mulVec f = b) :
    (green n).mulVec b = f := by
  rw [← hf, green, Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ hinv,
    Matrix.one_mulVec]

/-- A certified solution of the actual second Poisson equation identifies the
physical expression with its actual perturbed stationary current. This is an
infrastructure lemma, not the unproved general-n scalar correspondence. -/
theorem R2_eq_current_of_solution {n : ℕ}
    (δ : Matrix (Fin n) (Fin n) ℝ) (f : State n → ℝ)
    (hinv : IsUnit (centeredMatrix n).det)
    (hf : (centeredMatrix n).mulVec f =
      (perturbation δ).mulVec ((green n).mulVec (q n))) :
    R2 δ = dotProduct nu0 ((perturbation δ).mulVec f) := by
  unfold R2
  rw [green_eq_solution hinv f _ hf]

@[simp] theorem R2_zero (n : ℕ) : R2 (0 : Matrix (Fin n) (Fin n) ℝ) = 0 := by
  simp [R2, perturbation]

theorem column_sums_zero {n : ℕ} {δ : Matrix (Fin n) (Fin n) ℝ}
    (hδ : SymmetricBalanced δ) (j : Fin n) : ∑ i, δ i j = 0 := by
  simpa only [hδ.2.1] using hδ.2.2 j

/-- The symmetric balanced tangent sector is absent at population size three. -/
theorem symmetricBalanced_three_eq_zero {δ : Matrix (Fin 3) (Fin 3) ℝ}
    (hδ : SymmetricBalanced δ) : δ = 0 := by
  have h00 := hδ.1 0
  have h11 := hδ.1 1
  have h22 := hδ.1 2
  have h10 := hδ.2.1 1 0
  have h20 := hδ.2.1 2 0
  have h21 := hδ.2.1 2 1
  have h0 := hδ.2.2 0
  have h1 := hδ.2.2 1
  have h2 := hδ.2.2 2
  rw [Fin.sum_univ_three] at h0 h1 h2
  have h01 : δ 0 1 = 0 := by linarith
  have h02 : δ 0 2 = 0 := by linarith
  have h12 : δ 1 2 = 0 := by linarith
  have h10z : δ 1 0 = 0 := by linarith
  have h20z : δ 2 0 = 0 := by linarith
  have h21z : δ 2 1 = 0 := by linarith
  ext i j
  fin_cases i <;> fin_cases j
  all_goals first | exact h00 | exact h11 | exact h22 | exact h01 | exact h02 | exact h12 | exact h10z | exact h20z | exact h21z

theorem R2_symmetricBalanced_three {δ : Matrix (Fin 3) (Fin 3) ℝ}
    (hδ : SymmetricBalanced δ) : R2 δ = 0 := by
  rw [symmetricBalanced_three_eq_zero hδ, R2_zero]

#print axioms kernel_affine
#print axioms symmetricBalanced_three_eq_zero
#print axioms R2_symmetricBalanced_three

end
end SymmetricSector.Active
