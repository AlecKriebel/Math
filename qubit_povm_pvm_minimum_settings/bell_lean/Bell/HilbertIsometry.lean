import Bell.IsometricCompression
import Mathlib.Analysis.InnerProductSpace.PiL2

/-! An actual complex linear isometry from an arbitrary Hilbert space with an
orthonormal basis of size at most two into the fixed two-dimensional Hilbert
space. Its coordinates agree with the rectangular matrix embedding. -/
noncomputable section
open scoped Matrix InnerProductSpace
namespace Bell.Hilbert

variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]

theorem matrix_inner_preservation (V : Matrix m n ℂ)
    (hV : V.conjTranspose * V = 1)
    (x y : EuclideanSpace ℂ n) :
    ⟪Matrix.toEuclideanLin V x, Matrix.toEuclideanLin V y⟫_ℂ = ⟪x, y⟫_ℂ := by
  simp only [EuclideanSpace.inner_eq_star_dotProduct,
    Matrix.piLp_equiv_toEuclideanLin_apply]
  rw [dotProduct_comm (V *ᵥ _), Matrix.star_mulVec, ← Matrix.dotProduct_mulVec,
    Matrix.mulVec_mulVec, hV, Matrix.one_mulVec, dotProduct_comm]

def matrixLinearIsometry (V : Matrix m n ℂ) (hV : V.conjTranspose * V = 1) :
    EuclideanSpace ℂ n →ₗᵢ[ℂ] EuclideanSpace ℂ m :=
  (Matrix.toEuclideanLin V).isometryOfInner (matrix_inner_preservation V hV)

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
variable {d : ℕ}

/-- The promised local Hilbert-space embedding, with no hypothesis restricting
vectors or states to real coordinates. -/
def linearIsometry (b : OrthonormalBasis (Fin d) ℂ E) (hd : d ≤ 2) :
    E →ₗᵢ[ℂ] EuclideanSpace ℂ (Fin 2) :=
  (matrixLinearIsometry (IsometricCompression.canonicalEmbedding hd)
    (IsometricCompression.canonicalEmbedding_isometry hd)).comp b.repr.toLinearIsometry

@[simp]
theorem linearIsometry_apply (b : OrthonormalBasis (Fin d) ℂ E) (hd : d ≤ 2) (x : E) :
    linearIsometry b hd x = (WithLp.equiv 2 (Fin 2 → ℂ)).symm
      (IsometricCompression.canonicalEmbedding hd *ᵥ (b.repr x : Fin d → ℂ)) := rfl

@[simp]
theorem linearIsometry_coordinate (b : OrthonormalBasis (Fin d) ℂ E) (hd : d ≤ 2)
    (x : E) (i : Fin 2) :
    linearIsometry b hd x i =
      (IsometricCompression.canonicalEmbedding hd *ᵥ (b.repr x : Fin d → ℂ)) i := rfl

theorem linearIsometry_inner (b : OrthonormalBasis (Fin d) ℂ E) (hd : d ≤ 2) (x y : E) :
    ⟪linearIsometry b hd x, linearIsometry b hd y⟫_ℂ = ⟪x, y⟫_ℂ :=
  (linearIsometry b hd).inner_map_map x y

theorem linearIsometry_norm (b : OrthonormalBasis (Fin d) ℂ E) (hd : d ≤ 2) (x : E) :
    ‖linearIsometry b hd x‖ = ‖x‖ := (linearIsometry b hd).norm_map x

theorem linearIsometry_injective (b : OrthonormalBasis (Fin d) ℂ E) (hd : d ≤ 2) :
    Function.Injective (linearIsometry b hd) := (linearIsometry b hd).injective

end Bell.Hilbert
