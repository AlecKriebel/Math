/- Uncompiled source. Actual integral embedding, followed by Jacobi and base change. -/
import Kourovka.Ambient.Lie
import Kourovka.Lattice.Checks.Chunk00
import Kourovka.Lattice.Checks.Chunk01
import Kourovka.Lattice.Checks.Chunk02
import Kourovka.Lattice.Checks.Chunk03
import Kourovka.Lattice.Checks.Chunk04
import Kourovka.Lattice.Checks.Chunk05
import Kourovka.Lattice.Checks.Chunk06
import Kourovka.Lattice.Checks.Chunk07
import Kourovka.Lattice.Checks.Chunk08
import Kourovka.Lattice.Checks.Chunk09
import Kourovka.Lattice.Checks.Chunk10
import Kourovka.Lattice.Checks.Chunk11
import Kourovka.Lattice.Checks.Chunk12
import Kourovka.Lattice.Checks.Chunk13
import Kourovka.Lattice.Checks.Chunk14
import Kourovka.Lattice.Checks.Chunk15
import Kourovka.Lattice.Checks.Chunk16
import Kourovka.Lattice.Checks.Chunk17
import Kourovka.Lattice.Checks.Chunk18
import Kourovka.Lattice.Checks.Chunk19
import Kourovka.Lattice.Checks.Chunk20
import Kourovka.Lattice.Checks.Chunk21
import Kourovka.Lattice.Checks.Chunk22
import Kourovka.Lattice.Checks.Chunk23
import Kourovka.Lattice.Checks.Chunk24
import Kourovka.Lattice.Checks.Chunk25
import Kourovka.Lattice.Checks.Chunk26
import Kourovka.Lattice.Checks.Chunk27
import Kourovka.Lattice.Checks.Chunk28
import Kourovka.Lattice.Checks.Chunk29
import Kourovka.Lattice.Checks.Chunk30

namespace Kourovka.Lattice
open Kourovka.Linear Kourovka.Ambient

theorem embedCheck_all : ∀ i : I, EmbedCheck i := by
  intro i
  fin_cases i
  · exact Checks.embed_0
  · exact Checks.embed_1
  · exact Checks.embed_2
  · exact Checks.embed_3
  · exact Checks.embed_4
  · exact Checks.embed_5
  · exact Checks.embed_6
  · exact Checks.embed_7
  · exact Checks.embed_8
  · exact Checks.embed_9
  · exact Checks.embed_10
  · exact Checks.embed_11
  · exact Checks.embed_12
  · exact Checks.embed_13
  · exact Checks.embed_14
  · exact Checks.embed_15
  · exact Checks.embed_16
  · exact Checks.embed_17
  · exact Checks.embed_18
  · exact Checks.embed_19
  · exact Checks.embed_20
  · exact Checks.embed_21
  · exact Checks.embed_22
  · exact Checks.embed_23
  · exact Checks.embed_24
  · exact Checks.embed_25
  · exact Checks.embed_26
  · exact Checks.embed_27
  · exact Checks.embed_28
  · exact Checks.embed_29
  · exact Checks.embed_30

/-- An equality for arbitrary integer vectors, obtained from a complete basis certificate. -/
theorem embed_bracket (a b : V Int) : embed (LB a b) = Ambient.B (embed a) (embed b) :=
  hom_of_basis embed LB Ambient.B embedCheck_all a b

/-- Jacobi is transported through an injective map, not inferred from a lossy reduction. -/
theorem integer_leibniz (a b c : V Int) :
    LB a (LB b c) = LB (LB a b) c + LB b (LB a c) := by
  apply embed_injective
  simp only [map_add, embed_bracket]
  exact Ambient.leibniz (embed a) (embed b) (embed c)

theorem integer_jacobi_defect (a b c : V Int) :
    LB a (LB b c) - LB (LB a b) c - LB b (LB a c) = 0 := by
  rw [integer_leibniz]
  abel

variable {R : Type*} [CommRing R]

theorem LB_leibniz (a b c : V R) : LB a (LB b c) = LB (LB a b) c + LB b (LB a c) := by
  apply jacobi_of_basis LB
  intro i j k
  have hh := congrArg (mapVec (Int.castRingHom R))
    (integer_jacobi_defect (unitVec i) (unitVec j) (unitVec k))
  simpa only [mapVec_sub, mapVec_zero, mapVec_LB, mapVec_unit] using hh

def lieRing (R : Type*) [CommRing R] : LieRing (V R) :=
  { (inferInstance : AddCommGroup (V R)) with
    bracket := fun u v => LB u v
    add_lie := by intro u v w; exact congrArg (fun f => f w) (map_add LB u v)
    lie_add := by intro u v w; exact map_add (LB u) v w
    lie_self := LB_alternating
    leibniz_lie := LB_leibniz }

def lieAlgebra (R : Type*) [CommRing R] :
    letI := lieRing R
    LieAlgebra R (V R) := by
  letI := lieRing R
  exact { (inferInstance : Module R (V R)) with
    lie_smul := by intro c u v; exact map_smul (LB u) c v }

/-- Conjugating back records the precise adapted-coordinate relationship. -/
theorem diagonal_bracket (a b : V Int) :
    diagonal (LB a b) = (adaptedB (R := Int)) (diagonal a) (diagonal b) := by
  have hh := congrArg P.symm (embed_bracket a b)
  simpa only [embed_apply, LinearEquiv.symm_apply_apply,
    adaptedB, transport_apply] using hh

end Kourovka.Lattice
