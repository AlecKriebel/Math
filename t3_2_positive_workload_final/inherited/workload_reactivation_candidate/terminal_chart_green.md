# Terminal-chart localization for reaction-count Green occupations

Assume the embedded labelled chain has infinite expected positive return
count. The certified killed Green construction supplies probability
occupations `nu_M` on physical labelled transitions. They escape every fixed
finite set and satisfy exact bounded-test telescoping and endpoint balance.

## Compact descriptor

Push each transition source and endpoint to the descriptor consisting of:

- each population coordinate in `N_0 union {infinity}`;
- capped availability `min(x_i,2)`;
- the actual current target and labelled channel;
- enabled-source support;
- the complete recursively normalized source-propensity flag;
- a compact positive ratio vector in every tied layer;
- workload chamber or wall;
- lattice residue and structural rank.

The iterated source simplex is compact because there are finitely many
sources: normalize all propensities, then recursively normalize the
coordinates whose preceding normalized mass is zero. This terminates after
at most the number of sources.

Every sequence of Green occupations has a weakly convergent subsequence on
this compact space. Bounded reaction jumps preserve every asymptotic
coordinate and flag on an edge of positive limiting mass. A change of active
set, support, box, workload chamber, or flag is retained as a chart edge.

## Active and bounded coordinates

The active set is the set of coordinates equal to infinity in the boundary
descriptor. Split the limiting occupation over the finitely many active
sets and retain a positive-mass component.

Coordinates outside the active set have a probability distribution on
`N_0`. For every `epsilon>0`, choose a finite box carrying at least
`1-epsilon` of both source and endpoint mass and pad it by the maximum
reaction jump. Box-crossing flow is retained as promotion/exit flow. If no
fixed box is tight, that coordinate is promoted to the active set.

Thus an occupation alternating between neighborhoods of `(n,0,0)` and
`(0,n,0)` is split into the `{A}` and `{B}` active charts; it is never placed
in a chart enabling both active source families.

## Finite chart circulation

After fixing one box and one compact tied-ratio cell, all discrete chart data
form a finite graph. Indicator-function telescoping gives asymptotic flow
balance. Choose a terminal strongly connected component of positive limiting
flow. Positive outgoing flow is a structural exit; otherwise the component
has fixed active set, box, support, flag, ratio cell, workload chamber,
target phase and lattice data.

Letting `epsilon` decrease and diagonalizing gives a nonzero terminal chart
occupation with zero normalized structural-exit flux.

## Workload balance

Scale the terminal workload to integer values. Restrict the killed Green
paths to a long workload band. Because reaction workload jumps are bounded,
summing flux over consecutive lower cuts counts each transition only a
bounded number of times. One lower cut therefore has normalized inward flux
tending to zero. The retained upper-cut flux is outward. Hence on the
terminal chart,

\[
\sum_{x,e}\nu(x,e)\,h\cdot\zeta_e\ge0.
\]

If a faster neutral layer dominates raw reaction counts, contract its finite
phase and normalize the exact trace at the next physical source layer. A
layer of vanishing fraction is passed to the next slower normalization, not
discarded. The finite flag guarantees termination.
