import Mathlib.Analysis.InnerProductSpace.Completion
import Mathlib.LinearAlgebra.Finsupp.LinearCombination
import Mathlib.Data.Finsupp.SMul
import Mathlib.Tactic

/-! Realization of a positive complex kernel by actual vectors in a complete
Hilbert space. The seminorm may be degenerate; completion performs separation.
Positivity is a condition on finite scalar sums, never an assumed realization. -/
noncomputable section
open scoped BigOperators InnerProductSpace
namespace CyclicBell.General.Coverage
variable {ι : Type}

def kernelInner (K : ι → ι → ℂ) (c e : ι →₀ ℂ) : ℂ :=
  c.sum (fun i ci => e.sum (fun j ej => star ci * K i j * ej))

theorem kernelInner_add_left (K : ι → ι → ℂ) (c e f : ι →₀ ℂ) :
    kernelInner K (c+e) f=kernelInner K c f+kernelInner K e f := by
  unfold kernelInner
  apply Finsupp.sum_add_index'
  · intro i; simp
  · intro i a b
    simp only [star_add,add_mul,Finsupp.sum,Finset.sum_add_distrib]

theorem kernelInner_smul_left (K : ι → ι → ℂ) (c e : ι →₀ ℂ) (z : ℂ) :
    kernelInner K (z • c) e=star z*kernelInner K c e := by
  unfold kernelInner
  rw [Finsupp.sum_smul_index (by intro i; simp)]
  simp only [Finsupp.sum,star_mul,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem kernelInner_hermitian (K : ι → ι → ℂ)
    (hK : ∀ i j,star (K j i)=K i j) (c e : ι →₀ ℂ) :
    star (kernelInner K e c)=kernelInner K c e := by
  unfold kernelInner
  simp only [Finsupp.sum,star_sum,star_mul,star_star]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  rw [hK]
  ring

theorem kernelInner_single (K : ι → ι → ℂ) (i j : ι) :
    kernelInner K (Finsupp.single i 1) (Finsupp.single j 1)=K i j := by
  simp [kernelInner]

structure PositiveKernel (ι : Type) where
  entry : ι → ι → ℂ
  hermitian : ∀ i j,star (entry j i)=entry i j
  positive : ∀ c : ι →₀ ℂ,0≤(kernelInner entry c c).re

/-- An algebraic copy of finitely supported coefficients, with no preexisting
norm instance. Its norm below is defined solely from the supplied kernel. -/
def KernelSpan (k : PositiveKernel ι) := ι →₀ ℂ

instance kernelSpanAddCommGroup (k : PositiveKernel ι) : AddCommGroup (KernelSpan k) :=
  inferInstanceAs (AddCommGroup (ι →₀ ℂ))

instance kernelSpanModule (k : PositiveKernel ι) : Module ℂ (KernelSpan k) :=
  inferInstanceAs (Module ℂ (ι →₀ ℂ))

instance kernelSpanCore (k : PositiveKernel ι) : PreInnerProductSpace.Core ℂ (KernelSpan k) where
  inner := kernelInner k.entry
  conj_inner_symm := kernelInner_hermitian k.entry k.hermitian
  re_inner_nonneg := k.positive
  add_left := kernelInner_add_left k.entry
  smul_left := kernelInner_smul_left k.entry

instance kernelSpanSeminorm (k : PositiveKernel ι) : SeminormedAddCommGroup (KernelSpan k) :=
  InnerProductSpace.Core.toSeminormedAddCommGroup (𝕜 := ℂ)

instance kernelSpanNormedSpace (k : PositiveKernel ι) : NormedSpace ℂ (KernelSpan k) :=
  InnerProductSpace.Core.toSeminormedSpace (𝕜 := ℂ)

instance kernelSpanInnerProduct (k : PositiveKernel ι) : InnerProductSpace ℂ (KernelSpan k) :=
  { kernelSpanCore k with
    norm_sq_eq_re_inner := by
      intro c
      change (Real.sqrt (kernelInner k.entry c c).re)^2=(kernelInner k.entry c c).re
      exact Real.sq_sqrt (k.positive c) }

theorem kernelSpan_norm_sq (k : PositiveKernel ι) (c : KernelSpan k) :
    ‖c‖^2=(kernelInner k.entry c c).re :=
  norm_sq_eq_re_inner (𝕜 := ℂ) c

theorem kernelSpan_contraction (k : PositiveKernel ι)
    (A : KernelSpan k →ₗ[ℂ] KernelSpan k)
    (hA : ∀ c,(kernelInner k.entry (A c) (A c)).re≤(kernelInner k.entry c c).re)
    (c : KernelSpan k) : ‖A c‖≤‖c‖ := by
  apply (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).mp
  simpa only [kernelSpan_norm_sq] using hA c

abbrev KernelHilbert (k : PositiveKernel ι) := UniformSpace.Completion (KernelSpan k)

def kernelEmbed (k : PositiveKernel ι) : KernelSpan k →L[ℂ] KernelHilbert k :=
  UniformSpace.Completion.toComplL

theorem kernelEmbed_dense (k : PositiveKernel ι) : DenseRange (kernelEmbed k) :=
  UniformSpace.Completion.denseRange_coe

theorem kernelEmbed_inner (k : PositiveKernel ι) (c e : KernelSpan k) :
    ⟪kernelEmbed k c,kernelEmbed k e⟫_ℂ = kernelInner k.entry c e :=
  UniformSpace.Completion.inner_coe c e

def kernelVector (k : PositiveKernel ι) (i : ι) : KernelHilbert k :=
  kernelEmbed k (Finsupp.single i 1)

theorem kernelVector_inner (k : PositiveKernel ι) (i j : ι) :
    ⟪kernelVector k i,kernelVector k j⟫_ℂ = k.entry i j := by
  rw [kernelVector,kernelVector,kernelEmbed_inner,kernelInner_single]

theorem kernelCombination_eq (k : PositiveKernel ι) :
    Finsupp.linearCombination ℂ (kernelVector k)=(kernelEmbed k).toLinearMap := by
  ext i
  change Finsupp.linearCombination ℂ (kernelVector k) (Finsupp.single i 1) =
    kernelEmbed k (Finsupp.single i 1)
  rw [Finsupp.linearCombination_single,one_smul]
  rfl

theorem kernelVector_dense_span (k : PositiveKernel ι) :
    Dense (Submodule.span ℂ (Set.range (kernelVector k)) : Set (KernelHilbert k)) := by
  rw [← Finsupp.range_linearCombination,kernelCombination_eq]
  exact kernelEmbed_dense k

/-- The carrier is genuinely complete and its indicated vectors span densely.
The only assumptions are the scalar definition of a positive Hermitian kernel. -/
theorem positiveKernel_realization (K : ι → ι → ℂ)
    (hHerm : ∀ i j,star (K j i)=K i j)
    (hPos : ∀ c : ι →₀ ℂ,0≤(kernelInner K c c).re) :
    ∃ (H : Type) (nH : NormedAddCommGroup H),
      letI := nH
      ∃ (iH : InnerProductSpace ℂ H),
        letI := iH
        ∃ (cH : CompleteSpace H),
          letI := cH
          ∃ v : ι → H,(∀ i j,⟪v i,v j⟫_ℂ = K i j) ∧
            Dense (Submodule.span ℂ (Set.range v) : Set H) := by
  let k : PositiveKernel ι := ⟨K,hHerm,hPos⟩
  exact ⟨KernelHilbert k,inferInstance,inferInstance,inferInstance,kernelVector k,
    kernelVector_inner k,kernelVector_dense_span k⟩

end CyclicBell.General.Coverage
