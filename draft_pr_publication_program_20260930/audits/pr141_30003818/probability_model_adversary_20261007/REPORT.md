# Independent adversarial probability-model audit of PR141

Verdict: **PASS for the submitted Brownian probability mechanism and literal analytic-transform scope. No mandatory mathematical correction found.** This is an initial mathematical review, not a priority determination, publication-package audit, or acceptance of a future manuscript.

Reviewed original head: `523247e3246a5f44c7b0089074bb304c1f642bd0`. Original problem: 30003818 / OWR-16164-012. The original claim is `claimed_solved`, submitted 1/5. This review neither invents further central research turns nor changes the unmerged canonical status.

I independently read the original `JOINT_LAW.md` and its author diagnostic script; I did not read or use the submitted old review as authority. I inspected the primary report's printed page 1452 (PDF page 72, zero-based 71), including a fresh local rendering of the existing full report. The source is [Oberwolfach Report 23/2018](https://ems.press/content/serial-article-files/46745), DOI [10.4171/owr/2018/23](https://doi.org/10.4171/owr/2018/23). The problem asks for the law of the first-visit cell lengths with uniform random or equidistant seeds. It specifies independent Brownian motions and imposes no density, named distribution, asymptotic regime, or computational-efficiency requirement. Third-party full texts and the page rendering are outside the public artifact manifest.

## Exact claim and success criteria

For every positive finite integer k and fixed circle seeds p, let independent, equal-diffusivity Brownian motions continue indefinitely. Define T_i(x) as the physical time of the first hit of x by walker i; give x to the least-index minimizer, and integrate the ownership indicator to obtain L_i. The submitted formula gives the entire conditional joint Laplace transform for theta_i >= 0 in terms of specified scalar interval-exit density series, finite permutations, and ordinary finite-dimensional integrals. Integrating the conditional law over independent uniform p gives the random-seed law; equidistant p gives the other requested law.

Success here means that every finite-query joint owner probability is correctly evaluated without an unknown Brownian probability or integral-equation solution, the moment series is justified, and its transform uniquely specifies the joint probability measure. A compact density or efficient numerically certified implementation would be a stronger result, and is not established or required by the original source.

## Independent probabilistic reconstruction

First fix m distinct query points, none equal to a seed. For one Brownian motion, successively record the first hit of the yet-unvisited query set. Until that hit, the motion lies in the connected component of the circle with those remaining targets deleted. Lifting this component gives a bounded real interval. Hitting its left or right endpoint is exactly hitting the corresponding next query target. The interval endpoints are auxiliary absorbing boundaries only for that stage; old query points and other walkers' territory do not absorb the actual walker.

The first stopping time is a finite closed-set hitting time. Inductively, each next time is the first subsequent hit of a finite remaining set and is also a stopping time. Conditional on the past, the remaining set is one of finitely many deterministic sets. Strong Markov may therefore be applied on each such history. Bounded-interval exit is almost surely finite, and induction gives finite eventual visits to all m targets. At each restart the previously reached target has been removed, so the current position lies strictly outside the remaining set; the next elapsed time is strictly positive almost surely. Distinct spatial targets cannot be reached by the same continuous walker at the same time.

Thus a full first-visit permutation pi and its positive elapsed-time increments have the product density D_i^pi in the submission. The sum over all possible first-visit permutations has mass one. If a proposed next target is not an endpoint of the current unvisited component, its density is identically zero: impossible orders are excluded by geometry, not by a separate unproved probabilistic claim. The strong Markov product retains all dependence among one walker's different target hitting times.

For a singleton remaining set, the circle complement is one interval of circumference one, with both endpoints representing the same target. These are two different paths to that target. Both exit fluxes must be added. The submitted construction does exactly this. Discarding one endpoint would lose positive mass and invalidate the last stage of every nontrivial target-order construction.

A walker's time of hitting query j is the sum of all elapsed increments through its position in that walker's permutation. Independence across walkers now permits multiplication of their full-vector densities. The owner event is the intersection of the strict inequalities between these reconstructed physical times. Integrating that product over the displayed linear cones and summing permutations therefore yields Q_a. This is a direct event decomposition; there is no coalescing-walker, stopped-walker, independent-per-query-clock, or spatial Voronoi approximation hidden in it.

For every fixed nonseed query, each independent walker has an atomless hitting-time law (the singleton interval-exit law). Consequently the k hitting times tie with probability zero. There are finitely many queries in each coefficient, so all their comparisons are simultaneously strict almost surely. The hyperplane-boundary argument is also valid: the full elapsed-increment vector has a Lebesgue density, and an equality between two walkers' proper sums is a proper linear hyperplane.

## Measurability, ties over the whole circle, and random seeds

On continuous path space, the range up to a fixed time is compact. The distance from x to that range is the infimum of the continuous distance functions at rational times up to that time, together with the endpoint time. Hence the event that x has been reached by that time is jointly measurable in the path and x. Checking rational threshold times suffices to make the extended hitting time jointly measurable. The least-index rule therefore defines a measurable ownership field, and its spatial integrals are measurable random variables.

Pointwise almost-sure statements cannot automatically be intersected over uncountably many x. The submission correctly uses Fubini instead: fixed-x nonseed infinite-hit or tie probability is zero, so almost surely their exceptional spatial set has zero Lebesgue measure. The finite seed set also has zero measure. Changing the tie convention on that null set changes no L_i, and the lengths sum to one. This addresses the relevant uncountable-index issue without claiming ties never occur anywhere.

Conditioning on the seeds leaves independent Brownian motions with deterministic starting positions. Coincident seeds have zero probability in the independent uniform model; they do not produce a difficulty in its spatial integration. The fixed-seed mechanism would also work for coincident seeds away from their shared seed location, but such an extension is unnecessary for the requested models. Equidistant starts, including k=1, are covered. Ordering labels after sampling would give a different labeled random-seed law; the submission explicitly states its independent-uniform labeling convention and explains that a different seed distribution can be integrated against the same conditional formula.

## An independent positive Poisson-query construction

There is a second construction of the claimed transform which does not start from the alternating Taylor expansion. Let T=max_i theta_i > 0. Independently of the walkers, draw N from a Poisson distribution of mean T and, conditional on N=m, draw m independent uniform spatial query points and m independent marks U_j uniform on [0,1]. A query is forbidden if U_j <= theta_{I(x_j)}/T.

Conditional on the entire ownership field, the mean measure of forbidden marked queries is the known number Z=sum_i theta_i L_i. The Poisson void probability is exp(-Z). Therefore the unconditional probability that every query is allowed is exactly the joint Laplace transform of L.

Conditioning instead on N and the query locations, the probability that all are allowed is obtained from the already verified Q_a. Define

R_m(theta;p) = integral over circle^m of sum_a Q_a(x;p) product_j (1-theta_{a_j}/T) dx.

Then the same transform equals exp(-T) sum_{m>=0} T^m R_m/m!, with 0 <= R_m <= 1. This is a positive-term formula with uniform Poisson-tail truncation control. When T=0 the transform is one. All its coefficients are specified by the same fully deterministic finite-query integrals, and there is no unknown ownership distribution in them.

Conditional on a field, R_m is (1-Z/T)^m. Expanding the Poisson expression gives exp(-Z), and its Taylor coefficients are exactly (-1)^m E[Z^m]/m!. This independently confirms the submission's moment coefficients and alternating transform. The marked-query construction also shows directly why correlations across spatial ownership indicators must be retained: the queries are independent only conditional on the full field.

This alternative is an optional useful presentation or verification enhancement; its absence is not a defect in the submitted formula.

## Independent exact checks and falsification controls

`independent_global_race.py` imports no submitted checker and uses only the Python standard library. It builds two separate exact rational finite-cycle continuous-time random-walk models. These are diagnostics, not a proof of a Brownian limit.

The first model follows all walkers' positions and a global mask of which query sites have first been visited. The next global jump is chosen uniformly among the equal-rate walkers and their two directions. All walkers continue after visits. A query's owner is recorded only on its first global visit. Success or failure for a prescribed owner vector is evaluated by a reachable-state absorbing-chain linear system.

The second model independently filters each walker by a full prescribed individual target order. Every physical jump is still interleaved on the same global clock. On completion of global ownership observations, the unobserved individual suffixes are integrated by separately solved killed-chain harmonic probabilities; they are not arbitrarily discarded. Summing over all walkers' individual full orders is the finite-state analogue of the submission's complete-vector integrals over cumulative-time cones. This exposes normalization or premature-stopping errors that an individual-order-only test misses.

For four fixtures (cycles of four or five sites, two walkers and two queries, and three walkers with one query), all 15 joint owner probabilities agree exactly between the two systems and sum to one. For the symmetric four-site fixture with starts 0,2 and queries 1,3, the owner-vector probabilities are 3/16, 5/16, 5/16, 3/16. In particular, the two query-owner labels are not independent even though the walkers are independent.

Eight degrees 0 through 7 were independently checked for a deliberately correlated ownership field on pieces of unequal lengths 1/7,2/7,4/7 with a four-pattern probability mixture. Both the ordinary tensor moments and positive Poisson-query coefficients agree exactly with their direct field values; the positive and alternating series coefficients coincide exactly.

The cumulative-clock control uses feasible circle target orders with increments (3,4) and (5,1), in opposite visit orders. True physical hitting times are (3,7) and (6,5), with owner vector (0,1). Comparing only the last elapsed increments instead produces (1,0), reversing both owners. These strict inequalities persist on an open increment region. Both two-target orders are physically possible, so this is a substantive model distinction rather than an impossible input. The submitted formula reconstructs the correct cumulative times.

An impossible-order control shows that a walker starting at 0 on an eight-site cycle cannot first reach the middle of consecutive targets 1,2,3. The exact probability is zero. Independently sampled target clocks would assign positive probability to such an event and thus destroy the required dependence. The singleton control gives total hitting probability one, confirming that both possible endpoint directions are included.

Normal and optimized Python executions each passed all 61 explicit RuntimeError-guarded checks, so optimization does not erase these checks. Full rational probabilities, actual PIDs, UTC times, proof and script hashes, and scope qualifications are preserved in the two result receipts. One preliminary execution of this new reviewer script failed because its hardcoded expected value for the deliberately wrong reset-clock owner vector was mistyped as (1,1); it was corrected to the directly computed (1,0). This reviewer self-test correction does not concern any submitted formula. The preliminary failure is recorded in the research log; it is not relabeled a successful run.

## Sufficiency of the result and exact limitations

For theta >= 0, Z lies between zero and max theta. Tonelli gives E[Z^m] equal to the spatial finite-query tensor integral. Absolute domination by exp(max theta) justifies averaging the outer exponential series. Taylor's remainder for exp(-Z) is bounded by Z^(M+1)/(M+1)!, giving the submitted uniform factorial bound. No exchange of an inner heat-kernel series with its near-zero-time integral is needed: those scalar series define their positive-time summed density first.

The bounded simplex support guarantees transform uniqueness. Differentiation at zero yields every mixed moment; polynomials separate points and are dense on the compact simplex. Thus the explicitly determined transform identifies the full joint probability measure. Restricting the transform initially to nonnegative theta does not prevent determining the derivatives or coefficients, since the bounded-variable analytic extension is justified and the moment polynomials are determined on an open positive orthant.

The result therefore answers the literal original finite-k distribution question in an analytic-transform form. It does not give a named density, an efficient algorithm, quantitative Brownian quadrature accuracy, asymptotics, or independent historical novelty. The outer truncation bound alone must not be promoted to a numerical accuracy certificate for the inner scalar series or multivariate integrations. Continued independence, common diffusivity, independent uniform seed labeling, and the explicit circumference convention must remain visible in any manuscript and metadata.

No exact mathematical gap remains in this reviewed mechanism. Priority and the final publication package require separate reviews. The strongest verified mathematical statement is the full conditional transform and its uniform outer bound, with the two requested starting laws obtained as stated.
