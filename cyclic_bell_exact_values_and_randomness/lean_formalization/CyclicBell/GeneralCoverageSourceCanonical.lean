import CyclicBell.GeneralCoverageSourceFactors
import CyclicBell.GeneralCoveragePolarCanonical

/-! Actual positive modulus and canonical polar factor of the source pencils.
The literal source Bob coefficient matrix is identified with its conjugate. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def sourcePencil (y : Ix d) : Mat (Ix d) := sourceClock d + chi y • cyclicShift d

def sourceModulus (y : Ix d) : Mat (Ix d) :=
  finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => (‖1+z‖ : ℂ))

def sourceCanonicalPolar (y : Ix d) : Mat (Ix d) := ((sourceBob y)ᵀ)ᴴ

theorem sourcePencil_relative (y : Ix d) :
    sourcePencil y=sourceClock d*(1+sourceRelative y) := by
  unfold sourcePencil sourceRelative
  rw [mul_add,mul_one,mul_smul_comm,←mul_assoc,source_clock_unitary.2,one_mul]

theorem sourceModulus_star (y : Ix d) : (sourceModulus y)ᴴ=sourceModulus y := by
  unfold sourceModulus
  rw [←finiteCalc_star]
  apply finiteCalc_congr
  intro z
  simp

theorem sourceModulus_gram (y : Ix d) :
    sourceModulus y =
      (finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => squareRootNorm (1+z)))ᴴ *
      finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => squareRootNorm (1+z)) := by
  rw [←finiteCalc_star,←finiteCalc_mul]
  apply finiteCalc_congr
  intro z
  exact (squareRootNorm_square (1+(z : ℂ))).symm

theorem sourceModulus_positive (y : Ix d) : 0≤toCMatrix (sourceModulus y) := by
  rw [sourceModulus_gram]
  exact star_mul_self_nonneg _

theorem sourceCanonicalPolar_unitary (hd : 2≤d) (y : Ix d) :
    UnitaryRel (sourceCanonicalPolar y) :=
  (unitary_transpose (sourceBob_unitary hd y)).adjoint

theorem sourceLiteralInversePolar_modulus (hd : 2≤d) (y : Ix d)
    (z : MatrixSpectrum (sourceRelative y)) :
    star (sourceLiteralInversePolar (d := d) z)*(‖1+(z : ℂ)‖ : ℂ)=1+z := by
  obtain ⟨j,hj⟩ := source_relative_spectral_root hd y z
  rw [hj,sourceLiteralInversePolar_quotient hd,star_star]
  have hn : (‖1+equalityRoot j‖ : ℂ)≠0 := by
    exact_mod_cast (norm_ne_zero_iff.mpr (by simpa using equalityRoot_no_bad_phase hd (0 : Ix d) j))
  exact div_mul_cancel₀ _ hn

/-- Genuine polar factorization of the literal source pencil. -/
theorem sourceCanonicalPolar_factor (hd : 2≤d) (y : Ix d) :
    sourceCanonicalPolar y*sourceModulus y=sourcePencil y := by
  unfold sourceCanonicalPolar
  rw [sourceBob_transpose_finiteCalc,Matrix.conjTranspose_mul,Matrix.conjTranspose_conjTranspose,
    sourcePencil_relative,mul_assoc]
  congr 1
  unfold sourceModulus
  rw [←finiteCalc_star,←finiteCalc_mul]
  calc
    _ = finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => 1+z) :=
      finiteCalc_congr _ _ (sourceLiteralInversePolar_modulus hd y)
    _ = _ := by rw [finiteCalc_add,finiteCalc_one]; exact congrArg (fun T : Mat (Ix d) => 1+T) (finiteCalc_coordinate _ _)

theorem sourceModulus_square (hd : 2≤d) (y : Ix d) :
    sourceModulus y*sourceModulus y=(sourcePencil y)ᴴ*sourcePencil y := by
  conv_rhs => rw [←sourceCanonicalPolar_factor hd y]
  rw [Matrix.conjTranspose_mul,sourceModulus_star,mul_assoc,←mul_assoc (sourceCanonicalPolar y)ᴴ,
    (sourceCanonicalPolar_unitary hd y).1,one_mul]

/-- Identification with the actual CFC positive square root, not a named surrogate. -/
theorem sourceModulus_eq_canonical (hd : 2≤d) (y : Ix d) :
    CFC.sqrt (star (toCMatrix (sourcePencil y))*toCMatrix (sourcePencil y))=
      toCMatrix (sourceModulus y) := by
  apply CFC.sqrt_unique _ (sourceModulus_positive y)
  exact congrArg toCMatrix (sourceModulus_square hd y)

/-- The source pencil has no singular polar ambiguity: its positive modulus
has an explicitly constructed two-sided inverse. -/
theorem sourceModulus_inverse (hd : 2≤d) (y : Ix d) :
    ∃ G : Mat (Ix d),sourceModulus y*G=1 ∧ G*sourceModulus y=1 := by
  let G := finiteCalc (sourceRelative y) (source_relative_unitary y)
    (fun z => ((‖1+z‖ : ℂ))⁻¹)
  have hn (z : MatrixSpectrum (sourceRelative y)) : (‖1+(z : ℂ)‖ : ℂ)≠0 := by
    obtain ⟨j,hj⟩ := source_relative_spectral_root hd y z
    rw [hj]
    exact_mod_cast (norm_ne_zero_iff.mpr (by simpa using equalityRoot_no_bad_phase hd (0 : Ix d) j))
  refine ⟨G,?_,?_⟩
  · change finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => (‖1+z‖ : ℂ))*
        finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => (‖1+z‖ : ℂ)⁻¹)=1
    rw [←finiteCalc_mul,←finiteCalc_one (sourceRelative y) (source_relative_unitary y)]
    apply finiteCalc_congr
    intro z
    exact mul_inv_cancel₀ (hn z)
  · change finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => (‖1+z‖ : ℂ)⁻¹)*
        finiteCalc (sourceRelative y) (source_relative_unitary y) (fun z => (‖1+z‖ : ℂ))=1
    rw [←finiteCalc_mul,←finiteCalc_one (sourceRelative y) (source_relative_unitary y)]
    apply finiteCalc_congr
    intro z
    exact inv_mul_cancel₀ (hn z)

theorem sourceModulus_eq_relative_modulus (hd : 2≤d) (y : Ix d) :
    CFC.sqrt (star (1+toCMatrix (sourceRelative y))*(1+toCMatrix (sourceRelative y)))=
      toCMatrix (sourceModulus y) := by
  have he : (sourcePencil y)ᴴ*sourcePencil y=
      (1+sourceRelative y)ᴴ*(1+sourceRelative y) := by
    rw [sourcePencil_relative,Matrix.conjTranspose_mul,mul_assoc,
      ←mul_assoc (sourceClock d)ᴴ,source_clock_unitary.1,one_mul]
  have h := sourceModulus_eq_canonical hd y
  change CFC.sqrt (toCMatrix ((sourcePencil y)ᴴ*sourcePencil y))=toCMatrix (sourceModulus y) at h
  rw [he] at h
  exact h

/-- Literal Q_y=H_y^{-1}(1+W_y†)Z† from app:attainment, with a proved
actual two-sided inverse G rather than a totalized inverse assumption. -/
theorem sourceBob_transpose_inverse_formula (hd : 2≤d) (y : Ix d) :
    ∃ G : Mat (Ix d),sourceModulus y*G=1 ∧ G*sourceModulus y=1 ∧
      (sourceBob y)ᵀ=G*(1+(sourceRelative y)ᴴ)*(sourceClock d)ᴴ := by
  obtain ⟨G,hHG,hGH⟩ := sourceModulus_inverse hd y
  have h := congrArg Matrix.conjTranspose (sourceCanonicalPolar_factor hd y)
  simp only [Matrix.conjTranspose_mul,sourceModulus_star,sourceCanonicalPolar,
    Matrix.conjTranspose_conjTranspose] at h
  refine ⟨G,hHG,hGH,?_⟩
  calc
    (sourceBob y)ᵀ = G*(sourceModulus y*(sourceBob y)ᵀ) := by rw [←mul_assoc,hGH,one_mul]
    _ = G*(sourcePencil y)ᴴ := by rw [h]
    _ = _ := by rw [sourcePencil_relative,Matrix.conjTranspose_mul,Matrix.conjTranspose_add,
        Matrix.conjTranspose_one,mul_assoc]

/-- The source coefficient observable is the entrywise conjugate of the
unitary canonical polar factor of Z+chi(y)X (manuscript app:attainment). -/
theorem sourceBob_canonical_polar (hd : 2≤d) (y : Ix d) :
    sourceBob y=(sourceCanonicalPolar y)ᴴᵀ ∧
    toCMatrix (sourcePencil y)=toCMatrix (sourceCanonicalPolar y)*
      CFC.sqrt (star (toCMatrix (sourcePencil y))*toCMatrix (sourcePencil y)) ∧
    UnitaryRel (sourceCanonicalPolar y) := by
  refine ⟨?_,?_,sourceCanonicalPolar_unitary hd y⟩
  · simp [sourceCanonicalPolar]
  · rw [sourceModulus_eq_canonical hd]
    exact (congrArg toCMatrix (sourceCanonicalPolar_factor hd y)).symm

end CyclicBell.General
