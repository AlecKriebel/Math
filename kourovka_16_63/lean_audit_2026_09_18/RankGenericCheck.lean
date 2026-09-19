import Kourovka.Certificates.InnerWitness
namespace Kourovka.Certificates.InnerRank.GenericCheck
open Kourovka.Linear Kourovka.Ambient Kourovka.Lattice
open scoped BigOperators
set_option maxRecDepth 20000
set_option maxHeartbeats 2000000
set_option maxHeartbeats 2000000
variable (hD : ∀ i : Param, DerivationCondition (LB (R:=Rat)) (innerColumn i))
include hD
theorem innerMap_derivation_check (a : Param → Rat) : DerivationCondition LB (innerMap a) := by
  rw [derivation_iff_delta_zero]
  have hexpand : innerMap a = ∑ i : Param, a i • innerColumn i := rfl
  rw [hexpand]
  simp only [map_sum,map_smul]
  have h : ∀ i, delta (LB (R:=Rat)) (innerColumn i) = 0 :=
    fun i => (derivation_iff_delta_zero _ _).mp (hD i)
  simp only [h,smul_zero,Finset.sum_const_zero]
def J : (Param → Rat) →ₗ[Rat] LinearMap.ker (matrixLinear (LB (R:=Rat))) where
  toFun a := ⟨toEntries (innerMap a),by
    change matrixLinear LB (toEntries (innerMap a)) = 0
    apply (kernel_iff_derivation LB LB_alternating _).mpr
    simpa only [fromEntries_entries] using innerMap_derivation_check hD a⟩
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
theorem J_injective : Function.Injective (J hD) := by
  intro a b hab
  apply innerMap_injective
  have h := congrArg (fun u : LinearMap.ker (matrixLinear (LB (R:=Rat))) => fromEntries u.val) hab
  change fromEntries (toEntries (innerMap a)) = fromEntries (toEntries (innerMap b)) at h
  simpa only [fromEntries_entries] using h
theorem lower : 30 ≤ Module.finrank Rat (LinearMap.ker (matrixLinear (LB (R:=Rat)))) := by
  have hn := (J hD).finrank_range_add_finrank_ker
  have hker : LinearMap.ker (J hD) = ⊥ := LinearMap.ker_eq_bot.mpr (J_injective hD)
  have hd : Module.finrank Rat (Param → Rat) = 30 := by
    simp only [Module.finrank_pi,Fintype.card_fin]
  rw [hker,finrank_bot,add_zero,hd] at hn
  have hle := (LinearMap.range (J hD)).finrank_le
  simpa only [hn] using hle
theorem upper : Module.finrank Rat (LinearMap.range (matrixLinear (LB (R:=Rat)))) ≤ 931 := by
  have hn := (matrixLinear (LB (R:=Rat))).finrank_range_add_finrank_ker
  have hd : Module.finrank Rat (Col → Rat) = 961 := by
    simp only [Module.finrank_pi,Module.finrank_self,mul_one,num_cols]
  rw [hd] at hn
  have hk := lower hD
  omega
end Kourovka.Certificates.InnerRank.GenericCheck
