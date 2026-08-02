# Asymptotically universal simultaneous amplification

This directory is the dedicated workspace for the reversed-quantifier problem

```text
exists {G_n}, for every fixed r>1, exists N_0(r), for every n>=N_0(r):
both Bd and dB fixation strictly exceed their complete-graph baselines.
```

The fixed-graph obstruction in Paper I and the phase-three partial asymptotic
obstructions are inherited facts. They are not rederived here.

## Discovery tracks

- `obstruction/`: universal Bd--dB tradeoffs and fixed-fitness upper bounds;
- `construction/`: dense, mesoscopic, and multiscale candidate families;
- `threshold/`: exact searches and lower/upper bounds for `R_sim`.

Every result is labeled `PROVED`, `EXACTLY COMPUTED`, `RIGOROUSLY BOUNDED`,
`NUMERICALLY OBSERVED`, or `OPEN`. Finite-size experiments are discovery
evidence only. Broad literature search is embargoed until a complete result is
independently verified.

## Current proved threshold advance

The explicit center--singular-triangle family in
`construction/CENTER_TRIANGLE_PROOF.md` satisfies

```text
rho_Bd(G_N,r) -> 1/3,    rho_dB(G_N,r) -> 1/3
```

for every fixed `r>1`.  Consequently it simultaneously amplifies every fixed
`1<r<3/2` for all sufficiently large `N`, proving the new lower bound
`R_sim>=3/2`.  The proof has passed an independent hostile audit in
`threshold/CENTER_TRIANGLE_AUDIT.md`.  At `r=3/2` this particular family
suppresses both rules by rigorously computed order-`N^-2` margins, so its
exact interval is `(1,3/2)`.  Alternative U, Alternative O, and any universal
upper bound remain open.

## Current obstruction checkpoint

Both update rules now have exact branching--coalescing set duals, derived
directly from their Boolean graphical maps.  Uniform-singleton fixation is
the stationary dual density, and inverse-fitness singleton fixation is the
stationary singleton mass.  These identities retain every coalescence and do
not use the retracted independent-genealogy comparison.

The complete graph is not a universal dB maximizer below `2`: exact weighted
windmills beat it at `r=3/2`, `7/4`, and `9/5`.  The stronger cross-rule sum
inequality remains viable: it is proved exactly for every positive weighted
triangle at `r=3/2` and survived the recorded larger searches, but is still
open for arbitrary graphs.  The boundary `r=2` is under active attack.

The higher-threshold construction search also produced an exact no-window
identity for the natural singular four-vertex module and an exact rooted
portal favorable to both rules at `r=31/20`; neither yields a population
construction beyond `3/2`.

A separate exact burst analysis now excludes all separated one-portal
mesoscopic modules made from a growing diffuse family of protected two-state
blades in a broad compact regime.  For literal strong pairs the obstruction
already begins at `(1+sqrt(3))/2`; the homogeneous Bd and dB load windows are
disjoint for every `r>1`.  This is a class theorem, not a universal upper
bound: nonseparated and general multi-portal architectures remain open.

The corresponding symmetric two-portal trace has also been closed without
discarding the simultaneous-two-portal state.  Its Bd entrance gain is
exactly incompatible with dB entrance gain at every `r>1`, although the
post-establishment drift favors mutants under both rules.  The obstruction is
uniform on compact nonsingular parameter ranges and is independently audited
from all labelled atomic transitions.  Asymmetric portal networks and
singular coupling scales remain open.

The same obstruction now holds for every finite number of exchangeable
portals while retaining all portal-count states.  Its scalar comparison is
uniform in the portal count and consequently also excludes a diverging but
sublinear portal set throughout the separated strong-pair regime with
bounded normalized load.  The post-establishment drift is at least `r^3`
for both rules, so the class failure is localized exactly at entrance.
Positive-proportion or nonexchangeable portal architectures are not covered.

The current universal-obstruction attack factors the conjectured
`r=3/2` fixation product through a conservative reversed-arrow dual.  Exact
weighted-adjoint entropy, rank-capacity, and reversible-Poisson identities
are now available, but the necessary global inequalities remain open;
several stronger pointwise and rank-order shortcuts have exact
counterexamples.  At `r=2`, orbital symmetrization remains open for regular
kernels but cannot be extended by directed or conductance averaging to the
unrestricted graph class.

No specialist outreach will be prepared or initiated under the repository's
independent-research policy. If a theorem reaches publication, external review
will be listed as a human-only next action.
