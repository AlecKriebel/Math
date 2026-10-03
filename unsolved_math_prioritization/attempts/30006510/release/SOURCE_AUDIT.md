# Source, scope and prior-work audit

Checked 3 October 2026. This file is authored provenance, not a copy of the source corpus.

## Problem recovery

The requested problem page, https://www.unsolvedmath.com/problems/30006510, was attempted first through the web tool; it was inaccessible. A subsequent direct read returned HTTP 403. The pinned problem record supplied the identifier OWR-14299586-001 and report DOI. Its adjacent-formula extraction was not treated as reliable mathematical typesetting.

The original report PDF was successfully read. Printed p. 3046 was also rendered and visually inspected. The problem is in Anna Gusakova's contribution, not a theorem attributed to the report's organizers. The report is numbered 57/2025 and the workshop ran 7--12 December 2025. A 2026 publication/catalogue date does not change that workshop date.

The operative assumptions are locally finite, countable, full-dimensional closed convex cells, disjoint interiors and covering hyperbolic space, with full-isometry invariance for the intensity/Palm discussion. The source explicitly distinguishes the unavailable center for infinite-volume cells from the broader question about unbounded cells. The question is open-ended: it does not prescribe axioms that make our restricted no-go result a complete negative solution.

Source: [OWR report](https://ems.press/content/serial-article-files/52444), pp. 3046--3047; [DOI](https://doi.org/10.4171/owr/2025/57).

## Foundational and recent primary sources

1. **Bühler--Gusakova--Recke, arXiv:2512.19425v1 (22 December 2025).** Read the typical-cell discussion, Theorem 2.1, Lemma 2.2 and the paragraph following its proof. Theorem 2.1 supplies the finite-marginal MTP used here. Lemma 2.2 already excludes an invariant one-point representative of infinite-volume components. Our probability-kernel formulation is a direct extension of that argument and is not claimed novel. The paper's model-specific equivalence between its unbounded and infinite-volume behavior is not imported as a statement about arbitrary convex cells. [Paper](https://arxiv.org/abs/2512.19425).

2. **Günter Last, Stationary random measures on homogeneous spaces.** Read the 18 July 2008 author manuscript, particularly Section 8 and equations (8.11), (8.14), (8.15). The published citation is *J. Theoret. Probab.* 23 (2010), 478--497. The reciprocal-volume identity, proper stationary partitions, and the role of unimodularity predate this attempt. We give a self-contained transport proof tailored to the finite-volume subcollection; no novelty is claimed for Palm inversion. [Author manuscript](https://publikationen.bibliothek.kit.edu/1000012083/1022543).

3. **D'Achille--Curien--Enriquez--Lyons--Ünel, arXiv:2303.16831v3 (10 June 2025).** Read the face-Palm setup and Section 5.3. A typical ideal cell is already constructed from a Poisson ideal nucleus on a marked corona, using Palm disintegration with noncompact isotropy. The source's comparisons on the isometry-invariant sigma-field must not be promoted to a universally centered embedded cell law. This valid special construction is included as prior work, not represented as our discovery. [Paper](https://arxiv.org/abs/2303.16831).

4. **D'Achille--Thäle, arXiv:2606.26049v1 (24 June 2026).** Read Section 2, especially the paragraph before Corollary 2.4. The paper separates usual typical full-dimensional IPVT cells from bounded lower-dimensional faces with ordinary positive finite counting intensity. It does not establish a general full-cell construction for arbitrary invariant tessellations. [Paper](https://arxiv.org/abs/2606.26049).

5. **Besau--Gusakova--Thäle, arXiv:2609.10007v1 (9 September 2026).** Read the abstract and model overview to check a recent potential status change. A chosen horoball supplies an ideal direction; projection produces a stationary Euclidean tessellation. Its intensity and typical-cell conclusions concern that structured projected model. We do not use any of its technical results in our proofs. [Paper](https://arxiv.org/abs/2609.10007).

Only primary literature supports the mathematical claims. General web search results were discovery aids. Failure to find a solution is not a proof that none exists; the recommendation is that this attempt has not solved the source problem.

## Genuine prior-attempt check

Read the current main queue row: rank 501, identifier 30006510, queued, 0/5 at the time of checking. Checked the main attempts directory listing, exact-ID PR search, exact-ID branch search, title/topic PR searches, and branch searches for "typical" and "hyperbolic." No attempt matching this mathematical question was found. Default-branch code search returned no useful hits and is not treated as an exhaustive history guarantee.

Two keyword hits were examined and are mathematically different:

- [PR 284](https://github.com/AlecKriebel/Math/pull/284), problem 30001080: a characterization of mass-stationarity by transports in an Abelian-group framework, rather than typical cells for hyperbolic infinite-volume tessellations.
- [PR 340](https://github.com/AlecKriebel/Math/pull/340), problem 30002957: finite Delaunay-face proportions and a Palm sampler, rather than an extension of full-dimensional cell intensity.

The pinned catalogue also has a high-intensity hyperbolic Voronoi crossing problem (10000055) and a finiteness question for hyperbolic tessellation groups (30003834). Their statements are mathematically different, not duplicates under another name. The exact target had no matching prior research-result entry in the pinned research-results map.

## Claim discipline and exclusions

- Retain the original as unsolved, with five substantive approaches.
- No novelty claim is made for the median principle, Palm identities, MTP obstruction, mean measure, lattice randomization, or boundary dynamics.
- Theorems in `RESULT.md` are scoped partial statements with proofs; finite arithmetic controls do not certify continuous geometry or historical status.
- Source PDFs, full extracted text, screenshots, the catalogue/corpus, access logs and private coordination are excluded from the public candidate directory.
- The author packet is frozen for independent review and does not itself authorize publication.
