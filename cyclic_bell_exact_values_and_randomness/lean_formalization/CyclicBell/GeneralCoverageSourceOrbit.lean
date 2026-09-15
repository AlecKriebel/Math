import CyclicBell.GeneralCoverageSourceFactors

/-! Covariance and cyclic phase product for the literal source observable. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem source_relative_clock_conjugation (y : Ix d) (n : ℕ) :
    ((sourceClock d)ᴴ)^n*sourceRelative y*((sourceClock d)^n)=
      chi (-(n : Ix d)) • sourceRelative y := by
  rw [←Matrix.conjTranspose_pow,source_clock_power,Matrix.diagonal_conjTranspose,
    source_relative_weights]
  ext i j
  simp only [Matrix.diagonal_mul,Matrix.mul_diagonal,Matrix.smul_apply,smul_eq_mul,weightedCycle]
  by_cases hij : i=j+1
  · subst i
    simp only [if_pos rfl,ite_true,mul_one,Pi.star_apply,chi_star,←chi_add]
    congr 1
    ring
  · simp [hij]

theorem source_finiteCalc_clock_covariance (y : Ix d) (n : ℕ) (f : ℂ → ℂ) :
    ((sourceClock d)ᴴ)^n*finiteCalc (sourceRelative y) (source_relative_unitary y) f*
      ((sourceClock d)^n)=
      finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => f (chi (-(n : Ix d))*z)) := by
  have h := finiteCalc_covariance (sourceRelative y) (((sourceClock d)ᴴ)^n)
    (source_relative_unitary y) (source_clock_unitary.adjoint.pow n)
    (chi (-(n : Ix d))) (chi_star_mul _)
    (by simpa only [Matrix.conjTranspose_pow,Matrix.conjTranspose_conjTranspose] using
      source_relative_clock_conjugation y n) f
  simpa only [Matrix.conjTranspose_pow,Matrix.conjTranspose_conjTranspose] using h

theorem source_root_rotated (j k : Ix d) : chi (-k)*equalityRoot j=equalityRoot (j-k) := by
  simp only [equalityRoot,sub_eq_add_neg,chi_add]
  ring

theorem source_polar_product_reindex (j : Ix d) :
    (∏ k : Ix d,polarBase (j-k))=∏ k : Ix d,polarBase k := by
  exact Fintype.prod_equiv (Equiv.subLeft j)
    (fun k : Ix d => polarBase (j-k)) (fun k : Ix d => polarBase k) (by intro k; rfl)

theorem sourceLiteralInversePolar_orbit_product (hd : 2≤d) (j : Ix d) :
    (∏ k : Ix d,sourceLiteralInversePolar (d := d) (chi (-k)*equalityRoot j))=1 := by
  simp_rw [source_root_rotated,sourceLiteralInversePolar_at_root hd]
  change (∏ k : Ix d,(starRingEnd ℂ) (polarBase (j-k)))=1
  rw [←map_prod (starRingEnd ℂ),source_polar_product_reindex,polarBase_product]
  simp

end CyclicBell.General
