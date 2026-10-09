# Independent audit: geometric isolation in rational Witt bordism

Problem 30001946 / OWR-11454-004. Audit date: 9 October 2026.

## Decision and exact scope

**Accept the corrected restricted results, not a solution of the original question.** The original five-route investigation remains exhausted at **5/5**, and its original methodological target remains **UNRESOLVED**. This audit adds **zero research routes**. It checks the supplied arguments, supplies missing local details, and corrects two edge statements. It does not certify novelty, exhaust the literature, or infer a geometric construction from a computed bordism group.

The reviewed original REPORT.md has SHA-256 `0700fae7ee46c3d3e40e41020c2f47f0778527df279ed9ed4b3d11588eb5a1f5` and 20,973 bytes. It is retained unchanged in `original/authored/REPORT.md`. `REPORT_CORRECTED.md` and `REPORT_CORRECTIONS.patch` provide the reviewable correction. Acceptance applies to the corrected report together with the details below, not verbatim to the original proof wording.

Accepted results are:

1. The standard direct-cone construction in odd dimensions and in even dimension 2m when IH_m vanishes.
2. The explicit sufficient boundary-surjectivity criterion in even dimension at least 4, with the actual pinch and separation traces checked below.
3. Its product-cone consequence, including a separately handled zero-dimensional-link edge case.
4. The weighted-projective counterexample to uncorrected neighborhood capping and to universal regular-locus representation of middle intersection classes.
5. The stated restricted relationship to Banagl–Chriestenson Proposition 10.1, with its equivariant hypothesis retained.

No publication, repository modification, queue edit, or source-document redistribution is part of this audit.

## 1. Required corrections

### C1. Disconnected interface and normalization

The original sentence “Its normalization is the suspension Sigma E” is incorrect when E is disconnected. Write E as the disjoint union of connected closed manifolds E_a. The normalization of the pinch-event link, and the normalization of Sigma E, are both the disjoint union of Sigma E_a. Sigma E need not itself be normal. Thus the needed middle-IH equality and vanishing survive, but the literal normalization assertion must change.

This is not a newly discovered gap in Siegel's text: the original source on printed p.1077 carefully says that the two spaces have the *same normalization*. The corrected report restores that scope.

### C2. Zero-dimensional link in the product corollary

The corollary does not explicitly require dim(L_i)>0, whereas its all-degree cone-formula sentence does. If cL_i is allowed to be a one-dimensional pseudomanifold with no codimension-one singularities, and its boundary is exactly L_i, the allowable zero-dimensional-link case is an interval, with two link points and a regular midpoint. Here H_0(L_i;Q) maps onto H_0(cL_i;Q), but it is not an isomorphism and is not the zero target of the stated cutoff rule. Surjectivity follows directly. Positive-dimensional L_i use the usual cone formula. The corrected report makes this distinction explicit; the corollary's conclusion is unchanged.

### C3. Proof expansions, without changing the theorem

The correction spells out the separation quotient, incoming versus outgoing suspension poles, event codimension, and cap orientation convention. These are supporting details rather than counterexamples to the construction. In particular, a “wedge of suspensions” must mean identification of just their outgoing poles at the event link; identifying both poles would give the wrong local model.

## 2. Cone and Mayer–Vietoris checks

All intersection homology here is traditional lower-middle perversity over Q. There are no codimension-one singular strata; boundary collars are not treated as interior strata.

For a closed n-dimensional Witt space X, the cone has the old links along product strata. Its apex has codimension n+1 and link X. If n is odd that codimension is even; there is no new Witt condition. If n=2m>0, the new condition is exactly IH_m(X)=0. A small ball in the regular part may be removed from an oriented nullbordism to obtain a spherical outgoing boundary. Dimensions 0 and 2 already have only isolated possible singularities under the stated convention.

For E of dimension 2m-1, the cone formula cutoff is

(2m-1) - lower_middle(2m) = (2m-1) - (m-1) = m.

Thus IH_m(cE)=0 and H_(m-1)(E) -> IH_(m-1)(cE) is an isomorphism. Apply Mayer–Vietoris using collar-thickened open sets in T=N union_E cE. The degree-(m-1) map into IH_(m-1)(N) direct-sum IH_(m-1)(cE) is injective because its cone component is an isomorphism. Exactness therefore gives

IH_m(T) = coker[H_m(E) -> IH_m(N)].

No omitted kernel term remains. T is already Witt before this computation: the newly added cap point has even codimension 2m and odd-dimensional link E. The surjectivity assumption is exactly the additional condition needed to make cT Witt at its apex. It is not necessary for every possible isolation bordism.

For a manifold core M, the same calculation gives IH_m(M union_E cE) = coker[H_m(E)->H_m(M)], which the ordinary relative long exact sequence identifies with im[H_m(M)->H_m(M,E)]. This establishes the signature computation used below.

## 3. Actual pinch geometry, including non-normality

Choose a finite triangulation compatible with the interface, original strata and a bicollar E times [-1,1]. Siegel's explicit pinch is the quotient collapsing its middle E slice to a common point, with the mapping cylinder followed by a product collar on the target. Its outgoing boundary is J=Y union_v T, where Y=M union_E cE and T=N union_E cE use separate sides of the interface but one shared apex in J.

At the pinch event the link is

L_p = (E times [-1,1]) union cone(E times {-1,1}),

where the latter is one cone on the disjoint union of the two boundary copies. Equivalently, L_p is Sigma E with its two suspension poles identified. It is generally not Sigma E. If E has k connected components, the normalization of L_p is the disjoint union of the k individual suspensions Sigma E_a. That is also the normalization of Sigma E.

Traditional lower-middle IH is invariant under normalization: the needed bound p(S)<=codim(S)-2 holds. This precise normalization statement is independently supported by Friedman, Singular Intersection Homology, Proposition 5.1.11 of the retained author manuscript. It must not be extended to unrestricted high perversities.

The vanishing IH_m(Sigma E_a)=0 follows directly from a two-cone Mayer–Vietoris calculation. The middle groups of both cones are zero. In degree m-1 the map from H_(m-1)(E_a) into the two cone groups has two isomorphic components, up to sign, and hence is injective. Alternatively allowable m-cycles avoid the poles and their (m+1)-dimensional cones have allowable zero-dimensional apex intersection. The MV argument avoids any ambiguity in the word “move.” It works for all m>=2 in the proposition, whether m is even or odd.

The event is a 0-stratum in the (2m+1)-dimensional trace, so its 2m-dimensional link needs precisely the just-proved middle vanishing. The outgoing apex line is a 1-stratum of codimension 2m, with odd-dimensional normal link E disjoint-union E; it imposes no Witt middle-vanishing condition. Its non-normality is allowed. Old strata have their old links. All new singular codimensions are at least 4, so no codimension-one strata have appeared.

Siegel states the additivity proposition in dimension 4k. The present extension of its *local trace construction* to all even dimensions is justified by these explicit m-degree calculations, not by citing an unstated 4k+2 version of that proposition.

## 4. Vertex separation is an actual collared Witt bordism

Start with V=Y disjoint-union T and identify only the two chosen cap vertices by f:V->J. Take the mapping cylinder, then append J times [0,1]. Near the event, write E_Y and E_T for the incoming cone links. A full neighborhood is the quotient of

(cE_Y times (-epsilon,epsilon)) disjoint-union (cE_T times (-epsilon,epsilon))

by identifying their two apex rays for t>=0 only. For t<0 the apex lines remain distinct. This description is obtained directly by restricting the mapping-cylinder quotient and its appended collar; no classification or invariant comparison is used.

A product cone cE_i times R has event link Sigma E_i. Identifying the outgoing apex rays identifies exactly their positive suspension poles. The event link is therefore (Sigma E_Y) wedge (Sigma E_T), with their incoming poles separate. Its normalization is the disjoint union of the suspensions of all connected components of both links. The preceding suspension calculation gives zero IH_m. Each incoming or outgoing apex line has codimension 2m, so introduces no further vanishing condition. Other local models are unchanged product models from Y and T.

This quotient is PL: use finite product-cone triangulations whose positive apex rays are subcomplexes, then identify just those rays; equivalently triangulate the finite simplicial mapping cylinder of vertex identification and the target collar. There is no arbitrary cell-like quotient being assumed triangulable. The new event link is a pseudomanifold with permitted non-normal point identifications; its regular stratum is dense and its codimension-one faces have the usual two-sided incidence.

The incoming boundary has its untouched V product collar. The explicitly attached target product gives a J collar. Orient each top-dimensional regular stratum by its inherited product orientation. Since the identified loci have codimension at least 4, no top-dimensional orientation faces are identified inconsistently. Choose the overall bordism orientation so its boundary is V disjoint-union -J. Reverse this trace and concatenate with the pinch bordism to obtain X bordant to Y disjoint-union T.

Orient M and N as subspaces of X, so their interface orientations are opposite. Orient each cap to cancel the relevant boundary orientation. The preceding bordism has boundary X disjoint-union -Y disjoint-union -T. Orient cT to have boundary +T and glue along the collared T faces. Collar gluing cancels the T boundary and leaves exactly X disjoint-union -Y. This proves the scoped proposition without appealing to equality of Witt classes.

All operations involve finitely many finite triangulations, cones, products, identifications of explicitly named subcomplexes, and collar gluings. Finiteness here proves termination of this *conditional recipe*, not termination of any general singularity-reduction algorithm.

## 5. Product-cone neighborhoods and prior Moore-approximation theorem

The separate cone-factor-exchange route is correctly only conditional. The boundary of cB times cL has the two pieces B times cL and cB times L, with compatible corner rounding. Witt products are Witt, but this requires cB as well as cL to be Witt. For even-dimensional B, nonzero middle homology violates that requirement, independently of the original link condition on L. Even a permitted exchange can replace a singular locus of dimension dim(B) by one of dimension dim(L), so it is not a monotone induction. No general twisted-bundle gluing was provided. This route supplies neither an obstruction to the original question nor a universal solution.

For positive-dimensional closed manifold L, the inclusion L->cL induces a surjection in every degree to traditional IH: an isomorphism below the positive cone cutoff and a zero target at and above it. Kunneth for a manifold factor B over Q makes H_m(B times L)->IH_m(B times cL) surjective term by term. Finite disjoint unions give direct sums. The zero-dimensional interval edge case is handled in C2. No trivialization of an arbitrary link bundle is inferred.

Banagl–Chriestenson Proposition 10.1 is used within its supplied framework: compact oriented depth-one Thom–Mather space, dimension n=4d with d>0; compact compatibly oriented link-bundle manifolds E, B and L; a structure group G acting on L; the Witt condition; and a G-equivariant Moore approximation of degree floor((dim L+1)/2). A Moore approximation is a G-equivariant map inducing rational homology isomorphisms below that degree, with source homology zero from that degree upward. Its equivariance must match the link bundle's structure group (or an appropriate reduction).

Under those conditions Proposition 10.1 proves IH_(2d)(T E)=0. The paper's Corollary 10.2 then states equality of Witt classes of X and the capped regular part. Here an *actual* bordism follows by applying the separately checked pinch/separation/cone construction, provided the particular data and cone bundle are PL-compatible. There is no claim that an arbitrary topological or smooth construction automatically supplies all requested PL data.

The local duality-obstruction vanishing hypothesis used for the paper's intersection-space duality/signature comparison is not a hypothesis of Proposition 10.1. Conversely, the Moore approximation hypothesis cannot be dropped. Example 10.3, CP2 artificially stratified by CP1 with Hopf link bundle, exhibits a signature defect and explains the absent equivariant approximation. The present weighted example has a genuine nonmanifold stratum.

## 6. Independent weighted-projective verification

Let X=P(1,1,2,2,2), the underlying quotient space. Where u_0 or u_1 is nonzero, fixing that coordinate gives a smooth chart. On u_0=u_1=0, the weight-two coordinates define P(2,2,2)=CP2. Fixing a nonzero weight-two coordinate leaves the residual group {+1,-1}, acting trivially on the two tangent complex coordinates and by -1 on both normal complex coordinates. Thus the transverse link is RP3, and the full local model is R4 times c(RP3).

RP3 has integral H_1=Z/2 and top H_3=Z. The total point link is S3 join RP3, equivalently the fourfold suspension of RP3. It has nonzero Z/2 in reduced degree 5, so local homology has nonmanifold torsion in degree 6. This proves the CP2 locus is genuinely nonmanifold. Over Q the same link has sphere homology, so X is an oriented rational homology manifold and IH(X;Q)=H(X;Q). Its only positive-dimensional singular stratum has even codimension 4, consistent with Wittness.

The coordinate power map q:CP4->X is the quotient by G=(Z/2)^3 acting through independent signs on the last three homogeneous coordinates. To check the fibers, equality in the weighted target means that, for one nonzero scalar lambda, the first two coordinates scale by lambda and the squares of the last three by lambda squared. Choosing square roots gives exactly independent signs after the same projective scalar. Every target has a preimage, and compactness/Hausdorffness identifies the target with the quotient. The action is globally effective; a point with all coordinates nonzero has eight distinct projective preimages. The generic degree is +8, since the map is holomorphic and orientation preserving there.

Every sign change is induced by a complex diagonal linear automorphism and acts trivially on the rational cohomology ring of CP4. A finite equivariant triangulation, subdivided to remove simplex inversions, identifies rational quotient cochains with invariant cochains. Exactness of finite-group averaging gives H*(X;Q)=H*(CP4;Q). Nonfreeness does not invalidate this argument. Consequently H^4(X;Q) is one-dimensional. If q*a=h^2, naturality of evaluation gives 8<a^2,[X]>=1. Its pairing is <1/8> and its signature is +1. Kawasaki coefficients (1,2,4,8,8) independently give the rescaled form <2>; the two are related by the rational basis scale 1/4. The signature proof does not require Kawasaki's integral ring theorem.

There is an explicit compatible decomposition, not just a presumed regular neighborhood. Normalize ||u||=1 on the regular complement, leaving the U(1) action (u,v)->(t u,t^2 v). This identifies X minus CP2 with a rank-three complex vector bundle over CP1. Take its closed unit disk bundle M. On the other side normalize ||v||=1; then the exterior plus CP2 is

N=(D4 times S5)/U(1), with t acting with weights (1,2).

It is a bundle over CP2 with fiber D4/{+1,-1}=c(RP3). Its boundary is

E=(S3 times S5)/U(1).

The action on E is free, and projection to CP1 exhibits E as an S5-bundle; projection to CP2 exhibits it as the RP3 link bundle. Rescaling norms identifies these descriptions along the same boundary. The equations, inequalities and compact-group quotient models are semialgebraic; compatible triangulation and regular collars give the claimed PL decomposition. M retracts to CP1 and N retracts to CP2. The latter retraction is used to compute ordinary homology only after recognizing N as a rational homology manifold (with boundary); no false general homotopy invariance of IH is used.

Thus H_4(M;Q)=0 and IH_4(N;Q)=Q. The rational Serre page for S5->E->CP1 has support only at (0,0),(2,0),(0,5),(2,5). The base is simply connected, so no monodromy coefficient issue occurs; no differential can connect nonzero terms. In particular H_3(E)=H_4(E)=0. It follows both that IH_4(Y)=0 for Y=M union_E cE, and that IH_4(T)=Q. Therefore sigma(X)=1 while sigma(Y)=0, so these two particular spaces cannot be Witt bordant by signature invariance. The same regular-complement retraction gives H_4(X_reg)=0 while IH_4(X)=Q, disproving the proposed universal localization surjectivity.

This is not a counterexample to Friedman's requested existence; another isolated-singularity output can carry the missing form. Nor does signature zero in some other example by itself certify nullbordism or a specified construction.

## 7. Source and executable verification limits

The retained OWR source explicitly states that existence was already known from Siegel's computation and generators, and asks for a purely topological construction. Its adjacent characteristic-two question is different. The audit reread the exact target and did not reopen or resolve the characteristic-two problem.

Source checks cover Siegel II.2–3 (printed pp.1076–1078; pp.1076–1077 visually inspected), Banagl–Chriestenson definitions and Proposition 10.1/Corollary 10.2/Example 10.3 in the retained author preprint, and Friedman's normalization proposition. The correction/irreducibility warnings in Friedman's bundled corrigendum and the 2015 stratification-change theorem were checked as contextual boundaries. Changing stratifications of a known bordism does not remove genuine singularities of its boundary. The full Siegel surgery proof, all cited papers, Kawasaki's original article, and a universal literature-openness claim have not been independently certified.

`independent_checks.py` uses explicit runtime guards, rational arithmetic, subset-gcd/lcm calculations independent of the author's sorted-weight shortcut, finite sign-orbit enumeration, degree-support/differential checks, and rational matrix ranks. It contains no Python assert statements. The original arithmetic script does use asserts: under -O and -OO its guards disappear, so its success message alone is not robust verification. The new checks and deliberately corrupted inputs are actually run in all three interpreter modes.

The recorded fixtures for normalization and theorem scope are claim-consistency checks; they do not mechanize topology. Neither finite m tests nor any arithmetic checksum proves a universal geometric result. The mathematical justification is the written local-model and source audit above.

Read-only replay and mutation results, exact diagnostics, source hashes, original pins, corrected report hash and acceptance scope are recorded in the packet and accompanying replay evidence. Frozen replay is performed as UID 1000 with file modes 0444 and directory modes 0555, bytecode writing disabled, and actual denied write probes. Source bodies and private coordination files are excluded from the archive.
