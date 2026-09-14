import Mathlib

/-!
# Elementary analytic polynomial certificates for the symmetric sector

These statements use exactly the polynomials in Appendix A, equations (A.23)
and (A.34), rather than merely checking their discriminants. All proofs are
kernel checked. They do not, by themselves, identify the reduced scalar with
an active-chain quadratic form or establish the needed matrix comparison.
-/

namespace SymmetricSector

/-- The interior residual polynomial printed as (A.23). -/
def barrierPolynomial (N k : ℚ) : ℚ :=
  21*N^2*k + 14*N^2 - 64*N*k^2 - 57*N*k + 50*k^3 + 36*k^2 - 14*k

/-- The cleared debt comparison polynomial printed as (A.34). -/
def tailPolynomial (N j : ℚ) : ℚ :=
  1881*N^2*j + 1881*N^2 - 6250*N*j^2 - 21278*N*j - 10032*N +
    6000*j^3 + 12000*j^2 + 10032*j + 12540

/-- A sum-of-squares identity replacing the cubic discriminant argument. -/
theorem tailPolynomial_sos (N j : ℚ) :
    24000 * tailPolynomial N j =
      j*(12000*j-6250*N)^2 + N*j*(6081500*N-510672000) +
      N*(45144000*N-240768000) + 288000000*j^2 + 240768000*j + 300960000 := by
  unfold tailPolynomial
  ring

/-- The actual tail polynomial is positive on a larger domain than required. -/
theorem tailPolynomial_pos (N j : ℚ) (hN : 84 ≤ N) (hj : 0 ≤ j) :
    0 < tailPolynomial N j := by
  have hN0 : 0 ≤ N := by linarith
  have h₁ : 0 ≤ j*(12000*j-6250*N)^2 := mul_nonneg hj (sq_nonneg _)
  have h₂ : 0 ≤ N*j*(6081500*N-510672000) :=
    mul_nonneg (mul_nonneg hN0 hj) (by linarith)
  have h₃ : 0 ≤ N*(45144000*N-240768000) :=
    mul_nonneg hN0 (by linarith)
  have h₄ : 0 ≤ j^2 := sq_nonneg _
  have hid := tailPolynomial_sos N j
  nlinarith

private def radialCubic (x : ℚ) := 50*x^3-64*x^2+21*x
private def radialQuadratic (x : ℚ) := 36*x^2-57*x+14

private theorem radialCubic_nonneg (x : ℚ) (hx : 0 ≤ x) :
    0 ≤ radialCubic x := by
  have hid : radialCubic x = x*(50*(x-16/25)^2+13/25) := by
    unfold radialCubic
    ring
  rw [hid]
  exact mul_nonneg hx (by positivity)

private theorem barrierDerivative_pos (x : ℚ) (hx : 0 ≤ x) :
    0 < 50*radialCubic x + radialQuadratic x := by
  have hid : 50*radialCubic x + radialQuadratic x =
      2500*x*(x-16/25)^2 + ((72*x-31)^2+1055)/144 := by
    unfold radialCubic radialQuadratic
    ring
  rw [hid]
  have : 0 ≤ 2500*x*(x-16/25)^2 := by positivity
  positivity

private theorem barrierBase_pos (x : ℚ) (hx : 0 ≤ x) :
    0 < 625*radialCubic x + 25*radialQuadratic x -14*x := by
  have hid : 625*radialCubic x + 25*radialQuadratic x -14*x =
      31250*x*(x-16/25)^2 + ((900*x-557)^2+4751)/900 := by
    unfold radialCubic radialQuadratic
    ring
  rw [hid]
  have : 0 ≤ 31250*x*(x-16/25)^2 := by positivity
  positivity

/-- The actual barrier polynomial is positive for real-rank rational inputs,
not just the physical integer ranks. The endpoint `N = 24` is separate. -/
theorem barrierPolynomial_pos (N k : ℚ) (hN : 25 ≤ N) (hk : 0 ≤ k) :
    0 < barrierPolynomial N k := by
  have hNpos : 0 < N := by linarith
  have hx : 0 ≤ k/N := div_nonneg hk (le_of_lt hNpos)
  have hm : 0 ≤ N-25 := by linarith
  have h₁ := radialCubic_nonneg (k/N) hx
  have h₂ := barrierDerivative_pos (k/N) hx
  have h₃ := barrierBase_pos (k/N) hx
  have hm₁ : 0 ≤ (N-25)^2 * radialCubic (k/N) := mul_nonneg (sq_nonneg _) h₁
  have hm₂ : 0 ≤ (N-25) * (50*radialCubic (k/N)+radialQuadratic (k/N)) :=
    mul_nonneg hm (le_of_lt h₂)
  have hid : barrierPolynomial N k = N *
      ((N-25)^2*radialCubic (k/N) +
       (N-25)*(50*radialCubic (k/N)+radialQuadratic (k/N)) +
       (625*radialCubic (k/N)+25*radialQuadratic (k/N)-14*(k/N))) := by
    unfold barrierPolynomial radialCubic radialQuadratic
    field_simp
    <;> ring
  rw [hid]
  apply mul_pos hNpos
  linarith

/-- Exact physical-rank minimum at the isolated order `N = 24`. -/
theorem barrierPolynomial_24_min (k : ℕ) (hk : 2 ≤ k) (hkN : k < 24) :
    24 ≤ barrierPolynomial 24 (k:ℚ) := by
  interval_cases k <;> norm_num [barrierPolynomial]

theorem barrierPolynomial_24_at_15 : barrierPolynomial 24 15 = 24 := by
  norm_num [barrierPolynomial]

/-- The contraction constant in (A.27). -/
def phaseContraction (N : ℚ) : ℚ := (2*N-5)/(2*N*(N-2))

/-- The alternating-phase tail ratio in (A.32). -/
def phaseEpsilon (N : ℚ) : ℚ := (25/11) * phaseContraction N / (1-phaseContraction N)

theorem phaseContraction_denominator_pos (N : ℚ) (hN : 3 ≤ N) :
    0 < 2*N*(N-2) := by
  have h₁ : 0 < N := by linarith
  have h₂ : 0 < N-2 := by linarith
  positivity

theorem phaseContraction_nonneg (N : ℚ) (hN : 3 ≤ N) : 0 ≤ phaseContraction N := by
  unfold phaseContraction
  apply div_nonneg <;> nlinarith

theorem phaseContraction_lt_one (N : ℚ) (hN : 3 ≤ N) : phaseContraction N < 1 := by
  have hd : 0 < 2*N*(N-2) := by
    have h₁ : 0 < N := by linarith
    have h₂ : 0 < N-2 := by linarith
    positivity
  unfold phaseContraction
  apply (div_lt_one hd).2
  nlinarith [sq_nonneg (N-3)]

/-- The printed cleared tail inequality, proved on its full half-line. -/
theorem epsilonPolynomial_pos (N : ℚ) (hN : 46 ≤ N) :
    0 < 22*N^2-1066*N+2555 := by
  have hm : 0 ≤ N-46 := by linarith
  nlinarith [sq_nonneg (N-46)]

/-- The full rational tail implication, including its positive denominators. -/
theorem phaseEpsilon_lt_one_twentieth (N : ℚ) (hN : 46 ≤ N) : phaseEpsilon N < 1/20 := by
  have hN3 : 3 ≤ N := by linarith
  have hd : 0 < 2*N*(N-2) := by
    have h₁ : 0 < N := by linarith
    have h₂ : 0 < N-2 := by linarith
    positivity
  have hc := phaseContraction_lt_one N hN3
  have he := epsilonPolynomial_pos N hN
  have hmul : phaseContraction N * (2*N*(N-2)) = 2*N-5 := by
    exact div_mul_cancel₀ _ (ne_of_gt hd)
  unfold phaseEpsilon
  apply (div_lt_iff₀ (by linarith : 0 < 1-phaseContraction N)).2
  apply (mul_lt_mul_right hd).mp
  nlinarith [hmul]

#print axioms tailPolynomial_pos
#print axioms barrierPolynomial_pos
#print axioms barrierPolynomial_24_min
#print axioms phaseContraction_denominator_pos
#print axioms phaseEpsilon_lt_one_twentieth

end SymmetricSector
