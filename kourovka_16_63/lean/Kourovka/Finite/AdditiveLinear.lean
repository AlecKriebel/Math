/- Uncompiled source. Why additive automorphisms over ZMod(n) are not being omitted. -/
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.Module.Equiv.Basic
import Mathlib.Tactic

namespace Kourovka.Finite
variable {n d e : Nat}
abbrev VecAt (n d : Nat) := Fin d → ZMod n

/-- Every additive map between these coordinate modules is ZMod(n)-linear. -/
def additiveToLinear (F : VecAt n d →+ VecAt n e) : VecAt n d →ₗ[ZMod n] VecAt n e where
  toFun := F
  map_add' := F.map_add
  map_smul' := by
    intro a x
    obtain ⟨z,rfl⟩ := ZMod.intCast_surjective a
    have hcast (v : VecAt n d) : (z : ZMod n) • v = z • v := by
      funext i
      simp [smul_eq_mul,zsmul_eq_mul]
    have hcast' (v : VecAt n e) : (z : ZMod n) • v = z • v := by
      funext i
      simp [smul_eq_mul,zsmul_eq_mul]
    change F ((z : ZMod n) • x) = (z : ZMod n) • F x
    rw [hcast,hcast']
    exact F.map_zsmul x z

@[simp] theorem additiveToLinear_apply (F : VecAt n d →+ VecAt n e) (x : VecAt n d) :
    additiveToLinear F x = F x := rfl

/-- A genuine equivalence, so the passage to linear maps loses no additive maps. -/
def additiveLinearEquiv :
    (VecAt n d →+ VecAt n e) ≃ (VecAt n d →ₗ[ZMod n] VecAt n e) where
  toFun := additiveToLinear
  invFun := LinearMap.toAddMonoidHom
  left_inv := by intro F; ext x; rfl
  right_inv := by intro F; ext x; rfl

/-- The same automatic linearity applies to all additive bijections. -/
def additiveEquivToLinear (F : VecAt n d ≃+ VecAt n e) :
    VecAt n d ≃ₗ[ZMod n] VecAt n e :=
  { additiveToLinear F.toAddMonoidHom with
    invFun := F.symm
    left_inv := F.left_inv
    right_inv := F.right_inv }

@[simp] theorem additiveEquivToLinear_apply (F : VecAt n d ≃+ VecAt n e) (x : VecAt n d) :
    additiveEquivToLinear F x = F x := rfl

end Kourovka.Finite
