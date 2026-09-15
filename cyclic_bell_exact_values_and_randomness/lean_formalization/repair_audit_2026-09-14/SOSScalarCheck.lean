import CyclicBell.ScalarData
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.FirstSOS
open D4
def pCoefficients : Fin 4 → ℂ := ![(s : ℂ), 2 * (alpha : ℂ), (s : ℂ), 0]
def qCoefficients : Fin 4 → ℂ := ![(beta : ℂ), (alpha : ℂ), (alpha : ℂ), (beta : ℂ)]
theorem coefficient_zero :
    (s : ℂ) * ((s : ℂ) + (k : ℂ) * (beta : ℂ)) = 0 := by
  have hr : s * (s + k * beta) = 0 := by rw [k_beta]; ring
  exact_mod_cast hr

theorem coefficient_one :
    (s : ℂ) * ((s : ℂ) + 2 * (alpha : ℂ) + (k : ℂ) * (alpha : ℂ)) = 1 := by
  have hr : s * (s + 2 * alpha + k * alpha) = 1 := by
    rw [k_alpha]
    unfold alpha
    nlinarith [s_sq, sc_product]
  exact_mod_cast hr

theorem p_coefficient_energy :
    (∑ j : Fin 4, star (pCoefficients j) * pCoefficients j) = 2 := by
  norm_num [pCoefficients, Fin.sum_univ_succ]
  apply Complex.ext <;> norm_num [Complex.mul_re, Complex.mul_im] <;>
    nlinarith [s_sq, alpha_sq]

theorem q_coefficient_energy :
    (∑ j : Fin 4, star (qCoefficients j) * qCoefficients j) = 1 := by
  norm_num [qCoefficients, Fin.sum_univ_succ]
  apply Complex.ext <;> norm_num [Complex.mul_re, Complex.mul_im] <;>
    nlinarith [alpha_sq, beta_sq]


end CyclicBell.FirstSOS
