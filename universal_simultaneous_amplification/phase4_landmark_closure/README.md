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

No specialist outreach will be prepared or initiated under the repository's
independent-research policy. If a theorem reaches publication, external review
will be listed as a human-only next action.
