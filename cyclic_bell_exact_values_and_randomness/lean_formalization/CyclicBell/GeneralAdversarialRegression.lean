import CyclicBell.GeneralNestedGuessing
import CyclicBell.GeneralSourceFourier

/-! Focused positive regression source: arbitrary POVMs really include
nonprojective effects, and closure before slicing is a substantive distinction.
The real-line closure example is not asserted to be a quantum behavior example.
UNCOMPILED: these controls have not been run by Lean. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General

/-- Sixteen equiprobable Eve effects on C^1. No measurement is projective. -/
def uniformOneDimensionalGuess : GuessPOVM 4 (Fin 1) where
  effect := fun _ => (1/16 : ℂ) • (1 : Mat (Fin 1))
  positive := by
    intro g
    have he : (1/16 : ℂ) • (1 : Mat (Fin 1))=
        Matrix.diagonal (fun _ : Fin 1 => (1/16 : ℂ)) := by
      ext i j
      fin_cases i
      fin_cases j
      norm_num [Matrix.diagonal_apply,Matrix.smul_apply,Matrix.one_apply]
    rw [he]
    exact Matrix.PosSemidef.diagonal (by intro i; norm_num [Complex.nonneg_iff])
  complete := by
    ext i j
    fin_cases i
    fin_cases j
    norm_num [Matrix.sum_apply,Matrix.smul_apply,Matrix.one_apply,
      Finset.sum_const,Fintype.card_prod,ZMod.card,GuessLabel]

theorem uniformGuess_not_projective (g : GuessLabel 4) :
    uniformOneDimensionalGuess.effect g*uniformOneDimensionalGuess.effect g≠
      uniformOneDimensionalGuess.effect g := by
  intro he
  have h := congrArg (fun M : Mat (Fin 1) => M 0 0) he
  norm_num [uniformOneDimensionalGuess,Matrix.mul_apply,Matrix.smul_apply,Matrix.one_apply] at h

/-- Closure must be taken before the exact-score slice. This simple topological
control is independent of, and does not purport to prove, Qqa⊆Qqc. -/
theorem closure_before_slice_control :
    (0 : ℝ)∈closure (Set.Ioi (0 : ℝ)) ∧
      (0 : ℝ)∉closure {x : ℝ | 0<x ∧ x=0} := by
  constructor
  · rw [closure_Ioi]
    exact (show (0 : ℝ) ≤ 0 from le_rfl)
  · have he : {x : ℝ | 0<x ∧ x=0}=∅ := by
      ext x
      simp only [Set.mem_setOf_eq,Set.mem_empty_iff_false,iff_false,not_and]
      intro hx hx0
      simpa only [hx0,lt_self_iff_false] using hx
    rw [he,closure_empty]
    simp

/-- The all-dimensional lower estimate and d=4 table peak are distinct. -/
theorem general_floor_not_four_peak : paperGuessFloor 4<(3 : ℝ)/32 := by
  rw [paperGuessFloor_four]
  norm_num

end CyclicBell.General
