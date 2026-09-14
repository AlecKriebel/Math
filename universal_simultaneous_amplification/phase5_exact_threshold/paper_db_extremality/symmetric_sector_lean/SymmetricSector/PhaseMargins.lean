import SymmetricSector.FiniteMargins
import SymmetricSector.AnalyticTail

namespace SymmetricSector

/-- The exact Appendix A phase allowance is strictly below one at every
order where the Schur/barrier argument invokes it. This theorem concerns
the actual recurrence and maximum; it does not assume a scalar bound. -/
theorem all_phase_margin (N : ℕ) (hN : 40 ≤ N) : beta N + epsilon N < 1 := by
  by_cases hfinite : N ≤ 287
  · exact finite_phase_positive hN hfinite
  · exact analytic_phase_margin N (by omega)

end SymmetricSector
