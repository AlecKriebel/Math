import CyclicBell.GeneralSupportSaturation
import CyclicBell.GeneralEqualityPhases

/-! Support restriction, kernel-safe polar cancellation and the passage to
actual reflection equations. Nothing is asserted on the orthogonal complement
of the reduced-state support.  -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι ν : Type*} [Fintype ι] [Fintype ν] [DecidableEq ι] [DecidableEq ν]

def equalitySupport (U : Mat ι) (hU : UnitaryRel U) : Mat ι := finiteCalc U hU (equalityIndicator d)
def supportedPhase (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) : Mat ι :=
  finiteCalc U hU (scalarPolarPhase y)
def rootProjection (U : Mat ι) (hU : UnitaryRel U) (k : Ix d) : Mat ι :=
  finiteSpectralProjection U hU (equalityRoot k)

theorem scalarGap_zero_root (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (z : MatrixSpectrum U)
    (hz : (Real.sqrt (scalarMaximum d-scalarSum (d := d) z) : ℂ)=0) :
    (z : ℂ)^d=(-1 : ℂ)^(d-1) := by
  have hn := sub_nonneg.mpr (scalar_bound hd z (spectrum_unit_norm (toCMatrix_unitary hU) z))
  have hs : Real.sqrt (scalarMaximum d-scalarSum (d := d) z)=0 := by exact_mod_cast hz
  have hsq := Real.sq_sqrt hn
  rw [hs,zero_pow (by decide)] at hsq
  exact (scalar_equality_iff hd z (spectrum_unit_norm (toCMatrix_unitary hU) z)).mp (by linarith)

theorem equalitySupport_from_gap (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (hG : localG (d := d) U hU*T=0) : equalitySupport (d := d) U hU*T=T := by
  have h := finiteCalc_zero_transfer U hU
    (fun z => (Real.sqrt (scalarMaximum d-scalarSum (d := d) z) : ℂ))
    (fun z => equalityIndicator d z-1) T
    (fun z hz => by simp [equalityIndicator,scalarGap_zero_root hd U hU z hz]) hG
  rw [finiteCalc_sub,finiteCalc_one,Matrix.sub_mul,Matrix.one_mul,sub_eq_zero] at h
  exact h

/-- Functional identities on equality roots become equations on the actual
support, even when the same identity fails elsewhere in the Hilbert space. -/
theorem equality_supported_action (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (hE : equalitySupport (d := d) U hU*T=T)
    (f g : ℂ → ℂ) (hfg : ∀ k : Ix d,f (equalityRoot k)=g (equalityRoot k)) :
    finiteCalc U hU f*T=finiteCalc U hU g*T := by
  have he : finiteCalc U hU f*equalitySupport (d := d) U hU=
      finiteCalc U hU g*equalitySupport (d := d) U hU := by
    unfold equalitySupport
    rw [← finiteCalc_mul,← finiteCalc_mul]
    apply finiteCalc_congr U hU
    intro z
    by_cases hz : (z : ℂ)^d=(-1 : ℂ)^(d-1)
    · obtain ⟨k,hk⟩ := equalityRoot_complete z (spectrum_unit_norm (toCMatrix_unitary hU) z) hz
      simp [equalityIndicator,hz,hk,hfg k]
    · simp [equalityIndicator,hz]
  calc
    finiteCalc U hU f*T=finiteCalc U hU f*(equalitySupport (d := d) U hU*T) := by rw [hE]
    _=(finiteCalc U hU f*equalitySupport (d := d) U hU)*T := by rw [Matrix.mul_assoc]
    _=(finiteCalc U hU g*equalitySupport (d := d) U hU)*T := by rw [he]
    _=finiteCalc U hU g*T := by rw [Matrix.mul_assoc,hE]

theorem equality_power_on_support (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (hE : equalitySupport (d := d) U hU*T=T) :
    U^d*T=((-1 : ℂ)^(d-1)) • T := by
  have h := equality_supported_action hd U hU T hE (fun z => z^d)
    (fun _ => (-1 : ℂ)^(d-1)) (equalityRoot_power hd)
  rw [finiteCalc_pow, finiteCalc_const] at h
  change (finiteCalc U hU id)^d*T = _ at h
  rw [finiteCalc_coordinate] at h
  simpa only [Matrix.smul_mul,Matrix.one_mul] using h

theorem halfRoot_times_phase (z : ℂ) :
    squareRootNorm z*(z/(‖z‖ : ℂ))=continuousPolarRoot z := by
  by_cases hz : z=0
  · simp [hz]
  · have hs : squareRootNorm z≠0 := squareRootNorm_ne_zero hz
    have hn : (‖z‖ : ℂ)≠0 := by exact_mod_cast (norm_ne_zero_iff.mpr hz)
    have hsq := squareRootNorm_square z
    have hstar : star (squareRootNorm z)=squareRootNorm z := by simp [squareRootNorm]
    rw [hstar] at hsq
    unfold continuousPolarRoot
    field_simp
    linear_combination z*hsq

theorem localH_phase (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) :
    localH U hU y*supportedPhase U hU y=localK U hU y := by
  unfold localH supportedPhase localK scalarPolarPhase
  rw [← finiteCalc_mul]
  exact finiteCalc_congr U hU (fun z => halfRoot_times_phase _)

def supportedHalfInverse (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) : Mat ι :=
  finiteCalc U hU (fun z => if z^d=(-1 : ℂ)^(d-1) then (squareRootNorm (1+chi y*z))⁻¹ else 0)

theorem supportedHalfInverse_cancel (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U) (y : Ix d) :
    supportedHalfInverse U hU y*localH U hU y=equalitySupport (d := d) U hU := by
  unfold supportedHalfInverse localH equalitySupport
  rw [← finiteCalc_mul]
  apply finiteCalc_congr U hU
  intro z
  by_cases hz : (z : ℂ)^d=(-1 : ℂ)^(d-1)
  · have hn := squareRootNorm_ne_zero
      (good_phase_nonzero hd y z (spectrum_unit_norm (toCMatrix_unitary hU) z) hz)
    simp [equalityIndicator,hz,hn]
  · simp [equalityIndicator,hz]

theorem phase_square_on_support (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (hE : equalitySupport (d := d) U hU*T=T) (y : Ix d) :
    supportedPhase U hU y^2*T=chi y • (U*T) := by
  have h := equality_supported_action hd U hU T hE
    (fun z => scalarPolarPhase y z^2) (fun z => chi y*z)
    (fun k => by dsimp only; rw [scalarPolarPhase_at_root hd,polarPhase_square])
  have hf : finiteCalc U hU (fun z => chi y*z)=chi y • U := by
    change finiteCalc U hU (fun z => chi y*id z)=chi y • U
    rw [finiteCalc_smul,finiteCalc_coordinate]
  rw [finiteCalc_pow,hf] at h
  simpa only [supportedPhase, Matrix.smul_mul] using h

theorem phase_isometry_on_support (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (hE : equalitySupport (d := d) U hU*T=T) (y : Ix d) :
    (supportedPhase U hU y).conjTranspose*supportedPhase U hU y*T=T := by
  have h := equality_supported_action hd U hU T hE
    (fun z => star (scalarPolarPhase y z)*scalarPolarPhase y z) (fun _ => 1)
    (fun k => by dsimp only; rw [scalarPolarPhase_at_root hd]; exact polarPhase_unit y k)
  simpa only [supportedPhase,finiteCalc_mul,finiteCalc_star,finiteCalc_one,Matrix.one_mul] using h

/-- This is the missing polar-kernel cancellation step, with its support
premises derived in the subsequent quantum theorem. -/
theorem polar_cancel_on_support (hd : 2≤d) (A U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (D B : Mat ν) (y : Ix d)
    (hE : equalitySupport (d := d) U hU*T=T) (hA : A.conjTranspose*T=T*D)
    (hP : localH U hU y*A.conjTranspose*T=localK U hU y*T*B) :
    A.conjTranspose*T=supportedPhase U hU y*T*B := by
  let Q := A.conjTranspose*T-supportedPhase U hU y*T*B
  have hHQ : localH U hU y*Q=0 := by
    unfold Q
    simp only [Matrix.mul_sub,← Matrix.mul_assoc,localH_phase,hP,sub_self]
  have hEQ : equalitySupport (d := d) U hU*Q=Q := by
    unfold Q
    rw [Matrix.mul_sub,hA,← Matrix.mul_assoc _ T D,hE]
    have hc := finiteCalc_commute U hU (equalityIndicator d) (scalarPolarPhase y)
    change equalitySupport (d := d) U hU*supportedPhase U hU y=supportedPhase U hU y*equalitySupport (d := d) U hU at hc
    simp only [← Matrix.mul_assoc]
    rw [hc,Matrix.mul_assoc (supportedPhase U hU y) (equalitySupport (d := d) U hU) T,hE]
  exact sub_eq_zero.mp (supported_kernel_cancel _ _ _ Q
    (supportedHalfInverse_cancel hd U hU y) hEQ hHQ)

theorem matrix_intertwiner_pow (A : Mat ι) (T : Matrix ι ν ℂ) (B : Mat ν)
    (h : A*T=T*B) (n : ℕ) : A^n*T=T*B^n := by
  induction n with
  | zero => simp
  | succ n ih => rw [pow_succ',Matrix.mul_assoc,ih,← Matrix.mul_assoc,h,Matrix.mul_assoc,pow_succ']

/-- From the actual saturated strategy to supported unitary routing equations.
The R_y on the right are Bob's genuine transpose-lifted observables. -/
theorem quantum_supported_routing (hd : 2≤d)
    {κ : Type*} [Fintype κ] [DecidableEq κ]
    (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ)
    (hs : firstValue s=scalarMaximum d+1) :
    let A := encoded (s.alice 0)
    let U := A.conjTranspose*encoded (s.alice 1)
    let hU := (encoded_unitary (s.alice 0)).adjoint.mul (encoded_unitary (s.alice 1))
    let T := aliceAmplitude (stateFactor s.state)
    let D := bobRight (ε := ι × κ) (encoded (s.bob none))
    let B := fun y : Ix d => bobRight (ε := ι × κ) (encoded (s.bob (some y)))
    equalitySupport (d := d) U hU*T=T ∧
    A.conjTranspose*T=T*D ∧
    (∀ y,supportedPhase U hU y*T=T*(D*(B y).conjTranspose)) ∧
    (∀ y,(A*supportedPhase U hU y)*T=T*(B y).conjTranspose) ∧
    U*T=T*(D*(B 0).conjTranspose)^2 := by
  dsimp only
  let A := encoded (s.alice 0)
  let U := A.conjTranspose*encoded (s.alice 1)
  let hA := encoded_unitary (s.alice 0)
  let hU := hA.adjoint.mul (encoded_unitary (s.alice 1))
  let T := aliceAmplitude (stateFactor s.state)
  let D := bobRight (ε := ι × κ) (encoded (s.bob none))
  let B := fun y : Ix d => bobRight (ε := ι × κ) (encoded (s.bob (some y)))
  have hD : UnitaryRel D := bobRight_unitary (encoded_unitary _)
  have hB (y : Ix d) : UnitaryRel (B y) := bobRight_unitary (encoded_unitary _)
  obtain ⟨hG,hAD,hP⟩ := first_saturation_equations hd s hs
  have hE : equalitySupport (d := d) U hU*T=T := equalitySupport_from_gap hd U hU T hG
  change A*T*D=T at hAD
  have hAT : A.conjTranspose*T=T*D := by
    have h := congrArg (fun Q : Matrix ι (κ × (ι × κ)) ℂ => A.conjTranspose*Q) hAD
    have haa : A.conjTranspose*A=1 := hA.1
    simpa only [← Matrix.mul_assoc,haa,Matrix.one_mul] using h.symm
  have hS (y : Ix d) : supportedPhase U hU y*T=T*(D*(B y).conjTranspose) := by
    have hc := polar_cancel_on_support hd A U hU T D (B y) y hE hAT (hP y)
    have h := congrArg (fun Q : Matrix ι (κ × (ι × κ)) ℂ => Q*(B y).conjTranspose) hc
    simpa [Matrix.mul_assoc,(hB y).2,hAT] using h.symm
  have hV (y : Ix d) : (A*supportedPhase U hU y)*T=T*(B y).conjTranspose := by
    rw [Matrix.mul_assoc,hS,← Matrix.mul_assoc,← Matrix.mul_assoc,hAD]
  refine ⟨hE,hAT,hS,hV,?_⟩
  have hp := phase_square_on_support hd U hU T hE 0
  simp only [chi_zero,one_smul] at hp
  rw [← hp,matrix_intertwiner_pow _ T _ (hS 0) 2]

/-- Adjacent polar ratios produce an actual reflection on the state support. -/
theorem supported_adjacent_reflection (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (hE : equalitySupport (d := d) U hU*T=T) (y : Ix d) :
    supportedPhase U hU (y+1)*T=
      cis (Real.pi/(d : ℝ)) •
        (supportedPhase U hU y*(1-2 • rootProjection U hU (reflectionLabel d-y))*T) := by
  have h := equality_supported_action hd U hU T hE
    (scalarPolarPhase (y+1))
    (fun z => cis (Real.pi/(d : ℝ))*scalarPolarPhase y z*
      (1-2*(if z=equalityRoot (reflectionLabel d-y) then 1 else 0))) (fun k => ?_)
  · simpa only [supportedPhase,rootProjection,finiteSpectralProjection,finiteCalc_mul,finiteCalc_smul,finiteCalc_sub,finiteCalc_one,finiteCalc_const,Matrix.smul_mul,smul_mul_assoc,mul_smul_comm,Matrix.one_mul,two_smul,add_mul,one_mul] using h
  · dsimp only
    rw [scalarPolarPhase_at_root hd,scalarPolarPhase_at_root hd,
      polarPhase_adjacent hd]
    simp only [equalityRoot_injective.eq_iff]
    split_ifs <;> ring

end CyclicBell.General
