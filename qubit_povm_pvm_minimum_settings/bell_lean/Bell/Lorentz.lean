import Mathlib

/-!
# Finite Lorentz-incidence algebra (paper §§5–9, Appendices F/G)

The identities below are universally quantified, not instance checks.  The
matrix-to-physical-strategy reconstruction, smoothness, multiplier theorem,
inertia argument, and global projective-fiber case assembly remain separate
formalization obligations.  `StrictParameters` records scalar inequalities;
it does NOT silently assert that they imply Lorentz signature.
-/

noncomputable section
open scoped BigOperators Matrix
namespace Bell.Lorentz

abbrev V := Fin 4 → ℝ
abbrev M := Matrix (Fin 4) (Fin 4) ℝ

def ray : Fin 5 → V :=
  ![ ![1,0,0,0], ![0,1,0,0], ![0,0,1,0], ![0,0,0,1], ![1,1,-1,-1] ]

def unitVector : V := ![1,1,0,0]

theorem binary_circuit : ray 0 + ray 1 = unitVector := by
  funext i
  fin_cases i <;> norm_num [ray, unitVector]

theorem ternary_circuit : ray 2 + ray 3 + ray 4 = unitVector := by
  funext i
  fin_cases i <;> norm_num [ray, unitVector]

/-- The unique local circuit, including all coefficient vectors in its kernel. -/
theorem circuit_kernel (μ : Fin 5 → ℝ) :
    (∑ j, μ j • ray j = 0) ↔ ∃ t : ℝ, μ = ![t,t,-t,-t,-t] := by
  constructor
  · intro h
    have h₀ := congrFun h 0
    have h₁ := congrFun h 1
    have h₂ := congrFun h 2
    have h₃ := congrFun h 3
    norm_num [ray, Fin.sum_univ_succ] at h₀ h₁ h₂ h₃
    refine ⟨μ 0, ?_⟩
    funext j
    fin_cases j <;> norm_num <;> linarith
  · rintro ⟨t, rfl⟩
    funext i
    fin_cases i <;> norm_num [ray, Fin.sum_univ_succ] <;> ring

def weightedOuter (μ : Fin 5 → ℝ) : M :=
  fun i k => ∑ j, μ j * ray j i * ray j k

/-- Independence of the five rank-one coefficient matrices (Proposition 6.2). -/
theorem weightedOuter_injective_zero (μ : Fin 5 → ℝ)
    (h : weightedOuter μ = 0) : μ = 0 := by
  have hoff := congrArg (fun A : M => A 0 1) h
  norm_num [weightedOuter, ray, Fin.sum_univ_succ] at hoff
  have h₀ := congrArg (fun A : M => A 0 0) h
  have h₁ := congrArg (fun A : M => A 1 1) h
  have h₂ := congrArg (fun A : M => A 2 2) h
  have h₃ := congrArg (fun A : M => A 3 3) h
  norm_num [weightedOuter, ray, Fin.sum_univ_succ] at h₀ h₁ h₂ h₃
  funext j
  fin_cases j <;> norm_num <;> linarith

def metric (a b c d : ℝ) : M :=
  !![0, 1/2, a, b;
     1/2, 0, c, d;
     a, c, 0, a+b+c+d-1/2;
     b, d, a+b+c+d-1/2, 0]

def nullPolynomial (a b c d : ℝ) (x : V) : ℝ :=
  x 0 * x 1 + 2*a*x 0*x 2 + 2*b*x 0*x 3 +
  2*c*x 1*x 2 + 2*d*x 1*x 3 + 2*(a+b+c+d-1/2)*x 2*x 3

structure StrictParameters where
  a : ℝ
  b : ℝ
  c : ℝ
  d : ℝ
  a_pos : 0 < a
  b_pos : 0 < b
  c_pos : 0 < c
  d_pos : 0 < d
  e_pos : 0 < a + b + c + d - 1/2
  ab_lt : a + b < 1/2
  cd_lt : c + d < 1/2
  ac_lt : a + c < 1/2
  bd_lt : b + d < 1/2

theorem metric_quadratic (a b c d : ℝ) (x : V) :
    dotProduct x (metric a b c d *ᵥ x) = nullPolynomial a b c d x := by
  simp [dotProduct, Matrix.mulVec, metric, nullPolynomial, Fin.sum_univ_succ]
  <;> ring

theorem coefficient_rays_null (a b c d : ℝ) (j : Fin 5) :
    nullPolynomial a b c d (ray j) = 0 := by
  fin_cases j <;> norm_num [nullPolynomial, ray] <;> ring

theorem metric_normalization (a b c d : ℝ) :
    nullPolynomial a b c d unitVector = 1 := by
  norm_num [nullPolynomial, unitVector]

def phi (x : V) : V :=
  ![x 2*(x 0+x 3), x 3*(x 0+x 2), x 2*(x 1+x 3), x 3*(x 1+x 2)]

def omega (x : V) : ℝ := x 2*x 3*(x 2-x 3)*(x 0-x 1)^2

def inversePolynomial (ξ : V) : V :=
  ![(ξ 0-ξ 1)*(ξ 0-ξ 2)*(ξ 1-ξ 3),
    (ξ 2-ξ 3)*(ξ 0-ξ 2)*(ξ 1-ξ 3),
    (ξ 0*ξ 3-ξ 1*ξ 2)*(ξ 0-ξ 2),
    (ξ 0*ξ 3-ξ 1*ξ 2)*(ξ 1-ξ 3)]

theorem phi_differences (x : V) :
    phi x 0 - phi x 1 = x 0*(x 2-x 3) ∧
    phi x 2 - phi x 3 = x 1*(x 2-x 3) ∧
    phi x 0 - phi x 2 = x 2*(x 0-x 1) ∧
    phi x 1 - phi x 3 = x 3*(x 0-x 1) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num [phi] <;> ring

theorem phi_minor (x : V) :
    phi x 0 * phi x 3 - phi x 1 * phi x 2 =
      x 2*x 3*(x 0-x 1)*(x 2-x 3) := by
  norm_num [phi]
  <;> ring

/-- The exact generic inverse identity in Appendix G.1. -/
theorem inverse_identity (x : V) : inversePolynomial (phi x) = omega x • x := by
  funext i
  fin_cases i <;> norm_num [inversePolynomial, phi, omega] <;> ring

theorem inverse_homogeneous (ξ : V) (t : ℝ) :
    inversePolynomial (t • ξ) = t^3 • inversePolynomial ξ := by
  funext i
  fin_cases i <;> norm_num [inversePolynomial] <;> ring

/-- Explicit recovery on the generic chart; no division occurs until nonzero
`omega` has been supplied. -/
theorem generic_recovery (x : V) (hx : omega x ≠ 0) :
    (omega x)⁻¹ • inversePolynomial (phi x) = x := by
  rw [inverse_identity, smul_smul, inv_mul_cancel₀ hx, one_smul]

/-- Coordinate description of the five base lines; includes the zero vector. -/
def BaseLines (x : V) : Prop :=
  (x 1=0 ∧ x 2=0 ∧ x 3=0) ∨
  (x 0=0 ∧ x 2=0 ∧ x 3=0) ∨
  (x 0=0 ∧ x 1=0 ∧ x 3=0) ∨
  (x 0=0 ∧ x 1=0 ∧ x 2=0) ∨
  (x 0=x 1 ∧ x 2= -x 0 ∧ x 3= -x 0)

/-- Full algebraic base-locus implication, for every metric of the displayed
normal form. Nonzero vectors in these lines give the five projective rays. -/
theorem phi_zero_null_base (a b c d : ℝ) (x : V)
    (hp : phi x = 0) (hn : nullPolynomial a b c d x = 0) : BaseLines x := by
  have h₀ : x 2*(x 0+x 3)=0 := by simpa [phi] using congrFun hp 0
  have h₁ : x 3*(x 0+x 2)=0 := by simpa [phi] using congrFun hp 1
  have h₂ : x 2*(x 1+x 3)=0 := by simpa [phi] using congrFun hp 2
  have h₃ : x 3*(x 1+x 2)=0 := by simpa [phi] using congrFun hp 3
  by_cases hx2 : x 2=0
  · by_cases hx3 : x 3=0
    · have h01 : x 0*x 1=0 := by
        simpa [nullPolynomial, hx2, hx3] using hn
      rcases mul_eq_zero.mp h01 with hx0 | hx1
      · exact Or.inr (Or.inl ⟨hx0,hx2,hx3⟩)
      · exact Or.inl ⟨hx1,hx2,hx3⟩
    · have hx0 : x 0=0 := by
        have hh := (mul_eq_zero.mp h₁).resolve_left hx3
        simpa [hx2] using hh
      have hx1 : x 1=0 := by
        have hh := (mul_eq_zero.mp h₃).resolve_left hx3
        simpa [hx2] using hh
      exact Or.inr (Or.inr (Or.inr (Or.inl ⟨hx0,hx1,hx2⟩)))
  · by_cases hx3 : x 3=0
    · have hx0 : x 0=0 := by
        have hh := (mul_eq_zero.mp h₀).resolve_left hx2
        simpa [hx3] using hh
      have hx1 : x 1=0 := by
        have hh := (mul_eq_zero.mp h₂).resolve_left hx2
        simpa [hx3] using hh
      exact Or.inr (Or.inr (Or.inl ⟨hx0,hx1,hx3⟩))
    · have ha := (mul_eq_zero.mp h₀).resolve_left hx2
      have hb := (mul_eq_zero.mp h₁).resolve_left hx3
      have hc := (mul_eq_zero.mp h₂).resolve_left hx2
      exact Or.inr (Or.inr (Or.inr (Or.inr ⟨by linarith, by linarith, by linarith⟩)))

theorem baseLines_phi_zero (x : V) (hx : BaseLines x) : phi x = 0 := by
  rcases hx with h | h | h | h | h
  all_goals
    rcases h with ⟨h₀,h₁,h₂⟩
    funext i
    fin_cases i <;> simp [phi, h₀, h₁, h₂] <;> ring

/-- Cross-branch factorizations on both zero-coordinate divisors. -/
theorem cross_x2_identity (a b c d t : ℝ) :
    nullPolynomial a b c d ![-1,-1,t,1] = (1-2*(b+d))*(1-t) := by
  norm_num [nullPolynomial]
  <;> ring

theorem cross_x3_identity (a b c d t : ℝ) :
    nullPolynomial a b c d ![-1,-1,1,t] = (1-2*(a+c))*(1-t) := by
  norm_num [nullPolynomial]
  <;> ring

theorem cross_x2_is_base (a b c d t : ℝ) (hs : b+d < 1/2)
    (hn : nullPolynomial a b c d ![-1,-1,t,1] = 0) : t=1 := by
  rw [cross_x2_identity] at hn
  have hc : 1-2*(b+d) ≠ 0 := by linarith
  have hh := (mul_eq_zero.mp hn).resolve_left hc
  linarith

theorem cross_x3_is_base (a b c d t : ℝ) (hs : a+c < 1/2)
    (hn : nullPolynomial a b c d ![-1,-1,1,t] = 0) : t=1 := by
  rw [cross_x3_identity] at hn
  have hc : 1-2*(a+c) ≠ 0 := by linarith
  have hh := (mul_eq_zero.mp hn).resolve_left hc
  linarith

/-- Uniqueness of the nonbase root on either direct zero-coordinate branch. -/
theorem direct_zero_chart_unique (b d U V t s : ℝ)
    (hb : 0<b) (hd : 0<d) (hUV : U≠0 ∨ V≠0) (ht : t≠0) (hs : s≠0)
    (hnt : t^2*U*V + 2*t*(b*U+d*V)=0)
    (hns : s^2*U*V + 2*s*(b*U+d*V)=0) : t=s := by
  have hft : t*(t*U*V+2*(b*U+d*V))=0 := by nlinarith [hnt]
  have hfs : s*(s*U*V+2*(b*U+d*V))=0 := by nlinarith [hns]
  have hlt := (mul_eq_zero.mp hft).resolve_left ht
  have hls := (mul_eq_zero.mp hfs).resolve_left hs
  have hcoef : U*V ≠ 0 := by
    intro hz
    rcases mul_eq_zero.mp hz with hU | hV
    · have hV : V=0 := by
        have hv : d*V=0 := by nlinarith [hlt]
        exact (mul_eq_zero.mp hv).resolve_left (ne_of_gt hd)
      exact hUV.elim (fun h => h hU) (fun h => h hV)
    · have hU : U=0 := by
        have hu : b*U=0 := by nlinarith [hlt]
        exact (mul_eq_zero.mp hu).resolve_left (ne_of_gt hb)
      exact hUV.elim (fun h => h hU) (fun h => h hV)
  have heq : (t-s)*(U*V)=0 := by nlinarith [hlt,hls]
  have hh := (mul_eq_zero.mp heq).resolve_right hcoef
  linarith

/-- Determinant of the coefficients of two linear polynomials. -/
def linearEliminant (A B C D : ℝ) : ℝ := A*D-B*C

theorem linearEliminant_of_common_root (A B C D p : ℝ)
    (h₁ : A*p+B=0) (h₂ : C*p+D=0) : linearEliminant A B C D=0 := by
  unfold linearEliminant
  have hid : A*D-B*C = A*(C*p+D)-C*(A*p+B) := by ring
  rw [hid,h₁,h₂]
  ring

/-- Appendix G.4 resultant, implemented as its 2-by-2 determinant. -/
theorem resultant01 (A B U V q : ℝ) :
    linearEliminant (2*A+2*(A+B-1/2)*q) (1+2*B*q)
      (V*(1+q)-U*q) (-U*q) =
    -(q+1)*(V+q*(U*(2*A-1)+2*V*B)) := by
  unfold linearEliminant
  ring

/-- Appendix G.5 resultant. -/
theorem resultant23 (A B U V q : ℝ) :
    linearEliminant (q+2*A) (2*B*q+2*(A+B-1/2)) V (V-U*(q+1)) =
    -(q+1)*(U*q+2*U*A+2*V*B-V) := by
  unfold linearEliminant
  ring

theorem simultaneous_coefficient_obstruction01 (A B q : ℝ) :
    2*B*(2*A+2*(A+B-1/2)*q) -
      2*(A+B-1/2)*(1+2*B*q) = (2*A-1)*(2*B-1) := by ring

theorem simultaneous_coefficient_obstruction23 (A B q : ℝ) :
    2*B*(q+2*A) - (2*B*q+2*(A+B-1/2)) = (2*A-1)*(2*B-1) := by ring

/-- No coefficient degeneracy on the first normalized exceptional chart. -/
theorem null01_coefficient_nonzero (A B p q : ℝ) (hA : A<1/2) (hB : B<1/2)
    (hN : (2*A+2*(A+B-1/2)*q)*p+(1+2*B*q)=0) :
    2*A+2*(A+B-1/2)*q ≠ 0 := by
  intro hz
  have hc : 1+2*B*q=0 := by simpa [hz] using hN
  have hp : 0<(2*A-1)*(2*B-1) := mul_pos_of_neg_of_neg (by linarith) (by linarith)
  have hid := simultaneous_coefficient_obstruction01 A B q
  rw [hz,hc] at hid
  nlinarith [hid]

theorem null23_coefficient_nonzero (A B p q : ℝ) (hA : A<1/2) (hB : B<1/2)
    (hN : (q+2*A)*p+(2*B*q+2*(A+B-1/2))=0) : q+2*A ≠ 0 := by
  intro hz
  have hc : 2*B*q+2*(A+B-1/2)=0 := by simpa [hz] using hN
  have hp : 0<(2*A-1)*(2*B-1) := mul_pos_of_neg_of_neg (by linarith) (by linarith)
  have hid := simultaneous_coefficient_obstruction23 A B q
  rw [hz,hc] at hid
  nlinarith [hid]

/-- Square completion for any symmetric real bilinear form (Appendix F).
The relation with second derivatives of inverse matrices is not assumed here. -/
theorem bilinear_square_completion {E : Type*} [AddCommGroup E] [Module ℝ E]
    (B : E →ₗ[ℝ] E →ₗ[ℝ] ℝ) (hB : ∀ x y, B x y=B y x) (z h : E) :
    B (z+h) (z+h) - 2*B (z+h) h + B h h = B z z := by
  simp only [map_add, LinearMap.add_apply]
  rw [hB h z]
  ring

end Bell.Lorentz
