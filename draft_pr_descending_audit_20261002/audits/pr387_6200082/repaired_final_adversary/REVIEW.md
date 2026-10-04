# Final independent adversarial review of revised PR387

**Verdict: ACCEPT as a credited `already_solved`, zero-author-turn partial PR. No mandatory mathematical or package repair remains at the reviewed head.** This verdict concerns the entire current combined packet, including its mandatory clarification, and does not certify the superseded initial reduction as written. It recommends acceptance; this agent did not merge, change status remotely, or publish anything.

Exact head: `f8a700bf81558761a7341d7f56d1eb8baf943f11`. The 19 reviewed files are individually SHA256-bound in `INPUT_BINDINGS.json` and matched to their actual Git objects. The exact frozen input-manifest SHA256 is recorded there. Review date: 2026-10-03 UTC. Main was independently captured at `9d5b8ad9ec4e84b0f1b1136448c7e12382588ca8`; any later acceptance must use current main without replacing unrelated work.

## Independence, exact question, and source provenance

I independently fetched the original university problem PDF, the published Bowen PDF, ABBG v3 and Buser1982. I read their statements and relevant proofs and saved `INDEPENDENT_RECONSTRUCTION.md` before opening the target exposition or any previous family verdict. Additional original Bowen, Sullivan and Lueck sources were inspected afterward. The source acquisitions and hashes appear in `SOURCE_BINDINGS.json`. Critical original/Buser/ABBG pages were rendered and visually inspected. The prior family reviews were read only after this reconstruction and the current packet inspection; their conclusions were compared with, rather than used to supply, my reconstruction.

The exact university version of Kapovich's collection identifies Problem82 as **Lewis Bowen's** problem, printed p21. It asks about Schottky groups, or the broader free convex-cocompact family in real Isom(H4), without a rank restriction. “Kapovich Problem82” in the README is acceptable shorthand for the collection; SOURCE_GATE gives the precise attribution. The target is the full limit set in the usual round sphere metric. A result only for classical Schottky groups, a fixed rank, or arbitrary groups' conical limit sets would not settle it.

Bowen's actual typeset Duke2015 paper gives the uniform free-family Cheeger conclusion and its dimension consequence, printed pp571–572. Its publication data agree with the author's publication list. The arXiv preprint is distinguished from that published PDF. ABBG v3 is dated June2021 and was later published in Duke2023; the packet does not pretend that the v3 bytes are the published2023 PDF. ABBG explicitly diagnoses the incomplete infinite-superposition continuity step and a separate normalization error in Bowen Lemma2.2. The present application uses ABBG Theorem2.9 and its correctly normalized Lemma2.10, not either faulty assertion.

Mere publication is insufficient evidence here. The remainder of this review verifies the revised reduction, all strengthened hypotheses, the finite-stage theorem mechanism, and the final geometry/spectrum deduction.

## Positive domains, finite components, finite covers, and metric radius

Assume the asserted uniform Cheeger gap failed only in the exact free convex-cocompact target family. Its quotients have infinite volume. A finite-volume convex-cocompact torsion-free quotient has no cusps and would be compact. A closed aspherical4-manifold group has cohomological dimension4, using its orientation module when necessary, while a nontrivial free group has cohomological dimension1. The trivial case also has infinite-volume quotient.

The additive clarification correctly chooses actual smooth relatively compact domains with positive ratios `H_i < h_i+eta_i ->0`. An infimum0 need not be achieved, and Bowen's literal multiplicative approximation at h=0 cannot be used. Buser7.2, printed p229, takes exactly the actual domain ratio H. With Ricci=-3, dimension4, curvature parameter1, and a sufficiently small fixed radius after H_i<1, it provides the stated all-fixed-radius tubular-boundary estimate. Its prefactor includes a fixed radius power, which is legitimately absorbed into C. Its relative volume lower bound ensures the shaved open sets have positive volume. They are contained in a bounded neighborhood of the original relatively compact domain.

For `C_i=N_1(closure T_i)`, properness gives compactness. A boundary point has distance1 from the closed set and a nearest point on its boundary, so the claimed boundary-neighborhood inclusion follows by the triangle inequality. Division by vol(C_i)>=vol(T_i) preserves every fixed-R vanishing ratio. A finite half-unit net of closure(T_i) meets every path component of C_i: paths from a point to its nearest point and then to the nearby net point remain in C_i. Thus there are finitely many components even if T_i itself has infinitely many. No unsupported connected-component selection remains.

A compact set D in H4 surjecting onto C_i exists by finitely many relatively compact evenly covered coordinate neighborhoods. Every conjugacy class with a representative displacing a point above C_i by <=i has a representative g with `gD intersect N_i(D)` nonempty. Proper discontinuity bounds this set of elements finitely. Intersect finite-index normal kernels separating the nonidentity representatives. Normality excludes all their conjugates; subgroup residual finiteness is not being used to exclude infinitely many unrelated elements at once.

Taking the full preimage `K_i=p_i^{-1}(C_i)` in that finite normal cover is essential. It is compact and has at most the covering degree times the number of base path components. A local covering map is open and is a local homeomorphism, so boundaries pull back exactly. Lift a minimizing geodesic to the base boundary to prove the reverse direction of the neighborhood-preimage equality. Projection is length nonincreasing, proving the other direction. Consequently boundaries, all boundary neighborhoods, and domain volumes multiply exactly by the covering degree. A selected component would not justify these equalities; my exact circle-cover control falsifies that substitute.

For every lift q above K_i, nonidentity deck displacement is >i. At radius `R<i/4`, two points x,y in B(q,R) satisfy

    d(x,g y) > i-d(q,x)-d(q,y) > d(q,x)+d(q,y) >= d(x,y).

Therefore no nonidentity translate shortens their distance. The quotient map is metric-isometric on that ball, not merely injective, and its radius supremum is >=i/4. The clarification correctly treats closed endpoint equalities by a strict radius. A cyclic hyperbolic axis of period12 with threshold10 and points -4,+4 falsifies the radius-i/2 metric claim: cover distance8 becomes quotient distance4. Divergence at the safe i/4 radius is all the current proof needs.

The finite-index groups remain free, so the entire quotients E_i have H2=0 over both Q and R. Working directly in the original free groups is valid and bypasses irregular-compact-set fundamental-group-image lifting entirely. The restricted contradiction is sufficient; it is not presented as a reproof of the most general G2 theorem.

## Special extended spaces and every weighted net

Let M_i=N_10(K_i), with ambient restricted distance and Riemannian volume, and use the extended pair `(M_i,E_i)`. M_i is compact, proper and separable, with finitely many path components. Its added volume lies in N_10(boundary K_i), and its boundary R-neighborhood lies in N_(R+10)(boundary K_i). Thus vol(M_i)/vol(K_i)->1 and every required boundary ratio vanishes. Metric covering radii still diverge on this fixed thickening: enclose a lifted ball centered there in a ball of radius larger by10 centered above K_i.

Volumes tend to infinity. For any fixed R, once the boundary ratio is <1, some point of K_i is farther than R from its boundary. Its ambient R-ball lies in K_i. Eventual covering radius makes that ball a hyperbolic R-ball. Since these volumes become arbitrarily large with R, bounded domain volume is impossible.

The parameters `(r0,r1,r2,r3)=(1,2,4,5)` satisfy all strict and weak inequalities in ABBG. Each M_i half-ball contains an embedded hyperbolic quarter-ball, by moving a quarter-unit toward a nearest point of K_i, or using the nearest point if its distance is smaller. Using an eighth-ball instead removes any desired endpoint convention. The lower volume bound is uniform. At every radius, quotient ball volume is at most universal-cover ball volume, giving the single common function `v_max(r)=V_H4(r)` required by ABBG's stronger upper bound.

Volume is nonatomic and Radon. Every ambient sphere has zero volume: upstairs its pieces lie in a countable union of hyperbolic spheres. Because the distance is the restricted ambient distance, the same holds for M_i spheres. Arbitrarily small relative neighborhoods have positive measure: the inward-ball construction works at arbitrarily small scale, not just radius1/2. This verifies full support. ABBG explicitly permits finitely many path components; neither specialness nor its disconnected-complex theorem requires one component.

For any fixed radius R, a random root lies outside the R-boundary strip with probability tending to1. Both the marked subspace and ambient local balls there are exactly hyperbolic once the covering radius is large. These common local balls give the extended metric-measure relations, so the pair BS-converges to `(H4,H4)`, not merely to an unmarked manifold.

Now take **any** permitted [4,5]-weighted(1,4)-net. Its centers are finite by compactness and separation. Its ambient open balls cover M_i. Eventual local metric radius makes the original balls globally strongly convex, with contractible nonempty finite intersections. Their union U is an open neighborhood of M_i; no cut-by-boundary ball is asserted convex.

The good-cover extension is valid. The closed complement F=E_i minus U has positive distance from compact M_i. Exhaust F in compact distance annuli and cover each annulus by finitely many balls centered on F, with radius at most1, less than half the distance from M_i, and below the local strong-convexity radius. This produces a locally finite cover of F in all E_i. Adding the finite original family gives a locally finite good cover of E_i. The full nerve models E_i and has b2=0. Global lower injectivity radius on the complement is unnecessary.

Let A be the original nerve and B the induced subcomplex on added vertices plus original vertices adjacent to an added vertex. Every mixed simplex belongs to B, so full nerve=A union B. Their intersection uses only original centers whose radius-at-most5 balls leave M_i. Such centers lie within5 of boundary M_i. Their disjoint embedded half-balls lie within6 of that boundary, whence

    #interface vertices <= vol(N_6(boundary M_i))/V_H4(1/2).

Adjacent original centers have distance<10. Packing their half-balls in the ambient10.5-ball gives the uniform bound `Delta=ceil(V_H4(10.5)/V_H4(1/2))`. The interface has at most its vertex count times binom(Delta,2) two-simplices. Exactness of

    H2(A intersection B) -> H2(A) directsum H2(B) -> H2(full nerve)

then gives b2(A)<=b2(full nerve)+b2(A intersection B)=o(vol M_i). This remains true even if B's homology is infinite dimensional. All constants are independent of the chosen net and all its weights. More precisely, the normalized absolute error from B_i=1 is bounded by the common boundary ratio times a fixed constant plus1/vol(M_i). This is ABBG's universal all-nets hypothesis, with the positivity requirement met.

## ABBG proof dependencies checked independently

The usable theorem is supported by its finite-stage mechanism. At stage j, the retention decision compares a point to all earlier-marked current-stage Poisson points and retained earlier-stage points. It does not recursively depend on current-stage retention decisions. The dependency radius is bounded by j*r1. In a bounded proper neighborhood only finitely many Poisson points occur, and finite joint inclusion probabilities vary continuously with distances, marks and coins. This strengthens the one-point phrasing in Claim2.16 to the joint-event version actually needed. No infinite-stage continuity passage is used.

The expected completion estimate survives the literal source's packing slips. To make the quantitative check reproducible, write a=vol(R_j)/vol(M)>=epsilon/2 for the uncovered region and take the constants c,c' of Lemma2.11. A first density set R° has

    vol(R°) >= c' a vol(R_j),
    vol(B_r1(x) intersection R_j) >= c epsilon/2 for x in R°.

Its volume fraction is at least c'epsilon²/4. Apply the density lemma again using the safe second threshold `t2=c c'epsilon²/4`. The resulting R°° has volume at least `c'^3 epsilon³ vol(R_j)/8`. A maximal r0-separated subset Z of it therefore has cardinality at least that volume divided by v_max(r0). The probability of exactly one new Poisson point in B_(2r1)(z), lying in B_r1(z) intersection R°, is at least `t2 exp(-v_max(2r1))`. Such a point lies in the uncovered region and is automatically retained.

One retained point may be counted by several successful z, and retained centers' r1-balls need not be disjoint. Both multiplicities are bounded by

    P=ceil(v_max(r1+r0/2)/v_min).

Thus a fixed positive fraction of R_j is removed in expectation whenever its fraction exceeds epsilon/2. This gives the required contraction after correcting the printed source's overly literal second-density threshold and disjointness sentences. For completion, r0-separated centers give disjoint **r0/2**-balls, which remain in the uncovered r1-region; these are the lower-volume balls supplied by the theorem. These are routine constant repairs using exactly the theorem hypotheses, not an unproved replacement of the central continuity step.

Changing finitely many net vertices changes at most a bounded number of simplices per vertex, hence bounds Betti changes by a constant times the added count. Random radii make finite ball-intersection threshold equalities null: along the common diagonal increment of all relevant radii there is a single threshold, so Fubini supplies a null equality set. Ambient-space convergence is present in the extended topology. Equal-volume small disjoint balls convert volume rooting to vertex rooting. The expectation of the counting measure divided by expected vertex count is the correct normalization; an expectation of separately normalized vertex measures is generally different, as the independent mixture control shows. The apparent stray factor in Claim2.21 is avoided by the direct equality `a E|S|/vol(M) = v E|S|/vol(M)+(a-v) E|S|/vol(M)` and uniform packing.

Elek's underlying bounded-degree simplicial convergence input also has a checkable independent mechanism. The k-th combinatorial Laplacian is a positive integer matrix of uniformly bounded norm. Its trace moments per vertex are bounded local functions, so BS convergence gives weak convergence of its spectral measures. The product of its nonzero eigenvalues is a nonzero integer characteristic-polynomial coefficient and is >=1. If its matrix size is <=C times vertex count and its norm is <=L, the fraction of eigenvalues in(0,t) is bounded by `C log(max(L,1))/|log(t)|`. Thus no positive mass can accumulate invisibly at0. Kernel dimension per vertex, equal to b_k per vertex by finite-dimensional Hodge decomposition, converges. Disjoint unions supply the corrected weighted normalization in ABBG Lemma2.10. This checks the role of the cited simplicial theorem without asking publication to serve as proof.

Together these ingredients prove convergence for the finite random almost-net nerves and transfer it, through the uniformly small completion error and all-nets hypothesis, to the prescribed positive B_i. They are precisely what the current application requires from ABBG2.9.

## Compact tower, G2 quantifiers, and spectral conclusion

A separate torsion-free cocompact residual H4 lattice exists; ABBG p4 explicitly recalls compact symmetric-space quotients and Malcev residual finiteness. A nested finite-index normal tower with trivial intersection has diverging local metric radius everywhere. Finitely many short conjugacy classes meet a compact lattice fundamental set, and normality plus trivial intersection eventually eliminates each. Its volumes diverge with index. Every permitted weighted net gives a good cover of the entire compact quotient, so its nerve has exactly b2(Y_j).

Lueck approximation applies to the fixed closed manifold's finite CW model and its normal residual tower. The quoted Lueck5.12 is stated for **closed** locally symmetric manifolds, which is all this argument needs. For H4 the complex ranks of SO(4,1) and SO(4) are both2; the compact dual is S4. Therefore the middle L2 Betti number is positive. In the curvature-minus-one normalization its volume density is3/(4pi²), though no numerical Cheeger/dimension gap is computed.

The tower and M_i sequence share the same lower volume bound, upper bound function, four radii, homology degree and extended BS limit. Interleave them, choosing B_i=1 on the hypothetical domain subsequence and B_j=b2(Y_j)+1 on the tower. The every-net errors vanish on both. ABBG2.9 forces the interleaved B/volume ratios to converge, but the two subsequential limits are0 and a positive middle-Betti density. This is the contradiction producing the uniform Cheeger gap in the exact target family.

Independently, all of Bowen's free-G2 eligibility quantifiers are satisfied: every free group is countable in this discrete Lie-group setting and residually finite; every finitely generated subgroup is free of finite rank; every finite-index normal subgroup of each is free and has a graph classifying space. Ordinary b2 is identically0 throughout the complete reverse-inclusion net. This is stronger than checking one tower or only the ambient group's L2 Betti number. Arbitrary rank and representation are allowed. The current restricted reduction need not establish the general theorem for every nonfree G2 group.

Torsion-free discrete isometry groups have trivial point stabilizers, because those stabilizers are finite discrete subgroups of compact orthogonal groups. Their quotients are complete boundaryless manifolds. Infinite-order orientation-reversing elements are allowed. The coarea inequality is orientation independent; if needed, the orientation subgroup of index<=2 stays free and convex cocompact and has unchanged limit set. Elementary trivial/cyclic cases have finite or empty limit set of dimension0.

For the infinite-volume quotient, coarea of f² for compactly supported smooth f and Cauchy–Schwarz give lambda0>=h²/4 for the nonnegative Laplacian. This domain condition is explicit in the clarification; completeness alone on a finite-volume manifold would not justify a positive spectrum bottom. Convex cocompactness excludes cusps and identifies the full limit set with the conical set. Sullivan2.17/2.21 give, after reversing his Laplacian sign, lambda0=9/4 for delta<=3/2 and lambda0=delta(3-delta) for delta>=3/2. Both agree at the threshold.

With c=min(h_*²/4,1)>0, the upper branch gives

    (2delta-3)² <=9-4c,
    delta <=D=(3+sqrt(9-4c))/2<3.

The low branch satisfies the same D because D>3/2. Round angular/chordal metrics and the normalized visual metric are bi-Lipschitz equivalent. Basepoint changes are smooth Mobius diffeomorphisms of the compact sphere and preserve dimension. Arbitrary snowflakes would rescale dimension and are not used. No result for arbitrary geometrically infinite groups' full limit sets is inferred.

## Whole package, replay, and acceptance scope

All18 problem-folder files plus QUEUE were read. `HISTORICAL_14_PRESERVATION.json` proves the original nine author/source-verification and five review artifacts are byte-exact. README and the current manifest make the additive clarification mandatory and explicitly classify the old pass/pending statements as historical. The old REVIEW.md's connected-domain assertion consequently is not current certification. SOURCE_GATE's pending status and STATE's pending review are historical/proposed metadata, consistent with the stated acceptance gate.

The private standard-library portable replay passes58,717 author assertions,80,000 historical-reviewer assertions and15 wrapper manifest bindings. `INPUT_BINDINGS.json` additionally binds all19 exact-head inputs, including manifests not self-bound by the wrapper. Raw PDFs/images are optional for public replay; fresh primary PDF hashes and new visual source inspection provide current analytic evidence. I did not independently verify the three historical image hashes because those local images were not among the assigned frozen19 inputs. No such verification is needed to establish the exact source statement, which was freshly rendered and inspected.

My independent controls check3,072 five-vertex induced-cover/Mayer–Vietoris cases, including2,304 with zero ambient b2;13,230 exact metric-radius cases;29 full-preimage neighborhood multiplication cases; and23,976 exact spectral identities. Negative controls falsify replacing the H2 interface term by H1, replacing full preimage by a component, replacing metric radius i/4 by injectivity radius i/2, and using incorrect probability normalization. These finite controls support algebra/counterexamples only. They do not compute a Cheeger constant or certify smoothing/convergence/existence by sampling.

The actual three-dot PR diff contains exactly the19 manifest paths. At the captured current main the18 problem paths were absent, and the QUEUE target row was unchanged from merge base. The proposal changes precisely that row's status from queued to already_solved while leaving0/5 and all other cells unchanged. `READONLY_GIT_SCOPE.json` and the two queue diffs record the current-main-preserving prospective change. Main has unrelated newer work; the branch tree must not replace it. A fresh integration/merge check remains an execution responsibility, not an unresolved mathematical issue.

The revised local PR body records the clarification and fresh exact-head gate. Auxiliary `repaired_remote_head.json` contains an older captured body despite the new head; it is an historical capture, not the latest body evidence. This observation does not affect the reviewed19 inputs. The parent should verify current remote head/body and successful current-main integration immediately before acceptance.

Strongest verified result: the complete original free convex-cocompact real-H4 question has the credited negative answer with a uniform rank-independent dimension ceiling below3, using Bowen's prior result with the explicitly audited ABBG repaired dependency and mandatory domain clarification. Remaining mathematical gap: none found. No new author theorem, optimal/numerical gap, paper, preprint, DOI, Zenodo package, release, or external outreach is supported or requested. The accepted finding may be incorporated as the already_solved portion of the larger program with zero new author proof-attempt turns.
