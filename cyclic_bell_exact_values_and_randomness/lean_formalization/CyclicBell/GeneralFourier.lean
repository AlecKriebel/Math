import Mathlib.Analysis.Fourier.ZMod
import CyclicBell.Model

/-!
All-dimensional Fourier/autocorrelation algebra, with the manuscript's PLUS
Fourier sign. The character is the actual standard complex additive character,
not an uninterpreted root or a hypothesis asserting orthogonality.
SOURCE CANDIDATE. No Lean invocation has been performed on this file.
-/
noncomputable section
open scoped BigOperators ComplexConjugate
open Finset
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

abbrev Ix (d : ℕ) := ZMod d

/-- Basic positivity belongs before both scalar bounds and witness construction. -/
theorem dimension_pos : 0 < (d : ℝ) := by
  exact_mod_cast Nat.pos_of_ne_zero (NeZero.ne d)

def chi (j : Ix d) : ℂ := ZMod.stdAddChar j

@[simp] theorem chi_zero : chi (0 : Ix d) = 1 := by
  exact (ZMod.stdAddChar (N := d)).map_zero_eq_one

@[simp] theorem chi_add (j k : Ix d) : chi (j + k) = chi j * chi k := by
  exact (ZMod.stdAddChar (N := d)).map_add_eq_mul j k

@[simp] theorem chi_norm (j : Ix d) : ‖chi j‖ = 1 := by
  exact (ZMod.toCircle j).norm_coe

@[simp] theorem chi_ne_zero (j : Ix d) : chi j ≠ 0 := by
  intro h
  have := chi_norm j
  rw [h, norm_zero] at this
  exact zero_ne_one this

@[simp] theorem chi_normSq (j : Ix d) : Complex.normSq (chi j) = 1 := by
  rw [Complex.normSq_eq_norm_sq, chi_norm]
  norm_num

@[simp] theorem chi_star_mul (j : Ix d) : star (chi j) * chi j = 1 := by
  change (starRingEnd ℂ) (chi j) * chi j = 1
  rw [← Complex.normSq_eq_conj_mul_self, chi_normSq]
  norm_num

@[simp] theorem chi_star (j : Ix d) : star (chi j) = chi (-j) := by
  apply mul_right_cancel₀ (chi_ne_zero j)
  rw [chi_star_mul, ← chi_add, neg_add_cancel, chi_zero]

@[simp] theorem chi_sub (j k : Ix d) : chi (j - k) = chi j * star (chi k) := by
  rw [sub_eq_add_neg, chi_add, chi_star]

@[simp] theorem chi_pow (j : Ix d) (n : ℕ) : chi j^n=chi ((n : Ix d)*j) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ,ih,← chi_add]
    congr 1
    push_cast
    ring

theorem chi_injective : Function.Injective (chi : Ix d → ℂ) :=
  ZMod.injective_stdAddChar

@[simp] theorem chi_eq_one_iff (j : Ix d) : chi j = 1 ↔ j = 0 := by
  rw [← chi_zero (d := d), chi_injective.eq_iff]

/-- Literal complex-exponential bridge, including non-prime d. -/
theorem chi_intCast (j : ℤ) :
    chi (j : Ix d) = Complex.exp (2 * Real.pi * Complex.I * j / d) :=
  ZMod.stdAddChar_coe j

theorem chi_natCast (j : ℕ) :
    chi (j : Ix d) = Complex.exp (2 * Real.pi * Complex.I * j / d) := by
  simpa using chi_intCast (d := d) (j : ℤ)

theorem chi_val (j : Ix d) :
    chi j = Complex.exp (2 * Real.pi * Complex.I * j.val / d) := by
  simpa only [ZMod.natCast_zmod_val] using chi_natCast (d := d) j.val

/-- No field structure is used on the index ring. -/
theorem character_sum (t : Ix d) :
    (∑ j : Ix d, chi (t * j)) = if t = 0 then (d : ℂ) else 0 := by
  classical
  by_cases h : t = 0
  · simp [h, ZMod.card]
  · simp only [if_neg h]
    exact AddChar.sum_eq_zero_of_ne_one (ZMod.isPrimitive_stdAddChar d h)

theorem sum_translate {E : Type*} [AddCommMonoid E] (f : Ix d → E) (t : Ix d) :
    (∑ j, f (j + t)) = ∑ j, f j := by
  exact Fintype.sum_equiv (Equiv.addRight t) _ _ (fun _ => rfl)

theorem sum_negate {E : Type*} [AddCommMonoid E] (f : Ix d → E) :
    (∑ j, f (-j)) = ∑ j, f j := by
  exact Fintype.sum_equiv (Equiv.neg _) _ _ (fun _ => rfl)

/-- Manuscript forward transform: PLUS sign and no normalization. -/
def fourier (q : Ix d → ℂ) (m : Ix d) : ℂ := ∑ j, chi (m * j) * q j

def autocorrelation (q : Ix d → ℂ) (t : Ix d) : ℂ :=
  ∑ j, q (j + t) * star (q j)

def powerSpectrum (q : Ix d → ℂ) (m : Ix d) : ℝ := Complex.normSq (fourier q m)

def UnitPhases (q : Ix d → ℂ) : Prop := ∀ j, star (q j) * q j = 1

def FourierFlat (q : Ix d → ℂ) : Prop := ∀ m, powerSpectrum q m = d

/-- Fix the sign mismatch with Mathlib rather than silently changing a+b. -/
theorem fourier_eq_dft_neg (q : Ix d → ℂ) (m : Ix d) :
    fourier q m = ZMod.dft q (-m) := by
  simp [fourier, ZMod.dft_apply, chi, smul_eq_mul, mul_comm]

theorem fourier_inversion (q : Ix d → ℂ) (j : Ix d) :
    q j = (d : ℂ)⁻¹ * ∑ m, chi (-(m * j)) * fourier q m := by
  have h := congrFun (ZMod.dft.symm_apply_apply q) j
  rw [ZMod.invDFT_apply] at h
  change (d : ℂ)⁻¹ * (∑ m, chi (m * j) * ZMod.dft q m) = q j at h
  symm
  refine Eq.trans ?_ h
  congr 1
  symm
  calc
    (∑ m, chi (m * j) * ZMod.dft q m) =
        ∑ m, chi ((-m) * j) * ZMod.dft q (-m) :=
      (sum_negate (fun m => chi (m * j) * ZMod.dft q m)).symm
    _ = _ := by simp only [neg_mul, fourier_eq_dft_neg]

@[simp] theorem fourier_zero (q : Ix d → ℂ) : fourier q 0 = ∑ j, q j := by
  simp [fourier]

/-- The inner pair of indices is transported by an actual translation. -/
theorem fourier_autocorrelation (q : Ix d → ℂ) (m : Ix d) :
    fourier (autocorrelation q) m = (powerSpectrum q m : ℂ) := by
  unfold powerSpectrum
  rw [Complex.normSq_eq_conj_mul_self]
  change fourier (autocorrelation q) m = star (fourier q m) * fourier q m
  unfold fourier autocorrelation
  simp only [star_sum, star_mul, chi_star, Finset.mul_sum, Finset.sum_mul,
    mul_assoc]
  rw [Finset.sum_comm]
  conv_rhs => rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  calc
    (∑ t, chi (m * t) * (q (j + t) * star (q j))) =
        ∑ t, chi (m * (t - j)) * (q t * star (q j)) := by
      have h := sum_translate (fun t => chi (m * (t - j)) * (q t * star (q j))) j
      simpa only [add_sub_cancel_right, add_comm, add_sub_cancel_left] using h
    _ = ∑ t, (chi (-(m * j)) * star (q j)) * (chi (m * t) * q t) := by
      apply Finset.sum_congr rfl
      intro t _
      rw [mul_sub, sub_eq_add_neg, chi_add]
      ring
    _ = _ := by
      apply Finset.sum_congr rfl
      intro t _
      ring

/-- Wiener--Khinchin with the precise normalization used by the manuscript. -/
theorem autocorrelation_inversion (q : Ix d → ℂ) (t : Ix d) :
    autocorrelation q t = (d : ℂ)⁻¹ *
      ∑ m, chi (-(m * t)) * (powerSpectrum q m : ℂ) := by
  rw [fourier_inversion (autocorrelation q) t]
  simp only [fourier_autocorrelation]

@[simp] theorem autocorrelation_zero (q : Ix d → ℂ) (hq : UnitPhases q) :
    autocorrelation q 0 = d := by
  simp only [autocorrelation, add_zero]
  calc
    (∑ j, q j * star (q j)) = ∑ _j : Ix d, (1 : ℂ) := by
      apply Finset.sum_congr rfl
      intro j _
      simpa [mul_comm] using hq j
    _ = d := by simp [ZMod.card]

theorem autocorrelation_neg (q : Ix d → ℂ) (t : Ix d) :
    autocorrelation q (-t) = star (autocorrelation q t) := by
  unfold autocorrelation
  simp only [star_sum, star_mul, star_star]
  calc
    (∑ j, q (j + -t) * star (q j)) =
        ∑ j, q j * star (q (j + t)) := by
      have h := sum_translate (fun j => q (j - t) * star (q j)) t
      simpa only [sub_eq_add_neg, add_neg_cancel_right] using h.symm
    _ = _ := by apply Finset.sum_congr rfl; intro j _; ring

theorem parseval (q : Ix d → ℂ) (hq : UnitPhases q) :
    (∑ m, powerSpectrum q m) = (d : ℝ)^2 := by
  have h := autocorrelation_inversion q 0
  rw [autocorrelation_zero q hq] at h
  simp only [mul_zero, neg_zero, chi_zero, one_mul] at h
  have hd : (d : ℂ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  have hc := congrArg (fun z : ℂ => (d : ℂ) * z) h
  simp only [← mul_assoc, mul_inv_cancel₀ hd, one_mul] at hc
  have hr := congrArg Complex.re hc
  simpa [pow_two] using hr.symm

/-- Flatness is equivalent to vanishing of every nonzero lag, with R(0)
provided by actual unimodularity. -/
theorem flat_iff_autocorrelation (q : Ix d → ℂ) (hq : UnitPhases q) :
    FourierFlat q ↔ ∀ t : Ix d, t ≠ 0 → autocorrelation q t = 0 := by
  constructor
  · intro hf t ht
    rw [autocorrelation_inversion]
    simp only [FourierFlat, powerSpectrum] at hf
    simp only [powerSpectrum, hf, ← Finset.sum_mul]
    have hs : (∑ m : Ix d, chi (-(m * t))) = 0 := by
      simpa [neg_mul, mul_comm, ht] using character_sum (-t)
    rw [hs]
    simp
  · intro hr m
    have h := fourier_autocorrelation q m
    have he : fourier (autocorrelation q) m = (d : ℂ) := by
      rw [fourier]
      rw [Finset.sum_eq_single 0]
      · simp [autocorrelation_zero q hq]
      · intro t _ ht
        simp [hr t ht]
      · simp
    rw [he] at h
    exact (congrArg Complex.re h).symm

/-- Distributional formula only. Its physical Born bridge is proved in
GeneralWitness, not encoded into this definition. -/
def fourierTable (q : Ix d → ℂ) (a b : Ix d) : ℝ :=
  powerSpectrum q (-(a + b)) / (d : ℝ)^3

@[simp] theorem table_nonnegative (q : Ix d → ℂ) (a b : Ix d) :
    0 ≤ fourierTable q a b := by
  apply div_nonneg (Complex.normSq_nonneg _)
  positivity

theorem table_row_sum (q : Ix d → ℂ) (hq : UnitPhases q) (a : Ix d) :
    (∑ b, fourierTable q a b) = 1 / (d : ℝ) := by
  have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  unfold fourierTable
  rw [← Finset.sum_div]
  have hs : (∑ b, powerSpectrum q (-(a+b))) = ∑ m, powerSpectrum q m := by
    calc
      (∑ b, powerSpectrum q (-(a+b))) = ∑ b, powerSpectrum q (-b) := by
        simpa [add_comm] using sum_translate (fun b => powerSpectrum q (-b)) a
      _ = _ := sum_negate _
  rw [hs, parseval q hq]
  field_simp
  ring

theorem table_column_sum (q : Ix d → ℂ) (hq : UnitPhases q) (b : Ix d) :
    (∑ a, fourierTable q a b) = 1 / (d : ℝ) := by
  simpa [fourierTable, add_comm] using table_row_sum q hq b

theorem table_normalized (q : Ix d → ℂ) (hq : UnitPhases q) :
    (∑ a, ∑ b, fourierTable q a b) = 1 := by
  simp only [table_row_sum q hq, Finset.sum_const, Finset.card_univ,
    ZMod.card, nsmul_eq_mul]
  have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  field_simp

theorem table_uniform_iff (q : Ix d → ℂ) :
    (∀ a b, fourierTable q a b = 1/(d : ℝ)^2) ↔ FourierFlat q := by
  have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  constructor
  · intro h m
    have hm := h (-m) 0
    simp only [fourierTable, add_zero, neg_neg] at hm
    calc
      powerSpectrum q m = (powerSpectrum q m / (d : ℝ)^3) * (d : ℝ)^3 := by
        field_simp
      _ = (1/(d : ℝ)^2) * (d : ℝ)^3 := by rw [hm]
      _ = d := by field_simp; ring
  · intro h a b
    rw [fourierTable, h]
    field_simp
    ring

theorem nonzero_lag_not_uniform (q : Ix d → ℂ) (hq : UnitPhases q)
    (t : Ix d) (ht : t ≠ 0) (hR : autocorrelation q t ≠ 0) :
    ¬ ∀ a b, fourierTable q a b = 1/(d : ℝ)^2 := by
  intro hu
  exact hR ((flat_iff_autocorrelation q hq).mp ((table_uniform_iff q).mp hu) t ht)

/-- The same plus-sign transform for an arbitrary complex module. -/
def moduleFourier {E : Type*} [AddCommGroup E] [Module ℂ E]
    (f : Ix d → E) (m : Ix d) : E := ∑ j, chi (m*j) • f j

theorem moduleFourier_eq_dft {E : Type*} [AddCommGroup E] [Module ℂ E]
    (f : Ix d → E) (m : Ix d) : moduleFourier f m = ZMod.dft f (-m) := by
  simp [moduleFourier, ZMod.dft_apply, chi, mul_comm]

theorem moduleFourier_inversion {E : Type*} [AddCommGroup E] [Module ℂ E]
    (f : Ix d → E) (j : Ix d) :
    f j = (d : ℂ)⁻¹ • ∑ m, chi (-(m*j)) • moduleFourier f m := by
  have h := congrFun (ZMod.dft.symm_apply_apply f) j
  rw [ZMod.invDFT_apply] at h
  symm
  refine Eq.trans ?_ h
  congr 1
  symm
  calc
    (∑ m, chi (m*j) • ZMod.dft f m) =
        ∑ m, chi ((-m)*j) • ZMod.dft f (-m) :=
      (sum_negate (fun m => chi (m*j) • ZMod.dft f m)).symm
    _ = _ := by simp only [neg_mul, moduleFourier_eq_dft]

/-- Operator-valued coefficients, not traces of coefficients. -/
def operatorFourier {E : Type*} [AddCommGroup E] [Module ℂ E]
    (σ : Ix d → Ix d → E) (k l : Ix d) : E :=
  ∑ a, ∑ b, chi (k*a + l*b) • σ a b

theorem operatorFourier_nested {E : Type*} [AddCommGroup E] [Module ℂ E]
    (σ : Ix d → Ix d → E) (k l : Ix d) :
    moduleFourier (fun b => moduleFourier (fun a => σ a b) k) l =
      operatorFourier σ k l := by
  simp only [moduleFourier, operatorFourier, smul_sum, smul_smul, chi_add]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro b _
  rw [mul_comm]

theorem operatorFourier_inversion {E : Type*} [AddCommGroup E] [Module ℂ E]
    (σ : Ix d → Ix d → E) (a b : Ix d) :
    σ a b = (d : ℂ)⁻¹ ^ 2 •
      ∑ k, ∑ l, chi (-(k*a + l*b)) • operatorFourier σ k l := by
  have hr (k : Ix d) : moduleFourier (fun a' => σ a' b) k =
      (d : ℂ)⁻¹ • ∑ l, chi (-(l*b)) • operatorFourier σ k l := by
    rw [moduleFourier_inversion (fun b' => moduleFourier (fun a' => σ a' b') k) b]
    simp only [operatorFourier_nested]
  calc
    σ a b = (d : ℂ)⁻¹ • ∑ k, chi (-(k*a)) •
        moduleFourier (fun a' => σ a' b) k := moduleFourier_inversion (fun a' => σ a' b) a
    _ = (d : ℂ)⁻¹ • ∑ k, chi (-(k*a)) •
        ((d : ℂ)⁻¹ • ∑ l, chi (-(l*b)) • operatorFourier σ k l) := by
      simp_rw [hr]
    _ = _ := by
      simp only [smul_sum, smul_smul, neg_add, chi_add]
      apply Finset.sum_congr rfl
      intro k _
      apply Finset.sum_congr rfl
      intro l _
      congr 1
      ring

/-- Complete operator privacy is equivalent to all nontrivial operator Fourier
coefficients vanishing; normalized zeroth coefficient is explicit. -/
theorem operator_uniform_iff {E : Type*} [AddCommGroup E] [Module ℂ E]
    (σ : Ix d → Ix d → E) (ρ : E) :
    (∀ a b, σ a b = ((d : ℂ)⁻¹)^2 • ρ) ↔
      operatorFourier σ 0 0 = ρ ∧
      ∀ k l, (k,l) ≠ (0,0) → operatorFourier σ k l = 0 := by
  have hd : (d : ℂ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  constructor
  · intro h
    have he (k l : Ix d) : operatorFourier σ k l =
        ((d : ℂ)⁻¹)^2 • ((if k = 0 then (d : ℂ) else 0) *
          (if l = 0 then (d : ℂ) else 0)) • ρ := by
      simp only [operatorFourier, h, chi_add, smul_smul, ← Finset.sum_smul,
        ← Finset.mul_sum, ← Finset.sum_mul]
      rw [character_sum, character_sum]
      congr 1
      ring
    constructor
    · rw [he]
      simp only [ite_true, smul_smul]
      have hc : (d : ℂ)⁻¹ ^ 2 * ((d : ℂ)*(d : ℂ)) = 1 := by field_simp; ring
      rw [hc, one_smul]
    · intro k l hkl
      rw [he]
      by_cases hk : k = 0
      · have hl : l ≠ 0 := by intro hl; exact hkl (Prod.ext hk hl)
        simp [hk, hl]
      · simp [hk]
  · rintro ⟨hzero,hrest⟩ a b
    rw [operatorFourier_inversion σ a b]
    congr 1
    rw [Finset.sum_eq_single 0]
    · rw [Finset.sum_eq_single 0]
      · simp [hzero]
      · intro l _ hl
        rw [hrest 0 l (by simpa using hl)]
        simp
      · simp
    · intro k _ hk
      apply Finset.sum_eq_zero
      intro l _
      rw [hrest k l (by intro h; exact hk (congrArg Prod.fst h))]
      simp
    · simp

end CyclicBell.General
