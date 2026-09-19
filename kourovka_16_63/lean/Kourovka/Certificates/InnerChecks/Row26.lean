/- Exact kernel-checked row of the rational left-inverse witness. -/
import Kourovka.Certificates.InnerWitnessData
set_option Elab.async false
set_option maxRecDepth 200000
set_option maxHeartbeats 50000000
namespace Kourovka.Certificates.InnerRank
theorem leftInverse_26 : LeftInverseCheck 26 := by
  intro j
  simp only [inner_entry_fast]
  fin_cases j <;> decide +kernel
end Kourovka.Certificates.InnerRank
