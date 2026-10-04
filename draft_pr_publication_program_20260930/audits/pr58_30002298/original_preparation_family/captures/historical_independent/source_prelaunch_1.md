# Independent review of the Fantappie denominator characterization

## Verdict

**PASS for a credited known characterization. Recommend already_solved for the exact unit-density Question 1 in 30002298 / OWR-12339-004.** No mandatory mathematical correction is required.

The reduced denominator consists precisely of the distinct affine factors associated with the nonzero algebraic vertices. Comparing those vertices with the original triangulation-intersection vertex set gives the requested geometric criterion. The origin exception, signed line-cone condition, and prescribed normalization are all necessary and correctly handled.

This is a review of previously published coverage and the submitted explanatory argument, with no campaign discovery or priority claim. It does not certify any answer to the neighboring questions about signed coefficients, spanning hypotheses, or reconstruction algorithms.

Reviewed on 2026-09-30 by a separate gpt-6-astra reviewer with xhigh reasoning. Frozen artifact: SOURCE_STATUS.md, SHA-256:

457559b700340e08ab2402629685c961b15327f74a21a354be198c561fd601e0

No author artifact or source file was edited.

## Exact primary scope

I read Pasechnik's complete original contribution, printed pp.637–640, and visually inspected p.638. Question 1 uses the unit-density transform with the normalization \(d!\) and exponent \(d+1\). The compact set is a finite union of convex polytopes. The vertex set in the question is the intersection of the vertex sets of triangulations, not the convex-hull vertices or the vertices of an arbitrarily fixed triangulation. The preceding cancellation example establishes the intended reduced-denominator interpretation. [Original OWR report](https://ems.press/content/serial-article-files/46446)

The package's constant-term normalization removes the scalar ambiguity in a denominator. Its separate treatment of the zero transform and of measure-zero pieces is consistent with the ambient Lebesgue measure. It does not replace that measure by an atomic or surface measure.

I read the full 13-page [Akopyan–Bárány–Robins author manuscript, arXiv:1508.07594v2](https://arxiv.org/abs/1508.07594v2), especially Definition 1, Theorem 1 and its minimality argument, the cone transform and kernel proof in Sections 4–5, and Remark 10. The latter explicitly states the identification of Fantappiè denominator vertices with algebraic vertices, referring to the preceding transform argument. The local definition uses finite real linear combinations of line-cone indicators, modulo null sets. It is not a condition merely on whether the tangent cone itself contains a line.

The [ISTA publication record](https://research-explorer.ista.ac.at/record/1180) independently confirms *Advances in Mathematics* **308** (2017), 627–644, DOI 10.1016/j.aim.2016.12.026. The mathematical text inspected is the complete January 2017 author version, not a claimed inspection of the publisher's typeset PDF. The arXiv version history and institutional publication metadata agree.

For the normalization and simplex identity, I checked Theorem 2, equation (1.9), and Corollary 3 in the full [Gravin–Pasechnik–Shapiro–Shapiro publisher text](https://link.springer.com/article/10.1007/s13324-018-0226-8), alongside the supplied manuscript. Equation (1.9) is stated for simple convex polytopes; using it separately on each simplex, as the artifact does, is legitimate without assuming that the entire nonconvex set is simple.

## Reduced poles and cancellation

The submitted argument establishes more than a denominator divisor bound.

A triangulation gives a finite sum of simplex transforms. For each simplex the denominator is a product of distinct normalized affine factors \(1-\langle w,u\rangle\). Distinct nonzero vertices give distinct nonassociate factors, and the zero vertex gives the unit polynomial. A common squarefree denominator therefore exists. Reduction cannot introduce new factors or increase their multiplicities.

Regrouping the simplex partial fractions at a vertex \(w\) gives the coefficient \(c_w\) in the artifact. Its degree is \(-d\), and all of its possible denominator hyperplanes pass through the origin. The determinant and sign are correct: with kernel \(\exp(\langle u,x\rangle)\), integration over a simplicial cone gives \((-1)^d|\det(q_1,\ldots,q_d)|/\prod_i\langle q_i,u\rangle\) in its convergence region. In dimension one this reduces to the elementary integral \(-1/u\) on the positive ray. The uniform sign convention does not alter the cone-kernel criterion.

For a nonzero \(v\), the hyperplane \(H_v=\{\langle v,u\rangle=1\}\) cannot equal a homogeneous edge-denominator hyperplane. Nor can it equal \(H_w\) for another vertex. Thus there is a relatively open dense part of \(H_v\) on which all the other factors in the partial-fraction expression are regular. Multiplication by \(1-\langle v,u\rangle\) and restriction there yields exactly \(c_v|_{H_v}\).

The key noncancellation step is sound. If \(c_v|_{H_v}\) vanished identically, then for generic \(u\) with \(\langle v,u\rangle\ne0\), homogeneity and the substitution \(u/\langle v,u\rangle\) would force \(c_v(u)=0\). A rational function vanishing on a nonempty open set is identically zero. Conversely, a zero coefficient contributes no pole. Therefore the affine factor survives exactly when \(c_v\ne0\).

This argument handles cancellations between all incident simplices and excludes hidden cancellations between different affine vertex factors. It does not assume that a single chosen simplex contributes an uncancelled residue.

## Tangent cones and the original vertex set

The local coefficient is the cone Fourier–Laplace valuation of the tangent cone. Tangent-cone indicators add almost everywhere under the simplex decomposition. At a point lying on a positive-dimensional face of a simplex, that simplex's tangent cone is invariant in a nonzero direction and has zero valuation. Only simplex-vertex contributions can remain.

The kernel characterization identifies zero cone valuation with expressibility as a finite signed sum of line-cone indicators. Hence \(c_v\ne0\) is precisely the algebraic-vertex condition used in the artifact.

The inclusion \(A(P)\subseteq V(P)\) is correctly justified directly. If a point were absent from the vertex set of one triangulation, every simplex would have empty tangent cone there, or a tangent cone with lineality. Adding those local indicators would express the tangent cone of the union as a sum of line-cones. Such a point is not algebraic. This argument applies to each original triangulation and avoids any unproved equivalence between triangulations and non-face-to-face dissections.

It also proves finiteness: the algebraic vertices lie in the finite vertex set of any one triangulation. Thus the product in the proposed complete denominator is finite. Together with the pole argument, this gives equation (5), and comparison with the original vertex product gives equation (4).

## Finite cone flipping

The finite geometric version is valid and retains the signed nature of the condition.

Flipping one generator replaces a simplicial cone by the negative of the flipped cone modulo a cone invariant in that generator direction. Iterating gives the product of the generator signs. Choosing the vector used for flipping to avoid the finitely many orthogonal hyperplanes is always possible.

All resulting generators have strictly positive scalar product with that vector. Their finite positive hull is pointed, and its nonzero directions lie in a common open halfspace. Overlaying all cone facets gives finitely many full-dimensional chambers on which the signed coverage is constant. Boundaries have zero ambient measure.

The needed injectivity has no positivity assumption on the signed coefficients. For clarity, it can also be seen analytically: after exponential damping by a vector strictly positive on every generator, the signed cone function is integrable. Its ordinary Laplace integral agrees with the rational cone expression in the convergence tube. A zero rational expression then gives a zero Fourier transform of the damped integrable function, so Fourier uniqueness makes that function zero almost everywhere. This confirms that the signed chamber function vanishes exactly in the line-cone kernel.

Consequently the finite coverage test is equivalent to the local algebraic-vertex condition, independent of the generic flipping vector. Requiring a disjoint union of line-cones instead, or merely checking whether the original cone is itself a line-cone, would change the criterion.

## Origin and edge cases

At the origin the nominal factor is 1. Therefore literal denominator equality cannot detect whether that point is algebraic. The exception is not cosmetic.

For the two opposite tetrahedra, the common-apex coefficient vanishes because the two three-dimensional cone contributions have opposite signs. The six other vertices survive. The displayed rational formula and the signed line-cone indicator decomposition both check out. In the centered example, the omitted factor is already a unit, so the original denominator equality still holds. After a translation making the common apex nonzero, the same geometric cancellation removes a nonconstant factor and the equality fails.

The common apex is indeed unavoidable in triangulations of this example: a full-dimensional simplex contained in the union cannot cross both sides of the separating plane, since the union meets that plane only at the apex. Covering either tetrahedron near its extreme apex therefore forces the apex to be a simplex vertex. The six outer points are convex-hull extreme points and are likewise unavoidable. The original vertex set really contains the cancelled apex; it has not been silently replaced by the algebraic vertex set.

Lower-dimensional components vanish under the stated measure and tangent-indicator convention. The zero-transform denominator convention is therefore consistent. No connectedness, general-position, or convexity hypothesis on the entire union has been introduced.

## Reproduction and independent controls

The submitted verifier was copied and executed separately. Its **284** exact assertions pass, and its regenerated receipt is byte-identical to the submitted receipt.

The independent verifier passes **6,463** exact assertions, including:

- All **256** unions of the eight coordinate orthants in dimension three, with all eight generic sign choices for the flipping direction
- **255** nonempty common-apex pole models, comparing the homogeneous cone coefficient with exact cancellation of the common affine apex factor and the presence of each outer vertex factor
- Opposite-cone parity controls in dimensions one through seven
- Six boxes in dimensions one through three, comparing permutation-triangulation transforms with a separate repeated-integration formula, normalized reduced denominators, and exact low-degree moments
- Centered and translated opposite-tetrahedron controls and the signed indicator identity on every open orthant

These are finite exact algebraic checks using SymPy 1.14.0. They do not replace the general cone-kernel theorem or establish new publication priority. One variable-shadowing error in the reviewer-only harness was corrected before the final successful run; no author code or mathematical assertion changed.

## Disposition

Recommend **already_solved, zero new substantive proof-search attempts**, credited to Akopyan–Bárány–Robins and the cited transform identities. The exact original characterization is covered. Keep the explicit origin convention and the author-manuscript versus publisher-PDF distinction.

There are no mandatory changes to the frozen artifact. The six publication files are REVIEW.md, review_summary.json, submitted_check_denominators.py, submitted_check_results.json, independent_checks.py, and independent_results.json. Local replay and source-reference files are not part of that package.
