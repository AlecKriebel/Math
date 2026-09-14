import SymmetricSector.Small03
import SymmetricSector.Small04
import SymmetricSector.Small05
import SymmetricSector.Small06
import SymmetricSector.Small07
import SymmetricSector.Small08
import SymmetricSector.Small09
import SymmetricSector.Small10
import SymmetricSector.Small11
import SymmetricSector.Small12
import SymmetricSector.Small13
import SymmetricSector.Small14
import SymmetricSector.Small15
import SymmetricSector.Small16
import SymmetricSector.Small17
import SymmetricSector.Small18
import SymmetricSector.Small19
import SymmetricSector.Small20
import SymmetricSector.Small21
import SymmetricSector.Small22
import SymmetricSector.Small23
import SymmetricSector.Small24
import SymmetricSector.Small25
import SymmetricSector.Small26
import SymmetricSector.Small27
import SymmetricSector.Small28
import SymmetricSector.Small29
import SymmetricSector.Small30
import SymmetricSector.Small31
import SymmetricSector.Small32
import SymmetricSector.Small33
import SymmetricSector.Small34
import SymmetricSector.Small35
import SymmetricSector.Small36
import SymmetricSector.Small37
import SymmetricSector.Small38
import SymmetricSector.Small39

namespace SymmetricSector

/-- The first range of the exact finite symmetric-sector lemma, including both endpoints.
Every case uses a checked solution witness and independently proved invertibility. -/
theorem finite_small_scalar_pos (N : ℕ) (h₃ : 3 ≤ N) (h₃₉ : N ≤ 39) :
    0 < reducedScalar N := by
  interval_cases N
  · exact Cert3.positive
  · exact Cert4.positive
  · exact Cert5.positive
  · exact Cert6.positive
  · exact Cert7.positive
  · exact Cert8.positive
  · exact Cert9.positive
  · exact Cert10.positive
  · exact Cert11.positive
  · exact Cert12.positive
  · exact Cert13.positive
  · exact Cert14.positive
  · exact Cert15.positive
  · exact Cert16.positive
  · exact Cert17.positive
  · exact Cert18.positive
  · exact Cert19.positive
  · exact Cert20.positive
  · exact Cert21.positive
  · exact Cert22.positive
  · exact Cert23.positive
  · exact Cert24.positive
  · exact Cert25.positive
  · exact Cert26.positive
  · exact Cert27.positive
  · exact Cert28.positive
  · exact Cert29.positive
  · exact Cert30.positive
  · exact Cert31.positive
  · exact Cert32.positive
  · exact Cert33.positive
  · exact Cert34.positive
  · exact Cert35.positive
  · exact Cert36.positive
  · exact Cert37.positive
  · exact Cert38.positive
  · exact Cert39.positive

#print axioms finite_small_scalar_pos
end SymmetricSector
