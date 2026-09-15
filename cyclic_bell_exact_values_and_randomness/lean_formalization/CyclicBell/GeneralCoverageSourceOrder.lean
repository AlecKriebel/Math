import CyclicBell.GeneralCoverageSourceOrbit
import CyclicBell.GeneralCoverageTwistedPower

/-! Measurement order for the actual cosecant source observables. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem finiteCalc_orderedProduct {ι : Type*} [Fintype ι] [DecidableEq ι]
    (U : Mat ι) (hU : UnitaryRel U) (f : ℕ → ℂ → ℂ) (n : ℕ) :
    Coverage.orderedProduct (fun k => finiteCalc U hU (f k)) n =
      finiteCalc U hU (fun z => Coverage.orderedProduct (fun k => f k z) n) := by
  induction n with
  | zero => simp
  | succ n ih =>
    simp only [Coverage.orderedProduct_succ]
    rw [ih,←finiteCalc_mul]

theorem scalar_orderedProduct_range (f : ℕ → ℂ) (n : ℕ) :
    Coverage.orderedProduct f n=∏ k ∈ Finset.range n,f k := by
  induction n with
  | zero => simp
  | succ n ih => rw [Coverage.orderedProduct_succ,Finset.prod_range_succ,ih]

theorem source_finEquiv_apply (i : Fin d) : ZMod.finEquiv d i=(i.val : Ix d) := by
  cases d with
  | zero => exact False.elim (NeZero.ne 0 rfl)
  | succ n => exact (ZMod.natCast_zmod_val (n := n+1) i).symm

theorem source_product_range (f : Ix d → ℂ) :
    (∏ k ∈ Finset.range d,f (k : Ix d))=∏ k : Ix d,f k := by
  rw [←Fin.prod_univ_eq_prod_range]
  exact Fintype.prod_equiv (ZMod.finEquiv d).toEquiv
    (fun i : Fin d => f (i.val : Ix d)) f (by intro i; exact congrArg f (source_finEquiv_apply i).symm)

theorem source_inverse_polar_ordered_product (hd : 2≤d) (y : Ix d) :
    Coverage.orderedProduct (fun n =>
      finiteCalc (sourceRelative y) (source_relative_unitary y)
        (fun z => sourceLiteralInversePolar (d := d) (chi (-(n : Ix d))*z))) d=1 := by
  rw [finiteCalc_orderedProduct,←finiteCalc_one (sourceRelative y) (source_relative_unitary y)]
  apply finiteCalc_congr
  intro z
  obtain ⟨j,hj⟩ := source_relative_spectral_root hd y z
  rw [hj,scalar_orderedProduct_range]
  rw [source_product_range (fun k : Ix d => sourceLiteralInversePolar (d := d) (chi (-k)*equalityRoot j))]
  exact sourceLiteralInversePolar_orbit_product hd j

/-- The source observable is an actual order-d unitary for every d≥2,
including composite dimensions. -/
theorem sourceBob_order (hd : 2≤d) (y : Ix d) : sourceBob y^d=1 := by
  have hz : ((sourceClock d)ᴴ)^d=1 := by
    rw [←Matrix.conjTranspose_pow,source_clock_order,Matrix.conjTranspose_one]
  have hQ : ((sourceBob y)ᵀ)^d=1 := by
    rw [sourceBob_transpose_finiteCalc]
    have ht := Coverage.conjugate_twisted_power
      (finiteCalc (sourceRelative y) (source_relative_unitary y) (sourceLiteralInversePolar (d := d)))
      ((sourceClock d)ᴴ) (show StarUnitary ((sourceClock d)ᴴ) from source_clock_unitary.adjoint) d
    rw [ht]
    change Coverage.orderedProduct (fun n =>
      ((sourceClock d)ᴴ)^n * finiteCalc (sourceRelative y) (source_relative_unitary y)
        (sourceLiteralInversePolar (d := d)) * ((sourceClock d)ᴴ)ᴴ^n) d * ((sourceClock d)ᴴ)^d=1
    simp only [Matrix.conjTranspose_conjTranspose,source_finiteCalc_clock_covariance]
    rw [source_inverse_polar_ordered_product hd,hz,one_mul]
  have h := congrArg Matrix.transpose hQ
  simpa only [Matrix.transpose_pow,Matrix.transpose_transpose,Matrix.transpose_one] using h

end CyclicBell.General
