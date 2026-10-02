# Turn 2: generic global finite recovery and uniqueness in the unrestricted dual family

AI-assisted proof candidate, independent review pending. Original source unresolved, second author turn. The hypotheses concern a general degree-delta dual hypersurface, not the dual of a general smooth primal surface. No real visibility or noisy-data assertion is made.

## 1. Statement

Fix distinct planes H1,H2 in P3_C and their intersection L. For a general homogeneous polynomial Phi of degree delta>=7, set Gamma_i=V(Phi) intersect H_i. An admissible compatibility triple consists of lines l_i in H_i and a projectivity h:l1 -> l2 such that h identifies the effective intersection divisors Gamma1 intersect l1 and Gamma2 intersect l2, including multiplicities. The restrictions must be nonzero. These are the epipole/pencil-projectivity data of a rank-two fundamental matrix, as in Turn1.

**Theorem.** For delta=7 there are only finitely many admissible compatibility triples. For every delta>=8 there is exactly one: l1=l2=L and h the identity under the true identification. In both cases the conclusion holds on a nonempty Zariski-open set of degree-delta equations. That open set can be chosen so the dual surface and both section curves are smooth and their common divisor on L is squarefree.

Thus a single pair of full dual section curves generically determines epipolar geometry uniquely in the unrestricted dual-degree family when delta>=8; at delta7 it determines finitely many candidates. The theorem does not identify the number of candidates at delta7. It does not apply without proof to the much smaller family of duals of smooth fixed-degree primal surfaces.

## 2. Restriction to two lines

Let V be the vector space of all degree-delta forms in four variables, of dimension N=binomial(delta+3,3).

If l1 and l2 are skew, the restriction map V -> H0(l1,O(delta)) direct-sum H0(l2,O(delta)) is surjective. In coordinates where the lines are the two coordinate pairs, any prescribed binary forms extend by their sum. The target dimension is 2delta+2.

If l1 and l2 are distinct and meet at p, the image is exactly the subspace of pairs with matching values at p under the ambient O(delta) fiber identification. It has dimension 2delta+1. In coordinates with the lines parameterized by (s,t) and (s,u), prescribed forms A(s,t),B(s,u) with common coefficient c of s^delta extend as A+B-c s^delta. This also proves surjectivity onto that fiber-product subspace.

Fix h and a nonzero scalar lambda, after locally choosing lifts/trivializations so compatibility is r1=lambda h* r2. For skew lines these are delta+1 independent linear conditions on Phi.

For intersecting lines they are again delta+1 independent conditions unless h maps the intersection point to itself and lambda matches the induced evaluation fiber scaling. In that exceptional case they impose exactly delta independent conditions. Here is a precise linear proof: the target restrictions (A,B) obey one linear relation epsilon1(A)-epsilon2(B)=0. On the graph A=lambda h*B this relation is the functional lambda epsilon1(h*B)-epsilon2(B). It is identically zero exactly in the stated exceptional case; otherwise it is a nonzero functional. Evaluations at two distinct points of a line are independent for delta>=1. The kernel dimensions, and hence ranks of the compatibility map on the restriction image, follow immediately. This argument includes restrictions vanishing at p; no division by their values is used.

## 3. Off-diagonal incidence dimensions

The space of line pairs (l1 in H1,l2 in H2) has dimension4. Skew pairs form an open subset. Adding h contributes3 dimensions and lambda contributes1. Over each such parameter the equations have rank delta+1. Hence the skew compatibility incidence in V times these parameters has dimension

N+4+3+1-(delta+1)=N+7-delta.

Distinct intersecting line pairs have dimension at most3: choose p on L (one parameter), then one line through p in each plane (one each). Cases with one line equal to L are contained in this locus and have smaller dimension. On its nonexceptional h,lambda stratum the incidence dimension is at most

N+3+3+1-(delta+1)=N+6-delta.

In the exceptional stratum h must map the specified point to the specified point, cutting PGL2 dimension from3 to2. The matching lambda is then unique, and rank falls only to delta. Its incidence dimension is at most

N+3+2-delta=N+5-delta.

All counts may be made on finitely many algebraic coordinate charts for the line bundles and projectivity parameters. The compatibility equations are linear in Phi, with the ranks just proved, so these are actual vector-bundle dimension bounds, not an assumption that equations are independent. The nonzero-restriction condition only removes points and cannot increase dimension.

For delta>=8 every off-diagonal incidence stratum has dimension less than N. Its projection is contained in a proper closed subset of V (take the closure of its constructible image). A general Phi therefore has no off-diagonal compatible triple. For delta=7 the skew incidence has dimension at most N and the intersecting incidences less than N. For each of the finitely many irreducible incidence components which dominates V, the generic fiber has dimension at most0 by the fiber-dimension theorem; nondominating components can be avoided. Shrinking to a nonempty open subset of V, all off-diagonal fibers have dimension at most0. A zero-dimensional finite-type complex algebraic set is finite. The scalar lambda is unique for any nonzero compatible pair, so forgetting it does not alter that finiteness.

## 4. The diagonal case

The only line contained in both H1 and H2 is L. If l1=l2 then both equal L. Compatibility is exactly a projective automorphism of the degree-delta divisor D=V(Phi|L).

For squarefree D with at least three points, its projective automorphism group is finite: it injects into permutations of the points, since a projectivity fixing three distinct points is the identity. For a general squarefree D of degree delta>=7 the group is trivial. One elementary proof works on ordered configurations of delta distinct points. For each nonidentity permutation sigma, the condition that a projectivity realizes sigma is algebraic on this open configuration space, by taking the unique projectivity determined by any chosen three points and their images. It is a proper condition: choose three domain indices I, and choose j outside I union sigma(I), possible because delta>=7. Vary the j-th point while the other points stay fixed; the determined projectivity does not change. If sigma(j)!=j, its required image is fixed, which cannot hold for all j-th points. If sigma(j)=j, fixing all the varying j-th points forces the projectivity to be the identity, which cannot realize a nonidentity permutation on a distinct configuration. Thus no nonidentity sigma is realized identically. The finite union of their proper closed loci is proper. Passing to unordered configurations gives the claim.

The restriction map V -> H0(L,O(delta)) is surjective. Therefore the general Phi has squarefree D with trivial projective stabilizer. Its diagonal compatibility triple is uniquely the true one. Combining this with Section3 proves the theorem.

## 5. Geometry, credit and limitations

The good conditions above are nonempty opens in the irreducible vector space V. Smoothness of V(Phi) and of both fixed plane sections is also a nonempty open condition, as the Fermat equation demonstrates. Their intersection remains nonempty. Projective coordinate changes allow a general pair of distinct camera planes.

Contour duality and projective biduality identify the section curves with the full dual apparent contours of X=V(Phi)^vee in the admissible conormal sense. This X can be singular; a smooth dual hypersurface of degree delta is not asserted to be the dual of a smooth primal hypersurface of any prescribed degree. The source's real visible boundary question also has further visibility/occlusion issues. These gaps are retained in the final disposition. A unique compatible triple in this algebraic family is a statement about epipolar geometry, not unique reconstruction of the surface itself.

The correspondence formulation, the seven-dimensional parameter count, and the use of generalized Kruppa equations are credited to the imported report and classical primary literature. The finite-recovery theorem for two projections of the same spatial curve in Kaminski and collaborators is not used as a silhouette theorem. The new work in this turn is the explicit union-of-two-lines restriction and incidence argument in the stated family; no novelty certification is claimed.

The checker independently verifies restriction-map ranks in intersecting and skew coordinate models, including special scaling, maps moving the common point, and sections vanishing there. These finite controls supplement the exact all-degree linear proof and do not establish genericity by numerical testing.
