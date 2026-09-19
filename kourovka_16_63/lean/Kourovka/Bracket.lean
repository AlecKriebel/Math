/-
UNCOMPILED research source. The explicit sparse bracket is defined over any
commutative ring; there is deliberately no LieRing or BCH Group instance.
The generic additive/scalar/alternation proofs are proof attempts awaiting Lean.
-/
import Kourovka.ExportedData
import Mathlib.Tactic

namespace Kourovka.Sparse

abbrev Term := Nat × Nat × Nat × Int
abbrev Vec (R : Type*) := Fin 31 → R

variable {R : Type*} [CommRing R]

/-- Zero extension, not reduction of an index modulo 31. -/
def coord (v : Vec R) (i : Nat) : R :=
  if h : i < 31 then v ⟨i, h⟩ else 0

@[simp] theorem coord_add (u v : Vec R) (i : Nat) :
    coord (u + v) i = coord u i + coord v i := by
  by_cases h : i < 31 <;> simp [coord, h]

@[simp] theorem coord_smul (a : R) (u : Vec R) (i : Nat) :
    coord (a • u) i = a * coord u i := by
  by_cases h : i < 31 <;> simp [coord, h, smul_eq_mul]

/-- A skew-half entry contributes an alternating bilinear form. -/
def entry (t : Term) (u v : Vec R) (k : Fin 31) : R :=
  let (i, j, o, c) := t
  if o = k.val then (c : R) * (coord u i * coord v j - coord v i * coord u j)
  else 0

@[simp] theorem entry_self (t : Term) (u : Vec R) (k : Fin 31) :
    entry t u u k = 0 := by
  rcases t with ⟨i, j, o, c⟩
  simp [entry]

theorem entry_add_left (t : Term) (u v w : Vec R) (k : Fin 31) :
    entry t (u + v) w k = entry t u w k + entry t v w k := by
  rcases t with ⟨i, j, o, c⟩
  by_cases h : o = k.val
  · simp only [entry, h, if_true, coord_add]
    ring
  · simp [entry, h]

theorem entry_add_right (t : Term) (u v w : Vec R) (k : Fin 31) :
    entry t u (v + w) k = entry t u v k + entry t u w k := by
  rcases t with ⟨i, j, o, c⟩
  by_cases h : o = k.val
  · simp only [entry, h, if_true, coord_add]
    ring
  · simp [entry, h]

theorem entry_smul_left (t : Term) (a : R) (u v : Vec R) (k : Fin 31) :
    entry t (a • u) v k = a * entry t u v k := by
  rcases t with ⟨i, j, o, c⟩
  by_cases h : o = k.val
  · simp only [entry, h, if_true, coord_smul]
    ring
  · simp [entry, h]

theorem entry_smul_right (t : Term) (a : R) (u v : Vec R) (k : Fin 31) :
    entry t u (a • v) k = a * entry t u v k := by
  rcases t with ⟨i, j, o, c⟩
  by_cases h : o = k.val
  · simp only [entry, h, if_true, coord_smul]
    ring
  · simp [entry, h]

def fromTerms : List Term → Vec R → Vec R → Vec R
  | [], _, _ => 0
  | t :: ts, u, v => fun k => entry t u v k + fromTerms ts u v k

theorem fromTerms_self (ts : List Term) (u : Vec R) :
    fromTerms ts u u = 0 := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
      funext k
      simp [fromTerms, ih]

theorem fromTerms_add_left (ts : List Term) (u v w : Vec R) :
    fromTerms ts (u + v) w = fromTerms ts u w + fromTerms ts v w := by
  induction ts with
  | nil => simp [fromTerms]
  | cons t ts ih =>
      funext k
      simp only [fromTerms, entry_add_left, ih, Pi.add_apply]
      ring

theorem fromTerms_add_right (ts : List Term) (u v w : Vec R) :
    fromTerms ts u (v + w) = fromTerms ts u v + fromTerms ts u w := by
  induction ts with
  | nil => simp [fromTerms]
  | cons t ts ih =>
      funext k
      simp only [fromTerms, entry_add_right, ih, Pi.add_apply]
      ring

theorem fromTerms_smul_left (ts : List Term) (a : R) (u v : Vec R) :
    fromTerms ts (a • u) v = a • fromTerms ts u v := by
  induction ts with
  | nil => simp [fromTerms]
  | cons t ts ih =>
      funext k
      simp only [fromTerms, entry_smul_left, ih, Pi.smul_apply, smul_eq_mul]
      ring

theorem fromTerms_smul_right (ts : List Term) (a : R) (u v : Vec R) :
    fromTerms ts u (a • v) = a • fromTerms ts u v := by
  induction ts with
  | nil => simp [fromTerms]
  | cons t ts ih =>
      funext k
      simp only [fromTerms, entry_smul_right, ih, Pi.smul_apply, smul_eq_mul]
      ring

/-- The explicit original-coordinate bracket. No Lie instance is installed. -/
def bracket (u v : Vec R) : Vec R := fromTerms exportedTerms u v

end Kourovka.Sparse
