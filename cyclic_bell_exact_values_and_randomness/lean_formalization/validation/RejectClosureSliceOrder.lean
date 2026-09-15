import CyclicBell.GeneralAdversarialRegression
noncomputable section
open CyclicBell CyclicBell.General
open scoped Topology
-- MUST FAIL: the closure of the exactly saturated subfamily can be smaller.
example : (0 : ℝ)∈closure {x : ℝ | 0<x ∧ x=0} := by
  simp only [closure_before_slice_control.2]
