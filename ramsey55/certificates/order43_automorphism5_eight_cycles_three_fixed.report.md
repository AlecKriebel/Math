# Order-43 automorphism-5 fixed-vertex split

## Scope and result

This branch covers graphs on 43 vertices admitting an automorphism with cycle
type \(5^8 1^3\). The formula and symmetry split were independently replayed.
No construction was found. The negative solver outcomes below have no proof
certificates and therefore **do not** exclude this automorphism class.

## Exact orbit formula

- edge-orbit variables: 183 (180 orbits of size 5 and 3 singleton orbits);
- unique five-set signatures: 192,054;
- Ramsey clauses: 384,108;
- hypothetical deterministic DIMACS SHA-256:
  `8abb891e769995940c06f403bb261b8d4e4c7c5d03749b7a13ca445182c4b7c6`.

The signature-size histogram is

```text
2: 8, 3: 24, 5: 24, 6: 280, 7: 3,096,
8: 2,632, 9: 42,000, 10: 143,990.
```

Two independent implementations reproduced all counts and the DIMACS hash.
The formula was kept in memory and was not materialized.

## Fixed-vertex degree normalization

Every vertex in a \((5,5)\)-Ramsey graph on 43 vertices has degree between 18
and 24, using \(R(4,5)=25\) on its neighborhood and non-neighborhood. If a
vertex is fixed by the order-5 automorphism, its degree is

\[
5m+\epsilon,
\]

where \(m\) is the number of adjacent moved cycles and \(\epsilon\in\{0,1,2\}\)
is its degree among the other two fixed vertices. The interval 18--24 forces
\(m=4\) for every fixed vertex.

Global color complementation reduces the fixed three-vertex graph to either
an edgeless graph or a graph with one edge. The three four-subsets of the
eight moved cycles are then classified by their eight membership-cell counts:

- edgeless fixed graph, with its full \(S_3\) action: 21 types;
- one-edge fixed graph, with endpoint exchange: 38 types.

Thus 59 types form a complete exact cover after cycle-block relabeling.

## Proof-free search observations

Two complete CaDiCaL sweeps used deterministic seeds and independent phase
orders:

- 100,000 conflicts per type: 56 observed UNSAT, 3 budget exhaustions;
- 500,000 conflicts per type: 56 observed UNSAT, 3 budget exhaustions.

Across the two sweeps, 58 of 59 types returned an unchecked UNSAT outcome at
least once. The sole common survivor is the one-edge type with membership
counts `(1,1,1,1,1,1,1,1)`.

For that type, each moved 5-cycle must choose exactly one of its two internal
distance classes. Endpoint exchange and the common multiplier \(x\mapsto2x\)
reduce the 256 orientation vectors to 80 exact orbits. Two complete refined
sweeps gave:

- 20,000 conflicts per orientation: 62 observed UNSAT, 18 exhaustions;
- 100,000 conflicts per orientation: 67 observed UNSAT, 13 exhaustions;
- union: 68 of 80 orientations observed UNSAT at least once, with 12 common
  budget exhaustions.

MapleChrono and Glucose4 also each exhausted 500,000 conflicts on the
unrefined all-ones type. These are constructive-search observations only.

## Reproducibility

- search:
  `src/automorphism5_fixed_split_search.py`;
- structural tests:
  `tests/automorphism5_fixed_split_tests.py`;
- 100k result SHA-256:
  `6dd44e0095c78047e6db655d530b38b44ca077af0a3f01d2d4c39952f027f739`;
- 500k result SHA-256:
  `5338bb9ddd408a55b6b3acfd57e727eb6e1360d96ead41697d9c84fd71dd3af0`;
- internal-80 20k result SHA-256:
  `d63191a64d3cdbd37cb8da42bc9c9b8d2770c87183fc15fb1bca0671aa9b3ad3`;
- internal-80 100k result SHA-256:
  `3b6e45a1d7ac983bebe7d0f385339251a1b7737ac80f457b7194893ad072178a`.

All negative records explicitly set `negative_certified: false`.
