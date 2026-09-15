import CyclicBell.GeneralScalar
import CyclicBell.MatrixAlgebra
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Basic
import Mathlib.Analysis.CStarAlgebra.CStarMatrix

/-! Kernel-safe continuous factors and their matrix functional calculus.

Instead of importing a discontinuous polar phase at zero, use
  h(z)=sqrt(norm z), k(z)=z/sqrt(norm z), with k(0)=0.
Both are continuous, star(h)*h=star(k)*k=norm z, and star(h)*k=z.
This supplies the exact polar-positive-factor algebra even at a kernel.
CFC commutation is proved by conjugation and uniqueness, not assumed.
UNCOMPILED SOURCE; pinned API usage and all proof terms need an offline build. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def squareRootNorm (z : ℂ) : ℂ := (Real.sqrt ‖z‖ : ℂ)
def continuousPolarRoot (z : ℂ) : ℂ := z / squareRootNorm z

@[simp] theorem squareRootNorm_zero : squareRootNorm 0=0 := by simp [squareRootNorm]
@[simp] theorem continuousPolarRoot_zero : continuousPolarRoot 0=0 := by simp [continuousPolarRoot]

theorem squareRootNorm_continuous : Continuous squareRootNorm := by
  unfold squareRootNorm
  fun_prop

theorem squareRootNorm_square (z : ℂ) : star (squareRootNorm z)*squareRootNorm z=(‖z‖ : ℂ) := by
  simp only [squareRootNorm,Complex.conj_ofReal,← Complex.ofReal_mul]
  congr 1
  exact Real.mul_self_sqrt (norm_nonneg z)

theorem squareRootNorm_ne_zero {z : ℂ} (hz : z≠0) : squareRootNorm z≠0 := by
  exact_mod_cast (ne_of_gt (Real.sqrt_pos.2 (norm_pos_iff.mpr hz)))

theorem continuousPolarRoot_norm (z : ℂ) : ‖continuousPolarRoot z‖=Real.sqrt ‖z‖ := by
  by_cases hz : z=0
  · simp [hz]
  · have hs : 0<Real.sqrt ‖z‖ := Real.sqrt_pos.2 (norm_pos_iff.mpr hz)
    rw [continuousPolarRoot,norm_div,squareRootNorm,Complex.norm_real,
      Real.norm_eq_abs,abs_of_pos hs]
    apply (div_eq_iff (ne_of_gt hs)).mpr
    exact (Real.mul_self_sqrt (norm_nonneg z)).symm

/-- Continuity at the kernel is established from the vanishing norm; there is
no inverse-at-zero assumption. -/
theorem continuousPolarRoot_continuous : Continuous continuousPolarRoot := by
  apply continuous_iff_continuousAt.mpr
  intro z
  by_cases hz : z=0
  · subst z
    have hn : Filter.Tendsto (fun w : ℂ => ‖continuousPolarRoot w‖) (𝓝 0) (𝓝 0) := by
      simp_rw [continuousPolarRoot_norm]
      simpa using (Real.continuous_sqrt.comp continuous_norm).continuousAt.tendsto (x := (0 : ℂ))
    change Filter.Tendsto continuousPolarRoot (𝓝 0) (𝓝 (continuousPolarRoot 0))
    rw [continuousPolarRoot_zero]
    exact (tendsto_zero_iff_norm_tendsto_zero).mpr hn
  · exact continuous_id.continuousAt.div squareRootNorm_continuous.continuousAt
      (squareRootNorm_ne_zero hz)

theorem continuousPolarRoot_cross (z : ℂ) :
    star (squareRootNorm z)*continuousPolarRoot z=z := by
  by_cases hz : z=0
  · simp [hz]
  · have hn := squareRootNorm_ne_zero hz
    have hs : star (squareRootNorm z)=squareRootNorm z := by simp [squareRootNorm]
    rw [hs,continuousPolarRoot]
    field_simp

theorem continuousPolarRoot_square (z : ℂ) :
    star (continuousPolarRoot z)*continuousPolarRoot z=(‖z‖ : ℂ) := by
  rw [← Complex.normSq_eq_conj_mul_self,Complex.normSq_eq_norm_sq,
    continuousPolarRoot_norm,Real.sq_sqrt (norm_nonneg z)]

/-- Unitarity as equations, usable in any star algebra. -/
def StarUnitary {A : Type*} [Monoid A] [Star A] (u : A) : Prop :=
  star u*u=1 ∧ u*star u=1

theorem starUnitary_normal {A : Type*} [Monoid A] [Star A] {u : A}
    (hu : StarUnitary u) : IsStarNormal u := by
  constructor
  change star u*u=u*star u
  rw [hu.1,hu.2]

/-- A genuine star-algebra homomorphism, with its law proofs supplied. -/
def conjugationHom {A : Type*} [Ring A] [StarRing A] [Algebra ℂ A] [StarModule ℂ A]
    (u : A) (hu : StarUnitary u) : A →⋆ₐ[ℂ] A where
  toFun x := u*x*star u
  map_zero' := by simp
  map_one' := by simpa using hu.2
  map_add' x y := by noncomm_ring
  map_mul' x y := by
    have hc (v : A) : star u*(u*v)=v := by rw [← mul_assoc,hu.1,one_mul]
    simp only [mul_assoc,hc]
  commutes' z := by
    simp [Algebra.algebraMap_eq_smul_one,smul_mul_assoc,mul_smul_comm,hu.2]
  map_star' x := by simp [star_mul,mul_assoc]

theorem conjugationHom_continuous {A : Type*} [CStarAlgebra A]
    (u : A) (hu : StarUnitary u) : Continuous (conjugationHom u hu) := by
  change Continuous (fun x : A => u*x*star u)
  fun_prop

/-- Uniqueness of CFC proves commutation with every continuous function of U.
Only u/B commutation is needed; different Bob operators need not commute. -/
theorem cfcHom_commute_unitary {A : Type*} [CStarAlgebra A]
    {u b : A} (hu : StarUnitary u) (hb : StarUnitary b) (hub : u*b=b*u)
    (f : C(spectrum ℂ u,ℂ)) :
    (cfcHom (R := ℂ) (starUnitary_normal hu) f)*b=
      b*(cfcHom (R := ℂ) (starUnitary_normal hu) f) := by
  let φ := cfcHom (R := ℂ) (starUnitary_normal hu)
  let ψ := (conjugationHom b hb).comp φ
  have hψ : Continuous ψ := conjugationHom_continuous b hb |>.comp
    (cfcHom_continuous (R := ℂ) (starUnitary_normal hu))
  have hid : ψ ((ContinuousMap.id ℂ).restrict (spectrum ℂ u))=u := by
    change b*(φ ((ContinuousMap.id ℂ).restrict (spectrum ℂ u)))*star b=u
    rw [cfcHom_id,← hub,mul_assoc,hb.2,mul_one]
  have he : φ=ψ := cfcHom_eq_of_continuous_of_map_id (starUnitary_normal hu) ψ hψ hid
  have hf := congrArg (fun p : C(spectrum ℂ u,ℂ) →⋆ₐ[ℂ] A => p f) he
  change φ f=b*(φ f)*star b at hf
  have hh := congrArg (fun x : A => x*b) hf
  simpa [mul_assoc,hb.1] using hh

/-- Spectral unit modulus follows directly from the injective CFC map and
star(u)*u=1; no undeclared spectral theorem is imported by name. -/
theorem spectrum_unit_norm {A : Type*} [CStarAlgebra A] {u : A}
    (hu : StarUnitary u) (z : spectrum ℂ u) : ‖(z : ℂ)‖=1 := by
  let φ := cfcHom (R := ℂ) (starUnitary_normal hu)
  let c : C(spectrum ℂ u,ℂ) := (ContinuousMap.id ℂ).restrict (spectrum ℂ u)
  have hi : Function.Injective φ := (cfcHom_isClosedEmbedding (starUnitary_normal hu)).injective
  have he : star c*c=1 := by
    apply hi
    simp only [map_mul,map_star,map_one]
    change star (φ c)*φ c=1
    rw [cfcHom_id]
    exact hu.1
  have hz := congrArg (fun f : C(spectrum ℂ u,ℂ) => f z) he
  change star (z : ℂ)*(z : ℂ)=1 at hz
  rw [← Complex.normSq_eq_conj_mul_self] at hz
  have hr := congrArg Complex.re hz
  simp only [Complex.ofReal_re,Complex.one_re,Complex.normSq_eq_norm_sq] at hr
  nlinarith [norm_nonneg (z : ℂ)]

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

abbrev CMat (ι : Type*) := CStarMatrix ι ι ℂ

def toCMatrix (U : Mat ι) : CMat ι := CStarMatrix.ofMatrix U

theorem toCMatrix_unitary {U : Mat ι} (hU : UnitaryRel U) : StarUnitary (toCMatrix U) := hU

def matrixCfc (U : Mat ι) (hU : UnitaryRel U) :
    C(spectrum ℂ (toCMatrix U),ℂ) →⋆ₐ[ℂ] Mat ι :=
  (CStarMatrix.ofMatrixStarAlgEquiv : Mat ι ≃⋆ₐ[ℂ] CMat ι).symm.toStarAlgHom.comp
    (cfcHom (R := ℂ) (starUnitary_normal (toCMatrix_unitary hU)))

theorem matrixCfc_coordinate (U : Mat ι) (hU : UnitaryRel U) :
    matrixCfc U hU ((ContinuousMap.id ℂ).restrict (spectrum ℂ (toCMatrix U)))=U := by
  simp [matrixCfc,cfcHom_id,toCMatrix]

theorem matrixCfc_commute (U B : Mat ι) (hU : UnitaryRel U) (hB : UnitaryRel B)
    (hUB : U*B=B*U) (f : C(spectrum ℂ (toCMatrix U),ℂ)) :
    matrixCfc U hU f*B=B*matrixCfc U hU f := by
  have h := cfcHom_commute_unitary (toCMatrix_unitary hU) (toCMatrix_unitary hB)
    (show toCMatrix U*toCMatrix B=toCMatrix B*toCMatrix U from hUB) f
  exact congrArg CStarMatrix.ofMatrix.symm h

def modulusCM (U : Mat ι) (y : Ix d) : C(spectrum ℂ (toCMatrix U),ℂ) :=
  ⟨fun z => (‖1+chi y*(z : ℂ)‖ : ℂ),by fun_prop⟩
def rootCM (U : Mat ι) (y : Ix d) : C(spectrum ℂ (toCMatrix U),ℂ) :=
  ⟨fun z => squareRootNorm (1+chi y*(z : ℂ)),by
    exact squareRootNorm_continuous.comp (by fun_prop)⟩
def polarRootCM (U : Mat ι) (y : Ix d) : C(spectrum ℂ (toCMatrix U),ℂ) :=
  ⟨fun z => continuousPolarRoot (1+chi y*(z : ℂ)),by
    exact continuousPolarRoot_continuous.comp (by fun_prop)⟩
def scalarGapCM (d : ℕ) [NeZero d] (U : Mat ι) : C(spectrum ℂ (toCMatrix U),ℂ) :=
  ⟨fun z => (Real.sqrt (scalarMaximum d-scalarSum (d := d) (z : ℂ)) : ℂ),by
    unfold scalarSum
    fun_prop⟩

theorem rootCM_square (U : Mat ι) (y : Ix d) : star (rootCM U y)*rootCM U y=modulusCM U y := by
  ext z
  exact squareRootNorm_square _

theorem polarRootCM_square (U : Mat ι) (y : Ix d) :
    star (polarRootCM U y)*polarRootCM U y=modulusCM U y := by
  ext z
  exact continuousPolarRoot_square _

theorem rootCM_cross (U : Mat ι) (y : Ix d) :
    star (rootCM U y)*polarRootCM U y =
      1+chi y • ((ContinuousMap.id ℂ).restrict (spectrum ℂ (toCMatrix U))) := by
  ext z
  exact continuousPolarRoot_cross _

theorem scalarGapCM_square (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U) :
    star (scalarGapCM d U)*scalarGapCM d U =
      (scalarMaximum d : ℂ) • 1 - ∑ y : Ix d,modulusCM U y := by
  ext z
  have hp : 0≤scalarMaximum d-scalarSum (d := d) (z : ℂ) :=
    sub_nonneg.mpr (scalar_bound hd _ (spectrum_unit_norm (toCMatrix_unitary hU) z))
  change star ((Real.sqrt (scalarMaximum d-scalarSum (d := d) (z : ℂ)) : ℝ) : ℂ) *
      ((Real.sqrt (scalarMaximum d-scalarSum (d := d) (z : ℂ)) : ℝ) : ℂ) = _
  simp only [Complex.conj_ofReal,← Complex.ofReal_mul,Real.mul_self_sqrt hp]
  simp [scalarSum,modulusCM,Complex.ofReal_sub,Complex.ofReal_sum]

/-- ALL functional-factor hypotheses are derived from physical unitarity and
commutation. The existential is a constructed certificate, not a validity field. -/
theorem matrix_functional_factors (hd : 2≤d) (U : Mat ι) (B : Ix d → Mat ι)
    (hU : UnitaryRel U) (hB : ∀ y,UnitaryRel (B y)) (hUB : ∀ y,U*B y=B y*U) :
    ∃ (H K D : Ix d → Mat ι) (G : Mat ι),
      (∀ y,(H y).conjTranspose*H y=D y) ∧
      (∀ y,(K y).conjTranspose*K y=D y) ∧
      (∀ y,(H y).conjTranspose*K y=1+chi y • U) ∧
      (∀ y,D y*B y=B y*D y) ∧
      G.conjTranspose*G=(scalarMaximum d : ℂ) • 1-∑ y,D y := by
  let φ := matrixCfc U hU
  refine ⟨(fun y => φ (rootCM U y)),(fun y => φ (polarRootCM U y)),
    (fun y => φ (modulusCM U y)),φ (scalarGapCM d U),?_,?_,?_,?_,?_⟩
  · intro y
    have h := congrArg φ (rootCM_square U y)
    simpa only [map_mul,map_star,Matrix.star_eq_conjTranspose] using h
  · intro y
    have h := congrArg φ (polarRootCM_square U y)
    simpa only [map_mul,map_star,Matrix.star_eq_conjTranspose] using h
  · intro y
    have h := congrArg φ (rootCM_cross U y)
    simpa only [map_mul,map_star,map_add,map_one,map_smul,matrixCfc_coordinate,
      Matrix.star_eq_conjTranspose] using h
  · intro y
    exact matrixCfc_commute U (B y) hU (hB y) (hUB y) _
  · have h := congrArg φ (scalarGapCM_square hd U hU)
    simpa only [map_mul,map_star,map_sub,map_smul,map_one,map_sum,
      Matrix.star_eq_conjTranspose] using h

end CyclicBell.General
