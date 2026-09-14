import SymmetricSector.PhaseConnection

/-! Positivity of the actual Schur blocks and their true inverses. The proof
uses strict row bounds of the transposed subblocks, inherited from the concrete
coefficient matrix, then transposes the resulting inverse. -/
namespace SymmetricSector
open Matrix
open scoped BigOperators

 theorem phaseS_nonneg (N : ℕ) (hN : 3 ≤ N) (i j : Good N) :
    0 ≤ phaseS N i j := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hj : (j.val+2 : ℚ) ≤ N := by
    exact_mod_cast (show j.val+2 ≤ N by have := j.isLt; omega)
  simp only [phaseS, coefficientK]
  split_ifs
  · positivity
  · apply div_nonneg
    · linarith
    · positivity
  · exact le_refl _

 theorem phaseC_nonneg (N : ℕ) (hN : 3 ≤ N) (i : Good N) (j : Bad N) :
    0 ≤ phaseC N i j := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hj : (j.val+3 : ℚ) ≤ N := by
    exact_mod_cast (show j.val+3 ≤ N by have := j.isLt; omega)
  have hj0 : (0 : ℚ) ≤ j.val := by positivity
  simp only [phaseC, coefficientK]
  split_ifs
  · apply div_nonneg
    · linarith
    · positivity
  · apply div_nonneg
    · linarith
    · positivity
  · exact le_refl _

 theorem phaseD_nonneg (N : ℕ) (hN : 3 ≤ N) (i : Bad N) (j : Good N) :
    0 ≤ phaseD N i j := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  simp only [phaseD, coefficientK]
  split_ifs
  · simp only [neg_div, neg_neg]
    positivity
  · simp

 theorem phaseQ_nonneg (N : ℕ) (hN : 3 ≤ N) (i j : Bad N) :
    0 ≤ phaseQ N i j := by
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast hN
  have hj0 : (0 : ℚ) ≤ j.val := by positivity
  have hk₁ : (j.val+2 : ℚ)-1 = j.val+1 := by ring
  have hk₂ : (j.val+2 : ℚ)-2 = j.val := by ring
  simp only [phaseQ, coefficientK, hk₁, hk₂]
  split_ifs with hd hl hu
  · positivity
  · positivity
  · have hi := i.isLt
    have hj : (j.val+4 : ℚ) ≤ N := by
      exact_mod_cast (show j.val+4 ≤ N by omega)
    exact div_nonneg (by linarith) (by positivity)
  · exact le_refl _

 theorem phaseS_transpose_row_lt_one (N : ℕ) (hN : 3 ≤ N) (i : Good N) :
    ∑ j, (phaseS N)ᵀ i j < 1 := by
  have h := coefficientK_abs_row_sum_lt_one N hN (.inl i)
  rw [Fintype.sum_sum_type] at h
  have hn : 0 ≤ ∑ j : Bad N, |coefficientK N (.inl i) (.inr j)| :=
    Finset.sum_nonneg fun _ _ => abs_nonneg _
  have he : (∑ j : Good N, |coefficientK N (.inl i) (.inl j)|) =
      ∑ j, (phaseS N)ᵀ i j := by
    apply Finset.sum_congr rfl
    intro j _
    exact abs_of_nonneg (phaseS_nonneg N hN j i)
  rw [he] at h
  linarith

 theorem phaseQ_transpose_row_lt_one (N : ℕ) (hN : 3 ≤ N) (i : Bad N) :
    ∑ j, (phaseQ N)ᵀ i j < 1 := by
  have h := coefficientK_abs_row_sum_lt_one N hN (.inr i)
  rw [Fintype.sum_sum_type] at h
  have hn : 0 ≤ ∑ j : Good N, |coefficientK N (.inr i) (.inl j)| :=
    Finset.sum_nonneg fun _ _ => abs_nonneg _
  have he : (∑ j : Bad N, |coefficientK N (.inr i) (.inr j)|) =
      ∑ j, (phaseQ N)ᵀ i j := by
    apply Finset.sum_congr rfl
    intro j _
    exact abs_of_nonneg (phaseQ_nonneg N hN j i)
  rw [he] at h
  linarith

/-- Transposition transfers the checked maximum-principle inverse positivity. -/
private theorem inverse_nonneg_of_transpose_rows {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℚ) (hA : ∀ i j, 0 ≤ A i j)
    (hrow : ∀ i, ∑ j, Aᵀ i j < 1) : ∀ i j, 0 ≤ (1-A)⁻¹ i j := by
  have ht := Phase.inverse_entrywise_nonneg Aᵀ (fun i j => hA j i) hrow
  intro i j
  have h := ht j i
  have he : 1-Aᵀ = (1-A)ᵀ := by simp
  rw [he, ← Matrix.transpose_nonsing_inv] at h
  exact h

 theorem phaseS_inverse_nonneg (N : ℕ) (hN : 3 ≤ N) :
    ∀ i j, 0 ≤ (1-phaseS N)⁻¹ i j :=
  inverse_nonneg_of_transpose_rows _ (phaseS_nonneg N hN) (phaseS_transpose_row_lt_one N hN)

 theorem phaseQ_inverse_nonneg (N : ℕ) (hN : 3 ≤ N) :
    ∀ i j, 0 ≤ (1-phaseQ N)⁻¹ i j :=
  inverse_nonneg_of_transpose_rows _ (phaseQ_nonneg N hN) (phaseQ_transpose_row_lt_one N hN)

 theorem phaseA_nonneg (N : ℕ) (hN : 3 ≤ N) : ∀ i j, 0 ≤ phaseA N i j := by
  intro i j
  unfold phaseA
  simp only [Matrix.mul_apply]
  apply Finset.sum_nonneg
  intro k _
  apply mul_nonneg _ (phaseD_nonneg N hN k j)
  apply Finset.sum_nonneg
  intro l _
  apply mul_nonneg _ (phaseQ_inverse_nonneg N hN l k)
  apply Finset.sum_nonneg
  intro m _
  exact mul_nonneg (phaseS_inverse_nonneg N hN i m) (phaseC_nonneg N hN m l)

#print axioms phaseS_inverse_nonneg
#print axioms phaseQ_inverse_nonneg
#print axioms phaseA_nonneg
end SymmetricSector
