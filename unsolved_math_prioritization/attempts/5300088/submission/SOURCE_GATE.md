# Source and scope gate

Checked 2026-10-04. Target 5300088 / AMR-052-0088, queue rank 633.

## Exact source

The initial catalogue URL, https://www.unsolvedmath.com/problems/5300088, was inaccessible through web retrieval. The selected record was recovered from the pinned catalogue and checked against the primary source: Ben Bielefeld (editor), *Conformal Dynamics Problem List*, Section 5, printed page 12, arXiv:math/9201271. This is the 1990 list of questions from the November 1989 conference. The original is an upper bound for every ball wholly contained in the convex core, depending only on the number of generators. It does not ask for a sharp value or the existence of a large ball. The relevant source page was visually inspected.

Primary source: https://arxiv.org/pdf/math/9201271#page=12

## Hypothesis audit

- Dimension: three. Curvature: hyperbolic, normalized to -1. Rescaling arbitrary curvature would alter the question.
- Complete manifolds and finitely generated fundamental group; the source is in the orientable Kleinian setting. The orientation-cover reduction in `PARTIAL.md` handles the broader reading.
- No global lower injectivity bound, cocompactness, convex-cocompactness, finite volume, fixed topology, or incompressible boundary is given.
- Balls must be contained entirely in the core. Merely centering them there is insufficient, including for full-dimensional cores.
- Closed manifolds are a genuine subcase and have no core boundary to exploit.
- Elementary or lower-dimensional cores are harmless for this three-dimensional embedded-ball quantity.

## Primary literature actually checked

1. Matthew E. White, *Injectivity Radius and Fundamental Groups of Hyperbolic 3-Manifolds*, arXiv:math/0104191. Introduction and Theorem 4.4: closed manifolds; the injectivity radius is the global minimum. The first page was visually checked. https://arxiv.org/pdf/math/0104191
2. David Bachman, Daryl Cooper, Matthew E. White, *Large embedded balls and Heegaard genus in negative curvature*, Algebraic & Geometric Topology 4 (2004), 31-47; arXiv:math/0305290. Theorem 1.1 gives the unconditional cosh(r)<=2g estimate for closed orientable connected manifolds. We do not use its conditional sharper version. https://arxiv.org/pdf/math/0305290
3. Carol E. Fan, *Injectivity Radius Bounds in Hyperbolic Convex Cores I*, arXiv:math/9907058. Corollary 5.1 is a rank bound for the book-of-I-bundles case; Remark 5.2 supplies the warning about ambient injectivity at core points. The relevant concluding pages were text-checked and page 21 visually checked. https://arxiv.org/pdf/math/9907058
4. Brian H. Bowditch, *An upper bound for injectivity radii in convex cores*, Groups, Geometry, and Dynamics 7 (2013), 109-126, DOI 10.4171/GGD/178. Theorem 0.1 depends on compact-core topology; Theorem 1.1 uses triangulation complexity. Page 109 was visually checked. https://ems.press/content/serial-article-files/29640
5. Ian Biringer and Juan Souto, *Thick hyperbolic 3-manifolds with bounded rank*, arXiv:1708.01774v2, revised 2023-03-09. The theorem used is Corollary 14.9 (printed pages 6 and 220), with rank and global thickness hypotheses; both pages were visually checked. The v2 arXiv record reports substantial revisions, so the older v1 is not used. https://arxiv.org/pdf/1708.01774
6. Ian Biringer, research narrative dated June 22, 2024, Section 2. The source continues to pose the unrestricted rank questions; the web tool supplied its full text after direct local download returned HTTP 406. https://ianbiringer.net/researchstatement.pdf
7. Juan Souto, *Geometry, Heegaard splittings and rank of the fundamental group of hyperbolic 3-manifolds*, arXiv:0904.0237. Used as a background cross-check of the closed-case question and the min/max distinction, not as a proof of any new reduction. https://arxiv.org/pdf/0904.0237

Current author publication lists were also inspected: https://ianbiringer.net/ and https://juan.perlora.eu/_subsites/research.html . Biringer's list identifies the thick-case work with Memoirs of the AMS (2026), while Souto's list still says to appear. The AMS publisher page returned HTTP 403. We therefore fix theorem numbering and pagination to the inspected arXiv v2 rather than infer final-publication details.

No verified primary-source resolution of the rank-only thin case was found in this search. This is not a guarantee that every newer, unindexed, or unpublished result has been found.

## Related targets and provenance

The live queue row was queued 0/5 before this attempt. No own state entry, prior attempt directory, matching exact-ID PR, matching branch, or code-search result was found. The phrase search found unrelated injectivity problems, not this target. No row for this ID occurs in the related-target grouping file. Broader catalogue matches concern volume or different injectivity questions and are not equivalent targets.

The pinned prior AI report reverses the direction of the target; the later repository desk assessment already warns about this. The present work independently verifies that warning against the original and does not claim the warning as a new discovery. No historical reviews or imported reports were edited.

This packet contains original exposition, derived mathematics, bibliographic links, and source hashes. It redistributes no third-party paper, extracted full text, source screenshot, or corpus. Source hashes identify the privately inspected bytes; sources are not required to run the finite controls.
