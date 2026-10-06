# PR97 independent adversarial review: C1 pencil and disk regularization

**Verdict: the analytic proof and the usual smooth contact-form conclusion pass this bounded audit. A small regularity wording repair is required for the additional C1 extension.** No counterexample or mathematical gap was found in the pencil, finite-interval smoothing, or C2-disk correction. This is not a novelty or priority clearance.

The authenticated CANDIDATE.md and upstream_record.json were read first. OWN_OBLIGATIONS_BEFORE_SOURCES.md records the independent obligations before primary texts; OWN_DERIVATION.md gives the full separate argument. I did not read the old review/REVIEW.md, its code/results, or any other new reviewer's findings. Original effort remains 2/5; zero new central proof-search turns were used. No outside individual was contacted and no PR, service, queue, main, or publication state was changed.

## Strongest verified result

For a closed oriented smooth three-manifold with the assumed cooriented taut C2 foliation and C1 global forms satisfying d alpha=alpha wedge omega, nonzero alpha, and nonvanishing omega wedge d omega:

- if omega is smooth, ker(omega) is tight in the usual smooth sense;
- if omega is C1, every sufficiently C1-close smooth contact form is tight;
- if omega is C1, there is no embedded C2 disk with Legendrian boundary and with the disk and contact tangent planes distinct along that boundary.

The first statement answers Calegari Question 13.2 under the standard smooth contact-form interpretation, even if alpha and the foliation are not smooth. The latter two are precisely what the low-regularity proof directly establishes. Nothing here verifies every purported equivalence between alternate definitions of overtwistedness for arbitrary C1 plane fields.

## Source checks and hypotheses

The ROOT-retrieved primary PDFs were shared read-only and SHA256 pinned in SOURCE_READ_RECORD.json. Only the relevant complete pages were read and rendered; I did not claim to read the entire papers or the Eliashberg–Thurston book.

- [Calegari's original problem list](https://arxiv.org/abs/math/0209081), version 0.78, printed pp.1 and29: the exact question inherits a minimal taut C2 foliation, atoroidality, and nonzero Godbillon–Vey evaluation. It asks conditional tightness after assuming a contact connection form, not the construction/existence question. The global defining form is explicit in the question. Closed orientation is the stated candidate scope for the ordinary fundamental-class evaluation. Minimality excludes a spherical leaf.
- [Vogel 2011](https://msp.org/gt/2011/15-1/gt-v15-n1-p03-p.pdf), printed pp.42–43: the contact-neighborhood assertion quantifies over contacts sufficiently C0 close to a taut foliation. It is stronger than mere existence of one tight approximation. Its disk formulation has boundary tangent to the distribution and disk/contact planes transverse along the boundary; for contact structures the integral-disk alternative cannot occur. This resolves the apparent mismatch with the tangent-boundary-plane presentation of the usual overtwisted model.
- [Dathe–Rukimbira](https://arxiv.org/abs/0812.3389), printed p.5: explicitly states the same disk criterion and Proposition3.3's taut-foliation neighborhood tightness result. Its Proposition3.4 has a *closed* defining form, so it is not a direct replacement for this proof's generally nonclosed alpha.
- [Vogel 2016](https://msp.org/gt/2016/20-5/gt-v20-n5-p01-p.pdf), printed pp.2448 and2451: Definition2.2 permits a C1 contact plane field, while Theorem2.9 is the *smooth family of smooth structures* Gray theorem. Neither of these inspected pages alone proves that every overtwisted C1 structure has a C-infinity Legendrian-boundary disk. No such assertion is needed after the recommended wording repair.

Relevant PDF pages were rendered and visually read in full: Calegari PDF pages1,29; Vogel2011 pages2,3; Vogel2016 pages10,13; Dathe–Rukimbira page5. All rendering children exited0. Source-specific page/index pins and actual process receipts are retained. The standard taut-neighborhood and smooth Gray statements are imported theorems; finite symbolic computations do not reprove them.

## Adversarial checks

The distributional calculation is valid at C1: the equation makes d alpha equal to a C1 product; d(d alpha)=0 distributionally, ordinary C1 product differentiation is valid, and a continuous three-form that vanishes distributionally vanishes pointwise. No hidden C2 derivative of alpha is used.

All contact smoothing occurs on a single finite [0,S]. The lower contact-volume bound comes from the exact pencil identity, not from the limit foliation. Errors have to shrink with 1+S and with the finite norm bound B; this is possible after choosing S. There is no claim of one error tolerance for all s, no foliated Gray endpoint, and no smoothing of the foliation. Each sign is handled by the appropriate ambient orientation. Compactness and nonzero alpha provide the needed minima, and a common finite S works on finitely many components.

For the C2 disk, a fixed smooth reference knot gives a fixed solid-torus chart and a degree-one boundary projection. C2-close smooth embeddings stay embedded. Differentiation of q_j uses second derivatives of the boundary; all first derivatives of the shifted cutoff remain bounded, so q_j tending to zero in C1 makes the correction small in C1. A support radius strictly smaller than the chart radius makes extension by zero smooth. Along the boundary, the angular one-form evaluates to one exactly, preserving the Legendrian constraint. Boundary plane separation is uniformly positive and persists. A local exact model and the C1-only oscillatory counterexample independently test the mechanism; neither constructs a global solution of Question13.1.

The independent SymPy checks use explicit exception guards, and both ordinary and optimized processes exited0. The first run before the local-model addition is preserved separately; the expanded ordinary and optimized runs are the final checks. Output timestamps differ, so no byte-for-byte cross-mode claim is made. The elementary analytic bounds and source theorem checks carry the mathematical proof.

## Required wording repair R1 (low severity, only the added C1 extension)

Section1 currently says, after introducing C1 forms, that the disk may be taken smooth and calls the criterion equivalent. These words can be read as asserting that a C1 plane field always possesses a smooth Legendrian-boundary disk whenever it is overtwisted by any standard formulation. That stronger low-regularity equivalence was not proved or verified in the cited pages.

Replace that paragraph, for example, by:

> For smooth contact structures, tightness has its usual meaning and is equivalent to the absence of an embedded smooth disk whose boundary is Legendrian and whose tangent planes are distinct from the contact planes along the boundary. For C1 forms we use the explicit disk criterion: tightness here means the absence of such an embedded C2 disk. The proof also shows that every sufficiently C1-close smooth contact form is tight. We do not need a low-regularity Gray theorem or assert that the original C1 distribution has a smooth Legendrian-boundary disk.

The same distinction should be made in the theorem statement/abstract of a later manuscript if it presents a C1 extension. Alternatively, state the principal theorem for smooth omega and present the two directly verified C1 conclusions as a separate proposition. No alteration of the pencil or smoothing proof is needed. This is a wording and scope repair, not evidence against the original smooth tightness answer, and it does not consume an additional proof-search turn.

Audit completion:100% for this bounded family. No priority, novelty, whole-package publication, human-review, or service authority is supplied.
