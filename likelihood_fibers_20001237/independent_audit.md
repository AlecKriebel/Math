# Independent mathematical audit: AIM-COMPUTATION-0075

Audit date: 2026-10-21. Scope: mathematical consistency and source attribution, not novelty certification or a solution of the historical general problem. 

## Independent calculations

For 2×2 independence, write N=Σu, r=u11+u12, c=u11+u21. The normalized likelihood-open model is p=(ab,a(1−b),(1−a)b,(1−a)(1−b)), with a,b outside {0,1}. Its critical equations are r−Na=c−Nb=0. At N≠0, a valid point exists exactly when r(N−r)c(N−c)≠0. At N=0 the fiber is empty unless r=c=0, in which case it is the whole two-dimensional model open. These equations concern the differential of log likelihood for arbitrary complex data; an actual single-valued monomial likelihood needs integral exponents, but the checkerboard u=(1,−1,−1,1) supplies such an example.

The expected-count model instead has q=(t,r−t,c−t,N−r−c+t) and determinant Nt−rc. Its affine fibers are a point for N≠0, empty for N=0 and rc≠0, and a line for N=0 and rc=0. On each such line the four cell coordinates are nonzero linear polynomials in t, so the cell-torus part is nonempty and dense. This does not imply any normalized critical point: q=Np is invertible only after inverting N.

For m×n rank-at-most-one expected-count matrices with m,n≥2 and prescribed row/column vectors R,C having common total N:

- N≠0: the unique affine matrix is RCᵀ/N. It is in the cell torus exactly when every component of both margins is nonzero.
- N=0, R≠0 and C≠0: empty.
- N=0, R≠0 and C=0: q=Rvᵀ with Σv=1, an affine space of dimension n−1. Its cell-torus part is nonempty exactly when every R_i is nonzero.
- N=0, R=0 and C≠0: the transpose case, dimension m−1, with the analogous nonzero-margin criterion.
- N=0, R=C=0: the rank-at-most-one cone in the tensor product of the two sum-zero subspaces, dimension m+n−3. Its cell-torus part is nonempty over C: each sum-zero subspace of dimension at least one contains a vector with all coordinates nonzero.

Proof: factor each nonzero rank-one matrix as xyᵀ, so R=xΣy, C=yΣx, and N=(Σx)(Σy). The zero matrix occurs only in the last case; choosing bases of the sum-zero subspaces identifies that last fiber with the usual rank-one determinantal cone of format (m−1)×(n−1).

Normalized m×n independence has critical equations R=Nα, C=Nβ, with Σα=Σβ=1 and all components nonzero. At N=0 its valid critical fiber is the full model open, dimension m+n−2, precisely when R=C=0; otherwise it is empty. These are statements about model points, not redundant parameter fibers.

## Projective closure check

Under the Segre parametrization p_ij=x_i y_j, the 2×2 projective likelihood correspondence is the incidence locus

r x1−(N−r)x0=0,    c y1−(N−c)y0=0.

At N=0 and r,c≠0 its fiber is the single point ([1:−1],[1:−1]); at N=r=0,c≠0 it is P¹×{[1:−1]}; symmetrically for N=c=0,r≠0; at N=r=c=0 it is all P¹×P¹. At N≠0 both factors are unique, though coordinate-zero boundaries can occur.

To check that this incidence locus has no extra component, work first over affine statistic space (N,r,c). The two incidence equations, linear in these statistics, have coefficient rank two except when x0+x1=y0+y1=0, where they have rank one. The rank-one stratum has total dimension two; every component of the two-equation locus in the smooth ambient fivefold has dimension at least three. The rank-two locus is an irreducible line bundle over the complement of one point in P¹×P¹. Thus its closure is the whole incidence locus set-theoretically. Pullback to the full affine data space adds a free kernel coordinate, and projectivization in nonzero data gives the claimed correspondence. The valid open additionally requires x0x1y0y1(x0+x1)(y0+y1)≠0. Hence all the N=0 fibers except the all-statistics-zero case disappear on that open.

## Saturation and specialization

Specialization need not commute with saturation. For I=(x−t) in C[t,x] and D=x, I:D^∞=I. Specializing t=0 gives (x), whereas first specializing I and then saturating by x gives the unit ideal. The specialized global closure therefore has a boundary point although the valid open fiber is empty. Re-localizing after specialization removes it correctly.

For a prescribed polynomial system I and excluded product D, use I+(zD−1). Base change of this affine scheme gives exactly the desired open fiber, including its scheme structure; the auxiliary z is uniquely determined and does not change dimension. This avoids falsely treating global saturation as a uniform boundary removal on every specialized closure fiber. Inverting a data factor N is an additional restriction of the base, not a consequence of excluding p+=0.

## General toric and algorithmic scope

For a homogeneous toric model with 1 in the row span of A, on its smooth cell torus and with p+≠0, normalized critical equations are Au=N Ap. In particular N=0 gives either all valid model points when Au=0, or none. This follows by pulling back the log-likelihood differential to a torus parametrization. Kernel data must not be discarded by projectivizing Au. This does not classify exceptional fibers with N≠0 for arbitrary A.

For a fixed finite polynomial family over an effective field, comprehensive Gröbner stratification of I+(zD−1) can determine empty, zero-dimensional, and positive-dimensional fibers. This is standard algorithmic existence, not a new explicit structural classification. Fiber dimension is constructible over a finite-type parameter base; without properness the jump set need not be closed. Proper compactification can introduce boundary fiber components.

## Primary-source checks and attribution

Barnhill–Cobb–Faust, *Likelihood Correspondence of Toric Statistical Models*, arXiv:2312.08501v3, §3 Theorems 3.1–3.2 and Corollary 3.5, supplies the saturated toric likelihood ideal and explicit complete/joint-independence Gröbner bases. This directly covers the relevant framework, so the independence formulas or ideal computations must not be advertised as new. Generic ML degree one is established prior art and does not rule out exceptional positive-dimensional complex fibers. Source inspected: https://arxiv.org/html/2312.08501v3 . The source gate separately records its ISSAC 2026 publication at https://doi.org/10.1145/3815436.3815479 .

Stacks Project §37.30, especially Lemmas 37.30.3 and 37.30.5, supports constructibility and proper upper semicontinuity: https://stacks.math.columbia.edu/tag/05F6 . The finite-type base assumption here avoids upgrading a merely locally constructible statement on an arbitrary base.

For nonnegative observed data, N=0 forces u=0. For positive total and positive margins the independence MLE is unique and interior, even if individual observed cells vanish. Complex zero-total examples do not contradict this. Sampling zeros, structural zeros, coordinate boundary points, discriminants, and positive-dimensional valid fibers are distinct concepts.

## Draft disposition

The full report.md draft was read and independently approved within its stated acceptance scope. No substantive correction was required. The global reducedness assertion for the 2×2 incidence also checks locally: near the only coefficient-rank-drop point set x0=y0=1, s=1+x1, t=1+y1; eliminating N gives C[r,c,s,t]/(rs−ct), an integral domain. Elsewhere the incidence is locally a vector bundle.

An independent SymPy run verified determinant Nt−rc and inverse-variable ideals for zero-total/nonzero-row, boundary, generic, and kernel statistics. The first two give the unit ideal; (N,r,c)=(1,1/3,1/2) gives (z−18,a−1/3,b−1/2); the kernel case gives z a(1−a)b(1−b)−1. This confirms those sample branches, while the proofs establish the full classifications. No general-problem resolution or novelty claim is accepted.

The finalized exact_checks.py was independently read and rerun: all 22 checks passed under SymPy 1.14.0. Rational-function checks cover generic subbranches; the complete strata rely on the accompanying proofs, not finite samples. The final report includes the local reducedness argument and was rechecked after that addition.
