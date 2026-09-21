import Bell.Quantum
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.LinearAlgebra.TensorProduct.Matrix
import Mathlib.LinearAlgebra.Trace

/-! Independent finite-dimensional operator coordinates. No fixed-qubit embedding
occurs in these definitions. The tensor inner product is constructed from source
orthonormal bases, with its pure-tensor formula and basis independence proved. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder TensorProduct InnerProductSpace
namespace Bell.Hilbert

variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]
variable {H K : Type*} [AddCommGroup H] [Module ℂ H] [AddCommGroup K] [Module ℂ K]

/-- The Hermitian form for which the source basis is orthonormal. -/
def basisInner (b : Basis ι ℂ H) (x y : H) : ℂ :=
  dotProduct (star (b.equivFun x)) (b.equivFun y)

@[simp] theorem basisInner_zero_left (b : Basis ι ℂ H) (y : H) :
    basisInner b 0 y = 0 := by simp [basisInner]
@[simp] theorem basisInner_zero_right (b : Basis ι ℂ H) (x : H) :
    basisInner b x 0 = 0 := by simp [basisInner]
@[simp] theorem basisInner_add_left (b : Basis ι ℂ H) (x y z : H) :
    basisInner b (x+y) z = basisInner b x z + basisInner b y z := by
  simp [basisInner, star_add, add_dotProduct]
@[simp] theorem basisInner_add_right (b : Basis ι ℂ H) (x y z : H) :
    basisInner b x (y+z) = basisInner b x y + basisInner b x z := by
  simp [basisInner, dotProduct_add]

/-- Positivity and self-adjointness of an endomorphism, expressed through the
source Hermitian form rather than a target matrix or target embedding. -/
def PositiveFor (inner : H → H → ℂ) (T : H →ₗ[ℂ] H) : Prop :=
  (∀ x y, inner (T x) y = inner x (T y)) ∧ ∀ x, 0 ≤ inner x (T x)

theorem basisMatrix_positive (b : Basis ι ℂ H) (T : H →ₗ[ℂ] H)
    (hT : PositiveFor (basisInner b) T) :
    (LinearMap.toMatrix b b T).PosSemidef := by
  constructor
  · ext i j
    have h := hT.1 (b i) (b j)
    simpa [basisInner, Basis.equivFun_apply, dotProduct, LinearMap.toMatrix_apply,
      Matrix.conjTranspose_apply, Finsupp.single_apply, apply_ite] using h
  · intro x
    have h := hT.2 (b.equivFun.symm x)
    have he : (b.repr (b.equivFun.symm x) : ι → ℂ) = x := by
      exact b.equivFun.apply_symm_apply x
    have ht := T.toMatrix_mulVec_repr b b (b.equivFun.symm x)
    rw [he] at ht
    simpa only [basisInner, LinearEquiv.apply_symm_apply, Basis.equivFun_apply, ← ht] using h

theorem basisMatrix_positive_iff (b : Basis ι ℂ H) (T : H →ₗ[ℂ] H) :
    (LinearMap.toMatrix b b T).PosSemidef ↔ PositiveFor (basisInner b) T := by
  refine ⟨?_, basisMatrix_positive b T⟩
  intro hT
  constructor
  · intro x y
    simp only [basisInner, Basis.equivFun_apply,
      ← LinearMap.toMatrix_mulVec_repr b b T]
    rw [Matrix.star_mulVec, ← Matrix.dotProduct_mulVec, hT.1]
  · intro x
    simpa only [basisInner, Basis.equivFun_apply,
      ← LinearMap.toMatrix_mulVec_repr b b T] using hT.2 (b.repr x)

theorem basisInner_self_nonneg (b : Basis ι ℂ H) (x : H) :
    0 ≤ basisInner b x x := dotProduct_star_self_nonneg _

theorem basisInner_self_eq_zero_iff (b : Basis ι ℂ H) (x : H) :
    basisInner b x x = 0 ↔ x = 0 := by
  rw [basisInner, dotProduct_star_self_eq_zero]
  exact b.equivFun.map_eq_zero_iff

@[simp] theorem basisInner_smul_left (b : Basis ι ℂ H) (a : ℂ) (x y : H) :
    basisInner b (a • x) y = star a * basisInner b x y := by
  simp [basisInner, star_smul, smul_dotProduct, smul_eq_mul]
@[simp] theorem basisInner_smul_right (b : Basis ι ℂ H) (a : ℂ) (x y : H) :
    basisInner b x (a • y) = a * basisInner b x y := by
  simp [basisInner, dotProduct_smul, smul_eq_mul]

theorem basisInner_conj_symm (b : Basis ι ℂ H) (x y : H) :
    star (basisInner b x y) = basisInner b y x := by
  simp [basisInner, dotProduct, star_sum, star_mul, Pi.star_apply]

section InnerProduct
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]

theorem orthonormal_basisInner (b : OrthonormalBasis ι ℂ E) (x y : E) :
    basisInner b.toBasis x y = ⟪x, y⟫_ℂ := by
  rw [← b.repr.inner_map_map x y]
  simp only [basisInner, Basis.equivFun_apply, OrthonormalBasis.coe_toBasis_repr,
    EuclideanSpace.inner_eq_star_dotProduct]
  exact dotProduct_comm _ _

/-- The canonical Hilbert tensor-product inner product in source coordinates. -/
def tensorInner (b : OrthonormalBasis ι ℂ E) (c : OrthonormalBasis κ ℂ F)
    (x y : E ⊗[ℂ] F) : ℂ := basisInner (b.toBasis.tensorProduct c.toBasis) x y

theorem tensorInner_tmul (b : OrthonormalBasis ι ℂ E) (c : OrthonormalBasis κ ℂ F)
    (x x' : E) (y y' : F) :
    tensorInner b c (x ⊗ₜ[ℂ] y) (x' ⊗ₜ[ℂ] y') =
      ⟪x, x'⟫_ℂ * ⟪y, y'⟫_ℂ := by
  rw [← orthonormal_basisInner b x x', ← orthonormal_basisInner c y y']
  simp only [tensorInner, basisInner, Basis.equivFun_apply, dotProduct,
    Fintype.sum_prod_type, Basis.tensorProduct_repr_tmul_apply, smul_eq_mul,
    Pi.star_apply, star_mul, Finset.sum_mul, Finset.mul_sum]
  conv_rhs => rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- The tensor Hermitian form is independent of the chosen source ONBs. -/
theorem tensorInner_basis_independent
    {ι' κ' : Type*} [Fintype ι'] [Fintype κ'] [DecidableEq ι'] [DecidableEq κ']
    (b : OrthonormalBasis ι ℂ E) (c : OrthonormalBasis κ ℂ F)
    (b' : OrthonormalBasis ι' ℂ E) (c' : OrthonormalBasis κ' ℂ F)
    (x y : E ⊗[ℂ] F) : tensorInner b c x y = tensorInner b' c' x y := by
  induction x using TensorProduct.induction_on with
  | zero => simp [tensorInner]
  | tmul x₁ x₂ =>
    induction y using TensorProduct.induction_on with
    | zero => simp [tensorInner]
    | tmul y₁ y₂ => rw [tensorInner_tmul, tensorInner_tmul]
    | add y₁ y₂ h₁ h₂ => simpa only [tensorInner, basisInner_add_right] using congrArg₂ (· + ·) h₁ h₂
  | add x₁ x₂ h₁ h₂ => simpa only [tensorInner, basisInner_add_left] using congrArg₂ (· + ·) h₁ h₂

/-- Positivity of a local physical operator uses the given Hilbert inner product. -/
def PositiveOperator (T : E →ₗ[ℂ] E) : Prop := PositiveFor (fun x y : E => ⟪x, y⟫_ℂ) T

theorem operatorMatrix_positive (b : OrthonormalBasis ι ℂ E) (T : E →ₗ[ℂ] E)
    (hT : PositiveOperator T) : (LinearMap.toMatrix b.toBasis b.toBasis T).PosSemidef := by
  apply basisMatrix_positive
  simpa only [PositiveFor, orthonormal_basisInner] using hT

end InnerProduct
end Bell.Hilbert
