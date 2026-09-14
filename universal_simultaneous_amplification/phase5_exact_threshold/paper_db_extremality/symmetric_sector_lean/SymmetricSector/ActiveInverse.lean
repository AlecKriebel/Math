import SymmetricSector.Incoming
import SymmetricSector.MarkovInverse

namespace SymmetricSector.Active
noncomputable section
open scoped BigOperators

@[simp] theorem K0_row_sum {n : ℕ} (hn : 2 ≤ n) (y : State n) :
    ∑ z, K0 n y z = 1 := by
  have h := K0_rank hn (fun _ => 1) y
  simpa [Matrix.mulVec, dotProduct] using h

theorem K0_nonneg {n : ℕ} (y z : State n) : 0 ≤ K0 n y z := by
  unfold K0 kernel complete
  positivity

theorem K0_continue_pos {n : ℕ} (hn : 2 ≤ n) (y : State n) (i : Fin n)
    (hi : i ≠ y.target) :
    0 < K0 n y (sampled y.cache y.target i y.property.2 hi) := by
  have hp : 0 < complete n y.target i := by
    simp only [complete, if_neg hi.symm]
    exact one_div_pos.mpr (complete_denominator_pos hn)
  have hs : 0 < ∑ j : Fin n,
      if j ≠ y.target ∧
          (sampled y.cache y.target i y.property.2 hi).cache = insert j y.cache ∧
          (sampled y.cache y.target i y.property.2 hi).target = y.target
        then complete n y.target j else 0 := by
    apply lt_of_lt_of_le hp
    have h := Finset.single_le_sum (f := fun j =>
      if j ≠ y.target ∧
          (sampled y.cache y.target i y.property.2 hi).cache = insert j y.cache ∧
          (sampled y.cache y.target i y.property.2 hi).target = y.target
        then complete n y.target j else 0)
      (a := i) (s := Finset.univ)
      (fun j hj => by unfold complete; positivity) (Finset.mem_univ i)
    simpa [sampled, hi] using h
  unfold K0 kernel
  have hstop : 0 ≤ (1 / (2 * (y.rank : ℝ))) *
      (∑ w ∈ y.cache, ∑ j : Fin n,
        if j ≠ w ∧
            (sampled y.cache y.target i y.property.2 hi).cache = insert j (y.cache.erase w) ∧
            (sampled y.cache y.target i y.property.2 hi).target = w
          then complete n w j else 0) := by
    unfold complete
    positivity
  linarith

theorem K0_stop_pos {n : ℕ} (hn : 2 ≤ n) (y : State n) (w i : Fin n)
    (hw : w ∈ y.cache) (hi : i ≠ w) :
    0 < K0 n y (sampled (y.cache.erase w) w i (Finset.not_mem_erase w _) hi) := by
  let z := sampled (y.cache.erase w) w i (Finset.not_mem_erase w _) hi
  have hp : 0 < complete n w i := by
    simp only [complete, if_neg hi.symm]
    exact one_div_pos.mpr (complete_denominator_pos hn)
  have hs : 0 < ∑ v ∈ y.cache, ∑ j : Fin n,
      if j ≠ v ∧ z.cache = insert j (y.cache.erase v) ∧ z.target = v
        then complete n v j else 0 := by
    apply lt_of_lt_of_le hp
    have hinner : complete n w i ≤ ∑ j : Fin n,
        if j ≠ w ∧ z.cache = insert j (y.cache.erase w) ∧ z.target = w
          then complete n w j else 0 := by
      have h := Finset.single_le_sum (s := Finset.univ) (a := i)
        (f := fun j => if j ≠ w ∧ z.cache = insert j (y.cache.erase w) ∧ z.target = w
          then complete n w j else 0) (fun j hj => by unfold complete; positivity)
        (Finset.mem_univ i)
      simpa [z, sampled, hi] using h
    refine hinner.trans ?_
    apply Finset.single_le_sum (s := y.cache) (a := w)
      (f := fun v => ∑ j : Fin n,
        if j ≠ v ∧ z.cache = insert j (y.cache.erase v) ∧ z.target = v
          then complete n v j else 0)
    · intro v hv
      apply Finset.sum_nonneg
      intro j hj
      unfold complete
      positivity
    · exact hw
  have hc : 0 ≤ (1 / 2 : ℝ) * (∑ j : Fin n,
      if j ≠ y.target ∧ z.cache = insert j y.cache ∧ z.target = y.target
        then complete n y.target j else 0) := by unfold complete; positivity
  change 0 < _ + (1 / (2 * (y.rank : ℝ))) * _
  exact add_pos_of_nonneg_of_pos hc (mul_pos (one_div_pos.mpr (retarget_denominator_pos y)) hs)

/-- A harmonic function attaining its maximum propagates that value across
every actual transition of positive probability. -/
theorem harmonic_max_successor {n : ℕ} (hn : 2 ≤ n) (f : State n → ℝ)
    (hf : (K0 n).mulVec f = f) (y z : State n)
    (hy : ∀ u, f u ≤ f y) (hp : 0 < K0 n y z) : f z = f y := by
  have hsum : ∑ u, K0 n y u * (f y - f u) = 0 := by
    simp only [mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul, K0_row_sum hn, one_mul]
    have hh := congrFun hf y
    change (∑ u, K0 n y u * f u) = f y at hh
    rw [hh, sub_self]
  have hterm := (Finset.sum_eq_zero_iff_of_nonneg
    (fun u (_ : u ∈ Finset.univ) => mul_nonneg (K0_nonneg y u) (sub_nonneg.mpr (hy u)))).mp hsum
    z (Finset.mem_univ z)
  have hz : f y - f z = 0 := (mul_eq_zero.mp hterm).resolve_left (ne_of_gt hp)
  linarith

/-- The unique maximal-cache state with the given target. -/
def fullState {n : ℕ} (hn : 2 ≤ n) (v : Fin n) : State n :=
  ⟨(Finset.univ.erase v, v), by
    constructor
    · apply Finset.card_pos.mp
      simp
      omega
    · exact Finset.not_mem_erase _ _⟩

@[simp] theorem fullState_target {n : ℕ} (hn : 2 ≤ n) (v : Fin n) :
    (fullState hn v).target = v := rfl

@[simp] theorem fullState_rank {n : ℕ} (hn : 2 ≤ n) (v : Fin n) :
    (fullState hn v).rank = n - 1 := by simp [fullState, State.rank, State.cache]

theorem eq_fullState {n : ℕ} (hn : 2 ≤ n) (y : State n) (hk : y.rank = n - 1) :
    y = fullState hn y.target := by
  apply Subtype.ext
  exact Prod.ext (full_rank_cache y hk) rfl

/-- Concrete connectivity proof for the actual active chain. A function equal
along its positive transitions is constant: continue moves fill every cache,
and one stop move connects any two distinct maximal-cache targets. -/
theorem constant_of_positive_moves {n : ℕ} (hn : 2 ≤ n) (f : State n → ℝ)
    (heq : ∀ y z, 0 < K0 n y z → f y = f z) : ∀ y z, f y = f z := by
  have hreach : ∀ d, ∀ y : State n, n - 1 - y.rank = d →
      f y = f (fullState hn y.target) := by
    intro d
    induction d using Nat.strong_induction_on with
    | h d ih =>
      intro y hd
      by_cases hfull : y.rank = n - 1
      · exact congrArg f (eq_fullState hn y hfull)
      · have hex : ∃ i : Fin n, i ≠ y.target ∧ i ∉ y.cache := by
          by_contra hh
          push_neg at hh
          have hsub : Finset.univ.erase y.target ⊆ y.cache := by
            intro i hi
            exact hh i (Finset.mem_erase.mp hi).1
          have hcard := Finset.card_le_card hsub
          have hyr := rank_le y
          simp only [Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ,
            Fintype.card_fin] at hcard
          change n - 1 ≤ y.rank at hcard
          omega
        obtain ⟨i, hiv, hiC⟩ := hex
        let z := sampled y.cache y.target i y.property.2 hiv
        have hzrank : z.rank = y.rank + 1 := by
          rw [sampled_rank, if_neg hiC]
        have hlt : n - 1 - z.rank < d := by
          have hyr := rank_le y
          rw [hzrank]
          omega
        have hz := ih (n - 1 - z.rank) hlt z rfl
        calc
          f y = f z := heq y z (K0_continue_pos hn y i hiv)
          _ = f (fullState hn y.target) := hz
  have htop : ∀ v w : Fin n, f (fullState hn v) = f (fullState hn w) := by
    intro v w
    by_cases h : v = w
    · rw [h]
    · have hw : w ∈ (fullState hn v).cache := by
        simp only [fullState, State.cache, Finset.mem_erase, Finset.mem_univ, and_true]
        exact Ne.symm h
      have hp := K0_stop_pos hn (fullState hn v) w v hw h
      have hz : sampled ((fullState hn v).cache.erase w) w v
          (Finset.not_mem_erase w _) h = fullState hn w := by
        apply Subtype.ext
        apply Prod.ext
        · change insert v ((Finset.univ.erase v).erase w) = Finset.univ.erase w
          ext i
          by_cases hiv : i = v
          · subst i; simp [h]
          · simp [hiv]
        · rfl
      rw [hz] at hp
      exact heq _ _ hp
  intro y z
  exact (hreach _ y rfl).trans ((htop _ _).trans (hreach _ z rfl).symm)

#print axioms K0_row_sum
#print axioms K0_continue_pos
#print axioms K0_stop_pos
#print axioms constant_of_positive_moves

theorem nu0_pos {n : ℕ} (hn : 2 ≤ n) (y : State n) : 0 < nu0 y := by
  exact div_pos (by exact_mod_cast rank_pos y) (nu0_denominator_pos hn)

/-- Every harmonic function for the actual complete active chain is constant.
The stationary energy argument and concrete labeled moves discharge all graph
connectivity assumptions. -/
theorem K0_harmonic_constant {n : ℕ} (hn : 2 ≤ n) (f : State n → ℝ)
    (hf : (K0 n).mulVec f = f) : ∀ y z, f y = f z := by
  apply constant_of_positive_moves hn f
  intro y z hp
  apply SymmetricSector.Markov.harmonic_edge_eq (K0 n) nu0 f K0_nonneg
    (nu0_pos hn) (K0_row_sum hn) _ hf hp
  intro j
  exact congrFun (nu0_stationary hn) j

#print axioms K0_harmonic_constant

/-- The genuine centered active-chain resolvent is invertible for every n≥2. -/
theorem centeredMatrix_isUnit {n : ℕ} (hn : 2 ≤ n) : IsUnit (centeredMatrix n) := by
  apply SymmetricSector.Markov.centered_isUnit (K0 n) nu0
  · intro j
    exact congrFun (nu0_stationary hn) j
  · exact nu0_sum hn
  · exact K0_harmonic_constant hn

theorem centeredMatrix_det_isUnit {n : ℕ} (hn : 2 ≤ n) :
    IsUnit (centeredMatrix n).det :=
  (Matrix.isUnit_iff_isUnit_det _).mp (centeredMatrix_isUnit hn)

#print axioms centeredMatrix_isUnit
#print axioms centeredMatrix_det_isUnit

end
end SymmetricSector.Active
