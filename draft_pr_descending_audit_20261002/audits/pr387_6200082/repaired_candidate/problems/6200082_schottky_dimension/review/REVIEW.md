# Independent review: credited prior resolution of Problem 82

PASS. Proposed disposition already_solved, zero new author turns. The negative answer is credited to Lewis Bowen's published 2015 theorem, with the later Abért–Bergeron–Biringer–Gelander approximation repair explicitly retained. This is a verification of that prior-result chain, not a new discovery or a complete reproof of every classical analytic dependency.

Frozen author packet manifest SHA-256: 5c448076b5c26a9aa790eb5cd06720f1597193e89ebc693b160e9b1f6019d466. WIP: 7bd98e077a854ada800178bbf3ead4f9932d7ca2. Read SOURCE_GATE.md, PRIOR_RESOLUTION.md and the entire CORRECTED_APPLICATION.md. No mandatory correction is required.

## Exact source and result

Visually inspected original printed page 21. Problem 82 asks whether Schottky, or more generally free convex-cocompact, subgroups of Isom(H4) can have limit-set Hausdorff dimension arbitrarily close to three. There is no fixed-rank restriction. Visually checked Bowen's published printed page 572 and read Theorem 1.2 and Corollary 1.3 on page 571. They give the required uniform Cheeger gap and the dimension corollary. The full versus conical limit-set distinction is harmless precisely because convex cocompactness excludes cusps and all limit points are conical. No statement for arbitrary geometrically infinite free groups is inferred.

The free group acts freely: a discrete point stabilizer is finite, and the group is torsion-free. Thus the quotient meets the geometric-action convention. Every finitely generated subgroup and each finite-index subgroup is free, with zero ordinary second Betti number, so it satisfies Bowen's G_2 hypothesis. A residual compact H4 lattice supplies positive middle L2-Betti number. This checks the free-group case directly rather than silently importing a stronger three-manifold-subgroup classification.

Cheeger's inequality has the right sign and normalization, lambda_0>=h^2/4. With c=min(h_*^2/4,1), the spectral branch delta>=3/2 gives delta(3-delta)>=c and hence delta<=(3+sqrt(9-4c))/2<3. The small-delta branch and elementary groups automatically satisfy that upper bound. No numerical value or optimality of the gap is asserted. The metric is the usual round/visual sphere metric, not an arbitrarily snowflaked visual parameter.

## Known proof gap and the corrected theorem

Read ABBG arXiv:1811.02520v3, Section 2.3, including its diagnosis of the random-net continuity problem and Theorem 2.9's complete hypotheses. The authors explicitly say the replacement applies to Bowen's applications, while noting it does not formally imply every version of the original statement. The packet correctly retains this qualification and distinguishes the June 2021 manuscript from the 2023 publication.

The repair requires all-radius upper volume bounds and approximation of the Betti numbers of the ambient-ball nerve for EVERY permitted weighted net. Those strengthened hypotheses cannot be replaced by one convenient discretization. The packet's application checks them as follows.

Bowen's Lemmas 7.2 and 7.3 were read in the preprint, including the residual-cover construction, boundary ratios for every fixed radius and diverging covering radius along the compact sets. These supply connected compact Følner domains in free quotients if the asserted gap failed. The free-group second homology vanishes for these quotients. These particular lemmas are credited dependencies; the faulty approximation theorem is not used to infer their conclusions.

Thickening by ten preserves negligible fixed-radius boundary neighborhoods and asymptotic volume. Covering radius on each fixed thickening diverges as well, by the displacement triangle inequality. The volumes must diverge: otherwise interior hyperbolic balls of each fixed radius, obtained outside the negligible boundary region, would have unbounded required volume in a bounded-volume set.

The inward-ball argument gives a uniform positive lower half-ball volume even at the thickened boundary, while every ambient quotient ball has volume bounded above by the H4 ball for that radius. The parameters 1,2,4,5 meet the exact r_3>r_2>=2r_1>2r_0 restrictions. Ambient restricted metrics and volumes are non-atomic, fully supported, have null spheres and are compact/path connected as required. Away from a negligible boundary portion the pointed extended pair agrees on each fixed radius with (H4,H4). This establishes the stated extended BS-convergence, not just convergence of unmarked manifolds.

## The all-net nerve estimate

For every allowed separated weighted net, use ambient balls of radii between four and five. The diverging local covering radius makes these balls and their relevant finite intersections strongly convex. They cover M_i and give its ambient open neighborhood U_i. Crucially, the argument never assumes that cutting a ball by a possibly reentrant boundary preserves convexity.

The finite original collection can be extended to a locally finite good cover of E_i by sufficiently small convex balls outside M_i. Since U_i is an open neighborhood of compact M_i, a locally finite complementary refinement can be chosen away from a smaller neighborhood. The full nerve models E_i and therefore has zero second Betti number. The subcomplex containing added vertices and all original vertices meeting them covers every mixed simplex. Its intersection with the original nerve has only original centers within distance five of the boundary. Separation, embedded half-balls and the fixed-radius boundary estimate bound the number of these centers by o(vol M_i). Uniform degree follows from hyperbolic packing at radius ten. Thus the intersection's number of two-simplices is o(vol M_i), uniformly over every net and weights.

Mayer–Vietoris gives b_2(original nerve)<=b_2(full nerve)+b_2(intersection), and hence the required uniform negligible ratio. The intersection estimate does not require the complementary cover to have a global injectivity-radius bound. Local small convex balls suffice there; all original balls lie in the diverging-injectivity neighborhood. Taking B_i=1 meets the positivity hypothesis and has negligible normalized error.

## Interleaving and conclusion

A nested residual normal tower of a fixed compact torsion-free H4 lattice has diverging injectivity radius and the same extended BS-limit. Its weighted nets have nerves homotopy equivalent to the whole compact quotient. Lück approximation and the positive middle L2-Betti number give a positive limiting normalized b_2. Taking B_j=b_2+1 again meets positivity with a vanishing normalized extra term.

Interleaving the two sequences preserves the common constants, all-radius bounds, convergence and every-net approximation. ABBG Theorem 2.9 forces convergence of the resulting B/volume sequence, contradicting its zero and positive subsequential limits. This validates the replacement theorem in the precise free-H4 application. The known continuity gap is not ignored or treated as repaired merely by changing a citation.

## Verification and publication

All 58,717 author controls reproduce byte-for-byte. The complete eight manifest entries and seven local source bindings (four PDFs and three images) verify. Separate exact rational controls pass 80,000 assertions checking the spectral quadratic equivalence and monotonicity. These computations do not prove existence or evaluate the Cheeger constant; the analytic conclusion rests on the audited theorem chain and hypotheses.

Approve publication as already_solved, zero new author turns, with Bowen and ABBG credit and the proof-history note prominent. Preserve all nine frozen author files and the review whitelist. Only the target queue status/turn cells should change. No raw source redistribution, novelty claim, merge or release is authorized by this review.
