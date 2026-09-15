import CyclicBell.Model

/-!
Finite-dimensional matrix infrastructure for the two universal bounds.
All state inequalities below apply directly to arbitrary PSD trace-one matrices;
there is no pure-state restriction and no assumed spectral decomposition.
SOURCE CANDIDATE: this file has not been run through Lean.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell

variable {ι : Type*} [Fintype ι] [DecidableEq ι]
abbrev Mat (ι : Type*) := Matrix ι ι ℂ

@[simp] theorem star_real (r : ℝ) : star (r : ℂ) = (r : ℂ) := by simp

/-- Both inverse equations, with no finite-order or spectral assumptions. -/
def UnitaryRel (U : Mat ι) : Prop := U.conjTranspose * U = 1 ∧ U * U.conjTranspose = 1

namespace UnitaryRel
variable {U V : Mat ι}
theorem one : UnitaryRel (1 : Mat ι) := by simp [UnitaryRel]
theorem adjoint (hU : UnitaryRel U) : UnitaryRel U.conjTranspose := by
  simpa [UnitaryRel, and_comm] using hU

theorem mul (hU : UnitaryRel U) (hV : UnitaryRel V) : UnitaryRel (U * V) := by
  constructor
  · calc
      (U * V).conjTranspose * (U * V) =
          V.conjTranspose * (U.conjTranspose * U) * V := by
            simp [Matrix.conjTranspose_mul, mul_assoc]
      _ = 1 := by rw [hU.1]; simpa using hV.1
  · calc
      (U * V) * (U * V).conjTranspose =
          U * (V * V.conjTranspose) * U.conjTranspose := by
            simp [Matrix.conjTranspose_mul, mul_assoc]
      _ = 1 := by rw [hV.2]; simpa using hU.2

theorem pow (hU : UnitaryRel U) (k : ℕ) : UnitaryRel (U ^ k) := by
  induction k with
  | zero => simpa using (one (ι := ι))
  | succ k hk => simpa [pow_succ] using hk.mul hU

theorem cancel_left (hU : UnitaryRel U) (T : Mat ι) :
    U.conjTranspose * (U * T) = T := by rw [← mul_assoc, hU.1, one_mul]
theorem cancel_right (hU : UnitaryRel U) (T : Mat ι) :
    U * (U.conjTranspose * T) = T := by rw [← mul_assoc, hU.2, one_mul]

theorem scalar (hU : UnitaryRel U) {z : ℂ} (hz : star z * z = 1) :
    UnitaryRel (z • U) := by
  constructor
  · simp only [Matrix.conjTranspose_smul, smul_mul_assoc, mul_smul_comm,
      smul_smul, hU.1, mul_comm z, hz, one_smul]
  · have hz' : z * star z = 1 := by simpa [mul_comm] using hz
    simp only [Matrix.conjTranspose_smul, smul_mul_assoc, mul_smul_comm,
      smul_smul, hU.2, mul_comm (star z), hz', one_smul]

/-- Commuting with a unitary entails commuting with its adjoint. -/
theorem commute_adjoint_right (hV : UnitaryRel V) {T : Mat ι}
    (h : T * V = V * T) : T * V.conjTranspose = V.conjTranspose * T := by
  calc
    T * V.conjTranspose = V.conjTranspose * (V * T) * V.conjTranspose := by
      simp only [← mul_assoc, hV.1, one_mul]
    _ = V.conjTranspose * (T * V) * V.conjTranspose := by rw [h]
    _ = V.conjTranspose * T := by simp only [mul_assoc, hV.2, mul_one]
end UnitaryRel

/-- The Hermitian part, with a real factor 1/2. -/
def herm (T : Mat ι) : Mat ι := (1 / 2 : ℂ) • (T + T.conjTranspose)

def stateEval (ρ T : Mat ι) : ℝ := (Matrix.trace (ρ * T)).re

@[simp] theorem stateEval_add (ρ S T : Mat ι) :
    stateEval ρ (S + T) = stateEval ρ S + stateEval ρ T := by
  simp [stateEval, mul_add]
@[simp] theorem stateEval_sub (ρ S T : Mat ι) :
    stateEval ρ (S - T) = stateEval ρ S - stateEval ρ T := by
  simp [stateEval, mul_sub]
@[simp] theorem stateEval_zero (ρ : Mat ι) : stateEval ρ 0 = 0 := by simp [stateEval]
@[simp] theorem stateEval_real_smul (ρ T : Mat ι) (r : ℝ) :
    stateEval ρ ((r : ℂ) • T) = r * stateEval ρ T := by
  simp [stateEval, Matrix.trace_smul, mul_smul_comm, Complex.mul_re]

theorem stateEval_sum {κ : Type*} [Fintype κ] (ρ : Mat ι) (T : κ → Mat ι) :
    stateEval ρ (∑ k, T k) = ∑ k, stateEval ρ (T k) := by
  simp [stateEval, Finset.mul_sum, Matrix.trace_sum]

theorem stateEval_adjoint (ρ T : Mat ι) (hρ : ρ.IsHermitian) :
    stateEval ρ T.conjTranspose = stateEval ρ T := by
  have he : star (Matrix.trace (ρ * T)) = Matrix.trace (ρ * T.conjTranspose) := by
    rw [← Matrix.trace_conjTranspose, Matrix.conjTranspose_mul, hρ.eq,
      Matrix.trace_mul_comm]
  have hr := congrArg Complex.re he
  simpa [stateEval] using hr.symm

theorem stateEval_herm (ρ T : Mat ι) (hρ : ρ.IsHermitian) :
    stateEval ρ (herm T) = stateEval ρ T := by
  have hh : herm T = (((1 / 2 : ℝ) : ℂ)) • (T + T.conjTranspose) := by
    simp [herm]
  rw [hh, stateEval_real_smul, stateEval_add, stateEval_adjoint ρ T hρ]
  ring

theorem posSemidef_trace_re_nonnegative {T : Mat ι} (hT : T.PosSemidef) :
    0 ≤ (Matrix.trace T).re := by
  have hd : ∀ i, 0 ≤ (T i i).re := by
    intro i
    simpa [dotProduct, Pi.single_apply, Matrix.mulVec] using
      hT.re_dotProduct_nonneg (Pi.single i 1)
  simpa [Matrix.trace, Matrix.diag_apply] using
    (Finset.sum_nonneg (s := Finset.univ) (fun i _ => hd i))

/-- Direct mixed-state positivity. No commutation of ρ and T is needed. -/
theorem stateEval_square_nonnegative {ρ : Mat ι} (hρ : ρ.PosSemidef) (T : Mat ι) :
    0 ≤ stateEval ρ (T.conjTranspose * T) := by
  have hp := hρ.mul_mul_conjTranspose_same T
  have ht : Matrix.trace (ρ * (T.conjTranspose * T)) =
      Matrix.trace (T * ρ * T.conjTranspose) := by
    rw [← mul_assoc, Matrix.trace_mul_comm]
    simp only [mul_assoc]
  unfold stateEval
  rw [ht]
  exact posSemidef_trace_re_nonnegative hp

theorem stateEval_one {ρ : Mat ι} (hρ : Matrix.trace ρ = 1) :
    stateEval ρ 1 = 1 := by simp [stateEval, hρ]

/-- Elementary aligned-term SOS, valid for every unitary. -/
theorem aligned_gap_identity {U : Mat ι} (hU : UnitaryRel U) :
    1 - herm U = (1 / 2 : ℂ) • ((1 - U).conjTranspose * (1 - U)) := by
  simp only [herm, Matrix.conjTranspose_sub, Matrix.conjTranspose_one,
    sub_mul, mul_sub, one_mul, mul_one, hU.1]
  apply Matrix.ext
  intro i j
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

theorem aligned_upper {ρ U : Mat ι} (hρ : ρ.PosSemidef)
    (htrace : Matrix.trace ρ = 1) (hU : UnitaryRel U) : stateEval ρ U ≤ 1 := by
  have h := stateEval_square_nonnegative hρ (1 - U)
  have hid := congrArg (stateEval ρ) (aligned_gap_identity hU)
  have hhalf : (1 / 2 : ℂ) = ((1 / 2 : ℝ) : ℂ) := by norm_num
  rw [stateEval_sub, stateEval_one htrace, stateEval_herm ρ U hρ.1,
    hhalf, stateEval_real_smul] at hid
  linarith

/-! Tensor placement, kept explicit rather than assumed commutation. -/

@[simp] theorem tensor_add_left {nA nB : ℕ} (A C : Op nA) (B : Op nB) :
    tensor (A + C) B = tensor A B + tensor C B := by
  ext i j; simp [tensor, add_mul]
@[simp] theorem tensor_add_right {nA nB : ℕ} (A : Op nA) (B D : Op nB) :
    tensor A (B + D) = tensor A B + tensor A D := by
  ext i j; simp [tensor, mul_add]
@[simp] theorem tensor_smul_left {nA nB : ℕ} (z : ℂ) (A : Op nA) (B : Op nB) :
    tensor (z • A) B = z • tensor A B := by
  ext i j; simp [tensor, mul_assoc]
@[simp] theorem tensor_smul_right {nA nB : ℕ} (z : ℂ) (A : Op nA) (B : Op nB) :
    tensor A (z • B) = z • tensor A B := by
  ext i j; simp [tensor]; ring

theorem tensor_mul {nA nB : ℕ} (A C : Op nA) (B D : Op nB) :
    tensor A B * tensor C D = tensor (A * C) (B * D) := by
  ext i j
  simp only [Matrix.mul_apply, tensor, Fintype.sum_prod_type, Finset.sum_mul,
    Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro k _
  apply Finset.sum_congr rfl
  intro l _
  ring

@[simp] theorem tensor_adjoint {nA nB : ℕ} (A : Op nA) (B : Op nB) :
    (tensor A B).conjTranspose = tensor A.conjTranspose B.conjTranspose := by
  ext i j; simp [tensor, Matrix.conjTranspose_apply, mul_comm]

@[simp] theorem tensor_one (nA nB : ℕ) :
    tensor (1 : Op nA) (1 : Op nB) = 1 := by
  ext i j
  rcases i with ⟨i,k⟩; rcases j with ⟨j,l⟩
  by_cases hij : i = j <;> by_cases hkl : k = l <;>
    simp [tensor, Matrix.one_apply, hij, hkl, Prod.mk.injEq]

theorem tensor_unitary {nA nB : ℕ} {A : Op nA} {B : Op nB}
    (hA : UnitaryRel A) (hB : UnitaryRel B) : UnitaryRel (tensor A B) := by
  constructor <;> simp only [tensor_adjoint, tensor_mul, hA.1, hA.2, hB.1, hB.2,
    tensor_one]

def liftAlice {nA : ℕ} (nB : ℕ) (A : Op nA) : JointOp nA nB := tensor A 1

def liftBob (nA : ℕ) {nB : ℕ} (B : Op nB) : JointOp nA nB := tensor 1 B

@[simp] theorem liftAlice_mul_liftBob {nA nB : ℕ} (A : Op nA) (B : Op nB) :
    liftAlice nB A * liftBob nA B = tensor A B := by
  simp [liftAlice, liftBob, tensor_mul]
@[simp] theorem liftBob_mul_liftAlice {nA nB : ℕ} (A : Op nA) (B : Op nB) :
    liftBob nA B * liftAlice nB A = tensor A B := by
  simp [liftAlice, liftBob, tensor_mul]

theorem tensor_cross_commute {nA nB : ℕ} (A : Op nA) (B : Op nB) :
    liftAlice nB A * liftBob nA B = liftBob nA B * liftAlice nB A := by simp

/-! PVM-to-observable bridge, including unused outcomes. -/

def spectralSum {n : ℕ} (M : PVM n) (f : Fin 4 → ℂ) : Op n :=
  ∑ a, f a • M.effect a

theorem effect_mul {n : ℕ} (M : PVM n) (a b : Fin 4) :
    M.effect a * M.effect b = if a = b then M.effect a else 0 := by
  by_cases hab : a = b
  · subst b; simp [M.idempotent]
  · simp [hab, M.orthogonal a b hab]

theorem spectralSum_one {n : ℕ} (M : PVM n) : spectralSum M (fun _ => 1) = 1 := by
  simpa [spectralSum] using M.complete

theorem spectralSum_mul {n : ℕ} (M : PVM n) (f g : Fin 4 → ℂ) :
    spectralSum M f * spectralSum M g = spectralSum M (fun a => f a * g a) := by
  classical
  unfold spectralSum
  simp only [Finset.sum_mul, Finset.mul_sum, smul_mul_assoc, mul_smul_comm,
    smul_smul, effect_mul]
  apply Finset.sum_congr rfl
  intro a _
  rw [Finset.sum_eq_single a]
  · simp [smul_smul, mul_comm]
  · intro b _ hba; simp [hba]
  · simp

theorem spectralSum_adjoint {n : ℕ} (M : PVM n) (f : Fin 4 → ℂ) :
    (spectralSum M f).conjTranspose = spectralSum M (fun a => star (f a)) := by
  simp only [spectralSum, Matrix.conjTranspose_sum, Matrix.conjTranspose_smul]
  apply Finset.sum_congr rfl
  intro a _
  rw [(M.positive a).isHermitian.eq]

theorem observable_unitary {n : ℕ} (M : PVM n) : UnitaryRel (observable M) := by
  change UnitaryRel (spectralSum M (fun a => Complex.I ^ a.val))
  constructor
  · rw [spectralSum_adjoint, spectralSum_mul]
    rw [← spectralSum_one M]
    apply congrArg (spectralSum M)
    funext a
    fin_cases a <;> norm_num
  · rw [spectralSum_adjoint, spectralSum_mul]
    rw [← spectralSum_one M]
    apply congrArg (spectralSum M)
    funext a
    fin_cases a <;> norm_num

theorem observable_power {n : ℕ} (M : PVM n) (k : ℕ) :
    observable M ^ k = spectralSum M (fun a => (Complex.I ^ a.val) ^ k) := by
  induction k with
  | zero => simpa using (spectralSum_one M).symm
  | succ k hk =>
      rw [pow_succ, hk]
      change spectralSum M _ * spectralSum M _ = _
      rw [spectralSum_mul]
      apply congrArg (spectralSum M)
      funext a
      rw [pow_succ]

theorem observable_fourth_power {n : ℕ} (M : PVM n) : observable M ^ 4 = 1 := by
  rw [observable_power]
  rw [← spectralSum_one M]
  apply congrArg (spectralSum M)
  funext a
  fin_cases a <;> norm_num [pow_succ]

end CyclicBell
