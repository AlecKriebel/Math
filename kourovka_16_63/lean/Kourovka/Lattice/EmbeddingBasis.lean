/- Basis formulas used to check the embedding without reevaluating the ambient sparse bracket. -/
import Kourovka.Lattice.ScaledData
import Kourovka.Ambient.FastBasis

set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

namespace Kourovka.Lattice
open Kourovka.Linear Kourovka.Ambient

/-- The columns of the explicit unimodular basis change. -/
def originalBasis {R : Type*} [CommRing R] (i : I) : V R :=
  if i = 1 then unitVec 1 + unitVec 2 + unitVec 4 + unitVec 10 + unitVec 27
  else if i = 2 then unitVec 3
  else if i = 3 then unitVec 2
  else unitVec i

theorem P_unit (i : I) :
    P (unitVec i : V Int) = originalBasis i := by
  fin_cases i <;> decide +kernel

theorem diagonal_unit (i : I) :
    diagonal (unitVec i) = (1009 : Int)^degree i • unitVec i := by
  funext j
  change (1009 : Int)^degree j * (if i = j then 1 else 0) =
    (1009 : Int)^degree i * (if i = j then 1 else 0)
  by_cases h : i = j
  · subst j; simp
  · simp [h]

theorem embed_unit (i : I) :
    embed (unitVec i) = (1009 : Int)^degree i • originalBasis i := by
  rw [embed_apply, diagonal_unit, map_smul, P_unit]

/-- The scaled bracket basis coordinates, computed with plain integer operations. -/
theorem LB_basis_coeff (i j : I) :
    (LB (unitVec i) (unitVec j) : V Int) =
      fun o => Ambient.FastBasis.coeff scaledTerms i j o := by
  funext o
  exact Ambient.FastBasis.fromTerms_sound scaledTerms i j o

end Kourovka.Lattice
