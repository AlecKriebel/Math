import CyclicBell.GeneralExposure
import CyclicBell.GeneralWitness

/-! The literal Fourier/diagonal operator space and spectral-extremum form
of the manuscript's computational-MUB obstruction. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem hermitian_spectral_upper_psd (K : Mat ι) (hK : K.IsHermitian) (c : ℝ)
    (hc : ∀ z ∈ spectrum ℝ K,z≤c) : ((c : ℂ) • 1-K).PosSemidef := by
  let U : Mat ι := hK.eigenvectorUnitary
  have hU : U * U.conjTranspose=1 := Matrix.mem_unitaryGroup_iff.mp hK.eigenvectorUnitary.2
  have hp : (Matrix.diagonal (fun i => ((c-hK.eigenvalues i : ℝ) : ℂ))).PosSemidef := by
    apply Matrix.posSemidef_diagonal_iff.mpr
    intro i
    exact_mod_cast sub_nonneg.mpr (hc _ (hK.eigenvalues_mem_spectrum_real i))
  have hs : K=U * Matrix.diagonal (fun i => (hK.eigenvalues i : ℂ)) * U.conjTranspose := hK.spectral_theorem
  have he : (c : ℂ) • 1-K=
      U * Matrix.diagonal (fun i => ((c-hK.eigenvalues i : ℝ) : ℂ)) * U.conjTranspose := by
    have hd : Matrix.diagonal (fun i => ((c-hK.eigenvalues i : ℝ) : ℂ)) =
        (c : ℂ) • 1 - Matrix.diagonal (fun i => (hK.eigenvalues i : ℂ)) := by
      ext i j
      by_cases hij : i=j <;> simp [Matrix.diagonal_apply,Matrix.one_apply,hij]
    rw [hd,Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_smul,Matrix.mul_one,Matrix.smul_mul,hU]
    exact congrArg (fun X : Mat ι => (c : ℂ) • 1-X) hs
  rw [he]
  exact hp.mul_mul_conjTranspose_same U

theorem hermitian_spectral_lower_psd (K : Mat ι) (hK : K.IsHermitian) (c : ℝ)
    (hc : ∀ z ∈ spectrum ℝ K,c≤z) : (K-(c : ℂ) • 1).PosSemidef := by
  let U : Mat ι := hK.eigenvectorUnitary
  have hU : U * U.conjTranspose=1 := Matrix.mem_unitaryGroup_iff.mp hK.eigenvectorUnitary.2
  have hp : (Matrix.diagonal (fun i => ((hK.eigenvalues i-c : ℝ) : ℂ))).PosSemidef := by
    apply Matrix.posSemidef_diagonal_iff.mpr
    intro i
    exact_mod_cast sub_nonneg.mpr (hc _ (hK.eigenvalues_mem_spectrum_real i))
  have hs : K=U * Matrix.diagonal (fun i => (hK.eigenvalues i : ℂ)) * U.conjTranspose := hK.spectral_theorem
  have he : K-(c : ℂ) • 1=
      U * Matrix.diagonal (fun i => ((hK.eigenvalues i-c : ℝ) : ℂ)) * U.conjTranspose := by
    have hd : Matrix.diagonal (fun i => ((hK.eigenvalues i-c : ℝ) : ℂ)) =
        Matrix.diagonal (fun i => (hK.eigenvalues i : ℂ)) - (c : ℂ) • 1 := by
      ext i j
      by_cases hij : i=j <;> simp [Matrix.diagonal_apply,Matrix.one_apply,hij]
    rw [hd,Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_smul,Matrix.mul_one,Matrix.smul_mul,hU]
    exact congrArg (fun X : Mat ι => X-(c : ℂ) • 1) hs
  rw [he]
  exact hp.mul_mul_conjTranspose_same U

variable {d : ℕ} [NeZero d]

def fourierBasisMatrix (d : ℕ) [NeZero d] : Mat (Ix d) := fun i a => fourierVector a i

def fourierCoefficientOperator (x : Ix d → ℝ) : Mat (Ix d) :=
  fourierBasisMatrix d * Matrix.diagonal (fun a => (x a : ℂ)) * (fourierBasisMatrix d).conjTranspose

def fourierCoefficientKernel (x : Ix d → ℝ) (j : Ix d) : ℂ :=
  (invSqrtDim d : ℂ)^2 * ∑ a,(x a : ℂ)*chi (-(a*j))

theorem fourierCoefficient_circulant (x : Ix d → ℝ) :
    fourierCoefficientOperator x=circulantOperator (fourierCoefficientKernel x) := by
  ext i j
  simp only [fourierCoefficientOperator,Matrix.mul_apply,Matrix.diagonal_apply,
    Matrix.conjTranspose_apply,fourierBasisMatrix,fourierVector,circulantOperator,
    fourierCoefficientKernel,Finset.mul_sum]
  simp only [mul_ite,mul_zero,Finset.sum_ite_eq',Finset.mem_univ,if_true,
    star_mul,star_real,chi_star,neg_neg]
  apply Finset.sum_congr rfl
  intro a _
  rw [mul_sub,neg_sub,chi_sub,chi_star]
  ring

def MUBSpaceOperator (r : Ix d → ℂ) (x y : Ix d → ℝ) : Mat (Ix d) :=
  fourierCoefficientOperator x +
    Matrix.diagonal r * fourierCoefficientOperator y * (Matrix.diagonal r).conjTranspose

theorem MUBSpace_representation (r : Ix d → ℂ) (x y : Ix d → ℝ) :
    MUBSpaceOperator r x y = exposureOperator r (fourierCoefficientKernel x) (fourierCoefficientKernel y) := by
  rw [MUBSpaceOperator,fourierCoefficient_circulant,fourierCoefficient_circulant]
  ext i j
  simp [exposureOperator,diagonalConjugatedCirculant,circulantOperator,
    Matrix.diagonal_mul,Matrix.mul_diagonal,Matrix.diagonal_conjTranspose]

theorem MUBSpace_hermitian (r : Ix d → ℂ) (x y : Ix d → ℝ) :
    (MUBSpaceOperator r x y).IsHermitian := by
  have hx (v : Ix d → ℝ) : (fourierCoefficientOperator v).IsHermitian := by
    unfold fourierCoefficientOperator
    apply Matrix.isHermitian_mul_mul_conjTranspose
    exact Matrix.isHermitian_diagonal_iff.mpr (fun i => by change star (v i : ℂ) = (v i : ℂ); simp)
  exact (hx x).add (Matrix.isHermitian_mul_mul_conjTranspose _ (hx y))

/-- Literal proposition: every nonscalar element of the stated Fourier/diagonal
operator space with a computational eigenvector has spectral values strictly
on both sides of that eigenvalue. -/
theorem computational_MUB_spectral_obstruction (r : Ix d → ℂ) (hr : UnitPhases r)
    (x y : Ix d → ℝ) (i : Ix d) (c : ℝ)
    (heigen : MUBSpaceOperator r x y *ᵥ (Pi.single i (1 : ℂ) : Ix d → ℂ) =
      (c : ℂ) • (Pi.single i (1 : ℂ) : Ix d → ℂ)) :
    MUBSpaceOperator r x y=(c : ℂ) • 1 ∨
      ((∃ z ∈ spectrum ℝ (MUBSpaceOperator r x y),c<z) ∧
       (∃ z ∈ spectrum ℝ (MUBSpaceOperator r x y),z<c)) := by
  classical
  let K := MUBSpaceOperator r x y
  have hK : K.IsHermitian := MUBSpace_hermitian r x y
  by_cases hs : K=(c : ℂ) • 1
  · exact Or.inl hs
  · apply Or.inr
    have he : K = exposureOperator r (fourierCoefficientKernel x) (fourierCoefficientKernel y) :=
      MUBSpace_representation r x y
    have hdiag : ∀ j,K j j=(c : ℂ) := by
      intro j
      rw [he,exposure_constant_diagonal _ _ _ hr j]
      apply exposure_eigenvalue_diagonal _ _ _ hr i c
      rwa [← he]
    have hn := constant_diagonal_no_extremum K c hdiag hs
    constructor
    · by_contra h
      push_neg at h
      exact hn.1 (hermitian_spectral_upper_psd K hK c h)
    · by_contra h
      push_neg at h
      exact hn.2 (hermitian_spectral_lower_psd K hK c h)

theorem phi_computational_projector (K : Mat (Ix d)) (b : Ix d) :
    expectation (maximallyEntangled d)
      (kron K (projector (Pi.single b (1 : ℂ) : Ix d → ℂ)))=K b b/(d : ℂ) := by
  rw [phi_trace]
  congr 1
  simp [Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,Matrix.transpose_apply,
    projector,Pi.single_apply,eq_comm]

/-- Saturation of a separately bounded sum at the computational PVM forces
EVERY coefficient to be scalar. Thus such a bound cannot distinguish this PVM
from other measurements. -/
theorem computational_PVM_coefficientwise_saturation (r : Ix d → ℂ) (hr : UnitPhases r)
    (x y : Ix d → Ix d → ℝ) (c : Ix d → ℝ)
    (hcap : ∀ b,∀ z ∈ spectrum ℝ (MUBSpaceOperator r (x b) (y b)),z≤c b)
    (hsat : (expectation (maximallyEntangled d)
      (∑ b,kron (MUBSpaceOperator r (x b) (y b))
        (projector (Pi.single b (1 : ℂ) : Ix d → ℂ)))).re=(∑ b,c b)/(d : ℝ)) :
    ∀ b,MUBSpaceOperator r (x b) (y b)=(c b : ℂ) • 1 := by
  classical
  let K := fun b => MUBSpaceOperator r (x b) (y b)
  have hpos (b : Ix d) : ((c b : ℂ) • 1-K b).PosSemidef :=
    hermitian_spectral_upper_psd _ (MUBSpace_hermitian _ _ _) _ (hcap b)
  have hdiag (b j : Ix d) : K b j j=K b b b := by
    dsimp [K]
    rw [MUBSpace_representation,
      exposure_constant_diagonal _ _ _ hr j,exposure_constant_diagonal _ _ _ hr b]
  have hn (b : Ix d) : 0≤c b-(K b b b).re := by
    have h := (hpos b).2 (Pi.single b (1 : ℂ))
    have he : (0 : ℂ)≤(c b : ℂ)-K b b b := by
      simpa [Matrix.mulVec, dotProduct, Pi.single_apply] using h
    exact he.1
  have he : (∑ b,(K b b b).re) = ∑ b,c b := by
    simp only [expectation_sum,phi_computational_projector,Complex.re_sum] at hsat
    have hdiv (z : ℂ) : (z/(d : ℂ)).re=z.re/(d : ℝ) := by
      simp only [Complex.div_re,Complex.natCast_re,Complex.natCast_im,mul_zero,add_zero,Complex.normSq_natCast]
      field_simp [ne_of_gt (dimension_pos (d := d))]
      ring
    simp_rw [hdiv] at hsat
    rw [← Finset.sum_div] at hsat
    exact (div_left_inj' (ne_of_gt (dimension_pos (d := d)))).mp hsat
  have hzero : (∑ b,(c b-(K b b b).re))=0 := by rw [Finset.sum_sub_distrib,he,sub_self]
  intro b
  have hb := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hn j)).mp hzero b (Finset.mem_univ b)
  have hreal : K b b b=((K b b b).re : ℂ) := by
    have hh := congrArg (fun T : Mat (Ix d) => T b b) (MUBSpace_hermitian r (x b) (y b)).eq
    have hi := congrArg Complex.im hh
    have hi0 : (K b b b).im=0 := by
      change -(K b b b).im=(K b b b).im at hi
      linarith
    apply Complex.ext <;> simp [hi0]
  apply constant_diagonal_extremal_scalar (K b) (c b)
  · intro j
    rw [hdiag b j,hreal,sub_eq_zero.mp hb]
  · exact Or.inl (hpos b)

end CyclicBell.General
