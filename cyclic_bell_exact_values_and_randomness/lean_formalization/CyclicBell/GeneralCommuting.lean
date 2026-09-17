import CyclicBell.GeneralFunctionalCalculus
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap

/-! Arbitrary-Hilbert-space commuting-operator bounds through continuous
half-polar factors. No finite-dimensional or tensor-factor assumption appears
in the final Hilbert theorem. This is an alternate proof of thm:exact rather
than an assertion that a matrix theorem automatically applies to infinite H.
The canonical polar-decomposition identity remains a separate manuscript lemma.
-/
noncomputable section
open scoped BigOperators ComplexOrder InnerProductSpace
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {A : Type*} [CStarAlgebra A]

def algebraHerm (a : A) : A := (1/2 : ℂ) • (a+star a)

theorem starUnitary_star {u : A} (hu : StarUnitary u) : StarUnitary (star u) := by
  simpa [StarUnitary] using And.intro hu.2 hu.1

theorem starUnitary_mul {u v : A} (hu : StarUnitary u) (hv : StarUnitary v) : StarUnitary (u*v) := by
  constructor
  · simp only [star_mul]
    calc star v*star u*(u*v)=star v*(star u*u)*v := by noncomm_ring
         _=1 := by rw [hu.1,mul_one,hv.1]
  · simp only [star_mul]
    calc (u*v)*(star v*star u)=u*(v*star v)*star u := by noncomm_ring
         _=1 := by rw [hv.2,mul_one,hu.2]

theorem star_commute_of_unitary {u v : A} (hu : StarUnitary u) (h : u*v=v*u) : star u*v=v*star u := by
  calc
    star u*v = star u*v*(u*star u) := by rw [hu.2,mul_one]
    _ = star u*(v*u)*star u := by noncomm_ring
    _ = star u*(u*v)*star u := by rw [h]
    _ = v*star u := by rw [← mul_assoc, hu.1, one_mul]

def algebraModulusCM (u : A) (y : Ix d) : C(spectrum ℂ u,ℂ) :=
  ⟨fun z => (‖1+chi y*(z : ℂ)‖ : ℂ),by fun_prop⟩
def algebraRootCM (u : A) (y : Ix d) : C(spectrum ℂ u,ℂ) :=
  ⟨fun z => squareRootNorm (1+chi y*(z : ℂ)),squareRootNorm_continuous.comp (by fun_prop)⟩
def algebraPolarRootCM (u : A) (y : Ix d) : C(spectrum ℂ u,ℂ) :=
  ⟨fun z => continuousPolarRoot (1+chi y*(z : ℂ)),continuousPolarRoot_continuous.comp (by fun_prop)⟩
def algebraGapCM (u : A) : C(spectrum ℂ u,ℂ) :=
  ⟨fun z => (Real.sqrt (scalarMaximum d-scalarSum (d := d) z) : ℂ),by unfold scalarSum; fun_prop⟩

theorem algebra_functional_factors (hd : 2≤d) (u : A) (b : Ix d → A)
    (hu : StarUnitary u) (hb : ∀ y,StarUnitary (b y)) (hc : ∀ y,u*b y=b y*u) :
    ∃ H K D : Ix d → A, ∃ G : A,
      (∀ y,star (H y)*H y=D y) ∧ (∀ y,star (K y)*K y=D y) ∧
      (∀ y,star (H y)*K y=1+chi y • u) ∧ (∀ y,D y*b y=b y*D y) ∧
      star G*G=(scalarMaximum d : ℂ) • 1-∑ y,D y := by
  let φ := cfcHom (R := ℂ) (starUnitary_normal hu)
  refine ⟨(fun y => φ (algebraRootCM u y)),(fun y => φ (algebraPolarRootCM u y)),
    (fun y => φ (algebraModulusCM u y)),φ (algebraGapCM (d := d) u),?_,?_,?_,?_,?_⟩
  · intro y
    have he : star (algebraRootCM u y)*algebraRootCM u y=algebraModulusCM u y := by
      ext z; exact squareRootNorm_square _
    simpa only [map_star,map_mul] using congrArg φ he
  · intro y
    have he : star (algebraPolarRootCM u y)*algebraPolarRootCM u y=algebraModulusCM u y := by
      ext z; exact continuousPolarRoot_square _
    simpa only [map_star,map_mul] using congrArg φ he
  · intro y
    have he : star (algebraRootCM u y)*algebraPolarRootCM u y=
        1+chi y • ((ContinuousMap.id ℂ).restrict (spectrum ℂ u)) := by
      ext z; exact continuousPolarRoot_cross _
    simpa only [map_star,map_mul,map_add,map_smul,map_one,φ,cfcHom_id] using congrArg φ he
  · intro y
    exact cfcHom_commute_unitary hu (hb y) (hc y) _
  · have he : star (algebraGapCM (d := d) u)*algebraGapCM (d := d) u=
        (scalarMaximum d : ℂ) • 1-∑ y : Ix d,algebraModulusCM u y := by
      ext z
      have hp := sub_nonneg.mpr (scalar_bound hd z (spectrum_unit_norm hu z))
      change star ((Real.sqrt (scalarMaximum d - scalarSum (d := d) z) : ℝ) : ℂ) *
        ((Real.sqrt (scalarMaximum d - scalarSum (d := d) z) : ℝ) : ℂ) = _
      rw [star_real, ← Complex.ofReal_mul, Real.mul_self_sqrt hp]
      simp [scalarSum,algebraModulusCM,Complex.ofReal_sub,Complex.ofReal_sum]
    simpa only [map_star,map_mul,map_sub,map_sum,map_smul,map_one] using congrArg φ he

def operatorFirst (a₀ a₁ : A) (b : Ix d → A) : A := ∑ y,algebraHerm ((a₀+chi y • a₁)*b y)

theorem algebra_halfPolar_gap (a h k D b L : A)
    (hh : star h*h=D) (hk : star k*k=D) (hc : star h*k=L)
    (hb : StarUnitary b) (hDb : D*b=b*D) :
    star (h*star a-k*b)*(h*star a-k*b)=
      a*D*star a+D-((a*L*b)+star (a*L*b)) := by
  have hkc : star k*h=star L := by simpa using congrArg star hc
  have hbd : star b*D*b=D := by rw [mul_assoc,hDb,← mul_assoc,hb.1,one_mul]
  calc
    _=a*(star h*h)*star a-a*(star h*k)*b-star b*(star k*h)*star a+star b*(star k*k)*b := by
      simp only [star_sub,star_mul,star_star]
      noncomm_ring
    _=_ := by rw [hh,hk,hc,hkc,hbd]; simp only [star_mul]; noncomm_ring

/-- The global first-family operator SOS in an arbitrary complex C*-algebra. -/
theorem first_cstar_sos (hd : 2≤d) (a₀ a₁ : A) (b : Ix d → A)
    (h₀ : StarUnitary a₀) (h₁ : StarUnitary a₁) (hb : ∀ y,StarUnitary (b y))
    (hc₀ : ∀ y,a₀*b y=b y*a₀) (hc₁ : ∀ y,a₁*b y=b y*a₁) :
    ∃ (P : Ix d → A) (G : A),
      (scalarMaximum d : ℂ) • 1-operatorFirst a₀ a₁ b=
        (1/2 : ℂ) • (∑ y,star (P y)*P y)+(1/2 : ℂ) • (star G*G)+
        (1/2 : ℂ) • (star (G*star a₀)*(G*star a₀)) := by
  let u := star a₀*a₁
  have hu : StarUnitary u := starUnitary_mul (starUnitary_star h₀) h₁
  have hc (y : Ix d) : u*b y=b y*u := by
    rw [mul_assoc,hc₁,← mul_assoc,star_commute_of_unitary h₀ (hc₀ y),mul_assoc]
  obtain ⟨H,K,D,G,hh,hk,hcross,hDb,hG⟩ := algebra_functional_factors hd u b hu hb hc
  let P := fun y => H y*star a₀-K y*b y
  refine ⟨P,G,?_⟩
  have hrow (y : Ix d) : star (P y)*P y=
      a₀*D y*star a₀+D y-((a₀+chi y • a₁)*b y+star ((a₀+chi y • a₁)*b y)) := by
    have h := algebra_halfPolar_gap a₀ (H y) (K y) (D y) (b y) _
      (hh y) (hk y) (hcross y) (hb y) (hDb y)
    have he : a₀*(1+chi y • u)=a₀+chi y • a₁ := by
      simp only [mul_add,mul_one,mul_smul_comm,u,← mul_assoc,h₀.2,one_mul]
    simpa only [he] using h
  have hgA : star (G*star a₀)*(G*star a₀)=a₀*(star G*G)*star a₀ := by
    simp [star_mul,mul_assoc]
  rw [hgA,hG]
  simp_rw [hrow]
  unfold operatorFirst algebraHerm
  simp only [Finset.sum_sub_distrib,Finset.sum_add_distrib,← Finset.sum_mul,← Finset.mul_sum,
    mul_sub,sub_mul,mul_smul_comm,smul_mul_assoc,one_mul,mul_one,h₀.2,
    Finset.smul_sum,smul_sub,smul_add]
  module

theorem algebra_aligned_gap (a : A) (ha : StarUnitary a) :
    1-algebraHerm a=(1/2 : ℂ) • (star (1-a)*(1-a)) := by
  unfold algebraHerm
  simp only [star_sub,star_one]
  have h : (1-star a)*(1-a)=2 • (1 : A)-(a+star a) := by
    simp only [sub_mul,mul_sub,one_mul,mul_one,ha.1]
    module
  rw [h,smul_sub]
  module

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def vectorEval (ψ : H) (a : H →L[ℂ] H) : ℝ := (⟪ψ, a ψ⟫_ℂ).re

theorem vectorEval_add (ψ : H) (a b : H →L[ℂ] H) : vectorEval ψ (a+b)=vectorEval ψ a+vectorEval ψ b := by
  simp [vectorEval,inner_add_right]
theorem vectorEval_sub (ψ : H) (a b : H →L[ℂ] H) : vectorEval ψ (a-b)=vectorEval ψ a-vectorEval ψ b := by
  simp [vectorEval,inner_sub_right]
theorem vectorEval_real_smul (ψ : H) (r : ℝ) (a : H →L[ℂ] H) :
    vectorEval ψ ((r : ℂ) • a)=r*vectorEval ψ a := by simp [vectorEval,inner_smul_right]
theorem vectorEval_sum {J : Type*} [Fintype J] (ψ : H) (a : J → H →L[ℂ] H) :
    vectorEval ψ (∑ j,a j)=∑ j,vectorEval ψ (a j) := by simp [vectorEval,inner_sum]
theorem vectorEval_one (ψ : H) (hψ : ‖ψ‖=1) : vectorEval ψ 1=1 := by
  simp [vectorEval,inner_self_eq_norm_sq_to_K,hψ]
theorem vectorEval_square (ψ : H) (a : H →L[ℂ] H) : vectorEval ψ (star a*a)=‖a ψ‖^2 := by
  change (⟪ψ, a.adjoint (a ψ)⟫_ℂ).re=‖a ψ‖^2
  rw [a.adjoint_inner_right]
  simp only [inner_self_eq_norm_sq_to_K]
  change (((‖a ψ‖ : ℝ) : ℂ) ^ 2).re = ‖a ψ‖ ^ 2
  rw [← Complex.ofReal_pow, Complex.ofReal_re]

/-- Actual arbitrary complete complex Hilbert space, with no finite-dimension
instance and no tensor-product decomposition in its assumptions. -/
theorem first_commuting_hilbert_bound (hd : 2≤d) (ψ : H) (hψ : ‖ψ‖=1)
    (a₀ a₁ : H →L[ℂ] H) (b : Ix d → H →L[ℂ] H)
    (h₀ : StarUnitary a₀) (h₁ : StarUnitary a₁) (hb : ∀ y,StarUnitary (b y))
    (hc₀ : ∀ y,a₀*b y=b y*a₀) (hc₁ : ∀ y,a₁*b y=b y*a₁) :
    vectorEval ψ (operatorFirst a₀ a₁ b)≤2/Real.sin (Real.pi/(2*d)) := by
  obtain ⟨P,G,hgap⟩ := first_cstar_sos hd a₀ a₁ b h₀ h₁ hb hc₀ hc₁
  have h := congrArg (vectorEval ψ) hgap
  have half : (1/2 : ℂ)=((1/2 : ℝ) : ℂ) := by norm_num
  simp only [vectorEval_sub,vectorEval_real_smul,vectorEval_one ψ hψ,
    vectorEval_add,half,vectorEval_sum,vectorEval_square] at h
  have hp : 0≤∑ y,‖P y ψ‖^2 := Finset.sum_nonneg (fun _ _ => sq_nonneg _)
  have hg := sq_nonneg ‖G ψ‖
  have hgA := sq_nonneg ‖(G*star a₀) ψ‖
  change vectorEval ψ (operatorFirst a₀ a₁ b)≤scalarMaximum d
  linarith

theorem aligned_commuting_hilbert_bound (ψ : H) (hψ : ‖ψ‖=1) (a : H →L[ℂ] H)
    (ha : StarUnitary a) : vectorEval ψ (algebraHerm a)≤1 := by
  have h := congrArg (vectorEval ψ) (algebra_aligned_gap a ha)
  have half : (1/2 : ℂ)=((1/2 : ℝ) : ℂ) := by norm_num
  simp only [vectorEval_sub,vectorEval_one ψ hψ,half,vectorEval_real_smul,vectorEval_square] at h
  nlinarith [sq_nonneg ‖(1-a) ψ‖]

theorem first_augmented_commuting_hilbert_bound (hd : 2≤d) (ψ : H) (hψ : ‖ψ‖=1)
    (a₀ a₁ bstar : H →L[ℂ] H) (b : Ix d → H →L[ℂ] H)
    (h₀ : StarUnitary a₀) (h₁ : StarUnitary a₁) (hstar : StarUnitary bstar)
    (hb : ∀ y,StarUnitary (b y))
    (hc₀ : ∀ y,a₀*b y=b y*a₀) (hc₁ : ∀ y,a₁*b y=b y*a₁) :
    vectorEval ψ (operatorFirst a₀ a₁ b+algebraHerm (a₀*bstar))≤
      2/Real.sin (Real.pi/(2*d))+1 := by
  rw [vectorEval_add]
  exact add_le_add (first_commuting_hilbert_bound hd ψ hψ a₀ a₁ b h₀ h₁ hb hc₀ hc₁)
    (aligned_commuting_hilbert_bound ψ hψ _ (starUnitary_mul h₀ hstar))

end CyclicBell.General
