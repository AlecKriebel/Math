# Independent audit: Hamiltonian-path tetrahedralizations

Problem 5500029 / AMR-054-0029 / TOPP 29. Audit date: 2026-10-10 UTC.

## Verdict

**ACCEPT THE STATED PARTIAL RESULTS. The unrestricted problem remains unresolved.**

No mathematical defect requiring a manuscript correction was found in the frozen candidate. Acceptance covers the degeneracy-safe degree-three reinsertion theorem, its minimum-degree-four reduction, the explicitly credited simplicial positive class, the seven-vertex failure of naive specialization, and the degree-four failure of one local replacement rule. It does not certify a general construction, a polytope counterexample, or novelty.

Public proof edition: [PROOF.md](PROOF.md), 17,111 bytes, SHA-256 `b2d676f76040f013b12a961f24bde43f552547860e34124ee8fa929adbdfc3a1`.

This is the publication edition of the recorded independent AI-assisted audit. The complete analytic review is retained. The accepted proof required no mathematical correction. Editorial changes reconcile acceptance, bind the public proof bytes, add the suggested Holton–McKay erratum reference, and distinguish historical source/computational observations from edition preparation. No mathematical computation or scholarly-source retrieval, visual inspection, or literature search was rerun during edition preparation. The manuscript and audit are unrefereed; external human peer review, journal acceptance, and formal proof-assistant certification are not claimed.

## 1. Exact target and scope

The input correctly fixes a full-dimensional convex 3-polytope, its original extreme vertices, positive-volume face-to-face tetrahedra, no Steiner points, and a Hamiltonian **path** in triangular-face adjacency. Coplanarity and nonsimplicial facets are allowed. Additional prescribed nonextreme points are not silently included in this target.

The live [TOPP 29 statement](https://topp.openproblem.net/p29), checked during this audit, asks the convex-polytope path question and still labels it open. The candidate does not replace it by a cycle problem, an arbitrary-point-set problem, or a general-position-only problem. The source page's compressed related-results description is not used to infer an unproved nonsimplicial small-vertex theorem.

## 2. Degree-three deletion and reinsertion

### 2.1 Deletion geometry

A degree-three vertex of a full-dimensional 3-polytope has a triangular vertex figure. Its three edge rays span a pointed, full-dimensional simplicial tangent cone. The stated affine normalization to the nonnegative orthant is therefore legitimate, including for nonsimplicial polytopes.

For every other vertex beyond the three named neighbors, the coordinate sum is strictly greater than one: a smaller or equal sum would express it as a nontrivial convex combination of the four named vertices. A vertex with exactly one positive coordinate would lie on an existing edge ray and would either fail to be extreme or make the purported neighbor nonextreme. Thus the opposite vertex q used later has at least two positive coordinates.

The plane of coordinate sum one exposes exactly the triangle abc in the deleted hull Q. Since there is at least one remaining vertex beyond this plane, Q is three-dimensional. Along a ray from v to a point x of Q, the crossing point x/s(x) is in abc and hence in Q. Convexity then proves both the union decomposition and its exact triangular intersection.

No vertex other than v disappears as an extreme point under deletion: extremality in the original hull implies extremality in the hull of a subset containing that vertex. Thus the induction never introduces a different prescribed point-set problem.

### 2.2 Replacement patch and intersections

The segment vq intersects abc at q/s(q). Consequently the cap tetrahedron and the tetrahedron behind abc have convex union U. This supplies the convexity that is unavailable in the later degree-four example.

The coefficient adjustment in the candidate is correct. Increasing the coefficient of q by r, decreasing each active coordinate coefficient by r q_i, and increasing the coefficient of v by r(s(q)-1) preserves the represented point and the sum of coefficients. All coefficients remain nonnegative when r is the minimum active ratio. An active coordinate coefficient vanishes, placing the point in one of the replacement tetrahedra.

For a point in the piece omitting e_i, the coefficient of q equals x_i/q_i and does not exceed any other active ratio. If the point also lies in the piece omitting e_j, those two ratios agree and the remaining coefficients show that the intersection is exactly conv(v,q,e_k). This is a common nondegenerate triangular face. It proves face-to-face intersection, not merely equal total volume. Positive q_i is exactly the nonzero-volume condition. The replacement dual is K3 or K2.

### 2.3 Flat boundary flip and all outside tetrahedra

This is the principal degeneracy-sensitive point, and the candidate's argument survives scrutiny.

If q_i=0, the omitted port lies in the supporting plane x_i=0. It cannot have a tetrahedron of Q across it. In that plane, the four vertices v,e_j,q,e_k form a convex quadrilateral because q_j,q_k>0 and q_j+q_k>1. The replacement changes only its internal diagonal, from e_j e_k to vq; its four boundary edges remain fixed.

It is insufficient in general to say only that there is no tetrahedron across a boundary plane: a diagonal can also be shared by other tetrahedra on the same side. The candidate explicitly handles this issue. In Q, the edge e_j e_k is the intersection of the new triangular facet abc and the facet in x_i=0. Near any relative interior point of this edge, the incident tetrahedron tau fills the entire local dihedral wedge of Q, since its two faces there lie in those two supporting facet planes. Any distinct positive-volume tetrahedron containing that edge would occupy a positive angular subwedge and overlap the interior of tau. This contradicts the old triangulation.

Nor can a distinct outside tetrahedron touch an interior point of the removed diagonal without containing that edge: its old intersection with tau was already a common face of the simplicial complex. No additional original extreme vertex lies in that edge's interior. Hence removal of the diagonal leaves no lower-dimensional nonconformity. Every other possible contact lies on preserved outer patch faces or on their preserved edges and vertices. The new boundary triangulation is therefore compatible with the whole outside complex.

### 2.4 Ports, path splicing, and reduction

Every old path edge incident with tau uses a distinct triangular port. Only boundary ports can be omitted, so every used port survives on a distinct replacement tetrahedron. K2 and K3 have a spanning path between any two distinct prescribed vertices; the endpoint and single-tetrahedron cases are handled separately. This proves the path conclusion without requiring a cycle.

Finite repeated deletion reduces the vertex count. It terminates at four vertices or at a full-dimensional polytope with no degree-three vertex. Every 3-polytope has minimum degree at least three, so a non-tetrahedral terminal core has minimum degree at least four. Reversing the deletions proves the sufficient reduction and the vertex-minimal-counterexample consequence. No converse for arbitrary deletion, or bound on core size, follows or is claimed.

## 3. Credited positive core classes

### 3.1 Boundary-dual face deletion

The stated lemma is valid for the Hamiltonian cubic planar graph arising as the boundary dual of a simplicial 3-polytope. In a planar embedding, the Hamiltonian cycle is a Jordan curve. Each noncycle edge is a chord on one of its two sides. Choose a chord of minimum cyclic endpoint distance and one shorter cycle arc between its endpoints.

The region on that chord's side bounded by the chord and selected arc has no other vertex in its interior, since every vertex lies on the Hamiltonian cycle. A chord inside this region would have both endpoints on the selected arc; a chord connecting an internal arc vertex to the complementary arc would have to cross the chosen chord. At the chosen chord's endpoints, cubic degree leaves no additional chord. Any chord wholly inside the region would therefore have strictly shorter cyclic endpoint distance, a contradiction. The region is a face. After deleting all its vertices, the remaining cycle interval is a Hamiltonian path, possibly a single vertex.

The use of cubic degree and the embedding is important. The audit does not extrapolate the informal shortest-chord sentence to arbitrary embedded graphs.

Coning a vertex v to all triangular facets not incident with v produces positive tetrahedra. Radial projection from v gives their coverage and face-to-face intersections. Their dual is exactly the boundary dual with the vertices of the face corresponding to v deleted. Nonfacial coplanar quadruples do not interfere with this construction.

### 3.2 At most twenty vertices

For a simplicial 3-polytope on n vertices, Euler's relation and triangular facets give 2n-4 boundary faces. Its boundary dual is a simple 3-connected cubic planar graph. Thus n≤20 places it within the published ≤36-vertex Hamiltonicity theorem. The credited corollary follows with exactly the stated simplicial qualification. It does not establish the same conclusion for every nonsimplicial polytope on twenty vertices.

The [author-hosted Holton–McKay paper with appended erratum](https://users.cecs.anu.edu.au/~bdm/papers/HoltonCubic38.pdf) was retrieved independently. Physical pages 1–3 and 16 were visually inspected. Theorem 1.1 on printed page 306 gives the ≤36 result. The appended 1989 erratum adds a case to Theorem 1.2's classification at orders 38, 40, and 42; it does not change Theorem 1.1. The original classification and its computation were **not** re-enumerated or fully re-audited here. The public proof edition includes the erratum citation, https://doi.org/10.1016/0095-8956(89)90025-7. This is a bibliographic improvement, not a mathematical correction.

### 3.3 Pyramids

A fan triangulation of a convex polygon has path dual. Coning it to a pyramid apex preserves the dual. This proves the unrestricted-size pyramidal class in the stated no-Steiner sense. In particular, the limiting pyramid below has a different Hamiltonian tetrahedralization.

## 4. Recorded independent verification of the seven-vertex family

This section describes checks performed during the original independent audit. Their analytic conclusions and exact geometric quantities are preserved below; generated certificate arrays and executable programs are not distributed. No such check was rerun in preparing this edition.

The independent verifier does not import the candidate checker. It derives all 35 determinants symbolically as 4×4 determinants using SymPy, checks that each polynomial has degree at most one, and checks its endpoint signs. A zero constant term is allowed only when the value at t=1 is nonzero; every other determinant has equal nonzero signs at both endpoints. This establishes nonvanishing throughout 0<t≤1, rather than inferring affine dependence from three numerical samples.

The hull facets throughout that interval are:

015, 016, 056, 123, 126, 135, 236, 345, 346, 456.

All seven labels occur as extreme hull vertices. The lower six-point hull has exactly the eight facets stated in the manuscript. Because every four-point orientation sign remains fixed, these supporting-face certificates persist throughout the interval.

For each of the 28 unordered tetrahedron pairs, the independent checker finds a plane through three input vertices separating the two tetrahedra into opposite closed halfspaces. On at least one side, the plane section is precisely their common vertex face. The corresponding orientation signs are among the 35 already certified signs, so every separation certificate is valid over the entire interval. This directly proves all pairwise face-to-face intersections for every parameter value in the interval.

In manuscript order, the eight positive six-times-volumes are:

240−24t; 80−12t; 120−28t; 80−12t; 29t; 32t; 20t; 24t.

Their sum and an independently computed supporting-boundary hull volume are both **520+29t**. Each tetrahedron is contained in the hull, and the pair certificates give disjoint interiors. Equal volume then implies complete coverage: a point omitted by the finite closed union would have a neighborhood meeting the full-dimensional convex hull in positive volume.

As a second exact method, rational Gaussian elimination enumerates vertices of intersections through barycentric inequalities. All pair intersections and total volumes were checked at t=1, 1/100, 1/3, and 3/4. These four checks are supporting redundancy; the full-interval proof uses the symbolic sign and separation certificates. The claimed Hamiltonian order passes independently.

At t=0, the first four tetrahedra have positive six-times-volumes 240,80,120,80 and exactly cover the pyramid, with all six pairwise intersections verified exactly. Their dual is K1,3. All 24 permutations were checked and none is a Hamiltonian path. Filtering the displayed perturbed path fails because its last two surviving tetrahedra share only two vertex labels.

An independent alternative limit triangulation, 6012, 6023, 6034, 6045, has path dual and covers the same hull with six-times-volume 520. Thus the fixture rejects precisely the naive keep-and-discard specialization rule; it is not a counterexample to the polytope existence problem.

## 5. Degree-four obstruction and global repair

The prescribed segment vq meets z=0 at (1/2,1/2,0), outside triangle acd. The local old and cap tetrahedra have combined six-times-volume 32, while the three proposed replacement tetrahedra have total 48. Independent exact arithmetic confirms both totals. Equal-volume replacement is therefore impossible, regardless of whether one separately checks overlaps.

The four tetrahedra around vq are all positive, meet face-to-face, and cover the full hull, whose six-times-volume is 64. Their dual is the four-cycle. This verifies the global repair and confirms that the example is an obstruction only to the proposed local induction step.

## 6. Recorded independent computation and controls

During the independent audit, an independently written checker used symbolic determinant calculation, rational Gaussian elimination for barycentric halfspace intersections, exact supporting facets and boundary volume, and direct graph search. It imported no candidate code. Every correctness check raised an explicit exception; Python assertions were not used. The programs and their raw generated outputs are not part of this edition.

The recorded ordinary and optimized-Python runs passed and produced identical substantive results:

- 35 full-interval determinant polynomials; 28 full-interval pair-separation certificates
- 112 exact rational tetrahedron-pair checks across four positive parameter values
- Exact limiting complex, exhaustive 24-order path test, and a valid alternative limit fan
- 102 rational nonnegative-coordinate patches, including 39 flat-boundary cases
- 456 ordered endpoint-port tests
- Full cube deletion and reinsertion, checking exact intersections, intermediate hull coverage, and path adjacency after each insertion; three of four reinsertions are flat-boundary K2 replacements
- Degree-four local failure and global cycle repair
- 137 labeled cycle-plus-matching planar examples on 4,6,8,10 vertices checking the shortest-chord face-deletion argument. These are finite guards for that lemma, not a rerun of Holton–McKay's classification.

Twelve mathematical/scope negative controls reject: a filtered nonpath, an omitted covering tetrahedron, a duplicate tetrahedron, flat tetrahedra treated as positive, general position at t=0, the incorrect degree-four volume replacement, and six target substitutions (arbitrary point sets, cycles, extra boundary points, Steiner points, general-position restriction, full-resolution status). Two independent frozen-input controls reject a changed proof hash and an omitted proof file. All fourteen controls also passed under optimization in the recorded audit.

Separately, during the recorded audit all functions of the supplied exact checker were rerun without invoking its output-writing main function. Their results matched the then-sealed evidence, including its nine controls. This historical reproduction is distinct from the independent checks and from edition preparation.

## 7. Recorded source audit and limits

These retrieval and inspection statements describe the proof review and audit on 10 October 2026. Edition preparation did not repeat source retrieval, visual inspection, or literature searching.

- [Escalona–Fabila-Monroy–Urrutia, arXiv:1210.5484](https://arxiv.org/abs/1210.5484): the supplied PDF's full extracted text was read; physical pages 3 and 7 were independently rendered and inspected for Lemma 3, Theorem 4, and Corollary 5. The predecessor and positive-class credit are accurate. The source assumes general position, while the candidate supplies its own degeneracy argument. The source's switches between path and cycle language are not imported into the candidate's explicitly proved path splicing.
- [Published journal article](https://link.springer.com/article/10.1007/s40590-015-0080-8): the accessible publisher abstract and bibliographic metadata were independently checked. They state the improved bound floor((m−2)/2)−1 and the general-position small-hull qualification. The subscription full proof was not accessed or inspected. No theorem here depends on proving the improved bound.
- The arXiv identifier has a 2012 v1 history. The supplied PDF carries an internal 2021 date. Those two facts do not establish a second arXiv version.
- The 84-point literature obstruction concerns tetrahedralizations sharing one vertex. It is not evidence against every tetrahedralization. No fresh proof audit of that entire construction or of the 92-vertex predecessor was needed for acceptance of the authored reduction and fixtures; copied third-party source files are not distributed.
- The Holton–McKay theorem is a credited prior input. Its exact statement and appended erratum were checked as described above; its entire proof and enumeration were not rerun.

This audit does not claim an exhaustive search of later literature, novelty of the reduction or examples, or a resolution for degree-at-least-four cores. The remaining task is exactly the unrestricted no-Steiner Hamiltonian-path existence problem on those cores.

## 8. Proof-only edition and acceptance boundary

[ACCEPTANCE.json](ACCEPTANCE.json) records machine-readable acceptance of the partial scope and exact identities of the public proof and this audit. [MANIFEST.json](MANIFEST.json) records the public member inventory and hashes. [SOURCE_METADATA.json](SOURCE_METADATA.json) and [SOURCE_REVIEW.md](SOURCE_REVIEW.md) retain public bibliography, source identities, and inspection limits.

The analytic degree-three reinsertion proof, positive-class arguments, and explicit shortcut obstructions are preserved. Historical finite checks are supporting aggregate metadata, not a claim that absent programs or certificate files can be replayed from this edition. The analytic verdict depends on no omitted program, raw output, or dataset. Programs, generated certificate arrays, raw outputs, datasets, copied third-party documents/images, and private coordination are excluded.

The unrestricted problem remains open in the recorded TOPP source and unresolved by this work. No novelty, exhaustive later-literature search, external human peer review, or full-resolution certification is claimed. The bibliographic erratum addition changes no mathematical conclusion.
