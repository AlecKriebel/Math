import SymmetricSector.Definitions
import Mathlib.Data.Nat.Choose.Sum

namespace SymmetricSector
open scoped BigOperators

private def gradientFlow (N k : ℕ) : ℚ :=
  k * (Nat.choose (N-1) k : ℚ) * gradient N k

/-- A.3 in a form with no absent lower boundary index. -/
theorem gradient_recurrence (N k : ℕ) (hk : k+1 < N) :
    ((N:ℚ)-(k+1))*gradient N (k+1) =
      k*gradient N k + 2*N*(1/(k+1:ℚ)-c₀ N) := by
  rw [gradient, if_pos hk]
  have hd : ((N:ℚ)-(k+1)) ≠ 0 := by
    have hh : (k:ℚ)+1 < N := by exact_mod_cast hk
    linarith
  exact mul_div_cancel₀ _ hd

private theorem gradientFlow_step (N k : ℕ) (hk : k+1 < N) :
    gradientFlow N (k+1) - gradientFlow N k =
      2*(Nat.choose N (k+1):ℚ)-2*N*c₀ N*(Nat.choose (N-1) k:ℚ) := by
  have hN : 1 ≤ N := by omega
  have hkN : k ≤ N-1 := by omega
  have hc₁ : (Nat.choose (N-1) (k+1):ℚ)*(k+1) =
      (Nat.choose (N-1) k:ℚ)*((N:ℚ)-1-k) := by
    have hh := Nat.choose_succ_right_eq (N-1) k
    exact_mod_cast hh
  have hc₂ : (N:ℚ)*(Nat.choose (N-1) k:ℚ) =
      (Nat.choose N (k+1):ℚ)*(k+1) := by
    have hh := Nat.succ_mul_choose_eq (N-1) k
    simpa only [Nat.succ_eq_add_one, Nat.sub_add_cancel hN, Nat.cast_mul,
      Nat.cast_add, Nat.cast_one] using congrArg (fun x : ℕ => (x:ℚ)) hh
  have hr := gradient_recurrence N k hk
  have hd : (k+1:ℚ) ≠ 0 := by positivity
  have hr' := congrArg (fun x : ℚ => x*(k+1)) hr
  field_simp at hr'
  unfold gradientFlow
  push_cast
  apply (mul_right_cancel₀ hd)
  have he₁ := congrArg (fun x : ℚ => x*(Nat.choose (N-1) k:ℚ)) hr'
  have he₂ := congrArg (fun x : ℚ => x*gradient N (k+1)*(k+1)) hc₁
  linear_combination he₁ + he₂ + 2*hc₂

private theorem gradientFlow_sum (N k : ℕ) (hk : k < N) :
    gradientFlow N k =
      2*(∑ i ∈ Finset.range k, (Nat.choose N (i+1):ℚ)) -
      2*N*c₀ N*(∑ i ∈ Finset.range k, (Nat.choose (N-1) i:ℚ)) := by
  induction k with
  | zero => simp [gradientFlow]
  | succ k ih =>
    have hi := ih (by omega)
    have hs := gradientFlow_step N k hk
    simp only [Finset.sum_range_succ]
    linarith

/-- The terminal A.3 equation is a theorem for the actual recursive gradient,
including its binomial normalization `c₀`. -/
theorem gradient_terminal (N : ℕ) (hN : 2 ≤ N) :
    ((N:ℚ)-1)*gradient N (N-1) = 2*N*c₀ N-2 := by
  have hN1 : 1 ≤ N := by omega
  have hN0 : (N:ℚ) ≠ 0 := by exact_mod_cast (show N ≠ 0 by omega)
  have hs := gradientFlow_sum N (N-1) (by omega)
  have hsum (m : ℕ) : (∑ i ∈ Finset.range (m+1), (Nat.choose m i:ℚ)) = 2^m := by
    exact_mod_cast Nat.sum_range_choose m
  have hb : (∑ i ∈ Finset.range (N-1), (Nat.choose (N-1) i:ℚ)) = 2^(N-1)-1 := by
    have hh := hsum (N-1)
    rw [Finset.sum_range_succ, Nat.choose_self, Nat.cast_one] at hh
    linarith
  have ha : (∑ i ∈ Finset.range (N-1), (Nat.choose N (i+1):ℚ)) = 2^N-2 := by
    have hh := hsum N
    have hshift := Finset.sum_range_succ' (fun i => (Nat.choose N i:ℚ)) (N-1)
    rw [Nat.sub_add_cancel hN1] at hshift
    rw [Finset.sum_range_succ, Nat.choose_self, Nat.cast_one] at hh
    simp only [Nat.choose_zero_right, Nat.cast_one] at hshift
    linarith
  rw [ha, hb] at hs
  unfold gradientFlow at hs
  simp only [Nat.choose_self, Nat.cast_one, mul_one, Nat.cast_sub hN1] at hs
  have hc : c₀ N * ((N:ℚ)*2^(N-1)) = 2^N-1 := by
    apply div_mul_cancel₀
    exact mul_ne_zero hN0 (pow_ne_zero _ (by norm_num))
  nlinarith

/-- A.3 including its terminal rank, now derived without an assumed boundary. -/
theorem gradient_poisson_equation (N k : ℕ) (hN : 2 ≤ N) (hk : 1 ≤ k) (hkN : k ≤ N) :
    ((N:ℚ)-k)*gradient N k - ((k:ℚ)-1)*gradient N (k-1) =
      2*N*(1/(k:ℚ)-c₀ N) := by
  by_cases heq : k = N
  · subst k
    have ht := gradient_terminal N hN
    have hN0 : (N:ℚ) ≠ 0 := by exact_mod_cast (show N ≠ 0 by omega)
    have hi : (N:ℚ)*(1/(N:ℚ)) = 1 := by field_simp
    simp only [sub_self, zero_mul]
    nlinarith
  · have hr := gradient_recurrence N (k-1) (by omega)
    rw [Nat.sub_add_cancel hk] at hr
    rw [Nat.cast_sub hk, Nat.cast_one] at hr
    linear_combination hr

/-- The exact second-order Dirichlet equation for the actual gradients. -/
theorem gradient_second_order (N k : ℕ) (hN : 2 ≤ N) (hk : 1 ≤ k) (hkN : k < N) :
    (N:ℚ)*gradient N k - ((k:ℚ)-1)*gradient N (k-1) -
      ((N:ℚ)-k-1)*gradient N (k+1) = 2*N/((k:ℚ)*(k+1)) := by
  have h₁ := gradient_poisson_equation N k hN hk (by omega)
  have h₂ := gradient_poisson_equation N (k+1) hN (by omega) (by omega)
  push_cast at h₂
  have hk0 : (k:ℚ) ≠ 0 := by exact_mod_cast (show k ≠ 0 by omega)
  have hk1 : (k+1:ℚ) ≠ 0 := by positivity
  have hi : 1/(k:ℚ) - 1/(k+1:ℚ) = 1/((k:ℚ)*(k+1)) := by
    field_simp
    <;> ring
  calc
    (N:ℚ)*gradient N k - ((k:ℚ)-1)*gradient N (k-1) -
      ((N:ℚ)-k-1)*gradient N (k+1) = 2*N*(1/(k:ℚ)-1/(k+1:ℚ)) := by
        linear_combination h₁ - h₂
    _ = 2*N/((k:ℚ)*(k+1)) := by rw [hi]; ring

/-- A finite maximum principle with precisely the absent endpoint coefficients.
The values of `x 0` and `x N` require no assumptions because their multipliers vanish. -/
theorem rank_maximum_principle (N : ℕ) (hN : 2 ≤ N) (x : ℕ → ℚ)
    (hx : ∀ k, 1 ≤ k → k < N →
      (N:ℚ)*x k ≤ ((k:ℚ)-1)*x (k-1) + ((N:ℚ)-k-1)*x (k+1)) :
    ∀ k, 1 ≤ k → k < N → x k ≤ 0 := by
  intro k hk hkN
  by_contra hbad
  have hpos : 0 < x k := lt_of_not_ge hbad
  have hmem : k ∈ Finset.Icc 1 (N-1) := Finset.mem_Icc.mpr ⟨hk, by omega⟩
  obtain ⟨i, hi, hmax⟩ := Finset.exists_max_image (Finset.Icc 1 (N-1)) x ⟨k,hmem⟩
  have hi1 := (Finset.mem_Icc.mp hi).1
  have hiN : i < N := by have := (Finset.mem_Icc.mp hi).2; omega
  have hipos : 0 < x i := lt_of_lt_of_le hpos (hmax k hmem)
  have hrow := hx i hi1 hiN
  have hileft : ((i:ℚ)-1)*x (i-1) ≤ ((i:ℚ)-1)*x i := by
    by_cases heq : i=1
    · subst i
      norm_num
    · apply mul_le_mul_of_nonneg_left
      · exact hmax (i-1) (Finset.mem_Icc.mpr ⟨by omega,by omega⟩)
      · have hh : (1:ℚ) ≤ i := by exact_mod_cast hi1
        linarith
  have hiright : ((N:ℚ)-i-1)*x (i+1) ≤ ((N:ℚ)-i-1)*x i := by
    by_cases heq : i+1=N
    · have hh : (i:ℚ)+1=N := by exact_mod_cast heq
      have hz : (N:ℚ)-i-1=0 := by linarith
      rw [hz]
      simp
    · apply mul_le_mul_of_nonneg_left
      · exact hmax (i+1) (Finset.mem_Icc.mpr ⟨by omega,by omega⟩)
      · have hh : (i:ℚ)+1 ≤ N := by exact_mod_cast (show i+1 ≤ N by omega)
        linarith
  nlinarith

/-- The second-order rank operator; its endpoint multipliers vanish. -/
def rankL (N : ℕ) (x : ℕ → ℚ) (k : ℕ) : ℚ :=
  (N:ℚ)*x k - ((k:ℚ)-1)*x (k-1) - ((N:ℚ)-k-1)*x (k+1)

private theorem reciprocal_rankL (N k : ℕ) (hk : 1 ≤ k) :
    rankL N (fun j => 2/(j:ℚ)) k =
      2*N/((k:ℚ)*(k+1)) + if k=1 then 2 else 0 := by
  unfold rankL
  by_cases heq : k=1
  · subst k
    norm_num
    ring
  · rw [if_neg heq]
    dsimp only
    have hk0 : (k:ℚ) ≠ 0 := by exact_mod_cast (show k ≠ 0 by omega)
    have hk1 : (k+1:ℚ) ≠ 0 := by positivity
    have hkm : (k:ℚ)-1 ≠ 0 := by
      have hh : (2:ℚ) ≤ k := by exact_mod_cast (show 2 ≤ k by omega)
      linarith
    rw [Nat.cast_sub hk, Nat.cast_one]
    push_cast
    field_simp
    <;> ring

/-- The actual recursive Poisson gradients satisfy the manuscript upper bound. -/
theorem gradient_le_reciprocal (N k : ℕ) (hN : 2 ≤ N) (hk : 1 ≤ k) (hkN : k < N) :
    gradient N k ≤ 2/(k:ℚ) := by
  have hm := rank_maximum_principle N hN (fun j => gradient N j - 2/(j:ℚ))
  have hdom : ∀ j, 1 ≤ j → j < N →
      (N:ℚ)*(gradient N j-2/(j:ℚ)) ≤
      ((j:ℚ)-1)*(gradient N (j-1)-2/((j-1:ℕ):ℚ)) +
      ((N:ℚ)-j-1)*(gradient N (j+1)-2/((j+1:ℕ):ℚ)) := by
    intro j hj hjN
    have hg := gradient_second_order N j hN hj hjN
    have hb := reciprocal_rankL N j hj
    unfold rankL at hb
    have hnonneg : (0:ℚ) ≤ if j=1 then 2 else 0 := by split_ifs <;> norm_num
    dsimp at hb
    linarith
  have hh := hm hdom k hk hkN
  linarith

private theorem scaled_reciprocal_subsolution (N k : ℕ) (hN : 2 ≤ N) (hk : 1 ≤ k) :
    ((N:ℚ)-2)/N * rankL N (fun j => 2/(j:ℚ)) k ≤ 2*N/((k:ℚ)*(k+1)) := by
  have hNpos : (0:ℚ) < N := by exact_mod_cast (show 0 < N by omega)
  have hα : ((N:ℚ)-2)/N ≤ 1 := (div_le_one hNpos).2 (by linarith)
  rw [reciprocal_rankL N k hk]
  by_cases heq : k=1
  · subst k
    norm_num
    rw [div_mul_eq_mul_div]
    apply (div_le_iff₀ hNpos).2
    nlinarith
  · rw [if_neg heq, add_zero]
    have hforce : (0:ℚ) ≤ 2*N/((k:ℚ)*(k+1)) := by positivity
    simpa only [one_mul] using mul_le_mul_of_nonneg_right hα hforce

/-- The actual recursive gradients satisfy both bounds in (A.3a), for every
physical rank and every `N≥2`. No binomial-tail inequality is assumed. -/
theorem gradient_bounds (N k : ℕ) (hN : 2 ≤ N) (hk : 1 ≤ k) (hkN : k < N) :
    2*((N:ℚ)-2)/(N*k) ≤ gradient N k ∧ gradient N k ≤ 2/(k:ℚ) := by
  refine ⟨?_, gradient_le_reciprocal N k hN hk hkN⟩
  let α : ℚ := ((N:ℚ)-2)/N
  have hm := rank_maximum_principle N hN (fun j => α*(2/(j:ℚ)) - gradient N j)
  have hdom : ∀ j, 1 ≤ j → j < N →
      (N:ℚ)*(α*(2/(j:ℚ))-gradient N j) ≤
      ((j:ℚ)-1)*(α*(2/((j-1:ℕ):ℚ))-gradient N (j-1)) +
      ((N:ℚ)-j-1)*(α*(2/((j+1:ℕ):ℚ))-gradient N (j+1)) := by
    intro j hj hjN
    have hg := gradient_second_order N j hN hj hjN
    have hb := scaled_reciprocal_subsolution N j hN hj
    change α*rankL N (fun i => 2/(i:ℚ)) j ≤ _ at hb
    unfold rankL at hb
    dsimp at hb
    nlinarith
  have hh := hm hdom k hk hkN
  have hid : α*(2/(k:ℚ)) = 2*((N:ℚ)-2)/(N*k) := by dsimp [α]; ring
  rw [hid] at hh
  linarith

#print axioms gradient_recurrence
#print axioms gradient_terminal
#print axioms gradient_second_order
#print axioms rank_maximum_principle
#print axioms gradient_bounds

/-- The actual Poisson gradient is strictly positive at every retained rank. -/
theorem gradient_pos (N k : ℕ) (hN : 3 ≤ N) (hk : 1 ≤ k) (hkN : k < N) :
    0 < gradient N k := by
  have hb := (gradient_bounds N k (by omega) hk hkN).1
  have hNq : (3:ℚ) ≤ N := by exact_mod_cast hN
  have hkq : (1:ℚ) ≤ k := by exact_mod_cast hk
  have hl : 0 < 2*((N:ℚ)-2)/(N*k) := by
    apply div_pos
    · nlinarith
    · exact mul_pos (by linarith) (by linarith)
  exact hl.trans_le hb

#print axioms gradient_pos

end SymmetricSector
