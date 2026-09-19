/-
UNCOMPILED research source. These are generic expression-soundness lemmas,
not claims that the concrete generation certificate has been kernel checked.
The LieRing/LieAlgebra interfaces were inspected at the pinned mathlib commit.
-/
import Mathlib.Algebra.Lie.Basic

namespace Kourovka

/-- A finite expression in two generators, using linear combinations and brackets. -/
inductive Word (R : Type*) where
  | x : Word R
  | y : Word R
  | add : Word R → Word R → Word R
  | smul : R → Word R → Word R
  | lie : Word R → Word R → Word R

namespace Word

variable {R : Type*} [CommRing R]
variable {L : Type*} [LieRing L] [LieAlgebra R L]
variable {M : Type*} [LieRing M] [LieAlgebra R M]

def eval (x y : L) : Word R → L
  | .x => x
  | .y => y
  | .add u v => eval x y u + eval x y v
  | .smul a u => a • eval x y u
  | .lie u v => ⁅eval x y u, eval x y v⁆

/-- A bracket-preserving linear map respects every generated expression. -/
theorem map_eval (f : L →ₗ[R] M)
    (hf : ∀ u v, f ⁅u, v⁆ = ⁅f u, f v⁆)
    (x y : L) (w : Word R) :
    f (eval x y w) = eval (f x) (f y) w := by
  induction w with
  | x => rfl
  | y => rfl
  | add u v ihu ihv => simp only [eval, map_add, ihu, ihv]
  | smul a u ihu => simp only [eval, map_smul, ihu]
  | lie u v ihu ihv => simp only [eval, hf, ihu, ihv]

/-- Generation, rather than a classification theorem, determines such a map. -/
theorem fixed_eval (f : L →ₗ[R] L)
    (hf : ∀ u v, f ⁅u, v⁆ = ⁅f u, f v⁆)
    (x y : L) (hx : f x = x) (hy : f y = y) (w : Word R) :
    f (eval x y w) = eval x y w := by
  rw [map_eval f hf x y w, hx, hy]

/-- A derivation annihilating the generators annihilates every expression. -/
theorem derivation_zero_eval (D : L →ₗ[R] L)
    (hD : ∀ u v, D ⁅u, v⁆ = ⁅D u, v⁆ + ⁅u, D v⁆)
    (x y : L) (hx : D x = 0) (hy : D y = 0) (w : Word R) :
    D (eval x y w) = 0 := by
  induction w with
  | x => exact hx
  | y => exact hy
  | add u v ihu ihv => simp only [eval, map_add, ihu, ihv, add_zero]
  | smul a u ihu => simp only [eval, map_smul, ihu, smul_zero]
  | lie u v ihu ihv =>
      simp only [eval, hD, ihu, ihv, zero_lie, lie_zero, add_zero]

/-- This is a generic conditional lemma; concrete generation is a separate obligation. -/
theorem fixed_of_generation (f : L →ₗ[R] L)
    (hf : ∀ u v, f ⁅u, v⁆ = ⁅f u, f v⁆)
    (x y : L) (hx : f x = x) (hy : f y = y)
    (hgen : ∀ z : L, ∃ w : Word R, eval x y w = z) :
    ∀ z : L, f z = z := by
  intro z
  obtain ⟨w, hw⟩ := hgen z
  rw [← hw]
  exact fixed_eval f hf x y hx hy w

/-- The corresponding generic lemma for arbitrary derivations, not just inner ones. -/
theorem zero_of_generation (D : L →ₗ[R] L)
    (hD : ∀ u v, D ⁅u, v⁆ = ⁅D u, v⁆ + ⁅u, D v⁆)
    (x y : L) (hx : D x = 0) (hy : D y = 0)
    (hgen : ∀ z : L, ∃ w : Word R, eval x y w = z) :
    ∀ z : L, D z = 0 := by
  intro z
  obtain ⟨w, hw⟩ := hgen z
  rw [← hw]
  exact derivation_zero_eval D hD x y hx hy w

end Word
end Kourovka
