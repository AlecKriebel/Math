import SymmetricSector.Active
import SymmetricSector.OrbitMoments

/-!
# Incoming current of the actual labeled active chain

All sums below use `Active.kernel` and its actual nonempty-cache state space.
The four predecessor families are enumerated exactly, including empty-family
boundary cases. No stationarity or desired reward identity is assumed.
-/
namespace SymmetricSector.Active
noncomputable section
open scoped BigOperators
open Finset

/-- The two and only two caches with a specified insertion result. -/
theorem insert_eq_iff_cache {α : Type*} [DecidableEq α]
    (B C : Finset α) (i : α) (hi : i ∈ B) :
    insert i C = B ↔ C = B ∨ C = B.erase i := by
  constructor
  · intro h
    by_cases hiC : i ∈ C
    · exact Or.inl (by simpa [insert_eq_of_mem hiC] using h)
    · right
      rw [← h, erase_insert hiC]
  · rintro (rfl | rfl)
    · exact insert_eq_of_mem hi
    · exact insert_erase hi

/-- An event with a prescribed valid cache and target selects one labeled state. -/
theorem sum_cache_target {n : ℕ} (C : Finset (Fin n)) (v : Fin n)
    (hC : C.Nonempty) (hv : v ∉ C) (a : ℝ) :
    (∑ y : State n, if y.cache = C ∧ y.target = v then a else 0) = a := by
  simpa using sum_state_event C v hC hv a (fun _ => 1)

/-- The cache-cardinality weight makes an invalid empty cache contribute zero. -/
theorem sum_cache_target_rank {n : ℕ} (C : Finset (Fin n)) (v : Fin n)
    (hv : v ∉ C) (a : ℝ) :
    (∑ y : State n,
      if y.cache = C ∧ y.target = v then (C.card : ℝ) * a else 0) =
      (C.card : ℝ) * a := by
  by_cases hC : C.Nonempty
  · exact sum_cache_target C v hC hv _
  · have he : C = ∅ := not_nonempty_iff_eq_empty.mp hC
    simp [he]

/-- Count all old targets outside a fixed nonempty predecessor cache. -/
theorem sum_cache {n : ℕ} (C : Finset (Fin n)) (hC : C.Nonempty) (a : ℝ) :
    (∑ y : State n, if y.cache = C then a else 0) =
      ((n : ℝ) - C.card) * a := by
  have hsplit (y : State n) :
      (if y.cache = C then a else 0) =
        ∑ v : Fin n, if y.cache = C ∧ y.target = v then a else 0 := by
    by_cases hy : y.cache = C <;> simp [hy]
  simp_rw [hsplit]
  rw [sum_comm]
  have hterm (v : Fin n) :
      (∑ y : State n, if y.cache = C ∧ y.target = v then a else 0) =
        if v ∉ C then a else 0 := by
    by_cases hv : v ∉ C
    · rw [if_pos hv, sum_cache_target C v hC hv]
    · rw [if_neg hv]
      apply sum_eq_zero
      intro y hy
      rw [if_neg]
      rintro ⟨hc, ht⟩
      apply y.property.2
      change y.target ∈ y.cache
      simpa only [hc, ht] using not_not.mp hv
  rw [sum_congr rfl (fun v _ => hterm v), ← sum_filter]
  have hset : univ.filter (fun v => v ∉ C) = univ \ C := by
    ext v; simp
  rw [hset, sum_const, nsmul_eq_mul, card_sdiff (subset_univ C)]
  have hle : C.card ≤ n := by simpa using card_le_card (subset_univ C)
  simp [Nat.cast_sub hle]

/-- The continue branch has two predecessor caches, with their exact rank weights. -/
theorem incoming_continue_source {n : ℕ} (P : Matrix (Fin n) (Fin n) ℝ)
    (y : State n) (i : Fin n) :
    (∑ u : State n, (u.rank : ℝ) *
      (if i ≠ u.target ∧ y.cache = insert i u.cache ∧ y.target = u.target
       then P u.target i else 0)) =
      if i ∈ y.cache then (2 * (y.rank : ℝ) - 1) * P y.target i else 0 := by
  by_cases hi : i ∈ y.cache
  · rw [if_pos hi]
    have hiv : i ≠ y.target := by
      intro heq
      apply y.property.2
      change y.target ∈ y.cache
      simpa only [← heq] using hi
    have hdist : y.cache ≠ y.cache.erase i := by
      intro heq
      exact (not_mem_erase i y.cache) (heq ▸ hi)
    have hpoint (u : State n) :
        (u.rank : ℝ) *
          (if i ≠ u.target ∧ y.cache = insert i u.cache ∧ y.target = u.target
           then P u.target i else 0) =
        (if u.cache = y.cache ∧ u.target = y.target then
          (y.cache.card : ℝ) * P y.target i else 0) +
        (if u.cache = y.cache.erase i ∧ u.target = y.target then
          ((y.cache.erase i).card : ℝ) * P y.target i else 0) := by
      by_cases ht : u.target = y.target
      · simp only [ht, hiv, true_and, and_true]
        by_cases hc : u.cache = y.cache
        · have hne : u.cache ≠ y.cache.erase i := by simpa [hc] using hdist
          simp [hc, hne, hdist, hiv, insert_eq_of_mem hi, State.rank]
        · by_cases he : u.cache = y.cache.erase i
          · simp [he, hc, hiv, hi, insert_erase hi, State.rank]
          · have hins : y.cache ≠ insert i u.cache := by
              intro hh
              rcases (insert_eq_iff_cache y.cache u.cache i hi).mp hh.symm with h | h
              · exact hc h
              · exact he h
            simp [hc, he, hins]
      · have htn : y.target ≠ u.target := Ne.symm ht
        simp [ht, htn]
    rw [sum_congr rfl (fun u _ => hpoint u), sum_add_distrib,
      sum_cache_target_rank y.cache y.target y.property.2,
      sum_cache_target_rank (y.cache.erase i) y.target (not_mem_mono (erase_subset _ _) y.property.2)]
    rw [card_erase_of_mem hi, Nat.cast_sub (by exact Nat.succ_le_of_lt (rank_pos y))]
    simp only [Nat.cast_one]
    change _ = (2 * (y.cache.card : ℝ) - 1) * _
    ring
  · rw [if_neg hi]
    apply sum_eq_zero
    intro u hu
    rw [if_neg, mul_zero]
    rintro ⟨_, hc, _⟩
    exact hi (hc ▸ mem_insert_self i u.cache)

/-- Retargeting to the prescribed output label has exactly two predecessor caches. -/
theorem retarget_cache_iff {n : ℕ} (B C : Finset (Fin n)) (v i : Fin n)
    (hv : v ∉ B) (hi : i ∈ B) :
    (v ∈ C ∧ B = insert i (C.erase v)) ↔
      C = insert v B ∨ C = insert v (B.erase i) := by
  constructor
  · rintro ⟨hvC, hc⟩
    have hrec : C = insert v (C.erase v) := (insert_erase hvC).symm
    rcases (insert_eq_iff_cache B (C.erase v) i hi).mp hc.symm with h | h
    · exact Or.inl (hrec.trans (congrArg (insert v) h))
    · exact Or.inr (hrec.trans (congrArg (insert v) h))
  · rintro (rfl | rfl)
    · simp [erase_insert hv, insert_eq_of_mem hi]
    · have hve : v ∉ B.erase i := not_mem_mono (erase_subset _ _) hv
      simp [erase_insert hve, insert_erase hi]

/-- For a fixed source draw, the stop branch's two predecessor counts are
`n-k-1` and `n-k`. Their old target is any label outside the predecessor cache. -/
theorem incoming_stop_source {n : ℕ} (P : Matrix (Fin n) (Fin n) ℝ)
    (y : State n) (i : Fin n) :
    (∑ u : State n, ∑ w ∈ u.cache,
      if i ≠ w ∧ y.cache = insert i (u.cache.erase w) ∧ y.target = w
       then P w i else 0) =
      if i ∈ y.cache then (2 * (n : ℝ) - 2 * (y.rank : ℝ) - 1) * P y.target i
      else 0 := by
  have htarget (u : State n) :
      (∑ w ∈ u.cache,
        if i ≠ w ∧ y.cache = insert i (u.cache.erase w) ∧ y.target = w
         then P w i else 0) =
      if i ≠ y.target ∧ y.target ∈ u.cache ∧
          y.cache = insert i (u.cache.erase y.target) then P y.target i else 0 := by
    by_cases hvu : y.target ∈ u.cache
    · rw [← sum_erase_add _ _ hvu]
      have hzero : (∑ w ∈ u.cache.erase y.target,
          if i ≠ w ∧ y.cache = insert i (u.cache.erase w) ∧ y.target = w
           then P w i else 0) = 0 := by
        apply sum_eq_zero
        intro w hw
        rw [if_neg]
        rintro ⟨_, _, ht⟩
        exact (mem_erase.mp hw).1 ht.symm
      rw [hzero, zero_add]
      simp [hvu]
    · have hzero : (∑ w ∈ u.cache,
          if i ≠ w ∧ y.cache = insert i (u.cache.erase w) ∧ y.target = w
           then P w i else 0) = 0 := by
        apply sum_eq_zero
        intro w hw
        rw [if_neg]
        rintro ⟨_, _, ht⟩
        exact hvu (ht ▸ hw)
      rw [hzero]
      simp [hvu]
  simp_rw [htarget]
  by_cases hi : i ∈ y.cache
  · rw [if_pos hi]
    have hiv : i ≠ y.target := by
      intro heq
      apply y.property.2
      change y.target ∈ y.cache
      simpa only [← heq] using hi
    have hdist : insert y.target y.cache ≠ insert y.target (y.cache.erase i) := by
      intro heq
      have hm : i ∈ insert y.target y.cache := mem_insert_of_mem hi
      rw [heq] at hm
      simp [hiv] at hm
    have hpoint (u : State n) :
        (if i ≠ y.target ∧ y.target ∈ u.cache ∧
          y.cache = insert i (u.cache.erase y.target) then P y.target i else 0) =
        (if u.cache = insert y.target y.cache then P y.target i else 0) +
        (if u.cache = insert y.target (y.cache.erase i) then P y.target i else 0) := by
      simp only [hiv, true_and, retarget_cache_iff y.cache u.cache y.target i y.property.2 hi]
      by_cases hc : u.cache = insert y.target y.cache
      · have hn : u.cache ≠ insert y.target (y.cache.erase i) := by simpa [hc] using hdist
        simp [hc, hn, hiv, hdist]
      · simp [hc, hiv]
    rw [sum_congr rfl (fun u _ => hpoint u), sum_add_distrib,
      sum_cache _ (insert_nonempty _ _), sum_cache _ (insert_nonempty _ _),
      card_insert_of_not_mem y.property.2,
      card_insert_of_not_mem (not_mem_mono (erase_subset _ _) y.property.2),
      card_erase_of_mem hi]
    rw [Nat.cast_add, Nat.cast_add,
      Nat.cast_sub (by exact Nat.succ_le_of_lt (rank_pos y))]
    simp only [Nat.cast_one]
    change _ = (2 * (n : ℝ) - 2 * (y.cache.card : ℝ) - 1) * _
    ring
  · rw [if_neg hi]
    apply sum_eq_zero
    intro u hu
    rw [if_neg]
    rintro ⟨_, _, hc⟩
    exact hi (hc ▸ mem_insert_self i (u.cache.erase y.target))


/-- The rank-weighted incoming column sum of the actual two-branch kernel. -/
theorem incoming_rank_kernel {n : ℕ} (P : Matrix (Fin n) (Fin n) ℝ)
    (y : State n) :
    (∑ u : State n, (u.rank : ℝ) * kernel P u y) =
      ((n : ℝ) - 1) * ∑ i ∈ y.cache, P y.target i := by
  have hpoint (u : State n) :
      (u.rank : ℝ) * kernel P u y = (1 / 2 : ℝ) *
        ((∑ i : Fin n, (u.rank : ℝ) *
          (if i ≠ u.target ∧ y.cache = insert i u.cache ∧ y.target = u.target
           then P u.target i else 0)) +
          ∑ i : Fin n, ∑ w ∈ u.cache,
          if i ≠ w ∧ y.cache = insert i (u.cache.erase w) ∧ y.target = w
           then P w i else 0) := by
    unfold kernel
    rw [sum_comm (s := u.cache), ← mul_sum]
    have hu : (u.rank : ℝ) ≠ 0 := by exact_mod_cast (rank_pos u).ne'
    field_simp
    ring
  rw [sum_congr rfl (fun u _ => hpoint u), ← mul_sum, sum_add_distrib,
    sum_comm]
  simp_rw [incoming_continue_source]
  conv_lhs => enter [2, 2]; rw [sum_comm]
  simp_rw [incoming_stop_source]
  rw [← sum_add_distrib]
  have hterms (i : Fin n) :
      (if i ∈ y.cache then (2 * (y.rank : ℝ) - 1) * P y.target i else 0) +
      (if i ∈ y.cache then (2 * (n : ℝ) - 2 * (y.rank : ℝ) - 1) * P y.target i
       else 0) =
      if i ∈ y.cache then (2 * ((n : ℝ) - 1)) * P y.target i else 0 := by
    by_cases hi : i ∈ y.cache <;> simp [hi] <;> ring
  rw [sum_congr rfl (fun i _ => hterms i), ← sum_filter]
  have hfilter : univ.filter (fun i => i ∈ y.cache) = y.cache := by ext i; simp
  rw [hfilter, ← mul_sum]
  ring

/-- Exact incoming current, before specialization to either the complete kernel
or its signed derivative. Diagonal entries need no assumption because the
actual kernel excludes self draws. -/
theorem nu0_kernel {n : ℕ} (hn : 2 ≤ n)
    (P : Matrix (Fin n) (Fin n) ℝ) (y : State n) :
    Matrix.vecMul nu0 (kernel P) y =
      (∑ i ∈ y.cache, P y.target i) / ((n : ℝ) * 2 ^ (n - 2)) := by
  unfold Matrix.vecMul dotProduct
  calc
    (∑ u : State n, nu0 u * kernel P u y) =
      (∑ u : State n, (u.rank : ℝ) * kernel P u y) /
        ((n : ℝ) * ((n - 1 : ℕ) : ℝ) * 2 ^ (n - 2)) := by
      simp only [nu0, div_mul_eq_mul_div, sum_div]
    _ = _ := by
      rw [incoming_rank_kernel, Nat.cast_sub (by omega : 1 ≤ n), Nat.cast_one]
      have hN : (n : ℝ) - 1 ≠ 0 := by
        have : (1 : ℝ) < n := by exact_mod_cast (show 1 < n by omega)
        linarith
      field_simp
      ring

/-- Stationarity of the printed labeled distribution for the genuine complete chain. -/
theorem nu0_stationary {n : ℕ} (hn : 2 ≤ n) :
    Matrix.vecMul nu0 (K0 n) = nu0 := by
  funext y
  rw [K0, nu0_kernel hn, complete_subset_sum y.cache y.target y.property.2]
  unfold nu0
  change (y.rank : ℝ) / _ / _ = _
  ring

/-- Appendix A.17b's actual signed incoming current, with the printed normalization. -/
theorem nu0_perturbation {n : ℕ} (hn : 2 ≤ n)
    (δ : Matrix (Fin n) (Fin n) ℝ) (y : State n) :
    Matrix.vecMul nu0 (perturbation δ) y =
      x δ y / ((n : ℝ) * 2 ^ (n - 2)) := by
  exact nu0_kernel hn δ y

#print axioms incoming_rank_kernel
#print axioms nu0_stationary
#print axioms nu0_perturbation

/-- Reindex actual labeled states by target and all subsets of its complement.
The empty-cache term is included only when the observable is proved zero there. -/
theorem sum_state_powerset {n : ℕ}
    (f : Finset (Fin n) → Fin n → ℝ) (hzero : ∀ v, f ∅ v = 0) :
    (∑ y : State n, f y.cache y.target) =
      ∑ v : Fin n, ∑ B ∈ (univ.erase v).powerset, f B v := by
  classical
  have hsub := sum_subtype (F := (inferInstance : Fintype (State n))) (p := fun p : Finset (Fin n) × Fin n => p.1.Nonempty ∧ p.2 ∉ p.1)
    (univ.filter (fun p : Finset (Fin n) × Fin n => p.1.Nonempty ∧ p.2 ∉ p.1))
    (by intro p; simp) (fun p => f p.1 p.2)
  change (∑ y : State n, (fun p : Finset (Fin n) × Fin n => f p.1 p.2) y.val) = _
  rw [← hsub, sum_filter, Fintype.sum_prod_type, sum_comm]
  apply sum_congr rfl
  intro v hv
  have hterm (B : Finset (Fin n)) :
      (if B.Nonempty ∧ v ∉ B then f B v else 0) =
        if v ∉ B then f B v else 0 := by
    by_cases hB : B.Nonempty
    · simp [hB]
    · have he : B = ∅ := not_nonempty_iff_eq_empty.mp hB
      simp [he, hzero]
  rw [sum_congr rfl (fun B _ => hterm B), ← sum_filter]
  congr 1
  ext B
  simp only [mem_filter, mem_univ, true_and, mem_powerset]
  constructor
  · intro hvB i hi
    simp only [mem_erase, mem_univ, and_true]
    intro heq
    exact hvB (heq ▸ hi)
  · intro hB hvB
    exact not_mem_erase v univ (hB hvB)

/-- Double-count subset memberships without any division or low-cardinality convention. -/
theorem twice_sum_powerset_card {α : Type*} [DecidableEq α] (s : Finset α) :
    (2 : ℝ) * (∑ B ∈ s.powerset, (B.card : ℝ)) = (s.card : ℝ) * 2 ^ s.card := by
  induction s using Finset.induction_on with
  | empty => simp
  | @insert i s hi ih =>
    rw [sum_powerset_insert hi]
    have hsum : (∑ B ∈ s.powerset, ((insert i B).card : ℝ)) =
        (∑ B ∈ s.powerset, (B.card : ℝ)) + 2 ^ s.card := by
      have hpoint (B : Finset α) (hB : B ∈ s.powerset) :
          ((insert i B).card : ℝ) = (B.card : ℝ) + 1 := by
        rw [card_insert_of_not_mem (not_mem_mono (mem_powerset.mp hB) hi)]
        simp
      rw [sum_congr rfl hpoint, sum_add_distrib]
      simp [card_powerset]
    rw [hsum, card_insert_of_not_mem hi, Nat.cast_add, Nat.cast_one, pow_succ]
    nlinarith

/-- The printed labeled stationary weights sum to one for every n≥2. -/
theorem nu0_sum {n : ℕ} (hn : 2 ≤ n) : (∑ y : State n, nu0 y) = 1 := by
  have hN : 0 < n - 1 := by omega
  have hexp : n - 1 = (n - 2) + 1 := by omega
  have hcard (v : Fin n) :
      (∑ B ∈ (univ.erase v).powerset, (B.card : ℝ)) =
        ((n - 1 : ℕ) : ℝ) * 2 ^ (n - 2) := by
    have h := twice_sum_powerset_card (univ.erase v)
    simp only [card_erase_of_mem (mem_univ v), card_univ, Fintype.card_fin] at h
    rw [hexp, pow_succ] at h
    have hcast : ((n - 2 + 1 : ℕ) : ℝ) = ((n - 1 : ℕ) : ℝ) := by rw [← hexp]
    rw [hcast] at h
    linarith
  unfold nu0
  rw [← sum_div]
  have hsum := sum_state_powerset (n := n) (fun B _ => (B.card : ℝ)) (by intro v; simp)
  change (∑ y : State n, (y.cache.card : ℝ)) / _ = _
  rw [hsum]
  simp_rw [hcard]
  simp only [sum_const, card_univ, Fintype.card_fin, nsmul_eq_mul]
  have hd := (nu0_denominator_pos hn).ne'
  convert div_self hd using 1 <;> ring

#print axioms nu0_sum

/-- Squared Frobenius norm, defined by the actual matrix entries. -/
def frobeniusSq {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ) : ℝ :=
  ∑ v, ∑ i, δ v i ^ 2

/-- The row norms used in the labeled orbit calculation sum to the matrix norm. -/
theorem sum_rowNorm {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (hdiag : ∀ v, δ v v = 0) :
    (∑ v, OrbitMoments.rowNorm (univ.erase v) (δ v)) = frobeniusSq δ := by
  unfold OrbitMoments.rowNorm frobeniusSq
  apply sum_congr rfl
  intro v hv
  simpa [hdiag] using sum_erase_add (s := univ) (f := fun i => δ v i ^ 2) (mem_univ v)

/-- The exact unnormalized square coefficient in a rank-k orbit. -/
def orbitA (N k : ℕ) : ℝ :=
  (OrbitMoments.inclusionMultiplicity N k 1 : ℝ) -
    (OrbitMoments.inclusionMultiplicity N k 2 : ℝ)

/-- The exact unnormalized mixed coefficient in a rank-k orbit. -/
def orbitB (N k : ℕ) : ℝ :=
  -2 * ((OrbitMoments.inclusionMultiplicity N k 2 : ℝ) -
    (OrbitMoments.inclusionMultiplicity N k 3 : ℝ))

/-- Partition all subsets by their actual cardinality. -/
theorem sum_powerset_by_card {α : Type*} (s : Finset α) (f : Finset α → ℝ) :
    (∑ B ∈ s.powerset, f B) =
      ∑ k ∈ range (s.card + 1), ∑ B ∈ s.powersetCard k, f B := by
  rw [powerset_card_disjiUnion, sum_disjiUnion]

/-- The actual feature-current product at a fixed target and fixed rank. -/
theorem target_orbit_current {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (hδ : SymmetricBalanced δ) (a b : ℕ → ℝ) (v : Fin n) (k : ℕ) :
    (∑ B ∈ (univ.erase v).powersetCard k,
      (∑ i ∈ B, δ v i) *
        (a B.card * (∑ i ∈ B, δ v i) + b B.card * OrbitMoments.edgeFeature B δ)) =
      (orbitA (n - 1) k * a k + orbitB (n - 1) k * b k) *
        OrbitMoments.rowNorm (univ.erase v) (δ v) := by
  have hterm (B : Finset (Fin n)) (hB : B ∈ (univ.erase v).powersetCard k) :
      (∑ i ∈ B, δ v i) *
        (a B.card * (∑ i ∈ B, δ v i) + b B.card * OrbitMoments.edgeFeature B δ) =
      a k * (∑ i ∈ B, δ v i) ^ 2 +
        b k * ((∑ i ∈ B, δ v i) * OrbitMoments.edgeFeature B δ) := by
    rw [(mem_powersetCard.mp hB).2]
    ring
  rw [sum_congr rfl hterm, sum_add_distrib, ← mul_sum, ← mul_sum,
    OrbitMoments.target_orbit_square δ hδ.1 hδ.2.2 v k,
    OrbitMoments.target_orbit_cross δ hδ.2.1 hδ.1 hδ.2.2 v k]
  simp only [Fintype.card_fin, orbitA, orbitB]
  ring

/-- General-n A.17b before Pascal simplification of the exact orbit counts.
The left-hand side is the actual active perturbation applied to the actual
feature function, paired with the printed stationary distribution. -/
theorem nu0_perturbation_feature_orbits {n : ℕ} (hn : 2 ≤ n)
    (δ : Matrix (Fin n) (Fin n) ℝ) (hδ : SymmetricBalanced δ) (a b : ℕ → ℝ) :
    dotProduct nu0 ((perturbation δ).mulVec (feature δ a b)) =
      frobeniusSq δ * (∑ k ∈ range n,
        (orbitA (n - 1) k * a k + orbitB (n - 1) k * b k) /
          ((n : ℝ) * 2 ^ (n - 2))) := by
  rw [Matrix.dotProduct_mulVec]
  unfold dotProduct
  simp_rw [nu0_perturbation hn]
  have hpoint (y : State n) :
      x δ y / ((n : ℝ) * 2 ^ (n - 2)) * feature δ a b y =
      ((∑ i ∈ y.cache, δ y.target i) *
        (a y.cache.card * (∑ i ∈ y.cache, δ y.target i) +
          b y.cache.card * OrbitMoments.edgeFeature y.cache δ)) /
        ((n : ℝ) * 2 ^ (n - 2)) := by
    unfold feature x z OrbitMoments.edgeFeature
    ring
  rw [sum_congr rfl (fun y _ => hpoint y), ← sum_div]
  have hreindex := sum_state_powerset (n := n)
    (fun B v => (∑ i ∈ B, δ v i) *
      (a B.card * (∑ i ∈ B, δ v i) + b B.card * OrbitMoments.edgeFeature B δ))
    (by intro v; simp)
  rw [hreindex]
  simp_rw [sum_powerset_by_card]
  have hcard (v : Fin n) : (univ.erase v).card + 1 = n := by
    simp only [card_erase_of_mem (mem_univ v), card_univ, Fintype.card_fin]
    omega
  simp_rw [hcard, target_orbit_current δ hδ a b]
  rw [sum_comm]
  simp_rw [← mul_sum, sum_rowNorm δ hδ.1]
  rw [← sum_mul, ← sum_div]
  ring

#print axioms nu0_perturbation_feature_orbits

/-- Both features have zero mean on every actual fixed-rank labeled orbit. -/
theorem target_orbit_feature_zero {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (hδ : SymmetricBalanced δ) (v : Fin n) (k : ℕ) (a b : ℝ) :
    (Finset.sum ((Finset.univ.erase v).powersetCard k)
      (fun B : Finset (Fin n) =>
        a * (∑ i ∈ B, δ v i) + b * OrbitMoments.edgeFeature B δ)) = 0 := by
  rw [sum_add_distrib, ← mul_sum, ← mul_sum, OrbitMoments.orbit_linear,
    OrbitMoments.target_row_sum δ hδ.1 hδ.2.2 v, mul_zero, mul_zero, zero_add]
  have hedge : (∑ B ∈ (univ.erase v).powersetCard k, OrbitMoments.edgeFeature (α := Fin n) B δ) = 0 := by
    unfold OrbitMoments.edgeFeature
    rw [OrbitMoments.sum_subsets_pair]
    have hdiag : (∑ i ∈ univ.erase v, δ i i) = 0 := by simp [hδ.1]
    rw [hdiag, mul_zero, zero_add]
    have hoff : (∑ i ∈ univ.erase v, ∑ j ∈ (univ.erase v).erase i, δ i j) = 0 := by
      simp_rw [OrbitMoments.erase_diagonal_sum (univ.erase v) δ hδ.1,
        OrbitMoments.restricted_row_sum δ hδ.2.1 hδ.2.2 v,
        sum_neg_distrib, OrbitMoments.target_row_sum δ hδ.1 hδ.2.2 v, neg_zero]
    rw [hoff, mul_zero]
  rw [hedge, mul_zero]

/-- Every symmetric balanced feature has zero stationary mean. No injectivity
of the feature coordinates is required or asserted. -/
theorem nu0_feature_zero {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (hδ : SymmetricBalanced δ) (a b : ℕ → ℝ) :
    dotProduct nu0 (feature δ a b) = 0 := by
  unfold dotProduct nu0 feature x z
  simp_rw [div_mul_eq_mul_div]
  rw [← sum_div]
  suffices h : (∑ y : State n,
      (y.rank : ℝ) * (a y.rank * (∑ i ∈ y.cache, δ y.target i) +
        b y.rank * ∑ w ∈ y.cache, ∑ i ∈ y.cache, δ w i)) = 0 by rw [h, zero_div]
  have hreindex := sum_state_powerset (n := n)
    (fun B v => (B.card : ℝ) *
      (a B.card * (∑ i ∈ B, δ v i) + b B.card * OrbitMoments.edgeFeature B δ))
    (by intro v; simp)
  change (∑ y : State n,
    (y.cache.card : ℝ) * (a y.cache.card * (∑ i ∈ y.cache, δ y.target i) +
      b y.cache.card * OrbitMoments.edgeFeature y.cache δ)) = 0
  rw [hreindex]
  apply sum_eq_zero
  intro v hv
  rw [sum_powerset_by_card]
  apply sum_eq_zero
  intro k hk
  have hterm (B : Finset (Fin n)) (hB : B ∈ (univ.erase v).powersetCard k) :
      (B.card : ℝ) *
        (a B.card * (∑ i ∈ B, δ v i) + b B.card * OrbitMoments.edgeFeature B δ) =
      ((k : ℝ) * a k) * (∑ i ∈ B, δ v i) +
        ((k : ℝ) * b k) * OrbitMoments.edgeFeature B δ := by
    rw [(mem_powersetCard.mp hB).2]
    ring
  rw [sum_congr rfl hterm, target_orbit_feature_zero δ hδ]

#print axioms nu0_feature_zero

@[simp] theorem orbitA_zero (N : ℕ) : orbitA N 0 = 0 := by
  simp [orbitA, OrbitMoments.inclusionMultiplicity]

@[simp] theorem orbitB_zero (N : ℕ) : orbitB N 0 = 0 := by
  simp [orbitB, OrbitMoments.inclusionMultiplicity]

@[simp] theorem orbitB_one (N : ℕ) : orbitB N 1 = 0 := by
  simp [orbitB, OrbitMoments.inclusionMultiplicity]

/-- Pascal simplification of the square orbit coefficient, including rank one. -/
theorem orbitA_succ (N j : ℕ) (hN : 2 ≤ N) :
    orbitA N (j + 1) = (Nat.choose (N - 2) j : ℝ) := by
  have hNm : N - 1 = (N - 2) + 1 := by omega
  cases j with
  | zero => simp [orbitA, OrbitMoments.inclusionMultiplicity]
  | succ j =>
    have h1 : 1 ≤ j.succ + 1 := by omega
    have h2 : 2 ≤ j.succ + 1 := by omega
    rw [orbitA, OrbitMoments.inclusionMultiplicity, if_pos h1,
      OrbitMoments.inclusionMultiplicity, if_pos h2]
    simp only [Nat.succ_eq_add_one, Nat.add_sub_cancel]
    have hj : j + 1 + 1 - 2 = j := by omega
    rw [hj, hNm, Nat.choose_succ_succ', Nat.cast_add]
    ring

/-- Pascal simplification of the mixed orbit coefficient, including rank two. -/
theorem orbitB_add_two (N j : ℕ) (hN : 3 ≤ N) :
    orbitB N (j + 2) = -2 * (Nat.choose (N - 3) j : ℝ) := by
  have hNm : N - 2 = (N - 3) + 1 := by omega
  cases j with
  | zero => simp [orbitB, OrbitMoments.inclusionMultiplicity]
  | succ j =>
    have h2 : 2 ≤ j.succ + 2 := by omega
    have h3 : 3 ≤ j.succ + 2 := by omega
    rw [orbitB, OrbitMoments.inclusionMultiplicity, if_pos h2,
      OrbitMoments.inclusionMultiplicity, if_pos h3]
    simp only [Nat.succ_eq_add_one, Nat.add_sub_cancel]
    have hj : j + 1 + 2 - 3 = j := by omega
    rw [hj, hNm, Nat.choose_succ_succ', Nat.cast_add]
    ring

/-- The square channel has precisely the printed range 1≤k<N. -/
theorem sum_orbitA (N : ℕ) (hN : 2 ≤ N) (a : ℕ → ℝ) :
    (∑ k ∈ range (N + 1), orbitA N k * a k) =
      ∑ j ∈ range (N - 1), (Nat.choose (N - 2) j : ℝ) * a (j + 1) := by
  rw [sum_range_succ']
  simp only [orbitA_zero, zero_mul, add_zero]
  simp_rw [orbitA_succ N _ hN]
  have hNm : N = (N - 1) + 1 := by omega
  conv_lhs => enter [1]; rw [hNm]
  rw [sum_range_succ]
  have hzero : (N - 2).choose (N - 1) = 0 := Nat.choose_eq_zero_of_lt (by omega)
  rw [hzero, Nat.cast_zero, zero_mul, add_zero]

/-- The mixed channel has precisely the printed range 2≤k<N. -/
theorem sum_orbitB (N : ℕ) (hN : 3 ≤ N) (b : ℕ → ℝ) :
    (∑ k ∈ range (N + 1), orbitB N k * b k) =
      ∑ j ∈ range (N - 2), (-2 * (Nat.choose (N - 3) j : ℝ)) * b (j + 2) := by
  rw [sum_range_succ']
  simp only [orbitB_zero, zero_mul, add_zero]
  have hNm : N = (N - 1) + 1 := by omega
  conv_lhs => enter [1]; rw [hNm]
  rw [sum_range_succ']
  simp only [Nat.zero_add, orbitB_one, zero_mul, add_zero, ← Nat.add_assoc]
  simp_rw [orbitB_add_two N _ hN]
  have hNm' : N - 1 = (N - 2) + 1 := by omega
  conv_lhs => enter [1]; rw [hNm']
  rw [sum_range_succ]
  have hzero : (N - 3).choose (N - 2) = 0 := Nat.choose_eq_zero_of_lt (by omega)
  rw [hzero, Nat.cast_zero, mul_zero, zero_mul, add_zero]


end
end SymmetricSector.Active
