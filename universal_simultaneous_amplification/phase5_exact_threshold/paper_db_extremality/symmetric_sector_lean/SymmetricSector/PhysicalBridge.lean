import SymmetricSector.Active
import SymmetricSector.Gradients
import SymmetricSector.BlockActions
import SymmetricSector.ActiveInverse

namespace SymmetricSector.Active
noncomputable section
open scoped BigOperators

/-- Zero extension of the physical good channel; ranks are one-based. -/
def coeffA (N : ℕ) (c : Channel N → ℚ) (k : ℕ) : ℝ :=
  (goodAt N (fun i => c (.inl i)) (k : ℤ) : ℝ)

/-- Zero extension of the physical bad channel; its first rank is two. -/
def coeffB (N : ℕ) (c : Channel N → ℚ) (k : ℕ) : ℝ :=
  (badAt N (fun i => c (.inr i)) (k : ℤ) : ℝ)

@[simp] theorem coeffA_at (N : ℕ) (c : Channel N → ℚ) (i : Good N) :
    coeffA N c (i.val + 1) = (c (.inl i) : ℝ) := by
  simp [coeffA]

@[simp] theorem coeffB_at (N : ℕ) (c : Channel N → ℚ) (i : Bad N) :
    coeffB N c (i.val + 2) = (c (.inr i) : ℝ) := by
  simp [coeffB]


/-- The two feature sums on an arbitrary cache, including the empty cache
that can occur between retargeting and sampling. -/
def cacheX {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (C : Finset (Fin n)) (v : Fin n) : ℝ := ∑ i ∈ C, δ v i

def cacheZ {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (C : Finset (Fin n)) : ℝ := ∑ w ∈ C, ∑ i ∈ C, δ w i

@[simp] theorem cacheX_insert {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (C : Finset (Fin n)) (v i : Fin n) (hi : i ∉ C) :
    cacheX δ (insert i C) v = δ v i + cacheX δ C v := by
  simp [cacheX, Finset.sum_insert hi]

theorem cacheZ_insert {n : ℕ} {δ : Matrix (Fin n) (Fin n) ℝ}
    (hδ : SymmetricBalanced δ) (C : Finset (Fin n)) (i : Fin n) (hi : i ∉ C) :
    cacheZ δ (insert i C) = cacheZ δ C + 2 * cacheX δ C i := by
  unfold cacheZ cacheX
  simp only [Finset.sum_insert hi, hδ.1, zero_add, Finset.sum_add_distrib]
  have hs : (∑ x ∈ C, δ x i) = ∑ x ∈ C, δ i x := by
    apply Finset.sum_congr rfl
    intro x hx
    exact hδ.2.1 x i
  rw [hs]
  ring

theorem cacheX_erase_self {n : ℕ} {δ : Matrix (Fin n) (Fin n) ℝ}
    (hδ : SymmetricBalanced δ) (C : Finset (Fin n)) (w : Fin n) (hw : w ∈ C) :
    cacheX δ (C.erase w) w = cacheX δ C w := by
  have hs := Finset.sum_erase_add (s := C) (f := δ w) hw
  simpa [cacheX, hδ.1] using hs

theorem cacheZ_erase {n : ℕ} {δ : Matrix (Fin n) (Fin n) ℝ}
    (hδ : SymmetricBalanced δ) (C : Finset (Fin n)) (w : Fin n) (hw : w ∈ C) :
    cacheZ δ (C.erase w) = cacheZ δ C - 2 * cacheX δ C w := by
  have hs := cacheZ_insert hδ (C.erase w) w (Finset.not_mem_erase _ _)
  rw [Finset.insert_erase hw, cacheX_erase_self hδ C w hw] at hs
  linarith

/-- Exact one-draw feature action. This holds on arbitrary caches and thus
also handles the empty intermediate cache at the lower stop boundary. -/
theorem feature_sample_complete {n : ℕ} (hn : 2 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ)
    (C : Finset (Fin n)) (v : Fin n) (hv : v ∉ C) (a b : ℕ → ℝ) :
    (∑ i : Fin n, if hi : i ≠ v then complete n v i *
      feature δ a b (sampled C v i hv hi) else 0) =
      (((C.card : ℝ) * a C.card +
          ((((n - 1 : ℕ) : ℝ)) - C.card - 1) * a (C.card + 1) -
          2 * b (C.card + 1)) * cacheX δ C v +
        ((C.card : ℝ) * b C.card +
          ((((n - 1 : ℕ) : ℝ)) - C.card - 2) * b (C.card + 1)) * cacheZ δ C) /
        ((n - 1 : ℕ) : ℝ) := by
  let U : Finset (Fin n) := Finset.univ.erase v
  let D := U \ C
  have hCU : C ⊆ U := by
    intro i hi
    simp only [U, Finset.mem_erase, Finset.mem_univ, and_true]
    intro h
    exact hv (h ▸ hi)
  have hN : ((n - 1 : ℕ) : ℝ) ≠ 0 := ne_of_gt (complete_denominator_pos hn)
  have hsumX : (∑ i ∈ D, δ v i) = -cacheX δ C v := by
    have hs := Finset.sum_sdiff hCU (f := δ v)
    have hrow := Finset.sum_erase_add (s := Finset.univ) (f := δ v) (Finset.mem_univ v)
    rw [hδ.1, add_zero, hδ.2.2] at hrow
    change (∑ i ∈ U, δ v i) = 0 at hrow
    change (∑ i ∈ D, δ v i) + cacheX δ C v = ∑ i ∈ U, δ v i at hs
    rw [hrow] at hs
    linarith
  have hsumZ : (∑ i ∈ D, cacheX δ C i) = -cacheZ δ C - cacheX δ C v := by
    have hs := Finset.sum_sdiff hCU (f := cacheX δ C)
    have hrow : (∑ i ∈ U, cacheX δ C i) = -cacheX δ C v := by
      have hall : (∑ i : Fin n, cacheX δ C i) = 0 := by
        unfold cacheX
        rw [Finset.sum_comm]
        simp only [column_sums_zero hδ, Finset.sum_const_zero]
      have he := Finset.sum_erase_add (s := Finset.univ) (f := cacheX δ C)
        (Finset.mem_univ v)
      rw [hall] at he
      change (∑ i ∈ U, cacheX δ C i) + cacheX δ C v = 0 at he
      linarith
    change (∑ i ∈ D, cacheX δ C i) + cacheZ δ C = ∑ i ∈ U, cacheX δ C i at hs
    rw [hrow] at hs
    linarith
  have hDcard : (D.card : ℝ) = (((n - 1 : ℕ) : ℝ)) - C.card := by
    rw [Finset.card_sdiff hCU, Nat.cast_sub (Finset.card_le_card hCU)]
    simp [U]
  have hremove : (∑ i : Fin n, if hi : i ≠ v then complete n v i *
      feature δ a b (sampled C v i hv hi) else 0) =
      ∑ i ∈ U, (if hi : i ≠ v then complete n v i *
        feature δ a b (sampled C v i hv hi) else 0) := by
    have hs := Finset.sum_erase_add (s := Finset.univ)
      (f := fun i => if hi : i ≠ v then complete n v i *
        feature δ a b (sampled C v i hv hi) else 0) (Finset.mem_univ v)
    simpa [U] using hs.symm
  rw [hremove, ← Finset.sum_sdiff hCU]
  have hinside : (∑ i ∈ C, if hi : i ≠ v then complete n v i *
        feature δ a b (sampled C v i hv hi) else 0) =
      (C.card : ℝ) / ((n - 1 : ℕ) : ℝ) *
        (a C.card * cacheX δ C v + b C.card * cacheZ δ C) := by
    have ht (i : Fin n) (hiC : i ∈ C) :
        (if hi : i ≠ v then complete n v i *
          feature δ a b (sampled C v i hv hi) else 0) =
        (1 / ((n - 1 : ℕ) : ℝ)) *
          (a C.card * cacheX δ C v + b C.card * cacheZ δ C) := by
      have hiv : i ≠ v := by intro h; exact hv (h ▸ hiC)
      simp [hiv, complete, hiv.symm, feature, x, z, sampled,
        State.rank, State.cache, State.target, Finset.insert_eq_of_mem hiC, cacheX, cacheZ]
    rw [Finset.sum_congr rfl ht]
    simp [nsmul_eq_mul]
    ring
  have houtside : (∑ i ∈ D, if hi : i ≠ v then complete n v i *
        feature δ a b (sampled C v i hv hi) else 0) =
      (1 / ((n - 1 : ℕ) : ℝ)) *
        (a (C.card + 1) * ((D.card : ℝ) * cacheX δ C v + ∑ i ∈ D, δ v i) +
          b (C.card + 1) * ((D.card : ℝ) * cacheZ δ C + 2 * ∑ i ∈ D, cacheX δ C i)) := by
    have ht (i : Fin n) (hiD : i ∈ D) :
        (if hi : i ≠ v then complete n v i *
          feature δ a b (sampled C v i hv hi) else 0) =
        (1 / ((n - 1 : ℕ) : ℝ)) *
          (a (C.card + 1) * (δ v i + cacheX δ C v) +
            b (C.card + 1) * (cacheZ δ C + 2 * cacheX δ C i)) := by
      have hiC : i ∉ C := (Finset.mem_sdiff.mp hiD).2
      have hiv : i ≠ v := (Finset.mem_erase.mp (Finset.mem_sdiff.mp hiD).1).1
      rw [dif_pos hiv]
      simp only [complete, if_neg hiv.symm, feature, x, z, sampled,
        State.rank, State.cache, State.target, Finset.card_insert_of_not_mem hiC]
      change _ * (a (C.card+1) * cacheX δ (insert i C) v +
        b (C.card+1) * cacheZ δ (insert i C)) = _
      rw [cacheX_insert δ C v i hiC, cacheZ_insert hδ C i hiC]
    rw [Finset.sum_congr rfl ht]
    simp only [← Finset.mul_sum, Finset.sum_add_distrib, Finset.sum_const, nsmul_eq_mul]
    ring
  rw [hinside, houtside, hDcard, hsumX, hsumZ]
  ring

/-- The explicitly defined coefficient operator before finite-channel boundary
truncation. Its coefficients are not inferred using injectivity of features. -/
def featureCoeffA (N : ℕ) (a b : ℕ → ℝ) (k : ℕ) : ℝ :=
  ((k : ℝ) * a k + ((N : ℝ) - k - 1) * a (k + 1) - 2 * b (k + 1)) /
    (2 * N)

def featureCoeffB (N : ℕ) (a b : ℕ → ℝ) (k : ℕ) : ℝ :=
  (((k : ℝ) - 1) * a (k - 1) + ((N : ℝ) - k) * a k +
    ((k : ℝ) - 1) * ((k : ℝ) - 2) * b (k - 1) +
    ((N : ℝ) * ((k : ℝ) - 2) + k) * b k +
    (k : ℝ) * ((N : ℝ) - k - 2) * b (k + 1)) / (2 * k * N)

/-- General population-size intertwining, proved directly from the actual
labeled kernel and feature sums. Arbitrary endpoint coefficients are allowed:
the absent feature multipliers, rather than an injectivity assumption, enforce
the physical boundaries. -/
theorem K0_feature {n : ℕ} (hn : 2 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ)
    (a b : ℕ → ℝ) (y : State n) :
    (K0 n).mulVec (feature δ a b) y =
      feature δ (featureCoeffA (n - 1) a b) (featureCoeffB (n - 1) a b) y := by
  rw [K0, kernel_action, feature_sample_complete hn hδ]
  have hk : 1 ≤ y.rank := rank_pos y
  have hk0 : (y.rank : ℝ) ≠ 0 := by exact_mod_cast (show y.rank ≠ 0 by omega)
  have hN : ((n - 1 : ℕ) : ℝ) ≠ 0 := ne_of_gt (complete_denominator_pos hn)
  have hstop :
      (∑ w ∈ y.cache, ∑ i : Fin n, if hi : i ≠ w then complete n w i *
          feature δ a b (sampled (y.cache.erase w) w i (Finset.not_mem_erase w _) hi)
          else 0) =
        ((((y.rank : ℝ) - 1) * a (y.rank - 1) +
            ((((n - 1 : ℕ) : ℝ)) - y.rank) * a y.rank - 2 * b y.rank) * z δ y +
          (((y.rank : ℝ) - 1) * b (y.rank - 1) +
            ((((n - 1 : ℕ) : ℝ)) - y.rank - 1) * b y.rank) *
              ((y.rank : ℝ) - 2) * z δ y) / ((n - 1 : ℕ) : ℝ) := by
    simp_rw [feature_sample_complete hn hδ]
    have ht (w : Fin n) (hw : w ∈ y.cache) :
        ((((y.cache.erase w).card : ℝ) * a (y.cache.erase w).card +
              ((((n - 1 : ℕ) : ℝ)) - (y.cache.erase w).card - 1) *
                a ((y.cache.erase w).card + 1) - 2 * b ((y.cache.erase w).card + 1)) *
            cacheX δ (y.cache.erase w) w +
          (((y.cache.erase w).card : ℝ) * b (y.cache.erase w).card +
              ((((n - 1 : ℕ) : ℝ)) - (y.cache.erase w).card - 2) *
                b ((y.cache.erase w).card + 1)) * cacheZ δ (y.cache.erase w)) /
              ((n - 1 : ℕ) : ℝ) =
        ((((y.rank : ℝ) - 1) * a (y.rank - 1) +
            ((((n - 1 : ℕ) : ℝ)) - y.rank) * a y.rank - 2 * b y.rank) * cacheX δ y.cache w +
          (((y.rank : ℝ) - 1) * b (y.rank - 1) +
            ((((n - 1 : ℕ) : ℝ)) - y.rank - 1) * b y.rank) *
              (z δ y - 2 * cacheX δ y.cache w)) / ((n - 1 : ℕ) : ℝ) := by
      have hc : (y.cache.erase w).card = y.rank - 1 := Finset.card_erase_of_mem hw
      rw [hc, Nat.sub_add_cancel hk, Nat.cast_sub hk, Nat.cast_one,
        cacheX_erase_self hδ y.cache w hw, cacheZ_erase hδ y.cache w hw]
      change _ = _
      unfold z
      change _ = _
      dsimp only [cacheZ]
      ring
    rw [Finset.sum_congr rfl ht]
    rw [← Finset.sum_div, Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]
    simp only [Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul, ← Finset.mul_sum]
    have hz : (∑ w ∈ y.cache, cacheX δ y.cache w) = z δ y := rfl
    simp only [← Finset.mul_sum, hz]
    change _ = _
    ring
  rw [hstop]
  change (1 / 2 : ℝ) * _ + _ = _
  unfold feature featureCoeffA featureCoeffB x z
  change _ = _
  dsimp only [cacheX, cacheZ]
  generalize (((n - 1 : ℕ) : ℝ)) = N at *
  field_simp [hN, hk0]
  ring

/-- A fixed additive normalization of the genuine rank Poisson potential.
Its adjacent differences are the Appendix A recurrence gradients. -/
def rankPotential (N k : ℕ) : ℝ := -∑ j ∈ Finset.range k, (gradient N j : ℝ)

theorem rankPotential_step (N k : ℕ) :
    rankPotential N k - rankPotential N (k + 1) = (gradient N k : ℝ) := by
  simp only [rankPotential, Finset.sum_range_succ]
  ring

/-- The Appendix A gradient recurrence solves the actual labeled complete-chain
Poisson equation, including the lower and upper physical ranks. -/
theorem rankPotential_poisson {n : ℕ} (hn : 3 ≤ n) (y : State n) :
    rankPotential (n - 1) y.rank -
      (K0 n).mulVec (fun y => rankPotential (n - 1) y.rank) y =
        observable y - (c₀ (n - 1) : ℝ) := by
  rw [K0_rank (by omega)]
  have hk := rank_pos y
  have hkN := rank_le y
  have hN : ((n - 1 : ℕ) : ℝ) ≠ 0 := ne_of_gt (complete_denominator_pos (by omega))
  have h₁ := rankPotential_step (n - 1) y.rank
  have h₂ := rankPotential_step (n - 1) (y.rank - 1)
  rw [Nat.sub_add_cancel hk] at h₂
  have heq := gradient_poisson_equation (n - 1) y.rank (by omega) hk hkN
  have heqR := congrArg (fun r : ℚ => (r : ℝ)) heq
  push_cast at heqR
  unfold observable
  rw [show rankPotential (n - 1) (y.rank + 1) - rankPotential (n - 1) y.rank =
    -(gradient (n - 1) y.rank : ℝ) by linarith, h₂]
  have hk0 : (y.rank : ℝ) ≠ 0 := by exact_mod_cast (show y.rank ≠ 0 by omega)
  generalize (((n - 1 : ℕ) : ℝ)) = N at *
  field_simp [hN, hk0] at heqR ⊢
  linear_combination heqR

/-- The first perturbation source is the actual gradient source of A.15.
This uses the physical kernel derivative, and is not a scalar definition. -/
theorem perturbation_rankPotential {n : ℕ}
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) (y : State n) :
    (perturbation δ).mulVec (fun y => rankPotential (n - 1) y.rank) y =
      (gradient (n - 1) y.rank : ℝ) / 2 * x δ y +
        (gradient (n - 1) (y.rank - 1) : ℝ) / (2 * (y.rank : ℝ)) * z δ y := by
  rw [perturbation_rank δ hδ, rankPotential_step]
  have h := rankPotential_step (n - 1) (y.rank - 1)
  rw [Nat.sub_add_cancel (rank_pos y)] at h
  rw [h]

#print axioms feature_sample_complete
#print axioms K0_feature
#print axioms rankPotential_poisson
#print axioms perturbation_rankPotential

/-- The true stationary mean of the observable equals the printed binomial
normalization, derived from the actual Poisson residual and stationarity. -/
theorem center_eq_c₀ {n : ℕ} (hn : 3 ≤ n) : center n = (c₀ (n - 1) : ℝ) := by
  let h : State n → ℝ := fun y => rankPotential (n - 1) y.rank
  have hp : h - (K0 n).mulVec h = fun y => observable y - (c₀ (n - 1) : ℝ) := by
    funext y
    exact rankPotential_poisson hn y
  have hs := congrArg (dotProduct (nu0 (n := n))) hp
  rw [dotProduct_sub, Matrix.dotProduct_mulVec, nu0_stationary (by omega), sub_self] at hs
  have hr : dotProduct (nu0 (n := n)) (fun y => observable y - (c₀ (n - 1) : ℝ)) =
      center n - (c₀ (n - 1) : ℝ) := by
    simp only [dotProduct, mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul,
      nu0_sum (by omega : 2 ≤ n), one_mul, center]
  rw [hr] at hs
  linarith

/-- The actual centered matrix acts by the physical Poisson residual plus the
stationary mean. -/
theorem centeredMatrix_action {n : ℕ} (f : State n → ℝ) (y : State n) :
    (centeredMatrix n).mulVec f y =
      f y - (K0 n).mulVec f y + dotProduct nu0 f := by
  simp only [centeredMatrix, Matrix.add_mulVec, Matrix.sub_mulVec, Matrix.one_mulVec,
    Pi.add_apply, Pi.sub_apply]
  rfl

/-- Inverting a concrete physical Poisson solution amounts to subtracting its
stationary mean. Both the actual inverse and its uniqueness are proved. -/
theorem green_poisson_normalize {n : ℕ} (hn : 2 ≤ n)
    (f b : State n → ℝ) (hf : ∀ y, f y - (K0 n).mulVec f y = b y) :
    (green n).mulVec b = fun y => f y - dotProduct nu0 f := by
  apply green_eq_solution (centeredMatrix_det_isUnit hn)
  funext y
  rw [centeredMatrix_action]
  have hk : (K0 n).mulVec (fun y => f y - dotProduct nu0 f) y =
      (K0 n).mulVec f y - dotProduct nu0 f := by
    simp only [Matrix.mulVec, dotProduct, mul_sub, Finset.sum_sub_distrib,
      ← Finset.sum_mul, K0_row_sum hn, one_mul]
  have hm : dotProduct (nu0 (n := n)) (fun y => f y - dotProduct nu0 f) = 0 := by
    simp only [dotProduct, mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul,
      nu0_sum hn, one_mul, sub_self]
  rw [hk, hm]
  have hh := hf y
  linarith

/-- The first genuine Green application, with its additive normalization
fully determined rather than postulated. -/
theorem green_q {n : ℕ} (hn : 3 ≤ n) :
    (green n).mulVec (q n) = fun y => rankPotential (n - 1) y.rank -
      dotProduct (nu0 (n := n)) (fun y : State n => rankPotential (n - 1) y.rank) := by
  apply green_poisson_normalize (by omega)
  intro y
  rw [rankPotential_poisson hn, q, center_eq_c₀ hn]

theorem perturbation_const {n : ℕ} {δ : Matrix (Fin n) (Fin n) ℝ}
    (hδ : SymmetricBalanced δ) (t : ℝ) :
    (perturbation δ).mulVec (fun _ => t) = 0 := by
  funext y
  simpa using perturbation_rank δ hδ (fun _ => t) y

/-- Exact identification of the actual first perturbed Green application with
Appendix A.15, with no assumed resolvent or scalar. -/
theorem perturbation_green_q {n : ℕ} (hn : 3 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) (y : State n) :
    (perturbation δ).mulVec ((green n).mulVec (q n)) y =
      (gradient (n - 1) y.rank : ℝ) / 2 * x δ y +
        (gradient (n - 1) (y.rank - 1) : ℝ) / (2 * (y.rank : ℝ)) * z δ y := by
  rw [green_q hn]
  change (perturbation δ).mulVec ((fun y => rankPotential (n - 1) y.rank) -
    (fun _ => dotProduct (nu0 (n := n)) (fun y : State n => rankPotential (n - 1) y.rank))) y = _
  rw [Matrix.mulVec_sub, perturbation_const hδ, sub_zero]
  exact perturbation_rankPotential hδ y

#print axioms center_eq_c₀
#print axioms green_q
#print axioms perturbation_green_q

end
end SymmetricSector.Active
