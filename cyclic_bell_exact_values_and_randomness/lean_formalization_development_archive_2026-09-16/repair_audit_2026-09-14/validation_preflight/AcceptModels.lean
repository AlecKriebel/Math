import CyclicBell.GeneralStatements
import CyclicBell.AdversarialStatements
import CyclicBell.Regression
import CyclicBell.GeneralCoverageSourceWeyl
noncomputable section
open CyclicBell CyclicBell.General
open scoped Topology BigOperators
example : betaQc (secondReducedBell (d := 5))=5 :=
  (second_reduced_values_q_qa_qc (d := 5) (by norm_num)).2.2
example : betaQa (secondAugmentedBell (d := 5))=6 :=
  by convert (second_augmented_values_q_qa_qc (d := 5) (by norm_num)).2.1 using 1 <;> norm_num
example : betaQ binaryBell=3*Real.sqrt 3 := binary_values_q_qa_qc.1
example (nA nB : ℕ) (s : StrategyOn 4 (Fin 2) (AugmentedInputs 4) (Fin nA) (Fin nB)) :
    commutingBehavior (finiteToCommuting s)=behavior s := finiteToCommuting_behavior s
example : Qqa 4 (Fin 2) (AugmentedInputs 4)=closure (Qq 4 (Fin 2) (AugmentedInputs 4)) := rfl

example (d : ℕ) [NeZero d] (w : ZMod d → ℂ) (hw : ∀ j,w j≠0) :
    (weightedCycle w).charpoly=Polynomial.X^d-Polynomial.C (∏ j,w j) :=
  weighted_cycle_charpoly w hw
