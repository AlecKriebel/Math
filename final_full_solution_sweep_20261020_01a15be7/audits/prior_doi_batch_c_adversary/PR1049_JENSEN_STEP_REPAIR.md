# Conditional repair of Yakir's root-count deduction

Independent derivation, 2026-10-22 UTC. This repairs only the deduction of the root-count estimate from Lemma 1.3 of arXiv:2011.06234v2. It is not a new proof or full re-audit of Lemma 1.3, Sections 3–5, or the journal typesetting. The inspected preprint has SHA-256 `5733fe94bbbb57352f8b934a248fe825b1c0ea64ec4da6ce2575a66716a37657`. The apparent sign error and reciprocal-polynomial typo on printed page 5 need not be used.

Let P(z)=sum_{j=0}^{n-1} X_j z^j, X_j in {−1,1}, independently uniform. Let N count its zeros in the **open** unit disk, with multiplicity. Its constant coefficient is nonzero. Set

S(t)=sum_{j=0}^{n-1} exp(2jt), psi(t)=(1/2)log S(t),

J(t)=integral log|P(exp(t+i theta))| dtheta/(2pi), L(t)=J(t)−psi(t).

All these angular logarithmic integrals are finite, including when a root lies on the integration circle: each root contributes the locally integrable log of distance. There is no claim that the pointwise expected logarithm at theta=0 is finite.

The input, **precisely the stated angular-moment Lemma 1.3**, is, for ell=1,2, uniformly over r in [1−n^(−11/10),1+n^(−11/10)],

E[(integral log|P(r exp(i theta))/sigma(r)| dtheta/(2pi))^ell]
= (−gamma/2)^ell + O(n^(−1/2) log^2 n),

where sigma(r)^2=sum r^(2j). It follows by expanding the square that

E[(L(log r)+gamma/2)^2]=O(n^(−1/2)log^2 n).  (1)

No interchange of a pointwise divergent expected logarithm is involved.

Put delta=(1/10)n^(−11/10). For large n, exp(±delta) lie in the permitted r interval (for example exp(delta)−1≤2delta and 1−exp(−delta)≤delta). If pi_t(j)=exp(2jt)/S(t), direct differentiation gives

psi'(t)=E_{pi_t}[j], psi''(t)=2 Var_{pi_t}(j)≤(n−1)^2/2.

The last inequality is the elementary variance bound for a variable in [0,n−1]: Var(X)≤(n−1)^2/4. Thus the difference quotients

D_plus=(psi(delta)−psi(0))/delta,
D_minus=(psi(0)−psi(−delta))/delta

differ from psi'(0)=(n−1)/2 by at most delta(n−1)^2/4≤n^(9/10)/40. Once n^(9/10)≥20, each differs from n/2 by at most n^(9/10)/20. These are uniform deterministic bounds, with no expansion remainder to estimate.

For every polynomial P, Jensen's formula in logarithmic radius gives

J(t)=log|P(0)|+sum_roots max(0,t−log|alpha|).

This is a continuous, convex, piecewise linear function. At 0 its left derivative is precisely N, while its right derivative also counts unit-circle roots. Consequently

[J(0)−J(−delta)]/delta ≤ N ≤ [J(delta)−J(0)]/delta.  (2)

This remains valid when there are unit-circle roots; that case cannot be discarded here.

If N≥n/2+n^(9/10), (2) forces

L(delta)−L(0)≥(19/20)delta n^(9/10)=(19/200)n^(−1/5).

If N≤n/2−n^(9/10), the other inequality forces

L(0)−L(−delta)≤−(19/200)n^(−1/5).

By (1) and (a−b)^2≤2(a+c)^2+2(b+c)^2, the second moment of either difference is O(n^(−1/2)log^2 n). Applying Markov to the square and a union bound gives

Pr(|N−n/2|≥n^(9/10))=O(n^(−1/10)log^2 n)→0.

This proves the announced two-tail estimate **conditional on exactly the source's Lemma 1.3**, without any reciprocal polynomial or unjustified sign reversal. The slight integer degree/centering difference does not matter: for Hayman–Lingham Problem 4.15, H(z)=zP(z) has degree n, exactly one additional root at zero, and |N_H−n/2|≤n^(9/10)+1 outside o(2^n) choices. Every integer n is treated; no parity subsequence is used.

## Disposition boundary

This closes the identified local p5 deduction objection on its stated analytic input. The accounting proposal should remain held until the parent independently checks this derivation and decides whether its existing independent verification of Lemma 1.3 is sufficient. Do not convert this note into a claim that all 14 pages, all citations, the journal proof, or global firstness have just been independently verified. Do not produce a new publication: DOI 10.4064/sm201117-28-1 is an existing prior paper.
