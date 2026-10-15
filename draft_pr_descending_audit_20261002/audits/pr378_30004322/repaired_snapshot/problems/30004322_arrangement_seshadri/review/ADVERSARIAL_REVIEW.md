# Independent full review: Seshadri constants of arrangement singularities

**Scoped PASS for all five author turns. The original conjecture remains unsolved5/5. No mandatory mathematical correction.** This is an independent AI-assisted source/proof audit, not external peer review, formal verification or a certification of historical novelty.

## Binding, target and source scope

The immutable36-file author packet is bound by FINAL_AUTHOR_MANIFEST.json SHA2567df340e34bab39476fcafb29c1f980617c477f698d06ed9fb18f931367ccb101 and WIP commitdd1736df47b536de489f8e5a651f22a1ebca6205 on math/30004322-arrangement-seshadri-wip. Every raw remote file and Git blob ID independently matches. No author byte was changed.

I read Szemberg's complete contribution on OWR printed3295–3297 and the organizers' discussion on3272, and visually checked the exact conjecture on3297. Its maximum collinearity is over **all projective lines**, not only arrangement components. The source concerns the full singular set of a reduced arrangement of distinct complex lines. A one-line arrangement has an empty singular set and is not assigned1/0; a pencil has a single point and constant1. Pokora's original Question3.1 uses the potentially stronger component-line formulation, which is not silently substituted here.

The organizer report already announces the small-arrangement result through12 lines and a prior LP approach. Pokora's Proposition3.3/Example3.4 give the credited full Fermat/CEVA values. His examples also use auxiliary curves and lines in Bézout arguments, so the method itself is not new. Hanumanthu–Harbourne's definition agrees with the modular-point hypothesis used in turn3. The July2024 curve-configuration manuscript preserves the general line question and proves additional conditional results, not a universal theorem used here.

For publication, retain both legitimate dates: OWR report53/2019, workshop10–16November2019, and actual EMS publication **19November2020**. The all-lines formulation and primary dates are confirmed at https://ems.press/journals/owr/articles/17296 .

## Turn1: finite-degree exact test

The arithmetic-genus inequality is valid for the strict transform of an integral plane curve after blowing up the distinct specified points. That strict transform remains integral, so its arithmetic genus is h1(O)≥0 over C. Ordinary singularities, general position and very-general-point assumptions are not needed. Cauchy–Schwarz gives the stated inequality in the total multiplicity S.

The proof uses monotonicity of S²−rS only above r/2 and explicitly incorporates the necessary degree threshold into D. The quadratic coefficients A=k²−r, B=2k−rk+3r and C0=1−3r are correct. The isqrt expression gives the exact floor of the positive root; no numerical root estimate controls the search. The strict condition r<k² is essential and is never assumed for every line arrangement.

The algorithm's multiplicity vectors include every violating integral curve. A nonzero fat-point polynomial may be reducible or nonreduced, but its degree/actual-multiplicity ratio bounds a component ratio from above. Components avoiding Z add only degree and cannot invalidate the inequality. Thus candidate d/S values are still upper bounds for epsilon. Conversely, all violating integral-curve ratios lie in a finite set after the degree bound, so their infimum is attained and included. This justifies the exact minimum, not merely a decision procedure for one inequality.

For coordinates in the stated effective subfield K⊂C, the linear equations have coefficients in K. Their rank does not change on extending scalars to C, so exact K-linear algebra detects a complex kernel without an irreducibility or complex-coefficient oracle. The algorithm does not promise computability for arbitrary unnamed transcendental inputs or polynomial-time complexity.

The off-conic control is correctly limited to arbitrary point sets. It is not asserted to be the full singular locus of an arrangement. My separate control uses a different eighth point, and reconstructs the exact line maximum and all relevant conic evaluation ranks.

## Turn2: Hesse auxiliary cover and the global dual

The general weighted-line argument separates the support-line exceptions before applying Bézout. Non-support curves satisfy the weighted multiplicity bound, while each support line is handled by its actual point count. The comparison tau≤k0 therefore proves both the all-lines maximum and the exact Seshadri constant.

I independently reconstructed the12 Hesse lines,9 quadruple points,12 double points and9 auxiliary Fermat lines over Q(zeta3), using actual projective equations rather than the author's incidence table. Every pair intersection is accounted for. The arrangement-only cover has matching cost6 certificates. The augmented primal weights1/4 and1/6 and the dual point weights1/6 and1/4 give cost9/2 exactly.

The global dual qualification is justified in the correct order: the primal certificate first bounds every other line's point count by4; only afterward is the dual checked on arbitrary auxiliary lines. There is no circular use of global LP optimality. Separate exact checks also enumerate all lines spanned by pairs of these21 points; lines with at most one point have trivial dual constraints. The nonlinear ratio gap2/9 and identification of the twelve computing lines follow as stated.

The value1/5 is presented as a recovered known small-arrangement case, not a new resolution. The distinct Hesse conic example in the additional Janasz–Pokora source is general prior context; no identification of its point catalog with this explicit twelve-line arrangement is needed for the proof.

## Turn3: two arbitrary added lines and the multiplicity corollary

Absorbing added lines through the modular point preserves the pencil-union coverage property. Every singular point outside that union must lie on one of the at-most-two unabsorbed new lines. Each such line has m distinct pencil intersections, because it avoids the pencil center. The case split on k_A is complete. In the only unresolved-looking case, each new line has at most one further point, so their outside union has at most two points and a single auxiliary line covers it.

The resulting cover has degree at most k_A, while k_actual may be larger. The final Bézout proof uses k_actual; it never assumes equality with the component maximum. Including zero-weight component lines in the finite exceptional list is legitimate: the positive cover remains unchanged, and those lines' finite point counts are separately handled. This yields the promised finite determination of the actual all-lines maximum.

The high-multiplicity corollary also has a complete dichotomy. Either the uniform half-weight cover is short enough, or every outside-pencil component already uses its full allowed point count on the m pencil intersections. Then no off-pencil singular point can exist. Pencils are handled separately. My additional45 rational projective arrangements exercise the pencil, full-added-cover and auxiliary-joining-line branches and independently inspect all point-spanned lines.

## Turn4: deletion criteria and exact losses

The full Fermat proof correctly uses n≥3, so every grid point and pencil center has multiplicity at least3. For a retained line, its lost grid points are exactly those whose other two incident lines were deleted. Its center is retained only when at least two lines in that pencil remain; this qualification is explicit.

The sumset size criterion, the strict uniform budget D²+3D<9n, and the separate D≤n−2 condition are sufficient rather than necessary. Summing three failed inequalities gives the stated contradiction. The complete-pencil special case retains the required second pencil center. The total loss count P−2T correctly changes the multiplicity-three count to one when all three incident lines were deleted. No claim extends the inherited value to arbitrary deletions.

## Turn5: all-q incidence and component-cover optimality

For every q≥1, residue0/2/3 retention in each 5q-pencil gives exactly7q² triple and6q² double grid points, plus three distinct coordinate vertices. Each allowed residue triple has q² lifts because two indices determine the third uniquely modulo5q. The q=1 centers still have multiplicity3 and remain singular; they must not be confused with the separately counted grid triples.

The residue-dependent line point counts are3q+1 and4q+1. Primal weights1/3,1/2,1/2 cover every grid type and each center, with total4q. Bézout therefore controls every noncomponent curve of every degree, including auxiliary lines. The all-lines maximum and exact constant1/(4q+1), with exactly6q computing components, follow rigorously.

The dual assigns1/q only to000 points and1/(2q) only to double points. Its load is exactly1 on every retained component, establishing the **component-cover** optimum4q. It does not certify an unrestricted auxiliary-line optimum, and the packet correctly declines that claim. The changed value relative to the full15q-line arrangement is compatible with turn4's sufficient deletion limits.

I independently reconstructed the actual projective point and line equations over Q(zeta5), Q(zeta10) and Q(zeta15) for q=1,2,3, including pair-intersection exhaustion and all primal/dual component constraints. For q=1,2 I also checked every point-spanned projective line and the stated set of computing components. These finite controls support the written all-q residue proof; they are not a replacement for it.

## Reproduction, limits and disposition

All214,070 author assertions replay byte-for-byte. All62 historical/final public bindings and six local source bindings verify. Every one of the36 raw Git blobs at the bound WIP head matches. Independent controls add93,918 exact assertions, including21,320 integer cutoff cases, exact conic kernels, rational modular-point arrangements, cyclotomic Hesse/subfamily geometry and separate deletion counts.

Both the first author checker and the independent cyclotomic checker require SymPy. The portable review verifier takes an explicit author directory. If source PDFs are absent from a public checkout, its author replay must report zero source files checked; this is an explicit omission, not a claim that absent PDFs were validated.

The full original line-arrangement conjecture remains unresolved. Publish the five scoped results as **unsolved5/5**, preserving their source credit, the effective-coordinate restriction, the strict r<k² range, all-lines versus component distinctions, and the limited final dual. No sixth author search, raw-source redistribution or historical novelty claim is part of this review.
