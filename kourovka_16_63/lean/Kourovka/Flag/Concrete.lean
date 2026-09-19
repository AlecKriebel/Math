/- Uncompiled source. Concrete field, flag, and exact small bracket identities. -/
import Kourovka.Ambient.Lie
import Kourovka.Parameters

set_option Elab.async false
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

namespace Kourovka.Flag
open Kourovka.Linear Kourovka.Ambient

abbrev k := ZMod 1009
instance primeFact : Fact (Nat.Prime 1009) := ⟨Kourovka.prime_is_prime⟩
abbrev E := Ambient.V k

def x : E := unitVec 0
def e : E := unitVec 1
def f : E := unitVec 2
def u (j : Fin 7) : E := unitVec ⟨3 + j.val, by omega⟩
def v (j : Fin 5) : E := unitVec ⟨10 + j.val, by omega⟩
def w (j : Fin 7) : E := unitVec ⟨15 + j.val, by omega⟩
def q (j : Fin 3) : E := unitVec ⟨22 + j.val, by omega⟩
def r (j : Fin 5) : E := unitVec ⟨25 + j.val, by omega⟩
def z : E := unitVec 30
def t : E := u 0
def y : E := e + f + u 1 + v 0 + r 2
def uv : E := u 1 + v 0

def ad1 : E := B x y
def ad2 : E := B x ad1
def ad3 : E := B x ad2

/-- No selected subgroup is hidden in this predicate. -/
def Preserves (Q : E →ₗ[k] E) : Prop :=
  ∀ a b, Q (B a b) = B (Q a) (Q b)

def IsDerivation (D : E →ₗ[k] E) : Prop :=
  ∀ a b, D (B a b) = B (D a) b + B a (D b)

/-- Explicit linear-combination definitions make membership witnesses transparent. -/
def F2 : Submodule k E where
  carrier := {a | ∃ s t : k, a = s • x + t • y}
  zero_mem' := ⟨0, 0, by simp⟩
  add_mem' := by
    rintro a b ⟨s,t,rfl⟩ ⟨s',t',rfl⟩
    refine ⟨s+s',t+t',?_⟩
    simp only [add_smul]
    abel
  smul_mem' := by
    rintro a b ⟨s,t,rfl⟩
    exact ⟨a*s,a*t,by simp [smul_add,smul_smul]⟩

def F3 : Submodule k E where
  carrier := {a | ∃ s t' u' : k, a = s • x + t' • y + u' • t}
  zero_mem' := ⟨0, 0, 0, by simp⟩
  add_mem' := by
    rintro a b ⟨s,t',u',rfl⟩ ⟨s',t'',u'',rfl⟩
    refine ⟨s+s',t'+t'',u'+u'',?_⟩
    simp only [add_smul]
    abel
  smul_mem' := by
    rintro a b ⟨s,t',u',rfl⟩
    exact ⟨a*s,a*t',a*u',by simp [smul_add,smul_smul]⟩

theorem x_mem_F2 : x ∈ F2 := ⟨1,0,by simp⟩
theorem y_mem_F2 : y ∈ F2 := ⟨0,1,by simp⟩
theorem t_mem_F3 : t ∈ F3 := ⟨0,0,1,by simp⟩
theorem F2_le_F3 : F2 ≤ F3 := by
  rintro a ⟨s,t',rfl⟩
  exact ⟨s,t',0,by simp⟩

/-- The flag really is the span flag used in the paper. -/
theorem F2_eq_span : F2 = Submodule.span k ({x,y} : Set E) := by
  apply le_antisymm
  · rintro a ⟨s,t',rfl⟩
    apply Submodule.add_mem
    · exact Submodule.smul_mem _ _ (Submodule.subset_span (by simp))
    · exact Submodule.smul_mem _ _ (Submodule.subset_span (by simp))
  · apply Submodule.span_le.mpr
    intro a ha
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at ha
    rcases ha with rfl | rfl
    · exact x_mem_F2
    · exact y_mem_F2

theorem F3_eq_span : F3 = Submodule.span k ({x,y,t} : Set E) := by
  apply le_antisymm
  · rintro a ⟨s,t',u',rfl⟩
    apply Submodule.add_mem
    · apply Submodule.add_mem
      · exact Submodule.smul_mem _ _ (Submodule.subset_span (by simp))
      · exact Submodule.smul_mem _ _ (Submodule.subset_span (by simp))
    · exact Submodule.smul_mem _ _ (Submodule.subset_span (by simp))
  · apply Submodule.span_le.mpr
    intro a ha
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at ha
    rcases ha with rfl | rfl | rfl
    · exact F2_le_F3 x_mem_F2
    · exact F2_le_F3 y_mem_F2
    · exact t_mem_F3

/-- This tactic expands exact bilinearity, then checks 31 coordinate identities. -/
macro "ambient_calc" : tactic =>
  `(tactic| (
    simp only [ad3, ad2, ad1, uv, y, t, x, e, f, u, v, w, q, r, z,
      map_add, map_sub, map_smul, map_neg, LinearMap.add_apply,
      LinearMap.sub_apply, LinearMap.smul_apply, LinearMap.neg_apply, basis_bracket]
    ext i
    fin_cases i <;>
      norm_num [IntData.term, IntData.termVec, unitVec, Fin.ext_iff, Fin.coe_ofNat_eq_mod, Pi.smul_apply, smul_eq_mul] <;> ring))

theorem t_ne_zero : t ≠ 0 := by
  intro h
  have hh : (1 : k) = 0 := congrFun h ⟨3, by decide⟩
  exact one_ne_zero hh

theorem xt : B x t = (6 : k) • t := by decide +kernel
theorem yt : B y t = (6 : k) • u 1 := by decide +kernel
theorem ef : B e f = x := by decide +kernel
theorem euv : B e uv = t := by decide +kernel
theorem rt : B (r 2) t = 0 := by decide +kernel

theorem first_bracket (a b s t' c : k) :
    B (a • x + b • y) (s • x + t' • y + c • t) =
      (a*t' - b*s) • ad1 + (6*a*c) • t + (6*b*c) • u 1 := by
  have hxy : B x y = ad1 := rfl
  have hyx : B y x = -ad1 := skew y x
  simp only [map_add, map_smul, LinearMap.add_apply, LinearMap.smul_apply,
    alternating, xt, yt, hxy, hyx, smul_zero, add_zero, zero_add]
  funext i
  simp only [Pi.add_apply, Pi.smul_apply, Pi.neg_apply, smul_eq_mul]
  ring

theorem ad1_value : ad1 = (2 : k) • e + (-2 : k) • f +
    (4 : k) • u 1 + (4 : k) • v 0 := by decide +kernel

theorem first_derivation (a b s t' c : k) :
    B (a • x + b • y) t + B x (s • x + t' • y + c • t) =
      (6*a + 6*c) • t + (6*b) • u 1 + t' • ad1 := by
  have hxy : B x y = ad1 := rfl
  have hyx : B y x = -ad1 := skew y x
  simp only [map_add, map_smul, LinearMap.add_apply, LinearMap.smul_apply,
    alternating, xt, yt, hxy, hyx, smul_zero, add_zero, zero_add]
  funext i
  simp only [Pi.add_apply, Pi.smul_apply, Pi.neg_apply, smul_eq_mul]
  ring

theorem e_projector : (16 : k) • e =
    (8 : k) • ad1 + (2 : k) • ad2 + (-1 : k) • ad3 := by decide +kernel

theorem f_projector : (48 : k) • f =
    (-8 : k) • ad1 + (6 : k) • ad2 + (-1 : k) • ad3 := by decide +kernel

theorem uv_projector : (48 : k) • uv =
    (-4 : k) • ad1 + (0 : k) • ad2 + (1 : k) • ad3 := by decide +kernel

theorem r_projector : (16 : k) • r 2 =
    (16 : k) • y + (-4 : k) • ad1 + (-4 : k) • ad2 + ad3 := by decide +kernel

theorem fu0 : B f (u 0) = (6 : k) • u 1 := by decide +kernel

theorem fu1 : B f (u 1) = (5 : k) • u 2 := by decide +kernel

theorem fu2 : B f (u 2) = (4 : k) • u 3 := by decide +kernel

theorem fu3 : B f (u 3) = (3 : k) • u 4 := by decide +kernel

theorem fu4 : B f (u 4) = (2 : k) • u 5 := by decide +kernel

theorem fu5 : B f (u 5) = (1 : k) • u 6 := by decide +kernel

theorem fv0 : B f (v 0) = (4 : k) • v 1 := by decide +kernel

theorem fv1 : B f (v 1) = (3 : k) • v 2 := by decide +kernel

theorem fv2 : B f (v 2) = (2 : k) • v 3 := by decide +kernel

theorem fv3 : B f (v 3) = (1 : k) • v 4 := by decide +kernel

theorem u2u6 : B (u 2) (u 6) = (2880 : k) • w 5 := by decide +kernel
theorem u0w5 : B (u 0) (w 5) = (86400 : k) • q 0 := by decide +kernel
theorem u0v4 : B (u 0) (v 4) = (8640 : k) • q 0 := by decide +kernel

/-- Scalar cancellation is justified in the field, not in a prime-power ring. -/
theorem cancel_smul {c : k} (hc : c ≠ 0) {a b : E} (h : c • a = c • b) : a = b := by
  have hh := congrArg (fun v : E => c⁻¹ • v) h
  simpa [smul_smul, hc] using hh

/-- A linear map's values on the three projector inputs determine a spectral piece. -/
theorem map_piece (S : E →ₗ[k] E) (d c a₁ a₂ a₃ : k) (v' : E)
    (hc : c ≠ 0)
    (h1 : S ad1 = d • ad1) (h2 : S ad2 = d • ad2) (h3 : S ad3 = d • ad3)
    (hp : c • v' = a₁ • ad1 + a₂ • ad2 + a₃ • ad3) : S v' = d • v' := by
  apply cancel_smul hc
  calc
    c • S v' = S (c • v') := (map_smul S c v').symm
    _ = S (a₁ • ad1 + a₂ • ad2 + a₃ • ad3) := congrArg S hp
    _ = d • (a₁ • ad1 + a₂ • ad2 + a₃ • ad3) := by
      simp only [map_add, map_smul, h1, h2, h3, smul_add, smul_smul]
      funext i
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      ring
    _ = d • (c • v') := congrArg (fun v : E => d • v) hp.symm
    _ = c • (d • v') := by simp [smul_smul, mul_comm]

theorem map_r_piece (S : E →ₗ[k] E) (c d : k)
    (hy : S y = c • x + d • y)
    (h1 : S ad1 = d • ad1) (h2 : S ad2 = d • ad2) (h3 : S ad3 = d • ad3) :
    S (r 2) = c • x + d • r 2 := by
  apply cancel_smul (c := 16) (by decide)
  calc
    (16 : k) • S (r 2) = S ((16 : k) • r 2) := (map_smul S 16 (r 2)).symm
    _ = S ((16 : k) • y + (-4 : k) • ad1 + (-4 : k) • ad2 + ad3) :=
      congrArg S r_projector
    _ = (16 : k) • (c • x) + d •
        ((16 : k) • y + (-4 : k) • ad1 + (-4 : k) • ad2 + ad3) := by
      simp only [map_add, map_smul, hy, h1, h2, h3, smul_add, smul_smul]
      funext i
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      ring
    _ = (16 : k) • (c • x + d • r 2) := by
      rw [← r_projector]
      simp [smul_add, smul_smul, mul_comm]

/-- Propagate images through a nonzero raw bracket coefficient. -/
theorem image_from_bracket (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (a b z' : E) (c s t' : k) (hc : c ≠ 0)
    (hb : B a b = c • z') (ha : Q a = s • a) (hb' : Q b = t' • b) :
    Q z' = (s*t') • z' := by
  apply cancel_smul hc
  calc
    c • Q z' = Q (c • z') := (map_smul Q c z').symm
    _ = Q (B a b) := congrArg Q hb.symm
    _ = B (Q a) (Q b) := hQ a b
    _ = c • ((s*t') • z') := by
      rw [ha,hb']
      simp only [map_smul, LinearMap.smul_apply, hb, smul_smul]
      congr 1
      ring

end Kourovka.Flag
