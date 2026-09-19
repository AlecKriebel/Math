/- Integral expression generation over coefficient rings and the p-adic integers. -/
import Kourovka.Lattice.IntegralWords

namespace Kourovka.Lattice.IntegralGeneration
open Kourovka.Linear Kourovka.Ambient
variable {R : Type*} [CommRing R]

/-- Coordinate ring maps as additive maps, so integral expression naturality is automatic. -/
def castAdd (R : Type*) [CommRing R] : V Int →+ V R where
  toFun := mapVec (Int.castRingHom R)
  map_zero' := mapVec_zero _
  map_add' := mapVec_add _

theorem generator_value_ring (i : I) :
    Expr.eval (fun a b : V R => Ambient.B a b) X Y (generator i) =
      (denominator i : R) • unitVec i := by
  have h := congrArg (castAdd R) (generator_value i)
  unfold ev at h
  rw [Expr.map_eval (castAdd R) (fun a b : V Int => Ambient.B a b)
    (fun a b : V R => Ambient.B a b) (mapVec_B (Int.castRingHom R))] at h
  rw [map_zsmul] at h
  simpa [castAdd, X, Y, Int.cast_smul_eq_zsmul] using h

/-- Exact generation over any coefficient ring in which the displayed denominators are units. -/
theorem closedSubmodule_eq_top (S : Submodule R (V R))
    (hB : ∀ a, a ∈ S → ∀ b, b ∈ S → Ambient.B a b ∈ S)
    (hX : X ∈ S) (hY : Y ∈ S)
    (hunit : ∀ i, IsUnit (denominator i : R)) : S = ⊤ := by
  have hbasis (i : I) : (unitVec i : V R) ∈ S := by
    have hm := Expr.eval_mem S (fun a b => Ambient.B a b) hB X Y hX hY (generator i)
    rw [generator_value_ring] at hm
    obtain ⟨u,hu⟩ := hunit i
    rw [← hu] at hm
    have hh := S.smul_mem (↑(u⁻¹) : R) hm
    simpa only [smul_smul,Units.inv_mul,one_smul] using hh
  apply top_unique
  intro a ha
  rw [decompose a]
  apply Submodule.sum_mem
  intro i hi
  exact S.smul_mem _ (hbasis i)

local instance : Fact (Nat.Prime 1009) := ⟨Kourovka.prime_is_prime⟩

theorem denominator_unit_padic (i : I) :
    IsUnit (denominator i : PadicInt 1009) := by
  by_contra h
  have hn := PadicInt.not_isUnit_iff.mp h
  have hd := (PadicInt.norm_int_lt_one_iff_dvd (denominator i)).mp hn
  exact denominator_not_divisible i hd

/-- In particular the two generators generate the actual Z_1009 ambient lattice. -/
theorem padic_generation (S : Submodule (PadicInt 1009) (V (PadicInt 1009)))
    (hB : ∀ a, a ∈ S → ∀ b, b ∈ S → Ambient.B a b ∈ S)
    (hX : X ∈ S) (hY : Y ∈ S) : S = ⊤ :=
  closedSubmodule_eq_top S hB hX hY denominator_unit_padic

end Kourovka.Lattice.IntegralGeneration
