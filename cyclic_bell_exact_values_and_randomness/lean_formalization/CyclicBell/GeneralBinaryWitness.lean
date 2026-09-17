import CyclicBell.GeneralBinary

/-! The literal binary attaining matrices, with valid spectral projectors.
This finishes the finite-dimensional value/attainment portion of the binary
benchmark source route.  -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General

theorem sum_zmod_two {R : Type*} [AddCommMonoid R] (f : Ix 2 → R) :
    (∑ j,f j)=f 0+f 1 := by
  classical
  have hu : (Finset.univ : Finset (Ix 2))={0,1} := by
    ext j
    fin_cases j <;> simp
  rw [hu]
  simp

def binaryX : Mat (Ix 2) := cyclicShift 2
def binaryZ : Mat (Ix 2) := Matrix.diagonal (fun j => (-1 : ℂ)^j.val)
def binaryIdealAlice (x : Fin 2) : Mat (Ix 2) :=
  if x=0 then binaryZ else (-1/2 : ℂ) • binaryZ+(Real.sqrt 3/2 : ℂ) • binaryX
def binaryIdealBob (y : Fin 2) : Mat (Ix 2) :=
  if y=0 then binaryX else (-(Real.sqrt 3/2) : ℂ) • binaryZ+(1/2 : ℂ) • binaryX

theorem binaryPauli_relations :
    HermitianInvolution binaryX ∧ HermitianInvolution binaryZ ∧ binaryX*binaryZ=-(binaryZ*binaryX) := by
  have htwo : (2 : Ix 2) = 0 := by decide
  have hone : (1 : Ix 2) + 1 = 0 := by decide
  have hthree : (3 : Ix 2) = 1 := by decide
  have cases_two : ∀ i : Ix 2, i = 0 ∨ i = 1 := by
    intro i
    fin_cases i
    · exact Or.inl rfl
    · exact Or.inr rfl
  refine ⟨⟨?_,?_⟩,⟨?_,?_⟩,?_⟩
  all_goals
    ext i j
    rcases cases_two i with rfl | rfl <;>
      rcases cases_two j with rfl | rfl <;>
      norm_num [binaryX,binaryZ,cyclicShift,weightedCycle,Matrix.IsHermitian,
        Matrix.conjTranspose_apply,Matrix.diagonal_apply,Matrix.mul_apply,
        sum_zmod_two, ZMod.val, Fin.add_def, Fin.ext_iff, htwo, hone]
  all_goals try simp [htwo, hone, hthree]

theorem binaryIdealAlice_involution (x : Fin 2) : HermitianInvolution (binaryIdealAlice x) := by
  fin_cases x
  · simpa [binaryIdealAlice] using binaryPauli_relations.2.1
  · constructor
    · simp [binaryIdealAlice,Matrix.IsHermitian,Matrix.conjTranspose_add,Matrix.conjTranspose_smul,
        binaryPauli_relations.1.1.eq,binaryPauli_relations.2.1.1.eq]
    · change ((-1/2 : ℂ) • binaryZ+(Real.sqrt 3/2 : ℂ) • binaryX) *
        ((-1/2 : ℂ) • binaryZ+(Real.sqrt 3/2 : ℂ) • binaryX) = 1
      simp only [
        add_mul,mul_add,smul_mul_assoc,mul_smul_comm,smul_smul,
        binaryPauli_relations.1.2,binaryPauli_relations.2.1.2,binaryPauli_relations.2.2]
      ext i j
      try simp only [Matrix.add_apply,Matrix.smul_apply,smul_eq_mul,Matrix.neg_apply]
      linear_combination ((1 : Mat (Ix 2)) i j/4)*sqrt_three_square

theorem binaryIdealBob_involution (y : Fin 2) : HermitianInvolution (binaryIdealBob y) := by
  fin_cases y
  · simpa [binaryIdealBob] using binaryPauli_relations.1
  · constructor
    · simp [binaryIdealBob,Matrix.IsHermitian,Matrix.conjTranspose_add,Matrix.conjTranspose_smul,
        binaryPauli_relations.1.1.eq,binaryPauli_relations.2.1.1.eq]
    · change ((-(Real.sqrt 3/2) : ℂ) • binaryZ+(1/2 : ℂ) • binaryX) *
        ((-(Real.sqrt 3/2) : ℂ) • binaryZ+(1/2 : ℂ) • binaryX) = 1
      simp only [
        add_mul,mul_add,smul_mul_assoc,mul_smul_comm,smul_smul,
        binaryPauli_relations.1.2,binaryPauli_relations.2.1.2,binaryPauli_relations.2.2]
      ext i j
      try simp only [Matrix.add_apply,Matrix.smul_apply,smul_eq_mul,Matrix.neg_apply]
      linear_combination ((1 : Mat (Ix 2)) i j/4)*sqrt_three_square

/-- Literal manuscript A0=Z,A1=-Z/2+sqrt(3)X/2,B0=X,
B1=-sqrt(3)Z/2+X/2, on the normalized actual Phi2 state. -/
theorem binary_physical_attainment :
    stateEval (entangledState 2).density
      (binaryScoreOperator (aliceLift (κ := Ix 2) (binaryIdealAlice 0))
        (aliceLift (κ := Ix 2) (binaryIdealAlice 1))
        (bobLift (ι := Ix 2) (binaryIdealBob 0))
        (bobLift (ι := Ix 2) (binaryIdealBob 1)))=3*Real.sqrt 3 := by
  have htwo : (2 : Ix 2) = 0 := by decide
  have hone : (1 : Ix 2) + 1 = 0 := by decide
  have hthree : (3 : Ix 2) = 1 := by decide
  unfold binaryScoreOperator
  rw [stateEval_add,stateEval_add,stateEval_sub]
  simp only [lift_product]
  have hs : (2 : ℂ)=((2 : ℝ) : ℂ) := by norm_num
  simp only [hs,stateEval_real_smul,entangled_stateEval,phi_trace]
  norm_num [binaryIdealAlice,binaryIdealBob,binaryX,binaryZ,cyclicShift,weightedCycle,
    Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,Matrix.transpose_apply,
    Matrix.diagonal_apply,sum_zmod_two,Complex.div_re,Complex.div_im,
    ZMod.val, Fin.add_def, Fin.ext_iff, htwo, hone]
  simp only [htwo, hone]
  norm_num
  ring

/-- PVM validity is attached to every explicit binary input, not just the
observables' formal involution identities. -/
theorem binary_physical_measurement_package :
    (∀ x a,(binaryEffect (binaryIdealAlice x) a).PosSemidef) ∧
    (∀ y b,(binaryEffect (binaryIdealBob y) b).PosSemidef) ∧
    (∀ x,∑ a,binaryEffect (binaryIdealAlice x) a=1) ∧
    (∀ y,∑ b,binaryEffect (binaryIdealBob y) b=1) ∧
    (∀ x a b,a≠b → binaryEffect (binaryIdealAlice x) a*binaryEffect (binaryIdealAlice x) b=0) ∧
    (∀ y a b,a≠b → binaryEffect (binaryIdealBob y) a*binaryEffect (binaryIdealBob y) b=0) := by
  exact ⟨fun x a => binaryEffect_positive _ (binaryIdealAlice_involution x) a,
    fun y b => binaryEffect_positive _ (binaryIdealBob_involution y) b,
    fun x => binaryEffect_complete _,fun y => binaryEffect_complete _,
    fun x a b h => binaryEffect_orthogonal _ (binaryIdealAlice_involution x).2 a b h,
    fun y a b h => binaryEffect_orthogonal _ (binaryIdealBob_involution y).2 a b h⟩

end CyclicBell.General
