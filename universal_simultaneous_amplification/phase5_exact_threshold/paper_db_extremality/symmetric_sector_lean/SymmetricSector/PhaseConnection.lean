import SymmetricSector.RowBounds

/-! Concrete Schur reduction of the manuscript's reduced scalar. Blocks are
restrictions of the transpose of the actual coefficient operator, not independent
stand-ins. These exact algebraic connections are separate from the analytic
barrier inequalities needed to prove positivity. -/
namespace SymmetricSector
open Matrix
open scoped BigOperators

noncomputable section

abbrev Good (N : ℕ) := Fin (N - 1)
abbrev Bad (N : ℕ) := Fin (N - 2)

def phaseS (N : ℕ) : Matrix (Good N) (Good N) ℚ :=
  fun i j => coefficientK N (.inl j) (.inl i)
def phaseC (N : ℕ) : Matrix (Good N) (Bad N) ℚ :=
  fun i j => coefficientK N (.inr j) (.inl i)
def phaseD (N : ℕ) : Matrix (Bad N) (Good N) ℚ :=
  fun i j => -coefficientK N (.inl j) (.inr i)
def phaseQ (N : ℕ) : Matrix (Bad N) (Bad N) ℚ :=
  fun i j => coefficientK N (.inr j) (.inr i)

def goodSource (N : ℕ) : Good N → ℚ := fun i => source N (.inl i)
def badSource (N : ℕ) : Bad N → ℚ := fun i => source N (.inr i)
def goodReward (N : ℕ) : Good N → ℚ := fun i => reward N (.inl i)
def badReward (N : ℕ) : Bad N → ℚ := fun i => reward N (.inr i)

def phaseW (N : ℕ) : Bad N → ℚ := (1 - phaseQ N)⁻¹ *ᵥ (-badReward N)
def phaseF0 (N : ℕ) : Good N → ℚ :=
  (1 - phaseS N)⁻¹ *ᵥ (goodReward N - phaseC N *ᵥ phaseW N)
def phaseA (N : ℕ) : Matrix (Good N) (Good N) ℚ :=
  (1 - phaseS N)⁻¹ * phaseC N * (1 - phaseQ N)⁻¹ * phaseD N
def phaseEll (N : ℕ) : Good N → ℚ :=
  goodSource N - badSource N ᵥ* ((1 - phaseQ N)⁻¹ * phaseD N)
def phaseDebt (N : ℕ) : ℚ := dotProduct (badSource N) (phaseW N)

theorem phaseS_isUnit (N : ℕ) (hN : 3 ≤ N) : IsUnit (1 - phaseS N) := by
  have hu : IsUnit (1 - (phaseS N)ᵀ) :=
    Phase.isUnit_one_sub_of_abs_row_sum_lt_one _ (by
      intro i
      have h := coefficientK_abs_row_sum_lt_one N hN (.inl i)
      rw [Fintype.sum_sum_type] at h
      have hn : 0 ≤ ∑ j : Bad N, |coefficientK N (.inl i) (.inr j)| :=
        Finset.sum_nonneg fun _ _ => abs_nonneg _
      change ∑ j : Good N, |coefficientK N (.inl i) (.inl j)| < 1
      linarith)
  have he : (1 - (phaseS N)ᵀ)ᵀ = 1 - phaseS N := by simp
  rw [← he]
  exact (Matrix.isUnit_transpose _).mpr hu

theorem phaseQ_isUnit (N : ℕ) (hN : 3 ≤ N) : IsUnit (1 - phaseQ N) := by
  have hu : IsUnit (1 - (phaseQ N)ᵀ) :=
    Phase.isUnit_one_sub_of_abs_row_sum_lt_one _ (by
      intro i
      have h := coefficientK_abs_row_sum_lt_one N hN (.inr i)
      rw [Fintype.sum_sum_type] at h
      have hn : 0 ≤ ∑ j : Good N, |coefficientK N (.inr i) (.inl j)| :=
        Finset.sum_nonneg fun _ _ => abs_nonneg _
      change ∑ j : Bad N, |coefficientK N (.inr i) (.inr j)| < 1
      linarith)
  have he : (1 - (phaseQ N)ᵀ)ᵀ = 1 - phaseQ N := by simp
  rw [← he]
  exact (Matrix.isUnit_transpose _).mpr hu

/-- The adjoint system is the actual transpose of the coefficient system. -/
def dualSolution (N : ℕ) : Channel N → ℚ :=
  (1 - (coefficientK N)ᵀ)⁻¹ *ᵥ reward N

theorem dualSolution_equation (N : ℕ) (hN : 3 ≤ N) :
    (1 - (coefficientK N)ᵀ) *ᵥ dualSolution N = reward N := by
  have hu : IsUnit (1 - (coefficientK N)ᵀ) := by
    have h := (Matrix.isUnit_transpose _).mpr (coefficient_system_isUnit N hN)
    simpa using h
  rw [dualSolution, Matrix.mulVec_mulVec,
    Matrix.mul_nonsing_inv _ ((1 - (coefficientK N)ᵀ).isUnit_iff_isUnit_det.mp hu),
    Matrix.one_mulVec]

/-- Transposing the actual inverse preserves the scalar pairing exactly. -/
theorem reducedScalar_eq_dual_pairing (N : ℕ) :
    reducedScalar N = dotProduct (source N) (dualSolution N) := by
  unfold reducedScalar dualSolution
  rw [Matrix.dotProduct_mulVec, dotProduct_comm, ← Matrix.mulVec_transpose,
    Matrix.transpose_nonsing_inv]
  simp


def dualGood (N : ℕ) : Good N → ℚ := fun i => dualSolution N (.inl i)
def dualBad (N : ℕ) : Bad N → ℚ := fun i => dualSolution N (.inr i)

/-- The first block equation is obtained from the actual adjoint system. -/
theorem dualGood_equation (N : ℕ) (hN : 3 ≤ N) :
    (1 - phaseS N) *ᵥ dualGood N - phaseC N *ᵥ dualBad N = goodReward N := by
  ext i
  have hi := congrFun (dualSolution_equation N hN) (.inl i)
  simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply] at hi
  simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply,
    Matrix.mulVec, dotProduct, Fintype.sum_sum_type, Matrix.transpose_apply] at hi ⊢
  change dualSolution N (.inl i) -
      (∑ j, coefficientK N (.inl j) (.inl i) * dualSolution N (.inl j)) -
      (∑ j, coefficientK N (.inr j) (.inl i) * dualSolution N (.inr j)) =
      reward N (.inl i)
  linarith

/-- The bad block keeps the minus sign in H = [[S,C],[-D,Q]]. -/
theorem dualBad_equation (N : ℕ) (hN : 3 ≤ N) :
    phaseD N *ᵥ dualGood N + (1 - phaseQ N) *ᵥ dualBad N = badReward N := by
  ext i
  have hi := congrFun (dualSolution_equation N hN) (.inr i)
  simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply] at hi
  simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply,
    Matrix.mulVec, dotProduct, Fintype.sum_sum_type, Matrix.transpose_apply] at hi
  simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply, Pi.add_apply,
    Matrix.mulVec, dotProduct, phaseD, phaseQ, dualGood, dualBad, badReward,
    neg_mul, Finset.sum_neg_distrib]
  linarith

/-- A.19's complete alternating equation for the genuine dual solution. -/
theorem dualGood_schur (N : ℕ) (hN : 3 ≤ N) :
    (1 + phaseA N) *ᵥ dualGood N = phaseF0 N := by
  have h := Phase.schur_good_equation (phaseS N) (phaseS_isUnit N hN)
    (phaseQ N) (phaseQ_isUnit N hN) (phaseC N) (phaseD N)
    (dualGood N) (goodReward N) (dualBad N) (badReward N)
    (dualGood_equation N hN) (dualBad_equation N hN)
  simpa only [phaseA, phaseF0, phaseW, Matrix.mulVec_neg, sub_neg_eq_add] using h

/-- Exact scalar/debt identity for the actual quotient, without assuming phase
positivity or a physical-Hessian identification. -/
theorem reducedScalar_eq_schur_pairing (N : ℕ) (hN : 3 ≤ N) :
    reducedScalar N = dotProduct (phaseEll N) (dualGood N) - phaseDebt N := by
  rw [reducedScalar_eq_dual_pairing]
  have h := Phase.schur_scalar_identity (phaseQ N) (phaseQ_isUnit N hN)
    (phaseD N) (dualGood N) (goodSource N) (dualBad N) (badReward N) (badSource N)
    (dualBad_equation N hN)
  have he : dotProduct (source N) (dualSolution N) =
      dotProduct (goodSource N) (dualGood N) + dotProduct (badSource N) (dualBad N) := by
    exact Fintype.sum_sum_type _
  rw [he]
  exact h


/-- Both block equations for any supplied right-hand side of the actual dual
system; this also permits proving Schur invertibility without positivity. -/
theorem actual_dual_block_equations (N : ℕ) (z : Channel N → ℚ)
    (ga : Good N → ℚ) (gb : Bad N → ℚ)
    (hz : (1 - (coefficientK N)ᵀ) *ᵥ z = Sum.elim ga gb) :
    ((1 - phaseS N) *ᵥ (fun i => z (.inl i)) -
      phaseC N *ᵥ (fun i => z (.inr i)) = ga) ∧
    (phaseD N *ᵥ (fun i => z (.inl i)) +
      (1 - phaseQ N) *ᵥ (fun i => z (.inr i)) = gb) := by
  constructor
  · ext i
    have hi := congrFun hz (.inl i)
    simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply] at hi
    simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply,
      Matrix.mulVec, dotProduct, Fintype.sum_sum_type, Matrix.transpose_apply,
      Sum.elim_inl] at hi
    simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply,
      Matrix.mulVec, dotProduct, phaseS, phaseC]
    linarith
  · ext i
    have hi := congrFun hz (.inr i)
    simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply] at hi
    simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply,
      Matrix.mulVec, dotProduct, Fintype.sum_sum_type, Matrix.transpose_apply,
      Sum.elim_inr] at hi
    simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply, Pi.add_apply,
      Matrix.mulVec, dotProduct, phaseD, phaseQ, neg_mul, Finset.sum_neg_distrib]
    linarith

/-- The actual Schur matrix is invertible at every required finite order. -/
theorem phaseA_isUnit (N : ℕ) (hN : 3 ≤ N) : IsUnit (1 + phaseA N) := by
  have hu : IsUnit (1 - (coefficientK N)ᵀ) := by
    have h := (Matrix.isUnit_transpose _).mpr (coefficient_system_isUnit N hN)
    simpa using h
  apply Matrix.mulVec_surjective_iff_isUnit.mp
  intro b
  let rhs : Channel N → ℚ := Sum.elim ((1 - phaseS N) *ᵥ b) 0
  let z := (1 - (coefficientK N)ᵀ)⁻¹ *ᵥ rhs
  have hz : (1 - (coefficientK N)ᵀ) *ᵥ z = rhs := by
    dsimp only [z]
    rw [Matrix.mulVec_mulVec,
      Matrix.mul_nonsing_inv _ ((1 - (coefficientK N)ᵀ).isUnit_iff_isUnit_det.mp hu),
      Matrix.one_mulVec]
  obtain ⟨hzg, hzb⟩ := actual_dual_block_equations N z _ _ hz
  have hs := Phase.schur_good_equation (phaseS N) (phaseS_isUnit N hN)
    (phaseQ N) (phaseQ_isUnit N hN) (phaseC N) (phaseD N)
    (fun i => z (.inl i)) ((1 - phaseS N) *ᵥ b) (fun i => z (.inr i)) 0 hzg hzb
  refine ⟨fun i => z (.inl i), ?_⟩
  simpa only [phaseA, Matrix.mulVec_zero, add_zero, Matrix.mulVec_mulVec,
    Matrix.nonsing_inv_mul _ ((1 - phaseS N).isUnit_iff_isUnit_det.mp (phaseS_isUnit N hN)),
    Matrix.one_mulVec] using hs

/-- Appendix A.19 for the actual scalar, with all inverses proved legitimate. -/
theorem reducedScalar_schur_identity (N : ℕ) (hN : 3 ≤ N) :
    reducedScalar N =
      dotProduct (phaseEll N) ((1 + phaseA N)⁻¹ *ᵥ phaseF0 N) - phaseDebt N := by
  rw [reducedScalar_eq_schur_pairing N hN]
  rw [Phase.witness_eq_inverse_mulVec (1 + phaseA N) (phaseA_isUnit N hN)
    (phaseF0 N) (dualGood N) (dualGood_schur N hN)]

#print axioms phaseS_isUnit
#print axioms phaseQ_isUnit
#print axioms dualGood_schur
#print axioms reducedScalar_eq_schur_pairing
#print axioms phaseA_isUnit
#print axioms reducedScalar_schur_identity

end
end SymmetricSector
