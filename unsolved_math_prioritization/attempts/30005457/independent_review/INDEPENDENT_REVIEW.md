# Independent review: 30005457, lattice WARM five-turn partials

**Verdict: PASS_SCOPED_PARTIALS. The original stochastic existence and uniqueness questions remain unsolved, 5/5.** No mandatory mathematical correction was found. This audit does not certify historical novelty or stochastic percolation.

Reviewed 2026-10-01. Author `FROZEN_MANIFEST.json` SHA-256: `2be4995cf8928554fafe2dccd2a516621df56e638c29003f23e7b4cfdd47cf58`. `PARTIAL_RESULTS.md`: `75e395ed2bed4cc2380c1eb06c6ce80d5e087fd5baf06018df7ecc9757819ad5`. All seventeen manifest entries and both primary PDF hashes match. The frozen mathematical files were not altered.

The reviewer is separately studying the homogeneous critical line problem, but supplied no lemma or proof step to this alpha=2 lattice construction. Sharing the common OWR source was coordination only. The independent checks here were written separately, without importing either author checker. Both inspected author checkers were also replayed and their 4,300- and 132-assertion receipts matched byte-for-byte.

## Exact source and scope

The authoritative [OWR 12/2023](https://ems.press/content/serial-article-files/47008), printed p. 656, was read and independently rendered. Open Problem 3 asks for some finite d>=2, alpha>1 and bounded positive rates not bounded away from zero on the full nearest-neighbor lattice, producing an infinite surviving component with positive probability or almost surely; it separately asks uniqueness. The packet retains those clauses. It does not replace the lattice by a sparse subgraph or remove its unsupported edges from the stochastic model.

The cited [Hirsch–Holmes–Kleptsyn tree paper](https://arxiv.org/abs/2009.07682) initializes every tally at one. Its introduction distinguishes infinite reinforcement from positive lower linear reinforcement and proves its construction for the latter. The packet's deterministic support calculations do not establish either stochastic survival event and do not rely on an unproved transfer of the tree construction. The original workshop leaves initialization generic; using the explicitly stated standard unit initialization is disclosed rather than exploiting zero initial edges. The neighboring alpha=1 homogeneous-line target is different.

The very-strong-reinforcement absence result is credited background; its full proof is not an input to the new partial arguments. Limited searches do not certify that no later solution exists.

## 1. Tree-transfer obstruction

An injective bounded-length embedding of a branching tree would place exponentially many distinct depth-k vertices inside a polynomial-size lattice ball. The stated bound remains valid even when representing paths intersect, so the obstruction is correctly stronger than a planar drawing issue.

For a fixed nearest-neighbor lattice tree, a root path of graph length r is unique and its endpoint lies in the lattice ball of radius r. The union bound by (2r+1)^d rho^r therefore proves absence of an infinite independently thinned cluster, and countability permits all roots simultaneously. The dependent variant explicitly assumes the needed conditional upper bound along every path. No such bound is claimed for WARM. Thus this is a genuine obstruction to the proposed transfer mechanism, not a lattice nonpercolation theorem.

## 2. Explicit percolating deterministic equilibrium and relative stability

The q=1/16 rate field is positive at every vertex, bounded, and has infimum zero. The y=0 line and the off-line dimers cover every vertex with a supported edge; denominators in the full lattice drift are therefore nonzero. Unsupported edges remain part of the underlying lattice and have zero equilibrium weight, not zero initial stochastic count.

The local equilibrium identities were independently reconstructed. The central line edge receives q/(1+q) from the origin and the complementary amount from its other endpoint. The generic line-edge identity and reflected negative indices agree. Dimer weights are exactly sums of endpoint rates. Total rate and total supported weight both equal 514/225; square roots of the rates are summable by geometric summation.

The relative Jacobian calculations give diagonal correction 32/257 off the center, 17/257 on the two central edges, and zero on dimers. Its off-diagonal entries are nonpositive; the relative row absolute sum has the claimed correction. The l-infinity logarithmic norm is at most -193/257 at equilibrium.

On the relative 1/100 box, the probability-product and reciprocal-coordinate bounds give the uniform correction

    665986566400 / 2444044428243 < 1/3.

Hence the logarithmic norm is at most -2/3 throughout that box. Only finitely many scale-cancelled local formulas are involved, giving genuine uniform differentiability on the infinite supported-edge l-infinity space. The Dini-derivative contraction prevents exit and gives forward existence there. This proves stability on the invariant support face only. It supplies neither off-support stability nor a stochastic basin-entry event.

## 3. Unit-start topology obstruction

Finite total rate makes the superposed clock count finite almost surely on every bounded physical-time interval. Consequently only finitely many edges have acquired an increment then. The all-one baseline gives N_e(t)/t>=1/t, while the candidate line weights tend to zero; its full relative error is therefore unbounded. After subtracting the baseline, infinitely many target-supported edges still have zero increment and relative error one.

The proved relative attraction ball is never entered at finite time. The packet correctly does not infer impossibility of coordinatewise or l1 convergence from this fact. Every positive-rate clock still rings infinitely often over the infinite time horizon. A countable intersection of positive-probability startup events is not silently given positive probability.

## 4. Infinite-volume l1 stochastic-approximation bridge

This is the technically most important scoped claim. Its assumptions include bounded degree, no isolated vertices, positive rates and sum sqrt(p(v))<infinity. The proof is sound for the actual baseline-subtracted process.

**Noise.** The compensated count vector belongs to l1 at every finite time: both the finite total count and the total compensator mass Pt are finite. Coordinatewise Doob inequalities may be summed because sum_e sqrt(lambda_e)<=D sum_v sqrt(p(v)). This is not an unjustified Banach-space martingale inequality. The resulting C sqrt(T) maximal expectation gives summable dyadic probability bounds and therefore sublinear l1 noise uniformly between dyadic times. Pathwise integration by parts gives the stated vanishing weighted-noise integral on every fixed logarithmic-time window. No independence between edge martingales is needed.

**Compactness.** The total increment mass divided by time converges to P. Tail increments on edges outside a finite vertex neighborhood are bounded by outside-clock counts, whose summed rate tends to zero. The countable-exhaustion strong laws give the required asymptotic l1 tail control. Together with finite-coordinate bounds this proves asymptotic precompactness and all defining inequalities of K. Closedness plus the summable coordinate envelope lambda make K compact; all its constraints are preserved under convex combinations.

**ODE.** Every star in K has a positive local sum at least p(v), so its rational probabilities are defined. The map f preserves total mass, edge bounds and the local lower sums. The local column derivative bound is correct, and its factor p(v) cancels the possibly small lower bound p(v) on the star sum. Summing the two endpoint contributions gives a uniform l1 Lipschitz constant 8D on K. Integrating along convex segments is valid. Euler steps stay in K, and Lipschitz/Euler estimates yield existence and uniqueness of the global K-flow without an open-neighborhood extension or a uniform positive lower rate.

**Baseline.** The all-one vector is not in l1 on the infinite graph. The proof never norms it: it compares local probability vectors after adding 1/t coordinatewise and then uses the summable p(v) weights. Each fixed star eventually has a positive lower sum by its own clock. Finite-star convergence and a 2p(v) tail bound give the vanishing total drift error. The arbitrary convention at a zero star is used only outside the limiting domain and is not asserted to be continuous there.

**Limiting paths.** The integral equation, bounded l1 drift, vanishing noise windows and asymptotic compactness give uniform subsequential convergence of shifted paths on bounded logarithmic intervals. For finitely many vertices, positivity of the K-valued limit supplies uniform local denominator bounds; the remaining vertex contributions have a summable tail. Thus the passage to the infinite ODE is justified. Uniqueness then yields the stated asymptotic-following conclusion. This proves limiting-trajectory control, not selection of an equilibrium or survival pattern.

## 5. Lyapunov function and same-rate finite-component approximations

On K, the lower bound S_v>=p(v)^2/D and the uniform upper bound control the logarithms. Summability of sqrt(p) implies summability of p|log p|, so the Lyapunov series converges uniformly and defines a continuous real function. Its derivative can be passed through the series: the vertex terms have a summable p(v)(1+2D) bound, while the edge terms have a summable lambda envelope. The identity

    dL/dtau = sum_e x_e g_e(x)^2

is correct, including zero coordinates. Its dissipation is continuous on compact K and vanishes exactly at equilibria. The deterministic LaSalle conclusion follows. The author expressly does not turn this into an unsupported stochastic LaSalle/critical-value theorem.

The finite central-path residual is q^(M+1)/(1+q) on each endpoint edge, or 1/272 in relative coordinates. Removing endpoint competition decreases the Jacobian correction. The uniform -2/3 relative norm and the strict inward forcing inequality 1/272<1/150 produce an invariant compact box. The time-one contraction gives a unique fixed point there; uniqueness under every time-s map makes it an equilibrium.

For the absolute l1 estimate, constancy of the total finite-path reinforcement rate makes every drift-Jacobian column sum -1. Nonpositive off-diagonal entries then make its l1 column measure exactly -1+2D_e. The same relative-box estimate bounds this by -2/3. Comparing with the constant reference, including its residual forcing, yields the asserted 3q^(M+1)/(1+q) absolute error.

The tail dimers use the **same original rate field**, and every vertex retains a positive supported incident edge. Both discarded-line and replacement-dimer masses were independently summed. The resulting l1 distance tends to zero, while every approximating support component is finite. Therefore percolation is not an open property near this equilibrium in l1, and no l1 neighborhood can attract every deterministic trajectory to it. This does not determine the actual stochastic limiting support.

## Reproducible checks and disposition

The separate standard-library Fraction checker passed **11,782 exact assertions**. It independently reconstructs local lattice intensities, finite-path Jacobians, relative row and ordinary column logarithmic norms, the compact-domain Lipschitz bounds, rate and tail sums, and weighted-gradient identities. These finite controls supplement the infinite-volume proofs reviewed above. Both original exact receipts replay byte-for-byte; no stochastic simulation is treated as a survival certificate.

All scoped partial results pass. Keep the original positive-probability/a.s. lattice percolation question and uniqueness question **unsolved, 5/5**. Preserve the distinction between deterministic support, invariant-face attraction, l1 limiting trajectories and actual stochastic survival. Source PDFs and reading copies are excluded from the portable review package; no novelty claim is authorized by this review.
