/- Uncompiled exact embedding certificate shard 0. -/
import Kourovka.Lattice.ScaledData
namespace Kourovka.Lattice.Checks
set_option Elab.async false
set_option maxRecDepth 200000
set_option maxHeartbeats 50000000
theorem embed_0 : EmbedCheck 0 := by
  intro j
  fin_cases j <;> decide +kernel
end Kourovka.Lattice.Checks
