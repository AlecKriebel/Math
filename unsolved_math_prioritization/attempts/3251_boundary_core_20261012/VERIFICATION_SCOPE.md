# Exact audited finite coverage

These counts describe archived author and independent checks. Original programs, raw cases and output identities are not distributed. This edition does not rerun those exhaustive suites; it preserves their complete audits and verifies all reported coverage cells against accepted records. Small explicit examples are checked separately.

## Structural graph universe

All 33,868 labelled simple graphs of orders zero through six: 696 with chi>omega; 84 equality graphs (12 labelled C5s and 72 labelled joins K1 with C5); 624 indivisible graphs, all at clique number two; 3,732 antineighborhood instances; 12 minimal indivisibles, all C5s; 219,764 k>=3 edge-boundary instances with at least one division; zero equal-only and zero different-only forcing edges at k>=3.

The author also checks 11 named graphs and 1,972 separator-arithmetic instances. Independently, 181 benchmark instances cover six joins K_u with C5 for 0<=u<=5, every one-edge toggle, disconnected clique additions, antiholes of orders 7,9,11, four joins with the seven-antihole, and the join of two C5s. Independent arithmetic covers 1,449 triples with 3<=k<=20, 1<=s<=k and 2<=t<=8. No k>=3 indivisible or forcing-side example exists in this exhaustive universe; those bounds are proof-based and computationally vacuous here.

## Mixed-constraint universe

Every multiset of subsets of size at least two on each fixed labelled order 0<=n<=5, maximum vertex incidence two; positional edge occurrences are labelled, and all B/0/1 demand assignments are checked. Empty families, isolated vertices, repeated edges and nonuniform families are included.

| n | Families | Demand-labelled cases | Unsatisfiable | Repeated-edge families | Nonuniform families |
|---|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 3 | 13 | 0 | 1 | 0 |
| 3 | 16 | 130 | 1 | 4 | 3 |
| 4 | 139 | 2,599 | 4 | 20 | 67 |
| 5 | 1,750 | 69,604 | 142 | 171 | 1,285 |

Totals: 1,910 edge multisets; 72,348 demand-labelled cases; 147 unsatisfiable. Independent coverage includes 2,936 opposite one-sided-demand cases on identical repeated edges and 6,414 colorable cases obstructed if all demands were changed to B. Exact canonical case-set comparison preserves demand order on repeated copies.

## Graph-boundary universe

Every bit mask on all n choose 2 possible edges is checked once for 0<=n<=6. For graphs with k>=3, every clique boundary containing all vertices of maximum-clique incidence at least three and every admissible labelled coloring are checked. Independent graph/boundary/pattern case-set comparison is exact. Different author and independent stream encodings are not confused with identical digests.

| n | Graphs | With k>=3 | Eligible boundary pairs | Admissible colorings | k-1/common-neighborhood branches |
|---|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 2 | 0 | 0 | 0 | 0 |
| 3 | 8 | 1 | 8 | 25 | 12 |
| 4 | 64 | 23 | 244 | 805 | 364 |
| 5 | 1,024 | 636 | 8,152 | 29,351 | 12,760 |
| 6 | 32,768 | 26,979 | 392,104 | 1,563,254 | 618,664 |

Totals: 33,868 graphs; 400,508 eligible boundary pairs; 1,593,435 admissible colorings; 631,800 forced branches. Independent maximum-clique and clique lists agree for every graph. Additional coverage includes 19,947 empty-boundary pairs and 51,413 maximum-clique-boundary pairs.

## Explicit and supplementary tests

- Author odd cycles of lengths 3,5,7,9: all-B constraints are unsatisfiable; 48 single-one-sided rescues are checked. Abstract sharpness fixtures at ranks 3,4,5 have blocked monochromatic P, a divisible unconstrained family, outside incidence two, and complete shadow K_(2r-1).
- Independent odd-cycle assignments: all 2,457 B/0/1 assignments at lengths 3,5,7. Odd Euler real degrees 4,4,2 plus an isolate: all 27 assignments. Abstract precolor lemma: 2,441 simple-uniform cases through order five, including 238 high-incidence prescribed-vertex cases, plus repeated uniform-edge fixtures at ranks 3,4,5.
- Generalized nonclique special case: 23,897 colorings through graph order five, including 15,328 nonclique cases and 150 colorings containing high-incidence vertices.
- Full core Proposition A: 51,981 prescribed-color cases through graph order five, including 34,936 nonclique cases and 1,136 cases prescribing an entire maximum clique. These overlap other universes and are not a disjoint grand total.
- Necessity controls: C5 at k=2 with empty boundary; a nine-vertex triangle with three private attached triangles and its six-vertex nonclique boundary.

## Interpreter and hostile-control scope

The original structural author and independent programs pass under normal Python, -O and -OO, byte-identically within each family. Structural independent controls: 37 per mode, comprising two positives and 35 required failures. Original structural author controls: 22 negative controls per mode. Separate review-seal checks are archived.

The original boundary independent main, supplement and core suites pass byte-identically within each family under normal Python, -O and -OO. Main independent controls: 36 required rejections per mode, 108 total. Core controls: 13 required rejections per mode, 39 total. Author primary terminal evidence: 31 negative controls per mode. Author addendum terminal evidence: 16 integrity controls per mode. Both terminal receipts and all named evidence members were verified; only the independent core audit adds mathematical proof acceptance and the 51,981 finite cases. No acceptance gate relies on Python assertions.

All controls used disposable copies and are scoped to the explicitly tested static failure modes. They do not claim protection against concurrent filesystem races or replacement of every trusted external anchor. Finite regressions do not prove the unrestricted conjecture or sharpness of the forcing-side numerical barriers.
