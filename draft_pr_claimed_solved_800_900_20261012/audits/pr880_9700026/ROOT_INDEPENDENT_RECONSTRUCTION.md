# Root independent reconstruction before inherited proof

Timestamp: 2026-10-15T09:34:16.259290+00:00. Checkpoint: 5% toward complete evaluation/publication of PR #880. This memo was written after reading the actual primary 2007 model and before reading the frozen author proof, certificate, verifier, or inherited audit verdicts. Independent family status messages were visible; this is a checkable root derivation, not an assertion of blind independence from those messages.

## Claim and success criterion

The target is the literal deterministic finite-city assertion in 2007 Conjecture 32(a), as repeated in the exact catalog conjunction: if alpha>1 OR 0<beta<2alpha, one coordinate tends to one. A positive persistence theorem for alpha>1 and beta>2alpha refutes that clause. It must apply robustly to distinct interior city locations and positive normalized initial weights, rather than depend on a symmetric exceptional equilibrium. This does not resolve beta<2alpha collapse, beta=2alpha, convergence/uniqueness of equilibrium, initial-value independence, or the stochastic process with new cities.

## Actual model and independent route

The model is hard weighted Voronoi allocation, not a soft allocation: z_i'=area(S_i(z))-z_i on the unit square, S_i defined by maximizing z_i^alpha / |y-x_i|^beta. Positive powers show its cells depend only on gamma=alpha/beta. Thus (2,8) and (1/2,2) define the same cells. Contradictory predictions from two source clauses alone do not identify the false clause; an actual noncollapse proof is required.

Fix finitely many distinct interior locations, and choose h>0 so that each coordinate-centered square with half-width h fits in the domain and 2*sqrt(2)*h is strictly below every intercity distance. For a positive probability vector, the square of half-width h*z_i^gamma is in the domain, and a point in it has distance at most sqrt(2)*h*z_i^gamma from x_i. Its own powered score z_i^gamma/distance is at least 1/(sqrt(2)*h). Every competitor has z_j^gamma<=1 and distance at least separation-sqrt(2)*h>sqrt(2)*h, so its score is strictly smaller. The city point itself is a null exceptional point. Hence area(S_i)>=4*h^2*z_i^(2gamma).

With kappa=2*alpha/beta<1 and c=4*h^2, the scalar inequality z_i'>=c*z_i^kappa-z_i yields a positive barrier min(z_i(0),c^(1/(1-kappa))); a smaller strict barrier can simplify first crossing. A rigorous integrated comparison or first-crossing argument must be supplied. The upper bound 1-(m-1)*epsilon follows from all coordinate lower bounds. This excludes every coordinate tending to one, for all positive initial data and all distinct interior locations. Finite exact experiments cannot prove this all-time statement.

For existence, area allocations sum to one once ties have measure zero; z_i'>=-z_i gives z_i(t)>=z_i(0)*exp(-t), so a solution stays in a compact subset of the positive simplex on every finite time interval. Continuity of the area map and Peano existence plus continuation suffice for the negative claim for every forward classical solution. Local Lipschitz regularity and uniqueness, if asserted, need an independent proof rather than an assumed smooth dependence of cells. Apollonius bisectors are circles or lines; use a nonvanishing gradient uniformly on compact positive parameter boxes and a strip/coarea estimate. At equality of weights the line case must be included. No uniqueness assumption is needed to obtain the persistence inequality for each solution.

## Remaining checks before promotion

Authenticate the exact source mapping and unrestricted alpha>1 clause, general-position wording, rational witness and its claimed constants, null ties, continuity, existence/continuation and integrated barriers. Independently inspect the frozen proof/code and all supplied artifact trust boundaries. Then conduct a separate deep bounded priority audit. A local historical self-hash is not pre-execution authentication. No proof, priority, publication, or novelty acceptance is made at this checkpoint.
