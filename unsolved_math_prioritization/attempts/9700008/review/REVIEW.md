# Independent audit of the Metropolis partial results (9700008)

Verdict: **PASS_SCOPED_PARTIAL_RESULTS**, with no mandatory correction. The complete original record remains **unsolved / source-held**, using two substantive approaches. This is an independent AI mathematical review, not human peer review or a novelty certification.

Reviewed artifact: `PARTIAL.md`, SHA-256 `7e5b4acc667845034b4962bd009cfc1feaa4cb0eabffc90b0632622572364cb4`. Review date: 2026-09-30. Reviewer used its inherited runtime; exact model identifier was not exposed and no model or reasoning switch was made.

## Source and convention audit

The [original Aldous page](https://www.stat.berkeley.edu/~aldous/Research/OP/cayley.html) was independently retrieved. It specifies a geometric success parameter between zero and one and stopping at T−1, explicitly assigns the uniform distribution at zero, and asks both a decreasing-relaxation question and comparisons involving an undefined infinity endpoint. The two occurrences of that endpoint really are on the source page. Replacing infinity by zero, inverting the parameter, or replacing success probability by mean stopping time would be a substantive reinterpretation. The submitted conditional discussion does none of these silently.

The [Aldous–Fill Metropolis definition](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch11.S2.html) supports the symmetric-proposal acceptance rule. Their [relaxation section](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch4.S4.html) explicitly uses the reciprocal ordinary algebraic spectral gap in discrete time, not the absolute gap. It also gives the variational characterization and states that the complete graph attains relaxation time 1−1/N. This independently confirms that values below one at the uniform endpoint are intentional. Bipartite periodicity does not invalidate that ordinary-gap convention.

## Complete-graph audit

Solving the two-level resolvent gives the stated center and off-center masses, which are positive and sum to one. The noncentral zero-sum subspace has dimension N−2; its eigenvalue is −1/(N−1). The remaining two-dimensional quotient has eigenvalues one and (N−2)/(N−1)−b/a. These account for all N dimensions, also when N=2 and the contrast subspace is empty. The quotient eigenvalue is at least the contrast eigenvalue because b/a≤1. Thus the claimed ordinary relaxation formula follows, and direct differentiation gives the positive derivative (N−1)^3/(N−p)^2.

The K4 masses, eigenvalues, and times were independently checked. At both parameters the positive nontrivial eigenvalue exceeds 1/3, so the absolute-gap version has precisely the same times. Fixed post-construction lazification scales all ordinary gaps equally; for laziness at least one half it also removes negative eigenvalues. Lazifying the proposal before constructing the geometric resolvent is a different operation, but the submitted separate formula for it is correct.

At p=1/2 the ordinary endpoint ratio is N²/(2N−1), and the absolute-gap ratio for N≥4 is N(N−2)/(2N−1). Both diverge. The use of graphs of growing degree is disclosed, and no bounded-degree assertion follows. This only refutes the explicitly conditional zero-endpoint interpretation; it does not adjudicate the undefined infinity comparison.

## All-regular-graph bound

The proof does not need transitivity, but it does need the stated symmetric regular proposal. Positivity follows from connectedness and the resolvent expansion. Any nonroot maximizer contradicts its resolvent equation, so the root is the unique maximum.

For each edge oriented strictly downhill in stationary mass, the submitted flow is nonnegative. Its divergence equals the point source minus the target mass, including the root divergence 1−μ(root). Equal-weight edges carry zero flow and do not affect the divergence identity. The strict downhill orientation is acyclic. Adding a sink with demand μ(x) at each nonroot vertex yields a finite acyclic source-to-sink flow. The standard decomposition is valid: no positive-flow component can arise without a source, and removing complete source–sink paths exhausts it. Deleting their terminal sink edges leaves paths with at most N−1 graph edges, total terminal mass μ(x), and total traversal mass on any edge exactly its flow. The remaining root mass uses a length-zero path.

For a downhill edge x→y the nonroot resolvent at y implies μ(y)≥(1−p)μ(x)/d. Hence its flow is at most μ(y)/p. The variance is bounded by the second moment around the root; weighted path Cauchy–Schwarz gives the claimed length factor. Detailed balance makes each unordered-edge conductance min(μ(x),μ(y))/d. Thus there is no missing factor two, and the Poincaré constant is bounded above by d(N−1)/p for every graph in the stated class. This bound concerns ordinary relaxation; an absolute-relaxation bound on all regular graphs is not asserted.

## Independent controls

The submitted verifier was replayed outside the author's folder. Its 14,121 rational assertions and receipt reproduce byte-identically. Its frozen proof hash, verifier hash, and receipt hash were independently checked.

A separately written checker performs 992 exact assertions. It enumerates every connected labeled simple regular graph on two through five vertices, adds K3,3 and the triangular prism, and uses three rational parameter values. For all 63 models it computes the resolvent independently and certifies the full Poincaré inequality via positive leading principal minors of the exact rational quadratic-form matrix on a coordinate section transverse to constants. These controls do not reuse the author's flow-decomposition algorithm. Complete characteristic polynomials on N=2–10, the derivative, and the endpoint ratio are also checked symbolically. These finite checks supplement the all-size proofs; they are not a computer proof over every graph.

## Publication limitations

Preserve the undefined endpoint warning and the original record's unresolved status. Keep the ordinary-versus-absolute distinction, the growing-degree qualification, and the distinction between lazifying the proposal and lazifying the final chain. No additional theorem, definition of the source endpoint, first-discovery assertion, or human peer-review assertion is authorized by this audit. No mathematical correction was required.
