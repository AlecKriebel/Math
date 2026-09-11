import Bell.CommonSpanFiltering

/-! # The four-dimensional common-span count

The active-effect span is the range of an explicit coefficient map. Its rank
is the number of active outcomes at an extreme full-Schmidt-rank behavior.
Common-span filtering bounds each party's total active outcomes by five.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell
open Lorentz QubitGeometry

def activeEffectMap {n : ℕ} (M : POVM n) : (EffectSupport M → ℝ) →ₗ[ℝ] V where
  toFun c := ∑ a, c a • coordinates (M.effect a)
  map_add' := by intros; simp [add_smul,Finset.sum_add_distrib]
  map_smul' := by intros; simp [mul_smul,Finset.smul_sum]

def effectSpan {n : ℕ} (M : POVM n) : Submodule ℝ V := LinearMap.range (activeEffectMap M)

def extendActiveCoefficients {n : ℕ} (M : POVM n) (c : EffectSupport M → ℝ) : Fin n → ℝ :=
  fun a => if h : M.effect a ≠ 0 then c ⟨a,h⟩ else 0

theorem active_coefficients_operator {n : ℕ} (M : POVM n) (c : EffectSupport M → ℝ) :
    ∑ a, extendActiveCoefficients M c a • M.effect a = pauli (activeEffectMap M c) := by
  classical
  change (∑ a, extendActiveCoefficients M c a • M.effect a) =
    pauli (∑ a : EffectSupport M, c a • coordinates (M.effect a))
  simp only [map_sum, map_smul, pauli_coordinates (M.positive _).isHermitian]
  have h := Fintype.sum_subtype_add_sum_subtype (fun a => M.effect a ≠ 0)
    (fun a => extendActiveCoefficients M c a • M.effect a)
  have hp (a : EffectSupport M) :
      extendActiveCoefficients M c a • M.effect a = c a • M.effect a := by
    simp only [extendActiveCoefficients, dif_pos a.property]
  have hn (a : {a : Fin n // ¬ M.effect a ≠ 0}) :
      extendActiveCoefficients M c a • M.effect a = 0 := by
    simp only [extendActiveCoefficients, dif_neg a.property, zero_smul]
  simpa only [hp, hn, Finset.sum_const_zero, add_zero] using h.symm

theorem coefficient_sum_mem_span {n : ℕ} (M : POVM n) (c : Fin n → ℝ) :
    ∑ a, c a • coordinates (M.effect a) ∈ effectSpan M := by
  classical
  refine ⟨fun a => c a, ?_⟩
  change (∑ a : EffectSupport M, c a • coordinates (M.effect a)) = _
  have h := Fintype.sum_subtype_add_sum_subtype (fun a => M.effect a ≠ 0)
    (fun a => c a • coordinates (M.effect a))
  have hz : ∀ a : {a : Fin n // ¬ M.effect a ≠ 0}, c a • coordinates (M.effect a) = 0 := by
    intro a
    simp [not_not.mp a.property]
  simpa only [hz, Finset.sum_const_zero, add_zero] using h

theorem effect_coordinates_mem_span {n : ℕ} (M : POVM n) (a : Fin n) :
    coordinates (M.effect a) ∈ effectSpan M := by
  classical
  simpa [Pi.single_apply, ite_smul] using coefficient_sum_mem_span M (Pi.single a 1)

theorem timeUnit_mem_effectSpan {n : ℕ} (M : POVM n) : timeUnit ∈ effectSpan M := by
  have h := coefficient_sum_mem_span M (fun _ => 1)
  simpa only [one_smul,← map_sum,M.normalized,← pauli_timeUnit,coordinates_pauli] using h

theorem effectSpan_finrank_of_independent {n : ℕ} (M : POVM n)
    (hind : LinearIndependent ℝ (fun a : EffectSupport M => coordinates (M.effect a))) :
    Module.finrank ℝ (effectSpan M) = Fintype.card (EffectSupport M) := by
  have hinj : Function.Injective (activeEffectMap M) := by
    intro c d h
    have hz : ∑ a, (c a-d a) • coordinates (M.effect a)=0 := by
      simp only [sub_smul,Finset.sum_sub_distrib]
      exact sub_eq_zero.mpr h
    have he := Fintype.linearIndependent_iff.mp hind _ hz
    funext a
    exact sub_eq_zero.mp (he a)
  simpa only [effectSpan,Module.finrank_fintype_fun_eq_card] using
    (LinearMap.finrank_range_of_inj hinj)

theorem nondeterministic_support_at_least_two {n : ℕ} (M : POVM n)
    (hnd : ¬ DeterministicMeasurement M) : 2 ≤ Fintype.card (EffectSupport M) := by
  classical
  by_contra! hc
  have hsub : Subsingleton (EffectSupport M) := (Fintype.card_le_one_iff_subsingleton).mp (by omega)
  have hne : Nonempty (EffectSupport M) := by
    by_contra hn
    have hz : ∀ a, M.effect a=0 := by
      intro a
      by_contra ha
      exact hn ⟨⟨a,ha⟩⟩
    have he := congrArg (fun A : Operator => A 0 0) M.normalized
    simp [hz] at he
  obtain ⟨a⟩ := hne
  have hz : ∀ b, b ≠ a.val → M.effect b=0 := by
    intro b hb
    by_contra hbn
    exact hb (congrArg Subtype.val (hsub.elim ⟨b,hbn⟩ a))
  have ha : M.effect a=1 := by
    have hsum : ∑ b, M.effect b=M.effect a := by
      apply Finset.sum_eq_single a.val
      · intro b _ hb; exact hz b hb
      · simp
    exact hsum.symm.trans M.normalized
  apply hnd
  exact ⟨a,fun b => by by_cases hb : b=a.val <;> simp [hb,hz,ha]⟩

/-- For two inputs, the intersection of active-effect spans has dimension at
most one. Its scalar generator is the identity, not a numerical tolerance. -/
theorem extreme_span_intersection_le_one
    (AO BO : Fin 2 → ℕ) (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,AO,BO⟩)) :
    Module.finrank ℝ ↥(effectSpan (s.alice 0) ⊓ effectSpan (s.alice 1)) ≤ 1 := by
  classical
  let S := effectSpan (s.alice 0) ⊓ effectSpan (s.alice 1)
  have hv : ∀ v : S, (v : V)=(v : V) 0 • timeUnit := by
    intro v
    obtain ⟨c0,hc0⟩ := v.property.1
    obtain ⟨c1,hc1⟩ := v.property.2
    let c : (x : Fin 2) → Fin (AO x) → ℝ :=
      Fin.cases (extendActiveCoefficients (s.alice 0) c0)
        (Fin.cases (extendActiveCoefficients (s.alice 1) c1) (fun i => Fin.elim0 i))
    have hcommon : ∀ x, ∑ a, c x a • (s.alice x).effect a=pauli v := by
      intro x
      fin_cases x
      · change (∑ a, extendActiveCoefficients (s.alice 0) c0 a • (s.alice 0).effect a)=_
        rw [active_coefficients_operator,hc0]
      · change (∑ a, extendActiveCoefficients (s.alice 1) c1 a • (s.alice 1).effect a)=_
        rw [active_coefficients_operator,hc1]
    have hs := extreme_common_span_scalar s hex 0 0 c (pauli v) (pauli_isHermitian v) hcommon
    have he := congrArg coordinates hs
    rw [coordinates_pauli,map_smul,← pauli_timeUnit,coordinates_pauli] at he
    have ht := congrFun he 0
    simp only [Pi.smul_apply, smul_eq_mul, timeUnit, Matrix.cons_val_zero, mul_one] at ht
    rw [← ht] at he
    exact he
  let f : S →ₗ[ℝ] ℝ := (LinearMap.proj 0).comp S.subtype
  have hinj : Function.Injective f := by
    intro u v h
    apply Subtype.ext
    rw [hv u,hv v]
    exact congrArg (fun t : ℝ => t • timeUnit) h
  simpa using LinearMap.finrank_le_finrank_of_injective hinj

theorem extreme_active_outcome_sum_le_five
    (AO BO : Fin 2 → ℕ) (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,AO,BO⟩)) :
    Fintype.card (EffectSupport (s.alice 0))+Fintype.card (EffectSupport (s.alice 1)) ≤ 5 := by
  have hdim := (effectSpan (s.alice 0)).finrank_sup_add_finrank_inf_eq (effectSpan (s.alice 1))
  have hsup := (effectSpan (s.alice 0) ⊔ effectSpan (s.alice 1)).finrank_le
  have hinf := extreme_span_intersection_le_one AO BO s hex
  rw [effectSpan_finrank_of_independent _ (extreme_effect_independent s hex 0 0),
    effectSpan_finrank_of_independent _ (extreme_effect_independent s hex 1 0)] at hdim
  have hV : Module.finrank ℝ V=4 := by simp [V]
  rw [hV] at hsup
  omega

theorem extreme_two_or_three_outcomes
    (AO BO : Fin 2 → ℕ) (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,AO,BO⟩))
    (hnd : ∀ x, ¬ DeterministicMeasurement (s.alice x)) :
    (∀ x, Fintype.card (EffectSupport (s.alice x))=2 ∨
          Fintype.card (EffectSupport (s.alice x))=3) ∧
      ∃ x, Fintype.card (EffectSupport (s.alice x))=2 := by
  have hsum := extreme_active_outcome_sum_le_five AO BO s hex
  have h0 := nondeterministic_support_at_least_two (s.alice 0) (hnd 0)
  have h1 := nondeterministic_support_at_least_two (s.alice 1) (hnd 1)
  constructor
  · intro x
    fin_cases x
    · change Fintype.card (EffectSupport (s.alice 0)) = 2 ∨
        Fintype.card (EffectSupport (s.alice 0)) = 3
      omega
    · change Fintype.card (EffectSupport (s.alice 1)) = 2 ∨
        Fintype.card (EffectSupport (s.alice 1)) = 3
      omega
  · by_cases h : Fintype.card (EffectSupport (s.alice 0))=2
    · exact ⟨0,h⟩
    · exact ⟨1,by omega⟩

end Bell
