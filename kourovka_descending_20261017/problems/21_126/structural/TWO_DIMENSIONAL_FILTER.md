# Stronger prior exclusion: two-dimensional Artin groups

Prepared October24,2026 UTC. This is a **known theorem**, newly incorporated into this family's audit. It is stronger than the forest-only argument in FORESTS_AND_CLOSURE.md and must receive priority credit.

Huang–Osajda, *Metric systolicity and two-dimensional Artin groups*, Math. Ann.374(2019),1311–1352, [DOI10.1007/s00208-019-01823-6](https://doi.org/10.1007/s00208-019-01823-6), [arXiv1710.05157v2](https://arxiv.org/abs/1710.05157v2), Corollary1.3, states that finitely presented subgroups of two-dimensional Artin groups have a quadratic Dehn upper bound. Their Theorems1.1–1.2 prove this by metric systolicity and its inheritance by finitely presented subgroups. This is an actual subgroup theorem; no unsupported ambient CAT(0) inference is being used.

The dimension condition is explicit in the introduction (arXiv printed p5): dimension means cohomological dimension, and dimension≤2 is equivalent to the reciprocal-label condition 1/p+1/q+1/r≤1 for every labelled triangle. A triangle-free RAAG has no such triangle, so meets the condition. If it has at least one edge its cohomological dimension is exactly2: its Salvetti complex is two-dimensional and it contains Z². Edgeless graphs give free groups; their finitely generated subgroups are free and have linear Dehn upper bounds. Thus **every finitely presented subgroup of every finite triangle-free RAAG has a quadratic upper bound**. In particular neither branch of21.126 can be witnessed in such an ambient group.

The original arXiv PDF downloaded from the v2 URL has the arXiv margin date March15,2019 but a body date November2,2021. Both are recorded faithfully; the latter is not treated as the arXiv submission date. The independently inspected publisher version of record was published April10,2019 and contains the same theorem, so this date anomaly does not affect priority or the mathematics.

## Expanded exclusion class

Let C+ be the least finite-graph class containing (a) all triangle-free graphs and (b) all complete multipartite graphs with at most three parts, and closed under disjoint unions and adding universal vertices. By the degree-nine three-free-factor theorem of Ascari et al.2406.19860v2 and the closure proposition proved in FORESTS_AND_CLOSURE.md, all finitely presented subgroups of RAAGs on graphs in C+ have δ≼n^9. This includes the older forest-seeded class, whose earlier census remains separately preserved.

The exact standard-library census in dimension_two_census.py/json gives:

| Vertices | Labelled graphs in C+ | All labelled graphs | Isomorphism classes in C+ / all |
|---|---:|---:|---:|
|0|1|1|1/1|
|1|1|1|1/1|
|2|2|2|2/2|
|3|8|8|4/4|
|4|64|64|11/11|
|5|754|1024|29/34|
|6|11723|32768|not computed|

The five outside canonical masks at5 vertices, using the script's lexicographic edge ordering, are59,185,187,221,254; their exact edge lists are in the JSON. Outside means only that this particular sufficient criterion does not apply. It does not establish that the ambient RAAG can support either requested witness, and it does not assert that no other known theorem excludes it.

A hypothetical witness therefore needs an ambient graph outside C+ in any finite-support embedding. The remaining problem includes infinitely many defining graphs of dimension≥3, arbitrary nonnormal finitely presented subgroups, and both rate branches. No full resolution or originality claim is made.
