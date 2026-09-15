import CyclicBell.GeneralCycles
import CyclicBell.GeneralScalar

/-! Source appendix coefficient calculations, with the literal positive clock
and forward shift. Coefficient DFT identities do not certify source-observable
unitarity or identify the canonical polar partial isometry. Uncompiled source. -/
noncomputable section
open scoped BigOperators Matrix
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def sourceClock (d : ℕ) [NeZero d] : Mat (Ix d) := Matrix.diagonal chi

def sourceTriangular (n : ℕ) : ℕ := n*(n+1)/2

theorem sourceTriangular_double (n : ℕ) : 2*sourceTriangular n=n*(n+1) := by
  unfold sourceTriangular
  have he : 2 ∣ n*(n+1) := by
    rcases Nat.even_or_odd n with ⟨k,hk⟩ | ⟨k,hk⟩
    · refine ⟨k*(n+1),?_⟩
      rw [hk]
      ring
    · refine ⟨n*(k+1),?_⟩
      rw [hk]
      ring
  simpa [mul_comm] using Nat.div_mul_cancel he

def sourceCoeffBase (k : Ix d) : ℂ :=
  ((-1 : ℂ)^k.val * chi (sourceTriangular k.val : Ix d)) /
    ((d : ℂ)*(Real.sin (Real.pi*((k.val : ℝ)+1/2)/(d : ℝ)) : ℂ))

def sourceCoeff (y k : Ix d) : ℂ := sourceCoeffBase k * chi (-(y*(k+1)))

def sourceMode (k : Ix d) : Mat (Ix d) :=
  cyclicShift d^(k.val+1) * sourceClock d^k.val

def sourceBob (y : Ix d) : Mat (Ix d) := ∑ k,sourceCoeff y k • sourceMode k

/-- The natural exponent is really the integer k(k+1)/2. -/
theorem source_triangular_phase (k : Ix d) :
    chi (sourceTriangular k.val : Ix d)=
      cis (Real.pi*(k.val : ℝ)*((k.val : ℝ)+1)/(d : ℝ)) := by
  have hc : chi (sourceTriangular k.val : Ix d)=
      cis (2*Real.pi*(sourceTriangular k.val : ℝ)/(d : ℝ)) := by
    simpa only [Int.cast_natCast] using chi_cis_int (d := d) (sourceTriangular k.val : ℤ)
  rw [hc]
  congr 1
  have h : (2 : ℝ)*sourceTriangular k.val=(k.val : ℝ)*((k.val : ℝ)+1) := by
    exact_mod_cast sourceTriangular_double k.val
  push_cast
  calc
    2*Real.pi*(sourceTriangular k.val : ℝ)/(d : ℝ)=
        Real.pi*(2*(sourceTriangular k.val : ℝ))/(d : ℝ) := by ring
    _ = Real.pi*(k.val : ℝ)*((k.val : ℝ)+1)/(d : ℝ) := by rw [h]; ring

theorem sourceCoeff_literal (y k : Ix d) :
    sourceCoeff y k =
      ((-1 : ℂ)^k.val * chi (sourceTriangular k.val : Ix d)*chi (-(y*(k+1)))) /
        ((d : ℂ)*(Real.sin (Real.pi*((k.val : ℝ)+1/2)/(d : ℝ)) : ℂ)) := by
  unfold sourceCoeff sourceCoeffBase
  ring

/-- Every source denominator is physically nonzero, including d=1 as algebra. -/
theorem source_sine_positive (k : Ix d) :
    0<Real.sin (Real.pi*((k.val : ℝ)+1/2)/(d : ℝ)) := by
  have hd := dimension_pos (d := d)
  have hk : (k.val : ℝ)+1≤(d : ℝ) := by
    exact_mod_cast Nat.succ_le_of_lt (ZMod.val_lt k)
  have hk' : (k.val : ℝ)+1/2<(d : ℝ) := by linarith
  apply Real.sin_pos_of_pos_of_lt_pi
  · exact div_pos (mul_pos Real.pi_pos (by positivity)) hd
  · apply (div_lt_iff₀ hd).mpr
    exact mul_lt_mul_of_pos_left hk' Real.pi_pos

theorem sourceCoeffBase_nonzero (k : Ix d) : sourceCoeffBase k≠0 := by
  unfold sourceCoeffBase
  apply div_ne_zero
  · exact mul_ne_zero (pow_ne_zero _ (by norm_num)) (chi_ne_zero _)
  · apply mul_ne_zero
    · exact_mod_cast (NeZero.ne d)
    · exact_mod_cast ne_of_gt (source_sine_positive k)

/-- Full coefficient DFT, for any output dimension, including composite d. -/
theorem source_coefficient_DFT (m k : Ix d) :
    (∑ y,chi (m*y)*sourceCoeff y k)=
      if k=m-1 then (d : ℂ)*sourceCoeffBase k else 0 := by
  have he (y : Ix d) : chi (m*y)*sourceCoeff y k=
      sourceCoeffBase k*chi ((m-(k+1))*y) := by
    unfold sourceCoeff
    calc
      chi (m*y)*(sourceCoeffBase k*chi (-(y*(k+1))))=
          sourceCoeffBase k*(chi (m*y)*chi (-(y*(k+1)))) := by ring
      _ = sourceCoeffBase k*chi ((m-(k+1))*y) := by
        rw [← chi_add]
        congr 2
        ring
  simp_rw [he]
  rw [← Finset.mul_sum,character_sum]
  have hk : m-(k+1)=0 ↔ k=m-1 := by constructor <;> intro h <;> linear_combination h
  simp only [hk]
  split_ifs <;> ring

/-- The source operator DFT retains the source mode's two powers and their order. -/
theorem source_operator_DFT (m : Ix d) :
    (∑ y,chi (m*y) • sourceBob y)=
      ((d : ℂ)*sourceCoeffBase (m-1)) • sourceMode (m-1) := by
  simp only [sourceBob,Finset.smul_sum,smul_smul]
  rw [Finset.sum_comm]
  simp only [← Finset.sum_smul,source_coefficient_DFT,ite_smul,zero_smul]
  simp

theorem sourceCoeffBase_zero :
    sourceCoeffBase (0 : Ix d)=(1 : ℂ)/
      ((d : ℂ)*(Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)) := by
  simp [sourceCoeffBase,sourceTriangular,show Real.pi*((0 : ℝ)+1/2)/d=
    Real.pi/(2*(d : ℝ)) by ring]

theorem source_shift_order : cyclicShift d^d=1 := by
  rw [cyclicShift,weighted_full_power]
  simp

theorem source_clock_power (n : ℕ) : sourceClock d^n=Matrix.diagonal (fun j => chi ((n : Ix d)*j)) := by
  induction n with
  | zero => ext i j; simp [Matrix.diagonal_apply,Matrix.one_apply]
  | succ n ih =>
    rw [pow_succ,ih,sourceClock,Matrix.diagonal_mul_diagonal]
    congr 1
    funext j
    rw [← chi_add]
    congr 1
    push_cast
    ring

theorem source_clock_order : sourceClock d^d=1 := by
  rw [source_clock_power]
  ext i j
  simp [Matrix.diagonal_apply,Matrix.one_apply]

theorem source_clock_last : sourceClock d^(d-1)=(sourceClock d)ᴴ := by
  rw [source_clock_power]
  ext i j
  have h : ((d-1 : ℕ) : Ix d)= -1 := by
    have hn : d-1+1=d := Nat.sub_add_cancel (Nat.one_le_iff_ne_zero.mpr (NeZero.ne d))
    have hc := congrArg (fun n : ℕ => (n : Ix d)) hn
    push_cast at hc
    linear_combination hc
  simp [sourceClock,h,Matrix.diagonal_apply,Matrix.conjTranspose_apply,chi_star]

theorem sourceMode_zero : sourceMode (0 : Ix d)=cyclicShift d := by simp [sourceMode]

theorem sourceMode_last : sourceMode (-1 : Ix d)=(sourceClock d)ᴴ := by
  have hv : (-1 : Ix d).val=d-1 := ZMod.val_neg_one
  unfold sourceMode
  rw [hv,Nat.sub_add_cancel (Nat.one_le_iff_ne_zero.mpr (NeZero.ne d)),source_shift_order,
    one_mul,source_clock_last]

/-- The last numerator is +1, despite its two parity-dependent factors. -/
theorem sourceCoeffBase_last : sourceCoeffBase (-1 : Ix d)=sourceCoeffBase 0 := by
  have hv : (-1 : Ix d).val=d-1 := ZMod.val_neg_one
  have hdR : (d : ℝ)≠0 := ne_of_gt (dimension_pos (d := d))
  have hcast : ((d-1 : ℕ) : ℝ)=(d : ℝ)-1 := by
    have hc := congrArg (fun n : ℕ => (n : ℝ))
      (Nat.sub_add_cancel (Nat.one_le_iff_ne_zero.mpr (NeZero.ne d)))
    push_cast at hc
    linarith
  have hphase : chi (sourceTriangular (d-1) : Ix d)=(-1 : ℂ)^(d-1) := by
    have ht := source_triangular_phase (d := d) (-1 : Ix d)
    rw [hv] at ht
    rw [ht,show Real.pi*((d-1 : ℕ) : ℝ)*(((d-1 : ℕ) : ℝ)+1)/(d : ℝ)=
      ((d-1 : ℕ) : ℝ)*Real.pi by rw [hcast]; field_simp [hdR]; ring,← cis_pow,cis_pi]
  have hs : Real.sin (Real.pi*(((d-1 : ℕ) : ℝ)+1/2)/(d : ℝ))=
      Real.sin (Real.pi/(2*(d : ℝ))) := by
    rw [show Real.pi*(((d-1 : ℕ) : ℝ)+1/2)/(d : ℝ)=
      Real.pi-Real.pi/(2*(d : ℝ)) by rw [hcast]; field_simp [hdR]; ring,Real.sin_pi_sub]
  rw [sourceCoeffBase, hv,hphase,hs,sourceCoeffBase_zero]
  congr 1
  rw [← mul_pow]
  norm_num

/-- Manuscript eq:source-fourier, first displayed sum. -/
theorem source_fourier_zero :
    (∑ y,sourceBob (d := d) y)=
      ((1 : ℂ)/(Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)) • (sourceClock d)ᴴ := by
  have hdC : (d : ℂ)≠0 := by exact_mod_cast (NeZero.ne d)
  have h := source_operator_DFT (d := d) 0
  simp only [zero_mul,chi_zero,one_smul,zero_sub,sourceMode_last,sourceCoeffBase_last,
    sourceCoeffBase_zero] at h
  rw [h]
  congr 1
  by_cases hs : (Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)=0
  · simp [hs]
  · field_simp [hdC,hs]

/-- Manuscript eq:source-fourier, second displayed sum. -/
theorem source_fourier_one :
    (∑ y,chi y • sourceBob (d := d) y)=
      ((1 : ℂ)/(Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)) • cyclicShift d := by
  have hdC : (d : ℂ)≠0 := by exact_mod_cast (NeZero.ne d)
  have h := source_operator_DFT (d := d) 1
  simp only [one_mul,sub_self,sourceCoeffBase_zero,sourceMode_zero] at h
  rw [h]
  congr 1
  by_cases hs : (Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)=0
  · simp [hs]
  · field_simp [hdC,hs]

/-- Exact qutrit coefficient values, not numerical approximations. -/
theorem source_qutrit_coefficients (y : Ix 3) :
    sourceCoeff y 0=(2 : ℂ)/3*chi (2*y) ∧
    sourceCoeff y 1=-(1 : ℂ)/3*chi (y+1) ∧
    sourceCoeff y 2=(2 : ℂ)/3 := by
  have hsin : Real.sin (Real.pi*((1 : ℝ)+1/2)/3)=1 := by
    rw [show Real.pi*((1 : ℝ)+1/2)/3=Real.pi/2 by ring,Real.sin_pi_div_two]
  have hs0 : Real.sin (Real.pi*((0 : ℝ)+1/2)/3)=1/2 := by
    rw [show Real.pi*((0 : ℝ)+1/2)/3=Real.pi/6 by ring,Real.sin_pi_div_six]
  have hs2 : Real.sin (Real.pi*((2 : ℝ)+1/2)/3)=1/2 := by
    rw [show Real.pi*((2 : ℝ)+1/2)/3=Real.pi-Real.pi/6 by ring,Real.sin_pi_sub,
      Real.sin_pi_div_six]
  have h0 : -(y*(0+1))=2*y := by fin_cases y <;> decide
  have h1 : -(y*(1+1))=y := by fin_cases y <;> decide
  have h2 : -(y*(2+1))=0 := by fin_cases y <;> decide
  refine ⟨?_,?_,?_⟩
  · norm_num [sourceCoeff,sourceCoeffBase,sourceTriangular,hs0,h0]
  · norm_num [sourceCoeff,sourceCoeffBase,sourceTriangular,hsin,h1,chi_add]
    ring
  · norm_num [sourceCoeff,sourceCoeffBase,sourceTriangular,hs2,h2]

/-- Displayed qutrit formula with forward X and positive Z, app:attainment. -/
theorem source_qutrit_operator (y : Ix 3) :
    sourceBob y=(1/3 : ℂ) •
      ((2 : ℂ) • sourceClock 3^2 + (2*chi (2*y)) • cyclicShift 3 -
        chi (y+1) • (cyclicShift 3^2*sourceClock 3)) := by
  obtain ⟨h0,h1,h2⟩ := source_qutrit_coefficients y
  have hsum : sourceBob y=sourceCoeff y 0 • sourceMode 0+
      sourceCoeff y 1 • sourceMode 1+sourceCoeff y 2 • sourceMode 2 := by
    unfold sourceBob
    rw [← sum_representatives]
    norm_num [Finset.sum_range_succ]
  rw [hsum,h0,h1,h2]
  simp only [sourceMode,show (0 : Ix 3).val=0 from rfl,
    show (1 : Ix 3).val=1 from rfl,show (2 : Ix 3).val=2 from rfl]
  norm_num only [pow_zero,pow_one,zero_add,one_add,source_shift_order,mul_one,one_mul]
  ext i j
  simp only [Matrix.smul_apply,Matrix.add_apply,Matrix.sub_apply,smul_eq_mul]
  ring

end CyclicBell.General
