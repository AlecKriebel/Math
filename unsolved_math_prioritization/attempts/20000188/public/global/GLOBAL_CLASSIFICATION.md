# Global classification for the fixed complex two-camera residual

Authored in shared pass 1, 2026-10-16. This proves statements for the adopted residual only. The use of epipolar fiber products is a prior method, not a novelty claim. This note does not claim a literature-complete theorem or settle other interpretations of AIM Reconstruction Problem 1.4.

## 1. Normal form and terminology

Let both cameras have rank three and distinct centers. A projective change of world coordinates, followed by independent projective changes of image coordinates, puts them in the form

- p1([x0:x1:x2:x3])=[x1:x2:x3], with center c1=[1:0:0:0];
- p2([x0:x1:x2:x3])=[x0:x2:x3], with center c2=[0:1:0:0].

To prove this, choose the first two basis vectors on the respective distinct kernel lines. Choose a complementary two-dimensional vector space. In each image, the images of the other kernel vector and those two complement vectors form a basis. Rescaling the image bases gives the displayed form. In both images the epipole is e_i=[1:0:0]. The baseline is B=V(x2,x3). An epipolar plane is H_t={v x2-u x3=0}, for t=[u:v] in P1. Its two image lines are ell_i(t), both having equation v b-u c=0 in the respective image coordinates [a:b:c].

Let the prescribed image curves C_i be reduced integral plane curves of degrees d_i, defined by irreducible homogeneous forms f_i(a,b,c). Their inverse-image cones are the integral hypersurfaces

S1=V(F1), F1=f1(x1,x2,x3), and S2=V(F2), F2=f2(x0,x2,x3).

A valid world curve is a reduced integral closed curve C in P3 whose two rational projections are defined generically and have image closures C_i.

## 2. The exhaustive case split

### Theorem 2.1

Exactly one of the following holds.

(A) Both C_i are corresponding epipolar lines ell_i(t), for the same t. Then every valid world curve is an integral curve in H_t other than a line through c1 or c2; conversely every such integral curve is valid. Thus there are positive-dimensional families of candidates and unbounded degrees. The detailed degree spectrum is treated in the exceptional-case note.

(B) At least one C_i is an epipolar line, but case (A) does not hold. There are no valid world curves.

(C) Neither C_i is an epipolar line. Then S1 and S2 meet properly in a complete-intersection curve X. There is at least one valid world curve. The valid world curves are exactly the reduced supports of all irreducible components of X other than B. There are finitely many. Every nonbaseline component has scheme multiplicity one in X. B occurs as a support component exactly when both e_i lie on C_i, and may have multiplicity greater than m_e1(C1)m_e2(C2).

### Proof

If C1 is ell_1(t), any valid world curve lies in H_t. The second camera maps H_t\{c2} onto ell_2(t). Its restriction to an integral curve either has point image or dense image in that line. The demanded image is a curve, hence C2=ell_2(t). This proves (B), and symmetrically the same assertion starting with C2. Within H_t, a curve is contracted by p_i precisely when it is a line through c_i: every fiber of the projection is a line through its center. An integral curve contained in such a line equals that line. This proves (A), including both directions.

The two cone hypersurfaces can share a surface component only if they are equal, because each is integral. Equality forces their defining irreducible polynomials to be scalar multiples, and hence independent of both x0 and x1. A homogeneous binary polynomial irreducible over C is linear. Thus equality holds exactly for the corresponding-epipolar-line pair in (A). In case (C), their intersection is therefore a proper complete intersection and has pure dimension one (indeed its coordinate ring is Cohen–Macaulay). Every valid curve is a one-dimensional irreducible closed subset of X, hence a component support.

Suppose a component support D is contracted by p1. It is a line through c1. If it is not B, its second-camera image is an epipolar line. Since D lies on S2, that line lies in C2, forcing C2 to be that epipolar line, contrary to (C). The same argument applies to p2. Thus every component other than B maps dominantly to both prescribed integral curves and is valid. B itself maps to the two epipoles, so is never valid. Its inclusion in both cones is exactly the condition e_i in C_i.

Existence and multiplicity-one for the other components follow also from the fiber-product construction in Section 3. Both epipolar maps there are nonconstant finite maps onto P1. Their fiber product is nonempty and its generic fiber is reduced, because the field has characteristic zero. Its generic points triangulate to points outside B, giving at least one valid component. Off B and away from centers and exceptional image values, the complete intersection is identified with that fiber product. After removing the finite branch loci of the two epipolar maps and finite image singularities, this is étale over an open subset of P1. Hence every genuine component is generically reduced, proving its scheme multiplicity is one. QED.

## 3. A finite parametrizing correspondence

Assume case (C). Let nu_i:Gamma_i -> C_i be the normalization. The epipolar pencil [b:c] extends uniquely to a morphism

h_i:Gamma_i -> P1.

It is nonconstant because C_i is not an epipolar line. Write A_i=nu_i^*O_Ci(1). Let E_i be the common zero divisor of the two pulled-back sections b,c; it is supported exactly on the branches over e_i. At a branch over e_i, its coefficient is the branch multiplicity, namely the minimum order of the two affine coordinates b/a,c/a. Consequently

m_i:=deg E_i=mult_ei(C_i), with m_i=0 if e_i is absent;

delta_i:=deg h_i=d_i-m_i>0, and A_i= h_i^*O_P1(1)(E_i).

These identities follow by removing the base divisor E_i from the pencil. The equality between the sum of branch multiplicities and point multiplicity follows by intersecting with a general line through e_i.

Form the finite fiber product Y=Gamma_1 x_{P1} Gamma_2. It is reduced: each Gamma_i is finite flat over the nonsingular base P1; thus Y is finite flat, hence torsion-free over the base, and its generic algebra is a tensor product of finite separable extensions, hence reduced. Any nilpotent would vanish generically and be base-torsion, impossible. Let T range over the connected integral components of the normalization of Y. Every such T is a smooth projective integral curve. Write g_i:T->Gamma_i, t:T->P1, r_i=deg g_i, and k=deg t. Then

k=r1 delta1=r2 delta2.

Every irreducible component of Y dominates P1, since Y is finite flat and its component generic points cannot be supported in fibers. The r_i are therefore positive.

### Theorem 3.1

The components T correspond bijectively to the valid world curves. Each T is canonically their normalization under the triangulation map below.

### Proof

For generic q_i=[a_i:b_i:c_i] with q_i != e_i and h1(q1)=h2(q2), the two viewing lines are distinct lines in the same epipolar plane. Their unique intersection is a world point off B. Indeed, the first viewing line contains c1 but not c2, the second contains c2 but not c1, so their intersection is neither center and is not another baseline point. Conversely, any world point off B determines its image pair and common epipolar plane. Away from finitely many image singularities, the pair determines unique points of Gamma_i. Thus generic triangulation and generic projection are inverse rational maps between Y and the genuine part of X. This proves a bijection of components and birationality on each one. The rational map from smooth projective T to projective P3 extends everywhere; its image is the corresponding integral world curve. Being nonconstant and birational, it is the normalization map. QED.

This is a computable classification, not an existence assertion about an unknown world curve: Gamma_i, their finite maps, the fiber product, its factorization, and its normalizations are computed from the two prescribed image equations alone. One can instead use the substantially simpler support decomposition of the explicit ideal (F1,F2), as in Section 7.

## 4. Triangulation, epipole cancellation, and exact degrees

On a fixed T put M=t^*O_P1(1), D_i=g_i^*E_i. Let s_i be the canonical section of O_T(D_i). Let u,v be the two pulled-back homogeneous coordinates of P1, which have no common zero. The two image morphisms can be written

q_i=[a_i:s_i u:s_i v], with a_i a section of M(D_i).

Here g_i^*A_i=M(D_i). The formula represents isomorphisms of line bundles; no globally chosen scalar functions are required.

The triangulation map is represented before cancellation by

[x0:x1:x2:x3]=[a2 s1:a1 s2:s1 s2 u:s1 s2 v].

All four sections lie in L=M(D1+D2). Let alpha_p=ord_p(D1), beta_p=ord_p(D2). Their exact common zero divisor is

Z=min(D1,D2), with coefficient min(alpha_p,beta_p).

Indeed if alpha_p>0 then q1(p)=e1 so a1(p) is nonzero in a local frame, and similarly for beta_p>0. When both vanish, the first two coordinate orders are alpha_p,beta_p and the minimum of the final two is alpha_p+beta_p. When only one is positive, the corresponding opposite first coordinate does not vanish. When neither is positive, one of the last two coordinates does not vanish. These cases prove the assertion and rule out any hidden base point.

Cancel Z. The resulting base-point-free sections of L(-Z) define the normalization map phi_T. Since it is birational onto its image C_T,

D:=deg C_T=deg L(-Z)
 =r1 d1+r2 d2-k-deg min(D1,D2)
 =k+deg max(D1,D2).

This includes singular images, epipoles, ramification and arbitrary coincidences of branch directions. The generic degrees of the two camera projections are exactly r1,r2.

### Center and baseline behavior, point by point

- If alpha=beta=0, the world point is outside B.
- If alpha<beta, the world point is c1, and that world branch has point multiplicity beta-alpha.
- If alpha>beta, the world point is c2, and that world branch has point multiplicity alpha-beta.
- If alpha=beta>0, the world point is an interior point of B, determined by the ratio of the nonzero leading terms a2 s1 and a1 s2 after cancellation. Both x0 and x1 are nonzero.

For example, in the alpha<beta case, after dividing the coordinates by a2 s1, the minimum order among x1/x0,x2/x0,x3/x0 is beta-alpha. If alpha>0, a1 is a unit. If alpha=0, a1 might vanish, but one of u,v is a unit, so the minimum remains beta. The other center is symmetric.

Adding branch multiplicities yields the exact center formulas

mult_c1(C_T)=deg(D2-min(D1,D2));
mult_c2(C_T)=deg(D1-min(D1,D2)).

In particular,

D=r1 d1+mult_c1(C_T)=r2 d2+mult_c2(C_T).

The pullback of the baseline ideal (x2,x3) has zero divisor max(D1,D2), including at centers. Thus the degree formula may also be read as D=k+deg(phi_T^{-1} I_B). This is a pullback-ideal divisor, not a claim that the singular curve’s scheme-theoretic intersection length with B is always the same quantity.

## 5. Scheme multiplicity of the baseline

Let mu_B denote the baseline's coefficient in the fundamental one-cycle of X, and set it to zero when B is absent. Because the genuine components each have coefficient one, Bezout gives

d1 d2=sum_T deg C_T + mu_B.

Moreover sum_T k=delta1 delta2, sum_T r1=delta2, and sum_T r2=delta1. Substituting the exact degree formula proves

mu_B=m1 m2+sum_T deg min(D1,D2).

There is also a directly computable local branch form. For every pair of branches gamma_i of C_i at e_i having the same extended epipolar value, let n_i be their branch multiplicities and let a,b be the ramification indices of h1,h2 at those branch points. Their contribution to the final sum is

min(n1 b,n2 a).

Indeed, in complex analytic uniformizers the local fiber product has equation z^a=w^b after absorbing nonzero units into the local coordinates. It has g=gcd(a,b) normalized branches. On each, the pullback orders of E1,E2 are n1 b/g,n2 a/g. Summing their minima over the g branches proves the formula. Distinct epipolar values give no contribution. This also proves that the baseline coefficient is determined by image-epipole branch multiplicities and their epipolar ramification indices, without constructing the whole global fiber product.

### Required adversarial example

Take f1=a c-b^2 and f2=a c-b^2. In world coordinates the cones are

F1=x1 x3-x2^2, F2=x0 x3-x2^2.

Both image epipole multiplicities are one. Each h_i has degree one and at the epipole has ramification index one. The fiber product has one component, k=1, with alpha=beta=1. The true world curve is the smooth plane conic x0=x1, x1 x3=x2^2, of degree 2. The two cones have degree product 4, and mu_B=1+1=2. At the generic baseline point x0-x1 is a unit, so the local complete-intersection ideal is (x3,x2^2), verifying length two directly. Subtracting only m1 m2 would be wrong.

### A singular-image / smooth-world check

Take f1=b^3-a c^2 (a cuspidal cubic at e1) and f2=a c-b^2. The genuine component is the smooth twisted cubic

[x0:x1:x2:x3]=[s^2 t:s^3:s t^2:t^3].

Here d1=3,m1=2,d2=2,m2=1,delta1=delta2=k=r1=r2=1. At t=0 the pulled-back epipole orders are alpha=2,beta=1, so the world point is c2 with point multiplicity one. The formulas give world degree 1+2=3, center multiplicities (0,1), and baseline coefficient 2*1+1=3. The degree budget is 6=3+3. This is a check that a singular prescribed image need not force a singular world curve: its singularity can arise from projection through a center.

## 6. Blowup and exceptional geometry

Let W=Bl_{c1,c2} P3. The centers are disjoint; their blowups resolve both camera projections and give a morphism

q:W -> V={b1 c2-c1 b2=0} subset P2 x P2.

Here the symbols b_i,c_i are image coordinates, not camera-center points. This V is the epipolar incidence threefold. It is nonsingular away from the single pair (e1,e2), where its local equation is the ordinary determinantal node b1 c2-c1 b2=0. The morphism q is an isomorphism off that pair and its fiber over that pair is the strict transform of the baseline, a P1. The exceptional divisor of the blowup at c1 maps isomorphically onto P2 x {e2}; that at c2 maps isomorphically onto {e1} x P2. Their baseline-direction points lie on the contracted strict transform of B.

These assertions can be checked in the viewing-ray incidence model: W is the closure of the graph of (p1,p2), since the two disjoint center ideals resolve independently. A pair different from (e1,e2) specifies a unique graph point. If both image coordinates are nonepipolar, triangulation gives its world point. If q1=e1 but q2!=e2, its world point is c2 and q2 specifies the exceptional direction; the other case is symmetric. For (e1,e2), every point of the baseline, including its two resolved endpoint directions, gives the full P1 fiber. The local graph equations are the familiar two charts of a small resolution of the displayed node.

There is a second resolution of V obtained by retaining the epipolar-plane parameter:

Vplus={(q1,q2,t): q_i in ell_i(t)}.

It is a P1 x P1 bundle over P1 and its exceptional fiber over (e1,e2) is the P1 of epipolar planes. On nonepipolar pairs the resolutions agree; they differ precisely at the node. Normalizing the curve fiber product and cancelling the common divisor in Section 4 resolves its lift through this birational correspondence. The equal-order/unequal-order rule is essential: merely pairing points over the image epipoles loses the limiting baseline point or center.

The exceptional loci that can supply additional component supports in relevant inverse images are listed below. In the common-plane case some of these curves are contained in the surface component rather than being separate components:

1. The baseline B in the world complete intersection, occurring exactly when both image epipoles are present. It is invalid and may be nonreduced in that intersection.
2. A viewing-ray line contracted by one camera and mapped by the other to an epipolar line. These can occur only in cases involving an epipolar-line image. In case (B) they provide no valid reconstruction.
3. Curves contained in the exceptional divisor over c1 or c2 in the full resolved inverse image q^{-1}(C1 x C2). When e2 in C2, E1 contains the copy of C1; when e1 in C1, E2 contains the copy of C2. These map to a center in world space and are invalid as world curves. They are artifacts of taking the whole inverse image rather than the strict transforms of genuine curves.
4. In the corresponding-line case, a common epipolar plane, a two-dimensional component rather than a finite list of curves. Its integral subcurves are classified in (A).

No additional contracted world-curve component is possible: a one-dimensional fiber of a pinhole camera is a line through that center, and the preceding viewing-ray argument is exhaustive.

Important distinction: the full inverse image of C1 x C2 in W can contain vertical exceptional curves and additional scheme structure. It should not be equated with the disjoint union of the T. The T parametrize only the genuine curve components and come with a morphism to W by the valuative criterion for its proper graph morphism. Their world maps may meet one another at centers or on B.

## 7. A concrete exact-input decision algorithm

The geometric assertions hold over C. Literal algorithmic computability additionally requires exact coefficient input in an effective characteristic-zero field supporting the relevant operations over its algebraic closure, including absolute geometric prime decomposition, for example algebraic-number coefficients handled in Qbar. Unrepresented arbitrary complex constants are not finite algorithmic input.

Given exact matrices and two irreducible homogeneous plane-curve equations:

1. Compute their distinct camera centers and put the cameras in the normal form by linear algebra.
2. Test whether either image equation defines an epipolar line. Apply Theorem 2.1(A)/(B) before invoking a finite-component algorithm.
3. Otherwise form the explicit ideal I=(f1(x1,x2,x3),f2(x0,x2,x3)). Compute its homogeneous radical and its absolute minimal homogeneous prime ideals (geometric components over the algebraic closure, not merely primes over a smaller coefficient field). Drop the baseline prime (x2,x3), if present. The remaining prime ideals are exactly, and exhaustively, the valid world curves.
4. For each prime, obtain its degree from its Hilbert polynomial. Compute the generic projection degrees by eliminating coordinates or by the induced function-field extension. Equivalently normalize the image curves and compute the finite fiber-product factors to obtain r_i and use Section 4's formula. Thus a prescribed (world degree, first projection degree, second projection degree) is feasible if and only if it occurs on this explicit finite list.
5. Test embedded smoothness of each computed prime curve by the projective Jacobian criterion or normalization-map criteria developed in the local-smoothness note. No unknown lift is quantified over: all candidate ideals are already explicit and finite. The corresponding-line family has its separate complete criterion.
6. If multiplicities of the cone intersection are requested, localize I at the baseline prime and compute its length, or use the exact formula in Section 5. Genuine component coefficients are one.

Groebner basis, radical/prime-decomposition, normalization, Hilbert-polynomial, and zero-dimensional emptiness procedures furnish standard terminating algebraic algorithms for these operations in the exact-input model. A finite test of the explicit singular scheme of an explicitly computed candidate is a decision criterion, unlike a restatement that an unspecified smooth lift should exist.

## Scope and acceptance obligations

This note independently proves the global case split, component bijection, epipolar/center degree corrections, baseline coefficient, and finite candidate algorithm. The embedded-smoothness proof and corresponding-line degree/smoothness spectrum belong to the complementary notes and must be combined before claiming the adopted residual complete. The independent acceptance is recorded in ../audit/INDEPENDENT_AUDIT.md. No statement here establishes novelty or the status of the unquantified original AIM problem.
