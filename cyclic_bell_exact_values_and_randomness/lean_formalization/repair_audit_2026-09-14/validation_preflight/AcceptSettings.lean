import CyclicBell.GeneralPhaseEntropy
noncomputable section
open scoped BigOperators Topology
open CyclicBell CyclicBell.General
example : (∑ a : ZMod 5,∑ b : ZMod 5,
    phasePairProbability (0 : ℝ) (-1/4) a b)=1 := phasePair_normalized _ _
example : behavior (anchoredStandardStrategy 2 0) 1 none (0 : ZMod 2) 0=1/4 :=
  anchored_qubit_cross_uniform 0 1 (by decide) 0 0
example : 1/(5 : ℝ)^2<standardPeak 5 := standardPeak_gt_uniform (by norm_num)
example : Filter.Tendsto (fun d : ℕ => standardJointMinEntropy d-Real.log (d : ℝ)/Real.log 2)
    Filter.atTop (nhds (Real.log (Real.pi^2/8)/Real.log 2)) := standard_entropy_asymptotic
