# First independent scientific reconstruction

This checkpoint is made before consuming any external primary bodies, other audit verdicts, or surrounding task conclusions. Inputs are exactly the repaired candidate and source record listed in the accompanying ledger.

## Mechanism reconstructed from first principles

Take a uniform vertex U and fixed degree cutoff k. In a local configuration tree, an ordered nonbacktracking ray has successive total degrees with size-biased law D*. Because D >= 2, every discovered nonroot has at least one unused forward half-edge. Because the degree law is unbounded, p_k = P(D* >= k) is strictly positive for every finite k. Thus the chance that the first R nonroot vertices contain no seed is (1-p_k)^R. On the event of a seed at distance r <= R, the reversed route reaches U within the sum of R type-1 exponential traversal times; this has expectation R/lambda_1 and upper tail bounded by R/(lambda_1 T).

The actual type-2 occupied set through T is contained in the unopposed type-2 FPP ball. The needed protection is avoidance by every path vertex, not merely a comparison of endpoint arrival times. In fixed finite time that ball is locally finite: the size-biased forward offspring mean nu = E[D(D-1)]/E[D] is finite, and expected generation-r rings by T are bounded by d_0 nu^(r-1) (lambda_2 T)^r/r!. Their sum is finite. Revealing full incident half-edge counts also remains finite almost surely, since each of finitely many encountered degrees is finite; no third-moment bound is necessary for almost-sure finite cutoffs.

For each fixed k,R,T, independent uniform roots have disjoint exposed neighborhoods with probability tending to one. Cut off the random exposed half-edge total at M first, then use matching collision bounds of order M^2/n, then let M increase. This gives the substantive upper bound

limsup P(U is not weak-type by T) <= (1-p_k)^R + R/(lambda_1 T).

The bound can be made arbitrarily small for each fixed k. It proves a local saturation fact from an initially fixed positive (possibly extremely small) degree-selected density; by itself it does not prove vanishing density. To obtain that stronger regime, freeze a sequence of cutoffs k_j increasing to infinity, choose R_j and T_j to make the preceding error <= 2/j^2, and choose deterministic N_j beyond the convergence threshold for those frozen parameters. Also require log N_j >= j T_j and N_j P(D>=k_j) >= 4j^2. Then j(n) increases arbitrarily slowly and the schedule t_n = T_j(n) satisfies t_n/log n <= 1/j(n). Seed count diverges, seed vertex fraction vanishes, and seed stub fraction vanishes by integrability of D. The final weak-type fraction follows by E[unoccupied fraction] = P(uniform U unoccupied) and Markov, with no vertex-independence assumption.

## Actual adversarial conclusions at this checkpoint

The mechanism needs only local finiteness and nontermination of the ray. The minimum-degree assumption is essential to this particular proof; vertices in finite components with no seed would defeat saturation for degree laws having substantial mass below 2. Unbounded degree support is needed to let the selected minimum degree diverge, rather than for the macroscopic initial-population advantage itself. Finite second moment furnishes nonexplosion and the finite-time comparison; a theorem for infinite-mean size bias cannot be substituted without further justification.

An arbitrarily slow diagonal schedule can make any predetermined finite sequence T_j sublogarithmic relative to n. Thus the stated sublogarithmic time is an existence refinement, not a claimed explicit rate estimate. It does not contradict the logarithmic-time sweep of a single weak seed. It also does not settle finitely many strategically placed hubs.

The candidate survives these first-principles tests conditional on the exact local exploration claim. A likely priority vulnerability is that a pre-existing theorem for growing initial populations, if it accepts degree-selected half-edge totals or arbitrary initial locations, might already yield a weaker positive-fraction conclusion. A random-regular theorem alone cannot enforce diverging seed degrees. No external comparison has yet been made.

Progress estimate: 15% of the designated degree-selection/recent-disclosure priority audit, with the independent mechanism reconstruction completed and all theorem-level literature comparisons outstanding.
