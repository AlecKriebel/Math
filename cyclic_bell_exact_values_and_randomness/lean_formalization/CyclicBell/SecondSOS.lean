import CyclicBell.Fourier4
import CyclicBell.ScalarData

/-!
The actual d=4 second-family SOS, including the coefficient and normalization
bridge. This is the source's 1/(2d) identity, not the new first-family SOS.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.SecondSOS
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
set_option maxRecDepth 20000
set_option maxHeartbeats 12000000

def reducedOperator (lam : Fin 4 → ℂ) (A B : Fin 4 → Mat ι) : Mat ι :=
  ∑ l : Fin 4, herm (star (lam l) • (A l * fourier4 B l))

def residual (lam : Fin 4 → ℂ) (A B : Fin 4 → Mat ι) (l : Fin 4) : Mat ι :=
  (4 * lam l) • 1 - A l * fourier4 B l

def squareSum (lam : Fin 4 → ℂ) (A B : Fin 4 → Mat ι) : Mat ι :=
  ∑ l : Fin 4, (residual lam A B l).conjTranspose * residual lam A B l

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

/-- No commutation of distinct Alice or Bob observables is used. -/
theorem reduced_gap_identity (lam : Fin 4 → ℂ)
    (hLam : (∑ l : Fin 4, star (lam l) * lam l) = 1)
    (A B : Fin 4 → Mat ι) (hA : ∀ l, UnitaryRel (A l))
    (hB : ∀ y, UnitaryRel (B y)) :
    (4 : ℂ) • (1 : Mat ι) - reducedOperator lam A B =
      (1 / 8 : ℂ) • squareSum lam A B := by
  have henergy (l : Fin 4) :
      (A l * fourier4 B l).conjTranspose * (A l * fourier4 B l) =
        (fourier4 B l).conjTranspose * fourier4 B l := by
    rw [Matrix.conjTranspose_mul]
    simp only [mul_assoc, (hA l).cancel_left]
  have hs : squareSum lam A B =
      (32 : ℂ) • (1 : Mat ι) - (8 : ℂ) • reducedOperator lam A B := by
    unfold squareSum residual
    simp_rw [scalar_gap_expansion, henergy]
    rw [Finset.sum_sub_distrib, Finset.sum_add_distrib,
      ← Finset.sum_smul, ← Finset.mul_sum, hLam, mul_one,
      fourier4_unitary_energy B hB, ← Finset.smul_sum]
    unfold reducedOperator herm
    simp only [Finset.smul_sum, smul_add, smul_smul]
    apply Matrix.ext
    intro i j
    simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul,
      Matrix.sum_apply, Finset.sum_apply]
    ring
  rw [hs]
  apply Matrix.ext
  intro i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

/-- The whole augmented operator gap is an explicit sum of positive squares. -/
theorem augmented_gap_identity (lam : Fin 4 → ℂ)
    (hLam : (∑ l : Fin 4, star (lam l) * lam l) = 1)
    (A B : Fin 4 → Mat ι) (Bstar : Mat ι)
    (hA : ∀ l, UnitaryRel (A l)) (hB : ∀ y, UnitaryRel (B y))
    (hstar : UnitaryRel Bstar) :
    (5 : ℂ) • (1 : Mat ι) -
      (reducedOperator lam A B + herm (A 0 * Bstar)) =
      (1 / 8 : ℂ) • squareSum lam A B +
      (1 / 2 : ℂ) • ((1 - A 0 * Bstar).conjTranspose * (1 - A 0 * Bstar)) := by
  rw [← reduced_gap_identity lam hLam A B hA hB,
    ← aligned_gap_identity ((hA 0).mul hstar)]
  apply Matrix.ext
  intro i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

theorem reduced_upper {ρ : Mat ι} (hρ : ρ.PosSemidef)
    (htrace : Matrix.trace ρ = 1) (lam : Fin 4 → ℂ)
    (hLam : (∑ l : Fin 4, star (lam l) * lam l) = 1)
    (A B : Fin 4 → Mat ι) (hA : ∀ l, UnitaryRel (A l))
    (hB : ∀ y, UnitaryRel (B y)) :
    stateEval ρ (reducedOperator lam A B) ≤ 4 := by
  have hn : 0 ≤ stateEval ρ (squareSum lam A B) := by
    unfold squareSum
    rw [stateEval_sum]
    exact Finset.sum_nonneg (fun l _ => stateEval_square_nonnegative hρ _)
  have he := congrArg (stateEval ρ) (reduced_gap_identity lam hLam A B hA hB)
  have hfour : (4 : ℂ) = ((4 : ℝ) : ℂ) := by norm_num
  have heighth : (1 / 8 : ℂ) = ((1 / 8 : ℝ) : ℂ) := by norm_num
  rw [stateEval_sub, hfour, stateEval_real_smul, stateEval_one htrace,
    heighth, stateEval_real_smul] at he
  nlinarith

theorem augmented_upper {ρ : Mat ι} (hρ : ρ.PosSemidef)
    (htrace : Matrix.trace ρ = 1) (lam : Fin 4 → ℂ)
    (hLam : (∑ l : Fin 4, star (lam l) * lam l) = 1)
    (A B : Fin 4 → Mat ι) (Bstar : Mat ι)
    (hA : ∀ l, UnitaryRel (A l)) (hB : ∀ y, UnitaryRel (B y))
    (hstar : UnitaryRel Bstar) :
    stateEval ρ (reducedOperator lam A B) + stateEval ρ (A 0 * Bstar) ≤ 5 := by
  have hr := reduced_upper hρ htrace lam hLam A B hA hB
  have ha := aligned_upper hρ htrace ((hA 0).mul hstar)
  linarith

/-- Instantiation of the actual source coefficients; no normalization hypothesis
is left to the caller in the physical endpoint. -/
theorem source_reduced_gap (A B : Fin 4 → Mat ι)
    (hA : ∀ l, UnitaryRel (A l)) (hB : ∀ y, UnitaryRel (B y)) :
    (4 : ℂ) • (1 : Mat ι) - reducedOperator sourceLambda A B =
      (1 / 8 : ℂ) • squareSum sourceLambda A B := by
  apply reduced_gap_identity _ _ A B hA hB
  simp only [D4.sourceLambda_eq]
  exact D4.lambda_normalization

end CyclicBell.SecondSOS
