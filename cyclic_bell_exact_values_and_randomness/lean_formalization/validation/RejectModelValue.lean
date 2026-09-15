import CyclicBell
/- Deliberately false: confuses the reduced and augmented second-family value.
An actual proof failure is required; missing imports or identifiers do not pass. -/
noncomputable section
open CyclicBell CyclicBell.General
example : betaQc (secondReducedBell (d := 5))=6 := by
  have h := (second_reduced_values_q_qa_qc (d := 5) (by norm_num)).2.2
  linarith
