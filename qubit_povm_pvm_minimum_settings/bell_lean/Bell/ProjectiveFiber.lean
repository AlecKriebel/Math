import Bell.Lorentz

/-!
# Total projective-fiber injectivity (paper Proposition 9.1)

This module supplies proof-source for the full generic/exceptional case split,
not just symbolic identities on a generic chart.  In particular, the four
exceptional planes are handled by homogeneous *quadratic* reconstruction maps.
Their reconstruction scalars are shown nonzero before they are inverted.

The quadratic maps provide an alternative to the resultant/root-uniqueness
arguments in Appendix G.  The only metric hypotheses used are the fields of
`StrictParameters`; Lorentz signature is not inserted as an implicit premise.

Execution status is recorded in `reports/status.json`.  This file must not be
represented as kernel checked until an actual Lean build has succeeded.
-/

noncomputable section
namespace Bell.Lorentz

/-- Equality of nonzero projective representatives.  Zero vectors are not
excluded by this definition alone; callers separately enforce nonzero images. -/
def SameRay (x z : V) : Prop := ∃ s : ℝ, s ≠ 0 ∧ x = s • z

@[simp]
theorem phi_zero : phi (0 : V) = 0 := by
  funext i
  fin_cases i <;> norm_num [phi]

theorem phi_homogeneous (x : V) (s : ℝ) :
    phi (s • x) = s^2 • phi x := by
  funext i
  fin_cases i <;> norm_num [phi] <;> ring

theorem null_homogeneous (a b c d s : ℝ) (x : V) :
    nullPolynomial a b c d (s • x) = s^2 * nullPolynomial a b c d x := by
  simp only [nullPolynomial, Pi.smul_apply, smul_eq_mul]
  ring

theorem sameRay_refl (x : V) : SameRay x x :=
  ⟨1, by norm_num, by simp⟩

theorem sameRay_symm {x z : V} (h : SameRay x z) : SameRay z x := by
  obtain ⟨s, hs, hx⟩ := h
  refine ⟨s⁻¹, inv_ne_zero hs, ?_⟩
  rw [hx, smul_smul, inv_mul_cancel₀ hs, one_smul]

theorem sameRay_trans {x y z : V} (hxy : SameRay x y) (hyz : SameRay y z) :
    SameRay x z := by
  obtain ⟨s, hs, hx⟩ := hxy
  obtain ⟨t, ht, hy⟩ := hyz
  exact ⟨s*t, mul_ne_zero hs ht, by rw [hx, hy, smul_smul]⟩

theorem nonzero_image_implies_nonzero {x : V} (hx : phi x ≠ 0) : x ≠ 0 := by
  intro h
  exact hx (by rw [h, phi_zero])

/-- A homogeneous inverse identity turns proportional images into proportional
sources.  Only the left reconstruction scalar is divided by. -/
theorem sameRay_of_homogeneous_inverse
    (F : V → V) (n : ℕ) (x z : V) (wx wz t : ℝ)
    (hhom : ∀ ξ s, F (s • ξ) = s^n • F ξ)
    (hleft : F (phi x) = wx • x)
    (hright : F (phi z) = wz • z)
    (hw : wx ≠ 0) (hx : phi x ≠ 0)
    (himage : phi x = t • phi z) : SameRay x z := by
  have hrec : x = wx⁻¹ • F (phi x) := by
    rw [hleft, smul_smul, inv_mul_cancel₀ hw, one_smul]
  have heq : x = (wx⁻¹ * t^n * wz) • z := by
    calc
      x = wx⁻¹ • F (phi x) := hrec
      _ = wx⁻¹ • F (t • phi z) := by rw [himage]
      _ = wx⁻¹ • (t^n • (wz • z)) := by rw [hhom, hright]
      _ = (wx⁻¹ * t^n * wz) • z := by simp only [smul_smul, mul_assoc]
  refine ⟨wx⁻¹ * t^n * wz, ?_, heq⟩
  intro hzero
  have hzero' : x = 0 := by simpa [hzero] using heq
  exact nonzero_image_implies_nonzero hx hzero'

/-- Target-coordinate zeros transfer across a nonzero projective scale. -/
theorem image_zero_transfers (x z : V) (t : ℝ) (ht : t ≠ 0)
    (himage : phi x = t • phi z) (i : Fin 4) (hi : phi x i = 0) :
    phi z i = 0 := by
  have h := congrFun himage i
  simp only [Pi.smul_apply, smul_eq_mul] at h
  have hm : t * phi z i = 0 := h.symm.trans hi
  exact (mul_eq_zero.mp hm).resolve_left ht

/-- Equal target-coordinate pairs transfer across a nonzero projective scale. -/
theorem image_eq_transfers (x z : V) (t : ℝ) (ht : t ≠ 0)
    (himage : phi x = t • phi z) (i j : Fin 4)
    (hij : phi x i = phi x j) : phi z i = phi z j := by
  have hi := congrFun himage i
  have hj := congrFun himage j
  simp only [Pi.smul_apply, smul_eq_mul] at hi hj
  have hm : t * (phi z i - phi z j) = 0 := by
    calc
      t * (phi z i - phi z j) = t*phi z i - t*phi z j := by ring
      _ = phi x i - phi x j := by rw [← hi, ← hj]
      _ = 0 := sub_eq_zero.mpr hij
  exact sub_eq_zero.mp ((mul_eq_zero.mp hm).resolve_left ht)

/-- Vanishing spatial pair is always in the base locus of `phi`. -/
theorem phi_zero_of_last_pair_zero (x : V) (h₂ : x 2 = 0) (h₃ : x 3 = 0) :
    phi x = 0 := by
  funext i
  fin_cases i <;> simp [phi, h₂, h₃]

/-- On the first-pair-zero plane, nullness forces a base point. -/
theorem phi_zero_of_first_pair_zero (g : StrictParameters) (x : V)
    (hn : nullPolynomial g.a g.b g.c g.d x = 0)
    (h₀ : x 0 = 0) (h₁ : x 1 = 0) : phi x = 0 := by
  have hm : (2*(g.a+g.b+g.c+g.d-1/2)) * (x 2*x 3) = 0 := by
    calc
      _ = nullPolynomial g.a g.b g.c g.d x := by
        simp only [nullPolynomial, h₀, h₁]
        ring
      _ = 0 := hn
  have hc : 2*(g.a+g.b+g.c+g.d-1/2) ≠ 0 := by
    have he := g.e_pos
    linarith
  have h23 := (mul_eq_zero.mp hm).resolve_left hc
  funext i
  fin_cases i <;> simp [phi, h₀, h₁, h23, mul_comm]

/-- The common fifth base line, in a coordinate form convenient for guards. -/
theorem phi_zero_of_fifth_line (x : V)
    (h₀ : x 0 = -x 2) (h₁ : x 1 = -x 2) (h₃ : x 3 = x 2) :
    phi x = 0 := by
  funext i
  fin_cases i <;> simp [phi, h₀, h₁, h₃]

/-! ## Quadratic inverse on `x 2 = 0` -/

def zero2Coefficient (g : StrictParameters) (ξ : V) : ℝ :=
  -2 * (g.b * ξ 1 + g.d * ξ 3)

def zero2Inverse (g : StrictParameters) (ξ : V) : V :=
  ![ξ 1 * zero2Coefficient g ξ, ξ 3 * zero2Coefficient g ξ,
    0, ξ 1 * ξ 3]

def zero2Weight (x : V) : ℝ := x 0 * x 1 * x 3

theorem zero2Inverse_homogeneous (g : StrictParameters) (ξ : V) (s : ℝ) :
    zero2Inverse g (s • ξ) = s^2 • zero2Inverse g ξ := by
  funext i
  fin_cases i <;> norm_num [zero2Inverse, zero2Coefficient] <;> ring

theorem zero2Coefficient_of_null (g : StrictParameters) (x : V)
    (h₂ : x 2 = 0) (hn : nullPolynomial g.a g.b g.c g.d x = 0) :
    zero2Coefficient g (phi x) = x 0*x 1 := by
  unfold nullPolynomial at hn
  rw [h₂] at hn
  norm_num [zero2Coefficient, phi, h₂]
  linear_combination -hn

theorem zero2Inverse_identity (g : StrictParameters) (x : V)
    (h₂ : x 2 = 0) (hn : nullPolynomial g.a g.b g.c g.d x = 0) :
    zero2Inverse g (phi x) = zero2Weight x • x := by
  unfold zero2Inverse
  rw [zero2Coefficient_of_null g x h₂ hn]
  funext i
  fin_cases i <;> norm_num [phi, zero2Weight, h₂] <;> ring

theorem zero2Weight_nonzero (g : StrictParameters) (x : V)
    (h₂ : x 2 = 0) (hn : nullPolynomial g.a g.b g.c g.d x = 0)
    (hp : phi x ≠ 0) : zero2Weight x ≠ 0 := by
  have h₃ : x 3 ≠ 0 := by
    intro h₃
    exact hp (phi_zero_of_last_pair_zero x h₂ h₃)
  have h₀ : x 0 ≠ 0 := by
    intro h₀
    have hm : (2*g.d*x 3) * x 1 = 0 := by
      calc
        _ = nullPolynomial g.a g.b g.c g.d x := by
          simp only [nullPolynomial, h₀, h₂]
          ring
        _ = 0 := hn
    have hc : 2*g.d*x 3 ≠ 0 := mul_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt g.d_pos)) h₃
    have h₁ := (mul_eq_zero.mp hm).resolve_left hc
    exact hp (phi_zero_of_first_pair_zero g x hn h₀ h₁)
  have h₁ : x 1 ≠ 0 := by
    intro h₁
    have hm : (2*g.b*x 3) * x 0 = 0 := by
      calc
        _ = nullPolynomial g.a g.b g.c g.d x := by
          simp only [nullPolynomial, h₁, h₂]
          ring
        _ = 0 := hn
    have hc : 2*g.b*x 3 ≠ 0 := mul_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt g.b_pos)) h₃
    exact h₀ ((mul_eq_zero.mp hm).resolve_left hc)
  exact mul_ne_zero (mul_ne_zero h₀ h₁) h₃

/-- The target-zero equations cannot move to the cross branch on the null
quadric: its only possible nonzero null source would have zero image. -/
theorem zero2_plane_of_target (g : StrictParameters) (z : V)
    (hn : nullPolynomial g.a g.b g.c g.d z = 0) (hp : phi z ≠ 0)
    (h₀ : phi z 0 = 0) (h₂ : phi z 2 = 0) : z 2 = 0 := by
  by_contra hz₂
  have ha : z 0 = -z 3 := by
    have hh : z 2*(z 0+z 3) = 0 := by simpa [phi] using h₀
    have hh' := (mul_eq_zero.mp hh).resolve_left hz₂
    linarith
  have hb : z 1 = -z 3 := by
    have hh : z 2*(z 1+z 3) = 0 := by simpa [phi] using h₂
    have hh' := (mul_eq_zero.mp hh).resolve_left hz₂
    linarith
  have hz₃ : z 3 ≠ 0 := by
    intro hz₃
    apply hp
    funext i
    fin_cases i <;> simp [phi, ha, hb, hz₃]
  have hfac : (1-2*(g.b+g.d))*z 3*(z 3-z 2) = 0 := by
    calc
      _ = nullPolynomial g.a g.b g.c g.d z := by
        simp only [nullPolynomial, ha, hb]
        ring
      _ = 0 := hn
  have hc : (1-2*(g.b+g.d))*z 3 ≠ 0 := by
    exact mul_ne_zero (by have h := g.bd_lt; linarith) hz₃
  have heq : z 3 = z 2 := sub_eq_zero.mp ((mul_eq_zero.mp hfac).resolve_left hc)
  exact hp (phi_zero_of_fifth_line z (by simpa [heq] using ha)
    (by simpa [heq] using hb) heq)

/-! ## Quadratic inverse on `x 3 = 0` -/

def zero3Coefficient (g : StrictParameters) (ξ : V) : ℝ :=
  -2 * (g.a * ξ 0 + g.c * ξ 2)

def zero3Inverse (g : StrictParameters) (ξ : V) : V :=
  ![ξ 0 * zero3Coefficient g ξ, ξ 2 * zero3Coefficient g ξ,
    ξ 0 * ξ 2, 0]

def zero3Weight (x : V) : ℝ := x 0 * x 1 * x 2

theorem zero3Inverse_homogeneous (g : StrictParameters) (ξ : V) (s : ℝ) :
    zero3Inverse g (s • ξ) = s^2 • zero3Inverse g ξ := by
  funext i
  fin_cases i <;> norm_num [zero3Inverse, zero3Coefficient] <;> ring

theorem zero3Coefficient_of_null (g : StrictParameters) (x : V)
    (h₃ : x 3 = 0) (hn : nullPolynomial g.a g.b g.c g.d x = 0) :
    zero3Coefficient g (phi x) = x 0*x 1 := by
  unfold nullPolynomial at hn
  rw [h₃] at hn
  norm_num [zero3Coefficient, phi, h₃]
  linear_combination -hn

theorem zero3Inverse_identity (g : StrictParameters) (x : V)
    (h₃ : x 3 = 0) (hn : nullPolynomial g.a g.b g.c g.d x = 0) :
    zero3Inverse g (phi x) = zero3Weight x • x := by
  unfold zero3Inverse
  rw [zero3Coefficient_of_null g x h₃ hn]
  funext i
  fin_cases i <;> norm_num [phi, zero3Weight, h₃] <;> ring

theorem zero3Weight_nonzero (g : StrictParameters) (x : V)
    (h₃ : x 3 = 0) (hn : nullPolynomial g.a g.b g.c g.d x = 0)
    (hp : phi x ≠ 0) : zero3Weight x ≠ 0 := by
  have h₂ : x 2 ≠ 0 := by
    intro h₂
    exact hp (phi_zero_of_last_pair_zero x h₂ h₃)
  have h₀ : x 0 ≠ 0 := by
    intro h₀
    have hm : (2*g.c*x 2) * x 1 = 0 := by
      calc
        _ = nullPolynomial g.a g.b g.c g.d x := by
          simp only [nullPolynomial, h₀, h₃]
          ring
        _ = 0 := hn
    have hc : 2*g.c*x 2 ≠ 0 := mul_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt g.c_pos)) h₂
    have h₁ := (mul_eq_zero.mp hm).resolve_left hc
    exact hp (phi_zero_of_first_pair_zero g x hn h₀ h₁)
  have h₁ : x 1 ≠ 0 := by
    intro h₁
    have hm : (2*g.a*x 2) * x 0 = 0 := by
      calc
        _ = nullPolynomial g.a g.b g.c g.d x := by
          simp only [nullPolynomial, h₁, h₃]
          ring
        _ = 0 := hn
    have hc : 2*g.a*x 2 ≠ 0 := mul_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt g.a_pos)) h₂
    exact h₀ ((mul_eq_zero.mp hm).resolve_left hc)
  exact mul_ne_zero (mul_ne_zero h₀ h₁) h₂

theorem zero3_plane_of_target (g : StrictParameters) (z : V)
    (hn : nullPolynomial g.a g.b g.c g.d z = 0) (hp : phi z ≠ 0)
    (h₁ : phi z 1 = 0) (h₃ : phi z 3 = 0) : z 3 = 0 := by
  by_contra hz₃
  have ha : z 0 = -z 2 := by
    have hh : z 3*(z 0+z 2) = 0 := by simpa [phi] using h₁
    have hh' := (mul_eq_zero.mp hh).resolve_left hz₃
    linarith
  have hb : z 1 = -z 2 := by
    have hh : z 3*(z 1+z 2) = 0 := by simpa [phi] using h₃
    have hh' := (mul_eq_zero.mp hh).resolve_left hz₃
    linarith
  have hz₂ : z 2 ≠ 0 := by
    intro hz₂
    apply hp
    funext i
    fin_cases i <;> simp [phi, ha, hb, hz₂]
  have hfac : (1-2*(g.a+g.c))*z 2*(z 2-z 3) = 0 := by
    calc
      _ = nullPolynomial g.a g.b g.c g.d z := by
        simp only [nullPolynomial, ha, hb]
        ring
      _ = 0 := hn
  have hc : (1-2*(g.a+g.c))*z 2 ≠ 0 := by
    exact mul_ne_zero (by have h := g.ac_lt; linarith) hz₂
  have heq : z 3 = z 2 := by
    have hh := (mul_eq_zero.mp hfac).resolve_left hc
    linarith
  exact hp (phi_zero_of_fifth_line z ha hb heq)

/-! ## Quadratic inverse on `x 0 = x 1` -/

def equal01Coefficient (g : StrictParameters) (ξ : V) : ℝ :=
  (1-2*(g.a+g.c))*ξ 0 + (1-2*(g.b+g.d))*ξ 1

def equal01Inverse (g : StrictParameters) (ξ : V) : V :=
  ![(equal01Coefficient g ξ-ξ 0)*(equal01Coefficient g ξ-ξ 1),
    (equal01Coefficient g ξ-ξ 0)*(equal01Coefficient g ξ-ξ 1),
    ξ 0*(equal01Coefficient g ξ-ξ 1),
    ξ 1*(equal01Coefficient g ξ-ξ 0)]

def equal01Weight (x : V) : ℝ := x 0*(x 0+x 2)*(x 0+x 3)

theorem equal01Inverse_homogeneous (g : StrictParameters) (ξ : V) (s : ℝ) :
    equal01Inverse g (s • ξ) = s^2 • equal01Inverse g ξ := by
  funext i
  fin_cases i <;> norm_num [equal01Inverse, equal01Coefficient] <;> ring

theorem equal01Coefficient_of_null (g : StrictParameters) (x : V)
    (h01 : x 0 = x 1) (hn : nullPolynomial g.a g.b g.c g.d x = 0) :
    equal01Coefficient g (phi x) = (x 0+x 2)*(x 0+x 3) := by
  unfold nullPolynomial at hn
  rw [← h01] at hn
  norm_num [equal01Coefficient, phi]
  linear_combination -hn

theorem equal01Inverse_identity (g : StrictParameters) (x : V)
    (h01 : x 0 = x 1) (hn : nullPolynomial g.a g.b g.c g.d x = 0) :
    equal01Inverse g (phi x) = equal01Weight x • x := by
  unfold equal01Inverse
  rw [equal01Coefficient_of_null g x h01 hn]
  funext i
  fin_cases i <;> norm_num [phi, equal01Weight, ← h01] <;> ring

theorem equal01Weight_nonzero (g : StrictParameters) (x : V)
    (h01 : x 0 = x 1) (hn : nullPolynomial g.a g.b g.c g.d x = 0)
    (hp : phi x ≠ 0) : equal01Weight x ≠ 0 := by
  have h₀ : x 0 ≠ 0 := by
    intro h₀
    exact hp (phi_zero_of_first_pair_zero g x hn h₀ (by rw [← h01, h₀]))
  have h02 : x 0+x 2 ≠ 0 := by
    intro hz
    have h₂ : x 2 = -x 0 := by linarith
    have hm : (1-2*(g.a+g.c))*x 0*(x 0+x 3) = 0 := by
      calc
        _ = nullPolynomial g.a g.b g.c g.d x := by
          simp only [nullPolynomial, ← h01, h₂]
          ring
        _ = 0 := hn
    have hc : (1-2*(g.a+g.c))*x 0 ≠ 0 := by
      exact mul_ne_zero (by have h := g.ac_lt; linarith) h₀
    have h₃ : x 3 = -x 0 := by
      have hh := (mul_eq_zero.mp hm).resolve_left hc
      linarith
    apply hp
    funext i
    fin_cases i <;> simp [phi, ← h01, h₂, h₃]
  have h03 : x 0+x 3 ≠ 0 := by
    intro hz
    have h₃ : x 3 = -x 0 := by linarith
    have hm : (1-2*(g.b+g.d))*x 0*(x 0+x 2) = 0 := by
      calc
        _ = nullPolynomial g.a g.b g.c g.d x := by
          simp only [nullPolynomial, ← h01, h₃]
          ring
        _ = 0 := hn
    have hc : (1-2*(g.b+g.d))*x 0 ≠ 0 := by
      exact mul_ne_zero (by have h := g.bd_lt; linarith) h₀
    exact h02 ((mul_eq_zero.mp hm).resolve_left hc)
  exact mul_ne_zero (mul_ne_zero h₀ h02) h03

/-- Equality of the appropriate target pairs forces the same source plane,
without assuming any generic coordinate is nonzero. -/
theorem equal01_plane_of_target (z : V) (hp : phi z ≠ 0)
    (h02 : phi z 0 = phi z 2) (h13 : phi z 1 = phi z 3) : z 0 = z 1 := by
  by_contra hz
  have hc : z 0-z 1 ≠ 0 := sub_ne_zero.mpr hz
  have hm₂ : z 2*(z 0-z 1) = 0 := by
    rw [← (phi_differences z).2.2.1, h02, sub_self]
  have hm₃ : z 3*(z 0-z 1) = 0 := by
    rw [← (phi_differences z).2.2.2, h13, sub_self]
  exact hp (phi_zero_of_last_pair_zero z
    ((mul_eq_zero.mp hm₂).resolve_right hc)
    ((mul_eq_zero.mp hm₃).resolve_right hc))

/-! ## Quadratic inverse on `x 2 = x 3` -/

def equal23Coefficient (g : StrictParameters) (ξ : V) : ℝ :=
  (1-2*(g.a+g.b))*ξ 0 + (1-2*(g.c+g.d))*ξ 2

def equal23Inverse (g : StrictParameters) (ξ : V) : V :=
  ![ξ 0*equal23Coefficient g ξ-ξ 0*ξ 2,
    ξ 2*equal23Coefficient g ξ-ξ 0*ξ 2,
    ξ 0*ξ 2, ξ 0*ξ 2]

def equal23Weight (x : V) : ℝ := x 2*(x 0+x 2)*(x 1+x 2)

theorem equal23Inverse_homogeneous (g : StrictParameters) (ξ : V) (s : ℝ) :
    equal23Inverse g (s • ξ) = s^2 • equal23Inverse g ξ := by
  funext i
  fin_cases i <;> norm_num [equal23Inverse, equal23Coefficient] <;> ring

theorem equal23Coefficient_of_null (g : StrictParameters) (x : V)
    (h23 : x 2 = x 3) (hn : nullPolynomial g.a g.b g.c g.d x = 0) :
    equal23Coefficient g (phi x) = (x 0+x 2)*(x 1+x 2) := by
  unfold nullPolynomial at hn
  rw [← h23] at hn
  norm_num [equal23Coefficient, phi, ← h23]
  linear_combination -hn

theorem equal23Inverse_identity (g : StrictParameters) (x : V)
    (h23 : x 2 = x 3) (hn : nullPolynomial g.a g.b g.c g.d x = 0) :
    equal23Inverse g (phi x) = equal23Weight x • x := by
  unfold equal23Inverse
  rw [equal23Coefficient_of_null g x h23 hn]
  funext i
  fin_cases i <;> norm_num [phi, equal23Weight, ← h23] <;> ring

theorem equal23Weight_nonzero (g : StrictParameters) (x : V)
    (h23 : x 2 = x 3) (hn : nullPolynomial g.a g.b g.c g.d x = 0)
    (hp : phi x ≠ 0) : equal23Weight x ≠ 0 := by
  have h₂ : x 2 ≠ 0 := by
    intro h₂
    exact hp (phi_zero_of_last_pair_zero x h₂ (by rw [← h23, h₂]))
  have h02 : x 0+x 2 ≠ 0 := by
    intro hz
    have h₀ : x 0 = -x 2 := by linarith
    have hm : (2*(g.c+g.d)-1)*x 2*(x 1+x 2) = 0 := by
      calc
        _ = nullPolynomial g.a g.b g.c g.d x := by
          simp only [nullPolynomial, ← h23, h₀]
          ring
        _ = 0 := hn
    have hc : (2*(g.c+g.d)-1)*x 2 ≠ 0 := by
      exact mul_ne_zero (by have h := g.cd_lt; linarith) h₂
    have h₁ : x 1 = -x 2 := by
      have hh := (mul_eq_zero.mp hm).resolve_left hc
      linarith
    exact hp (phi_zero_of_fifth_line x h₀ h₁ h23.symm)
  have h12 : x 1+x 2 ≠ 0 := by
    intro hz
    have h₁ : x 1 = -x 2 := by linarith
    have hm : (2*(g.a+g.b)-1)*x 2*(x 0+x 2) = 0 := by
      calc
        _ = nullPolynomial g.a g.b g.c g.d x := by
          simp only [nullPolynomial, ← h23, h₁]
          ring
        _ = 0 := hn
    have hc : (2*(g.a+g.b)-1)*x 2 ≠ 0 := by
      exact mul_ne_zero (by have h := g.ab_lt; linarith) h₂
    exact h02 ((mul_eq_zero.mp hm).resolve_left hc)
  exact mul_ne_zero (mul_ne_zero h₂ h02) h12

theorem equal23_plane_of_target (g : StrictParameters) (z : V)
    (hn : nullPolynomial g.a g.b g.c g.d z = 0) (hp : phi z ≠ 0)
    (h01 : phi z 0 = phi z 1) (h23 : phi z 2 = phi z 3) : z 2 = z 3 := by
  by_contra hz
  have hc : z 2-z 3 ≠ 0 := sub_ne_zero.mpr hz
  have hm₀ : z 0*(z 2-z 3) = 0 := by
    rw [← (phi_differences z).1, h01, sub_self]
  have hm₁ : z 1*(z 2-z 3) = 0 := by
    rw [← (phi_differences z).2.1, h23, sub_self]
  exact hp (phi_zero_of_first_pair_zero g z hn
    ((mul_eq_zero.mp hm₀).resolve_right hc)
    ((mul_eq_zero.mp hm₁).resolve_right hc))

/-! ## Exhaustive assembly -/

/-- Full projective injectivity on the strict null quadric away from its base
locus.  The case split includes all intersections of the exceptional planes.
No theorem about the physical incidence manifold is assumed in this result. -/
theorem projective_fiber_injective (g : StrictParameters) (x z : V)
    (hnx : nullPolynomial g.a g.b g.c g.d x = 0)
    (hnz : nullPolynomial g.a g.b g.c g.d z = 0)
    (hpx : phi x ≠ 0) (t : ℝ) (ht : t ≠ 0)
    (himage : phi x = t • phi z) : SameRay x z := by
  have hpz : phi z ≠ 0 := by
    intro hz
    apply hpx
    simpa [hz] using himage
  by_cases hx₂ : x 2 = 0
  · have hz₂ : z 2 = 0 := zero2_plane_of_target g z hnz hpz
      (image_zero_transfers x z t ht himage 0 (by simp [phi, hx₂]))
      (image_zero_transfers x z t ht himage 2 (by simp [phi, hx₂]))
    exact sameRay_of_homogeneous_inverse (zero2Inverse g) 2 x z
      (zero2Weight x) (zero2Weight z) t (zero2Inverse_homogeneous g)
      (zero2Inverse_identity g x hx₂ hnx) (zero2Inverse_identity g z hz₂ hnz)
      (zero2Weight_nonzero g x hx₂ hnx hpx) hpx himage
  by_cases hx₃ : x 3 = 0
  · have hz₃ : z 3 = 0 := zero3_plane_of_target g z hnz hpz
      (image_zero_transfers x z t ht himage 1 (by simp [phi, hx₃]))
      (image_zero_transfers x z t ht himage 3 (by simp [phi, hx₃]))
    exact sameRay_of_homogeneous_inverse (zero3Inverse g) 2 x z
      (zero3Weight x) (zero3Weight z) t (zero3Inverse_homogeneous g)
      (zero3Inverse_identity g x hx₃ hnx) (zero3Inverse_identity g z hz₃ hnz)
      (zero3Weight_nonzero g x hx₃ hnx hpx) hpx himage
  by_cases hx01 : x 0 = x 1
  · have hz01 : z 0 = z 1 := equal01_plane_of_target z hpz
      (image_eq_transfers x z t ht himage 0 2 (by simp [phi, hx01]))
      (image_eq_transfers x z t ht himage 1 3 (by simp [phi, hx01]))
    exact sameRay_of_homogeneous_inverse (equal01Inverse g) 2 x z
      (equal01Weight x) (equal01Weight z) t (equal01Inverse_homogeneous g)
      (equal01Inverse_identity g x hx01 hnx) (equal01Inverse_identity g z hz01 hnz)
      (equal01Weight_nonzero g x hx01 hnx hpx) hpx himage
  by_cases hx23 : x 2 = x 3
  · have hz23 : z 2 = z 3 := equal23_plane_of_target g z hnz hpz
      (image_eq_transfers x z t ht himage 0 1 (by simp [phi, hx23]))
      (image_eq_transfers x z t ht himage 2 3 (by simp [phi, hx23]))
    exact sameRay_of_homogeneous_inverse (equal23Inverse g) 2 x z
      (equal23Weight x) (equal23Weight z) t (equal23Inverse_homogeneous g)
      (equal23Inverse_identity g x hx23 hnx) (equal23Inverse_identity g z hz23 hnz)
      (equal23Weight_nonzero g x hx23 hnx hpx) hpx himage
  have hw : omega x ≠ 0 := by
    exact mul_ne_zero
      (mul_ne_zero (mul_ne_zero hx₂ hx₃) (sub_ne_zero.mpr hx23))
      (pow_ne_zero 2 (sub_ne_zero.mpr hx01))
  exact sameRay_of_homogeneous_inverse inversePolynomial 3 x z
    (omega x) (omega z) t inverse_homogeneous
    (inverse_identity x) (inverse_identity z) hw hpx himage

/-- Projective-quotient formulation of the same total theorem. -/
theorem projective_fiber_injective_of_sameRay (g : StrictParameters) (x z : V)
    (hnx : nullPolynomial g.a g.b g.c g.d x = 0)
    (hnz : nullPolynomial g.a g.b g.c g.d z = 0)
    (hpx : phi x ≠ 0) (h : SameRay (phi x) (phi z)) : SameRay x z := by
  obtain ⟨t, ht, himage⟩ := h
  exact projective_fiber_injective g x z hnx hnz hpx t ht himage

end Bell.Lorentz
