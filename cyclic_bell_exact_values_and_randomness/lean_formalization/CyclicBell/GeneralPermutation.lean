import CyclicBell.GeneralFirstBound
import CyclicBell.GeneralCycles

/-! The manuscript's CONDITIONAL polar-linear phase-permutation theorem.
The scalar cap, phase alignment and cyclic products below are exactly the
conditional hypotheses of thm:permutation. They are not hypotheses in a
physical Strategy. The upper bound still quantifies over arbitrary local
finite dimensions. Zero linear factors are permitted.  -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {R : Type*} [Fintype R]
variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

def linearScalar (α β : R → ℂ) (z : ℂ) : ℝ := ∑ r, ‖α r+β r*z‖

def linearOperator (α β : R → ℂ) (A U : Mat ι) (B : R → Mat ι) : Mat ι :=
  ∑ r, herm (A*(α r • 1+β r • U)*B r)

def linearValue (α β : R → ℂ)
    (s : StrategyOn d (Fin 2) (Option R) ι κ) : ℝ :=
  (∑ r,stateEval s.state.density (kron
    (α r • encoded (s.alice 0)+β r • encoded (s.alice 1)) (encoded (s.bob (some r)))))+
  stateEval s.state.density (kron (encoded (s.alice 0)) (encoded (s.bob none)))

def linearModulusCM (U : Mat ι) (α β : ℂ) : C(spectrum ℂ (toCMatrix U),ℂ) :=
  ⟨fun z => (‖α+β*(z : ℂ)‖ : ℂ),by fun_prop⟩
def linearRootCM (U : Mat ι) (α β : ℂ) : C(spectrum ℂ (toCMatrix U),ℂ) :=
  ⟨fun z => squareRootNorm (α+β*(z : ℂ)),squareRootNorm_continuous.comp (by fun_prop)⟩
def linearPolarRootCM (U : Mat ι) (α β : ℂ) : C(spectrum ℂ (toCMatrix U),ℂ) :=
  ⟨fun z => continuousPolarRoot (α+β*(z : ℂ)),continuousPolarRoot_continuous.comp (by fun_prop)⟩
def linearGapCM (U : Mat ι) (α β : R → ℂ) (M : ℝ) : C(spectrum ℂ (toCMatrix U),ℂ) :=
  ⟨fun z => (Real.sqrt (M-linearScalar α β (z : ℂ)) : ℂ),by unfold linearScalar; fun_prop⟩

theorem linear_factor_relations (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M)
    (U : Mat ι) (B : R → Mat ι) (hU : UnitaryRel U)
    (hB : ∀ r,UnitaryRel (B r)) (hc : ∀ r,U*B r=B r*U) :
    ∃ H K D : R → Mat ι, ∃ G : Mat ι,
      (∀ r,(H r).conjTranspose*H r=D r) ∧
      (∀ r,(K r).conjTranspose*K r=D r) ∧
      (∀ r,(H r).conjTranspose*K r=α r • 1+β r • U) ∧
      (∀ r,D r*B r=B r*D r) ∧
      G.conjTranspose*G=(M : ℂ) • 1-∑ r,D r := by
  let φ := matrixCfc U hU
  refine ⟨(fun r => φ (linearRootCM U (α r) (β r))),
    (fun r => φ (linearPolarRootCM U (α r) (β r))),
    (fun r => φ (linearModulusCM U (α r) (β r))),φ (linearGapCM U α β M),?_,?_,?_,?_,?_⟩
  · intro r
    have h : star (linearRootCM U (α r) (β r))*linearRootCM U (α r) (β r)=
        linearModulusCM U (α r) (β r) := by ext z; exact squareRootNorm_square _
    simpa only [map_star,map_mul,Matrix.star_eq_conjTranspose] using congrArg φ h
  · intro r
    have h : star (linearPolarRootCM U (α r) (β r))*linearPolarRootCM U (α r) (β r)=
        linearModulusCM U (α r) (β r) := by ext z; exact continuousPolarRoot_square _
    simpa only [map_star,map_mul,Matrix.star_eq_conjTranspose] using congrArg φ h
  · intro r
    have h : star (linearRootCM U (α r) (β r))*linearPolarRootCM U (α r) (β r)=
        α r • 1+β r • ((ContinuousMap.id ℂ).restrict (spectrum ℂ (toCMatrix U))) := by
      ext z
      simpa only [linearRootCM, linearPolarRootCM, ContinuousMap.mul_apply,
        ContinuousMap.star_apply, ContinuousMap.smul_apply, ContinuousMap.add_apply,
        ContinuousMap.one_apply, ContinuousMap.coe_mk, ContinuousMap.restrict_apply,
        ContinuousMap.id_apply, smul_eq_mul, mul_one] using continuousPolarRoot_cross (α r+β r*(z : ℂ))
    simpa only [map_star,map_mul,map_add,map_smul,map_one,φ,matrixCfc_coordinate,
      Matrix.star_eq_conjTranspose] using congrArg φ h
  · intro r
    exact matrixCfc_commute U (B r) hU (hB r) (hc r) _
  · have h : star (linearGapCM U α β M)*linearGapCM U α β M=
        (M : ℂ) • 1-∑ r,linearModulusCM U (α r) (β r) := by
      ext z
      have hp := sub_nonneg.mpr (hcap z (spectrum_unit_norm (toCMatrix_unitary hU) z))
      change star ((Real.sqrt (M-linearScalar α β (z : ℂ)) : ℝ) : ℂ) *
        ((Real.sqrt (M-linearScalar α β (z : ℂ)) : ℝ) : ℂ) = _
      simp only [Complex.star_def,Complex.conj_ofReal,← Complex.ofReal_mul,Real.mul_self_sqrt hp]
      simp [linearScalar,linearModulusCM,Complex.ofReal_sub,Complex.ofReal_sum]
    simpa only [map_star,map_mul,map_sub,map_smul,map_one,map_sum,
      Matrix.star_eq_conjTranspose] using congrArg φ h

theorem linear_matrix_sos (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M)
    (A U : Mat ι) (B : R → Mat ι) (hA : UnitaryRel A) (hU : UnitaryRel U)
    (hB : ∀ r,UnitaryRel (B r)) (hc : ∀ r,U*B r=B r*U) :
    ∃ (P : R → Mat ι) (G : Mat ι),
      (M : ℂ) • 1-linearOperator α β A U B=
        (1/2 : ℂ) • (∑ r,(P r).conjTranspose*P r)+
        (1/2 : ℂ) • (G.conjTranspose*G)+
        (1/2 : ℂ) • ((G*A.conjTranspose).conjTranspose*(G*A.conjTranspose)) := by
  obtain ⟨H,K,D,G,hH,hK,hHK,hDB,hG⟩ := linear_factor_relations α β M hcap U B hU hB hc
  refine ⟨(fun r => halfPolarResidual A (H r) (K r) (B r)),G,?_⟩
  simp_rw [halfPolar_gap_identity A _ _ _ _ _ (hH _) (hK _) (hHK _) (hB _) (hDB _)]
  have hgA : (G*A.conjTranspose).conjTranspose*(G*A.conjTranspose)=
      A*(G.conjTranspose*G)*A.conjTranspose := by simp [Matrix.conjTranspose_mul,mul_assoc]
  rw [hgA,hG]
  unfold linearOperator herm
  simp only [Finset.sum_sub_distrib,Finset.sum_add_distrib,← Finset.sum_mul,
    ← Finset.mul_sum,mul_sub,sub_mul,mul_smul_comm,smul_mul_assoc,one_mul,mul_one,hA.2,
    Finset.smul_sum,smul_sub,smul_add]
  ext i j
  simp only [Matrix.sub_apply,Matrix.add_apply,Matrix.smul_apply,smul_eq_mul,Finset.sum_apply]
  ring

theorem linear_matrix_upper (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M) (ρ : StateOn ι)
    (A U : Mat ι) (B : R → Mat ι) (hA : UnitaryRel A) (hU : UnitaryRel U)
    (hB : ∀ r,UnitaryRel (B r)) (hc : ∀ r,U*B r=B r*U) :
    stateEval ρ.density (linearOperator α β A U B)≤M := by
  obtain ⟨P,G,h⟩ := linear_matrix_sos α β M hcap A U B hA hU hB hc
  have hp : 0≤stateEval ρ.density (∑ r,(P r).conjTranspose*P r) := by
    rw [stateEval_sum]
    exact Finset.sum_nonneg (fun r _ => stateEval_square_nonnegative ρ.positive _)
  have hg := stateEval_square_nonnegative ρ.positive G
  have hga := stateEval_square_nonnegative ρ.positive (G*A.conjTranspose)
  have he := congrArg (stateEval ρ.density) h
  rw [stateEval_sub,stateEval_real_smul,stateEval_one ρ.normalized] at he
  have half : (1/2 : ℂ)=((1/2 : ℝ) : ℂ) := by norm_num
  simp only [half,stateEval_add,stateEval_real_smul] at he
  linarith

theorem linear_physical_upper (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M)
    (s : StrategyOn d (Fin 2) (Option R) ι κ) : linearValue α β s≤M+1 := by
  let A := encoded (s.alice 0)
  let C := encoded (s.alice 1)
  let U := A.conjTranspose*C
  have hA : UnitaryRel A := encoded_unitary _
  have hC : UnitaryRel C := encoded_unitary _
  have hU : UnitaryRel U := hA.adjoint.mul hC
  have h := linear_matrix_upper α β M hcap s.state (aliceLift (κ := κ) A)
    (aliceLift (κ := κ) U) (fun r => bobLift (ι := ι) (encoded (s.bob (some r))))
    (kron_unitary hA UnitaryRel.one) (kron_unitary hU UnitaryRel.one)
    (fun r => kron_unitary UnitaryRel.one (encoded_unitary _)) (fun r => lift_commute _ _)
  have he (r : R) : aliceLift (κ := κ) A*(α r • 1+β r • aliceLift U)*
      bobLift (ι := ι) (encoded (s.bob (some r)))=
        kron (α r • A+β r • C) (encoded (s.bob (some r))) := by
    simp only [aliceLift,bobLift,← kron_one,← kron_smul_left,← kron_add_left,kron_mul,
      mul_add,mul_smul_comm,mul_one,one_mul]
    congr 1
    rw [hA.cancel_right]
  unfold linearOperator at h
  simp_rw [he] at h
  rw [stateEval_sum] at h
  simp_rw [stateEval_herm _ _ s.state.positive.isHermitian] at h
  have ha := aligned_upper s.state.positive s.state.normalized
    (kron_unitary hA (encoded_unitary (s.bob none)))
  exact add_le_add h ha

/-- These data are the explicit conditional phase hypotheses, not validity of
an arbitrary quantum strategy and not a definition of maximality. -/
structure PermutationData (d : ℕ) [NeZero d] (R : Type*) [Fintype R]
    (α β : R → ℂ) (M : ℝ) where
  z : Ix d → ℂ
  s : R → Ix d → ℂ
  z_unit : UnitPhases z
  s_unit : ∀ r,UnitPhases (s r)
  z_product : ∏ j,z j=1
  s_product : ∀ r,∏ j,s r j=1
  phase_alignment : ∀ r j,s r j*(‖α r+β r*z j‖ : ℂ)=α r+β r*z j
  equality : ∀ j,linearScalar α β (z j)=M

def linearPermutationAlice {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) (x : Fin 2) : Measurement d (Ix d) :=
  if x=0 then fourierMeasurement d else cycleMeasurement (p.z ∘ σ)
    (phases_permuted _ p.z_unit σ) (by simpa only [Function.comp_apply,product_permuted] using p.z_product)

def linearPermutationBob {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) : Option R → Measurement d (Ix d)
  | none => fourierMeasurement d
  | some r => cycleMeasurement (fun j => star (p.s r (σ j)))
      (by intro j; simpa [mul_comm] using p.s_unit r (σ j))
      (by rw [product_permuted (fun j => star (p.s r j)) σ]
          simpa only [star_prod,star_one] using congrArg star (p.s_product r))

def linearPermutationStrategy {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) :
    StrategyOn d (Fin 2) (Option R) (Ix d) (Ix d) where
  state := entangledState d
  alice := linearPermutationAlice p σ
  bob := linearPermutationBob p σ

theorem aligned_phase_conjugate {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (r : R) (j : Ix d) :
    (α r+β r*p.z j)*star (p.s r j)=(‖α r+β r*p.z j‖ : ℂ) := by
  calc
    (α r+β r*p.z j)*star (p.s r j) =
      p.s r j*(‖α r+β r*p.z j‖ : ℂ)*star (p.s r j) := by rw [p.phase_alignment]
    _ = (star (p.s r j)*p.s r j)*(‖α r+β r*p.z j‖ : ℂ) := by ring
    _ = _ := by rw [p.s_unit r j,one_mul]

theorem linear_permutation_encodings {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) :
    encoded (linearPermutationAlice p σ 0)=cyclicShift d ∧
    encoded (linearPermutationAlice p σ 1)=weightedCycle (p.z ∘ σ) ∧
    encoded (linearPermutationBob p σ none)=cyclicShift d ∧
    (∀ r,encoded (linearPermutationBob p σ (some r))=
      entryConjugate (weightedCycle (p.s r ∘ σ))) := by
  simp only [linearPermutationAlice,show (0 : Fin 2)=0 from rfl,if_true,
    show (1 : Fin 2)≠0 by decide,if_false,linearPermutationBob,
    fourierMeasurement_encoding,cycleMeasurement_encoding,weighted_entry_conjugate]
  exact ⟨trivial,trivial,trivial,fun _ => rfl⟩

theorem linear_permutation_attains {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) :
    linearValue α β (linearPermutationStrategy p σ)=M+1 := by
  obtain ⟨h0,h1,hb,hbr⟩ := linear_permutation_encodings p σ
  have hv (T : Mat (Ix d × Ix d)) : stateEval (entangledState d).density T=
      (expectation (maximallyEntangled d) T).re :=
    congrArg Complex.re (expectation_eq_trace (maximallyEntangled d) T).symm
  have hw (r : R) : α r • cyclicShift d + β r • weightedCycle (p.z ∘ σ) =
      weightedCycle (fun j => α r + β r * p.z (σ j)) := by
    simpa only [cyclicShift,mul_one,Function.comp_apply] using
      weighted_linear (fun _ : Ix d => (1 : ℂ)) (p.z ∘ σ) (α r) (β r)
  unfold linearValue linearPermutationStrategy
  simp only [h0,h1,hb,hbr,hv,weighted_entry_conjugate,hw,phi_weighted,
    Function.comp_apply,aligned_phase_conjugate p]
  rw [(added_first_harmonics p.z σ).1,Complex.one_re]
  have hs : (∑ r : R,(∑ j : Ix d, (‖α r+β r*p.z (σ j)‖ : ℂ))/(d : ℂ))=(M : ℂ) := by
    rw [← Finset.sum_div,Finset.sum_comm]
    have he (j : Ix d) : (∑ r : R,(‖α r+β r*p.z (σ j)‖ : ℂ))=(M : ℂ) := by
      exact_mod_cast p.equality (σ j)
    simp_rw [he]
    simp only [Finset.sum_const,Finset.card_univ,ZMod.card,nsmul_eq_mul]
    have hdC : (d : ℂ) ≠ 0 := by exact_mod_cast NeZero.ne d
    field_simp
  rw [← Complex.re_sum,hs,Complex.ofReal_re]

theorem linear_permutation_harmonics {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) (r : R) :
    expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ 0)) (encoded (linearPermutationBob p σ (some r))))=
        (∑ j,star (p.s r j))/(d : ℂ) ∧
    expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ 1)) (encoded (linearPermutationBob p σ (some r))))=
        (∑ j,p.z j*star (p.s r j))/(d : ℂ) := by
  obtain ⟨h0,h1,_,hb⟩ := linear_permutation_encodings p σ
  rw [h0,h1,hb]
  exact first_harmonic_permutation p.z (p.s r) σ

/-- Conditional theorem matching the sufficient hypotheses in the manuscript.
It is not asserted to classify every maximizer. -/
theorem conditional_permutation_theorem (hd : 2≤d) (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M)
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) :
    linearValue α β (linearPermutationStrategy p σ)=M+1 ∧
    (∀ nA nB : ℕ,∀ t : StrategyOn d (Fin 2) (Option R) (Fin nA) (Fin nB),
      linearValue α β t≤linearValue α β (linearPermutationStrategy p σ)) ∧
    (∀ r,expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ 0)) (encoded (linearPermutationBob p σ (some r))))=
        (∑ j,star (p.s r j))/(d : ℂ)) := by
  refine ⟨linear_permutation_attains p σ,?_,fun r => (linear_permutation_harmonics p σ r).1⟩
  intro nA nB t
  rw [linear_permutation_attains]
  exact linear_physical_upper α β M hcap t

end CyclicBell.General
