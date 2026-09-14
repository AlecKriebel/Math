import SymmetricSector.AllOrder
import SymmetricSector.PhysicalIdentity

/-! Formalized symmetric-balanced component of the fitness-two local proof.

These theorems concern the genuine active-chain expression ν₀ Δ G Δ G q.
They do not assert the coverage/collision identification with fixation,
stationary perturbation analyticity, the full tangent decomposition, the other
sector signs, or a full local-optimality theorem. -/
namespace SymmetricSector.Active
noncomputable section

/-- All-order strict positivity on each nonzero symmetric-balanced direction
at every population size where this sector can be nontrivial. -/
theorem R2_symmetricBalanced_pos {n : ℕ} (hn : 4 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) (hne : δ ≠ 0) :
    0 < R2 δ := by
  rw [R2_eq_frobeniusSq_mul_reducedScalar hn hδ]
  apply mul_pos (frobeniusSq_pos δ hne)
  exact_mod_cast reducedScalar_pos (n - 1) (by omega)

/-- Nonnegativity includes the absent three-label sector, where the actual
physical form is zero by the independently proved zero-matrix theorem. -/
theorem R2_symmetricBalanced_nonneg {n : ℕ} (hn : 3 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) :
    0 ≤ R2 δ := by
  by_cases hthree : n = 3
  · subst n
    rw [R2_symmetricBalanced_three hδ]
  · by_cases hzero : δ = 0
    · rw [hzero, R2_zero]
    · exact (R2_symmetricBalanced_pos (by omega) hδ hzero).le

/-- Exact zero case, including the absent sector at n=3. -/
theorem R2_symmetricBalanced_eq_zero_iff {n : ℕ} (hn : 3 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) :
    R2 δ = 0 ↔ δ = 0 := by
  constructor
  · intro hz
    by_cases hthree : n = 3
    · subst n
      exact symmetricBalanced_three_eq_zero hδ
    · by_contra hne
      exact (ne_of_gt (R2_symmetricBalanced_pos (by omega) hδ hne)) hz
  · rintro rfl
    exact R2_zero n

#print axioms R2_symmetricBalanced_pos
#print axioms R2_symmetricBalanced_nonneg
#print axioms R2_symmetricBalanced_eq_zero_iff

end
end SymmetricSector.Active
