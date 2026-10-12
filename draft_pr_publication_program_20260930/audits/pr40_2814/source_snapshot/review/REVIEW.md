# Independent source audit: KP-3.16 / 2814

**Verdict: PASS for a source-status correction reporting a complete existing literature resolution claim. This is not an independent certification of the cited proofs.**

Checked on 2026-09-30 by a separate GPT-6 Astra agent at xhigh reasoning. No new mathematical result or historical-priority claim is made.

Reviewed artifact: SOURCE_STATUS.md, SHA-256:

c232697fb80c20a88efe7db12390d9bda2d7f5c2fdc96e5cfad3a98a8cfdf16c

The artifact is unchanged. The exact justified status is:

**Covered by existing theorem statements, including a recent closed-case preprint; source identity and full scope independently verified, full proof correctness not independently certified.**

**Project disposition: retain unsolved / source hold.** The external resolution claim is recorded precisely, but this audit does not establish a campaign solution or independently verify the full original resolution.

## Original target

K3's Chapter 3 introduction and §3.1, printed p. 131, define hyperbolicity using a complete metric of constant sectional curvature −1. Problem 3.16, p. 142, asks for infinitely many simple closed geodesics in every finite-volume hyperbolic 3-manifold. Its attribution continues on p. 143. Neither the question nor the chapter introduction imposes orientability. The original problem page was visually checked.

The relevant objects are geometrically distinct embedded closed geodesic circles in the given metric. Counting repeated traversals or replacing each geodesic by an unrelated embedded representative would not answer it.

Burns–Matveev Question 5.6.1, pp. 12–13, asks the same finite-volume hyperbolic three-dimensional question. The subsequent discussion suggests a broader variable-curvature problem; the following nonpositive-curvature section is separate. Thus 20001896 is a duplicate of this exact target, not a second independent discovery opportunity.

Sources: [K3 preliminary author PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), [Burns–Matveev AIM text](https://aimath.org/pastworkshops/geodesicsproblems.pdf).

## Closed manifolds

Luo–Marković's arXiv:2608.29761v1, submitted 30 August 2026, states the required infinitude in Theorem 1.5, p. 2. Its conventions fix a closed hyperbolic manifold of dimension at least three without an orientability restriction. Theorem 1.4 gives an asymptotic collar statement with exponent \(\kappa>3/(n-2)\). Definitions 1.1–1.2 and the paragraph before Theorem 1.5 ensure that the counted simple geodesics are prime. The theorem page was visually inspected.

The local definition also directly excludes both self-intersections and iterates: equal image points have ambient distance zero, and the collar implication then forces their circle distance to vanish. This is the required embedded-geodesic notion. No projection from an orientable double cover is being used.

The paper explicitly names Kirby Problem 3.16. Its PDF has internal date 1 September 2026; the arXiv submission date is earlier. Both the versioned and current arXiv records were checked. They list v1 and no journal reference. Preprint attribution is therefore appropriate; this audit does not assert peer-reviewed publication.

Source: [Luo–Marković, versioned primary preprint](https://arxiv.org/abs/2608.29761v1).

## Cusped manifolds

Kuhlmann's published Theorem 1.1 expressly assumes an **orientable** cusped hyperbolic 3-manifold. The statement and its definitions concern geodesic knots, hence embedded geodesics. This supplies the orientable finite-volume noncompact case. Its theorem page was visually checked. Attributing nonorientable coverage to this theorem alone would exceed its stated hypotheses.

Xia's Theorem 1.2, p. 2, and Theorem 4.1, p. 8, explicitly cover nonelementary hyperbolic 3-manifolds with a virtually rank-two cusp and explicitly include all cusped finite-volume examples. Section 3 handles toral cusp groups; §4 treats orientation-reversing cusp transformations. Thus ambient nonorientability is not omitted, including when a chosen cusp is toral. The main theorem page was visually checked. The current arXiv record lists v1, submitted 27 October 2021, without a journal reference.

Sources: [Kuhlmann, AGT 6 (2006), 2151–2162](https://msp.org/agt/2006/6-5/agt-v6-n5-p04-p.pdf), [Xia, arXiv:2110.14376v1](https://arxiv.org/abs/2110.14376v1).

## Exhaustion of the scope

A complete noncompact finite-volume hyperbolic 3-manifold has a rank-two cusp and is nonelementary. Its compact flat cusp cross-sections are tori or Klein bottles. Consequently, the stated results cover the four relevant cases:

| Manifold | Direct source |
|---|---|
| Closed, orientable | Luo–Marković, Theorem 1.5 |
| Closed, nonorientable | Luo–Marković, Theorem 1.5 |
| Noncompact finite volume, orientable | Kuhlmann, Theorem 1.1; also Xia |
| Noncompact finite volume, nonorientable | Xia, Theorem 1.2 / 4.1 |

The standard finite-volume cusp classification justifies this partition. The argument does not assume that an embedded geodesic in a finite cover projects to an embedded geodesic below; that implication would be false in general.

The conclusions concern infinitely many individual simple geodesics, not an infinite pairwise-disjoint collection. They do not establish a fixed uniform collar for all geodesics, or settle arbitrary variable-negative-curvature metrics, infinite-volume manifolds, or orbifolds.

## Audit boundary and disposition

The frozen package accurately separates theorem-scope verification from independent proof verification. This review examined the original questions, definitions, conventions, theorem statements, applicable case splits and current bibliographic records. It did not conduct a complete adversarial audit of all estimates in the two preprints. Reading their contents or checking their hypotheses does not amount to such a proof certificate.

The five source PDF hashes and byte sizes all match the package's manifest; the artifact hash also matches the assigned frozen version. These are source-identity checks, not numerical evidence for the universal theorem. Their receipt is source_verification.json.

No correction to SOURCE_STATUS.md is required for this verdict. The package is suitable for publication as an attributed bibliographic status update with its existing preprint and proof-audit qualifications retained. A project status should not credit this as a newly discovered or independently proved solution. Historical pre-August-30 open-status notes may remain as dated records, but are not current summaries of the cited literature.

This audit does not re-certify the author's repository-wide prior-attempt search. A publication owner should retain the ordinary one-target/one-PR duplicate check.
