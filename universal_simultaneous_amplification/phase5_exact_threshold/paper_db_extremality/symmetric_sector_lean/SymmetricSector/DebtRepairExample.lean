import SymmetricSector.LeftDebt

namespace SymmetricSector
open Matrix
open scoped BigOperators

/-- The supersolution printed in A.28, at the smallest order relevant to
this indexing comparison (physical bad ranks two and three). -/
def printedY4 (i : Bad 4) : ℚ :=
  2 * (i.val + 3) / (3 * (i.val + 2) * (i.val + 1))

/-- A checkable counterexample to directly deriving A.31 by pairing the
printed Y barrier with the bad reward. This is not a counterexample to
A.31 itself: LeftDebt proves that bound via the sharper Z barrier. -/
theorem printed_Y_pairing_gap_at_four :
    dotProduct printedY4 (-badReward 4) -
      (∑ i : Bad 4, (4*(i.val+3)/(3*(i.val+2)*((4:ℚ)-2))) *
        goodReward 4 (goodBelow 4 i)) = (1/360 : ℚ) := by
  decide +kernel

#print axioms printed_Y_pairing_gap_at_four
end SymmetricSector
