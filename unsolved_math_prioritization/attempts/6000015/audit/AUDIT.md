# Independent audit: Stein tangent bundles and polyhedral quotients

Date: 3 October 2026. Problem 6000015 / AMR-059-0015.

## Verdict

**PASS within the stated partial scope. No blocking mathematical defect found. The original unrestricted question remains unresolved; retain the unsolved, 5/5 disposition.**

The main theorem establishes Steinness of the specified tangent complex manifold for every line-free open polyhedral domain and every free properly discontinuous affine group preserving it, including noncompact quotient bases. The supporting norm obstruction, translation result, dimension-one result, and continuous weak exhaustion are valid with the stated hypotheses. None establishes the unrestricted original assertion or a counterexample to it.

This is an independent AI-assisted mathematical audit, not human peer review, a novelty determination, or a complete literature survey. No changes to the frozen author packet were required or made.

## 1. Frozen identity and source gate

The reviewed manifest has SHA-256

`9e6d6a08ddef9005d5bacf9995a3221692e1daf2ed689a52c16597bf6b3733c9`.

The reviewed `PROOF.md` has SHA-256

`d00dc75d1a734bbfb257403eeac82b9b86341003f93ae90f78f5b4df1bc3defb`.

Every one of the six author-file sizes and hashes matches the manifest. The manifest and proof were checked both before and after review.

The original article's title page and printed p.126 were visually inspected. Item 5(a) asks about the natural complex structure on the tangent bundle of a Hessian manifold whose metric is complete. The separate line-free convex-domain quotient formulation has no compactness or homogeneity assumption. Completeness here concerns the Riemannian metric; it is not affine geodesic completeness. Item 5(b) asks a different deformation-stability question and supplies no resolution of 5(a). See [Furuhata–Matsuzoe–Urakawa (1998), pp.125–126](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en).

Shimizu's seven-page paper was read in full, including the characteristic-function properties, homogeneous-cone lemma, homogenization construction, divisor descent, and exhaustion proof; formulas absent from text extraction were inspected in rendered pages. Its theorem gives strict plurisubharmonicity on a divisor complement. Compactness gives exhaustion there; homogeneity eliminates the divisor. The resulting whole-tangent-bundle Stein statement uses both compactness and homogeneity. The frozen packet respects these restrictions. Shimizu's lemma invokes Rothaus for its final step; this audit does not claim to have re-proved that cited theorem. See [Shimizu (1985), pp.299–305](https://doi.org/10.2748/tmj/1178228643).

Source conclusions were checked against the supplied primary PDFs. A fresh article-page web fetch was unsuccessful and was not treated as additional evidence. No claim about current catalogue status or exhaustive modern literature coverage is made here.

## 2. Central polyhedral argument: adversarial checks

### Facets, characters, and discrete lattice

A full-dimensional open polyhedron has a finite nonredundant facet description. Its affine automorphisms preserve the face structure of its closure, so the facet permutation homomorphism is well-defined even when the polyhedron is unbounded. The kernel has finite index.

Line-freeness forces the facet normals to span the entire dual space: a common nonzero annihilator would give a full line through each interior point. For an element fixing each facet, the two corresponding affine forms vanish on the same hyperplane and are positive on the interior. They therefore differ by a unique positive factor. Composition makes each factor a character.

The logarithmic-character map is injective. Fixing all facet forms fixes the linear and translation parts because a selection of independent normals determines both. More strongly, convergence of the character vector to zero forces convergence of those affine transformations to the identity, by exactly the two coefficient identities displayed in the proof. Such a nontrivial sequence contradicts proper discontinuity: choose a compact neighborhood of an interior point, on which transformations sufficiently close to the identity intersect that neighborhood. Finitely many possible elements and convergence of their characters then force eventual identity. Thus zero is isolated in the additive image. A discrete subgroup of a finite-dimensional real vector space is a full lattice in its real span. No finite-generation assumption was silently inserted.

### Freeness and proper discontinuity on the tube

These hypotheses lift from the base. An element fixing a tube point fixes its real part, hence is the identity. If an element moves one compact subset of the tube to meet another, its base action moves their compact real projections to meet. There are only finitely many such elements. Consequently the quotient is a Hausdorff complex manifold with the expected tangent-bundle complex charts.

These observations also justify the finite final quotient. If a coset in the finite permutation quotient fixed a point modulo the kernel, a representative composed with an element of the kernel would fix a tube point. Freeness of the original action makes that coset trivial.

### Branch choice, embedding, and closed descent

The facet map is an affine embedding because its linear part has rank n. Its image is a closed affine complex subspace. Its intersection with the product of right half-planes is exactly the tube image.

The principal logarithm is globally single-valued and biholomorphic from a right half-plane to the strip with imaginary part between minus and plus pi/2. Componentwise logarithms therefore preserve injectivity, smoothness, and relative closedness. The image described by the exponential equations is a closed complex submanifold of the product strip. It need not be closed in all of complex Euclidean space; the argument only uses closedness relative to the strip, which is the correct assertion.

Positive real scaling produces real logarithmic translation with no branch jump. The real lattice acts freely and properly on the ambient strip. An invariant relatively closed set has closed image in the quotient, since its invariant complement is the preimage of the open complementary set. Evenly covered coordinate neighborhoods show that its quotient remains an embedded complex submanifold. Thus the restriction step does not assume that an arbitrary quotient of a Stein manifold is Stein.

### Strictness and properness, including escape in the base

For the proposed ambient function, the real-part term contributes P/2 to the Levi matrix; the strip barriers contribute one quarter of the diagonal matrix of squared secants. The latter is positive definite everywhere. This proves strictness even along the real span of the lattice, where the projection term vanishes.

A sublevel bounds the perpendicular real component and bounds every imaginary coordinate away from the strip boundary. The remaining real component can be translated into a compact fundamental parallelepiped. This supplies compact representatives of every sublevel and proves properness on the quotient. Restriction to the closed complex submanifold retains both properness and strictness. No compactness of the original base is used.

For the final finite sum, every summand is nonnegative and the identity term is present. Each sublevel is therefore a closed subset of a compact sublevel of the identity summand. Holomorphic pullbacks preserve strictness. The descended function on the finite quotient has compact sublevels as images of compact sets. All assumptions of the smooth strict-plurisubharmonic-exhaustion criterion are met.

The shorter facet potential also has the claimed positive-definite Levi matrix, since the normals span. Its vanishing on the zero section correctly prevents it from being an exhaustion when the base is noncompact. The longer strip construction genuinely addresses this additional escape direction.

## 3. Remaining mathematical claims

### Complete exact Kähler lift

The one-form defined intrinsically by minus the metric pairing of the fiber vector with the projected tangent vector is globally well-defined. Symmetry of the Hessian cubic tensor cancels its base-base differential terms, giving the stated Kähler form with the stated sign.

The completeness argument is valid for the lifted metric. A finite-length path has a convergent base path by Riemannian completeness. Eventually the base lies in an affine chart with compact closure and uniformly positive metric bounds. In that chart finite lifted length controls both coordinate variations, so the fiber coordinates converge too. The argument does not require affine completeness or global affine coordinates. Stokes' theorem excludes positive-dimensional compact complex submanifolds. Exactness alone has not been confused with a global strict plurisubharmonic exhaustion.

### Squared-norm obstruction

The periodic Hessian metric and its eigenvalue bounds were independently checked. At the indicated fiber point, direct Wirtinger differentiation gives the full Levi matrix equal to minus 3/8 times the identity and complex gradient equal to (-5i,0). The second coordinate is therefore simultaneously a negative Levi direction and a zero gradient direction. In the composition formula its second-derivative term vanishes, leaving a strictly negative contribution whenever the first derivative of the scalar function is positive at the specified norm value.

The conclusion is correctly restricted to this ansatz. It does not rule out every nondecreasing scalar function with possible zero derivative, and it does not claim to: the text explicitly requires positive derivative. A fixed base correction has a bounded, fiber-independent contribution at the fixed base point, while the bad norm direction becomes quadratically negative as the fiber coordinate grows. The complex tangent manifold of this affine torus remains a product of two punctured planes and is Stein.

### Translation and one-dimensional cases

Integer-translation invariance plus convexity gives invariance under each real translation direction. A complement to their real span intersects the domain nontrivially and yields the claimed product decomposition. The discrete translation subgroup is a full lattice in its span; the complex quotient factor is a product of punctured planes. The remaining tube is convex. The Stein conclusion follows.

For a connected one-dimensional affine manifold, the tangent manifold is a connected Riemann surface with a closed noncompact real fiber. Hence the tangent manifold is noncompact and the open-Riemann-surface theorem applies. This does not require completeness.

### Normalized-support envelope

The normalized gradient set is closed and bounded using an interior ball, hence compact. A nonnegative affine function normalized to one cannot vanish inside the domain unless it is the zero function, which normalization excludes. This justifies uniformly positive denominators on a sufficiently small base neighborhood and gives the stated continuous maximum formula.

If all normalized gradients annihilated a nonzero direction, the separation representation by containing open affine halfspaces would place a complete line in the domain. Thus the fiber seminorm is genuinely a norm. Continuity and compactness of the unit sphere give local uniform norm equivalence.

Each support-form potential is smooth plurisubharmonic. Continuity and local boundedness of their supremum permit the disk-submean proof as written, with no exchange of supremum and integral. Affine invariance is exact. On a compact quotient base, a finite cover by charts whose closures lie in trivializing neighborhoods turns the local fiber bounds into compact sublevels.

The quadrant example exhibits an open region on which only one coordinate potential is active. The envelope there is independent of the other complex coordinate, so the null direction is real analytic degeneracy on a neighborhood rather than merely an isolated zero. No strictness or noncompact-base exhaustion has been incorrectly inferred from this construction.

## 4. Reproducibility and limits of the checks

The frozen verifier ran successfully with SymPy 1.14.0. Its output is byte-identical to the frozen result file: all **60 exact controls pass**. `replay_results.json` records that replay.

`independent_checks.py` separately forms Wirtinger operators and real Hessians and adds **22 passing controls**, recorded in `independent_results.json`. These include the full torus Levi matrix and gradient, the all-fiber transverse obstruction, a non-coordinate rank-one strip projection, the swap-and-scale quadrant action whose square fixes the facets, an explicitly controlled noncompact-base direction, the bounded interval's affine facet relation, and the support envelope's transverse degeneracy.

The finite swap-and-scale example also tests a nontrivial finite facet quotient: the map (x1,x2) to (2x2,2x1) has square equal to scaling by four. Its logarithmic action is a coordinate swap plus a real diagonal shift. The quotient base is noncompact; the perpendicular projection controls the difference of logarithmic coordinates. These computations are stress tests of formulas, not substitutes for the general proof of group discreteness, descent, or properness.

To reproduce, run `python independent_checks.py` from this audit directory, or provide the public packet directory as its first argument. The script reads the frozen packet and writes only its JSON result to standard output.

## 5. Disposition

No correction is required for the retained partial mathematics. The five approaches are genuinely distinct mathematical attempts, and the work log consistently reports that the original problem has not been solved. Preserve that status. The remaining problem includes arbitrary nonpolyhedral line-free domains with affine quotient groups, noncompact-base escape, and the unrestricted complete Hessian setting. Neither the weak exhaustion nor the failure of the metric-norm method closes those gaps.
