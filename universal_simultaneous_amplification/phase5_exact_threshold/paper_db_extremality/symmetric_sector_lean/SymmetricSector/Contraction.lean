import SymmetricSector.GoodPhase

/-! Concrete completed-excursion contraction for the actual Schur blocks.
The supersolution retains the finite top boundary rather than inserting a
formal coefficient at a nonexistent bad rank. -/
namespace SymmetricSector
open Matrix
open scoped BigOperators

/-- A bad coordinate has a good coordinate with the same zero-based index. -/
def badAsGood {N : ℕ} (i : Bad N) : Good N := ⟨i.val, by have := i.isLt; omega⟩

/-- The A.27 bad-block barrier at physical bad rank `i+2`. -/
def phaseHhat (N : ℕ) (i : Bad N) : ℚ :=
  ((i.val : ℚ) + 2) / ((N : ℚ) - 2) * goodReward N (badAsGood i)

theorem phaseHhat_pos (N : ℕ) (hN : 3 ≤ N) (i : Bad N) :
    0 < phaseHhat N i := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  exact mul_pos (div_pos (by positivity) (by linarith))
    (goodReward_pos N hN (badAsGood i))

/-- Exact predecessor ratio, including the absent bottom bad coordinate. -/
theorem hhat_predecessor (N : ℕ) (hN : 3 ≤ N) (i : Bad N) :
    zeroExtend (phaseHhat N) ((i.val : ℤ) - 1) =
      ((i.val : ℚ) + 1) * i.val /
        (((N : ℚ) - 2) * ((N : ℚ) - i.val - 1)) * goodReward N (badAsGood i) := by
  by_cases hi : i.val = 0
  · simp [hi, zeroExtend_of_negative]
  · let j : Bad N := ⟨i.val - 1, by have := i.isLt; omega⟩
    have hji : j.val + 1 = i.val := by dsimp [j]; omega
    have hz : (i.val : ℤ) - 1 = j.val := by dsimp [j]; omega
    have hq : (j.val : ℚ) + 1 = i.val := by exact_mod_cast hji
    have hadj := goodReward_adjacent N hN (badAsGood i) (badAsGood j) hji
    have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
    have hiq : (i.val : ℚ) + 3 ≤ N := by
      exact_mod_cast (show i.val + 3 ≤ N by have := i.isLt; omega)
    have hn : (N : ℚ) - 2 ≠ 0 := by linarith
    have hd : (N : ℚ) - i.val - 1 ≠ 0 := by linarith
    have hgr : goodReward N (badAsGood j) =
        (i.val * goodReward N (badAsGood i)) / ((N : ℚ) - i.val - 1) := by
      apply (eq_div_iff hd).mpr
      dsimp only [badAsGood] at hadj ⊢
      linarith
    rw [hz, zeroExtend_at]
    unfold phaseHhat
    rw [hgr]
    have hj2 : (j.val : ℚ) + 2 = i.val + 1 := by linarith
    rw [hj2]
    field_simp [hn, hd]
    ring

/-- The missing top successor can only lower the barrier's Q action. -/
theorem hhat_successor_le (N : ℕ) (hN : 3 ≤ N) (i : Bad N) :
    zeroExtend (phaseHhat N) ((i.val : ℤ) + 1) ≤
      ((i.val : ℚ) + 3) * ((N : ℚ) - i.val - 2) /
        (((N : ℚ) - 2) * (i.val + 1)) * goodReward N (badAsGood i) := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hiq : (i.val : ℚ) + 3 ≤ N := by
    exact_mod_cast (show i.val + 3 ≤ N by have := i.isLt; omega)
  by_cases hi : i.val + 1 < N - 2
  · let j : Bad N := ⟨i.val + 1, hi⟩
    have hji : i.val + 1 = j.val := rfl
    have hz : (i.val : ℤ) + 1 = j.val := by simp [j]
    have hadj := goodReward_adjacent N hN (badAsGood j) (badAsGood i) hji
    have hn : (N : ℚ) - 2 ≠ 0 := by linarith
    have hd : (i.val : ℚ) + 1 ≠ 0 := by positivity
    have hgr : goodReward N (badAsGood j) =
        (((N : ℚ) - i.val - 2) * goodReward N (badAsGood i)) / (i.val + 1) := by
      apply (eq_div_iff hd).mpr
      dsimp only [badAsGood, j] at hadj ⊢
      push_cast at hadj ⊢
      linarith
    rw [hz, zeroExtend_at]
    apply le_of_eq
    unfold phaseHhat
    rw [hgr]
    dsimp only [j]
    push_cast
    field_simp [hn, hd]
    ring
  · rw [zeroExtend_of_le _ (by omega)]
    exact mul_nonneg (div_nonneg (mul_nonneg (by positivity) (by linarith))
      (mul_nonneg (by linarith) (by positivity))) (goodReward_pos N hN _).le

/-- Interior rational residual; the true top residual is at least this much. -/
theorem hhat_residual_lower (N : ℕ) (hN : 3 ≤ N) (i : Bad N) :
    ((N : ℚ)^2 - i.val - 1) /
        ((N : ℚ) * ((N : ℚ) - 2) * ((N : ℚ) - i.val - 1)) *
        goodReward N (badAsGood i) ≤
      ((1 - phaseQ N) *ᵥ phaseHhat N) i := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hiq : (i.val : ℚ) + 3 ≤ N := by
    exact_mod_cast (show i.val + 3 ≤ N by have := i.isLt; omega)
  have hn : (N : ℚ) ≠ 0 := by linarith
  have hn2 : (N : ℚ) - 2 ≠ 0 := by linarith
  have hx1 : (i.val : ℚ) + 1 ≠ 0 := by positivity
  have hx2 : (i.val : ℚ) + 2 ≠ 0 := by positivity
  have hx3 : (i.val : ℚ) + 3 ≠ 0 := by positivity
  have hnx : (N : ℚ) - i.val - 1 ≠ 0 := by linarith
  have hu := mul_le_mul_of_nonneg_left (hhat_successor_le N hN i)
    (show 0 ≤ ((i.val : ℚ) + 2) * (i.val + 1) / (2 * (i.val + 3) * N) by positivity)
  rw [Matrix.sub_mulVec, Matrix.one_mulVec]
  simp only [Pi.sub_apply, phaseQ_mulVec, hhat_predecessor N hN]
  calc
    _ = phaseHhat N i -
        (((N : ℚ) * i.val + i.val + 2) / (2 * (i.val + 2) * N) * phaseHhat N i +
          ((i.val : ℚ) + 2) * (i.val + 1) / (2 * (i.val + 3) * N) *
            (((i.val : ℚ) + 3) * ((N : ℚ) - i.val - 2) /
              (((N : ℚ) - 2) * (i.val + 1)) * goodReward N (badAsGood i)) +
          ((N : ℚ) - i.val - 3) / (2 * N) *
            (((i.val : ℚ) + 1) * i.val /
              (((N : ℚ) - 2) * ((N : ℚ) - i.val - 1)) * goodReward N (badAsGood i))) := by
      unfold phaseHhat
      field_simp [hn, hn2, hx1, hx2, hx3, hnx]
      ring
    _ ≤ _ := by linarith

/-- The radial upper bound implies the genuine bad-block supersolution. -/
theorem phaseHhat_supersolution (N : ℕ) (hN : 3 ≤ N) :
    phaseD N *ᵥ phaseV N ≤ (1 - phaseQ N) *ᵥ phaseHhat N := by
  intro i
  have ht := t_upper hN (show i.val + 1 ≤ N - 1 by have := i.isLt; omega)
  have hm := mul_le_mul_of_nonneg_right ht (goodReward_pos N hN (badAsGood i)).le
  have hn : (0 : ℚ) < N := by exact_mod_cast (show 0 < N by omega)
  have hm' := mul_le_mul_of_nonneg_left hm (show 0 ≤ 1 / (N : ℚ) by positivity)
  refine le_trans ?_ (hhat_residual_lower N hN i)
  rw [phaseD_mulVec, phaseV_eq_radialVector N hN]
  have hz : zeroExtend (radialVector N) (i.val : ℤ) =
      radialVector N (badAsGood i) := zeroExtend_at (radialVector N) (badAsGood i)
  rw [hz]
  unfold radialVector
  dsimp only [badAsGood]
  push_cast at hm'
  have hn2 : (N : ℚ) - 2 ≠ 0 := by
    have hh : (3 : ℚ) ≤ N := by exact_mod_cast hN
    linarith
  have hiq : (i.val : ℚ) + 3 ≤ N := by
    exact_mod_cast (show i.val + 3 ≤ N by have := i.isLt; omega)
  have hnx : (N : ℚ) - i.val - 1 ≠ 0 := by linarith
  have hnx' : (N : ℚ) - (i.val + 1) ≠ 0 := by linarith
  convert hm' using 1 <;> dsimp only [badAsGood]
  field_simp [hn.ne', hn2, hnx, hnx']
  ring

/-- The predecessor part of C times Hhat is exact at all good ranks. -/
theorem hhat_C_predecessor (N : ℕ) (hN : 3 ≤ N) (i : Good N) :
    ((N : ℚ) - i.val - 1) / (2 * (i.val + 1) * N) *
        zeroExtend (phaseHhat N) ((i.val : ℤ) - 1) =
      i.val / (2 * (N : ℚ) * ((N : ℚ) - 2)) * goodReward N i := by
  by_cases hi : i.val = 0
  · simp [hi, zeroExtend_of_negative]
  · let j : Bad N := ⟨i.val - 1, by have := i.isLt; omega⟩
    have hji : j.val + 1 = i.val := by dsimp [j]; omega
    have hz : (i.val : ℤ) - 1 = j.val := by dsimp [j]; omega
    have hq : (j.val : ℚ) + 1 = i.val := by exact_mod_cast hji
    have hadj := goodReward_adjacent N hN i (badAsGood j) hji
    have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
    have hiq : (i.val : ℚ) + 2 ≤ N := by
      exact_mod_cast (show i.val + 2 ≤ N by have := i.isLt; omega)
    have hn : (N : ℚ) ≠ 0 := by linarith
    have hn2 : (N : ℚ) - 2 ≠ 0 := by linarith
    have hx : (i.val : ℚ) + 1 ≠ 0 := by positivity
    have hd : (N : ℚ) - i.val - 1 ≠ 0 := by linarith
    have hgr : goodReward N (badAsGood j) =
        (i.val * goodReward N i) / ((N : ℚ) - i.val - 1) := by
      apply (eq_div_iff hd).mpr
      dsimp only [badAsGood] at hadj ⊢
      linarith
    rw [hz, zeroExtend_at]
    unfold phaseHhat
    rw [hgr]
    have hj2 : (j.val : ℚ) + 2 = i.val + 1 := by linarith
    rw [hj2]
    field_simp [hn, hn2, hx, hd]
    ring

/-- The actual exit C Hhat is bounded by the A.27 contraction constant.
The final good rank is treated separately because its same-index bad rank
is absent. -/
theorem phaseC_hhat_le (N : ℕ) (hN : 3 ≤ N) :
    phaseC N *ᵥ phaseHhat N ≤ c N • goodReward N := by
  intro i
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hn : (N : ℚ) ≠ 0 := by linarith
  have hn2 : (N : ℚ) - 2 ≠ 0 := by linarith
  have hx2 : (i.val : ℚ) + 2 ≠ 0 := by positivity
  have hden := c_den_pos hN
  rw [phaseC_mulVec, hhat_C_predecessor N hN]
  change _ ≤ c N * goodReward N i
  by_cases hi : i.val < N - 2
  · let j : Bad N := ⟨i.val, hi⟩
    have hz : zeroExtend (phaseHhat N) (i.val : ℤ) = phaseHhat N j :=
      zeroExtend_at (phaseHhat N) j
    have hj : badAsGood j = i := by apply Fin.ext; rfl
    rw [hz, phaseHhat, hj]
    dsimp only [j]
    have hiq : (i.val : ℚ) + 3 ≤ N := by
      exact_mod_cast (show i.val + 3 ≤ N by omega)
    calc
      _ = (2 * (i.val : ℚ) + 1) / (2 * N * ((N : ℚ) - 2)) * goodReward N i := by
        field_simp [hn, hn2, hx2]
        ring
      _ ≤ _ := mul_le_mul_of_nonneg_right
        ((div_le_div_iff_of_pos_right hden).mpr (by linarith)) (goodReward_pos N hN i).le
  · rw [zeroExtend_of_le _ (by omega), mul_zero, zero_add]
    have hiq : (i.val : ℚ) + 2 ≤ N := by
      exact_mod_cast (show i.val + 2 ≤ N by have := i.isLt; omega)
    exact mul_le_mul_of_nonneg_right
      ((div_le_div_iff_of_pos_right hden).mpr (by linarith)) (goodReward_pos N hN i).le

/-- The true bad inverse response to D v is controlled by Hhat. -/
theorem bad_inverse_D_phaseV_le (N : ℕ) (hN : 3 ≤ N) :
    (1 - phaseQ N)⁻¹ *ᵥ (phaseD N *ᵥ phaseV N) ≤ phaseHhat N := by
  have h := Phase.mulVec_mono ((1 - phaseQ N)⁻¹) (phaseQ_inverse_nonneg N hN)
    (phaseHhat_supersolution N hN)
  simp only [Matrix.mulVec_mulVec] at h
  rw [Matrix.nonsing_inv_mul _
    ((1 - phaseQ N).isUnit_iff_isUnit_det.mp (phaseQ_isUnit N hN)), Matrix.one_mulVec] at h
  simpa only [Matrix.mulVec_mulVec] using h

/-- A.27 for the genuine full completed-excursion operator. -/
theorem phaseA_phaseV_le (N : ℕ) (hN : 3 ≤ N) :
    phaseA N *ᵥ phaseV N ≤ c N • phaseV N := by
  have hb := bad_inverse_D_phaseV_le N hN
  have hc : phaseC N *ᵥ ((1 - phaseQ N)⁻¹ *ᵥ (phaseD N *ᵥ phaseV N)) ≤
      phaseC N *ᵥ phaseHhat N := by
    intro i
    exact Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left (hb j) (phaseC_nonneg N hN i j)
  have hs := Phase.mulVec_mono ((1 - phaseS N)⁻¹) (phaseS_inverse_nonneg N hN)
    (hc.trans (phaseC_hhat_le N hN))
  simpa only [phaseA, phaseV, Matrix.mulVec_mulVec, Matrix.mulVec_smul, Matrix.mul_assoc] using hs

#print axioms phaseHhat_supersolution
#print axioms phaseC_hhat_le
#print axioms phaseA_phaseV_le

end SymmetricSector
