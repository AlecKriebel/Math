/- Uncompiled source. All 31 finite shards are imported, not a sample. -/
import Kourovka.Ambient.Checks.Chunk00
import Kourovka.Ambient.Checks.Chunk01
import Kourovka.Ambient.Checks.Chunk02
import Kourovka.Ambient.Checks.Chunk03
import Kourovka.Ambient.Checks.Chunk04
import Kourovka.Ambient.Checks.Chunk05
import Kourovka.Ambient.Checks.Chunk06
import Kourovka.Ambient.Checks.Chunk07
import Kourovka.Ambient.Checks.Chunk08
import Kourovka.Ambient.Checks.Chunk09
import Kourovka.Ambient.Checks.Chunk10
import Kourovka.Ambient.Checks.Chunk11
import Kourovka.Ambient.Checks.Chunk12
import Kourovka.Ambient.Checks.Chunk13
import Kourovka.Ambient.Checks.Chunk14
import Kourovka.Ambient.Checks.Chunk15
import Kourovka.Ambient.Checks.Chunk16
import Kourovka.Ambient.Checks.Chunk17
import Kourovka.Ambient.Checks.Chunk18
import Kourovka.Ambient.Checks.Chunk19
import Kourovka.Ambient.Checks.Chunk20
import Kourovka.Ambient.Checks.Chunk21
import Kourovka.Ambient.Checks.Chunk22
import Kourovka.Ambient.Checks.Chunk23
import Kourovka.Ambient.Checks.Chunk24
import Kourovka.Ambient.Checks.Chunk25
import Kourovka.Ambient.Checks.Chunk26
import Kourovka.Ambient.Checks.Chunk27
import Kourovka.Ambient.Checks.Chunk28
import Kourovka.Ambient.Checks.Chunk29
import Kourovka.Ambient.Checks.Chunk30

import Mathlib.Algebra.Lie.Basic
namespace Kourovka.Ambient
open Kourovka.Linear
open IntData

theorem termCheck_all : ∀ i : I, TermCheck i := by
  intro i
  fin_cases i
  · exact IntData.Checks.term_0
  · exact IntData.Checks.term_1
  · exact IntData.Checks.term_2
  · exact IntData.Checks.term_3
  · exact IntData.Checks.term_4
  · exact IntData.Checks.term_5
  · exact IntData.Checks.term_6
  · exact IntData.Checks.term_7
  · exact IntData.Checks.term_8
  · exact IntData.Checks.term_9
  · exact IntData.Checks.term_10
  · exact IntData.Checks.term_11
  · exact IntData.Checks.term_12
  · exact IntData.Checks.term_13
  · exact IntData.Checks.term_14
  · exact IntData.Checks.term_15
  · exact IntData.Checks.term_16
  · exact IntData.Checks.term_17
  · exact IntData.Checks.term_18
  · exact IntData.Checks.term_19
  · exact IntData.Checks.term_20
  · exact IntData.Checks.term_21
  · exact IntData.Checks.term_22
  · exact IntData.Checks.term_23
  · exact IntData.Checks.term_24
  · exact IntData.Checks.term_25
  · exact IntData.Checks.term_26
  · exact IntData.Checks.term_27
  · exact IntData.Checks.term_28
  · exact IntData.Checks.term_29
  · exact IntData.Checks.term_30

theorem jacobiCheck_all : ∀ i : I, JacobiCheck i := by
  intro i
  fin_cases i
  · exact IntData.Checks.jacobi_0
  · exact IntData.Checks.jacobi_1
  · exact IntData.Checks.jacobi_2
  · exact IntData.Checks.jacobi_3
  · exact IntData.Checks.jacobi_4
  · exact IntData.Checks.jacobi_5
  · exact IntData.Checks.jacobi_6
  · exact IntData.Checks.jacobi_7
  · exact IntData.Checks.jacobi_8
  · exact IntData.Checks.jacobi_9
  · exact IntData.Checks.jacobi_10
  · exact IntData.Checks.jacobi_11
  · exact IntData.Checks.jacobi_12
  · exact IntData.Checks.jacobi_13
  · exact IntData.Checks.jacobi_14
  · exact IntData.Checks.jacobi_15
  · exact IntData.Checks.jacobi_16
  · exact IntData.Checks.jacobi_17
  · exact IntData.Checks.jacobi_18
  · exact IntData.Checks.jacobi_19
  · exact IntData.Checks.jacobi_20
  · exact IntData.Checks.jacobi_21
  · exact IntData.Checks.jacobi_22
  · exact IntData.Checks.jacobi_23
  · exact IntData.Checks.jacobi_24
  · exact IntData.Checks.jacobi_25
  · exact IntData.Checks.jacobi_26
  · exact IntData.Checks.jacobi_27
  · exact IntData.Checks.jacobi_28
  · exact IntData.Checks.jacobi_29
  · exact IntData.Checks.jacobi_30

variable {R : Type*} [CommRing R]

@[simp] theorem mapVec_termVec (f : Int →+* R) (t : Option (I × Int)) :
    mapVec f (termVec t) = termVec t := by
  cases t with
  | none => simp [termVec]
  | some p =>
      rcases p with ⟨i,c⟩
      simp only [termVec, Int.cast_id, mapVec_smul, mapVec_unit]
      congr 1
      exact map_intCast f c

/-- Exact basis bracket formula in every commutative coefficient ring. -/
theorem basis_bracket (i j : I) :
    (B (unitVec i) (unitVec j) : V R) = termVec (term i j) := by
  have h := congrArg (mapVec (Int.castRingHom R)) (termCheck_all i j)
  simpa only [mapVec_B, mapVec_unit, mapVec_termVec] using h

@[simp] theorem termVec_coord (t : Option (I × Int)) (o : I) :
    (termVec t : V Int) o =
      match t with | none => 0 | some (k,c) => if k = o then c else 0 := by
  cases t with
  | none => rfl
  | some p => rcases p with ⟨k,c⟩; simp [termVec, unitVec, smul_eq_mul]

theorem basis_coeff (i j o : I) :
    (B (unitVec i) (unitVec j) : V Int) o = coeff i j o := by
  rw [basis_bracket]
  exact termVec_coord (term i j) o

theorem nestedLeft_sound (i j k o : I) :
    (B (unitVec i) (B (unitVec j) (unitVec k)) : V Int) o =
      nestedLeft i j k o := by
  rw [basis_bracket j k]
  unfold nestedLeft
  cases ht : term j k with
  | none => simp [termVec]
  | some p =>
      rcases p with ⟨l,c⟩
      simp only [termVec, map_smul, Pi.smul_apply, smul_eq_mul, Int.cast_id]
      rw [basis_coeff]

theorem nestedRight_sound (i j k o : I) :
    (B (B (unitVec i) (unitVec j)) (unitVec k) : V Int) o =
      nestedRight i j k o := by
  rw [basis_bracket i j]
  unfold nestedRight
  cases ht : term i j with
  | none => simp [termVec]
  | some p =>
      rcases p with ⟨l,c⟩
      simp only [termVec, map_smul, LinearMap.smul_apply, Pi.smul_apply, smul_eq_mul, Int.cast_id]
      rw [basis_coeff]

theorem jacobi_basis_integer (i j k : I) :
    (B (unitVec i) (B (unitVec j) (unitVec k)) -
      B (B (unitVec i) (unitVec j)) (unitVec k) -
      B (unitVec j) (B (unitVec i) (unitVec k)) : V Int) = 0 := by
  funext o
  simp only [Pi.sub_apply, Pi.zero_apply, nestedLeft_sound, nestedRight_sound]
  have h := jacobiCheck_all i j k o
  omega

/-- The integer check transports to arbitrary rings, including nonfields ZMod(p^i). -/
theorem jacobi_basis (i j k : I) :
    (B (unitVec i) (B (unitVec j) (unitVec k)) -
      B (B (unitVec i) (unitVec j)) (unitVec k) -
      B (unitVec j) (B (unitVec i) (unitVec k)) : V R) = 0 := by
  have h := congrArg (mapVec (Int.castRingHom R)) (jacobi_basis_integer i j k)
  simpa only [mapVec_sub, mapVec_zero, mapVec_B, mapVec_unit] using h

/-- Full Jacobi/Leibniz, for every vector; no enumeration of R is involved. -/
theorem leibniz (u v w : V R) : B u (B v w) = B (B u v) w + B v (B u w) :=
  jacobi_of_basis B jacobi_basis u v w

/-- A proved candidate LieRing structure. It is a value, not a global Pi instance. -/
def lieRing (R : Type*) [CommRing R] : LieRing (V R) :=
  { (inferInstance : AddCommGroup (V R)) with
    bracket := fun u v => B u v
    add_lie := by intro u v w; exact congrArg (fun f => f w) (map_add B u v)
    lie_add := by intro u v w; exact map_add (B u) v w
    lie_self := alternating
    leibniz_lie := leibniz }

/-- Scalar compatibility for the explicit structure above. -/
def lieAlgebra (R : Type*) [CommRing R] :
    letI := lieRing R
    LieAlgebra R (V R) := by
  letI := lieRing R
  exact { (inferInstance : Module R (V R)) with
    lie_smul := by intro a u v; exact map_smul (B u) a v }

end Kourovka.Ambient
