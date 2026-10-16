# Independent geometric reconstruction and attack memo

Timestamp: 2026-10-15T09:29:20.138854+00:00
Checkpoint completion estimate: 25% of this geometric/invariant-region audit.

## Independence and primary scope

This memo was written before reading the author's PROOF.md, certificates, verifier, or inherited audit reports. It uses only the task's exact target statement and the actual primary-source text: the April 25, 2007 notes, global model on printed pp. 2–5 and section 6.4 on printed p. 40; and all 11 printed pages of arXiv:1209.5120v1. No source text is republished here.

The 2007 deterministic model has finitely many fixed cities and weights in the probability simplex, with z_i' = A_i(z)-z_i and A_i the area won by the largest value z_i^alpha / |y-x_i|^beta. This is a hard maximum partition. Literal Conjecture 32(a), subject to an unspecified general-position qualification, predicts convergence of one coordinate to 1 when alpha > 1 OR 0 < beta < 2 alpha. Part (b) makes stronger positive-limit/initial-condition-independence assertions only for 0 < alpha < 1 and beta > 2 alpha. The 2012 paper addresses the stochastic model and restricts its displayed parameter domain to alpha <= 1. It does not itself state this fixed-city conjecture. Its heuristics and remarks are not a proof of deterministic persistence.

## Independent mechanism reconstructed

Let m >= 2 distinct city positions lie in the open unit square and let z_i > 0, sum z_i = 1. Write p = alpha/beta > 0 and q = 2p. For city i choose c_i > 0 at most its distance to the square boundary and at most half its distance to every other city. Then the disk |y-x_i| < c_i z_i^p lies in the unit square, because z_i <= 1. For every competitor j, |y-x_j| >= |x_i-x_j|-|y-x_i| >= 2c_i-c_i z_i^p >= c_i. Thus z_j^p / |y-x_j| <= 1/c_i, whereas z_i^p / |y-x_i| > 1/c_i. The entire open disk is strictly won by i, simultaneously against every j. Consequently A_i(z) >= pi c_i^2 z_i^q.

For beta > 2 alpha, q < 1. With C_i = pi c_i^2, any eta_i > 0 satisfying eta_i <= z_i(0) and eta_i^(1-q) < C_i has positive inward derivative whenever z_i = eta_i. Thus z_i(t) >= eta_i for every t >= 0 along any global classical solution in the positive simplex. Alternatively, on 0 < z_i <= (C_i/2)^(1/(1-q)), z_i' >= z_i; first crossing below min(z_i(0),(C_i/2)^(1/(1-q))) is impossible. Simultaneous barriers need no assumption on the other lower bounds: only z_j <= 1. Since all m coordinates have positive lower bounds, z_i <= 1-sum_(j != i) eta_j < 1. This would disprove the unrestricted alpha > 1 clause at, for example, alpha=2, beta=8 without proving convergence.

## Foundational checks and exact remaining audit targets

- Partition ties must have zero planar area. For each pair of distinct sites and positive weights the tie equation is a nonzero quadratic polynomial in y, giving a line/circle/empty set. It cannot be identically zero for distinct sites. Finite unions have area zero; sum A_i=1, so simplex mass is preserved.
- Positivity cannot be assumed circularly: z_i' >= -z_i gives z_i(t) >= z_i(0) exp(-t) before any possible finite-time boundary contact. This handles finite-time positivity independently of the stronger persistence barrier.
- The argument is conditional on existence of a classical trajectory. Continuity of areas on the positive orthant follows by dominated convergence outside tie sets. Global continuation uses bounds away from the finite-time boundary. Any uniqueness claim needs its own regularity argument; persistence itself applies to every trajectory.
- Source cities can be on the closed-square boundary, but the exact claim requested here concerns distinct interior cities. An interior counterexample sufficient to disprove a universal/general-position collapse assertion avoids that boundary issue.
- At beta=2 alpha the lower area scales linearly and may have C_i<1, so this mechanism gives no positive inward barrier. For beta<2 alpha it also fails near zero. These cases must not be promoted by this argument.
- It is essential to compare with EVERY other city. A disk that avoids only the nearest city's cell or a soft allocation formula would not verify the source claim.
- A finite computation can stress the finite geometric inequalities and exact constants. It cannot itself prove time-asymptotic persistence. Need verify author's exact constants, rational certificate, invariant-bound proof and scope, without inheriting acceptance.
- General-position robustness must be explicit: the analytic estimate applies to every distinct interior configuration and every positive probability vector, including open sets of asymmetric rational examples. Special symmetry is unnecessary.

Strongest independently reconstructed result so far: conditional-on-solution uniform persistence for all distinct interior sites and beta>2 alpha, by a direct all-competitor disk inclusion and a scalar lower barrier. Exact remaining gap: complete source-author proof/constant/certificate audit plus falsification checks and a precise final verdict.
