import SymmetricSector.PhysicalIdentity
import SymmetricSector.Small03
import SymmetricSector.Small04

/-! The two requested scalar consistency checks transported to the actual
physical quadratic form. These supplement, and do not replace, its proved
general population-size identity. -/
namespace SymmetricSector.Active
noncomputable section

/-- N=3 means physical population size n=4, not n=3. -/
theorem R2_four_normalization {δ : Matrix (Fin 4) (Fin 4) ℝ}
    (hδ : SymmetricBalanced δ) :
    R2 δ = (3 / 208 : ℝ) * frobeniusSq δ := by
  rw [R2_eq_frobeniusSq_mul_reducedScalar (by norm_num) hδ]
  norm_num only [show 4 - 1 = 3 by omega, SymmetricSector.Cert3.value,
    Rat.cast_div, Rat.cast_natCast]
  ring

/-- N=4 means physical population size n=5. -/
theorem R2_five_normalization {δ : Matrix (Fin 5) (Fin 5) ℝ}
    (hδ : SymmetricBalanced δ) :
    R2 δ = (359 / 26660 : ℝ) * frobeniusSq δ := by
  rw [R2_eq_frobeniusSq_mul_reducedScalar (by norm_num) hδ]
  norm_num only [show 5 - 1 = 4 by omega, SymmetricSector.Cert4.value,
    Rat.cast_div, Rat.cast_natCast]
  ring

#print axioms R2_four_normalization
#print axioms R2_five_normalization

end
end SymmetricSector.Active
