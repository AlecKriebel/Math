import CyclicBell.GeneralCorrelationValues
import CyclicBell.GeneralBinaryWitness

/-! Binary benchmark in arbitrary complete Hilbert spaces, and actual q/qa/qc
value assembly. The arbitrary-Hilbert proof is an algebraic SOS, not an inference
from finite matrices. The existing finite purifying-Eve privacy theorem remains
separate and is not promoted to infinite-dimensional privacy.
UNCOMPILED SOURCE CANDIDATES; this benchmark is prior art, not a novelty claim. -/
noncomputable section
open scoped BigOperators ComplexOrder InnerProductSpace Topology
namespace CyclicBell.General
variable {A : Type*} [CStarAlgebra A]

def AlgebraInvolution (a : A) : Prop := star a=a ∧ a*a=1

def algebraBinaryScore (a₀ a₁ b₀ b₁ : A) : A :=
  a₀*b₀-(2 : ℂ) • (a₀*b₁)+(2 : ℂ) • (a₁*b₀)+(2 : ℂ) • (a₁*b₁)

def algebraBinaryResidual0 (a₀ b₀ b₁ : A) : A :=
  (Real.sqrt 3 : ℂ) • a₀-b₀+(2 : ℂ) • b₁

def algebraBinaryResidual1 (a₁ b₀ b₁ : A) : A :=
  (Real.sqrt 3 : ℂ) • a₁-b₀-b₁

/-- Expansion before division: the Bob anticommutators cancel exactly. -/
theorem algebraBinary_scaled_sos (a₀ a₁ b₀ b₁ : A)
    (h₀ : AlgebraInvolution a₀) (h₁ : AlgebraInvolution a₁)
    (k₀ : AlgebraInvolution b₀) (k₁ : AlgebraInvolution b₁)
    (hc00 : a₀*b₀=b₀*a₀) (hc01 : a₀*b₁=b₁*a₀)
    (hc10 : a₁*b₀=b₀*a₁) (hc11 : a₁*b₁=b₁*a₁) :
    star (algebraBinaryResidual0 a₀ b₀ b₁)*algebraBinaryResidual0 a₀ b₀ b₁ +
      (2 : ℂ) • (star (algebraBinaryResidual1 a₁ b₀ b₁)*algebraBinaryResidual1 a₁ b₀ b₁) =
      (18 : ℂ) • (1 : A) - (2*(Real.sqrt 3 : ℂ)) • algebraBinaryScore a₀ a₁ b₀ b₁ := by
  have hs : (Real.sqrt 3 : ℂ)*(Real.sqrt 3 : ℂ)=3 := by
    simpa only [pow_two] using sqrt_three_square
  unfold algebraBinaryResidual0 algebraBinaryResidual1 algebraBinaryScore
  simp only [star_add,star_sub,star_smul,h₀.1,h₁.1,k₀.1,k₁.1,
    Complex.conj_ofReal,star_natCast,add_mul,mul_add,sub_mul,mul_sub,
    smul_mul_assoc,mul_smul_comm,smul_smul,hs,h₀.2,h₁.2,k₀.2,k₁.2,
    ← hc00,← hc01,← hc10,← hc11]
  module

/-- Manuscript eq:binary-sos in a general complex C*-algebra. -/
theorem binary_cstar_sos (a₀ a₁ b₀ b₁ : A)
    (h₀ : AlgebraInvolution a₀) (h₁ : AlgebraInvolution a₁)
    (k₀ : AlgebraInvolution b₀) (k₁ : AlgebraInvolution b₁)
    (hc00 : a₀*b₀=b₀*a₀) (hc01 : a₀*b₁=b₁*a₀)
    (hc10 : a₁*b₀=b₀*a₁) (hc11 : a₁*b₁=b₁*a₁) :
    ((3*Real.sqrt 3 : ℝ) : ℂ) • (1 : A) - algebraBinaryScore a₀ a₁ b₀ b₁ =
      (1/(2*(Real.sqrt 3 : ℂ))) •
        (star (algebraBinaryResidual0 a₀ b₀ b₁)*algebraBinaryResidual0 a₀ b₀ b₁) +
      (1/(Real.sqrt 3 : ℂ)) •
        (star (algebraBinaryResidual1 a₁ b₀ b₁)*algebraBinaryResidual1 a₁ b₀ b₁) := by
  have hs0 : (Real.sqrt 3 : ℂ)≠0 := by exact_mod_cast ne_of_gt sqrt_three_positive
  have hconst : (1/(2*(Real.sqrt 3 : ℂ)))*18=(3*Real.sqrt 3 : ℝ) := by
    push_cast
    field_simp [hs0]
    linear_combination -6 * sqrt_three_square
  have hone : (1/(2*(Real.sqrt 3 : ℂ)))*(2*(Real.sqrt 3 : ℂ))=1 := by field_simp [hs0]
  have htwo : (1/(2*(Real.sqrt 3 : ℂ)))*2=1/(Real.sqrt 3 : ℂ) := by field_simp [hs0]
  have h := congrArg (fun T : A => (1/(2*(Real.sqrt 3 : ℂ))) • T)
    (algebraBinary_scaled_sos a₀ a₁ b₀ b₁ h₀ h₁ k₀ k₁ hc00 hc01 hc10 hc11)
  simpa only [smul_add,smul_sub,smul_smul,hconst,hone,htwo,one_smul] using h.symm

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- No finite-dimensional hypothesis; positivity is the squared Hilbert norm. -/
theorem binary_commuting_hilbert_upper (ψ : H) (hψ : ‖ψ‖=1)
    (a₀ a₁ b₀ b₁ : H →L[ℂ] H)
    (h₀ : AlgebraInvolution a₀) (h₁ : AlgebraInvolution a₁)
    (k₀ : AlgebraInvolution b₀) (k₁ : AlgebraInvolution b₁)
    (hc00 : a₀*b₀=b₀*a₀) (hc01 : a₀*b₁=b₁*a₀)
    (hc10 : a₁*b₀=b₀*a₁) (hc11 : a₁*b₁=b₁*a₁) :
    vectorEval ψ (algebraBinaryScore a₀ a₁ b₀ b₁) ≤ 3*Real.sqrt 3 := by
  have h := congrArg (vectorEval ψ)
    (binary_cstar_sos a₀ a₁ b₀ b₁ h₀ h₁ k₀ k₁ hc00 hc01 hc10 hc11)
  have c₀ : (1/(2*(Real.sqrt 3 : ℂ)))=((1/(2*Real.sqrt 3) : ℝ) : ℂ) := by push_cast; rfl
  have c₁ : (1/(Real.sqrt 3 : ℂ))=((1/Real.sqrt 3 : ℝ) : ℂ) := by push_cast; rfl
  simp only [vectorEval_sub,vectorEval_add,c₀,c₁,vectorEval_real_smul,
    vectorEval_one ψ hψ,vectorEval_square,mul_one] at h
  have hc₀ : 0<(1/(2*Real.sqrt 3) : ℝ) := by positivity
  have hc₁ : 0<(1/Real.sqrt 3 : ℝ) := by positivity
  have hnonneg := add_nonneg
    (mul_nonneg hc₀.le (sq_nonneg ‖algebraBinaryResidual0 a₀ b₀ b₁ ψ‖))
    (mul_nonneg hc₁.le (sq_nonneg ‖algebraBinaryResidual1 a₁ b₀ b₁ ψ‖))
  linarith

theorem chi_two_one : chi (1 : Ix 2) = -1 := by
  have h := character_sum (1 : Ix 2)
  rw [sum_zmod_two] at h
  norm_num only [mul_zero,mul_one,chi_zero,show (1 : Ix 2)≠0 by decide,if_false] at h
  linear_combination h

theorem algebraEncoded_two_involution (M : AlgebraPVM 2 A) : AlgebraInvolution (algebraEncoded M) := by
  have h : algebraEncoded M = M.effect 0-M.effect 1 := by
    rw [algebraEncoded,sum_zmod_two]
    simp [chi_two_one,sub_eq_add_neg]
  constructor
  · rw [h,star_sub,M.selfadjoint,M.selfadjoint]
  · simpa only [pow_two] using algebraEncoded_order M

/-- Bell value on actual real binary probabilities, with coefficients 1,-2,2,2. -/
def binaryBell (p : BellBehavior 2 (Fin 2) (Fin 2)) : ℝ :=
  (probabilityCorrelator p 0 0).re-2*(probabilityCorrelator p 0 1).re+
    2*(probabilityCorrelator p 1 0).re+2*(probabilityCorrelator p 1 1).re

theorem binaryBell_continuous : Continuous binaryBell := by
  unfold binaryBell probabilityCorrelator
  fun_prop

theorem binaryBell_commuting (s : CommutingOn 2 (Fin 2) (Fin 2) H) :
    binaryBell (commutingBehavior s) = vectorEval s.vector
      (algebraBinaryScore (algebraEncoded (s.alice 0)) (algebraEncoded (s.alice 1))
        (algebraEncoded (s.bob 0)) (algebraEncoded (s.bob 1))) := by
  unfold binaryBell algebraBinaryScore
  simp only [probabilityCorrelator_commuting,vectorEval_add,vectorEval_sub]
  have ht : (2 : ℂ)=((2 : ℝ) : ℂ) := by norm_num
  rw [ht]
  simp only [vectorEval_real_smul]
  rfl

theorem binaryBell_commuting_upper (s : CommutingOn 2 (Fin 2) (Fin 2) H) :
    binaryBell (commutingBehavior s) ≤ 3*Real.sqrt 3 := by
  rw [binaryBell_commuting]
  exact binary_commuting_hilbert_upper s.vector s.normalized _ _ _ _
    (algebraEncoded_two_involution _) (algebraEncoded_two_involution _)
    (algebraEncoded_two_involution _) (algebraEncoded_two_involution _)
    (algebraPVM_cross_commute _ _ (s.cross 0 0))
    (algebraPVM_cross_commute _ _ (s.cross 0 1))
    (algebraPVM_cross_commute _ _ (s.cross 1 0))
    (algebraPVM_cross_commute _ _ (s.cross 1 1))

theorem binaryBell_Qqc_upper (p : BellBehavior 2 (Fin 2) (Fin 2))
    (hp : p ∈ Qqc 2 (Fin 2) (Fin 2)) : binaryBell p ≤ 3*Real.sqrt 3 := by
  rcases hp with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  exact binaryBell_commuting_upper s

/-- Explicit outcome identification avoids silently changing the binary label
convention used by the existing Fin 2 privacy instrument. -/
def binaryOutcome (a : Ix 2) : Fin 2 := ⟨a.val,ZMod.val_lt a⟩

theorem binaryOutcome_injective : Function.Injective binaryOutcome := by
  intro a b h
  fin_cases a <;> fin_cases b <;> norm_num [binaryOutcome] at h ⊢

variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

def binaryMeasurement (T : Mat ι) (hT : HermitianInvolution T) : Measurement 2 ι where
  effect := fun a => binaryEffect T (binaryOutcome a)
  positive := fun a => binaryEffect_positive T hT _
  complete := by
    rw [sum_zmod_two]
    simpa [binaryOutcome,Fin.sum_univ_succ] using binaryEffect_complete T
  idempotent := fun a => binaryEffect_idempotent T hT.2 _
  orthogonal := fun a b hab => binaryEffect_orthogonal T hT.2 _ _
    (fun h => hab (binaryOutcome_injective h))

theorem binaryMeasurement_encoded (T : Mat ι) (hT : HermitianInvolution T) :
    encoded (binaryMeasurement T hT)=T := by
  rw [encoded,sum_zmod_two]
  simp only [binaryMeasurement,binaryOutcome,chi_zero,chi_two_one,binaryEffect,
    show (0 : Ix 2).val=0 from rfl,show (1 : Ix 2).val=1 from rfl,
    pow_zero,pow_one,one_smul,neg_one_smul]
  module

def binaryIdealStrategy : StrategyOn 2 (Fin 2) (Fin 2) (Ix 2) (Ix 2) where
  state := entangledState 2
  alice := fun x => binaryMeasurement (binaryIdealAlice x) (binaryIdealAlice_involution x)
  bob := fun y => binaryMeasurement (binaryIdealBob y) (binaryIdealBob_involution y)

theorem binaryBell_behavior (s : StrategyOn 2 (Fin 2) (Fin 2) ι κ) :
    binaryBell (behavior s)=stateEval s.state.density
      (binaryScoreOperator (aliceLift (κ := κ) (encoded (s.alice 0)))
        (aliceLift (κ := κ) (encoded (s.alice 1)))
        (bobLift (ι := ι) (encoded (s.bob 0)))
        (bobLift (ι := ι) (encoded (s.bob 1)))) := by
  unfold binaryBell binaryScoreOperator
  simp only [probabilityCorrelator_behavior,stateEval_add,stateEval_sub,lift_product]
  have ht : (2 : ℂ)=((2 : ℝ) : ℂ) := by norm_num
  rw [ht]
  simp only [stateEval_real_smul]
  rfl

theorem binaryIdealStrategy_attains : binaryBell (behavior binaryIdealStrategy)=3*Real.sqrt 3 := by
  rw [binaryBell_behavior]
  simp only [binaryIdealStrategy,binaryMeasurement_encoded]
  exact binary_physical_attainment

/-- Literal q/qa/qc value part of thm:binary-benchmark. The finite privacy
conclusion remains the separately written binary_saturation_privacy theorem. -/
theorem binary_values_q_qa_qc :
    betaQ binaryBell=3*Real.sqrt 3 ∧ betaQa binaryBell=3*Real.sqrt 3 ∧ betaQc binaryBell=3*Real.sqrt 3 := by
  exact three_model_suprema (Qq 2 (Fin 2) (Fin 2)) (Qqc 2 (Fin 2) (Fin 2))
    binaryBell binaryBell_continuous (3*Real.sqrt 3) Qq_subset_Qqc binaryBell_Qqc_upper
    (behavior binaryIdealStrategy) (behavior_mem_Qq binaryIdealStrategy) binaryIdealStrategy_attains

end CyclicBell.General
