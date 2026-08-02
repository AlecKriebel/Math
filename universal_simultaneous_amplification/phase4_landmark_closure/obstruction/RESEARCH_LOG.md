# Phase 4 obstruction-route research log

All timestamps are America/Los_Angeles.  This track uses no literature search
and no external contact.  Labels are `PROVED`, `RIGOROUSLY BOUNDED`,
`EXACTLY COMPUTED`, `NUMERICALLY OBSERVED`, `FAILED ROUTE`, and `OPEN`.

## 2026-08-01

- 20:05 -- Began the universal Bd--dB tradeoff attack.  The inherited
  fixed-graph strong-selection obstruction, support-degree condition, and
  fixed finite-type branching obstruction are treated as black boxes.  The
  target is a genuinely uniform fixed-fitness obstruction or a universal
  upper bound on the simultaneous interval.  Discovery completion estimate:
  **5%**.
- 20:42 -- [PROVED] Derived the exact singleton first-change tradeoff.  With
  `p_{ji}=w_ij/d_j`, `t_i=sum_j p_{ji}`, and
  `lambda_i(r)=sum_j r p_{ji}/(1+(r-1)p_{ji})`, a singleton at `i` reaches
  two mutants before extinction with probabilities `r/(r+t_i)` under Bd and
  `lambda_i/(1+lambda_i)` under dB.  Since `average_i t_i=1`, opposite
  curvature gives average Bd reach-two at least `r/(r+1)` and average dB
  reach-two at most `r/(r+1)`.  This is an exact state-space-independent
  tradeoff, but reach-two is not fixation.  Discovery completion estimate:
  **18%**.
- 21:00 -- [PROVED] Strengthened the inherited support-degree condition to a
  weight-sensitive necessary condition.  If a family dB-amplifies every
  fixed fitness eventually, then the average Simpson concentration
  `n^{-1} sum_{i,j} (w_ij/d_j)^2` tends to zero.  The proof uses the exact
  singleton extinction probability, Jensen's inequality, and then sends the
  fixed fitness to infinity only after the population limit.  Also obtained
  `t_i -> 1` in `L^1` for a uniformly sampled vertex.  This removes the
  weak-support-completion loophole at the level of local influence, but still
  permits weakly coupled growing regular modules.  Discovery completion
  estimate: **28%**.
- 21:18 -- [NUMERICALLY OBSERVED / OPEN] For multitype linear branching with
  death rate one and a column-stochastic birth kernel, random exact finite-band
  solves up to four types and level six consistently show that the uniformly
  averaged probability of hitting level `K` is at most
  `(1-1/r)/(1-r^{-K})`, with equality for a doubly stochastic kernel.  A proof
  would promote the singleton tradeoff to all establishment levels, but no
  valid concavity or martingale proof has yet been found.  Discovery
  completion estimate: **31%**.
- 21:44 -- [PROVED] Introduced mutant genealogical lineages between replacement
  events.  For dB, their total genealogy is dominated by a linear branching
  process with death one and birth matrix `r P^T`; for Bd it is dominated by
  birth `r P` and type-i death `t_i`.  Exact total-progeny PGF equations plus
  Jensen yield graph-universal finite bounds.  In particular
  `limsup rho_dB <= 1-1/r` for every graph sequence, and, once the all-r dB
  hypothesis forces `average |t-1| -> 0`, also
  `limsup rho_Bd <= 1-1/r`.  Hence any positive family has both fixation
  probabilities converging to the well-mixed infinite-size limit and can
  amplify only by a vanishing amount.  Discovery completion estimate:
  **46%**.
- 22:05 -- [PROVED] Derived a nonperturbative tradeoff between the two
  rare-mutant branching survival probabilities.  If `B` is Bd branching
  survival, `S` is dB branching survival, `a=1-1/r`,
  `g=(B-a)_+`, and `delta=a-S`, then
  `delta >= 4a g^2/(2r+sqrt(r)+1)^2`.  The proof uses exact fixed-point
  variance identities, L1 contraction of `P^T`, and a temperature-weighted
  Jensen inequality for Bd.  Discovery completion estimate: **57%**.
- 22:20 -- [PROVED] In an analytic undirected perturbation of a symmetric
  doubly stochastic kernel, computed the sharp second-order establishment
  signs.  The dB branching loss is at least `r` times any positive Bd
  branching gain.  The resolvent is `rI-P_0`, so this calculation is uniform
  in the mixing spectral gap.  Discovery completion estimate: **63%**.
- 22:34 -- [PROVED FAILED ROUTE] The local norms do not control singular
  modular cuts.  Two growing regular cliques with distinct internal degree
  scales and all-to-all cross weight `epsilon_m/m^2` have
  `average |t-1| -> 0` and `c(G)->0`, while the normalized cut ratio tends to
  the arbitrary internal-degree ratio.  Thus a universal closure must control
  a hierarchy of vanishing cuts or the post-establishment dynamics across
  them.  Discovery completion estimate revised to **55%** because the
  decisive global bridge remains open.
- 22:42 -- [EXACTLY COMPUTED] Added an independent standard-library verifier.
  It replayed 480 rational weighted-graph checks of the singleton formulas,
  opposite-curvature inequalities, and concentration deficit.  Wrote the
  claims-labelled obstruction report.  No fixed-r universal suppression
  inequality, Alternative O proof, or upper bound on `R_sim` was obtained.
  Obstruction-subtask completion estimate: **75%**; landmark-closure estimate:
  **35%**.
