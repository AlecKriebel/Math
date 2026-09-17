import CyclicBell.GeneralCorrelationValues
import CyclicBell.GeneralConsequences

/-! The nonuniform physical witnesses maximize the literal model suprema.
Membership, value and Born distribution use the same witness throughout.
No optimality claim for Eve is made. -/
noncomputable section
open scoped BigOperators ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

/-- Simultaneous membership uses a genuine finite realization, followed by
closure inclusion and the separately constructed Hilbert-space embedding. -/
theorem finite_behavior_in_three_models {α β ι κ : Type} [Fintype ι] [Fintype κ]
    [DecidableEq ι] [DecidableEq κ] (s : StrategyOn d α β ι κ) :
    behavior s ∈ Qq d α β ∧ behavior s ∈ Qqa d α β ∧ behavior s ∈ Qqc d α β := by
  have h := behavior_mem_Qq s
  exact ⟨h,Qq_subset_Qqa h,Qq_subset_Qqc h⟩

/-- Source sec:randomness, first family, now referencing all three actual
model optima. The target probabilities are the same physical Born array in
membership, score and nonuniformity. -/
theorem first_three_model_counterexample (hd : 4≤d) :
    ∃ s : StrategyOn d (Fin 2) (AugmentedInputs d) (Ix d) (Ix d),
      (behavior s ∈ Qq d (Fin 2) (AugmentedInputs d) ∧
        behavior s ∈ Qqa d (Fin 2) (AugmentedInputs d) ∧
        behavior s ∈ Qqc d (Fin 2) (AugmentedInputs d)) ∧
      firstAugmentedBell (behavior s)=betaQ (firstAugmentedBell (d := d)) ∧
      firstAugmentedBell (behavior s)=betaQa (firstAugmentedBell (d := d)) ∧
      firstAugmentedBell (behavior s)=betaQc (firstAugmentedBell (d := d)) ∧
      (¬ ∀ a b,behavior s 1 none a b=1/(d : ℝ)^2) ∧
      (∀ a b,(∑ b',behavior s 1 none a b')=1/(d : ℝ) ∧
        (∑ a',behavior s 1 none a' b)=1/(d : ℝ)) ∧
      (∃ a b,1/(d : ℝ)^2+
        2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
          ((d : ℝ)^2*((d : ℝ)-1)) ≤ behavior s 1 none a b) := by
  let s := firstPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
  have hs : firstAugmentedBell (behavior s)=scalarMaximum d+1 := by
    rw [firstAugmentedBell_behavior]
    exact firstPermutation_attains (by omega) _
  obtain ⟨hq,hqa,hqc⟩ := first_augmented_values_q_qa_qc (d := d) (by omega : 2≤d)
  refine ⟨s,finite_behavior_in_three_models s,hs.trans hq.symm,hs.trans hqa.symm,
    hs.trans hqc.symm,?_,?_,?_⟩
  · simpa only [s,firstSwap_target hd] using swappedTarget_not_uniform (d := d) hd
  · intro a b
    simp only [s,firstSwap_target hd]
    exact swappedTarget_marginals a b
  · simpa only [s,firstSwap_target hd] using swappedTarget_quantitative (d := d) hd

/-- Parallel second-family endpoint. Its score is not substituted for family I. -/
theorem second_three_model_counterexample (hd : 4≤d) :
    ∃ s : StrategyOn d (Ix d) (AugmentedInputs d) (Ix d) (Ix d),
      (behavior s ∈ Qq d (Ix d) (AugmentedInputs d) ∧
        behavior s ∈ Qqa d (Ix d) (AugmentedInputs d) ∧
        behavior s ∈ Qqc d (Ix d) (AugmentedInputs d)) ∧
      secondAugmentedBell (behavior s)=betaQ (secondAugmentedBell (d := d)) ∧
      secondAugmentedBell (behavior s)=betaQa (secondAugmentedBell (d := d)) ∧
      secondAugmentedBell (behavior s)=betaQc (secondAugmentedBell (d := d)) ∧
      (¬ ∀ a b,behavior s 1 none a b=1/(d : ℝ)^2) ∧
      (∀ a b,(∑ b',behavior s 1 none a b')=1/(d : ℝ) ∧
        (∑ a',behavior s 1 none a' b)=1/(d : ℝ)) ∧
      (∃ a b,1/(d : ℝ)^2+
        2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
          ((d : ℝ)^2*((d : ℝ)-1)) ≤ behavior s 1 none a b) := by
  let s := secondPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
  have hs : secondAugmentedBell (behavior s)=(d : ℝ)+1 := by
    rw [secondAugmentedBell_behavior]
    exact secondPermutation_attains (by omega) _
  obtain ⟨hq,hqa,hqc⟩ := second_augmented_values_q_qa_qc (d := d) (by omega : 2≤d)
  refine ⟨s,finite_behavior_in_three_models s,hs.trans hq.symm,hs.trans hqa.symm,
    hs.trans hqc.symm,?_,?_,?_⟩
  · simpa only [s,second_first_target_same,firstSwap_target hd]
      using swappedTarget_not_uniform (d := d) hd
  · intro a b
    simp only [s,second_first_target_same,firstSwap_target hd]
    exact swappedTarget_marginals a b
  · simpa only [s,second_first_target_same,firstSwap_target hd]
      using swappedTarget_quantitative (d := d) hd

/-- One explicit realization maximizes every scalar model value and permits a
physical fixed-pair guess beating the uniform benchmark. This is NOT a supremum
over all adversaries or all maximizing realizations. -/
theorem first_three_model_physical_guessing_gap (hd : 4≤d) :
    let s := firstPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
    firstAugmentedBell (behavior s)=betaQ (firstAugmentedBell (d := d)) ∧
    firstAugmentedBell (behavior s)=betaQa (firstAugmentedBell (d := d)) ∧
    firstAugmentedBell (behavior s)=betaQc (firstAugmentedBell (d := d)) ∧
    ∃ g : Ix d×Ix d,1/(d : ℝ)^2<fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g := by
  dsimp only
  have hs := (first_all_dimension_physical_Eve_gap (d := d) hd)
  obtain ⟨hq,hqa,hqc⟩ := first_augmented_values_q_qa_qc (d := d) (by omega : 2≤d)
  simp only [firstAugmentedBell_behavior]
  exact ⟨hs.1.trans hq.symm,hs.1.trans hqa.symm,hs.1.trans hqc.symm,hs.2⟩

theorem second_three_model_physical_guessing_gap (hd : 4≤d) :
    let s := secondPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
    secondAugmentedBell (behavior s)=betaQ (secondAugmentedBell (d := d)) ∧
    secondAugmentedBell (behavior s)=betaQa (secondAugmentedBell (d := d)) ∧
    secondAugmentedBell (behavior s)=betaQc (secondAugmentedBell (d := d)) ∧
    ∃ g : Ix d×Ix d,1/(d : ℝ)^2<fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g := by
  dsimp only
  have hs := second_all_dimension_physical_Eve_gap (d := d) hd
  obtain ⟨hq,hqa,hqc⟩ := second_augmented_values_q_qa_qc (d := d) (by omega : 2≤d)
  simp only [secondAugmentedBell_behavior]
  exact ⟨hs.1.trans hq.symm,hs.1.trans hqa.symm,hs.1.trans hqc.symm,hs.2⟩

end CyclicBell.General
