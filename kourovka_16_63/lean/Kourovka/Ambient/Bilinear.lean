/- Uncompiled source. The actual original-coordinate bracket as a bilinear map. -/
import Kourovka.Bracket
import Kourovka.Linear.Basis

namespace Kourovka.Ambient
open Kourovka.Linear
abbrev I := Fin 31
abbrev V (R : Type*) := I → R

variable {R : Type*} [CommRing R]

/-- This uses the frozen integer table, not an unspecified Lie bracket. -/
def B : V R →ₗ[R] V R →ₗ[R] V R where
  toFun u :=
    { toFun := Sparse.bracket u
      map_add' := Sparse.fromTerms_add_right exportedTerms u
      map_smul' := by
        intro a v
        exact Sparse.fromTerms_smul_right exportedTerms a u v }
  map_add' := by
    intro u v
    apply LinearMap.ext
    intro w
    funext k
    exact congrFun (Sparse.fromTerms_add_left exportedTerms u v w) k
  map_smul' := by
    intro a u
    apply LinearMap.ext
    intro v
    funext k
    exact congrFun (Sparse.fromTerms_smul_left exportedTerms a u v) k

theorem B_apply (u v : V R) : B u v = Sparse.bracket u v := rfl

theorem alternating (u : V R) : B u u = 0 :=
  Sparse.fromTerms_self exportedTerms u

theorem skew (u v : V R) : B u v = - B v u := by
  have h := alternating (u + v)
  simp only [map_add, LinearMap.add_apply, alternating] at h
  apply eq_neg_iff_add_eq_zero.mpr
  simpa only [zero_add, add_zero, add_comm] using h

variable {S : Type*} [CommRing S]

def mapVec (f : R →+* S) (v : V R) : V S := fun i => f (v i)

@[simp] theorem mapVec_unit (f : R →+* S) (i : I) :
    mapVec f (unitVec i) = unitVec i := by
  funext j
  by_cases h : i = j <;> simp [mapVec, unitVec, h]

@[simp] theorem mapVec_add (f : R →+* S) (u v : V R) :
    mapVec f (u + v) = mapVec f u + mapVec f v := by
  funext i
  simp [mapVec]

@[simp] theorem mapVec_sub (f : R →+* S) (u v : V R) :
    mapVec f (u - v) = mapVec f u - mapVec f v := by
  funext i
  simp [mapVec]

@[simp] theorem mapVec_zero (f : R →+* S) : mapVec f (0 : V R) = 0 := by
  funext i
  simp [mapVec]

@[simp] theorem mapVec_smul (f : R →+* S) (a : R) (u : V R) :
    mapVec f (a • u) = f a • mapVec f u := by
  funext i
  simp [mapVec, smul_eq_mul]

theorem mapVec_terms (f : R →+* S) (ts : List Sparse.Term) (u v : V R) :
    mapVec f (Sparse.fromTerms ts u v) =
      Sparse.fromTerms ts (mapVec f u) (mapVec f v) := by
  induction ts with
  | nil => simp [Sparse.fromTerms]
  | cons t ts ih =>
      rcases t with ⟨i,j,o,c⟩
      funext k
      have hh := congrFun ih k
      simp only [mapVec] at hh ⊢
      simp only [Sparse.fromTerms, Sparse.entry, map_add]
      rw [hh]
      congr 1
      by_cases ho : o = k.val
      · by_cases hi : i < 31 <;> by_cases hj : j < 31 <;>
          simp [ho, Sparse.coord, hi, hj, mapVec, map_sub, map_mul]
      · simp [ho]

theorem mapVec_B (f : R →+* S) (u v : V R) :
    mapVec f (B u v) = B (mapVec f u) (mapVec f v) :=
  mapVec_terms f exportedTerms u v

end Kourovka.Ambient
