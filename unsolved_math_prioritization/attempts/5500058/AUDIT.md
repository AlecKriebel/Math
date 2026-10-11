# Independent audit: stripe-coloring partial construction for target 5500058

Audit date: 2026-10-11 UTC.

## Review and distribution status

AI-assisted and unrefereed, with an independent internal AI mathematical audit.
Acceptance is scoped to the stated partial theorem; it is not external human
peer review or formal proof-assistant certification. This is not a computational
reproduction package. The proof is self-contained. Programs, raw expanded cases,
datasets, copied source documents and source-derived images are not distributed.
Source hashes authenticate bytes, not correctness, novelty, or current status.
Editorial preparation performed no new mathematical program runs, scholarly
source-body inspection, or literature survey.

## Decision

**ACCEPT the stated sufficient criterion and the full-plane, fixed-coloring continuum corollary as a valid partial result.** No substantive mathematical gap was found. This is neither a proof nor a disproof of the universal three-color triangle problem. Novelty is not established; overlap with announced ICML 2025 stripe constructions is plausible and must remain disclosed.

The accepted original proof was 7,242 bytes, SHA-256 `35340484a8258b1587538fbb8d07515c709df8829629f04121c3547d65243012`. An earlier 7,234-byte version used equality rather than an upper bound in one sentence about a containing strip. The creator corrected that wording to “at most ell*w/2.” The correction strengthens presentation precision; the claimed inequality and theorem were already valid. This audit applies to the corrected original pin. PROOF.md is the public editorial
edition of that proof; its distributed identity is separately bound in
ACCEPTANCE.json and MANIFEST.json. All mathematical arguments are retained.

## Scope and quantifiers

The claimed coloring is exactly c(X,Y) = floor(400Y/77) mod 3, for all real X,Y. It is a single coloring that avoids every rigid or reflected copy of every triangle with vertices (0,0), (1,0), (x,y), where 849/1000 <= x <= 851/1000 and 349/1000 <= y <= 351/1000. The parameter rectangle includes all real points, not only rational ones. Its endpoints are included.

The original target remains universal over triangle shapes, with a coloring allowed to depend on the triangle. The partial theorem does not replace that quantifier with a finite grid, a sampled region, an almost-everywhere assertion, or a measurable-only question. No conclusion is obtained for all shapes, and no obstruction to arbitrary three-colorings is established by the failed stripe examples.

## Geometric proof checks

1. **Complete strip partition.** For h > 0, the intervals [jh,(j+1)h), j in Z, partition the full real axis, including negative coordinates and every boundary. Mathematical floor, rather than truncation toward zero, is essential.
2. **Separation is strictly greater than the gap.** For stripes with indices j and j+3q, q >= 1, vertical separation is greater than (3q-1)h and less than (3q+1)h. The strict lower inequality follows because the point in the lower stripe lies strictly below its upper endpoint. Thus distance <= 2h forces same-color B and C into the same stripe, and distance <= 5h prohibits same-color A and C being at least six stripe indices apart. Equality in either distance hypothesis is safe. No boundary case is omitted.
3. **Exhaustive placement reduction.** Because monochromatic indices differ by multiples of three, B,C share one stripe j, and A can only occupy j-3, j, or j+3. This covers every integer stripe index and all translations.
4. **Same-stripe exclusion.** A triangle of diameter L, actual projection span w0, and area Delta satisfies 2 Delta = ell*w0 <= L*w0, using the cross-section through a vertex of intermediate projected height. The cross-section lies inside the convex triangle, so ell <= L. Ties between vertex heights cause no difficulty: one of the two areas can be zero. A containing strip of width w only gives 2 Delta <= ell*w <= L*w, hence the wording correction. Here L=AB=1 and 2 Delta=y. Three points in one half-open stripe have actual span strictly below h, contradicting h <= y. Equality h=y is therefore covered as well.
5. **Both direction signs and both isometry determinants.** Any plane isometry has form p -> Qp+t with Q orthogonal, det(Q)=+1 or -1. Vertical differences equal u dot (p-q), where u=Q^T(0,1) is unit. If A is above the common B,C stripe, replace u by -u solely for this difference calculation. This does not presume that the coloring is invariant under reflection or that reflected half-open stripes have the same endpoint convention. After this sign choice, r=u dot (B-A)/h and s=u dot (C-A)/h satisfy 2<r<4, 2<s<4, |r-s|<1.
6. **Hexagon is complete.** The closure of these inequalities is the intersection of six half-planes. Independently enumerating every pair of boundary lines gives exactly (2,2),(2,3),(3,4),(4,4),(4,3),(3,2). There is no missing vertex or disconnected component.
7. **Unit-disk contradiction.** Solving the projection equations gives u=(hr,h(s-rx)/y). This is an invertible linear map because h,y>0. The image of the closed hexagon is the convex hull of the six images. If M is their largest norm and M<1, every convex combination has norm at most M<1. It therefore contains no unit projection vector. A bound at vertices is sufficient even though the quadratic expression need not be affine.

These steps are deterministic mathematical reasoning. Neither finite angular sampling nor neural-network output is used to prove avoidance.

## Exact continuum arithmetic

For each fixed (r,s), h^2[r^2+(s-rx)^2/y^2] is largest at the least allowed y, because its numerator term is nonnegative. Its x-dependent term is convex, so its largest value on the x interval is at one of the endpoints. This reduces the continuum maximization to exact endpoint arithmetic; checking corners is justified analytically rather than used as a sampling heuristic.

With h=77/400, the six maxima in the proof's order are:

- (2,2): 428672629/2436020000, at x=849/1000, y=349/1000
- (2,3): 1617437129/2436020000, at x=849/1000, y=349/1000
- (3,4): 9508390661/9744080000, at x=849/1000, y=349/1000
- (4,4): 428672629/609005000, at x=849/1000, y=349/1000
- (4,3): 391319929/609005000, at x=851/1000, y=349/1000
- (3,2): 4156282361/9744080000, at x=851/1000, y=349/1000

The maximum is exactly 9508390661/9744080000 < 122/125 = 0.976. The positive squared-norm margin below one is 235689339/9744080000.

The side bounds also match exactly:

- a^2 <= 73001/500000 < 5929/40000 = (2h)^2 < 1
- b^2 <= 423701/500000 < 5929/6400 = (5h)^2 < 1
- h < 349/1000 <= y

The side maxima use opposite x endpoints as appropriate: a uses the least x and greatest y, b the greatest x and y. These inequalities ensure AB really is longest throughout the entire closed rectangle.

The center's six squared norms were independently reproduced as 3509/20000, 13189/20000, 77561/80000, 3509/5000, 6413/10000, 34001/80000. At this point a^2=58/400, b^2=338/400, and the dot product at C is -1/200.

## Independent computation and negative controls

At the time of the independent audit, two newly authored checkers imported no creator code and used only Python's standard library and exact rational arithmetic. The following describes that historical verification; the programs and raw outputs are not distributed and were not rerun during editorial preparation:

- The independent arithmetic checker derives the hexagon, reproduces all claimed fractions, verifies all six stored negative witnesses, and constructs both determinant +1 and determinant -1 isometries for each witness. Every squared pair distance is checked before its stripe indices and colors are accepted.
- The independent projection-polygon checker uses a different exact decision method from the creator's rational-angle/SymPy code. For each allowable pair of same-color stripe offsets, it intersects rational half-planes in the projection-vector plane. A nonempty two-dimensional polygon's interior intersects the unit circle exactly when its minimum squared norm is <1 and its maximum squared norm is >1. Maximum norms occur at vertices; minimum norms are obtained at the origin, an edge's perpendicular projection, or a vertex. All are rational calculations. Lower-dimensional polygons have no strictly feasible strip placement.

The second method checks 13 noncollinear cases: six supplied test cases, all three supplied scaled-stripe certificates, and four parameter-rectangle corners. All expected decisions match, including the main center certificate. Corner decisions are a regression check only; the separate convexity argument proves the full continuum. The collinear case is excluded from this bounded-polygon algorithm and independently verified by its explicit rational witness instead.

Actual negative cases reproduced:

- Unit-leg right isosceles, h=1, 3 colors: indices (0,0,0)
- Unit-leg right isosceles, h=1/4, 3 colors: indices (0,-3,-3)
- Unit-leg right isosceles, h=2/3, 2 colors: indices (0,-2,-2)
- Flat triangle (0,0),(1,0),(1/2,1/10), h=1/10, 3 colors: indices (0,-6,-3)
- Skinny triangle (0,0),(1,0),(1,1/10), h=9/100, 3 colors: indices (0,-12,-12)
- Collinear triple (0,0),(1,0),(2,0), h=2/3: indices (0,0,0)

The flat-triangle witness in the prose is correct: projection (-3/5,-4/5), translation 9/100, heights (9/100,-51/100,-29/100). This is an exact counterexample to that stripe coloring, not to existence of every possible coloring.

The positive right-isosceles control at h=2/3 also has a short independent proof: each unit leg has length <=2h, forcing all vertices into one stripe if monochromatic; the minimum triangle width has square 1/2 > h^2=4/9, making this impossible. Deliberately invalid norm data and a floor-to-truncation mutation are rejected. These are real failures, not placeholder tests.

## Creator exact-checker review

The creator's exact stripe-decider source was historically read in full. Its pairwise residual constraints are equivalent to max(residuals)-min(residuals)<h, exactly the condition for a common translation into the required half-open stripes. The L1 projection bound yields a finite exhaustive offset range. The rational parametrization of the unit circle omits (-1,0), but no valid coloring failure can exist only at that point: all inequalities are strict, so feasibility is open in orientation and would extend to nearby parametrized points. The quadratic sign cases and rational witness construction are consistent with this logic. The creator's explanatory exact-checker note was also reviewed and separately pinned in the historical audit.

The audit did not execute any source-author code or depend on the creator's computational output as proof. The independent polygon procedure validates every noncollinear case in the creator's retained test-case and certificate files. No floating-point discovery result was promoted to a certificate. This is a mathematical and reproducible-code review, not machine-checked formalization in a proof assistant or a comprehensive software-security audit.

## Primary-source comparison and version limits

1. **Aichholzer and Perz, EuroCG 2019.** The official seven-page PDF at https://www.eurocg2019.uu.nl/papers/10.pdf was freshly retrieved. It exactly matches the supplied local PDF: 545,660 bytes; SHA-256 b80f4828852d28e4dab3d43812ec3a92784bffb776f1fcd358e09703e65190b7. Page 6, Theorems 3.1 and 3.2, respectively require b<=2y and nonobtuse angles with a>=1/2 for the three-color cases. The center has b>2y, a<1/2, and an obtuse angle, so neither specified theorem covers it. This comparison is correct and confined to those theorem statements.
2. **Mundinger, Zimmer, Kiem, Spiegel, Pokutta, ICML 2025 / PMLR 267.** Publication identity is verified on https://proceedings.mlr.press/v267/mundinger25a.html. Its linked official PDF, https://raw.githubusercontent.com/mlresearch/v267/main/assets/mundinger25a/mundinger25a.pdf, was freshly retrieved and byte-matches the supplied PMLR PDF: 7,518,011 bytes; SHA-256 48d3b8ae521103e6686357f737626693a992a62ce5732c509eb7f7b255b5a795. The independently opened publisher landing page agrees on title/authors/year. Pages 2, 5, and 9 were text-inspected, with Figure 4 and Section 4.4/Figure 8 visually inspected. The paper announces formalized additional stripe regions. Its Figure 4 appears to include the present center in an extra three-color region, but the visual reading does not prove exact containment of this particular rectangle or identity of the constructions. The paper's statement that separate papers are in preparation is a statement of that published version, not an independently verified claim that such papers remain unpublished on the audit date. Figure 8 reports a neural numerical threshold; it supplies no all-points avoidance proof or counterexample to Graham's conjecture.
3. **Axenovich et al., arXiv:2512.15516v1.** The version-pinned primary HTML https://arxiv.org/html/2512.15516v1#S1.SS4 was opened independently. Section 1.4 describes Graham's general <=3 conjecture and credits the 2025 authors for a large family. This supports the explicitly dated literature context; it is not an exhaustive October 2026 novelty/status search.

The arXiv and PMLR copies of the 2025 neural paper have different hashes and sizes and must not be conflated. This audit's primary 2025 comparison is the publisher-linked PMLR copy. Web PDF opening failed for that link, but a direct official-link retrieval succeeded, eliminating the byte-access limitation. Public retrieval and version metadata are retained in SOURCES.json.

## Allowed conclusion and remaining limits

The audited finite certificate proves an uncountable, positive-area family of full-plane avoidance constructions, including all boundaries, rigid motions, and reflections. It is a useful independently authored reconstruction/audit artifact. It does not resolve target 5500058, establish a new three-color region beyond all published or announced work, certify every result in the cited papers, prove global optimality of stripe widths, or rule out non-stripe colorings in any failed control.

The independent audit did not execute external source-author code. The accepted original proof included the one-line containing-strip wording correction described above.

## Final packet authentication

The creator's sealed MANIFEST.json has SHA-256 3e33cbee47f7bd2dbf385a62213776f5ba27e236f9acd4e86d8a9eb8f122aca5 (7,693 bytes). All 42 listed members were independently rehashed and their byte counts matched. The creator manifest explicitly excludes generated __pycache__ directories; this is authentication of its listed inventory with that exclusion, not a claim covering every regular file. That authenticates the retained packet; it does not mean all its historical search and literature claims were independently re-performed. This review's mathematical acceptance remains pinned specifically to the proof above and the stated verification scope.

This edition distributes only authored mathematics, the full mathematical audit, scoped acceptance, and allowed public verification metadata. The original evidence inventories also include source PDFs and page renders, which are not distributed. Authentication of an inventory does not expand distribution permission.
