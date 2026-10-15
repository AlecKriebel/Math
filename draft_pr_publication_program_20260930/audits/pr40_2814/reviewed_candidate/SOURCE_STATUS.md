# Current literature status of Kirby Problem 3.16

**Status checked 2026-09-30: the complete target is covered by existing theorem statements, including a new August 2026 preprint. This is a source-status correction, with no new mathematical result claimed.**

Luo and Marković's preprint supplies the closed case that the pinned dataset still calls open. Kuhlmann supplies the orientable cusped case, and Xia explicitly supplies the nonorientable cusped case. The newly located closed theorem is a preprint result; this report verifies its identity and scope and does not represent an independent referee certificate for its proof.

## Exact source and interpretation

The author-hosted preliminary version of *K3: A New Problem List in Low-Dimensional Topology*, AMS Mathematical Surveys and Monographs 295 (2026), prints Problem 3.16 on page 142, with attribution to A. Reid on page 143. It asks whether every finite-volume hyperbolic 3-manifold has infinitely many simple closed geodesics. The pinned record reproduces this question accurately. The rendered page was inspected. [K3 author PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)

Here a hyperbolic manifold is a complete, boundaryless, torsion-free quotient of hyperbolic space, with its given hyperbolic metric. No orientability assumption appears in the question. A simple closed geodesic is an embedded geodesic circle, counted by its image. Reparametrizing or traversing one circle repeatedly does not give additional examples. The problem does not ask merely for embedded curves in geodesic free homotopy classes: replacing an embedded curve by its geodesic representative can lose embeddedness in dimension three.

The same target is Question 5.6.1 in the Burns–Matveev AIM text, pages 12–13, represented by upstream ID20001896 / AIM-GEOMETRY-0234. The following section on nonpositive curvature is unrelated extraction spill. [AIM original PDF](https://aimath.org/pastworkshops/geodesicsproblems.pdf)

## The closed case now has a primary-source resolution claim

Qiliang Luo and Vladimir Marković, *Simple geodesics in closed hyperbolic manifolds*, arXiv:2608.29761v1, was submitted August 30, 2026. The downloaded PDF's internal date is September 1. Its Theorem 1.5, page 2, states infinitude for every closed hyperbolic manifold. The conventions and Theorem 1.4 impose dimension at least three but no orientability restriction. [Versioned primary preprint](https://arxiv.org/abs/2608.29761v1)

Theorem 1.4 gives a stronger asymptotic statement: for any fixed positive length-window width and any exponent greater than 3/(n−2), the proportion of geodesics in that window lacking the indicated inverse-polynomial collar tends to zero. Their definition of a collar excludes self-intersections and iterates. Theorem 1.5 is therefore about genuine simple geodesics. The full 13-page paper was read; the stated hypotheses directly cover closed nonorientable manifolds too. This application does not rely on projecting simple geodesics from an orientable double cover.

The arXiv record currently lists only v1 and no journal reference. Thus the proper attribution is an existing preprint theorem, not a new result of this project or a claim of established peer review.

## Cusps and orientability

Sally M. Kuhlmann, *Geodesic knots in cusped hyperbolic 3-manifolds*, Algebraic & Geometric Topology 6 (2006), 2151–2162, Theorem 1.1, expressly assumes orientability. The theorem and its final proof on page 2160 were inspected. Its knots are geodesic and embedded, rather than arbitrary embedded representatives. The pinned background's unqualified attribution of the entire cusped case to this paper is too broad when nonorientable manifolds are included. [Published primary paper](https://msp.org/agt/2006/6-5/agt-v6-n5-p04-p.pdf)

Feihuang Xia, *Simple closed geodesics in cusped hyperbolic 3-manifolds*, arXiv:2110.14376v1 (2021), Theorem 1.2 on page 2 and Theorem 4.1 on page 8, covers any nonelementary hyperbolic 3-manifold with a virtually rank-two cusp. It explicitly includes all cusped finite-volume hyperbolic 3-manifolds. Section 4 handles the orientation-reversing cusp transformations; Section 3 treats toral cusps. The full 11-page text was inspected, including both cases. The arXiv record located is a preprint. [Versioned primary preprint](https://arxiv.org/abs/2110.14376v1)

A complete, noncompact, finite-volume hyperbolic 3-manifold has rank-two cusp ends, with flat torus or Klein-bottle cross-sections, and is nonelementary. Xia therefore supplies the remaining nonorientable cusped scope; no descent-of-embeddedness shortcut is needed.

## Scope conclusion and historical correction

The cases exhaust the original question:

- Closed, orientable or nonorientable: Luo–Marković, Theorem 1.5
- Cusped and orientable: Kuhlmann, Theorem 1.1; also Xia
- Cusped and nonorientable: Xia, Theorem 1.2 / 4.1

These existing results give a positive answer at the level of the cited theorem statements. The August 17, 2026 triage in record2814 and the August 8 triage attached to duplicate20001896 both predate the August 30 closed-case preprint. Their historical claims need not be erased, but neither should be presented as a current open-status assessment.

This source correction covers finite-volume hyperbolic 3-manifolds only. It makes no claim about arbitrary variable negative curvature, infinite-volume manifolds, orbifolds, pairwise disjoint geodesics, or a uniform collar width for all geodesics.

## Prior work and audit boundary

No earlier project attempt was found in the current main tree, the complete returned list of 30 open/closed PRs, or the available local attempt folders. The main tree snapshot was untruncated. The imported AIM duplicate has a third-party partial report concerning finite-cover descent. It was read completely and preserved as prior art; it is not evidence that Alec or this campaign already attempted this target. The two IDs nevertheless represent one mathematical target and must not receive independent proof budgets or duplicate-result credit.

No substantive new proof attempt was started: the current literature already supplies the missing case. No numerical census or finite experiment could certify the universal theorem, and none is offered as such. Separate review should confirm these source and scope checks before publication. A fully independent adversarial audit of the cited preprint proofs remains outside this compact bibliographic correction.
