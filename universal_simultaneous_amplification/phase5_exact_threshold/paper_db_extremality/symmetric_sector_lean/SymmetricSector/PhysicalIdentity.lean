import SymmetricSector.ChannelFeatures
import SymmetricSector.Reward

/-! The Appendix A.17 identity for the actual labeled active-chain expression.
No coefficient equation, feature identity, stationary law, Green inverse,
or scalar sign is assumed in the principal identity below. Its remaining
upstream interpretation as a fixation Hessian is outside this formal component.
-/
namespace SymmetricSector.Active
noncomputable section
open scoped BigOperators

/-- Exact reward pairing at the manuscript's population index n, with N=n−1. -/
theorem coefficientFeature_reward {n : ℕ} (hn : 4 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ)
    (c : Channel (n - 1) → ℚ) :
    dotProduct nu0 ((perturbation δ).mulVec (coefficientFeature δ c)) =
      frobeniusSq δ * ((dotProduct (reward (n - 1)) c : ℚ) : ℝ) := by
  cases n with
  | zero => omega
  | succ N =>
    have hN : 3 ≤ N := by omega
    simpa only [coefficientFeature, Nat.succ_sub_one] using
      nu0_perturbation_coeff_feature hN δ hδ c

/-- The second true Green application is precisely the physical feature of the
unique actual finite-channel solution. This is proved using both genuine
Poisson equations, stationary centering, and invertibility of the labeled chain. -/
theorem green_perturbation_green_q {n : ℕ} (hn : 4 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) :
    (green n).mulVec ((perturbation δ).mulVec ((green n).mulVec (q n))) =
      coefficientFeature δ (coefficientSolution (n - 1)) := by
  apply green_eq_solution (centeredMatrix_det_isUnit (by omega))
  funext y
  rw [centeredMatrix_action]
  have hmean : dotProduct nu0
      (coefficientFeature δ (coefficientSolution (n - 1))) = 0 := by
    exact nu0_feature_zero δ hδ _ _
  rw [hmean, add_zero]
  have hp := congrFun (coefficientFeature_poisson hn hδ) y
  change coefficientFeature δ (coefficientSolution (n - 1)) y -
      (K0 n).mulVec (coefficientFeature δ (coefficientSolution (n - 1))) y =
    (perturbation δ).mulVec (fun y => rankPotential (n - 1) y.rank) y at hp
  rw [hp, perturbation_rankPotential hδ, perturbation_green_q (by omega) hδ]

/-- Appendix A.17: the actual physical quadratic expression ν₀ Δ G Δ G q
is exactly the squared Frobenius norm times the manuscript's reduced scalar.
The statement includes the zero perturbation and uses no division by its norm. -/
theorem R2_eq_frobeniusSq_mul_reducedScalar {n : ℕ} (hn : 4 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) :
    R2 δ = frobeniusSq δ * (reducedScalar (n - 1) : ℝ) := by
  unfold R2
  rw [green_perturbation_green_q hn hδ,
    coefficientFeature_reward hn hδ]
  rfl

#print axioms coefficientFeature_reward
#print axioms green_perturbation_green_q
#print axioms R2_eq_frobeniusSq_mul_reducedScalar

end
end SymmetricSector.Active
