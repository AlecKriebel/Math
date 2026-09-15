import CyclicBell.GeneralHilbertBridge
import CyclicBell.GeneralSecondWitness

/-!
Literal three-model suprema for both cyclic families, reduced and augmented.
Q_q uses arbitrary finite local coordinate spaces and mixed states. Q_qa is the
actual product-topology closure. Q_qc uses genuine commuting PVM vector states
on complete complex Hilbert spaces. An explicit purification proves Q_q⊆Q_qc.
The value proof does not need, and does not claim, Q_qa⊆Q_qc or closedness of Q_qc.
All declarations are UNCOMPILED SOURCE CANDIDATES, not accepted Lean theorems.
-/
noncomputable section
open scoped BigOperators ComplexOrder Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

/-- Finite tensor model, with no dimension bound, full-rank assumption, or Bell
condition in membership. Existential instance data fixes the physical carriers. -/
def Qq (d : ℕ) [NeZero d] (α β : Type) : Set (BellBehavior d α β) :=
  {p | ∃ (ι κ : Type) (fι : Fintype ι) (fκ : Fintype κ),
    letI := fι
    letI := fκ
    ∃ (eι : DecidableEq ι) (eκ : DecidableEq κ),
    letI := eι
    letI := eκ
    ∃ s : StrategyOn d α β ι κ, behavior s = p}

/-- The closure in the actual finite real behavior coordinates. -/
def Qqa (d : ℕ) [NeZero d] (α β : Type) : Set (BellBehavior d α β) := closure (Qq d α β)

/-- No finite-dimensional hypothesis appears in the commuting model. Lean's
small carrier universe is a size convention, not a Hilbert-dimension bound. -/
def Qqc (d : ℕ) [NeZero d] (α β : Type) : Set (BellBehavior d α β) :=
  {p | ∃ (H : Type) (nH : NormedAddCommGroup H),
    letI := nH
    ∃ (iH : InnerProductSpace ℂ H),
    letI := iH
    ∃ (cH : CompleteSpace H),
    letI := cH
    ∃ s : CommutingOn d α β H, commutingBehavior s = p}

def betaQ {α β : Type} (f : BellBehavior d α β → ℝ) : ℝ := bellSupremum (Qq d α β) f
def betaQa {α β : Type} (f : BellBehavior d α β → ℝ) : ℝ := bellSupremum (Qqa d α β) f
def betaQc {α β : Type} (f : BellBehavior d α β → ℝ) : ℝ := bellSupremum (Qqc d α β) f

theorem behavior_mem_Qq {α β ι κ : Type} [Fintype ι] [Fintype κ]
    [DecidableEq ι] [DecidableEq κ] (s : StrategyOn d α β ι κ) : behavior s ∈ Qq d α β := by
  exact ⟨ι,κ,inferInstance,inferInstance,inferInstance,inferInstance,s,rfl⟩

theorem commutingBehavior_mem_Qqc {α β H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (s : CommutingOn d α β H) :
    commutingBehavior s ∈ Qqc d α β := by
  exact ⟨H,inferInstance,inferInstance,inferInstance,s,rfl⟩

theorem Qq_subset_Qqa {α β : Type} : Qq d α β ⊆ Qqa d α β := subset_closure

/-- Membership transfer is supplied by the actual purification/measurement
construction, not by a universal-embedding premise. -/
theorem Qq_subset_Qqc {α β : Type} : Qq d α β ⊆ Qqc d α β := by
  intro p hp
  rcases hp with ⟨ι,κ,fι,fκ,eι,eκ,s,rfl⟩
  letI := fι
  letI := fκ
  letI := eι
  letI := eκ
  rw [← finiteToCommuting_behavior s]
  exact commutingBehavior_mem_Qqc (finiteToCommuting s)

theorem Qqc_probability_nonnegative {α β : Type} (p : BellBehavior d α β)
    (hp : p ∈ Qqc d α β) (x : α) (y : β) (a b : Ix d) : 0 ≤ p x y a b := by
  rcases hp with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  exact commutingBehavior_nonnegative s x y a b

theorem Qqc_probability_normalized {α β : Type} (p : BellBehavior d α β)
    (hp : p ∈ Qqc d α β) (x : α) (y : β) : (∑ a,∑ b,p x y a b)=1 := by
  rcases hp with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  exact commutingBehavior_normalized s x y

theorem firstReducedBell_Qqc_upper (hd : 2≤d) (p : BellBehavior d (Fin 2) (Ix d))
    (hp : p ∈ Qqc d (Fin 2) (Ix d)) : firstReducedBell p ≤ scalarMaximum d := by
  rcases hp with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  exact firstReducedBell_commuting_upper hd s

theorem firstAugmentedBell_Qqc_upper (hd : 2≤d)
    (p : BellBehavior d (Fin 2) (AugmentedInputs d))
    (hp : p ∈ Qqc d (Fin 2) (AugmentedInputs d)) : firstAugmentedBell p ≤ scalarMaximum d+1 := by
  rcases hp with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  exact firstAugmentedBell_commuting_upper hd s

theorem secondReducedBell_Qqc_upper (hd : 2≤d) (p : BellBehavior d (Ix d) (Ix d))
    (hp : p ∈ Qqc d (Ix d) (Ix d)) : secondReducedBell p ≤ (d : ℝ) := by
  rcases hp with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  exact secondReducedBell_commuting_upper hd s

theorem secondAugmentedBell_Qqc_upper (hd : 2≤d)
    (p : BellBehavior d (Ix d) (AugmentedInputs d))
    (hp : p ∈ Qqc d (Ix d) (AugmentedInputs d)) : secondAugmentedBell p ≤ (d : ℝ)+1 := by
  rcases hp with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  exact secondAugmentedBell_commuting_upper hd s

/-- An actual strategy on the reduced Bob alphabet. The added measurement is
not retained as a hidden restriction in the reduced model. -/
def firstReducedStrategy (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    StrategyOn d (Fin 2) (Ix d) (Ix d) (Ix d) :=
  pullStrategy (firstPermutationStrategy hd σ) id some

def secondReducedStrategy (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    StrategyOn d (Ix d) (Ix d) (Ix d) (Ix d) :=
  pullStrategy (secondPermutationStrategy hd σ) id some

theorem firstPermutation_aligned_correlator (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    (probabilityCorrelator (behavior (firstPermutationStrategy hd σ)) 0 none).re=1 := by
  rw [probabilityCorrelator_behavior]
  change stateEval (entangledState d).density
    (kron (encoded (permutationAlice hd σ 0)) (encoded (permutationBob σ none)))=1
  rw [permutationAlice_zero,permutationBob_none,entangled_stateEval,
    (added_first_harmonics (equalityRoot : Ix d → ℂ) σ).1]
  rfl

theorem secondPermutation_aligned_correlator (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    (probabilityCorrelator (behavior (secondPermutationStrategy hd σ)) 0 none).re=1 := by
  rw [probabilityCorrelator_behavior]
  change stateEval (entangledState d).density
    (kron (encoded (secondAlice hd σ 0)) (encoded (permutationBob σ none)))=1
  rw [secondAlice_zero,permutationBob_none,entangled_stateEval,
    (added_first_harmonics (equalityRoot : Ix d → ℂ) σ).1]
  rfl

theorem firstReducedStrategy_attains (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    firstReducedBell (behavior (firstReducedStrategy hd σ))=scalarMaximum d := by
  have h : firstReducedBell (pullBehavior id some (behavior (firstPermutationStrategy hd σ)))+1 =
      scalarMaximum d+1 := by
    calc
      _ = firstAugmentedBell (behavior (firstPermutationStrategy hd σ)) := by
        rw [firstAugmentedBell,firstPermutation_aligned_correlator]
      _ = firstValue (firstPermutationStrategy hd σ) := firstAugmentedBell_behavior _
      _ = scalarMaximum d+1 := firstPermutation_attains hd σ
  exact add_right_cancel h

theorem secondReducedStrategy_attains (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    secondReducedBell (behavior (secondReducedStrategy hd σ))=(d : ℝ) := by
  have h : secondReducedBell (pullBehavior id some (behavior (secondPermutationStrategy hd σ)))+1 =
      (d : ℝ)+1 := by
    calc
      _ = secondAugmentedBell (behavior (secondPermutationStrategy hd σ)) := by
        rw [secondAugmentedBell,secondPermutation_aligned_correlator]
      _ = secondValue (secondPermutationStrategy hd σ) := secondAugmentedBell_behavior _
      _ = (d : ℝ)+1 := secondPermutation_attains hd σ
  exact add_right_cancel h

/-- Manuscript thm:exact, literal finite/closure/commuting suprema. -/
theorem first_reduced_values_q_qa_qc (hd : 2≤d) :
    betaQ (firstReducedBell (d := d)) = 2/Real.sin (Real.pi/(2*d)) ∧
    betaQa (firstReducedBell (d := d)) = 2/Real.sin (Real.pi/(2*d)) ∧
    betaQc (firstReducedBell (d := d)) = 2/Real.sin (Real.pi/(2*d)) := by
  let s := firstReducedStrategy hd (Equiv.refl (Ix d))
  exact three_model_suprema (Qq d (Fin 2) (Ix d)) (Qqc d (Fin 2) (Ix d))
    firstReducedBell firstReducedBell_continuous (scalarMaximum d) Qq_subset_Qqc
    (firstReducedBell_Qqc_upper hd) (behavior s) (behavior_mem_Qq s)
    (firstReducedStrategy_attains hd _)

/-- Manuscript cor:first-augmented with its authoritative operator normalization. -/
theorem first_augmented_values_q_qa_qc (hd : 2≤d) :
    betaQ (firstAugmentedBell (d := d)) = 2/Real.sin (Real.pi/(2*d))+1 ∧
    betaQa (firstAugmentedBell (d := d)) = 2/Real.sin (Real.pi/(2*d))+1 ∧
    betaQc (firstAugmentedBell (d := d)) = 2/Real.sin (Real.pi/(2*d))+1 := by
  let s := firstPermutationStrategy hd (Equiv.refl (Ix d))
  apply three_model_suprema (Qq d (Fin 2) (AugmentedInputs d))
    (Qqc d (Fin 2) (AugmentedInputs d)) firstAugmentedBell firstAugmentedBell_continuous
    (scalarMaximum d+1) Qq_subset_Qqc (firstAugmentedBell_Qqc_upper hd)
    (behavior s) (behavior_mem_Qq s)
  rw [firstAugmentedBell_behavior]
  exact firstPermutation_attains hd _

/-- Source SOS value, now as three actual reduced-model suprema. -/
theorem second_reduced_values_q_qa_qc (hd : 2≤d) :
    betaQ (secondReducedBell (d := d)) = (d : ℝ) ∧
    betaQa (secondReducedBell (d := d)) = (d : ℝ) ∧
    betaQc (secondReducedBell (d := d)) = (d : ℝ) := by
  let s := secondReducedStrategy hd (Equiv.refl (Ix d))
  exact three_model_suprema (Qq d (Ix d) (Ix d)) (Qqc d (Ix d) (Ix d))
    secondReducedBell secondReducedBell_continuous (d : ℝ) Qq_subset_Qqc
    (secondReducedBell_Qqc_upper hd) (behavior s) (behavior_mem_Qq s)
    (secondReducedStrategy_attains hd _)

theorem second_augmented_values_q_qa_qc (hd : 2≤d) :
    betaQ (secondAugmentedBell (d := d)) = (d : ℝ)+1 ∧
    betaQa (secondAugmentedBell (d := d)) = (d : ℝ)+1 ∧
    betaQc (secondAugmentedBell (d := d)) = (d : ℝ)+1 := by
  let s := secondPermutationStrategy hd (Equiv.refl (Ix d))
  apply three_model_suprema (Qq d (Ix d) (AugmentedInputs d))
    (Qqc d (Ix d) (AugmentedInputs d)) secondAugmentedBell secondAugmentedBell_continuous
    ((d : ℝ)+1) Qq_subset_Qqc (secondAugmentedBell_Qqc_upper hd)
    (behavior s) (behavior_mem_Qq s)
  rw [secondAugmentedBell_behavior]
  exact secondPermutation_attains hd _

end CyclicBell.General
