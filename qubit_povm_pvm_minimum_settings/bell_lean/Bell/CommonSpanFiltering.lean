import Bell.ExtremeMeasurement
import Bell.FrameRealization

/-!
# Common-span filtering from complete-behavior extremality

The branch weights are the changed state normalizations, not equal weights.
Both inputs are filtered by the SAME operator, so every branch is one complete
physical strategy. Strict marginal positivity then makes every coefficient
constant, forcing the common span to consist only of scalar identities.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell
open Lorentz QubitGeometry

namespace FullPureStrategy
variable {A : Architecture} (s : FullPureStrategy A)

def reduced : Operator := s.coefficient*s.coefficient.conjTranspose

def steered (y : Fin A.bobInputs) (b : Fin (A.bobOutputs y)) : Operator :=
  s.coefficient*((s.bob y).effect b).transpose*s.coefficient.conjTranspose

theorem reduced_definite : s.reduced.PosDef := by
  apply posDef_of_posSemidef_det_ne_zero
  · exact (Matrix.PosSemidef.one : (1 : Operator).PosSemidef).mul_mul_conjTranspose_same s.coefficient
  · rw [reduced,Matrix.det_mul,Matrix.det_conjTranspose]
    exact mul_ne_zero (isUnit_iff_ne_zero.mp s.coefficient_invertible)
      (map_ne_zero (starRingEnd ℂ) (isUnit_iff_ne_zero.mp s.coefficient_invertible))

theorem steered_positive (y : Fin A.bobInputs) (b : Fin (A.bobOutputs y)) :
    (s.steered y b).PosSemidef :=
  ((s.bob y).positive b).transpose.mul_mul_conjTranspose_same s.coefficient

theorem steered_sum (y : Fin A.bobInputs) : ∑ b, s.steered y b=s.reduced := by
  simp only [steered,← Matrix.sum_mul,← Matrix.mul_sum,← Matrix.transpose_sum,
    (s.bob y).normalized,Matrix.transpose_one,mul_one,reduced]

theorem behavior_steered (x : Fin A.aliceInputs) (y : Fin A.bobInputs)
    (a : Fin (A.aliceOutputs x)) (b : Fin (A.bobOutputs y)) :
    s.behavior x y a b=localTrace ((s.alice x).effect a) (s.steered y b) :=
  pureDensity_born _ _ _

def filteredTable (c : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x) → ℝ)
    (H : Operator) (t : ℝ) : Behavior A := fun x y a b =>
  ((1+t*c x a)/(1+t*localTrace H s.reduced))*s.behavior x y a b

/-- The operator construction of each normalized filtering branch. -/
def filteredAssemblage
    (c : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x) → ℝ)
    (H : Operator) (t : ℝ) (hH : H.IsHermitian)
    (hcommon : ∀ x, ∑ a, c x a • (s.alice x).effect a=H)
    (hleft : (1+t • H).PosDef)
    (hcoef : ∀ x a, 0 < 1+t*c x a)
    (hscale : 0 < 1+t*localTrace H s.reduced) : UnnormalizedAssemblage A where
  left x a := (1+t*c x a) • (s.alice x).effect a
  right y b := (1+t*localTrace H s.reduced)⁻¹ • s.steered y b
  leftSum := 1+t • H
  rightSum := (1+t*localTrace H s.reduced)⁻¹ • s.reduced
  leftPositive := fun x a => posSemidef_real_smul ((s.alice x).positive a) (hcoef x a).le
  rightPositive := fun y b => posSemidef_real_smul (s.steered_positive y b) (inv_nonneg.mpr hscale.le)
  leftTotal := by
    intro x
    simp_rw [add_smul,one_smul,mul_smul]
    rw [Finset.sum_add_distrib,← Finset.smul_sum,(s.alice x).normalized,hcommon x]
  rightTotal := by intro y; rw [← Finset.smul_sum,s.steered_sum]
  leftDefinite := hleft
  rightDefinite := posDef_real_smul s.reduced_definite (inv_pos.mpr hscale)
  normalized := by
    have ht : Matrix.trace ((1+t • H)*s.reduced) =
        ((1+t*localTrace H s.reduced : ℝ) : ℂ) := by
      apply Complex.ext
      · change localTrace (1+t • H) s.reduced=1+t*localTrace H s.reduced
        rw [localTrace_comm,map_add,map_smul]
        simp [localTrace_comm s.reduced H,localTrace,s.normalized,reduced]
      · have hLH : (1+t • H).IsHermitian := by
          simpa [map_add,map_smul] using pauli_isHermitian
            (timeUnit+t • coordinates H)
        simpa using trace_product_im_zero hLH s.reduced_definite.isHermitian
    rw [Matrix.mul_smul,Matrix.trace_smul,ht]
    simp only [smul_eq_mul]
    norm_cast
    exact inv_mul_cancel₀ hscale.ne'

theorem filteredTable_mem_rawPOVM
    (c : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x) → ℝ)
    (H : Operator) (t : ℝ) (hH : H.IsHermitian)
    (hcommon : ∀ x, ∑ a, c x a • (s.alice x).effect a=H)
    (hleft : (1+t • H).PosDef)
    (hcoef : ∀ x a, 0 < 1+t*c x a)
    (hscale : 0 < 1+t*localTrace H s.reduced) :
    s.filteredTable c H t ∈ rawPOVM A := by
  let b := s.filteredAssemblage c H t hH hcommon hleft hcoef hscale
  have he : (fun x y a b' => localTrace (b.left x a) (b.right y b'))=s.filteredTable c H t := by
    funext x y a b'
    change localTrace ((1+t*c x a) • (s.alice x).effect a)
      ((1+t*localTrace H s.reduced)⁻¹ • s.steered y b') = _
    rw [map_smul,localTrace_comm,map_smul]
    simp [filteredTable,behavior_steered,localTrace_comm,smul_eq_mul,div_eq_mul_inv]
    ring
  rw [← he]
  exact b.behavior_mem_rawPOVM

end FullPureStrategy

/-- Physical common-span filtering, with all output counts arbitrary. -/
theorem extreme_common_coefficients {A : Architecture} (s : FullPureStrategy A)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM A))
    (y : Fin A.bobInputs)
    (c : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x) → ℝ)
    (H : Operator) (hH : H.IsHermitian)
    (hcommon : ∀ x, ∑ a, c x a • (s.alice x).effect a=H) :
    ∀ x a, (s.alice x).effect a ≠ 0 → c x a=localTrace H s.reduced := by
  classical
  let τ := localTrace H s.reduced
  let coeff : Unit ⊕ ((x : Fin A.aliceInputs) × Fin (A.aliceOutputs x)) → ℝ :=
    Sum.elim (fun _ => τ) (fun i => c i.1 i.2)
  obtain ⟨ε,hε,hTp,hTm,hc⟩ := exists_positive_perturbation coeff
    (Matrix.PosDef.one : (1 : Operator).PosDef) hH
  have hzp : 0 < 1+ε*τ := (hc (.inl ())).1
  have hzm : 0 < 1-ε*τ := (hc (.inl ())).2
  have hcp : ∀ x a, 0 < 1+ε*c x a := fun x a => (hc (.inr ⟨x,a⟩)).1
  have hcm : ∀ x a, 0 < 1+(-ε)*c x a := fun x a => by
    simpa using (hc (.inr ⟨x,a⟩)).2
  have hp := s.filteredTable_mem_rawPOVM c H ε hH hcommon hTp hcp hzp
  have hm := s.filteredTable_mem_rawPOVM c H (-ε) hH hcommon
    (by simpa [sub_eq_add_neg,neg_smul] using hTm) hcm (by simpa using hzm)
  have hmid : ((1+ε*τ)/2) • s.filteredTable c H ε +
      ((1-ε*τ)/2) • s.filteredTable c H (-ε)=s.behavior := by
    funext x y' a b
    simp only [FullPureStrategy.filteredTable,Pi.add_apply,Pi.smul_apply,smul_eq_mul]
    change ((1+ε*τ)/2) * (((1+ε*c x a)/(1+ε*τ))*s.behavior x y' a b) +
      ((1-ε*τ)/2) * (((1+(-ε)*c x a)/(1+(-ε)*τ))*s.behavior x y' a b) = _
    have hn : 1+(-ε)*τ ≠ 0 := by simpa using hzm.ne'
    field_simp [hzp.ne',hzm.ne',hn]
    ring
  have he := (extreme_positive_combination hex
    (subset_convexHull ℝ _ hp) (subset_convexHull ℝ _ hm)
    (div_pos hzp (by norm_num)) (div_pos hzm (by norm_num)) (by ring) hmid).1
  intro x a ha
  have hem := congrArg (fun p : Behavior A => ∑ b, p x y a b) he
  simp only [FullPureStrategy.filteredTable,← Finset.mul_sum] at hem
  have hmass : (∑ b, s.behavior x y a b) = localTrace ((s.alice x).effect a) s.reduced := by
    simp_rw [s.behavior_steered]
    rw [← map_sum,s.steered_sum]
  rw [hmass] at hem
  have hμ : 0 < localTrace ((s.alice x).effect a) s.reduced := full_pure_marginal_positive s x a ha
  have hcoef : (1+ε*c x a)/(1+ε*τ)=1 := by
    apply (mul_right_cancel₀ hμ.ne')
    simpa [τ] using hem
  have heq : 1+ε*c x a=1+ε*τ := (div_eq_one_iff_eq hzp.ne').mp hcoef
  change c x a=τ
  nlinarith

theorem extreme_common_span_scalar {A : Architecture} (s : FullPureStrategy A)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM A))
    (x₀ : Fin A.aliceInputs) (y : Fin A.bobInputs)
    (c : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x) → ℝ)
    (H : Operator) (hH : H.IsHermitian)
    (hcommon : ∀ x, ∑ a, c x a • (s.alice x).effect a=H) :
    H=localTrace H s.reduced • (1 : Operator) := by
  rw [← hcommon x₀,← (s.alice x₀).normalized,Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro a _
  by_cases ha : (s.alice x₀).effect a=0
  · simp [ha]
  · rw [extreme_common_coefficients s hex y c H hH hcommon x₀ a ha]

end Bell
