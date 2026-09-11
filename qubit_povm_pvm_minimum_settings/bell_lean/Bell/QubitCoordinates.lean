import Bell.Expectation
import Bell.IncidenceAlgebra
import Bell.ProjectiveFiber

/-!
# Exact real coordinates for complex Hermitian qubit operators

The positive cone, its nonzero null boundary and strict interior are related to
actual Matrix.PosSemidef/PosDef predicates. The imaginary Pauli coordinate is
retained; none of these definitions restricts the quantum model to real qubits.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix ComplexOrder
namespace Bell.QubitGeometry
open Bell.Lorentz

/-- Pauli-coordinate encoding as a real linear map. -/
def pauli : V →ₗ[ℝ] Operator where
  toFun := fun x =>
    !![(x 0 + x 3 : ℝ), (x 1 : ℂ) - (x 2 : ℂ) * Complex.I;
       (x 1 : ℂ) + (x 2 : ℂ) * Complex.I, (x 0 - x 3 : ℝ)]
  map_add' := by
    intro x y
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Pi.add_apply] <;> ring
  map_smul' := by
    intro t x
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Pi.smul_apply, smul_eq_mul] <;> ring

/-- Decoding is defined on all matrices; it is inverse on the Hermitian subspace. -/
def coordinates : Operator →ₗ[ℝ] V where
  toFun := fun A => ![(A 0 0).re / 2 + (A 1 1).re / 2,
    (A 0 1).re, -(A 0 1).im, (A 0 0).re / 2 - (A 1 1).re / 2]
  map_add' := by
    intro A B
    ext i
    fin_cases i <;> simp [Matrix.add_apply] <;> ring
  map_smul' := by
    intro t A
    ext i
    fin_cases i <;> simp [Matrix.smul_apply, smul_eq_mul] <;> ring

theorem pauli_isHermitian (x : V) : (pauli x).IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [pauli, Matrix.conjTranspose_apply]

@[simp]
theorem coordinates_pauli (x : V) : coordinates (pauli x) = x := by
  ext i
  fin_cases i <;> simp [coordinates, pauli] <;> ring

theorem pauli_coordinates {A : Operator} (hA : A.IsHermitian) : pauli (coordinates A) = A := by
  have h00 := congrArg Complex.im (congrFun (congrFun hA.eq 0) 0)
  have h11 := congrArg Complex.im (congrFun (congrFun hA.eq 1) 1)
  have h01r := congrArg Complex.re (congrFun (congrFun hA.eq 0) 1)
  have h01i := congrArg Complex.im (congrFun (congrFun hA.eq 0) 1)
  simp only [Matrix.conjTranspose_apply, Complex.star_def, Complex.conj_im,
    Complex.conj_re] at h00 h11 h01r h01i
  ext i j
  fin_cases i <;> fin_cases j <;> apply Complex.ext <;>
    simp [pauli, coordinates] <;> linarith

/-- The Minkowski quadratic form, in the same Pauli convention as the paper. -/
def lorentzSquare (x : V) : ℝ := x 0 ^ 2 - x 1 ^ 2 - x 2 ^ 2 - x 3 ^ 2

def lorentzPair (x y : V) : ℝ :=
  x 0 * y 0 - x 1 * y 1 - x 2 * y 2 - x 3 * y 3

def minkowski : M := !![1,0,0,0; 0,-1,0,0; 0,0,-1,0; 0,0,0,-1]

def timeUnit : V := ![1,0,0,0]

@[simp]
theorem minkowski_square : minkowski * minkowski = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [minkowski, Matrix.mul_apply, Fin.sum_univ_succ, Matrix.one_apply]

@[simp]
theorem minkowski_transpose : minkowski.transpose = minkowski := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

@[simp]
theorem pauli_timeUnit : pauli timeUnit = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [pauli, timeUnit, Matrix.one_apply]

theorem lorentzPair_eq_matrixPair (x y : V) :
    lorentzPair x y = matrixPair minkowski x y := by
  simp [lorentzPair, matrixPair, minkowski, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]

@[simp]
theorem lorentzPair_self (x : V) : lorentzPair x x = lorentzSquare x := by
  unfold lorentzPair lorentzSquare
  ring

@[simp]
theorem pauli_trace (x : V) : Matrix.trace (pauli x) = (2 * x 0 : ℝ) := by
  simp [Matrix.trace, pauli, Fin.sum_univ_succ]
  ring

@[simp]
theorem pauli_det (x : V) : (pauli x).det = (lorentzSquare x : ℂ) := by
  simp [pauli, lorentzSquare, Matrix.det_fin_two]
  ring_nf
  simp

theorem pauli_trace_product (x y : V) :
    Matrix.trace (pauli x * pauli y) = (2 * dotProduct x y : ℝ) := by
  simp [pauli, Matrix.trace, Matrix.mul_apply, dotProduct, Fin.sum_univ_succ]
  ring_nf
  simp

theorem pauli_injective : Function.Injective pauli := by
  intro x y h
  simpa using congrArg coordinates h

private theorem nonnegative_roots (a b : ℝ) (hs : 0 ≤ a+b) (hp : 0 ≤ a*b) :
    0 ≤ a ∧ 0 ≤ b := by
  constructor
  · by_contra! ha
    have hb : 0 < b := by linarith
    exact (not_lt_of_ge hp) (mul_neg_of_neg_of_pos ha hb)
  · by_contra! hb
    have ha : 0 < a := by linarith
    exact (not_lt_of_ge hp) (mul_neg_of_pos_of_neg ha hb)

/-- A two-dimensional trace/determinant criterion; Hermiticity is explicit. -/
theorem qubit_psd_iff {A : Operator} (hA : A.IsHermitian) :
    A.PosSemidef ↔ 0 ≤ (Matrix.trace A).re ∧ 0 ≤ A.det.re := by
  have ht : Matrix.trace A = (hA.eigenvalues 0 + hA.eigenvalues 1 : ℝ) := by
    rw [hA.spectral_theorem, Matrix.trace_mul_comm, ← Matrix.mul_assoc]
    simp [Fin.sum_univ_succ]
  have hd : A.det = ((hA.eigenvalues 0 * hA.eigenvalues 1 : ℝ) : ℂ) := by
    simpa [Fin.prod_univ_succ] using hA.det_eq_prod_eigenvalues
  constructor
  · intro hp
    refine ⟨positive_trace_nonneg hp, ?_⟩
    rw [hd]
    simpa using mul_nonneg (hp.eigenvalues_nonneg 0) (hp.eigenvalues_nonneg 1)
  · rintro ⟨htr, hdet⟩
    rw [ht] at htr
    rw [hd] at hdet
    simp only [Complex.ofReal_re] at htr hdet
    obtain ⟨h0, h1⟩ := nonnegative_roots _ _ htr hdet
    apply hA.posSemidef_of_eigenvalues_nonneg
    intro i
    fin_cases i
    · exact h0
    · exact h1

def Future (x : V) : Prop := 0 ≤ x 0 ∧ 0 ≤ lorentzSquare x

def FutureNull (x : V) : Prop := 0 < x 0 ∧ lorentzSquare x = 0

def FutureTimelike (x : V) : Prop := 0 < x 0 ∧ 0 < lorentzSquare x

theorem pauli_posSemidef_iff (x : V) : (pauli x).PosSemidef ↔ Future x := by
  rw [qubit_psd_iff (pauli_isHermitian x)]
  simp only [pauli_trace, pauli_det, Complex.ofReal_re, Future]
  constructor
  · rintro ⟨ht, hd⟩
    exact ⟨by linarith, hd⟩
  · rintro ⟨ht, hd⟩
    exact ⟨by linarith, hd⟩

theorem FutureNull.posSemidef {x : V} (hx : FutureNull x) : (pauli x).PosSemidef :=
  (pauli_posSemidef_iff x).mpr ⟨hx.1.le, hx.2.ge⟩

theorem FutureNull.nonzero {x : V} (hx : FutureNull x) : x ≠ 0 := by
  intro h
  simpa [h] using hx.1

theorem future_time_zero {x : V} (hx : Future x) (ht : x 0 = 0) : x = 0 := by
  have hq := hx.2
  simp only [lorentzSquare, ht, sq] at hq
  have h1 : x 1 = 0 := by nlinarith [sq_nonneg (x 2), sq_nonneg (x 3)]
  have h2 : x 2 = 0 := by nlinarith [sq_nonneg (x 1), sq_nonneg (x 3)]
  have h3 : x 3 = 0 := by nlinarith [sq_nonneg (x 1), sq_nonneg (x 2)]
  ext i
  fin_cases i <;> simp [ht, h1, h2, h3]

theorem future_nonzero_time {x : V} (hx : Future x) (hne : x ≠ 0) : 0 < x 0 := by
  by_contra! h
  exact hne (future_time_zero hx (le_antisymm h hx.1))

/-- Positive definiteness follows from PSD and invertibility, without a choice
of eigenbasis in the resulting theorem. -/
theorem posDef_of_posSemidef_det_ne_zero {A : Operator}
    (hA : A.PosSemidef) (hdet : A.det ≠ 0) : A.PosDef := by
  refine ⟨hA.isHermitian, fun x hx => ?_⟩
  have hq := hA.2 x
  have hn : dotProduct (star x) (A *ᵥ x) ≠ 0 := by
    intro hz
    have hAx := (hA.dotProduct_mulVec_zero_iff x).mp hz
    have hi := congrArg (fun y => A⁻¹ *ᵥ y) hAx
    rw [Matrix.mulVec_mulVec,
      Matrix.nonsing_inv_mul A (isUnit_iff_ne_zero.mpr hdet), Matrix.one_mulVec,
      Matrix.mulVec_zero] at hi
    exact hx hi
  exact lt_iff_le_and_ne.mpr ⟨hq, Ne.symm hn⟩

theorem FutureTimelike.posDef {x : V} (hx : FutureTimelike x) : (pauli x).PosDef := by
  apply posDef_of_posSemidef_det_ne_zero
  · exact (pauli_posSemidef_iff x).mpr ⟨hx.1.le, hx.2.le⟩
  · rw [pauli_det]
    exact_mod_cast hx.2.ne'

/-- The sum-of-squares identity behind Lorentz-cone strict convexity. -/
theorem lorentz_pair_squares (x y : V) :
    2*x 0*y 0*lorentzPair x y =
      (y 0*x 1-x 0*y 1)^2 + (y 0*x 2-x 0*y 2)^2 + (y 0*x 3-x 0*y 3)^2 +
      y 0^2*lorentzSquare x + x 0^2*lorentzSquare y := by
  unfold lorentzPair lorentzSquare
  ring

theorem future_pair_nonnegative {x y : V} (hx : Future x) (hy : Future y) :
    0 ≤ lorentzPair x y := by
  by_cases hx0 : x = 0
  · simp [hx0, lorentzPair]
  by_cases hy0 : y = 0
  · simp [hy0, lorentzPair]
  have hxt := future_nonzero_time hx hx0
  have hyt := future_nonzero_time hy hy0
  have hprod : 0 < 2*x 0*y 0 := by positivity
  have heq := lorentz_pair_squares x y
  have hn : 0 ≤ 2*x 0*y 0*lorentzPair x y := by
    rw [heq]
    positivity
  exact (nonneg_of_mul_nonneg_left hn hprod)

theorem null_pair_zero_sameRay {x y : V} (hx : FutureNull x) (hy : FutureNull y)
    (hpair : lorentzPair x y = 0) : SameRay x y := by
  have heq := lorentz_pair_squares x y
  rw [hx.2, hy.2, hpair] at heq
  have h1 : y 0*x 1-x 0*y 1 = 0 := by nlinarith [sq_nonneg (y 0*x 2-x 0*y 2), sq_nonneg (y 0*x 3-x 0*y 3)]
  have h2 : y 0*x 2-x 0*y 2 = 0 := by nlinarith [sq_nonneg (y 0*x 1-x 0*y 1), sq_nonneg (y 0*x 3-x 0*y 3)]
  have h3 : y 0*x 3-x 0*y 3 = 0 := by nlinarith [sq_nonneg (y 0*x 1-x 0*y 1), sq_nonneg (y 0*x 2-x 0*y 2)]
  refine ⟨x 0 / y 0, div_ne_zero hx.1.ne' hy.1.ne', ?_⟩
  ext i
  fin_cases i <;> simp only [Pi.smul_apply, smul_eq_mul] <;>
    field_simp [hy.1.ne'] <;> nlinarith

theorem null_pair_positive_of_distinct {x y : V} (hx : FutureNull x) (hy : FutureNull y)
    (hne : ¬ SameRay x y) : 0 < lorentzPair x y := by
  have hn := future_pair_nonnegative (show Future x from ⟨hx.1.le, hx.2.ge⟩)
    (show Future y from ⟨hy.1.le, hy.2.ge⟩)
  have hneq : lorentzPair x y ≠ 0 := fun hz => hne (null_pair_zero_sameRay hx hy hz)
  exact lt_of_le_of_ne hn (Ne.symm hneq)

theorem timelike_pair_positive {x y : V} (hx : FutureNull x) (hy : FutureTimelike y) :
    0 < lorentzPair x y := by
  have heq := lorentz_pair_squares x y
  have hp : 0 < x 0^2 * lorentzSquare y := mul_pos (sq_pos_of_ne_zero hx.1.ne') hy.2
  have hscale : 0 < 2*x 0*y 0 := by positivity
  have htotal : 0 < 2*x 0*y 0*lorentzPair x y := by
    rw [heq, hx.2]
    nlinarith [sq_nonneg (y 0*x 1-x 0*y 1), sq_nonneg (y 0*x 2-x 0*y 2),
      sq_nonneg (y 0*x 3-x 0*y 3)]
  exact (mul_pos_iff_of_pos_left hscale).mp htotal

end Bell.QubitGeometry
