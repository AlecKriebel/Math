# Results and proof dependencies

## Canonical theorem

- [Complete construction](pass1_construction/CONSTRUCTION_PROOF.md): degree-four graph, uniform C = 100 quasi-isometry, iid reduction, complete probability proof, and d = 1 endpoint.
- [Exact constants](pass1_construction/EXPLICIT_CONSTANTS.json): p₀ = 9/10, p = 19/20, L = 100, survival at least 143/245, bridge probability below 27/107648, and nonuniqueness probability above 2200741829/6461571200.
- [Independent probability audit](pass1_probability/PROBABILITY_AUDIT.md): parity proof for the quadrant dual crosscut, global bridge counting, disjoint edge sigma-fields, and strict supercriticality.
- [Independent geometry audit](pass1_geometry/GEOMETRY_AND_ENDPOINT_AUDIT.md): simplicity, degrees, uniform metric bounds, exact infinite-cluster correspondence, planarity, one-endedness, and the dimension-one endpoint.
- [Independent validation](pass1_validation/INDEPENDENT_VALIDATION.md): separate mathematical proof review and documented finite checks.
- [Final independent acceptance](pass1_audit/INDEPENDENT_ACCEPTANCE.md): accepted statement, source-scope limits, and immutable input pins.

## Supplementary constructions

The geometry audit includes the following independent strengthening directions. They are secondary to the canonical dimension-two witness and retain their own constants.

- Full opposite orthants in every d ≥ 2, replacing weak edges by length L_d = 80d paths: maximum degree 2d, quasi-isometry constant 80d, p_c ≤ 9/10 < 19/20, and positive-probability nonuniqueness.
- An additive-only realization in every d ≥ 2: retain lattice edges and add M = 1024d² distinct two-edge paths beside each strong edge. This is a simple graph of degree at most 2d(M+1), with additive metric error two. Use p₀ = 1/(16d) and p = 1/(8d). Its effective strong probability is 1−(1−p)(1−p²)^M. The same quadrant-survival and bridge arguments yield positive-probability supercritical nonuniqueness.
- The probability audit's reflection fallback uses p₀ = 1295/1296, p = 2591/2592 and L = 12960. It is an optional cross-check; the canonical proof relies only on the shorter direct parity argument. The finite validator checks its arithmetic, which does not by itself certify the fallback's full-plane contour argument.

See the final acceptance report for the exact scope independently accepted. No optional statement is needed as an input to the canonical theorem.

## Source and verification records

- [Source contract](CONSTRUCTION_CONTRACT.md) and [source-scope adjudication](source_scope/SOURCE_SCOPE_ADJUDICATION.md).
- [Bounded source and prior-art comparison](pass1_literature/SOURCE_COMPARISON.md) and [source guide](SOURCES.md).
- [Original and public identities](ORIGINAL_IDENTITIES.json), [package manifest](MANIFEST.json), [replay results](CHECK_REPLAY.json), and [reproducibility guide](REPRODUCIBILITY.md).
