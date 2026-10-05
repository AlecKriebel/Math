# Independent adversarial audit: 5300088 / AMR-052-0088

Audit date: 2026-10-04. Queue rank: 633.

## Decision

**PASS as an unsolved, five-route partial research record.** No proof or counterexample to the full rank-only convex-core ball problem has been supplied, and none is certified here. No substantive defect was found in the retained Schottky construction, the stated necessary conditions, or the cited theorem scopes. Two low-severity clarifications are recorded in `CORRECTIONS.json`; neither changes the mathematical disposition or the non-elementary arguments. The frozen author files were not edited.

The exact reviewed author manifest has SHA-256 `166b1c2642947993cefe9212ba2d523438168a0ce58372731b1a850cc2021945`. The reviewed `PARTIAL.md` has SHA-256 `c3e83dea255fed2940b9c8bc6d4cf9f14d34b77f94851fab3e1047394a5f96cc`. The packet has 12 files and 42,761 bytes. All 11 manifest entries match, with the manifest itself separately bound above. `BOUND_MANIFEST.json` binds all author and audit files by SHA-256 and byte count, except itself.

## Reproduction and independent controls

Run from this directory, or supply any relocated copy of the frozen packet:

    python3 -B independent_verify.py --packet ../submission
    python3 -B -O independent_verify.py --packet ../submission

The verifier uses only the Python standard library. It reads the packet, checks its exact allowlist and both frozen binding hashes, runs the author's verifier normally and with optimization, and compares each output byte-for-byte with the frozen `CONTROL_RESULTS.json`. The author's 7,801 checks pass in both modes. Its manifest replay also passes.

The independent suite passes **55,357 checks** in both modes with byte-identical output. It uses direct scalar coordinate transformations and explicit inverses rather than importing or calling the author's matrix routines. It checks Lorentz Gram products, determinant +1, time orientation, side-pairing coefficient identities, the cap slab, convex combinations generating the interior octahedron, all eight facet normals, and the logarithmic depth identity. It evaluates **13,600 word/parameter pairs**: all 4,372 nonempty reduced words through length seven at each of q=3, q=7/2, and q=13, plus all 484 through length five at q=101. It checks each word's hyperboloid identity, inverse action, first-letter ping-pong cap, and displacement lower bound. Mutation controls reject removing the screw rotation from the claimed hull construction, identifying depth with injectivity, and substituting rank for genus in the wrong direction.

These counts include integrity/replay checks and finite exact controls. They do not turn finitely many words or parameter samples into an infinite proof. The following mathematical audit supplies the separate conventional reasoning.

## Exact target and source hypotheses

The original question concerns an upper bound on every embedded ball wholly inside the convex core, with the bound depending only on the number of generators. It is not an existence statement for large balls. The source also mentions quasifuchsian and two-dimensional special cases. This was checked from the primary PDF and a fresh local rendering of printed page 12. [Bielefeld, Section 5](https://arxiv.org/pdf/math/9201271#page=12)

The literature distinctions survive independent inspection:

- White's convention is the global minimum injectivity radius, and Theorem 4.4 treats closed manifolds. It does not control an arbitrary center. [White](https://arxiv.org/pdf/math/0104191)
- Bachman–Cooper–White's unconditional Theorem 1.1 gives cosh(r) <= 2g for closed, connected, orientable manifolds of sectional curvature at most -1. The separately stated stronger conditional inequality is not used. [Bachman–Cooper–White](https://arxiv.org/pdf/math/0305290#page=2)
- Fan's rank-dependent pointwise result assumes homotopy equivalence to a book of I-bundles. Her subsequent remark describes why pointwise injectivity is too strong in general. The packet appropriately credits that mechanism. [Fan, Corollary 5.1 and Remark 5.2](https://arxiv.org/pdf/math/9907058#page=19)
- Bowditch's final theorem depends on compact-core topology and includes the eventual cusp and degenerate-end cases. Its triangulation parameter does not become a rank parameter automatically. [Bowditch, Theorems 0.1 and 1.1](https://ems.press/content/serial-article-files/29640)
- Biringer–Souto's Corollary 14.9 assumes a positive global injectivity lower bound as well as bounded rank; conventions include orientability and completeness. Both statement and proof were inspected in v2, including fresh local renderings of printed pages 6 and 220. A lower bound just on the candidate ball is insufficient. [Biringer–Souto v2](https://arxiv.org/pdf/1708.01774v2#page=6)

The June 2024 author narrative poses the rank-to-genus and closed-ball questions and states the implication between them. Current author lists were checked; one lists the thick-case work in Memoirs of the AMS (2026), while the other still says to appear. This does not establish identical final-publication pagination. A dated search found no verified full thin-case resolution, but absence from that search is not a theorem. [Research narrative](https://ianbiringer.net/researchstatement.pdf), [Biringer list](https://ianbiringer.net/), [Souto list](https://juan.perlora.eu/_subsites/research.html)

All seven stored primary PDFs with claimed byte counts and hashes match their source-manifest entries. `SOURCE_CHECKS.json` records the inspection scopes and metadata without including PDF bytes, screenshots, or extracted source text.

## Mathematical attack on the radius/depth formula

For a nonempty convex core and x in it, the largest permitted centered radius is min(inj(x), d_C(x)). Below injectivity radius, the covering ball is embedded; below core depth, it remains in the core. Conversely any such embedded ball gives both inequalities. Taking suprema makes tangency immaterial. The term “isometric embedding” has the conventional Riemannian embedded-ball meaning used in the cited papers. It need not preserve ambient pairwise distances between all image points near the ball boundary.

The only degenerate-case convention omitted in the display is the empty-core case: declare r_C=0 and use supremum zero for an empty family in the nonnegative extended half-line. Otherwise the ordinary extended-real convention gives sup(empty)=-infinity. No positive-radius claim is affected.

The orientation-cover reduction is valid for nonorientable examples: the index-two subgroup has rank at most 2n-1, finite index preserves the limit set, and an embedded simply connected ball lifts into the cover's core. Elementary cases are already harmless.

## Infinite-word and quotient audit

Write f(u)=(s+cu)/(c+su). Direct algebra gives

    c-st=1, s-ct=t, c-s=q^(-2)>0,
    f(u)-t=(u+t)/(c+su).

Thus the positive side pairing is valid on the full interval [-1,1], with positive denominator, rather than merely at tested points. The inverse pairing follows by signs. Since q>=3 implies t>=4/5, we have 2t^2>1, so the four closed caps are pairwise separated even on the ideal boundary.

Starting with a point of D and applying a reduced word from right to left, the current image is always in the cap of the current first letter. A new letter cannot be the inverse of that letter. Disjointness puts the current cap outside the new letter's excluded inverse cap, so its image enters the new cap strictly. This proves wD is disjoint from D for every nonempty reduced word. Applying the same result to h^(-1)g proves disjointness of all distinct translates.

Consequences do not require a finite-word extrapolation or an unproved claim that D tiles all of H^3:

1. No nonempty reduced word represents the identity, so the representation is faithful and the generated group is abstractly free of rank two.
2. Since D contains a neighborhood of o and every nonidentity group element moves o outside D, the identity is isolated in the group topology. The group is discrete.
3. A free group is torsion-free. A discrete torsion-free subgroup of the orientation-preserving isometry group acts freely and properly discontinuously; the quotient is a complete orientable hyperbolic manifold.
4. The open L-ball lies in D and its translates are disjoint. Hence every nonidentity displacement of o is at least 2L, not merely L. The explicit generator displacement is exactly 2L. Therefore inj(p)=L.

The halfspace location of wo alone would only give the weaker L displacement. The disjoint translated L-balls supply the necessary factor of two; the packet's embedding argument is valid for this reason.

## Full-dimensional hull and depth audit

The entire orbit of o except o lies in the four closed halfspaces. Every ideal accumulation point therefore lies in their four ideal caps. Each cap obeys |u_3|<=sech L; the closed Euclidean convex hull obeys the same slab inequality. Klein convexity identifies its intersection with the open unit ball with the hyperbolic hull.

The four ideal fixed points +/-e_1, +/-e_2 are in the limit set. Invariance places A(+/-e_2)=(s/c,0,+/-1/c) there as well. Taking weight c/(c+s) on either of those points and the remaining weight on -e_1 gives exactly +/-q^(-2)e_3. These are interior points of the ambient Klein ball, genuinely in the hyperbolic hull. The use of ideal vertices +/-e_1 and +/-e_2 to describe a closed Euclidean hull causes no difficulty.

The resulting octahedron is described by

    |u_1| + |u_2| + q^2 |u_3| <= 1.

Its eight facet planes have normal norm sqrt(q^4+2), hence it contains the Euclidean ball of radius 1/sqrt(q^4+2). Radial Klein distance is atanh of Euclidean radius. This proves positive core depth and three-dimensional interior at p, so the example is not merely Fuchsian.

For the upper bound, points on the third axis with Klein coordinate just larger than sech L are outside the invariant hull. Their distances tend down to atanh(sech L). Because the full preimage of C(N) is precisely this invariant hull, distance from p to the complement equals distance from o to the lifted complement. In particular quotient identifications cannot invalidate either depth inequality.

Finally,

    atanh(sech L) = log((q+1)/(q-1)) -> 0,
    inj(p) = log q -> infinity.

This rejects a rank-only bound on pointwise injectivity even for an interior point of a full-dimensional core. It supplies no upper or lower divergence statement about r_C over all centers. The author explicitly preserves that distinction.

## The other retained reductions

The essential-loop conjugation proof of the 1-Lipschitz injectivity bound is valid. Cyclic covers of a fixed closed hyperbolic genus-g surface bundle admit 2g+1 generators, have linearly growing volume, and therefore cannot have bounded diameter. Straightening a t-tetrahedron fundamental cycle gives volume at most t*v_3, so their triangulation complexities diverge too. None of this forces embedded radii to diverge.

The boundary Euler identity uses a connected compact orientable core with nonempty boundary and no spherical components, as stated. Its estimate on negative Euler characteristic cannot create a sweepout. The warning about torus components refers to what that displayed Euler estimate itself records; it should not be interpreted as a claim that no other rank-based topological constraint on tori exists.

The rank<=Heegaard-genus inequality runs the wrong way for the proposed substitution. A rank-only genus bound would suffice for the closed case, but is not furnished here.

For a hypothetical bounded-rank sequence with r_j -> infinity, failure of global injectivity infima to tend to zero would give a uniformly thick subsequence, contradicting Corollary 14.9. The Lipschitz estimate puts every epsilon-thin point at distance greater than r_j-epsilon from x_j; the infimum yields the stated weak inequality. The sequence has locally hyperbolic-space neighborhoods. If “isometric neighborhoods” is read with ambient restricted distances rather than the Riemannian convention, take r_j>2s instead of merely r_j>s; the same eventual conclusion follows. None of these necessary conditions constructs a counterexample or contradicts pointed convergence to H^3.

## Clarifications and final limits

`CORRECTIONS.json` gives two optional low-severity wording improvements: the empty-core supremum convention, and replacing the final phrase about controlling both terms by an explicit bound on their minimum. The latter avoids suggesting separately bounded injectivity, which the example disproves.

This is an independent AI-assisted mathematical and reproducibility audit, not human peer review or proof-assistant certification. The source inspection checks identities and hypotheses used by the packet, not every argument inside every cited paper. The dated literature search is non-exhaustive. The accepted status is **unsolved, 5/5**. No remote writes, source redistribution, or modifications to the author packet were performed.
