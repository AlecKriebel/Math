# Source audit: 30002298 / OWR-12339-004

Checked 2026-09-30 with gpt-6-astra at xhigh reasoning.

## Prior-attempt gate

The assigned row was rank 72, queued, 0/5. No earlier project attempt, matching branch or all-state pull request was found. The attempt path's git history, the repository histories and assessment/reset records, and the related-target groups were checked. A search of the pinned dataset for Fantappiè and related moment/polytope questions found no exact duplicate. The pinned report dictionary has no report for this problem code.

The public problem page could not be retrieved. The full pinned statement and the complete official source contribution were nevertheless read. No shared queue, state, catalog, or historical review was edited.

## Full original source

[Structured Function Systems and Applications, OWR 11/2013](https://ems.press/content/serial-article-files/46446), DOI [10.4171/OWR/2013/11](https://doi.org/10.4171/OWR/2013/11), pp.579–655. Dmitrii Pasechnik's contribution, “Rational moment generating functions and nonconvex compact polyhedra,” occupies pp.637–640. Question 1 is on p.638. The complete contribution, its references and the rendered question page were inspected.

The important source conventions are:

- Unit Lebesgue density and the normalized exponent $d+1$, not an arbitrary density or the unmodified exponent-one transform
- A compact polyhedron is a finite union of convex polytopes
- $V(P)$ is the intersection of triangulation vertex sets
- The denominator is reduced, as confirmed by the explicit cancellation example

Questions 2–3 on signed decompositions and spanning assumptions are separate questions. This package does not claim to resolve them.

## Published characterization

Akopyan–Bárány–Robins, [“Algebraic vertices of non-convex polyhedra”](https://arxiv.org/abs/1508.07594v2), *Advances in Mathematics* 308 (2017), 627–644, DOI [10.1016/j.aim.2016.12.026](https://doi.org/10.1016/j.aim.2016.12.026). The complete 13-page author manuscript was read, including Definition 1, Theorem 1, the proof of Lemma 6, and Remark 10. The latter explicitly links the Fantappiè denominator vertices to the local algebraic-vertex definition. Its page was inspected visually.

The arXiv record verifies the authors, version dated 5 January 2017, journal reference and DOI. The publisher's indexed abstract and the author's [research bibliography](https://sites.google.com/site/sinairobins/research) corroborate publication. Direct publisher access returned 403; no publisher PDF is presented as read. The open author manuscript supplies the full mathematical text used here.

The source distinguishes several notions of nonconvex vertex. The package consequently proves the needed inclusion $A(P)\subseteq V(P)$ directly for the original triangulations; it does not silently equate triangulations, non-face-to-face dissections, convex-hull vertices, and algebraic vertices.

## Transform identities

Gravin–Pasechnik–Shapiro–Shapiro, [“On moments of a polytope”](https://link.springer.com/article/10.1007/s13324-018-0226-8), *Analysis and Mathematical Physics* 8 (2018), 255–287, DOI 10.1007/s13324-018-0226-8. The full publisher HTML and the [open author manuscript](https://arxiv.org/pdf/1210.3193v2) were consulted, particularly Theorem 2, equation (1.9), Corollary 3, and the discussion of vertex conventions and cancellation.

Equation (1.9) fixes the sign convention in the cone coefficient used in SOURCE_STATUS.md. The package uses the unit-density simplex identities, and does not infer higher-density multiplicities from an abstract or extend the assigned target to polynomial densities.

## Normalization, scope and checks

The published identification is unpacked with an explicit rational-pole calculation. It treats the origin separately because its nominal affine factor is the unit 1. Thus literal equality of denominator polynomials does not detect an invisible origin vertex. The exact checker verifies this through the source's pair of opposite tetrahedra, both centered at zero and translated away from zero.

All 284 assertions in the final checker pass using SymPy 1.14.0 and exact integer/rational algebra. No floating-point tolerances are used. These are 14 small examples in dimensions 1–3; they do not substitute for the general published valuation result. The code writes its receipt beside itself.

Title and topic searches found no correction invalidating the cited characterization. This is a bounded current-source search, not a claim to have exhausted the bibliography.

The exact characterization is credited to prior published work. No new substantive proof-search attempt or historical-priority claim is recorded. Separate adversarial review is required before a draft PR.
