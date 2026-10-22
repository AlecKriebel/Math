# Source ledger: weakened Wills, approach 1

This ledger records public bibliographic metadata, source PDF identities, and the completed research and audit inspection history. Source documents and source-derived text or images are not distributed with this edition. Edition preparation rechecked the previously retrieved public-source byte identities; it did not perform a new literature search or scholarly inspection. A bounded literature search is not a certificate that no other result exists.

## S1. Exact question

- Author/contribution: Martin Henk, “Bounds on the lattice point enumerator of convex bodies.”
- Container: Oberwolfach Report 39/2004, printed p.2089, PDF p.23 including leading blanks.
- Public source: https://ems.press/content/serial-article-files/45962?nt=1
- Bytes: 318855.
- SHA-256: `f4cedcda7c37488c7277bbad3220d3574d6da3a4aa581c9da0b2aab3044131d1`.
- Inspected: the target text and a rendered image of the question page.
- Use: exact all-convex-bodies inequality, intrinsic-volume normalization, fixed leading coefficients 1, and the report's historical statement that full Wills is known through dimension 3 but false in sufficiently high dimensions.
- Scope: no centering or full-dimensional lattice-point assumption. The workshop/report date is 2004.

## S2. General-lattice surface estimate

- Martin Henk and Jörg M. Wills, “A Blichfeldt-type inequality for the surface area,” arXiv:0705.2088v1 (15 May 2007); subsequently Monatshefte für Mathematik 154 (2008), 135–144, DOI 10.1007/s00605-008-0530-8.
- Public source: https://arxiv.org/abs/0705.2088v1
- Journal bibliographic metadata checked against the author publication list: https://page.math.tu-berlin.de/~henk/publications.html
- Bytes: 155567.
- SHA-256: `b03ced13d5174f622ad724d15034e4a56af69c604a5f06e018c0215b0ad2f698`.
- Read: introduction; equation (1.3); the primitive-normal determinant identity (2.6); Theorem 4.1, Corollary 4.2 and its proof, pp.8–9.
- Visually checked: pp.1 and 8.
- Use: Corollary 4.2 supplies a dimension-only coefficient on surface area divided by the smallest codimension-one lattice determinant, with coefficient 1 on normalized volume, when lattice points span the ambient lattice space. Blichfeldt's bound covers lower-rank slice hulls.
- Limitation: its larger surface coefficient does not resolve the target in the original dimension. Its full-rank hypothesis is checked separately each time it is applied to a slice hull.

## S3. Related centered-body paper

- Sören Lennart Berg and Martin Henk, “Lattice point inequalities for centered convex bodies,” arXiv:1505.06444v1 (24 May 2015); journal DOI 10.1137/15M1031369.
- Public source: https://arxiv.org/abs/1505.06444v1
- Download: https://arxiv.org/pdf/1505.06444 returned the inspected v1; retrieval 2026-10-10T00:24:48Z, HTTP 200.
- Bytes: 177868.
- SHA-256: `dd05ad068da739ffeaecede393f95efcd60ddcf1d10c6bdfedfea268ddb12763`.
- Read/visually checked: Proposition 1.1, p.2; Theorem 1.1 and Conjecture 1, p.3; Theorem 1.2, p.4.
- Finding: the main estimates use the centroid-at-origin hypothesis and the first successive minimum, with sharp simplex/planar statements. These are not the all-translations intrinsic-volume estimate. No extension from this v1 to the target is asserted, and the later journal version is not represented as separately inspected.

## S4. Earlier asymptotic lattice-surface estimates

- U. Betke and K. Böröczky, Jr., “Asymptotic Formulae for the Lattice Point Enumerator,” Canadian Journal of Mathematics 51(2) (1999), 225–249.
- DOI: https://doi.org/10.4153/CJM-1999-012-9
- Publisher PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/36CE7C75D35B9B2953D68D0F4CECF1DD/S0008414X00004600a.pdf/asymptotic-formulae-for-the-lattice-point-enumerator.pdf
- Retrieval: 2026-10-10T00:27:24Z, HTTP 200.
- Bytes: 215667.
- SHA-256: `10aa148184bfb2da64804ca503ff909d4fc251d9c1f385645e868d1f71b61424`.
- Read: introduction through Theorem D; relevant inradius discussion; Theorem A proof; Theorem D proof and final remarks.
- Visually checked: Theorems A, B, D and Corollary C, printed pp.226–228, PDF pp.2–4.
- Finding: Theorem A supplies a fixed-lattice-facet-polytope O(lambda^(n−2)) remainder. Theorem D supplies a mixed-volume estimate plus o(surface) for families with Euclidean inradius tending to infinity. The half-unit ball and half-unit crosspolytope both satisfy its auxiliary support-function hypothesis for Z^n.
- Limitation: neither theorem gives a constant depending only on dimension multiplying the sum of the lower intrinsic volumes over every changing polytope. The lattice-width condition from our slicing lemma is not an inradius condition.

## S5. Primary input for flatness

- W. Banaszczyk, A. E. Litvak, A. Pajor, and S. J. Szarek, “The flatness theorem for non-symmetric convex bodies via the local theory of Banach spaces,” Mathematics of Operations Research 24(3) (1999), 728–750.
- DOI: https://doi.org/10.1287/moor.24.3.728
- Author-hosted manuscript: https://www.math.ualberta.ca/~alexandr/papers/wwBLPS2503.pdf
- Link verified from the author's publication list: https://www.math.ualberta.ca/~alexandr/papers/
- Retrieval: 2026-10-10T00:37:20Z, HTTP 200; an earlier web-reader attempt timed out, then ordinary PDF retrieval succeeded.
- Bytes: 276161.
- SHA-256: `0341439faa4fb7b44b46987929ac82f29f9654b6b5f35bbff247dbd9092d01c6`.
- Read: definitions on manuscript p.2; Proposition 2.3 and Theorem 2.4 on p.9; supporting discussion.
- Visually checked: p.9.
- Use: Proposition 2.3 combined with Theorem 2.4 yields a finite dimension-only flatness bound for bodies disjoint from the integer lattice. The authored note explicitly passes to hollow bodies using inner homotheties.
- Scope warning: Corollary 2.5 concerns simplices, not arbitrary convex bodies. The proof note correctly cites Proposition 2.3 and Theorem 2.4 instead.

## S6. Terminology check for hollow bodies

- Lukas Mayrhofer, Jamico Schade, Stefan Weltge, “Lattice-free simplices with lattice width 2d−o(d),” arXiv:2111.08483v2, 9 March 2022.
- Public source: https://arxiv.org/abs/2111.08483v2
- Download: https://arxiv.org/pdf/2111.08483 returned the inspected v2; retrieval 2026-10-10T00:31:56Z, HTTP 200.
- Bytes: 168810.
- SHA-256: `7495d9881a90a4f2817db00bc2080a6f50578c7a03a332a64d810a169e029835`.
- Read/visually checked: introduction on p.1.
- Use: confirms “lattice-free” means no interior integer points and defines the finite fixed-dimensional flatness constant.
- Scope: no use is made of its lower-bound construction or its then-current best quantitative upper bound. Those parts were not needed or audited.

## Research and verification limits

The available primary sources do not supply the full requested inequality. The restricted slicing theorem and the explicit height-one-pyramid calculations are authored deductions. Their historical novelty has not been established. No purported current complete resolution was found by this pass, but the literature search was bounded.
