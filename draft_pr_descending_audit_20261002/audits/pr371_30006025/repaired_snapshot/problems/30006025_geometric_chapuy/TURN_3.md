# Turn 3: the regular-polygon lift exists, but has the wrong short-geodesic law

Problem 30006025. Third substantive author turn. **The original geometric question remains unresolved.** Relaxing exact edge-length preservation gives a classical positive construction from cubic one-face maps to closed hyperbolic surfaces. We show that this particular replacement cannot reproduce the source's Weil–Petersson short-geodesic limit, regardless of how the input maps are sampled.

The polygon/dessin construction and the CFF correspondence are established background, not new bijections. For an explicit modern account of the uniform-dessin construction, see Girondo–González-Diez–Hidalgo, https://arxiv.org/abs/2306.09543 , Section 2 and Lemma 1. The new deduction recorded here combines that construction with a credited triangle-group systole formula and the credited Mirzakhani–Petri limit. No historical novelty is claimed.

## 1. A genuine smooth hyperbolic replacement

Take any rooted trivalent one-face orientable map M of genus g>=2. It has E=6g−3 edges, V=4g−2 vertices, and N=2E=12g−6 positions in its cyclic face word. Let P_N be the regular hyperbolic N-gon of curvature minus one with all interior angles 2pi/3. It exists since N>6, and its side length is

    ell_N=2 arcosh(2 cos(pi/N)/sqrt(3)).                   (1)

Glue the sides by the orientation-compatible pairing prescribed by M, using the unique endpoint-matching edge isometries. The quotient is a compact orientable topological genus-g surface. Across edges the metric is smooth. Every vertex cycle contains three polygon corners, whose angle sum is 2pi, so there is no cone singularity there either. Hence the quotient S(M) is a smooth closed curvature-minus-one surface.

Its area is exactly

    (N−2)pi−N(2pi/3)=4pi(g−1),                           (2)

as required by Gauss–Bonnet. The embedded rooted graph and its rotation system are retained as markings. With those markings the combinatorial map is recoverable; forgetting them may identify several different inputs as the same unmarked hyperbolic surface.

This construction replaces all sampled graph lengths by ell_N and changes the perimeter to N ell_N. It is not a length-preserving lift of the Dirichlet metric map of perimeter 12g. Nor is the regular-polygon construction asserted to be a new surface model.

## 2. How the tree sampling enters, and the exact output law

One may first use any fixed signed CFF bijection. Its graph-preserving statement gives 2^(E+1) copies of each rooted E-edge genus-g map in correspondence with signed C-decorated trees. Restricting to cubic underlying graphs retains that same multiplicity. Thus uniform sampling from that finite restricted decorated-tree set yields a uniform rooted cubic one-face map after the copy label is forgotten. This is a consequence of the credited bijection, not a claim that a naive independent cyclic order at merged vertices is its inverse.

Applying Section 1 gives a well-defined finite-support law on marked hyperbolic surfaces. The unmarked law is its pushforward, weighted by the number of marked inputs mapping to each unmarked surface. It need not be uniform on unmarked isometry classes. More importantly, all the conclusions below apply to **any** probability distribution on the input maps, not only this CFF-derived uniform law.

For fixed g, such a finite-support law is singular with respect to Weil–Petersson volume. That observation alone would not exclude a useful asymptotic approximation as g grows. The persistent geometric obstruction in Section 4 is stronger and is the relevant reason this replacement fails the source's short-curve comparison.

## 3. Every output covers the same triangle orbifold

Subdivide each original edge by its midpoint. The resulting clean uniform dessin has N edges: white vertices have degree two, black vertices degree three, and its unique face has degree N in the dessin convention. Its Fuchsian representation is an index-N, torsion-free subgroup

    Gamma_M < Delta(2,3,N),                              (3)

where Delta is the orientation-preserving triangle group.

This can be seen directly from the geometry. Divide P_N into 2N congruent right triangles with angles pi/2, pi/3 and pi/N. The side pairings preserve their tiling. The local angle sums at original vertices, edge midpoints and the face center are all 2pi, so the surface subgroup is torsion-free. Its quotient is exactly the smooth surface of Section 1. Equivalently, the dart permutations are a fixed-point-free involution alpha, a product sigma of 3-cycles, and a single N-cycle sigma alpha. They define the triangle-group permutation representation. Uniform cycle lengths give the torsion-free stabilizer, as in the cited uniform-dessin lemma.

The area of the triangle orbifold is

    2pi(1−1/2−1/3−1/N)=pi/3−2pi/N.

Dividing (2) by this area gives index N, agreeing with the dart count. The group need not be normal and the dessin need not be regular in the group-theoretic sense. “Regular polygon” does not mean a regular covering or a regular map.

## 4. A uniform lower bound for every closed geodesic

Emmanuel Philippe, *Les groupes de triangles (2,p,q) sont déterminés par leur spectre des longueurs*, Ann. Inst. Fourier58(7)(2008),2659–2693, Corollary 5.2, gives for the orientation-preserving triangle group

    systole(Delta(2,3,N))
       =2 arcosh(2 cos²(pi/N)−1/2),       N>=7.           (4)

Primary source: https://doi.org/10.5802/aif.2424 , direct PDF https://aif.centre-mersenne.org/item/10.5802/aif.2424.pdf . The group conventions and the exact p=3 formula on printed 2686 were checked visually. This classification theorem is used as an established external result, not reproved by finite word enumeration.

Every nontrivial deck transformation of the closed surface S(M) is hyperbolic and belongs to Delta(2,3,N). Therefore

    sys(S(M)) >= 2 arcosh(2 cos²(pi/N)−1/2).              (5)

Only this lower bound is asserted: a subgroup need not contain an element attaining the parent group's systole.

For all N>=18 the right-hand side is strictly greater than one. Indeed

    2 cos²(pi/N)−1/2 > 2 cos²(pi/12)−1/2
                     = (1+sqrt(3))/2 >4/3.

Also cosh(1/2)<4/3. An entirely rational bound is

    cosh(1/2) <= 1+(1/8)/(1−1/48)=53/47<4/3,

obtained by bounding the positive Taylor-series tail by a geometric series. Thus (5) is strictly greater than one, uniformly in g and in M. In fact the parent-group bound increases to 2 arcosh(3/2), but the simpler constant one suffices.

## 5. Persistent disagreement with the source's Weil–Petersson statistic

Let Z_g count primitive closed geodesics with lengths in [1/2,1]. For every surface produced by the regular-polygon replacement,

    Z_g=0 deterministically.                              (6)

For a Weil–Petersson random closed genus-g surface, Mirzakhani–Petri's theorem gives

    Z_g => Poisson(mu),
    mu=integral_(1/2)^1 (cosh t−1)/t dt >0.                (7)

We use the displayed density (exp(t)+exp(−t)−2)/(2t) in their Theorem 4.1, which is exactly the density in the OWR source and in the later metric-map paper. The nearby numerical or small-epsilon approximations in source copies are not needed here. Primary author PDF: https://webusers.imj-prg.fr/~bram.petri/RandSurf.pdf ; https://arxiv.org/abs/1710.09727 . The precise probability measure and displayed theorem were read and visually checked.

Consequently the total variation distance between the **one-dimensional count laws** in (6) and (7) tends to

    1−exp(−mu) > 3/19.                                   (8)

For the explicit strict lower bound, cosh t−1>t²/2 for t>0 gives mu>3/16, and exp(x)>1+x gives 1−exp(−3/16)>3/19. This is an exact bound; no numerical approximation is required.

Thus no choice of input-map distribution can make this particular regular-polygon model have the source's limiting short-geodesic count law. The failure persists after any deterministic rescaling bounded away from zero, with a suitably chosen fixed short interval. No claim about arbitrary Gromov–Hausdorff couplings or other geometric constructions is inferred solely from this statistic.

## 6. Remaining opportunity and scope

The construction is a legitimate geometric realization of the combinatorial objects, but it discards the metric-map lengths and lives in a uniformly thick family of triangle-orbifold covers. Reweighting the finite set of input trees cannot introduce geodesics excluded from every output. A successful source-compatible construction must change more than that sampling weight or this fixed regular-polygon geometry.

This is not a negative answer to Louf's unrestricted question. Deforming polygon geometry, introducing genuinely variable lengths and angles, or using another geometric correspondence remains possible. The next turn will study an angle-independent geometric constraint on preserving the source's perimeter, rather than keeping the triangle-group hypothesis.

The checker validates the combinatorial area/index identities, the clean-dessin cycle data for exact examples, and rational inequalities supporting the uniform gap. It does not replace Philippe's theorem or Mirzakhani–Petri's limit by finite computations.

Author turns completed: 3/5. Original question unresolved. Subjective completion estimate: 12%.
