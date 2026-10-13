# Independent final editorial and reproduction acceptance

Row 1761 / problem 30002861 / OWR-13678-002. Reviewed 13 October 2026 UTC.

## Decision and identified edition

**Accepted without mandatory correction.** The final five-pass mathematical edition presents its accepted results, exact finite certificates, corrections, inherited dependencies and unresolved question accurately. This is an editorial and reproduction review of the completed sequence, not a sixth substantive mathematical pass or a new external peer review.

The reviewed collection consists of 56 public Markdown and JSON files totaling 692,621 bytes. Its [CONTENT_MANIFEST.json](final_edition/CONTENT_MANIFEST.json) has SHA-256 `30826908e280df3eec7cc2634b298cd5f16641d02661acfafbfc1b3214a78f97`. That identity specifies the reviewed collection; it is not a mathematical proof. This separate acceptance is not included in that collection's count or manifest.

The review covered the [final reader guide](final_edition/README.md), [progression](final_edition/PROGRESSION.md), [dependencies](final_edition/DEPENDENCIES.md), [correction record](final_edition/CORRECTIONS_AND_SCOPE.md), [reproduction guide](final_edition/REPRODUCTION.md), both fifth-pass proofs, the [boundary-completion acceptance](final_edition/INDEPENDENT_BOUNDARY_COMPLETION_ACCEPTANCE.md), the [additive-obstruction acceptance](final_edition/INDEPENDENT_ADDITIVE_OBSTRUCTION_ACCEPTANCE.md) and all three new finite certificates. It also checked the retained corrected fourth edition and the earlier editions nested within it. The preceding mathematical audits remain the accepted basis for their results; this review does not pretend to re-audit every earlier universal theorem from scratch.

## Mathematical conclusions and limits

The [canonical-collar theorem](final_edition/FIFTH_PASS_BOUNDARY_COMPLETION.md) is valid with its stated strict adjacent-turn inequalities. Its argument establishes global supporting-half-plane inequalities and all common-face intersections, including lower-dimensional contacts. The outside vertices form a genuine conforming collar for arbitrary strictly ordered straight-side subdivisions. A simple outside boundary is obtained by proof rather than assumed from a drawing or finite sample.

The finite completion criterion retains every necessary degree-parity, activity and nonzero-weight qualification. Each old edge uses its actual opposite vertices; a boundary subedge uses the forced exterior point of its strict side. The common factor relating the normalized fan coefficients to the two determinant coefficients is nonzero. Consequently successful individual balances produce an actual closed balanced component and the accepted quartic obstruction. A single boundary product does not replace the individual equations. No input satisfying all these tests is supplied, so this is a finite verification and construction interface, not an existence solution.

The boundary-chord argument uses only the corrected equality on an actual incident edge segment. At a strict corner the local common polynomial is a nonzero product of the adjacent side-line forms, obtained from a genuine exterior triangle. At a straight boundary vertex its other zero line is the forced exterior line. Therefore boundary chords can only form a noncrossing matching of straight boundary vertices, with the order Q_i, v, w, Q_j along their common line. The conclusion about an interior opposite vertex applies exactly to a triangle incident with a boundary edge. It does not apply to every triangle that merely touches a boundary vertex.

The [additive obstruction](final_edition/FIFTH_PASS_ADDITIVE_OBSTRUCTION.md) is confined to the exact fifteen-vertex, twenty-one-face candidate with all old coordinates and geometric faces retained. Its twenty-eight old interior equations determine all fifteen weights up to one common arbitrary nonzero scalar. This includes negative scaling and does not impose a new positivity restriction. At each of its two reflex vertices, the forced line is strictly separated from the entire available unbounded cone, including its bounding rays. Convexity would make that old reflex vertex interior and require a prohibited second triangle. The reasoning applies to simultaneous additions and arbitrary numbers or valences of new vertices. Retriangulating or subdividing old faces, moving old coordinates and using a different candidate remain outside the theorem.

The weight system's rank fourteen and the actual quartic reduced system's rank eight refer to different matrices. The old nonconvex candidate has full actual row rank and is not a quartic counterexample. Neither the additive obstruction nor the canonical-collar criterion resolves the general quartic existence question.

## Independently reproduced finite evidence

In addition to the exact certificate reconstructions supplied with the edition, this review performed a separately written rational-arithmetic reconstruction using the displayed candidate formulas and the public mathematical inputs. No author or earlier auditor implementation was imported into that reconstruction.

For the [additive candidate certificate](final_edition/ADDITIVE_OBSTRUCTION_CERTIFICATE.json), it reproduced the coordinates, all twenty-eight endpoint determinant pairs and balances, the rank-fourteen weight system, the normalized tree determinant -1, both primitive forced lines, all whole-cone coefficients and both negative cone-coordinate pairs for the algebraically valid but geometrically illegal point P_1. It independently reconstructed the actual fan rows and obtained rank eight and normalized maximal-minor determinant 1. The same-color determinant for vertices 2, 5 and 13 is again

    -217587275/3719962464204,

so the candidate is genuinely outside the three-color-line pencil class.

For the [author collar certificate](final_edition/BOUNDARY_COMPLETION_CERTIFICATE.json) and [independent collar certificate](final_edition/INDEPENDENT_COLLAR_CERTIFICATE.json), the reconstruction checked all seven listed polygon controls, including the rational-circle pentagon, rational octagon, highly anisotropic affine images and very small positive subdivision parameters. It obtained the stated forced exterior points, side signatures, incidences and vertex-edge-face counts. Exact sequential half-plane clipping tested 2,271 triangle pairs in total: 210 in the additive candidate, 576 in the three author polygon controls, 1,107 in the four independent polygon controls and 378 in the retained integer mesh. Each pair met in exactly its prescribed common simplex, including empty, point and segment intersections.

For the integer control, independent assembly reproduced the complete 27-by-12 magnitude matrix and the nonzero maximal minor

    -6624693947958945585230391966837094249267200/402018373.

Its rank is twelve. The cyclic boundary-transfer product is

    585991946946275/301150964543077,

which is not one. Thus this exact legal collar remains magnitude-unbalanced. The supplied reconstructions also reproduce the full compatible face-sign-normalized rows, their common determinant factors, and all six actual exterior polynomial factorizations. Different fan starts and local face signs are explicitly distinguished in the reproduction guide.

Meaningful controls confirm the distinctions: changing an old weight breaks an interior equation; duplicating a tree row destroys its full minor; a legal reflex-cone point does not lie on its forced line; P_1 lies on that line but outside the legal cone; duplicate geometric faces violate the mesh condition; changed determinant coefficients disagree with the geometry; and the full-rank control has no claimed dependency. The legal local subdivided-side example has transfer -2, rejecting an unjustified positivity requirement. The edition's certificate mutation checks likewise reject altered exterior points, transfers, ranks, minors, line and cone coefficients, and exterior polynomial factors.

These finite computations verify the stated finite witnesses and controls. The all-polygon collar theorem and all-additions obstruction rely on their written geometric proofs and independent mathematical acceptances, not extrapolation from finite experiments.

## Editorial integrity, corrections and attribution

The final edition contains one exact copy of the accepted corrected fourth public collection, with its earlier editions nested once. All public manifest entries and 349 local reference targets were verified, including all five section-anchor references. The new material does not silently replace or widen a predecessor theorem.

The [incident-segment correction](final_edition/fourth_edition/third_edition/CORRECTION_NOTE.md) is preserved: the piecewise function agrees with its local common polynomial on actual incident segments; continuation along a whole supporting line is a statement about an individual adjacent polynomial piece. The [full-eighteen-vertex topology theorem](final_edition/fourth_edition/third_edition/THIRD_PASS_CEVA_OBSTRUCTION.md) remains distinct from the [complete nested-ring-core theorem](final_edition/fourth_edition/third_edition/THIRD_PASS_NESTED_RING_EXTENSION.md), which does not exclude arbitrary irregular proper components in larger meshes. The fourth-pass phrase correction from “change of topology” to “change of triangulation incidence” preserves the underlying disk and every mathematical datum.

The fifth-pass editorial changes add precise proof and certificate references, record the already supplied mathematical acceptances and clarify the boundary-edge meaning of “boundary triangle.” They do not change the fifth-pass mathematical conclusions. The exact candidate-specific and unresolved-existence qualifications remain intact.

All included artifacts are authored mathematical or bibliographic Markdown and JSON. Hash references identify included public artifacts or the six already recorded scholarly PDFs. The collection does not include programs, copied source documents or coordinate datasets, private material, or hashes identifying withheld operational objects. A bibliographic link to a public ancillary source is not redistribution of that program.

The cubic negative result remains credited to Junkai Qiu's [versioned September 2026 preprint](https://arxiv.org/abs/2609.06364v1). Its earlier accepted exact reconstruction remains identified as a 41-vertex example with full spline-space dimension 107 and evaluation rank 40. This review does not claim a new cubic counterexample or a new source inspection. The inherited literature and manuscript-status observations retain their original dated limits.

## Final disposition

The bundled row remains **unsolved**. The general fixed-mesh quartic value-and-gradient question remains unresolved. The count is **five newly documented shared substantive passes**, with an unknown lifetime total. Branches, audits, corrections, editorial work and publication add no pass. No sixth pass, novelty, priority, worldwide-openness, external-peer-review or universal-quartic claim is introduced.

The final edition is accepted for its stated mathematical and editorial scope. Publication status and any later changes are separate questions; this acceptance does not certify an uninspected revision.
