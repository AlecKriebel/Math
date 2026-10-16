# Turn 2: two exponential-Laurent inputs and an arbitrary third input

## Theorem and scope

Let R_1,R_2 be nonconstant complex Laurent polynomials, Q_1,Q_2 nonconstant complex polynomials, and g an arbitrary nonconstant entire function. Then the original source property holds for

    f_1(z)=R_1(exp(Q_1(z))),
    f_2(z)=R_2(exp(Q_2(z))),
    f_3(z)=g(z).                                             (1)

Thus every ambient entire F bounded on the full zero hypersurface has one constant value there. There is no growth, finite-order, finite-type or nonvanishing restriction on g. The positions of the two displayed inputs may be permuted.

This is a scoped affirmative theorem. It extends the explicitly checked family of turn 1 to a genuinely arbitrary third input, but still does not settle three arbitrary entire inputs. The base Liouville-covering result, separated-sum irreducibility, finite-cover ideas and Demailly's earlier two-simple-exponential case remain credited prior work. No novelty assertion is made.

By Theorem A of turn 1, it suffices to prove the case Q_1(z)=Q_2(z)=z, with the third precomposition the identity. We prove that case below. The argument explicitly handles fibers with several components and the exceptional fibers where their number might become infinite.

## 1. Generic separated algebraic curves are connected

Regard R_i as a nonconstant rational map from the Riemann sphere to itself, of degree d_i. Let E_i be the finite subset of C consisting of:

- all finite branch values of that rational map;
- R_i(0), if it is finite;
- R_i(infinity), if it is finite.

A value t outside E_i has exactly d_i distinct preimages, all in C*. The map from R_i^{-1}(C minus E_i) to C minus E_i is a connected finite unramified cover: its domain is the sphere with finitely many points removed. Its monodromy action on a fiber is therefore transitive. A degree-one rational map presents no exception: its one-point fiber has the trivial transitive action.

Let c lie outside the finite sumset E_1+E_2. Define

    C_c={(u,v) in (C*)^2:R_1(u)+R_2(v)=c},
    U_c=C minus (E_1 union (c-E_2)).

Over U_c, the projection t=R_1(u)=c-R_2(v) realizes a degree d_1 d_2 covering C_c^0->U_c. The two indicated sets of punctures are disjoint. A small loop about a puncture of E_1 acts trivially on the second root coordinate; a loop about a puncture of c-E_2 acts trivially on the first. Conjugating the small loops by paths to a common basepoint does not change the identity action on the other coordinate. The loops around E_1 generate the full first-coordinate monodromy image, because the additional punctures have trivial first-coordinate monodromy. Likewise the loops around c-E_2 generate the full second-coordinate image. Hence the product monodromy contains the product of two transitive groups and is transitive on the root pairs. Thus C_c^0 is connected.

The curve C_c is smooth: a singular point would have R_1'(u)=R_2'(v)=0, making c a sum of finite branch values. The omitted part C_c minus C_c^0 is finite, since each omitted t has finitely many u and v preimages. Every curve component meets C_c^0: the projection t cannot be constant on a component, since both equations at a fixed t have finite fibers. Therefore C_c is connected. Being smooth and connected, it is irreducible.

## 2. Only finitely many components occur in the exponential lift

Let r_{i,0} denote the coefficient of the constant Laurent term of R_i, and put c_0=r_{1,0}+r_{2,0}. Enlarge the excluded set to

    Sigma=(E_1+E_2) union {c_0}.                              (2)

For c outside Sigma, consider

    X_c={(x,y) in C^2:R_1(exp x)+R_2(exp y)=c}.

This is the pullback of the universal exponential cover C^2->(C*)^2 to the smooth connected algebraic curve C_c. If

    H_c = image[pi_1(C_c)->pi_1((C*)^2)=Z^2],

the number of connected components is [Z^2:H_c], possibly infinite a priori. Each individual component is a regular cover of C_c with abelian deck group H_c. The following argument establishes the required finite, uniform bound:

    1 <= [Z^2:H_c] <= 2 d_1 d_2.                             (3)

Take the smooth compact normalization of a projective closure of C_c. The coordinates u,v are meromorphic functions on it. The degree of u is at most d_2, and the degree of v at most d_1, since a generic fixed u leaves at most d_2 choices of v, and conversely. Consequently, at every boundary point p,

    |ord_p u| <= d_2,    |ord_p v| <= d_1.                    (4)

Small loops about boundary points, lying in C_c, have winding vectors (ord_p u,ord_p v), so all these vectors belong to H_c.

These boundary vectors span a rank-two subgroup. Otherwise an integer pair (a,b)!=(0,0) annihilates all of them, so the meromorphic function u^a v^b has no zeros or poles on the compact normalization. It is constant. Neither a nor b can vanish: either possibility would force one of u,v to be constant, contradicting the finite-fiber projection argument above. The curve would therefore lie in one connected component of the torus coset u^a v^b=k. Such a component is parametrized by

    u=alpha t^r,  v=beta t^s,  t in C*,

with nonzero integers r,s. The separated Laurent identity on a nonempty open part of this coset, hence on the whole coset, implies

    R_1(alpha t^r)+R_2(beta t^s)=c.

Its constant Laurent coefficient is exactly r_{1,0}+r_{2,0}; since r and s are nonzero, no nonconstant Laurent term becomes a constant. Thus c=c_0, a contradiction.

Choose two independent boundary vectors. Their determinant is a nonzero integer with absolute value at most 2 d_1 d_2 by (4). Their generated lattice is a subgroup of H_c, so the latter's index is at most this determinant. This proves (3). It does not claim that boundary loops generate the entire winding lattice or that the upper bound is sharp.

The smooth algebraic curve C_c is quasiprojective and ultra-Liouville. The credited Lin abelian-cover theorem therefore makes every connected component of X_c Liouville. In particular, a bounded entire function restricted to X_c takes at most 2 d_1 d_2 values, one on each component. Components may have the same value; that coincidence will not be used to change their multiplicities.

## 3. Local triviality with component labels

Pointwise finiteness alone does not justify a global symmetric trace for a nonproper family. We now supply the missing local-triviality assertion directly, rather than assuming a properness theorem for X_c.

Fix c_* outside E_1+E_2, and let c=c_*+delta be sufficiently close to c_*. Choose a smooth isotopy h_delta of the Riemann sphere, depending continuously on delta, such that:

- h_delta is the identity near every point of E_1;
- h_delta(t)=t+delta near every point of c_*-E_2;
- h_delta is the identity outside a sufficiently large disc, and fixes infinity.

The two finite sets are disjoint, so disjoint small neighborhoods can be chosen. An explicit construction on C is h_delta(t)=t+chi(t)delta, with a smooth cutoff chi equal to zero on the first neighborhoods, one on the second, and zero off a large disc. For sufficiently small |delta|, its derivative is uniformly close to the identity, so it is a diffeomorphism; equivalently its perturbation has Lipschitz norm less than one, giving global injectivity and surjectivity. The isotopy tau->h_{tau delta} has the same properties.

Define

    k_delta(t)=c-h_delta(c_*-t).

This is also an isotopy from the identity and fixes each point of E_2, indeed a neighborhood of it; it fixes infinity on the sphere. Both h_delta and k_delta fix every branch value of the respective R_i and the images of the distinguished points 0,infinity. The covering homotopy property, applied after removing all branch values, lifts these isotopies uniquely from the identity to isotopies a_delta,b_delta of the source spheres satisfying

    R_1(a_delta(u))=h_delta(R_1(u)),
    R_2(b_delta(v))=k_delta(R_2(v)).                         (5)

They extend across the finitely many removed preimages. To see this last point without a regularity assumption at branch points, use local coordinates in which a finite holomorphic map is z->z^m; a lifted isotopy has the unique continuous extension over the isolated center. The lifts and their inverses give homeomorphisms. They fix 0 and infinity separately: these points have images fixed throughout the isotopy, and a continuous path in their finite fibers is constant. Hence the restrictions a_delta,b_delta are isotopies of C*.

For (u,v) in C_{c_*}, equations (5) give

    R_1(a_delta(u))+R_2(b_delta(v))
       =h_delta(R_1(u))+c-h_delta(c_*-R_2(v))=c.

Thus (a_delta,b_delta) identifies C_{c_*} with C_c. Their isotopies on C* lift through exp:C->C*, again starting with the identity, and yield homeomorphisms identifying X_{c_*} with X_c continuously in c. This is a local topological trivialization of the family of exponential curves.

In particular the number q of components is locally constant on C minus Sigma, and thus is one fixed integer there, since that punctured plane is connected. By (3), 1<=q<=2 d_1 d_2. Locally every component has a continuous label. We shall combine these labels with holomorphic local sections; the trivialization itself need not be holomorphic.

## 4. Bounded symmetric coefficients in the arbitrary third variable

Let V={(x,y,w):R_1(exp x)+R_2(exp y)+g(w)=0}, and let F be ambient entire with |F|<=M on V. Put

    B=C minus g^{-1}(-Sigma).

The removed set is locally finite and discrete, because g is nonconstant entire and Sigma is finite. Hence B is a nonempty connected open dense subset of C. Over every w in B the fiber X_{-g(w)} has exactly q Liouville components. The restriction of F to each is constant.

Near any w_* in B, choose a point on each of the q components. The fiber is smooth, so at such a point at least one of the x,y derivatives of R_1(exp x)+R_2(exp y) is nonzero. The holomorphic implicit function theorem gives a local holomorphic section through that point over w. Compose F with each section to obtain q holomorphic functions eta_1(w),...,eta_q(w). The local triviality of Section 3 ensures that these sections represent every fiber component exactly once after the neighborhood is made smaller. Because F is constant on each component, these are precisely its component values with component multiplicity.

Define

    A(w,T)=product_{j=1}^q (T-eta_j(w)).                    (6)

Changing labels permutes the factors, and different section choices on the same component do not change its constant value. Thus the coefficients of (6) glue to globally defined holomorphic functions a_k on B. The bound on F implies

    |a_k(w)| <= binomial(q,k) M^k.

Each coefficient has removable singularities at every point of g^{-1}(-Sigma), and hence extends to a bounded entire function on C. One-variable Liouville makes every coefficient constant. It follows that F on the portion of V over B takes values in the finite root set of one fixed monic degree-q polynomial A(T).

That portion is dense in V, including all exceptional fibers. Indeed, at any (x_0,y_0,w_0) in V and for a sequence w_n in B tending to w_0, the local openness of the nonconstant holomorphic function x->R_1(exp x) gives solutions x_n->x_0 of

    R_1(exp x_n)=-R_2(exp y_0)-g(w_n).

One may choose them by Rouche's theorem in successively smaller discs about x_0; no nonvanishing derivative at x_0 is required. Thus A(F)=0 everywhere on V by continuity. The Rubel–Squires–Taylor irreducibility theorem applies to the three nonconstant entire inputs defining V, so V is connected. Its finite continuous image F(V) has one point. This proves the basic case and, by the finite-pullback equivalence, (1).

## 5. Quantifiers, credit and remaining gap

All finite exceptional sets concern the two Laurent rational maps. The third entire function may have infinitely many critical or asymptotic values, and their behavior is not assumed controlled. Its preimage of the finite exceptional set is handled by bounded removable singularities. Exceptional slices may have infinitely many components; the final density argument still covers every one of their points.

The two-exponential special case R_i(w)=w is already included in Demailly's Corollary 2 and is not a new claimed discovery. The finite-component/winding and isotopy arguments above verify the broader Laurent-polynomial case using the credited abelian-cover theorem. Polynomial phases are an application of the proved turn-1 equivalence. No assertion is made about historical novelty of this broader corollary.

The unresolved source still permits all three inputs to lie outside these families. The arguments require finite branching data for at least two rational torus maps; arbitrary transcendental phases or arbitrary entire input maps need not supply it. This is the precise scope of the positive result at author turn 2/5.

The exact checker tests lattice-index and determinant bounds, component-value symmetric identities and finite product-monodromy controls. It does not numerically prove a covering theorem, the source irreducibility input or the generic-curve argument.
