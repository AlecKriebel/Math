import CyclicBell.GeneralSupportAlgebra

/-! A shorter proof of manuscript prop:mub. Every Hermitian circulant and
every diagonal-unitary conjugate of a Hermitian circulant has constant diagonal.
A nonscalar Hermitian matrix with constant diagonal cannot attain a spectral
extremum at a computational vector. This argument replaces the manuscript's
wraparound-block/SVD proof; it does NOT verify each intermediate Toeplitz claim.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem positive_zero_diagonal {A : Mat ι} (hA : A.PosSemidef) (hz : ∀ i,A i i=0) : A=0 := by
  have htrace : Matrix.trace A=0 := by simp [Matrix.trace,Matrix.diag_apply,hz]
  have hgram : hA.sqrt*hA.sqrt.conjTranspose=A := by
    rw [hA.posSemidef_sqrt.isHermitian.eq,hA.sqrt_mul_self]
  have ht := congrArg Matrix.trace hgram
  rw [trace_gram_frobenius,htrace] at ht
  have hn : frobeniusSq hA.sqrt=0 := by exact_mod_cast ht
  have he := frobeniusSq_eq_zero _ |>.mp hn
  rw [← hgram,he,zero_mul]

/-- Spectral extremality is expressed by the precise Loewner inequality.
It is not a no-go theorem for a joint Bell SOS or for arbitrary extra settings. -/
theorem constant_diagonal_extremal_scalar (K : Mat ι) (κ : ℝ)
    (hdiag : ∀ i,K i i=(κ : ℂ))
    (hext : (((κ : ℂ) • (1 : Mat ι))-K).PosSemidef ∨
      (K-((κ : ℂ) • (1 : Mat ι))).PosSemidef) : K=(κ : ℂ) • 1 := by
  rcases hext with h | h
  · have hz : ∀ i,(((κ : ℂ) • (1 : Mat ι))-K) i i=0 := by
      intro i; simp [hdiag,Matrix.sub_apply,Matrix.smul_apply]
    exact sub_eq_zero.mp (positive_zero_diagonal h hz) |>.symm
  · have hz : ∀ i,(K-((κ : ℂ) • (1 : Mat ι))) i i=0 := by
      intro i; simp [hdiag,Matrix.sub_apply,Matrix.smul_apply]
    exact sub_eq_zero.mp (positive_zero_diagonal h hz)

theorem constant_diagonal_no_extremum (K : Mat ι) (κ : ℝ)
    (hdiag : ∀ i,K i i=(κ : ℂ)) (hnonscalar : K≠(κ : ℂ) • 1) :
    ¬ (((κ : ℂ) • (1 : Mat ι))-K).PosSemidef ∧
    ¬ (K-((κ : ℂ) • (1 : Mat ι))).PosSemidef := by
  exact ⟨fun h => hnonscalar (constant_diagonal_extremal_scalar K κ hdiag (Or.inl h)),
    fun h => hnonscalar (constant_diagonal_extremal_scalar K κ hdiag (Or.inr h))⟩

variable {d : ℕ} [NeZero d]

def circulantOperator (c : Ix d → ℂ) : Mat (Ix d) := fun i j => c (i-j)

def diagonalConjugatedCirculant (r c : Ix d → ℂ) : Mat (Ix d) :=
  fun i j => r i*c (i-j)*star (r j)

def exposureOperator (r c c' : Ix d → ℂ) : Mat (Ix d) :=
  circulantOperator c+diagonalConjugatedCirculant r c'

theorem exposure_constant_diagonal (r c c' : Ix d → ℂ) (hr : UnitPhases r) (i : Ix d) :
    exposureOperator r c c' i i=c 0+c' 0 := by
  simp only [exposureOperator,Matrix.add_apply,circulantOperator,
    diagonalConjugatedCirculant,sub_self]
  have hu := hr i
  calc c 0+r i*c' 0*star (r i)=c 0+c' 0*(star (r i)*r i) := by ring
       _=_ := by rw [hu,mul_one]

/-- Computational eigenvectors read the common diagonal entry. -/
theorem exposure_eigenvalue_diagonal (r c c' : Ix d → ℂ) (hr : UnitPhases r)
    (i : Ix d) (κ : ℝ)
    (heigen : exposureOperator r c c'*ᵥ((Pi.single i (1 : ℂ) : Ix d → ℂ))=(κ : ℂ) • (Pi.single i (1 : ℂ) : Ix d → ℂ)) :
    c 0+c' 0=(κ : ℂ) := by
  have hi := congrArg (fun x : Ix d → ℂ => x i) heigen
  simpa [Matrix.mulVec_single,exposure_constant_diagonal r c c' hr i] using hi

/-- Manuscript prop:mub, expressed as impossibility of either coefficientwise
spectral extremum. The phase vector may be ANY diagonal unitary; therefore it
includes exactly r_j=exp(pi*i*j/d), without a special-case assumption. -/
theorem computational_MUB_exposure_obstruction (r c c' : Ix d → ℂ)
    (hr : UnitPhases r) (i : Ix d) (κ : ℝ)
    (heigen : exposureOperator r c c'*ᵥ((Pi.single i (1 : ℂ) : Ix d → ℂ))=(κ : ℂ) • (Pi.single i (1 : ℂ) : Ix d → ℂ)) :
    exposureOperator r c c'=(κ : ℂ) • 1 ∨
      (¬ (((κ : ℂ) • (1 : Mat (Ix d)))-exposureOperator r c c').PosSemidef ∧
       ¬ (exposureOperator r c c'-((κ : ℂ) • (1 : Mat (Ix d)))).PosSemidef) := by
  by_cases h : exposureOperator r c c'=(κ : ℂ) • 1
  · exact Or.inl h
  · refine Or.inr (constant_diagonal_no_extremum _ κ ?_ h)
    intro j
    rw [exposure_constant_diagonal r c c' hr j,exposure_eigenvalue_diagonal r c c' hr i κ heigen]

/-- Source phase specialization; no generated numerical phase table is used. -/
theorem source_computational_MUB_exposure (c c' : Ix d → ℂ) (i : Ix d) (κ : ℝ)
    (heigen : exposureOperator (fun j : Ix d => cis (Real.pi*j.val/d)) c c'*ᵥ((Pi.single i (1 : ℂ) : Ix d → ℂ))=
      (κ : ℂ) • (Pi.single i (1 : ℂ) : Ix d → ℂ)) :
    exposureOperator (fun j : Ix d => cis (Real.pi*j.val/d)) c c'=(κ : ℂ) • 1 ∨
      (¬ (((κ : ℂ) • (1 : Mat (Ix d)))-
        exposureOperator (fun j : Ix d => cis (Real.pi*j.val/d)) c c').PosSemidef ∧
       ¬ (exposureOperator (fun j : Ix d => cis (Real.pi*j.val/d)) c c'-
        ((κ : ℂ) • (1 : Mat (Ix d)))).PosSemidef) :=
  computational_MUB_exposure_obstruction _ c c' (fun j => cis_unit _) i κ heigen

end CyclicBell.General
