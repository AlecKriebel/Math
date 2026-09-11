import Bell.Witness

/-!
# The ideal three-state discrimination problem (paper §3.1)

The weak-duality proof below quantifies over arbitrary complex three-outcome
qubit POVMs.  It uses their positive quadratic forms, not a finite search over
measurements. This is only the IDEAL discrimination problem, not the global
Bell optimization over variable states and Bob measurements.
-/

noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

def idealScoreOperator : Fin 3 → Operator :=
  ![ !![3/10,0;0,0], !![0,0;0,3/10], !![1/5,1/5;1/5,1/5] ]

def idealDual : Operator := !![8/25,2/25;2/25,8/25]

def idealDiscriminationScore (M : POVM 3) : ℝ :=
  ∑ j, (Matrix.trace (idealScoreOperator j * M.effect j)).re

def slackGram0 : Operator := !![1/10,4/10;1/10,4/10]
def slackGram1 : Operator := !![4/10,1/10;4/10,1/10]
def slackGram2 : Matrix (Fin 3) Qubit ℂ :=
  !![1/5,-1/5;1/5,-1/5;1/5,-1/5]

theorem ideal_dual_slack0 :
    slackGram0.conjTranspose * slackGram0 = idealDual-idealScoreOperator 0 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [slackGram0,idealDual,idealScoreOperator,
      Matrix.conjTranspose_apply,Matrix.mul_apply,Fin.sum_univ_succ]

theorem ideal_dual_slack1 :
    slackGram1.conjTranspose * slackGram1 = idealDual-idealScoreOperator 1 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [slackGram1,idealDual,idealScoreOperator,
      Matrix.conjTranspose_apply,Matrix.mul_apply,Fin.sum_univ_succ]

theorem ideal_dual_slack2 :
    slackGram2.conjTranspose * slackGram2 = idealDual-idealScoreOperator 2 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [slackGram2,idealDual,idealScoreOperator,
      Matrix.conjTranspose_apply,Matrix.mul_apply,Fin.sum_univ_succ]

theorem ideal_dual_feasible (j : Fin 3) :
    (idealDual-idealScoreOperator j).PosSemidef := by
  fin_cases j
  · rw [← ideal_dual_slack0]
    exact gram_positive slackGram0
  · rw [← ideal_dual_slack1]
    exact gram_positive slackGram1
  · rw [← ideal_dual_slack2]
    exact gram_positive slackGram2

theorem ideal_complementarity (j : Fin 3) :
    (idealDual-idealScoreOperator j)*aliceEffect 2 j=0 := by
  fin_cases j <;> funext i k <;> fin_cases i <;> fin_cases k <;>
    norm_num [idealDual,idealScoreOperator,aliceEffect,aux0,aux1,aux2,
      Matrix.mul_apply,Fin.sum_univ_succ]

/-- The ideal POVM bound, for every complex three-outcome qubit POVM. -/
theorem ideal_discrimination_upper (M : POVM 3) :
    idealDiscriminationScore M ≤ 16/25 := by
  have hp0 := (M.positive 0).re_dotProduct_nonneg (![(1:ℂ),4])
  have hp1 := (M.positive 1).re_dotProduct_nonneg (![(4:ℂ),1])
  have hp2 := (M.positive 2).re_dotProduct_nonneg (![(1:ℂ),-1])
  have h00 := congrArg (fun A : Operator => (A 0 0).re) M.normalized
  have h01 := congrArg (fun A : Operator => (A 0 1).re) M.normalized
  have h10 := congrArg (fun A : Operator => (A 1 0).re) M.normalized
  have h11 := congrArg (fun A : Operator => (A 1 1).re) M.normalized
  change 0 ≤ (dotProduct (star (![(1:ℂ),4]))
    (M.effect 0 *ᵥ ![(1:ℂ),4])).re at hp0
  change 0 ≤ (dotProduct (star (![(4:ℂ),1]))
    (M.effect 1 *ᵥ ![(4:ℂ),1])).re at hp1
  change 0 ≤ (dotProduct (star (![(1:ℂ),-1]))
    (M.effect 2 *ᵥ ![(1:ℂ),-1])).re at hp2
  unfold idealDiscriminationScore
  norm_num [idealScoreOperator,Matrix.trace,Matrix.mul_apply,Matrix.mulVec,
    dotProduct,Fin.sum_univ_succ,Matrix.one_apply] at hp0 hp1 hp2 h00 h01 h10 h11 ⊢
  linarith

theorem ideal_discrimination_attained :
    idealDiscriminationScore (witnessStrategy.alice 2)=16/25 := by
  norm_num [idealDiscriminationScore,idealScoreOperator,witnessStrategy,
    aliceEffect,aux0,aux1,aux2,Matrix.trace,Matrix.mul_apply,Fin.sum_univ_succ]

end Bell
