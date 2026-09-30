# Independent review of the bounded-switch ball-product proof

**Verdict: PASS for the full stated PL homeomorphism.** No substantive mathematical gap was found in the frozen proof. The original question concerns the entire bounded-switch complex, and the argument reaches that conclusion for every stated parameter, rather than only identifying its homology or boundary. No mathematical revision is required by this review.

**Target:** 30001696 / OWR-4798-013.  
**Reviewed document:** `PROOF.md`.  
**Originally reviewed SHA-256:** `1a71f296c2ab4a1ad3670b993d275e8ef87e9f81ffe5f094c00a33bcf57990da`.  
**Final reviewed SHA-256:** `58809f3edaa2930f1111ba823b1ce50c8e328dd8388b2e19323600ede3d04305`.  
**Date:** 30 September 2026. **Reviewer model:** gpt-6-astra, xhigh.

This is an independent AI mathematical review, not human peer review or formal verification. The proof remains unrefereed. Historical priority is not established by this review or by the bounded literature search described below.

## Source scope and dependencies

Question 4 in Steven Klee's contribution to [Oberwolfach Report 08/2011](https://doi.org/10.4171/owr/2011/08), printed p. 372, asks whether the full complex is a combinatorial triangulation of the sphere–ball product. The preceding pages define it using at most $i$ consecutive sign switches, with $0\leq i\leq d-1$. The candidate uses exactly this convention. The endpoint $i=d-1$ is the whole cross-polytope boundary; the substantive argument treats $0\leq i\leq d-2$.

[Klee–Novik](https://arxiv.org/abs/1102.0542), Definition 3.1, Theorem 1.2 and Section 4, establishes the quoted manifold, homology and boundary statements, and the ball-product cases $i=0,1$. In particular, the existing boundary theorem is not a proof of the stronger interior classification. The candidate does not use that mistaken inference.

The two external results actually needed for the new argument have the required strength:

- [Margaliot–Sontag, Theorem 3](https://www.sontaglab.org/FTPDIR/margaliot_sontag_totally_positive_automatica2019.pdf), printed p. 4, states the strict zero-sensitive inequality $s^+(Ax)\leq s^-(x)$ for a totally positive square matrix and every nonzero real vector. Their terminology requires every minor to be positive. [Schwarz, Theorems 3–4](https://msp.org/pjm/1970/32-1/pjm-v32-n1-p20-s.pdf), corroborates the tridiagonal flow and variation facts, using older terminology.
- [Hardt–Lambrechts–Turchin–Volić, Theorem 2.6](https://arxiv.org/pdf/0806.0476), states the semialgebraic Hauptvermutung for compact semialgebraic sets: two polyhedra semialgebraically homeomorphic to such a set are PL-homeomorphic. It cites Shiota–Yokoi, Corollary 4.3. This has no dimension or simply-connectedness restriction. The original Shiota–Yokoi article was not needed to reconstruct an additional argument: the precise cited theorem was checked in the later primary paper.

## Realization and the behavior at zero coordinates

A face of the cross-polytope is contained in an allowed facet exactly when its nonzero signs have at most $i$ changes. Filling any runs of zero coordinates between equal signs without changes, and those between opposite signs with one change, proves that the minimum over completions is $s^-$. Radial normalization from the polyhedral sphere therefore gives exactly the candidate's set $C_i$.

The interior characterization by $s^+\leq i$ is also correct. Near a fixed nonzero vector, the existing nonzero signs are fixed, and the zero coordinates can independently receive either sign. Every full completion is realized by nearby points on the round sphere. Hence a forbidden completion prevents interior membership, while the absence of any forbidden completion supplies an entire neighborhood. This handles sparse vectors and multiple adjacent zeros; it does not assume that boundary points have just one zero.

Closedness follows by persistence of a forbidden alternating nonzero subsequence. Thus $C_i$ is compact. Both its ambient-sphere interior and its ambient-sphere boundary are semialgebraic, since the relevant conditions are finite unions of sign strata. None of these deductions assumes the desired product topology.

## The spectral flow

The detailed-balance identity has the correct direction for $J=DLD^{-1}$. On a degree-$k$ monomial, the degree-$k+1$ terms cancel and the leading degree-$k$ coefficient is $N-2k$. Evaluation of polynomials of degree at most $N$ at $N+1$ distinct nodes is an isomorphism. Consequently the triangular polynomial calculation gives the complete simple spectrum and an eigenvector of exact degree $k$ for every eigenvalue. Symmetry then provides the orthogonal splitting used later.

The compound-matrix proof of strict total positivity is valid. In the increasing wedge basis, a nonzero off-diagonal coefficient replaces one occupied index by an adjacent unoccupied index. There is no interchange of indices, so its sign is positive. The graph of such moves is connected for every proper nonzero exterior power: one can successively move the ordered occupied positions to $0,1,\ldots,k-1$. Therefore each additive compound is irreducible and Metzler. Adding a sufficiently large scalar identity produces a nonnegative irreducible matrix; a finite positive path gives a positive term in the exponential series for every entry. The full determinant is positive separately. This proves positivity of all minors, including the nonprincipal ones required by the variation theorem.

The time convention is correct. With $a=e^{-2t}$, multiplication by $e^{tJ}$ differs from $M_a$ by the common positive scalar $e^{Nt}$. Thus positive time corresponds to $0<a<1$. The strict variation theorem puts every forward image of $C_i$ in its ambient interior. This strict interior statement, rather than mere preservation of $C_i$, is what makes the later hitting function continuous.

## Separation of the two spectral spheres

For the low spectral space, the divided-difference argument proves the claimed bound even at zero coordinates. If a completion had $r$ changes, choose $r+1$ alternating nodes. The denominator signs in the order-$r$ divided difference alternate too, so every nonzero summand has the same sign. A polynomial of degree at most $r-1$ cannot vanish at all these nodes, yet its order-$r$ divided difference is zero. This is the required contradiction. Positive binomial square-root factors do not change signs.

For the high spectral space, insert one root between successive opposite-sign nonzero blocks of a putative vector with at most $r-1$ changes. A polynomial of degree at most $r-1$, with an appropriate overall sign, agrees strictly with all its nonzero signs. The corresponding low spectral vector has a strictly positive inner product with it, contradicting orthogonality. Zeros between blocks cause no difficulty, since roots can be placed between the last nonzero coordinate of one block and the first of the next.

Hence the whole low spectral sphere lies in the interior, and the high spectral sphere is disjoint from $C_i$. Compactness makes both separation statements uniform. The argument does not classify an arbitrary sphere embedding: these are the spheres of two explicit orthogonal linear subspaces.

## Global orbit coordinates and the hitting graph

The squared ratio of the high to low component norms is a quotient of sums of the form $\sum a^{2k}c_k^2$. Its logarithmic derivative is twice the difference of two weighted averages. All high indices exceed all low indices, so the logarithmic derivative of the unsquared ratio is between $1$ and $N$. This proves strict monotonicity, both limiting values, and the direction of both inequalities (5.3). In particular every orbit with both components nonzero meets the equal-norm cross-section exactly once.

The inverse orbit coordinates are continuous. For a fixed point, parameters just below and above its unique equal-norm parameter give ratios on opposite sides of one. These strict inequalities persist under a small change of the point and bracket its new parameter. The orbit-coordinate map and its inverse are semialgebraic: $M_a$ has integer powers of the positive parameter, all projection matrices have algebraic entries, and normalization uses a positive square root. Swapping factors in the graph of the bijective semialgebraic map supplies the graph of the inverse.

For each section point, sufficiently small parameters lie in $C_i$'s interior and sufficiently large parameters lie outside $C_i$. The uniform ratio estimates and compact spectral-sphere separation justify these assertions; convergence to a single fixed direction is not required. Strict trapping makes membership a lower interval, closed at its finite positive upper endpoint. Any point strictly below that endpoint is interior. Thus the endpoint is the unique boundary point on that orbit.

The continuity proof for the endpoint is sufficient: an interior lower bracket and an exterior upper bracket persist after perturbing the section point. Its graph is the inverse image of the semialgebraic boundary, so it is semialgebraic. The section is compact, including when one sphere factor is zero-dimensional, and the positive continuous hitting function consequently has a strictly positive minimum and a finite maximum.

## Extension across the core and the product identification

This is the most important potential failure point, and the proposed cutoff resolves it. A constant orbital rescaling by the hitting time would not alone justify continuity at the entire low spectral sphere, whose internal spectral dynamics is nontrivial. The actual map instead fixes all orbit parameters below one uniform positive cutoff.

For a section point and an orbit parameter in $[\epsilon,1]$, the ratio estimate gives $R\geq\epsilon^N$; for parameters at least one it gives $R\geq1$. Therefore $R<\epsilon^N$ forces the parameter to be less than $\epsilon$. The straightening map is exactly the identity on this neighborhood of the core. Its inverse fixes the same neighborhood: monotonicity of each piecewise-linear parameter map gives $h_s(a)\leq\epsilon$ exactly when $a\leq\epsilon$. Continuity in both directions follows without any assumption about pointwise limiting spectral directions.

Away from the core, the map is a continuous semialgebraic bijection in the global orbit coordinates. On each orbit it maps the closed hitting endpoint to parameter one, and it has no missing or identified points. The map consequently identifies $C_i$ with the standard norm-ratio neighborhood $D_E$. Formula (7.4) and its displayed inverse are correct and have nonzero denominators. They identify this neighborhood with $S(E)\times D(F)$, with dimensions $i$ and $d-i-1$ as claimed. The boundary is carried to the sphere factor in the closed ball.

For $i=0$, the core sphere is two points and the result is two balls. For $i=d-2$, the high sphere is two points and the result is a sphere times an interval. The section may be disconnected in these cases, which does not affect compactness, continuity or the uniform cutoff. The minimal case $d=2,i=0$ works as written. The separately handled full-boundary case $i=d-1$, including $d=1,i=0$, is immediate.

## The PL conclusion

The construction yields a semialgebraic homeomorphism, not merely a topological homeomorphism. The original realization is a finite compact polyhedron. Standard polyhedral sphere and ball models in the two linear subspaces have semialgebraic radial homeomorphisms to their round models, and their product has a finite standard PL triangulation. Thus both polyhedra are semialgebraically homeomorphic to the same compact set. All hypotheses of the semialgebraic Hauptvermutung are satisfied.

The theorem supplies a PL homeomorphism; it need not say that the explicitly constructed map is itself piecewise linear. That distinction does not weaken the requested existence conclusion. No high-dimensional manifold classification, smoothability assumption, or claim that every topological homeomorphism is PL has entered the argument.

## Independent checks and priority limits

`independent_checks.py` uses SymPy 1.14.0 and exact integer/rational arithmetic. It passed **20,326 assertions**. It independently reconstructs the rational conjugate of the flow, tests its characteristic polynomial, projectors and inverse, and checks every minor at two positive-time parameters in dimensions 2–6. It exhausts every nonzero ternary sign pattern in these dimensions, including all zero completions, and checks the strict variation inequality. Further cases cover polynomial vectors with forced zeros, samples in the repelling subspace, ratio derivatives and uniform bounds through dimension eight, and both pieces of the cutoff and its inverse. The accompanying receipt records the script hash and category counts. Reproduce from this directory with `python independent_checks.py`.

These checks are finite diagnostics; they do not certify the general topological theorem. The general verdict rests on the preceding mathematical audit.

The bounded literature check included the original report, Klee–Novik, [Machacek's manifold and collapse results](https://arxiv.org/abs/1909.04640), [Galashin–Karp–Lam's contractive-flow method](https://arxiv.org/abs/1707.02010), and [Wang–Zheng's 2019 account of related sphere triangulations](https://www.mat.univie.ac.at/~slc/wpapers/FPSAC2019/18.pdf). Machacek's Theorems 3.4 and 3.6 identify a manifold and its homotopy type in the projective quotient, and the latter article records the known low-$i$ ball-product cases. These are consistent with the candidate but do not themselves state its all-parameter product homeomorphism. Searches on the complex notation, bounded sign variation and ball/disk-bundle terminology did not locate an earlier complete proof. This is not an exhaustive priority determination, and the candidate's explicit novelty qualification should remain.

## Final status-header verification

The final document differs from the originally reviewed document only in its status line, which now records that independent adversarial AI review passed. Replacing that one line by its former text reproduces the original SHA-256 exactly. The mathematical text and references are unchanged, and the PASS verdict covers the final hash stated above.
