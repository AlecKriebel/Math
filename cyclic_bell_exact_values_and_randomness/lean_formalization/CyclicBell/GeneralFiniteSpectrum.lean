import CyclicBell.GeneralFunctionalCalculus
import Mathlib.LinearAlgebra.Eigenspace.Minpoly

/-! Finite-spectrum functional calculus and zero transfer. Arbitrary scalar
functions are continuous on a finite spectrum, but this module is explicitly
finite-dimensional. In particular, the division used in zero transfer is NOT
an assertion that a singular matrix is invertible. UNCOMPILED SOURCE. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General
variable {ι ν : Type*} [Fintype ι] [Fintype ν] [DecidableEq ι]

abbrev MatrixSpectrum (U : Mat ι) := spectrum ℂ (toCMatrix U)

theorem matrixSpectrum_finite (U : Mat ι) : Set.Finite (MatrixSpectrum U) := by
  change Set.Finite (spectrum ℂ U)
  exact Matrix.finite_spectrum U

instance finiteMatrixSpectrum (U : Mat ι) : Finite (MatrixSpectrum U) :=
  Set.finite_coe_iff.mpr (matrixSpectrum_finite U)

instance discreteMatrixSpectrum (U : Mat ι) : DiscreteTopology (MatrixSpectrum U) :=
  inferInstance

def finiteCM (U : Mat ι) (f : ℂ → ℂ) : C(MatrixSpectrum U,ℂ) :=
  ⟨fun z => f z,continuous_of_discreteTopology⟩

def finiteCalc (U : Mat ι) (hU : UnitaryRel U) (f : ℂ → ℂ) : Mat ι :=
  matrixCfc U hU (finiteCM U f)

theorem finiteCalc_congr (U : Mat ι) (hU : UnitaryRel U) {f g : ℂ → ℂ}
    (h : ∀ z : MatrixSpectrum U,f z=g z) : finiteCalc U hU f=finiteCalc U hU g := by
  apply congrArg (matrixCfc U hU)
  ext z
  exact h z

@[simp] theorem finiteCalc_zero (U : Mat ι) (hU : UnitaryRel U) : finiteCalc U hU (fun _ => 0)=0 := by
  change matrixCfc U hU 0=0
  exact map_zero _
@[simp] theorem finiteCalc_one (U : Mat ι) (hU : UnitaryRel U) : finiteCalc U hU (fun _ => 1)=1 := by
  change matrixCfc U hU 1=1
  exact map_one _
@[simp] theorem finiteCalc_const (U : Mat ι) (hU : UnitaryRel U) (c : ℂ) :
    finiteCalc U hU (fun _ => c)=c • 1 := by
  change matrixCfc U hU (c • 1)=c • 1
  rw [map_smul,map_one]
@[simp] theorem finiteCalc_coordinate (U : Mat ι) (hU : UnitaryRel U) : finiteCalc U hU id=U :=
  matrixCfc_coordinate U hU
@[simp] theorem finiteCalc_add (U : Mat ι) (hU : UnitaryRel U) (f g : ℂ → ℂ) :
    finiteCalc U hU (fun z => f z+g z)=finiteCalc U hU f+finiteCalc U hU g := by
  exact map_add (matrixCfc U hU) (finiteCM U f) (finiteCM U g)
@[simp] theorem finiteCalc_sub (U : Mat ι) (hU : UnitaryRel U) (f g : ℂ → ℂ) :
    finiteCalc U hU (fun z => f z-g z)=finiteCalc U hU f-finiteCalc U hU g := by
  exact map_sub (matrixCfc U hU) (finiteCM U f) (finiteCM U g)
@[simp] theorem finiteCalc_mul (U : Mat ι) (hU : UnitaryRel U) (f g : ℂ → ℂ) :
    finiteCalc U hU (fun z => f z*g z)=finiteCalc U hU f*finiteCalc U hU g := by
  exact map_mul (matrixCfc U hU) (finiteCM U f) (finiteCM U g)
@[simp] theorem finiteCalc_smul (U : Mat ι) (hU : UnitaryRel U) (c : ℂ) (f : ℂ → ℂ) :
    finiteCalc U hU (fun z => c*f z)=c • finiteCalc U hU f := by
  exact map_smul (matrixCfc U hU) c (finiteCM U f)
@[simp] theorem finiteCalc_star (U : Mat ι) (hU : UnitaryRel U) (f : ℂ → ℂ) :
    finiteCalc U hU (fun z => star (f z))=(finiteCalc U hU f).conjTranspose := by
  exact map_star (matrixCfc U hU) (finiteCM U f)
@[simp] theorem finiteCalc_pow (U : Mat ι) (hU : UnitaryRel U) (f : ℂ → ℂ) (n : ℕ) :
    finiteCalc U hU (fun z => f z^n)=finiteCalc U hU f^n := by
  exact map_pow (matrixCfc U hU) (finiteCM U f) n
@[simp] theorem finiteCalc_sum {J : Type*} [Fintype J] (U : Mat ι) (hU : UnitaryRel U)
    (f : J → ℂ → ℂ) : finiteCalc U hU (fun z => ∑ j,f j z)=∑ j,finiteCalc U hU (f j) := by
  exact map_sum (matrixCfc U hU) (fun j => finiteCM U (f j)) Finset.univ

theorem finiteCalc_commute (U : Mat ι) (hU : UnitaryRel U) (f g : ℂ → ℂ) :
    finiteCalc U hU f*finiteCalc U hU g=finiteCalc U hU g*finiteCalc U hU f := by
  rw [← finiteCalc_mul,← finiteCalc_mul]
  exact finiteCalc_congr U hU (fun z => mul_comm _ _)

/-- Transfer a vanishing equation using its exact spectral zero set. This is
valid for rectangular amplitude matrices and does not assume faithful states. -/
theorem finiteCalc_zero_transfer (U : Mat ι) (hU : UnitaryRel U)
    (f g : ℂ → ℂ) (T : Matrix ι ν ℂ)
    (hzero : ∀ z : MatrixSpectrum U,f z=0 → g z=0)
    (hf : finiteCalc U hU f*T=0) : finiteCalc U hU g*T=0 := by
  let r : ℂ → ℂ := fun z => g z/f z
  have he : finiteCalc U hU g=finiteCalc U hU r*finiteCalc U hU f := by
    rw [← finiteCalc_mul]
    apply finiteCalc_congr U hU
    intro z
    by_cases hz : f z=0
    · simp [r,hz,hzero z hz]
    · simp [r,div_mul_cancel₀ _ hz]
  rw [he,mul_assoc,hf,mul_zero]

theorem finiteCalc_supported_congr (U : Mat ι) (hU : UnitaryRel U)
    (f g k : ℂ → ℂ) (T : Matrix ι ν ℂ)
    (hzero : ∀ z : MatrixSpectrum U,f z=0 → g z=k z)
    (hf : finiteCalc U hU f*T=0) : finiteCalc U hU g*T=finiteCalc U hU k*T := by
  have h := finiteCalc_zero_transfer U hU f (fun z => g z-k z) T
    (fun z hz => sub_eq_zero.mpr (hzero z hz)) hf
  rw [finiteCalc_sub,sub_mul,sub_eq_zero] at h
  exact h

def finiteSpectralProjection (U : Mat ι) (hU : UnitaryRel U) (z : ℂ) : Mat ι :=
  finiteCalc U hU (fun w => if w=z then 1 else 0)

theorem finiteSpectralProjection_star (U : Mat ι) (hU : UnitaryRel U) (z : ℂ) :
    (finiteSpectralProjection U hU z).conjTranspose=finiteSpectralProjection U hU z := by
  rw [finiteSpectralProjection,← finiteCalc_star]
  apply finiteCalc_congr U hU
  intro w
  split_ifs <;> simp

theorem finiteSpectralProjection_mul (U : Mat ι) (hU : UnitaryRel U) (z w : ℂ) :
    finiteSpectralProjection U hU z*finiteSpectralProjection U hU w=
      if z=w then finiteSpectralProjection U hU z else 0 := by
  unfold finiteSpectralProjection
  rw [← finiteCalc_mul]
  split_ifs with hzw
  · subst w
    apply finiteCalc_congr U hU
    intro v
    split_ifs <;> simp
  · rw [← finiteCalc_zero U hU]
    apply finiteCalc_congr U hU
    intro v
    by_cases hvz : (v : ℂ)=z <;> by_cases hvw : (v : ℂ)=w <;> simp_all

theorem finiteSpectralProjection_eigen (U : Mat ι) (hU : UnitaryRel U) (z : ℂ) :
    U*finiteSpectralProjection U hU z=z • finiteSpectralProjection U hU z := by
  rw [← finiteCalc_coordinate U hU,finiteSpectralProjection,← finiteCalc_mul,← finiteCalc_smul]
  apply finiteCalc_congr U hU
  intro w
  by_cases hw : (w : ℂ)=z <;> simp [hw]

end CyclicBell.General
