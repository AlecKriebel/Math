import SymmetricSector.Definitions
import SymmetricSector.Phase

/-! Explicit row bounds for the concrete coefficient matrix. These bounds
establish invertibility independently of the non-injective feature map. -/
namespace SymmetricSector
open scoped BigOperators

private theorem sum_rank_indicator_le (m r : ℕ) (w : ℚ) (hw : 0 ≤ w) :
    (∑ j : Fin m, if j.val = r then w else 0) ≤ w := by
  classical
  by_cases hr : r < m
  · have he : (∑ j : Fin m, if j.val = r then w else 0) = w := by
      rw [Finset.sum_eq_single (⟨r, hr⟩ : Fin m)]
      · simp
      · intro b _ hb
        have : b.val ≠ r := by
          intro h
          apply hb
          exact Fin.ext h
        simp [this]
      · simp
    exact he.le
  · have he : ∀ j : Fin m, j.val ≠ r := by
      intro j hj
      subst r
      exact hr j.isLt
    simpa [he] using hw

private theorem abs_choose_le {p q : Prop} [Decidable p] [Decidable q]
    (a b : ℚ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    |if p then a else if q then b else 0| ≤
      (if p then a else 0) + (if q then b else 0) := by
  split_ifs <;> simp_all [abs_of_nonneg]

private theorem sum_good_good_le (N : ℕ) (hN : 3 ≤ N) (i : Fin (N-1)) :
    (∑ j : Fin (N-1), |coefficientK N (.inl i) (.inl j)|) ≤
      (i.val+1 : ℚ)/(2*N) + ((N : ℚ)-(i.val+1)-1)/(2*N) := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hik : (i.val+1 : ℚ) < N := by
    exact_mod_cast (show i.val+1 < N by omega)
  have ha : 0 ≤ (i.val+1 : ℚ)/(2*N) := by positivity
  have hb : 0 ≤ ((N : ℚ)-(i.val+1)-1)/(2*N) := by
    apply div_nonneg
    · have hi : (i.val+2 : ℚ) ≤ N := by
        exact_mod_cast (show i.val+2 ≤ N by omega)
      linarith
    · positivity
  calc
    _ ≤ ∑ j : Fin (N-1),
        ((if j.val = i.val then (i.val+1 : ℚ)/(2*N) else 0) +
         (if j.val = i.val+1 then ((N : ℚ)-(i.val+1)-1)/(2*N) else 0)) := by
      apply Finset.sum_le_sum
      intro j _
      simpa only [coefficientK, Fin.ext_iff, eq_comm] using
        (abs_choose_le (p := j.val = i.val) (q := j.val = i.val+1) _ _ ha hb)
    _ = _ := Finset.sum_add_distrib
    _ ≤ _ := add_le_add (sum_rank_indicator_le _ _ _ ha) (sum_rank_indicator_le _ _ _ hb)

private theorem sum_good_bad_le (N : ℕ) (hN : 3 ≤ N) (i : Fin (N-1)) :
    (∑ j : Fin (N-2), |coefficientK N (.inl i) (.inr j)|) ≤ 1/(N : ℚ) := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hw : 0 ≤ 1/(N : ℚ) := by positivity
  have he : ∀ j : Fin (N-2), |coefficientK N (.inl i) (.inr j)| =
      if j.val = i.val then 1/(N : ℚ) else 0 := by
    intro j
    simp only [coefficientK]
    split_ifs <;> simp [abs_div, abs_of_nonneg (show 0 ≤ (N : ℚ) by positivity)]
  simp_rw [he]
  exact sum_rank_indicator_le _ _ _ hw

theorem good_abs_row_sum_lt_one (N : ℕ) (hN : 3 ≤ N) (i : Fin (N-1)) :
    ∑ j : Channel N, |coefficientK N (.inl i) j| < 1 := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  rw [Fintype.sum_sum_type]
  have h := add_le_add (sum_good_good_le N hN i) (sum_good_bad_le N hN i)
  have hd : 0 < (2*N : ℚ) := by positivity
  have he : (i.val+1 : ℚ)/(2*N) + ((N : ℚ)-(i.val+1)-1)/(2*N) + 1/N =
      (N+1)/(2*N) := by field_simp; ring
  rw [he] at h
  exact lt_of_le_of_lt h ((div_lt_one hd).2 (by linarith))

private theorem sum_pred_indicator_le (m r : ℕ) (w : ℚ) (hw : 0 ≤ w) :
    (∑ j : Fin m, if r = j.val+1 then w else 0) ≤ w := by
  by_cases hr : r = 0
  · simp [hr, hw]
  · have he : ∀ j : Fin m, (r = j.val+1) ↔ j.val = r-1 := by
      intro j
      omega
    simp_rw [he]
    exact sum_rank_indicator_le _ _ _ hw

private theorem sum_bad_good_le (N : ℕ) (hN : 3 ≤ N) (i : Fin (N-2)) :
    (∑ j : Fin (N-1), |coefficientK N (.inr i) (.inl j)|) ≤
      (i.val+1 : ℚ)/(2*(i.val+2)*N) +
      ((N : ℚ)-(i.val+2))/(2*(i.val+2)*N) := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hik : (i.val+2 : ℚ) < N := by
    exact_mod_cast (show i.val+2 < N by omega)
  have ha : 0 ≤ (i.val+1 : ℚ)/(2*(i.val+2)*N) := by positivity
  have hb : 0 ≤ ((N : ℚ)-(i.val+2))/(2*(i.val+2)*N) := by
    exact div_nonneg (by linarith) (by positivity)
  calc
    _ ≤ ∑ j : Fin (N-1),
        ((if j.val = i.val then (i.val+1 : ℚ)/(2*(i.val+2)*N) else 0) +
         (if j.val = i.val+1 then ((N : ℚ)-(i.val+2))/(2*(i.val+2)*N) else 0)) := by
      apply Finset.sum_le_sum
      intro j _
      have hk : (i.val+2 : ℚ)-1 = i.val+1 := by ring
      simpa only [coefficientK, hk] using
        (abs_choose_le (p := j.val = i.val) (q := j.val = i.val+1) _ _ ha hb)
    _ = _ := Finset.sum_add_distrib
    _ ≤ _ := add_le_add (sum_rank_indicator_le _ _ _ ha) (sum_rank_indicator_le _ _ _ hb)

private theorem sum_bad_bad_le (N : ℕ) (hN : 3 ≤ N) (i : Fin (N-2)) :
    (∑ j : Fin (N-2), |coefficientK N (.inr i) (.inr j)|) ≤
      (N*(i.val : ℚ)+(i.val+2))/(2*(i.val+2)*N) +
      ((i.val+1 : ℚ)*i.val)/(2*(i.val+2)*N) +
      ((N : ℚ)-(i.val+2)-1)/(2*N) := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hik : (i.val+3 : ℚ) ≤ N := by
    exact_mod_cast (show i.val+3 ≤ N by omega)
  have ha : 0 ≤ (N*(i.val : ℚ)+(i.val+2))/(2*(i.val+2)*N) := by positivity
  have hb : 0 ≤ ((i.val+1 : ℚ)*i.val)/(2*(i.val+2)*N) := by positivity
  have hc : 0 ≤ ((N : ℚ)-(i.val+2)-1)/(2*N) :=
    div_nonneg (by linarith) (by positivity)
  calc
    _ ≤ ∑ j : Fin (N-2),
      (((if j.val = i.val then (N*(i.val : ℚ)+(i.val+2))/(2*(i.val+2)*N) else 0) +
        (if i.val = j.val+1 then ((i.val+1 : ℚ)*i.val)/(2*(i.val+2)*N) else 0)) +
        (if j.val = i.val+1 then ((N : ℚ)-(i.val+2)-1)/(2*N) else 0)) := by
      apply Finset.sum_le_sum
      intro j _
      have hk₁ : (i.val+2 : ℚ)-1 = i.val+1 := by ring
      have hk₂ : (i.val+2 : ℚ)-2 = i.val := by ring
      by_cases hij : i = j
      · subst j
        have hn : ¬ i.val = i.val+1 := by omega
        simp [coefficientK, hk₁, hk₂, hn, abs_of_nonneg ha]
      · have hval : ¬ j.val = i.val := by intro h; exact hij (Fin.ext h.symm)
        by_cases hp : i.val = j.val+1
        · have hn : ¬ j.val = i.val+1 := by omega
          simp only [coefficientK, if_neg (Ne.symm hval), if_pos hp, if_neg hval,
            if_neg hn, hk₁, hk₂, zero_add, add_zero, abs_of_nonneg hb, le_refl]
        · by_cases hn : j.val = i.val+1
          · have hjbound : (i.val+4 : ℚ) ≤ N := by
              exact_mod_cast (show i.val+4 ≤ N by omega)
            have hactual : 0 ≤ ((N : ℚ)-(i.val+2)-2)/(2*N) :=
              div_nonneg (by linarith) (by positivity)
            simp only [coefficientK, if_neg (Ne.symm hval), if_neg hp, if_pos hn,
              if_neg hval, zero_add, abs_of_nonneg hactual]
            apply div_le_div_of_nonneg_right _ (by positivity)
            linarith
          · simp only [coefficientK, if_neg (Ne.symm hval), if_neg hval,
              if_neg hp, if_neg hn, abs_zero, zero_add, le_refl]
    _ = _ := by rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
    _ ≤ _ := add_le_add
      (add_le_add (sum_rank_indicator_le _ _ _ ha) (sum_pred_indicator_le _ _ _ hb))
      (sum_rank_indicator_le _ _ _ hc)

theorem bad_abs_row_sum_lt_one (N : ℕ) (hN : 3 ≤ N) (i : Fin (N-2)) :
    ∑ j : Channel N, |coefficientK N (.inr i) j| < 1 := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  rw [Fintype.sum_sum_type]
  have h := add_le_add (sum_bad_good_le N hN i) (sum_bad_bad_le N hN i)
  have hd : 0 < (2*(i.val+2)*N : ℚ) := by positivity
  have he :
      ((i.val+1 : ℚ)/(2*(i.val+2)*N) + ((N : ℚ)-(i.val+2))/(2*(i.val+2)*N)) +
      ((N*(i.val : ℚ)+(i.val+2))/(2*(i.val+2)*N) +
      ((i.val+1 : ℚ)*i.val)/(2*(i.val+2)*N) + ((N : ℚ)-(i.val+2)-1)/(2*N)) =
      1 - (N+3*(i.val+2)-1)/(2*(i.val+2)*N) := by
    field_simp
    ring
  rw [he] at h
  apply lt_of_le_of_lt h
  have hp : 0 < (N+3*(i.val+2)-1)/(2*(i.val+2)*N : ℚ) := by
    apply div_pos _ hd
    have hi0 : (0 : ℚ) ≤ i.val := by positivity
    linarith
  linarith

/-- Every row of the actual signed coefficient operator contracts absolute values. -/
theorem coefficientK_abs_row_sum_lt_one (N : ℕ) (hN : 3 ≤ N) (i : Channel N) :
    ∑ j, |coefficientK N i j| < 1 := by
  cases i with
  | inl i => exact good_abs_row_sum_lt_one N hN i
  | inr i => exact bad_abs_row_sum_lt_one N hN i

/-- The actual coefficient system has a unique solution at every required order. -/
theorem coefficient_system_isUnit (N : ℕ) (hN : 3 ≤ N) :
    IsUnit (1 - coefficientK N) :=
  Phase.isUnit_one_sub_of_abs_row_sum_lt_one _ (coefficientK_abs_row_sum_lt_one N hN)

#print axioms coefficient_system_isUnit
end SymmetricSector
