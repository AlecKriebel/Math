import SymmetricSector.BlockBounds
import SymmetricSector.RankBounds
import SymmetricSector.BlockActions

namespace SymmetricSector
open Matrix
open scoped BigOperators

/-- The genuine first good-channel response in (A.20). -/
noncomputable def phaseV (N : ℕ) : Good N → ℚ :=
  (1 - phaseS N)⁻¹ *ᵥ goodReward N

/-- Candidate for the exact radial formula in (A.20). -/
def radialVector (N : ℕ) (i : Good N) : ℚ :=
  t N (i.val + 1) * goodReward N i

theorem goodReward_pos (N : ℕ) (hN : 3 ≤ N) (i : Good N) :
    0 < goodReward N i := by
  have hi : i.val ≤ N - 2 := by have := i.isLt; omega
  have hchoose : 0 < (Nat.choose (N - 2) i.val : ℚ) := by
    exact_mod_cast Nat.choose_pos hi
  unfold goodReward reward
  apply div_pos hchoose
  positivity

/-- Binomial ratio at consecutive good indices, after clearing positive factors. -/
theorem goodReward_adjacent (N : ℕ) (hN : 3 ≤ N)
    (i j : Good N) (hji : j.val + 1 = i.val) :
    ((N : ℚ) - (i.val + 1)) * goodReward N j = i.val * goodReward N i := by
  have hj : j.val ≤ N - 2 := by have := j.isLt; omega
  have hi : i.val = j.val + 1 := hji.symm
  have hc := Nat.choose_succ_right_eq (N - 2) j.val
  have hsub : ((N - 2 - j.val : ℕ) : ℚ) = (N : ℚ) - (j.val + 2) := by
    rw [Nat.cast_sub hj, Nat.cast_sub (show 2 ≤ N by omega)]
    push_cast
    ring
  have hq : (Nat.choose (N - 2) (j.val + 1) : ℚ) * (j.val + 1) =
      Nat.choose (N - 2) j.val * ((N : ℚ) - (j.val + 2)) := by
    have hcq := congrArg (fun m : ℕ => (m : ℚ)) hc
    simp only [Nat.cast_mul, Nat.cast_add, Nat.cast_one] at hcq
    rw [hsub] at hcq
    exact hcq
  unfold goodReward reward
  simp only [hi]
  push_cast
  linear_combination -hq / (2 ^ (N - 1) * (N + 1))

/-- The weighted predecessor identity includes the absent bottom coordinate. -/
theorem radial_predecessor (N : ℕ) (hN : 3 ≤ N) (i : Good N) :
    ((N : ℚ) - i.val - 1) * zeroExtend (radialVector N) ((i.val : ℤ) - 1) =
      i.val * t N i.val * goodReward N i := by
  by_cases hi : i.val = 0
  · simp [hi, zeroExtend_of_negative, radialVector]
  · let j : Good N := ⟨i.val - 1, by have := i.isLt; omega⟩
    have hji : j.val + 1 = i.val := by dsimp [j]; omega
    have hz : (i.val : ℤ) - 1 = j.val := by dsimp [j]; omega
    rw [hz, zeroExtend_at]
    unfold radialVector
    rw [hji]
    have h := goodReward_adjacent N hN i j hji
    linear_combination (t N i.val) * h

/-- Cleared recurrence, whose denominator is positive at every good rank. -/
theorem t_step_cleared (N : ℕ) (hN : 3 ≤ N) (i : Good N) :
    (2 * (N : ℚ) - (i.val + 1)) * t N (i.val + 1) =
      2 * N + i.val * t N i.val := by
  have hi : (i.val : ℚ) + 1 < N := by
    exact_mod_cast (show i.val + 1 < N by have := i.isLt; omega)
  have hn : (0 : ℚ) < N := by exact_mod_cast (show 0 < N by omega)
  rw [t, mul_div_cancel₀]
  linarith

/-- The candidate solves the actual good block, including its bottom row. -/
theorem radialVector_equation (N : ℕ) (hN : 3 ≤ N) :
    (1 - phaseS N) *ᵥ radialVector N = goodReward N := by
  rw [Matrix.sub_mulVec, Matrix.one_mulVec]
  ext i
  simp only [Pi.sub_apply, phaseS_mulVec]
  have hp := radial_predecessor N hN i
  have hs := t_step_cleared N hN i
  have hn : (N : ℚ) ≠ 0 := by exact_mod_cast (show N ≠ 0 by omega)
  unfold radialVector at *
  field_simp [hn]
  linear_combination (goodReward N i) * hs - hp

/-- Exact A.20 identification with the genuine matrix inverse. -/
theorem phaseV_eq_radialVector (N : ℕ) (hN : 3 ≤ N) :
    phaseV N = radialVector N := by
  exact (Phase.witness_eq_inverse_mulVec (1 - phaseS N)
    (phaseS_isUnit N hN) (goodReward N) (radialVector N)
    (radialVector_equation N hN)).symm

theorem phaseV_pos (N : ℕ) (hN : 3 ≤ N) (i : Good N) : 0 < phaseV N i := by
  rw [phaseV_eq_radialVector N hN]
  exact mul_pos (t_pos hN (by omega) (by have := i.isLt; omega)) (goodReward_pos N hN i)

#print axioms phaseV_eq_radialVector
#print axioms phaseV_pos
end SymmetricSector
