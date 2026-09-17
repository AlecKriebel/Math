import CyclicBell.Fourier4
import CyclicBell.ScalarData

/-!
# A polynomial SOS for the first family at d=4

This is a finite algebraic replacement for the manuscript's all-d polar proof,
not a claimed formalization of that all-d proof. It has no spectral assumptions.

k = sqrt 2, s = sin(pi/8), alpha=(c+s)/2, beta=(s-c)/2.
P(T)=sI+2alpha T+sT²; Q(T)=beta I+alpha T+alpha T²+beta T³.
For U=A0†A1, T_y=i^y U, let
F_y=(I+T_y)A0†-P(T_y)B_y, G_y=T_y A0†-Q(T_y)B_y.
Then M4 I-I4=(s/2) sum_y(F_y†F_y+k G_y†G_y).
The source below proves the algebra and direct PSD mixed-state bound separately.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.FirstSOS
open D4
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
set_option maxRecDepth 20000
set_option maxHeartbeats 12000000

def pCoefficients : Fin 4 → ℂ := ![(s : ℂ), 2 * (alpha : ℂ), (s : ℂ), 0]
def qCoefficients : Fin 4 → ℂ := ![(beta : ℂ), (alpha : ℂ), (alpha : ℂ), (beta : ℂ)]
def P (U : Mat ι) (y : Fin 4) : Mat ι := cyclePoly pCoefficients U y
def Q (U : Mat ι) (y : Fin 4) : Mat ι := cyclePoly qCoefficients U y

def F (A U : Mat ι) (B : Fin 4 → Mat ι) (y : Fin 4) : Mat ι :=
  (1 + rotated U y) * A.conjTranspose - P U y * B y

def G (A U : Mat ι) (B : Fin 4 → Mat ι) (y : Fin 4) : Mat ι :=
  rotated U y * A.conjTranspose - Q U y * B y

def rawTerm (A U : Mat ι) (B : Fin 4 → Mat ι) (y : Fin 4) : Mat ι :=
  A * (1 + rotated U y) * B y

def reducedOperator (A U : Mat ι) (B : Fin 4 → Mat ι) : Mat ι :=
  ∑ y : Fin 4, herm (rawTerm A U B y)

def squareSum (A U : Mat ι) (B : Fin 4 → Mat ι) : Mat ι :=
  ∑ y : Fin 4, ((F A U B y).conjTranspose * F A U B y +
    (k : ℂ) • ((G A U B y).conjTranspose * G A U B y))

def M : ℝ := 4 * (2 + k) * s

theorem M_eq : M = 2 / Real.sin (Real.pi / 8) := first_constant_bridge

theorem P_expand (U : Mat ι) (y : Fin 4) :
    P U y = (s : ℂ) • 1 + (2 * (alpha : ℂ)) • rotated U y +
      (s : ℂ) • (rotated U y ^ 2) := by
  simp [P, cyclePoly_eq, pCoefficients, Fin.sum_univ_succ, add_assoc]

theorem Q_expand (U : Mat ι) (y : Fin 4) :
    Q U y = (beta : ℂ) • 1 + (alpha : ℂ) • rotated U y +
      (alpha : ℂ) • rotated U y ^ 2 + (beta : ℂ) • rotated U y ^ 3 := by
  simp [Q, cyclePoly_eq, qCoefficients, Fin.sum_univ_succ, add_assoc]

theorem coefficient_zero :
    (s : ℂ) * ((s : ℂ) + (k : ℂ) * (beta : ℂ)) = 0 := by
  have hr : s * (s + k * beta) = 0 := by rw [k_beta]; ring
  exact_mod_cast hr

theorem coefficient_one :
    (s : ℂ) * ((s : ℂ) + 2 * (alpha : ℂ) + (k : ℂ) * (alpha : ℂ)) = 1 := by
  have hr : s * (s + 2 * alpha + k * alpha) = 1 := by
    rw [k_alpha]
    unfold alpha
    nlinarith [s_sq, sc_product]
  exact_mod_cast hr

theorem cross_factorization {U : Mat ι} (hU : UnitaryRel U) (y : Fin 4) :
    (s : ℂ) • (((1 + rotated U y).conjTranspose * P U y) +
      (k : ℂ) • ((rotated U y).conjTranspose * Q U y)) = 1 + rotated U y := by
  have hT := rotated_unitary hU y
  calc
    (s : ℂ) • (((1 + rotated U y).conjTranspose * P U y) +
      (k : ℂ) • ((rotated U y).conjTranspose * Q U y)) =
      ((s : ℂ) * ((s : ℂ) + (k : ℂ) * (beta : ℂ))) •
        ((rotated U y).conjTranspose + rotated U y ^ 2) +
      ((s : ℂ) * ((s : ℂ) + 2 * (alpha : ℂ) + (k : ℂ) * (alpha : ℂ))) •
        (1 + rotated U y) := by
      rw [P_expand, Q_expand]
      simp only [Matrix.conjTranspose_add, Matrix.conjTranspose_one, add_mul, mul_add,
        smul_mul_assoc, mul_smul_comm, smul_add, add_smul, smul_smul,
        pow_succ, pow_zero, mul_one, one_mul, mul_assoc, hT.1, hT.cancel_left]
      apply Matrix.ext
      intro i j
      simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
      ring
    _ = 1 + rotated U y := by rw [coefficient_zero, coefficient_one]; simp

theorem p_coefficient_energy :
    (∑ j : Fin 4, star (pCoefficients j) * pCoefficients j) = 2 := by
  norm_num [pCoefficients, Fin.sum_univ_succ]
  apply Complex.ext <;> norm_num [Complex.mul_re, Complex.mul_im] <;>
    nlinarith [s_sq, alpha_sq]

theorem q_coefficient_energy :
    (∑ j : Fin 4, star (qCoefficients j) * qCoefficients j) = 1 := by
  norm_num [qCoefficients, Fin.sum_univ_succ]
  apply Complex.ext <;> norm_num [Complex.mul_re, Complex.mul_im] <;>
    nlinarith [alpha_sq, beta_sq]

theorem P_energy {U : Mat ι} (hU : UnitaryRel U) :
    (∑ y : Fin 4, (P U y).conjTranspose * P U y) = (8 : ℂ) • (1 : Mat ι) := by
  simpa only [P, p_coefficient_energy, show (4 : ℂ) * 2 = 8 by norm_num]
    using cyclePoly_energy pCoefficients hU

theorem Q_energy {U : Mat ι} (hU : UnitaryRel U) :
    (∑ y : Fin 4, (Q U y).conjTranspose * Q U y) = (4 : ℂ) • (1 : Mat ι) := by
  simpa only [Q, q_coefficient_energy, mul_one] using cyclePoly_energy qCoefficients hU

theorem top_energy {U : Mat ι} (hU : UnitaryRel U) :
    (∑ y : Fin 4, (1 + rotated U y).conjTranspose * (1 + rotated U y)) =
      (8 : ℂ) • (1 : Mat ι) := by
  have hpoly (y : Fin 4) :
      cyclePoly (![1,1,0,0] : Fin 4 → ℂ) U y = 1 + rotated U y := by
    simp [cyclePoly_eq, Fin.sum_univ_succ]
  have he := cyclePoly_energy (![1,1,0,0] : Fin 4 → ℂ) hU
  norm_num [hpoly, Fin.sum_univ_succ] at he ⊢
  exact he

theorem rotated_energy {U : Mat ι} (hU : UnitaryRel U) :
    (∑ y : Fin 4, (rotated U y).conjTranspose * rotated U y) =
      (4 : ℂ) • (1 : Mat ι) := by
  have hh (y : Fin 4) := (rotated_unitary hU y).1
  simp only [hh]
  norm_num [Fin.sum_univ_succ, ← add_smul]
  simpa using (Nat.cast_smul_eq_nsmul ℂ 4 (1 : Mat ι)).symm

/-- Elementary Gram expansion: coefficients r,t are real, not arbitrary complex. -/
theorem two_square_expansion (C₀ C₁ D₀ D₁ : Mat ι) (r t : ℝ) :
    (r : ℂ) • ((C₀-D₀).conjTranspose * (C₀-D₀) +
      (t : ℂ) • ((C₁-D₁).conjTranspose * (C₁-D₁))) =
    (r : ℂ) • (C₀.conjTranspose*C₀ + (t : ℂ) • (C₁.conjTranspose*C₁)) +
    (r : ℂ) • (D₀.conjTranspose*D₀ + (t : ℂ) • (D₁.conjTranspose*D₁)) -
    ((r : ℂ) • (C₀.conjTranspose*D₀ + (t : ℂ) • (C₁.conjTranspose*D₁)) +
     ((r : ℂ) • (C₀.conjTranspose*D₀ + (t : ℂ) • (C₁.conjTranspose*D₁))).conjTranspose) := by
  simp only [Matrix.conjTranspose_sub, Matrix.conjTranspose_add,
    Matrix.conjTranspose_smul, Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose,
    star_mul, star_real, sub_mul, mul_sub, smul_add, smul_sub, smul_smul]
  apply Matrix.ext
  intro i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

theorem row_cross {U : Mat ι} (hU : UnitaryRel U) (A B : Mat ι) (y : Fin 4) :
    (s : ℂ) • (((1 + rotated U y) * A.conjTranspose).conjTranspose * (P U y * B) +
      (k : ℂ) • ((rotated U y * A.conjTranspose).conjTranspose * (Q U y * B))) =
      A * (1 + rotated U y) * B := by
  calc
    _ = A * ((s : ℂ) • (((1 + rotated U y).conjTranspose * P U y) +
      (k : ℂ) • ((rotated U y).conjTranspose * Q U y))) * B := by
      simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose,
        Matrix.conjTranspose_add, Matrix.conjTranspose_one, one_mul,
        mul_add, add_mul, mul_smul_comm, smul_mul_assoc, smul_add, smul_smul, mul_assoc]
    _ = _ := by rw [cross_factorization hU]

theorem right_energy_sum (W : Fin 4 → Mat ι) (V : Mat ι) :
    (∑ y : Fin 4, (W y * V).conjTranspose * (W y * V)) =
      V.conjTranspose * (∑ y : Fin 4, (W y).conjTranspose * W y) * V := by
  simp only [Matrix.conjTranspose_mul, Finset.mul_sum, Finset.sum_mul, mul_assoc]

theorem first_diagonal_sum {A U : Mat ι} (hA : UnitaryRel A) (hU : UnitaryRel U) :
    (∑ y : Fin 4,
      (s : ℂ) • (((1 + rotated U y) * A.conjTranspose).conjTranspose *
        ((1 + rotated U y) * A.conjTranspose) +
      (k : ℂ) • ((rotated U y * A.conjTranspose).conjTranspose *
        (rotated U y * A.conjTranspose)))) = (M : ℂ) • (1 : Mat ι) := by
  rw [← Finset.smul_sum, Finset.sum_add_distrib, ← Finset.smul_sum,
    right_energy_sum, right_energy_sum, top_energy hU, rotated_energy hU]
  simp only [Matrix.conjTranspose_conjTranspose, smul_mul_assoc, mul_smul_comm,
    mul_one, hA.2, smul_smul]
  apply Matrix.ext
  intro i j
  simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  push_cast
  unfold M
  push_cast
  ring

theorem second_diagonal_sum {U : Mat ι} (hU : UnitaryRel U)
    (B : Fin 4 → Mat ι) (hB : ∀ y, UnitaryRel (B y))
    (hc : ∀ y, U * B y = B y * U) :
    (∑ y : Fin 4,
      (s : ℂ) • ((P U y * B y).conjTranspose * (P U y * B y) +
      (k : ℂ) • ((Q U y * B y).conjTranspose * (Q U y * B y)))) =
      (M : ℂ) • (1 : Mat ι) := by
  have hp (y : Fin 4) : (P U y * B y).conjTranspose * (P U y * B y) =
      (P U y).conjTranspose * P U y :=
    commuting_right_energy (hB y) (cyclePoly_commute pCoefficients (hc y) y)
  have hq (y : Fin 4) : (Q U y * B y).conjTranspose * (Q U y * B y) =
      (Q U y).conjTranspose * Q U y :=
    commuting_right_energy (hB y) (cyclePoly_commute qCoefficients (hc y) y)
  simp_rw [hp, hq]
  rw [← Finset.smul_sum, Finset.sum_add_distrib, ← Finset.smul_sum, P_energy hU, Q_energy hU]
  apply Matrix.ext
  intro i j
  simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  unfold M
  push_cast
  ring

/-- The full polynomial operator identity, not just witness annihilation. -/
theorem reduced_gap_identity {A U : Mat ι} (hA : UnitaryRel A) (hU : UnitaryRel U)
    (B : Fin 4 → Mat ι) (hB : ∀ y, UnitaryRel (B y))
    (hc : ∀ y, U * B y = B y * U) :
    (M : ℂ) • (1 : Mat ι) - reducedOperator A U B =
      ((s / 2 : ℝ) : ℂ) • squareSum A U B := by
  have hrow (y : Fin 4) :
      (s : ℂ) • ((F A U B y).conjTranspose * F A U B y +
        (k : ℂ) • ((G A U B y).conjTranspose * G A U B y)) =
      (s : ℂ) • (((1 + rotated U y) * A.conjTranspose).conjTranspose *
        ((1 + rotated U y) * A.conjTranspose) +
        (k : ℂ) • ((rotated U y * A.conjTranspose).conjTranspose *
          (rotated U y * A.conjTranspose))) +
      (s : ℂ) • ((P U y * B y).conjTranspose * (P U y * B y) +
        (k : ℂ) • ((Q U y * B y).conjTranspose * (Q U y * B y))) -
      (rawTerm A U B y + (rawTerm A U B y).conjTranspose) := by
    unfold F G rawTerm
    rw [two_square_expansion, row_cross hU]
  have hraw :
      (∑ y : Fin 4, (rawTerm A U B y + (rawTerm A U B y).conjTranspose)) =
        (2 : ℂ) • reducedOperator A U B := by
    unfold reducedOperator herm
    rw [Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro y _
    simp [smul_smul]
  have he : (s : ℂ) • squareSum A U B =
      (M : ℂ) • (1 : Mat ι) + (M : ℂ) • 1 - (2 : ℂ) • reducedOperator A U B := by
    calc
      (s : ℂ) • squareSum A U B =
          ∑ y : Fin 4, (s : ℂ) • ((F A U B y).conjTranspose * F A U B y +
            (k : ℂ) • ((G A U B y).conjTranspose * G A U B y)) := by
              simp only [squareSum, Finset.smul_sum]
      _ = ∑ y : Fin 4,
          ((s : ℂ) • (((1 + rotated U y) * A.conjTranspose).conjTranspose *
            ((1 + rotated U y) * A.conjTranspose) +
            (k : ℂ) • ((rotated U y * A.conjTranspose).conjTranspose *
              (rotated U y * A.conjTranspose))) +
          (s : ℂ) • ((P U y * B y).conjTranspose * (P U y * B y) +
            (k : ℂ) • ((Q U y * B y).conjTranspose * (Q U y * B y))) -
          (rawTerm A U B y + (rawTerm A U B y).conjTranspose)) := by
            exact Finset.sum_congr rfl (fun y _ => hrow y)
      _ = _ := by
        rw [Finset.sum_sub_distrib, Finset.sum_add_distrib,
          first_diagonal_sum hA hU, second_diagonal_sum hU B hB hc, hraw]
  have hehalf := congrArg (fun T : Mat ι => (1 / 2 : ℂ) • T) he
  apply Matrix.ext
  intro i j
  have hh := congrFun (congrFun hehalf i) j
  simp only [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul] at hh ⊢
  push_cast at hh ⊢
  linear_combination -hh

/-- Augmentation is included in the same explicit positive-square identity. -/
theorem augmented_gap_identity {A U Bstar : Mat ι}
    (hA : UnitaryRel A) (hU : UnitaryRel U)
    (B : Fin 4 → Mat ι) (hB : ∀ y, UnitaryRel (B y))
    (hc : ∀ y, U * B y = B y * U) (hstar : UnitaryRel Bstar) :
    ((M + 1 : ℝ) : ℂ) • (1 : Mat ι) -
      (reducedOperator A U B + herm (A * Bstar)) =
      ((s / 2 : ℝ) : ℂ) • squareSum A U B +
      (1 / 2 : ℂ) • ((1 - A * Bstar).conjTranspose * (1 - A * Bstar)) := by
  rw [← reduced_gap_identity hA hU B hB hc, ← aligned_gap_identity (hA.mul hstar)]
  apply Matrix.ext
  intro i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  push_cast
  ring

/-- Mixed-state first-family upper bound with arbitrary finite index type. -/
theorem reduced_upper {ρ A U : Mat ι} (hρ : ρ.PosSemidef)
    (htrace : Matrix.trace ρ = 1) (hA : UnitaryRel A) (hU : UnitaryRel U)
    (B : Fin 4 → Mat ι) (hB : ∀ y, UnitaryRel (B y))
    (hc : ∀ y, U * B y = B y * U) :
    stateEval ρ (reducedOperator A U B) ≤ M := by
  have hss : 0 ≤ stateEval ρ (squareSum A U B) := by
    unfold squareSum
    rw [stateEval_sum]
    apply Finset.sum_nonneg
    intro y _
    rw [stateEval_add, stateEval_real_smul]
    exact add_nonneg (stateEval_square_nonnegative hρ _) <|
      mul_nonneg k_nonneg (stateEval_square_nonnegative hρ _)
  have he := congrArg (stateEval ρ) (reduced_gap_identity hA hU B hB hc)
  rw [stateEval_sub, stateEval_real_smul, stateEval_one htrace,
    stateEval_real_smul] at he
  have hs : 0 ≤ s / 2 := le_of_lt (div_pos s_pos (by norm_num))
  have hh := mul_nonneg hs hss
  nlinarith

/-- The extra aligned unitary term adds exactly the independent upper bound 1. -/
theorem augmented_upper {ρ A U Bstar : Mat ι} (hρ : ρ.PosSemidef)
    (htrace : Matrix.trace ρ = 1) (hA : UnitaryRel A) (hU : UnitaryRel U)
    (B : Fin 4 → Mat ι) (hB : ∀ y, UnitaryRel (B y))
    (hc : ∀ y, U * B y = B y * U) (hstar : UnitaryRel Bstar) :
    stateEval ρ (reducedOperator A U B) + stateEval ρ (A * Bstar) ≤
      2 / Real.sin (Real.pi / 8) + 1 := by
  have hr := reduced_upper hρ htrace hA hU B hB hc
  have ha := aligned_upper hρ htrace (hA.mul hstar)
  rw [M_eq] at hr
  linarith

end CyclicBell.FirstSOS
