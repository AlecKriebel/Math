/- Uncompiled finite proof shard 2. No external execution is trusted by these declarations. -/
import Kourovka.Ambient.IntData
namespace Kourovka.Ambient.IntData.Checks
set_option Elab.async false
set_option maxRecDepth 200000
set_option maxHeartbeats 50000000

theorem term_2 : TermCheck 2 := by
  intro j
  fin_cases j <;> decide +kernel

theorem jacobi_2 : JacobiCheck 2 := by
  intro j
  fin_cases j <;> decide +kernel
end Kourovka.Ambient.IntData.Checks
