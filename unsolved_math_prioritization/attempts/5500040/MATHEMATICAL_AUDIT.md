# Independent audit of pointed pseudotriangulation counts

## Verdict and public proof edition

**PASS AS AN UNRESOLVED PARTIAL RESULT.** The exposure-witness sufficient-condition theorem, the six-point obstruction to universal containment maps, the one-interior-point fiber identity, and the general weighted-refinement identity are correct. No mathematical defect or required correction was found. The universal inequality remains unresolved by this work. Acceptance does not mean a proof, counterexample, novelty finding, or comprehensive literature-status certification for the universal problem.

Public proof edition: [PROOF_PARTIAL.md](PROOF_PARTIAL.md), 13,110 bytes, SHA-256 `6a409ad91bbdc7a1ec5dddc830d1690c8b5e8397ab8bb79f6136c3bbde527f18`.

This is the publication edition of the recorded independent AI-assisted audit completed on 10 October 2026. The complete analytic audit is preserved, including its independent analytic 11/25 count. The original proof required no mathematical correction. This manuscript and audit are unrefereed; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

All source inspection, determinant recomputation, finite enumeration, program comparison, and negative-control descriptions below are historical observations from that audit. Edition preparation reran none of those checks, retrieved no scholarly sources, and performed no source-file rehash, visual inspection, or new literature search. Programs, generated detailed certificates/results, copied sources, and fixture datasets are excluded. Their recorded aggregate outcomes are supporting metadata; the analytic verdict depends on none of those omitted materials.

## 1 Exact quantifiers and definitions

The proof works with a fixed finite planar point set S in general position, n at least 3, fixed original hull H, interior set I, straight segments, no Steiner points, and distinct edge sets as distinct objects. Its inequality is per point set. It does not substitute a minimum across different point sets or an upper comparison for the requested lower comparison.

The strongest authored conclusion has the additional geometric hypothesis that every interior point has at least one original-hull exposure witness. The product multiplier uses the cardinalities of those specific witness sets. The six-point counterexample refutes only a stronger strategy. The proof consistently preserves these distinctions.

## 2 Exposure lemma and injection

If p is extreme in S minus q, a strict supporting direction at p places every remaining point other than p in one open halfplane. Therefore the incident rays of any graph omitting pq lie in an open halfplane. Such a p is pointed. Contraposition forces pq at a nonpointed p; deleting pq leaves pointedness. General position permits the strict separation used here.

Every interior vertex of a triangulation is nonpointed, so every member of the fixed geometric set F of witness edges occurs in every input triangulation. This also excludes crossing pairs in F. Each deletion choice joins one interior point to an original hull point. Hence deletion edges for distinct interior points differ, and deleting another point's chosen edge cannot change the ray set at p. The number of removed edges is exactly |I|. The remaining graph is crossing-free and pointed at every vertex, with (2n+|I|-3)-|I| = 2n-3 edges.

The needed structural input is exactly the equivalence between items (2) and (4) of Theorem 2.7 in Rote, Santos and Streinu's [survey](https://arxiv.org/abs/math/0612672). It concerns the given embedding. Neither connectivity nor simple faces needs a separate unproved inference. Physical PDF page 9 was inspected visually; page 8's Theorems 2.5 and 2.6 also justify the maximal-extension explanation. The survey attributes Theorem 2.7 to Streinu, reference [63]. The theorem is not the weaker assertion that an abstract Laman graph admits some suitable realization.

Finally F is independent of the input, F is contained in every T, and the deleted D is contained in F. Thus P union F equals T and F minus P equals D. Each edge of D identifies its unique interior endpoint and hence its witness choice. Both triangulations and their independent witness choices are recovered. The product-multiplier injection is therefore valid. The convex case is included through the empty product and empty deletion set.

This argument is analytic and does not depend on any finite computation. It covers arbitrary sizes under its stated hypothesis, with no assertion that arbitrary point sets satisfy that hypothesis.

## 3 The wheel obstruction

For the five listed hull points and p=(0,0), all twenty triple determinants were recomputed independently. The determinant against each directed hull edge is positive for every other point. This verifies the hull order, strict convexity, interior position of p, and nondegeneracy of the coordinate example.

The adjacent-spoke determinants are (4,5,7,11,6), and the skip-one-spoke determinants are (5,2,4,5,4), exactly as stated. The wheel has ten edges. Any contained PPT has nine and must retain the five hull edges, so only a single spoke can be deleted. Original angular gaps are in (0,pi). A merged pair of gaps lies in (0,2pi); its positive determinant places it in (0,pi). Thus no deletion makes p pointed. There is no contained PPT.

The consequences for a universal containment injection and containment-only Hall matching follow already from this one empty fiber. No conclusion that ppt(S)<t(S) follows. The obstruction is a valid exact analytic proof even if every program and count is removed.

The existence of triangulations with no contained PPT is prior knowledge. [TOPP 50](https://topp.openproblem.net/p50) records that fact and references O'Rourke's 2002 column; the package correctly claims only its own coordinate certificate, not discovery of the phenomenon.

### An additional analytic count check

For this central pentagon, the hull triples containing p are exactly 013, 023, 024, 124, and 134. The three spoke determinants around each of those triples are positive; each of the other five triples has a negative one. Each containing triple has two boundary arcs with one unused hull vertex apiece, and the third arc has none, so it admits a unique triangulation with exactly those three spokes. This gives five degree-3 triangulations. Each of the five choices of four spokes admits one triangulation, filling the single skipped-hull-vertex cap. All five spokes give the wheel. Thus t=5+5+1=11.

By the one-interior fiber calculation below, these contribute 5*3 + 5*2 + 1*0 = 25 PPTs. Consequently the stated 11/25 count and 0:1, 2:5, 3:5 containment histogram also have a short analytic verification, independent of the enumerators.

## 4 One interior point and general refinements

In a PPT with one interior point, no hull vertex can be reflex in a bounded face. The sole interior point contributes one reflex angle. Each pseudotriangle has exactly three convex corners, so the unique face with that reflex angle is a quadrilateral; every other bounded face is a triangle. A simple concave quadrilateral has exactly one internal diagonal. This proves existence and uniqueness of a triangulation refinement.

Conversely a PPT contained in a triangulation differs by one edge, which must be a spoke. Removing spoke j merges two incident triangle angles. The endpoint p becomes reflex exactly when their sum exceeds pi. General position excludes equality. Thus the stated d_p(T) formula counts the fiber exactly. For k=3 every sum is 2pi minus the remaining angle and exceeds pi, so d=3. For k=4 opposite pair-sums add to 2pi, and neither equals pi, so exactly two succeed. The five-spoke wheel gives d=0. A universal termwise lower bound fails.

The positive Catalan difference for arbitrary one-interior-point sets is already [Randall, Rote, Santos and Snoeyink's wheel theorem](https://page.mi.fu-berlin.de/rote/Papers/abstract/Counting%2Btriangulations%2Band%2Bpseudo-triangulations%2Bof%2Bwheels.html). Corollary 5 on physical PDF page 3 was inspected visually, and the shifted notation was checked on page 2: their C_n is the standard Catalan C_(n-2). The package correctly credits this global compensation instead of claiming it as an authored result.

For general S, every simple pseudotriangle admits a triangulation with the same vertices. Triangulating each bounded face yields at least one full triangulation refinement. All sets are finite. Giving each incidence (P,T) weight 1/R(P) and summing first over T or first over P proves the general identity. The wheel demonstrates that an individual inner sum may be zero. The necessary lower bound on its average is explicitly left unproved. Nothing in the audit supplies that missing global compensation.

## 5 Recorded independent exact enumeration and controls

The recorded independently written checker imported no original enumeration code. It used the earlier coordinate fixtures and enumeration evidence, with a different search and pointedness test:

1. Directed strict supporting edges determine the hull.
2. A Bron-Kerbosch search enumerates maximal cliques in the noncrossing-edge compatibility graph. These are all triangulations; every generated edge count is checked.
3. From every triangulation, all deletions of r nonhull edges are visited for each 0<=r<=|I|. Every pseudotriangulation is included in this search because it has a triangulation refinement and its edge-count deficit is its number of pointed interior vertices.
4. An interior vertex is nonpointed exactly when some triangle of its neighbors strictly contains it. This is an exact Caratheodory/convex-hull test, independent of the earlier halfplane ray test. General position excludes the two-point boundary case.
5. A crossing-free graph with exactly 2n-3 plus its number of nonpointed vertices is a pseudotriangulation: extend it maximally without changing pointed vertices and use survey Theorems 2.5 and 2.6. The extension cannot increase the edge count. This also justifies classification of intermediate pointedness layers.

In those recorded checks, all 7,527 pseudotriangulation edge sets, with all their pointed-vertex sets, matched exactly. The independent search examined 40,769 distinct candidates across the eight fixtures. It independently checked the fixed-edge inverse, collision freedom, witness sets, refinement multiplicities, one-interior unique refinement, Catalan differences, and exact rational weighted identities.

| Fixture | Triangulations | PPTs | All pseudotriangulations |
|---|---:|---:|---:|
| convex_pentagon | 5 | 5 | 5 |
| one_interior_triangle | 1 | 3 | 4 |
| one_interior_quadrilateral | 3 | 8 | 11 |
| central_pentagon_wheel | 11 | 25 | 36 |
| two_interior_triangle | 2 | 13 | 25 |
| three_interior_triangle | 6 | 71 | 208 |
| two_deep_interior_pentagon | 34 | 148 | 322 |
| two_ear_chains | 80 | 1476 | 6916 |

The independent canonical collection of edge sets has SHA-256 `5755bc1e3c11e5e4e555be708cd5e1c8a835f4998a3452d6c65aefff51fe5e0b`. This is a supplemental audit hash, not the original detailed JSON hash.

The recorded independent normal and optimized runs produced identical evidence. Independent controls preserve wheel counts under an invertible affine map, reflection, label reversal, and integer scaling by 10^30, while rejecting collinear, repeated, floating-point, and Boolean coordinates. The supplied enumerator was also rerun in both modes; both detailed outputs match the original 14,196,007-byte JSON exactly. The supplied seven controls passed again in both modes.

These are checks of the eight stated coordinate fixtures, not all order types, larger untested point sets, or a substitute for a universal proof.

## 6 Recorded bibliography and current-status boundaries

- [TOPP 40](https://topp.openproblem.net/p40) identifies the precise comparison problem, displays it as open, and records the stronger equality-only-in-convex-position companion. Its old revision history means the page is not a comprehensive current literature survey.
- [Aichholzer, Orden, Santos and Speckmann](https://arxiv.org/abs/math/0601747) is arXiv version 2, June 14, 2007, with journal publication in JCTA 115 (2008), 254–278. The full local paper supports the family credits: Lemma 2 and Section 2 for almost-convex sets including double circles; Lemma 5 for single chains; Theorem 18 and Corollary 19 for double chains. The stronger monotonicity assertion is their Conjecture 1 and is not assumed by the authored theorem. The single-chain proof already uses a forced-tip-edge idea; the package's explicit no-novelty claim is appropriate.
- [On Numbers of Pseudo-Triangulations](https://arxiv.org/abs/1210.7126) is by Moria Ben-Ner, André Schulz and Adam Sheffer. Both the live arXiv author list and retained title-page image verify the correction. It is not a Sharir–Sheffer paper. The arXiv submission date of October 26, 2012 and printed PDF date of November 21, 2021 were checked separately. Section 5, physical page 14, restates the lower comparison conjecture; Theorem 2.3 is an upper factor-three comparison between pointedness layers. The authored work does not reverse that bound.
- The Rote–Santos–Streinu survey is version 2 of October 17, 2007. The structural theorem is accurately identified and used in its given embedding.
- The wheel theorem is attributed to all four authors, with CCCG 2001, pages 149–152. The retained author-hosted PDF is the longer eight-page version; its Corollary 5 supports the identity.
- TOPP 50 supports the credited pre-existing containment obstruction. No copied source prose is needed for the authored proof.

Direct public-page checks and a bounded arXiv/TOPP search during this audit located no resolution that changes the packet's status. This supports accepting its cautious statement that no resolution was located; it does not certify exhaustive knowledge of all later literature.

## 7 Acceptance boundary and distribution

Accept this package as rigorous partial progress with no claimed novelty and an unresolved universal target. Do not label it SOLVED or COUNTEREXAMPLE. No correction patch is required. Keep the finite fixtures, already-known family results, and analytic sufficient-condition theorem distinct.

The accompanying README.md describes this proof-only edition. ACCEPTANCE.json binds the exact public proof and audit bytes and records the prior aggregate checks. SOURCE_REVIEW.md and SOURCE_METADATA.json retain public bibliography, source identities, and historical inspection limits. MANIFEST.json inventories the eight public documents. No commands, programs, generated detailed certificates/results, copied third-party PDFs or source text, fixture datasets, or private coordination are distributed. This edition makes no packaged computational reproducibility claim; all analytic arguments and mathematical qualifications remain in full.
