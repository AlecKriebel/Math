# Scholarly sources and verification scope

All six listed PDFs were retrieved from public scholarly hosts and inspected locally. Their byte counts and SHA-256 hashes are recorded in `SOURCE_METADATA.json`; no PDF or extracted source text is included in this packet. Numbered propositions in [ABV] refer specifically to the inspected arXiv v2, rather than an unverified numbering match to the journal version.

## [OWR] Joseph Ayoub, “n-Motivic Sheaves”

Contribution to *Algebraic K-Theory and Motivic Cohomology*, Oberwolfach Report 31/2009, printed pp. 1760–1762, within pp. 1731–1774.

- Report: https://doi.org/10.4171/owr/2009/31
- Inspected PDF: https://ems.press/content/serial-article-files/46231?nt=1
- Inspected locations: printed pp. 1760–1762, especially Example 1, the definitions and formulas for π₀ and Alb, Example 4, and Conjecture 5.
- Visual check: printed pp. 1760–1761, including the tilde over CH in the actual typesetting. The catalogue's subscript-like “g” is not the printed mathematical notation.
- Relevant conventions: characteristic zero, rational coefficients, the full Chow sheaf, and the full Albanese scheme. The omission of a connected-component operation is in the primary formulation too.

## [ABV] Joseph Ayoub and Luca Barbieri-Viale, “1-motivic sheaves and the Albanese functor”

*Journal of Pure and Applied Algebra* 213 (2009), 809–839. Inspected manuscript: arXiv:math/0607738v2, 21 October 2008.

- Record: https://arxiv.org/abs/math/0607738
- Inspected PDF: https://arxiv.org/pdf/math/0607738
- Definition and structure checks: §§1.3.1–1.3.2 (components and the Serre–Albanese scheme), Lemma 1.3.3 (étale surjectivity), Proposition 1.3.8 and Theorem 1.3.10 (1-motivic sheaves), Proposition 1.3.11 and Lemma 1.3.12 (reflector and its adjunction).
- Further checks: Theorem 2.4.1 (derived functor), Remark 2.4.3 (curve characterization of algebraic equivalence), Theorem 3.1.4 (Néron–Severi quotient), Propositions 3.3.2, 3.3.3, 3.3.5 and Remark 3.3.6 (Picard, localization, and Albanese calculations).
- The remark relating the higher Albanese sheaf to the morphic map is prospective, not a proof of the requested general identification.

## [W] Mark E. Walker, “The morphic Abel–Jacobi map”

*Compositio Mathematica* 143 (2007), 909–944.

- Journal record: https://doi.org/10.1112/S0010437X07002278
- Inspected PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4A44146CE680F4F3C857048FDEDD9F48/S0010437X07002278a.pdf/the-morphic-abel-jacobi-map.pdf
- Definitions: §§2–3, especially Proposition 2.5, Definition 3.1, Definition 3.2, Proposition 3.3 and the six-term exact sequence.
- Functoriality: Theorem 4.22, including normalized Hodge structures, Borel–Moore comparison, and localization.
- Target and map: Definition 5.2, Examples 5.5–5.6, Theorem 5.7, Corollary 5.9 and Remark 5.10.
- Nonvanishing: Theorem 6.2 and its proof on pp. 933–934 show why the full target cannot be replaced by its finite coniveau quotient, even rationally.
- The packet uses right exactness of J from §3; a contrary “left-exact” phrase in the proof of Theorem 5.7 is not used.

## [N] Zhaohu Nie, “Blow-up formulas and smooth birational invariants”

*Proceedings of the American Mathematical Society* 137 (2009), 2529–2539.

- Inspected PDF: https://irma.math.unistra.fr/~lfu/Activities/supporting%20files/Nie_Blow%20up%20formulas%20and%20smooth%20birational%20invariants.pdf
- Checked: equation (1.1), Theorem 2.4 and Proposition 2.5, including the negative-Lawson-index convention and the projective-bundle isomorphism.
- This is used with Walker's correspondence functoriality, not as an independent assertion about Hodge structures.

## [S] Fumiaki Suzuki, “Factorization of the Abel–Jacobi maps”

*Épijournal de Géométrie Algébrique* 5 (2021), article 20. Inspected version marked arXiv:2012.04802v2, 18 December 2021.

- Record: https://arxiv.org/abs/2012.04802
- Inspected PDF: https://epiga.episciences.org/8881/pdf
- Checked: introductory target definition, Theorem 1.1 and Remark 1.2. The target is the Jacobian of the coniveau lattice, with a finite isogeny to the algebraic intermediate Jacobian.

## [ACV] Jeffrey D. Achter, Sebastian Casalaina-Martin and Charles Vial, “The Walker Abel–Jacobi map descends”

*Mathematische Zeitschrift* 300 (2022), 1799–1817. Inspected manuscript: arXiv:2101.07506v2, 3 September 2021.

- Record: https://arxiv.org/abs/2101.07506
- Journal record: https://doi.org/10.1007/s00209-021-02833-4
- Inspected PDF: https://arxiv.org/pdf/2101.07506
- Checked: opening definition of the Walker intermediate Jacobian, Theorems A and B, and the accompanying distinctions between the isogeny target and the usual algebraic intermediate Jacobian.
- Its descent theorem concerns the finite-dimensional coniveau Jacobian. It does not identify or eliminate the additional full-Lawson kernel used in this packet.

## Dated literature check

On 7 October 2026, bounded public searches for the conjunctions of motivic Albanese, 1-motivic sheaves, Walker, morphic Abel–Jacobi, and the comparison conjecture located the original report, [ABV], [W], [S], and [ACV], but no inspected source proving the general connected comparison. The author's public version of the report also retains the full-sheaf formula: https://user.math.uzh.ch/ayoub/Other-PDF/N-MSH.PDF (search-index view only; not used in place of the inspected official PDF).

This is a limited literature check, not proof of an exhaustive or current global open status. The mathematical outcome “unresolved” describes this investigation. All general-comparison claims remain subject to independent review.
