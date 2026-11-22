# Independent adversarial review: row 1899 partial results

Decision: ACCEPTED WITH EXPLICIT PARTIAL-PROGRESS SCOPE. This accepts the mathematical statements below, not a solution of arbitrary gaps with all ordinary two-way margin entries positive. No novelty, exhaustive-literature, or historical five-turn claim is accepted or made.

The reviewed REPORT.md has SHA-256 0205fc9137b0ce9e65d9fbdcd952bb759f58912292825ce9e9961082e796fce5. The accompanying receipt binds all reviewed source and certificate bytes. Review performed 2026-10-21 UTC.

## Accepted mathematical results

1. The varying-design logistic family is completely parameterized by integer t from 0 to q and has middle-cell spacing L. Its positive group and response totals do not turn its weighted statistic into an ordinary two-way margin.
2. The complete 2×J×K ordinary fiber has interval cell spectra. Fixing an interpolated integer target and deleting its edge leaves an integral capacitated bipartite flow problem. This argument works with zero as well as positive margins.
3. The path-crossing bound is correct even if a connecting path first decreases its target coordinate: the first crossing above a starts at a value at most a and lands at least c.
4. The complete integer kernel has a unit-target cube, so its equations alone cannot impose a nontrivial target congruence. The corrected report properly attributes any restricted spectrum to nonnegativity restricting feasible integer points, without asserting a proper exposed face is necessary.
5. The anchored cubes form an integer basis. An ordered sequence of signed unit cubes has partial coordinate magnitude at most its number of terms, so the displayed padding bound makes the entire path nonnegative. This is endpoint-dependent padding, not a proof that arbitrary positive margins suffice.
6. The fixed-two-dimensions Graver/Dickson argument is sound. Every slice decomposes conformally over a finite signed Graver set. The resulting finite-dimensional nonnegative count vector belongs to a fixed nonnegative integer kernel, whose coordinatewise-minimal nonzero vectors form a finite set by Dickson. Repeated subtraction partitions all labeled occurrences; grouping each piece by original slice preserves sign conformity, slice row/column sums, and the entrywise sum of slices. Partial aggregate moves stay coordinatewise between the endpoints. The displayed finite D bounds every move coordinate independently of the number of slices. This proves a uniform gap bound whenever two dimensions are fixed. It does not give such a bound when two dimensions vary.
7. The exposed-support criterion is a correct sufficient route: nonnegative pair-potential costs and zero total cost force support on their zero set. Full pair coverage is necessary for positive margins. No universal embedding into such a support has been proved here.

## Independent exact certificate checks

The separate verifier reconstructs the 6×4×3 margin matrix and the three printed margin arrays directly. It does not call the MILP solver or execute any author verification script.

- All 165 stored witnesses in probe_results.json pass strict Python-integer nonnegativity, shape, target, and all 54 margin equalities.
- All 10 positive-offset cases contain every integer through the sharp incident-margin upper bound 2s+3t. Their complete interval spectra are certified by existence plus this bound, not infeasibility statuses.
- The zero-margin active set has exactly 26 cells. Independent Fraction Gaussian elimination gives rank 25. The supplied integer vectors c,d satisfy M c=b and M d=0, and d is nonzero. Consequently every real scaled solution is s c+tau d. A coordinate equals tau; endpoint inequalities and attained constraints give precisely s≤tau≤2s. This proves, for every positive integer s, the complete integer target spectrum {0,2,...,2s}.
- All four extra witnesses for margins A1 pass the same independent integer checks, proving target spectrum {0,1,2,3}.
- The all-parameter padding theorem is valid: adding one table with target in [0,5], s−1 base tables with targets 0 or 2, and t−1 all-ones-margin tables with targets in [0,3] realizes [0,5]+{0,2,...,2(s−1)}+[0,3(t−1)]=[0,2s+3t]. The incident margin gives the reverse containment. Thus this entire particular padded and dilated family has no gaps for every integer s,t≥1. No claim that all feasible tables decompose this way is needed.

## Optional elementary strengthening

For any feasible x in any complete I×J×K format with dimensions at least two, and any integer t≥0, x+t1 has every cell at least t. A signed unit cube through target h can therefore be added r times for every integer −t≤r≤t while preserving nonnegativity and margins. Thus each old attainable target d supplies every target in [d,d+2t] after padding, centered at d+t. This explains directly why uniform padding cannot be assumed to preserve old holes. It is not itself a proof that all sufficiently short original intervals become an entire new global spectrum.

## Correction and limits

One original wording overstatement was reported and corrected before acceptance: a restricted integer congruence need not be shown to arise on a proper exposed face. No remaining mathematical error was found in the reviewed report. Solver infeasibility flags alone are not accepted as proofs; zero-offset completeness instead rests on the independent exact affine certificate. Bibliographic search completeness and external-paper proof correctness were not independently audited. The arbitrary-gap positive ordinary-margin construction remains unresolved by this work.
