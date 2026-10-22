# Nonnegative leading weights under the global side condition

14 October 2026. A corollary for the proposed remainder-free Hardy–Rellich antecedent. This does not replace the source's solution-dependent remainder or resolve the overall informal question.

## Statement

Fix $Q=n+2\geq4$ and $0<R\leq\infty$. Use the same Grushin geometry, original test class, and off-axis extended-integral convention as in the [nonnegative-potential theorem](NONNEGATIVE_RELLICH_CONVERSE.md). Suppose

\[
V\in C^2(0,R),\quad V\geq0,\qquad
W\in C^1(0,R),\quad W\geq0,
\]

and

\[
(Q-5)\frac{V(r)}{r^2}+3\frac{V'(r)}r-V''(r)\geq0
\qquad\text{for every }r\in(0,R).
\tag{1}
\]

Assume the full source-form core inequality

\[
\int_{B_R}V(\rho)\frac{(L_Gu)^2}{\psi}\,dz
\geq
\int_{B_R}\left[
W(\rho)+(Q-1)
\left(\frac{V(\rho)}{\rho^2}-\frac{V'(\rho)}{\rho}\right)
\right]|\nabla_Gu|^2\,dz
\tag{2}
\]

for every real $u\in C_c^\infty(B_R\setminus\{0\})$.

Then there is a strictly positive flux-classical solution on the entire fixed interval $(0,R)$ of

\[
(r^{Q-1}Vf')'+r^{Q-1}Wf=0.
\tag{3}
\]

The coefficient is one, and no endpoint conditions are added.

## Proof

The independently checked dichotomy in the [degenerate-weight addendum, Section 2](../pass1_audit/DEGENERATE_WEIGHT_ADDENDUM.md) applies to the global hypotheses $V\in C^2$, $V\geq0$ and (1): either $V>0$ everywhere or $V\equiv0$.

If $V>0$, the [regular-leading-weight theorem](NONNEGATIVE_RELLICH_CONVERSE.md) proves (3).

If $V\equiv0$, then $V'\equiv0$ and the left side of (2) is zero under the stated integral convention. The inequality becomes

\[
0\geq\int_{B_R}W(\rho)|\nabla_Gu|^2\,dz
\qquad(u\in C_c^\infty(B_R\setminus\{0\})).
\]

If $W$ were positive at one radius, continuity would provide an off-axis neighborhood on which $W>0$. A nonzero smooth compact test in that neighborhood has strictly positive gradient energy, contradicting this inequality. Thus $W\leq0$, and the assumed $W\geq0$ implies $W\equiv0$. Equation (3) is then identically zero and has the strictly positive flux-classical solution $f\equiv1$.

These two cases exhaust the hypotheses.

## Global versus near-zero scope

The side condition (1) is required on the entire interval for this corollary. It supplies the global dichotomy and rules out a leading weight that is positive near zero but vanishes elsewhere.

The near-zero-only extension in Section 6 of the regular theorem retains the original requirement $V>0$ on the entire interval. This corollary does not permit combining a merely near-zero side condition with arbitrary zeros of $V$ elsewhere.

The historical $Q=3$ core branch is not included in this corollary. All references to the core retain its status as an explicitly proposed solution-free formulation.

## Pinned proof and independent-review dependencies

- Regular theorem: NONNEGATIVE_RELLICH_CONVERSE.md, 11470 bytes, SHA-256 8df0b419df801b28918c2cbbcb776b8ddec9ab9ae91cfd1f76e8597f64ff6b6e.
- Independent acceptance of that theorem: NONNEGATIVE_RELLICH_ACCEPTANCE.md, SHA-256 97bbd16dbab85840db9156fd72fc66816159aef2df6c7be9594039ebd7d47aad; its separate audit manifest pins the supporting Hardy positivity proof.
- Dichotomy and zero-weight classification: DEGENERATE_WEIGHT_ADDENDUM.md, 3692 bytes, SHA-256 e87230321f98f219db6cf0528561c314045494c7b706cb77db3ec77bf197f09f.
- Independent check of that addendum: DEGENERATE_WEIGHT_REVIEW.md, 3864 bytes, SHA-256 f1c8d32c0b146bce56ac9c8404006322b464ed6f72f26db2244dc84a8fbca349.

These are mathematical argument and audit dependencies, not a claim of human peer review or novelty.
