import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Data.Finset.Max
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-!
# Finite phase-operator infrastructure

These statements concern explicitly supplied finite matrices.  They do not assert
that any manuscript matrix satisfies their assumptions: those entrywise checks
belong to the concrete sector formalization.
-/

namespace SymmetricSector.Phase

set_option linter.unusedSectionVars false

open Matrix
open scoped BigOperators

variable {ι : Type*} [Fintype ι] [DecidableEq ι]
variable {𝕜 : Type*} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜]

/-- A strict absolute row contraction has no nonzero fixed vector. -/
theorem fixed_eq_zero_of_abs_row_sum_lt_one
    (A : Matrix ι ι 𝕜) (hA : ∀ i, ∑ j, |A i j| < 1)
    (x : ι → 𝕜) (hx : A *ᵥ x = x) : x = 0 := by
  classical
  by_cases hn : Nonempty ι
  · letI := hn
    obtain ⟨i, -, hi⟩ := Finset.exists_max_image Finset.univ (fun j => |x j|)
      Finset.univ_nonempty
    have hb : ∀ j, |x j| ≤ |x i| := fun j => hi j (Finset.mem_univ j)
    have he : |x i| ≤ (∑ j, |A i j|) * |x i| := by
      calc
        |x i| = |∑ j, A i j * x j| := by
          change |x i| = |(A *ᵥ x) i|
          rw [hx]
        _ ≤ ∑ j, |A i j * x j| := Finset.abs_sum_le_sum_abs _ _
        _ = ∑ j, |A i j| * |x j| := by simp only [abs_mul]
        _ ≤ ∑ j, |A i j| * |x i| := Finset.sum_le_sum fun j _ =>
          mul_le_mul_of_nonneg_left (hb j) (abs_nonneg _)
        _ = (∑ j, |A i j|) * |x i| := by rw [Finset.sum_mul]
    have hzero : |x i| = 0 := by
      by_contra h
      have hp : 0 < |x i| := lt_of_le_of_ne (abs_nonneg _) (Ne.symm h)
      have hc := mul_lt_mul_of_pos_right (hA i) hp
      nlinarith
    ext j
    exact abs_eq_zero.mp (le_antisymm (by simpa [hzero] using hb j) (abs_nonneg _))
  · haveI : IsEmpty ι := not_nonempty_iff.mp hn
    exact Subsingleton.elim _ _

/-- Invertibility follows from strict absolute row sums; no computed determinant
or externally asserted solver result is used. -/
theorem isUnit_one_sub_of_abs_row_sum_lt_one
    (A : Matrix ι ι 𝕜) (hA : ∀ i, ∑ j, |A i j| < 1) : IsUnit (1 - A) := by
  apply Matrix.mulVec_injective_iff_isUnit.mp
  intro x y hxy
  have hz : (1 - A) *ᵥ (x - y) = 0 := by
    rw [Matrix.mulVec_sub, hxy, sub_self]
  have hfix : A *ᵥ (x - y) = x - y := by
    have h : (x - y) - A *ᵥ (x - y) = 0 := by
      simpa only [Matrix.sub_mulVec, Matrix.one_mulVec] using hz
    exact (sub_eq_zero.mp h).symm
  have := fixed_eq_zero_of_abs_row_sum_lt_one A hA (x - y) hfix
  exact sub_eq_zero.mp this

/-- A checked solution witness identifies the mathematical inverse solution. -/
theorem witness_eq_inverse_mulVec
    (M : Matrix ι ι 𝕜) (hM : IsUnit M) (b x : ι → 𝕜)
    (hx : M *ᵥ x = b) : x = M⁻¹ *ᵥ b := by
  rw [← hx, Matrix.mulVec_mulVec,
    Matrix.nonsing_inv_mul M (M.isUnit_iff_isUnit_det.mp hM), Matrix.one_mulVec]


/-- Finite maximum principle for a nonnegative strict row contraction. -/
theorem nonpos_of_le_mulVec
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (hrow : ∀ i, ∑ j, A i j < 1) (x : ι → 𝕜)
    (hx : x ≤ A *ᵥ x) : x ≤ 0 := by
  classical
  intro j
  by_contra hj
  have hj' : 0 < x j := lt_of_not_ge hj
  obtain ⟨i, -, hi⟩ := Finset.exists_max_image Finset.univ x
    ⟨j, Finset.mem_univ j⟩
  have hb : ∀ k, x k ≤ x i := fun k => hi k (Finset.mem_univ k)
  have hp : 0 < x i := lt_of_lt_of_le hj' (hb j)
  have he : x i ≤ (∑ k, A i k) * x i := by
    calc
      x i ≤ (A *ᵥ x) i := hx i
      _ = ∑ k, A i k * x k := rfl
      _ ≤ ∑ k, A i k * x i := Finset.sum_le_sum fun k _ =>
        mul_le_mul_of_nonneg_left (hb k) (hA i k)
      _ = (∑ k, A i k) * x i := by rw [Finset.sum_mul]
  have hc := mul_lt_mul_of_pos_right (hrow i) hp
  nlinarith

/-- The finite maximum principle identifies nonnegative solutions. -/
theorem solution_nonneg
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (hrow : ∀ i, ∑ j, A i j < 1) (x : ι → 𝕜)
    (hx : 0 ≤ (1 - A) *ᵥ x) : 0 ≤ x := by
  have hneg : -x ≤ A *ᵥ (-x) := by
    intro i
    have h := hx i
    simp only [Matrix.sub_mulVec, Matrix.one_mulVec, Pi.sub_apply,
      Pi.zero_apply] at h
    simp only [Pi.neg_apply, Matrix.mulVec_neg]
    linarith
  have h := nonpos_of_le_mulVec A hA hrow (-x) hneg
  intro i
  have hi := h i
  simpa only [Pi.neg_apply, Pi.zero_apply, neg_nonpos] using hi

/-- Nonnegative inverse action, proved using a finite maximum principle. -/
theorem inverse_mulVec_nonneg
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (hrow : ∀ i, ∑ j, A i j < 1) (b : ι → 𝕜) (hb : 0 ≤ b) :
    0 ≤ (1 - A)⁻¹ *ᵥ b := by
  have hu : IsUnit (1 - A) := isUnit_one_sub_of_abs_row_sum_lt_one A (by
    intro i
    simpa only [abs_of_nonneg (hA i _)] using hrow i)
  apply solution_nonneg A hA hrow
  rw [Matrix.mulVec_mulVec, Matrix.mul_nonsing_inv _
    ((1 - A).isUnit_iff_isUnit_det.mp hu), Matrix.one_mulVec]
  exact hb

/-- Entrywise nonnegativity of the nonsingular inverse is a theorem. -/
theorem inverse_entrywise_nonneg
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (hrow : ∀ i, ∑ j, A i j < 1) : ∀ i j, 0 ≤ (1 - A)⁻¹ i j := by
  intro i j
  have h := inverse_mulVec_nonneg A hA hrow (Pi.single j 1) (by
    intro k
    simp only [Pi.single_apply, Pi.zero_apply]
    split <;> simp_all)
  simpa only [Matrix.mulVec_single_one] using h i

/-- Checked residual inequalities transfer to true inverse solutions. -/
theorem inverse_mulVec_le_supersolution
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (hrow : ∀ i, ∑ j, A i j < 1) (b w : ι → 𝕜)
    (hw : b ≤ (1 - A) *ᵥ w) : (1 - A)⁻¹ *ᵥ b ≤ w := by
  have hu : IsUnit (1 - A) := isUnit_one_sub_of_abs_row_sum_lt_one A (by
    intro i
    simpa only [abs_of_nonneg (hA i _)] using hrow i)
  have h := inverse_mulVec_nonneg A hA hrow ((1 - A) *ᵥ w - b)
    (sub_nonneg.mpr hw)
  rw [Matrix.mulVec_sub, Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _
    ((1 - A).isUnit_iff_isUnit_det.mp hu), Matrix.one_mulVec] at h
  exact sub_nonneg.mp h


/-- A positive weight with strict contraction gives a finite maximum principle,
without any convergence assumption or invocation of a Neumann series. -/
theorem weighted_nonpos_of_le_mulVec
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (v : ι → 𝕜) (hv : ∀ i, 0 < v i) (c : 𝕜) (hc : c < 1)
    (hAv : A *ᵥ v ≤ c • v) (x : ι → 𝕜) (hx : x ≤ A *ᵥ x) : x ≤ 0 := by
  classical
  intro j
  by_contra hj
  have hj' : 0 < x j := lt_of_not_ge hj
  obtain ⟨i, -, hi⟩ := Finset.exists_max_image Finset.univ (fun k => x k / v k)
    ⟨j, Finset.mem_univ j⟩
  have hb : ∀ k, x k ≤ (x i / v i) * v k := fun k =>
    (div_le_iff₀ (hv k)).mp (hi k (Finset.mem_univ k))
  have hp : 0 < x i / v i := lt_of_lt_of_le (div_pos hj' (hv j))
    (hi j (Finset.mem_univ j))
  have hxi : 0 < x i := by
    have hh := mul_pos hp (hv i)
    simpa only [div_mul_cancel₀ _ (ne_of_gt (hv i))] using hh
  have he : x i ≤ c * x i := by
    calc
      x i ≤ (A *ᵥ x) i := hx i
      _ = ∑ k, A i k * x k := rfl
      _ ≤ ∑ k, A i k * ((x i / v i) * v k) := Finset.sum_le_sum fun k _ =>
        mul_le_mul_of_nonneg_left (hb k) (hA i k)
      _ = (x i / v i) * (A *ᵥ v) i := by
        simp only [Matrix.mulVec, dotProduct, Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro k _
        ring
      _ ≤ (x i / v i) * (c * v i) :=
        mul_le_mul_of_nonneg_left (hAv i) hp.le
      _ = c * x i := by field_simp [ne_of_gt (hv i)]; ring
  have := mul_lt_mul_of_pos_right hc hxi
  nlinarith

/-- Pointwise absolute values respect any entrywise nonnegative finite matrix. -/
theorem abs_mulVec_le (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (x : ι → 𝕜) : (fun i => |(A *ᵥ x) i|) ≤ A *ᵥ (fun i => |x i|) := by
  intro i
  change |∑ j, A i j * x j| ≤ ∑ j, A i j * |x j|
  calc
    _ ≤ ∑ j, |A i j * x j| := Finset.abs_sum_le_sum_abs _ _
    _ = _ := by simp only [abs_mul, abs_of_nonneg (hA i _)]

/-- A checked weighted phase contraction proves invertibility of I+A. -/
theorem isUnit_one_add_of_weighted_contraction
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (v : ι → 𝕜) (hv : ∀ i, 0 < v i) (c : 𝕜) (hc : c < 1)
    (hAv : A *ᵥ v ≤ c • v) : IsUnit (1 + A) := by
  apply Matrix.mulVec_injective_iff_isUnit.mp
  intro x y hxy
  have hz : (1 + A) *ᵥ (x - y) = 0 := by
    rw [Matrix.mulVec_sub, hxy, sub_self]
  have hfix : A *ᵥ (x - y) = -(x - y) := by
    simpa only [Matrix.add_mulVec, Matrix.one_mulVec, add_eq_zero_iff_eq_neg'] using hz
  have hb := abs_mulVec_le A hA (x - y)
  rw [hfix] at hb
  simp only [Pi.neg_apply, abs_neg] at hb
  have hzero := weighted_nonpos_of_le_mulVec A hA v hv c hc hAv
    (fun i => |(x - y) i|) hb
  apply sub_eq_zero.mp
  ext i
  exact abs_eq_zero.mp (le_antisymm (hzero i) (abs_nonneg _))

/-- Weighted finite comparison bound used to control the complete alternating
resolvent, rather than only its first excursion. -/
theorem le_weight_of_le_add_mulVec
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (v : ι → 𝕜) (hv : ∀ i, 0 < v i) (c : 𝕜) (hc : c < 1)
    (hAv : A *ᵥ v ≤ c • v) (b : 𝕜) (hb : 0 ≤ b)
    (x : ι → 𝕜) (hx : x ≤ b • v + A *ᵥ x) :
    x ≤ (b / (1 - c)) • v := by
  have hden : 0 < 1 - c := sub_pos.mpr hc
  have ht : 0 ≤ b / (1 - c) := div_nonneg hb hden.le
  have he : b / (1 - c) * (1 - c) = b := div_mul_cancel₀ b (ne_of_gt hden)
  have hsub : x - (b / (1 - c)) • v ≤ A *ᵥ (x - (b / (1 - c)) • v) := by
    intro i
    have hi := hx i
    have ha := mul_le_mul_of_nonneg_left (hAv i) ht
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul] at hi ha
    simp only [Matrix.mulVec_sub, Matrix.mulVec_smul, Pi.sub_apply,
      Pi.smul_apply, smul_eq_mul]
    have hei : b / (1 - c) * v i - b / (1 - c) * (c * v i) = b * v i := by
      calc
        _ = (b / (1 - c) * (1 - c)) * v i := by ring
        _ = _ := by rw [he]
    linarith
  exact sub_nonpos.mp (weighted_nonpos_of_le_mulVec A hA v hv c hc hAv
    (x - (b / (1 - c)) • v) hsub)

/-- Complete resolvent bound, from its defining equation and a positive weight. -/
theorem alternating_solution_bound
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (v : ι → 𝕜) (hv : ∀ i, 0 < v i) (c : 𝕜) (hc : c < 1)
    (hAv : A *ᵥ v ≤ c • v) (f x : ι → 𝕜)
    (hf : ∀ i, |f i| ≤ v i) (hx : (1 + A) *ᵥ x = f) :
    (fun i => |x i|) ≤ (1 / (1 - c)) • v := by
  apply le_weight_of_le_add_mulVec A hA v hv c hc hAv 1 zero_le_one
  intro i
  have he := congrFun hx i
  simp only [Matrix.add_mulVec, Matrix.one_mulVec, Pi.add_apply] at he
  have hax := abs_mulVec_le A hA x i
  have habs : |x i| ≤ |f i| + |(A *ᵥ x) i| := by
    calc
      |x i| = |f i - (A *ᵥ x) i| := by rw [← he]; congr 1; ring
      _ ≤ _ := abs_sub _ _
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, one_mul]
  linarith [hf i]


/-- Monotonicity is checked directly for every finite nonnegative matrix. -/
theorem mulVec_mono (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    {x y : ι → 𝕜} (hxy : x ≤ y) : A *ᵥ x ≤ A *ᵥ y := by
  intro i
  exact Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left (hxy j) (hA i j)

/-- Error of the full alternating inverse relative to the first phase. -/
theorem alternating_error_bound
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (v : ι → 𝕜) (hv : ∀ i, 0 < v i) (c : 𝕜) (hc : c < 1)
    (hAv : A *ᵥ v ≤ c • v) (f x : ι → 𝕜)
    (hf : ∀ i, |f i| ≤ v i) (hx : (1 + A) *ᵥ x = f) :
    (fun i => |x i - f i|) ≤ (c / (1 - c)) • v := by
  have hb := alternating_solution_bound A hA v hv c hc hAv f x hf hx
  have hmul := mulVec_mono A hA hb
  have ht : 0 ≤ 1 / (1 - c) := div_nonneg zero_le_one (sub_nonneg.mpr hc.le)
  intro i
  have he := congrFun hx i
  simp only [Matrix.add_mulVec, Matrix.one_mulVec, Pi.add_apply] at he
  calc
    |x i - f i| = |(A *ᵥ x) i| := by rw [← he]; simp
    _ ≤ (A *ᵥ (fun j => |x j|)) i := abs_mulVec_le A hA x i
    _ ≤ (A *ᵥ ((1 / (1 - c)) • v)) i := hmul i
    _ = 1 / (1 - c) * (A *ᵥ v) i := by rw [Matrix.mulVec_smul]; rfl
    _ ≤ 1 / (1 - c) * (c * v i) := mul_le_mul_of_nonneg_left (hAv i) ht
    _ = ((c / (1 - c)) • v) i := by simp only [Pi.smul_apply, smul_eq_mul]; ring

/-- A nonnegative row transfers coordinate bounds to its scalar pairing. -/
theorem dotProduct_mono (ell : ι → 𝕜) (hell : 0 ≤ ell)
    {x y : ι → 𝕜} (hxy : x ≤ y) : dotProduct ell x ≤ dotProduct ell y :=
  Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (hxy i) (hell i)

/-- Absolute scalar error is bounded by the pairing of coordinate errors. -/
theorem abs_dotProduct_le (ell : ι → 𝕜) (hell : 0 ≤ ell) (x : ι → 𝕜) :
    |dotProduct ell x| ≤ dotProduct ell (fun i => |x i|) := by
  calc
    _ ≤ ∑ i, |ell i * x i| := Finset.abs_sum_le_sum_abs _ _
    _ = _ := by simp only [dotProduct, abs_mul, abs_of_nonneg (hell _)]

/-- Abstract form of A.36. Every matrix, source, and debt hypothesis is explicit;
this theorem supplies the universal implication from the phase estimates. -/
theorem phase_scalar_lower_bound
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (v : ι → 𝕜) (hv : ∀ i, 0 < v i) (c : 𝕜) (hc0 : 0 ≤ c) (hc : c < 1)
    (hAv : A *ᵥ v ≤ c • v) (a : 𝕜) (ha : 0 < a)
    (f x ell : ι → 𝕜) (hell : 0 ≤ ell) (hflo : a • v ≤ f) (hfhi : f ≤ v)
    (hx : (1 + A) *ᵥ x = f) (debt beta : 𝕜)
    (hdebt : debt ≤ beta * dotProduct ell f) :
    (1 - beta - (1 / a) * (c / (1 - c))) * dotProduct ell f ≤
      dotProduct ell x - debt := by
  have hf0 : 0 ≤ f := by
    intro i
    have h := hflo i
    have hh : 0 ≤ a * v i := mul_nonneg ha.le (hv i).le
    exact le_trans hh h
  have hfabs : ∀ i, |f i| ≤ v i := fun i => by
    simpa only [abs_of_nonneg (hf0 i)] using hfhi i
  have herr := alternating_error_bound A hA v hv c hc hAv f x hfabs hx
  have hscalar : |dotProduct ell x - dotProduct ell f| ≤
      (c / (1 - c)) * dotProduct ell v := by
    calc
      _ = |dotProduct ell (x - f)| := by rw [dotProduct_sub]
      _ ≤ dotProduct ell (fun i => |(x - f) i|) := abs_dotProduct_le ell hell _
      _ ≤ dotProduct ell ((c / (1 - c)) • v) := dotProduct_mono ell hell herr
      _ = _ := by simp [dotProduct, Finset.mul_sum]; apply Finset.sum_congr rfl; intro i _; ring
  have hlo : a * dotProduct ell v ≤ dotProduct ell f := by
    calc
      _ = dotProduct ell (a • v) := by
        simp [dotProduct, Finset.mul_sum]; apply Finset.sum_congr rfl; intro i _; ring
      _ ≤ _ := dotProduct_mono ell hell hflo
  have he0 : 0 ≤ c / (1 - c) := div_nonneg hc0 (sub_nonneg.mpr hc.le)
  have hvbound : dotProduct ell v ≤ (1 / a) * dotProduct ell f := by
    rw [one_div, ← div_eq_inv_mul]
    exact (le_div_iff₀ ha).mpr (by simpa only [mul_comm] using hlo)
  have he := mul_le_mul_of_nonneg_left hvbound he0
  have herrLower := (abs_le.mp hscalar).1
  nlinarith

/-- Strict positivity follows from the complete phase loss budget. -/
theorem phase_scalar_pos
    (A : Matrix ι ι 𝕜) (hA : ∀ i j, 0 ≤ A i j)
    (v : ι → 𝕜) (hv : ∀ i, 0 < v i) (c : 𝕜) (hc0 : 0 ≤ c) (hc : c < 1)
    (hAv : A *ᵥ v ≤ c • v) (a : 𝕜) (ha : 0 < a)
    (f x ell : ι → 𝕜) (hell : 0 ≤ ell) (hflo : a • v ≤ f) (hfhi : f ≤ v)
    (hx : (1 + A) *ᵥ x = f) (debt beta : 𝕜)
    (hdebt : debt ≤ beta * dotProduct ell f)
    (hfirst : 0 < dotProduct ell f)
    (hloss : beta + (1 / a) * (c / (1 - c)) < 1) :
    0 < dotProduct ell x - debt := by
  have h := phase_scalar_lower_bound A hA v hv c hc0 hc hAv a ha f x ell hell
    hflo hfhi hx debt beta hdebt
  exact lt_of_lt_of_le (mul_pos (by linarith) hfirst) h


section Schur

variable {κ : Type*} [Fintype κ] [DecidableEq κ]

/-- Exact elimination of the bad coordinate from its specified linear equation. -/
theorem schur_bad_equation
    (Q : Matrix κ κ 𝕜) (hQ : IsUnit (1 - Q))
    (D : Matrix κ ι 𝕜) (x : ι → 𝕜) (y gb : κ → 𝕜)
    (hy : D *ᵥ x + (1 - Q) *ᵥ y = gb) :
    y = (1 - Q)⁻¹ *ᵥ gb - (1 - Q)⁻¹ *ᵥ (D *ᵥ x) := by
  have he : (1 - Q) *ᵥ y = gb - D *ᵥ x := eq_sub_of_add_eq' hy
  have h := witness_eq_inverse_mulVec (1 - Q) hQ _ y he
  simpa only [Matrix.mulVec_sub] using h

/-- Exact Schur-complement identity for the signed block operator
`H = [[S,C],[-D,Q]]`, with no positivity hypothesis required. -/
theorem schur_good_equation
    (S : Matrix ι ι 𝕜) (hS : IsUnit (1 - S))
    (Q : Matrix κ κ 𝕜) (hQ : IsUnit (1 - Q))
    (C : Matrix ι κ 𝕜) (D : Matrix κ ι 𝕜)
    (x ga : ι → 𝕜) (y gb : κ → 𝕜)
    (hx : (1 - S) *ᵥ x - C *ᵥ y = ga)
    (hy : D *ᵥ x + (1 - Q) *ᵥ y = gb) :
    (1 + (1 - S)⁻¹ * C * (1 - Q)⁻¹ * D) *ᵥ x =
      (1 - S)⁻¹ *ᵥ (ga + C *ᵥ ((1 - Q)⁻¹ *ᵥ gb)) := by
  have hye := schur_bad_equation Q hQ D x y gb hy
  have hxe := congrArg (fun z => (1 - S)⁻¹ *ᵥ z) hx
  dsimp only at hxe
  rw [Matrix.mulVec_sub, Matrix.mulVec_mulVec,
    Matrix.nonsing_inv_mul _ ((1 - S).isUnit_iff_isUnit_det.mp hS),
    Matrix.one_mulVec, hye, Matrix.mulVec_sub, Matrix.mulVec_sub] at hxe
  ext i
  have hi := congrFun hxe i
  simp only [Pi.sub_apply] at hi
  simp only [Matrix.add_mulVec, Matrix.one_mulVec, Matrix.mulVec_add,
    ← Matrix.mulVec_mulVec, Pi.add_apply]
  linarith

/-- Exact scalar part of Schur elimination, retaining the occupation debt. -/
theorem schur_scalar_identity
    (Q : Matrix κ κ 𝕜) (hQ : IsUnit (1 - Q)) (D : Matrix κ ι 𝕜)
    (x sa : ι → 𝕜) (y gb sb : κ → 𝕜)
    (hy : D *ᵥ x + (1 - Q) *ᵥ y = gb) :
    dotProduct sa x + dotProduct sb y =
      dotProduct (sa - sb ᵥ* ((1 - Q)⁻¹ * D)) x -
        dotProduct sb ((1 - Q)⁻¹ *ᵥ (-gb)) := by
  rw [schur_bad_equation Q hQ D x y gb hy]
  simp only [dotProduct_sub, sub_dotProduct, Matrix.mulVec_neg, dotProduct_neg,
    ← Matrix.mulVec_mulVec, ← Matrix.dotProduct_mulVec]
  ring

end Schur

#print axioms isUnit_one_sub_of_abs_row_sum_lt_one
#print axioms witness_eq_inverse_mulVec
#print axioms inverse_entrywise_nonneg
#print axioms inverse_mulVec_le_supersolution
#print axioms isUnit_one_add_of_weighted_contraction
#print axioms alternating_error_bound
#print axioms phase_scalar_lower_bound
#print axioms phase_scalar_pos
#print axioms schur_good_equation
#print axioms schur_scalar_identity

end SymmetricSector.Phase
