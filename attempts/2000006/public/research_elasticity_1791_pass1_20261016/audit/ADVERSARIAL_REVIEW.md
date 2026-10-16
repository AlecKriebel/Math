# E-6322 pass 1: independent adversarial review

Date: 2026-10-16. Target: the complete frozen `RESEARCH_TARGET.md`, read in full before this review. Scope: all positive coefficient quadruples, arbitrary permitted smooth diffeomorphic full trace, full finite-energy comparison class, and an essential determinant lower bound over the entire domain.

## Verdict

**Accept the verified partial results with their stated hypotheses. Do not accept a proof or a counterexample to E-6322.** No unconditional large-data regularity estimate and no compliant degenerating full-class minimizer has been supplied. The pass does not resolve Ball's broader adequate-growth programme either.

The useful advances are legitimate full-class stress identities, a precise conditional regularity-to-positivity reduction, exact exclusions of several tempting singular cores, sharp energy-only examples distinguishing the boundary from the interior, and primary-source checks of the available invertibility theory. The restrictions below are part of acceptance.

## 1. Full comparison class and baseline

The independent-minors function

\[
\Phi(F,C,J)=a|F|^6+b|C|^3+cJ^2+dJ^{-2},\qquad J>0,
\]

extended by infinity for nonpositive \(J\), is convex and lower semicontinuous. The smooth allowed extension gives a finite-energy competitor. A minimizing sequence is bounded in \(W^{1,6}\), while its minors have the needed weak continuity in \(L^3\) and \(L^2\). The direct-method existence claim is valid and nonvacuous. This is known existence theory, not positivity.

For an affine full trace, the averages of all minors equal those of the affine gradient. Approximation for the null-Lagrangian identities does not require the approximants to preserve positive determinant. Jensen and strict convexity of \(a|F|^6\) prove that the affine map is the unique minimizer in the complete target class. All nonaffine identity-trace examples in the packet are consequently nonminimizers.

Replacing the complete class with radial maps, homeomorphisms, smooth maps, or a weak/strong closure of diffeomorphisms would change the problem. No reviewed accepted argument makes that replacement.

## 2. Variations: accepted identities and exact limits

The formulas for \(T=PF^T\), \(U=F^TP\), and \(E=WI-U\) have the correct left/right matrix ordering. The stated bounds \(|T|,|U|\le9W\) and \(|E|\le12W\) are valid for arbitrary positive coefficients. Exact outer and inner composition formulas, determinant preservation, trace preservation, and energy domination were checked independently.

The inner equation is

\[
\operatorname{div}\bigl(3dJ^{-2}I+Q(Dy)\bigr)=0,
\]

where \(Q\) contains only positive-degree terms and \(|Q(F)|\le C(a,b,c)|F|^6\). The baseline gives only \(Q\in L^1\). An \(L^1\) tensor source does not by itself supply bounded scalar pressure.

Ordinary additive variations and the integrability of \(P=DW(Dy)\) are not consequences of the safe identities. The radial examples establish the obstruction; the independent file `INDEPENDENT_OBSTRUCTION.md` gives the stronger elementary example \(y=(x_1,x_2,x_3|x|)\), which is a \(C^{1,1}\) homeomorphism with identity trace and finite energy, yet \(P\notin L^1\). This example is not a minimizer.

The inverse-coordinate algebra is also correct. It remains conditional on a separately established almost-everywhere inverse and change of variables. The algebraic inverse matrix field has the displayed \(9/5\), \(9/4\), and determinant-cubic integrability. Its definition does not establish that it is the weak derivative of an inverse, nor transfer minimality to every competitor for the inverse integrand.

## 3. Conditional positivity: the meaningful distinction

### 3.1 Energy alone

For nonnegative \(J\in C^{1,\alpha}\), an interior zero gives \(J(x)\le C|x-x_0|^{1+\alpha}\). Inverse-square integrability excludes it for \(\alpha\ge1/2\), including equality.

At a boundary zero, the correct estimate is instead \(J(z,t)\le C(t+|z|^{1+\alpha})\). In three dimensions the inverse-square integral necessarily diverges by this argument only at \(\alpha=1\). Thus \(J\in C^{1,1}(\overline\Omega)\), sufficiently \(y\in C^{2,1}(\overline\Omega)\), is an energy-only whole-domain positivity condition.

It is essential to name the regular object. **\(J\in C^{1,1}\) is not \(y\in C^{1,1}\).** The latter alone is insufficient, as the independent obstruction shows.

The interior rank-two examples and both boundary constructions pass the determinant, regularity, full-trace, and integrability checks. In the collar construction the choice \(\partial_t\chi\le0\) and \(h\le t\) gives

\[
\partial_t[t+\chi(h-t)]=(1-\chi)+\chi\partial_t h+(\partial_t\chi)(h-t)>0
\]

at every interior point. The logarithmic variant genuinely gives one map in every \(C^{2,\alpha}\), \(\alpha<1\), with a boundary-only zero and finite energy. The explicit closed-ball example in the exact lane separately verifies the same boundary phenomenon for a family of Hölder exponents.

### 3.2 Minimality plus additional regularity

The pressure reduction uses stationarity essentially and is stronger than the energy-only thresholds. If \(Q\in L^q\), \(1<q<\infty\), then the global negative-norm estimate on the bounded connected smooth domain gives

\[
\|3dJ^{-2}-(3dJ^{-2})_\Omega\|_{L^q}
\le C_{\Omega,q}\|Q\|_{L^q}.
\]

There is no circular assumption that the pressure is already in \(L^q\): the input \(J^{-2}\in L^1\) suffices. A direct proof tests with the Bogovskii right inverse of mean-zero compactly supported smooth scalar functions, then uses duality. No pressure boundary condition is needed. Breit–Cianchi's equation (1.2) states exactly this negative-norm theorem for initially \(L^1\) functions; Wichmann's Theorem 34 verifies the compact-support Bogovskii mapping property.

Consequently \(Dy\in L^{6q}\) transfers to \(J^{-2}\in L^q\). In particular bounded gradient gives every finite inverse-Jacobian moment. If a minimizer is \(C^{1,\beta}\) on the entire closure for any \(\beta>0\), then \(J\) is Hölder continuous there. At a hypothetical zero, \(J\le Cr^\beta\); choose finite \(q\) with \(2q\beta\ge3\). The interior ball or boundary cone makes \(J^{-2q}\) nonintegrable, a contradiction. Compactness then supplies a positive minimum.

This conditional theorem is accepted. It does not supply its own regularity premise. Bare Lipschitz continuity of the deformation, finite higher moments alone, or regularity only on compact interior subsets does not give the frozen global conclusion. No novelty claim is certified.

## 4. Singular-core exclusions and examples

The homogeneous-core replacement lemma is valid for exact cores

\[
y(x_0+r\theta)=y_0+r^\alpha\phi(\theta),\quad1<\alpha<3/2,
\]

whose degree-one homogeneous cone has a continuous strictly positive angular Jacobian. The replacement \(R^{\alpha-1}r\phi(\theta)\) has matching spherical trace, belongs to the full class, and converges strongly to the original deformation in \(W^{1,6}\). Its strict barrier gain has order \(R^{9-6\alpha}\), whereas the positive-degree cost has order \(R^{6\alpha-3}\). The sign and exponent comparison are correct. This rules out those exact cores even with unrelated nonaffine outer data.

An additional simple exclusion applies whenever the trace on a small sphere is affine: affine replacement is strictly better by the full-class Jensen result. In particular the explicit rank-two and coordinatewise-power radial cores are not rescued by changing the outer trace. This is not an exclusion of all anisotropic asymptotic behaviour.

The exact lane's radial energy, quadratic energy-gap expansion, annular descent residual, rank-two gradient/cofactor formulas, axis nonstationarity, boundary determinant, and homogeneous-core coefficients were checked. The collapsed-segment example has the correct cylindrical integrability window \(2/3<\alpha<1\) and demonstrates failure of everywhere injectivity within the admissible class. A collapsed null fiber is compatible with almost-everywhere injectivity.

The quantifier ambiguity in the exact lane's preliminary summary was corrected: its elementary Hölder examples form a family, with one example for each exponent. The separate logarithmic construction does supply a single example for all sub-Lipschitz exponents.

## 5. Source and invertibility audit

The full smooth diffeomorphic trace supplies degree one on \(G(\Omega)\) and zero off its closure. Krömer's Theorem 6.1 therefore applies directly to all target competitors, including domains with holes. Its result is almost-everywhere injectivity and change of variables, not a homeomorphism or a Jacobian bound. Corollary 6.5's two-component topological hypothesis must not be silently substituted for the direct degree argument.

The energy gives \(K_O\in L^1\) and \(K_I^{1/2}\in L^1\) by the displayed Hölder estimates. These do not meet Krömer's Theorems 6.8 or 6.10. Traver's 2026 terminology likewise expressly allows exceptional squeezed fibers. Titles containing “global invertibility” cannot be promoted to everywhere invertibility.

The source audit distinguishes two-dimensional classical/interior estimates, near-affine existence results, proper restricted minimization classes, double-cover traces, no-barrier models, higher-gradient energies, and higher-codimension singular minimizers from this benchmark. The bounded literature search found no verified matching resolution; absence from that search is not proof of novelty or of the complete current literature status.

Primary passages independently inspected in this audit:

- Ball (2002), Theorem 2.1, Problem 6, equations (2.19), (2.21)–(2.22), and Theorem 2.3: https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf
- Krömer, arXiv:1912.11086v2, Theorems 6.1, 6.8 and 6.10; printed p.27 also visually inspected: https://arxiv.org/pdf/1912.11086v2
- Traver, arXiv:2507.07206v2, definition (1.1), Theorem 1.2 and Corollary 1.3; printed p.2 also visually inspected: https://arxiv.org/pdf/2507.07206v2
- Benešová–Kružík–Schlömerkemper, arXiv:1706.04055v5, Propositions 5.1 and 5.4 and their derivative-of-minor hypotheses: https://arxiv.org/pdf/1706.04055v5
- Guerra–Tione, arXiv:2609.32404v1, Theorem 1.2, specifically dimension, codimension, density and minimization class: https://arxiv.org/html/2609.32404v1
- Breit–Cianchi, arXiv:1401.4885v2, equations (1.1)–(1.2), including the initial \(L^1\) hypothesis: https://arxiv.org/pdf/1401.4885v2
- Wichmann (2024), Appendix A, Theorem 34, and the distributional pressure duality in Lemma 15: https://link.springer.com/article/10.1007/s00021-024-00852-9

These are theorem-hypothesis/source checks and independent verification of the packet's deductions, not complete new proofs of every external theorem. The original Ball (1981), Bauman–Phillips–Owen maximal-smoothness paper, and Zhang full text remain outside the full-text verification claim.

## 6. Reproducibility and stopping boundary

The exact-lane script was rerun: all 13 symbolic and 11 quadrature checks passed. The counterexample scaling script and positivity formula script were rerun successfully. `verify_audit.py` additionally performs 54 exact left/right matrix-direction checks, verifies the triangular cofactor and Piola component, and verifies the homogeneous barrier-gain factorization. Results are in `AUDIT_CHECKS.json`. Computation supplements the written arguments; it is not a certificate of general minimality.

The final input byte counts and hashes are recorded in `AUDIT_MANIFEST.json`. Acceptance attaches to those inspected versions. This review made no publication, commit, push, external communication on the user's behalf, or change to the frozen target.

**Unresolved next step:** prove an unconditional global regularity/integrability/comparison statement strong enough to eliminate low-Jacobian sets for actual large-data minimizers, or construct and certify a compliant full-class minimizer with essential determinant infimum zero. None of the accepted conditional statements or admissible-only examples reaches that step.
