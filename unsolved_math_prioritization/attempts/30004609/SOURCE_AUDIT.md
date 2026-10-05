# Source and novelty audit

Checked 2026-10-04. This is a bounded primary-source review, not a proof that no prior resolution exists.

## Exact target

The catalogue URL is https://www.unsolvedmath.com/problems/30004609. Direct retrieval returned HTTP 403 and the web reader could not access it. The selected record was therefore identified in the pinned public-source corpus by numeric ID 30004609 and independently matched to the primary Oberwolfach source, rather than treating a failed catalogue request as a successful read.

The primary source is the contribution *Free arrangements with low exponents* in Oberwolfach Report 5/2021, report DOI https://doi.org/10.4171/owr/2021/5, printed pp. 283-286, with the conjecture on p. 284. The setup on p. 283 specifies a characteristic-zero field and a central essential arrangement. Essentialization and product reduction are explained in the candidate proof. The catalogue statement omits the field, but the source does not support replacing characteristic zero by an arbitrary field.

Public PDF: https://ems.press/content/serial-article-files/46883.

The source PDF and previous manuscript were downloaded privately and inspected as text, with the conjecture page and the problematic inference page also visually rendered and inspected. Only metadata and original mathematical analysis appear in this packet.

## Withdrawal and historical claims

The current record https://arxiv.org/abs/1707.07091v4 marks *Free arrangements with low exponents* withdrawn on January 16, 2022. The notice identifies two issues:

- completeness of the hand case enumerations in Sections 4.2.1 and 4.2.2 is not guaranteed;
- the factor-size inference in Proposition 4.8(a) is not justified.

The version inspected for the mathematical history is https://arxiv.org/abs/1707.07091v3, dated November 16, 2020. The withdrawn version has no PDF, so an unversioned-PDF failure was resolved by inspecting the explicitly identified previous version. The earlier abstract and the 2021 Oberwolfach report describe rank-4/5 and inductively-free positive results, but those statements must be read together with the later correction notice.

The author's public research page https://sites.google.com/view/stefan-tohaneanu/research still identifies an extended abstract in Oberwolfach Reports. This page does not establish a later journal resolution of the general conjecture.

The example in the withdrawal notice has

Q = x y (x+y)(x+2y)(x+z) z w (z+w).

Our checker supplies a Saito basis with degrees 1,3,2,2, verifies all 32 tangency conditions, proves the basis determinant equals Q, and computes that the degree-one logarithmic derivation space has dimension one. Its incidence graph is a tree with a unique four-point line. A full-lattice computation finds a modular chain. Deleting x+z produces the direct product of a four-line pencil in x,y and a three-line pencil in z,w. The component sizes are therefore 4 and 3, while the deleted arrangement has exponents 1,1,2,3. This verifies the announced obstruction to the earlier inference, while confirming this example satisfies the desired supersolvability conclusion.

## Inputs used by the candidate

The candidate reproves the rank-two multiplicity bound, connectedness and pruning arguments. It uses no withdrawn rank-4/5 enumeration or Proposition 4.8.

Freeness implies formality by Yuzvinsky, *The first two obstructions to the freeness of arrangements*, Trans. AMS 335 (1993), 231-244, Corollary 2.5, DOI https://doi.org/10.1090/S0002-9947-1993-1089421-5. The original AMS PDF endpoint returned HTTP 403. The exact result and corollary location were independently corroborated in the primary research article by Möller, Mücksch and Röhrle, *On Formality and Combinatorial Formality for hyperplane arrangements*, https://arxiv.org/abs/2202.09104v2, introduction p. 2 and formality definitions in Section 2; published Discrete & Computational Geometry 72 (2024), 73-90, DOI https://doi.org/10.1007/s00454-022-00479-5. That manuscript was retrieved and inspected privately.

Terao factorization and standard product/essentialization results are used in their usual arrangement-theoretic forms. Factorization is stated by Terao himself on slide 7 of https://www.math.sci.hokudai.ac.jp/~terao/chambers.201408.SetteWS_beamer.ver.8.pdf and is also recalled in the primary OWR source. Product freeness and union of exponent multisets are restated, with attribution to Orlik-Terao Proposition 4.28, in Proposition 7 of https://www.combinatorics.org/ojs/index.php/eljc/article/download/v27i1p28/pdf/.

## Repository and prior-report gate

Read the live repository and queue instructions. The live main revision checked was 2b18c9302f69afc94288a6dd9135bf0cba87ae28. The selected queue row was rank 644, numeric ID 30004609, queued, 0/5. Its live attempt directory returned HTTP 404 and its state entry was absent. All-state PR searches for the numeric ID and title keyword, an exact-ID code search, and a numeric-ID branch search returned no matches. The related-target group file had no match. No other pinned dataset record matched both supersolvability and exponents. The pinned prior-report corpus had no exact numeric-ID or source-code match in either keys or values.

## Bounded novelty search

Searches combined the exact manuscript title/ID, Tohaneanu with supersolvability and low exponents, one cubic exponent, formal arrangements and incidence graphs, and relation-space/rank-two formulations. Primary-source findings were the original OWR conjecture, its withdrawn manuscript, the published formality article, and related low-rank line-arrangement work. No inspected source supplied the all-ranks relation-incidence proof or a full general resolution. This negative search result does not certify novelty.

Third-party summaries that repeat the older abstract were not used as evidence that the withdrawn partial proofs are valid. Searches also distinguished the unrelated supersolvable Dirac-Motzkin conjecture, for which a resolution would not settle this target.
