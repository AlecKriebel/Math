import CyclicBell.GeneralBinary
import CyclicBell.GeneralExposure
import CyclicBell.GeneralOneInput

/-! Physical Fourier privacy, value-only counterexamples and exact entropy
arithmetic. These are source candidates, with explicit guesses and no claim of
optimal adversarial success over the whole maximizing face. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι κ ε : Type*} [Fintype ι] [Fintype κ] [Fintype ε]
  [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]

def jointInstrument (T : Matrix (ι×κ) ε ℂ) (M : Measurement d ι) (N : Measurement d κ)
    (a b : Ix d) : Mat ε := conditionalE T (kron (M.effect a) (N.effect b))

theorem effectKernelE_sum {J : Type*} [Fintype J] (T : Matrix ι ε ℂ) (X : J → Mat ι) :
    effectKernelE T (∑ j,X j)=∑ j,effectKernelE T (X j) := by
  simp [effectKernelE,Matrix.transpose_sum,Finset.mul_sum,Finset.sum_mul]

theorem jointInstrument_total (T : Matrix (ι×κ) ε ℂ) (M : Measurement d ι) (N : Measurement d κ) :
    (∑ a,∑ b,jointInstrument T M N a b)=reducedE T := by
  have he (a b : Ix d) : jointInstrument T M N a b=effectKernelE T (kron (M.effect a) (N.effect b)) := by
    apply conditionalE_effectKernel
    · simp [Matrix.IsHermitian,kron_star,(M.positive a).isHermitian.eq,(N.positive b).isHermitian.eq]
    · simp only [kron_mul,M.idempotent,N.idempotent]
  simp_rw [he]
  rw [← effectKernelE_sum]
  simp_rw [← effectKernelE_sum]
  simp only [← kron_sum_left,← kron_sum_right,M.complete,N.complete,kron_one]
  simp [effectKernelE,reducedE]

/-- The operator Fourier criterion now refers to the ACTUAL quantum
post-measurement states; normalization of the zeroth mode is discharged. -/
theorem physical_private_iff_fourier (T : Matrix (ι×κ) ε ℂ)
    (M : Measurement d ι) (N : Measurement d κ) :
    (∀ a b,jointInstrument T M N a b=((d : ℂ)⁻¹)^2 • reducedE T) ↔
      ∀ k l : Ix d,(k,l)≠(0,0) →
        (∑ a,∑ b,chi (k*a+l*b) • jointInstrument T M N a b)=0 := by
  rw [operator_uniform_iff]
  have hz : operatorFourier (jointInstrument T M N) 0 0=reducedE T := by
    simpa [operatorFourier] using jointInstrument_total T M N
  simp only [hz,true_and,operatorFourier]

theorem reducedE_trace (T : Matrix ι ε ℂ) : Matrix.trace (reducedE T)=(frobeniusSq T : ℂ) := by
  simp only [reducedE,Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,Matrix.transpose_apply,
    Matrix.map_apply,Complex.mul_conj,frobeniusSq,Complex.ofReal_sum]
  rw [Finset.sum_comm]

/-- For an operator-uniform private table, every complete Eve POVM has the
same success. Positivity of Q is part of being a POVM, but completeness alone
is already enough for this algebraic equality. -/
theorem operator_uniform_guess_success {A B : Type*} [Fintype A] [Fintype B]
    (ρ : Mat ε) (hρ : Matrix.trace ρ=1) (c : ℝ) (Q : A → B → Mat ε)
    (hQ : ∑ a,∑ b,Q a b=1) :
    (∑ a,∑ b,(Matrix.trace (Q a b*((c : ℂ) • ρ))).re)=c := by
  simp only [mul_smul_comm,Matrix.trace_smul,smul_eq_mul,Complex.mul_re,Complex.ofReal_re,
    Complex.ofReal_im,zero_mul,sub_zero,← Finset.mul_sum]
  rw [← Complex.re_sum,← Complex.re_sum,← Matrix.trace_sum,← Matrix.trace_sum,
    ← Finset.sum_mul,← Finset.sum_mul,hQ,one_mul,hρ]
  simp

theorem binary_private_guess_success (T : Matrix ι ε ℂ) (hT : frobeniusSq T=1)
    (A₀ A₁ B₀ B₁ : Mat ι)
    (hA₀ : HermitianInvolution A₀) (hA₁ : HermitianInvolution A₁)
    (hB₀ : HermitianInvolution B₀) (hB₁ : HermitianInvolution B₁)
    (hc : BinaryCross A₀ A₁ B₀ B₁)
    (hsat : stateEval (T*T.conjTranspose) (binaryScoreOperator A₀ A₁ B₀ B₁)=3*Real.sqrt 3)
    (Q : Fin 2 → Fin 2 → Mat ε) (hQ : ∑ a,∑ b,Q a b=1) :
    (∑ a,∑ b,(Matrix.trace (Q a b*conditionalE T (binaryEffect A₀ a*binaryEffect B₀ b))).re)=1/4 := by
  simp_rw [binary_saturation_privacy T hT A₀ A₁ B₀ B₁ hA₀ hA₁ hB₀ hB₁ hc hsat]
  exact operator_uniform_guess_success (reducedE T) (by rw [reducedE_trace,hT]; simp) (1/4) Q hQ

theorem second_all_dimension_physical_Eve_gap (hd : 4≤d) :
    let s := secondPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
    secondValue s=d+1 ∧
    ∃ g : Ix d×Ix d,1/(d : ℝ)^2<fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g := by
  dsimp
  refine ⟨secondPermutation_attains (by omega) _,?_⟩
  obtain ⟨a,b,h⟩ := swappedTarget_quantitative (d := d) hd
  refine ⟨(a,b),?_⟩
  rw [fixedGuessSuccess_eq]
  change 1/(d : ℝ)^2<behavior (secondPermutationStrategy (by omega) (finalSwap d)) 1 none a b
  rw [second_first_target_same,firstSwap_target hd]
  exact (quantitative_gap_positive hd).trans_le h

/-- No valid vanishing deficit-only upper bound, with all physical strategy
and tolerance quantifiers. An exactly maximizing strategy is feasible for every
positive tolerance. Additional observed behavior constraints are not excluded. -/
theorem first_no_value_only_endpoint_robustness (hd : 4≤d) (f : ℝ → ℝ)
    (hf : Filter.Tendsto f (nhdsWithin 0 (Set.Ioi 0)) (nhds 0)) :
    ¬ (∀ ε : ℝ,0<ε →
      ∀ s : StrategyOn d (Fin 2) (AugmentedInputs d) (Ix d) (Ix d),
        scalarMaximum d+1-firstValue s≤ε →
        ∀ g : Ix d×Ix d,fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g≤1/(d : ℝ)^2+f ε) := by
  intro h
  let s := firstPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
  obtain ⟨hs,g,hg⟩ := first_all_dimension_physical_Eve_gap (d := d) hd
  apply no_endpoint_modulus (1/(d : ℝ)^2) (fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g) hg f hf
  intro ε hε
  exact h ε hε s (by rw [hs]; linarith) g

theorem second_no_value_only_endpoint_robustness (hd : 4≤d) (f : ℝ → ℝ)
    (hf : Filter.Tendsto f (nhdsWithin 0 (Set.Ioi 0)) (nhds 0)) :
    ¬ (∀ ε : ℝ,0<ε →
      ∀ s : StrategyOn d (Ix d) (AugmentedInputs d) (Ix d) (Ix d),
        (d : ℝ)+1-secondValue s≤ε →
        ∀ g : Ix d×Ix d,fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g≤1/(d : ℝ)^2+f ε) := by
  intro h
  let s := secondPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
  obtain ⟨hs,g,hg⟩ := second_all_dimension_physical_Eve_gap (d := d) hd
  apply no_endpoint_modulus (1/(d : ℝ)^2) (fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g) hg f hf
  intro ε hε
  exact h ε hε s (by rw [hs]; linarith) g

theorem binary_entropy_exact : -(Real.log (1/4)/Real.log 2)=2 := by
  have h2 : Real.log 2≠0 := ne_of_gt (Real.log_pos (by norm_num))
  have h4 : Real.log 4=2*Real.log 2 := by
    rw [show (4 : ℝ)=2^2 by norm_num,Real.log_pow]; norm_num
  rw [Real.log_div (by norm_num) (by norm_num),Real.log_one,h4]
  field_simp
  ring

theorem d4_entropy_exact : -(Real.log (3/32)/Real.log 2)=5-Real.log 3/Real.log 2 := by
  have h2 : Real.log 2≠0 := ne_of_gt (Real.log_pos (by norm_num))
  have h32 : Real.log 32=5*Real.log 2 := by
    rw [show (32 : ℝ)=2^5 by norm_num,Real.log_pow]; norm_num
  rw [Real.log_div (by norm_num) (by norm_num),h32]
  field_simp
  ring

theorem d4_entropy_less_than_four : -(Real.log (3/32)/Real.log 2)<4 := by
  rw [d4_entropy_exact]
  have h2 : 0<Real.log 2 := Real.log_pos (by norm_num)
  have h23 : Real.log 2<Real.log 3 := Real.log_lt_log (by norm_num) (by norm_num)
  have hratio : 1<Real.log 3/Real.log 2 := (lt_div_iff₀ h2).mpr (by simpa using h23)
  linarith

end CyclicBell.General
