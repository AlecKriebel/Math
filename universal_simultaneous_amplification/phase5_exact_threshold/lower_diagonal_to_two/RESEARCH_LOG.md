# Lower diagonal to fitness two: research log

## 2026-08-08 — branch opened

- Started from the proved separated response normal form and the exact
  `R_hyb` library; no fixed-order clone or doublet screen is being repeated.
- Isolated a new self-dual macro mechanism for growing strong-pair modules.
  If monomorphic pair `i` has inverse internal strength `a_i` and weak
  symmetric coupling `e_ij`, its leading Bd module-conversion rates use
  source activity `a_i`, while dB uses target activity `a_j`.
- The target-activity chain `(a,e)` is exactly the source-activity chain for
  `(1/a, a_i a_j e_ij)`.  An involution satisfying
  `a_phi(i)=1/a_i` and `e_phi(i),phi(j)=a_i a_j e_ij` therefore makes the two
  macro fixation probabilities identical under uniform singleton starts.
- A numerical search is testing whether this self-dual class contains a
  growing strong amplifier.  Any lead must still be lifted through exact
  pair-resolution, uniform entrance, separated-gate, and diagonal error
  bounds before it becomes a lower-bound theorem.

## 2026-08-08 — paired-star hierarchy exactly stopped

- The self-dual, rank-one, unconstrained small-rank, and two-center star
  macro searches all returned to the source/target tradeoff boundary.  These
  are numerical route triage only.
- An apparent dB hierarchy lead was replayed in the exact paired-star
  quotient.  With central-pair weight `A=L^3`, peripheral-pair weight
  `W=L^6`, and bridge weight one, peripheral dB singleton fixation tends to
  `(1/2)(1-r^-4)`, but peripheral Bd fixation tends to zero.  For example at
  `r=2` the exact-quotient floating values fall from `0.0403105` at `L=4`
  to `0.0015443` at `L=12`.
- The reason is now exact and topology independent.  After a singleton has
  resolved in its `K_2`, Bd macro conversion uses source activity and dB
  uses target activity.  Their first favorable/adverse odds are `r^2 x`
  and `r^2/x`.  Even granting fixation with probability one after the first
  gain gives a sharp scalar envelope.
- **PROVED CLASS OBSTRUCTION:** that envelope becomes nonpositive in the
  leaf-eliminated response at the unique algebraic crossing
  `R_pair=1.6986624639825652...` and remains so through fitness two.  The
  theorem permits arbitrary growing macrograph rank and later recovery
  paths.  It excludes every hierarchy that first separates into monomorphic
  strong pairs; it does not exclude a portal acting during the discordant
  pair state.
- Next executable task: build the smallest nonseparated pair--portal trace,
  retain portal events during the discordant-pair episode, and optimize its
  exact first-excursion response against the separated envelope.

## 2026-08-08 — exact star--reservoir diode and entrance obstruction

- A star between two clique reservoirs is an exact same-direction diode.
  With `L` leaves and reservoir order `C`, its two-interface odds products
  grow as `r^(C+2L)` for Bd and tend to `r^(C+4)` for dB, up to the displayed
  exact rational factors in `STAR_RESERVOIR_DIODE_AND_ENTRANCE_OBSTRUCTION.md`.
- The diode does not rescue a three-scale construction in which each clique
  and star locally absorbs before coupling.  The total dB singleton fixation
  mass of the star is only `O(1)`, while it contributes `L+1` uniformly
  sampled vertices, and `K_C` itself loses one finite-population unit.
- **PROVED CLASS OBSTRUCTION:** for every fixed `r>5/3`, every separated
  cycle with at least two `K_C` reservoirs and one `S_L` antenna per
  reservoir is eventually dB-suppressing, even after granting certain global
  fixation once the initially occupied component fixes.  The proof is the
  exact inequality `A_L<=A_1=-(2r-3)/r` and the complete-baseline correction
  `p/m`.
- The necessary escape is now sharper: star--reservoir events must act while
  the initial clique or antenna is polymorphic and create a positive entrance
  correction of order at least `1/C`.

## 2026-08-08 — dense complementary two-channel trigger obstruction

- Tested the proposed dense population of asymmetric two-root triggers before
  returning to dilute-core far-field calculations.
- **PROVED:** for a dB singleton at vertex `v`, with incoming temperature
  `T_v`, fixation is at most `r T_v/(1+r T_v)`.  Since `sum_v T_v=n`, a
  class of density `delta` contributes at most
  `delta*r/(r+delta)` to uniform dB fixation.  This remains true after
  granting fixation following the first mutant expansion.
- Consequently a positive-density dB-specific root class cannot have average
  singleton success tending to one.  The asymmetric local limit with
  `u_dB(B)->1` is necessarily dilute and cannot occupy half the population.
- **PROVED CLASS OBSTRUCTION:** if disjoint classes `A,B` carry all Bd and dB
  fixation respectively, while every wrong-channel and relay singleton mass
  is `o(1)`, then simultaneous amplification is impossible for
  `r>R_split=1.75487766624669...`, the unique real root of
  `r^3-2r^2+r-1`.  The literal equal two-root split already fails for every
  `r>(1+sqrt(5))/2`.
- All relay starts and far-field starts occur explicitly in the two remainder
  masses; no portal class is silently removed.  To approach fitness two, a
  positive-density class must now carry substantial fixation under both
  update rules, or a nonvanishing relay population must carry the missing
  uniform-start mass.

## 2026-08-08 — homogeneous nonvanishing pair relay exactly closed

- Tested the smallest nonvanishing relay population that itself has protected
  two-vertex collision states: a density-one population of homogeneous pairs
  over a complete inter-pair background.
- Reconstructed the exact two-state rare-colony equations for both rules.
  Singleton, doubleton, repair, shrinkage, and every external child are
  retained; this is not a collision-free branching approximation.
- **PROVED ALL-STRENGTH CLASS OBSTRUCTION:** for every fixed normalized pair
  strength `z>0`, Bd establishment is exactly `p`, while dB establishment is
  the unique positive root `T_D` of an explicit quadratic and satisfies
  `0<T_D<p`.  The certificate is
  `F(0)=-(r-1)(z+1)(rz+z+1)<0` and
  `F(p)=z^2(r-1)^2>0`, with opposite-sign roots.
- Full three-coordinate cells, fully crossed pair cells, and a four-coordinate
  two-pair cell were also screened with exact orbit aggregation at `r=1.9`.
  They collapsed to the complete/regular boundary or remained dB-suppressing.
  This is numerical triage only and is not used in the theorem.
- A positive construction must therefore put its nonvanishing protected
  relay population on a genuinely nonregular or hierarchical external
  network; homogeneous dense pair protection cannot supply strict gain under
  either rule.

## 2026-08-08 — arbitrary heterogeneous dense pair relay closed

- Extended the density-one pair calculation from one common strength to an
  arbitrary limiting distribution of normalized partner strengths.
- **PROVED ALL-STRENGTH CLASS OBSTRUCTION:** the uniformly averaged dB
  establishment probability is at most `p=(r-1)/r`, with equality only when
  the partner strength vanishes almost surely.
- The proof keeps the child-law bias exactly.  With `x=(1+z)^-1`, the local
  survival and child-weighted response are rational coordinates `s_A(x)` and
  `g_A(x)`, while self-consistency is `E g_A=A/r`.  The upper envelope of
  `s_A` over a fixed value of `g_A` is strictly concave.  Jensen plus the
  exact comparison point `x_0=A/(r-1)` gives `E s_A<=p`.
- This eliminates mixtures of weak and strong protected pairs over a complete
  external background.  The remaining positive-density trigger search must
  use a nonregular child network, a larger local state space, or intercell
  interaction before the rare-colony trace resolves.

## 2026-08-08 — growing-rank constructive cycle and exact endpoint target

- Stopped fixed-cell obstruction work and ran one bounded constructive cycle
  on growing-rank integrated modules, where core events remain active during
  every polymorphic local state.
- Complete-bipartite modules through part sizes 40 at `r=1.7,1.9,1.99`
  converged numerically to the portal-clone boundary.  A positive-density
  clique--antenna screen was also negative.  These are observations only,
  not class obstructions.
- **EXACT CONSTRUCTIVE REDUCTION:** at `r=2`, the full integrated response is
  the pair of vertexwise rational harmonic scores `mathcal B,mathcal D` in
  `ENDPOINT_INTEGRATED_MODULE_TARGET.md`.  Adding ordinary leaves can make
  both coordinates positive exactly when
  `mathcal D>0` and `mathcal S=mathcal B+mathcal D>0`.
- The next constructive target is therefore a rational growing-rank gadget
  with positive `mathcal D` and `mathcal S`, plus compact-uniform trace
  margins.  This packages every entrance and far-field term and is strictly
  weaker than asking the raw gadget to have both response coordinates
  positive.

## 2026-08-08 — exact Bd-catalyst ray criterion

- Sharpened the endpoint target using the exact zero-scale pair response
  `(-2,(2-r)/(r-1))`.
- **EXACT CONSTRUCTIVE REDUCTION:** a growing-rank catalyst sequence with
  normalized response converging compact-uniformly to `(b(r),0)`, where
  `inf b>0`, combines with the pair resource to give a single
  fitness-independent response diagonal for every fixed `r<2`.
- At fixed fitness the sharp cost condition is
  `(-D_catalyst/B_catalyst)<(2-r)/(2(r-1))`.  Hence the catalyst's dB-cost to
  Bd-gain ratio must tend to zero; a constant limiting ratio cannot reach
  two.
- Graded portal-clone paths, integrated stars through 300 leaves, singular
  `(1,k,k^2)` gateways, and an `o(n)` dense twin gateway were screened for
  this ray.  None showed a vanishing ratio.  This is numerical triage only,
  and no class obstruction is claimed.

## 2026-08-08 — diffuse rank-one catalyst ray rigorously obstructed

- Replaced the narrow gateway screens by an arbitrary multiscale rank-one
  clone blow-up: arbitrary rational class proportions and propensities,
  growing class number, and clone multiplicity sent out on the diagonal.
- Derived every Bd and dB rare-mutant type rate directly from the finite
  loopless graph.  Uniform singleton starts have exactly the class law used
  in the limit.
- **PROVED ALL-FITNESS IDENTITY:** for every `r>1`, the uniformly averaged
  limiting Bd survival probability is exactly `(r-1)/r`, independently of
  the propensity distribution.  The Bd self-consistency equation gives the
  cancellation in one line.  The averaged dB survival is at most `(r-1)/r`,
  strictly below it for every nonconstant profile by strict Jensen.
- At `r=2` the stronger typewise certificate `b_i+s_i<=1` also holds; it
  follows from `4MS<=1` via a decreasing Stieltjes transform.
- **PROVED FULL-FIXATION CLASS OBSTRUCTION:** fixation implies reaching a
  fixed cutoff `K`; the finite labelled chain below `K` converges to the
  exact branching trace.  Sending clone multiplicity, then `K`, to infinity
  compact-uniformly away from neutrality gives zero positive normalized Bd
  gain.  Consequently no trace-resolved rank-one clone diagonal has
  `B_k(r)/c_k -> b(r)>0`, regardless of its dB coordinate.
- Equality is the constant-propensity complete graph.  The remaining
  catalyst search must use genuinely non-rank-one incidence or correlations
  surviving below every growing cutoff.
