# Fresh independent complete audit: rank 477 / ID 2801 / KP-3.3

Date: 2026-10-03 UTC.

## Verdict

**PASS, for the complete finite-volume cusped hyperbolic 3-manifold target, including nonorientable manifolds. No substantive gap or required mathematical repair was found in the proof of Huabin Ge, arXiv:2609.27635v1, Theorem 1.1, through Sections 2–4.**

This is a proof audit with the classical Epstein–Penner decomposition as an expressly identified standard input. It is neither a new mathematical discovery nor a formal proof-assistant verification. It does not certify Ge's additional geodesic-boundary assertions or the consequences in Sections 5–6. All credit for the pertinent new theorem and construction remains with Ge. The source is a recent preprint; refereed acceptance was not verified.

This report records the independent mathematical audit. Its publication status is recorded separately in the package README. The six reviewed author files were not edited during the audit.

## 1. Frozen object and source identity

The audited directory is `author/`, containing six files. Their original byte lengths and SHA-256 hashes are preserved in `AUTHOR_MANIFEST.json`. Author and locally retained source bytes were checked independently and matched their recorded hashes. The source PDF SHA-256 is:

`247c0162c4755990b05557c6ca4d2bfc765a3fe9652b4f70f3288be8f5c97999`.

The complete relevant PDF text was extracted and read, rather than relying on its abstract or the author package's verdict. Core formulas were also visually checked on printed pages 4 and 7–11. The supplied K3 printed-page-134 image was independently inspected. The exact target is the geometric ideal triangulation question at Problem 3.3 of the 2026 K3 list. Printed page 131 explicitly uses complete hyperbolic metrics. Yoshida's original printed introduction states the finite-volume, noncompact version. The indexed UnsolvedMath KP-3.3 alias agrees with the book; this does not overcome or conceal the recorded failure to read the numeric ID URL.

The live primary arXiv record was reopened at both the unversioned and v1 URLs. It lists Huabin Ge, submission on 23 September 2026 at 10:00:09 UTC, 20 pages, and v1 only. No journal reference or withdrawal was displayed. Theorem 1.1 in the PDF/HTML has the exact complete finite-volume cusped scope, and Section 2.2 explicitly permits nonorientable M. The arXiv license link resolves to CC BY 4.0. Bounded identifier/title searches with correction and gap terms did not locate a primary correction; this is limited negative evidence, not a claim that no criticism exists.

Primary links:

- https://arxiv.org/abs/2609.27635v1
- https://arxiv.org/pdf/2609.27635v1
- https://arxiv.org/html/2609.27635v1
- https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- https://ir.library.osaka-u.ac.jp/repo/ouka/all/10590/ojm33_01_03.pdf

## 2. Classical geometric input and actual affine face maps: PASS

The required Epstein–Penner input is a locally finite, equivariant decomposition into finite ideal convex polyhedra, with finitely many cell orbits, obtained by radial projection of bounded three-dimensional convex polytopes in supporting affine hyperplanes of Lorentz space. The supporting hyperplanes do not contain the origin and admit equations lambda_i(x)=1. Every vertex has positive time coordinate and lies on the future light cone.

This is the declared classical theorem, not a conclusion of the finite controls. Attempts to open the original Epstein–Penner DOI/PDF did not yield readable article text. I therefore do not claim to have reread or reproved that original article. The needed convex-hull decomposition is corroborated in the published Luo–Schleimer–Tillmann paper, particularly its opening discussion:

https://sschleimer.warwick.ac.uk/Maths/2008geodesic_ideal_tri.pdf

The new proof does not incorrectly assert that arbitrary hyperbolic isometries are affine in Klein coordinates. It uses the finite polytopes before radial projection, where a deck transformation is a linear Lorentz transformation. Its restriction from a face to its paired representative is affine. This distinction is essential and is handled correctly.

The argument excludes nontrivial stabilizers of cells and polygonal facets: such a stabilizer permutes the finite set of future light vectors and fixes their sum. The sum is timelike because at least two vertices lie on distinct light rays, and the Lorentz product between such rays is strictly negative. Normalization gives a fixed point in hyperbolic space. A discrete torsion-free isometry group has trivial point stabilizers. This argument works in O+(3,1), including orientation-reversing elements.

Consequently the quotient has genuine pairs of distinct facet occurrences, even when two facets belong to the same representative cell. No prohibited fixed-facet symmetry is being silently imposed.

## 3. Regular subdivisions and exact face compatibility: PASS

For a finite full-dimensional convex polytope, the lower envelope of the convex hull of lifted vertex heights is a finite piecewise-affine convex function on the whole polytope. Its domains give a pure face-to-face subdivision. Maximal cells are full-dimensional convex hulls of subsets of original vertices; there are no new vertices or overlapping interiors. Projection is injective on the lower graph, so intersections of projected lower faces are common faces.

Every original extreme vertex remains present: it cannot be expressed as a convex combination of the other original vertices. Thus a nominally trivial subdivision cannot conceal unused non-affine vertex data.

Lemma 2.1 is valid in both directions. Restricting a lower affine support to a facet gives its contact cell there. Conversely, extend a facet support to the ambient affine space and subtract a sufficiently large multiple of a facet-defining affine function that is zero on the facet and positive at all outside vertices. Finiteness makes one sufficiently large multiple work for every outside vertex. The contact set on the facet is unchanged and all outside inequalities are strict.

Adding an affine function to heights preserves all lower contact sets after translating the support functions. Affine pullback preserves the same inequalities. Therefore the compatibility condition on each paired polygon gives equality of the actual geometric subdivisions, not merely combinatorial agreement.

## 4. Height quotient, dimensions, repeated incidences, and gauges: PASS

For each full-dimensional current polytope, affine functions restrict injectively to its vertices. The affine gauge space has dimension 4, so H_i has dimension v_i−4. For an n_alpha-gonal facet, the corresponding affine gauge has dimension 3, and Q_alpha has dimension n_alpha−3. These dimension statements use affine spanning, not generic-position assumptions.

The map B_alpha([h])=[h_minus−h_plus composed with phi_alpha] is well-defined: altering either cell representative by an affine function changes the difference on the facet by an affine function. This remains true when both facets belong to the same cell. Its kernel is precisely the stated space of compatible height classes.

All combinatorial counts are local counts before quotient identifications. Each polytope edge is incident to exactly two of its facets. Therefore

    sum_i f_i = 2F,
    sum_i e_i = sum_alpha n_alpha.

These equalities survive repeated global vertices, repeated global edges, same-cell face pairings, and multiple interfaces between the same two cells. Euler's identity v_i−e_i+f_i=2 then gives

    dim(domain B)−dim(codomain B)
      = sum_i(v_i−4)−sum_alpha(n_alpha−3)
      = (1/2) sum_i(f_i−4).

The estimate for dim ker B is rank-nullity with rank B at most the codomain dimension. **No global independence, maximal-rank assertion, or independence of the individual face equations is assumed.** Dependencies only improve the estimate.

Each bounded full-dimensional convex three-polytope has at least four facets, with equality only for a tetrahedron. If a current polytope is not a tetrahedron, the displayed bound is positive. Its total is an integer because the total number of facet occurrences is even.

No missing edge-cycle or cusp-vertex scalar-height condition is needed. The construction does not seek one scalar height function on the quotient. It seeks subdivisions that agree on each paired facet. Such pairwise equality descends through all identification chains. Existing edges have just their two endpoints and acquire no extra vertices; hence there is no additional edge subdivision to synchronize. Requiring equal numeric heights at globally identified vertices would impose an unnecessary condition and would invalidate this method, but the proof does not impose it.

## 5. Strict refinement and preservation of admissibility: PASS

A nonzero class has at least one non-affine cell height. If its regular subdivision had only the original polytope as maximal cell, an affine lower support would agree with the heights on all its extreme vertices. That would make the class zero. Thus at least one current polytope is divided into at least two full-dimensional cells.

Each new outer facet lies in an old facet and is paired with its image under the restricted old affine pairing. Each new internal facet belongs to exactly two current full-dimensional cells and is paired between those two copies by the identity. This is a finite admissible system of bounded full-dimensional convex polytopes again.

In particular, iteration genuinely refines the existing subdivision. It does not replace an old cut by a different cut or discard a previously established interface. Independent affine gauges on the new cells are permissible because the next compatibility map includes every current internal interface as well as every outer interface.

## 6. Finite termination using original vertices: PASS

Fix an original polytope P_i and its original vertex set V_i. By induction every later cell inside P_i is the convex hull of a subset of V_i. Every full-dimensional current cell therefore contains an affinely independent four-element subset of V_i.

Two distinct current cells cannot contain the same independent four-set: the tetrahedron spanned by it has nonempty three-dimensional interior, which would be contained in both cells, contrary to disjoint cell interiors. Selecting one such four-set for each current cell is consequently injective. The current cell count inside P_i is bounded by the finite number of independent four-element subsets of V_i.

Every nontrivial refinement strictly increases the total full-dimensional cell count; the sum of these original-polytope bounds is fixed and finite. The process must terminate. If any non-tetrahedron remained, the positive kernel bound would furnish another strict refinement, a contradiction.

This proof does not require a single generic height that triangulates all cells, or that the final refinement be regular relative to one original global height vector. Neither stronger assertion is used.

## 7. Lorentz/Klein nondegeneracy, positivity, and descent: PASS

For a resulting tetrahedron with affine-independent Lorentz-space vertices v_1,...,v_4 in lambda_i=1, any linear relation sum c_k v_k=0 gives sum c_k=0 after applying lambda_i. Affine independence forces all coefficients to vanish. Dividing each column by its positive time coordinate preserves linear independence. Thus the normalized columns (1,p_k) are linearly independent and the four ideal Klein points p_k are affinely independent. Their hyperbolic convex hull is a genuine nonflat ideal tetrahedron with positive volume.

Radial projection carries convex combinations to convex combinations with weights proportional to the positive time coordinates. On lambda_i=1 it is injective, with inverse obtained by rescaling (1,p) to lambda_i=1. It therefore preserves the subdivision, intersections, and disjoint interiors. All vertices remain ideal; no finite Steiner vertex or flat tetrahedron enters.

Trivial cell stabilizers make equivariant extension from cell representatives unambiguous. Facet compatibility makes adjacent extensions agree. Local finiteness follows from that of the original decomposition and the finite number of subdivisions in each original cell. There are finitely many tetrahedron orbits.

The quotient is the required usual face-pairing ideal triangulation, allowing identification of tetrahedron vertices and edges. It is not claimed to be an embedded simplicial triangulation of a cusp compactification. It geometrically subdivides the existing complete metric, so its gluing and completeness follow from that metric rather than an approximate gluing-equation calculation.

No orientation hypothesis entered the construction. In the orientable case one chooses each tetrahedron's order using the global orientation and obtains upper-half-plane shapes. In the nonorientable case the geometric subdivision and equivariant descent remain valid without a global ordering. There is no unproved descent of an arbitrary triangulation from an orientable cover.

## 8. Adversarial cases and interpretation boundaries

- A face paired to itself by an extra symmetry is not an ordinary pair of two facet occurrences. Allowing such data would break the face-count identity and can impose impossible diagonal invariance, for example under a square quarter-turn. This is not a counterexample to the application: the Epstein–Penner manifold system has no such facet stabilizers. Preserve the ordinary paired-occurrence interpretation when citing the affine theorem.
- The assertion that a stabilizer fixes a timelike barycenter applies here to cells and polygonal facets. It must not be extended to ideal vertices, whose peripheral stabilizers are nontrivial. No step uses trivial ideal-vertex stabilizers.
- Coplanar subsets of four original vertices are never counted as termination witnesses or admitted as tetrahedra. Only full-dimensional regular cells and independent four-sets enter those arguments.
- Prescribing an arbitrary boundary triangulation in advance is a different extension problem. The proof constructs compatible boundary choices and does not claim that all prescribed choices extend.
- The classical decomposition is essential. The proof does not establish the analogous claim for incomplete metrics, infinite-volume manifolds, or arbitrary nonconvex cells.

These are scope clarifications, not blocking repairs to the submitted target proof.

## 9. Exact controls and package check

The frozen control script was inspected and rerun with exact SymPy rational arithmetic. It reported PASS with 64 checks. Its parsed output was exactly equal to the frozen verification_results.json.

The tested cube example produces the two stated prisms, then the stated six tetrahedra of volume 1/6, with matching translated outer-face triangulations and matching internal rectangle diagonal. The eight opposite-square parity cases give quotient dimensions 1,1,1,2,1,2,2,3, and the cube has 58 affinely independent four-subsets.

The number 64 includes individual elementary assertions; it is not 64 independent manifold examples. These are appropriately labelled finite affine controls. They neither prove the universal theorem nor verify the classical Epstein–Penner input. The written universal argument above supplies the actual proof audit.

## 10. Gate disposition and remaining obligations

Mathematical source/proof gate: **PASS**.

Required mathematical repairs: **none** for the stated KP-3.3 target.

Required retained qualifications: attribute the result to Ge's arXiv:2609.27635v1; label its recent preprint status; retain the standard Epstein–Penner input; retain face-pairing triangulation semantics and nonorientable scope; do not portray finite tests as universal formal verification; do not certify Sections 5–6 or historical first priority.

The independent mathematical gate passes without altering the six reviewed author files. Their hashes are retained in AUTHOR_MANIFEST.json. Original mathematical attempt count remains zero. The current research-record disposition is stated in the package README.
