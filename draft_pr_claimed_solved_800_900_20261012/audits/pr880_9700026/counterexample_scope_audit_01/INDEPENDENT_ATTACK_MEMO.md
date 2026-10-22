# Independent scaling and counterexample attack memo

Checkpoint: 2026-10-15T09:29:53Z. Completion estimate: 30% of this audit.

This memo was written after reading the local primary 2007 notes (global model conventions and the whole printed page 40, including Conjecture 32) and the complete 11-page 2012 paper text, with visual checks of the original 2007 printed page 40 and the 2012 model page 2. No author PROOF.md, certificate, verifier, or inherited review/verdict has yet been opened. The assignment disclosed the proposed parameter choice and claimed bounds, but the argument below is independently derived.

## Primary target and distinction of models

The literal 2007 associated ODE has fixed city positions in the unit square, simplex state, and derivative `area(S_i(z)) - z_i`. Allocation is by the maximum of `z_i^alpha / distance^beta`. The initial populations are positive and locations and initial state are described, without formal definition, as in general position. Clause (a) includes the disjunction `alpha > 1 OR 0 < beta < 2 alpha`; clause (b) includes `0 < alpha < 1 AND beta > 2 alpha` and claims convergence to a positive initial-state-independent limit. The global 2007 convention allows all positive alpha and beta. The 2012 paper restricts its stochastic model to alpha <= 1 and does not state the 2007 fixed-city conjecture. Its remarks about alpha > 1 in the stochastic setting do not prove anything about this ODE.

## Scaling attack, and its precise limitation

For positive z and distances, taking the positive 1/beta power converts influence ranking into ranking `z_i^(alpha/beta) / distance`. The cells, their areas, and the ODE therefore depend on q=alpha/beta only. Simultaneously multiplying (alpha,beta) by any positive number preserves the entire vector field and the clock. For example (1/2,2) and (2,8) both have q=1/4. These parameter pairs fall respectively under clauses (b) and (a). Thus the two clauses as a conjunction cannot both be correct for a nontrivial same geometry/initial state: a positive limit for all coordinates conflicts with one coordinate tending to one when there are at least two cities.

This algebraic incompatibility alone does NOT identify which clause is false. It would be circular to infer failure of the collapse clause from the unproved convergence clause. An actual collapse counterexample requires an independent positive lower bound for every coordinate for all time (or another independent obstruction).

## Independent geometry supplies an actual obstruction

Take a finite number m>=2 of pairwise distinct strictly interior cities, a positive simplex state, and q=alpha/beta. Let d>0 be the minimum separation and rho>0 be the minimum Euclidean distance of any city to the square boundary. Put c=min(rho,d/2). Because every simplex coordinate is at most one, the disk centered at x_i of radius r_i=c z_i^q lies in the square. For a point in this disk, every competitor is at distance at least d-r_i >= d/2, and its reduced influence is at most 2/d. City i's reduced influence is at least 1/c >= 2/d. Consequently the entire disk is contained in S_i up to boundary, giving

`area(S_i(z)) >= a z_i^p`, with `a=pi c^2>0` and `p=2q`.

When beta>2 alpha, p<1. On every positive ODE solution,

`z_i' >= a z_i^p - z_i`.

Writing u_i=z_i^(1-p) gives `u_i' >= (1-p)(a-u_i)`, hence

`z_i(t) >= [a + (z_i(0)^(1-p)-a) exp(-(1-p)t)]^(1/(1-p))`

and therefore `z_i(t) >= min(z_i(0),a^(1/(1-p))) > 0` for all finite/nonnegative times. The global sum-one identity yields a matching strict upper bound `z_i(t) <= 1 - sum_{j!=i} delta_j < 1`. This does not assert convergence or uniqueness of an equilibrium. It independently falsifies the alpha>1 part of the literal clause (a) whenever beta>2 alpha, provided global solutions exist. Interior continuity/local Lipschitz and continuation must still be checked carefully in the author proof.

This mechanism works on the entire admissible open set of distinct interior configurations and positive simplex initial states. Thus the undefined general-position qualification cannot be defeated merely by deleting symmetric equilibria, exceptional collinear points, or a measure-zero set. The later certificate audit must still independently check its advertised asymmetric rational instance and an explicit perturbation neighborhood.

## Adversarial checks queued before promotion

1. Verify the actual cells are hard maximum cells, not normalized soft influence probabilities. The latter have different integrability and growth laws.
2. Verify tie loci have zero area for distinct sites and positive coordinates. Ensure the simplex and positivity arguments are not circular.
3. Verify all-time bounds by scalar comparison and continuation, not integration at finitely many times.
4. Verify certificate coordinates are distinct, strictly interior, noncollinear, asymmetric, and normalized, with exact rational inequalities and strict perturbation slack.
5. A single city has z=1 and is irrelevant as a counterexample. Colliding cities destroy d>0. Zero-weight initial coordinates fall outside the hypothesis and may remain zero. Boundary sites require a truncated-ball variant and are unnecessary. One-dimensional or collinear examples alone would not resolve the stated generic planar qualification.
6. At beta=2 alpha the scalar exponent is one and this positive lower bound mechanism fails. At beta<2 alpha it is greater than one and cannot prove persistence. No conclusion in either regime is justified by this argument.
7. Falsity of one clause suffices for a negative answer to the catalog conjunction, if the catalog really imports that literal conjunction without restricting alpha. It does not solve the restricted positive-convergence/initial-independence problem, the beta<2 alpha collapse problem, or the growing-city stochastic model.
