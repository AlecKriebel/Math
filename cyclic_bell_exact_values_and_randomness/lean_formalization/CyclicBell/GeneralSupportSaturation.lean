import CyclicBell.GeneralFirstBound
import CyclicBell.GeneralSupportAlgebra

/-! Passage from quantum saturation to actual matrix-on-support equations.
The amplitude is obtained from a positive square root of the arbitrary mixed
state. No faithfulness, supported dimension, reflection relation or maximality
is a field of the model. UNCOMPILED SOURCE. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

def localH (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) : Mat ι :=
  finiteCalc U hU (fun z => squareRootNorm (1+chi y*z))
def localK (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) : Mat ι :=
  finiteCalc U hU (fun z => continuousPolarRoot (1+chi y*z))
def localD (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) : Mat ι :=
  finiteCalc U hU (fun z => (‖1+chi y*z‖ : ℂ))
def localG (U : Mat ι) (hU : UnitaryRel U) : Mat ι :=
  finiteCalc U hU (fun z => (Real.sqrt (scalarMaximum d-scalarSum (d := d) z) : ℂ))

theorem localH_square (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) :
    (localH U hU y).conjTranspose*localH U hU y=localD U hU y := by
  unfold localH localD
  rw [← finiteCalc_star,← finiteCalc_mul]
  exact finiteCalc_congr U hU (fun z => squareRootNorm_square _)

theorem localK_square (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) :
    (localK U hU y).conjTranspose*localK U hU y=localD U hU y := by
  unfold localK localD
  rw [← finiteCalc_star,← finiteCalc_mul]
  exact finiteCalc_congr U hU (fun z => continuousPolarRoot_square _)

theorem localHK_cross (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) :
    (localH U hU y).conjTranspose*localK U hU y=1+chi y • U := by
  unfold localH localK
  rw [← finiteCalc_star,← finiteCalc_mul,← finiteCalc_coordinate U hU,
    ← finiteCalc_one U hU,← finiteCalc_smul,← finiteCalc_add]
  exact finiteCalc_congr U hU (fun z => continuousPolarRoot_cross _)

theorem localG_square (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U) :
    (localG (d := d) U hU).conjTranspose*localG U hU=
      (scalarMaximum d : ℂ) • 1-∑ y,localD U hU y := by
  unfold localG localD
  rw [← finiteCalc_star,← finiteCalc_mul,← finiteCalc_sum,← finiteCalc_const,← finiteCalc_sub]
  apply finiteCalc_congr U hU
  intro z
  have hn : 0≤scalarMaximum d-scalarSum (d := d) z :=
    sub_nonneg.mpr (scalar_bound hd z (spectrum_unit_norm (toCMatrix_unitary hU) z))
  simp [Complex.conj_ofReal,← Complex.ofReal_mul,Real.mul_self_sqrt hn,
    scalarSum,Complex.ofReal_sub,Complex.ofReal_sum]

def firstLocalOperator (A C : Mat ι) (B : Ix d → Mat κ) : Mat (ι × κ) :=
  ∑ y,herm (kron (A+chi y • C) (B y))

def firstLocalResidual (A U : Mat ι) (hU : UnitaryRel U) (B : Ix d → Mat κ) (y : Ix d) : Mat (ι × κ) :=
  kron (localH U hU y*A.conjTranspose) 1-kron (localK U hU y) (B y)

theorem first_local_sos (hd : 2≤d) (A C : Mat ι) (B : Ix d → Mat κ)
    (hA : UnitaryRel A) (hC : UnitaryRel C) (hB : ∀ y,UnitaryRel (B y)) :
    let U := A.conjTranspose*C
    let hU := hA.adjoint.mul hC
    (scalarMaximum d : ℂ) • 1-firstLocalOperator A C B=
      (1/2 : ℂ) • (∑ y,(firstLocalResidual A U hU B y).conjTranspose*firstLocalResidual A U hU B y)+
      (1/2 : ℂ) • ((kron (localG U hU) (1 : Mat κ)).conjTranspose*kron (localG U hU) 1)+
      (1/2 : ℂ) • ((kron (localG U hU*A.conjTranspose) (1 : Mat κ)).conjTranspose*
        kron (localG U hU*A.conjTranspose) 1) := by
  dsimp only
  let U := A.conjTranspose*C
  let hU := hA.adjoint.mul hC
  have hy (y : Ix d) : (firstLocalResidual A U hU B y).conjTranspose*firstLocalResidual A U hU B y=
      kron (A*localD U hU y*A.conjTranspose+localD U hU y) 1-
        (kron (A+chi y • C) (B y)+(kron (A+chi y • C) (B y)).conjTranspose) := by
    have h := halfPolar_gap_identity (aliceLift (κ := κ) A)
      (aliceLift (κ := κ) (localH U hU y)) (aliceLift (κ := κ) (localK U hU y))
      (aliceLift (κ := κ) (localD U hU y)) (bobLift (ι := ι) (B y))
      (aliceLift (κ := κ) (1+chi y • U))
      (by simp [aliceLift,localH_square]) (by simp [aliceLift,localK_square])
      (by simp [aliceLift,localHK_cross]) (kron_unitary UnitaryRel.one (hB y)) (lift_commute _ _)
    have he : A*(1+chi y • U)=A+chi y • C := by
      simp only [mul_add,mul_one,mul_smul_comm,U,hA.cancel_right]
    simpa [firstLocalResidual,halfPolarResidual,aliceLift,bobLift,kron_mul,
      he,← kron_add_left,mul_assoc] using h
  simp_rw [hy]
  simp only [kron_star,kron_mul,Matrix.conjTranspose_one,one_mul,Matrix.conjTranspose_mul]
  rw [localG_square hd]
  have hgA : A*(localG U hU).conjTranspose*(localG U hU*A.conjTranspose)=
      A*((localG U hU).conjTranspose*localG U hU)*A.conjTranspose := by noncomm_ring
  rw [hgA,localG_square hd]
  unfold firstLocalOperator herm
  simp only [kron_add_left,kron_smul_left,Finset.sum_add_distrib,Finset.sum_sub_distrib,
    ← Finset.sum_mul,← Finset.mul_sum,mul_sub,sub_mul,one_mul,mul_one,hA.2,
    mul_smul_comm,smul_mul_assoc,Finset.smul_sum,smul_sub,smul_add]
  ext i j
  simp [kron,Matrix.mul_apply,Finset.sum_sub_distrib,Finset.sum_add_distrib]
  ring

theorem firstValue_operator (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ) :
    firstValue s=stateEval s.state.density
      (firstLocalOperator (encoded (s.alice 0)) (encoded (s.alice 1))
        (fun y => encoded (s.bob (some y)))+
        herm (kron (encoded (s.alice 0)) (encoded (s.bob none)))) := by
  simp only [firstValue,stateEval_add,firstLocalOperator,stateEval_sum,
    stateEval_herm s.state.positive.isHermitian]

/-- Output equations are derived from the literal scalar maximum, for the
amplitude of the given mixed state's canonical finite purification. -/
theorem first_saturation_equations (hd : 2≤d)
    (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ)
    (hs : firstValue s=scalarMaximum d+1) :
    let A := encoded (s.alice 0)
    let U := A.conjTranspose*encoded (s.alice 1)
    let hU := (encoded_unitary (s.alice 0)).adjoint.mul (encoded_unitary (s.alice 1))
    let T := aliceAmplitude (stateFactor s.state)
    localG (d := d) U hU*T=0 ∧
    A*T*bobRight (ε := ι × κ) (encoded (s.bob none))=T ∧
    ∀ y : Ix d,localH U hU y*A.conjTranspose*T=
      localK U hU y*T*bobRight (ε := ι × κ) (encoded (s.bob (some y))) := by
  dsimp only
  let A := encoded (s.alice 0)
  let C := encoded (s.alice 1)
  let U := A.conjTranspose*C
  let hA := encoded_unitary (s.alice 0)
  let hU := hA.adjoint.mul (encoded_unitary (s.alice 1))
  let B : Ix d → Mat κ := fun y => encoded (s.bob (some y))
  let P := firstLocalResidual A U hU B
  let G := kron (localG (d := d) U hU) (1 : Mat κ)
  let G' := kron (localG (d := d) U hU*A.conjTranspose) (1 : Mat κ)
  let R := 1-kron A (encoded (s.bob none))
  have hgap := first_local_sos hd A C B hA (encoded_unitary _) (fun y => encoded_unitary _)
  have halign := aligned_gap_identity (kron_unitary hA (encoded_unitary (s.bob none)))
  have htotal : (scalarMaximum d+1 : ℂ) • 1-
      (firstLocalOperator A C B+herm (kron A (encoded (s.bob none))))=
        (1/2 : ℂ) • (∑ y,(P y).conjTranspose*P y)+
        (1/2 : ℂ) • (G.conjTranspose*G)+(1/2 : ℂ) • (G'.conjTranspose*G')+
        (1/2 : ℂ) • (R.conjTranspose*R) := by
    change _=(1/2 : ℂ) • (∑ y,(P y).conjTranspose*P y)+_+_+_
    rw [← hgap,← halign]
    ext i j
    simp [add_smul]
    ring
  have hp : ∀ y,0≤stateEval s.state.density ((P y).conjTranspose*P y) :=
    fun y => stateEval_square_nonnegative s.state.positive _
  have hg := stateEval_square_nonnegative s.state.positive G
  have hg' := stateEval_square_nonnegative s.state.positive G'
  have hr := stateEval_square_nonnegative s.state.positive R
  have hsum := Finset.sum_nonneg (fun y _ => hp y)
  have he := congrArg (stateEval s.state.density) htotal
  have hv := firstValue_operator s
  have half : (1/2 : ℂ)=((1/2 : ℝ) : ℂ) := by norm_num
  simp only [stateEval_sub,stateEval_add,half,stateEval_real_smul,stateEval_sum,
    stateEval_one s.state.normalized] at he
  have hs' : stateEval s.state.density (firstLocalOperator A C B)+
      stateEval s.state.density (herm (kron A (encoded (s.bob none))))=scalarMaximum d+1 := by
    rw [← stateEval_add,← hv]
    exact hs
  have hg0 : stateEval s.state.density (G.conjTranspose*G)=0 := by linarith
  have hr0 : stateEval s.state.density (R.conjTranspose*R)=0 := by linarith
  have hp0 : ∀ y,stateEval s.state.density ((P y).conjTranspose*P y)=0 :=
    finite_positive_sum_zero _ hp (by linarith)
  have hgL := congrArg aliceAmplitude ((state_square_zero_iff s.state G).mp hg0)
  have hrL := congrArg aliceAmplitude ((state_square_zero_iff s.state R).mp hr0)
  refine ⟨?_,?_,?_⟩
  · simpa [G,← aliceLift,amplitude_left] using hgL
  · simpa only [R,sub_mul,one_mul,amplitude_sub,amplitude_tensor,amplitude_zero,sub_eq_zero]
      using hrL.symm
  · intro y
    have hL := congrArg aliceAmplitude ((state_square_zero_iff s.state (P y)).mp (hp0 y))
    simpa only [P,firstLocalResidual,sub_mul,amplitude_sub,amplitude_tensor,
      bobRight,Matrix.transpose_one,kron_one,mul_one,amplitude_zero,sub_eq_zero] using hL

end CyclicBell.General
