import CyclicBell.MatrixAlgebra
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
theorem scalar_gap_expansion (lam : ℂ) (C : Mat ι) :
    ((4 * lam) • (1 : Mat ι) - C).conjTranspose * ((4 * lam) • 1 - C) =
      (16 * (star lam * lam)) • 1 + C.conjTranspose * C -
        (4 : ℂ) • ((star lam) • C + ((star lam) • C).conjTranspose) := by
  simp only [Matrix.conjTranspose_sub, Matrix.conjTranspose_smul,
    Matrix.conjTranspose_one, sub_mul, mul_sub, smul_mul_assoc, mul_smul_comm,
    smul_smul, one_mul, mul_one, star_mul, star_star, star_ofNat]
  apply Matrix.ext
  intro i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

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


end CyclicBell
