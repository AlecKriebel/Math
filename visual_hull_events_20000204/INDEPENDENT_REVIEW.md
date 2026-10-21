# Independent mathematical review

Date: 2026-10-21. Problem identifier: 20000204 / queue row 1859.

## Verdict

PASS for the explicitly scoped elementary lemmas, counterexamples, and conditional algebraic-envelope consequence in RESEARCH.md. NOT ACCEPTED as a new resolution of the unrestricted AIM question, a new proof of the known two-type classification, a classification of all singular/non-generic event surfaces, or a realization theorem.

The review checked the complete mathematical draft, independently reconstructed the global quantified activity formula, proved the local escape and orientation criteria, checked the counterexamples, inspected the relevant 2004 and 2018 source passages, and reran checks.py successfully. The script verifies exact arithmetic and signs, not the full geometric proofs or a CAD computation.

## Accepted scopes

1. For a specified nonempty compact regular-closed semialgebraic solid, the all-external-view hull is closed, compact, contains the solid, and lies inside its convex hull. The stated quantified formula characterizes its artificial boundary exactly. Effective quantifier elimination is available when all input coefficients are effectively represented real algebraic numbers. This is an in-principle decision method, not a practical performance claim or an event-type catalogue.
2. For a line with finitely many smooth boundary contacts, no interior intersections, and a fixed point outside the object, strict positivity of the signed-normal escape inequalities produces a free line through that point. The uniform local argument and compact complement justify the perturbation globally. The positive-dependence condition and its two-contact orientation consequences are necessary, not sufficient. Odd finite-order contact for a regular defining function forces an interior crossing.
3. Convex objects have no artificial boundary. The quartic perturbation construction gives an open family of coercive strongly convex polynomials meeting the general projective quartic locus; hence positive complex edge degree 160 does not imply activity. No explicit general quartic or extra differential genericity is computationally certified. The spherical-shell example correctly separates filled invisible volume from artificial boundary.
4. The three disjoint unit balls with longitudinal coordinates 3, 6, 9 give an exact local-versus-global obstruction. Every sufficiently small rotation of the tritangent axis through the origin hits a ball; a direction in the plane x=0 remains free. The displayed translated lines approach that axis while remaining free. Outward-normal signs, strict-distance inequalities, positive dependence, and disjointness are correct. This example has disconnected, reducible algebraic boundary and is not promoted to a general irreducible projective example.
5. Under the separate real generic external-hull and complex general-projective hypotheses, the patch-level closure argument yields only unions of the edge and tritangent components. The degree formulas are used only for d>=3, with absent low-degree components omitted. Exact values for d=3 through 7 were independently checked. This is a necessary restriction and formal consequence of cited results, with no novelty or attainability assertion.
6. The three orthographic-direction reconstruction of a ball has the stated artificial cylinder patch. These are cameras at infinity, not three finite perspective centers. The general semialgebraic formula accommodates singular solid boundaries, but the smooth-contact lemma and two-type catalogue do not thereby extend to them.

## Source distinctions checked

Bottino–Laurentini (2004), Proposition 5 and surrounding Sections 2–4, gives the known necessary tangent-crossing/triple-point candidate restriction in the generic smooth external-hull model, followed by local and visibility pruning. Kohn–Sturmfels–Trager (2018), Section 4 / Theorem 4.1, gives five algebraic visual-event discriminant components for a general projective surface. These are not conflicting classifications: the latter is not a real active hull-boundary theorem. Smoothness alone does not abolish cusp-crossing, flecnodal, or parabolic events.

Sources: https://doi.org/10.1109/TPAMI.2004.130 ; https://cgvg.polito.it/Articles/The%20Visual%20Hull%20of%20Curved%20Objects.pdf ; https://doi.org/10.1007/s40306-017-0240-1 ; https://arxiv.org/abs/1707.01877 ; http://aimpl.org/algvision/4/ .

## Rejected promotions and remaining limits

- Do not replace the patch-level statement by a new pointwise theorem covering every seam and exceptional higher-contact line without additional support.
- Do not infer a real active patch, or realizability of a degree-spectrum alternative, from a positive complex degree.
- Do not infer global hull membership from generator root isolation, signed-normal dependence, local rotational trapping, or existence of nearby free lines.
- Do not reuse the imported detailed nine-symbol piecewise-smooth table as independently checked: only the limited recovered preview was inspected for that paper.
- No full CAD computation, explicit nonconvex general algebraic active-patch certificate, universal singular catalogue, or finite-perspective theorem was established.
- The source/status gate and this review establish no universal openness assertion and no novelty claim.

## Publication scope

This acceptance report covers the mathematics above. The published executable replaces assertion statements with explicit exceptions so that optimization does not disable its checks. The complete transformed syntax tree was compared with the accepted original after reversing exactly that replacement. Exact finite tests support the listed arithmetic only, not the general proofs.
