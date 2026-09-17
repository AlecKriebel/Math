import CyclicBell.MatrixAlgebra

/-! Complex-valued expectation linearity and tensor trace bridges.
No reality assumption is imposed on a correlator before taking its real part.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell
variable {ι κ : Type*} [Fintype ι] [Fintype κ]

@[simp] theorem expectation_add (ψ : ι → ℂ) (S T : Matrix ι ι ℂ) :
    expectation ψ (S + T) = expectation ψ S + expectation ψ T := by
  simp [expectation, ip, applyOp, add_mul, mul_add, Finset.sum_add_distrib]

@[simp] theorem expectation_smul (ψ : ι → ℂ) (z : ℂ) (T : Matrix ι ι ℂ) :
    expectation ψ (z • T) = z * expectation ψ T := by
  unfold expectation ip applyOp
  simp only [Matrix.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

@[simp] theorem expectation_sum (ψ : ι → ℂ) (T : κ → Matrix ι ι ℂ) :
    expectation ψ (∑ k, T k) = ∑ k, expectation ψ (T k) := by
  unfold expectation ip applyOp
  simp only [Matrix.sum_apply, Finset.sum_apply, Finset.sum_mul, Finset.mul_sum]
  calc
    _ = ∑ i, ∑ k, ∑ j, star (ψ i) * (T k i j * ψ j) := by
      apply Finset.sum_congr rfl
      intro i _
      rw [Finset.sum_comm]
    _ = _ := by rw [Finset.sum_comm]

@[simp] theorem tensor_sum_left {nA nB : ℕ} (A : κ → Op nA) (B : Op nB) :
    tensor (∑ k, A k) B = ∑ k, tensor (A k) B := by
  ext i j
  simp [tensor, Matrix.sum_apply, Finset.sum_mul]

@[simp] theorem tensor_sum_right {nA nB : ℕ} (A : Op nA) (B : κ → Op nB) :
    tensor A (∑ k, B k) = ∑ k, tensor A (B k) := by
  ext i j
  simp [tensor, Matrix.sum_apply, Finset.mul_sum]

/-- Mixed trace on a pure density is exactly the vector expectation. -/
theorem trace_pure_tensor {nA nB : ℕ} (ψ : Joint nA nB → ℂ) (A : Op nA) (B : Op nB) :
    Matrix.trace (projector ψ * tensor A B) = expectation ψ (tensor A B) :=
  (expectation_eq_trace ψ (tensor A B)).symm

/-! The coordinate State/PVM model generates honest Born probabilities. -/

theorem born_nonnegative {nA nB : ℕ} (ρ : State nA nB) (M : PVM nA) (N : PVM nB)
    (a b : Fin 4) : 0 ≤ born ρ.density (M.effect a) (N.effect b) := by
  have hh : (tensor (M.effect a) (N.effect b)).conjTranspose *
      tensor (M.effect a) (N.effect b) = tensor (M.effect a) (N.effect b) := by
    rw [tensor_adjoint, (M.positive a).isHermitian.eq, (N.positive b).isHermitian.eq,
      tensor_mul, M.idempotent, N.idempotent]
  have hp := stateEval_square_nonnegative ρ.positive (tensor (M.effect a) (N.effect b))
  rw [hh] at hp
  exact hp

theorem born_left_marginal {nA nB : ℕ} (ρ : State nA nB) (M : PVM nA) (N : PVM nB)
    (a : Fin 4) : (∑ b : Fin 4, born ρ.density (M.effect a) (N.effect b)) =
      stateEval ρ.density (tensor (M.effect a) 1) := by
  change (∑ b : Fin 4, stateEval ρ.density (tensor (M.effect a) (N.effect b))) = _
  rw [← stateEval_sum, ← tensor_sum_right, N.complete]

theorem born_right_marginal {nA nB : ℕ} (ρ : State nA nB) (M : PVM nA) (N : PVM nB)
    (b : Fin 4) : (∑ a : Fin 4, born ρ.density (M.effect a) (N.effect b)) =
      stateEval ρ.density (tensor 1 (N.effect b)) := by
  change (∑ a : Fin 4, stateEval ρ.density (tensor (M.effect a) (N.effect b))) = _
  rw [← stateEval_sum, ← tensor_sum_left, M.complete]

theorem born_normalized {nA nB : ℕ} (ρ : State nA nB) (M : PVM nA) (N : PVM nB) :
    (∑ a : Fin 4, ∑ b : Fin 4, born ρ.density (M.effect a) (N.effect b)) = 1 := by
  simp only [born_left_marginal]
  rw [← stateEval_sum, ← tensor_sum_left, M.complete, tensor_one, stateEval_one ρ.normalized]

end CyclicBell
