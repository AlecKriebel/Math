# Scoped acceptance: problem 30002367

**Authorship and review status:** This authored report was prepared with AI assistance and is unrefereed, with no proof-assistant certification. Its mathematical acceptance is scoped to the explicitly named foundations. This report's status is distinct from the bibliographically confirmed journal publication of Hemminger's prior result.

**Date:** 2026-10-10 UTC.

**Outcome:** Accept as a credited prior resolution by David Hemminger, with zero new target proof-attempt turns and no target novelty claim.

The accepted target is Totaro's original Conjecture 12.8: for every finite group G, every prime p, and every field k of characteristic different from p containing μp, the centralizer-detection degree of CH^*(BG_k)/p equals its maximal nonzero unstable-module suspension in **Chow degree**. The source's abbreviated OWR statement is interpreted using the explicit field and grading conventions in Totaro's 2014 book, p.131. No unrestricted-base-field extension is certified.

The final certificate verifies the group class, coefficients, X=Spec(k) hypotheses, actual multiplication pullbacks, truncation <d+1 versus ≤d, degree doubling, and existence of a finite maximum. The mathematical audit reconstructs the localization-to-detection bridge and both directions of the suspension equality, and establishes finiteness through Hemminger's coarse n² bound without assuming Noetherianity or p∤|G|.

A complete source-proof correction replaces the false rank-only centralizer formula with a product over character spaces. It retains the actual C_G(λ) action and all mixed components, and proves exactness from explicit faithfully free flag-bundle presentations. The separate independent review accepts this correction and the final parity and augmentation arguments.

The inspected arXiv v2 requires these source qualifications:

1. Page 16: use the block-centralizer descent correction, not the displayed GL(n−r)×Gm^r formula.
2. Page 21: use the contravariantly correct centralizer inclusion; expand tensor notation as finite sums when needed.
3. Page 5: do not use the printed odd-prime lower-operation criterion on arbitrary odd-supported topological modules. The categorical nilpotent-filtration theorem and the written direct parity argument are used instead.
4. Page 8: interpret degree doubling at the category/action level; do not assert the literal even-square subalgebra is the ordinary Steenrod algebra after regrading.

Theorem statements and applications are accepted relative to the precisely named standard external foundations in the audit, including the classical nilpotent-filtration theorem, Lannes/Brown-Gitler theory, and equivariant Chow/Steenrod foundations. Those foundational proofs are not claimed to have been independently rederived.

Publication in *Algebraic & Geometric Topology* 21 (2021), 1881-1910, DOI 10.2140/agt.2021.21.1881, is confirmed by publisher and arXiv metadata. Mathematical inspection was of arXiv:1911.03033v2 and selected primary-book/dissertation evidence. The journal PDF was access-denied and is not claimed inspected or byte-identical to the preprint. This audit does not assert that the journal version contains the same source defects.

This edition contains the complete authored mathematical reports and public scholarly-source metadata. Copied source-document bodies, extracts and images; dataset contents; computational scripts, checkers, logs and result artifacts; and private coordination material are excluded.

## Read order

1. `APPLICABILITY_CERTIFICATE.md`
2. `MATHEMATICAL_AUDIT.md`
3. `CENTRALIZER_DESCENT_CORRECTION.md`
4. `INDEPENDENT_REVIEW.md`
5. `SOURCE_LEDGER.json`
