import CyclicBell.GeneralCoverageSourceLiteralInterpolation
import CyclicBell.GeneralCoverageCovariance
import CyclicBell.GeneralEqualityPhases
import CyclicBell.GeneralSupportAlgebra

/-! Literal source coefficient operators and actual finite spectral calculus. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem source_relative_spectral_root (hd : 2≤d) (y : Ix d)
    (z : MatrixSpectrum (sourceRelative y)) : ∃ j : Ix d,(z : ℂ)=equalityRoot j :=
  equalityRoot_complete z
    (spectrum_unit_norm (toCMatrix_unitary (source_relative_unitary y)) z)
    (source_relative_spectral_power hd y z)

theorem sourceLiteralInversePolar_unit_on_spectrum (hd : 2≤d) (y : Ix d)
    (z : MatrixSpectrum (sourceRelative y)) :
    star (sourceLiteralInversePolar (d := d) z)*sourceLiteralInversePolar (d := d) z=1 := by
  obtain ⟨j,hj⟩ := source_relative_spectral_root hd y z
  rw [hj,sourceLiteralInversePolar_at_root hd,star_star,mul_comm]
  exact polarBase_unit j

theorem sourceLiteralInversePolar_finiteCalc (y : Ix d) :
    finiteCalc (sourceRelative y) (source_relative_unitary y) (sourceLiteralInversePolar (d := d)) =
      ∑ k : Ix d, sourceCosecantCoefficient k • ((sourceRelative y)ᴴ)^(k.val+1) := by
  unfold sourceLiteralInversePolar
  rw [finiteCalc_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [finiteCalc_smul,finiteCalc_pow]
  change sourceCosecantCoefficient k •
    finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => star (id z)) ^ (k.val+1) = _
  rw [finiteCalc_star,finiteCalc_coordinate]

theorem sourceBob_transpose_finiteCalc (y : Ix d) :
    (sourceBob y)ᵀ =
      finiteCalc (sourceRelative y) (source_relative_unitary y) (sourceLiteralInversePolar (d := d)) *
        (sourceClock d)ᴴ := by
  rw [sourceLiteralInversePolar_finiteCalc,sourceBob_transpose_polynomial]

theorem sourceLiteralInversePolar_finiteCalc_unitary (hd : 2≤d) (y : Ix d) :
    UnitaryRel (finiteCalc (sourceRelative y) (source_relative_unitary y)
      (sourceLiteralInversePolar (d := d))) := by
  constructor
  · rw [←finiteCalc_star,←finiteCalc_mul,←finiteCalc_one (sourceRelative y) (source_relative_unitary y)]
    apply finiteCalc_congr
    exact sourceLiteralInversePolar_unit_on_spectrum hd y
  · rw [←finiteCalc_star,←finiteCalc_mul,←finiteCalc_one (sourceRelative y) (source_relative_unitary y)]
    apply finiteCalc_congr
    intro z
    rw [mul_comm]
    exact sourceLiteralInversePolar_unit_on_spectrum hd y z

/-- Unitarity of the literal source Bob coefficients, without an assumed
coefficient-to-polar bridge or an assumed valid strategy. -/
theorem sourceBob_unitary (hd : 2≤d) (y : Ix d) : UnitaryRel (sourceBob y) := by
  have ht : UnitaryRel ((sourceBob y)ᵀ) := by
    rw [sourceBob_transpose_finiteCalc]
    exact (sourceLiteralInversePolar_finiteCalc_unitary hd y).mul source_clock_unitary.adjoint
  simpa only [Matrix.transpose_transpose] using unitary_transpose ht

end CyclicBell.General
