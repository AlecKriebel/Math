import CyclicBell.GeneralCoverageWitness
import CyclicBell.GeneralCoverageSourceFactors
import CyclicBell.GeneralRigidity
import CyclicBell.GeneralCoverageSourceOrder
import CyclicBell.GeneralCoverageSpectralMeasurement

/-! Literal simple spectrum of the source appendix relative weighted cycle.
Normalization is by its actual scalar offset; the source clock/shift matrices
are retained throughout. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def sourceNormalizedWeights (y j : Ix d) : ℂ := star (equalityBase d)*chi (y-j-1)

theorem sourceNormalizedWeights_unit (y : Ix d) : UnitPhases (sourceNormalizedWeights y) := by
  intro j
  have hb : star (equalityBase d)*equalityBase d=1 := cis_unit _
  have hc := chi_star_mul (y-j-1)
  simp only [sourceNormalizedWeights,star_mul,star_star]
  calc
    (star (chi (y-j-1))*equalityBase d)*(star (equalityBase d)*chi (y-j-1)) =
        (star (equalityBase d)*equalityBase d)*(star (chi (y-j-1))*chi (y-j-1)) := by ring
    _ = 1 := by rw [hb,hc]; simp

theorem sourceNormalizedWeights_product (hd : 2≤d) (y : Ix d) :
    (∏ j,sourceNormalizedWeights y j)=1 := by
  have hb : star (equalityBase d)*equalityBase d=1 := cis_unit _
  simp only [sourceNormalizedWeights]
  rw [Finset.prod_mul_distrib,Finset.prod_const,
    Finset.card_univ,ZMod.card,source_relative_weight_product hd,
    ←source_equalityBase_power hd,←mul_pow,hb,one_pow]

theorem sourceNormalizedWeights_matrix (y : Ix d) :
    weightedCycle (sourceNormalizedWeights y) = star (equalityBase d) • sourceRelative y := by
  rw [source_relative_weights]
  ext i j
  simp only [weightedCycle,sourceNormalizedWeights,Matrix.smul_apply,smul_eq_mul]
  split_ifs <;> simp

theorem source_relative_eigenspace_eq_normalized (y a : Ix d) :
    Module.End.eigenspace (sourceRelative y).mulVecLin (equalityRoot a) =
      Module.End.eigenspace (weightedCycle (sourceNormalizedWeights y)).mulVecLin (chi a) := by
  have hb : star (equalityBase d)*equalityBase d=1 := cis_unit _
  have hb' : equalityBase d*star (equalityBase d)=1 := by simpa only [mul_comm] using hb
  rw [sourceNormalizedWeights_matrix]
  ext v
  simp only [Module.End.mem_eigenspace_iff,Matrix.mulVecLin_apply,
    Matrix.smul_mulVec_assoc,equalityRoot]
  constructor
  · intro h
    rw [h,smul_smul,←mul_assoc,hb,one_mul]
  · intro h
    have hh := congrArg (fun w : Ix d → ℂ => equalityBase d • w) h
    simpa only [smul_smul,hb',one_smul] using hh

theorem source_relative_eigenspace_finrank (hd : 2≤d) (y a : Ix d) :
    Module.finrank ℂ (Module.End.eigenspace (sourceRelative y).mulVecLin (equalityRoot a))=1 := by
  rw [source_relative_eigenspace_eq_normalized]
  exact weighted_cycle_eigenspace_finrank _ (sourceNormalizedWeights_unit y)
    (sourceNormalizedWeights_product hd y) a

theorem source_relative_charpoly (hd : 2≤d) (y : Ix d) :
    (sourceRelative y).charpoly=Polynomial.X^d-Polynomial.C ((-1 : ℂ)^(d-1)) := by
  rw [source_relative_weights,weighted_cycle_charpoly _ (fun j => chi_ne_zero _),
    source_relative_weight_product hd]

def sourceRelativeBasisMatrix (y : Ix d) : Mat (Ix d) :=
  fun i a => phasedVector («prefix» (sourceNormalizedWeights y)) a i

theorem sourceRelativeBasisMatrix_unitary (y : Ix d) : UnitaryRel (sourceRelativeBasisMatrix y) := by
  constructor
  · ext a b
    change ip (phasedVector («prefix» (sourceNormalizedWeights y)) a)
      (phasedVector («prefix» (sourceNormalizedWeights y)) b) = (1 : Mat (Ix d)) a b
    simpa only [Matrix.one_apply] using phase_orthonormal _
      (prefix_unit _ (sourceNormalizedWeights_unit y)) a b
  · have h := phase_complete _ (prefix_unit _ (sourceNormalizedWeights_unit y))
    ext i j
    simpa only [sourceRelativeBasisMatrix,Matrix.mul_apply,Matrix.conjTranspose_apply,
      projector,Matrix.sum_apply] using congrArg (fun M : Mat (Ix d) => M i j) h

theorem source_relative_basis_eigen (hd : 2≤d) (y a : Ix d) :
    sourceRelative y *ᵥ phasedVector («prefix» (sourceNormalizedWeights y)) a =
      equalityRoot a • phasedVector («prefix» (sourceNormalizedWeights y)) a := by
  change (sourceRelative y).mulVecLin _ = _
  apply Module.End.mem_eigenspace_iff.mp
  rw [source_relative_eigenspace_eq_normalized]
  apply Module.End.mem_eigenspace_iff.mpr
  exact weighted_eigenbasis (sourceNormalizedWeights y) (sourceNormalizedWeights_unit y)
    (sourceNormalizedWeights_product hd y) a

theorem source_clock_adjoint_phasedVector (q : Ix d → ℂ) (a : Ix d) :
    (sourceClock d)ᴴ *ᵥ phasedVector q a = phasedVector q (a+1) := by
  ext j
  simp only [sourceClock,Matrix.diagonal_conjTranspose,Matrix.mulVec_diagonal,
    Pi.star_apply,phasedVector,fourierVector,chi_star]
  have he : -(a+1)*j = -j + -(a*j) := by ring
  rw [show -((a+1)*j) = -j + -(a*j) by ring,chi_add]
  ring

def sourceBobCycleWeights (a : Ix d) : ℂ := star (polarBase (a+1))

theorem sourceBobCycleWeights_unit : UnitPhases (sourceBobCycleWeights (d := d)) := by
  intro a
  simpa only [sourceBobCycleWeights,star_star,mul_comm] using polarBase_unit (a+1)

theorem sourceBobCycleWeights_product : (∏ a : Ix d,sourceBobCycleWeights a)=1 := by
  have h : (∏ a : Ix d,polarBase (a+1))=∏ a : Ix d,polarBase a :=
    Fintype.prod_equiv (Equiv.addRight 1) _ _ (fun _ => rfl)
  unfold sourceBobCycleWeights
  rw [←star_prod,h,polarBase_product,star_one]

theorem sourceBob_transpose_basis_action (hd : 2≤d) (y a : Ix d) :
    (sourceBob y)ᵀ *ᵥ phasedVector («prefix» (sourceNormalizedWeights y)) a =
      sourceBobCycleWeights a • phasedVector («prefix» (sourceNormalizedWeights y)) (a+1) := by
  rw [sourceBob_transpose_finiteCalc,←Matrix.mulVec_mulVec,source_clock_adjoint_phasedVector]
  rw [finiteCalc_eigenvector (sourceRelative y) (source_relative_unitary y)
    (sourceLiteralInversePolar (d := d)) (equalityRoot (a+1)) _ (source_relative_basis_eigen hd y (a+1)),
    sourceLiteralInversePolar_at_root hd]
  rfl

theorem sourceBob_transpose_similarity (hd : 2≤d) (y : Ix d) :
    (sourceBob y)ᵀ * sourceRelativeBasisMatrix y =
      sourceRelativeBasisMatrix y * weightedCycle (sourceBobCycleWeights (d := d)) := by
  ext i a
  have h := congrArg (fun v : Ix d → ℂ => v i) (sourceBob_transpose_basis_action hd y a)
  have hr : (sourceRelativeBasisMatrix y * weightedCycle (sourceBobCycleWeights (d := d))) i a =
      sourceBobCycleWeights a * phasedVector («prefix» (sourceNormalizedWeights y)) (a+1) i := by
    rw [Matrix.mul_apply,Finset.sum_eq_single (a+1)]
    · simp only [sourceRelativeBasisMatrix,weightedCycle,if_pos rfl,ite_true,mul_comm]
    · intro b _ hba
      simp only [weightedCycle,if_neg hba,mul_zero]
    · simp
  rw [hr]
  exact h


theorem matrix_eigenspace_eq_kernel {ι : Type*} [Fintype ι] [DecidableEq ι]
    (U : Mat ι) (z : ℂ) :
    Module.End.eigenspace U.mulVecLin z=LinearMap.ker (U-z • 1).mulVecLin := by
  ext v
  simp only [Module.End.mem_eigenspace_iff,LinearMap.mem_ker,Matrix.mulVecLin_apply,
    Matrix.sub_mulVec,Matrix.smul_mulVec_assoc,Matrix.one_mulVec,sub_eq_zero]

theorem matrix_eigenspace_finrank_of_rank {ι : Type*} [Fintype ι] [DecidableEq ι]
    (U W : Mat ι) (z : ℂ) (h : (U-z • 1).rank=(W-z • 1).rank) :
    Module.finrank ℂ (Module.End.eigenspace U.mulVecLin z)=
      Module.finrank ℂ (Module.End.eigenspace W.mulVecLin z) := by
  rw [matrix_eigenspace_eq_kernel,matrix_eigenspace_eq_kernel]
  have hU := LinearMap.finrank_range_add_finrank_ker (U-z • 1).mulVecLin
  have hW := LinearMap.finrank_range_add_finrank_ker (W-z • 1).mulVecLin
  change (U-z • 1).rank+_= _ at hU
  change (W-z • 1).rank+_= _ at hW
  omega

theorem matrix_eigenspace_finrank_transpose {ι : Type*} [Fintype ι] [DecidableEq ι]
    (U : Mat ι) (z : ℂ) :
    Module.finrank ℂ (Module.End.eigenspace Uᵀ.mulVecLin z)=
      Module.finrank ℂ (Module.End.eigenspace U.mulVecLin z) := by
  apply matrix_eigenspace_finrank_of_rank
  have he : Uᵀ-z • 1=(U-z • 1)ᵀ := by simp
  rw [he,Matrix.rank_transpose]

theorem matrix_rank_mul_unitary_right {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A S : Mat ι) (hS : UnitaryRel S) : (A*S).rank=A.rank := by
  apply le_antisymm (Matrix.rank_mul_le_left _ _)
  have h := Matrix.rank_mul_le_left (A*S) Sᴴ
  simpa only [Matrix.mul_assoc,hS.2,Matrix.mul_one] using h

theorem matrix_rank_mul_unitary_left {ι : Type*} [Fintype ι] [DecidableEq ι]
    (S A : Mat ι) (hS : UnitaryRel S) : (S*A).rank=A.rank := by
  apply le_antisymm (Matrix.rank_mul_le_right _ _)
  have h := Matrix.rank_mul_le_right Sᴴ (S*A)
  simpa only [←Matrix.mul_assoc,hS.1,Matrix.one_mul] using h

theorem matrix_eigenspace_finrank_unitary_intertwiner {ι : Type*} [Fintype ι] [DecidableEq ι]
    (U W S : Mat ι) (hS : UnitaryRel S) (hUS : U*S=S*W) (z : ℂ) :
    Module.finrank ℂ (Module.End.eigenspace U.mulVecLin z)=
      Module.finrank ℂ (Module.End.eigenspace W.mulVecLin z) := by
  apply matrix_eigenspace_finrank_of_rank
  have h : (U-z • 1)*S=S*(W-z • 1) := by
    simp only [Matrix.sub_mul,Matrix.mul_sub,Matrix.smul_mul,Matrix.mul_smul,
      Matrix.one_mul,Matrix.mul_one,hUS]
  have hr := congrArg Matrix.rank h
  simpa only [matrix_rank_mul_unitary_right _ S hS,matrix_rank_mul_unitary_left S _ hS] using hr

/-- Literal source Bob matrix: every dth root has a one-dimensional eigenspace. -/
theorem sourceBob_eigenspace_finrank (hd : 2≤d) (y a : Ix d) :
    Module.finrank ℂ (Module.End.eigenspace (sourceBob y).mulVecLin (chi a))=1 := by
  rw [←matrix_eigenspace_finrank_transpose]
  rw [matrix_eigenspace_finrank_unitary_intertwiner _ _ _
    (sourceRelativeBasisMatrix_unitary y) (sourceBob_transpose_similarity hd y)]
  exact weighted_cycle_eigenspace_finrank _ sourceBobCycleWeights_unit sourceBobCycleWeights_product a

theorem matrix_mem_spectrum_of_eigenspace_finrank_one {ι : Type*} [Fintype ι] [DecidableEq ι]
    (U : Mat ι) (z : ℂ) (hz : Module.finrank ℂ (Module.End.eigenspace U.mulVecLin z)=1) :
    z ∈ MatrixSpectrum U := by
  have he : Module.End.HasEigenvalue U.mulVecLin z := by
    intro hbot
    change Module.End.eigenspace U.mulVecLin z=⊥ at hbot
    rw [hbot,finrank_bot] at hz
    exact zero_ne_one hz
  have hs := he.mem_spectrum
  change z ∈ spectrum ℂ U
  rwa [←AlgEquiv.spectrum_eq (Matrix.toLinAlgEquiv' : Mat ι ≃ₐ[ℂ] Module.End ℂ (ι → ℂ)) U]

/-- Exactly the shifted roots from the manuscript, all present and simple. -/
theorem source_relative_full_simple_spectrum (hd : 2≤d) (y : Ix d) :
    MatrixSpectrum (sourceRelative y)=Set.range (equalityRoot (d := d)) ∧
      ∀ a : Ix d,Module.finrank ℂ
        (Module.End.eigenspace (sourceRelative y).mulVecLin (equalityRoot a))=1 := by
  refine ⟨?_,source_relative_eigenspace_finrank hd y⟩
  ext z
  constructor
  · intro hz
    obtain ⟨a,ha⟩ := source_relative_spectral_root hd y ⟨z,hz⟩
    exact ⟨a,ha.symm⟩
  · rintro ⟨a,rfl⟩
    exact matrix_mem_spectrum_of_eigenspace_finrank_one _ _ (source_relative_eigenspace_finrank hd y a)

/-- Exactly all dth roots for the actual source coefficient matrix, all simple. -/
theorem sourceBob_full_simple_spectrum (hd : 2≤d) (y : Ix d) :
    MatrixSpectrum (sourceBob y)=Set.range (chi (d := d)) ∧
      ∀ a : Ix d,Module.finrank ℂ (Module.End.eigenspace (sourceBob y).mulVecLin (chi a))=1 := by
  refine ⟨?_,sourceBob_eigenspace_finrank hd y⟩
  ext z
  constructor
  · intro hz
    obtain ⟨a,ha⟩ := finite_order_spectral_root (sourceBob y) (sourceBob_unitary hd y)
      (sourceBob_order hd y) ⟨z,hz⟩
    exact ⟨a,ha.symm⟩
  · rintro ⟨a,rfl⟩
    exact matrix_mem_spectrum_of_eigenspace_finrank_one _ _ (sourceBob_eigenspace_finrank hd y a)

end CyclicBell.General
