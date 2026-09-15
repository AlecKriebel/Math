import CyclicBell.ScalarData

/-!
SOURCE CANDIDATE, NOT YET COMPILED.
Target-only d=4 realization. No universal Bell bound or Bell maximality is
assumed or proved in this module. The exponential-phase bridge is written in Phases.lean; all sources remain uncompiled.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.D4

set_option maxRecDepth 10000
set_option maxHeartbeats 8000000

attribute [local simp] Matrix.cons_val_two Matrix.cons_val_three

abbrev Q := Fin 4

def q : Q → ℂ := ![1, (h : ℂ) + h * Complex.I, -1, -(h : ℂ) + h * Complex.I]

/-- Rows and columns both range over 0,1,2,3; F(j,a)=i^(-a*j). -/
def fourier : Matrix Q Q ℂ :=
  !![1, 1, 1, 1;
     1, -Complex.I, -1, Complex.I;
     1, -1, 1, -1;
     1, Complex.I, -1, -Complex.I]

def u (a : Q) : Vec 4 := fun j => fourier j a / 2
def v (a : Q) : Vec 4 := fun j => q j * u a j

/-- Phi4 has amplitude 1/2 on four diagonal coordinates. -/
def phi : Joint 4 4 → ℂ := fun i => if i.1 = i.2 then 1 / 2 else 0

def aliceEffect (a : Q) : Op 4 := projector (v a)
def bobEffect (b : Q) : Op 4 := projector (u b)

def targetBorn (a b : Q) : ℝ := pureBorn phi (aliceEffect a) (bobEffect b)

/-- Proposed closed form, kept independent of the Born-rule definition. -/
def table (a b : Q) : ℝ := if (a.val + b.val) % 2 = 0 then 1 / 32 else 3 / 32

/-- X|j>=|j+1 mod 4>, with rows as output coordinates. -/
def shift : Op 4 := !![0, 0, 0, 1; 1, 0, 0, 0; 0, 1, 0, 0; 0, 0, 1, 0]

/-- Algebraic form of (zeta^2,zeta^6,zeta^14,zeta^10). -/
def swappedWeights : Q → ℂ :=
  ![(h : ℂ) + h * Complex.I, -(h : ℂ) + h * Complex.I,
    (h : ℂ) - h * Complex.I, -(h : ℂ) - h * Complex.I]

def swappedObservable : Op 4 := shift * Matrix.diagonal swappedWeights

/-- The literal final-two transposition on the four phase labels. -/
def kappa : Equiv.Perm Q := Equiv.swap 2 3

def equalityRoots : Q → ℂ :=
  ![(h : ℂ) + h * Complex.I, -(h : ℂ) + h * Complex.I,
    -(h : ℂ) - h * Complex.I, (h : ℂ) - h * Complex.I]

theorem kappa_values : ∀ j : Q, kappa j = (![0, 1, 3, 2] : Q → Q) j := by
  decide

theorem weights_are_final_swap (j : Q) : swappedWeights j = equalityRoots (kappa j) := by
  rw [kappa_values j]
  fin_cases j <;> rfl

theorem q_recurrence (j : Q) : q (j + 1) = swappedWeights j * q j := by
  fin_cases j <;> apply Complex.ext <;>
    norm_num [q, swappedWeights, Fin.add_def, Complex.mul_re, Complex.mul_im] <;> nlinarith [h_sq]

theorem q_unit_modulus (j : Q) : Complex.normSq (q j) = 1 := by
  fin_cases j <;>
    norm_num [q, Complex.normSq_apply, Complex.mul_re, Complex.mul_im] <;> nlinarith [h_sq]

/-- No state-normalization hypothesis is supplied: it is computed. -/
theorem phi_normalized : ip phi phi = 1 := by
  apply Complex.ext <;> norm_num [ip, phi, Fintype.sum_prod_type, Fin.sum_univ_succ]

theorem u_orthonormal (a b : Q) : ip (u a) (u b) = if a = b then 1 else 0 := by
  fin_cases a <;> fin_cases b <;>
    norm_num [ip, u, fourier, Fin.sum_univ_succ, Complex.ext_iff]

theorem v_orthonormal (a b : Q) : ip (v a) (v b) = if a = b then 1 else 0 := by
  fin_cases a <;> fin_cases b <;>
    apply Complex.ext <;>
    norm_num [ip, u, v, q, fourier, Fin.sum_univ_succ,
      Complex.mul_re, Complex.mul_im] <;> nlinarith [h_sq]

theorem u_complete : (∑ a : Q, projector (u a)) = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [projector, u, fourier, Fin.sum_univ_succ, Complex.ext_iff]

theorem v_complete : (∑ a : Q, projector (v a)) = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;>
    norm_num [projector, u, v, q, fourier, Fin.sum_univ_succ,
      Complex.mul_re, Complex.mul_im] <;> nlinarith [h_sq]

def aliceTargetPVM : PVM 4 := pvmOfBasis v v_orthonormal v_complete
def bobTargetPVM : PVM 4 := pvmOfBasis u u_orthonormal u_complete

def targetState : State 4 4 := stateOfPure phi phi_normalized

theorem bob_encoding : observable bobTargetPVM = shift := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [observable, bobTargetPVM, pvmOfBasis, projector,
      u, fourier, shift, Fin.sum_univ_succ, Complex.ext_iff]

theorem alice_encoding : observable aliceTargetPVM = swappedObservable := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;>
    norm_num [observable, aliceTargetPVM, pvmOfBasis, projector,
      u, v, q, fourier, swappedObservable, swappedWeights, shift,
      Matrix.mul_apply, Matrix.diagonal, Fin.sum_univ_succ,
      Complex.mul_re, Complex.mul_im] <;> nlinarith [h_sq]

/-- The Born table is obtained from actual projectors and Phi4 via the general
    rank-one Born lemma. It is not installed as a strategy-validity field. -/
theorem targetBorn_eq_table (a b : Q) : targetBorn a b = table a b := by
  unfold targetBorn aliceEffect bobEffect
  rw [pureBorn_projectors]
  fin_cases a <;> fin_cases b <;>
    norm_num [table, ip, tensorVec, phi, u, v, q, fourier,
      Fintype.sum_prod_type, Fin.sum_univ_succ, Complex.normSq_apply,
      Complex.mul_re, Complex.mul_im] <;> nlinarith [h_sq]

/-- The same result explicitly uses the mixed-state density and trace Born rule. -/
theorem mixed_targetBorn_eq_table (a b : Q) :
    born targetState.density (aliceTargetPVM.effect a) (bobTargetPVM.effect b) =
      table a b := by
  change born (projector phi) (projector (v a)) (projector (u b)) = table a b
  rw [← pureBorn_eq_born]
  exact targetBorn_eq_table a b

theorem target_nonnegative (a b : Q) : 0 ≤ targetBorn a b := by
  rw [targetBorn_eq_table]
  unfold table
  split <;> norm_num

theorem alice_marginal (a : Q) : ∑ b : Q, targetBorn a b = 1 / 4 := by
  simp only [targetBorn_eq_table]
  fin_cases a <;> norm_num [table, Fin.sum_univ_succ]

theorem bob_marginal (b : Q) : ∑ a : Q, targetBorn a b = 1 / 4 := by
  simp only [targetBorn_eq_table]
  fin_cases b <;> norm_num [table, Fin.sum_univ_succ]

theorem target_normalized : (∑ a : Q, ∑ b : Q, targetBorn a b) = 1 := by
  simp only [alice_marginal]
  norm_num

theorem target_le_three_thirtyseconds (a b : Q) : targetBorn a b ≤ 3 / 32 := by
  rw [targetBorn_eq_table]
  unfold table
  split <;> norm_num

theorem target_01 : targetBorn 0 1 = 3 / 32 := by
  rw [targetBorn_eq_table]
  norm_num [table]

theorem guessing_gap : (1 : ℝ) / 16 < fixedGuessSuccess targetBorn 0 1 := by
  unfold fixedGuessSuccess
  rw [target_01]
  norm_num

theorem target_not_uniform : ¬ ∀ a b : Q, targetBorn a b = 1 / 16 := by
  intro hu
  have h01 := hu 0 1
  rw [target_01] at h01
  norm_num at h01

/-- Focused negative control: doubling Phi4's amplitudes violates normalization. -/
theorem wrong_state_normalization :
    ip (fun i => 2 * phi i) (fun i => 2 * phi i) ≠ 1 := by
  norm_num [ip, phi, Fintype.sum_prod_type, Fin.sum_univ_succ]

/-- Combined target-only endpoint. It says nothing about a Bell score or a
    maximizing realization and therefore cannot be cited as A, C, E, or F. -/
theorem target_measurement_package :
    ip phi phi = 1 ∧
    observable aliceTargetPVM = swappedObservable ∧
    observable bobTargetPVM = shift ∧
    (∀ a b : Q, targetBorn a b = table a b) ∧
    (∀ a : Q, (∑ b : Q, targetBorn a b) = 1 / 4) ∧
    (∀ b : Q, (∑ a : Q, targetBorn a b) = 1 / 4) ∧
    (∑ a : Q, ∑ b : Q, targetBorn a b) = 1 ∧
    (∀ a b : Q, targetBorn a b ≤ 3 / 32) ∧
    targetBorn 0 1 = 3 / 32 ∧
    (1 : ℝ) / 16 < fixedGuessSuccess targetBorn 0 1 ∧
    ¬ (∀ a b : Q, targetBorn a b = 1 / 16) := by
  exact ⟨phi_normalized, alice_encoding, bob_encoding, targetBorn_eq_table,
    alice_marginal, bob_marginal, target_normalized,
    target_le_three_thirtyseconds, target_01, guessing_gap, target_not_uniform⟩

end CyclicBell.D4
