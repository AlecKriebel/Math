import CyclicBell.GeneralPhaseEntropy

/-! Expanded physical contracts for the added settings appendix.  -/
noncomputable section
open scoped BigOperators Matrix Topology
namespace CyclicBell.PhaseTableAudit
open General

example (d : ℕ) [NeZero d] (α β : ℝ) :
    (∑ a : ZMod d,∑ b : ZMod d,
      (Matrix.trace ((entangledState d).density *
        kron ((phaseAlice α).effect a) ((phaseBob β).effect b))).re)=1 :=
  phasePair_normalized α β

example (d : ℕ) [NeZero d] (α β : ℝ) :
    (∀ a : ZMod d,∑ b : ZMod d,phasePairProbability α β a b=1/(d : ℝ)) ∧
    (∀ b : ZMod d,∑ a : ZMod d,phasePairProbability α β a b=1/(d : ℝ)) :=
  phasePair_marginals α β

example (d : ℕ) [NeZero d] (hd : 2≤d) (x y : Fin 2) (a b : ZMod d) :
    (Matrix.trace ((standardPhaseStrategy d).state.density *
      kron (((standardPhaseStrategy d).alice x).effect a)
        (((standardPhaseStrategy d).bob y).effect b))).re=
      (1/2 : ℝ)/((d : ℝ)^3*Real.sin
        (Real.pi*((a.val : ℝ)-(b.val : ℝ)+standardDelta x y)/d)^2) :=
  standard_behavior_formula hd x y a b

example (d : ℕ) [NeZero d] (hd : 2≤d) (x y : Fin 2) :
    (∀ a b : ZMod d,behavior (standardPhaseStrategy d) x y a b≤standardPeak d) ∧
    (∃ a b : ZMod d,behavior (standardPhaseStrategy d) x y a b=standardPeak d) ∧
    1/(d : ℝ)^2<standardPeak d ∧
    ¬(∀ a b : ZMod d,behavior (standardPhaseStrategy d) x y a b=1/(d : ℝ)^2) :=
  standard_tables_nonuniform hd x y

example (d : ℕ) [NeZero d] (c : Fin 2) (a b : ZMod d) :
    behavior (anchoredStandardStrategy d c) c none a b=
      if a=b then 1/(d : ℝ) else 0 := anchored_matching c a b

example (d : ℕ) [NeZero d] (hd : 3≤d) (c x : Fin 2) (hxc : x≠c) :
    1/(d : ℝ)^2<behavior (anchoredStandardStrategy d c) x none 0 0 := by
  rw [anchored_cross_hits_peak (by omega : 2≤d) c x hxc]
  exact anchorPeak_gt_uniform hd

example (c x : Fin 2) (hxc : x≠c) (a b : ZMod 2) :
    behavior (anchoredStandardStrategy 2 c) x none a b=1/4 :=
  anchored_qubit_cross_uniform c x hxc a b

example : Filter.Tendsto
    (fun d : ℕ => standardJointMinEntropy d-Real.log (d : ℝ)/Real.log 2)
    Filter.atTop (nhds (Real.log (Real.pi^2/8)/Real.log 2)) :=
  standard_entropy_asymptotic

end CyclicBell.PhaseTableAudit
