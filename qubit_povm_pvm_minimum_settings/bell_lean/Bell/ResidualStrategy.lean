import Bell.ResidualEncoding

/-!
# From arbitrary labelled binary/ternary strategies to residual closure

This file supplies the physical hypotheses of `ResidualFrames` from actual
complex-qubit effects and an invertible pure-state coefficient. The recoding
map back to the original finite alphabets is applied to the *whole strategy*.
No local maximality, positive multiplier, or rank-case hypothesis is assumed
by the concluding obstruction theorem.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell
open Lorentz QubitGeometry

/-- Encoded labels strictly below the active count retain a nonzero effect. -/
theorem encodePOVM_below_nonzero {n : ℕ} (N : POVM n)
    (hc : Fintype.card (EffectSupport N) ≤ 3) (a : Fin 3)
    (ha : a.val < Fintype.card (EffectSupport N)) :
    (encodePOVM N hc).effect a ≠ 0 := by
  let i : Fin (Fintype.card (EffectSupport N)) := ⟨a.val,ha⟩
  have he := encodePOVM_cast N hc i
  have hai : Fin.castLE hc i=a := Fin.ext rfl
  rw [hai] at he
  rw [he]
  exact (activeEnumeration N i).property

/-- Removing zero effects and padding does not introduce full-rank effects. -/
theorem encodePOVM_null {n : ℕ} (N : POVM n)
    (hc : Fintype.card (EffectSupport N) ≤ 3) (hn : ∀ a, (N.effect a).det=0) :
    ∀ a, ((encodePOVM N hc).effect a).det=0 := by
  intro a
  rcases encodePOVM_effect_cases N hc a with hzero|⟨b,hb⟩
  · rw [hzero]; simp
  · rw [hb]; exact hn b

theorem steeredFrame_unit (C : Operator) (N : Fin 2 → POVM 3)
    (hz : (N 0).effect 2=0) :
    steeredFrame C N *ᵥ unitVector=coordinates (C*C.conjTranspose) := by
  rw [steeredFrame,matrixOfLinear_mulVec,LinearMap.comp_apply,linearOfMatrix_apply,
    measurementFrame_unit N hz]
  simp [steeringTransform,pauli_timeUnit]

theorem steeredFrame_ray (C : Operator) (N : Fin 2 → POVM 3)
    (hz : (N 0).effect 2=0) (j : Fin 5) :
    steeredFrame C N *ᵥ ray j=
      coordinates (C*((N (rayInput j)).effect (rayLabel j)).transpose*C.conjTranspose) := by
  have hr : effectRay (rayInput j) (rayLabel j)=ray j := by fin_cases j <;> rfl
  simpa only [hr] using steeredFrame_effectRay C N hz (rayInput j) (rayLabel j)

theorem steering_nonzero (C : Operator) (hc : IsUnit C.det)
    {N : Operator} (hN : N.IsHermitian) (hne : N ≠ 0) :
    C*N.transpose*C.conjTranspose ≠ 0 := by
  intro hzero
  have he : steeringTransform C (coordinates N)=steeringTransform C 0 := by
    simp [steeringTransform,pauli_coordinates hN,hzero]
  have hx := steeringTransform_injective C hc he
  have hp := congrArg pauli hx
  exact hne (by simpa [pauli_coordinates hN] using hp)

theorem localTrace_coordinates {A B : Operator} (hA : A.IsHermitian) (hB : B.IsHermitian) :
    localTrace A B=2*dotProduct (coordinates A) (coordinates B) := by
  have h := congrArg Complex.re (pauli_trace_product (coordinates A) (coordinates B))
  simpa only [pauli_coordinates hA,pauli_coordinates hB,Complex.ofReal_re] using h

/-- The actual Born table is precisely the declared coefficient table. -/
theorem pure_frame_behavior (s : FullPureStrategy binaryTernaryArchitecture)
    (hA : (s.alice 0).effect 2=0) (hB : (s.bob 0).effect 2=0) :
    tableOfBlock ((2 : ℝ) • ((measurementFrame s.alice).transpose *
      steeredFrame s.coefficient s.bob))=s.behavior := by
  funext x y a b
  rw [tableOfBlock_apply,matrixPair_smul_matrix]
  have hp := matrixPair_mul_frames (1 : M) (measurementFrame s.alice)
    (steeredFrame s.coefficient s.bob) (effectRay x a) (effectRay y b)
  have hp' : matrixPair ((measurementFrame s.alice).transpose *
        steeredFrame s.coefficient s.bob) (effectRay x a) (effectRay y b)=
      dotProduct (measurementFrame s.alice *ᵥ effectRay x a)
        (steeredFrame s.coefficient s.bob *ᵥ effectRay y b) := by
    simpa [matrixPair_apply] using hp.symm
  rw [hp',measurementFrame_effectRay s.alice hA,steeredFrame_effectRay s.coefficient s.bob hB,
    s.behavior_steered]
  exact (localTrace_coordinates ((s.alice x).positive a).isHermitian
    (s.steered_positive y b).isHermitian).symm

/-- Build the geometric residual data from actual effects. -/
def physicalResidualFrames (s : FullPureStrategy binaryTernaryArchitecture)
    (hzA : (s.alice 0).effect 2=0) (hzB : (s.bob 0).effect 2=0)
    (hiA : IsUnit (measurementFrame s.alice).det)
    (hiB : IsUnit (measurementFrame s.bob).det)
    (hnA : ∀ j, ((s.alice (rayInput j)).effect (rayLabel j)).det=0)
    (hnB : ∀ j, ((s.bob (rayInput j)).effect (rayLabel j)).det=0)
    (heA : ∀ j, (s.alice (rayInput j)).effect (rayLabel j) ≠ 0)
    (heB : ∀ j, (s.bob (rayInput j)).effect (rayLabel j) ≠ 0) : ResidualFrames where
  alice := measurementFrame s.alice
  steering := steeredFrame s.coefficient s.bob
  alice_invertible := hiA
  steering_invertible := steeredFrame_invertible _ _ s.coefficient_invertible hiB
  alice_unit := measurementFrame_unit _ hzA
  alice_null j := by
    rw [measurementFrame_ray _ hzA]
    exact positive_null_coordinates ((s.alice _).positive _) (heA j) (hnA j)
  steering_null j := by
    rw [steeredFrame_ray _ _ hzB]
    apply positive_null_coordinates (s.steered_positive _ _)
    · exact steering_nonzero _ s.coefficient_invertible ((s.bob _).positive _).isHermitian (heB j)
    · change (s.coefficient * ((s.bob (rayInput j)).effect (rayLabel j)).transpose *
        s.coefficient.conjTranspose).det = 0
      simp only [Matrix.det_mul,Matrix.det_transpose,hnB j,mul_zero,zero_mul]
  reduced_timelike := by
    rw [steeredFrame_unit _ _ hzB]
    exact positive_definite_coordinates s.reduced_definite
  normalized := by
    rw [measurementFrame_unit _ hzA,steeredFrame_unit _ _ hzB]
    have ht := congrArg Complex.re s.normalized
    simp [timeUnit,coordinates,dotProduct,Matrix.trace,Fin.sum_univ_succ] at ht ⊢
    linarith

theorem physicalResidualFrames_behavior
    (s : FullPureStrategy binaryTernaryArchitecture)
    (hzA : (s.alice 0).effect 2=0) (hzB : (s.bob 0).effect 2=0)
    (hiA : IsUnit (measurementFrame s.alice).det)
    (hiB : IsUnit (measurementFrame s.bob).det)
    (hnA : ∀ j, ((s.alice (rayInput j)).effect (rayLabel j)).det=0)
    (hnB : ∀ j, ((s.bob (rayInput j)).effect (rayLabel j)).det=0)
    (heA : ∀ j, (s.alice (rayInput j)).effect (rayLabel j) ≠ 0)
    (heB : ∀ j, (s.bob (rayInput j)).effect (rayLabel j) ≠ 0) :
    tableOfBlock (physicalResidualFrames s hzA hzB hiA hiB hnA hnB heA heB).block=s.behavior :=
  pure_frame_behavior s hzA hzB

/-- A complete labelled binary/ternary residual can never be a strict
extreme Bell maximizer above all PVM mixtures. -/
theorem no_strict_extreme_binary_ternary
    (AO BO : Fin 2 → ℕ) (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,AO,BO⟩))
    (hndA : ∀ x, ¬ DeterministicMeasurement (s.alice x))
    (hndB : ∀ y, ¬ DeterministicMeasurement (s.bob y))
    (dA dB : Fin 2)
    (hA2 : Fintype.card (EffectSupport (s.alice dA))=2)
    (hA3 : Fintype.card (EffectSupport (s.alice (otherInput dA)))=3)
    (hB2 : Fintype.card (EffectSupport (s.bob dB))=2)
    (hB3 : Fintype.card (EffectSupport (s.bob (otherInput dB)))=3)
    (f : Behavior ⟨2,2,AO,BO⟩ →ₗ[ℝ] ℝ)
    (hmax : ∀ q ∈ convexPOVM ⟨2,2,AO,BO⟩, f q ≤ f s.behavior)
    (hstrict : ∀ q ∈ convexPVM ⟨2,2,AO,BO⟩, f q < f s.behavior) : False := by
  classical
  have hcA : ∀ x, Fintype.card (EffectSupport (s.alice x)) ≤ 3 := by
    intro x
    fin_cases dA <;> fin_cases x <;> simp [otherInput] at hA2 hA3 ⊢ <;> omega
  have hcB : ∀ y, Fintype.card (EffectSupport (s.bob y)) ≤ 3 := by
    intro y
    fin_cases dB <;> fin_cases y <;> simp [otherInput] at hB2 hB3 ⊢ <;> omega
  let t := s.pad AO BO dA dB hcA hcB
  let T := paddingMap AO BO s dA dB hcA hcB
  have hswap : s.swap.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,BO,AO⟩) := by
    rw [s.swap_behavior]
    exact swap_extreme hex
  have hzA : (t.alice 0).effect 2=0 := by
    apply encodePOVM_above
    simpa [inputAt] using hA2.le
  have hzB : (t.bob 0).effect 2=0 := by
    apply encodePOVM_above
    simpa [inputAt] using hB2.le
  have hiA : IsUnit (measurementFrame t.alice).det :=
    encoded_frame_invertible AO BO s hex dA hA2 hA3 hcA
  have hiB : IsUnit (measurementFrame t.bob).det :=
    encoded_frame_invertible BO AO s.swap hswap dB hB2 hB3 hcB
  have hnA : ∀ j, ((t.alice (rayInput j)).effect (rayLabel j)).det=0 := by
    intro j
    exact encodePOVM_null _ _ (extreme_nondeterministic_effects_null s hex _ 0 (hndA _)) _
  have hnB : ∀ j, ((t.bob (rayInput j)).effect (rayLabel j)).det=0 := by
    intro j
    exact encodePOVM_null _ _ (extreme_nondeterministic_effects_null
      (A := ⟨2,2,BO,AO⟩) s.swap hswap _ 0 (hndB _)) _
  have heA : ∀ j, (t.alice (rayInput j)).effect (rayLabel j) ≠ 0 := by
    intro j
    apply encodePOVM_below_nonzero
    fin_cases j
    · change 0 < Fintype.card (EffectSupport (s.alice dA)); omega
    · change 1 < Fintype.card (EffectSupport (s.alice dA)); omega
    · change 0 < Fintype.card (EffectSupport (s.alice (otherInput dA))); omega
    · change 1 < Fintype.card (EffectSupport (s.alice (otherInput dA))); omega
    · change 2 < Fintype.card (EffectSupport (s.alice (otherInput dA))); omega
  have heB : ∀ j, (t.bob (rayInput j)).effect (rayLabel j) ≠ 0 := by
    intro j
    apply encodePOVM_below_nonzero
    fin_cases j
    · change 0 < Fintype.card (EffectSupport (s.bob dB)); omega
    · change 1 < Fintype.card (EffectSupport (s.bob dB)); omega
    · change 0 < Fintype.card (EffectSupport (s.bob (otherInput dB))); omega
    · change 1 < Fintype.card (EffectSupport (s.bob (otherInput dB))); omega
    · change 2 < Fintype.card (EffectSupport (s.bob (otherInput dB))); omega
  let r := physicalResidualFrames t hzA hzB hiA hiB hnA hnB heA heB
  have heq : T.behavior (tableOfBlock r.block)=s.behavior := by
    rw [physicalResidualFrames_behavior]
    exact paddingMap_behavior AO BO s dA dB hcA hcB
  apply r.not_strict_maximum (f.comp T.behavior)
  · intro q hq
    change f (T.behavior q) ≤ f (T.behavior (tableOfBlock r.block))
    rw [heq]
    exact hmax _ (subset_convexHull ℝ _ (T.mem_rawPOVM hq))
  · intro q hq
    change f (T.behavior q) < f (T.behavior (tableOfBlock r.block))
    rw [heq]
    exact hstrict _ (T.mem_convexPVM hq)

end Bell
