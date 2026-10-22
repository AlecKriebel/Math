# Independent audit of the frequency-to-cross-section reduction

Row 1699 / problem 1900017 / Karpenkov Problem 17. Audited 11 October 2026. This is an authored, AI-assisted mathematical reconstruction, not source-author text and not a novelty claim. The companion finite-measure proof is [MEASURE_AUDIT.md](MEASURE_AUDIT.md).

## Disposition

**Prior preprint theorem claim; the original printed proof is not accepted verbatim as a complete proof audit.** The repaired target argument is verified relative to the explicitly identified established White theorem and standard Haar facts; this is not a complete audit of every assertion in the source. Theorem 1.9 of Aggarwal–Andritsch, arXiv:2608.05853v1, is exactly a finite-sum statement, not merely an abstract or a normalized probability distribution. Its reduction can be reconstructed, but several printed assertions are false literally and need the repairs below. The technical measure audit supplies a reconstructed summable upper bound, with no residual unproved specialized lemma apart from ordinary reliance on the stated published White theorem; its proof is not independently re-proved. There is no conclusion here for dimensions at least four.

The manuscript is a 50-page preprint submitted 6 August 2026. The inspected version-pinned arXiv record lists only v1 and no journal reference. This is manuscript-status evidence, not proof acceptance.

## 1. Exact problem and equivalence convention

Karpenkov's 2017 Problem 17, section 3.4, printed page 10, asks about the sum of geometric relative face frequencies in ambient dimensions at least three. The immediately preceding discussion describes Möbius-invariant measure on arrangements and cites his 2007 paper. The 2017 paper's general Definition 1.1 is an affine integer-congruence definition, so reading that definition alone would leave a genuine convention ambiguity.

The cited paper resolves that ambiguity. Karpenkov, *On invariant Möbius measure and Gauss–Kuzmin face distribution*, arXiv:math/0610042v2, sections 2.2 and 4.2, distinguishes integer-linear and integer-affine face types. Its relative frequency is the measure of continued-fraction arrangements containing a particular integral polytope as a face, and is invariant on integer-linear types. Thus the relevant object retains the origin, not just the affine shape. The v2 document was retrieved and inspected in this audit; its published bibliographic counterpart is Proc. Steklov Inst. Math. 258 (2007), 74–86, DOI 10.1134/S008154380703008X. The retrieved arXiv version is not silently identified byte-for-byte with the journal version.

The 2026 paper uses SL_3(Z)-orbits. The older integer-linear convention permits GL_3(Z). A GL_3(Z)-orbit consists of at most two SL_3(Z)-orbits, and the Möbius measure is invariant under determinant-negative integral maps as well: a reflection normalizes SL_3(R), takes an invariant measure to a scalar multiple, and its square is the identity, forcing that positive scalar to be one. Consequently the two sums differ by factors between one and two, and finiteness is equivalent. This is a bounded change of indexing, not an identity of the classes.

The arrangement space in Karpenkov and the cone space in the preprint also differ. In dimension three each generic arrangement has eight chambers. Forgetting the chosen chamber is an eight-sheeted covering; a fixed nonzero integral face belongs to exactly one chamber when no boundary plane contains a nonzero lattice point. Therefore the two face-event measures agree up to a single normalization constant. This finite covering changes neither finiteness nor the origin-sensitive type.

A face's primitive integral supporting covector n gives n(x)=k>0. An SL_3(Z) change of coordinates takes n to the last coordinate, so a representative lies in z=k. The integer k is the level and is preserved by linear equivalence. Neither an arbitrary lattice translation nor replacement by an affine type with its level is used in the reduction. The affine-type distribution of Theorem 1.4 is a different indexing construction.

## 2. Domain and null exclusions

The preprint restricts to simplicial cones whose boundary hyperplanes contain no nonzero integral points. For each fixed nonzero integer vector and each boundary plane, incidence is a proper algebraic condition in the smooth cone coordinates. The exceptional set is a countable union of measure-zero hypersurfaces. The same assertion holds for the right-Haar P-chart below. Thus deleting rational or partly rational boundary cases changes none of the geometric frequencies at issue.

This is an almost-everywhere statement for geometric measure. It does not establish a pointwise statement for every rational cone or a counting-distribution statement over rational cones. Faces with zero frequency add zero to the sum. A finite face is interpreted throughout as its full finite set of lattice points, equivalently its convex integral polygon, not merely its vertex list; this resolves the paper's shorthand 'convex subset of Z^3'.

## 3. The global chart assertion is false, but the needed local assertion holds

Write G=SL_3(R), Gamma=SL_3(Z), v=(1,1,1)/sqrt(3), and choose the paper's rotation g_v with g_v v=e_3. Let

P_+ = { [[A,b],[0,det(A)^(-1)]] : A in GL_2(R), det(A)>0, b in R^2 }.

For p in P_+, let F(p)=p^(-1)g_v R^3_{>=0}. Every generating ray of F(p) has strictly positive last coordinate, because the last coordinates of the columns of p^(-1)g_v equal det(A)/sqrt(3). The component det(A)<0 gives all negative last coordinates.

Consequently the pushforward from the paper's full P cannot be the globally invariant cone measure, as Lemma 4.2 claims: it assigns zero mass to all cones with mixed signs of generating-ray heights. For example the three columns e_1+e_3, e_2+e_3, and -e_3 generate a nondegenerate such cone; reorder two columns to get positive orientation. Every sufficiently small perturbation still has mixed signs. This is a nonempty open set, hence has positive invariant measure. This also disproves the asserted full-measure coverage by the product used in Lemma 4.2. The objection is independent of rational-boundary exclusions, since generic perturbations satisfy the required irrationality.

There is a second literal issue: the stabilizer of the positive cone inside SL_3(R) is D_+ semidirect A_3, not D_+ semidirect S_3. Odd permutation matrices have determinant -1; inserting a negative diagonal sign would change a ray and fail to preserve the positive cone. Here A_3 is the three-element even permutation group, not a diagonal subgroup. The corrected unordered-cone space is G/(D_+ semidirect A_3).

### Repaired face-adapted chart lemma

Let K_+ be the open set of cones all of whose generating rays have positive last coordinate. The map F:P_+ -> K_+ is a three-sheeted smooth covering. In ordered positively oriented ray coordinates it is a diffeomorphism. Its right-Haar measure pushforward is a fixed positive multiple of the restriction of invariant cone measure to K_+.

**Coverage and uniqueness.** Represent ordered positive-height rays by a determinant-one column matrix g, with heights h_1,h_2,h_3>0. Put t=(h_1 h_2 h_3)^(1/3) and a=diag(t/h_1,t/h_2,t/h_3). Then det(a)=1 and g a has last row (t,t,t). The unique p=g_v(g a)^(-1) belongs to P_+ and represents the given rays. The three positive-orientation orderings account for the covering degree after forgetting order.

**Measure.** Multiplication from D_+ times g_v^(-1)P_+ gives a smooth open product chart in G. Left D_+ and right P_+ actions show that Haar volume there is a constant times left Haar on D_+ times right Haar on P_+. Inversion preserves Haar volume because G is unimodular. Dividing out the diagonal coordinate gives the asserted measure on the ordered ray chart; quotienting by its three deck transformations changes only a constant. No global coverage claim is needed.

**Why this suffices for each face.** Suppose an integral polygon f in z=k>0 is a supporting face of a cone's lattice hull. Since x and 2x are in that hull for any lattice point x of f, the supporting halfspace must be z>=k. If the cone had a ray of negative height, its interior would contain a rational vector of negative height, and rescaling it would give a nonzero integral cone point below the supporting plane, impossible. Thus every ray has nonnegative height. Cones with a zero-height ray form a null set, so almost every cone in the face event lies in K_+. After mapping each face class to z=k by an integral determinant-one transformation, invariant measure uses the same constant for every class. The false global lemma can therefore be replaced by this local lemma in the finite-sum argument.

## 4. Cross-section and level repairs

For a unimodular lattice Lambda, let s be the least positive value of v dot x among nonzero x in the closed positive orthant. The cross-section C consists of lattices whose first slice contains three noncollinear points in the open orthant. This geometric definition is sufficient for what follows.

The printed level formula on page 18 takes an infimum over Lambda minus {0}. It therefore includes nonzero vectors in Lambda intersect v-perp, and its displayed denominator is zero. The intended expression is the least **nonzero height**, equivalently an infimum over Lambda outside v-perp. The product formula lv(Lambda)=s*covol(Lambda intersect v-perp) is valid. The primitive quotient Lambda/(Lambda intersect v-perp) is infinite cyclic. If its positive height is h, unimodularity gives h*covol(Lambda intersect v-perp)=1; hence s/h is a positive integer. This repairs the selection of t_Lambda and the denominator, and explains the level partition without relying on the invalid literal formula.

The proof of the cross-section property invokes Lemma 2.9, which assumes a closed H-orbit, but P Gamma is not closed. Indeed g belongs to P Gamma precisely when the last row of g has rational projective direction. Rational directions are dense, and nonrational directions exist, so P Gamma is dense and proper in G/Gamma. The required closed-orbit hypothesis is not satisfied.

### Direct local repair of the cross-section argument

Fix Lambda in C and a small matrix neighborhood of the identity projecting injectively into lattice space. Old first-slice interior witnesses stay positive under sufficiently small perturbations, so nearby first-contact heights are uniformly bounded above. Points in the positive orthant at such heights lie in a fixed compact tetrahedron. Pulling back by nearby matrices leaves only finitely many original lattice vectors that can witness first contact. By shrinking the neighborhood, any vector that can realize the new minimum must be one of the old first-contact vectors in the CLOSED orthant. The boundary cases are essential: a nonzero old vector on that boundary below s cannot exist, because s is the minimum over the closed orthant; boundary vectors at height s are retained in the contact set; a vector outside the closed orthant, even if another coordinate is zero, has a strictly negative coordinate and stays outside locally. Every other remaining finite candidate has a strict height gap. This argument is for full C, not an assertion that deleting all rational-boundary points leaves an open submanifold.

If a nearby lattice is in C, three of those old vectors become noncollinear co-minima. Their two difference vectors span v-perp already at the old lattice. Equality of the new heights therefore forces the perturbation to preserve v-perp. Conversely a sufficiently small perturbation preserving v-perp leaves the old interior noncollinear witnesses at a common lowest positive height, by the same finite-candidate gap argument. Thus C is locally the single subgroup sheet preserving v-perp, regardless of the dense remote branches of the full P-orbit.

The diagonal Lie algebra is transverse to that sheet: a positive determinant-one diagonal matrix preserving v-perp must have equal diagonal entries and is the identity. This gives actual local flow boxes. Local Haar factorization in these boxes identifies the transverse measure with right-Haar measure on the P-sheet, up to one global scale. No closedness of P Gamma is used.

The equality of the affine lattice generated by all first-face lattice points with the full slice lattice is also repairable elementarily. Choose a nondegenerate triangle of first-face lattice points minimizing positive lattice area. If its edge differences have index greater than one, a point in their fundamental parallelogram, or its reflection through the opposite diagonal, lies in the triangle and produces a smaller nondegenerate lattice triangle. Convexity keeps that new point in the first-face open-orthant region. This contradiction proves a unimodular witness triangle exists. Unlike the printed argument, this does not assume in advance that three points span an arbitrarily generated affine sublattice.

### Explicit identification with the affine-lattice first-contact set

For p=[[A,b],[0,det(A)^(-1)]] in P_+, put Phi(p)=[det(A)A,det(A)b]. Direct block multiplication proves Phi is a group isomorphism to GL_2^+(R) semidirect R^2. Its inverse sends [B,c] to det(B)^(-1/3)[[B,c],[0,1]]. The integral subgroup Gamma intersect P_+ maps exactly to SL_2(Z) semidirect Z^2. Thus the abstract quotient P_+/(Gamma intersect P_+) is the space of planar affine lattices, and the local transverse right-Haar measure is carried to its right-Haar measure with a constant independent of the lattice and level.

For Lambda=g_v^(-1)det(B)^(-1/3)[[B,c],[0,1]]Z^3, every lattice height is an integer multiple of det(B)^(-1/3). Its height-n planar coordinates are BZ^2+n c. Direct multiplication by g_v^(-1) shows that (x,y,n) is in g_v R^3_{>0} precisely when (x,y) belongs to n Delta, where Delta is the open equilateral triangle of area 3sqrt(3)/2 used in the measure audit. Closed orthants correspond to closed triangles. Therefore membership in level k of C is exactly: no point of BZ^2+ell c in ell closure(Delta) for 1<=ell<k, and three noncollinear points of BZ^2+k c in k Delta. This proves the input identification required by the separate measure reconstruction, rather than leaving it as an unverified condition.

## 5. Bounded multiplicity and finite-sum deduction

For a fixed f in z=k, define P_f={p in P_+: f is a face of F(p)} and pi(p)=g_v^(-1)p Gamma. After removing the null rational-boundary set, pi(P_f) is contained in C and its first lattice face is g_v^(-1)p f. Denote its image by C_[f]. This statement uses all lattice points of f. The exceptional-set deletion is required: the printed version of Lemma 4.3 asserts an equality for every point even though its proof only gives the generic statement.

If pi(p_1)=pi(p_2), then p_1=p_2 gamma for gamma in Gamma intersect P_+. Since det(A_gamma)>0 and gamma is integral unimodular block upper triangular, its bottom-right entry is +1 and its upper-left block is in SL_2(Z). Thus gamma preserves z=k. Both f and gamma f are faces of the same sail in the same supporting plane, so gamma f=f. This repairs the printed proof's unjustified claim that every element of P intersect Gamma preserves z=k: the other component sends it to z=-k.

The stabilizer Gamma_f is finite because it permutes the finite vertex set faithfully; a linear map fixing all its vertices fixes three linearly independent vectors. Preserving the affine plane z=k forces block form [[A,b],[0,1]] with A in SL_2(Z). Projection to A is injective on Gamma_f, since a nonzero translation cannot preserve a nonempty finite set.

For completeness, a finite subgroup of SL_2(Z) has size at most six: average an inner product to conjugate it into SO(2), whose finite subgroups are cyclic; the trace of a generator is an integer in [-2,2], so its possible orders are 1,2,3,4,6. The paper omits order three in its list, but the maximum-six bound survives unchanged.

The countable sets C_[f] are pairwise disjoint. A lattice's first face has one and only one Gamma-orbit after a choice of unimodular basis; another choice changes it by Gamma. Borel measurability can be obtained by countably partitioning the face-parameter set into local injectivity charts. Therefore the local quotient integration formula and the preceding bound give

rel([f]) <= 6 B mu_C(C_[f]),

where B>0 is independent of f. B absorbs the normalization of Möbius measure, the ray-order covering convention and the diagonal-flow Haar normalization. The paper fixes no common absolute normalization sufficient to warrant its bare numeric constant 6 for arbitrarily preassigned measures. Finiteness only needs a finite uniform B. One can rescale the Möbius measure so that B=1.

Summing nonnegative quantities over countably many face classes gives

sum_[f] rel([f]) <= 6 B mu_C(C).

Thus the **upper-bound** portion of the paper's cross-section finiteness theorem is enough. Neither its lower level-mass estimate, ergodic genericity theorem, periodic-sail theorem, nor an existing normalized probability distribution proves or is needed for this deduction. If S denotes the finite sum obtained after those dependencies are accepted, the number of classes of frequency greater than t>0 is at most S/t. This is conditional on the finite-measure input, not independent evidence for it.

## 6. Exact acceptance boundary

Checked here: frozen input identities; primary target statement; origin-sensitive equivalence using the cited older primary source; the finite index/covering changes; null rational-boundary removal; explicit counterexample to global chart coverage; repaired face-adapted chart, flow-box and level arguments; stabilizer bound; disjointness and countable-sum reduction with normalization tracked.

Separate measure audit: the chain from the level partition to the summable O((1+log k)/k^2) upper bound, including corrections to printed formulas. Its only specialized imported result is White (1964), Theorem 2, whose primary statement and precise application were checked; its proof is not re-proved. The Haar identification required there is supplied explicitly above. There is no further unproved specialized hypothesis in this reconstruction.

Not claimed: correctness of every assertion of the 50-page preprint; independent proof of every imported published theorem; a journal acceptance or human referee review; formal proof-assistant verification; a new solution; a result in dimension four or higher. The false literal intermediate statements are not counterexamples to the final finiteness claim. The proper literature disposition is a prior preprint theorem claim supported by a repaired target-proof reconstruction relative to an established imported theorem. The imported theorem is ordinary explicit reliance on published mathematics, not an identified unresolved gap. A complete independent audit of the original full manuscript is not claimed.

## Primary public sources

- https://arxiv.org/abs/2608.05853v1 and https://arxiv.org/pdf/2608.05853v1
- https://arxiv.org/abs/1712.01450v1 and https://arxiv.org/pdf/1712.01450v1
- https://arxiv.org/abs/math/0610042v2 and https://arxiv.org/pdf/math/0610042v2
- https://doi.org/10.1134/S008154380703008X (publication metadata)
