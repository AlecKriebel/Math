import CyclicBell.GeneralBinaryModels
import CyclicBell.GeneralConsequences
import CyclicBell.GeneralPartySwap

/-! Actual finite purified strategies and the binary setting-minimality
endpoint. `BinaryPrivacyAt` quantifies over ALL finite-dimensional compatible
purifications, not just the attaining realization. Physical strategy validity
contains no score, privacy or guessing condition. UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General

variable {d : ℕ} [NeZero d]
variable {α β ι κ ε : Type*} [Fintype ι] [Fintype κ] [Fintype ε]
  [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]

structure PurifiedStrategyOn (d : ℕ) [NeZero d] (α β ι κ ε : Type*)
    [Fintype ι] [Fintype κ] [Fintype ε] [DecidableEq ι] [DecidableEq κ] where
  amplitude : Matrix (ι×κ) ε ℂ
  normalized : frobeniusSq amplitude=1
  alice : α → Measurement d ι
  bob : β → Measurement d κ

def purifiedToStrategy (s : PurifiedStrategyOn d α β ι κ ε) : StrategyOn d α β ι κ where
  state := amplitudeState s.amplitude s.normalized
  alice := s.alice
  bob := s.bob

def purifiedBehavior (s : PurifiedStrategyOn d α β ι κ ε) : BellBehavior d α β :=
  behavior (purifiedToStrategy s)

def purifiedInstrument (s : PurifiedStrategyOn d α β ι κ ε)
    (x : α) (y : β) (a b : Ix d) : Mat ε := jointInstrument s.amplitude (s.alice x) (s.bob y) a b

/-- Every finite mixed strategy has a compatible finite purification. This
bridge is independent of binary saturation and any privacy statement. -/
def purifyStrategy (s : StrategyOn d α β ι κ) : PurifiedStrategyOn d α β ι κ (ι×κ) where
  amplitude := stateFactor s.state
  normalized := stateFactor_normalized s.state
  alice := s.alice
  bob := s.bob

theorem purifyStrategy_behavior (s : StrategyOn d α β ι κ) :
    purifiedBehavior (purifyStrategy s)=behavior s := by
  funext x y a b
  change bornProbability (stateFactor s.state*(stateFactor s.state).conjTranspose)
    ((s.alice x).effect a) ((s.bob y).effect b)=_
  rw [stateFactor_gram]
  rfl

theorem encoded_two_eq_sub (M : Measurement 2 ι) : encoded M=M.effect 0-M.effect 1 := by
  rw [encoded,sum_zmod_two]
  simp [chi_two_one,sub_eq_add_neg]

theorem encoded_two_involution (M : Measurement 2 ι) : HermitianInvolution (encoded M) := by
  constructor
  · rw [encoded_two_eq_sub]
    exact (M.positive 0).isHermitian.sub (M.positive 1).isHermitian
  · simpa only [pow_two] using encoded_order M

/-- The finite project's positive-character encoding agrees outcome-by-outcome
with the binary Hermitian spectral formula used by the privacy proof. -/
theorem measurement_two_effect (M : Measurement 2 ι) (a : Ix 2) :
    M.effect a=binaryEffect (encoded M) (binaryOutcome a) := by
  have hsum : M.effect 0+M.effect 1=(1 : Mat ι) := by
    simpa only [sum_zmod_two] using M.complete
  rw [encoded_two_eq_sub]
  have ha : a = 0 ∨ a = 1 := by
    fin_cases a <;> simp
  rcases ha with rfl | rfl
  all_goals
    norm_num [binaryEffect,binaryOutcome,show (1 : Ix 2).val = 1 from rfl]
    rw [← hsum]
    module

theorem binary_involution_leftLift (A : Mat ι) (hA : HermitianInvolution A) :
    HermitianInvolution (aliceLift (κ := κ) A) := by
  constructor
  · simp only [Matrix.IsHermitian,aliceLift,kron_star,Matrix.conjTranspose_one,hA.1.eq]
  · simp only [aliceLift,kron_mul,hA.2,one_mul,kron_one]

theorem binary_involution_rightLift (B : Mat κ) (hB : HermitianInvolution B) :
    HermitianInvolution (bobLift (ι := ι) B) := by
  constructor
  · simp only [Matrix.IsHermitian,bobLift,kron_star,Matrix.conjTranspose_one,hB.1.eq]
  · simp only [bobLift,kron_mul,hB.2,one_mul,kron_one]

theorem binaryEffect_leftLift (A : Mat ι) (a : Fin 2) :
    binaryEffect (aliceLift (κ := κ) A) a=aliceLift (κ := κ) (binaryEffect A a) := by
  unfold binaryEffect aliceLift
  simp only [kron_add_left,kron_smul_left,kron_one]

theorem binaryEffect_rightLift (B : Mat κ) (b : Fin 2) :
    binaryEffect (bobLift (ι := ι) B) b=bobLift (ι := ι) (binaryEffect B b) := by
  unfold binaryEffect bobLift
  simp only [kron_add_right,kron_smul_right,kron_one]

/-- Full finite-dimensional privacy endpoint expressed in the actual projective
strategy model and its actual conditional instrument, for arbitrary Eve dimension. -/
theorem binary_purified_saturation (s : PurifiedStrategyOn 2 (Fin 2) (Fin 2) ι κ ε)
    (hs : binaryBell (purifiedBehavior s)=3*Real.sqrt 3) :
    ∀ a b : Ix 2,purifiedInstrument s 0 0 a b=(1/4 : ℂ) • reducedE s.amplitude := by
  have hscore : stateEval (s.amplitude*s.amplitude.conjTranspose)
      (binaryScoreOperator (aliceLift (κ := κ) (encoded (s.alice 0)))
        (aliceLift (κ := κ) (encoded (s.alice 1)))
        (bobLift (ι := ι) (encoded (s.bob 0)))
        (bobLift (ι := ι) (encoded (s.bob 1))))=3*Real.sqrt 3 := by
    simpa only [purifiedBehavior,binaryBell_behavior,purifiedToStrategy,amplitudeState] using hs
  have h := binary_saturation_privacy s.amplitude s.normalized _ _ _ _
    (binary_involution_leftLift _ (encoded_two_involution (s.alice 0)))
    (binary_involution_leftLift _ (encoded_two_involution (s.alice 1)))
    (binary_involution_rightLift _ (encoded_two_involution (s.bob 0)))
    (binary_involution_rightLift _ (encoded_two_involution (s.bob 1)))
    ⟨lift_commute _ _,lift_commute _ _,lift_commute _ _,lift_commute _ _⟩ hscore
  intro a b
  have hab := h (binaryOutcome a) (binaryOutcome b)
  rw [binaryEffect_leftLift,binaryEffect_rightLift,lift_product,
    ← measurement_two_effect,← measurement_two_effect] at hab
  exact hab

/-- A behavior certifies a private binary target precisely when EVERY compatible
finite tensor-product purification has the operator-uniform conditional states.
This is the property being proved/refuted, never a validity field. -/
def BinaryPrivacyAt {α β : Type} (p : BellBehavior 2 α β) (x : α) (y : β) : Prop :=
  ∀ (ι κ ε : Type) (fι : Fintype ι) (fκ : Fintype κ) (fε : Fintype ε),
    letI := fι
    letI := fκ
    letI := fε
    ∀ (eι : DecidableEq ι) (eκ : DecidableEq κ) (eε : DecidableEq ε),
      letI := eι
      letI := eκ
      letI := eε
      ∀ s : PurifiedStrategyOn 2 α β ι κ ε,purifiedBehavior s=p →
        ∀ a b : Ix 2,purifiedInstrument s x y a b=(1/4 : ℂ) • reducedE s.amplitude

theorem binary_maximum_certifies_privacy (p : BellBehavior 2 (Fin 2) (Fin 2))
    (hs : binaryBell p=3*Real.sqrt 3) : BinaryPrivacyAt p 0 0 := by
  intro ι κ ε fι fκ fε
  letI := fι
  letI := fκ
  letI := fε
  intro eι eκ eε
  letI := eι
  letI := eκ
  letI := eε
  intro s he
  apply binary_purified_saturation s
  rw [he]
  exact hs

/-- Nonvacuity and attainment accompany the universally quantified certificate. -/
theorem binary_two_input_private_achievable :
    ∃ p : BellBehavior 2 (Fin 2) (Fin 2),p∈Qq 2 (Fin 2) (Fin 2) ∧
      binaryBell p=3*Real.sqrt 3 ∧ BinaryPrivacyAt p 0 0 := by
  refine ⟨behavior binaryIdealStrategy,behavior_mem_Qq binaryIdealStrategy,
    binaryIdealStrategy_attains,?_⟩
  exact binary_maximum_certifies_privacy _ binaryIdealStrategy_attains

/-- Grouping a stored classical assignment is an actual binary PVM. -/
def groupingBinaryMeasurement {L : Type*} [Fintype L] [DecidableEq L]
    (f : L → Ix 2) : Measurement 2 L where
  effect := groupingProjector f
  positive := grouping_positive f
  complete := grouping_complete f
  idempotent := grouping_idempotent f
  orthogonal := grouping_orthogonal f

/-- A success-one guessing POVM contradicts an operator-uniform target. Only
completeness is needed in this algebraic helper; our constructions also prove
positivity of the actual guessing effects. -/
theorem perfect_guess_not_private (T : Matrix (ι×κ) ε ℂ) (hT : frobeniusSq T=1)
    (M : Measurement 2 ι) (N : Measurement 2 κ) (Q : Ix 2 → Ix 2 → Mat ε)
    (hQ : ∑ a,∑ b,Q a b=1)
    (hguess : (∑ a,∑ b,(Matrix.trace (Q a b*jointInstrument T M N a b)).re)=1) :
    ¬ ∀ a b : Ix 2,jointInstrument T M N a b=(1/4 : ℂ) • reducedE T := by
  intro hprivate
  simp_rw [hprivate] at hguess
  have htrace : Matrix.trace (reducedE T)=1 := by rw [reducedE_trace,hT]; norm_num
  have hu := operator_uniform_guess_success (reducedE T) htrace (1/4) Q hQ
  norm_num only [Complex.ofReal_div,Complex.ofReal_one,Complex.ofReal_ofNat] at hu
  linarith

variable {Y : Type} [Fintype Y] [DecidableEq Y]

def oneInputPurifiedStrategy (p : OneInputBehavior Y (Ix 2) (fun _ => Ix 2)) :
    PurifiedStrategyOn 2 Unit Y (StoredAssignments (Ix 2) (fun _ : Y => Ix 2))
      (StoredAssignments (Ix 2) (fun _ : Y => Ix 2)) (StoredAssignments (Ix 2) (fun _ : Y => Ix 2)) where
  amplitude := storedPurification (hiddenWeight p)
  normalized := storedPurification_normalized _ (hiddenWeight_nonnegative p) (hiddenWeight_normalized p)
  alice := fun _ => groupingBinaryMeasurement (fun label => label.1)
  bob := fun y => groupingBinaryMeasurement (fun label => label.2 y)

theorem oneInputPurifiedStrategy_behavior (p : OneInputBehavior Y (Ix 2) (fun _ => Ix 2)) :
    purifiedBehavior (oneInputPurifiedStrategy p)=(fun _ y a b => p.joint y a b) := by
  funext x y a b
  exact (one_input_pure_projective_perfect_guess p).2.1 y a b

theorem oneInputPurifiedStrategy_not_private (p : OneInputBehavior Y (Ix 2) (fun _ => Ix 2)) (y : Y) :
    ¬ ∀ a b : Ix 2,purifiedInstrument (oneInputPurifiedStrategy p) () y a b=
      (1/4 : ℂ) • reducedE (oneInputPurifiedStrategy p).amplitude := by
  let s := oneInputPurifiedStrategy p
  apply perfect_guess_not_private s.amplitude s.normalized (s.alice ()) (s.bob y)
    (storedEveGuess (fun label => label.1) (fun label => label.2 y)) (storedEve_complete _ _)
  exact storedEve_success_one _ (hiddenWeight_nonnegative p) (hiddenWeight_normalized p) _ _

theorem left_one_input_no_binary_privacy (p : OneInputBehavior Y (Ix 2) (fun _ => Ix 2)) (y : Y) :
    ¬ BinaryPrivacyAt (fun (_ : Unit) y a b => p.joint y a b) () y := by
  intro h
  let L := StoredAssignments (Ix 2) (fun _ : Y => Ix 2)
  have hp := h L L L inferInstance inferInstance inferInstance
    inferInstance inferInstance inferInstance (oneInputPurifiedStrategy p) (oneInputPurifiedStrategy_behavior p)
  exact oneInputPurifiedStrategy_not_private p y hp

variable {X : Type} [Fintype X] [DecidableEq X]

def rightInputPurifiedStrategy (p : RightOneInputBehavior X (Ix 2) (fun _ => Ix 2)) :
    PurifiedStrategyOn 2 X Unit (StoredAssignments (Ix 2) (fun _ : X => Ix 2))
      (StoredAssignments (Ix 2) (fun _ : X => Ix 2)) (StoredAssignments (Ix 2) (fun _ : X => Ix 2)) where
  amplitude := storedPurification (rightHiddenWeight p)
  normalized := storedPurification_normalized _ (rightHiddenWeight_nonnegative p) (rightHiddenWeight_normalized p)
  alice := fun x => groupingBinaryMeasurement (fun label => label.2 x)
  bob := fun _ => groupingBinaryMeasurement (fun label => label.1)

theorem rightInputPurifiedStrategy_behavior (p : RightOneInputBehavior X (Ix 2) (fun _ => Ix 2)) :
    purifiedBehavior (rightInputPurifiedStrategy p)=(fun x _ a b => p.joint x a b) := by
  funext x y a b
  exact (right_one_input_pure_projective_perfect_guess p).2.1 x a b

theorem rightInputPurifiedStrategy_not_private (p : RightOneInputBehavior X (Ix 2) (fun _ => Ix 2)) (x : X) :
    ¬ ∀ a b : Ix 2,purifiedInstrument (rightInputPurifiedStrategy p) x () a b=
      (1/4 : ℂ) • reducedE (rightInputPurifiedStrategy p).amplitude := by
  let s := rightInputPurifiedStrategy p
  apply perfect_guess_not_private s.amplitude s.normalized (s.alice x) (s.bob ())
    (storedEveGuess (fun label => label.2 x) (fun label => label.1)) (storedEve_complete _ _)
  exact storedEve_success_one _ (rightHiddenWeight_nonnegative p) (rightHiddenWeight_normalized p) _ _

theorem right_one_input_no_binary_privacy (p : RightOneInputBehavior X (Ix 2) (fun _ => Ix 2)) (x : X) :
    ¬ BinaryPrivacyAt (fun x (_ : Unit) a b => p.joint x a b) x () := by
  intro h
  let L := StoredAssignments (Ix 2) (fun _ : X => Ix 2)
  have hp := h L L L inferInstance inferInstance inferInstance
    inferInstance inferInstance inferInstance (rightInputPurifiedStrategy p) (rightInputPurifiedStrategy_behavior p)
  exact rightInputPurifiedStrategy_not_private p x hp

/-- Source cor:binary-minimality, in explicit positive-input-alphabet form:
a two-input-per-party behavior certifies a private binary target, but no
nonsignalling one-input behavior on either wing can do so at any target.
The definition quantifies all compatible finite purifications. -/
theorem binary_componentwise_minimality :
    (∃ p : BellBehavior 2 (Fin 2) (Fin 2),p∈Qq 2 (Fin 2) (Fin 2) ∧
      binaryBell p=3*Real.sqrt 3 ∧ BinaryPrivacyAt p 0 0) ∧
    (∀ p : OneInputBehavior Y (Ix 2) (fun _ => Ix 2),∀ y : Y,
      ¬ BinaryPrivacyAt (fun (_ : Unit) y a b => p.joint y a b) () y) ∧
    (∀ p : RightOneInputBehavior X (Ix 2) (fun _ => Ix 2),∀ x : X,
      ¬ BinaryPrivacyAt (fun x (_ : Unit) a b => p.joint x a b) x ()) :=
  ⟨binary_two_input_private_achievable,left_one_input_no_binary_privacy,right_one_input_no_binary_privacy⟩

end CyclicBell.General
