/- Uncompiled proof source. Direct rigidity for ALL flag-preserving linear bijections,
and separately for ALL derivations. No component-group classification is assumed. -/
import Kourovka.Flag.Generation
import Kourovka.FlagScalars

namespace Kourovka.Flag
open Kourovka.Linear Kourovka.Ambient

/-- Only injectivity, bracket preservation and the two flag memberships are used here. -/
theorem fixes_x (Q : E ≃ₗ[k] E) (hQ : Preserves Q.toLinearMap)
    (hxmem : Q x ∈ F2) (htmem : Q t ∈ F3) : Q x = x := by
  unfold Preserves at hQ
  obtain ⟨a,b,hx⟩ := hxmem
  obtain ⟨s,t',c,ht⟩ := htmem
  have H : B (a • x + b • y) (s • x + t' • y + c • t) =
      (6 : k) • (s • x + t' • y + c • t) := by
    calc
      _ = B (Q x) (Q t) := by rw [hx,ht]
      _ = Q (B x t) := (hQ x t).symm
      _ = _ := by rw [xt,map_smul,ht]
  rw [first_bracket] at H
  have hs0 : (6 : k) * s = 0 := by
    simpa [ad1_value,x,y,t,u,v,r,e,f,unitVec,smul_eq_mul] using (congrFun H 0).symm
  have ht0 : (6 : k) * t' = 0 := by
    simpa [ad1_value,x,y,t,u,v,r,e,f,unitVec,smul_eq_mul] using (congrFun H 27).symm
  have hs : s = 0 := (mul_eq_zero.mp hs0).resolve_left (by decide)
  have ht' : t' = 0 := (mul_eq_zero.mp ht0).resolve_left (by decide)
  have hc : c ≠ 0 := by
    intro hc0
    have hz : Q t = Q 0 := by simpa [hs,ht',hc0] using ht
    exact t_ne_zero (Q.injective hz)
  have ha : (6 : k)*a*c = 6*c := by
    simpa [hs,ht',ad1_value,x,y,t,u,v,r,e,f,unitVec,smul_eq_mul] using congrFun H 3
  have hb : (6 : k)*b*c = 0 := by
    simpa [hs,ht',ad1_value,x,y,t,u,v,r,e,f,unitVec,smul_eq_mul] using congrFun H 4
  obtain ⟨_,_,_,ha1,hb0⟩ := Kourovka.FlagScalars.automorphism_first_stage
    (by decide : (6 : k) ≠ 0) a b s t' c hs0 ht0 (Or.inr (Or.inr hc)) ha hb
  simpa [ha1,hb0] using hx

/-- Propagate the h-weight projector inputs under a map fixing x. -/
theorem automorphism_ad_images (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (hx : Q x = x) (c d : k) (hy : Q y = c • x + d • y) :
    Q ad1 = d • ad1 ∧ Q ad2 = d • ad2 ∧ Q ad3 = d • ad3 := by
  unfold Preserves at hQ
  have h1 : Q ad1 = d • ad1 := by
    dsimp only [ad1]
    rw [hQ,hx,hy]
    simp only [map_add,map_smul,alternating,smul_zero,zero_add]
  have h2 : Q ad2 = d • ad2 := by
    dsimp only [ad2]
    rw [hQ,hx,h1,map_smul]
  have h3 : Q ad3 = d • ad3 := by
    dsimp only [ad3]
    rw [hQ,hx,h2,map_smul]
  exact ⟨h1,h2,h3⟩

/-- The residual sign is excluded using TWO actual reconstructions of T_0. -/
theorem residual_sign_is_one (Q : E →ₗ[k] E) (hQ : Preserves Q)
    (d : k) (hd2 : d*d = 1)
    (hf : Q f = d • f) (ht : Q t = t) (huv : Q uv = d • uv) : d = 1 := by
  unfold Preserves at hQ
  have hu0 : Q (u 0) = (1 : k) • u 0 := by simpa [t] using ht
  have hu1 : Q (u 1) = (d : k) • u 1 := by
    have hh := image_from_bracket Q hQ f (u 0) (u 1) 6 d 1
      (by decide) fu0 hf hu0
    simpa only [mul_one, one_mul, hd2] using hh
  have hu2 : Q (u 2) = (1 : k) • u 2 := by
    have hh := image_from_bracket Q hQ f (u 1) (u 2) 5 d d
      (by decide) fu1 hf hu1
    simpa only [mul_one, one_mul, hd2] using hh
  have hu3 : Q (u 3) = (d : k) • u 3 := by
    have hh := image_from_bracket Q hQ f (u 2) (u 3) 4 d 1
      (by decide) fu2 hf hu2
    simpa only [mul_one, one_mul, hd2] using hh
  have hu4 : Q (u 4) = (1 : k) • u 4 := by
    have hh := image_from_bracket Q hQ f (u 3) (u 4) 3 d d
      (by decide) fu3 hf hu3
    simpa only [mul_one, one_mul, hd2] using hh
  have hu5 : Q (u 5) = (d : k) • u 5 := by
    have hh := image_from_bracket Q hQ f (u 4) (u 5) 2 d 1
      (by decide) fu4 hf hu4
    simpa only [mul_one, one_mul, hd2] using hh
  have hu6 : Q (u 6) = (1 : k) • u 6 := by
    have hh := image_from_bracket Q hQ f (u 5) (u 6) 1 d d
      (by decide) fu5 hf hu5
    simpa only [mul_one, one_mul, hd2] using hh
  have hv0 : Q (v 0) = d • v 0 := by
    have hh := huv
    simp only [uv,map_add,smul_add] at hh
    rw [hu1] at hh
    exact add_left_cancel hh
  have hv1 : Q (v 1) = (1 : k) • v 1 := by
    have hh := image_from_bracket Q hQ f (v 0) (v 1) 4 d d
      (by decide) fv0 hf hv0
    simpa only [mul_one, one_mul, hd2] using hh
  have hv2 : Q (v 2) = (d : k) • v 2 := by
    have hh := image_from_bracket Q hQ f (v 1) (v 2) 3 d 1
      (by decide) fv1 hf hv1
    simpa only [mul_one, one_mul, hd2] using hh
  have hv3 : Q (v 3) = (1 : k) • v 3 := by
    have hh := image_from_bracket Q hQ f (v 2) (v 3) 2 d d
      (by decide) fv2 hf hv2
    simpa only [mul_one, one_mul, hd2] using hh
  have hv4 : Q (v 4) = (d : k) • v 4 := by
    have hh := image_from_bracket Q hQ f (v 3) (v 4) 1 d 1
      (by decide) fv3 hf hv3
    simpa only [mul_one, one_mul, hd2] using hh
  have hw5 : Q (w 5) = (1 : k) • w 5 := by
    simpa only [one_mul] using image_from_bracket Q hQ (u 2) (u 6) (w 5)
      2880 1 1 (by decide) u2u6 hu2 hu6
  have hq0 : Q (q 0) = (1 : k) • q 0 := by
    simpa only [one_mul] using image_from_bracket Q hQ (u 0) (w 5) (q 0)
      86400 1 1 (by decide) u0w5 hu0 hw5
  have hq0' : Q (q 0) = d • q 0 := by
    simpa only [one_mul] using image_from_bracket Q hQ (u 0) (v 4) (q 0)
      8640 1 d (by decide) u0v4 hu0 hv4
  have hh := congrFun (hq0'.symm.trans hq0) 22
  simpa [q,unitVec,smul_eq_mul] using hh

/-- Full finite-field flag rigidity. This quantifies over the entire linear-equivalence type. -/
theorem full_flag_rigidity (Q : E ≃ₗ[k] E) (hQ : Preserves Q.toLinearMap)
    (hF2 : ∀ a, a ∈ F2 → Q a ∈ F2)
    (hF3 : ∀ a, a ∈ F3 → Q a ∈ F3) : Q = LinearEquiv.refl k E := by
  unfold Preserves at hQ
  change ∀ a b, Q (B a b) = B (Q a) (Q b) at hQ
  have hx : Q x = x := fixes_x Q hQ (hF2 x x_mem_F2) (hF3 t t_mem_F3)
  obtain ⟨c,d,hy⟩ := hF2 y y_mem_F2
  obtain ⟨h1,h2,h3⟩ := automorphism_ad_images Q.toLinearMap hQ hx c d hy
  have he : Q e = d • e := map_piece Q.toLinearMap d 16 8 2 (-1) e
    (by decide) h1 h2 h3 e_projector
  have hf : Q f = d • f := map_piece Q.toLinearMap d 48 (-8) 6 (-1) f
    (by decide) h1 h2 h3 f_projector
  have huv : Q uv = d • uv := map_piece Q.toLinearMap d 48 (-4) 0 1 uv
    (by decide) h1 h2 h3 uv_projector
  have hr : Q (r 2) = c • x + d • r 2 := map_r_piece Q.toLinearMap c d hy h1 h2 h3
  have hd2 : d*d = 1 := by
    have hh := hQ e f
    rw [ef,hx,he,hf] at hh
    simp only [map_smul,LinearMap.smul_apply,ef,smul_smul] at hh
    simpa [x,unitVec,smul_eq_mul] using (congrFun hh 0).symm
  have ht : Q t = t := by
    calc
      Q t = Q (B e uv) := congrArg Q euv.symm
      _ = B (Q e) (Q uv) := hQ e uv
      _ = t := by
        rw [he,huv]
        simp only [map_smul,LinearMap.smul_apply,euv,smul_smul,hd2,one_smul]
  have hc : c = 0 := by
    have hh := hQ (r 2) t
    rw [rt,map_zero,hr,ht] at hh
    simp only [map_add,LinearMap.add_apply,map_smul,LinearMap.smul_apply,
      xt,rt,smul_zero,add_zero,smul_smul] at hh
    have hz : c*(6 : k) = 0 := by
      simpa [t,u,unitVec,smul_eq_mul] using (congrFun hh 3).symm
    exact (mul_eq_zero.mp hz).resolve_right (by decide)
  have hd : d = 1 := residual_sign_is_one Q.toLinearMap hQ d hd2 hf ht huv
  have hy' : Q y = y := by simpa [hc,hd] using hy
  apply LinearEquiv.ext
  intro a
  exact Generation.fixed_all Q.toLinearMap hQ hx hy' a

/-- The infinitesimal first step does not assume that the derivation is inner. -/
theorem derivation_kills_x (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hxmem : D x ∈ F2) (htmem : D t ∈ F3) : D x = 0 := by
  unfold IsDerivation at hD
  obtain ⟨a,b,hx⟩ := hxmem
  obtain ⟨s,t',c,ht⟩ := htmem
  have H : (6 : k) • (s • x + t' • y + c • t) =
      (6*a+6*c) • t + (6*b) • u 1 + t' • ad1 := by
    calc
      _ = D (B x t) := by rw [xt,map_smul,ht]
      _ = B (D x) t + B x (D t) := hD x t
      _ = _ := by rw [hx,ht,first_derivation]
  have hs0 : (6 : k)*s = 0 := by
    simpa [ad1_value,x,y,t,u,v,r,e,f,unitVec,smul_eq_mul] using congrFun H 0
  have ht0 : (6 : k)*t' = 0 := by
    simpa [ad1_value,x,y,t,u,v,r,e,f,unitVec,smul_eq_mul] using congrFun H 27
  have hs : s = 0 := (mul_eq_zero.mp hs0).resolve_left (by decide)
  have ht' : t' = 0 := (mul_eq_zero.mp ht0).resolve_left (by decide)
  have ha : (6 : k)*a+6*c = 6*c := by
    simpa [hs,ht',ad1_value,x,y,t,u,v,r,e,f,unitVec,smul_eq_mul] using (congrFun H 3).symm
  have hb : (6 : k)*b = 0 := by
    simpa [hs,ht',ad1_value,x,y,t,u,v,r,e,f,unitVec,smul_eq_mul] using (congrFun H 4).symm
  obtain ⟨_,_,ha0,hb0⟩ := Kourovka.FlagScalars.derivation_first_stage
    (by decide : (6 : k) ≠ 0) a b s t' c hs0 ht0 ha hb
  simpa [ha0,hb0] using hx

theorem derivation_ad_images (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hx : D x = 0) (c d : k) (hy : D y = c • x + d • y) :
    D ad1 = d • ad1 ∧ D ad2 = d • ad2 ∧ D ad3 = d • ad3 := by
  unfold IsDerivation at hD
  have h1 : D ad1 = d • ad1 := by
    dsimp only [ad1]
    rw [hD,hx,hy]
    simp only [map_zero,LinearMap.zero_apply,map_add,map_smul,alternating,
      smul_zero,zero_add]
  have h2 : D ad2 = d • ad2 := by
    dsimp only [ad2]
    rw [hD,hx,h1]
    simp only [map_zero,LinearMap.zero_apply,zero_add,map_smul]
  have h3 : D ad3 = d • ad3 := by
    dsimp only [ad3]
    rw [hD,hx,h2]
    simp only [map_zero,LinearMap.zero_apply,zero_add,map_smul]
  exact ⟨h1,h2,h3⟩

/-- Full infinitesimal rigidity, not a rank-only assertion about a selected family. -/
theorem infinitesimal_flag_rigidity (D : E →ₗ[k] E) (hD : IsDerivation D)
    (hF2 : ∀ a, a ∈ F2 → D a ∈ F2)
    (hF3 : ∀ a, a ∈ F3 → D a ∈ F3) : D = 0 := by
  unfold IsDerivation at hD
  have hx : D x = 0 := derivation_kills_x D hD (hF2 x x_mem_F2) (hF3 t t_mem_F3)
  obtain ⟨c,d,hy⟩ := hF2 y y_mem_F2
  obtain ⟨h1,h2,h3⟩ := derivation_ad_images D hD hx c d hy
  have he : D e = d • e := map_piece D d 16 8 2 (-1) e
    (by decide) h1 h2 h3 e_projector
  have hf : D f = d • f := map_piece D d 48 (-8) 6 (-1) f
    (by decide) h1 h2 h3 f_projector
  have huv : D uv = d • uv := map_piece D d 48 (-4) 0 1 uv
    (by decide) h1 h2 h3 uv_projector
  have hr : D (r 2) = c • x + d • r 2 := map_r_piece D c d hy h1 h2 h3
  have hd : d = 0 := by
    have hh := hD e f
    rw [ef,hx,he,hf] at hh
    simp only [map_smul,LinearMap.smul_apply,ef] at hh
    have hz : (2 : k)*d = 0 := by
      have hh' := (congrFun hh 0).symm
      simpa [x,unitVec,smul_eq_mul,two_mul] using hh'
    exact (mul_eq_zero.mp hz).resolve_left (by decide)
  have he0 : D e = 0 := by simpa [hd] using he
  have huv0 : D uv = 0 := by simpa [hd] using huv
  have ht : D t = 0 := by
    calc
      D t = D (B e uv) := congrArg D euv.symm
      _ = B (D e) uv + B e (D uv) := hD e uv
      _ = 0 := by simp only [he0,huv0,map_zero,LinearMap.zero_apply,add_zero]
  have hc : c = 0 := by
    have hh := hD (r 2) t
    rw [rt,map_zero,hr,ht] at hh
    simp only [hd,zero_smul,add_zero,map_zero,map_smul,LinearMap.smul_apply,
      xt,smul_smul] at hh
    have hz : c*(6 : k) = 0 := by
      simpa [t,u,unitVec,smul_eq_mul] using (congrFun hh 3).symm
    exact (mul_eq_zero.mp hz).resolve_right (by decide)
  have hy0 : D y = 0 := by simpa [hc,hd] using hy
  apply LinearMap.ext
  intro a
  exact Generation.zero_all D hD hx hy0 a

/- The preceding result applies to the ordinary mathlib LieEquiv type. -/
section LieEquivalences
local instance : LieRing E := Ambient.lieRing k
local instance : LieAlgebra k E := Ambient.lieAlgebra k

theorem lieEquiv_flag_rigidity (Q : E ≃ₗ⁅k⁆ E)
    (hF2 : ∀ a, a ∈ F2 → Q a ∈ F2)
    (hF3 : ∀ a, a ∈ F3 → Q a ∈ F3) : Q = LieEquiv.refl := by
  have hQ : Preserves Q.toLinearEquiv.toLinearMap := by
    intro a b
    exact Q.map_lie a b
  have hh := full_flag_rigidity Q.toLinearEquiv hQ hF2 hF3
  apply LieEquiv.ext
  intro a
  exact congrArg (fun f : E ≃ₗ[k] E => f a) hh
end LieEquivalences

end Kourovka.Flag
