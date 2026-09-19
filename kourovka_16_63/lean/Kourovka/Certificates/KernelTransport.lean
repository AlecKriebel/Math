/- Uncompiled source. Sound kernel transport under invertible row/column operations. -/
import Mathlib.Algebra.Module.Equiv.Basic
import Mathlib.SetTheory.Cardinal.Finite

namespace Kourovka.Certificates

variable {R : Type*} [CommRing R]
variable {U V W : Type*} [AddCommGroup U] [Module R U]
  [AddCommGroup V] [Module R V] [AddCommGroup W] [Module R W]

/-- Coordinate-free kernel carrier used by the certificate soundness statements. -/
def KernelSet (K : U →ₗ[R] V) := {u : U // K u = 0}

/-- No information is lost by an invertible output transformation. -/
def kernelPostEquiv (K : U →ₗ[R] V) (A : V ≃ₗ[R] W) :
    KernelSet (A.toLinearMap.comp K) ≃ KernelSet K where
  toFun x := ⟨x.val, by
    apply A.injective
    simpa only [map_zero,LinearMap.comp_apply] using x.property⟩
  invFun x := ⟨x.val,by simp only [LinearMap.comp_apply,x.property,map_zero]⟩
  left_inv := by intro x; rfl
  right_inv := by intro x; rfl

/-- All solutions, including nonunits, are transported by the inverse coordinate change. -/
def kernelPreEquiv (K : U →ₗ[R] V) (B : W ≃ₗ[R] U) :
    KernelSet (K.comp B.toLinearMap) ≃ KernelSet K where
  toFun x := ⟨B x.val,x.property⟩
  invFun x := ⟨B.symm x.val,by
    change K (B (B.symm x.val)) = 0
    simpa only [B.apply_symm_apply] using x.property⟩
  left_inv := by intro x; apply Subtype.ext; exact B.symm_apply_apply x.val
  right_inv := by intro x; apply Subtype.ext; exact B.apply_symm_apply x.val

/-- Exact equality of transformed linear maps is sufficient; no Smith normal form is assumed. -/
def kernelTransformEquiv (K D : U →ₗ[R] V) (A : V ≃ₗ[R] V) (B : U ≃ₗ[R] U)
    (h : (A.toLinearMap.comp K).comp B.toLinearMap = D) :
    KernelSet D ≃ KernelSet K := by
  subst D
  exact (kernelPreEquiv (A.toLinearMap.comp K) B).trans (kernelPostEquiv K A)

theorem kernelTransform_card (K D : U →ₗ[R] V) (A : V ≃ₗ[R] V) (B : U ≃ₗ[R] U)
    (h : (A.toLinearMap.comp K).comp B.toLinearMap = D) :
    Nat.card (KernelSet K) = Nat.card (KernelSet D) :=
  (Nat.card_congr (kernelTransformEquiv K D A B h)).symm

end Kourovka.Certificates
