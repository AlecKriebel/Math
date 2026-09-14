import SymmetricSector.BlockActions
import SymmetricSector.Gradients
import SymmetricSector.RankBounds
import SymmetricSector.BadBarriers

namespace SymmetricSector
open Matrix
open scoped BigOperators

/-- A sharper left supersolution than A.28; bad rank is `i+2`. -/
def leftBarrier (N : ℕ) : Bad N → ℚ := fun i => 2 / (3 * (i.val + 1))
/-- The printed A.28 barrier. -/
def printedLeftBarrier (N : ℕ) : Bad N → ℚ :=
  fun i => 2 * (i.val + 3) / (3 * (i.val + 2) * (i.val + 1))

theorem leftBarrier_nonneg (N : ℕ) (i : Bad N) : 0 ≤ leftBarrier N i := by
  unfold leftBarrier
  positivity

private theorem leftBarrier_prev (N : ℕ) (i : Bad N) (hi : 0 < i.val) :
    zeroExtend (leftBarrier N) ((i.val : ℤ)-1) = 2/(3*(i.val:ℚ)) := by
  let j : Bad N := ⟨i.val-1, by have := i.isLt; omega⟩
  have hj : ((j.val : ℤ)) = (i.val : ℤ)-1 := by dsimp [j]; omega
  rw [← hj, zeroExtend_at]
  dsimp [leftBarrier, j]
  rw [Nat.cast_sub (by omega : 1 ≤ i.val), Nat.cast_one]
  ring

private theorem leftBarrier_next (N : ℕ) (i : Bad N) (hi : i.val+1 < N-2) :
    zeroExtend (leftBarrier N) ((i.val : ℤ)+1) = 2/(3*(i.val+2:ℚ)) := by
  let j : Bad N := ⟨i.val+1, hi⟩
  have hj : ((j.val : ℤ)) = (i.val : ℤ)+1 := by simp [j]
  rw [← hj, zeroExtend_at]
  dsimp [leftBarrier, j]
  push_cast
  ring

/-- The sharper barrier dominates the universal upper bound on the bad source.
All three physical rank cases are checked, including both absent neighbors. -/
theorem leftBarrier_supersolution (N : ℕ) (hN : 4 ≤ N) :
    (fun i : Bad N => 1/((i.val+2:ℚ)*(i.val+1))) ≤
      (1-(phaseQ N)ᵀ) *ᵥ leftBarrier N := by
  intro i
  have hNq : (4:ℚ) ≤ N := by exact_mod_cast hN
  have hN0 : (N:ℚ) ≠ 0 := by linarith
  have hi0 : (0:ℚ) ≤ i.val := by positivity
  have hi1 : (i.val:ℚ)+1 ≠ 0 := by positivity
  have hi2 : (i.val:ℚ)+2 ≠ 0 := by positivity
  simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply]
  rw [phaseQ_transpose_mulVec]
  by_cases hb : i.val=0
  · have hn : i.val+1 < N-2 := by omega
    rw [leftBarrier_next N i hn]
    simp only [leftBarrier, hb, Nat.cast_zero]
    norm_num
    have hr : 2/3 - ((2:ℚ)/(4*N)*(2/3) + ((N:ℚ)-4)/(2*N)*(1/3)) - 1/2 =
        1/(3*N) := by field_simp; ring
    have hp : (0:ℚ) ≤ 1/(3*N) := by positivity
    linarith
  · rw [leftBarrier_prev N i (by omega)]
    have hiq : (0:ℚ) < i.val := by exact_mod_cast (show 0 < i.val by omega)
    have hiN := i.isLt
    by_cases ht : i.val+1 < N-2
    · rw [leftBarrier_next N i ht]
      dsimp only [leftBarrier]
      have hr : 2/(3*(i.val+1:ℚ)) -
          (((N:ℚ)*i.val+i.val+2)/(2*(i.val+2)*N)*(2/(3*(i.val+1))) +
           ((i.val:ℚ)+1)*i.val/(2*(i.val+2)*N)*(2/(3*i.val)) +
           ((N:ℚ)-i.val-4)/(2*N)*(2/(3*(i.val+2)))) -
          1/((i.val+2:ℚ)*(i.val+1)) =
          (2*i.val+1)/(3*N*(i.val+2)*(i.val+1)) := by
        field_simp [hN0, hi1, hi2, ne_of_gt hiq]
        <;> ring
      have hp : (0:ℚ) ≤ (2*i.val+1)/(3*N*(i.val+2)*(i.val+1)) := by positivity
      linarith
    · rw [zeroExtend_of_le _ (by omega : ((N-2:ℕ):ℤ) ≤ (i.val:ℤ)+1)]
      dsimp only [leftBarrier]
      have hn : (N:ℚ) = i.val+3 := by exact_mod_cast (show N=i.val+3 by omega)
      have hr : 2/(3*(i.val+1:ℚ)) -
          (((N:ℚ)*i.val+i.val+2)/(2*(i.val+2)*N)*(2/(3*(i.val+1))) +
           ((i.val:ℚ)+1)*i.val/(2*(i.val+2)*N)*(2/(3*i.val)) +
           ((N:ℚ)-i.val-4)/(2*N)*0) -
          1/((i.val+2:ℚ)*(i.val+1)) =
          i.val/(3*N*(i.val+2)*(i.val+1)) := by
        rw [hn]
        field_simp [hi1, hi2, ne_of_gt hiq]
        <;> ring
      have hp : (0:ℚ) ≤ i.val/(3*N*(i.val+2)*(i.val+1)) := by positivity
      linarith

/-- The source inequality uses the actual recursively defined Poisson gradient. -/
theorem badSource_le_reciprocal (N : ℕ) (hN : 4 ≤ N) (i : Bad N) :
    badSource N i ≤ 1/((i.val+2:ℚ)*(i.val+1)) := by
  have hi := i.isLt
  have hg := gradient_le_reciprocal N (i.val+1) (by omega) (by omega) (by omega)
  have hh := div_le_div_of_nonneg_right hg (by positivity : (0:ℚ) ≤ 2*(i.val+2))
  change gradient N (i.val+1)/(2*(i.val+2)) ≤ _
  refine hh.trans_eq ?_
  push_cast
  field_simp
  <;> ring

/-- True inverse left occupation is bounded by the sharper supersolution. -/
theorem leftOccupation_le_barrier (N : ℕ) (hN : 4 ≤ N) :
    badSource N ᵥ* (1-phaseQ N)⁻¹ ≤ leftBarrier N := by
  have hh := Phase.inverse_mulVec_le_supersolution (phaseQ N)ᵀ
    (fun i j => phaseQ_nonneg N (by omega) j i)
    (phaseQ_transpose_row_lt_one N (by omega)) (badSource N) (leftBarrier N)
    (fun i => (badSource_le_reciprocal N hN i).trans (leftBarrier_supersolution N hN i))
  have he : 1-(phaseQ N)ᵀ = (1-phaseQ N)ᵀ := by simp
  rw [he, ← Matrix.transpose_nonsing_inv, Matrix.mulVec_transpose] at hh
  exact hh

theorem leftBarrier_le_printed (N : ℕ) (i : Bad N) :
    leftBarrier N i ≤ printedLeftBarrier N i := by
  unfold leftBarrier printedLeftBarrier
  have hi0 : (0:ℚ) ≤ i.val := by positivity
  have hi1 : (i.val:ℚ)+1 ≠ 0 := by positivity
  have hi2 : (i.val:ℚ)+2 ≠ 0 := by positivity
  have he : 2*(i.val+3:ℚ)/(3*(i.val+2)*(i.val+1)) - 2/(3*(i.val+1)) =
      2/(3*(i.val+2)*(i.val+1)) := by field_simp; ring
  have hp : (0:ℚ) ≤ 2/(3*(i.val+2)*(i.val+1)) := by positivity
  linarith

/-- The actual Schur occupation is bounded below at every good rank. -/
theorem phaseEll_lower (N : ℕ) (hN : 4 ≤ N) (i : Good N) :
    lowerEll N (i.val+1) ≤ phaseEll N i := by
  have hNq : (4:ℚ) ≤ N := by exact_mod_cast hN
  have hN0 : (N:ℚ) ≠ 0 := by linarith
  have hi0 : (0:ℚ) ≤ i.val := by positivity
  have hi1 : (i.val:ℚ)+1 ≠ 0 := by positivity
  have hi2 : (i.val:ℚ)+2 ≠ 0 := by positivity
  have hoc := leftOccupation_le_barrier N hN
  have hmul : ((badSource N ᵥ* (1-phaseQ N)⁻¹) ᵥ* phaseD N) i ≤
      (leftBarrier N ᵥ* phaseD N) i := by
    exact Finset.sum_le_sum fun j _ =>
      mul_le_mul_of_nonneg_right (hoc j) (phaseD_nonneg N (by omega) j i)
  have hd : (leftBarrier N ᵥ* phaseD N) i ≤
      (1/(N:ℚ))*(2/(3*(i.val+1))) := by
    rw [← Matrix.mulVec_transpose, phaseD_transpose_mulVec]
    apply mul_le_mul_of_nonneg_left _ (by positivity)
    by_cases hi : i.val < N-2
    · let j : Bad N := ⟨i.val, hi⟩
      have he : (i.val:ℤ) = j.val := rfl
      rw [he, zeroExtend_at]
      exact le_refl _
    · rw [zeroExtend_of_le _ (by omega : ((N-2:ℕ):ℤ) ≤ i.val)]
      positivity
  have hg := (gradient_bounds N (i.val+1) (by omega) (by omega)
    (by have := i.isLt; omega)).1
  have hgs : ((N:ℚ)-2)/(N*(i.val+1)) ≤ goodSource N i := by
    change _ ≤ gradient N (i.val+1)/2
    push_cast at hg
    have he : 2*((N:ℚ)-2)/(N*(i.val+1)) = 2*(((N:ℚ)-2)/(N*(i.val+1))) := by ring
    rw [he] at hg
    linarith
  have he : ((N:ℚ)-2)/(N*(i.val+1)) - (1/(N:ℚ))*(2/(3*(i.val+1))) -
      lowerEll N (i.val+1) = 2/(3*N*(i.val+1)*(i.val+2)) := by
    unfold lowerEll
    push_cast
    field_simp
    <;> ring
  have hp : (0:ℚ) ≤ 2/(3*N*(i.val+1)*(i.val+2)) := by positivity
  unfold phaseEll
  rw [← Matrix.vecMul_vecMul]
  change lowerEll N (i.val+1) ≤ goodSource N i - _
  linarith

/-- Embed the bad index into the preceding good rank. -/
def goodBelow (N : ℕ) (i : Bad N) : Good N := ⟨i.val, by have := i.isLt; omega⟩
/-- Embed the bad index into the good rank with the same physical rank. -/
def goodAbove (N : ℕ) (i : Bad N) : Good N := ⟨i.val+1, by have := i.isLt; omega⟩

/-- The sharper barrier cancels the exact binomial reward ratio. -/
theorem leftBarrier_reward (N : ℕ) (hN : 4 ≤ N) (i : Bad N) :
    leftBarrier N i * (-badReward N i) =
      (4/(3*((N:ℚ)-2))) * goodReward N (goodAbove N i) := by
  have hh := badReward_good_pred_ratio N (by omega) (goodAbove N i)
  have hi : (((goodAbove N i).val:ℤ)-1) = i.val := by simp [goodAbove]
  rw [hi, zeroExtend_at] at hh
  simp only [Pi.neg_apply] at hh
  have hv : ((goodAbove N i).val:ℚ) = i.val+1 := by simp [goodAbove]
  rw [hv] at hh
  rw [hh]
  unfold leftBarrier
  have hi0 : (0:ℚ) ≤ i.val := by positivity
  have hi1 : (i.val:ℚ)+1 ≠ 0 := by positivity
  have hNq : (4:ℚ) ≤ N := by exact_mod_cast hN
  have hN2 : (N:ℚ)-2 ≠ 0 := by linarith
  field_simp
  <;> ring

/-- Reflection of the binomial weights removes the apparent reward index shift. -/
theorem goodReward_above_reflect (N : ℕ) (i : Bad N) :
    goodReward N (goodAbove N i) = goodReward N (goodBelow N i.rev) := by
  have hi := i.isLt
  have he : (N-2)-(i.val+1) = i.rev.val := by simp only [Fin.val_rev, Nat.sub_add_eq]
  have hc := Nat.choose_symm (show i.val+1 ≤ N-2 by omega)
  change (Nat.choose (N-2) (i.val+1):ℚ)/(2^(N-1)*(N+1)) =
    (Nat.choose (N-2) i.rev.val:ℚ)/(2^(N-1)*(N+1))
  rw [← he, hc]

/-- The source-inverse pairing is bounded by the sharper barrier reward. -/
theorem phaseDebt_le_barrier_pairing (N : ℕ) (hN : 4 ≤ N) :
    phaseDebt N ≤ dotProduct (leftBarrier N) (-badReward N) := by
  unfold phaseDebt phaseW
  rw [Matrix.dotProduct_mulVec]
  exact Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_right
    (leftOccupation_le_barrier N hN i) (negative_badReward_nonneg N i)

/-- A stronger form of the printed A.31 debt bound, derived from the actual
source, inverse and reward. -/
theorem phaseDebt_le_constant_sum (N : ℕ) (hN : 4 ≤ N) :
    phaseDebt N ≤ ∑ i : Bad N,
      (4/(3*((N:ℚ)-2))) * goodReward N (goodBelow N i) := by
  have he : dotProduct (leftBarrier N) (-badReward N) =
      ∑ i : Bad N, (4/(3*((N:ℚ)-2))) * goodReward N (goodBelow N i) := by
    unfold dotProduct
    simp only [Pi.neg_apply, leftBarrier_reward N hN, goodReward_above_reflect]
    exact Equiv.sum_comp (Fin.revPerm : Equiv.Perm (Bad N))
      (fun i : Bad N => (4/(3*((N:ℚ)-2))) * goodReward N (goodBelow N i))
  exact (phaseDebt_le_barrier_pairing N hN).trans_eq he

/-- The printed A.31 bound is now checked through a sharper supersolution;
the original A.28 barrier alone does not justify its shifted reward indexing. -/
theorem phaseDebt_le_printed (N : ℕ) (hN : 4 ≤ N) :
    phaseDebt N ≤ ∑ i : Bad N,
      (4*(i.val+3)/(3*(i.val+2)*((N:ℚ)-2))) * goodReward N (goodBelow N i) := by
  apply (phaseDebt_le_constant_sum N hN).trans
  apply Finset.sum_le_sum
  intro i _
  apply mul_le_mul_of_nonneg_right _ (goodReward_pos N (by omega) _).le
  have hNq : (4:ℚ) ≤ N := by exact_mod_cast hN
  have hi0 : (0:ℚ) ≤ i.val := by positivity
  have hi2 : (i.val:ℚ)+2 ≠ 0 := by positivity
  have hN2 : (N:ℚ)-2 ≠ 0 := by linarith
  have he : 4*(i.val+3)/(3*(i.val+2)*((N:ℚ)-2)) - 4/(3*((N:ℚ)-2)) =
      4/(3*(i.val+2)*((N:ℚ)-2)) := by field_simp; ring
  have hN2p : (0:ℚ) < (N:ℚ)-2 := by linarith
  have hp : (0:ℚ) ≤ 4/(3*(i.val+2)*((N:ℚ)-2)) := by positivity
  linarith

#print axioms leftBarrier_supersolution
#print axioms leftOccupation_le_barrier
#print axioms phaseEll_lower
#print axioms phaseDebt_le_printed

end SymmetricSector
