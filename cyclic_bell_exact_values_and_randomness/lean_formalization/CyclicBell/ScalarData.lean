import CyclicBell.Functionals
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-! Exact phase and coefficient bridges. No numerical roots or certificates.
The ζ used below IS exp(π i/8), so subsequent finite cyclotomic calculations
cannot silently choose a different embedding.  -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.D4

set_option maxRecDepth 10000
set_option maxHeartbeats 8000000

/-- Coordinate value cos(pi/4)=sin(pi/4); defined independently of the witness. -/
def h : ℝ := Real.sqrt 2 / 2

theorem h_sq : h ^ 2 = (1 : ℝ) / 2 := by
  unfold h
  nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)]

def k : ℝ := Real.sqrt 2
def s : ℝ := Real.sin (Real.pi / 8)
def c : ℝ := Real.cos (Real.pi / 8)
def zeta : ℂ := Complex.exp (((Real.pi / 8 : ℝ) : ℂ) * Complex.I)
theorem h_eq_k : h = k / 2 := rfl

def alpha : ℝ := (c + s) / 2
def beta : ℝ := (s - c) / 2

theorem k_sq : k ^ 2 = 2 := by
  exact Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)
theorem k_nonneg : 0 ≤ k := Real.sqrt_nonneg 2
theorem k_pos : 0 < k := Real.sqrt_pos.2 (by norm_num)
theorem k_lt_two : k < 2 := by nlinarith [k_sq, k_nonneg]
theorem s_pos : 0 < s := by
  exact Real.sin_pos_of_pos_of_lt_pi (by positivity) (by linarith [Real.pi_pos])
theorem c_pos : 0 < c := by
  apply Real.cos_pos_of_mem_Ioo
  constructor <;> linarith [Real.pi_pos]

theorem s_sq : s ^ 2 = (2 - k) / 4 := by
  have ht := Real.cos_two_mul (Real.pi / 8)
  rw [show 2 * (Real.pi / 8) = Real.pi / 4 by ring, Real.cos_pi_div_four] at ht
  have hu := Real.sin_sq_add_cos_sq (Real.pi / 8)
  dsimp [s, k]
  nlinarith

theorem c_sq : c ^ 2 = (2 + k) / 4 := by
  have ht := Real.sin_sq_add_cos_sq (Real.pi / 8)
  change s ^ 2 + c ^ 2 = 1 at ht
  linarith [s_sq]

theorem sc_product : s * c = k / 4 := by
  have ht := Real.sin_two_mul (Real.pi / 8)
  rw [show 2 * (Real.pi / 8) = Real.pi / 4 by ring, Real.sin_pi_div_four] at ht
  change Real.sqrt 2 / 2 = 2 * s * c at ht
  change k / 2 = 2 * s * c at ht
  linarith

theorem c_eq : c = (1 + k) * s := by
  apply mul_left_cancel₀ (ne_of_gt s_pos)
  have hs := congrArg (fun x : ℝ => k * x) s_sq
  nlinarith [s_sq, sc_product, k_sq]

theorem alpha_times_s : 4 * s * alpha = 1 := by
  unfold alpha
  nlinarith [s_sq, sc_product]
theorem beta_times_c : 4 * c * beta = -1 := by
  unfold beta
  nlinarith [c_sq, sc_product]
theorem alpha_source : alpha = 1 / (4 * s) := by
  apply (eq_div_iff (mul_ne_zero (by norm_num) (ne_of_gt s_pos))).2
  nlinarith [alpha_times_s]
theorem beta_source : beta = -1 / (4 * c) := by
  apply (eq_div_iff (mul_ne_zero (by norm_num) (ne_of_gt c_pos))).2
  nlinarith [beta_times_c]

theorem alpha_sq : alpha ^ 2 = (2 + k) / 8 := by
  unfold alpha
  nlinarith [s_sq, c_sq, sc_product]
theorem beta_sq : beta ^ 2 = (2 - k) / 8 := by
  unfold beta
  nlinarith [s_sq, c_sq, sc_product]
theorem alpha_beta : alpha * beta = -k / 8 := by
  unfold alpha beta
  nlinarith [s_sq, c_sq]
theorem alpha_in_s : alpha = (2 + k) * s / 2 := by rw [alpha, c_eq]; ring
theorem beta_in_s : beta = -k * s / 2 := by rw [beta, c_eq]; ring

theorem s_quadratic_certificate : s ^ 2 * (4 + 2 * k) = 1 := by
  rw [s_sq]
  nlinarith [k_sq]

theorem first_constant_bridge : 4 * (2 + k) * s = 2 / Real.sin (Real.pi / 8) := by
  change 4 * (2 + k) * s = 2 / s
  apply (eq_div_iff (ne_of_gt s_pos)).2
  nlinarith [s_quadratic_certificate]

theorem zeta_components : zeta = (c : ℂ) + (s : ℂ) * Complex.I := by
  apply Complex.ext <;> simp [zeta, c, s, Complex.exp_re, Complex.exp_im]

theorem zeta_unit : star zeta * zeta = 1 := by
  rw [zeta_components]
  apply Complex.ext <;>
    norm_num [Complex.mul_re, Complex.mul_im] <;> nlinarith [s_sq, c_sq]
theorem zeta_normSq : Complex.normSq zeta = 1 := by
  apply Complex.ofReal_injective
  rw [Complex.normSq_eq_conj_mul_self]
  exact zeta_unit

theorem zeta_sq : zeta ^ 2 = (h : ℂ) + (h : ℂ) * Complex.I := by
  rw [zeta_components]
  apply Complex.ext <;>
    norm_num [pow_two, Complex.mul_re, Complex.mul_im, h_eq_k] <;>
    nlinarith [s_sq, c_sq, sc_product]

theorem zeta_cube : zeta ^ 3 = (s : ℂ) + (c : ℂ) * Complex.I := by
  rw [show (3 : ℕ) = 2 + 1 by decide, pow_add, pow_one, zeta_sq, zeta_components]
  rw [c_eq]
  apply Complex.ext <;>
    norm_num [Complex.mul_re, Complex.mul_im, h_eq_k] <;>
    nlinarith [k_sq, congrArg (fun x : ℝ => s * x) k_sq]

theorem zeta_four : zeta ^ 4 = Complex.I := by
  rw [show (4 : ℕ) = 2 * 2 by decide, pow_mul, zeta_sq]
  apply Complex.ext <;> norm_num [pow_two, Complex.mul_re, Complex.mul_im] <;>
    nlinarith [h_sq]

theorem zeta_eight : zeta ^ 8 = -1 := by
  rw [show (8 : ℕ) = 4 * 2 by decide, pow_mul, zeta_four]
  norm_num

theorem zeta_sixteen : zeta ^ 16 = 1 := by
  rw [show (16 : ℕ) = 8 * 2 by decide, pow_mul, zeta_eight]
  norm_num

theorem zeta_ne_zero : zeta ≠ 0 := by
  intro hz
  have ht := zeta_unit
  simp [hz] at ht

theorem star_zeta : star zeta = zeta ^ 15 := by
  apply mul_right_cancel₀ zeta_ne_zero
  rw [zeta_unit, ← pow_succ, zeta_sixteen]

theorem zeta_pow_exp (m : ℕ) :
    zeta ^ m = Complex.exp (((m : ℂ) * ((Real.pi / 8 : ℝ) : ℂ)) * Complex.I) := by
  induction m with
  | zero => simp
  | succ m hm =>
    rw [pow_succ, hm, zeta, ← Complex.exp_add]
    congr 1
    push_cast
    ring

theorem eta_bridge :
    Complex.exp (((Real.pi / 4 : ℝ) : ℂ) * Complex.I) = zeta ^ 2 := by
  rw [zeta_pow_exp]
  congr 1
  push_cast
  ring

/-- A finite, explicitly checked power table; no reduction engine is trusted. -/
def phaseTable : Fin 16 → ℂ :=
  ![1, (c : ℂ) + s * Complex.I, (h : ℂ) + h * Complex.I,
    (s : ℂ) + c * Complex.I, Complex.I, -(s : ℂ) + c * Complex.I,
    -(h : ℂ) + h * Complex.I, -(c : ℂ) + s * Complex.I,
    -1, -(c : ℂ) - s * Complex.I, -(h : ℂ) - h * Complex.I,
    -(s : ℂ) - c * Complex.I, -Complex.I, (s : ℂ) - c * Complex.I,
    (h : ℂ) - h * Complex.I, (c : ℂ) - s * Complex.I]

theorem zeta_phaseTable (j : Fin 16) : zeta ^ j.val = phaseTable j := by
  fin_cases j
  · norm_num [phaseTable]
  · simpa [phaseTable] using zeta_components
  · simpa [phaseTable] using zeta_sq
  · simpa [phaseTable] using zeta_cube
  · simpa [phaseTable] using zeta_four
  · change zeta ^ 5 = _
    rw [show (5 : ℕ) = 4 + 1 by decide, pow_add, zeta_four, pow_one, zeta_components]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · change zeta ^ 6 = _
    rw [show (6 : ℕ) = 4 + 2 by decide, pow_add, zeta_four, zeta_sq]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · change zeta ^ 7 = _
    rw [show (7 : ℕ) = 4 + 3 by decide, pow_add, zeta_four, zeta_cube]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · simpa [phaseTable] using zeta_eight
  · change zeta ^ 9 = _
    rw [show (9 : ℕ) = 8 + 1 by decide, pow_add, zeta_eight, pow_one, zeta_components]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · change zeta ^ 10 = _
    rw [show (10 : ℕ) = 8 + 2 by decide, pow_add, zeta_eight, zeta_sq]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · change zeta ^ 11 = _
    rw [show (11 : ℕ) = 8 + 3 by decide, pow_add, zeta_eight, zeta_cube]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · change zeta ^ 12 = _
    rw [show (12 : ℕ) = 8 + 4 by decide, pow_add, zeta_eight, zeta_four]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · change zeta ^ 13 = _
    rw [show (13 : ℕ) = 8 + 5 by decide, pow_add, zeta_eight, show (5 : ℕ) = 4 + 1 by decide, pow_add, zeta_four, pow_one, zeta_components]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · change zeta ^ 14 = _
    rw [show (14 : ℕ) = 8 + 6 by decide, pow_add, zeta_eight, show (6 : ℕ) = 4 + 2 by decide, pow_add, zeta_four, zeta_sq]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]
  · change zeta ^ 15 = _
    rw [show (15 : ℕ) = 8 + 7 by decide, pow_add, zeta_eight, show (7 : ℕ) = 4 + 3 by decide, pow_add, zeta_four, zeta_cube]
    apply Complex.ext <;> norm_num [phaseTable, Complex.mul_re, Complex.mul_im]

theorem zeta_pow_5 : zeta ^ 5 = -(s : ℂ) + (c : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (5 : Fin 16)

theorem zeta_pow_6 : zeta ^ 6 = -(h : ℂ) + (h : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (6 : Fin 16)

theorem zeta_pow_7 : zeta ^ 7 = -(c : ℂ) + (s : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (7 : Fin 16)

theorem zeta_pow_9 : zeta ^ 9 = -(c : ℂ) - (s : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (9 : Fin 16)

theorem zeta_pow_10 : zeta ^ 10 = -(h : ℂ) - (h : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (10 : Fin 16)

theorem zeta_pow_11 : zeta ^ 11 = -(s : ℂ) - (c : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (11 : Fin 16)

theorem zeta_pow_12 : zeta ^ 12 = -Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (12 : Fin 16)

theorem zeta_pow_13 : zeta ^ 13 = (s : ℂ) - (c : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (13 : Fin 16)

theorem zeta_pow_14 : zeta ^ 14 = (h : ℂ) - (h : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (14 : Fin 16)

theorem zeta_pow_15 : zeta ^ 15 = (c : ℂ) - (s : ℂ) * Complex.I := by
  simpa [phaseTable] using zeta_phaseTable (15 : Fin 16)

/-- Period reduction is justified by ζ^16=1, not imposed as a quotient. -/
theorem zeta_pow_mod (m : ℕ) : zeta ^ m = zeta ^ (m % 16) := by
  conv_lhs => rw [← Nat.div_add_mod m 16, pow_add, pow_mul]
  simp [zeta_sixteen]

theorem zeta_pow_unit (m : ℕ) : star (zeta ^ m) * zeta ^ m = 1 := by
  rw [star_pow, ← mul_pow, zeta_unit]
  simp

/-- Algebraic second-family coefficients, equivalent to the source formula. -/
def lambda : Fin 4 → ℂ := ![(alpha : ℂ), (alpha : ℂ), (beta : ℂ) * Complex.I,
  (beta : ℂ) * Complex.I]

theorem sourceLambda_eq (l : Fin 4) : sourceLambda l = lambda l := by
  have hsneg : Real.sin (Real.pi * ((0 : ℝ) - 1 / 2) / 4) = -s := by
    rw [show Real.pi * ((0 : ℝ) - 1 / 2) / 4 = -(Real.pi / 8) by ring,
      Real.sin_neg]
    rfl
  have hsone : Real.sin (Real.pi * ((1 : ℝ) - 1 / 2) / 4) = s := by
    congr 1 <;> ring
  have hstwo : Real.sin (Real.pi * ((2 : ℝ) - 1 / 2) / 4) = c := by
    rw [show Real.pi * ((2 : ℝ) - 1 / 2) / 4 = Real.pi / 2 - Real.pi / 8 by ring,
      Real.sin_pi_div_two_sub]
    rfl
  have hsthree : Real.sin (Real.pi * ((3 : ℝ) - 1 / 2) / 4) = c := by
    rw [show Real.pi * ((3 : ℝ) - 1 / 2) / 4 = Real.pi / 8 + Real.pi / 2 by ring,
      Real.sin_add_pi_div_two]
    rfl
  have hs0 : (s : ℂ) ≠ 0 := by exact_mod_cast (ne_of_gt s_pos)
  have hc0 : (c : ℂ) ≠ 0 := by exact_mod_cast (ne_of_gt c_pos)
  unfold sourceLambda
  rw [eta_bridge]
  fin_cases l <;>
    simp only [Fin.reduceFinMk,
      Nat.cast_zero, Nat.cast_one, Nat.cast_ofNat, hsneg, hsone, hstwo, hsthree]
  all_goals dsimp [lambda]
  all_goals norm_num [alpha_source, beta_source, ← pow_mul, zeta_four,
      zeta_phaseTable (12 : Fin 16), phaseTable, Complex.ofReal_mul,
      Complex.ofReal_neg, Complex.ofReal_div]
  all_goals field_simp [hs0, hc0] <;> ring_nf
  all_goals norm_num [zpow_ofNat, ← pow_mul, zeta_four, zeta_pow_12]

theorem lambda_normalization : (∑ l : Fin 4, star (lambda l) * lambda l) = 1 := by
  norm_num [lambda, Fin.sum_univ_succ]
  apply Complex.ext <;> norm_num [Complex.mul_re, Complex.mul_im] <;>
    nlinarith [alpha_sq, beta_sq]

theorem sourceLambda_normalization :
    (∑ l : Fin 4, Complex.normSq (sourceLambda l)) = 1 := by
  apply Complex.ofReal_injective
  simp only [Complex.ofReal_sum, Complex.normSq_eq_conj_mul_self, sourceLambda_eq]
  exact lambda_normalization


theorem k_alpha : k * alpha = c := by
  rw [alpha_in_s, c_eq]
  have hk := congrArg (fun x : ℝ => x * s) k_sq
  dsimp at hk
  linear_combination hk / 2

theorem k_beta : k * beta = -s := by
  rw [beta_in_s]
  have hk := congrArg (fun x : ℝ => x * s) k_sq
  dsimp at hk
  linear_combination -hk / 2

attribute [simp] zeta_sq zeta_four zeta_eight zeta_sixteen
attribute [simp] zeta_pow_5 zeta_pow_6 zeta_pow_7 zeta_pow_9 zeta_pow_10 zeta_pow_11 zeta_pow_12 zeta_pow_13 zeta_pow_14 zeta_pow_15

end CyclicBell.D4
