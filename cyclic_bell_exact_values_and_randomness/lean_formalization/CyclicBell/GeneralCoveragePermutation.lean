import CyclicBell.GeneralPermutation
import CyclicBell.GeneralCommuting

/-! Arbitrary-Hilbert extension of the conditional phase-permutation theorem.
The coefficient set and affine factors are arbitrary; their scalar cap is an
explicit conditional hypothesis. Continuous half-polar factors include zeros.
-/
noncomputable section
open scoped BigOperators ComplexOrder InnerProductSpace
namespace CyclicBell.General
variable {R : Type*} [Fintype R]
variable {A : Type*} [CStarAlgebra A]

def linearAlgebraModulusCM (u : A) (α β : ℂ) : C(spectrum ℂ u,ℂ) :=
  ⟨fun z => (‖α+β*(z : ℂ)‖ : ℂ),by fun_prop⟩
def linearAlgebraRootCM (u : A) (α β : ℂ) : C(spectrum ℂ u,ℂ) :=
  ⟨fun z => squareRootNorm (α+β*(z : ℂ)),squareRootNorm_continuous.comp (by fun_prop)⟩
def linearAlgebraPolarRootCM (u : A) (α β : ℂ) : C(spectrum ℂ u,ℂ) :=
  ⟨fun z => continuousPolarRoot (α+β*(z : ℂ)),continuousPolarRoot_continuous.comp (by fun_prop)⟩
def linearAlgebraGapCM (u : A) (α β : R → ℂ) (M : ℝ) : C(spectrum ℂ u,ℂ) :=
  ⟨fun z => (Real.sqrt (M-linearScalar α β (z : ℂ)) : ℂ),by unfold linearScalar; fun_prop⟩

theorem linear_algebra_functional_factors (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M)
    (u : A) (b : R → A) (hu : StarUnitary u)
    (hb : ∀ r,StarUnitary (b r)) (hc : ∀ r,u*b r=b r*u) :
    ∃ H K D : R → A, ∃ G : A,
      (∀ r,star (H r)*H r=D r) ∧ (∀ r,star (K r)*K r=D r) ∧
      (∀ r,star (H r)*K r=α r • 1+β r • u) ∧ (∀ r,D r*b r=b r*D r) ∧
      star G*G=(M : ℂ) • 1-∑ r,D r := by
  let φ := cfcHom (R := ℂ) (starUnitary_normal hu)
  refine ⟨(fun r => φ (linearAlgebraRootCM u (α r) (β r))),
    (fun r => φ (linearAlgebraPolarRootCM u (α r) (β r))),
    (fun r => φ (linearAlgebraModulusCM u (α r) (β r))),
    φ (linearAlgebraGapCM u α β M),?_,?_,?_,?_,?_⟩
  · intro r
    have he : star (linearAlgebraRootCM u (α r) (β r))*linearAlgebraRootCM u (α r) (β r)=
        linearAlgebraModulusCM u (α r) (β r) := by ext z; exact squareRootNorm_square _
    simpa only [map_star,map_mul] using congrArg φ he
  · intro r
    have he : star (linearAlgebraPolarRootCM u (α r) (β r))*linearAlgebraPolarRootCM u (α r) (β r)=
        linearAlgebraModulusCM u (α r) (β r) := by ext z; exact continuousPolarRoot_square _
    simpa only [map_star,map_mul] using congrArg φ he
  · intro r
    have he : star (linearAlgebraRootCM u (α r) (β r))*linearAlgebraPolarRootCM u (α r) (β r)=
        α r • 1+β r • ((ContinuousMap.id ℂ).restrict (spectrum ℂ u)) := by
      ext z
      simpa only [linearAlgebraRootCM,linearAlgebraPolarRootCM,ContinuousMap.mul_apply,
        ContinuousMap.star_apply,ContinuousMap.smul_apply,ContinuousMap.add_apply,
        ContinuousMap.one_apply,ContinuousMap.coe_mk,ContinuousMap.restrict_apply,
        ContinuousMap.id_apply,smul_eq_mul,mul_one] using continuousPolarRoot_cross (α r+β r*(z : ℂ))
    simpa only [map_star,map_mul,map_add,map_smul,map_one,φ,cfcHom_id] using congrArg φ he
  · intro r
    exact cfcHom_commute_unitary hu (hb r) (hc r) _
  · have he : star (linearAlgebraGapCM u α β M)*linearAlgebraGapCM u α β M=
        (M : ℂ) • 1-∑ r,linearAlgebraModulusCM u (α r) (β r) := by
      ext z
      have hp := sub_nonneg.mpr (hcap z (spectrum_unit_norm hu z))
      change star ((Real.sqrt (M-linearScalar α β (z : ℂ)) : ℝ) : ℂ) *
        ((Real.sqrt (M-linearScalar α β (z : ℂ)) : ℝ) : ℂ) = _
      rw [star_real, ← Complex.ofReal_mul, Real.mul_self_sqrt hp]
      simp [linearScalar,linearAlgebraModulusCM,Complex.ofReal_sub,Complex.ofReal_sum]
    simpa only [map_star,map_mul,map_sub,map_sum,map_smul,map_one] using congrArg φ he

def linearAlgebraOperator (α β : R → ℂ) (a₀ a₁ : A) (b : R → A) : A :=
  ∑ r,algebraHerm ((α r • a₀+β r • a₁)*b r)

/-- Operator certificate for all affine coefficient families, including zeros. -/
theorem linear_cstar_sos (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M)
    (a₀ a₁ : A) (b : R → A) (h₀ : StarUnitary a₀) (h₁ : StarUnitary a₁)
    (hb : ∀ r,StarUnitary (b r))
    (hc₀ : ∀ r,a₀*b r=b r*a₀) (hc₁ : ∀ r,a₁*b r=b r*a₁) :
    ∃ (P : R → A) (G : A),
      (M : ℂ) • 1-linearAlgebraOperator α β a₀ a₁ b=
        (1/2 : ℂ) • (∑ r,star (P r)*P r)+(1/2 : ℂ) • (star G*G)+
        (1/2 : ℂ) • (star (G*star a₀)*(G*star a₀)) := by
  let u := star a₀*a₁
  have hu : StarUnitary u := starUnitary_mul (starUnitary_star h₀) h₁
  have hc (r : R) : u*b r=b r*u := by
    rw [mul_assoc,hc₁,← mul_assoc,star_commute_of_unitary h₀ (hc₀ r),mul_assoc]
  obtain ⟨H,K,D,G,hh,hk,hcross,hDb,hG⟩ := linear_algebra_functional_factors α β M hcap u b hu hb hc
  let P := fun r => H r*star a₀-K r*b r
  refine ⟨P,G,?_⟩
  have hrow (r : R) : star (P r)*P r=
      a₀*D r*star a₀+D r-((α r • a₀+β r • a₁)*b r+star ((α r • a₀+β r • a₁)*b r)) := by
    have h := algebra_halfPolar_gap a₀ (H r) (K r) (D r) (b r) _
      (hh r) (hk r) (hcross r) (hb r) (hDb r)
    have he : a₀*(α r • 1+β r • u)=α r • a₀+β r • a₁ := by
      simp only [mul_add,mul_one,mul_smul_comm,u,← mul_assoc,h₀.2,one_mul]
    simpa only [he] using h
  have hgA : star (G*star a₀)*(G*star a₀)=a₀*(star G*G)*star a₀ := by
    simp [star_mul,mul_assoc]
  rw [hgA,hG]
  simp_rw [hrow]
  unfold linearAlgebraOperator algebraHerm
  simp only [Finset.sum_sub_distrib,Finset.sum_add_distrib,← Finset.sum_mul,← Finset.mul_sum,
    mul_sub,sub_mul,mul_smul_comm,smul_mul_assoc,one_mul,mul_one,h₀.2,
    Finset.smul_sum,smul_sub,smul_add]
  module

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The conditional bound on an arbitrary complete complex Hilbert space. -/
theorem linear_commuting_hilbert_bound (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M)
    (ψ : H) (hψ : ‖ψ‖=1) (a₀ a₁ : H →L[ℂ] H) (b : R → H →L[ℂ] H)
    (h₀ : StarUnitary a₀) (h₁ : StarUnitary a₁) (hb : ∀ r,StarUnitary (b r))
    (hc₀ : ∀ r,a₀*b r=b r*a₀) (hc₁ : ∀ r,a₁*b r=b r*a₁) :
    vectorEval ψ (linearAlgebraOperator α β a₀ a₁ b)≤M := by
  obtain ⟨P,G,hgap⟩ := linear_cstar_sos α β M hcap a₀ a₁ b h₀ h₁ hb hc₀ hc₁
  have h := congrArg (vectorEval ψ) hgap
  have half : (1/2 : ℂ)=((1/2 : ℝ) : ℂ) := by norm_num
  simp only [vectorEval_sub,vectorEval_real_smul,vectorEval_one ψ hψ,
    vectorEval_add,half,vectorEval_sum,vectorEval_square] at h
  have hp : 0≤∑ r,‖P r ψ‖^2 := Finset.sum_nonneg (fun _ _ => sq_nonneg _)
  have hg := sq_nonneg ‖G ψ‖
  have hgA := sq_nonneg ‖(G*star a₀) ψ‖
  linarith

theorem linear_augmented_commuting_hilbert_bound (α β : R → ℂ) (M : ℝ)
    (hcap : ∀ z : ℂ, ‖z‖=1 → linearScalar α β z≤M)
    (ψ : H) (hψ : ‖ψ‖=1) (a₀ a₁ bstar : H →L[ℂ] H) (b : R → H →L[ℂ] H)
    (h₀ : StarUnitary a₀) (h₁ : StarUnitary a₁) (hstar : StarUnitary bstar)
    (hb : ∀ r,StarUnitary (b r))
    (hc₀ : ∀ r,a₀*b r=b r*a₀) (hc₁ : ∀ r,a₁*b r=b r*a₁) :
    vectorEval ψ (linearAlgebraOperator α β a₀ a₁ b+algebraHerm (a₀*bstar))≤M+1 := by
  rw [vectorEval_add]
  exact add_le_add (linear_commuting_hilbert_bound α β M hcap ψ hψ a₀ a₁ b h₀ h₁ hb hc₀ hc₁)
    (aligned_commuting_hilbert_bound ψ hψ _ (starUnitary_mul h₀ hstar))

section FiniteMoments
variable {d : ℕ} [NeZero d]

/-- Every local complex first moment vanishes for the displayed strategy. -/
theorem linear_permutation_local_moments_zero (hd : 2≤d) {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) :
    (∀ x : Fin 2, expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ x)) 1)=0) ∧
    (∀ q : Option R, expectation (maximallyEntangled d)
      (kron 1 (encoded (linearPermutationBob p σ q)))=0) := by
  obtain ⟨h0,h1,hb,hbr⟩ := linear_permutation_encodings p σ
  constructor
  · intro x
    rw [phi_trace,Matrix.transpose_one,Matrix.mul_one]
    have ht : Matrix.trace (encoded (linearPermutationAlice p σ x))=0 := by
      rcases (show x=0 ∨ x=1 by fin_cases x <;> decide) with rfl|rfl
      · rw [h0]; exact weighted_trace_zero hd _
      · rw [h1]; exact weighted_trace_zero hd _
    rw [ht,zero_div]
  · intro q
    rw [phi_trace,Matrix.one_mul,Matrix.trace_transpose]
    have ht : Matrix.trace (encoded (linearPermutationBob p σ q))=0 := by
      cases q with
      | none => rw [hb]; exact weighted_trace_zero hd _
      | some r => rw [hbr,weighted_entry_conjugate]; exact weighted_trace_zero hd _
    rw [ht,zero_div]

/-- All complex first-harmonic entries, including the alignment input, agree. -/
theorem linear_permutation_all_harmonics_invariant {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ τ : Equiv.Perm (Ix d))
    (x : Fin 2) (q : Option R) :
    expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ x)) (encoded (linearPermutationBob p σ q)))=
    expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p τ x)) (encoded (linearPermutationBob p τ q))) := by
  cases q with
  | some r =>
    obtain ⟨hσ0,hσ1⟩ := linear_permutation_harmonics p σ r
    obtain ⟨hτ0,hτ1⟩ := linear_permutation_harmonics p τ r
    rcases (show x=0 ∨ x=1 by fin_cases x <;> decide) with rfl|rfl
    · exact hσ0.trans hτ0.symm
    · exact hσ1.trans hτ1.symm
  | none =>
    obtain ⟨hσ0,hσ1,hσb,_⟩ := linear_permutation_encodings p σ
    obtain ⟨hτ0,hτ1,hτb,_⟩ := linear_permutation_encodings p τ
    rcases (show x=0 ∨ x=1 by fin_cases x <;> decide) with rfl|rfl
    · rw [hσ0,hτ0,hσb,hτb]
    · rw [hσ1,hτ1,hσb,hτb,(added_first_harmonics p.z σ).2,(added_first_harmonics p.z τ).2]
end FiniteMoments

end CyclicBell.General
