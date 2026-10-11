# Source and prior-art audit: PCF descent, 20001424

Checked 2026-09-30. Historical novelty is not established by this audit.

## Original question and precise scope

The complete pinned record and its imported prior research report are in `source_record.json`. The canonical AIM entry is workshop `finitedynamics`, Section2 “Moduli Problems,” problem2.6:

> Are all PCF maps defined over their field of moduli?

The live [AIM problem-list page](http://aimpl.org/finitedynamics/2/) repeatedly returned errors/timeouts during this audit. No claim is made to have reread its full live page. The user-authorized pinned canonical statement was therefore used, and the official [2014 workshop announcement](https://aimath.org/pastworkshops/finitedynamics.html) was independently retrieved. It confirms the rational-self-map/conjugacy context and links to that problem list. Its [workshop report](https://aimath.org/pastworkshops/finitedynamicsrep.pdf) describes the rigidity discussion. No extra odd-cardinality hypothesis appears in the pinned original question.

The candidate concerns characteristic-zero rational self-maps of P1, of degree11, over the algebraic numbers. It uses the usual absolute field of moduli of a PGL2-conjugacy class. This is stronger than producing a transcendental example whose moduli field is merely R. The graph, rather than a coefficient list, specifies the conjugacy class exactly.

## Prior-attempt gate

All-state numeric-ID/title PR searches, matching branches, ID-path history, existing attempt folders and repository code/title searches found no earlier attempt by this repository/campaign. The queue at the base commit was queued,0/5. Matches occurred only in QUEUE and SHORTLIST.

The upstream AIM report does contain a substantive third-party attempt. It proves an odd canonical-divisor criterion under trivial dynamical automorphisms. That report is preserved as prior context and is not claimed as new work. No provenance linking it to an earlier attempt in this repository was found.

## Established descent results and the imported report

[Silverman, *The field of definition for dynamical systems on P1*](https://www.numdam.org/item/CM_1995__98_3_269_0/), Compositio Math.98(1995),269–304, was retrieved in full. Theorem2.1 and Corollary2.2 explain the conic obstruction in the trivial-automorphism case; Theorem5.1 handles even degree and polynomial classes. An odd-degree rational divisor on that conic forces a rational point. Applying this established mechanism to a reduced odd postcritical set is the imported report's partial criterion. Its required trivial-automorphism hypothesis cannot simply be dropped. The candidate has an even postcritical cardinality and does not challenge this criterion.

The report's citation to a supposed general characterization by Bresciani must be corrected. [arXiv2405.03612](https://arxiv.org/abs/2405.03612) explicitly records withdrawal on May9,2024: a main argument confused ramification indices with vanishing orders. The original [v1](https://arxiv.org/pdf/2405.03612v1) was recovered, but its main theorem is not used as an established result. The missing v2 PDF is a withdrawal issue, not evidence of an inaccessible valid theorem.

## Graph realization and symmetry sources

1. **Hlushchanka**, [*Tischler graphs of critically fixed rational maps and their applications*](https://arxiv.org/abs/1904.04759), current PDF v2, posted October5,2025. The complete16-page source was read, with Theorem2 and the charge-graph construction visually checked. Relevant locations: Theorems1–2, definition of planar isomorphism in Section2, Corollary6, and Section5/Lemma7/Proposition8. The classifier uses orientation-preserving graph isomorphisms. Section5 gives degree as edge count plus one and local degree as valence plus one. The inverse is built from intrinsic fixed internal rays; this is essential to the symmetry argument.
2. **Hlushchanka–Prochorov**, [*Critically fixed Thurston maps: classification, recognition, and twisting*](https://arxiv.org/abs/2212.14759), [PLMS132(2026),e70129](https://doi.org/10.1112/plms.70129). Section3.3 reviews the rational classification. The 2026 publication metadata and current description confirm that the graph framework is established prior work, not a new result of this attempt.
3. **Hidalgo–Quispe**, [*On Real and Pseudo-Real Rational Maps*](https://arxiv.org/abs/1502.05306). Sections2.1/2.3, Lemma4 and Theorem6 explain real models, reflections, and the trivial-automorphism pseudo-real criterion. Their general families are not automatically PCF. The candidate supplies its own short no-real-model and field-of-moduli arguments.
4. **Bonifant–Buff–Milnor**, [*Antipode Preserving Cubic Maps: the Fjord Theorem*](https://arxiv.org/abs/1512.01850), [PLMS116(2018),670–728](https://doi.org/10.1112/plms.12075). The antipode-preserving cubic family and its PCF hyperbolic centers are already studied there. This is an important prior-art warning against claiming novelty for antipodal dynamics or assuming degree11 is minimal. No theorem asserting that a particular cubic center is a field-of-moduli counterexample is imported without a separate check of its symmetry. The current candidate instead gives a completely specified plane graph and a complete symmetry calculation.

## Novelty and verification boundary

Exact searches combined “critically fixed,” “postcritically finite,” “pseudo-real,” “antipodal,” and “field of moduli,” along with the relevant authors. No exact prior appearance of the decorated degree11 graph or an explicit statement of this same descent counterexample was verified. The graph-realization method and pseudo-real obstruction are known, and relevant cubic families predate this attempt. A bounded negative search cannot establish priority or novelty.

`CANDIDATE.md` is a proposed consequence of established results with a fully specified graph. The finite checker confirms the graph calculation only. A separate adversarial review is required before a draft PR. Source reference files remain outside the repository; links, locations and hashes are recorded rather than redistributing source PDFs.
