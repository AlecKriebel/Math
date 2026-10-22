# Source and scope checks

Checked 4 October 2026 UTC. A failed search is not evidence of the absence of a result.

## Catalogue and identity

- Requested catalogue URL: https://www.unsolvedmath.com/problems/2807. The web reader could not retrieve it; a direct GET returned HTTP 403. No access restriction was bypassed.
- The pinned upstream record is ID 2807, code KP-3.9, title Kirby Problem 3.9. The entire selected statement and background were read. No matching dedicated entry was found in the pinned research-results dictionary, so the embedded literature triage is the prior report used.
- Primary identity was verified against the AMS author-version PDF of *K3*, printed page 138, Problem 3.9. The nearby Problem 3.8 is stronger hyperbolic profinite rigidity. This is not Problem 3.9 from the old 1997 Kirby numbering.
- The live repository queue and state were checked. The row was queued, 0/5. Exact-ID PR, branch and code searches returned no prior result; the dedicated attempt directory did not exist. Searches are not a guarantee against differently named or unindexed work.

## Current primary material

1. Baykur–Kirby–Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, AMS Mathematical Surveys and Monographs 295, 2026, Problem 3.9, printed page 138. Author version: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf . The source identifies the closed hyperbolic rational-homology-sphere case as central.
2. T. Cheetham-West and K. Lê, *Detecting embedded surfaces using finite quotients*, arXiv:2603.22543v1, 23 March 2026. https://arxiv.org/abs/2603.22543v1 . Theorem 1.3 gives sufficient hypotheses; §6 leaves the general problem open. The current arXiv page listed only v1 when checked. The author's research page lists it as submitted. These observations do not establish that no later unindexed work exists.
3. G. S. Garden and S. Tillmann, *An invitation to Culler-Shalen theory in arbitrary characteristic*, arXiv:2411.06859v2, 12 December 2024. https://arxiv.org/abs/2411.06859v2 . Theorem 24 and Proposition 26 supply the character-curve-to-tree and splitting-to-surface inputs. The example in §6.3 requires the caution below.
4. T. Cheetham-West, A. Lubotzky, A. W. Reid and R. Spitler, *Property FA is not a profinite property*, Groups Geom. Dyn. 19 (2025), 1081–1087, DOI https://doi.org/10.4171/GGD/802 . Its general residually finite group examples are not asserted to be 3-manifold examples.

Tianwei Liu's survey arXiv:2508.20110v1 was consulted as secondary orientation, not used as an independent proof of a theorem. The source history includes an arXiv overlap notice; our mathematical inputs are the primary sources above.

## Precision checks on the 2026 preprint

The finite-image proof in its Lemma 4.11 must be restricted to the algebraic closure of a finite field. For a general algebraically closed positive-characteristic field with transcendental elements, a cyclic matrix subgroup can be infinite. Our Lemma 6 gives the finite-field-closure argument correctly; dimension can then be extended by algebraic base change. We do not infer that this wording issue refutes the preprint's main theorem.

Neither a set bijection on representations nor a set bijection on conjugacy classes should silently be equated with an algebraic isomorphism of character varieties. Our character-transport proof explicitly checks equality of trace functions and uses only finite versus infinite sets of characters.

## Exact inconsistencies in Garden–Tillmann v2 §6.3

### Displayed presentation versus first homology

The presentation on printed page 43 has relator exponent rows (6,2) and (10,−5). This was checked against both the PDF image and the HTML formula. Its abelianization matrix therefore has determinant −50 and gcd of entries 1, so its Smith form gives Z/50. The following page instead reports Z/40 for the named census manifold. Both cannot follow from the displayed presentation as written.

This is an internal source consistency issue. We have not established whether the presentation or the reported homology contains the error, and do not identify the displayed presentation with the census manifold as a newly checked fact. The no-dihedral obstruction uses cyclicity, which either displayed number would satisfy, but the source mismatch still prevents full certification of that example.

### Repeated roots in characteristic 43

The same section displays q(s)=2s⁸−10s⁶+18s⁴−12s²+1 and asserts eight distinct roots in every odd characteristic. Direct modular Euclidean computation gives gcd(q,q′)=s²+1 in F₄₃[s]. Thus characteristic 43 is a counterexample to that distinct-root assertion. This does not create a positive-dimensional variety: q is a nonzero polynomial in every characteristic, and a univariate nonzero polynomial has finitely many roots. In characteristic two it becomes the constant 1.

The standard-library controls reproduce both observations. Their purpose is to delimit what was verified, not to pronounce the qualitative theorem incorrect or claim a resolution of KP-3.9.

## Search limits

Searches used the exact target, Haken/profinite combinations, the primary preprint title, the author research page, and recent arXiv pages. No full resolution was located. The general question remains the question stated in the March 2026 primary preprint; this is a dated literature assessment, not proof of universal openness.

No source PDFs, full imported datasets, or private correspondence are included in this public attempt. No outside researcher was contacted.
