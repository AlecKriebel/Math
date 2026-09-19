/- Exact embedding certificate shard 1, using proved basis-coordinate reductions. -/
import Kourovka.Lattice.EmbeddingBasis
import Kourovka.Ambient.Lie
namespace Kourovka.Lattice.Checks
open Kourovka.Ambient
set_option Elab.async false
set_option maxRecDepth 200000
set_option maxHeartbeats 50000000
theorem embed_1 : EmbedCheck 1 := by
  intro j
  fin_cases j <;>
    simp only [embed_unit, LB_basis_coeff] <;>
    norm_num only [originalBasis] <;>
    simp only [map_add, map_smul, LinearMap.add_apply, LinearMap.smul_apply,
      basis_bracket] <;>
    decide +kernel
end Kourovka.Lattice.Checks
