# Research log: dB maximization at and above `r=3/2`

## 2026-08-01 23:00 — initialization

- Question: is the complete graph a universal maximizer of uniformly
  initialized death--birth fixation probability on every finite connected
  undirected weighted graph whenever `r>=3/2`?
- Discovery plan: unrestricted small-graph optimization for `n=3,...,7`,
  exact conversion of any apparent counterexample, then derivation of
  statewise/potential inequalities suggested by extremizers.
- No literature search will be used.
- Completion estimate: **3%**.

## 2026-08-01 23:18 — cancellation audit

- [RETRACTED NUMERICAL ARTIFACT] An apparent five-vertex dB excess was caused
  by subtracting nearly equal mutant and total neighbor masses.  Rebuilt the
  transition generator so mutant and resident masses are accumulated
  separately.  The candidate vanished under the corrected chain.
- Added range and residual checks to all floating-point searches.  A small
  linear residual is still not accepted as validation when a nearly
  disconnected chain is ill-conditioned.

## 2026-08-01 23:32 — exact dB counterexample at the proposed threshold

- [PROVED] The complete graph is **not** a universal dB maximizer at
  `r=3/2`.  An explicit seven-vertex graph has center `0`, blade pairs
  `(1,2),(3,4),(5,6)`, center-edge weights `(100,10,1)` on the three blades,
  and internal blade weights `(600,1200,1800)`.
- Exact rational solution of both the 126-state labelled chain and an
  independently derived 52-state orbit-lumped chain gives

      rho_dB(G,3/2) = 0.3175490238143979...
      rho_dB(K_7,3/2) = 1458/4655 = 0.3132116004296455...
      exact excess    = 0.004337423384752398... > 0.

  The verifier checks every labelled-to-lumped transition before either
  absorbing solve.  Thus the original `r>=3/2` maximizer conjecture is
  decisively false.
- [NUMERICALLY OBSERVED / OPEN] Corrected complete-support searches through
  `n=7` and connected atlas searches through `n=6` found no dB excess at
  `r=2`.  This does not prove that `K_n` is a universal dB maximizer for
  `r>=2`.

## 2026-08-02 00:05 — cross-rule sum reconnaissance

- Switched to the candidate obstruction

      rho_Bd(G,r)+rho_dB(G,r)
      <= rho_Bd(K_n,r)+rho_dB(K_n,r).

- [NUMERICALLY OBSERVED] Complete-support optimization for `n=3,...,7` at
  `r=3/2,2,3`, 30,000 cancellation-safe random complete/sparse trials for
  `n=6,7,8`, and separated arbitrary weighted gadgets through seven vertices
  found no positive excess.  The exact dB counterexample above has total-sum
  deficit `-0.0840241240120...` at `r=3/2` because its Bd loss is much larger
  than its dB gain.
- [NUMERICALLY OBSERVED] Exact two-count lumping for dense two-equitable-class
  graphs, followed by global optimization of both internal weights, found
  only the complete graph through `n=50` at `r=3/2`.  This search includes
  complete-bipartite limits but is not an asymptotic proof.
- [PROVED LOCAL IDENTITY] For temperature `t_i` and
  `lambda_i=sum_j rP_ji/(1+(r-1)P_ji)`, the singleton reach-two sum obeys

      r/(r+t_i) + lambda_i/(1+lambda_i)
      <= 2r/(r+1)
         - r(r-1)(t_i-1)^2/
           ((r+1)(r+t_i)(1+r t_i)).

  This exact pointwise tradeoff concerns reaching two mutants, not fixation.

## 2026-08-02 00:31 — exact triangle sum certificate and failed symmetrization

- [PROVED DIAGNOSTIC] For every positive weighted triangle at `r=3/2`,

      rho_Bd(G,3/2)+rho_dB(G,3/2)
      <= rho_Bd(K_3,3/2)+rho_dB(K_3,3/2),

  with equality only for equal edge weights.  Direct construction of both
  six-state chains gives a gap denominator with 127 positive coefficients.
  Its numerator is twice a sum of 24 positive rational atoms

      q_ijk sum_perm x^i y^j z^k (x-y)^2.

  The executable verifier reconstructs the chains and checks the polynomial
  identity exactly.  This is deliberately recorded only as finite-state
  evidence, not as a universal obstruction.
- [PROVED FAILED ROUTE] Pairwise permutation averaging is not monotone for the
  fixation sum.  At `r=3/2`, the weighted path with consecutive weights
  `(5,1)` has sum `5864/7371`.  Averaging its weight matrix with the copy that
  swaps the first two vertices gives the triangle `(5,1/2,1/2)`, whose sum is
  `106603567/135117445`.  The exact decrease is
  `6553805123/995950687095>0`.  Repeated vertex symmetrization therefore
  cannot be justified by a one-step monotonicity claim.
- [OPEN] Neither the universal cross-rule sum inequality nor a universal dB
  maximizer theorem at `r>=2` has been proved.  Subtask completion estimate:
  **72%**; the exact counterexample and finite diagnostic are closed, while
  the large-population obstruction remains open.

## 2026-08-02 00:47 — the dB counterexample extends exactly to `r=7/4`

- [PROVED] A nine-vertex four-blade windmill dB-amplifies at `r=7/4`.
  Ordered by blade, its center attachments and internal edges are

      outer    = (1, 40, 2400, 200000),
      internal = (9000000, 3800000, 2000000, 920000).

  Exact orbit-chain solution gives

      rho_dB(G,7/4)   = 0.387510078397605232...
      rho_dB(K_9,7/4) = 6588344/17097795
      exact excess    = 0.00217711587232053902... > 0.

  The exact verifier checks that all 512 labelled transition rows aggregate
  to the declared blade-count chain, then solves its 160 transient equations
  over the rationals.  The excess numerator and denominator have 1433 and
  1436 decimal digits respectively.
- [NUMERICALLY OBSERVED] A five-blade windmill optimized at `r=2` remained
  below `K_11` by about `0.02287`.  The same candidate is dB-amplifying at
  `r=1.8` and suppressing by `r=1.85`, suggesting—but not proving—that the
  windmill thresholds rise toward a limiting value below or equal to `2`.
  The conjecture that `K_n` maximizes dB for `r>=2` remains **OPEN**.
- The four- and five-blade dB gains come with much larger Bd losses; at
  `r=3/2` their cross-rule sum deficits are approximately `-0.09714` and
  `-0.10190`.  They do not threaten the proposed sum obstruction.

## 2026-08-02 01:02 — exact extension to `r=9/5`

- [PROVED] An eleven-vertex five-blade windmill dB-amplifies at `r=9/5`.
  Its exact integer weights are

      outer    = (1, 6, 120, 3500, 60000),
      internal = (9000000, 2500000, 880000, 410000, 190000).

  Exact arithmetic gives

      rho_dB(G,9/5)    = 0.410344367875481897...
      rho_dB(K_11,9/5) = 1937102445/4780900817
      exact excess     = 0.00516916781443449956... > 0.

  The FLINT verifier checks all 2048 labelled rows against the 486 orbit
  states and solves the 484 transient equations over the rationals.  The
  exact excess has rational height 16,305 bits.  This pushes the failure of
  complete-graph dB maximization from `7/4` to `9/5`; `r>=2` remains open.
- The `r=9/5` graph is still strongly Bd-suppressing, so this does not refute
  the cross-rule sum conjecture.
- [EXACTLY VERIFIED] The final checkpoint suite reran all three windmill
  certificates, the triangle sum certificate, the exact symmetrization
  counterexample, bytecode compilation, and whitespace checks successfully.
  There is no long-running search attached to this checkpoint.  Folder is
  stable for commit.  Subtask completion estimate: **78%**; the remaining
  22% is precisely the open `r=2` dB maximizer / universal sum obstruction.
