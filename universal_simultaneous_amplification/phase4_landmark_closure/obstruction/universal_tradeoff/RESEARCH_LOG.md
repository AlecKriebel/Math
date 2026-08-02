# Research log: universal `r=2` dB-dual mean ceiling

All timestamps use America/Los_Angeles.

## 2026-08-02

- 04:02 -- [NUMERICALLY OBSERVED] No violation of the candidate
  chi-square target-information bound `I2<=2` in extreme random weighted
  tests through seven vertices.  Complete graphs give equality.
- 04:11 -- [PROVED REDUCTION] Derived
  `I2 >= n E[1/(n-|A|)] >= n/(n-E|A|)` and the exact decomposition
  `I2=1+E|A|/n+(1/n)E sum e_v^2`.  Thus `I2<=2` would prove the universal
  half-density ceiling.  The contraction itself remains open.
- 04:19 -- [PROVED] Found an explicit graph-dependent linear Poisson
  certificate whenever
  `sum_i 1/(1+sum_v 2P_vi/(1+P_vi)) >= n/2`.  This proves the exact
  `r=2` half-density ceiling throughout that heterogeneous-temperature
  regime.  The complementary dense/near-regular regime remains open.
- 04:19 -- [PROVED FORMULA / NUMERICAL ROUTE] Derived the degree-three hole
  Mobius expansion of a general quadratic certificate.  Nonnegative pair
  coefficients in the potential force nonnegative cubic slack.  Broad LP
  screens support universal feasibility, but no all-graph formula or
  existence proof is claimed.
- 04:48 -- [PROVED / EXACTLY COMPUTED ARCHITECTURE OBSTRUCTION] Derived the
  exact generator of the natural weighted-pair observable
  `Q(A)=sum_(i,j in A) P_ij`.  On the four-vertex complete-support graph with
  one doubled edge, constructed a positive rational pseudo-law that
  annihilates every singleton drift and `DQ` but has
  `E(k^2/4-k/2)=100/7043>0`.  Therefore singleton stationarity plus the one
  `Q` balance cannot prove the proposed second-moment ceiling, even with an
  unrestricted coefficient on `DQ`.  The exact true stationary law on the
  same graph has margin `315/33422>0`, so the universal second-moment
  inequality itself remains OPEN.
- 05:35 -- [PROVED SHARP-CUT ROUTE FALSIFICATION] Constructed an explicit
  fitness-independent family of two growing dense cliques, with internal
  weighted degrees `3` and `4` and cross-edge weight `2^(-m^4)`.  It has
  complete support, `c(G_m)=O(1/m)`, and `t->1` uniformly.  At the fixed
  fitness `r=16/9`, the whole-clique cut has both Bd and dB forward biases
  tending to `64/27=r^(3/2)`, so their product tends to the sharp envelope
  `r^3`.  An exact rare-event reduction nevertheless gives fixation-sum gap
  `-a/(2m)+o(1/m)=-a/n+o(1/n)`, where `a=1-1/r`.  Hence the inherited local
  consequences plus the sharp cut-product inequality cannot imply an
  unscaled constant deficit.  Any universal obstruction must use the actual
  finite dB-amplification inequalities or resolve the `1/n` correction.
- 06:20 -- [PROVED TWO-MODULE `1/n` TRADEOFF] Derived exact weak-cut
  complete-comparison identities for two internally complete modules of
  arbitrary sizes and internal degree scales.  Each normalized fixation
  excess is a local finite-size budget minus two nonnegative macro-failure
  charges.  If both module sizes diverge, the dB budget is `-1+o(1)`, giving
  dB deficit `(1-1/r)/n+o(1/n)` independently of cut scale.  If the smaller
  module has fixed size `k`, actual dB amplification forces
  `r^(k-1)<=k` and `beta/alpha<=r(k-r^(k-1))/(k-1)+o(1)<1`; the same scale
  inequality forces an explicit Bd deficit `a_r*c_(k,r)/n+o(1/n)`.  For
  every fixed `r>3/2`, only `k=2,3,4` can occur, with the precise threshold
  subranges stated in the note.  Thus dB amplification implies Bd
  suppression throughout the separated two-complete-module model.
- 06:22 -- [PROVED MANY-MODULE / STAR ADDITIVE TRADEOFF] For any weighted
  macrograph of separated complete modules, derived the exact identity
  `n*Delta_U/a_r=E_U-L_U`, with additive local budget and nonnegative global
  macro-failure charge.  This gives dB deficit
  `a_r(q-1-o(q))/n` whenever every module size diverges.  For a star with one
  growing core and arbitrary `o(core)` heterogeneous satellites, proved the
  uniform scalar inequality `b_(k,r)(sigma)+d_(k,r)(sigma)<=-delta_r<0` for
  every `r>sqrt(2)`, module size, and scale; `sqrt(2)` is the sharp threshold
  for this coefficient-one scalar lemma.  Therefore actual dB amplification
  forces Bd deficit at least `a_r*delta_r*q/n+o(q/n)`.  The result is a class
  obstruction only and gives no new universal `R_sim` upper bound.  General
  macrographs remain blocked because their macro failure charges are global
  harmonic functions with no edge-additive decomposition.
