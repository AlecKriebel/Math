# PR387 geometry and source audit

Target: exact head `a3034c577445753e00d0b87d358b1fc429e1e9e8`, problem `6200082` / `AMR-061-0082`. Date: 2026-10-03 UTC.

**Scoped verdict: clean.** No substantive defect was found in the original-problem identification, free-group eligibility, full-isometry geometry, or deduction of a uniform Hausdorff dimension gap from the credited uniform Cheeger bound. The proposed **already_solved, 0/5 new author turns, no paper** disposition is appropriate provided the separate detailed audit accepts the repaired approximation application. This source/geometry audit does not claim to independently reprove ABBG Theorem 2.9 or certify every detail of the candidate's all-net repair construction.

## Independence and exact question

I first fetched and visually inspected the original primary PDF, then the published Bowen theorem/corollary pages and their relevant analytic sources. I saved `INDEPENDENT_RECONSTRUCTION.md` before opening the candidate's prior-resolution text or prior review. `RESEARCH_LOG.md` records that order. SOURCE_GATE was initially read only to locate the assigned published source and note the known repair dependency.

Kapovich's *Problems on Boundaries of Groups and Kleinian Groups*, dated 24 October 2007, printed/PDF p21, attributes Problem 82 to Lewis Bowen. Its question is equivalent to:

> For every epsilon > 0, is there a free convex-cocompact G < Isom(real H4) with dim_H Lambda(G) > 3 - epsilon?

The source expressly includes the narrower Schottky case. It imposes no rank restriction, chosen generating set, or orientation-preserving condition. The ambient space is real H4. The target is the **full** limit set with the ordinary round sphere metric; a conclusion confined to classical Schottky groups, fixed rank, or the conical set of an arbitrary geometrically infinite group would not settle the item. Original source: [Kapovich PDF, p21](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf).

## Primary statement and provenance checks

[Published Bowen PDF](https://math.uchicago.edu/~shmuel/L%5E2%20cohomology%20readings/Bowen,%20Cheeger%20constants%20and%20L2-Betti%20numbers.pdf) is a typeset Duke Mathematical Journal 164(3) (2015), 569-615 paper, DOI 10.1215/00127094-2871415. This is confirmed by its first page and [Bowen's author publication list](https://web.ma.utexas.edu/users/lpbowen/research.html), item37. The assigned published PDF, rather than an arXiv version silently substituted for it, was read. The independently retrieved original and published PDFs match the candidate source-manifest byte counts and SHA-256 hashes; so does the independently retrieved ABBG v3 PDF (`SOURCE_BINDING_CHECK.json`). My newly rendered page images are independent renderings, not claimed to match the candidate's image hashes.

Bowen printed p571: Theorem1.2 uses a complete contractible smooth X, a **countable residually finite** class G_d with a condition on **every finitely generated subgroup**, and a separate residually finite geometric cocompact lattice witness with positive degree-d L2-Betti number. His word geometric means the action is free and properly discontinuous (Definition1, p570), not cocompact on all X. Corollary1.3 includes a positive uniform free-group Cheeger bound in every even dimension at least4. Printed p572: Corollary1.4 gives a dimension bound strictly below the boundary dimension for the geometrically finite 3-manifold-subgroup class. The more general 3-manifold machinery is unnecessary to the direct free-G2 verification below.

Bowen Lemma8.1, printed pp601-602, gives the positive middle L2-Betti input. I checked its cited Lueck Theorem5.12(1), printed p228/PDF p241, in the [author monograph PDF](https://math.uchicago.edu/~shmuel/L%5E2%20cohomology%20readings/Lueck_L2-invariants.pdf), and also its simpler hyperbolic specialization Theorem1.62, printed pp53-54. Theorem5.12 is stated for **closed** locally symmetric manifolds; this is sufficient because the application chooses a uniform torsion-free lattice, although Bowen Lemma8.1 is stated more broadly for lattices. No nonuniform extension of that monograph theorem is needed here.

The [ABBG author version v3](https://arxiv.org/pdf/1811.02520v3) explicitly identifies the unfinished Bowen random-net continuity step (pp16-17), explains that its stronger/different Theorem2.9 applies to Bowen's applications, and requires all-radius upper volume bounds and Betti approximation for every allowed ambient-ball weighted net (pp17-18). This is not a blanket formal implication of every version of the original theorem. Its p18 footnote5 additionally diagnoses the normalization issue in Bowen Lemma2.2; ABBG's proof uses its own corrected Lemma2.10. The candidate's theorem-replacement approach bypasses that extra original defect as well.

Bibliographic distinction is correct: arXiv v3 is dated 30 June2021; publication is Duke Mathematical Journal172(4), 633-700, 15 March2023, DOI10.1215/00127094-2022-0029. The [author institution record](https://weizmann.elsevierpure.com/en/publications/convergence-of-normalized-betti-numbers-in-nonpositive-curvature/) and publisher-supplied Crossref metadata confirm these fields. The Academy's [repository record](https://real.mtak.hu/163252/) labels it published2023 but its downloaded PDF is the 2021 v3 author manuscript; it should not be described as a byte-exact published PDF. The packet does distinguish them.

## Independent free-G2 verification and action geometry

Let G be a group in the exact question. Convex cocompactness includes discreteness and yields finite generation: G acts properly and cocompactly on the nonempty proper geodesic convex hull in the non-elementary case. Elementary cases can be treated directly. Discrete subgroups of this second-countable Lie group are countable. The actual group is a finitely generated linear group in O^+(4,1), hence residually finite by Malcev; alternatively free-group residual finiteness is classical. These establish the *ambient* countability/residual-finiteness conditions, rather than merely asserting a Betti limit.

For **each** finitely generated H < G, Nielsen-Schreier makes H finite-rank free. For **each** finite-index normal N normal in H, N is free and has a graph as a K(N,1). Therefore H_2(N;Q)=0 and

    b_2(N) / [H:N] = 0.

The net ordered by reverse inclusion consequently has lower limit zero exactly. This verifies all subgroup and net quantifiers. Neither a special residual tower nor only H=G would be enough on its own. No Lueck approximation is needed for this elementary membership check. The same class G2 works for all ranks, so the lower Cheeger constant is uniform in rank and representation.

A point stabilizer in a discrete hyperbolic isometry group is finite, since it is discrete in a compact stabilizer. Freeness of the abstract group implies torsion-freeness, so all these stabilizers are trivial. The quotient M=H4/G is therefore a complete boundaryless hyperbolic manifold and meets Bowen's geometric convention. Reflections have order2 and are excluded. Orientation-reversing infinite-order isometries are allowed and pose no problem. The spectral statements are for full Isom, and the coarea calculation is orientation independent. Alternatively an orientation subgroup of index at most2 remains free and convex cocompact and has the same limit set, so an orientation-only formulation would recover the dimension conclusion.

The lattice witness is separate from G: compact hyperbolic4 manifolds exist; their fundamental groups are finitely generated linear/residually finite and can be chosen torsion free. The existence plus Malcev input is also explicitly recalled in ABBG p4. Lueck's hyperbolic result yields b_2^(2)(Lambda)>0. In curvature-minus-one normalization its value is 3vol(H4/Lambda)/(4pi^2), from Theorem5.12's compact-dual S4 formula. The numerical value is corroborative, not needed to evaluate any claimed dimension constant. The lattice is not asserted to be free.

## Checkable analytic deduction

The quotient M has **infinite volume**. A finite-volume convex-cocompact hyperbolic quotient has no cusps and is compact. Its torsion-free lattice would be a closed aspherical4-manifold group (cohomological dimension4, using the orientation module if necessary), whereas a nontrivial free group has cohomological dimension1. Equivalently its positive middle L2-Betti number contradicts the free group's graph model. The trivial/cyclic cases also have infinite-volume quotients.

Let h(M) be the infimum area(boundary Omega)/vol(Omega) over smooth relatively compact domains. For f in C_c^infinity(M), coarea applied to f^2 gives

    h(M) int_M f^2 <= int_M |grad(f^2)|
                        <= 2 (int_M f^2)^(1/2) (int_M |grad f|^2)^(1/2).

Thus the compact-support Rayleigh infimum lambda0(M) is at least h(M)^2/4. This proves the relevant noncompact Cheeger implication directly. It should not be generalized to an arbitrary finite-volume complete M using its half-volume Cheeger constant and the spectrum bottom0.

Once the repaired Bowen bound supplies a common h_*>0, put c=min(h_*^2/4,1). Then 0<c<=1 and lambda0(M)>=c. For a non-elementary convex-cocompact group, all limit points are conical and delta equals both critical exponent and round-metric Hausdorff dimension. [Sullivan1987](https://www.math.stonybrook.edu/~dennis/publications/PDF/DS-pub-0082.pdf), Theorems2.17,2.19,2.21 (printed pp333-334; p334 visually checked), gives the piecewise formula. Sullivan uses the **negative** Laplacian convention, so after changing sign to the nonnegative convention used here:

    lambda0 = 9/4                   if delta <= 3/2;
    lambda0 = delta(3-delta)        if delta >= 3/2.

Both expressions coincide at the threshold. On the upper branch,

    delta(3-delta) >= c
    iff (2delta-3)^2 <= 9-4c,

and the nonnegative sign of 2delta-3 yields

    delta <= D := (3 + sqrt(9-4c))/2 < 3.

Since c<=1, D >= (3+sqrt5)/2 > 3/2, so the lower branch obeys the same D automatically. Elementary convex-cocompact groups have finite (or empty) limit sets and dimension0, with the harmless usual empty-set convention. Therefore no sequence in the exact target family has dimension tending to3. Neither h_* nor D is numerically evaluated or claimed optimal.

For the normalized visual metric, if theta is the angle between two rays at o, exp(-(xi|eta)_o)=sin(theta/2). Chordal and angular round sphere metrics are bi-Lipschitz equivalent. Changing o is a smooth Mobius diffeomorphism of the compact sphere and is bi-Lipschitz, preserving dimension. In contrast a snowflake parameter a gives metric d^a and rescales Hausdorff dimension by1/a; an arbitrary parameter must not be inserted into a conclusion whose ceiling is3.

## Candidate comparison and recommended clarifications

The mathematical steps in PRIOR_RESOLUTION.md agree with the independent derivation. Its use of the broad free convex-cocompact clause resolves any classical/nonclassical Schottky terminology ambiguity. Its small-delta branch, c truncation, signs, elementary cases, rank independence and standard visual metric are correct. It keeps the repaired dependency prominent and does not extrapolate to arbitrary geometrically infinite full limit sets.

No mandatory geometry/source correction is required. Two small clarifications would improve the reviewable account:

1. Before Cheeger's inequality, explicitly state infinite volume and explain why a convex-cocompact free H4 group cannot be a lattice. This closes a domain condition currently supplied implicitly by the hypotheses.
2. If expanding the proof-history note, mention ABBG's additional Bowen Lemma2.2 normalization diagnosis and that the replacement proof uses corrected Lemma2.10. The existing narrow statement about the random-net gap is true; it simply does not enumerate every original proof defect.

Classical background not reproved here includes Nielsen-Schreier, Malcev, existence of compact hyperbolic4 manifolds, the geometric finiteness/convex cocompact equivalences, and Sullivan/Lueck's analytic theorems. Their precise roles have been isolated. The repaired uniform-Cheeger theorem is the only central dependency this geometry/source report leaves to the assigned separate detailed repair audit. Mere publication would not replace that audit.
