/- Integer-only evaluation of basis brackets, linked to the original sparse map.
This is an optimization of proof reduction, not a replacement bracket or oracle. -/
import Kourovka.Ambient.IntData

namespace Kourovka.Ambient.FastBasis
open Kourovka.Linear

/-- An integer coordinate of a skew-half term, with no scalar-ring structure reduction. -/
def entry (t : Sparse.Term) (i j o : I) : Int :=
  if t.2.2.1 = o.val then
    (if i.val = t.1 ∧ j.val = t.2.1 then t.2.2.2 else 0) -
    (if j.val = t.1 ∧ i.val = t.2.1 then t.2.2.2 else 0)
  else 0

/-- Integer-only evaluator for an arbitrary list, retaining all duplicate terms. -/
def coeff : List Sparse.Term → I → I → I → Int
  | [], _, _, _ => 0
  | t :: ts, i, j, o => entry t i j o + coeff ts i j o

theorem coord_unit (i : I) (a : Nat) :
    Sparse.coord (unitVec i : V Int) a = if i.val = a then 1 else 0 := by
  by_cases ha : a < 31
  · simp only [Sparse.coord, dif_pos ha, unitVec]
    simp only [Fin.ext_iff]
  · have hi : i.val ≠ a := by intro h; exact ha (h ▸ i.isLt)
    simp [Sparse.coord, ha, hi]

theorem entry_sound (t : Sparse.Term) (i j o : I) :
    Sparse.entry t (unitVec i : V Int) (unitVec j) o = entry t i j o := by
  rcases t with ⟨a,b,k,c⟩
  simp only [Sparse.entry, coord_unit, entry, Int.cast_id]
  split_ifs <;> simp_all

theorem fromTerms_sound (ts : List Sparse.Term) (i j o : I) :
    Sparse.fromTerms ts (unitVec i : V Int) (unitVec j) o = coeff ts i j o := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    change Sparse.entry t (unitVec i : V Int) (unitVec j) o +
      Sparse.fromTerms ts (unitVec i : V Int) (unitVec j) o = _
    rw [entry_sound, ih]
    rfl

theorem bracket_sound (i j o : I) :
    (B (unitVec i) (unitVec j) : V Int) o = coeff exportedTerms i j o :=
  fromTerms_sound exportedTerms i j o

/-- The integer computation remains valid after base change to every commutative ring. -/
theorem cast_fromTerms_sound {R : Type*} [CommRing R]
    (ts : List Sparse.Term) (i j o : I) :
    Sparse.fromTerms ts (unitVec i : V R) (unitVec j) o =
      (coeff ts i j o : R) := by
  have h := congrFun (mapVec_terms (Int.castRingHom R) ts
    (unitVec i : V Int) (unitVec j)) o
  rw [mapVec_unit, mapVec_unit] at h
  change (Sparse.fromTerms ts (unitVec i : V Int) (unitVec j) o : R) =
    Sparse.fromTerms ts (unitVec i : V R) (unitVec j) o at h
  rw [fromTerms_sound] at h
  exact h.symm

theorem termVec_coeff (i j o : I) :
    (IntData.termVec (IntData.term i j) : V Int) o = IntData.coeff i j o := by
  cases h : IntData.term i j with
  | none => simp [IntData.termVec, IntData.coeff, h]
  | some t =>
    rcases t with ⟨k,c⟩
    by_cases hk : k = o <;>
      simp [IntData.termVec, IntData.coeff, h, unitVec, Pi.smul_apply, smul_eq_mul, hk]

/-- Every original TermCheck follows from the equivalent finite integer coordinate check. -/
theorem termCheck_of_coeff (i : I)
    (h : ∀ j o : I, coeff exportedTerms i j o = IntData.coeff i j o) :
    IntData.TermCheck i := by
  intro j
  funext o
  rw [bracket_sound, termVec_coeff]
  exact h j o

end Kourovka.Ambient.FastBasis
