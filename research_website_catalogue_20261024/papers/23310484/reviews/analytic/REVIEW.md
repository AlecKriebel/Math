# Independent analytic review — Zenodo 23310484

**Verdict: Pass within the stated scope.** No unresolved substantive defect was identified in the published proof. This is an AI analytic review, not independent human peer review, formal certification, or a determination of first priority.

## Source binding and independence

Reviewed the full published `sources/published-source/manuscript.tex` (all sections and references), independently of the archived review conclusions and the new sibling reviewers. The filenames of existing reports were visible in a file listing; their contents were not read. No packaged verification program was executed or treated as proof. A small independently written exact check of the formal Flores cycle is recorded separately.

The published PDF, `missing_faces_and_sphere_skeleta.pdf`, is 96,399 bytes with SHA-256 `055a6ff8f3451bedc7b75a106329bf2ffd1f02805a568f7f063c13a9b0eb9e59`. Both downloaded files independently matched their Zenodo-record MD5 checksums. The work is [Zenodo 23310484](https://doi.org/10.5281/zenodo.23310484), manuscript version 1.0 dated 12 October 2026. The exact TeX hash is recorded in `verdict.json`.

## Exact claim

Let `d >= 0` be an integer and `S` a finite simplicial complex whose realization is homeomorphic to the topological `2d`-sphere. A missing `d`-face `T` has `d+1` **actual vertices**, is absent, and has every proper subset present. Then the realization of `S^(d) union {T}` does not topologically embed in `S^(2d)`.

The higher-dimensional source need not have a combinatorial or standard PL sphere structure. The `d=2` argument establishes the stronger nonvanishing of the mod-2 degree-four van Kampen class. The zero-dimensional statement is vacuous under the stated actual-vertex convention. These are the claims checked; no claim of a new general embedding method or global novelty is added.

## Primary-source checks

The following imported statements were read in accessible primary mathematical sources and matched to their use. This is a targeted source check, not a full reconstruction of every cited theorem's original proof.

| Input | Reading and applicability |
| --- | --- |
| Adiprasito–Patáková, [Theorem 2](https://arxiv.org/html/2404.12265v3) | The original abstract complex can occur as a subcomplex of a triangulation of the PL ambient manifold; the embedding may change. The paper correctly does not claim the original embedding becomes simplexwise linear. |
| Karu–Xiao, [Theorems 1.2–1.3](https://arxiv.org/pdf/2204.07758) | Anisotropy over `Q(a_ij)` applies to simplicial homology spheres over F2, with `ell = sum x_j`. Setting `n=2d+1`, `m=d` gives exactly the required `ell u^2` form. |
| Nevo–Wagner, [author manuscript](https://pi.math.cornell.edu/~eranevo/homepage/NevoWagner-EmbeddabilitySkeletaSpheres-Rev2.pdf), Sections 2 and 5 | Read the obstruction definition, Theorem 5.3 structural setup and conditions (I.a)–(II.b), Lemma 5.2, and relevant new-face witness construction. The transfer theorem is formulated for finite complexes with those conditions, not only for globally standard PL spheres. |
| Davis–Fowler–Lafont, [p.797](https://msp.org/agt/2014/14-2/agt-v14-n2-p06-p.pdf) | Confirms every triangulation of a topological 4-manifold is PL; the manuscript additionally spells out the link argument. This does not assert standardness of the global PL 4-sphere. |
| Lickorish, [Theorem 5.9](https://arxiv.org/pdf/math/9911256) | Closed combinatorial manifolds that are PL homeomorphic are related by a finite sequence of bistellar moves and simplicial isomorphisms. This applies between S and its own barycentric subdivision. |
| Weber existence range | The original E-Periodica scan returned a verification page, so it was **not** read. The exact inclusive existence statement was checked instead in Skopenkov's author-written [Theorem 8.1 and its proof for `m=2n>=6`](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/skop.pdf), printed pp.52 and 55–58. This supports the required PL existence consequence, including `d=3`; it does not support a claim of having inspected Weber's original printed p.2. |

The parent supplied the alternate Skopenkov URL after the original retrieval limitation was reported. No sibling mathematical verdict was consulted to form this review.

## Independent proof reconstruction

### A. Local homology and the graded jump (manuscript lines 100–154)

A triangulation of a topological manifold has the indicated local relative-homology groups. Applying the local-link formula at every face gives integral sphere homology for its links; the empty face supplies the global sphere homology. This is sufficient for the homology-sphere Cohen–Macaulay and duality conclusions, without interpreting higher-dimensional links as PL spheres.

Put `r=2d+1`, `A=F[S]`, `C=F[S^(d)]`, and `B=F[S^(d) union {T}]`. The skeleton discards its first faces of cardinality `d+2`, so the graded vector spaces **and multiplications** of A and C agree through total degree `d+1`. Adjoining T changes nothing below degree `d+1`; the kernel M of `B -> C` has precisely the one-dimensional piece `F x_T` in that degree.

For a regular linear parameter sequence on A, the total-degree-`d+1` first Koszul-homology computation uses only degrees `d-1`, `d`, and `d+1`. Those complexes agree for A and C. Regularity therefore makes `H_1(Theta;C)_(d+1)=0`, while `M_d=0` makes `H_0(Theta;M)_(d+1)=M_(d+1)`. The exact sequence yields a genuine surviving extra class after quotienting. Thus B's quotient dimensions in degrees d and d+1 are `h_d(S)` and `h_d(S)+1` respectively. No unsupported pre-quotient monomial count is used.

The field restriction is handled correctly: the argument is conditional on regular parameters and later explicitly uses a rational-function field. The manuscript does not presume enough generic parameters over an arbitrary finite field.

### B. PL obstruction (lines 156–198)

Assume a PL embedding in the standard PL sphere. Ambient completion produces a finite triangulation P containing the original L. Generic coefficient columns are chosen simultaneously on all vertices of P. Restricting to S retains algebraic independence, and each full-facet determinant is a nonzero polynomial. The restricted parameters form an l.s.o.p. on the Cohen–Macaulay ring of S, hence are regular.

P is an F2 homology sphere, so the cited anisotropy applies over the chosen characteristic-zero rational-function field. If `ell u=0` in middle degree, then `ell u^2=0`; anisotropy forces `u=0`. Symmetric ambient Hilbert dimensions turn this injection into a surjection/isomorphism. The natural subcomplex quotient maps P's ring and parameter quotient onto L's. Any target in degree d+1 lifts upstairs and therefore inherits a preimage under multiplication by ell. That is incompatible with the strict dimension jump in A above.

The r parameters are deliberately overlong for L's `(d+1)`-dimensional face ring. The proof only requires a graded quotient there, not a regular sequence on L. The source manuscript explicitly preserves this distinction.

### C. Topological embeddings for d >= 3 (lines 200–221)

A compact d-dimensional polyhedron cannot be homeomorphic to the whole `2d`-sphere when d>0. A point outside a hypothetical embedded image can therefore be deleted. The normalized difference map of that embedding is continuous and equivariant on the full ordered deleted product. Its restriction also supplies a map on a simplicial deleted-product model if that convention is used.

The existence range `2m >= 3n+3`, with `n=d` and `m=2d`, becomes exactly `d>=3`. It includes `d=3`, and is weaker than the usual range for bijective isotopy classification. The argument uses only existence of some PL embedding. It does not claim the given possibly wild embedding is PL, approximable by embeddings, or isotopic to the resulting one. This gives the contradiction to B.

### D. The four-dimensional source and complement (lines 238–281)

The source-specific PL step is valid. Positive-dimensional face links have dimension at most two and, inductively, the required local sphere links and homology, so they are PL spheres. Vertex links are consequently closed triangulated homology 3-manifolds. A link loop can be moved radially into a small conical neighborhood contained in a punctured coordinate 4-ball, while that coordinate ball remains inside the punctured open star. Its contraction in the punctured ball retracts radially to the link. Thus the link is simply connected and is a PL 3-sphere by three-dimensional Poincaré and uniqueness. This supplies a combinatorial 4-manifold, not a globally standard PL sphere.

A legal bistellar support `B0=alpha*boundary(beta)` is a standard PL 4-ball. Its boundary is locally flat in the ambient combinatorial manifold: the boundary-vertex link pair is an embedded PL 2-sphere in a PL 3-sphere, where the three-dimensional PL Schoenflies theorem applies. The complementary closure C is therefore a compact collared PL manifold with boundary S3.

The collared decomposition of a topological S4 has connected intersection S3. Mayer–Vietoris gives connectedness of C; van Kampen then gives trivial fundamental group. The relative fundamental-class map has local degree ±1, so the pair sequence annihilates the possible degree-three homology as well as all other reduced homology. Simple connectivity plus acyclicity for this finite CW type implies contractibility by Hurewicz/Whitehead. No smooth or PL four-dimensional Schoenflies conclusion is smuggled into this argument.

### E. Common missing triangles: every transfer condition (lines 283–388)

The old support is induced: any subset of its vertices not containing all of beta lies in `alpha*boundary(beta)`, and anything containing beta is absent by legality. A triangle missing both before and after cannot be contained entirely in that support, since the only minimal nonface there is beta and beta becomes a face. Nor can it contain alpha: either it would already be a face, or one of its proper faces would disappear. This proves inducedness after augmentation and preservation of the removed-star condition.

All boundary edges of the common missing triangle lie in the complementary closure C. Contractibility gives an extension as a disk **map**. A collar makes its interior lie in the interior of C, and relative general position can keep its interior off the old 1-skeleton (`2+1<4`). An embedded disk is neither claimed nor needed. Consequently the missing triangle's image is disjoint from every vertex-disjoint support triangle. A boundary-fixed homeomorphism of the two move balls defines the second map, agreeing on the common complex. Combining the two maps on the finite abstract union and approximating simultaneously preserves all finitely many compact disjoint image pairs. It supplies the actual general-position maps and agreement needed by the transfer theorem, even if the puncturing homeomorphism was not PL.

There is an outside vertex, since an induced support ball exhausting the vertex set would equal the closed sphere. The outside vertex sets agree under insertion/deletion as well.

For a common boundary face rho, let W be the old support vertex set minus rho. The induced complex `Q[W]` is a cone because alpha minus rho is a nonempty simplex. Alexander duality makes its complement acyclic. Barycentric coordinate normalization outside W is a deformation retraction onto the induced deletion `Q-W`. Taking a 2-skeleton preserves H0 and H1, and adjoining one triangle cannot create either group. Thus every stipulated reduced H0/H1 vanishing holds. The same proof for the unaugmented skeleton supplies the homological cones with the exact support-avoidance condition. Cones can be chosen to be actual simplices whenever those simplices exist. These are precisely the structural and (I.a)–(II.b) requirements of the imported theorem.

### F. New triangles and the obstruction witness (lines 390–480)

The classification exhausts all move types. An old triangle becoming missing must itself equal alpha, giving the `(2,2)` move. A newly missing triangle that was not formerly a face must have a new proper edge, hence is beta plus an outside vertex for the `(3,1)` move. A new vertex in the `(4,0)` move has neighbors only on the support, where all such triangles are filled. Deletion of a vertex or edge cannot create a new missing triangle with all its proper faces present.

For `(2,2)`, the two augmented 2-skeleta coincide, so the old induction hypothesis transfers directly. For `(3,1)`, alpha has four vertices, beta has two, and adding the outside vertex v gives the seven formal vertices of the Flores 2-complex. The proposed map B on chains is a chain map: ordinary support faces are fixed; cone boundaries give the identities for triangles containing v; and the exceptional `v*beta` maps to M. Its two other boundary edges are old edges, so their prescribed cones are exactly those edges.

In the formal sum of all unordered disjoint triangle pairs, each edge–triangle boundary cell occurs exactly twice. Under B, at most one factor uses v, and its cone support avoids every support vertex outside its originating face. Thus the image pairs, including all boundary pairs, remain vertex-disjoint, and the image is a deleted-product 4-cycle. M has no accidental cone occurrence because cones lie in the old unaugmented skeleton. Its partner chain is exactly the boundary of alpha.

In the new move ball, the tetrahedron spanning `boundary(alpha)` and the beta interval can be placed in complementary 3- and 1-dimensional linear subspaces with a single transverse interior intersection. The other two edges of `boundary(M)` lead to the exterior vertex and do not enter the support-ball interior. This proves the mod-2 linking number one. The intersection–linking boundary identity makes the filling M contribute one against its sole partner chain, while all remaining disjoint pairs lie in the embedded unaugmented skeleton and contribute zero. Simultaneous sufficiently small approximations preserve the finitely many required separations and the linking number. Therefore the claimed obstruction evaluation equals one.

The independent exact finite check records 70 formal cycle terms and 210 boundary cells, each of multiplicity two. M's four partners are precisely the tetrahedral boundary. This checks the bounded combinatorics, not the topology or the universal transfer argument.

### G. Base, propagation, and low dimensions (lines 482–506)

The barycentric subdivision is flag because pairwise comparable faces form a chain; it has no missing triangles. The obstruction property holds there vacuously. It is PL homeomorphic to the original combinatorial 4-manifold in that manifold's own PL class. Pachner moves connect the two triangulations, all intermediates stay homeomorphic to S4, and the verified transfer handles every step. This avoids assuming the source is standard PL.

For d=1, an n-vertex triangulated 2-sphere has `3n-6` edges; adjoining a missing edge violates the planar simple-graph bound. For d=0, an actual vertex cannot be a missing singleton, so no case is omitted. The optional ghost convention is separate and does not alter the stated theorem.

## Strongest checked result and limits

The full topological nonembedding statement is supported for every stated d, with the stronger mod-2 obstruction assertion in dimension four. No substantive mathematical gap remains within this review. The original Weber scan's exact pagination was not authenticated on this run; the required mathematical existence statement and inclusive range were checked in the accessible alternate author-written proof instead. This retrieval limitation does not change the mathematical conclusion.

Novelty, journal suitability, and priority are separate judgments. In particular, this review does not promote an earlier conjecture into a claim that it remained globally open immediately before this manuscript. The proof uses substantial established theorems, and the public presentation should credit them and retain the unrefereed/AI-use disclosure.
