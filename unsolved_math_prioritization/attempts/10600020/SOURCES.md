# Sources and scope audit

Checked 2026-09-30. Source PDFs are cited, not redistributed.

1. **Exact original problem.** Fenn–Ilyutko–Kauffman–Manturov,
   *Unsolved Problems in Virtual Knot Theory and Combinatorial Knot Theory*,
   Banach Center Publications 103 (2014), 9–62. The complete item 20 is on
   printed p.32; Section 2.3 and Theorem 2.1 fix stable surface equivalence.
   [Published PDF](https://www.impan.pl/shop/publication/transaction/download/product/86155).
   The full PDF was available; the item was visually inspected. The corresponding
   [arXiv 1409.2823v1](https://arxiv.org/abs/1409.2823v1) PDF was also available.
   The published reference is Dye [36], the preprint reference Dye [32].
   The current arXiv record still lists the 2014 v1.

2. **Credited partial result.** H. A. Dye, *Non-Trivial Realizations of Virtual
   Link Diagrams*, [math/0502477v1](https://arxiv.org/abs/math/0502477v1).
   The entire 21-page preprint was read. Relevant passages are the warning about
   genus reduction on pp.2 and 10, Theorem 4.1 on pp.12–14, Theorem 4.2 on
   pp.15–16, Kishino's example on pp.17–18, and Conjecture 5.1 on p.19.
   Theorem 4.1 was visually inspected. Crossref confirms the published article
   in *J. Knot Theory Ramifications* 15(8) (2006), 963–981,
   [DOI 10.1142/S0218216506004890](https://doi.org/10.1142/S0218216506004890).
   The publisher PDF returned HTTP 403; no full published-version comparison is
   claimed. The explicit theorem numbering and proof audit use the full author
   preprint cited by the original question.

3. **Minimality and equivalence.** G. Kuperberg, *What is a virtual link?*,
   *Algebraic & Geometric Topology* 3 (2003), 587–591,
   [math/0208039v2](https://arxiv.org/abs/math/0208039v2),
   [DOI 10.2140/agt.2003.3.587](https://doi.org/10.2140/agt.2003.3.587).
   The complete five-page article was read, including the annular
   destabilization definition, Theorem 1 and its proof. This theorem concerns
   annuli in the product complement, not arbitrary disks in an ambient
   classical knot exterior.

4. **Conditional surgery input.** D. Gabai, *Foliations and the topology of
   3-manifolds II*, *J. Differential Geometry* 26 (1987), 461–478,
   [DOI 10.4310/jdg/1214441487](https://doi.org/10.4310/jdg/1214441487).
   Corollary 2.5 is stated on p.462 and repeated with proof on p.471. Its
   hypothesis is winding zero and noncontainment in a 3-cell in a solid torus;
   its conclusion excludes a solid torus after every nontrivial surgery.
   The full primary article was available as indexed PDF text at
   [this mirror](https://scispace.com/pdf/foliations-and-the-topology-of-3-manifolds-ii-4bywlfmfgl.pdf).
   The precise corollary, its proof, the surrounding Corollary 2.4, and the
   filling definitions were read. The local publisher download returned an HTML
   challenge and the mirror download returned an empty response; a requested
   PDF screenshot also failed. Consequently no successful local full-PDF or
   visual verification is asserted for this source. The deep foliation theorem
   is used as a prior theorem, not re-proved here.

## Current-literature and duplication checks

Targeted searches used the exact problem wording, Dye's title, minimal
unknotted realizations, null-homologous virtual knots, and Dehn-twist/surgery
terminology. No full resolution was located. Later surface-polynomial,
concordance, slice-genus and twist-family results returned by those searches
were not treated as solutions of the minimal-realization question. Search
absence is not proof of comprehensive literature coverage or priority.

The remote queue row was still queued 0/5 at rank 115. All local-ref history
for this attempt path, matching commit subjects, all-state PR searches for the
numeric ID/source code/title, related-target groups, and the pinned dataset
were checked. No previous Alec/campaign attempt or duplicate target was found.
The imported OPEN-TRIAGE report is upstream context, not a prior Alec attempt.

## Restrictions preserved

- Final surface genus remains minimal
- The supporting thickening is unknotted in three-dimensional space
- No passage to welded equivalence, crossing changes, or higher-dimensional
  surface embeddings is allowed
- No nonminimal crossing realization is promoted to a source solution
- The compression-circle test retains its nonsplit-link hypothesis
- No splitting disk is assumed to lie in the product complement
