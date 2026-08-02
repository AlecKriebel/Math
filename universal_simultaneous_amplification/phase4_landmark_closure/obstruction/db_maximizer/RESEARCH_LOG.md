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

## 2026-08-02 01:44 — exact `r=2` singular-family obstruction

- [NUMERICALLY OBSERVED] Expanded `r=2` searches found no dB counterexample.
  Larger clique blades, asymmetric two-vertex blade attachments, clique cores
  with pair satellites, and general undirected equitable block graphs all
  remained at or below the complete-graph baseline.  Representative deficits
  include `-0.04585` for four size-three clique blades and `-0.000197` for a
  size-20 clique core with three optimized pair satellites.  These values are
  discovery evidence only.
- [RETRACTED NUMERICAL ARTIFACT / EXACTLY COMPUTED] A size-60 clique core with
  three extremely isolated, internally fast pair satellites appeared to have
  excess `+4.75e-9` in double precision.  An exact 608-transient-state FLINT
  solve instead gives

      rho_dB(G,2)-rho_dB(K_66,2)
        = -3.763244026503474...e-10 < 0.

  A small floating-point residual is therefore not a sign certificate in
  this nearly decomposable regime.
- [PROVED FOR A BROAD FAMILY] Fix `c>=3`, `q>=1`, arbitrary `a_j,b_j>0`, and
  join a unit-weight `K_c` core to disjoint internally weighted pairs by edges
  of weight `epsilon*b_j`.  With `n=c+2q`,

      limsup_(epsilon -> 0) rho_dB(G_epsilon,2)
        <= (n-1)/(2n) < rho_dB(K_n,2).

  The proof uses exact complete-core establishment probabilities, a rare-event
  reduction, and the harmonic-mean scale tradeoff

      A*x/(2*T+x) + 1/(8*x+1) >= A/(2*T),

  where `T=2^(c-2)` and `A=(c-1)T/(2T-1)`.  After clearing denominators, the
  unrestricted quadratic minimum has numerator

      188*T^4 - 364*T^3 + 63*T^2 + 12*T - 4.

  Substitution `T=u+2` makes every coefficient positive.  The exact verifier
  checks this identity and the 608-state close case.
- [OPEN AT THAT CHECKPOINT] The pair theorem did not cover larger satellites,
  non-clique or multiscale cores, or parameters changing jointly with the
  weak-coupling limit.  The next checkpoint closes the fixed clique-satellite
  extension; universal dB maximization at `r=2` remains open.

## 2026-08-02 02:00 — extension from pairs to arbitrary clique satellites

- [PROVED FOR A BROADER FAMILY] The preceding theorem extends from
  two-vertex satellites to arbitrary fixed clique sizes `m_j>=2`, still with
  heterogeneous internal weights and attachment scales.  For a clique
  `K_m`, put `T_m=2^(m-2)`.  The favorable-to-adverse macro odds in the two
  directions have exact product

      16*T_c*T_m.

  After writing one directional odds as `z_j=16*T_c*T_m*y_j`, the mutant-core
  success probability is controlled by the weighted harmonic mean `y_H`.
  The required scalar inequality is

      A_c*y/(1+y) + A_m/(1+16*T_c*T_m*y) >= d_c-s_m,

  where `d_k=A_k/(2*T_k)` and `s_k=k/2-A_k=1/2-d_k`.
- [EXACTLY CERTIFIED] Monotonicity of `d_k` makes the right side nonpositive
  except for pair satellites and `(c,m)=(3,3),(4,3),(3,4)`.  The pair case is
  the coefficient-positive certificate above.  After positive denominator
  clearing, the remaining three numerators are

      64*y^2 - 7*y + 1,
      4480*y^2 - 65*y + 27,
      3456*y^2 - 65*y + 35,

  with discriminants `-207,-479615,-479615`.  The verifier reconstructs and
  checks all of these rational identities.
- [OPEN] Non-clique or nested satellites and jointly growing component sizes
  remain outside this exact obstruction.

## 2026-08-02 02:42 — arbitrary-module reduction and dual-level audit

- [PROVED CONDITIONAL REDUCTION] For an arbitrary fixed satellite module `H`,
  define `B=sum alpha_v`, `C=sum alpha_v/delta_v`, and
  `D=sum beta_v/delta_v`, where `alpha` is dB fixation at fitness two and
  `beta` at fitness one half.  The weak core--module theorem follows if every
  module satisfies

      B <= |H|/2,
      (2*B-|H|+1)*C <= B*D  when 2*B-|H|+1>0.

  The macro odds product is `16*T_c*C/D`.  Under the two invariants, the
  remaining continuous scalar inequality has no interior minimum in its
  module-slack parameter.  One endpoint is the already certified pair
  inequality; at the other endpoint the target lower bound is zero.  This
  proves the reduction, not the two invariants.
- [EXACTLY COMPUTED / OPEN] Both module inequalities pass exact FLINT solves
  on 250 connected rational small graphs, with the second inequality
  applicable on 64 of them.  They also survived every connected unweighted
  graph through seven vertices and tens of thousands of weighted numerical
  samples.  These computations are not a universal proof.
- [EXACTLY COMPUTED / CONJECTURE OPEN] The proposed stationary dB-dual level
  inequality

      k*pi_k <= (n-k)*(r-1)^(2*k-n)*pi_(n-k),  k>n/2,

  holds exactly for the certified 7-, 9-, and 11-vertex windmills both at
  their amplifier fitness and at `r=2`, and for the 66-vertex extreme
  clique-core false positive at `r=2`.  The closest non-full slack in the last
  case is about `1.0945e-27`, but is an exact positive rational.
- [EXACT TRANSFORM] If `F_s` is fixation averaged over all forward mutant sets
  of size `s`, Boolean duality gives

      1-F_(n-t) = sum_(k<=t) pi_k*C(n-k,t-k)/C(n,t).

  `verify_dual_level_windmills.py` uses this triangular identity to recover
  every `pi_k` from independently solved forward orbit chains.  At `r=2`, the
  conjectured paired inequality implies `E|A|<=n/2`, hence the first open
  module invariant, but does not yet yield the complete-graph fixation bound.
- [EXACTLY COMPUTED / STRONGER CONJECTURE OPEN] If

      C_k=sum_(|A|=k) Pi(A)*sum_(v in A) 1/d_v,

  then all six windmill cases also satisfy

      C_k <= (r-1)^(2*k-n)*C_(n-k),  k>n/2.

  Exact labelled Möbius inversion gives smallest non-full marked slacks from
  `5.03e-6` down to `4.51e-10`.  A numerical screen of 37,500 connected
  weighted graphs through eight vertices, at each of `r=3/2,2,3,5`, found no
  violation.  This marked form aligns with the inverse-degree quantities in
  the second open module invariant, but no implication has been proved.
- [EXACTLY COMPUTED / FURTHER MARKED VARIANTS OPEN] The same six windmill
  cases pass the degree-occupied conjecture, and both degree- and
  inverse-degree-hole conjectures.  If `a_v` is `d_v` or `1/d_v`, define

      O_k=sum_(|A|=k) Pi(A)*sum_(v in A) a_v,
      H_k=sum_(|A|=k) Pi(A)*sum_(v not in A) a_v.

  The exact tested inequalities are

      O_k <= (r-1)^(2*k-n)*O_(n-k),
      H_k <= ((n-k)/k)^2*(r-1)^(2*k-n)*H_(n-k).

  The squared hole prefactor makes the complete graph an equality.  All four
  marker variants also passed a numerical screen of 18,500 connected weighted
  graphs through seven vertices at each of `r=3/2,2,3,5`.  Degree marking may
  be more directly compatible with reversibility since `d_v*P_vu=w_vu`.
- [EXACTLY FALSIFIED ROUTE] The ratio of forward fixation probabilities at
  reciprocal fitness is not graph independent.  On the weighted triangle
  with edge weights `(1,2,3)`,

      rho_dB(G,2)   = 18764/43223,
      rho_dB(G,1/2) = 30154/129669,
      rho_dB(G,2)/rho_dB(G,1/2) = 28146/15077 != 2.

  The inverse-degree-weighted singleton-sum ratio is
  `428540/222057 != 2` as well.  Type complementation identifies the
  reverse-fitness singleton values with dual singleton masses, but supplies
  no graph-independent aggregate ratio.
- [EXACTLY FALSIFIED ROUTE] Binomial-normalized dual levels need not be
  unimodal.  On the six-vertex path `1-0-2-4-5-3` with consecutive weights
  `(30,4,64,1,1860)` at `r=2`, exact arithmetic gives

      pi_k/C(5,k)
        = (0.14253727..., 0.01391490..., 0.01433493...,
           0.000961348..., 0.000008561...).

  Hence the sequence decreases and then increases between levels two and
  three.  A likelihood-ratio/unimodality sharpening of the reflected-level
  conjecture is unavailable.

## 2026-08-02 03:31 — non-star weak module networks at `r=2`

- [EXACT REDUCED PROCESS] Consider several clique modules `K_(m_i)` with
  internal weights `a_i`, joined pairwise by complete bipartite edge bundles
  of weights `epsilon*b_ij`, with no distinguished core.  In the weak-coupling
  limit, a resident target module `j` flips mutant at rate

      2*m_j*alpha_j/[a_j*(m_j-1)]
        * sum_(i mutant) m_i*b_ij,

  while a mutant target flips resident at rate

      m_j*beta_j/[2*a_j*(m_j-1)]
        * sum_(i resident) m_i*b_ij.

  Thus the exact target-module directional odds are
  `4*alpha_j/beta_j=4*2^(m_j-2)`.  Uniform singleton initialization contributes local mass
  `m_j*alpha_j` before this macro chain starts.
- [NUMERICALLY OBSERVED] Global optimization of all module internal scales
  and symmetric cross-module weights found no `r=2` dB counterexample for
  complete or cyclic meta-supports with three through five modules and sizes

      (2,2,2), (2,2,2,2), (2,2,2,2,2),
      (2,2,3), (2,2,3,3), (2,2,2,3),
      (2,3,3,3), (3,3,3,3),
      (2,2,2,2,3), (2,2,2,3,3).

  The closest optimized deficit was about `-0.02694` for
  `(2,2,2,2,3)`.  This search is outside the proved star-shaped
  core--satellite family but remains numerical discovery only.
