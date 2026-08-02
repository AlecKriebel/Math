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
- 21:44 -- [RETRACTED; SEE 23:40] Introduced mutant genealogical lineages between replacement
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
- 22:05 -- [PROVED ONLY FOR SEPARATELY DEFINED ABSTRACT PROCESSES] Derived a nonperturbative tradeoff between the two
  rare-mutant branching survival probabilities.  If `B` is Bd branching
  survival, `S` is dB branching survival, `a=1-1/r`,
  `g=(B-a)_+`, and `delta=a-S`, then
  `delta >= 4a g^2/(2r+sqrt(r)+1)^2`.  The proof uses exact fixed-point
  variance identities, L1 contraction of `P^T`, and a temperature-weighted
  Jensen inequality for Bd.  Discovery completion estimate: **57%**.
- 22:20 -- [PROVED ONLY FOR SEPARATELY DEFINED ABSTRACT PROCESSES] In an analytic undirected perturbation of a symmetric
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
- 23:08 -- [RETRACTED AUDIT ATTEMPT] Rebuilt the report after a Markdown/LaTeX
  encoding failure.  A UTF-8 scan now finds no control or replacement
  characters and all displayed-math delimiters are balanced.  Expanded the
  genealogy argument into a breadth-first conditional-offspring coupling,
  explicitly stopped at $n$ lineages, so it does not make the false stronger
  claim that a post-fixation genealogy is dominated forever.  Also derived
  the exact complete dB baseline
  `(1-1/r)(1-1/n)/(1-r^(1-n))`.  The decisive missing term is now explicit:
  the baseline lies `a/n+O(r^-n)` below `a=1-1/r`, whereas the universal PGF
  method has an irreducible `O(log(n)/n)` error.  Obstruction-subtask
  completion estimate: **80%**; landmark-closure estimate: **38%**.
- 23:31 -- [PROVED / FAILED ROUTE] Derived the exact statewise hierarchical
  cut envelope.  If `A` and `B` are the two normalized boundary flows, then
  the Bd up/down bias is `r A/B`, the dB bias is at most `r^2 B/A`, and their
  product is at most `r^3`.  The bound is sharp on vanishing cuts; balancing
  `A/B=sqrt(r)` gives both rules bias `r^(3/2)`.  Therefore a per-cut product
  argument cannot produce even a crude fixed-fitness obstruction.  Audited a
  tempting stronger branching-survival coupling and rejected it: simultaneous
  mutant-to-mutant death/birth events destroy the independent active-lifetime
  coupling.  The later 23:40 audit shows that not even total genealogical
  progeny is dominated.
  Obstruction-subtask completion estimate: **83%**; landmark-closure estimate:
  **40%**.
- 23:40 -- [RETRACTED] The claimed total-genealogy domination is also invalid.
  It implies `limsup rho_dB<=1-1/r`, directly contradicting the separately
  proved center--singular-triangle family, whose dB fixation tends to `1/3`
  for every fixed `r` and hence exceeds `1-1/r` for `r<3/2`.  The precise
  failure is joint independence: a birth clock of one lineage is atomically
  coupled to the death clock of another lineage in a replacement event.
  Bounding each marginal birth intensity does not embed the joint family tree
  into a process with independent births and lifetimes.  Sections based on
  that coupling are retained only as a failed-route autopsy.  The singleton,
  concentration, abstract fixed-point, perturbative, and cut identities do
  not use this coupling and remain valid.  Obstruction completion estimate
  reset to **48%**; landmark-closure estimate **34%**.
- 23:43 -- [PROVED / EXACTLY COMPUTED] After retracting every genealogy-based
  fixation claim, derived a new threshold-sharp inequality that is genuinely
  about fixation.  For every positive weighted triangle `L` and `r>=3/2`,
  `H_L [alpha_dB(r)-(1-1/r)] <= I_dB(1/r)/r^2`.  The full six-state chain was
  derived symbolically from the dB rule.  After substituting `r=3/2+u`, the
  comparison numerator has 261 monomials and every coefficient is strictly
  positive; its denominator is coefficient-positive.  Along the singular
  triangle `(epsilon,1,epsilon)`, the normalized difference tends
  `(2r-3)/(3r)`, proving the threshold cannot be lowered.  Added the
  independent executable certificate `verify_triangle_db_threshold.py`.
  This is one exact half of the arbitrary-triangle satellite obstruction;
  the required joint Bd--dB product inequality remains **OPEN**.  Obstruction
  subtask completion estimate: **62%**; landmark-closure estimate **45%**.
- 23:46 -- [PROVED] Replaced the invalid lineage route by exact drift
  identities for the actual chains.  Under dB, weighted mutant degree
  `D(S)=sum_S d_i` has drift `(r-1) Psi_D(S)/n`; under Bd, inverse-degree mass
  `X(S)=sum_S 1/d_i` has drift
  `(r-1) Psi_B(S)/(n+(r-1)|S|)`.  Optional summation gives exact
  occupation-time formulas for both uniform-singleton fixation
  probabilities.  Extended the standard-library verifier to check both
  identities directly on all 39,360 rational nonabsorbing states.  These
  identities avoid all lineage independence assumptions.  The weighted
  triangle certificate is retained only as a diagnostic, per the mission's
  instruction not to extend finite triangle classification.  A universal
  comparison of the two actual-chain occupation measures remains **OPEN**.

## 2026-08-02

- 00:43 -- [PROVED] Replaced independent genealogy by exact additive
  set-valued duals which retain every coalescence.  Bd becomes a continuous
  branching--coalescing walk with neutral copying and selective OR arrows;
  dB becomes a geometric-OR burst, since
  `1-E(1-x)^K=rx/(1+(r-1)x)`.  Uniform-singleton fixation is exactly the
  stationary dual density.  More sharply, inverse-fitness fixation from
  vertex `i` equals the forward-fitness dB dual's stationary probability of
  the singleton set `{i}`.  Derived exact stationary size balances for both
  duals and verified the full intersection duality, stationary densities,
  reverse singleton identity, and balances over six rational weighted-graph
  cases.  This turns the proposed all-graph dB threshold inequality into a
  concrete density-versus-weighted-singleton-mass inequality, still OPEN.
  No independent-particle domination is used.  Obstruction completion
  estimate: **69%**; landmark-closure estimate: **49%**.
- 01:21 -- [PROVED / EXACTLY VERIFIED] Extended the set-dual certificate to
  check the reverse-fitness singleton identity separately for both Bd and dB,
  every singleton/doubleton stationarity equation, and the aggregate Bd
  level-one flux.  Expanding the dB size balance also gives the exact
  collision identity
  `E[C+(r-1)R2]=(1-1/r)E|A|`.  The proposed cross-rule product inequality
  remains OPEN, but it survived an exact rational screen of all connected
  labelled supports through four vertices under three weight patterns plus
  additional complete-support graphs: 145 tests at `r=3/2`, with strictly
  positive minimum slack.  This finite screen is explicitly not used as a
  proof.  The surviving proof gap is an all-level stationary inequality;
  level-one/two flux alone does not control higher dB burst jumps.
- 01:48 -- [PROVED OPERATOR IDENTITIES / OPEN CONJECTURE] Let `C` be the Bd
  set generator with every base arrow reversed.  Under reference mass
  `mu(A)=(r-1)^|A|`, proved the exact weighted-adjoint identity
  `L_Bd^dagger=C+r(Acut-Bcut)I`.  For each target, proved that the geometric
  dB burst is a positive resolvent of the corresponding local generator:
  `(I-(r-1)S/r)(G-I)=((N-I)+(r-1)(S-I))/r`.  Exact matrices verify both
  identities throughout the 148-case dual suite.  They isolate cut imbalance
  and interleaving as the remaining obstacles rather than discarding them.
  Also investigated the symmetric scaling
  `T(W)_ij=W_ij/(d_i d_j)`, for which `P(TW)=P^T/t` and
  `T^2(W)_ij=W_ij/(t_i t_j)`.  Both cross-rule sum inequalities pairing `W`
  with `T(W)` survived 828 exact comparisons on 138 rational graphs at
  `r=3/2,2,3`.  They remain OPEN and, even if true, do not alone exclude a
  simultaneous amplifier because `T` may send it to a suppressor; weak cuts
  obstruct the needed fixation-continuity step.
- 02:03 -- [NUMERICALLY REJECTED PROOF ARCHITECTURE] Tested a direct
  vector-supermartingale certificate for the original `r=3/2` fixation-sum
  conjecture.  With `h_B,h_D` the complete-graph count harmonics, seek one
  transfer potential `psi`, zero at both absorbers, such that
  `L_B(h_B+psi)<=0` and `L_D(h_D-psi)<=0`.  The correction cancels exactly at
  every singleton, so this would prove the sum bound.  Linear-program
  feasibility already fails on the three-vertex weighted path `(1,2)`, even
  though that graph has a strict sum deficit.  Cardinality corrections
  augmented by normalized degree and inverse-degree mass also fail on small
  paths.  Thus pointwise common-potential domination is too rigid; a valid
  proof must use an averaged stationary/occupation comparison or richer
  graph-weighted hierarchy.  No theorem is inferred from this numerical
  infeasibility test.
- 03:00 -- [PROVED REFORMULATION / EXACT DIAGNOSTIC] Size-biasing the dB
  dual stationary law by `|A|` gives the invariant law of the embedded chain
  observed at occupied-target events.  After the tilt
  `(r-1)^(-|A|)`, the proposed complementary-level inequality becomes the
  coefficient reflection `eta_k<=eta_(n-k)`, with no remaining fitness
  exponent.  Derived the exact conditional rank polynomial (76) for the
  complete-reference event mass and its `r=2` one-row subset-sum form (77).
  A new verifier checks 609 instances of the graph-independent
  combinatorial identity and exact stationary/one-step/factorial diagnostics
  on four rational graphs.  Iterates from the symmetric reference support a
  stronger binomial/factorial-transform cone, but pointwise complement
  order, Boolean stochastic domination, ultra-log-concavity, the coarse rank
  cone, the coarse factorial cone, and their intersection are each false as
  general invariant-cone claims.  Stationary rank reflection remains OPEN.
- 03:57 -- [NUMERICAL CERTIFICATE AUDIT / NEW INFORMATION REDUCTION] At
  `r=2`, the pointwise Poisson inequality targeting the exact complete-graph
  stationary mean fails for edge-supported quadratics already on four
  vertices and for unrestricted quadratics on small cycles.  In contrast,
  the weaker target `E|A|<=n/2` remains feasible with one common cardinality
  coefficient and support-edge pair coefficients on every connected
  unweighted graph through six vertices.  The exact degree-barrier package
  proves that an exact complete-target certificate needs degree at least
  `n-2` even on `K_n`; hence no bounded-degree exact-target hierarchy can
  close the problem.  A separate stationary random-target reformulation
  writes `mu_v=pi G_v`, `f_v=d mu_v/d pi`, and
  `I_2=(1/n)sum_v E_pi f_v^2`.  Since `f_v(B)=0` for `v in B`, Cauchy gives
  `I_2>=n/(n-E|A|)`.  Therefore the still-open sharp information inequality
  `I_2<=2` would prove the universal half-density bound.  These observations
  do not yet give a finite-baseline obstruction or an upper bound on
  `R_sim`.
- 07:31 -- [PROVED / EXACTLY VERIFIED] Classified every regular weighted
  four-vertex kernel at dB fitness two.  Opposite edges have equal weights,
  so the exact solution is `rho=4A/(4+5A)` with
  `A=sum_x 4x/(4+x)`; the complete gap is a positive rational-square sum and
  equality is unique at `K_4`.  A separate exact order-seven example proves
  that dB fixation is not globally concave on the positive regular-kernel
  polytope, closing the naive permutation-averaging proof.  The counterexample
  lies strictly below `K_7`, and broad order-nine screens still support but
  do not prove the regular maximizer or aggregate stationary-odds conjecture.
- 07:51 -- [PROVED REFORMULATIONS / EXACT FINITE CERTIFICATES] Rewrote the
  `r=2` component-odds target as the stationary comparison
  `E_{pi_i^0}h_i<=E_{eta_i}g` and split it exactly through a zero-count-biased
  post-clock law.  Directed and symmetric rational counterexamples close
  several stronger intermediate arguments, but neither side of the special
  undirected stationary sandwich has failed.  Separately, at `r=3/2` the
  fixation-product inequality is proved for every positive weighted triangle
  by a 24-atom square certificate.  The exact complete-dB harmonic produces
  an arbitrary-graph Bd--dB drift bridge with one unresolved signed row-cut
  term and two nonnegative dispersion losses.  Full-chain differentiation
  proves strict local log-product maximality of `K_n` on both edge modes for
  exact orders four through seven.  The all-order product inequality remains
  OPEN.
