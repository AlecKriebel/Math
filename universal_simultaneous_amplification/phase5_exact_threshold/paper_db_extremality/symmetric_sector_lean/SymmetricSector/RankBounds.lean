import SymmetricSector.Margins
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace SymmetricSector

/-- The actual radial recurrence is nonnegative at every physical rank. -/
theorem t_nonneg {N j : ℕ} (hN : 3 ≤ N) (hj : j ≤ N - 1) : 0 ≤ t N j := by
  have hn : (3 : ℚ) ≤ N := by exact_mod_cast hN
  induction j with
  | zero => simp [t]
  | succ k ih =>
      have hkN : (k : ℚ) + 1 + 1 ≤ N := by
        exact_mod_cast (show k + 1 + 1 ≤ N by omega)
      rw [t]
      apply div_nonneg
      · exact add_nonneg (by linarith) (mul_nonneg (Nat.cast_nonneg k) (ih (by omega)))
      · linarith

/-- Strict positivity starts at rank one; rank zero was only an auxiliary convention. -/
theorem t_pos {N j : ℕ} (hN : 3 ≤ N) (hj : 1 ≤ j) (hjN : j ≤ N - 1) :
    0 < t N j := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : j ≠ 0)
  have hn : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hkN : (k : ℚ) + 1 + 1 ≤ N := by
    exact_mod_cast (show k + 1 + 1 ≤ N by omega)
  rw [t]
  apply div_pos
  · exact add_pos_of_pos_of_nonneg (by linarith)
      (mul_nonneg (Nat.cast_nonneg k) (t_nonneg hN (by omega)))
  · linarith

/-- The polynomial remainder in the one-step proof of (A.21), expressed
with the distance `m` below the top boundary. -/
theorem upper_step {n m : ℚ} (hn : 3 ≤ n) (hm : 0 < m) :
    (2 * n + (n - m - 1) * ((n ^ 2 - n + m + 1) / ((n - 2) * (m + 1)))) /
        (n + m) ≤ (n ^ 2 - n + m) / ((n - 2) * m) := by
  have hn2 : 0 < n - 2 := by linarith
  have hm1 : 0 < m + 1 := by linarith
  have hnm : 0 < n + m := by linarith
  have hid :
      (n ^ 2 - n + m) / ((n - 2) * m) -
      (2 * n + (n - m - 1) * ((n ^ 2 - n + m + 1) / ((n - 2) * (m + 1)))) /
        (n + m) =
      (n ^ 2 * (n - 1) + 2*n*m^2 + 2*n*m + 2*m^3 + 3*m^2 + m) /
        ((n - 2) * m * (m + 1) * (n + m)) := by
    field_simp [ne_of_gt hn2, ne_of_gt hm, ne_of_gt hm1, ne_of_gt hnm]
    ring
  have hnum : 0 < n ^ 2 * (n - 1) + 2*n*m^2 + 2*n*m + 2*m^3 + 3*m^2 + m := by
    have hn0 : 0 < n := by linarith
    have hn1 : 0 < n - 1 := by linarith
    positivity
  have hden : 0 < (n - 2) * m * (m + 1) * (n + m) := by positivity
  have hdiff : 0 < (n ^ 2 - n + m) / ((n - 2) * m) -
      (2 * n + (n - m - 1) * ((n ^ 2 - n + m + 1) / ((n - 2) * (m + 1)))) /
        (n + m) := by rw [hid]; exact div_pos hnum hden
  linarith

/-- The general physical-rank radial upper bound (A.21), including the
auxiliary rank zero. The actual recurrence `t` is used. -/
theorem t_upper {N j : ℕ} (hN : 3 ≤ N) (hj : j ≤ N - 1) :
    t N j ≤ ((N : ℚ) ^ 2 - j) / (((N : ℚ) - 2) * ((N : ℚ) - j)) := by
  have hn : (3 : ℚ) ≤ N := by exact_mod_cast hN
  induction j with
  | zero =>
      simp only [t, Nat.cast_zero, sub_zero]
      apply div_nonneg (sq_nonneg _)
      exact mul_nonneg (by linarith) (Nat.cast_nonneg N)
  | succ k ih =>
      have hkN : k ≤ N - 1 := by omega
      have hkn0 : (k : ℚ) + 1 + 1 ≤ (N : ℚ) := by exact_mod_cast (show k + 1 + 1 ≤ N by omega)
      have hkn : (k : ℚ) + 1 ≤ (N : ℚ) - 1 := by linarith
      have hden : 0 < 2 * (N : ℚ) - (k + 1) := by linarith
      have hm : 0 < (N : ℚ) - (k + 1) := by linarith
      have hmono := div_le_div_of_nonneg_right
        (add_le_add_left (mul_le_mul_of_nonneg_left (ih hkN) (Nat.cast_nonneg k)) (2*(N:ℚ))) hden.le
      rw [t]
      simp only [Nat.cast_add, Nat.cast_one]
      refine hmono.trans ?_
      convert upper_step hn hm using 1 <;> ring

/-- Strict positivity of the occupation lower bound on the finite and
analytic phase domain; this also proves its denominator nonzero. -/
theorem lowerEll_pos_of_four {N j : ℕ} (hN : 4 ≤ N) (hj : 1 ≤ j) :
    0 < lowerEll N j := by
  have hn : (4 : ℚ) ≤ N := by exact_mod_cast hN
  have hjq : (1 : ℚ) ≤ j := by exact_mod_cast hj
  unfold lowerEll
  apply div_pos
  · have hprod : 0 ≤ ((N : ℚ) - 4) * (j : ℚ) :=
      mul_nonneg (by linarith) (Nat.cast_nonneg j)
    nlinarith
  · exact mul_pos (mul_pos (mul_pos (by norm_num) (by linarith)) (by linarith)) (by linarith)

/-- Specialization to the finite and analytic phase domain. -/
theorem lowerEll_pos {N j : ℕ} (hN : 40 ≤ N) (hj : 1 ≤ j) :
    0 < lowerEll N j := lowerEll_pos_of_four (by omega) hj

/-- The denominator of the actual radial recurrence is positive on its whole
physical domain, including its top rank. -/
theorem t_step_den_pos {N j : ℕ} (hN : 3 ≤ N) (hjN : j ≤ N - 1) :
    0 < 2 * (N : ℚ) - j := by
  have hn : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hj : (j : ℚ) + 1 ≤ N := by
    exact_mod_cast (show j + 1 ≤ N by omega)
  linarith

/-- All factors in the occupation lower bound's denominator are positive at
the ranks used by the phase proof. -/
theorem lowerEll_den_pos {N j : ℕ} (hN : 3 ≤ N) (hj : 1 ≤ j) :
    0 < 3 * (N : ℚ) * j * (j + 1) := by
  have hn : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hjq : (1 : ℚ) ≤ j := by exact_mod_cast hj
  positivity

/-- The denominator inside the numerator of a beta term never vanishes on
the physical phase domain. -/
theorem beta_numerator_den_pos {N j : ℕ} (hN : 3 ≤ N) :
    0 < 3 * ((j : ℚ) + 1) * ((N : ℚ) - 2) := by
  have hn : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hj : (0 : ℚ) ≤ j := Nat.cast_nonneg j
  have hn2 : 0 < (N : ℚ) - 2 := by linarith
  positivity

/-- Strict positivity of the denominator to which the reciprocal comparison
in beta is applied. The order bound excludes the exceptional zero at N=3,j=1. -/
theorem beta_den_pos {N j : ℕ} (hN : 4 ≤ N) (hj : 1 ≤ j)
    (hjN : j ≤ N - 2) :
    0 < (11 / 25 : ℚ) * lowerEll N j * t N j := by
  exact mul_pos (mul_pos (by norm_num) (lowerEll_pos_of_four hN hj))
    (t_pos (by omega) hj (by omega))

/-- This endpoint is deliberately excluded from the large-order phase argument;
the N=3 reduced scalar is certified by its exact linear-system witness. -/
theorem lowerEll_three_one : lowerEll 3 1 = 0 := by norm_num [lowerEll]

end SymmetricSector
