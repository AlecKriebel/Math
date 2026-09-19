/- Checked witness and injectivity of the thirty inner-derivation columns. -/
import Kourovka.Certificates.InnerChecks.Row00
import Kourovka.Certificates.InnerChecks.Row01
import Kourovka.Certificates.InnerChecks.Row02
import Kourovka.Certificates.InnerChecks.Row03
import Kourovka.Certificates.InnerChecks.Row04
import Kourovka.Certificates.InnerChecks.Row05
import Kourovka.Certificates.InnerChecks.Row06
import Kourovka.Certificates.InnerChecks.Row07
import Kourovka.Certificates.InnerChecks.Row08
import Kourovka.Certificates.InnerChecks.Row09
import Kourovka.Certificates.InnerChecks.Row10
import Kourovka.Certificates.InnerChecks.Row11
import Kourovka.Certificates.InnerChecks.Row12
import Kourovka.Certificates.InnerChecks.Row13
import Kourovka.Certificates.InnerChecks.Row14
import Kourovka.Certificates.InnerChecks.Row15
import Kourovka.Certificates.InnerChecks.Row16
import Kourovka.Certificates.InnerChecks.Row17
import Kourovka.Certificates.InnerChecks.Row18
import Kourovka.Certificates.InnerChecks.Row19
import Kourovka.Certificates.InnerChecks.Row20
import Kourovka.Certificates.InnerChecks.Row21
import Kourovka.Certificates.InnerChecks.Row22
import Kourovka.Certificates.InnerChecks.Row23
import Kourovka.Certificates.InnerChecks.Row24
import Kourovka.Certificates.InnerChecks.Row25
import Kourovka.Certificates.InnerChecks.Row26
import Kourovka.Certificates.InnerChecks.Row27
import Kourovka.Certificates.InnerChecks.Row28
import Kourovka.Certificates.InnerChecks.Row29

namespace Kourovka.Certificates.InnerRank
open Kourovka.Linear Kourovka.Ambient Kourovka.Lattice
open scoped BigOperators

theorem leftInverse_all (i : Param) : LeftInverseCheck i := by
  fin_cases i
  · exact leftInverse_00
  · exact leftInverse_01
  · exact leftInverse_02
  · exact leftInverse_03
  · exact leftInverse_04
  · exact leftInverse_05
  · exact leftInverse_06
  · exact leftInverse_07
  · exact leftInverse_08
  · exact leftInverse_09
  · exact leftInverse_10
  · exact leftInverse_11
  · exact leftInverse_12
  · exact leftInverse_13
  · exact leftInverse_14
  · exact leftInverse_15
  · exact leftInverse_16
  · exact leftInverse_17
  · exact leftInverse_18
  · exact leftInverse_19
  · exact leftInverse_20
  · exact leftInverse_21
  · exact leftInverse_22
  · exact leftInverse_23
  · exact leftInverse_24
  · exact leftInverse_25
  · exact leftInverse_26
  · exact leftInverse_27
  · exact leftInverse_28
  · exact leftInverse_29

/-- The checked finite matrix identities imply an identity on ALL parameter vectors. -/
theorem extractor_innerMap (a : Param → Rat) : extractor (innerMap a) = a := by
  have hmap : extractor.comp (innerMap (R:=Rat)) = LinearMap.id := by
    apply ext_basis
    intro j
    funext i
    change extractor (innerMap (unitVec j)) i = unitVec j i
    rw [innerMap_unit]
    simpa only [extractor, LinearMap.coe_mk, AddHom.coe_mk, unitVec, eq_comm] using
      leftInverse_all i j
  exact congrArg (fun F : (Param → Rat) →ₗ[Rat] (Param → Rat) => F a) hmap

theorem innerMap_injective : Function.Injective (innerMap (R:=Rat)) := by
  intro a b hab
  have h := congrArg extractor hab
  simpa only [extractor_innerMap] using h

end Kourovka.Certificates.InnerRank
