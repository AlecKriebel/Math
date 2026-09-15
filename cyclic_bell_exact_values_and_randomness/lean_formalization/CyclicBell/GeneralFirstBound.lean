import CyclicBell.GeneralFunctionalCalculus
import CyclicBell.GeneralModel

/-! All-dimensional first-family upper bound for arbitrary finite local
coordinate dimensions and arbitrary positive trace-one mixed states.

The continuous half-polar factors are obtained from the pinned Mathlib CFC,
including the zero case. Every factor premise is discharged before the physical
endpoint; neither a chosen spectrum nor attainment is a Strategy field.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def firstReducedOperator (A U : Mat ι) (B : Ix d → Mat ι) : Mat ι :=
  ∑ y,herm (A*(1+chi y • U)*B y)

def halfPolarResidual (A H K B : Mat ι) : Mat ι := H*A.conjTranspose-K*B

/-- Algebraic positive-factor identity; the zero/kernel case is already
included in the functional-factor construction used below. -/
theorem halfPolar_gap_identity (A H K D B L : Mat ι)
    (hH : H.conjTranspose*H=D) (hK : K.conjTranspose*K=D)
    (hHK : H.conjTranspose*K=L) (hB : UnitaryRel B) (hDB : D*B=B*D) :
    (halfPolarResidual A H K B).conjTranspose*halfPolarResidual A H K B =
      A*D*A.conjTranspose+D-(A*L*B+(A*L*B).conjTranspose) := by
  have hKH : K.conjTranspose*H=L.conjTranspose := by
    simpa only [Matrix.conjTranspose_mul,Matrix.conjTranspose_conjTranspose]
      using congrArg Matrix.conjTranspose hHK
  have hBD : B.conjTranspose*D*B=D := by
    rw [mul_assoc,hDB,← mul_assoc,hB.1,one_mul]
  calc
    (halfPolarResidual A H K B).conjTranspose*halfPolarResidual A H K B =
        A*(H.conjTranspose*H)*A.conjTranspose-
        A*(H.conjTranspose*K)*B-
        B.conjTranspose*(K.conjTranspose*H)*A.conjTranspose+
        B.conjTranspose*(K.conjTranspose*K)*B := by
      unfold halfPolarResidual
      simp only [Matrix.conjTranspose_sub,Matrix.conjTranspose_mul,
        Matrix.conjTranspose_conjTranspose]
      noncomm_ring
    _ = _ := by
      rw [hH,hK,hHK,hKH,hBD]
      simp only [Matrix.conjTranspose_mul]
      noncomm_ring

/-- Exact global SOS. No assumption about eigenvalues or the chosen witness. -/
theorem first_matrix_sos (hd : 2≤d) (A U : Mat ι) (B : Ix d → Mat ι)
    (hA : UnitaryRel A) (hU : UnitaryRel U) (hB : ∀ y,UnitaryRel (B y))
    (hUB : ∀ y,U*B y=B y*U) :
    ∃ (P : Ix d → Mat ι) (G : Mat ι),
      (scalarMaximum d : ℂ) • 1-firstReducedOperator A U B =
        (1/2 : ℂ) • (∑ y,(P y).conjTranspose*P y)+
        (1/2 : ℂ) • (G.conjTranspose*G)+
        (1/2 : ℂ) • ((G*A.conjTranspose).conjTranspose*(G*A.conjTranspose)) := by
  obtain ⟨H,K,D,G,hH,hK,hHK,hDB,hG⟩ := matrix_functional_factors hd U B hU hB hUB
  let P : Ix d → Mat ι := fun y => halfPolarResidual A (H y) (K y) (B y)
  refine ⟨P,G,?_⟩
  have hp (y : Ix d) : (P y).conjTranspose*P y =
      A*D y*A.conjTranspose+D y-
        (A*(1+chi y • U)*B y+(A*(1+chi y • U)*B y).conjTranspose) :=
    halfPolar_gap_identity A (H y) (K y) (D y) (B y) _ (hH y) (hK y) (hHK y) (hB y) (hDB y)
  have hag : (G*A.conjTranspose).conjTranspose*(G*A.conjTranspose)=
      A*(G.conjTranspose*G)*A.conjTranspose := by
    simp [Matrix.conjTranspose_mul,mul_assoc]
  rw [hag,hG]
  simp_rw [hp]
  rw [Finset.sum_sub_distrib,Finset.sum_add_distrib,← Finset.sum_mul,← Finset.mul_sum]
  unfold firstReducedOperator herm
  simp only [mul_sub,sub_mul,mul_smul_comm,smul_mul_assoc,one_mul,mul_one,hA.2,
    Finset.smul_sum,smul_sub,smul_add]
  ext i j
  simp only [Matrix.sub_apply,Matrix.add_apply,Matrix.smul_apply,smul_eq_mul,Finset.sum_apply]
  ring

/-- The trace argument covers mixed states directly. -/
theorem first_matrix_upper (hd : 2≤d) (ρ : StateOn ι)
    (A U : Mat ι) (B : Ix d → Mat ι) (hA : UnitaryRel A)
    (hU : UnitaryRel U) (hB : ∀ y,UnitaryRel (B y)) (hUB : ∀ y,U*B y=B y*U) :
    stateEval ρ.density (firstReducedOperator A U B)≤scalarMaximum d := by
  obtain ⟨P,G,hgap⟩ := first_matrix_sos hd A U B hA hU hB hUB
  have hnP : 0≤stateEval ρ.density (∑ y,(P y).conjTranspose*P y) := by
    rw [stateEval_sum]
    exact Finset.sum_nonneg (fun y _ => stateEval_square_nonnegative ρ.positive (P y))
  have hnG := stateEval_square_nonnegative ρ.positive G
  have hnGA := stateEval_square_nonnegative ρ.positive (G*A.conjTranspose)
  have h := congrArg (stateEval ρ.density) hgap
  have half : (1/2 : ℂ)=((1/2 : ℝ) : ℂ) := by norm_num
  rw [stateEval_sub,stateEval_real_smul,stateEval_one ρ.normalized] at h
  simp only [half,stateEval_add,stateEval_real_smul] at h
  nlinarith

def firstValue {κ : Type*} [Fintype κ] [DecidableEq κ]
    (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ) : ℝ :=
  (∑ y : Ix d,stateEval s.state.density
    (kron (encoded (s.alice 0)+chi y • encoded (s.alice 1)) (encoded (s.bob (some y)))))+
  stateEval s.state.density (kron (encoded (s.alice 0)) (encoded (s.bob none)))

/-- Physical first-family endpoint with unrestricted finite coordinate types.
The number of outcomes is d, but neither local dimension is constrained to d. -/
theorem first_physical_upper {κ : Type*} [Fintype κ] [DecidableEq κ]
    (hd : 2≤d) (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ) :
    firstValue s≤2/Real.sin (Real.pi/(2*d))+1 := by
  let A₀ := encoded (s.alice 0)
  let A₁ := encoded (s.alice 1)
  let U := A₀.conjTranspose*A₁
  let B : Ix d → Mat κ := fun y => encoded (s.bob (some y))
  have h0 : UnitaryRel A₀ := encoded_unitary _
  have h1 : UnitaryRel A₁ := encoded_unitary _
  have hU : UnitaryRel U := h0.adjoint.mul h1
  have hB (y : Ix d) : UnitaryRel (B y) := encoded_unitary _
  have h := first_matrix_upper hd s.state
    (aliceLift (κ := κ) A₀) (aliceLift (κ := κ) U)
    (fun y => bobLift (ι := ι) (B y))
    (kron_unitary h0 UnitaryRel.one) (kron_unitary hU UnitaryRel.one)
    (fun y => kron_unitary UnitaryRel.one (hB y)) (fun y => lift_commute U (B y))
  have hterm (y : Ix d) :
      aliceLift (κ := κ) A₀*(1+chi y • aliceLift U)*bobLift (ι := ι) (B y)=
        kron (A₀+chi y • A₁) (B y) := by
    have he : A₀*(1+chi y • U)=A₀+chi y • A₁ := by
      rw [mul_add,mul_one,mul_smul_comm]
      change A₀+chi y • (A₀*(A₀.conjTranspose*A₁))=_
      rw [h0.cancel_right]
    change kron A₀ 1*(1+chi y • kron U 1)*kron 1 (B y)=_
    rw [← kron_one,← kron_smul_left,← kron_add_left,kron_mul,kron_mul]
    simpa [he]
  unfold firstReducedOperator at h
  simp_rw [hterm] at h
  rw [stateEval_sum] at h
  simp_rw [stateEval_herm _ _ s.state.positive.isHermitian] at h
  have ha := aligned_upper s.state.positive s.state.normalized
    (kron_unitary h0 (encoded_unitary (s.bob none)))
  change firstValue s≤scalarMaximum d+1
  unfold firstValue
  exact add_le_add h ha

/-- The global coefficient normalization and physical model are visible in
this expanded form; no new Strategy premise has been added. -/
theorem first_physical_upper_expanded {κ : Type*} [Fintype κ] [DecidableEq κ]
    (hd : 2≤d) (ρ : StateOn (ι × κ))
    (A : Fin 2 → Measurement d ι) (B : AugmentedInputs d → Measurement d κ) :
    (∑ y : Ix d,(Matrix.trace (ρ.density*
      kron ((∑ a,chi a • (A 0).effect a)+chi y • (∑ a,chi a • (A 1).effect a))
        (∑ b,chi b • (B (some y)).effect b))).re)+
      (Matrix.trace (ρ.density*kron (∑ a,chi a • (A 0).effect a)
        (∑ b,chi b • (B none).effect b))).re ≤
        2/Real.sin (Real.pi/(2*d))+1 :=
  first_physical_upper hd {state:=ρ,alice:=A,bob:=B}

end CyclicBell.General
