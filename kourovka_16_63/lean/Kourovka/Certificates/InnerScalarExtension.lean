/- Characteristic-zero rank bound from the transported checked inner witness. -/
import Kourovka.Certificates.InnerRank
import Kourovka.Certificates.InnerScalarWitness
namespace Kourovka.Certificates.InnerRank
open Kourovka.Linear Kourovka.Ambient Kourovka.Lattice
open scoped BigOperators
set_option maxRecDepth 20000
set_option maxHeartbeats 2000000
variable (F : Type*) [Field F] [CharZero F]

def extendedInnerKernel : (Param→F) →ₗ[F] LinearMap.ker (matrixLinear (LB (R:=F))) where
  toFun a := ⟨toEntries (innerMap a),by
    change matrixLinear LB (toEntries (innerMap a))=0
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

theorem extendedInnerKernel_injective : Function.Injective (extendedInnerKernel F) := by
  intro a b hab
  apply extended_inner_injective F
  have h := congrArg (fun u:LinearMap.ker (matrixLinear (LB (R:=F))) => fromEntries u.val) hab
  change fromEntries (toEntries (innerMap a)) = fromEntries (toEntries (innerMap b)) at h
  simpa only [fromEntries_entries] using h

theorem characteristic_zero_kernel_finrank_lower :
    30≤Module.finrank F (LinearMap.ker (matrixLinear (LB (R:=F)))) := by
  have hk : LinearMap.ker (extendedInnerKernel F)=⊥ :=
    LinearMap.ker_eq_bot.mpr (extendedInnerKernel_injective F)
  have hr := (extendedInnerKernel F).finrank_range_add_finrank_ker
  have hd : Module.finrank F (Param→F)=30 := by simp [Param,Module.finrank_pi]
  rw [hk,finrank_bot,add_zero,hd] at hr
  have hle := (LinearMap.range (extendedInnerKernel F)).finrank_le
  rw [hr] at hle
  exact hle

/-- In particular this gives the missing high-valuation rank bound over Q_p,
by instantiating F with that field. It does NOT assert Smith acceptance. -/
theorem characteristic_zero_rank_upper :
    Module.finrank F (LinearMap.range (matrixLinear (LB (R:=F))))≤931 := by
  have h := (matrixLinear (LB (R:=F))).finrank_range_add_finrank_ker
  have hd : Module.finrank F (Col→F)=961 := by
    simp only [Module.finrank_pi,num_cols]
  rw [hd] at h
  have hk := characteristic_zero_kernel_finrank_lower F
  omega

end Kourovka.Certificates.InnerRank
