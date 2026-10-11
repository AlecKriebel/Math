# Source and prior-art audit: 6800007

Checked 2026-09-30. This is a bounded literature audit, not proof of historical novelty.

## Original target

The pinned record is 6800007 / AMR-067-0007, rank45 in the working queue. Its complete record and prior OPEN-TRIAGE report are preserved in `source_record.json`. The prior report is a literature triage, with no substantive proof attempt. The imported source attributes the question to Elisha Falbel in the 2018 Morgan–Pansu problem list.

The full [original TeX](https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex) was retrieved from the coauthor's university website. Section “Manifolds modelled on flag manifolds,” second question environment (Question7 in the PDF), asks:

> What is the homotopy classification of totally real immersions of real 3-manifolds in the complex full flag manifold F12?

The following sentence already invokes Gromov's h-principle. The preceding question about real-form orbits is a different problem and is not claimed solved here. The original does not explicitly impose orientability or compactness. The current candidate states its manifold, homotopy, complex-structure, and properness conventions explicitly.

## Primary sources read and what they establish

1. **Falbel–Veloso, 2018 preprint**, [arXiv1804.11096](https://arxiv.org/abs/1804.11096). The arXiv history lists only its April2018 version. The full PDF was retrieved. It defines the flag structures, the totally real condition, and the global invariant; its final section treats homogeneous examples. It does not contain the later Section8.1/Proposition8.1.
2. **Falbel–Veloso, 2020 paper**, [Geometriae Dedicata209,149–176](https://doi.org/10.1007/s10711-020-00528-4). The publisher confirms the publication metadata. The publicly readable [author-provided manuscript](https://www.researchgate.net/publication/340658748_Flag_structures_on_real_3-manifolds), uploaded by the coauthor in April2020, contains Section8.1. Its Proposition8.1 already provides the integer family over each nonzero homotopy class of maps from S3 to F. That is prior work. The downloadable author-PDF route was unavailable, but the complete author-manuscript text, including the proposition and its proof, was readable. It is not silently identified with the older arXiv version.
3. **Forstnerič, 1986**, [*On totally real embeddings into Cn*](https://users.fmf.uni-lj.si/forstneric/papers/1986Expositiones.pdf), Exposition.Math.4,243–255. The complete author-hosted scan was downloaded; printed pp244–245 were visually checked. Theorem1.1 gives the classical formal classification for Euclidean target. Theorem1.4's 3-manifold existence assertion is explicitly compact and orientable. The broad introductory wording in later sources is not used to remove that hypothesis. Section2 presents the convex-integration input.
4. **Borrelli, 2002**, [*On totally real isotopy classes*](https://doi.org/10.1155/S1073792802105125), IMRN2002(2),89–109. The [author's PostScript](https://math.univ-lyon1.fr/~borrelli/Articles/IMRN2002.ps) was retrieved and converted locally for reading. The paper distinguishes regular homotopy of immersions from isotopy of embeddings and discusses the h-principle and K-theory description. The candidate concerns immersions, not the stronger embedding problem.
5. **Koshkin, 2009**, [*Homotopy classification of maps into homogeneous spaces*](https://arxiv.org/abs/0808.0024), [published version](https://tcms.org.ge/Journals/JHRS/xvolumes/2009/n1a16/v4n1a16.pdf), J.Homotopy Relat.Struct.4(1),331–346. The general method of primary invariants and secondary quotient groups for maps from three-dimensional complexes is prior art. The present calculation explicitly includes the tangent-bundle isomorphism and its coupled loop action; no novelty claim is made for obstruction theory itself.

## Current searches and limits

Searches combined the exact original wording, Falbel/Veloso, totally real immersions, complex frame bundle, flag manifolds, cokernels, and homotopy classifications of homogeneous-space-valued maps. The coauthor's publication page and the publisher metadata were checked. Related recent work on homogeneous path structures and global invariants is not automatically a classification of totally real regular-homotopy classes.

No source giving the exact formula in `CANDIDATE.md` was verified in this pass. This negative search result does not establish novelty or the continued openness of every formulation. The candidate must undergo independent mathematical review before a draft PR. The known h-principle, sphere case, and general obstruction-theory method remain explicitly credited.

## Source preservation

Only links, relevant locations, the short target quotation, and local-file hashes are included in this repository package. Source PDFs, page renders, TeX, and PostScript are research reference copies kept outside the repository; no redistribution license is assumed. Their hashes are recorded in `source_manifest.json`.
