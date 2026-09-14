import SymmetricSector.GoodPhase

namespace SymmetricSector
open Matrix
open scoped BigOperators

/-- The printed A.31 debt coefficient, extended by zero at the top good rank. -/
def debtWeight (N : ℕ) (i : Good N) : ℚ :=
  if i.val < N - 2 then
    4 * (i.val + 3) / (3 * (i.val + 2) * ((N : ℚ) - 2)) else 0

/-- Every physical beta term is bounded by the actual finite maximum. -/
theorem betaTerm_le_beta {N j : ℕ} (hj : 1 ≤ j) (hjN : j ≤ N - 2) :
    betaTerm N j ≤ beta N := by
  have hm : j ∈ Finset.Icc 1 (N - 2) := Finset.mem_Icc.mpr ⟨hj, hjN⟩
  have hv : betaTerm N j ∈ (Finset.Icc 1 (N - 2)).image (betaTerm N) :=
    Finset.mem_image.mpr ⟨j, hm, rfl⟩
  rw [beta, dif_pos ⟨_, hv⟩]
  exact Finset.le_sup' id hv

theorem beta_pos (N : ℕ) (hN : 4 ≤ N) : 0 < beta N := by
  have hb : 0 < betaTerm N 1 := by
    unfold betaTerm
    apply div_pos _ (beta_den_pos hN (by omega) (by omega))
    exact div_pos (by norm_num) (beta_numerator_den_pos (N := N) (j := 1) (by omega))
  exact lt_of_lt_of_le hb (betaTerm_le_beta (by omega) (by omega))

/-- The maximum in A.32 bounds every coefficient of the actual debt sum. -/
theorem debtWeight_le_beta (N : ℕ) (hN : 4 ≤ N) (i : Good N) :
    debtWeight N i ≤ beta N * ((11 / 25 : ℚ) * lowerEll N (i.val+1) * t N (i.val+1)) := by
  by_cases hi : i.val < N - 2
  · have hb := betaTerm_le_beta (N := N) (j := i.val+1) (by omega) (by omega)
    have hd := beta_den_pos (N := N) (j := i.val+1) hN (by omega) (by omega)
    have hc := (div_le_iff₀ hd).mp hb
    norm_num [debtWeight, hi, betaTerm, Nat.cast_add, Nat.cast_one, add_assoc] at hc ⊢
    exact hc
  · rw [debtWeight, if_neg hi]
    exact mul_nonneg (beta_pos N hN).le
      (mul_nonneg (mul_nonneg (by norm_num) (lowerEll_pos_of_four hN (by omega)).le)
        (t_nonneg (by omega) (by have := i.isLt; omega)))

/-- The actual beta maximum converts A.31's checked debt estimate into the
scalar loss budget used by the alternating-resolvent theorem. -/
theorem debt_le_beta_pairing (N : ℕ) (hN : 40 ≤ N)
    (ell f : Good N → ℚ) (debt : ℚ)
    (hell : ∀ i, lowerEll N (i.val+1) ≤ ell i)
    (hf : (11 / 25 : ℚ) • phaseV N ≤ f)
    (hd : debt ≤ ∑ i, debtWeight N i * goodReward N i) :
    debt ≤ beta N * dotProduct ell f := by
  refine hd.trans ?_
  rw [dotProduct, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i _
  have hg := (goodReward_pos N (by omega) i).le
  have hb := mul_le_mul_of_nonneg_right (debtWeight_le_beta N (by omega) i) hg
  have he : beta N * ((11 / 25 : ℚ) * lowerEll N (i.val+1) * t N (i.val+1)) *
      goodReward N i = beta N * (lowerEll N (i.val+1) * ((11 / 25 : ℚ) * phaseV N i)) := by
    rw [phaseV_eq_radialVector N (by omega)]
    unfold radialVector
    ring
  rw [he] at hb
  refine hb.trans (mul_le_mul_of_nonneg_left ?_ (beta_pos N (by omega)).le)
  exact mul_le_mul (hell i) (hf i)
    (mul_nonneg (by norm_num) (phaseV_pos N (by omega) i).le)
    ((lowerEll_pos hN (by omega)).le.trans (hell i))

/-- The lower phase and occupation bounds are strictly positive, not merely
nonnegative, because the physical good-rank set is nonempty. -/
theorem first_phase_pairing_pos (N : ℕ) (hN : 40 ≤ N)
    (ell f : Good N → ℚ)
    (hell : ∀ i, lowerEll N (i.val+1) ≤ ell i)
    (hf : (11 / 25 : ℚ) • phaseV N ≤ f) :
    0 < dotProduct ell f := by
  have he (i : Good N) : 0 < ell i :=
    lt_of_lt_of_le (lowerEll_pos hN (by omega)) (hell i)
  have hp (i : Good N) : 0 < f i :=
    lt_of_lt_of_le (mul_pos (by norm_num) (phaseV_pos N (by omega) i)) (hf i)
  apply Finset.sum_pos'
  · intro i _
    exact (mul_pos (he i) (hp i)).le
  · let i : Good N := ⟨0, by omega⟩
    exact ⟨i, Finset.mem_univ i, mul_pos (he i) (hp i)⟩

end SymmetricSector
