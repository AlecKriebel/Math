import SymmetricSector.Analytic
import SymmetricSector.Margins

namespace SymmetricSector

/-- Rational subsolution step for the actual recurrence, avoiding square roots. -/
theorem rational_subsolution_step (N k u : ℚ) (hN : 288 ≤ N) (hk : 1 ≤ k)
    (hkN : k ≤ N-1) (hu : 24*N/(25*N-24*(k-1)) ≤ u) :
    24*N/(25*N-24*k) ≤ (2*N+(k-1)*u)/(2*N-k) := by
  have hNpos : 0 < N := by linarith
  have hd₁ : 0 < 25*N-24*(k-1) := by linarith
  have hd₂ : 0 < 25*N-24*k := by linarith
  have hd₃ : 0 < 2*N-k := by linarith
  have hstep : (2*N+(k-1)*(24*N/(25*N-24*(k-1))))/(2*N-k) ≤
      (2*N+(k-1)*u)/(2*N-k) := by
    apply (div_le_div_iff_of_pos_right hd₃).2
    exact add_le_add_left (mul_le_mul_of_nonneg_left hu (by linarith)) _
  apply le_trans ?_ hstep
  apply (div_le_div_iff₀ hd₂ hd₃).2
  apply (mul_le_mul_right hd₁).mp
  have hnum : 0 ≤ 2*N^2*(25*N-24*k-276) := by
    apply mul_nonneg (by positivity)
    linarith
  field_simp
  nlinarith

/-- Universal rational lower bound for the actual recursively defined `t`. -/
theorem t_lower_analytic (N k : ℕ) (hN : 288 ≤ N) (hk : 1 ≤ k) (hkN : k < N) :
    24*(N:ℚ)/(25*(N:ℚ)-24*(k:ℚ)) ≤ t N k := by
  induction k with
  | zero => omega
  | succ k ih =>
    have hNq : (288:ℚ) ≤ N := by exact_mod_cast hN
    have hkNq : (k:ℚ)+1 ≤ (N:ℚ)-1 := by
      have hh : (k:ℚ)+1+1 ≤ (N:ℚ) := by exact_mod_cast (show k+1+1 ≤ N by omega)
      linarith
    by_cases hk0 : k = 0
    · subst k
      simp only [t, Nat.cast_zero, zero_mul, add_zero, Nat.cast_one, zero_add, mul_one]
      have hd₁ : (0:ℚ) < 25*N-24 := by linarith
      have hd₂ : (0:ℚ) < 2*N-1 := by linarith
      apply (div_le_div_iff₀ hd₁ hd₂).2
      nlinarith
    · have hik := ih (by omega) (by omega)
      have hstep := rational_subsolution_step (N:ℚ) ((k:ℚ)+1) (t N k)
        hNq (by have : (0:ℚ) ≤ k := Nat.cast_nonneg k; linarith) hkNq (by simpa using hik)
      simpa only [t, Nat.cast_add, Nat.cast_one, add_sub_cancel_right] using hstep

/-- The exact `epsilon` definition agrees with the rational analytic one. -/
theorem epsilon_eq_phaseEpsilon (N : ℕ) : epsilon N = phaseEpsilon (N:ℚ) := rfl

theorem epsilon_lt_one_twentieth (N : ℕ) (hN : 46 ≤ N) : epsilon N < 1/20 := by
  rw [epsilon_eq_phaseEpsilon]
  exact phaseEpsilon_lt_one_twentieth _ (by exact_mod_cast hN)

/-- The polynomial certificate implies the actual termwise debt bound once the
rational radial subsolution is available. All factors being cleared are positive. -/
theorem rational_debt_bound (N j u : ℚ) (hN : 288 ≤ N) (hj : 1 ≤ j)
    (hjN : j ≤ N-2) (hu : 24*N/(25*N-24*j) ≤ u) :
    (4*(j+2)/(3*(j+1)*(N-2))) /
      ((11/25)*((3*N*j+3*N-8*j-10)/(3*N*j*(j+1)))*u) < 19/20 := by
  have hNpos : 0 < N := by linarith
  have hjpos : 0 < j := by linarith
  have hj1 : 0 < j+1 := by linarith
  have hN2 : 0 < N-2 := by linarith
  have hden : 0 < 25*N-24*j := by linarith
  have hellnum : 0 < 3*N*j+3*N-8*j-10 := by
    have hh : 0 ≤ (N-288)*(j-1) := mul_nonneg (by linarith) (by linarith)
    nlinarith
  have hell : 0 < (3*N*j+3*N-8*j-10)/(3*N*j*(j+1)) := by positivity
  have hlow : 0 < 24*N/(25*N-24*j) := by positivity
  have hnum : 0 ≤ 4*(j+2)/(3*(j+1)*(N-2)) := by positivity
  have hmul : (11/25)*((3*N*j+3*N-8*j-10)/(3*N*j*(j+1))) *
      (24*N/(25*N-24*j)) ≤
      (11/25)*((3*N*j+3*N-8*j-10)/(3*N*j*(j+1)))*u :=
    mul_le_mul_of_nonneg_left hu (by positivity)
  have hdenlow : 0 < (11/25)*((3*N*j+3*N-8*j-10)/(3*N*j*(j+1))) *
      (24*N/(25*N-24*j)) := by positivity
  apply lt_of_le_of_lt (div_le_div_of_nonneg_left hnum hdenlow hmul)
  have hid : (4*(j+2)/(3*(j+1)*(N-2))) /
      ((11/25)*((3*N*j+3*N-8*j-10)/(3*N*j*(j+1)))*(24*N/(25*N-24*j))) =
      25*j*(j+2)*(25*N-24*j)/(66*(N-2)*(3*N*j+3*N-8*j-10)) := by
    field_simp
    <;> ring
  rw [hid]
  apply (div_lt_iff₀ (by positivity : 0 < 66*(N-2)*(3*N*j+3*N-8*j-10))).2
  have hg := tailPolynomial_pos N j (by linarith) (by linarith)
  unfold tailPolynomial at hg
  nlinarith

/-- The genuine terms maximized in beta satisfy the analytic debt estimate. -/
theorem betaTerm_lt_nineteen_twentieths (N j : ℕ) (hN : 288 ≤ N)
    (hj : 1 ≤ j) (hjN : j ≤ N-2) : betaTerm N j < 19/20 := by
  have hu := t_lower_analytic N j hN hj (by omega)
  have hjNq : (j:ℚ) ≤ (N:ℚ)-2 := by
    have hh : (j:ℚ)+2 ≤ (N:ℚ) := by exact_mod_cast (show j+2 ≤ N by omega)
    linarith
  exact rational_debt_bound (N:ℚ) (j:ℚ) (t N j)
    (by exact_mod_cast hN) (by exact_mod_cast hj) hjNq hu

/-- The all-order analytic range for the exact physical-rank maximum. -/
theorem beta_lt_nineteen_twentieths (N : ℕ) (hN : 288 ≤ N) : beta N < 19/20 := by
  unfold beta
  split_ifs with h
  · apply (Finset.sup'_lt_iff h).2
    intro b hb
    rcases Finset.mem_image.mp hb with ⟨j, hj, rfl⟩
    exact betaTerm_lt_nineteen_twentieths N j hN (Finset.mem_Icc.mp hj).1
      (Finset.mem_Icc.mp hj).2
  · norm_num

/-- The analytic tail of the *actual* beta and epsilon in Appendix (A.32). -/
theorem analytic_phase_margin (N : ℕ) (hN : 288 ≤ N) : beta N + epsilon N < 1 := by
  have hb := beta_lt_nineteen_twentieths N hN
  have he := epsilon_lt_one_twentieth N (by omega)
  linarith

#print axioms rational_subsolution_step
#print axioms t_lower_analytic
#print axioms epsilon_lt_one_twentieth
#print axioms betaTerm_lt_nineteen_twentieths
#print axioms analytic_phase_margin

end SymmetricSector
