import CyclicBell.GeneralCorrelationValues
/- Deliberately false: the actual closure cannot raise the attained maximum. -/
noncomputable section
open CyclicBell CyclicBell.General
example : betaQa (secondAugmentedBell (d := 5))=7 := by
  have hn : betaQa (secondAugmentedBell (d := 5))≠7 := by
    have h := (second_augmented_values_q_qa_qc (d := 5) (by norm_num)).2.1
    norm_num at h
    linarith
  simp only [hn]
