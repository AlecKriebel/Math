import CyclicBell.GeneralSecondWitness
import CyclicBell.Guessing

/-! Operational bridges: actual measurement sandwiches and partial traces,
arbitrary-d trivial Eve, value-only nonrobustness, and private-MUB composition.
The partial trace is defined entrywise, not by assuming the desired privacy
condition. Every statement below is an UNCOMPILED SOURCE CANDIDATE. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι κ ε : Type*} [Fintype ι] [Fintype κ] [Fintype ε]
  [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]

def reducedE (T : Matrix ι ε ℂ) : Mat ε := T.transpose*T.map star

def partialE (R : Mat (ι×ε)) : Mat ε := fun e f => ∑ i,R (i,e) (i,f)

def conditionalE (T : Matrix ι ε ℂ) (X : Mat ι) : Mat ε := reducedE (X*T)

def effectKernelE (T : Matrix ι ε ℂ) (X : Mat ι) : Mat ε :=
  T.transpose*X.transpose*T.map star

/-- T contains the actual coefficients Psi(i,e). Its reduction is the partial
trace of |Psi><Psi|, including conjugation in the second density index. -/
theorem reducedE_partialTrace (T : Matrix ι ε ℂ) :
    reducedE T=partialE (projector (fun p : ι×ε => T p.1 p.2)) := by
  ext e f
  simp [reducedE,partialE,Matrix.mul_apply,projector,Matrix.transpose_apply,Matrix.map_apply]

theorem reducedE_positive (T : Matrix ι ε ℂ) : (reducedE T).PosSemidef := by
  have he : reducedE T=(T.map star).conjTranspose*(T.map star) := by
    congr 1; ext i e; simp [Matrix.conjTranspose_apply,Matrix.map_apply]
  rw [he]
  exact Matrix.posSemidef_conjTranspose_mul_self _

theorem conditionalE_actual_sandwich (T : Matrix ι ε ℂ) (X : Mat ι) :
    conditionalE T X=partialE
      (kron X (1 : Mat ε)*projector (fun p : ι×ε => T p.1 p.2)*
        (kron X (1 : Mat ε)).conjTranspose) := by
  rw [conditionalE,reducedE_partialTrace]
  congr 1
  ext ⟨i,e⟩ ⟨j,f⟩
  simp [Matrix.mul_apply,kron,projector,Matrix.conjTranspose_apply,
    Fintype.sum_prod_type,Finset.sum_mul,Finset.mul_sum,star_sum,star_mul]
  ring

theorem conditionalE_effectKernel (T : Matrix ι ε ℂ) (X : Mat ι)
    (hX : X.IsHermitian) (hXX : X*X=X) : conditionalE T X=effectKernelE T X := by
  have hconj : X.map star=X.transpose := by
    ext i j
    have h := congrFun (congrFun hX.eq j) i
    simpa [Matrix.conjTranspose_apply] using h
  unfold conditionalE reducedE effectKernelE
  rw [Matrix.transpose_mul,Matrix.map_mul,← mul_assoc,hconj]
  have hp : X.transpose*X.transpose=X.transpose := by
    simpa only [Matrix.transpose_mul] using congrArg Matrix.transpose hXX
  simp only [mul_assoc,hp]

theorem effectKernelE_on_state (T : Matrix ι ε ℂ) (X Y : Mat ι) (h : X*T=Y*T) :
    effectKernelE T X=effectKernelE T Y := by
  have ht := congrArg Matrix.transpose h
  simpa only [effectKernelE,Matrix.transpose_mul] using congrArg (fun S => S*T.map star) ht

theorem effectKernelE_smul (T : Matrix ι ε ℂ) (c : ℂ) (X : Mat ι) :
    effectKernelE T (c • X)=c • effectKernelE T X := by
  simp [effectKernelE,Matrix.transpose_smul,mul_smul_comm,smul_mul_assoc]

/-- Algebraic form of the actual private-MUB composition. T is the genuine
purification coefficient matrix across AB:E. P,R,Q are the lifted projectors.
The matching and sandwich hypotheses are only ON STATE; no full-space MUB
identity or same-party commutation is assumed. -/
theorem privateMUB_sandwich (T : Matrix ι ε ℂ) (P R Q : Mat ι) (c : ℝ)
    (hP : P.IsHermitian) (hR : R.IsHermitian) (hQ : Q.IsHermitian)
    (hp : P*P=P) (hr : R*R=R) (hq : Q*Q=Q) (hRQ : R*Q=Q*R)
    (hmatch : Q*T=P*T) (hsandwich : (P*R*P)*T=(c : ℂ) • (P*T)) :
    conditionalE T (R*Q)=(c : ℂ) • conditionalE T P := by
  have he : (R*Q)*T=R*(P*T) := by rw [mul_assoc,hmatch]
  have htranspose : P.map star=P.transpose := by
    ext i j; have hh := congrFun (congrFun hP.eq j) i
    simpa [Matrix.conjTranspose_apply] using hh
  have htransposeR : R.map star=R.transpose := by
    ext i j; have hh := congrFun (congrFun hR.eq j) i
    simpa [Matrix.conjTranspose_apply] using hh
  have hred : conditionalE T (R*Q)=effectKernelE T (P*R*P) := by
    unfold conditionalE reducedE effectKernelE
    rw [he]
    simp only [Matrix.transpose_mul,Matrix.map_mul,htranspose,htransposeR]
    have hRR : R.transpose*R.transpose=R.transpose := by
      simpa only [Matrix.transpose_mul] using congrArg Matrix.transpose hr
    simp only [mul_assoc,hRR]
  rw [hred,conditionalE_effectKernel T P hP hp]
  have hc : (P*R*P)*T=((c : ℂ) • P)*T := by simpa [smul_mul_assoc] using hsandwich
  rw [effectKernelE_on_state T _ _ hc,effectKernelE_smul]

/-- Manuscript lem:private-mub, with the quantum grouping AB:E explicit.
The caller provides exactly the private-reference, matching, and supported-MUB
hypotheses from the paper. No target privacy premise is present. -/
theorem privateMUB_composition (T : Matrix (ι×κ) ε ℂ)
    (P R : Measurement d ι) (Q : Measurement d κ) (π : Equiv.Perm (Ix d))
    (hprivate : ∀ b,conditionalE T (aliceLift (κ := κ) (P.effect b))=
      ((d : ℂ)⁻¹) • reducedE T)
    (hmatch : ∀ b,bobLift (ι := ι) (Q.effect (π b))*T=aliceLift (κ := κ) (P.effect b)*T)
    (hmub : ∀ a b,aliceLift (κ := κ) (P.effect b*R.effect a*P.effect b)*T=
      ((d : ℂ)⁻¹) • (aliceLift (κ := κ) (P.effect b)*T)) :
    ∀ a b,conditionalE T (kron (R.effect a) (Q.effect (π b)))=
      ((d : ℂ)⁻¹)^2 • reducedE T := by
  intro a b
  have h := privateMUB_sandwich T
    (aliceLift (κ := κ) (P.effect b)) (aliceLift (κ := κ) (R.effect a))
    (bobLift (ι := ι) (Q.effect (π b))) ((d : ℝ)⁻¹)
    (by simp [aliceLift,kron_star,(P.positive b).isHermitian.eq])
    (by simp [aliceLift,kron_star,(R.positive a).isHermitian.eq])
    (by simp [bobLift,kron_star,(Q.positive (π b)).isHermitian.eq])
    (by simp [aliceLift,P.idempotent]) (by simp [aliceLift,R.idempotent])
    (by simp [bobLift,Q.idempotent]) (lift_commute _ _) (hmatch b)
    (by simpa [aliceLift,kron_mul] using hmub a b)
  rw [lift_product,hprivate b,smul_smul] at h
  simpa [pow_two] using h

/-- A fixed guess, represented by a genuine d²-outcome PVM on C¹. -/
def fixedGuessEffect (g : Ix d×Ix d) (a b : Ix d) : Op 1 := if (a,b)=g then 1 else 0

theorem fixedGuess_positive (g : Ix d×Ix d) (a b : Ix d) :
    (fixedGuessEffect g a b).PosSemidef := by
  unfold fixedGuessEffect
  split_ifs <;> first | exact Matrix.PosSemidef.one | exact Matrix.PosSemidef.zero

theorem fixedGuess_complete (g : Ix d×Ix d) : (∑ a,∑ b,fixedGuessEffect g a b)=1 := by
  classical
  rcases g with ⟨a,b⟩
  simp [fixedGuessEffect,Prod.mk.injEq]

def fixedGuessSuccess (ρ : Mat (ι×κ)) (M : Measurement d ι) (N : Measurement d κ)
    (g : Ix d×Ix d) : ℝ :=
  ∑ a,∑ b,(Matrix.trace (fixedGuessEffect g a b *
    CyclicBell.actualTrivialConditional ρ (kron (M.effect a) (N.effect b)))).re

theorem general_trivialEve_instrument (ρ : StateOn (ι×κ)) (M : Measurement d ι)
    (N : Measurement d κ) (a b : Ix d) :
    CyclicBell.actualTrivialConditional ρ.density (kron (M.effect a) (N.effect b))=
      (bornProbability ρ.density (M.effect a) (N.effect b) : ℂ) • (1 : Op 1) := by
  apply CyclicBell.actualTrivialConditional_eq ρ.positive.isHermitian
  · simp [Matrix.IsHermitian,kron_star,(M.positive a).isHermitian.eq,(N.positive b).isHermitian.eq]
  · simp only [kron_mul,M.idempotent,N.idempotent]

theorem fixedGuessSuccess_eq (ρ : StateOn (ι×κ)) (M : Measurement d ι)
    (N : Measurement d κ) (g : Ix d×Ix d) :
    fixedGuessSuccess ρ.density M N g=bornProbability ρ.density (M.effect g.1) (N.effect g.2) := by
  classical
  rcases g with ⟨a,b⟩
  unfold fixedGuessSuccess
  simp_rw [general_trivialEve_instrument]
  simp [fixedGuessEffect,Prod.mk.injEq,Matrix.trace,Fin.sum_univ_succ]

theorem first_all_dimension_physical_Eve_gap (hd : 4≤d) :
    let s := firstPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
    firstValue s=scalarMaximum d+1 ∧
    ∃ g : Ix d×Ix d,1/(d : ℝ)^2<fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g := by
  dsimp
  refine ⟨firstPermutation_attains (by omega) _,?_⟩
  obtain ⟨a,b,h⟩ := swappedTarget_quantitative (d := d) hd
  refine ⟨(a,b),?_⟩
  rw [fixedGuessSuccess_eq]
  change 1/(d : ℝ)^2<behavior (firstPermutationStrategy (by omega) (finalSwap d)) 1 none a b
  rw [firstSwap_target hd]
  exact (quantitative_gap_positive hd).trans_le h

/-- An exact positive gap precludes any deficit-only upper bound tending to
zero. This formulation explicitly tests ALL epsilon>0, not just epsilon=0. -/
theorem no_endpoint_modulus (u g : ℝ) (hgap : u<g) (f : ℝ → ℝ)
    (hf : Filter.Tendsto f (nhdsWithin 0 (Set.Ioi 0)) (nhds 0)) :
    ¬ (∀ ε : ℝ,0<ε → g≤u+f ε) := by
  intro hbound
  have hh : ∀ᶠ ε in nhdsWithin 0 (Set.Ioi 0),f ε<(g-u)/2 :=
    hf.eventually (gt_mem_nhds (by linarith))
  have hpos : ∀ᶠ ε in nhdsWithin 0 (Set.Ioi 0),0<ε :=
    self_mem_nhdsWithin
  haveI : NeBot (nhdsWithin (0 : ℝ) (Set.Ioi 0)) := by infer_instance
  obtain ⟨ε,hε,hsmall⟩ := (hpos.and hh).exists
  have hb := hbound ε hε
  linarith

end CyclicBell.General
