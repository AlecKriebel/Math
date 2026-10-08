# Even-sided complementary regions: five scoped approaches

Problem 10300037 / AMR-102-0037, rank 1006. Author status: **unresolved in this packet, 5/5 mathematical approaches**. This is an AI-assisted, unrefereed mathematical analysis. It claims neither a new solution nor novelty for its partial results. The announced Delman–Roberts universal alternating-knot result is credited; absence of an inspected complete manuscript is not evidence that their result is false or that the problem is still open in the literature.

## 0. Target, conventions, and scope

The target is Delman's Question 9.4 in Calegari's 2002 problem list [C02, p.22]. In our own words: for every alternating knot in the three-sphere other than a torus knot, obtain an essential lamination with the specified even-sided polygon-bundle complementary geometry around the surgery locus, allowing the monkey-saddle construction at every nonmeridional surgery. The geometric requirement is retained; knowing that a closed filling has some taut foliation does not alone identify the requested complementary region or a common persistent lamination.

Let X(K)=S^3 minus the interior of a tubular neighborhood of K. On its oriented boundary choose a meridian-longitude basis (mu,lambda), with intersection mu.lambda=1. A rational slope is the unoriented primitive class ±(p mu+q lambda). Nontrivial surgery here means q != 0, including p=0. The meridional filling has q=0. We do not confuse 'boundary slope' in this question with the narrower finite set of slopes of compact incompressible surfaces.

The source's polygon bundle has a two-dimensional ideal polygon as fiber over S^1. It is not an I-bundle over a three-dimensional mapping torus. An ideal polygon is viewed topologically as a disk with finitely many ideal vertices removed from its boundary. In the local two-sided case we also allow the ideal digon, homeomorphic to a strip with two boundary lines; this is a product-type limiting case rather than a genuine polygon-gut region with at least three sides.

Calegari's essentiality condition excludes sphere leaves and compressible solid-torus-bounding torus leaves, and requires irreducible complementary regions with incompressible boundary and no compressing monogons [C02, Definitions 1.3–1.5]. His filling procedure is for cooriented very-full laminations. Our local analytic constructions below are explicitly in the cooriented setting. They do not establish the global essentiality conditions. Nor do we assert an essential lamination of the meridionally filled S^3 itself; essentiality belongs to the knot-exterior/surgery setting, and the meridian is excluded.

A compact branched-surface complement with annular cusps is distinguished throughout from the complete complement of a carried lamination. Passing between them requires control of the interstitial strips. In particular, the noncompact extension hypothesis in [DR-DD, Definition 4.8 and Proposition 4.10] must not be discarded.

## 1. Approach one: repair parity by a cover, and test descent

### Proposition 1 (alternating sign and monodromy test)

Let an oriented polygon have n >= 2 sides numbered cyclically. Prescribe a sign epsilon_j in {+1,-1} on side j, requiring adjacent signs to differ. Such a prescription exists exactly when n is even, and then there are precisely two prescriptions. If a polygon-bundle monodromy induces the cyclic shift j -> j+s, the prescription descends to the bundle exactly when s is even.

Proof. From epsilon_(j+1)=-epsilon_j one obtains epsilon_j=(-1)^j epsilon_0. Closure requires (-1)^n=1. When this holds the two choices of epsilon_0 give all possibilities. The descended condition is epsilon_(j+s)=epsilon_j, which is equivalent to (-1)^s=1. This proves both assertions for all n and s. These signs model the alternating asymptotic directions of cooriented saddle leaves, not arbitrary branch weights. QED.

An orientation-preserving disk homeomorphism permuting the marked boundary sides necessarily induces a cyclic shift, since it preserves their circular order. Thus the proposition covers its action on the marking even if the homeomorphism itself is not a rigid rotation.

The attempted repair is to pass to a finite cover in the base-circle direction. The d-fold cover has side permutation j -> j+d s. For even n, an odd s becomes even in the double cover. But the deck transformation of that double cover still induces the original odd shift and interchanges the only two sign prescriptions. Therefore neither prescription descends as a cooriented alternating prescription. For odd n, a cover only in the base direction does not even change the odd number of sides.

Concrete obstruction: n=6, s=3 has even fibers, yet its monodromy interchanges signs. Its two-fold base cover has trivial side permutation and admits alternating signs, but the deck involution exchanges those signs. This is a counterexample to the proposed parity-only descent argument, not a counterexample involving an alternating knot.

Remaining gap after this route: one must change the global lamination/cusp structure, or establish an appropriate invariant coorientation from the start. An unverified cover and descent does not produce the required knot-exterior lamination.

## 2. Approach two: use surgery arithmetic to create even polygon fibers

### Proposition 2 (cusped solid-torus calculation)

Consider a solid torus V with m >= 1 disjoint parallel essential annular sutures on its boundary, all of primitive slope a u+b v, where u is a meridian of V, v a longitude, b != 0 and gcd(a,b)=1. After making the slope linear, a meridian disk meets their cores in

N = m |b|

points. In the resulting marked-disk bundle, the cyclic permutation of these points on one trip around the core is the shift s = m a modulo N, up to reversing the circular orientation. The number of cycles is m, each of length |b|.

Proof. Normalize the longitude coordinate t modulo 1 and angular meridian coordinate theta modulo 1. A curve of class (a,b) is described by b theta-a t=c modulo 1. Take the m parallel curves at c=j/m, 0 <= j < m. At fixed t the equations have precisely m|b| solutions. On increasing t by one the angular set is rotated by a/b, which is the shift m a of the N circularly ordered points if b>0; when b<0 the direction is reversed. Its cycle count is gcd(m|b|,m a)=m, and each cycle length is |b|. Linearization of disjoint parallel essential curves on a torus is an ambient isotopy and does not alter this marked-bundle calculation. Thickening the points gives the annular sutures. QED.

If the intervals between successive marked points are assigned alternating signs, the monodromy condition is the same as for the marked points. Combining Propositions 1 and 2 gives an exact criterion:

**The linear cusped model admits a monodromy-invariant alternating side prescription if and only if m is even.**

Indeed, m even makes both N and s even. If m is odd and |b| odd, N is odd. If m is odd and |b| even, coprimality forces a odd and hence s odd. This eliminates the apparent loophole in which a surgery denominator merely makes the total side count even.

For a knot filling along r=p mu+q lambda, choose l=c mu+d lambda such that p d-q c=1. In the filling basis (r,l),

mu = d r-q l.

Thus a=d and b=-q. If a complementary collar has 2k meridional sutures before filling, its filled solid-torus local model has

N=2k|q|,   s=2k d modulo N.

The choice of l changes d by a multiple of q and hence changes s by a multiple of N, so the permutation is independent of this longitude choice. Every nonmeridional rational filling therefore has the required local parity. For |q|=1 and k=1 this is a digon/product case; do not claim genuine polygon guts there. For q=0, the intersection count collapses and this proof supplies no filling model, exactly as required by the exclusion of the meridian.

Remaining gap: the calculation assumes the meridional-cusped complementary collar. It neither constructs that collar for an arbitrary alternating knot nor verifies essentiality or interstitial extension. Surgery arithmetic cannot repair an odd number of cusp annuli while retaining this linear cooriented model.

## 3. Approach three: write the local saddle foliation explicitly

### Proposition 3 (analytic even-rotation local filling)

Let n >= 4 be even. Let P be the interior of a regular convex n-gon in R^2, with positive affine side distances L_j(x), normalized equivariantly under its rotations. Remove the vertices when adjoining the open sides. For an even cyclic shift s let R be the corresponding rotation and form the mapping torus of R. On P put

h(x)=sum_(j=0)^(n-1) (-1)^j log L_j(x).

On P x R_t, the one-form omega=dt-dh defines a nonsingular cooriented foliation invariant under (x,t)->(R x,t+1). Every interior leaf in the quotient is a disk; its asymptotic behavior at successive open side interiors alternates. The foliation extends smoothly over each open side as a tangent boundary foliation. The central circle meets every interior leaf transversely.

Proof. Each L_j is positive in P, so h is smooth. Rotation permutes the distances by an even shift, hence h(Rx)=h(x). Consequently omega is invariant and descends. The coefficient of dt is one, so omega never vanishes, and d omega=0 proves integrability. On the cover, the leaves are the graphs t=h(x)+C. The deck transformation takes graph C to graph C+1 and identifies no two points of a fixed graph. Each quotient leaf is therefore a copy of P, hence a disk.

Approaching an interior point of side j, all other L_i remain bounded away from zero and h=(-1)^j log L_j+H, where H is smooth there. Thus h tends to opposite infinite ends on successive sides. Multiplying omega by the positive function L_j in the interior gives

alpha_j=L_j dt-(-1)^j dL_j-L_j dH.

This extends smoothly to the open side and is nonzero there; its kernel is tangent to that side. Since alpha_j wedge d alpha_j vanishes on the dense interior, it vanishes on the side too. This verifies a genuine smooth side extension, not merely divergence of graph heights. No claim is made about adding ideal vertices as ordinary corners; they were deleted. Finally R fixes the center and h has a constant value there, so the central t-circle is transverse and meets every value of C modulo one. QED.

The n=2 case has a direct strip model: P=R_x x (-1,1)_y and h=log(1+y)-log(1-y). Its two side ends have opposite divergence and the same graph argument applies. We use identity side monodromy in this product/digon case.

For a four-sided explicit check, take P=(-1,1)^2 and

h=log(1-x^2)-log(1-y^2).

Writing A=1-x^2 and B=1-y^2, a polynomially rescaled defining form is

alpha=A B dt+2x B dx-2y A dy.

It is nonzero in the interior and along open edges. Its Frobenius expression alpha wedge d alpha vanishes identically; the finite diagnostic checks the corresponding exact polynomial identity as an implementation control. The general proposition follows from the proof above, not from that check.

This route supplies the local monkey-saddle/stacked-chair behavior for the even-rotation model. It does **not** show that an arbitrary lamination complement is conjugate to that model with the required boundary marking, nor that independently specified holonomy on boundary leaves matches it. In a filled closed manifold, the central circle meets the new interior leaves; tautness of the old boundary/lamination leaves still needs the global transverse-curve and gluing hypotheses. We do not infer global tautness from local interior transversals.

Remaining gap: produce the right global lamination and the actual compatible ideal-region compactification. The analytic filling itself does not force the global construction.

## 4. Approach four: build a global candidate from a sutured decomposition

Here we use credited geometric existence theorems rather than infer existence from a sign pattern. The following is a conditional, proved construction route, with every extra hypothesis retained.

For clarity, the substantive double-diamond conditions are these. After cutting along R, the traces of S on the two copies of R must have minimal intersection after projecting back to R, and decomposing along S must remain taut; these are the tightness conditions. The surface S is not a product disk (a disk meeting the annular sutures in just two arcs). Along one component of its boundary, two consecutive arcs on the copies of R, separated by a transition arc on the boundary torus, must project to properly isotopic arcs in R. The region between them incident to that transition must be a source sector in the smoothed R-union-S branched surface, so its cusp directions point outward. This is the content used from Definition 5.8, expressed in our notation. The distinguished meridian is formed by the transition arc together with the corresponding boundary arc of R in that region. Thus the source-sector and tightness requirements contain geometric information beyond evenness.

### Proposition 4 (double-diamond sufficient subclass)

Let K be a knot in S^3. Suppose its exterior admits a taut sutured decomposition beginning with a connected minimal Seifert surface R, followed by a surface S satisfying the double-diamond-taut conditions of [DR-DD, Definition 5.8]. Suppose also that the associated Gabai branched surface has no sink disk disjoint from the exterior boundary. Then the Delman–Roberts replacement construction gives a cooriented taut branched surface carrying a lamination, with a boundary collar having two annular cusps at a distinguished slope nu, satisfying the noncompact extension condition. The distinguished slope is the actual knot meridian. Every nonmeridional slope is strongly realized by a cooriented taut foliation. In each rational filling the collar's marked-disk local model has 2|q| sides and even side monodromy as in Proposition 2.

Proof and dependency ledger. The replacement theorem [DR-DD, Theorem 5.10] supplies the cooriented taut branched surface and the collar with exactly two annuli of slope nu. The no-sink-disk hypothesis is needed in Corollary 5.11: its proof checks laminarity and obtains a fully carried lamination by Li's laminar-branched-surface theorem. The same proof verifies the noncompact extension needed for Proposition 4.10; merely counting the two annuli would not replace it. Proposition 4.10 then extends the lamination to taut foliations for every slope except nu.

To identify nu, suppose nu differs from mu. Then the meridional slope mu would be among the strongly realized slopes. Capping its circular leaves with meridional disks in the filling torus yields a cooriented taut foliation of S^3. This contradicts the classical no-taut-foliation consequence of Novikov's theorem, also used in [DR-C, Remark 1.3]. Hence nu=mu. The surgery-basis calculation of Proposition 2 now applies with k=1. This deduction preserves the exceptional meridian; it does not incorrectly include it. QED, with the cited existence theorems as dependencies.

The hypotheses are nonvacuous. [DR-DD, Corollary 6.3] verifies them when a minimal Seifert surface is a plumbing with an unknotted annular band carrying 2m half twists, m >= 2, as specified there. The mirror version follows by reflecting the entire construction and reversing the appropriate slope signs. We claim the cited subclass and the conditional theorem, without claiming that every alternating knot has such a plumbing.

Why the route stops: an arbitrary alternating diagram has not here been converted into a taut hierarchy meeting the double-diamond and no-sink conditions. A disk carrying a useful sign pattern is not by itself a taut decomposing surface, and a taut branched surface is not automatically known to carry a lamination. We cannot delete either requirement. The announced full alternating-knot construction uses more general spine decompositions; its existence is credited but a complete argument has not been recovered in the inspected materials.

## 5. Approach five: pass through connected sums and track what survives

### Proposition 5 (credited annular gluing, and its exact limitation)

If a finite rational slope r is strongly realized by a cooriented taut foliation of X(K_1), then it is strongly realized for K_1#K_2 for any knot K_2. Consequently a persistently foliar summand makes the connected sum persistently foliar. This is the Delman–Roberts gluing proposition [DR-C, Proposition 4.1 and Corollary 4.2]; the argument below records why it preserves the slope but does not preserve a prescribed complementary polygon.

Take a longitude-realizing taut foliation on X(K_2), whose existence is the credited Gabai input used in [DR-C]. Cut the sum exterior along its meridional summing annulus A. The boundary linear foliations are transverse to the meridian, since r is finite; after a boundary isotopy their restrictions to A are matching interval foliations. Choose compatible coorientations and identify the two collars along A. They therefore glue without a singularity.

For the slope calculation, cut each boundary torus into the summing annulus and its complementary annulus. In a lift with meridional coordinate theta, the return along the longitude direction of the first torus has displacement r; that of the second, longitude-foliated torus has displacement zero. The new longitude concatenates the two complementary annuli, so its displacement is r+0=r. Equivalently, following q longitudinal circuits accumulates p meridional turns for r=p/q, giving the same primitive boundary slope after reduction.

For tautness, first accommodate either standard convention for a manifold with transverse boundary. If an old leaf meets a closed transversal in the interior of a summand, that transversal survives the gluing. If it is certified instead by a properly embedded transverse arc, close the arc by a positively transverse path on the same boundary torus. Such a path exists between any two boundary points: in the universal cover, add sufficiently many positively transverse meridional turns to the endpoint displacement for the linear boundary foliation. Smooth the two joins and push the boundary segment slightly into a product collar. After a small perturbation this gives an interior closed transversal through the same leaf, also surviving the gluing. Finally, every glued leaf contains a piece of an old leaf. This proves tautness for all glued leaves, including ones whose old pieces did not themselves meet the boundary. A leaf that does meet the boundary also retains an outer-boundary intersection, since its nonmeridional boundary curves traverse the complementary annulus. Compatible coorientations are used throughout. The irrational statement, when needed for the definition of persistent foliarness, is the corresponding linear-foliation version of the same credited proposition. No irrational Dehn filling is asserted.

The attempted extension to Question 9.4 fails at a specific logical step: the two glued foliations can use different minimal sets and can have leaves crossing A. This argument specifies neither a common essential sublamination nor the topology of its component surrounding the surgery core. Therefore it proves persistence of foliations, not closure of the exact even-sided-complement property under arbitrary connected sum.

There is a stronger verified geometric subclass: connected sums of two nontrivial fibered knots. For summands with the same veering direction, [DR-C, Sections 6.1–6.6, especially Propositions 6.4, 6.8 and 6.10] constructs a branched surface whose boundary component is a torus collar with two meridional annuli and whose other components are products, then checks laminar splitting and foliation extension. Section 6 explicitly works first with right-veering summands, with the left-veering case obtained by reflection. For the remaining monodromies, the paragraph after Corollary 7.2 continues the summand-by-summand construction: each summand retains its Type C meridional cusp; an opposite-sign transition uses a Type A smoothing at the other end, and the remaining sutures still agree with the Gabai product-disk complement. Together with the end-effective splitting of Theorem 5.12, this retains the two-cusp collar and product-complement route, rather than merely invoking a theorem about foliarness. Separately, Theorem 7.3 gives an explicit two-meridional-annulus collar and product complement whenever its tight opposite-sign arc hypothesis holds; we do not remove that hypothesis or infer it solely from a statement about slopes. The distinguished meridian is the actual knot meridian by [DR-C, Corollary 3.3]. The cusp calculation of Proposition 2 consequently gives the same 2|q| local side count. This is credited known work, not a new proof for prime alternating knots or all composites.

Remaining gap: this route leaves the prime non-torus alternating case and the complementary-region compatibility in general sums. A theorem about the existence of foliations after summing cannot silently be upgraded to the fixed geometric construction in the original question.

## 6. Sharp stopping point

The local parity, slope, monodromy, and analytic filling steps are understood in the explicitly stated models. The global construction is proved for the quoted double-diamond and fibered-connected-sum subclasses. For a general non-torus alternating knot, this packet supplies neither a universal global branched surface with the required carried lamination/interstitial geometry nor a counterexample.

The exact unresolved task **for this packet** is to give, for each such knot, a globally essential carried lamination together with its torus-parallel even-meridional-cusp region and noncompact extension data (or another verified construction of the source's ideal polygon-bundle region), prove the compatible side monodromy/coorientation and the global filling properties, and check all nonmeridional slopes. There are public announcements closely matching this goal. A complete proof may already exist; our inability to inspect it is recorded as a source-verification limit rather than a theorem of nonexistence or a current-openness claim.

## References

- [C02] D. Calegari, Problems in foliations and laminations of 3-manifolds (2002), Question 9.4 and Definitions 1.3–1.5. https://arxiv.org/abs/math/0209081
- [DR-DD] C. Delman and R. Roberts, Taut foliations from double-diamond replacements, inspected arXiv 1907.01899v2; published in Contemporary Mathematics 760 (2020), 123–142. Numbering here follows the inspected preprint. https://arxiv.org/abs/1907.01899v2
- [DR-C] C. Delman and R. Roberts, Persistently foliar composite knots, inspected arXiv 1905.04838v3; Algebraic & Geometric Topology 21 (2021), 2761–2798. https://arxiv.org/abs/1905.04838v3 and https://doi.org/10.2140/agt.2021.21.2761
- [D19] C. Delman, Persistently Foliar Knots, Georgia Topology Conference, May 25, 2019, especially slides 12 and 18. https://www.ux1.eiu.edu/~cidelman/Research/Presentations/persistentlyfoliarknots2019.pdf
- [C-notes] D. Calegari, foliation course/book notes, inspected file with PDF creation metadata January 20, 2024, p.46. https://math.uchicago.edu/~dannyc/courses/foliations_2016/foliations_notes.pdf
- [BNS25] J. Baldwin, Y. Ni and S. Sivek, Floer homology and right-veering monodromy, J. reine angew. Math. 818 (2025), 263–290, p.266 and reference 9. https://www.its.caltech.edu/~yini/Published/FloerRV.pdf
- [S26] D. Santoro, Taut foliations from knot diagrams, inspected arXiv 2402.01225v2 (June 19, 2026), especially Theorems 2.17 and 4.1; Adv. Math. 492 (2026), 110906. https://arxiv.org/abs/2402.01225v2
