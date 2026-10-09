# Source and attribution recovery: forest determinant, proof30003822

Checked 9 October 2026. This report verifies sources and the scope of their claims. It does not independently re-audit the reconstructed determinant proof.

## Result

The exact target is the Teufl–Wagner problem on the transition matrix indexed by all set partitions: for the generic matrix A = (a_ij), establish that (det A)^C_n divides det T in Z[a_ij]. The Bell-state matrix must not be silently replaced by a planar or noncrossing-state matrix. The original definition and question are in [TW2018, pp. 1457–1458](https://ems.press/content/serial-article-files/46745).

The paired Grassmann forest representation, its product and integration identities, and its Catalan-dimensional noncrossing basis belong to established prior work. An authored proof may apply those ingredients to the stated determinant question, but must not claim to have discovered the underlying quotient or basis. The exact determinant application was not located in the bounded review described below. That negative search result establishes neither novelty nor current open status.

## Pinpoint attribution

- [Caracciolo–Sokal–Sportiello, arXiv:0706.1509v2](https://arxiv.org/pdf/0706.1509v2): equation (4.3c), p. 13, gives the paired incidence-difference expression when lambda = 0. Corollaries 4.3–4.5, pp. 15–17, supply the forest multiplication, cycle annihilation and exponential expansion. Lemma 5.1, p. 18, and Corollary 5.2, p. 19, supply partial integration. The Catalan dimension and noncrossing basis are announced on p. 17 with proof deferred to reference [39]; they should not be described as proved there. This paper is published as J. Phys. A 40 (2007), 13799–13835, [DOI](https://doi.org/10.1088/1751-8113/40/46/001).
- [Sportiello’s thesis](https://pcteserver.mi.infn.it/~caraccio/PhD/Sportiello.pdf), Chapter 10: Theorem 10.3, printed p. 207, proves the noncrossing-basis/Catalan statement. Lemma 10.6 is stated on p. 208 and proved on pp. 211–213. The selected triangular coefficients are ±1 and avoid the lambda-dependent terms. Equations (10.3)–(10.5), p. 196, and the polynomial-parameter convention on p. 197 justify working with the normalized f-polynomials at lambda = 0. Specializing the raw scalar-product notation alone would be misleading. Chapter 10’s introduction, p. 195, explicitly discusses nonplanar transfer matrices.
- [Sportiello’s 19 January 2010 slides](https://lipn.univ-paris13.fr/~banderier/Seminaires/Slides/sportiello_19janvier2010.pdf), PDF pages 58–61, corroborate the basis, dimension and relation claims. The official [ICTP seminar listing of 13 January 2009](https://indico.ictp.it/event/a092/) also advertises the noncrossing basis. These are corroborating announcements, not substitutes for the thesis proof.

The basis at lambda = 0 is therefore supported by an actual prior proof, including a specialization argument. This does not by itself establish the determinant of the induced transition operator or the divisibility of the full Bell-state determinant. Those remain claims that the authored determinant proof must justify.

## Bibliographic status and dating

The [official SNS PhD catalogue](https://ricerca.sns.it/handle/11384/78634/browse?etal=-1&offset=136&order=1&rpp=20&sort_by=ASC&starts_with=J&type=title) lists Sportiello’s thesis as 2010 and links [item 11384/85875](https://ricerca.sns.it/handle/11384/85875). The listing was read; direct item retrieval failed. The thesis cover’s academic years 2000–2003 and PDF creation metadata are not treated as publication dates.

CSS reference [39] is marked in preparation in the inspected 2007 version. This is a historical statement, not a verified description of its present publication status. The independently available thesis proof resolves the immediate source-support gap without inventing a standalone publication for [39].

## Bounded priority review

Exact-title and author/topic searches were combined with primary-body inspection. The detailed source scope and limitations are in SOURCE_CATALOGUE.json; SOURCE_PROVENANCE.json summarizes the recorded search and inspection history.

[Kogan, Electrical Networks and Symplectic Invariants, arXiv:2610.07539v1](https://arxiv.org/abs/2610.07539v1), submitted 6 October 2026, was checked at its definitions and main statements: Theorem 1.1, Theorem 2.3, Proposition 3.1, Theorem 4.7 and Corollary 4.8. Its planar network, Pfaffian and grove invariant-tensor results are related background. The exact generic Bell-state transition determinant theorem was not located in those passages. A complete text term scan was only a navigation aid, not a proof of absence.

The publisher abstract of [Li–Yan (2025)](https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.23220) concerns electrical equivalence and spanning trees containing a prescribed forest. Full text was not inspected. The author-hosted Teufl–Wagner Laplace-determinant preprint body could not be retrieved; its abstract-level search hit is logged without a full-text exclusion claim.

No exhaustive citation-chain, archive or unpublished-manuscript survey was completed. No novelty claim is warranted from this review alone.

## Fresh provenance

Five primary PDFs were freshly retrieved and checked for byte count, SHA-256 and readable page structure. Their identities are in SOURCE_CATALOGUE.json and SOURCE_PROVENANCE.json, which also records the inspection scope and visual checks. These are new retrieval identities. No equality with earlier source-file bytes is asserted. This edition includes public citation, retrieval and inspection metadata, with no third-party source PDFs, extracted text, HTML or rendered source pages.
