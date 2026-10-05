# Primary-source and exact-statement audit

## Dataset and descriptor

The independently read descriptor catalog contains one target record for ID 30002003, rank 712, problem number OWR-11580-009. Its public-source DOI and title match the uniquely filtered dataset record. The decoded statement's byte count and hash match the descriptor exactly. Only identity, sizes, hashes, and match outcomes are retained in this safe audit; no raw record or full statement is included.

The first fresh filter request returned HTTP 500, and the web-text route produced a retrieval error. A subsequent public filter request with explicit offset=0 succeeded with HTTP 200. Its entire response is byte-identical to the author's preserved response, with one matching record and no truncation. This is successful independent recovery, not an inference from the author's summary. See INPUT_BINDING.json for exact scope and source URL.

The original UnsolvedMath webpage was not newly retrieved during this audit. The author's reported HTTP 403 is retained as a historical limitation; the successful public dataset recovery is a separate source, not a claim to have read that webpage.

## OWR report: precise contextual distinction

Source: Anne Moreau, joint with Victor Batyrev, contribution to *Enveloping Algebras and Geometric Representation Theory*, Oberwolfach Report 13/2012. [Report](https://ems.press/content/serial-article-files/46383) and [DOI](https://doi.org/10.4171/owr/2012/13).

The audit independently downloaded the report, verified its hash against the frozen metadata, extracted the relevant text, and rendered/read printed pages 766-767 (PDF pages 34-35, one-based). The horospherical theorem explicitly assumes projective minimal orbits. The following shortened conjectural sentence about spherical varieties does not repeat that condition. Thus its literal broad wording also admits the audited counterexample, while the surrounding theorem cautions against treating it as the fully qualified formulation.

## Batyrev-Moreau: full formulation and definitions

Source: Victor Batyrev and Anne Moreau, *The arc space of horospherical varieties and motivic integration*, arXiv:1203.0671v2, dated 17 December 2012. [Primary manuscript](https://arxiv.org/abs/1203.0671v2).

The independently downloaded PDF matches the recorded bytes and hash. The audit inspected Definitions 1.5 and 5.2, Theorem 5.3 and its following explanation, and Conjecture 6.7; PDF page 26 was rendered and visually checked. The full conjecture includes projectivity of all closed orbits and proposes both an inequality and its smoothness equality case. The theorem's full-dimensional-cone condition is explained there as projectivity of the closed orbit.

The publisher landing page independently confirms the 2013 Compositio Mathematica article, volume 149, issue 8, pages 1327-1352, DOI 10.1112/S0010437X13007124. [Publisher record](https://doi.org/10.1112/S0010437X13007124). The detailed mathematical inspection is of the authors' versioned primary manuscript, not an assertion that a separate publisher PDF was compared byte-for-byte. Following the publisher's advertised PDF URL returned HTTP 200 with an HTML landing page, rather than PDF bytes; no journal typeset full-text comparison is claimed.

## January 2026 criterion

Source: Giuliano Gagliardi, Johannes Hofscheier, Heath Pearson, *Toricness and smoothness criteria for spherical varieties*, arXiv:2601.06376v1, dated 10 January 2026. [Primary preprint](https://arxiv.org/abs/2601.06376v1).

The independently downloaded PDF is byte-identical to the recorded source. Theorem 1.5 and the following discussion were inspected in extracted text, public HTML, and a fresh rendering of PDF page 3. The theorem uses a localized spherical-skeleton invariant. The surrounding discussion describes extension of the stringy Euler criterion beyond horospherical varieties as conjectural. This supports the distinction between criteria at that manuscript date. It does not establish universal current openness or absence of every later paper.

## Other retained dependencies

- Boris Pasquier, *A survey on the singularities of spherical varieties*, arXiv:1510.03995v1. Remark 3.5 supplies equivariant SNC resolution context; Section 5 and Proposition 5.6 supply klt context. The Q-Gorenstein qualification in the packet is appropriate to the preceding definition, despite the survey proposition's abbreviated wording. The explicit counterexample's klt proof is independent of that general statement. [Primary manuscript](https://arxiv.org/abs/1510.03995v1)
- Victor Batyrev and Giuliano Gagliardi, *On the algebraic stringy Euler number*, arXiv:1610.03842v2. Introduction and Theorem 1.8 confirm that the established comparison concerns the equivariant Mori program for projective spherical varieties. It is not the ordinary/stringy Euler smoothness conjecture. [Primary manuscript](https://arxiv.org/abs/1610.03842v2)
- Timothy De Deyn, *A note on affine cones over Grassmannians and their stringy E-functions*, arXiv:2203.06040v2. Lemma 2.2, Proposition 3.1, and Sections 3.2-3.3 confirm the known line-bundle resolution and cone discrepancy calculation. The packet gives its own proof under explicit stronger hypotheses. [Primary manuscript](https://arxiv.org/abs/2203.06040v2)
- Stacks Project, Nagata's criterion for factoriality, Tag 0AFU. The stated criterion and proof were inspected directly; the prime-element and factorization-existence hypotheses hold for the noetherian domain used here. [Primary reference](https://stacks.math.columbia.edu/tag/0AFU)

All six mathematical PDFs were independently downloaded during this audit and match the original metadata exactly. Their titles, versioned URLs, byte counts, hashes, and inspected locations appear in SOURCE_VERIFICATION.json. PDFs, extracted text, and rendered pages remain excluded from the safe audit.

## History and status limits

The audit did not reconstruct the unavailable old AI-report corpus or re-run an exhaustive repository-wide historical search. It reviewed the packet's bounded historical statements and found no claim that complete absence had been established. Its fresh source checks certify the wording distinction and cited manuscript statuses, not originality or a global literature theorem.
