# Prescribed polygon-bundle cores: a first partial result

Problem 10300012 / AMR-102-0012, queue rank 1247, Calegari Question 6.2.
Date: 10 October 2026 UTC. **Attempt 1 of 5. Status: unresolved.**

This is an AI-assisted, unrefereed mathematical note. It proves a topological-lift lemma, a finite-cover consequence in the closed orientable case, and a quantitative sufficient condition in the base manifold. It does not prove either requested assertion for every prescribed core in the base manifold. No novelty, exhaustive literature search, human peer review, or proof-assistant certification is claimed.

## 1. The target and the restricted setting of the partials

Let Lambda be a full genuine essential lamination of a hyperbolic 3-manifold M, and let C be the specified complementary region that is an ideal-polygon bundle over a circle. Let c be its prescribed core circle. The questions are whether c is ambient isotopic to a geodesic and whether it has a noncoalescable insulator family [S1, Question 6.2, pp. 11-12].

Fullness here means existence of a qualifying complementary bundle. It is not the stronger condition that every complementary component is such a bundle. The arguments below use only the specified component and standard consequences of essentiality. They make no claim about the distinct sublamination problem, Question 6.1.

For the stated partial theorems, **M is closed and orientable** and carries its complete hyperbolic metric. This is an explicit restriction, not a reinterpretation of any wider reading of Question 6.2. In particular every nontrivial element of Gamma = pi_1(M) is loxodromic. No claim here covers a potentially parabolic core in a noncompact manifold or the nonorientable case.

An ideal polygon is the usual disk with finitely many distinguished boundary points removed, with the remaining boundary intervals called sides. The completed component Cbar is understood in the cut-open-lamination sense: its boundary sides are mapped to boundary leaves of Lambda. A core is the usual core isotopy class of the disk mapping torus, not an arbitrary knot that happens to generate its fundamental group. Work can be in the smooth/locally flat category. The finite monodromy permutation of sides need not be trivial.

### Imported topological inputs

We use the following established product-lamination theorem, explicitly recorded by Calegari in [S1, Question 6.3, Remark (2), p. 12] and attributed there to Gabai-Kazez [S2]:

The lifted essential lamination pair is homeomorphic to (R^2, lambda) x R, where lambda is an essential lamination of the plane by properly embedded lines.

This homeomorphism is **not** assumed Gamma-equivariant. The original [S2] publisher PDF returned HTTP 403 in this attempt and was not retrieved by another route. Its full proof was not inspected. The precise product statement used here was inspected in the primary problem source [S1]; it is an imported theorem, not a new assertion proved in this note.

We also use the solid-torus Core Lemma of Funar-Gadgil [S3, Lemma 4.2, pp. 376-377]. Their use of “geodesic” in that section means topological geodesic. The supporting group argument is restated in Section 4. Their Definition 0.1/1.1 does not require primitivity; their virtual uniqueness Theorem 4.3 explicitly does. We do not drop that hypothesis when citing that theorem. Instead our stronger subgroup-separation input below permits a separate construction for nonprimitive classes.

## 2. The core has an unknotted lift

### Lemma 2.1: complementary components inject

Each connected component of H^3 minus the lifted lamination is simply connected. Hence the inclusion C -> M is pi_1-injective and a chosen lift Ctilde is the universal cover of C.

**Proof.** Apply the product theorem. Each component of the complement is U x R, where U is a component of R^2 minus lambda. If a Jordan curve lies in U, its bounded complementary disk contains no point of lambda: a properly embedded leaf through such a point could not remain in that compact disk and would have to cross the Jordan curve. Thus the disk lies in U. The planar Jordan-curve criterion for simple connectivity implies pi_1(U)=0; equivalently, one can first replace any loop in the open set U by a polygonal loop and split it at its finitely many crossings into Jordan curves. Consequently U x R is simply connected. The restriction of the universal covering map to a complementary component is a covering of C. Its simply connected total space is the universal cover, so pi_1(C) injects into Gamma. Since pi_1(C)=Z, the core represents a nontrivial infinite-order element g. Its chosen lifted line is stabilized by exactly <g> as a lift of the prescribed embedded circle. This last stabilizer concerns the lifted **curve**, not its eventual hyperbolic axis. QED.

### Lemma 2.2: the auxiliary side cover and the proper strip

A component ctilde of the inverse image of c can be joined to a properly embedded line a in one boundary leaf of the lifted lamination by a proper embedded strip S = R x [0,1]. The strip may be chosen equivariant under a positive power g^k, with compact quotient.

**Proof.** Write Cbar as the mapping torus of an orientation-preserving homeomorphism phi of the ideal polygon P. It permutes its finite side set. Choose a positive integer k killing that permutation. The mapping class of phi^k relative to the ideal vertices is trivial: extend it to the closed disk fixing the vertices, isotope its boundary restriction to the identity while fixing those vertices, and apply the Alexander isotopy to the resulting disk homeomorphism fixed on the whole boundary. This gives a product identification of the k-fold mapping torus of phi with P x S^1, preserving each side as a boundary component.

The k-fold cover in this paragraph is only a cover of Cbar. **No extension to a finite cover of M is assumed or needed.** Its core c_k is a connected lift of c, of degree k over c. In the product identification it is isotopic to {p} x S^1 for an interior point p of P; this is precisely the core isotopy class, so we may make this isotopy before continuing. Choose a point q on one side and an embedded compact arc r in P from p to q, with r minus q in the interior. Then r x S^1 is an embedded compact annulus in this auxiliary completed bundle, joining c_k to {q} x S^1 on a boundary annulus.

The inclusion of the interior C into Cbar is a homotopy equivalence by a boundary collar, so their fundamental groups agree. Let W be the universal cover of Cbar. The completion map Cbar -> M lifts to W -> H^3 since W is simply connected. Lemma 2.1 identifies the restriction on the interior with the embedded component Ctilde, rather than merely with an abstract covering. Lift the annulus to W together with the chosen boundary side. Its lift is a strip, since the annulus carries the subgroup <g^k>. Here is the boundary-identification point in detail. The completion map is locally the inclusion of a closed half-box along a boundary plaque. At a fixed ambient point of a lifted leaf there is at most one completion point for each local side: two approaches through the same gap-side half-box have intrinsic distance tending to zero and therefore give the same completion point. A lifted leaf is an unknotted proper plane by the product theorem; it separates H^3. The connected component Ctilde lies on only one of its two sides, so two opposite-side completion points cannot come from this component. Thus the completion map is injective on any boundary side of this component. Boundary-plaque continuation along leafwise paths maps the side into the corresponding lifted leaf (and, in the standard completed-boundary description, onto that leaf). Only injectivity on the side, not surjectivity, is needed for the strip. Interior points lie outside the lifted lamination and cannot coincide with its boundary points. The lifted annulus strip is consequently embedded in H^3. This argument uses the cut-open completion with the induced path metric; it does not identify an arbitrary topological closure with that completion.

The strip has compact fundamental domain under g^k because the original annulus is compact. Since Gamma acts properly discontinuously on H^3, its integer translates escape every compact subset. More explicitly, only finitely many translates of the compact fundamental domain can meet any fixed compact subset of H^3. The lifted strip is therefore proper. Its boundary line a is proper for the same reason. For precise tracking of the original core, extend the initial isotopy from c_k to {p} x S^1 to an ambient isotopy supported in a compact subset of the auxiliary bundle interior, by isotopy extension for the compact circle. Lift this isotopy to W. Its support in Ctilde is contained in a locally finite union of g^k-translates of compact interior sets. It therefore extends by the identity outside Ctilde to a proper ambient isotopy of H^3: only finitely many translated compact support sets meet any compact subset of H^3, and their union is closed in H^3 and disjoint from the lifted lamination. Apply its inverse to the entire constructed strip. The first boundary becomes the original ctilde, while the second boundary a in the leaf remains fixed because the isotopy is supported away from the completed boundary. Properness and embeddedness of the whole strip persist under this ambient homeomorphism. QED.

### Proposition 2.3: topological geodesic property

The prescribed core c is a topological geodesic: every lift of c is an unknotted properly embedded line in H^3 = R^3.

**Proof.** The product theorem identifies the lifted boundary leaf containing a with l x R for a properly embedded planar line l. The planar Schoenflies theorem straightens l in R^2, so this lifted leaf is an unknotted plane in R^3. The proper line a in that plane can likewise be straightened by a homeomorphism of the plane, extended in the normal product direction to ambient R^3. Hence a is an unknotted line.

The proper strip of Lemma 2.2 gives a proper ambient isotopy from ctilde to a. One explicit local description uses a proper regular neighborhood of the strip with coordinates (t,u,v), where the strip is v=0, 0<=u<=1. A transverse disk isotopy, supported away from the boundary of this neighborhood, moves (u,v)=(0,0) to (s,0) for 0<=s<=1. Apply it in each t-slice and extend by the identity outside the neighborhood. Properness ensures that these local modifications fit to a global proper ambient isotopy. In the locally flat category use the corresponding product regular neighborhood. Thus ctilde is unknotted. Other lifts are deck translates and have the same property. QED.

No step above identifies ctilde with a hyperbolic axis by a Gamma-equivariant isotopy. The power g^k controls only one strip. This is the first obstruction to promoting Proposition 2.3 to the base-manifold conclusion.

## 3. A compact cyclic tube embeds in some finite cover

Let g be any nontrivial element of Gamma, **possibly a proper power**. Let L be its axis and let T_R(L) be the closed radius-R tube in H^3. The quotient Q_R = T_R(L)/<g> is a compact solid torus in the cyclic cover M_g = H^3/<g>.

### Lemma 3.1: cyclic separability input

The subgroup <g> is separable in Gamma: for each h outside <g>, a finite-index subgroup H_h of Gamma contains <g> and excludes h.

**Proof from published theorems.** Gamma acts properly and cocompactly on a CAT(0) cube complex by the closed-hyperbolic-3-manifold cubulation theorem recorded as [S4, Theorem 9.3, printed p. 1065]. Agol's [S4, Corollary 1.3, printed p. 1046], using Haglund-Wise, gives separability of all quasiconvex subgroups. Every cyclic subgroup generated by a loxodromic element is quasiconvex: its orbit lies at uniformly bounded distance from its axis and has bounded gaps along that axis; cocompactness identifies the word and hyperbolic metrics up to quasi-isometry. This reasoning applies to a nonmaximal finite-index subgroup of the axis stabilizer as well. Therefore <g>, not merely the maximal cyclic subgroup containing it, is separable. QED.

The primitive case can also be obtained from residual finiteness and the maximal-cyclic centralizer argument in [S3, Section 2]. That weaker argument is not substituted for cyclic separability in the nonprimitive case.

### Lemma 3.2: explicit compact-set embedding

For every R>0 there is a finite-index subgroup H containing <g> such that Q_R embeds by the covering projection in M_H = H^3/H.

**Proof.** In Fermi coordinates around L choose a compact fundamental cylinder F in T_R(L) whose longitudinal coordinate runs over one translation period of g. The set

E = {h in Gamma : hF intersects F}

is finite by proper discontinuity. For each h in E minus <g>, choose H_h from Lemma 3.1 and set H to their finite intersection (or Gamma if that finite set is empty).

Suppose x,y in T_R(L) project to the same point of M_H, so y=hx for h in H. Choose integers a,b with x=g^a x_0 and y=g^b y_0, where x_0,y_0 lie in F. Then y_0=(g^(-b) h g^a)x_0. The element in parentheses belongs to H intersect E, which by construction is contained in <g>. Thus h belongs to <g>. Consequently x,y already represent the same point of Q_R. The induced map from the compact Q_R is injective and is locally a smooth embedding, so it is an embedding. QED.

### Root bookkeeping

If g=h_0^m in Gamma for a primitive h_0 and m>1, then L/<g> has length m times the primitive base geodesic length. After Q_R embeds in M_H, the axis stabilizer in H is exactly <g>; otherwise two different points of Q_R would be identified. Thus g is primitive **in H**, while it remains a proper power **in Gamma**. The geodesic in M_H projects to a multiply traversed geodesic in M. This does not change the prescribed curve: the lift c_H chosen from M_g maps homeomorphically to c because <g> is the image of pi_1(c).

The cover M_H need not be regular. Replacing it by the normal-core cover may replace a homeomorphic lift of c by a higher-degree lift. We do not make that replacement without tracking its degree.

## 4. The Core Lemma and the virtual conclusion

### Lemma 4.1: solid-torus form of the Core Lemma

Let Q be an embedded hyperbolic tube around a simple closed geodesic delta in a hyperbolic 3-manifold. Suppose an embedded circle k in the interior of Q has winding number +1 or -1 in Q and its lift to H^3 is unknotted. Then k is isotopic in Q to the core delta.

This is the form of [S3, Lemma 4.2] used below. For clarity, here is its group argument, including the winding and orientation points. A lift D of Q is a standard solid cylinder D^2 x R containing a single lift K of k; uniqueness uses winding number one. The inclusion D minus K -> R^3 minus K induces a pi_1 isomorphism. Indeed the exterior of D is a standard annular product whose fundamental group is generated by the same meridian as the boundary of D, so van Kampen adds neither a generator nor a relation. Since K is an unknot, this group is Z. It is the kernel of the natural surjection pi_1(Q minus k) -> pi_1(Q)=Z. The conjugation action on the kernel preserves a meridian's orientation, since the ambient manifold and the closed curve are orientable. Thus the extension is Z x Z, rather than the Klein-bottle group.

For a small tubular neighborhood N(k), the compact exterior Q minus int N(k) is irreducible: a sphere bounds a ball in the solid torus Q, and k cannot lie in that ball because its winding number is one. Both boundary tori are incompressible. A small meridian of k generates the kernel. The outer meridian also has linking number +1 or -1 with K, because a meridian disk of Q has algebraic intersection +1 or -1 with the winding-one curve k; hence it too generates that kernel. On either boundary torus a longitude maps to +1 or -1 in the quotient pi_1(Q). The meridian and longitude images are therefore independent in Z x Z, which proves injectivity of both peripheral groups. The standard irreducible two-torus-boundary product characterization then gives T^2 x I. Equivalently, this is the final solid-torus step of the cited Core Lemma. It follows that k is a core of Q, hence isotopic to delta. This topological characterization is imported as part of the Core Lemma, not claimed as a new classification theorem.

### Theorem 4.2: both conclusions after a finite cover

In the closed orientable setting of Section 1, for every R>0 there is a finite-sheeted hyperbolic cover p:M' -> M and a lift c' of the **specified** core c such that:

1. p restricted to c' is a homeomorphism onto c;
2. c' is ambient isotopic in M' to a simple closed geodesic delta';
3. delta' has an embedded hyperbolic tube of radius greater than R;
4. if R is chosen greater than log(3)/2, delta' has a noncoalescable insulator family for pi_1(M').

**Proof.** In M_g, the chosen lift c_g of c is compact and embedded. Its distance from L/<g> has a finite maximum r_c. Choose a number B>max(R,r_c,log(3)/2). Use Lemma 3.2 to embed Q_B in a finite cover M'. The image c' lies in its interior. It has winding number one in Q_B because it represents g, and g generates the fundamental group of this tube. Proposition 2.3 supplies its unknotted universal lift. Lemma 4.1 gives the desired isotopy to delta'=L/<g>. This delta' has the stated tube, and [S5, Example A.3, printed p. 428] gives a noncoalescable Dirichlet insulator family. The choice of c_g guarantees the homeomorphic projection to the original c. QED.

Theorem 4.2 is a consequence of established topological-geodesic, subgroup-separability and insulator theory, with the prescribed core tracked explicitly. It is not a new proof of Calegari's base-manifold assertions. In particular no full-group-equivariant family is obtained by simply reading the family for the finite-index subgroup as one for Gamma.

## 5. A quantitative sufficient condition in the base manifold

This criterion is useful when geometric data about the prescribed core and its conjugacy class are available. It supplies an actual sufficient condition rather than replacing isotopy by homotopy.

Let c be rectifiable with length A, and suppose its class g is primitive in Gamma. Suppose the corresponding closed geodesic delta is embedded and has an embedded closed tube of radius r. Write ell>0 for its translation length and theta for its rotation angle modulo 2 pi. Put

S = sinh^2(ell/2),    T = sin^2(theta/2).

### Proposition 5.1: length-tube criterion

If

sinh^2(A/2) < S + (S+T) sinh^2(r),

then c is isotopic to delta. If also r>log(3)/2, the geodesic in this prescribed isotopy class has a noncoalescable insulator family.

**Proof.** A point x on a chosen lift of c is joined to gx by one traversal of the lifted curve, of length A. Thus d(x,gx)<=A. Let rho be its perpendicular distance from the axis L. In the hyperboloid model, use coordinates

x=(cosh rho cosh t, cosh rho sinh t, sinh rho cos phi, sinh rho sin phi).

The isometry g adds ell to t and theta to phi. The Lorentz inner product gives

cosh d(x,gx) = cosh^2(rho) cosh ell - sinh^2(rho) cos theta,

and hence the exact identity

sinh^2(d(x,gx)/2) = S + (S+T) sinh^2(rho).

Since S>0, the stated strict inequality forces rho<r. The whole prescribed core therefore lies inside the embedded tube about delta. Its winding number there is one, because g is primitive and the tube's core represents g. Proposition 2.3 and Lemma 4.1 establish isotopy. The tube-radius criterion from [S5] then supplies the insulator family. QED.

A rotation-free but stronger sufficient condition is sinh(A/2) < sinh(ell/2) cosh r, obtained by dropping the nonnegative T term. No length or radius inequality of this kind is derived from fullness alone.

## 6. Two obstructions that cannot be discarded

### 6.1 Proper powers are compatible with unknotted lifts

Every embedded geodesic traversed once represents a primitive conjugacy class. Indeed its axis stabilizer in a torsion-free discrete orientation-preserving hyperbolic group is cyclic. An element interchanging the endpoints of the axis would have order two, and is excluded. If g=h^m with m>1, the geodesic representative of g traverses L/<h> exactly m times. An isotopy of an embedded circle cannot end at that multiple parametrization.

Unknotted lifts do not remove this obstruction. Here is an explicit comparison example, **not a lamination counterexample**. Choose a sufficiently small tube around a simple primitive closed geodesic representing h, and identify the solid torus with S^1 x D^2. For an integer m>=2 and small epsilon>0, the curve

u -> (exp(i m u), epsilon exp(i u)),    u in R/(2 pi Z),

is embedded and represents h^m. Its universal lifts, in the universal cylinder D^2 x R, are helices that are graphs over the longitudinal coordinate. Each is an unknotted line: in normal-plane/longitudinal coordinates (z,t) on all H^3, the proper homeomorphism (z,t)->(z-f(t),t) straightens such a graph. This embedded circle has unknotted lifts but is not isotopic to an embedded geodesic in the base manifold. No essential lamination with this curve as a qualifying complementary core is constructed here.

A separate recent primary preprint [S6, Proposition 7.1] claims examples of divisible periodic Anosov orbits in closed hyperbolic manifolds. Its statement and construction pages were inspected, but its entire proof was not audited. An Anosov orbit alone does not supply the genuine polygon-bundle complement required here; no counterexample to Question 6.2 is inferred from it.

### 6.2 Insulator convexity already contains geometric separation

For a family indexed by distinct endpoint pairs A_i, the separation and convexity conditions of [S5, Definition A.1] imply that the hyperbolic lines joining the pairs A_i are pairwise disjoint. To see this, the separating Jordan curve lambda_ij divides S^2 into two components. The round circle containing A_i and disjoint from lambda_ij lies entirely in one component; the analogous circle containing A_j lies in the other. The two round circles are disjoint. Their hyperbolic planes are therefore disjoint, and the corresponding axes, contained in those planes, cannot intersect.

Thus arbitrary topological boundary leaves do not automatically give insulators: their ideal sets need not be round-circle-separable as required by this convexity condition. One must also verify full Gamma-equivariance, local finiteness, and the no-trilinking condition for each triple.

For a proper-power core, distinct lifted curves may have the same endpoint pair. Passing to the set of distinct endpoint pairs discards that multiplicity and hence does not detect primitivity. Any convention for “the core has an insulator family” must keep this issue separate from the embedded-geodesic/isotopy requirement. This note claims the family only after the core has been identified with the simple geodesic delta' in Theorem 4.2, or delta in Proposition 5.1.

## 7. Why the attempted general proof stops

The following are **not** established from essentiality, genuineness and fullness:

- that the prescribed base class g is primitive;
- that its primitive geodesic image is embedded;
- that the proper straightening of one lifted core can be chosen compatible with every deck transformation, rather than with one cyclic subgroup;
- that a finite-cover isotopy avoids every deck translate so as to descend to M;
- that a finite-index insulator family extends to a Gamma-equivariant family with convexity, local finiteness and no trilinking;
- that the geometric hypotheses in Proposition 5.1 hold for the prescribed component.

The exact base-isotopy route would require a simultaneous equivariant isotopy of the entire lift configuration. Separate unknottedness of the lines does not provide it. A sufficient descent statement for a regular finite cover would be an ambient isotopy commuting with the deck group; no such equivariance is supplied here. Simply averaging homeomorphisms is not an operation on isotopies. The side-monodromy cover in Lemma 2.2 is not a substitute for this descent.

Theorem 0.2 of [S5] concerns a shortest geodesic of a closed orientable hyperbolic manifold. It cannot identify this particular prescribed core or its conjugacy class with such a geodesic. Mostow rigidity and existence of a geodesic in a free homotopy class do not identify a knot isotopy class.

An ideal arc joining a rank-two cusp to itself, for a marked free product Z^2 * Z in a one-handle compression body, is a different geometric setting. Its special matrix-word exclusions and Ford-domain hypotheses are absent here. Such an arc argument does not establish the prescribed closed-core conclusion.

## 8. Outcome and next proof obligation

The full target remains unresolved after this first substantive attempt. The strongest conclusions in the closed orientable setting are Proposition 2.3, Theorem 4.2, and the explicitly conditional Proposition 5.1. The main remaining mathematical question is whether the lamination supplies enough global information to force primitivity and an equivariant geometric straightening/insulator construction in the base manifold, or whether a qualifying complementary core realizing one of the obstructions can be constructed.

This attempt does not construct that example and does not prove that equivariant straightening. The [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the stated partial results after examining the boundary-side/strip argument in Lemma 2.2 and the imported Core Lemma, including the completion-map and ambient-isotopy precision repairs. This AI-assisted, unrefereed acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. The original base-manifold problem remains unresolved.

## References

[S1] Danny Calegari, Problems in foliations and laminations of 3-manifolds, arXiv:math/0209081v1 (2002), Definitions 1.3-1.5 p. 2, Question 6.2 pp. 11-12, Question 6.3 Remark (2) p. 12. https://arxiv.org/abs/math/0209081

[S2] David Gabai and William H. Kazez, Order trees and laminations of the plane, Mathematical Research Letters 4 (1997), 603-616. https://doi.org/10.4310/MRL.1997.v4.n4.a14 . Product theorem used as explicitly stated in [S1]; original PDF retrieval blocked, full proof not inspected.

[S3] Louis Funar and Siddhartha Gadgil, Topological geodesics and virtual rigidity, Algebraic & Geometric Topology 1 (2001), 369-380. Definitions 0.1/1.1, Section 2, Lemma 4.2 and Theorem 4.3. https://doi.org/10.2140/agt.2001.1.369 ; https://arxiv.org/abs/math/0106163

[S4] Ian Agol, with an appendix by Ian Agol, Daniel Groves and Jason Manning, The virtual Haken conjecture, Documenta Mathematica 18 (2013), 1045-1087. Corollary 1.3 and Theorem 9.3. https://doi.org/10.4171/DM/421 ; published PDF https://ems.press/content/serial-article-files/26202?nt=1 . The final published numbering and statement, not the earlier arXiv draft, are used.

[S5] David Gabai, G. Robert Meyerhoff and Nathaniel Thurston, Homotopy hyperbolic 3-manifolds are hyperbolic, Annals of Mathematics 157 (2003), 335-431. Theorem 0.2; Appendix Definitions A.1-A.2 and Example A.3, pp. 427-428. https://annals.math.princeton.edu/wp-content/uploads/annals-v157-n2-p01.pdf

[S6] Sergio Fenley, Tali Pinsky and Mario Shannon, Hyperbolicity of complements of orbits in Anosov flows, arXiv:2607.28139v1 (2026), Proposition 7.1 pp. 21-23. https://arxiv.org/abs/2607.28139 . Recent preprint, used only as a literature caution, not a proof dependency or a lamination counterexample.
