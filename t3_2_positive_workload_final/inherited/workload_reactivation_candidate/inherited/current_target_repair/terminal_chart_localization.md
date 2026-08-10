# Terminal chart localization for reaction-count occupations

This theorem uses the certified embedded labelled reaction-count Green
occupation, not a time-normalized intensity measure.

## 1. Compact descriptor

Push each occupied labelled transition to the descriptor consisting of:

* the three coordinates in \(\mathbb N_0\cup\{\infty\}\);
* capped availability \(\min(x_i,2)\);
* actual current target and labelled channel;
* enabled source set;
* all pairwise normalized physical source-rate ratios;
* active face, lattice data and structural rank.

The descriptor lies in a compact finite product.  An escaping Green sequence
has a weakly convergent subsequence of probability edge occupations, and its
limit is supported at infinity.

## 2. Active sets and bounded coordinates

The active set of a boundary descriptor is the set of coordinates equal to
\(\infty\).  Bounded reaction jumps cannot change that set on an edge of
positive limiting mass.  Split the limiting occupation over the finitely many
active sets and retain one positive-mass component.

Coordinates outside the active set have a tight marginal.  Given
\(\varepsilon>0\), choose a finite box containing all but \(\varepsilon\) of
its source and endpoint mass.  After padding by the maximum jump, normalized
box-crossing flux is at most \(2\varepsilon\).  Such crossings are retained
as active-set promotion or box-exit flux rather than omitted.

## 3. Complete source flag

The finite source set has compact pairwise rate-ratio coordinates.  Their
limits define a total preorder.  Ratios converging to zero are passed to a
strictly slower layer; disabled sources are removed exactly.  Recursively
compactifying tied source differences produces at most three logarithmic
layers.  A finite-base rational scalarization is positive on every active
coordinate and preserves every source comparison.

## 4. Finite chart flow

For a fixed inactive box, the active set, availability, source support,
source preorder, tied compact cell, workload chamber, target and lattice
labels give finitely many chart nodes.  Exact bounded-test balance of the
reaction-count occupation gives a finite circulation.  Select a terminal
strongly connected component of its support.  Every omitted transition has
one declared meaning: box exit, active-set promotion, support or flag
refinement, lower workload shell, or lower structural rank.

Letting \(\varepsilon\downarrow0\) gives a nonzero terminal chart occupation
with zero normalized structural-exit flux.  A distributed occupation near
\((n,0,0)\) and \((0,n,0)\) splits between the active sets \(\{A\}\) and
\(\{B\}\); it is never placed in a chart that assumes both mixed sources are
enabled.

## 5. Workload balance

Scale the rational workload to integer values and sum the exact reaction-count
balance over a long workload band.  Bounded jumps cross only finitely many
cuts.  Averaging the lower cut selects one whose normalized inward flux tends
to zero, while the retained upper boundary flux is nonnegative.  Hence every
terminal chart occupation satisfies

\[
 \sum_{x,e}\nu(x,e)h\cdot\zeta_e\ge0.          \tag{5.1}
\]

For an \(\varepsilon\)-terminal box the lower bound is \(-C\varepsilon\).
All strict local conclusions are uniform on the compact tied-rate cell, so
one box with sufficiently small \(\varepsilon\) yields the contradiction.

## 6. Episode and trace localization

Current-target episodes have bounded designated depth.  Priority-clearing
traces may have unbounded reaction count, but their carrier trial has finite
mean and a uniform negative physical-credit drift in every strict chart.
Their expected labelled counts can therefore be pushed through the same
finite chart circulation.  If an episode or source layer has zero normalized
count, it is passed to the next slower reaction-count trace; it is not
discarded.

Thus every escaping occupation has a positive-mass terminal chart on which
the source-layer current-target theorem, the certified atlas, or the
one-active theorem applies.
