import CyclicBell.GeneralAdversarialValues

/-! Sharper d=4 guessing and conditional min-entropy bounds in all three
adversarial models. These are upper bounds on value-conditioned entropy, NOT
claims that the displayed finite witness is the worst adversary.  -/
noncomputable section
open scoped BigOperators Topology
namespace CyclicBell.General

/-- The already proved peak-excess estimate at lag two yields 3/32 for the
actual d=4 swapped target. This is stronger than the all-d displayed estimate. -/
theorem four_swappedTarget_three32 : ∃ a b : Ix 4,(3 : ℝ)/32≤swappedTarget 4 a b := by
  obtain ⟨a,b,h⟩ := exists_table_peak (swappedPhase : Ix 4 → ℂ) swappedPhase_unit
    (2 : Ix 4) (by decide)
  rw [swapped_R2_norm (by norm_num : 4≤4)] at h
  have hs : Real.sin (3*Real.pi/4)=Real.sin (Real.pi/4) := by
    rw [show 3*Real.pi/4=Real.pi-Real.pi/4 by ring,Real.sin_pi_sub]
  norm_num only [Nat.cast_ofNat] at h
  rw [hs,Real.sin_pi_div_four] at h
  refine ⟨a,b,?_⟩
  rw [swappedTarget_fourier]
  nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ)≤2)]

theorem first_four_Gval_three32 :
    (3 : ℝ)/32≤GvalQ (firstAugmentedBell (d := 4)) 1 none ∧
    (3 : ℝ)/32≤GvalQa (firstAugmentedBell (d := 4)) 1 none ∧
    (3 : ℝ)/32≤GvalQc (firstAugmentedBell (d := 4)) 1 none := by
  let s := firstPermutationStrategy (d := 4) (by norm_num : 2≤4) (finalSwap 4)
  obtain ⟨a,b,hab⟩ := four_swappedTarget_three32
  have hs : firstAugmentedBell (behavior s)=scalarMaximum 4+1 := by
    rw [firstAugmentedBell_behavior]
    exact firstPermutation_attains (by norm_num) _
  obtain ⟨hq,hqa,hqc⟩ := first_augmented_values_q_qa_qc (d := 4) (by norm_num)
  obtain ⟨h₁,h₂,h₃⟩ := three_model_Gval_interval s firstAugmentedBell 1 none (a,b)
    (hs.trans hq.symm) (hs.trans hqa.symm) (hs.trans hqc.symm)
  have hborn : (3 : ℝ)/32≤behavior s 1 none a b := by
    simpa only [s,firstSwap_target (by norm_num : 4≤4)] using hab
  exact ⟨hborn.trans h₁.1,hborn.trans h₂.1,hborn.trans h₃.1⟩

theorem second_four_Gval_three32 :
    (3 : ℝ)/32≤GvalQ (secondAugmentedBell (d := 4)) 1 none ∧
    (3 : ℝ)/32≤GvalQa (secondAugmentedBell (d := 4)) 1 none ∧
    (3 : ℝ)/32≤GvalQc (secondAugmentedBell (d := 4)) 1 none := by
  let s := secondPermutationStrategy (d := 4) (by norm_num : 2≤4) (finalSwap 4)
  obtain ⟨a,b,hab⟩ := four_swappedTarget_three32
  have hs : secondAugmentedBell (behavior s)=(4 : ℝ)+1 := by
    rw [secondAugmentedBell_behavior]
    exact secondPermutation_attains (by norm_num) _
  obtain ⟨hq,hqa,hqc⟩ := second_augmented_values_q_qa_qc (d := 4) (by norm_num)
  obtain ⟨h₁,h₂,h₃⟩ := three_model_Gval_interval s secondAugmentedBell 1 none (a,b)
    (hs.trans hq.symm) (hs.trans hqa.symm) (hs.trans hqc.symm)
  have hborn : (3 : ℝ)/32≤behavior s 1 none a b := by
    simpa only [s,second_first_target_same,firstSwap_target (by norm_num : 4≤4)] using hab
  exact ⟨hborn.trans h₁.1,hborn.trans h₂.1,hborn.trans h₃.1⟩

def guessingMinEntropy (g : ℝ) : ℝ := -(Real.log g/Real.log 2)

theorem guessingMinEntropy_antitone {a b : ℝ} (ha : 0<a) (hab : a≤b) :
    guessingMinEntropy b≤guessingMinEntropy a := by
  unfold guessingMinEntropy
  apply neg_le_neg
  apply div_le_div_of_nonneg_right _ (le_of_lt (Real.log_pos (by norm_num : (1 : ℝ)<2)))
  exact Real.log_le_log ha hab

theorem first_four_value_entropy_upper :
    guessingMinEntropy (GvalQ (firstAugmentedBell (d := 4)) 1 none)≤5-Real.log 3/Real.log 2 ∧
    guessingMinEntropy (GvalQa (firstAugmentedBell (d := 4)) 1 none)≤5-Real.log 3/Real.log 2 ∧
    guessingMinEntropy (GvalQc (firstAugmentedBell (d := 4)) 1 none)≤5-Real.log 3/Real.log 2 := by
  obtain ⟨h₁,h₂,h₃⟩ := first_four_Gval_three32
  have h (g : ℝ) (hg : (3 : ℝ)/32≤g) : guessingMinEntropy g≤5-Real.log 3/Real.log 2 := by
    exact (guessingMinEntropy_antitone (by norm_num : (0 : ℝ)<3/32) hg).trans_eq d4_entropy_exact
  exact ⟨h _ h₁,h _ h₂,h _ h₃⟩

theorem second_four_value_entropy_upper :
    guessingMinEntropy (GvalQ (secondAugmentedBell (d := 4)) 1 none)≤5-Real.log 3/Real.log 2 ∧
    guessingMinEntropy (GvalQa (secondAugmentedBell (d := 4)) 1 none)≤5-Real.log 3/Real.log 2 ∧
    guessingMinEntropy (GvalQc (secondAugmentedBell (d := 4)) 1 none)≤5-Real.log 3/Real.log 2 := by
  obtain ⟨h₁,h₂,h₃⟩ := second_four_Gval_three32
  have h (g : ℝ) (hg : (3 : ℝ)/32≤g) : guessingMinEntropy g≤5-Real.log 3/Real.log 2 := by
    exact (guessingMinEntropy_antitone (by norm_num : (0 : ℝ)<3/32) hg).trans_eq d4_entropy_exact
  exact ⟨h _ h₁,h _ h₂,h _ h₃⟩

/-- Does not claim optimality: any probability at least 3/32 has entropy
strictly below four. Positivity comes from the lower bound, not a caller's
assumption that a real logarithm has a probability interpretation. -/
theorem first_four_value_entropy_strict :
    guessingMinEntropy (GvalQ (firstAugmentedBell (d := 4)) 1 none)<4 ∧
    guessingMinEntropy (GvalQa (firstAugmentedBell (d := 4)) 1 none)<4 ∧
    guessingMinEntropy (GvalQc (firstAugmentedBell (d := 4)) 1 none)<4 := by
  obtain ⟨h₁,h₂,h₃⟩ := first_four_value_entropy_upper
  have he : 5-Real.log 3/Real.log 2<4 := by simpa only [d4_entropy_exact] using d4_entropy_less_than_four
  exact ⟨h₁.trans_lt he,h₂.trans_lt he,h₃.trans_lt he⟩

theorem second_four_value_entropy_strict :
    guessingMinEntropy (GvalQ (secondAugmentedBell (d := 4)) 1 none)<4 ∧
    guessingMinEntropy (GvalQa (secondAugmentedBell (d := 4)) 1 none)<4 ∧
    guessingMinEntropy (GvalQc (secondAugmentedBell (d := 4)) 1 none)<4 := by
  obtain ⟨h₁,h₂,h₃⟩ := second_four_value_entropy_upper
  have he : 5-Real.log 3/Real.log 2<4 := by simpa only [d4_entropy_exact] using d4_entropy_less_than_four
  exact ⟨h₁.trans_lt he,h₂.trans_lt he,h₃.trans_lt he⟩

end CyclicBell.General
