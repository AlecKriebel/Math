# Lê source and correction lineage

All PDF bodies named below were freshly retrieved independently in this audit. Fingerprints and URLs are in SOURCE_MAP.json. Raw copies, extracted text and page renders are private. Printed page numbers are used; MPI preprints have two additional cover/blank pages.

| Object | Date/version authenticated | Relevant actual statement/proof locator | Scope assessment |
|---|---|---|---|
| MPI43/2003 | Body dated May5,2003; current MPI file and GWDG mirror have identical354597bytes and SHA256ae9dad5eb358aa3d89948a614c2ff15f89fe54cec969a1fb1a023ac81de50d17 | Abstract printedp1 distinguishes C3-bounded finite sample and arbitrary infinite sample; introductionp3 and Theorem5.2 p32 claim arbitrary finite sample. Free-map and algebraic right-inverse perturbation pp33–39; nonbounded argument pp40–41. | Historical breadth is internally inconsistent. The actual nonbounded step is necessary, not a corollary of the bounded linear intermediate. |
| MPI77/2003 | Body dated August19,2003;114228bytes | MainTheorem p2, bound `N(m)=4(m+1)[(m+1)(m+4)+2]`. Proposition2.4a p3 adds avoidance of a closed set; Theorem2.5 p4 is explicitly compact. Noncompact construction p5. | Only C1 mapping regularity is promised in this preprint. It cannot silently replace the final smooth journal theorem. Its Proposition2.4a as literally written permits a closed set equal to the whole target, an obvious missing qualification; the intended avoidance mechanism still does not solve gluing. |
| arXivv1 | June9,2005 09:48:54UTC;331475bytes | Theorem5.2 p32, compact perturbation pp33–40, noncompact proof pp41–42. | Unrestricted global finite-simplex embedding claimed; noncompact construction is a separate unverified step. |
| arXivv2 | November30,2005 07:49:10UTC;214036bytes | MainTheorem/Theorem5.1 p15; noncompact paragraph p20. | Replaces long perturbation proof with Gromov cubic realization plus Nash metric correction. The intermediate result remains compact. Main statement says immersion; final noncompact paragraph calls its product an embedding. |
| FinalJournal of Geometry | Publisher receivedSeptember10,2004, revisedJanuary2,2005; issueMarch2006,84:83–93 | Actual publisher abstract unrestricted smooth/C1 finite-model embedding; no body obtained. | This is a distinct publication. Whether it contains a materially different valid global proof is not adjudicated. A title/DOI match on ResearchGate is insufficient: the displayed body starts MPI77/2003. |
| WorldScientificvolume | 2007, DOI10.1142/9789812770493_0012 | MPI's primary page identifies chapter,231–253; arXiv comment says231–254. Final body unavailable. | Not automatically identical to v2, v3 or v6. Metadata establishes publication, not exact theorem proof. |
| arXivv3 | November8,2010 10:48:27UTC;228158bytes | Section5 pp15–20. | Broad MainTheorem and noncompact sphere-decomposition construction retained. |
| arXivv4 | May30,2014 17:16:19UTC;231302bytes | MainTheorem p14, compact Theorem5.1 p15, revised Theorem5.5 proof, noncompact paragraph pp21–22. | Revision note improves Theorem5.5, not a verified removal of the noncompact issue. |
| arXivv5 | March9,2016 20:56:12UTC;257434bytes | MainTheorem p14; noncompact proof pp22–23; Theorem5.6 pp23–24 upgrades to embedding, with separate noncompact paragraph p24. | Attempts an explicit all-manifold embedding theorem. The last paragraph puts compact pieces into disjoint small neighborhoods with comasses tending to infinity. This still does not establish the missing compatibility of their collapsed boundary values. |
| arXivv6 | March10,2016 15:52:27UTC;244242bytes,23pages | MainTheorem p14 adds compactness; Theorem5.1 p15 already compact; finalMainTheorem proof p22 uses only compact case; Theorem5.6 pp22–23 adds compactness and ends after compact proof. | Actual noncompact blocks from v5 are absent. ArXiv comment explicitly records compactness added to MainTheorem and Theorem5.6. No unrestricted global proof survives in the checked revised body. |

## Exact noncompact proof gap, rather than an abstract-only dismissal

In MPI77 printedp5 and the later versions' noncompact paragraphs, `M` is covered by locally finite disk neighborhoods `N_i^j`, grouped into finitely many classes with disjoint members. Each disk is collapsed outside a central subdomain to a north pole of a separate sphere `S_i^j`. Compact results furnish maps `psi_i^j` of these spheres into a common finite positive model. The proof then treats their union as `psi^j` and writes a map `I_j` on all of `M` by composition; the final product is asserted to give the statistical embedding.

Three obligations are not proved by disjointness or local finiteness alone:

1. There must be a well-defined single map on the complement of all disks of class`j`, with boundary values and derivatives compatible with every `psi_i^j` at its collapsed pole. Independent disjoint image choices do not provide a common exterior value. The v5 embedding paragraph's disjoint target neighborhoods make that issue especially visible.
2. The sphere statistical structures and collapsing maps must give exact additive pullback identities for both tensors while remaining positive smooth metrics on the spheres. A partition of unity by itself is not a proof of those identities after nonlinear maps; cutoff derivatives enter pullback formulas.
3. Smoothness of the global maps and the claimed embedding topology/injectivity must be established in the intended regularity. Countably many compact embeddings in a finite target do not imply this automatically.

This audit does not claim that the unrestricted finite-simplex theorem is false. It identifies an exact missing globalization mechanism in the inspected argument and the later author's compactness restriction. That is enough to prevent treating those older paragraphs as a verified whole-target predecessor. The unseen final2006 and2007 bodies could change the conclusion; that uncertainty is preserved.

The unrestricted consequence sentence remaining after the compact MainTheorem in v6 does not reinstate a proof of the noncompact case. Neither a historical abstract nor a residual sentence overrides actual theorem hypotheses and the deleted argument.

## Compact mechanism and editorial issues

The compact mechanism is substantive prior work: realize the cubic via Gromov, choose a constant small scale so its metric cost lies below `g`, add a Nash embedding of the residual metric with cancelling cubic coordinates, then map a bounded part of the resulting linear statistical space into the simplex. Compactness supplies the uniform scale and bounded image. Theorem5.6 strengthens the final map to an embedding on compact input.

Some printed rescaling powers and dimension symbols in the intermediate formulas are inconsistent. The routine coherent scaling is to use `epsilon f1`, residual metric `g−epsilon^2 f1*g0`, and ambient cubic coefficient `epsilon^(−3)`. This audit does not treat such algebraic typography as a reason to erase the compact predecessor. It also does not independently reprove every Nash/Gromov or torus-curve lemma: the historical result is read in its corrected compact category, and the priority-critical noncompact step is assessed separately.

## Relation to the candidate's mechanism

The original long Lê proof already uses algebraic freedom of derivative vectors, jet-space transversality, and a minimum-norm right inverse for a linearized metric/cubic system (MPI43 pp34–38; v1 corresponding Section5). Matumoto1993 already globalizes compatible scalar3jets (pp329–331). These are required credits if the candidate is later written as research exposition. “Finite jets” or “smooth right inverses” alone cannot be presented as a newly invented general method.

The candidate's narrower possible contribution is its particular finite polynomial feature space, exact global pair with zero potential one-form, and nonuniform positive-Hessian extension for all noncompact input, with its dimension bound. This audit has not established historical priority of that combination.
