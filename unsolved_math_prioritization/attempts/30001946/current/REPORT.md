# Geometric isolation in rational Witt bordism: a bounded partial investigation

Problem 30001946 / OWR-11454-004. 9 October 2026.

## Disposition

**The full methodological question remains unresolved in this investigation.** Five materially distinct construction routes have been examined. This report gives an explicit sufficient geometric criterion, its proof and product-neighborhood consequences, and an explicit counterexample to two tempting universal intermediate claims. None is presented as a new theorem of the literature, and none is a counterexample to Friedman's question. The accompanying independent audit accepts the corrected scoped statements below; the original general target remains unresolved.

The strongest positive statement below is a construction for a restricted class. The strongest negative statement is that removing a neighborhood of the entire genuine singular locus and simply coning the resulting manifold boundary can change the Witt signature. In the example, the lost middle class cannot even be represented in the regular locus.

## 1. Exact target and conventions

Given any compact closed oriented PL stratified pseudomanifold X of dimension n satisfying the rational Witt condition, construct a compact oriented PL rational Witt space W of dimension n+1 with collared boundary X disjoint union -Y, where Y has only finitely many genuine singular points. Spaces need not be connected or normal. There are no codimension-one singular strata. Orientations are orientations of regular strata, with the usual boundary convention. In the cap constructions the orientations of M and N are retained, and each cone is oriented to cancel the induced orientation of its attaching boundary.

Here the Witt condition is the vanishing of lower-middle intersection homology in the middle degree of every even-dimensional link of an odd-codimensional singular stratum. Write IH for lower-middle intersection homology with Q coefficients, and cL for a closed cone when used in compact constructions. The boundary is not treated as an interior singular stratum.

This is Question 1 on printed pp.3279–3280 of [F11]. The source already knows existence from Siegel's computation and generators. Merely invoking that classification, or choosing a model with the same Witt class and invoking injectivity, does not answer the requested constructive question. The distinct characteristic-two Question 2 is outside this investigation.

An adequate full solution would specify all local changes, prove that every new odd-codimensional link satisfies the Witt condition, preserve boundary collars and orientation, and prove finite termination at an isolated-singularity output. No claim of universal openness or priority is made.

## 2. Route 1: global coning and its exact range

If n is odd, cX is an explicit Witt nullbordism. Away from its vertex, its strata are products of strata of X with an interval and have the same links. Its vertex has codimension n+1, which is even, so introduces no Witt vanishing condition. Its boundary X has the evident radial collar.

If n=2m>0, the only additional condition for the same construction is IH_m(X)=0: the vertex has odd codimension 2m+1 and link X. This condition is both necessary and sufficient for cX with the conical stratification to be Witt. For example c(CP^2) fails, because H_2(CP^2;Q)=Q. This is a failure of that recipe, even though CP^2 already satisfies the target conclusion.

A nullbordism can be converted into a bordism to an ordinary sphere by deleting a small open PL ball in its regular part. Thus no convention about the empty output is needed. Dimensions 0 and 2 already have at worst isolated singularities under the no-codimension-one convention, and the identity cylinder suffices. The coning argument is standard; see [S83, IV.1] and [B08].

**Remaining gap:** a general even-dimensional middle intersection group does not vanish. This route cannot erase it by coning alone.

## 3. Route 2: why the most direct neighborhood collapse fails

Suppose X=M union_E N, where M is a compact oriented manifold with boundary E, N is a closed neighborhood of the singular locus, and E is a bicollared hypersurface in the regular stratum. If n is even, the space

Y = M union_E cE

is a Witt space with one possible isolated singularity. The new link E has odd dimension. However, X and this particular Y need not be Witt bordant.

### 3.1 An example with a genuine positive-dimensional singular locus

Take the underlying complex weighted projective space

X = P(1,1,2,2,2),

not its orbifold stack. It is the quotient of C^5 minus the origin by

lambda·(u_0,u_1,v_0,v_1,v_2) = (lambda u_0,lambda u_1,lambda^2 v_0,lambda^2 v_1,lambda^2 v_2).

Its real dimension is 8. It is compact and oriented, and the usual algebraic stratification admits a compatible PL triangulation. Its singular set is

Sigma = {u_0=u_1=0} = P(2,2,2) = CP^2.

Where u_0 or u_1 is nonzero the quotient is a smooth complex vector-bundle chart. Near any point of Sigma, choose a nonzero v-coordinate and normalize it to 1. The remaining residual group is {+1,-1}; it acts as -1 on (u_0,u_1) and trivially on the two tangent coordinates along Sigma. Consequently the local model is

C^2 × (C^2/{+1,-1}) = R^4 × c(RP^3).

The normal link RP^3 is not an integral homology sphere, so these are genuine nonmanifold points, not artificial lower strata. It is a rational homology 3-sphere. Thus X is a rational homology manifold, IH_*(X;Q)=H_*(X;Q), and X is Q-Witt. Equivalently its only singular stratum has codimension 4, which is even. The weighted quotient and local quotient descriptions agree with [BFNR, §§1,3].

### 3.2 Its middle pairing is positive

The coordinate power map

q: CP^4 → X,  [z_0:z_1:z_2:z_3:z_4] ↦ [z_0:z_1:z_2^2:z_3^2:z_4^2]

identifies X with CP^4 modulo the finite group of independent sign changes in the last three coordinates. This group has order 8, acts effectively, and preserves complex orientation. It acts trivially on rational cohomology. The finite-quotient cochain argument gives

q*: H^*(X;Q) ≅ H^*(CP^4;Q).

For completeness, one may take an equivariant triangulation and barycentrically subdivide until simplex stabilizers fix simplices pointwise. Cochains on the quotient then identify with invariant cochains; averaging over the finite group is exact over Q. This proves the asserted cohomology isomorphism without assuming a free action.

Choose a in H^4(X;Q) with q*a=h^2, where h is the positive generator of H^2(CP^4;Q). Since q has degree 8,

8 <a cup a,[X]> = <h^4,[CP^4]> = 1.

The one-dimensional middle pairing is therefore positive, and sigma_IH(X)=1. An independent arithmetic cross-check is Kawasaki's ring formula as restated in [BFNR, Theorem2.1]: for these weights (l_0,...,l_4)=(1,2,4,8,8), so the integral degree-four generator squares to 2 times the positive top generator. The rational pairing can be written as <2> or, after rational rescaling, <1/8>.

### 3.3 Its regular complement has no middle homology

On X minus Sigma there is a projection

[u_0:u_1:v_0:v_1:v_2] ↦ [u_0:u_1] in CP^1.

In the charts u_i≠0, divide v_j by u_i^2. The transition on the three v-coordinates is the square of the base transition, so this is the total space of a complex rank-three vector bundle over CP^1. The convention for calling its line summands O(2) or O(-2) is immaterial here. In particular X minus Sigma deformation retracts to CP^1.

Choose a compact disk-bundle core M in this complement. Its exterior N, including Sigma, is a conical neighborhood of Sigma; their common boundary E is the sphere bundle of the rank-three complex bundle. This decomposition can be made PL compatible with the above stratification. Thus

H_4(M;Q)=H_4(CP^1;Q)=0.

The standard cone/Mayer–Vietoris calculation for the isolated cap Y=M union_E cE gives

IH_4(Y;Q) = image(H_4(M;Q) → H_4(M,E;Q)) = 0.

Hence sigma_IH(Y)=0. Witt signature is a bordism invariant [S83, II.2], so **there is no Q-Witt bordism from X to this Y**.

This does not obstruct a different isolated-singularity output with the correct pairing. It refutes only the universal claim that the uncorrected cap of the regular complement always works.

One can also see the exact missing class: N retracts to CP^2 and is a rational homology manifold, so IH_4(N)=Q. Since E is an S^5-bundle over CP^1, its rational Serre sequence has entries only in total degrees 0,2,5,7. Thus H_4(E)=0. The map H_4(E)→IH_4(N) is not surjective; its cokernel has dimension 1.

## 4. Route 3: exchanging the cone factors

For a product neighborhood N=B×cL with B,L positive-dimensional closed oriented manifolds, a natural local trace is cB×cL. Its two boundary pieces are B×cL and cB×L, glued along B×L. Product boundary collars can be rounded in the PL category. If both cones are Witt, their product is Witt, and this trace exchanges the two factors geometrically.

The extra condition is serious. If dim(B) is even, cB is Witt only when H_dim(B)/2(B;Q)=0. The original Witt condition constrains L, not B. For B=CP^2 it gives no such vanishing. Even when the trace is permitted, the new singular locus from the first cone vertex has dimension dim(L), which need not be less than dim(B). Finally, a general link bundle is not a product, so the block need not glue with its transition functions.

**Remaining gap:** a universally valid, bundle-compatible, strictly complexity-decreasing replacement. Neither the missing cone condition nor the monotonicity follows from Wittness. This route was stopped rather than counted as a general induction.

## 5. Route 4: a precise positive criterion and an actual bordism

The failed neighborhood argument has a useful exact repair under an explicit hypothesis.

### Proposition (surjective boundary criterion)

Let X=M union_E N be a compact closed oriented PL Q-Witt space of dimension n=2m≥4. Assume:

1. M is a compact oriented PL manifold with nonempty boundary E;
2. N is a compact oriented PL Q-Witt pseudomanifold with collared boundary -E;
3. E is bicollared in X;
4. the natural map H_m(E;Q)→IH_m(N;Q) is surjective.

Then there is an explicit PL Q-Witt bordism from X to Y=M union_E cE. In particular Y has at most one isolated singular point. All constructions below are finite after choosing compatible finite triangulations.

### Proof, part A: the residual cap has zero middle group

Put T=N union_E cE. Both caps Y and T are Witt because their new cone links have odd dimension 2m-1. A collared Mayer–Vietoris decomposition of T gives

H_m(E) → IH_m(N) direct-sum IH_m(cE) → IH_m(T)
→ H_(m-1)(E) → IH_(m-1)(N) direct-sum IH_(m-1)(cE).

The cone formula gives IH_m(cE)=0, and the inclusion E→cE induces an isomorphism in degree m-1. Therefore the last arrow is injective, and exactness yields the natural identification

IH_m(T) ≅ cokernel(H_m(E) → IH_m(N)).

This proves IH_m(T)=0 under hypothesis4. It also proves that this hypothesis is exactly the condition for the residual cap T to be directly conable as a Witt nullbordism; it is not claimed necessary for some other construction.

### Proof, part B: separate the two caps by a pinch trace

Use the explicit geometric pinch construction of [S83, II.3, pp.1076–1078]: collapse the middle slice E of a bicollar to a point and attach a collar to the target of the resulting mapping cylinder. Its outgoing boundary is J=Y union_v T, where the two cone vertices are identified. It has an explicit finite triangulation.

The only new potentially restrictive interior link is the suspension of E with its two suspension vertices identified. It has the same normalization as the suspension Sigma E. More precisely, if E is the disjoint union of its connected components E_a, their common normalization is the disjoint union of the suspensions Sigma E_a. Sigma E itself need not be normal when E is disconnected. In dimension 2m the group IH_m(Sigma E) vanishes: allowable m-cycles avoid the suspension vertices, move to the equatorial cylinder, and bound allowable cones to either vertex. Normalization does not change traditional-perversity intersection homology. The pinch event is a point of codimension 2m+1 and hence requires precisely this vanishing for its 2m-dimensional link. The vertex line in the outgoing collar has codimension 2m, so requires no extra vanishing. All other links are inherited from X. Thus the trace is Witt. This checks the actual geometry, rather than inferring a bordism from equality of invariants.

If one wants disjoint caps, separate the identified vertices by a second trace. Start with V=Y disjoint-union T, form the mapping cylinder of the map identifying just their cone vertices, and attach a target collar. Write E_Y and E_T for the two copies of E, and place the merging event at time 0. The local trace is the quotient of (cE_Y times (-epsilon,epsilon)) disjoint-union (cE_T times (-epsilon,epsilon)) which identifies only the two apex rays at times t>=0. Its link is (Sigma E_Y) wedge (Sigma E_T), with only the two outgoing suspension poles identified; the incoming poles remain distinct. This quotient has a finite PL triangulation by triangulating the two product cones and identifying the common ray. Its normalization is the disjoint union of Sigma E_a over the connected components of E_Y and E_T. Each has vanishing IH_m by the same calculation. Away from the event the merged vertex line has odd-dimensional normal link, and the remaining local models are products of the original ones. Hence this is an oriented collared Witt bordism from V to J. Reverse it and concatenate. We obtain a geometric bordism from X to Y disjoint-union T.

### Proof, part C: remove the residual component

By part A and the even-dimensional cone criterion, cT is a Witt nullbordism of T. Glue the oppositely oriented copy needed to cap the T boundary component of the preceding bordism. Collars give a PL gluing and preserve the induced orientations. The remaining boundary is X disjoint-union -Y. This proves the proposition.

### Corollary: product cone neighborhoods

Suppose in the proposition that N is a finite disjoint union of product neighborhoods B_i×cL_i, with B_i and L_i closed oriented PL manifolds and the cone factors Witt. Then hypothesis4 holds.

Indeed, for dim(L_i)>=1, the boundary inclusion L_i→cL_i induces a surjection H_j(L_i;Q)→IH_j(cL_i;Q) in every degree: the cone formula is the identity below its cutoff and zero at and above it. If a zero-dimensional L_i is allowed, the hypotheses that cL_i is a one-dimensional Witt pseudomanifold with no codimension-one singularities and boundary exactly L_i force the interval case, with two link points and a regular apex. Then H_0(L_i)→H_0(cL_i) is surjective directly, and all higher groups vanish; one must not apply the positive-dimensional cone cutoff formula at degree zero in that case. The Künneth formula for a product with the manifold B_i therefore makes

H_m(B_i×L_i;Q) → IH_m(B_i×cL_i;Q)

surjective. Direct sums handle finitely many components. The proposition supplies an actual bordism, not just a signature comparison. This corollary works in every even dimension at least4 in its stated category; the odd-dimensional target is already handled by coning.

### Relation to prior equivariant Moore approximation results

Banagl–Chriestenson [BC17, Proposition10.1] prove vanishing of the middle intersection group of the capped cone bundle T in dimension4d under a suitable middle-degree equivariant Moore approximation hypothesis on the link. Their Corollary10.2 records equality of rational Witt classes. Applying the explicit pinch-and-cone construction above to their vanishing conclusion yields isolation in that restricted PL-compatible depth-one class. The construction does not assert that the intersection space itself is the desired pseudomanifold.

The equivariance hypothesis cannot be silently discarded. Their Example10.3 already demonstrates a signature defect for CP^2 stratified by CP^1. Section3 above uses a genuine singular stratum to demonstrate the same type of obstruction. No universal existence of equivariant Moore approximations is assumed. Their separate local duality-obstruction hypotheses for Poincaré duality of intersection spaces must not be confused with Proposition10.1's hypotheses.

**Remaining gap:** arbitrary twisted and higher-depth neighborhoods need not satisfy the boundary surjectivity, and the example proves that it fails even for a simple depth-one Q-homology manifold. No geometric correction of the nonzero residual cap, or terminating replacement of the neighborhood, has been supplied.

## 6. Route 5: localizing the entire middle pairing in the regular part

One might try to realize a basis of IH_m(X) by cycles in X_reg, thicken them inside an ordinary manifold, and use ordinary handles to retain the full pairing while discarding the singular neighborhood. The necessary universal surjectivity assertion

H_m(X_reg;Q) → IH_m(X;Q)

is false. For the example in Section3, H_4(X_reg;Q)=0 and IH_4(X;Q)=Q. Thus even the unique nonzero middle generator cannot be moved into the regular locus. This is an exact obstruction to the proposed geometric localization, not merely a lack of a general-position proof.

Allowable intersection cycles may meet singular strata. Siegel's surgery works with such cycles and constructs generators using manifolds with boundary [S83, III–IV]. Replacing the failed localization claim by his computed classification and generators would return to the prior existence proof that motivated the question. A new relative geometric extraction/correction mechanism remains missing. The existing singular-surgery construction already treats dimensions4k+2 over Q (with dimension2 handled separately), as explained in [F09]. It is credited as prior work, not claimed anew or replaced by a false regular-cycle argument.

## 7. What has and has not been established

Established in the corrected scoped arguments, as detailed in the accompanying independent audit:

- The standard direct-cone range, including all odd dimensions.
- A precise sufficient condition producing a finite explicit isolation bordism, with all new link tests and collars described.
- Its product-cone-neighborhood consequence and its relation to an existing equivariant Moore approximation theorem.
- A weighted-projective obstruction to uncorrected singular-neighborhood collapse and to full middle-cycle localization in the regular locus.

Not established:

- A universal geometric construction for arbitrary compact oriented PL Q-Witt spaces.
- A counterexample to the original target; known bordism existence is respected.
- Novelty of any partial statement or example.
- A full audit of the cited literature. The accompanying independent audit checks the scoped arguments and the specifically identified source passages only.

The five construction routes are stopped. The exact unresolved step is the geometric treatment of a capped singular neighborhood T with nonzero middle intersection homology, allowing twisted link bundles and higher-depth links while preserving the correct Witt class and decreasing singular complexity. An abstract choice of an isolated representative of w(T) is not the missing geometric operation.

## References and inspected scope

[F11] Greg Friedman's Question1, *Stratified Spaces: Joining Analysis, Topology and Geometry*, Oberwolfach Report56/2011, pp.3279–3280. https://ems.press/content/serial-article-files/46371 . Exact target and its already-known existence statement inspected. The source's Siegel bibliographic entry is erroneous; [S83] gives the correct article.

[S83] P. H. Siegel, *Witt spaces: a geometric cycle theory for KO-homology at odd primes*, American Journal of Mathematics105(1983),1067–1105. https://doi.org/10.2307/2374334 ; author-hosted scan https://cmrr-star.ucsd.edu/static/pubs/witt_spaces_low_res.pdf . Inspected II.2–3 on pp.1076–1078 and selected III–IV material on pp.1092–1099. The complete surgery proof was not independently audited.

[F09] Greg Friedman, *Intersection homology with field coefficients: K-Witt spaces and K-Witt bordism*, Communications on Pure and Applied Mathematics62(2009),1265–1292. https://doi.org/10.1002/cpa.20291 . Author's bundled copy with corrigendum and follow-up: https://faculty.tcu.edu/gfriedman/papers/Gwitt3rev_corr.pdf . Rational/surgery conventions and the warning against omitting irreducibility edge cases inspected. The separate characteristic-two problem was not reopened.

[F15] Greg Friedman, *Stratified and unstratified bordism of pseudomanifolds*, Topology and its Applications194(2015),51–92. https://faculty.tcu.edu/gfriedman/papers/stratwitt.pdf . Definitions, Corollary4.5, and Theorem5.10 inspected. Matching stratifications of an existing bordism is not isolation of genuine singularities.

[FBook] Greg Friedman, *Singular Intersection Homology*, Cambridge University Press(2020), Chapter9. Public author manuscript: https://faculty.tcu.edu/gfriedman/ihbook.pdf . The retained manuscript's §§9.3 and9.5 are used for standard signature/bordism context; manuscript and published pagination are not conflated.

[B08] Markus Banagl, *The signature of singular spaces and its refinements to generalized homology theories*, author survey. https://www.mathi.uni-heidelberg.de/~banagl/pdfdocs/signMSRI2008.pdf . Witt-cone and bordism context inspected.

[BC17] Markus Banagl and Bryce Chriestenson, *Intersection Spaces, Equivariant Moore Approximation and the Signature*, Journal of Singularities16(2017),141–179, DOI10.5427/jsing.2017.16g. https://www.journalofsing.org/volume16/volume16.pdf ; preprint https://arxiv.org/abs/1607.05848 . Proposition10.1 and Corollary10.2/Example10.3 on published pp.165–166, and their neighboring hypotheses inspected in both the preprint and publisher PDF. Full paper not independently audited.

[BFNR] Anthony Bahri, Matthias Franz, Dietrich Notbohm, Nigel Ray, *Classifying weighted projective spaces*, public manuscript. https://eprints.maths.manchester.ac.uk/1671/1/bfnrfinal.pdf . §§1–3, especially Theorem2.1 and Lemma3.1, inspected through the web reader; direct local retrieval twice returned HTTP502. Kawasaki's underlying primary calculation is *Cohomology of twisted projective spaces and lens complexes*, Math. Ann.206(1973),243–248, https://doi.org/10.1007/BF01429212 . No claim is made to have independently audited that paper.
