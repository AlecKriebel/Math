# Independent adversarial audit: partial construction lanes

Date: 2026-10-20 UTC. Target: queue 1817 / AMR-030-0003 as formalized in the recovered source gate. This is an authored mathematical review, not a full solution or novelty certification. No external publication performed.

## Verdict

**PASS for the stated partial results. No full conjecture resolution.** No fatal mathematical error or required correction was found in the four documents below. Exact boundary handling, reflected copies, and distinctions between the whole plane and restricted samples are maintained. The conjecture remains unresolved by these results.

The periodic-polygonal certification lane supplies a correct decision procedure, not an implemented end-to-end verifier or an accepted candidate. The stripe lane implements its narrower rational fixed-width test. A finite menu of regular colorings is not the class of all triangle-dependent colorings.

## Stripe criterion

- Independently checked that a projection pair ranges over the ellipse defined by the inverse Gram matrix. Orthogonal reflection adds no projection pairs.
- A common translation into three same-color half-open strips exists exactly when the residual spread is strictly less than the width. This gives the open hexagon, not its closure. Equality-only contacts cannot be counted as failures.
- For a positive definite quadratic, an interior level-one point has nearby values on both sides of one. Conversely, strict inequalities between the closed minimum/maximum give interior points on both sides and an interior level-one point. Thus both inequalities in the exact test must be strict, as written.
- The finite offset bound is safe; the implementation's larger L1-based box is conservative. Hexagon edge minimization and vertex maximization are exact with rational arithmetic.
- Checked the sufficient bound involving the second-longest side, including equality. The proof uses at least two cross-strip edges, each strictly longer than twice the width.
- Checked the explicit flat-triangle projection witness: 1/100, 61/100, 39/100 have strip indices 0, 6, 3 at width 1/10. This rejects that width only.
- The variable-width union-of-open-intervals characterization is valid. Independently reviewed the later quantitative cutoff: delta lies in [3,6), so J lies strictly inside the horizontal ellipse domain with x at least aR/2. Factoring R²-x²/a² bounds its square root by sqrt(13R/a). The resulting derivative bound is at most -4 under the stated R threshold. An interval of y-values of length at least four has a multiple of three strictly inside, giving a residual (r,0) with |r|<1/2 and hence a strictly interior forbidden-hexagon intersection.
- Thus every 0<w<=epsilon really is bad. Combined with w<=h and the uniform finite offset box, this gives a finite exact all-width decision procedure for algebraically specified input. This is stronger than merely scanning finitely many widths, and handles potentially isolated good endpoints correctly by subtracting open intervals. The code does not implement this potentially enormous all-width search, and no all-width result for the exhibited flat triangle is claimed.

## Two-dimensional tilings

- Checked the square-checkerboard witness on the diagonal x+y=a and its offset parallel line. The interval for the third vertex is nonempty exactly under the asserted strict height bound; excluding a discrete collection of grid vertices leaves interior witnesses.
- Checked the rational example and its squared equal-side length 62509/1250.
- Checked all five unit edges of the first diamond. The second rotated diamond has the same properties; cosine 5/6 gives a unit edge between their outer vertices. The resulting seven-vertex graph cannot be properly three-colored.
- For each regular coloring, a translate of all seven vertices avoids the closed nowhere-dense boundary set. A monochromatic unit edge then has a locally monochromatic neighborhood at one endpoint. Circle intersections produce every sufficiently short base b with equal sides exactly one.
- The finite minimum of these neighborhood radii gives the claimed uniform epsilon for a fixed finite menu. It does not give an epsilon uniform over all regular colorings, and does not exclude a coloring selected separately for each b. The note expressly preserves this quantifier distinction.

## Finite obstructions

- Checked the dyadic valuation proof, including negative coordinates in the floor identities. For each fixed represented squared distance, the specified coloring properly separates all edges at that distance on the entire square lattice.
- Every congruent triangle contains such an edge. Consequently the restricted triangle hypergraph is two-colorable, not just three-colorable. This does not extend that coloring to all plane points.
- A finite rational point cloud scales into the integer lattice. Compactness then gives the asserted two-colorability on Q² for each fixed triangle. The coloring may depend on the triangle.
- Checked the finite-hypergraph compactness equivalence with the unrestricted all-plane problem. This yields no regularity or computability guarantee.
- Checked minimum degree at least three, at least nine vertices, and pair-codegree at most four. In particular, the equal-perimeter argument on five points forces equal distances, so each eight-point set can be partitioned into two nonedge triples and a pair.
- Checked the square-lattice similarity criterion z in Q(i), and the irrational squared-distance example. Density of Q² does not preserve exact congruence.

## Periodic-polygonal certification

- Checked that the half-open fundamental domain and exact finite partition define a total coloring, with every edge and vertex assigned.
- The lattice-offset bound includes all possible copies, including extremal integer norm bounds. Both determinant signs are enumerated.
- For fixed cells and offsets, every constraint other than the circle is affine in translation and orientation coordinates. Strict Fourier–Motzkin elimination remains exact for finite systems when strictness is propagated by logical OR for paired bounds.
- The rational circle parameterization produces degree-at-most-two inequalities with unchanged strictness; the omitted point (-1,0) is tested separately. Root/sign decomposition over real algebraic numbers is an exact decision method.
- Algebraic reconstruction of a feasible translation is possible through retained elimination bounds. This certifies a supplied candidate only; no bound on candidate complexity or periodic-polygonal existence is proved.
- Checked the explicit square-coloring rejection for every 0<h<2. All three coordinates are in strict square interiors, and for h=1/10 the equal squared sides are 113/50. This counterexample is not reparable by boundary reassignment.

## Source and implementation checks

Read the recovered Graham–Tressler text and independently extracted the recovered Aichholzer–Perz PDF. The latter's normalization is shortest side BC <= AC <= AB=1. Its Theorem 3.1 therefore gives the asserted second-longest-side condition at k=3; Theorem 3.2 gives the reported nonobtuse shortest-side condition. These are existing sufficient results, not novel coverage. The source's extended-abstract/preprint qualification is retained. The Graham–Tressler text states the relevant conjecture and explicitly describes stripe constructions as covering many but not all triangles.

Read the recovered Natalchenko–Sagdeev introduction: it reports the Euclidean three-color bound as conjectural, with seven the known general upper bound in that source. This audit does not independently exhaust later literature and does not certify current openness or earliest priority. The source gate's limited status wording is appropriate.

Reran both supplied scripts successfully:

- stripe_exact.py: all five expected rational checks pass, including tangency-sensitive cases and the explicit failure.
- check_square_grid.py: 41,616 pairs, 134 squared distances, 289 points pass.

These finite checks are implementation sanity checks, not substitutes for the general proofs.

## Reviewed versions

SHA-256 at review time:

- STRIPES.md: f49fbb5c3f934adbeeef85689df56498e306a983c2bb851305e05646e8f81157
- TILINGS.md: 0f40ed824f8aeb37a25a070d2b8b780bd891ec516066e55d3b118af7c03c10c9
- FINITE_OBSTRUCTIONS.md: a78b7ed361923fb78b20bc2fad2fe53b87b46c868fd69561dd4cd69052b96fe9
- CERTIFICATION.md: 1bbaa6fba7735ba98a64ed14de36b38f76b9452c4dac3cb665763685d81b54fc

Later substantive additions are outside this verdict until separately reviewed.
