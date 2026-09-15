import CyclicBell.GeneralCycleCharpoly
import CyclicBell.GeneralBinaryCertification
import CyclicBell.GeneralBinaryModels
import CyclicBell.GeneralModelCounterexamples
import CyclicBell.GeneralPartySwap
import CyclicBell.GeneralExactValues

/-! Expanded statement correspondence tests for the model/value continuation.
These are UNEXECUTED Lean examples, not an independent statement audit. They
expose physical definitions, arbitrary dimensions, real Born arrays, the actual
closure, and all three supremum operators. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder InnerProductSpace Topology
namespace CyclicBell.ModelValueStatementAudit
open General

example {d : ℕ} [NeZero d] {α β : Type} :
    Qqa d α β = closure (Qq d α β) := rfl

example {d : ℕ} [NeZero d] {α β : Type} : Qq d α β ⊆ Qqc d α β := Qq_subset_Qqc

example {d : ℕ} [NeZero d] {α β : Type} : Qq d α β ⊆ Qqa d α β := Qq_subset_Qqa

example {d : ℕ} [NeZero d] {α β : Type}
    (p : α → β → ZMod d → ZMod d → ℝ) (x : α) (y : β) :
    probabilityCorrelator p x y =
      ∑ a : ZMod d,∑ b : ZMod d,ZMod.stdAddChar (a+b)*(p x y a b : ℂ) := rfl

example {d : ℕ} [NeZero d] {α β : Type} {nA nB : ℕ}
    (s : StrategyOn d α β (Fin nA) (Fin nB)) :
    commutingBehavior (finiteToCommuting s) = General.behavior s := finiteToCommuting_behavior s

/-- Mixed states need not be faithful or have dimension d on either party. -/
example (n : ℕ) (ρ : StateOn (Fin n)) : ‖purificationVector ρ‖=1 := purificationVector_normalized ρ

example (n : ℕ) (ρ : StateOn (Fin n)) (T : Matrix (Fin n) (Fin n) ℂ) :
    (⟪purificationVector ρ,
      matrixCLM (kron T (1 : Matrix (Fin n) (Fin n) ℂ)) (purificationVector ρ)⟫_ℂ).re =
      (Matrix.trace (ρ.density*T)).re := purification_stateEval ρ T

example {d : ℕ} [NeZero d] {α β H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (s : CommutingOn d α β H)
    (x : α) (y : β) (a b : ZMod d) :
    commutingBehavior s x y a b =
      (⟪s.vector, ((s.alice x).effect a*(s.bob y).effect b) s.vector⟫_ℂ).re := rfl

example {d : ℕ} [NeZero d] {α β H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (s : CommutingOn d α β H)
    (x : α) (y : β) : (∑ a : ZMod d,∑ b : ZMod d,commutingBehavior s x y a b)=1 :=
  commutingBehavior_normalized s x y

example (d : ℕ) [NeZero d] (hd : 2≤d) :
    sSup (firstReducedBell '' Qq d (Fin 2) (ZMod d))=2/Real.sin (Real.pi/(2*d)) ∧
    sSup (firstReducedBell '' closure (Qq d (Fin 2) (ZMod d)))=2/Real.sin (Real.pi/(2*d)) ∧
    sSup (firstReducedBell '' Qqc d (Fin 2) (ZMod d))=2/Real.sin (Real.pi/(2*d)) :=
  first_reduced_values_q_qa_qc hd

example (d : ℕ) [NeZero d] (hd : 2≤d) :
    sSup (firstAugmentedBell '' Qq d (Fin 2) (Option (ZMod d)))=2/Real.sin (Real.pi/(2*d))+1 ∧
    sSup (firstAugmentedBell '' closure (Qq d (Fin 2) (Option (ZMod d))))=2/Real.sin (Real.pi/(2*d))+1 ∧
    sSup (firstAugmentedBell '' Qqc d (Fin 2) (Option (ZMod d)))=2/Real.sin (Real.pi/(2*d))+1 :=
  first_augmented_values_q_qa_qc hd

example (d : ℕ) [NeZero d] (hd : 2≤d) :
    sSup (secondReducedBell '' Qq d (ZMod d) (ZMod d))=(d : ℝ) ∧
    sSup (secondReducedBell '' closure (Qq d (ZMod d) (ZMod d)))=(d : ℝ) ∧
    sSup (secondReducedBell '' Qqc d (ZMod d) (ZMod d))=(d : ℝ) :=
  second_reduced_values_q_qa_qc hd

example (d : ℕ) [NeZero d] (hd : 2≤d) :
    sSup (secondAugmentedBell '' Qq d (ZMod d) (Option (ZMod d)))=(d : ℝ)+1 ∧
    sSup (secondAugmentedBell '' closure (Qq d (ZMod d) (Option (ZMod d))))=(d : ℝ)+1 ∧
    sSup (secondAugmentedBell '' Qqc d (ZMod d) (Option (ZMod d)))=(d : ℝ)+1 :=
  second_augmented_values_q_qa_qc hd

example : sSup (binaryBell '' Qq 2 (Fin 2) (Fin 2))=3*Real.sqrt 3 ∧
    sSup (binaryBell '' closure (Qq 2 (Fin 2) (Fin 2)))=3*Real.sqrt 3 ∧
    sSup (binaryBell '' Qqc 2 (Fin 2) (Fin 2))=3*Real.sqrt 3 := binary_values_q_qa_qc

example (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (ψ : H) (hψ : ‖ψ‖=1) (a₀ a₁ b₀ b₁ : H →L[ℂ] H)
    (h₀ : star a₀=a₀ ∧ a₀*a₀=1) (h₁ : star a₁=a₁ ∧ a₁*a₁=1)
    (k₀ : star b₀=b₀ ∧ b₀*b₀=1) (k₁ : star b₁=b₁ ∧ b₁*b₁=1)
    (h00 : a₀*b₀=b₀*a₀) (h01 : a₀*b₁=b₁*a₀)
    (h10 : a₁*b₀=b₀*a₁) (h11 : a₁*b₁=b₁*a₁) :
    (⟪ψ, (a₀*b₀-(2:ℂ) • (a₀*b₁)+(2:ℂ) • (a₁*b₀)+(2:ℂ) • (a₁*b₁)) ψ⟫_ℂ).re ≤
      3*Real.sqrt 3 := binary_commuting_hilbert_upper ψ hψ a₀ a₁ b₀ b₁ h₀ h₁ k₀ k₁ h00 h01 h10 h11

example (d : ℕ) [NeZero d] (hd : 4≤d) :
    let s := firstPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
    firstAugmentedBell (General.behavior s)=betaQ (firstAugmentedBell (d := d)) ∧
    firstAugmentedBell (General.behavior s)=betaQa (firstAugmentedBell (d := d)) ∧
    firstAugmentedBell (General.behavior s)=betaQc (firstAugmentedBell (d := d)) ∧
    ∃ g : ZMod d×ZMod d,1/(d : ℝ)^2<General.fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g :=
  first_three_model_physical_guessing_gap hd

example (d : ℕ) [NeZero d] (hd : 4≤d) :
    let s := secondPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
    secondAugmentedBell (General.behavior s)=betaQ (secondAugmentedBell (d := d)) ∧
    secondAugmentedBell (General.behavior s)=betaQa (secondAugmentedBell (d := d)) ∧
    secondAugmentedBell (General.behavior s)=betaQc (secondAugmentedBell (d := d)) ∧
    ∃ g : ZMod d×ZMod d,1/(d : ℝ)^2<General.fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g :=
  second_three_model_physical_guessing_gap hd

example {X O : Type*} [Fintype X] [Fintype O] [DecidableEq X] [DecidableEq O]
    {A : X → Type*} [∀ x,Fintype (A x)] [∀ x,DecidableEq (A x)] [∀ x,Nonempty (A x)]
    (p : RightOneInputBehavior X O A) (x : X) (a : A x) (b : O) :
    bornProbability
      (storedPurification (rightHiddenWeight p)*(storedPurification (rightHiddenWeight p)).conjTranspose)
      (groupingProjector (fun assignment : StoredAssignments O A => assignment.2 x) a)
      (groupingProjector (fun assignment : StoredAssignments O A => assignment.1) b)=p.joint x a b :=
  (right_one_input_pure_projective_perfect_guess p).2.1 x a b

example : scalarMaximum 2=2*Real.sqrt 2 ∧ scalarMaximum 3=4 ∧
    scalarMaximum 4=2*Real.sqrt (4+2*Real.sqrt 2) ∧ scalarMaximum 5=2*(1+Real.sqrt 5) ∧
    scalarMaximum 6=2*(Real.sqrt 6+Real.sqrt 2) := small_dimension_exact_value_table

example : betaQ (firstAugmentedBell (d := 4))=2*Real.sqrt (4+2*Real.sqrt 2)+1 ∧
    betaQa (firstAugmentedBell (d := 4))=2*Real.sqrt (4+2*Real.sqrt 2)+1 ∧
    betaQc (firstAugmentedBell (d := 4))=2*Real.sqrt (4+2*Real.sqrt 2)+1 :=
  first_four_augmented_radical_values

example : ∃ p : BellBehavior 2 (Fin 2) (Fin 2),p∈Qq 2 (Fin 2) (Fin 2) ∧
    binaryBell p=3*Real.sqrt 3 ∧ BinaryPrivacyAt p 0 0 := binary_two_input_private_achievable

example (Y : Type) [Fintype Y] [DecidableEq Y]
    (p : OneInputBehavior Y (ZMod 2) (fun _ => ZMod 2)) (y : Y) :
    ¬ BinaryPrivacyAt (fun (_ : Unit) y a b => p.joint y a b) () y := left_one_input_no_binary_privacy p y

example (X : Type) [Fintype X] [DecidableEq X]
    (p : RightOneInputBehavior X (ZMod 2) (fun _ => ZMod 2)) (x : X) :
    ¬ BinaryPrivacyAt (fun x (_ : Unit) a b => p.joint x a b) x () := right_one_input_no_binary_privacy p x

example {ι κ ε : Type*} [Fintype ι] [Fintype κ] [Fintype ε]
    [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : PurifiedStrategyOn 2 (Fin 2) (Fin 2) ι κ ε)
    (hs : binaryBell (purifiedBehavior s)=3*Real.sqrt 3) (a b : ZMod 2) :
    partialE (kron (kron ((s.alice 0).effect a) ((s.bob 0).effect b)) (1 : Mat ε)*
      projector (fun p : (ι×κ)×ε => s.amplitude p.1 p.2)*
      (kron (kron ((s.alice 0).effect a) ((s.bob 0).effect b)) (1 : Mat ε)).conjTranspose)=
      (1/4 : ℂ) • reducedE s.amplitude := by
  rw [← conditionalE_actual_sandwich]
  exact binary_purified_saturation s hs a b

example (d : ℕ) [NeZero d] (w : ZMod d → ℂ) (hw : ∀ j,w j≠0) :
    (weightedCycle w).charpoly=Polynomial.X^d-Polynomial.C (∏ j,w j) :=
  weighted_cycle_charpoly w hw

end CyclicBell.ModelValueStatementAudit
