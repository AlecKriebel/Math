import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum.Basic
import Mathlib.Tactic.NormNum.OfScientific
import Mathlib.Tactic.Push

namespace SymmetricSector

/-- The physical-rank radial recurrence (A.20); rank zero is an auxiliary zero. -/
def t (N : ℕ) : ℕ → ℚ
  | 0 => 0
  | k + 1 => (2 * (N : ℚ) + (k : ℚ) * t N k) / (2 * (N : ℚ) - (k + 1))

/-- The left occupation lower bound (A.30). All subtractions occur in ℚ. -/
def lowerEll (N j : ℕ) : ℚ :=
  (3 * N * j + 3 * N - 8 * j - 10) / (3 * N * j * (j + 1))

/-- Completed-excursion contraction constant (A.27). -/
def c (N : ℕ) : ℚ := (2 * N - 5) / (2 * N * (N - 2))

/-- Alternating-phase error allowance (A.32). -/
def epsilon (N : ℕ) : ℚ := (25 / 11 : ℚ) * c N / (1 - c N)

/-- One of the actual physical-rank terms maximized in (A.32). -/
def betaTerm (N j : ℕ) : ℚ :=
  (4 * (j + 2) / (3 * (j + 1) * (N - 2)) : ℚ) /
    ((11 / 25 : ℚ) * lowerEll N j * t N j)

/-- The exact physical-rank maximum in (A.32), with zero for empty rank sets. -/
def beta (N : ℕ) : ℚ :=
  if h : ((Finset.Icc 1 (N - 2)).image (betaTerm N)).Nonempty then
    ((Finset.Icc 1 (N - 2)).image (betaTerm N)).sup' h id
  else 0

/-- The denominator used by the contraction constant is strictly positive. -/
theorem c_den_pos {N : ℕ} (hN : 3 ≤ N) :
    0 < 2 * (N : ℚ) * ((N : ℚ) - 2) := by
  have hn : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hn2 : (0 : ℚ) < (N : ℚ) - 2 := by linarith
  exact mul_pos (mul_pos (by norm_num) (by linarith)) hn2

/-- The denominator `1-c_N` appearing in epsilon is strictly positive. -/
theorem one_sub_c_pos {N : ℕ} (hN : 3 ≤ N) : 0 < 1 - c N := by
  have hn : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hden := c_den_pos hN
  have hnum : 2 * (N : ℚ) - 5 < 1 * (2 * (N : ℚ) * ((N : ℚ) - 2)) := by
    nlinarith [sq_nonneg ((N : ℚ) - 3)]
  have hc : c N < 1 := (div_lt_iff₀ hden).mpr hnum
  linarith

/-- Rational value represented by an integer grid witness. -/
def gridValue (w : List ℕ) (j : ℕ) : ℚ := (w[j]?.getD 0 : ℚ) / 10000

/-- A finite certificate verifies each one-step recurrence inequality and each
physical-rank debt inequality. Its checks use ordinary decidable arithmetic. -/
def MarginCertificate (N : ℕ) (w : List ℕ) (margin : ℚ) : Prop :=
  gridValue w 0 = 0 ∧
  (∀ k : Fin (N - 1), gridValue w (k.val + 1) ≤
    (2 * (N : ℚ) + k.val * gridValue w k.val) / (2 * N - (k.val + 1))) ∧
  (∀ j : Fin (N - 2),
    0 < gridValue w (j.val + 1) ∧
    0 < lowerEll N (j.val + 1) ∧
    (4 * ((j.val + 1 : ℕ) + 2) /
        (3 * ((j.val + 1 : ℕ) + 1) * ((N : ℚ) - 2)) : ℚ) /
        ((11 / 25 : ℚ) * lowerEll N (j.val + 1) * gridValue w (j.val + 1))
      + epsilon N ≤ 1 - margin)

instance (N : ℕ) (w : List ℕ) (margin : ℚ) : Decidable (MarginCertificate N w margin) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

 theorem gridValue_le_t {N : ℕ} (hN : 3 ≤ N) {w : List ℕ} {m : ℚ}
    (cert : MarginCertificate N w m) {j : ℕ} (hj : j ≤ N - 1) :
    gridValue w j ≤ t N j := by
  induction j with
  | zero => simp [t, cert.1]
  | succ k ih =>
      have hk : k < N - 1 := by omega
      have hnq : (k : ℚ) + 1 < 2 * (N : ℚ) := by exact_mod_cast (show k + 1 < 2 * N by omega)
      have hden : 0 < 2 * (N : ℚ) - (k + 1) := by linarith
      refine (cert.2.1 ⟨k, hk⟩).trans ?_
      dsimp only
      rw [t]
      exact div_le_div_of_nonneg_right
        (add_le_add_left (mul_le_mul_of_nonneg_left (ih (by omega)) (Nat.cast_nonneg k)) _) hden.le

 theorem betaTerm_le_grid {N j : ℕ} (hN : 3 ≤ N) (hj : 1 ≤ j)
    (hjN : j ≤ N - 2) {w : List ℕ} {m : ℚ} (cert : MarginCertificate N w m) :
    betaTerm N j + epsilon N ≤ 1 - m := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : j ≠ 0)
  have hk : k < N - 2 := by omega
  obtain ⟨hgrid, hell, hbound⟩ := cert.2.2 ⟨k, hk⟩
  have ht : gridValue w (k + 1) ≤ t N (k + 1) := gridValue_le_t hN cert (by omega)
  have hn : (2 : ℚ) < N := by exact_mod_cast hN
  have hn2 : (0 : ℚ) < (N : ℚ) - 2 := by linarith
  have hd : (0 : ℚ) < (11 / 25 : ℚ) * lowerEll N (k + 1) * gridValue w (k + 1) :=
    mul_pos (mul_pos (by norm_num) hell) hgrid
  have hdn : (11 / 25 : ℚ) * lowerEll N (k + 1) * gridValue w (k + 1) ≤
      (11 / 25 : ℚ) * lowerEll N (k + 1) * t N (k + 1) :=
    mul_le_mul_of_nonneg_left ht (mul_pos (by norm_num) hell).le
  have hnum : (0 : ℚ) ≤ 4 * ((k + 1 : ℕ) + 2) /
      (3 * ((k + 1 : ℕ) + 1) * ((N : ℚ) - 2)) := by
    apply div_nonneg
    · exact mul_nonneg (by norm_num) (by positivity)
    · exact mul_nonneg (mul_nonneg (by norm_num) (by positivity)) hn2.le
  have hmono := div_le_div_of_nonneg_left hnum hd hdn
  exact (add_le_add_right hmono (epsilon N)).trans hbound

 theorem beta_add_epsilon_le_of_certificate {N : ℕ} (hN : 3 ≤ N)
    {w : List ℕ} {m : ℚ} (cert : MarginCertificate N w m) :
    beta N + epsilon N ≤ 1 - m := by
  have hne : ((Finset.Icc 1 (N - 2)).image (betaTerm N)).Nonempty :=
    Finset.image_nonempty.mpr ⟨1, Finset.mem_Icc.mpr ⟨le_refl _, by omega⟩⟩
  rw [beta, dif_pos hne]
  apply le_sub_iff_add_le.mp
  apply Finset.sup'_le
  intro v hv
  obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hv
  obtain ⟨hj, hjN⟩ := Finset.mem_Icc.mp hj
  exact le_sub_iff_add_le.mpr (betaTerm_le_grid hN hj hjN cert)

end SymmetricSector
