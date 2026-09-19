/- The full tensor action and its three commuting differential operators. -/
import Kourovka.Linear.BilinearOps
import Kourovka.Analytic.NilpotentUnit

namespace Kourovka.Analytic.Tensor
open Kourovka.Linear
variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]
abbrev T := Bilinear R M

/-- Output action D η. -/
def output (D:Module.End R M) : Module.End R (T (R:=R) (M:=M)) where
  toFun η := post D η
  map_add' := by intro η θ; ext u v; simp [post]
  map_smul' := by intro c η; ext u v; simp [post]

/-- First input action η(D-, -). -/
def inputLeft (D:Module.End R M) : Module.End R (T (R:=R) (M:=M)) where
  toFun η := pre η D LinearMap.id
  map_add' := by intro η θ; rfl
  map_smul' := by intro c η; rfl

/-- Second input action η(-, D-). -/
def inputRight (D:Module.End R M) : Module.End R (T (R:=R) (M:=M)) where
  toFun η := pre η LinearMap.id D
  map_add' := by intro η θ; rfl
  map_smul' := by intro c η; rfl

@[simp] theorem output_apply (D:Module.End R M) (η:T) (u v:M) : output D η u v=D (η u v) := rfl
@[simp] theorem inputLeft_apply (D:Module.End R M) (η:T) (u v:M) : inputLeft D η u v=η (D u) v := rfl
@[simp] theorem inputRight_apply (D:Module.End R M) (η:T) (u v:M) : inputRight D η u v=η u (D v) := rfl

/-- These pairwise commutations hold without any hypothesis on D. -/
theorem output_inputLeft_commute (D:Module.End R M) : Commute (output D) (inputLeft D) := by
  ext η u v
  rfl

theorem output_inputRight_commute (D:Module.End R M) : Commute (output D) (inputRight D) := by
  ext η u v
  rfl

theorem inputs_commute (D:Module.End R M) : Commute (inputLeft D) (inputRight D) := by
  ext η u v
  rfl

def differential (D:Module.End R M) : Module.End R (T (R:=R) (M:=M)) :=
  output D-inputLeft D-inputRight D

@[simp] theorem differential_apply (D:Module.End R M) (η:T) :
    differential D η=delta η D := by
  ext u v
  rfl

/-- The actual nonlinear action on bracket tensors. -/
def action (Q:M≃ₗ[R]M) : T (R:=R) (M:=M) ≃ₗ[R] T (R:=R) (M:=M) where
  toFun η := post Q.toLinearMap (pre η Q.symm.toLinearMap Q.symm.toLinearMap)
  invFun η := post Q.symm.toLinearMap (pre η Q.toLinearMap Q.toLinearMap)
  left_inv := by intro η; ext u v; simp [post,pre]
  right_inv := by intro η; ext u v; simp [post,pre]
  map_add' := by intro η θ; ext u v; simp [post,pre]
  map_smul' := by intro c η; ext u v; simp [post,pre]

@[simp] theorem action_apply (Q:M≃ₗ[R]M) (η:T) (u v:M) :
    action Q η u v = Q (η (Q.symm u) (Q.symm v)) := rfl

/-- Fixed bracket tensors mean preservation of the original bracket on all inputs. -/
theorem action_fixed_iff (Q:M≃ₗ[R]M) (η:T) :
    action Q η=η ↔ ∀ u v,Q (η u v)=η (Q u) (Q v) := by
  constructor
  · intro h u v
    have he := congrArg (fun b:T (R:=R) (M:=M) => b (Q u) (Q v)) h
    simpa only [action_apply,Q.symm_apply_apply] using he
  · intro h
    ext u v
    simpa only [action_apply,Q.apply_symm_apply] using h (Q.symm u) (Q.symm v)

/-- Exact post-factorization step used after the analytic identities have been established.
This conditional lemma DOES NOT supply the missing exponential, convergence, or integrality facts. -/
theorem fixed_iff_derivation_of_factor
    (Q:M≃ₗ[R]M) (D:Module.End R M) (U:(Module.End R (T (R:=R) (M:=M)))ˣ)
    (hfactor:(action Q).toLinearMap-LinearMap.id =
      (U:Module.End R (T (R:=R) (M:=M)))*differential D)
    (η:T (R:=R) (M:=M)) :
    (∀ u v,Q (η u v)=η (Q u) (Q v)) ↔
      (∀ u v,D (η u v)=η (D u) v+η u (D v)) := by
  rw [← action_fixed_iff,← sub_eq_zero]
  have he : action Q η-η=((U:Module.End R (T (R:=R) (M:=M)))*differential D) η := by
    exact congrArg (fun X:Module.End R (T (R:=R) (M:=M)) => X η) hfactor
  rw [he,factor_zero_iff,differential_apply]
  constructor
  · intro h u v
    have hh := congrArg (fun b:T (R:=R) (M:=M) => b u v) h
    simp only [delta_apply,LinearMap.zero_apply] at hh
    calc
      D (η u v) = (D (η u v)-η (D u) v-η u (D v))+(η (D u) v+η u (D v)) := by abel
      _ = η (D u) v+η u (D v) := by rw [hh,zero_add]
  · intro h
    ext u v
    rw [delta_apply,h]
    simp only [LinearMap.zero_apply]
    abel

end Kourovka.Analytic.Tensor
