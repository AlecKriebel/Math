# Five approaches to the continuum-limit optimality question

Research scope: row 1850, ID 30004632, OWR-4990379-002. These are authored mathematical notes. General problem remains unresolved; no queue or GitHub writes. Primary-source recovery is recorded separately in SOURCE_GATE.md. The independently checked restricted theorem and C^1 two-target extension are in RESEARCH.md.

## 1. Exact cell problem and a nontrivial computable reduction

The published 2023 Theorem 3 requires Assumptions 1–2, including almost-everywhere convergence of conditional Y measures. Its limiting cell problem minimizes integral grad_X c(x,y) dot z plus eta KL against sigma tensor pi_x, preserving both marginals. Momentum uses sign(z_l), NOT z_l. Confusing these changes the PDE.

For d=1, c(x,y)=(x-y)^2, uniform source discretized at midpoint x_i=(i-1/2)/n, Y={a,b}, a<b, and epsilon_n=eta/n, the normalized cell law has sigma=(delta_{-1/2}+delta_{1/2})/2. If q denotes the fraction assigned b, write the output occupancies as q-f(q), q+f(q). The entropy Euler equation gives

(q+f)(1-q+f) / [(q-f)(1-q-f)] = exp(2(b-a)/eta).

Consequently f(q)=[r-sqrt(r^2-4q(1-q))]/2, r=coth((b-a)/eta). This is symmetric, strictly concave for 0<eta<infinity, positive on (0,1), zero at 0 and 1, with |f'|<=1/r<1. At eta=0 the correct limit is min(q,1-q), while eta=infinity gives zero. Pair-map monotonicity follows because the derivatives of q±f(q) are nonnegative.

The target marginal enters the KL reference but cancels in this cross-ratio equation because it is fixed in the local solve. Source midpoint displacement is 1/(2n), not 1/n. The factor two in the exponent above is therefore intentional and checked.

## 2. Finite-eta stationary nonoptimal weak solutions and selection

Every deterministic conditional law pi_x=delta_{T(x)} admits only the product cell coupling with sigma. Balanced sigma gives zero sign-momentum. Thus every Monge coupling is stationary for the formal limiting system, including nonoptimal maps. This is already Remark 8 of the published paper, not a new obstruction and not proof that the actual algorithm-selected limit is stationary.

Concrete example: X=Y=[0,1], uniform marginals, T(x)=1-x, squared cost. The formal stationary cost is integral_0^1 (2x-1)^2 dx=1/3, whereas identity has cost zero. This works at every finite eta at the PDE level. Scalar two-target flux likewise has f(0)=f(1)=0, so arbitrary binary stationary profiles satisfy the distributional equation. Entropy/viscosity admissibility, NOT mere weak PDE solvability, must distinguish globally sorted from inverted profiles.

The 2023 paper additionally constructs genuine algorithm-selected stationary nonoptimal limits in d=2 at epsilon_n=0 using an indefinite quadratic potential invisible on the grid's local directions. Its semi-discrete example presents freezing from vanishing interface transport capacity. Neither is repaired merely by connectivity or smooth quadratic cost.

## 3. Rigorous one-dimensional sufficient conditions

At epsilon_n=0 exactly, adjacent pair updates are (u,v)->(max(0,u+v-1),min(1,u+v)). Prefix masses obey alternating max-plus updates. A self-contained light-cone proof gives a uniform O(n) sorting bound, hence exact optimality after finite rescaled time. This is a benchmark, not a novelty claim: Bonafini–Schmitzer's 2021 Section 5 already relates the method to odd-even sorting and explicitly states O(n) adaptation to continuous one-dimensional strictly-Monge problems.

For positive finite eta and TWO target atoms, the exact primitive scheme is a monotone staggered Hamilton–Jacobi scheme, with the flux in Approach 1. The theorem in RESEARCH.md derives unique weak-plan continuum convergence and finite-time sorting using a three-plane viscosity supersolution. It passed independent audit in POSITIVE_ETA_AUDIT.md, including the varying-entropy-scale corollary. The scope remains two targets in one dimension; no general resolution or novelty priority is asserted.

This route is genuinely about n->infinity before long time. It is not fixed-n entropy convergence. It uses the ORIGINAL alternating local-solve algorithm, not nonlocal flow updates.

## 4. Energy, dual certificates, and failed coercivity

In the two-target model, for a sufficiently regular scalar trajectory q_t+f(q)_x=0 with zero boundary flux, the unregularized transport cost has derivative -2(b-a) integral_0^1 f(q) dx. Indeed the x-dependent cost difference is (x-b)^2-(x-a)^2, whose derivative is -2(b-a). Dissipation vanishes at every binary q, including unsorted ones. Therefore no global energy-gap bound E-E_opt <= C integral f(q) can hold over all feasible couplings. Choosing q=1 on [0,m], zero elsewhere gives strict positive cost gap but zero dissipation. Any coercivity proof must use entropy selection, regularity that excludes such profiles, or a time-integrated/geometric argument.

For general quadratic cost, concentration on a map only yields global optimality if the map satisfies cyclic monotonicity (equivalently, under the usual hypotheses, is a convex gradient). Symmetry of a differential alone is insufficient; positive-semidefinite Jacobian and global potential/convex-domain hypotheses matter. A dual pair phi(x)+psi(y)<=c(x,y), with equality on the limiting support, certifies optimality but does not explain why the algorithm reaches that support. Imposing the desired certificate as an assumption merely restates the conclusion and does not resolve this target.

## 5. Order of limits and conditional convergence

For every fixed positive epsilon, n epsilon -> infinity. The published continuum theorem then freezes at initialization, while every fixed-n entropic iteration may converge globally as k->infinity. These two limits need not commute. Finite-scale rates with constants degenerating in n or epsilon cannot justify the reverse order.

A valid quantitative sufficient condition would be a scale-uniform estimate gap_n(k) <= R(k/n)+o_n(1), with R(t)->0, plus the relevant compactness/initialization conditions. Such an estimate passes to continuum trajectories and then to long-time optimality; fixed-scale convergence without that estimate does not. The one-dimensional primitive approach aims to supply such a conclusion directly at continuum level. General d>=2 finite-eta uniform coercivity, uniqueness/selection, and convergence remain open in this research.

## Sources

- Bonafini–Medina–Schmitzer (2023), Asymptotic analysis of domain decomposition for optimal transport, DOI https://doi.org/10.1007/s00211-023-01347-x . Main theorem is Theorem 3, not v1 Theorem 5.22. See Sections 1.2, 4.5, 5, 6 and Remark 8.
- Bonafini–Schmitzer (2021), Domain decomposition for entropy regularized optimal transport, https://arxiv.org/abs/2001.10986 ; published DOI https://doi.org/10.1007/s00211-021-01245-0 . Section 5 is the sorting benchmark.
- Schmitzer OWR contribution, https://ems.press/doi/pdf/10.4171/OWR/2021/10 , pp.515–517.
- Medina–Schmitzer (2025), https://arxiv.org/abs/2405.09400 . Hybrid nonlocal-flow updates change the algorithm and do not resolve the original target.

No numerical evidence is used as proof in these approaches.
