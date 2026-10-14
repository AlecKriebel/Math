# Independent acceptance audit: regular Grushin Hardy converses and a Hardy–Rellich core counterexample

14 October 2026. Authored mathematical audit of the shared PASS1 work. This is a proof audit of the exact artifacts pinned in `AUDIT_MANIFEST.json`, not a human peer-review or scholarly-novelty claim.

## Verdict and limits

**Accepted, with the exact scope below.**

1. For every historical dimension \(n\ge1\), \(Q=n+2\), every fixed \(0<R\le\infty\), \(V\in C^1(0,R)\) strictly positive and real \(W\in C^1(0,R)\), each of the two source all-test Hardy inequalities separately forces a positive flux-classical solution on all of \((0,R)\) of
   \[
   (r^{Q-1}Vf')'+r^{Q-1}Wf=0.
   \]
   The coefficient is exactly one. In fact, both all-test inequalities, their common radial one-dimensional form, and this positive-solution property are equivalent.
2. For the proposed remainder-free Hardy–Rellich core, the corresponding necessity assertion is false in the unrestricted real-\(W\), regular-leading-weight class. The exact example \(Q=5,V=1,R=e^{12},W=\lambda/r^2-r^{-4}\), with \(\lambda\) defined variationally in the audited proof, satisfies the full original all-test core and \(S_5[V]=0\), while its coefficient-one Bessel equation has no positive full-interval solution.
3. The separate elementary examples disprove the literal Hardy converse allowing \(V=0\) and negative \(W\). The isolated-zero example uses the explicitly stated flux-classical convention. These examples do not negate the strictly positive-leading-weight theorem.

These conclusions do not settle every interpretation of the informal Oberwolfach question. In particular, the Hardy–Rellich core is an explicitly proposed replacement of a solution-dependent source display. The historical \(Q=3\) Hardy–Rellich branch, an independently imposed \(W\ge0\) restriction, and the stronger independent-positive-function remainder premise are not resolved by these accepted results. No all-dimension classification is inferred from the single admissible \(Q=5\) counterexample.

## 1. Exact Hardy geometry and test classes

The polar chart
\[
x=r\sqrt{\sin\varphi}\,\omega,\qquad t=r^2\cos\varphi/2
\]
has Jacobian
\[
dz=\tfrac12r^{Q-1}(\sin\varphi)^{(n-2)/2}\,dr\,d\varphi\,d\omega.
\]
Thus \(\psi dz=\tfrac12r^{Q-1}(\sin\varphi)^{n/2}\,dr\,d\varphi\,d\omega\). Independent differentiation verifies the factor \(1/2\) and the common positive radial constant
\[
c_n=\frac{|S^{n-1}|}{2}\int_0^\pi\sin^{n/2}\varphi\,d\varphi.
\]
For \(n=1\), \(S^0\) has counting measure and both angular exponents are integrable. This argument does not invoke the newer source's dimension-restricted angular spectral theory.

The source radial derivative is exactly
\[
u_\rho=\rho^{-1}(x\cdot\nabla_x+2t\partial_t)u.
\]
Off the axis,
\[
\nabla_Gu\cdot\nabla_G\rho=\psi u_\rho.
\]
Consequently the gauge-gradient projection agrees with the source radial derivative after division by \(\psi\); it has not been substituted for an unrelated radial derivative. Cauchy–Schwarz yields \(\psi|u_\rho|^2\le|\nabla_Gu|^2\). At the axis the same inequality holds directly because its left side is zero.

If \(v\in C_c^\infty(0,R)\), then \(v\circ\rho\) is an admissible original spatial test: \(\rho\) is smooth at all nonzero points, including the nonzero axis. Radial restriction of either Hardy premise therefore yields exactly the same one-dimensional form, with the same factor on both sides. Conversely the one-dimensional form applies ray by ray to every spatial test, whose radial support lies in a common compact interior interval. All needed integrals are finite, including in \(Q=3\). This validates the all-test versus radial-test relationships rather than conflating them.

## 2. Full-interval positivity at coefficient one

The audited one-dimensional argument is complete under \(p>0\), \(p\in C^1\), real continuous \(q\), with no endpoint conditions. The crucial steps were independently checked:

- Local Sobolev approximation extends nonnegativity from smooth compact tests to compactly supported \(H^1\) functions.
- A solution with two interior zeros, truncated to that interval, has zero form energy. Polarization then forces its boundary fluxes to vanish. Initial-value uniqueness contradicts a nonzero solution. Merely citing nonnegative Dirichlet energy would not have sufficed; the proof supplies this missing implication.
- Shooting from interior points \(a_j\downarrow0\) with positive initial flux produces solutions positive on the entire \((a_j,R)\), not just on a compact annulus.
- Normalization at one interior point and comparison at two nearby fixed points bound the initial fluxes. A single convergent initial-flux subsequence determines a global solution through fixed fundamental solutions. No incompatible collection of annular limits is used.
- Its limit is nonnegative everywhere and equals one at the normalization point. An interior zero would have zero derivative and force the solution to vanish identically. Hence it is strictly positive everywhere on the full fixed interval.

The equation is never rescaled in \(q\) or shifted by a spectral parameter. Endpoint values of the approximating solutions are not imposed on the limiting solution. The ground-state identity used for sufficiency is integrated only on compact interior supports.

## 3. The Hardy–Rellich constrained gap is real

For \(R=e^{12}\), let \(\mathcal H\) be the completion of compact smooth tests for
\[
q_0[w]=\int_0^R(r^4w'^2+w^2),\qquad N[w]=\int_0^Rr^2w^2,
\qquad m[w]=\int_0^Rw.
\]
The exact thresholds are \(\alpha=\inf q_0/N\) and \(\beta=\inf_{m=0}q_0/N\). The audit verifies:

- \(N\le R^2q_0\) makes the embedding continuous; its near-zero tail is bounded by \(\delta^2q_0\). Local compactness on \([\delta,R]\) then proves compactness on the entire interval.
- \(|m[w]|\le\sqrt R\,q_0[w]^{1/2}\). Thus the mean-zero constraint is a genuinely closed codimension-one condition.
- Both infima are attained by weak compactness and the compact weighted inclusion.
- The unrestricted nonnegative minimizer is a strictly positive classical solution on every interior interval. Initial-value uniqueness proves strict positivity. Polarization of the nonnegative form \(q_0-\alpha N\) shows its nullspace is linear; two independent null vectors would have a combination vanishing at an interior point, contradicting the preceding positivity argument. Hence this space is one-dimensional.
- This ground state has positive ordinary mean. An attained mean-zero minimizer cannot attain the same threshold, so \(\beta>\alpha\).

The logarithmic sine trial establishes
\[
\alpha\le9/4+\pi^2/100+e^{-4}<19/8<12/5.
\]
This bound has an exact elementary certificate: \(\pi^2<10\) and the first eight terms of \(e^4\)'s series sum to \(16319/315>50\), so the displayed upper bound is less than \(237/100<19/8\). No numerical eigenvalue is needed.

It follows that
\[
\lambda=(\alpha+\min\{\beta,12/5\})/2
\]
is a well-defined exact real number with \(\alpha<\lambda<\beta\) and \(\lambda<12/5\). The Hardy form is \(q_\lambda=q_0-\lambda N\). It is nonnegative on mean-zero functions and negative on the unrestricted ground state. Approximation in the defining \(q_0\) norm produces an actual negative compact smooth test. This last passage is essential: a negative value only on a formal singular function would not refute the requested Bessel property.

A hypothetical positive coefficient-one Bessel solution would give the compact-support ground-state identity and forbid this negative test. Therefore the claimed failure of full-interval positivity is established without imposing endpoint conditions on that hypothetical solution. The form completion is a construction device for the example, not a change to the source test class or to the target solution convention.

## 4. All-size angular comparison and the axis

For \(Q=5\), the source angular spectrum is \(a_k=k(k+3)\), including every multiplicity; \(a_0=0\) and \(a_k\ge4\) for \(k\ge1\). Direct expansion and integration by parts independently give the exact mode difference
\[
F_a[d]=q_\lambda[d']+
 a\left(2\int r^2d'^2+(a-2-\lambda)\int d^2+\int r^{-2}d^2\right).
\]
The factor \(4/r^2\) on the original right side is indispensable for this formula and is present in the proof. Each coefficient \(d\) is smooth with compact radial support, so \(\int d'=0\) and \(q_\lambda[d']\ge0\).

The exact identity
\[
\int(rd'+d/2)^2=\int r^2d'^2-\tfrac14\int d^2
\]
shows that the brace is bounded below by
\[
(a-3/2-\lambda)\int d^2+\int r^{-2}d^2.
\]
For every nonconstant mode this is positive unless \(d=0\), since
\(a-3/2-\lambda>4-3/2-12/5=1/10\). This is an all-size argument, not a finite mode search. The zero mode is covered by the constrained form directly.

No axis is removed. For every original smooth compact test in \(\mathbb R^3\times\mathbb R\), \(L_Gu\) is bounded on its compact support and \(1/\psi=\rho^2/|x|^2\). The singularity \(|x|^{-2}\) is locally integrable in three horizontal dimensions, so every original test has finite left energy. The final proof avoids imposing an angular boundary condition: the angular eigenfunctions become Cartesian-smooth homogeneous polynomials after multiplication by powers of the gauge. Ambient integration by parts identifies the angular coefficients of L_Gu/psi. Parseval then gives left-energy and weighted-L2 convergence of the finite angular sums. Ambient integration by parts and weighted Cauchy–Schwarz give convergence in gradient energy as well. The signed right side converges because its radial multiplier is bounded on the common compact support. Nonnegative finite-sum differences therefore pass to the original test.

The all-test example therefore does not rest on a radial-only implication, an unproved finite-energy density assertion, or a change of angular boundary conditions.

## 5. Endpoint capacity: rejected shortcut and accepted obstruction

The tempting inference from \(q[d']\ge0\) to \(q[w]\ge0\) for arbitrary compact \(w\) is invalid without a mechanism removing \(\int w=0\). Here the side condition \(S_5[1]=0\) permits small leading derivative energy for an endpoint correction, but \(W\)'s negative term contributes \(+\int w^2\). The mean is continuous in this full form topology and its kernel is closed. Consequently the missing mean cannot be repaired at arbitrarily small full cost.

The variational gap proves a genuine counterexample, rather than merely identifying a gap in one proof strategy. No conclusion about nonnegative \(W\) follows from this example, whose \(W\) is negative near zero.

## 6. Reproducibility and sources

`check_audit.py` supplies an independent exact-arithmetic certificate for the trial bound and a smoke check of the mode coefficient. Normal, `-O`, and `-OO` executions produce identical `EXACT_CHECKS.json` bytes. Explicit exceptions keep checks active under optimization. The finite loop is supplementary; the universal mode inequality is the monotonic argument in Section 4. The author's finite-difference diagnostics are also supplementary and do not define \(\lambda\).

Public primary sources used to align the audit:

- Roychowdhury's contribution to *Mini-Workshop: Hardy Inequalities in Discrete and Continuum Settings*, Oberwolfach Reports 14/2025, printed p.606: [official report](https://ems.press/content/serial-article-files/51358?nt=1).
- Ganguly–Jotsaroop–Roychowdhury, *Hardy and Rellich identities and inequalities for Baouendi-Grushin operators via spherical vector fields*, v3: Theorem 1.3, Section 2, Corollary 3.1, and the relevant mode computations: [versioned PDF](https://arxiv.org/pdf/2404.05510v3).
- Historical GJR v1, for its \(Q\ge3\) Hardy scope and the different source-version range: [versioned PDF](https://arxiv.org/pdf/2404.05510v1).

The manifest records exact author-artifact and public-source byte/hash pins. It contains no copied source document, dataset content, private personal data, or private coordination material. Changes to the pinned proofs require re-audit of the changed content.
