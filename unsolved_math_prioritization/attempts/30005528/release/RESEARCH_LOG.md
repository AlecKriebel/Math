# Research and verification record

## Readiness

- The problem landing page returned HTTP 403. The catalogue record was recovered from the pinned source corpus and independently checked against the official report.
- The current main queue row was queued at 0/5. Exact-ID/code checks in the existing research corpus found no earlier same-problem attempt; repository code search also returned no result. These checks are documented as limited searches, not proof that no prior discussion exists anywhere.
- The source's compactness requirement applies to the alphabet. Its tiles are ordered pairs. The size function need not separate symbols, and no metric-distance packing realization is required.
- The later Gonçalves–Vedana paper was inspected for attribution and scope. It does not license promoting an abstract counterexample into a packing counterexample.

## Approach 1: encode a continuous rotation family

An irrational rotation supplies an aperiodic compact dynamical system, and its graph is a legal closed tile relation. A bare irrational rotation would give no periodic competitors. To eliminate that weakness, vary the rotation angle with a preserved height t∈[0,1] and choose the continuous cost 1+t.

The resulting system has aperiodic minimizers at t=0 and dense rational-rotation periodic competitors at positive heights. Every orbit average is evaluated directly, including the N+1 numerator terms in the source's normalization. The exact period criterion is p(√2+t)∈ℤ. This gives a complete counterexample in the first substantive approach; further attempts toward a solution are unnecessary.

## Adversarial checks incorporated into the proof

1. **All legal sequences:** because the relation is a graph, every legal sequence is an F-orbit; there are no hidden height-changing paths.
2. **Attainment:** bottom-circle sequences exist and all have average 1.
3. **Periodicity:** periodicity is of the ordered tile sequence, equivalently the underlying starting point, not merely periodicity of the numerical sizes. The sizes alone are constant along every orbit.
4. **Nonvacuity:** rational-rotation heights give densely many periodic starting points.
5. **Closedness:** the graph is compact and closed; the alphabet is connected.
6. **Limit issue:** near-optimal periodic competitors must have unbounded periods, as quantified in the proof.
7. **Scope:** the alphabet is not assumed to be an interval of real sizes with a prescribed pairwise-distance rule. Adding such hypotheses would change the problem.

## Exact checks and limits

The accompanying standard-library Python script checks 256 explicit algebraic heights, 23,955 smaller candidate periods, 1,280 finite-prefix normalization instances, and 5,022 rational periodic-angle instances with reduced denominator at most 128. Arithmetic uses fractions and the exact field ℚ(√2); no floating-point tolerance is used. It also checks the exact inequality behind the bounded-period gap in all 5,022 rational-angle instances.

These finite checks are only a reproducibility aid. The infinite conclusion follows from the displayed formulas, compactness, density of rational numbers, and the exact irrationality proof. Nothing is inferred from an unsuccessful finite search.

## Status

Complete counterexample to the literal abstract question, pending fresh independent audit. No claim of historical priority, solution of the interval-packing problem, or exhaustive literature coverage is made. Publication and any final status change require the independent review gate.
