# Independent acceptance: the fixed independent-function remainder

14 October 2026. Additional audit within the same shared PASS1. The exact proof and its Hardy-lemma dependency are pinned in `INDEPENDENT_FUNCTION_AUDIT_MANIFEST.json`.

**PASS.** For every \(Q=n+2\ge3\), fixed \(0<R\le\infty\), strict positive \(C^1\) leading weight \(V\), real \(C^1\) potential \(W\), and one fixed independent positive \(C^2\) function \(g\), the proposed all-test inequality
\[
A_V[u]\ge D_{V,W}[u]+E_{V,g}[u]
\]
forces a positive exact coefficient-one Bessel solution on all of \((0,R)\). No side condition on \(V''\), sign condition on \(W\), or endpoint condition is needed for this necessity statement.

## Critical checks

The same \(g\) must serve every test. Its ODE property is not part of the premise. Source radial derivatives, polar factors and compact radial test admissibility agree with the separately accepted Hardy geometry. Each radial test used in the proof has finite left energy even when the original all-test class contains infinite-energy functions meeting the axis.

With \(p=r^{Q-1}V\), \(q=r^{Q-1}W\) and \(v=u_\rho\) for a radial spatial test, the core becomes \(\int(pv'^2-qv^2)\), while the remainder becomes \(\int pg^2((v/g)')^2\), with the same polar constant. Their difference is exactly
\[
\int K(r)v(r)^2\,dr,
\qquad K=-q-\frac{(pg')'}g.
\]
The signs were independently checked by expanding the square and integrating its cross term. The coefficient is continuous under the stated regularity.

The only available derivative tests satisfy \(\int v=0\). This constraint does not require an endpoint-capacity argument here: if \(K<0\) anywhere, continuity supplies an interior negative interval, and a nonzero derivative of a compact bump supported there is a zero-mean test with strictly negative multiplication form. Hence \(K\ge0\) everywhere.

Therefore \(g\) is a positive supersolution, \((pg')'+qg\le0\). For every unrestricted compact smooth \(h\), the exact identity
\[
\int(ph'^2-qh^2)=\int pg^2((h/g)')^2+\int Kh^2
\]
proves full one-dimensional form nonnegativity. The separately pinned, self-contained positivity lemma supplies a strictly positive exact solution on the whole fixed interval, with coefficient one and no endpoint restriction.

The radial version of the fixed-\(g\) premise is indeed equivalent to the supersolution condition. The audited proof correctly does not infer all-test sufficiency from that radial equivalence. It also does not claim that the given \(g\) solves the equality: only its supersolution property is forced, and the final exact solution may be different.

## Source boundary

This is an explicitly proposed interpretation of the source remainder. The literal GJR statement already assumes its remainder function is a positive ODE solution, so reversing that literal reading would assume the conclusion. These quantifiers must remain separate. No test-dependent choice of \(g\), novelty claim, human-review claim, or full informal-source disposition follows from this audit. [GJR v3, Theorem 1.3](https://arxiv.org/pdf/2404.05510v3)
