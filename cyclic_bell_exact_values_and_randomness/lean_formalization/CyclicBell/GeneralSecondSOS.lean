import CyclicBell.GeneralModel

/-! General d second-family SOS, with its exact 1/(2d) prefactor.
The coefficient normalization is EXPLICIT in this generic helper. The separate
GeneralSecondCoefficients module discharges it for the manuscript coefficients.
No commutation of same-party observables is used.  -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def secondFourier (B : Ix d → Mat ι) (l : Ix d) : Mat ι := moduleFourier B l

theorem fourier_character_orthogonality (y z : Ix d) :
    (∑ l : Ix d,star (chi (l*y))*chi (l*z))=if y=z then (d : ℂ) else 0 := by
  have he (l : Ix d) : star (chi (l*y))*chi (l*z)=chi ((z-y)*l) := by
    rw [chi_star,← chi_add]
    congr 1
    ring
  simp_rw [he]
  rw [character_sum]
  by_cases hyz : y=z
  · simp [hyz]
  · have hzy : z-y≠0 := sub_ne_zero.mpr (Ne.symm hyz)
    simp [hyz,hzy]

/-- Parseval for operator Fourier transforms, including noncommuting By. -/
theorem secondFourier_energy (B : Ix d → Mat ι) :
    (∑ l,(secondFourier B l).conjTranspose*secondFourier B l)=
      (d : ℂ) • ∑ y,(B y).conjTranspose*B y := by
  have hexpand (l : Ix d) :
      (secondFourier B l).conjTranspose * secondFourier B l =
        ∑ y : Ix d, ∑ z : Ix d,
          (star (chi (l*y))*chi (l*z)) • ((B y).conjTranspose*B z) := by
    simp only [secondFourier,moduleFourier,Matrix.conjTranspose_sum,
      Matrix.conjTranspose_smul,Finset.sum_mul,Finset.mul_sum,
      smul_mul_assoc,mul_smul_comm,Finset.smul_sum,smul_smul]
    rw [Finset.sum_comm]
    simp only [mul_comm]
  simp_rw [hexpand]
  calc
    _ = ∑ y : Ix d, ∑ z : Ix d,
      (∑ l : Ix d, star (chi (l*y))*chi (l*z)) • ((B y).conjTranspose*B z) := by
      simp only [Finset.sum_smul]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro y _
      rw [Finset.sum_comm]
    _ = _ := by
      simp only [fourier_character_orthogonality]
      simp [Finset.smul_sum]

theorem secondFourier_unitary_energy (B : Ix d → Mat ι) (hB : ∀ y,UnitaryRel (B y)) :
    (∑ l,(secondFourier B l).conjTranspose*secondFourier B l)=(d : ℂ)^2 • (1 : Mat ι) := by
  rw [secondFourier_energy]
  simp only [(hB _).1]
  rw [Finset.sum_const, Finset.card_univ, ZMod.card]
  rw [← Nat.cast_smul_eq_nsmul ℂ d (1 : Mat ι), smul_smul, pow_two]

def secondReducedOperator (lam : Ix d → ℂ) (A B : Ix d → Mat ι) : Mat ι :=
  ∑ l,herm (star (lam l) • (A l*secondFourier B l))
def secondResidual (lam : Ix d → ℂ) (A B : Ix d → Mat ι) (l : Ix d) : Mat ι :=
  ((d : ℂ)*lam l) • 1-A l*secondFourier B l

theorem secondScalarExpansion (lam : ℂ) (C : Mat ι) :
    (((d : ℂ)*lam) • (1 : Mat ι)-C).conjTranspose*(((d : ℂ)*lam) • 1-C)=
      ((d : ℂ)^2*(star lam*lam)) • 1+C.conjTranspose*C-
        (d : ℂ) • (star lam • C+(star lam • C).conjTranspose) := by
  simp only [Matrix.conjTranspose_sub,Matrix.conjTranspose_smul,Matrix.conjTranspose_one,
    sub_mul,mul_sub,smul_mul_assoc,mul_smul_comm,smul_smul,one_mul,mul_one,
    star_mul,star_star,star_natCast]
  ext i j
  simp only [Matrix.sub_apply,Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
  ring

/-- The source identity eq:second-sos for normalized coefficients. -/
theorem second_general_sos (lam : Ix d → ℂ) (hlam : ∑ l,star (lam l)*lam l=1)
    (A B : Ix d → Mat ι) (hA : ∀ l,UnitaryRel (A l)) (hB : ∀ y,UnitaryRel (B y)) :
    (d : ℂ) • (1 : Mat ι)-secondReducedOperator lam A B =
      (1/(2*d) : ℂ) • ∑ l,(secondResidual lam A B l).conjTranspose*secondResidual lam A B l := by
  have hdC : (d : ℂ)≠0 := by exact_mod_cast (NeZero.ne d)
  have henergy (l : Ix d) :
      (A l*secondFourier B l).conjTranspose*(A l*secondFourier B l)=
        (secondFourier B l).conjTranspose*secondFourier B l := by
    rw [Matrix.conjTranspose_mul]
    simp only [mul_assoc,(hA l).cancel_left]
  have hs : (∑ l,(secondResidual lam A B l).conjTranspose*secondResidual lam A B l)=
      (2*(d : ℂ)^2) • (1 : Mat ι)-(2*d : ℂ) • secondReducedOperator lam A B := by
    unfold secondResidual
    simp_rw [secondScalarExpansion,henergy]
    rw [Finset.sum_sub_distrib,Finset.sum_add_distrib,← Finset.sum_smul,
      ← Finset.mul_sum,hlam,mul_one,secondFourier_unitary_energy B hB,← Finset.smul_sum]
    unfold secondReducedOperator herm
    simp only [Finset.smul_sum,smul_add,smul_smul]
    ext i j
    simp only [Matrix.sub_apply,Matrix.add_apply,Matrix.smul_apply,smul_eq_mul,Matrix.sum_apply,Finset.sum_apply]
    ring
  rw [hs]
  ext i j
  simp only [Matrix.sub_apply,Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
  field_simp [hdC]
  ring

theorem second_general_upper (ρ : StateOn ι) (lam : Ix d → ℂ)
    (hlam : ∑ l,star (lam l)*lam l=1) (A B : Ix d → Mat ι)
    (hA : ∀ l,UnitaryRel (A l)) (hB : ∀ y,UnitaryRel (B y)) :
    stateEval ρ.density (secondReducedOperator lam A B)≤d := by
  have hn : 0≤stateEval ρ.density
      (∑ l,(secondResidual lam A B l).conjTranspose*secondResidual lam A B l) := by
    rw [stateEval_sum]
    exact Finset.sum_nonneg (fun l _ => stateEval_square_nonnegative ρ.positive _)
  have h := congrArg (stateEval ρ.density) (second_general_sos lam hlam A B hA hB)
  have hc : (1/(2*d) : ℂ)=((1/(2*d) : ℝ) : ℂ) := by push_cast; rfl
  rw [hc] at h
  simp only [stateEval_sub,show (d : ℂ)=((d : ℝ) : ℂ) by simp,
    stateEval_real_smul,stateEval_one ρ.normalized] at h
  have hdR : 0 < (d : ℝ) := dimension_pos
  have hp : 0<(1/(2*d) : ℝ) := by positivity
  nlinarith

end CyclicBell.General
