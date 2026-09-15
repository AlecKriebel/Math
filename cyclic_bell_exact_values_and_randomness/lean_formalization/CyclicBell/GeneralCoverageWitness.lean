import CyclicBell.GeneralPermutation
import CyclicBell.GeneralCycleCharpoly
import Mathlib.LinearAlgebra.Eigenspace.Basic

/-! Additional literal coverage for the conditional permutation theorem:
all first moments/correlators and one-dimensional eigenspaces. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem measurement_effect_encoded {ι : Type*} [Fintype ι] [DecidableEq ι]
    (M : Measurement d ι) (a : Ix d) :
    M.effect a * encoded M = chi a • M.effect a := by
  unfold encoded
  rw [Finset.mul_sum,Finset.sum_eq_single a]
  · rw [mul_smul_comm,M.idempotent]
  · intro b _ hba
    rw [mul_smul_comm,M.orthogonal a b (Ne.symm hba),smul_zero]
  · simp

theorem phase_eigenspace_eq_span (q : Ix d → ℂ) (hq : UnitPhases q) (a : Ix d) :
    Module.End.eigenspace (encoded (phaseMeasurement q hq)).mulVecLin (chi a) =
      Submodule.span ℂ {phasedVector q a} := by
  let M := phaseMeasurement q hq
  apply le_antisymm
  · intro v hv
    have hev : encoded M *ᵥ v = chi a • v := Module.End.mem_eigenspace_iff.mp hv
    have hz (b : Ix d) (hba : b ≠ a) : M.effect b *ᵥ v = 0 := by
      have h := congrArg (fun T : Mat (Ix d) => T *ᵥ v) (measurement_effect_encoded M b)
      dsimp only at h
      rw [← Matrix.mulVec_mulVec,hev,Matrix.mulVec_smul,Matrix.smul_mulVec_assoc] at h
      ext i
      have he := congrArg (fun x : Ix d → ℂ => x i) h
      simp only [Pi.smul_apply,smul_eq_mul] at he
      have hne : chi a - chi b ≠ 0 := sub_ne_zero.mpr (fun h => hba (chi_injective h).symm)
      have hp : (chi a-chi b)*(M.effect b *ᵥ v) i=0 := by linear_combination he
      exact (mul_eq_zero.mp hp).resolve_left hne
    have hsum : ∑ b,M.effect b *ᵥ v = v := by
      have h := congrArg (fun T : Mat (Ix d) => T *ᵥ v) M.complete
      dsimp only at h
      rw [Matrix.one_mulVec] at h
      have he : (∑ b,M.effect b) *ᵥ v = ∑ b,M.effect b *ᵥ v := by
        ext i
        simp only [Matrix.mulVec,dotProduct,Matrix.sum_apply,Finset.sum_apply,Finset.sum_mul]
        rw [Finset.sum_comm]
      rwa [he] at h
    rw [Finset.sum_eq_single a (fun b _ hba => hz b hba) (by simp)] at hsum
    apply Submodule.mem_span_singleton.mpr
    refine ⟨ip (phasedVector q a) v,?_⟩
    have hp := projector_apply (phasedVector q a) v
    change applyOp (projector (phasedVector q a)) v = v at hsum
    rw [hp] at hsum
    simpa only [Pi.smul_apply,smul_eq_mul,mul_comm] using hsum
  · apply Submodule.span_le.mpr
    intro v hv
    have hv' : v=phasedVector q a := Set.mem_singleton_iff.mp hv
    subst v
    apply Module.End.mem_eigenspace_iff.mpr
    exact basis_eigenvector q hq a

/-- Every root eigenspace has dimension exactly one, including composite d. -/
theorem weighted_cycle_eigenspace_finrank (w : Ix d → ℂ) (hw : UnitPhases w)
    (hp : ∏ j,w j=1) (a : Ix d) :
    Module.finrank ℂ (Module.End.eigenspace (weightedCycle w).mulVecLin (chi a))=1 := by
  rw [← cycleMeasurement_encoding w hw hp]
  change Module.finrank ℂ (Module.End.eigenspace
    (encoded (phaseMeasurement («prefix» w) (prefix_unit w hw))).mulVecLin (chi a))=1
  rw [phase_eigenspace_eq_span _ (prefix_unit w hw) a]
  exact finrank_span_singleton (basis_vector_nonzero («prefix» w) (prefix_unit w hw) a)

variable {R : Type*} [Fintype R]

theorem phi_local_left (A : Mat (Ix d)) :
    expectation (maximallyEntangled d) (kron A 1)=Matrix.trace A/(d : ℂ) := by
  rw [phi_trace]
  simp

theorem phi_local_right (B : Mat (Ix d)) :
    expectation (maximallyEntangled d) (kron 1 B)=Matrix.trace B/(d : ℂ) := by
  rw [phi_trace]
  simp

/-- All local first moments and both correlator rows, including Bob's extra
setting, for the manuscript's conditional phase-permutation construction. -/
theorem conditional_permutation_complete_harmonics (hd : 2≤d)
    {α β : R → ℂ} {M : ℝ} (p : PermutationData d R α β M)
    (σ : Equiv.Perm (Ix d)) :
    (∀ x : Fin 2, expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ x)) 1)=0) ∧
    (∀ y : Option R, expectation (maximallyEntangled d)
      (kron 1 (encoded (linearPermutationBob p σ y)))=0) ∧
    (∀ r, expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ 0))
        (encoded (linearPermutationBob p σ (some r))))=(∑ j,star (p.s r j))/(d : ℂ)) ∧
    (∀ r, expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ 1))
        (encoded (linearPermutationBob p σ (some r))))=(∑ j,p.z j*star (p.s r j))/(d : ℂ)) ∧
    expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ 0))
        (encoded (linearPermutationBob p σ none)))=1 ∧
    expectation (maximallyEntangled d)
      (kron (encoded (linearPermutationAlice p σ 1))
        (encoded (linearPermutationBob p σ none)))=(∑ j,p.z j)/(d : ℂ) := by
  obtain ⟨h0,h1,hb,hbr⟩ := linear_permutation_encodings p σ
  refine ⟨?_,?_,fun r => (linear_permutation_harmonics p σ r).1,
    fun r => (linear_permutation_harmonics p σ r).2,?_,?_⟩
  · intro x
    fin_cases x
    · change expectation (maximallyEntangled d) (kron (encoded (linearPermutationAlice p σ 0)) 1)=0
      rw [h0,phi_local_left,cyclicShift,weighted_trace_zero hd,zero_div]
    · change expectation (maximallyEntangled d) (kron (encoded (linearPermutationAlice p σ 1)) 1)=0
      rw [h1,phi_local_left,weighted_trace_zero hd,zero_div]
  · intro y
    cases y with
    | none => rw [hb,phi_local_right,cyclicShift,weighted_trace_zero hd,zero_div]
    | some r => rw [hbr,weighted_entry_conjugate,phi_local_right,weighted_trace_zero hd,zero_div]
  · rw [h0,hb]
    exact (added_first_harmonics p.z σ).1
  · rw [h1,hb]
    exact (added_first_harmonics p.z σ).2

/-- Literal simple-spectrum conclusion for every displayed Alice and Bob
observable, including Bob's additional setting. -/
theorem conditional_permutation_simple_spectra {α β : R → ℂ} {M : ℝ}
    (p : PermutationData d R α β M) (σ : Equiv.Perm (Ix d)) :
    (∀ x : Fin 2, ∀ a : Ix d, Module.finrank ℂ
      (Module.End.eigenspace (encoded (linearPermutationAlice p σ x)).mulVecLin (chi a))=1) ∧
    (∀ y : Option R, ∀ a : Ix d, Module.finrank ℂ
      (Module.End.eigenspace (encoded (linearPermutationBob p σ y)).mulVecLin (chi a))=1) := by
  obtain ⟨h0,h1,hb,hbr⟩ := linear_permutation_encodings p σ
  have hshift (a : Ix d) : Module.finrank ℂ
      (Module.End.eigenspace (cyclicShift d).mulVecLin (chi a))=1 :=
    weighted_cycle_eigenspace_finrank (fun _ => 1) (by intro j; simp) (by simp) a
  constructor
  · intro x a
    fin_cases x
    · change Module.finrank ℂ (Module.End.eigenspace
        (encoded (linearPermutationAlice p σ 0)).mulVecLin (chi a))=1
      rw [h0]; exact hshift a
    · change Module.finrank ℂ (Module.End.eigenspace
        (encoded (linearPermutationAlice p σ 1)).mulVecLin (chi a))=1
      rw [h1]
      exact weighted_cycle_eigenspace_finrank _ (phases_permuted _ p.z_unit σ)
        (by simpa only [Function.comp_apply,product_permuted] using p.z_product) a
  · intro y a
    cases y with
    | none => rw [hb]; exact hshift a
    | some r =>
      rw [hbr,weighted_entry_conjugate]
      exact weighted_cycle_eigenspace_finrank _
        (by intro j; simpa [Function.comp_apply,mul_comm] using p.s_unit r (σ j))
        (by simpa only [Function.comp_apply,star_prod,star_one] using
          congrArg star ((product_permuted (p.s r) σ).trans (p.s_product r))) a

end CyclicBell.General
