import CyclicBell.Endpoints

/-! Focused mathematical negative controls. Unlike the intentionally rejected
files in validation/, these are TRUE statements in the default build. They
exercise normalization, the literal phase swap, and Bob's conjugation.
No claim of first-family canonical attainment is made in this module.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.D4
attribute [local simp] Matrix.cons_val_two Matrix.cons_val_three
set_option maxRecDepth 20000
set_option maxHeartbeats 12000000

/-- The canonical cyclic order gives q=(1,ζ²,-1,ζ²), not the swapped q. -/
def canonicalQ : Fin 4 → ℂ :=
  ![1, (h : ℂ) + h * Complex.I, -1, (h : ℂ) + h * Complex.I]

theorem canonicalQ_unit (j : Fin 4) : star (canonicalQ j) * canonicalQ j = 1 := by
  fin_cases j <;> apply Complex.ext <;>
    norm_num [canonicalQ, Complex.mul_re, Complex.mul_im] <;> nlinarith [h_sq]

def canonicalTargetPVM : PVM 4 := phasedPVM canonicalQ canonicalQ_unit

def canonicalTargetBorn (a b : Fin 4) : ℝ :=
  born targetState.density (canonicalTargetPVM.effect a) (bobTargetPVM.effect b)

/-- Altering the final phase back to the canonical order removes the bias. -/
theorem canonical_target_uniform (a b : Fin 4) : canonicalTargetBorn a b = 1 / 16 := by
  change born (projector phi) (projector (phasedVector canonicalQ a)) (projector (u b)) = _
  rw [← pureBorn_eq_born, pureBorn_projectors]
  fin_cases a <;> fin_cases b <;>
    norm_num [ip, tensorVec, phi, phasedVector, canonicalQ, u, fourier,
      Fintype.sum_prod_type, Fin.sum_univ_succ, Complex.normSq_apply,
      Complex.mul_re, Complex.mul_im] <;> nlinarith [h_sq]

theorem altered_witness_changes_target : canonicalTargetBorn 0 1 ≠ targetBorn 0 1 := by
  rw [canonical_target_uniform, target_01]
  norm_num

theorem swapped_q_is_not_canonical : q ≠ canonicalQ := by
  intro he
  have hj := congrFun he (3 : Fin 4)
  have hr := congrArg Complex.re hj
  norm_num [q, canonicalQ] at hr
  nlinarith [h_sq]

/-- Dropping the conjugation of V_0 changes the encoded observable. -/
theorem bob_conjugation_is_essential :
    witnessB 0 ≠ weighted (fun j => zeta ^ polarExponents 0 j) := by
  intro he
  have hj := congrFun (congrFun he (1 : Fin 4)) (0 : Fin 4)
  have hi := congrArg Complex.im hj
  norm_num [witnessB, weighted_entry, bobWeights, bobExponents, polarExponents,
    shift, Complex.mul_re, Complex.mul_im] at hi
  norm_num [zeta_components] at hi
  linarith [s_pos]

/-- Adjoint and entrywise conjugation are not interchangeable here. -/
theorem bob_adjoint_is_wrong :
    witnessB 0 ≠ (weighted (fun j => zeta ^ polarExponents 0 j)).conjTranspose := by
  intro he
  have hj := congrFun (congrFun he (1 : Fin 4)) (0 : Fin 4)
  have hi := congrArg Complex.im hj
  norm_num [witnessB, weighted_entry, Matrix.conjTranspose_apply, bobWeights,
    bobExponents, polarExponents, shift,
    Complex.mul_re, Complex.mul_im] at hi
  norm_num [zeta_components] at hi
  linarith [s_pos]

theorem first_target_positive : 0 < firstTargetValue := by
  unfold firstTargetValue
  have hs : 0 < Real.sin (Real.pi / 8) := s_pos
  positivity

/-- The source's displayed operator is NOT normalized by an extra d=4. -/
theorem extra_factor_four_is_wrong :
    firstAugmentedValue firstStrategy ≠ firstTargetValue / 4 := by
  rw [first_attainment]
  intro he
  linarith [first_target_positive]

end CyclicBell.D4
