import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Nat.Choose.Cast
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring
import Mathlib.Tactic

/-!
# Algebra underlying the symmetric-sector orbit moments

The label set is finite and `U = univ.erase v` is the set of labels distinct
from the distinguished target.  These identities use the actual row-balanced,
symmetric perturbation matrix, with no assumption about a reduced scalar.
-/
namespace SymmetricSector.OrbitMoments

open scoped BigOperators
open Finset

variable {α R : Type*} [DecidableEq α] [CommRing R]

/-- The squared row norm excluding the distinguished label. -/
def rowNorm (s : Finset α) (e : α → R) : R := ∑ i ∈ s, e i ^ 2

/-- An ordered internal-edge feature, including harmless diagonal terms. -/
def edgeFeature (s : Finset α) (d : α → α → R) : R := ∑ i ∈ s, ∑ j ∈ s, d i j

/-- Removing a zero diagonal term does not change the row sum. -/
theorem erase_diagonal_sum (s : Finset α) (d : α → α → R)
    (hdiag : ∀ i, d i i = 0) (i : α) :
    ∑ j ∈ s.erase i, d i j = ∑ j ∈ s, d i j := by
  by_cases hi : i ∈ s
  · simpa [hdiag i] using sum_erase_add (s := s) (f := d i) hi
  · simp [erase_eq_of_not_mem hi]

/-- The two-index coincidence contribution used in the `xz` orbit moment. -/
theorem edge_coincidence (s : Finset α) (e : α → R) (d : α → α → R)
    (hdiag : ∀ i, d i i = 0)
    (hrow : ∀ i ∈ s, ∑ j ∈ s, d i j = -e i) :
    (∑ i ∈ s, ∑ j ∈ s.erase i, e i * d i j) = -rowNorm s e := by
  simp_rw [← mul_sum, erase_diagonal_sum s d hdiag]
  calc
    (∑ i ∈ s, e i * ∑ j ∈ s, d i j) = ∑ i ∈ s, -(e i ^ 2) := by
      apply sum_congr rfl
      intro i hi
      rw [hrow i hi]
      ring
    _ = -rowNorm s e := by simp [rowNorm]

/-- Ordered off-diagonal products of a zero-sum vector sum to minus its norm. -/
theorem offDiagonal_vector (s : Finset α) (e : α → R)
    (he : ∑ i ∈ s, e i = 0) :
    (∑ i ∈ s, ∑ j ∈ s.erase i, e i * e j) = -rowNorm s e := by
  simp_rw [← mul_sum]
  calc
    (∑ i ∈ s, e i * ∑ j ∈ s.erase i, e j) = ∑ i ∈ s, -(e i ^ 2) := by
      apply sum_congr rfl
      intro i hi
      have hj := sum_erase_add (s := s) (f := e) hi
      rw [he] at hj
      have hs : ∑ j ∈ s.erase i, e j = -e i := eq_neg_of_add_eq_zero_left hj
      rw [hs]
      ring
    _ = -rowNorm s e := by simp [rowNorm]

/-- Deleting one vertex removes its two ordered incident-edge sums. -/
theorem edgeFeature_erase (s : Finset α) (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    {i : α} (hi : i ∈ s) :
    edgeFeature (s.erase i) d = edgeFeature s d - 2 * ∑ j ∈ s, d i j := by
  have hinner : ∀ j, (∑ l ∈ s.erase i, d j l) = (∑ l ∈ s, d j l) - d j i := by
    intro j
    exact eq_sub_iff_add_eq.mpr (sum_erase_add (s := s) (f := d j) hi)
  simp_rw [edgeFeature, hinner, sum_sub_distrib]
  have hout := sum_erase_add (s := s) (f := fun j => ∑ l ∈ s, d j l) hi
  have hcol : ∑ j ∈ s.erase i, d j i = ∑ j ∈ s, d i j := by
    simp_rw [hsym _ i]
    exact erase_diagonal_sum s d hdiag i
  rw [hcol]
  linear_combination hout

/-- The all-distinct triple contribution used in `xz` is twice the row norm. -/
theorem distinct_triples (s : Finset α) (e : α → R) (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    (he : ∑ i ∈ s, e i = 0)
    (hrow : ∀ i ∈ s, ∑ j ∈ s, d i j = -e i) :
    (∑ i ∈ s, ∑ j ∈ s.erase i, ∑ l ∈ (s.erase i).erase j,
      e i * d j l) = 2 * rowNorm s e := by
  have hz : edgeFeature s d = 0 := by
    unfold edgeFeature
    calc
      (∑ i ∈ s, ∑ j ∈ s, d i j) = ∑ i ∈ s, -e i := sum_congr rfl hrow
      _ = 0 := by simp [he]
  calc
    (∑ i ∈ s, ∑ j ∈ s.erase i, ∑ l ∈ (s.erase i).erase j, e i * d j l) =
        ∑ i ∈ s, e i * edgeFeature (s.erase i) d := by
      apply sum_congr rfl
      intro i hi
      simp_rw [← mul_sum, erase_diagonal_sum (s.erase i) d hdiag]
      simp [edgeFeature, mul_sum]
    _ = ∑ i ∈ s, 2 * e i ^ 2 := by
      apply sum_congr rfl
      intro i hi
      rw [edgeFeature_erase s d hsym hdiag hi, hz, hrow i hi]
      ring
    _ = 2 * rowNorm s e := by simp [rowNorm, mul_sum]

/-- Exact number of k-subsets containing m prescribed distinct labels.
The explicit zero branch handles k<m, including the low-rank endpoints. -/
def inclusionMultiplicity (N k m : ℕ) : ℕ :=
  if m ≤ k then Nat.choose (N - m) (k - m) else 0

/-- Subtracting a prescribed subset is a bijection with subsets of the complement. -/
theorem card_subsets_containing (s t : Finset α) (ht : t ⊆ s) (k : ℕ) :
    ((s.powersetCard k).filter fun B => t ⊆ B).card =
      inclusionMultiplicity s.card k t.card := by
  classical
  by_cases hk : t.card ≤ k
  · rw [inclusionMultiplicity, if_pos hk]
    rw [← card_sdiff ht, ← card_powersetCard]
    apply card_bij (fun B _ => B \ t)
    · intro B hB
      obtain ⟨⟨hBs, hBk⟩, htB⟩ := mem_filter.mp hB |>.imp_left mem_powersetCard.mp
      apply mem_powersetCard.mpr
      constructor
      · exact sdiff_subset_sdiff hBs (subset_refl t)
      · rw [card_sdiff htB, hBk]
    · intro B hB C hC hBC
      have htB := (mem_filter.mp hB).2
      have htC := (mem_filter.mp hC).2
      calc
        B = t ∪ B \ t := (union_sdiff_of_subset htB).symm
        _ = t ∪ C \ t := congrArg (t ∪ ·) hBC
        _ = C := union_sdiff_of_subset htC
    · intro C hC
      obtain ⟨hCsub, hCcard⟩ := mem_powersetCard.mp hC
      have hdisj : Disjoint t C := disjoint_left.mpr (by
        intro i hit hiC
        exact (mem_sdiff.mp (hCsub hiC)).2 hit)
      refine ⟨t ∪ C, ?_, ?_⟩
      · apply mem_filter.mpr
        constructor
        · apply mem_powersetCard.mpr
          constructor
          · exact union_subset ht (hCsub.trans sdiff_subset)
          · rw [card_union_of_disjoint hdisj, hCcard]
            omega
        · exact subset_union_left
      · ext i
        simp only [mem_sdiff, mem_union]
        constructor
        · rintro ⟨hi | hi, hni⟩
          · exact False.elim (hni hi)
          · exact hi
        · intro hi
          exact ⟨Or.inr hi, (mem_sdiff.mp (hCsub hi)).2⟩
  · rw [inclusionMultiplicity, if_neg hk]
    apply card_eq_zero.mpr
    apply eq_empty_iff_forall_not_mem.mpr
    intro B hB
    have hsub := (mem_filter.mp hB).2
    have hcard := (mem_powersetCard.mp (mem_filter.mp hB).1).2
    exact hk (hcard ▸ card_le_card hsub)

/-- Constant contributions of one prescribed label pattern have a kernel-checked count. -/
theorem sum_subsets_containing (s t : Finset α) (ht : t ⊆ s) (k : ℕ) (a : R) :
    (∑ B ∈ s.powersetCard k, if t ⊆ B then a else 0) =
      (inclusionMultiplicity s.card k t.card : R) * a := by
  classical
  rw [← sum_filter]
  simp [card_subsets_containing s t ht k, nsmul_eq_mul]

/-- Reindex a sum on a subset by its inclusion indicator in the ambient set. -/
theorem sum_subset_indicator (s B : Finset α) (hB : B ⊆ s) (f : α → R) :
    (∑ i ∈ B, f i) = ∑ i ∈ s, if i ∈ B then f i else 0 := by
  classical
  rw [← sum_filter]
  congr 1
  ext i
  simp only [mem_filter]
  exact ⟨fun hi => ⟨hB hi, hi⟩, fun hi => hi.2⟩

/-- First orbit moment, derived by counting the actual subsets containing one label. -/
theorem orbit_linear (s : Finset α) (k : ℕ) (e : α → R) :
    (∑ B ∈ s.powersetCard k, ∑ i ∈ B, e i) =
      (inclusionMultiplicity s.card k 1 : R) * ∑ i ∈ s, e i := by
  have hterm (B : Finset α) (hB : B ∈ s.powersetCard k) :
      (∑ i ∈ B, e i) = ∑ i ∈ s, if i ∈ B then e i else 0 :=
    sum_subset_indicator s B (mem_powersetCard.mp hB).1 e
  rw [sum_congr rfl hterm, sum_comm, mul_sum]
  apply sum_congr rfl
  intro i hi
  simpa using sum_subsets_containing s {i} (singleton_subset_iff.mpr hi) k (e i)

/-- Sum of a two-label observable over actual fixed-cardinality subsets. -/
theorem sum_subsets_pair_inclusion (s : Finset α) (k : ℕ) (f : α → α → R) :
    (∑ B ∈ s.powersetCard k, ∑ i ∈ B, ∑ j ∈ B, f i j) =
      ∑ i ∈ s, ∑ j ∈ s,
        (inclusionMultiplicity s.card k ({i, j} : Finset α).card : R) * f i j := by
  classical
  have hexpand : ∀ B ∈ s.powersetCard k,
      (∑ i ∈ B, ∑ j ∈ B, f i j) =
        ∑ i ∈ s, ∑ j ∈ s, if ({i, j} : Finset α) ⊆ B then f i j else 0 := by
    intro B hB
    have hBs := (mem_powersetCard.mp hB).1
    rw [sum_subset_indicator s B hBs]
    apply sum_congr rfl
    intro i hi
    by_cases hiB : i ∈ B
    · rw [if_pos hiB, sum_subset_indicator s B hBs]
      simp [insert_subset_iff, singleton_subset_iff, hiB]
    · simp [insert_subset_iff, hiB]
  rw [sum_congr rfl hexpand, sum_comm]
  apply sum_congr rfl
  intro i hi
  rw [sum_comm]
  apply sum_congr rfl
  intro j hj
  exact sum_subsets_containing s {i,j} (by
    intro l hl
    rcases mem_insert.mp hl with hli | hlj
    · exact hli ▸ hi
    · exact (mem_singleton.mp hlj) ▸ hj) k (f i j)

/-- Separating the diagonal in the fixed-cardinality two-label orbit sum. -/
theorem sum_subsets_pair (s : Finset α) (k : ℕ) (f : α → α → R) :
    (∑ B ∈ s.powersetCard k, ∑ i ∈ B, ∑ j ∈ B, f i j) =
      (inclusionMultiplicity s.card k 1 : R) * (∑ i ∈ s, f i i) +
      (inclusionMultiplicity s.card k 2 : R) *
        (∑ i ∈ s, ∑ j ∈ s.erase i, f i j) := by
  rw [sum_subsets_pair_inclusion]
  calc
    (∑ i ∈ s, ∑ j ∈ s,
        (inclusionMultiplicity s.card k ({i, j} : Finset α).card : R) * f i j) =
      ∑ i ∈ s, ((inclusionMultiplicity s.card k 1 : R) * f i i +
        (inclusionMultiplicity s.card k 2 : R) * ∑ j ∈ s.erase i, f i j) := by
      apply sum_congr rfl
      intro i hi
      rw [← sum_erase_add _ _ hi]
      have hsum :
          (∑ j ∈ s.erase i,
            (inclusionMultiplicity s.card k ({i, j} : Finset α).card : R) * f i j) =
          (inclusionMultiplicity s.card k 2 : R) * ∑ j ∈ s.erase i, f i j := by
        rw [mul_sum]
        apply sum_congr rfl
        intro j hj
        have hji := (mem_erase.mp hj).1
        simp [hji.symm]
      rw [hsum]
      simp [add_comm]
    _ = _ := by simp [sum_add_distrib, mul_sum]

/-- The unnormalized uniform-k-subset square moment, with every endpoint included. -/
theorem orbit_square (s : Finset α) (k : ℕ) (e : α → R)
    (he : ∑ i ∈ s, e i = 0) :
    (∑ B ∈ s.powersetCard k, (∑ i ∈ B, e i) ^ 2) =
      ((inclusionMultiplicity s.card k 1 : R) -
        (inclusionMultiplicity s.card k 2 : R)) * rowNorm s e := by
  simp_rw [pow_two, sum_mul_sum]
  rw [sum_subsets_pair, offDiagonal_vector s e he]
  simp only [rowNorm, pow_two]
  ring

/-- Three-label inclusion reindexing over the actual fixed-rank orbit. -/
theorem sum_subsets_triple_inclusion (s : Finset α) (k : ℕ)
    (f : α → α → α → R) :
    (∑ B ∈ s.powersetCard k, ∑ i ∈ B, ∑ j ∈ B, ∑ l ∈ B, f i j l) =
      ∑ i ∈ s, ∑ j ∈ s, ∑ l ∈ s,
        (inclusionMultiplicity s.card k ({i, j, l} : Finset α).card : R) * f i j l := by
  classical
  have hexpand : ∀ B ∈ s.powersetCard k,
      (∑ i ∈ B, ∑ j ∈ B, ∑ l ∈ B, f i j l) =
        ∑ i ∈ s, ∑ j ∈ s, ∑ l ∈ s,
          if ({i, j, l} : Finset α) ⊆ B then f i j l else 0 := by
    intro B hB
    have hBs := (mem_powersetCard.mp hB).1
    rw [sum_subset_indicator s B hBs]
    apply sum_congr rfl
    intro i hi
    by_cases hiB : i ∈ B
    · rw [if_pos hiB, sum_subset_indicator s B hBs]
      apply sum_congr rfl
      intro j hj
      by_cases hjB : j ∈ B
      · rw [if_pos hjB, sum_subset_indicator s B hBs]
        simp [insert_subset_iff, singleton_subset_iff, hiB, hjB]
      · simp [insert_subset_iff, hiB, hjB]
    · simp [insert_subset_iff, hiB]
  rw [sum_congr rfl hexpand, sum_comm]
  apply sum_congr rfl
  intro i hi
  rw [sum_comm]
  apply sum_congr rfl
  intro j hj
  rw [sum_comm]
  apply sum_congr rfl
  intro l hl
  apply sum_subsets_containing
  intro a ha
  rcases mem_insert.mp ha with hai | ha
  · exact hai ▸ hi
  rcases mem_insert.mp ha with haj | ha
  · exact haj ▸ hj
  · exact (mem_singleton.mp ha) ▸ hl

/-- Coincidence partition of a triple sum. Its second and third indices are
an ordered edge, so their diagonal is zero. -/
theorem triple_card_split (s : Finset α) (c : ℕ → R)
    (f : α → α → α → R) (hdiag : ∀ i j, f i j j = 0) :
    (∑ i ∈ s, ∑ j ∈ s, ∑ l ∈ s,
      c ({i, j, l} : Finset α).card * f i j l) =
      c 2 * ((∑ i ∈ s, ∑ j ∈ s.erase i, f i i j) +
        (∑ i ∈ s, ∑ j ∈ s.erase i, f i j i)) +
      c 3 * (∑ i ∈ s, ∑ j ∈ s.erase i,
        ∑ l ∈ (s.erase i).erase j, f i j l) := by
  have hpoint : ∀ i ∈ s,
      (∑ j ∈ s, ∑ l ∈ s, c ({i, j, l} : Finset α).card * f i j l) =
        c 2 * ((∑ j ∈ s.erase i, f i i j) + (∑ j ∈ s.erase i, f i j i)) +
        c 3 * (∑ j ∈ s.erase i, ∑ l ∈ (s.erase i).erase j, f i j l) := by
    intro i hi
    have hsame : (∑ l ∈ s, c ({i, i, l} : Finset α).card * f i i l) =
        c 2 * ∑ l ∈ s.erase i, f i i l := by
      rw [← sum_erase_add _ _ hi]
      simp only [hdiag, mul_zero, add_zero]
      rw [mul_sum]
      apply sum_congr rfl
      intro l hl
      have hli := (mem_erase.mp hl).1
      simp [hli, hli.symm]
    have hdiff : ∀ j ∈ s.erase i,
        (∑ l ∈ s, c ({i, j, l} : Finset α).card * f i j l) =
          c 3 * (∑ l ∈ (s.erase i).erase j, f i j l) + c 2 * f i j i := by
      intro j hj
      have hji := (mem_erase.mp hj).1
      rw [← sum_erase_add _ _ hi]
      have hsum :
          (∑ l ∈ s.erase i, c ({i, j, l} : Finset α).card * f i j l) =
          c 3 * ∑ l ∈ (s.erase i).erase j, f i j l := by
        rw [← sum_erase_add _ _ hj]
        simp only [hdiag, mul_zero, add_zero]
        rw [mul_sum]
        apply sum_congr rfl
        intro l hl
        have hlj := (mem_erase.mp hl).1
        have hli := (mem_erase.mp (mem_erase.mp hl).2).1
        simp [hli, hlj, hji, hli.symm, hlj.symm, hji.symm]
      rw [hsum]
      simp [hji, hji.symm]
    rw [← sum_erase_add _ _ hi, hsame]
    rw [sum_congr rfl hdiff]
    simp only [sum_add_distrib, ← mul_sum]
    ring
  rw [sum_congr rfl hpoint]
  simp only [sum_add_distrib, mul_add, ← mul_sum]

/-- The raw `xz` orbit moment for a symmetric, zero-diagonal matrix whose
restricted rows sum to minus the target vector. All low-rank cases are included. -/
theorem orbit_cross (s : Finset α) (k : ℕ) (e : α → R) (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    (he : ∑ i ∈ s, e i = 0)
    (hrow : ∀ i ∈ s, ∑ j ∈ s, d i j = -e i) :
    (∑ B ∈ s.powersetCard k, (∑ i ∈ B, e i) * edgeFeature B d) =
      (-2 : R) * ((inclusionMultiplicity s.card k 2 : R) -
        (inclusionMultiplicity s.card k 3 : R)) * rowNorm s e := by
  have hexpand : ∀ B : Finset α, (∑ i ∈ B, e i) * edgeFeature B d =
      ∑ i ∈ B, ∑ j ∈ B, ∑ l ∈ B, e i * d j l := by
    intro B
    unfold edgeFeature
    rw [sum_mul]
    simp_rw [mul_sum]
  rw [sum_congr rfl (fun B _ => hexpand B), sum_subsets_triple_inclusion]
  rw [triple_card_split s (fun m => (inclusionMultiplicity s.card k m : R))
    (fun i j l => e i * d j l) (by intro i j; simp [hdiag])]
  have hreverse : (∑ i ∈ s, ∑ j ∈ s.erase i, e i * d j i) =
      (∑ i ∈ s, ∑ j ∈ s.erase i, e i * d i j) := by
    apply sum_congr rfl
    intro i hi
    apply sum_congr rfl
    intro j hj
    rw [hsym j i]
  rw [hreverse, edge_coincidence s e d hdiag hrow,
    distinct_triples s e d hsym hdiag he hrow]
  ring

/-- At one label below full rank the two features are dependent. -/
theorem near_full_feature_relation (s : Finset α) (e : α → R) (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    (he : ∑ i ∈ s, e i = 0)
    (hrow : ∀ i ∈ s, ∑ j ∈ s, d i j = -e i) {u : α} (hu : u ∈ s) :
    edgeFeature (s.erase u) d = -2 * ∑ i ∈ s.erase u, e i := by
  have hz : edgeFeature s d = 0 := by
    unfold edgeFeature
    rw [sum_congr rfl hrow]
    simp [he]
  rw [edgeFeature_erase s d hsym hdiag hu, hz, hrow u hu]
  have he' := sum_erase_add (s := s) (f := e) hu
  rw [he] at he'
  linear_combination 2 * he'

section NormalizedMoments
variable {K : Type*} [Field K] [CharZero K]

/-- The exact fixed-rank inclusion probability. Both binomial denominators
are proved nonzero from their domain restrictions. -/
theorem inclusion_ratio (N k m : ℕ) (hk : k ≤ N) (hm : m ≤ N) :
    (inclusionMultiplicity N k m : K) / (N.choose k : K) =
      (k.choose m : K) / (N.choose m : K) := by
  have hNk : (N.choose k : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.choose_pos hk).ne'
  have hNm : (N.choose m : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.choose_pos hm).ne'
  by_cases hmk : m ≤ k
  · rw [inclusionMultiplicity, if_pos hmk]
    apply (div_eq_div_iff hNk hNm).mpr
    have h : (N.choose k : K) * (k.choose m : K) =
        (N.choose m : K) * ((N-m).choose (k-m) : K) := by
      exact_mod_cast Nat.choose_mul hk hmk
    simpa only [mul_comm] using h.symm
  · simp [inclusionMultiplicity, hmk, Nat.choose_eq_zero_of_lt (Nat.lt_of_not_ge hmk)]

/-- The degree-three binomial coefficient as a field-valued falling factorial. -/
theorem cast_choose_three (n : ℕ) :
    (n.choose 3 : K) = (n : K) * ((n : K)-1) * ((n : K)-2) / 6 := by
  cases n with
  | zero => simp
  | succ n =>
    have h : ((n : K)+1) * (n.choose 2 : K) = ((n+1).choose 3 : K) * 3 := by
      exact_mod_cast Nat.succ_mul_choose_eq n 2
    rw [Nat.cast_choose_two] at h
    simp only [Nat.cast_add, Nat.cast_one, Nat.cast_succ]
    apply (eq_div_iff (by norm_num : (6 : K) ≠ 0)).mpr
    linear_combination -2 * h

/-- Appendix A.17a, first orbit moment: averaging over every actual k-subset
of an ambient label set of size N. The domain guarantees a nonempty orbit. -/
theorem orbit_square_average (s : Finset α) (k : ℕ) (e : α → K)
    (hN : 2 ≤ s.card) (hk : k ≤ s.card) (he : ∑ i ∈ s, e i = 0) :
    (∑ B ∈ s.powersetCard k, (∑ i ∈ B, e i) ^ 2) / (s.card.choose k : K) =
      ((k : K) * ((s.card : K)-(k : K)) /
        ((s.card : K) * ((s.card : K)-1))) * rowNorm s e := by
  have hn : (s.card : K) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
  have hn1 : (s.card : K)-1 ≠ 0 := by
    have h : ((s.card - 1 : ℕ) : K) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
    simpa only [Nat.cast_sub (by omega : 1 ≤ s.card), Nat.cast_one] using h
  rw [orbit_square s k e he]
  calc
    ((inclusionMultiplicity s.card k 1 : K) -
        (inclusionMultiplicity s.card k 2 : K)) * rowNorm s e / (s.card.choose k : K) =
      ((inclusionMultiplicity s.card k 1 : K) / (s.card.choose k : K) -
        (inclusionMultiplicity s.card k 2 : K) / (s.card.choose k : K)) * rowNorm s e := by ring
    _ = _ := by
      rw [inclusion_ratio s.card k 1 hk (by omega), inclusion_ratio s.card k 2 hk hN]
      simp only [Nat.choose_one_right, Nat.cast_choose_two]
      field_simp
      ring

/-- Appendix A.17a, mixed orbit moment. The assumptions refer directly to
the edge matrix and the target row, rather than to a prescribed moment. -/
theorem orbit_cross_average (s : Finset α) (k : ℕ) (e : α → K) (d : α → α → K)
    (hN : 3 ≤ s.card) (hk : k ≤ s.card)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    (he : ∑ i ∈ s, e i = 0)
    (hrow : ∀ i ∈ s, ∑ j ∈ s, d i j = -e i) :
    (∑ B ∈ s.powersetCard k, (∑ i ∈ B, e i) * edgeFeature B d) /
      (s.card.choose k : K) =
      ((-2 : K) * (k : K) * ((k : K)-1) * ((s.card : K)-(k : K)) /
        ((s.card : K) * ((s.card : K)-1) * ((s.card : K)-2))) * rowNorm s e := by
  have hn : (s.card : K) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
  have hn1 : (s.card : K)-1 ≠ 0 := by
    have h : ((s.card - 1 : ℕ) : K) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
    simpa only [Nat.cast_sub (by omega : 1 ≤ s.card), Nat.cast_one] using h
  have hn2 : (s.card : K)-2 ≠ 0 := by
    have h : ((s.card - 2 : ℕ) : K) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
    simpa only [Nat.cast_sub (by omega : 2 ≤ s.card), Nat.cast_two] using h
  rw [orbit_cross s k e d hsym hdiag he hrow]
  calc
    (-2 : K) * ((inclusionMultiplicity s.card k 2 : K) -
        (inclusionMultiplicity s.card k 3 : K)) * rowNorm s e / (s.card.choose k : K) =
      (-2 : K) * ((inclusionMultiplicity s.card k 2 : K) / (s.card.choose k : K) -
        (inclusionMultiplicity s.card k 3 : K) / (s.card.choose k : K)) * rowNorm s e := by ring
    _ = _ := by
      rw [inclusion_ratio s.card k 2 hk (by omega), inclusion_ratio s.card k 3 hk hN]
      simp only [Nat.cast_choose_two, cast_choose_three]
      field_simp
      ring

end NormalizedMoments

section DistinguishedLabel
variable [Fintype α]

/-- A zero diagonal and zero complete row sum give zero sum on labels other than `v`. -/
theorem target_row_sum (d : α → α → R) (hdiag : ∀ i, d i i = 0)
    (hrow : ∀ i, ∑ j, d i j = 0) (v : α) :
    ∑ i ∈ univ.erase v, d v i = 0 := by
  rw [erase_diagonal_sum univ d hdiag, hrow v]

/-- On `U=V\{v}`, each row sum equals minus the edge to the target. -/
theorem restricted_row_sum (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hrow : ∀ i, ∑ j, d i j = 0)
    (v i : α) :
    ∑ j ∈ univ.erase v, d i j = -d v i := by
  have h := sum_erase_add (s := univ) (f := d i) (mem_univ v)
  rw [hrow i, hsym i v] at h
  exact eq_neg_of_add_eq_zero_left h

/-- Actual symmetric-matrix coincidence sum: no orbit-count or scalar assumptions. -/
theorem target_edge_coincidence (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    (hrow : ∀ i, ∑ j, d i j = 0) (v : α) :
    (∑ i ∈ univ.erase v, ∑ j ∈ (univ.erase v).erase i,
      d v i * d i j) = -rowNorm (univ.erase v) (d v) := by
  apply edge_coincidence _ _ _ hdiag
  intro i hi
  exact restricted_row_sum d hsym hrow v i

/-- Actual all-distinct triple sum, with all three labels different from `v`. -/
theorem target_distinct_triples (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    (hrow : ∀ i, ∑ j, d i j = 0) (v : α) :
    (∑ i ∈ univ.erase v, ∑ j ∈ (univ.erase v).erase i,
      ∑ l ∈ ((univ.erase v).erase i).erase j, d v i * d j l) =
      2 * rowNorm (univ.erase v) (d v) := by
  apply distinct_triples _ _ _ hsym hdiag (target_row_sum d hdiag hrow v)
  intro i hi
  exact restricted_row_sum d hsym hrow v i

/-- Specialization of the complete k-subset square sum to an actual target row. -/
theorem target_orbit_square (d : α → α → R)
    (hdiag : ∀ i, d i i = 0) (hrow : ∀ i, ∑ j, d i j = 0) (v : α) (k : ℕ) :
    (∑ B ∈ (univ.erase v).powersetCard k, (∑ i ∈ B, d v i) ^ 2) =
      ((inclusionMultiplicity (Fintype.card α - 1) k 1 : R) -
        (inclusionMultiplicity (Fintype.card α - 1) k 2 : R)) *
        rowNorm (univ.erase v) (d v) := by
  simpa using orbit_square (univ.erase v) k (d v) (target_row_sum d hdiag hrow v)

/-- Specialization of the complete k-subset mixed sum to an actual target row. -/
theorem target_orbit_cross (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    (hrow : ∀ i, ∑ j, d i j = 0) (v : α) (k : ℕ) :
    (∑ B ∈ (univ.erase v).powersetCard k, (∑ i ∈ B, d v i) * edgeFeature B d) =
      (-2 : R) * ((inclusionMultiplicity (Fintype.card α - 1) k 2 : R) -
        (inclusionMultiplicity (Fintype.card α - 1) k 3 : R)) *
        rowNorm (univ.erase v) (d v) := by
  have h := orbit_cross (univ.erase v) k (d v) d hsym hdiag
    (target_row_sum d hdiag hrow v) (by
      intro i hi
      exact restricted_row_sum d hsym hrow v i)
  simpa using h

/-- The rank N-1 feature relation, proved rather than presumed as a faithful basis. -/
theorem target_near_full_feature_relation (d : α → α → R)
    (hsym : ∀ i j, d i j = d j i) (hdiag : ∀ i, d i i = 0)
    (hrow : ∀ i, ∑ j, d i j = 0) (v u : α) (huv : u ≠ v) :
    edgeFeature ((univ.erase v).erase u) d =
      -2 * ∑ i ∈ (univ.erase v).erase u, d v i := by
  apply near_full_feature_relation (univ.erase v) (d v) d hsym hdiag
    (target_row_sum d hdiag hrow v)
  · intro i hi
    exact restricted_row_sum d hsym hrow v i
  · simp [huv]

end DistinguishedLabel
end SymmetricSector.OrbitMoments
