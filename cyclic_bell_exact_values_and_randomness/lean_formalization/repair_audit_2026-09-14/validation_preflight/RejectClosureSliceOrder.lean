import CyclicBell.GeneralStatements
import CyclicBell.AdversarialStatements
import CyclicBell.Regression
import CyclicBell.GeneralCoverageSourceWeyl
noncomputable section
open CyclicBell CyclicBell.General
open scoped Topology
-- MUST FAIL: the closure of the exactly saturated subfamily can be smaller.
example : (0 : ℝ)∈closure {x : ℝ | 0<x ∧ x=0} := by
  have h := closure_before_slice_control.2
  aesop
