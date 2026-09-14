import SymmetricSector.Incoming
import SymmetricSector.PhysicalBridge

/-! Appendix A.16–A.17b for the actual labeled feature function and perturbation.
The scalar reward weights are deduced from labeled predecessor enumeration and
actual subset orbits in `Incoming`, rather than specified as moment hypotheses.
-/
namespace SymmetricSector.Active
noncomputable section
open scoped BigOperators
open Finset

/-- The two exact binomial rewards of A.16, applied to arbitrary feature
coefficients. This identity already uses the actual active-chain expression
`ν₀ Δ F`; its channel ranges and all normalizing powers are proved. -/
theorem nu0_perturbation_feature {N : ℕ} (hN : 3 ≤ N)
    (δ : Matrix (Fin (N + 1)) (Fin (N + 1)) ℝ) (hδ : SymmetricBalanced δ)
    (a b : ℕ → ℝ) :
    dotProduct nu0 ((perturbation δ).mulVec (feature δ a b)) =
      frobeniusSq δ *
        ((∑ j ∈ range (N - 1), (Nat.choose (N - 2) j : ℝ) * a (j + 1)) /
            (2 ^ (N - 1) * ((N : ℝ) + 1)) -
         (∑ j ∈ range (N - 2), (Nat.choose (N - 3) j : ℝ) * b (j + 2)) /
            (2 ^ (N - 2) * ((N : ℝ) + 1))) := by
  rw [nu0_perturbation_feature_orbits (by omega) δ hδ a b]
  have hidx : N + 1 - 2 = N - 1 := by omega
  simp only [Nat.add_sub_cancel, hidx, Nat.cast_add, Nat.cast_one]
  congr 1
  rw [← sum_div, sum_add_distrib, sum_orbitA N (by omega), sum_orbitB N hN]
  have hb :
      (∑ j ∈ range (N - 2), (-2 * (Nat.choose (N - 3) j : ℝ)) * b (j + 2)) =
      -2 * ∑ j ∈ range (N - 2), (Nat.choose (N - 3) j : ℝ) * b (j + 2) := by
    rw [mul_sum]
    apply sum_congr rfl
    intro j hj
    ring
  rw [hb]
  have hexp : N - 1 = (N - 2) + 1 := by omega
  rw [hexp, pow_succ]
  field_simp
  ring

#print axioms nu0_perturbation_feature

/-- The manuscript reward vector is exactly the reward of its actual extended
feature function. This matches A.16 coefficient by coefficient over both
printed channels, not merely at selected population sizes. -/
theorem nu0_perturbation_coeff_feature {N : ℕ} (hN : 3 ≤ N)
    (δ : Matrix (Fin (N + 1)) (Fin (N + 1)) ℝ) (hδ : SymmetricBalanced δ)
    (c : Channel N → ℚ) :
    dotProduct nu0 ((perturbation δ).mulVec
      (feature δ (coeffA N c) (coeffB N c))) =
      frobeniusSq δ * ((dotProduct (reward N) c : ℚ) : ℝ) := by
  rw [nu0_perturbation_feature hN δ hδ]
  congr 1
  rw [← Fin.sum_univ_eq_sum_range, ← Fin.sum_univ_eq_sum_range]
  simp_rw [coeffA_at, coeffB_at]
  simp only [dotProduct, Fintype.sum_sum_type, reward]
  push_cast
  simp only [div_mul_eq_mul_div, neg_mul, neg_div, sum_neg_distrib]
  rw [← sum_div, ← sum_div]
  ring

/-- Every matrix's squared Frobenius norm is nonnegative. -/
theorem frobeniusSq_nonneg {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ) :
    0 ≤ frobeniusSq δ := by
  exact sum_nonneg (fun v _ => sum_nonneg (fun i _ => sq_nonneg (δ v i)))

/-- A nonzero physical perturbation has strictly positive squared Frobenius norm. -/
theorem frobeniusSq_pos {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ) (hδ : δ ≠ 0) :
    0 < frobeniusSq δ := by
  have hex : ∃ v i, δ v i ≠ 0 := by
    by_contra! hh
    apply hδ
    ext v i
    exact hh v i
  obtain ⟨v, i, hvi⟩ := hex
  apply sum_pos' (fun v _ => sum_nonneg (fun i _ => sq_nonneg (δ v i)))
  refine ⟨v, mem_univ v, ?_⟩
  apply sum_pos' (fun i _ => sq_nonneg (δ v i))
  exact ⟨i, mem_univ i, sq_pos_of_ne_zero hvi⟩

#print axioms nu0_perturbation_coeff_feature
#print axioms frobeniusSq_pos

end
end SymmetricSector.Active
