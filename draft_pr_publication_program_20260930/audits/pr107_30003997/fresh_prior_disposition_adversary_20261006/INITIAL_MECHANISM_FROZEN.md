# Initial independent mechanism (frozen before root comparison)

Frozen UTC: 2026-10-06T04:28:16.028623+00:00 (actual receipt time). This file precedes reading ROOT_PRIOR_THEOREM_COMPARISON.md, check_prior_family.py, ROOT_PRIOR_FINITE_CHECKS.json or any prior-family final reports.

I independently inspected full original Kaibel contribution at printed3014-3015 (PDF46-47), current repaired proof and both checkers/results, and the full-primary Chapoullie-Szigeti PDF's definition, Theorem13, full proof and Figure2 at PDF11-12. Primary hashes are pinned in INPUT_MANIFEST_INITIAL.json.

## Reconstruction

The published exact-cover reduction has one selector u_i per hyperedge H_i, two distinguishable parallel root arcs of opposite colors, black exits to each covered element and gray exits to an overlap-pair sink w_ij. Interpret W using i<j, H_i intersect H_j nonempty. In a monochromatic spanning tree, a chosen black root arc selects the hyperedge. Every element needs a black selector; every overlapping pair needs a gray selector. These are exactly coverage and pairwise disjointness requirements. All root-to-sink paths have two arcs in the printed multigraph.

Replace the two parallel arcs s->u_i by s->b_i->u_i and s->g_i->u_i. Retain both s->b_i and s->g_i, each forced by its head's indegree1. Exactly one b_i->u_i or g_i->u_i is chosen. Other nonroot choices are independent sink parents. This gives a bijection between all original ordinary rooted arborescences and all subdivided ordinary rooted arborescences: selected root-arc identity maps to selected u_i parent, and sink choices agree. The unused intermediate vertex is now a forced leaf and creates no additional restriction.

For an element destination v, charge only s->g_i by1 (globally all i, or only incident i; nonincident entries never occur on its path). For a pair destination w, charge only s->b_i by1. All other entries, including every cost vector for b_i,g_i,u_i, are0. Direct destination-specific path summation gives0 exactly when the selected upstream color agrees with the fixed exit color. A zero-cost tree is exactly an exact cover. The graph is simple and reachable with layers0/1/2/3, consecutive arcs and indegrees1/2/3. It has 1+3h+h+|W| vertices and4h+3h+2|W| arcs, with |W|<=3h in the3-regular family. A dense cost table is polynomial. Add1 to every destination/arc entry: fixed lengths give constant4h+3(h+|W|), and all values are1/2. No unsupported polyhedral equivalence is needed.

## Adversarial caveats already identified

Literal W without i<j allows diagonal conflicts: every selected hyperedge then violates its own sink. This destroys the forward exact-cover implication and cannot be silently copied. Figure2 has only distinct unordered pairs, the count |W|<=3h assumes those pairs, and the converse explicitly uses j<k. Thus a distinct-unordered-pair indexing clarification is compelled and elementary. Duplicate ordered pairs alone preserve the zero equivalence but break the advertised |W| bound and scale positive optima. The reachable-set display excludes s while their claimed intersection equals s; either add s to each displayed set or use empty intersection away from the root. Direct parent choices avoid this display and prove the required implication. These local corrections do not replace the proof's central mechanism.

## Exact-optimum identity challenge

The candidate identity OPT=min_sigma unsatisfied clauses is correct and quantitatively stronger than the zero-equivalence alone. It is not a literal printed theorem of the prior article and does not follow merely from its decision theorem statement. Its mechanism is nevertheless immediate witness accounting: after fixing shared variable parents, each clause selects an independent literal, hence contributes its minimum false-literal indicator. The prior selector/terminal mechanism likewise has an exact optimum counting uncovered elements plus selected overlapping pairs. An objective-preserving SAT encoding could be valuable in another context, but this candidate establishes no distinct approximation threshold, exact algorithm, counting claim, new structural boundary or separately posed unresolved target beyond the contained hardness. I will not upgrade this observation into a claim that every possible strengthening is known or that historical first priority is proved.

## Initial adversarial hypothesis

A bounded already_solved disposition meaning elementary published corollary/no novel resolution established appears defensible, conditional on fresh finite mapping controls and comparison of the independently reconstructed mechanism with root artifacts. Close without merging and without DOI appears proportionate. This is provisional; any mapping, model or source-access failure will keep the gate pending.
