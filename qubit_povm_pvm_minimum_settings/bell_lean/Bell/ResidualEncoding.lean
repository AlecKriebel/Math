import Bell.SmallOutputEncoding
import Bell.ResidualCoordinates

/-!
# Exact residual recoding and full-rank effect frames

The original finite alphabets are retained through a deterministic map back
from the padded binary/ternary architecture. Frame invertibility follows from
active-effect independence and common-span filtering, rather than being an
additional genericity assumption on the original strategy.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell
open Lorentz QubitGeometry

attribute [local simp] Matrix.cons_val_two Matrix.cons_val_three Matrix.cons_val_four

theorem effectSpan_le_of_effects {n : ℕ} (N : POVM n) (S : Submodule ℝ V)
    (h : ∀ a, coordinates (N.effect a) ∈ S) : effectSpan N ≤ S := by
  rintro v ⟨c,rfl⟩
  change (∑ a : EffectSupport N, c a • coordinates (N.effect a)) ∈ S
  exact S.sum_mem fun a _ => S.smul_mem _ (h a.val)

theorem effectSpan_coarsen_le {n m : ℕ} (N : POVM n) (f : Fin n → Fin m) :
    effectSpan (coarsenPOVM N f) ≤ effectSpan N := by
  apply effectSpan_le_of_effects
  intro b
  change coordinates (∑ a, if f a=b then N.effect a else 0) ∈ effectSpan N
  rw [map_sum]
  apply Submodule.sum_mem
  intro a _
  by_cases ha : f a=b
  · simpa [ha] using effect_coordinates_mem_span N a
  · simp [ha]

theorem effectSpan_encode {n : ℕ} (N : POVM n) (hc : Fintype.card (EffectSupport N) ≤ 3) :
    effectSpan (encodePOVM N hc)=effectSpan N := by
  apply le_antisymm
  · apply effectSpan_le_of_effects
    intro a
    rcases encodePOVM_effect_cases N hc a with hz|⟨b,hb⟩
    · simp [hz]
    · rw [hb]; exact effect_coordinates_mem_span N b
  · have hs := effectSpan_coarsen_le (encodePOVM N hc) (encodingLabel N hc)
    have he : coarsenPOVM (encodePOVM N hc) (encodingLabel N hc)=N := by
      apply POVM.ext_effect
      funext a
      exact encoding_coarsens _ hc a
    simpa [he] using hs

/-- Matrix columns are the first two effects of each input. -/
def measurementFrame (N : Fin 2 → POVM 3) : M := fun i j =>
  ![coordinates ((N 0).effect 0) i,coordinates ((N 0).effect 1) i,
    coordinates ((N 1).effect 0) i,coordinates ((N 1).effect 1) i] j

theorem measurementFrame_effectRay (N : Fin 2 → POVM 3) (hz : (N 0).effect 2=0)
    (x : Fin 2) (a : Fin 3) :
    measurementFrame N *ᵥ effectRay x a=coordinates ((N x).effect a) := by
  have hc2 (h : 2 < 3) : (⟨2,h⟩ : Fin 3) = 2 := rfl
  have hn0 := congrArg coordinates (N 0).normalized
  have hn1 := congrArg coordinates (N 1).normalized
  norm_num [map_add,Fin.sum_univ_succ,hz] at hn0 hn1
  ext i
  have h0 := congrFun hn0 i
  have h1 := congrFun hn1 i
  simp only [Pi.add_apply] at h0 h1
  fin_cases x <;> fin_cases a <;>
    norm_num [measurementFrame,effectRay,ray,Matrix.mulVec,dotProduct,Fin.sum_univ_succ,hz] <;>
    (try simp only [hc2, hz, map_zero, Pi.zero_apply]) <;>
    linarith

theorem measurementFrame_ray (N : Fin 2 → POVM 3) (hz : (N 0).effect 2=0) (j : Fin 5) :
    measurementFrame N *ᵥ ray j=coordinates ((N (rayInput j)).effect (rayLabel j)) := by
  have he := measurementFrame_effectRay N hz (rayInput j) (rayLabel j)
  have hr : effectRay (rayInput j) (rayLabel j)=ray j := by
    fin_cases j <;> rfl
  rwa [hr] at he

theorem measurementFrame_unit (N : Fin 2 → POVM 3) (hz : (N 0).effect 2=0) :
    measurementFrame N *ᵥ unitVector=timeUnit := by
  have he : unitVector=effectRay 0 0+effectRay 0 1 := by
    ext i; fin_cases i <;> norm_num [unitVector,effectRay,ray]
  rw [he,Matrix.mulVec_add,measurementFrame_effectRay N hz,measurementFrame_effectRay N hz,← map_add]
  have hn : (N 0).effect 0+(N 0).effect 1=1 := by
    simpa [Fin.sum_univ_succ,hz] using (N 0).normalized
  rw [hn,← pauli_timeUnit,coordinates_pauli]

theorem matrix_det_unit_of_surjective (E : M) (hsur : Function.Surjective (fun x => E *ᵥ x)) :
    IsUnit E.det := by
  classical
  choose z hz using fun j : Fin 4 => hsur (Pi.single j 1)
  change ∀ j, E *ᵥ z j = Pi.single j 1 at hz
  let R : M := fun i j => z j i
  have hER : E*R=1 := by
    ext i j
    change (E *ᵥ z j) i=(1 : M) i j
    rw [hz j]
    simp [Matrix.one_apply,Pi.single_apply,eq_comm]
  have hd := congrArg Matrix.det hER
  rw [Matrix.det_mul,Matrix.det_one] at hd
  apply isUnit_iff_ne_zero.mpr
  intro hz
  simp [hz] at hd

theorem matrix_det_unit_of_injective (E : M) (hi : Function.Injective (fun x => E *ᵥ x)) :
    IsUnit E.det := by
  apply matrix_det_unit_of_surjective
  exact (LinearMap.injective_iff_surjective_of_finrank_eq_finrank (f := linearOfMatrix E) rfl).mp hi

theorem measurementFrame_range (N : Fin 2 → POVM 3) (hz : (N 0).effect 2=0) :
    LinearMap.range (linearOfMatrix (measurementFrame N))=effectSpan (N 0) ⊔ effectSpan (N 1) := by
  apply le_antisymm
  · rintro v ⟨x,rfl⟩
    have he : x=(∑ i : Fin 4, x i • (Pi.single i 1 : V)) := by
      ext i
      simp [Pi.single_apply, eq_comm]
    rw [he,map_sum]
    apply Submodule.sum_mem
    intro j _
    rw [map_smul]
    apply Submodule.smul_mem
    have hb (k : Fin 4) :
        linearOfMatrix (measurementFrame N) (Pi.single k 1) =
          coordinates ((N (if k.val < 2 then 0 else 1)).effect
            (if k.val % 2 = 0 then 0 else 1)) := by
      fin_cases k <;> ext i <;>
        simp [linearOfMatrix_apply,measurementFrame,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]
    rw [hb]
    split_ifs <;>
      first
      | exact Submodule.mem_sup_left (effect_coordinates_mem_span (N 0) _)
      | exact Submodule.mem_sup_right (effect_coordinates_mem_span (N 1) _)
  · apply sup_le
    · apply effectSpan_le_of_effects
      intro a
      exact ⟨effectRay 0 a,measurementFrame_effectRay N hz 0 a⟩
    · apply effectSpan_le_of_effects
      intro a
      exact ⟨effectRay 1 a,measurementFrame_effectRay N hz 1 a⟩

/-- Padding is explicit, input-dependent and leaves the state coefficient fixed. -/
def FullPureStrategy.pad (AO BO : Fin 2 → ℕ) (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (dA dB : Fin 2)
    (hA : ∀ x, Fintype.card (EffectSupport (s.alice x)) ≤ 3)
    (hB : ∀ y, Fintype.card (EffectSupport (s.bob y)) ≤ 3) : FullPureStrategy binaryTernaryArchitecture where
  coefficient := s.coefficient
  coefficient_invertible := s.coefficient_invertible
  normalized := s.normalized
  alice x := encodePOVM (s.alice (inputAt dA x)) (hA _)
  bob y := encodePOVM (s.bob (inputAt dB y)) (hB _)

def paddingMap (AO BO : Fin 2 → ℕ) (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (dA dB : Fin 2)
    (hA : ∀ x, Fintype.card (EffectSupport (s.alice x)) ≤ 3)
    (hB : ∀ y, Fintype.card (EffectSupport (s.bob y)) ≤ 3) :
    StrategyMap binaryTernaryArchitecture ⟨2,2,AO,BO⟩ where
  aliceInput := inputIndex dA
  bobInput := inputIndex dB
  aliceOutput x := encodingLabel (s.alice x) (hA x)
  bobOutput y := encodingLabel (s.bob y) (hB y)

theorem paddingMap_behavior (AO BO : Fin 2 → ℕ) (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (dA dB : Fin 2)
    (hA : ∀ x, Fintype.card (EffectSupport (s.alice x)) ≤ 3)
    (hB : ∀ y, Fintype.card (EffectSupport (s.bob y)) ≤ 3) :
    (paddingMap AO BO s dA dB hA hB).behavior (s.pad AO BO dA dB hA hB).behavior=s.behavior := by
  rw [← StrategyMap.strategy_behavior]
  funext x y a b
  change born _ ((coarsenPOVM
      (encodePOVM (s.alice (inputAt dA (inputIndex dA x))) (hA _))
      (encodingLabel (s.alice x) (hA x))).effect a)
    ((coarsenPOVM (encodePOVM (s.bob (inputAt dB (inputIndex dB y))) (hB _))
      (encodingLabel (s.bob y) (hB y))).effect b) = _
  simp only [inputAt_index,encoding_coarsens]
  fin_cases dA <;> fin_cases dB <;> fin_cases x <;> fin_cases y <;>
    simp [inputAt,inputIndex,otherInput,encoding_coarsens,paddingMap,StrategyMap.strategy,
      FullPureStrategy.pad,FullPureStrategy.toStrategy,Strategy.behavior]

/-- A two/three pair at an extreme behavior spans all four Hermitian directions. -/
theorem encoded_frame_invertible (AO BO : Fin 2 → ℕ) (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,AO,BO⟩))
    (d : Fin 2) (hd : Fintype.card (EffectSupport (s.alice d))=2)
    (ho : Fintype.card (EffectSupport (s.alice (otherInput d)))=3)
    (hc : ∀ x, Fintype.card (EffectSupport (s.alice x)) ≤ 3) :
    IsUnit (measurementFrame (fun x => encodePOVM (s.alice (inputAt d x)) (hc _))).det := by
  let N := fun x => encodePOVM (s.alice (inputAt d x)) (hc _)
  have hz : (N 0).effect 2=0 := encodePOVM_above _ _ _ (by simpa [N,inputAt] using hd.le)
  have h0 := effectSpan_finrank_of_independent (s.alice 0) (extreme_effect_independent s hex 0 0)
  have h1 := effectSpan_finrank_of_independent (s.alice 1) (extreme_effect_independent s hex 1 0)
  have hs := (effectSpan (s.alice 0)).finrank_sup_add_finrank_inf_eq (effectSpan (s.alice 1))
  have hi := extreme_span_intersection_le_one AO BO s hex
  have hdim : Module.finrank ℝ ↥(effectSpan (s.alice 0) ⊔ effectSpan (s.alice 1))=4 := by
    have hle := (effectSpan (s.alice 0) ⊔ effectSpan (s.alice 1)).finrank_le
    rw [h0,h1] at hs
    have hV : Module.finrank ℝ V = 4 := by simp [V]
    rw [hV] at hle
    fin_cases d
    · change Fintype.card (EffectSupport (s.alice 0)) = 2 at hd
      change Fintype.card (EffectSupport (s.alice 1)) = 3 at ho
      omega
    · change Fintype.card (EffectSupport (s.alice 1)) = 2 at hd
      change Fintype.card (EffectSupport (s.alice 0)) = 3 at ho
      omega
  have hN : effectSpan (N 0) ⊔ effectSpan (N 1)=effectSpan (s.alice 0) ⊔ effectSpan (s.alice 1) := by
    simp only [N,effectSpan_encode]
    fin_cases d <;> simp [inputAt,otherInput,sup_comm]
  have hr : LinearMap.range (linearOfMatrix (measurementFrame N))=⊤ := by
    apply Submodule.eq_top_of_finrank_eq
    rw [measurementFrame_range N hz,hN,hdim]
    simp [V]
  exact matrix_det_unit_of_surjective _ (LinearMap.range_eq_top.mp hr)

/-- Congruence of transposed operators gives the exact real steered-frame map. -/
def steeringTransform (C : Operator) : V →ₗ[ℝ] V where
  toFun x := coordinates (C*(pauli x).transpose*C.conjTranspose)
  map_add' := by intros; simp [map_add,Matrix.transpose_add,Matrix.mul_add,Matrix.add_mul]
  map_smul' := by intros; simp [map_smul,Matrix.transpose_smul,Matrix.mul_smul,Matrix.smul_mul]

theorem steered_hermitian (C : Operator) (x : V) :
    (C*(pauli x).transpose*C.conjTranspose).IsHermitian := by
  have ht : ((pauli x).transpose).IsHermitian := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [pauli,Matrix.transpose_apply,Matrix.conjTranspose_apply] <;> ring
  change (C*(pauli x).transpose*C.conjTranspose).conjTranspose=C*(pauli x).transpose*C.conjTranspose
  simp [Matrix.conjTranspose_mul,ht.eq,Matrix.mul_assoc]

theorem steeringTransform_injective (C : Operator) (hc : IsUnit C.det) :
    Function.Injective (steeringTransform C) := by
  intro x y h
  have hp := congrArg pauli h
  change pauli (coordinates (C*(pauli x).transpose*C.conjTranspose)) =
    pauli (coordinates (C*(pauli y).transpose*C.conjTranspose)) at hp
  rw [pauli_coordinates (steered_hermitian C x),pauli_coordinates (steered_hermitian C y)] at hp
  have hct : IsUnit C.conjTranspose.det := by
    rw [Matrix.det_conjTranspose]
    exact hc.map (starRingEnd ℂ)
  have he := congrArg (fun N : Operator => C⁻¹*N) hp
  simp only [← Matrix.mul_assoc, Matrix.nonsing_inv_mul _ hc, one_mul] at he
  have he' : (pauli x).transpose=(pauli y).transpose := by
    have hr := congrArg (fun N : Operator => N*C.conjTranspose⁻¹) he
    simpa only [Matrix.mul_assoc, Matrix.mul_nonsing_inv _ hct, mul_one] using hr
  apply pauli_injective
  simpa using congrArg Matrix.transpose he'

def steeredFrame (C : Operator) (N : Fin 2 → POVM 3) : M :=
  matrixOfLinear ((steeringTransform C).comp (linearOfMatrix (measurementFrame N)))

theorem steeredFrame_effectRay (C : Operator) (N : Fin 2 → POVM 3)
    (hz : (N 0).effect 2=0) (x : Fin 2) (a : Fin 3) :
    steeredFrame C N *ᵥ effectRay x a=coordinates (C*((N x).effect a).transpose*C.conjTranspose) := by
  rw [steeredFrame,matrixOfLinear_mulVec,LinearMap.comp_apply,linearOfMatrix_apply,
    measurementFrame_effectRay N hz]
  simp [steeringTransform,pauli_coordinates ((N x).positive a).isHermitian]

theorem steeredFrame_invertible (C : Operator) (N : Fin 2 → POVM 3)
    (hC : IsUnit C.det) (hN : IsUnit (measurementFrame N).det) : IsUnit (steeredFrame C N).det := by
  apply matrix_det_unit_of_injective
  intro x y h
  simp only [steeredFrame,matrixOfLinear_mulVec,LinearMap.comp_apply,linearOfMatrix_apply] at h
  have hE := steeringTransform_injective C hC h
  have hi := congrArg (fun z => (measurementFrame N)⁻¹ *ᵥ z) hE
  simpa [Matrix.mulVec_mulVec,Matrix.nonsing_inv_mul _ hN] using hi

end Bell
