import CyclicBell.GeneralEqualityPhases

/-! Converse to outcome encoding: every order-d unitary defines an actual
positive, complete, pairwise orthogonal d-outcome measurement. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι : Type*} [Fintype ι] [DecidableEq ι] [Nonempty ι]

theorem finite_order_spectral_root (U : Mat ι) (hU : UnitaryRel U) (horder : U^d=1)
    (z : MatrixSpectrum U) : ∃ a : Ix d,(z : ℂ)=chi a := by
  have hp : (toCMatrix U)^d=1 := congrArg toCMatrix horder
  have hz : (z : ℂ)^d ∈ spectrum ℂ ((toCMatrix U)^d) := by
    rw [spectrum.map_pow]
    exact ⟨z,z.property,rfl⟩
  rw [hp,show (1 : CMat ι)=algebraMap ℂ (CMat ι) 1 by simp,spectrum.scalar_eq] at hz
  exact unit_power_root_character z (spectrum_unit_norm (toCMatrix_unitary hU) z) hz

theorem finite_order_spectral_complete (U : Mat ι) (hU : UnitaryRel U) (horder : U^d=1) :
    (∑ a : Ix d,finiteSpectralProjection U hU (chi a))=1 := by
  unfold finiteSpectralProjection
  rw [←finiteCalc_sum,←finiteCalc_one U hU]
  apply finiteCalc_congr
  intro z
  obtain ⟨a,ha⟩ := finite_order_spectral_root U hU horder z
  simp only [ha,chi_injective.eq_iff]
  simp

def finiteOrderMeasurement (U : Mat ι) (hU : UnitaryRel U) (horder : U^d=1) : Measurement d ι where
  effect a := finiteSpectralProjection U hU (chi a)
  positive a := by
    have h := Matrix.posSemidef_conjTranspose_mul_self (finiteSpectralProjection U hU (chi a))
    rw [finiteSpectralProjection_star,finiteSpectralProjection_mul,if_pos rfl] at h
    exact h
  complete := finite_order_spectral_complete U hU horder
  idempotent a := by rw [finiteSpectralProjection_mul,if_pos rfl]
  orthogonal a b hab := by
    rw [finiteSpectralProjection_mul,if_neg (fun h => hab (chi_injective h))]

theorem finiteOrderMeasurement_encoding (U : Mat ι) (hU : UnitaryRel U) (horder : U^d=1) :
    encoded (finiteOrderMeasurement U hU horder)=U := by
  change (∑ a : Ix d,chi a • finiteSpectralProjection U hU (chi a))=U
  unfold finiteSpectralProjection
  simp_rw [←finiteCalc_smul]
  rw [←finiteCalc_sum]
  conv_rhs => rw [←finiteCalc_coordinate U hU]
  apply finiteCalc_congr
  intro z
  obtain ⟨a,ha⟩ := finite_order_spectral_root U hU horder z
  simp only [ha,chi_injective.eq_iff,id_eq]
  simp

end CyclicBell.General
