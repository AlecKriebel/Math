# Independent review request: critical WARM line partials

Overall proposed queue disposition: **unsolved, 5/5**. Please independently audit every probability and infinite-volume step; the finite exact checker is not a substitute. The five author turns are frozen, and review is not a sixth search turn.

Primary source: OWR 12/2023, Victor Kleptsyn's contribution, printed pp. 653–656, Conjecture 2 on p. 655. Cached PDFs/text are in sources/. Couzinie–Hirsch arXiv:2010.03347v2 defines unit initialization and proves alpha<1; it does not settle alpha=1. The longer Aletti et al. problem collection repeats the initial-count omission. This packet explicitly proves only unit-initialized claims. Neighboring trace ants and supercritical lattice constructions are distinct.

Important attacks:

- Harmonic martingale compensators and L2 bounds; distinct edge martingales have disjoint jumps, not independent histories. Check the graphical construction's spatial covariance and shift-two ergodicity.
- Poisson one-edge and pair-sum bounds; exponent-one proof via the absolutely continuous exponential of the compensated harmonic count, without conditioning on a future event.
- Exact expectation identities E lambda_i=1 and E N_i=t+1 under translation invariance; no infinite sum of weights or Lyapunov function is taken.
- The log-pair Taylor error bound and its integrability; Fubini/Tonelli passage to pathwise local dissipation; the asymptotic-continuity argument in logarithmic time with jump paths and convergent martingale tails.
- The exact harmonic-entropy identity, the bound 0<=h(n)-log n<=gamma, and the resulting almost-sure adjacent-pair convergence.
- Classification of any full pointwise limit, including boundary zeros; deterministic pathwise liminf/limsup envelopes. Do not use ergodicity for a weak limiting law.
- Fifth-turn deterministic selected times and even window lengths. Recheck E(1/T)<=1, the boundary O(sqrt(tau)/L) bound, the O(L sqrt(D)) uniform local phase error, orthogonal-martingale O(1/L) variance, summability choices tau_n D(tau_n)<=n^-16 and L_n approximately n^3 sqrt(tau_n), and the pathwise endpoint-exclusion/log-ratio argument. Confirm one probability-one event for all countably many fixed edges.
- Preserve the distinction between this deterministic almost-sure subsequence and the unproved full temporal limit. No uniform bound on selected-time gaps is available. The boundary-flux integral is not declared convergent or absolutely integrable from an L2 estimate.

Write the review separately and leave all frozen mathematical files unchanged. Public review/check files can later be appended to the problem branch by the author under the parent publication gate. Source PDFs/text and full imported records remain local.
