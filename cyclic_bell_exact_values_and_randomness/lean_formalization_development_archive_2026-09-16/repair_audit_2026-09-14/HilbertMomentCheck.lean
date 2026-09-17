import CyclicBell.GeneralCommuting
noncomputable section
open scoped BigOperators ComplexOrder InnerProductSpace
namespace CyclicBell.General
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
def hilbertMoment (ψ : H) (T : H →L[ℂ] H) : ℂ := ⟪ψ, T ψ⟫_ℂ

theorem hilbertMoment_add (ψ : H) (S T : H →L[ℂ] H) :
    hilbertMoment ψ (S+T) = hilbertMoment ψ S + hilbertMoment ψ T := by
  simp [hilbertMoment,inner_add_right]

theorem hilbertMoment_smul (ψ : H) (z : ℂ) (T : H →L[ℂ] H) :
    hilbertMoment ψ (z • T) = z * hilbertMoment ψ T := by
  simp [hilbertMoment,inner_smul_right]

theorem hilbertMoment_sum {J : Type*} [Fintype J] (ψ : H) (T : J → H →L[ℂ] H) :
    hilbertMoment ψ (∑ j,T j) = ∑ j,hilbertMoment ψ (T j) := by
  simp [hilbertMoment,inner_sum]

theorem hilbertMoment_star (ψ : H) (T : H →L[ℂ] H) :
    star (hilbertMoment ψ T) = hilbertMoment ψ (star T) := by
  change star (⟪ψ, T ψ⟫_ℂ) = ⟪ψ, T.adjoint ψ⟫_ℂ
  rw [T.adjoint_inner_right]
  exact inner_conj_symm (T ψ) ψ

theorem hilbertMoment_selfadjoint (ψ : H) (T : H →L[ℂ] H) (hT : star T = T) :
    hilbertMoment ψ T = (vectorEval ψ T : ℂ) := by
  have hs : star (hilbertMoment ψ T) = hilbertMoment ψ T := by
    rw [hilbertMoment_star,hT]
  apply Complex.ext
  · rfl
  · have hi := congrArg Complex.im hs
    change -(hilbertMoment ψ T).im = (hilbertMoment ψ T).im at hi
    change (hilbertMoment ψ T).im = 0
    linarith

theorem vectorEval_hermitianPart (ψ : H) (T : H →L[ℂ] H) :
    vectorEval ψ (algebraHerm T) = vectorEval ψ T := by
  change (hilbertMoment ψ (algebraHerm T)).re = (hilbertMoment ψ T).re
  rw [algebraHerm,hilbertMoment_smul,hilbertMoment_add,← hilbertMoment_star]
  simp [Complex.mul_re]
  ring


end CyclicBell.General
