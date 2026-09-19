/- The checked inner-column witness bounds the complete derivation matrix rank. -/
import Kourovka.Certificates.InnerWitness
import Kourovka.Lattice.Integral

namespace Kourovka.Certificates.InnerRank
open Kourovka.Linear Kourovka.Ambient Kourovka.Lattice
open scoped BigOperators
set_option maxRecDepth 20000
set_option maxHeartbeats 2000000

/-- Jacobi, not a computed nullspace guess, puts every inner derivation in the kernel. -/
theorem innerColumn_derivation {R : Type*} [CommRing R] (i : Param) :
    DerivationCondition (LB (R:=R)) (innerColumn i) := by
  intro u v
  exact LB_leibniz (unitVec (Fin.castLE (by decide : 30 ≤ 31) i)) u v

theorem innerMap_derivation {R : Type*} [CommRing R] (a : Param → R) :
    DerivationCondition LB (innerMap a) := by
  rw [derivation_iff_delta_zero]
  have hexpand : innerMap a = ∑ i : Param, a i • innerColumn i := rfl
  rw [hexpand]
  simp only [map_sum,map_smul]
  have h : ∀ i, delta (LB (R:=R)) (innerColumn i) = 0 :=
    fun i => (derivation_iff_delta_zero _ _).mp (innerColumn_derivation i)
  simp only [h,smul_zero,Finset.sum_const_zero]

def innerKernelMap : (Param → Rat) →ₗ[Rat] LinearMap.ker (matrixLinear (LB (R:=Rat))) where
  toFun a := ⟨toEntries (innerMap a),by
    change matrixLinear LB (toEntries (innerMap a)) = 0
    apply (kernel_iff_derivation LB LB_alternating _).mpr
    simpa only [fromEntries_entries] using innerMap_derivation a⟩
  map_add' := by
    intro a b
    apply Subtype.ext
    change toEntries (innerMap (a+b)) = toEntries (innerMap a) + toEntries (innerMap b)
    simp only [map_add]
  map_smul' := by
    intro c a
    apply Subtype.ext
    change toEntries (innerMap (c • a)) = c • toEntries (innerMap a)
    simp only [map_smul]

theorem innerKernelMap_injective : Function.Injective innerKernelMap := by
  intro a b hab
  apply innerMap_injective
  have h := congrArg (fun u : LinearMap.ker (matrixLinear (LB (R:=Rat))) => fromEntries u.val) hab
  change fromEntries (toEntries (innerMap a)) = fromEntries (toEntries (innerMap b)) at h
  simpa only [fromEntries_entries] using h

theorem kernel_finrank_lower :
    30 ≤ Module.finrank Rat (LinearMap.ker (matrixLinear (LB (R:=Rat)))) := by
  have hn := innerKernelMap.finrank_range_add_finrank_ker
  have hker : LinearMap.ker innerKernelMap = ⊥ :=
    LinearMap.ker_eq_bot.mpr innerKernelMap_injective
  have hd : Module.finrank Rat (Param → Rat) = 30 := by
    simp only [Module.finrank_pi,Fintype.card_fin]
  rw [hker,finrank_bot,add_zero,hd] at hn
  have hle := (LinearMap.range innerKernelMap).finrank_le
  simpa only [hn] using hle

/-- The independent rank upper bound prevents hidden higher-valuation Smith factors.
This is over Rat; transfer to Q_p uses scalar extension of an integer matrix. -/
theorem rational_rank_upper :
    Module.finrank Rat (LinearMap.range (matrixLinear (LB (R:=Rat)))) ≤ 931 := by
  have hn := (matrixLinear (LB (R:=Rat))).finrank_range_add_finrank_ker
  have hd : Module.finrank Rat (Col → Rat) = 961 := by
    simp only [Module.finrank_pi,Module.finrank_self,mul_one,num_cols]
  rw [hd] at hn
  have hk := kernel_finrank_lower
  omega

end Kourovka.Certificates.InnerRank
