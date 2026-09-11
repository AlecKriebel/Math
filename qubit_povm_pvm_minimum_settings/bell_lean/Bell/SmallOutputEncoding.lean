import Bell.MeasurementSpans
import Bell.OneInput

/-!
# Removing zero effects and retaining the original labels

Every measurement with at most three active effects is encoded by a three-label
POVM and an explicit deterministic output map back. This map includes the
unused binary third label and preserves actual PVMs on every input strategy.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell
open Lorentz QubitGeometry

/-- Measurement equality is determined by its complete effect family. -/
theorem POVM.ext_effect {n : ℕ} {M N : POVM n} (h : M.effect = N.effect) : M = N := by
  cases M
  cases N
  cases h
  rfl

theorem coarsenPOVM_comp {l m n : ℕ} (M : POVM l) (f : Fin l → Fin m) (g : Fin m → Fin n)
    (a : Fin n) : (coarsenPOVM (coarsenPOVM M f) g).effect a=(coarsenPOVM M (g ∘ f)).effect a := by
  classical
  simp only [coarsenPOVM]
  have he : (∑ b, if g b=a then ∑ c, if f c=b then M.effect c else 0 else 0)=
      ∑ c, ∑ b, if g b=a ∧ f c=b then M.effect c else 0 := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro b _
    by_cases hb : g b=a <;> simp [hb]
  rw [he]
  apply Finset.sum_congr rfl
  intro c _
  rw [Finset.sum_eq_single (f c)]
  · simp [Function.comp_apply]
  · intro b _ hb
    simp [Ne.symm hb]
  · simp

theorem coarsenPOVM_id {n : ℕ} (M : POVM n) (a : Fin n) :
    (coarsenPOVM M id).effect a=M.effect a := by simp [coarsenPOVM]

theorem coarsenPOVM_const {m n : ℕ} (M : POVM m) (a b : Fin n) :
    (coarsenPOVM M (fun _ => a)).effect b=if b=a then 1 else 0 := by
  by_cases hab : b=a
  · subst b; simp [coarsenPOVM,M.normalized]
  · simp [coarsenPOVM,hab,Ne.symm hab]

theorem activeSupport_nonempty {n : ℕ} (M : POVM n) : Nonempty (EffectSupport M) := by
  classical
  by_contra hn
  have hz : ∀ a, M.effect a=0 := by
    intro a
    by_contra ha
    exact hn ⟨⟨a,ha⟩⟩
  have hc := congrArg (fun N : Operator => N 0 0) M.normalized
  simp [hz] at hc

def activeEnumeration {n : ℕ} (M : POVM n) : Fin (Fintype.card (EffectSupport M)) ≃ EffectSupport M :=
  (Fintype.equivFin (EffectSupport M)).symm

def activePOVM {n : ℕ} (M : POVM n) : POVM (Fintype.card (EffectSupport M)) where
  effect i := M.effect (activeEnumeration M i)
  positive i := M.positive _
  normalized := by
    classical
    rw [Equiv.sum_comp (activeEnumeration M) (fun a : EffectSupport M => M.effect a)]
    have h := Fintype.sum_subtype_add_sum_subtype (fun a => M.effect a ≠ 0) M.effect
    have hz (a : {a : Fin n // ¬ M.effect a ≠ 0}) : M.effect a = 0 := not_not.mp a.property
    simpa only [hz, Finset.sum_const_zero, add_zero] using h.trans M.normalized

def encodePOVM {n : ℕ} (M : POVM n) (hc : Fintype.card (EffectSupport M) ≤ 3) : POVM 3 :=
  coarsenPOVM (activePOVM M) (Fin.castLE hc)

def encodingLabel {n : ℕ} (M : POVM n) (hc : Fintype.card (EffectSupport M) ≤ 3)
    (a : Fin 3) : Fin n :=
  if h : a.val < Fintype.card (EffectSupport M) then (activeEnumeration M ⟨a.val,h⟩).val
  else (activeEnumeration M ⟨0,by
    letI : Nonempty (EffectSupport M) := activeSupport_nonempty M
    exact Fintype.card_pos⟩).val

theorem encodingLabel_cast {n : ℕ} (M : POVM n) (hc : Fintype.card (EffectSupport M) ≤ 3)
    (a : Fin (Fintype.card (EffectSupport M))) :
    encodingLabel M hc (Fin.castLE hc a)=(activeEnumeration M a).val := by
  simp only [encodingLabel, Fin.coe_castLE, dif_pos a.isLt]

theorem encodePOVM_cast {n : ℕ} (M : POVM n) (hc : Fintype.card (EffectSupport M) ≤ 3)
    (a : Fin (Fintype.card (EffectSupport M))) :
    (encodePOVM M hc).effect (Fin.castLE hc a)=M.effect (activeEnumeration M a) := by
  classical
  change (∑ b, if Fin.castLE hc b = Fin.castLE hc a then
    (activePOVM M).effect b else 0) = _
  rw [Finset.sum_eq_single a]
  · simp [activePOVM]
  · intro b _ hba
    have hn : Fin.castLE hc b ≠ Fin.castLE hc a := by
      intro he
      apply hba
      exact Fin.ext (congrArg (fun i : Fin 3 => i.val) he)
    simp [hn]
  · simp

theorem encodePOVM_above {n : ℕ} (M : POVM n) (hc : Fintype.card (EffectSupport M) ≤ 3)
    (a : Fin 3) (ha : Fintype.card (EffectSupport M) ≤ a.val) :
    (encodePOVM M hc).effect a=0 := by
  classical
  change (∑ b, if Fin.castLE hc b = a then (activePOVM M).effect b else 0) = 0
  apply Finset.sum_eq_zero
  intro b _
  have hn : Fin.castLE hc b ≠ a := by
    intro he
    have hv := congrArg Fin.val he
    have hb := b.isLt
    simp only [Fin.coe_castLE] at hv
    omega
  simp [hn]

theorem encoding_coarsens {n : ℕ} (M : POVM n) (hc : Fintype.card (EffectSupport M) ≤ 3)
    (a : Fin n) : (coarsenPOVM (encodePOVM M hc) (encodingLabel M hc)).effect a=M.effect a := by
  classical
  rw [encodePOVM,coarsenPOVM_comp]
  change (∑ b, if encodingLabel M hc (Fin.castLE hc b)=a then M.effect (activeEnumeration M b) else 0)=_
  simp_rw [encodingLabel_cast]
  rw [Equiv.sum_comp (activeEnumeration M)
    (fun b : EffectSupport M => if b.val = a then M.effect b else 0)]
  rw [← Finset.sum_subtype (p := fun b => M.effect b ≠ 0)
    (Finset.univ.filter (fun b => M.effect b ≠ 0)) (by simp)
    (fun b => if b = a then M.effect b else 0)]
  by_cases ha : M.effect a = 0 <;> simp [ha]

/-- Every encoded effect is either zero or one of the original active effects. -/
theorem encodePOVM_effect_cases {n : ℕ} (M : POVM n) (hc : Fintype.card (EffectSupport M) ≤ 3)
    (a : Fin 3) : (encodePOVM M hc).effect a=0 ∨
      ∃ b : EffectSupport M, (encodePOVM M hc).effect a=M.effect b := by
  by_cases ha : a.val < Fintype.card (EffectSupport M)
  · let b : Fin (Fintype.card (EffectSupport M)) := ⟨a.val,ha⟩
    right
    refine ⟨activeEnumeration M b, ?_⟩
    have he := encodePOVM_cast M hc b
    simpa only [show Fin.castLE hc b=a from Fin.ext rfl] using he
  · left
    exact encodePOVM_above M hc a (le_of_not_gt ha)

/-- Ordering a pair of inputs by which one has binary active support. -/
def inputAt (d x : Fin 2) : Fin 2 := if x=0 then d else otherInput d
def inputIndex (d x : Fin 2) : Fin 2 := if x=d then 0 else 1

@[simp] theorem inputAt_index (d x : Fin 2) : inputAt d (inputIndex d x)=x := by
  fin_cases d <;> fin_cases x <;> norm_num [inputAt,inputIndex,otherInput]
@[simp] theorem inputIndex_at (d x : Fin 2) : inputIndex d (inputAt d x)=x := by
  fin_cases d <;> fin_cases x <;> norm_num [inputAt,inputIndex,otherInput]

/-- A deterministic Alice input in a two-input architecture is a coarsening of
an actual one-input behavior. Its other input may have any finite output count. -/
theorem deterministic_alice_local (AO BO : Fin 2 → ℕ) (s : Strategy ⟨2,2,AO,BO⟩)
    (d : Fin 2) (hd : DeterministicMeasurement (s.alice d)) :
    s.behavior ∈ convexPVM ⟨2,2,AO,BO⟩ := by
  obtain ⟨label,hlabel⟩ := hd
  fin_cases d
  · change ∀ b : Fin (AO 0), (s.alice 0).effect b = if b = label then 1 else 0 at hlabel
    let B : Architecture := ⟨1,2,fun _ => AO 1,BO⟩
    let t : Strategy B := ⟨s.state,fun _ => s.alice 1,s.bob⟩
    let T : StrategyMap B ⟨2,2,AO,BO⟩ :=
      { aliceInput := fun _ => 0
        bobInput := id
        aliceOutput := Fin.cases (fun _ => label) (Fin.cases id (fun i => Fin.elim0 i))
        bobOutput := fun _ => id }
    have hp := T.mem_convexPVM (strategy_one_input t (Or.inl (by change 1 ≤ 1; omega)))
    rw [← T.strategy_behavior t] at hp
    have he : (T.strategy t).behavior=s.behavior := by
      funext x y a b
      fin_cases x
      · change born s.state.density
          ((coarsenPOVM (s.alice 1) (fun _ => label)).effect a)
          ((coarsenPOVM (s.bob y) id).effect b) =
          born s.state.density ((s.alice 0).effect a) ((s.bob y).effect b)
        rw [coarsenPOVM_const, coarsenPOVM_id, hlabel]
      · change born s.state.density
          ((coarsenPOVM (s.alice 1) id).effect a)
          ((coarsenPOVM (s.bob y) id).effect b) =
          born s.state.density ((s.alice 1).effect a) ((s.bob y).effect b)
        simp only [coarsenPOVM_id]
    rw [he] at hp
    exact hp
  · change ∀ b : Fin (AO 1), (s.alice 1).effect b = if b = label then 1 else 0 at hlabel
    let B : Architecture := ⟨1,2,fun _ => AO 0,BO⟩
    let t : Strategy B := ⟨s.state,fun _ => s.alice 0,s.bob⟩
    let T : StrategyMap B ⟨2,2,AO,BO⟩ :=
      { aliceInput := fun _ => 0
        bobInput := id
        aliceOutput := Fin.cases id (Fin.cases (fun _ => label) (fun i => Fin.elim0 i))
        bobOutput := fun _ => id }
    have hp := T.mem_convexPVM (strategy_one_input t (Or.inl (by change 1 ≤ 1; omega)))
    rw [← T.strategy_behavior t] at hp
    have he : (T.strategy t).behavior=s.behavior := by
      funext x y a b
      fin_cases x
      · change born s.state.density
          ((coarsenPOVM (s.alice 0) id).effect a)
          ((coarsenPOVM (s.bob y) id).effect b) =
          born s.state.density ((s.alice 0).effect a) ((s.bob y).effect b)
        simp only [coarsenPOVM_id]
      · change born s.state.density
          ((coarsenPOVM (s.alice 0) (fun _ => label)).effect a)
          ((coarsenPOVM (s.bob y) id).effect b) =
          born s.state.density ((s.alice 1).effect a) ((s.bob y).effect b)
        rw [coarsenPOVM_const, coarsenPOVM_id, hlabel]
    rw [he] at hp
    exact hp

theorem deterministic_bob_local (AO BO : Fin 2 → ℕ) (s : Strategy ⟨2,2,AO,BO⟩)
    (d : Fin 2) (hd : DeterministicMeasurement (s.bob d)) :
    s.behavior ∈ convexPVM ⟨2,2,AO,BO⟩ := by
  have hp := deterministic_alice_local BO AO (swapStrategy s) d hd
  have hs := swap_mem_convexPVM hp
  rw [swapStrategy_behavior] at hs
  exact hs

end Bell
