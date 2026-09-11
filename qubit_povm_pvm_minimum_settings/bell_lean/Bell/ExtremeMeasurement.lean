import Bell.StrategyMaps

/-!
# Extremality forces independent rank-one local effects

These are consequences of extremality of the COMPLETE behavior, not of an
unproved choice of extremal measurements. Full Schmidt rank makes every
nonzero effect's marginal positive, detecting each scalar perturbation.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder Topology
namespace Bell
open QubitGeometry Lorentz

abbrev EffectSupport {n : ℕ} (M : POVM n) := {a : Fin n // M.effect a ≠ 0}

def DeterministicMeasurement {n : ℕ} (M : POVM n) : Prop :=
  ∃ a : Fin n, ∀ b, M.effect b = if b=a then 1 else 0

def POVM.perturb {n : ℕ} (M : POVM n) (D : Fin n → Operator) (t : ℝ)
    (hD : ∑ a, D a = 0) (hp : ∀ a, (M.effect a+t • D a).PosSemidef) : POVM n where
  effect a := M.effect a+t • D a
  positive := hp
  normalized := by rw [Finset.sum_add_distrib,← Finset.smul_sum,M.normalized,hD,smul_zero,add_zero]

def FullPureStrategy.remeasureAlice {A : Architecture} (s : FullPureStrategy A)
    (x : Fin A.aliceInputs) (M : POVM (A.aliceOutputs x)) : FullPureStrategy A where
  coefficient := s.coefficient
  coefficient_invertible := s.coefficient_invertible
  normalized := s.normalized
  alice := Function.update s.alice x M
  bob := s.bob

/-- A two-sided physical perturbation at an extreme behavior has zero marginal
derivative at every label, rather than only zero total Bell-score derivative. -/
theorem extreme_perturbation_marginals {A : Architecture} (s : FullPureStrategy A)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM A))
    (x : Fin A.aliceInputs) (y : Fin A.bobInputs)
    (D : Fin (A.aliceOutputs x) → Operator) (ε : ℝ) (hε : ε ≠ 0)
    (hD : ∑ a, D a = 0)
    (hp : ∀ a, ((s.alice x).effect a+ε • D a).PosSemidef)
    (hm : ∀ a, ((s.alice x).effect a-ε • D a).PosSemidef) :
    ∀ a, localTrace (D a) (s.coefficient*s.coefficient.conjTranspose) = 0 := by
  let p := s.remeasureAlice x ((s.alice x).perturb D ε hD hp)
  let m := s.remeasureAlice x ((s.alice x).perturb D (-ε) hD
    (fun a => by simpa [sub_eq_add_neg,neg_smul] using hm a))
  have hmid : (1/2 : ℝ) • p.behavior+(1/2 : ℝ) • m.behavior=s.behavior := by
    funext x' y' a b
    by_cases hx : x'=x
    · subst x'
      simp only [p,m,FullPureStrategy.remeasureAlice,FullPureStrategy.behavior,
        FullPureStrategy.toStrategy,Strategy.behavior,pureState,Function.update_self,POVM.perturb,
        Pi.add_apply,Pi.smul_apply,smul_eq_mul]
      rw [pureDensity_born,pureDensity_born,pureDensity_born]
      simp_rw [localTrace_comm _ (s.coefficient * ((s.bob y').effect b).transpose *
        s.coefficient.conjTranspose),map_add,map_smul,smul_eq_mul]
      ring
    · simp [p,m,FullPureStrategy.remeasureAlice,FullPureStrategy.behavior,
        FullPureStrategy.toStrategy,Strategy.behavior,Function.update_of_ne hx,
        Pi.add_apply,Pi.smul_apply,smul_eq_mul]
      ring
  have he := (extreme_midpoint hex
    (subset_convexHull ℝ _ ⟨p.toStrategy,rfl⟩)
    (subset_convexHull ℝ _ ⟨m.toStrategy,rfl⟩) hmid).1
  intro a
  have he' := congrArg (fun q : Behavior A => ∑ b, q x y a b) he
  have hp' := born_sum_bob p.toStrategy.state ((p.alice x).effect a) (p.bob y)
  have hs' := born_sum_bob s.toStrategy.state ((s.alice x).effect a) (s.bob y)
  change (∑ b, p.behavior x y a b) = _ at hp'
  change (∑ b, s.behavior x y a b) = _ at hs'
  change (∑ b, p.behavior x y a b) = ∑ b, s.behavior x y a b at he'
  rw [hp',hs'] at he'
  change born (pureDensity p.coefficient) ((p.alice x).effect a) 1 =
    born (pureDensity s.coefficient) ((s.alice x).effect a) 1 at he'
  simp only [p,FullPureStrategy.remeasureAlice,FullPureStrategy.toStrategy,pureState,
    Function.update_self,POVM.perturb,pureDensity_born,Matrix.transpose_one,mul_one] at he'
  simp_rw [localTrace_comm _ (s.coefficient*s.coefficient.conjTranspose),map_add,map_smul,
    smul_eq_mul] at he'
  have hz : ε * localTrace (s.coefficient*s.coefficient.conjTranspose) (D a) = 0 := by
    linarith
  rw [← localTrace_comm (D a)] at hz
  exact (mul_eq_zero.mp hz).resolve_left hε

/-- Scalar dependence of active effects contradicts complete-behavior extremality. -/
theorem extreme_scalar_relation {A : Architecture} (s : FullPureStrategy A)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM A))
    (x : Fin A.aliceInputs) (y : Fin A.bobInputs)
    (c : Fin (A.aliceOutputs x) → ℝ) (hc : ∑ a, c a • (s.alice x).effect a = 0) :
    ∀ a, (s.alice x).effect a ≠ 0 → c a=0 := by
  obtain ⟨ε,hε,_,_,hw⟩ := exists_positive_perturbation c
    (Matrix.PosDef.one : (1 : Operator).PosDef) (Matrix.isHermitian_zero : (0 : Operator).IsHermitian)
  have hp : ∀ a, ((s.alice x).effect a+ε • (c a • (s.alice x).effect a)).PosSemidef := by
    intro a
    have h := posSemidef_real_smul ((s.alice x).positive a) (hw a).1.le
    convert h using 1 <;> module
  have hm : ∀ a, ((s.alice x).effect a-ε • (c a • (s.alice x).effect a)).PosSemidef := by
    intro a
    have h := posSemidef_real_smul ((s.alice x).positive a) (hw a).2.le
    convert h using 1 <;> module
  have hz := extreme_perturbation_marginals s hex x y
    (fun a => c a • (s.alice x).effect a) ε hε.ne' hc hp hm
  intro a ha
  have h := hz a
  rw [localTrace_comm, map_smul, smul_eq_mul,localTrace_comm] at h
  exact (mul_eq_zero.mp h).resolve_right (full_pure_marginal_positive s x a ha).ne'

/-- Nonzero effects form an independent family in the four-dimensional real
space of Hermitian matrices. Zero effects do not count toward this dimension. -/
theorem extreme_effect_independent {A : Architecture} (s : FullPureStrategy A)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM A))
    (x : Fin A.aliceInputs) (y : Fin A.bobInputs) :
    LinearIndependent ℝ (fun a : EffectSupport (s.alice x) => coordinates ((s.alice x).effect a)) := by
  classical
  rw [Fintype.linearIndependent_iff]
  intro c hc a
  let d : Fin (A.aliceOutputs x) → ℝ := fun b => if h : (s.alice x).effect b ≠ 0 then c ⟨b,h⟩ else 0
  have hd : ∑ b, d b • (s.alice x).effect b = 0 := by
    have he := congrArg pauli hc
    simp only [map_sum,map_smul,pauli_coordinates ((s.alice x).positive _).isHermitian,map_zero] at he
    have he' : (∑ b, d b • (s.alice x).effect b) =
        ∑ b : EffectSupport (s.alice x), c b • (s.alice x).effect b := by
      have hsum : (∑ b ∈ Finset.univ.filter (fun b => (s.alice x).effect b ≠ 0),
          d b • (s.alice x).effect b) = ∑ b, d b • (s.alice x).effect b := by
        apply Finset.sum_subset (Finset.filter_subset _ _)
        intro b _ hb
        have hzero : (s.alice x).effect b = 0 := by simpa using hb
        simp [hzero]
      rw [← hsum, Finset.sum_subtype (p := fun b => (s.alice x).effect b ≠ 0) _ (by simp)]
      apply Finset.sum_congr rfl
      intro b _
      simp [d, b.property]
    exact he'.trans he
  have hz := extreme_scalar_relation s hex x y d hd a a.property
  simpa [d,a.property] using hz

/-- A full-rank effect forces a deterministic measurement. Otherwise the
neighboring nonzero effect supplies a two-sided detectable perturbation. -/
theorem extreme_fullrank_effect_deterministic {A : Architecture} (s : FullPureStrategy A)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM A))
    (x : Fin A.aliceInputs) (y : Fin A.bobInputs)
    (a : Fin (A.aliceOutputs x)) (hdet : ((s.alice x).effect a).det ≠ 0) :
    DeterministicMeasurement (s.alice x) := by
  classical
  let M := s.alice x
  have hpd : (M.effect a).PosDef := posDef_of_posSemidef_det_ne_zero (M.positive a) hdet
  have hz : ∀ b, b ≠ a → M.effect b = 0 := by
    intro b hba
    by_contra hbn
    obtain ⟨ε,hε,hp,hm,hw⟩ := exists_positive_perturbation (fun _ : Unit => (1 : ℝ))
      hpd (M.positive b).isHermitian
    let D : Fin (A.aliceOutputs x) → Operator := fun k =>
      (if k=a then M.effect b else 0) - (if k=b then M.effect b else 0)
    have hsum : ∑ k, D k=0 := by simp [D,Finset.sum_sub_distrib]
    have hplus : ∀ k, (M.effect k+ε • D k).PosSemidef := by
      intro k
      by_cases hka : k=a
      · subst k; simpa [D,Ne.symm hba] using hp.posSemidef
      by_cases hkb : k=b
      · subst k
        have ht := posSemidef_real_smul (M.positive b) (hw ()).2.le
        convert ht using 1 <;> simp [D,hba] <;> module
      · simpa [D,hka,hkb] using M.positive k
    have hminus : ∀ k, (M.effect k-ε • D k).PosSemidef := by
      intro k
      by_cases hka : k=a
      · subst k; simpa [D,Ne.symm hba] using hm.posSemidef
      by_cases hkb : k=b
      · subst k
        have ht := posSemidef_real_smul (M.positive b) (hw ()).1.le
        convert ht using 1 <;> simp [D,hba] <;> module
      · simpa [D,hka,hkb] using M.positive k
    have he := extreme_perturbation_marginals s hex x y D ε hε.ne' hsum hplus hminus a
    have hpos := full_pure_marginal_positive s x b hbn
    simp only [D,if_pos rfl,if_neg (Ne.symm hba),sub_zero] at he
    exact hpos.ne' he
  have haI : M.effect a=1 := by
    rw [← M.normalized,Finset.sum_eq_single a]
    · intro b _ hba; exact hz b hba
    · simp
  refine ⟨a, fun b => ?_⟩
  change M.effect b = if b = a then 1 else 0
  by_cases hba : b = a
  · simpa [hba] using haI
  · simpa [hba] using hz b hba

theorem extreme_nondeterministic_effects_null {A : Architecture} (s : FullPureStrategy A)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM A))
    (x : Fin A.aliceInputs) (y : Fin A.bobInputs)
    (hnd : ¬ DeterministicMeasurement (s.alice x)) :
    ∀ a, ((s.alice x).effect a).det=0 := by
  intro a
  by_contra hd
  exact hnd (extreme_fullrank_effect_deterministic s hex x y a hd)

end Bell
