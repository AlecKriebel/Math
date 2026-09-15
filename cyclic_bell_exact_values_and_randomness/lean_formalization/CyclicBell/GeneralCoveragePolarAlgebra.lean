import Mathlib

/-!
Kernel-checked algebraic infrastructure for the literal source/polar bridge.

`weyl_mul_pow` keeps the scalar Weyl phase in every power; omitting that phase
would change the manuscript's triangular source coefficient. The polar lemmas
derive the residual factor identities from a square-root and a supported
isometry equation. They do not claim that a canonical polar decomposition has
already been constructed in an arbitrary Hilbert space.
-/

noncomputable section
open scoped BigOperators

namespace CyclicBell.General.Coverage

variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- Sum of the exponents accumulated when moving a Weyl pair past itself. -/
def triangular : ℕ → ℕ
  | 0 => 0
  | n + 1 => triangular n + n

@[simp] theorem triangular_zero : triangular 0 = 0 := rfl
@[simp] theorem triangular_succ (n : ℕ) : triangular (n + 1) = triangular n + n := rfl

theorem triangular_double_succ (n : ℕ) : 2 * triangular (n + 1) = n * (n + 1) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [triangular_succ (n + 1), Nat.mul_add, ih]
    ring

/-- The manuscript's integer triangular exponent is not division in ZMod d. -/
theorem triangular_succ_eq (n : ℕ) : triangular (n + 1) = n * (n + 1) / 2 := by
  have h := triangular_double_succ n
  omega

/-- Moving a whole power through the second member of a Weyl pair. -/
theorem weyl_pow_commute (X Z : A) (q : ℂ)
    (hZX : Z * X = q • (X * Z)) (n : ℕ) :
    Z ^ n * X = q ^ n • (X * Z ^ n) := by
  induction n with
  | zero => simp
  | succ n ih =>
    calc
      Z ^ (n + 1) * X = Z * (Z ^ n * X) := by rw [pow_succ', mul_assoc]
      _ = Z * (q ^ n • (X * Z ^ n)) := by rw [ih]
      _ = q ^ n • ((Z * X) * Z ^ n) := by
        rw [mul_smul_comm, mul_assoc]
      _ = q ^ n • ((q • (X * Z)) * Z ^ n) := by rw [hZX]
      _ = q ^ (n + 1) • (X * Z ^ (n + 1)) := by
        rw [smul_mul_assoc, smul_smul, pow_succ, pow_succ']
        simp only [mul_assoc]

theorem weyl_commute_pow (X Z : A) (q : ℂ)
    (hXZ : X * Z = q • (Z * X)) (n : ℕ) :
    X * Z ^ n = q ^ n • (Z ^ n * X) := by
  induction n with
  | zero => simp
  | succ n ih =>
    calc
      X * Z ^ (n + 1) = (X * Z ^ n) * Z := by rw [pow_succ,mul_assoc]
      _ = (q ^ n • (Z ^ n * X)) * Z := by rw [ih]
      _ = q ^ n • (Z ^ n * (X * Z)) := by rw [smul_mul_assoc,mul_assoc]
      _ = q ^ n • (Z ^ n * (q • (Z * X))) := by rw [hXZ]
      _ = q ^ (n + 1) • (Z ^ (n + 1) * X) := by
        rw [mul_smul_comm,smul_smul,pow_succ,pow_succ,mul_assoc]

/-- Exact noncommutative Weyl power formula, including its triangular phase. -/
theorem weyl_mul_pow (X Z : A) (q : ℂ)
    (hZX : Z * X = q • (X * Z)) (n : ℕ) :
    (X * Z) ^ n = q ^ triangular n • (X ^ n * Z ^ n) := by
  induction n with
  | zero => simp
  | succ n ih =>
    calc
      (X * Z) ^ (n + 1) = (q ^ triangular n • (X ^ n * Z ^ n)) * (X * Z) := by
        rw [pow_succ, ih]
      _ = q ^ triangular n • (X ^ n * (Z ^ n * X) * Z) := by
        rw [smul_mul_assoc]
        simp only [mul_assoc]
      _ = q ^ triangular n • (X ^ n * (q ^ n • (X * Z ^ n)) * Z) := by
        rw [weyl_pow_commute X Z q hZX n]
      _ = q ^ triangular (n + 1) • (X ^ (n + 1) * Z ^ (n + 1)) := by
        rw [mul_smul_comm, smul_mul_assoc, smul_smul, triangular_succ, pow_add]
        simp only [pow_succ, mul_assoc]

section Polar

omit [Algebra ℂ A]

variable [StarRing A]

/-- The transported left square root used in the polar residual. -/
def transportedRoot (V H : A) : A := V * H * star V

theorem transportedRoot_star (V H : A) (hH : star H = H) :
    star (transportedRoot V H) = transportedRoot V H := by
  simp [transportedRoot, star_mul, hH, mul_assoc]

/-- The support equation is enough: no inverse of H is used. -/
theorem transportedRoot_square (V H : A) (hVH : (star V * V) * H = H) :
    transportedRoot V H * transportedRoot V H = V * (H * H) * star V := by
  calc
    _ = V * H * ((star V * V) * H) * star V := by
      simp [transportedRoot, mul_assoc]
    _ = _ := by rw [hVH]; simp only [mul_assoc]

theorem supportedPolarFactor_square (V H : A) (hH : star H = H)
    (hVH : (star V * V) * H = H) : star (V * H) * (V * H) = H * H := by
  calc
    _ = H * ((star V * V) * H) := by simp [star_mul, hH, mul_assoc]
    _ = _ := by rw [hVH]

theorem supportedPolarFactor_cross (V H : A)
    (hVH : (star V * V) * H = H) : transportedRoot V H * (V * H) = V * (H * H) := by
  calc
    _ = V * H * ((star V * V) * H) := by simp [transportedRoot, mul_assoc]
    _ = _ := by rw [hVH]; simp only [mul_assoc]

/-- Algebra in manuscript `lem:polar`, after square-root/support identification.
The hypotheses are decomposition/support identities, not the desired gap.
This lemma is not a substitute for the missing analytic polar construction. -/
theorem supportedPolarResidual_square (V H B : A) (hH : star H = H)
    (hVH : (star V * V) * H = H) (hB : star B * B = 1)
    (hcomm : (H * H) * B = B * (H * H)) :
    let C := V * (H * H)
    let P := transportedRoot V H - (V * H) * B
    star P * P = V * (H * H) * star V + H * H - (C * B + star (C * B)) := by
  dsimp only
  have hcross := supportedPolarFactor_cross V H hVH
  have hcross' : star (V * H) * transportedRoot V H = star (V * (H * H)) := by
    simpa only [star_mul, transportedRoot_star V H hH] using congrArg star hcross
  have hdiag : star B * (H * H) * B = H * H := by
    rw [mul_assoc, hcomm, ← mul_assoc, hB, one_mul]
  calc
    _ = star (transportedRoot V H) * transportedRoot V H -
        star (transportedRoot V H) * (V * H) * B -
        star B * (star (V * H) * transportedRoot V H) +
        star B * (star (V * H) * (V * H)) * B := by
      simp only [star_sub, star_mul]
      noncomm_ring
    _ = _ := by
      rw [transportedRoot_star V H hH, transportedRoot_square V H hVH,
        hcross, hcross', supportedPolarFactor_square V H hH hVH, hdiag]
      simp only [star_mul]
      noncomm_ring

end Polar

end CyclicBell.General.Coverage
