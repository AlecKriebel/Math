import CyclicBell.GeneralCoverageSourcePolar

/-! Literal source coefficient / relative-unitary polynomial bridge.
Manuscript app:attainment; the transpose, triangular exponent and sign are
derived from the actual positive clock and forward shift. -/

noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem source_clock_transpose : (sourceClock d)ᵀ = sourceClock d := by
  simp only [sourceClock,Matrix.diagonal_transpose]

theorem source_shift_adjoint : (cyclicShift d)ᴴ = (cyclicShift d)ᵀ := by
  ext i j
  simp [Matrix.conjTranspose_apply,Matrix.transpose_apply,cyclicShift,weightedCycle]

theorem source_inverse_shift_clock :
    (cyclicShift d)ᵀ * sourceClock d =
      chi (1 : Ix d) • (sourceClock d * (cyclicShift d)ᵀ) := by
  have h := congrArg Matrix.transpose (source_clock_shift (d := d))
  simpa only [Matrix.transpose_mul,Matrix.transpose_smul,source_clock_transpose] using h

theorem source_relative_adjoint (y : Ix d) :
    (sourceRelative y)ᴴ = chi (-y) • ((cyclicShift d)ᵀ * sourceClock d) := by
  simp only [sourceRelative,Matrix.conjTranspose_smul,Matrix.conjTranspose_mul,
    Matrix.conjTranspose_conjTranspose,source_shift_adjoint,chi_star]

theorem source_relative_adjoint_power_clock (y : Ix d) (n : ℕ) :
    ((sourceRelative y)ᴴ)^(n+1) * (sourceClock d)ᴴ =
      chi (-y*((n+1 : ℕ) : Ix d)+(Coverage.triangular (n+1) : Ix d)) •
        ((sourceClock d)^n * ((cyclicShift d)ᵀ)^(n+1)) := by
  let Z := sourceClock d
  let X := (cyclicShift d)ᵀ
  have hZX : Z*Zᴴ=1 := source_clock_unitary.2
  have hXZ : X*Z=chi (1 : Ix d) • (Z*X) := source_inverse_shift_clock
  induction n with
  | zero =>
    simp only [zero_add,pow_one,pow_zero,one_mul,Coverage.triangular_succ,
      Coverage.triangular_zero,Nat.cast_zero,Nat.cast_one,add_zero,mul_one]
    rw [source_relative_adjoint,smul_mul_assoc,mul_assoc,source_clock_unitary.2,mul_one]
  | succ n ih =>
    let c : Ix d := -y*((n+1 : ℕ) : Ix d)+(Coverage.triangular (n+1) : Ix d)
    have hm := Coverage.weyl_commute_pow X Z (chi (1 : Ix d)) hXZ (n+1)
    have he : chi (-y)*chi c*chi (1 : Ix d)^(n+1) =
        chi (-y*((n+1+1 : ℕ) : Ix d)+(Coverage.triangular (n+1+1) : Ix d)) := by
      rw [chi_pow,mul_one,←chi_add,←chi_add]
      congr 1
      dsimp [c]
      push_cast
      ring
    change ((sourceRelative y)ᴴ)^(n+1+1)*Zᴴ = _
    calc
      _ = (sourceRelative y)ᴴ * (chi c • (Z^n*X^(n+1))) := by
        rw [pow_succ',mul_assoc,ih]
      _ = (chi (-y)*chi c) • (X*Z^(n+1)*X^(n+1)) := by
        rw [source_relative_adjoint,smul_mul_assoc,mul_smul_comm,smul_smul]
        simp only [Z,X,pow_succ',mul_assoc]
      _ = (chi (-y)*chi c*chi (1 : Ix d)^(n+1)) • (Z^(n+1)*X^(n+1+1)) := by
        rw [hm,smul_mul_assoc,smul_smul]
        simp only [pow_succ',mul_assoc]
      _ = _ := by rw [he]

def sourceCosecantCoefficient (k : Ix d) : ℂ :=
  (-1 : ℂ)^k.val / ((d : ℂ)*(Real.sin (Real.pi*((k.val : ℝ)+1/2)/d) : ℂ))

theorem sourceCoeff_weyl_phase (y k : Ix d) :
    sourceCoeff y k = sourceCosecantCoefficient k *
      chi (-y*((k.val+1 : ℕ) : Ix d)+(Coverage.triangular (k.val+1) : Ix d)) := by
  rw [Coverage.triangular_succ_eq]
  simp only [Nat.cast_add,Nat.cast_one,ZMod.natCast_zmod_val,chi_add]
  unfold sourceCoeff sourceCoeffBase sourceCosecantCoefficient sourceTriangular
  simp only [neg_mul]
  ring

theorem sourceMode_transpose (k : Ix d) :
    (sourceMode k)ᵀ = (sourceClock d)^k.val * ((cyclicShift d)ᵀ)^(k.val+1) := by
  simp only [sourceMode,Matrix.transpose_mul,Matrix.transpose_pow,source_clock_transpose]

/-- Exact polynomial identity for the actual source matrix, before assuming or
proving that the resulting matrix is a valid measurement observable. -/
theorem sourceBob_transpose_polynomial (y : Ix d) :
    (sourceBob y)ᵀ =
      (∑ k : Ix d,sourceCosecantCoefficient k • ((sourceRelative y)ᴴ)^(k.val+1)) *
        (sourceClock d)ᴴ := by
  simp only [sourceBob,Matrix.transpose_sum,Matrix.transpose_smul,Finset.sum_mul,
    smul_mul_assoc,source_relative_adjoint_power_clock,smul_smul]
  apply Finset.sum_congr rfl
  intro k _
  rw [sourceCoeff_weyl_phase,sourceMode_transpose]

end CyclicBell.General
