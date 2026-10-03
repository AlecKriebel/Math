# Independent exact finite invariants and asymptotic diagnostics

Prepared after the initial mechanism seal, still before candidate/prior/sibling exposure. These are elementary audit controls, without a novelty or priority claim.

For each positive squared distance `d`, let `V_d` be the set of points incident to a pair at that squared distance. Double counting point-distance incidences gives

`sum_p R_P(p) = sum_d |V_d|`.

Therefore `2*D(P) <= sum_p R_P(p) <= n(n-1)`, where `D(P)` is the number of global distances. This remains a different statistic from `M(P)`. An arbitrary assignment of local counts satisfying these bounds need not have a Euclidean realization, so the incidence bounds alone cannot prove the source claim.

For `n>=2` distinct points, `M(P)<=n-1`. More generally the same upper bound holds for labelled configurations with repeated coordinates: if their coordinate support has size `k<n`, all labels at a given coordinate have the same local distinct-distance count, so `M<=k<=n-1`; if `k=n`, the distinct-point bound applies. This does not by itself establish equality of the distinct-set and labelled-multiset extremal functions.

For a set union, cross-component distances change the local counts. Private controls give:

| Configuration | Exact counts | Spectrum | Point count | M |
|---|---|---|---:|---:|
| `(0,0),(1,0),(2,0)` | `(2,1,2)` | `{1,2}` | 3 | 2 |
| `(10,0),(11,0),(12,0)` | `(2,1,2)` | `{1,2}` | 3 | 2 |
| Both disjoint triples | `(5,4,5,5,4,5)` | `{4,5}` | 6 | 2 |
| Triples `0,1,2` and `2,3,4` as set union | `(4,3,2,3,4)` | `{2,3,4}` | 5 | 3 |

The extended run actually rejects an expected union `M=4`, an expected old-value union `{1,2}`, and an expected overlapping cardinality 6. These are actual failing mutated expected-answer assertions, not merely descriptions of intended tests.

The nine-point integer grid `{-1,0,1}^2` has 511 nonempty subsets. Private complete enumeration preserves all maxima/histograms/witnesses in `runs/bounded_grid/stdout.txt`. Together with the universal bound, the small witnesses establish only the elementary finite controls `g(1)=1`, `g(2)=1`, `g(3)=2`, `g(4)=3` under the distinct-set convention. In particular, the four-point configuration `(0,0),(1,0),(0,1),(0,-1)` has local counts `(1,2,3,3)`. All enumerated maxima for `n>=5` are explicitly grid-restricted, not global optimality results.

An exact near-coincident rational triple `0,1,1+10^-30` on a line has three distinct pair distances and all local counts 2. The floating conversion of its last two coordinates can coincide; exact fractions prevent that cardinality/equality error.

The asymptotic target is `g(n)/n -> 1`, using the universal upper bound. A fixed limit `c<1` from a construction is partial evidence only. A sparse subsequence of high ratios gives only a limsup unless there is a transfer argument. For reference, adjoining a point outside finitely many forbidden circles can give exactly one new distance at each old point and preserve all distinctions among old local counts; thus `g(n+1)>=g(n)` in the distinct-point model. A subsequence construction with size ratios tending to one can use this monotonicity to transfer to all sizes; an arbitrary sparse subsequence cannot. This is an audit diagnostic, not a construction approaching the target.
