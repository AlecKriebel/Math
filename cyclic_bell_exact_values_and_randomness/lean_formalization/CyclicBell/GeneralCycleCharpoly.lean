import CyclicBell.GeneralCycles
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff
import Mathlib.Algebra.Polynomial.Degree.Support

/-! The characteristic polynomial stated after eq:weighted-cycle, for arbitrary
NONZERO complex weights, not only phases or product-one cycles. Cayley-Hamilton
and a coefficient-by-coefficient column calculation avoid assuming a spectral
basis or importing an external characteristic-polynomial certificate.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix Polynomial
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

/-- Prefix products along the orbit of computational basis vector zero. -/
def cyclePrefixProduct (w : Ix d → ℂ) (k : ℕ) : ℂ := ∏ r ∈ Finset.range k,w (r : Ix d)

theorem cyclePrefixProduct_nonzero (w : Ix d → ℂ) (hw : ∀ j,w j≠0) (k : ℕ) :
    cyclePrefixProduct w k≠0 := Finset.prod_ne_zero_iff.mpr (fun r _ => hw _)

theorem cycle_natCast_eq_iff {i j : ℕ} (hi : i<d) (hj : j<d) :
    (i : Ix d)=(j : Ix d) ↔ i=j := by
  constructor
  · intro h
    have he := congrArg ZMod.val h
    simpa only [ZMod.val_natCast,Nat.mod_eq_of_lt hi,Nat.mod_eq_of_lt hj] using he
  · intro h
    exact congrArg (fun n : ℕ => (n : Ix d)) h

/-- The first d orbit columns have disjoint supports. -/
theorem weighted_power_zero_column (w : Ix d → ℂ) {i k : ℕ} (hi : i<d) (hk : k<d) :
    (weightedCycle w^k) (i : Ix d) 0=if i=k then cyclePrefixProduct w k else 0 := by
  rw [weighted_power_entry]
  simp only [zero_add,cycle_natCast_eq_iff hi hk,cyclePrefixProduct]

theorem short_polynomial_column (w : Ix d → ℂ) (c : ℕ → ℂ) {i : ℕ} (hi : i<d) :
    (∑ k ∈ Finset.range d,c k*(weightedCycle w^k) (i : Ix d) 0)=c i*cyclePrefixProduct w i := by
  rw [Finset.sum_eq_single i]
  · rw [weighted_power_zero_column w hi hi,if_pos rfl]
  · intro k hk hki
    rw [weighted_power_zero_column w hi (Finset.mem_range.mp hk),if_neg (Ne.symm hki),mul_zero]
  · intro h
    exact (h (Finset.mem_range.mpr hi)).elim

/-- The only use of Cayley-Hamilton is an exact Lean-library theorem. The
coefficient expansion is obtained by applying aeval to the polynomial sum. -/
theorem charpoly_coefficient_expansion (M : Mat (Ix d)) :
    (∑ k ∈ Finset.range (d+1),M.charpoly.coeff k • M^k)=0 := by
  have h := congrArg (Polynomial.aeval M) M.charpoly.as_sum_range_C_mul_X_pow
  rw [Matrix.aeval_self_charpoly] at h
  simp only [map_sum,map_mul,map_pow,Polynomial.aeval_C,Polynomial.aeval_X,
    Algebra.algebraMap_eq_smul_one,smul_mul_assoc,one_mul,
    Matrix.charpoly_natDegree_eq_dim,ZMod.card] at h
  exact h.symm

theorem cycle_charpoly_top_coefficient (w : Ix d → ℂ) : (weightedCycle w).charpoly.coeff d=1 := by
  simpa only [Matrix.charpoly_natDegree_eq_dim,ZMod.card]
    using (Matrix.charpoly_monic (weightedCycle w)).coeff_natDegree

/-- The first column determines every coefficient below degree d. Nonzero
weights are used ONLY to cancel their finite prefix products. -/
theorem cycle_charpoly_low_coefficient (w : Ix d → ℂ) (hw : ∀ j,w j≠0)
    {i : ℕ} (hi : i<d) :
    (weightedCycle w).charpoly.coeff i=if i=0 then -(∏ j,w j) else 0 := by
  have h := charpoly_coefficient_expansion (weightedCycle w)
  rw [Finset.sum_range_succ,cycle_charpoly_top_coefficient,one_smul,weighted_full_power] at h
  have he := congrArg (fun T : Mat (Ix d) => T (i : Ix d) 0) h
  simp only [Matrix.add_apply,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul,Matrix.zero_apply] at he
  rw [short_polynomial_column w _ hi,Matrix.one_apply] at he
  have hd0 : 0<d := Nat.pos_of_ne_zero (NeZero.ne d)
  have hzero : ((i : Ix d)=0) ↔ i=0 := cycle_natCast_eq_iff hi hd0
  rw [hzero] at he
  by_cases hi0 : i=0
  · subst i
    simp only [cyclePrefixProduct,Finset.range_zero,Finset.prod_empty,mul_one,
      if_pos rfl] at he ⊢
    linear_combination he
  · rw [if_neg hi0] at he ⊢
    simp only [mul_zero,add_zero] at he
    exact (mul_eq_zero.mp he).resolve_right (cyclePrefixProduct_nonzero w hw i)

/-- Literal characteristic polynomial in the manuscript: X^d - product(weights).
The hypothesis does not require unit modulus, normalization or product one. -/
theorem weighted_cycle_charpoly (w : Ix d → ℂ) (hw : ∀ j,w j≠0) :
    (weightedCycle w).charpoly=Polynomial.X^d-Polynomial.C (∏ j,w j) := by
  apply Polynomial.ext
  intro k
  have hd0 : d≠0 := NeZero.ne d
  by_cases hk : k<d
  · rw [cycle_charpoly_low_coefficient w hw hk]
    simp only [Polynomial.coeff_sub,Polynomial.coeff_X_pow,Polynomial.coeff_C]
    have hdk : d≠k := Ne.symm (Nat.ne_of_lt hk)
    simp only [hdk,if_false,zero_sub]
    split_ifs <;> simp
  · by_cases hkd : k=d
    · subst k
      rw [cycle_charpoly_top_coefficient]
      simp [Polynomial.coeff_sub,Polynomial.coeff_X_pow,Polynomial.coeff_C,hd0]
    · have hgt : d<k := by omega
      have hp : (weightedCycle w).charpoly.natDegree<k := by
        simpa only [Matrix.charpoly_natDegree_eq_dim,ZMod.card] using hgt
      rw [Polynomial.coeff_eq_zero_of_natDegree_lt hp]
      have hk0 : k≠0 := by omega
      simp [Polynomial.coeff_sub,Polynomial.coeff_X_pow,Polynomial.coeff_C,hkd,Ne.symm hkd,hk0]

/-- Product-one phase cycles have the full d-th-root characteristic polynomial,
without identifying a chosen PVM outcome distribution with that spectrum. -/
theorem phase_cycle_charpoly (w : Ix d → ℂ) (hw : UnitPhases w) (hp : ∏ j,w j=1) :
    (weightedCycle w).charpoly=Polynomial.X^d-1 := by
  have hn (j : Ix d) : w j≠0 := by
    intro h
    have hj := hw j
    simp [h] at hj
  rw [weighted_cycle_charpoly w hn,hp,Polynomial.C_1]

end CyclicBell.General
