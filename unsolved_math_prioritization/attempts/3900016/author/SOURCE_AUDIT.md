# Source and readiness audit

Research date: 8 October 2026 UTC. Numeric target: 3900016, AMR-038-0016.

## The target source

The [original problem preserved by the Geometry Junkyard](https://ics.uci.edu/~eppstein/junkyard/tri-diff-areas.html) was read in full. It attributes the question to Eddie Grove in 1990. Its three-dimensional lattice restriction is materially more specific than merely having integer planar coordinates. The [current open-problem index](https://ics.uci.edu/~eppstein/junkyard/open.html) still lists the item. An old index entry establishes the historical formulation, not the absence of a later solution.

The earlier classification report was literature-only triage. Its assertions that unspecified nontrivial general and lattice bounds were known did not supply verifiable references or numerical statements. Those assertions are not accepted as established literature facts. REPORT.md instead proves its displayed partial bounds directly and makes no best-known or novelty claim. The attribution and lattice-scope corrections are contextual corrections; no third-party source text is reproduced.

## Related work distinguished from this question

- Dumitrescu, Sharir, and Toth, [Extremal problems on triangle areas in two and three dimensions](https://adriandumitrescu.org/area.pdf), manuscript dated 1 October 2007. Its abstract and introduction concern area statistics of all triangles spanned by a finite point set. The inspected statements do not guarantee that selected triangles coexist in one vertex triangulation. Parsed text of the opening pages was inspected, not the complete proofs. A direct local request returned a non-PDF challenge page; no locally verified PDF hash or size is claimed.
- Jin, Zhu, and Luo, [A technique for solving the polygon inclusion problems](https://arxiv.org/abs/1707.04071v7), arXiv v7, revised 21 April 2024. The current abstract concerns optimization of individual enclosing or inscribed triangles. Only the abstract and version history were inspected. A maximum-area triangle algorithm does not itself solve the distinct-area triangulation problem. REPORT.md does not import an algorithmic theorem from this paper.

All external links are citations and identification aids, not claims that these works resolve the target.

## Search limits

Focused searches included the exact problem title and URL slug, Eddie Grove with triangulations, and combinations of convex polygon, triangulation, distinct areas, different triangle areas, and repeated areas. They returned the original problem, mirrors/index entries, and adjacent triangle-area literature. No verified full resolution of the exact target was found. This was a bounded web review, not a comprehensive bibliographic search or a certificate that the problem remains open everywhere.

The supplied exact joined record and a bounded corpus/repository cross-reference screen did not identify an inherited substantive same-target proof attempt. Near matches concerning area polynomials, lattice-triangulation flip mixing, and equal-area graph embeddings address different quantifiers or objects. Absence in those screens is not global absence. Corpus hashes and byte counts are recorded solely as verification metadata in SOURCE_MANIFEST.json; corpus contents are excluded.

## Accepted scope

The polygon vertices are extreme vertices, triangulations use no Steiner vertices, and the bounded lattice class is explicitly defined in REPORT.md. If a different convention permits collinear listed boundary points, it is a different domain requiring separate analysis. No linearly growing bound, optimality of the supplied asymptotic bound, complete small-lattice classification, or resolution of forced triple repetition is asserted.
