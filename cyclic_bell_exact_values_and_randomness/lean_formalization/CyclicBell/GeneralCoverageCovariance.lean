import CyclicBell.GeneralFiniteSpectrum

/-! Naturality of the actual matrix finite functional calculus. These results
are used to transport the source polar factors under the clock Weyl action. -/

noncomputable section
open scoped ComplexOrder Matrix
namespace CyclicBell.General

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem finiteCalc_toCMatrix (U : Mat ι) (hU : UnitaryRel U) (f : ℂ → ℂ) :
    toCMatrix (finiteCalc U hU f) = cfc f (toCMatrix U) := by
  rw [cfc_apply f (toCMatrix U) (starUnitary_normal (toCMatrix_unitary hU))
    ((matrixSpectrum_finite U).continuousOn f)]
  rfl

/-- Arbitrary scalar functions are permitted because the spectrum is finite. -/
theorem finiteCalc_unitary_conjugation (U V : Mat ι) (hU : UnitaryRel U)
    (hV : UnitaryRel V) (f : ℂ → ℂ) :
    V * finiteCalc U hU f * Vᴴ =
      finiteCalc (V * U * Vᴴ) ((hV.mul hU).mul hV.adjoint) f := by
  apply CStarMatrix.ofMatrix.injective
  change conjugationHom (toCMatrix V) (toCMatrix_unitary hV)
      (toCMatrix (finiteCalc U hU f)) =
    toCMatrix (finiteCalc (V * U * Vᴴ) ((hV.mul hU).mul hV.adjoint) f)
  rw [finiteCalc_toCMatrix,finiteCalc_toCMatrix]
  exact (conjugationHom (toCMatrix V) (toCMatrix_unitary hV)).map_cfc f (toCMatrix U)
    ((matrixSpectrum_finite U).continuousOn f)
    (conjugationHom_continuous _ _)
    (starUnitary_normal (toCMatrix_unitary hU))
    (starUnitary_normal (toCMatrix_unitary ((hV.mul hU).mul hV.adjoint)))

theorem finiteCalc_scalar_argument (U : Mat ι) (hU : UnitaryRel U)
    (c : ℂ) (hc : star c*c=1) (f : ℂ → ℂ) :
    finiteCalc (c • U) (hU.scalar hc) f = finiteCalc U hU (fun z => f (c*z)) := by
  apply CStarMatrix.ofMatrix.injective
  change toCMatrix (finiteCalc (c • U) (hU.scalar hc) f) =
    toCMatrix (finiteCalc U hU (fun z => f (c*z)))
  rw [finiteCalc_toCMatrix,finiteCalc_toCMatrix]
  have h := cfc_comp f (fun z : ℂ => c*z) (toCMatrix U)
    (starUnitary_normal (toCMatrix_unitary hU))
    (((matrixSpectrum_finite U).image (fun z : ℂ => c*z)).continuousOn f)
    (by fun_prop)
  rw [cfc_const_mul_id c (toCMatrix U) (starUnitary_normal (toCMatrix_unitary hU))] at h
  exact h.symm

theorem finiteCalc_operator_congr (U V : Mat ι) (hU : UnitaryRel U)
    (hV : UnitaryRel V) (h : U=V) (f : ℂ → ℂ) :
    finiteCalc U hU f = finiteCalc V hV f := by
  subst V
  rfl

/-- Clock covariance, derived from a Weyl relation rather than assumed for
all functions of the relative unitary. -/
theorem finiteCalc_covariance (U V : Mat ι) (hU : UnitaryRel U)
    (hV : UnitaryRel V) (c : ℂ) (hc : star c*c=1)
    (hVU : V * U * Vᴴ = c • U) (f : ℂ → ℂ) :
    V * finiteCalc U hU f * Vᴴ = finiteCalc U hU (fun z => f (c*z)) := by
  have h := finiteCalc_unitary_conjugation U V hU hV f
  exact h.trans ((finiteCalc_operator_congr _ _ _ (hU.scalar hc) hVU f).trans
    (finiteCalc_scalar_argument U hU c hc f))

end CyclicBell.General
