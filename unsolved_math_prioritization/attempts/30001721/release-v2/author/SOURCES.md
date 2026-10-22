# Source audit

Checked 2026-10-04. Only bibliographic links and short original scope summaries are included here. Downloaded full texts are not distributed with this packet.

## Target provenance

The investigation began at the [catalogue problem URL](https://www.unsolvedmath.com/problems/30001721). It was inaccessible to the web retrieval tool. Identity and wording were cross-checked against the pinned UnsolvedMath problems snapshot and the live repository queue row: rank 621, numeric ID 30001721, code OWR-4800-012, title *Tree Modules for Roots of Acyclic Quivers*, initially queued at 0/5. The checked problems.json SHA-256 was 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf. Catalogue curation is attributed to UnsolvedMath Contributors under CC BY 4.0; the primary papers retain their own rights.

S1. Thorsten Weist, “Localization in quiver moduli spaces and tree modules,” within *Representation Theory of Quivers and Finite Dimensional Algebras*, Oberwolfach Reports 8 (2011), no. 1, 523–608, contribution pp. 594–598. [Publisher](https://ems.press/journals/owr/articles/4800), [DOI](https://doi.org/10.4171/OWR/2011/10).

- The precise existence question and coefficient-quiver definition are on printed p. 594; the field is explicitly C and the quiver has no oriented cycles. This page was checked visually as well as through text extraction.
- Theorems 2 and 3 on pp. 596–597 respectively treat generalized Kronecker roots and imaginary Schur roots. These are not the universal assertion.
- The catalogue question asks existence; the adjacent stronger imaginary-root multiplicity question is separate.

## Scope of the established constructions

S2. C. M. Ringel, *Exceptional modules are tree modules*, Linear Algebra and its Applications 275–276 (1998), 471–493. [Publisher and abstract](https://www.sciencedirect.com/science/article/pii/S0024379597100465), [DOI](https://doi.org/10.1016/S0024-3795(97)10046-5).

The theorem covers indecomposables without self-extensions. Its hypothesis is not “arbitrary real root.” The present packet supplies an elementary real non-Schur example to prevent that conflation. The publisher abstract, not the complete paper, was checked here.

S3. T. Weist, *Tree modules*, Bulletin of the London Mathematical Society 44 (2012), no. 5, 882–898. [arXiv:1011.1203v3](https://arxiv.org/abs/1011.1203v3), [DOI](https://doi.org/10.1112/blms/bds019).

The downloaded version is arXiv v3, 18 October 2011. In that version Theorem 3.17 covers every isotropic root, and Theorem 3.18 covers Schur roots. Introduction pp. 1–2 and Example 4.1 pp. 15–16 explicitly delimit the construction; the example concerns an eight-subspace real non-Schur root obstructing the specified reflection construction. An abstract’s “recipe” wording is therefore not a theorem establishing all roots. Numbering in later publications/citations can differ.

S4. T. Weist, *On the recursive construction of indecomposable quiver representations*, Journal of Algebra 443 (2015), 49–74. [arXiv:1310.2757](https://arxiv.org/abs/1310.2757), [DOI](https://doi.org/10.1016/j.jalgebra.2015.07.012).

The downloaded 20-page arXiv version has covering results Theorem 2.7 and Proposition 2.8 on p. 8 and recursive-decomposition Question 4.1 on p. 17. The latter is posed as a question, not proved in general. We use the covering reduction only as a reduction. In particular, the sentence in the printed argument that treats fundamental-domain roots as Schur should not be applied to divisible isotropic roots without care; S3 handles all isotropic roots separately. S5 supplies an independent covering route.

S5. H. Franzen and T. Weist, *The value of the Kac polynomial at one*, Quarterly Journal of Mathematics 69 (2018), no. 1, 13–32. [arXiv:1608.03419](https://arxiv.org/abs/1608.03419), [DOI](https://doi.org/10.1093/qmath/hax030).

Checked arXiv Corollary 1.2 (p. 2), Corollary 8.2 (p. 11), and Question 8.8 (p. 12). The first is a universal-cover formula. The second requires exceptional compatible roots for its tree-count equality. The third explicitly asks a general lower-bound question. Thus the covering formula does not by itself establish tree-module existence.

S6. R. Kinser and T. Weist, *Tree normal forms for quiver representations*, Documenta Mathematica 24 (2019), 1245–1294. [arXiv:1810.04977](https://arxiv.org/abs/1810.04977), [DOI](https://doi.org/10.25537/dm.2019v24.1245-1294).

The downloaded arXiv paper states the stronger cellular-tree-normal-form assertion as Conjecture 4.11 (p. 16). Theorem 6.10 and subsequent remarks (pp. 30–31) concern restricted isotropic settings, rather than an all-roots solution. The paper also gives the familiar (n,n) Kronecker family used here as a control.

S7. A. Sengupta and A. Kuber, *Generalised tree modules: Hom-sets and indecomposability*, [arXiv:2504.18996v4](https://arxiv.org/abs/2504.18996v4), 12 August 2025.

The current abstract was checked to distinguish a recent naming collision. It concerns generalized tree modules for zero-relation algebras and sufficient conditions; it does not assert the universal target here. No full-text theorem from this paper is used.

## Duplicate and prior-work checks

- At the initial live check, the repository attempt path for ID 30001721 returned 404; PR and branch searches for the numeric ID returned no matches.
- The fetched related-target group file had no matching ID or tree-module/quiver term. The pinned catalogue had only one title matching tree modules/tree representations.
- The prior desk review suggested exceptional sequences and reflections, mentioning non-Schur imaginary roots. The present report expands its caution to real non-Schur roots. That desk note was a route suggestion, not a proof.
- No matching upstream full research report was found: no numeric-ID match, OWR-prefixed key, or “tree modules” string was present in the pinned research_results corpus. This is a bounded absence check, not a statement that no prior research exists.

Targeted web searches covered tree-module existence, real non-Schur roots, recursive constructions, Kac polynomial/tree counts, and 2024–2026 follow-up terminology. No full-resolution primary source was found in this pass. Search absence cannot certify universal literature completeness; the outcome is `unsolved`, not `already_solved`.
