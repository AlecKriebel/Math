# Independent mathematical acceptance report

Date: 15 October 2026. Status: **ACCEPTED for the precise partial results below. Erdős Problem 168 remains UNSOLVED.**

This report records an independent review of the five authored mathematical supplements identified in [AUDIT_BINDINGS.json](../AUDIT_BINDINGS.json). Acceptance is a mathematical and reproducibility review of these specific editions, not external peer review, an exhaustive novelty assessment, or a claim that the density is rational or irrational. The artifacts are newly reconstructed; no earlier artifact's byte identity is inferred.

## Accepted statements

1. [Finite certificates](../proofs/01_FINITE_CERTIFICATES.md): exact unrestricted hitting minima, optimal counts, witnesses and constrained comparisons through the first 200 smooth cutoffs, ending at d_200=15,116,544. Equality of unrestricted tau with q1 is accepted only on this stated finite range.
2. [Exact-one structure](../proofs/02_EXACT_ONE_STRUCTURE.md): the all-scale formula q0(X)=min C_r(X), the exceptional one-saving construction, the high-defect-row reduction, elementary bounds on B=Psi-3tau, and the pure-two jump property.
3. [Arithmetic results](../proofs/03_ARITHMETIC_RESULTS.md): the classical exact density series rederived with its correct conventions; the bounds and unboundedness of B; the ordinary-truncation denominator obstruction; the identity involving 101/126 and the actual output E; and the explicit corrected-color candidate's binary output and nine-breakpoint skew product. The candidate is identified with q1 by the separate theorem, not with unrestricted tau.
4. [Single-defect theorem](../proofs/04_SINGLE_DEFECT_THEOREM.md): for every real X>=1, q1(X)=min_r(C_r(X)-epsilon_r(X)), with epsilon_r the specified half-open exceptional patch indicator. The written classification, exhaustive local configurations and 280 finite base cutoffs provide a complete lower bound; the explicit patch provides the upper bound.
5. [Reciprocal-tail correction](../proofs/05_RECIPROCAL_TAIL_CORRECTION.md): for S={2,3}, X*T(X)-log X/((log 2)(log 3)) is unbounded in absolute value. This contradicts the O(1/X) remainder in Proposition 4.3 of the inspected arXiv:2604.15515v1. The exact tail identity and O(log X/X) bound remain valid, as do the independently derived density series and exact nested bounds. No conclusion about unrelated source statements is drawn.

Here q0 restricts total excess D to zero, q1 restricts D to at most one, and tau is unrestricted. Thus tau<=q1<=q0. No pairwise-ratio exclusion is substituted for avoiding the complete triple {n,2n,3n}.

## Critical proof checks

The exact-one proof reduces every cutoff to a forced phase, four terminal profiles and eleven small base cases. Its height-three stencil is exhaustive.

The single-defect proof exhausts high-row, low left-axis, impossible interior, and residual terminal defects. In the terminal case, normalization produces eight shapes and three phases each. Every one of the 173 surviving configurations agrees with its phase on the entire interface column. This invariant justifies extension to all omitted left columns, including rows above the normalized domain. Only one normalized configuration has negative cost, and it is exactly the translated exceptional patch. The 280 smaller smooth cutoffs are separately optimized with exact integer arithmetic.

The unbounded-B and auxiliary-tail arguments were checked analytically, including Laplace transforms, coefficient signs, nonresonance, the continued-fraction approximations, and the finite-set Abel-Bessel contradiction. The bounded-function norm does not need a limiting value; its uniform bound suffices. Numerical trends are not used as proofs of either unboundedness statement.

The density series uses d_1=1 and f(0)=0. Numeric X=192 contains 25 smooth values; it is not prefix index 192. Reciprocal tails use d>X, while vertex sets use d<=X. The exceptional interval's upper endpoint is excluded.

## Independent finite evidence

The review added separately implemented methods:

- A transposed exact transfer reproduces all minima and optimal counts through smooth index 77.
- Vertex include/exclude branching reproduces all minima through index 45.
- Direct full-integer interval optimization agrees with the smooth decomposition for every N=1,...,80.
- All 200 unrestricted and constrained witnesses were checked directly against their triples.
- A second implementation of the constrained transfer reproduces all 280 single-defect base minima. This is explicitly the same algorithm family, not a different optimality method.
- A closed-form binomial convolution, importing no local recurrence checker, independently reproduces the T3, T6 and T7 classifications and every one of the 173 suffix configurations.

The finite anchors agree: d_24=162 has tau=7 and one optimum; d_45=1536 has tau=14 and one optimum although each adjusted color class has size 15; d_77=19683 has tau=25 and twelve optima. The index-45 optimum's sole double-hit triple is {192,384,576}.

The review used successful normal, -O and -OO executions with explicit guards and rejection controls for changed minima, counts, endpoints, witnesses, recurrence values and missing interface information. The public package's own read-only replay and integrity checks are a separate final release gate; this report does not replace them.

## Source and edition boundaries

The reviewer visually checked the classical series in Graham–Witsenhausen–Spencer (1977), printed pp.107–108, and the precise tail claim in the pinned Veselinov v1 PDF, printed p.10. The source guide records the remaining retrieval and inspection limits. In particular, the final typeset Chung–Erdős–Graham chapter was not inspected, and its numerical claims are not adopted as independently established inputs.

The public proof editions were compared with the reviewed mathematical texts. The mathematical definitions, hypotheses, recurrences, tables, bounds and constants were preserved. Editorial changes concern presentation, scope statements and public replay paths. The exact accepted bytes are listed in [AUDIT_BINDINGS.json](../AUDIT_BINDINGS.json); later mathematical edits require renewed review.

## Explicitly unresolved

- All-scale unrestricted tau=q1.
- Binary actual output E(X) at every scale.
- A finite-state model for the unrestricted optimizer.
- Rationality or irrationality of alpha.

Finite agreement, a constrained all-scale formula, and an irrational rotation underlying the candidate do not establish any of these assertions.
