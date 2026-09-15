import CyclicBell
/- Deliberately false: the vectorized positive square root has norm one, not two. -/
noncomputable section
open CyclicBell CyclicBell.General
example : ‖purificationVector (entangledState 4)‖=2 := by
  have h := purificationVector_normalized (entangledState 4)
  linarith
