# A smooth-boundary candidate proof of dihedral comparison in dimension three

Target: 30003471 / OWR-15427-013. Prepared 2026-10-08.
Status: complete author candidate, awaiting independent mathematical audit. No claim of novelty, journal acceptance, formal verification, or community acceptance is made.

## 1. Precise claim

Let P and Q be compact, full-dimensional convex polytopes in Euclidean three-space. Fix an isomorphism of their face lattices and label corresponding facets F_i and G_i. Write n_i and m_i for their outward unit normals. If every pair of adjacent facets satisfies

    theta_P(i,j) <= theta_Q(i,j),

where theta denotes the interior dihedral angle, then

    n_i dot n_j = m_i dot m_j  for every i,j.

In particular all corresponding dihedral angles agree. This stronger statement implies the exact OWR question: if theta_P(e)>theta_Q(e) for every corresponding edge, apply the theorem with P and Q interchanged to obtain a contradiction. Consequently at least one corresponding edge satisfies theta_P(e)<=theta_Q(e). Equal angles are already included; the extra equality alternative in the OWR wording is redundant.

No simplicity, equal edge lengths, prescribed face metrics, smooth corner equivalence, or angle bound below pi/2 is assumed. Every actual facet is used once. The dimensions and compactness exclude flat or unbounded degeneracies.

The construction below adapts the smooth-approximation and logarithmic-cutoff method of Yuchen Bi, arXiv:2608.06320v1, to *two differently realized polytopes*. Its key extra ingredient is a globally compatible, degree-one auxiliary map constructed from the fixed combinatorial correspondence. We do not pull back Q's metric to P. The only specialized analytic result imported as a black box is the published smooth-boundary Dirac result specified next. The new WXY three-dimensional preprint is relevant prior literature, but is not a dependency of this argument.

## 2. Precisely imported smooth-domain result

We use Simon Brendle, *Scalar curvature rigidity of convex polytopes*, Inventiones Mathematicae 235 (2024), 669-708, DOI 10.1007/s00222-023-01229-x; inspected author manuscript arXiv:2301.05087v4, Section 2, especially Propositions 2.9, 2.14 and 2.15 (printed pp.8-12), with Definitions 2.2 and 2.7 and Lemma 2.8.

Here is its needed specialization. If Omega is a compact convex domain in R^3 with C-infinity boundary Sigma, and eta:Sigma->S^2 is smooth and homotopic to the outward Euclidean Gauss map, there is a nonzero smooth 2-by-2 complex matrix field A on Omega such that

    D A = 0,
    c(nu) A = A c(eta) on Sigma,
    integral_Omega |grad A|^2
       <= (1/2) integral_Sigma (||d eta||_tr-H)_+ |A|^2.       (2.1)

The Euclidean metric is defined on a neighborhood; nu is the outward unit normal; H is the sum of the principal curvatures, positive on a round sphere; trace norm is the sum of the two singular values. Norms of matrices are Hilbert-Schmidt norms. The Dirac operator acts on the columns. Choose one irreducible complex Clifford representation c on C^2 for both copies of R^3, with c(v)c(w)+c(w)c(v)=-2(v dot w)I. For example c(e_j)=-i sigma_j using the Pauli matrices.

For clarity about the translation: the boundary involution is chi_eta(A)=-c(nu) A c(eta). Thus chi_eta A=A is exactly the boundary relation in (2.1). Proposition 2.15 gives positive index, hence nonzero kernel; Proposition 2.14 makes its kernel smooth. Proposition 2.9, with D A=0 and scalar curvature zero, gives (2.1). Brendle's *separate polytope theorem* has a matching-angle hypothesis, which is not a hypothesis of these smooth-domain propositions. No index theorem on a singular polyhedral boundary is being imported.

Other imported foundations are standard: smooth approximation of continuous maps on a compact collar, the Sobolev trace H^1->L^4 for a bounded Lipschitz domain in R^3, bounded H^1 extension for such domains, Rellich compactness, and homotopy classification of maps S^2->S^2 by degree. These are invoked below with their exact domains and uniformity explained.

## 3. A compatible degree-one map for the target normals

Translate both polytopes so that chosen interior points are the origin. Write

    P = intersection_i {u_i(x)=n_i dot x-h_i <= 0},  h_i>0,
    Q = intersection_i {m_i dot y-k_i <= 0},          k_i>0.

A face-lattice isomorphism gives a piecewise-linear boundary homeomorphism f:boundary P->boundary Q: barycentrically subdivide every proper face, put an interior point in every nonempty face, and send each simplex associated with a nested chain of faces affinely to its corresponding simplex. The constructions agree on shared subfaces. Both subdivisions are triangulations, so this is a homeomorphism taking each closed F_i onto G_i. In particular it is bi-Lipschitz. If its degree is -1, first reflect Q by a Euclidean reflection. All relevant angles and Gram matrices are unchanged, and the resulting boundary map has degree +1.

For x on boundary P set

    q_0(x) = f(x)/|f(x)|.

The radial projection of boundary Q onto S^2 is an orientation-preserving homeomorphism, hence deg q_0=1. If x belongs to F_i, then

    q_0(x) dot m_i = k_i/|f(x)| >= c_0,
    c_0 = min_i k_i / max_{y in Q}|y| > 0.                    (3.1)

This holds simultaneously for *all* facets at a nonsimple vertex. Extend q_0 to a fixed collar U of boundary P by composing with radial projection from the origin onto boundary P. This extension is continuous, indeed Lipschitz, because P contains a ball about the origin. Smoothly approximate this R^3-valued extension uniformly on a slightly smaller compact collar and normalize. Taking the approximation sufficiently close to q_0 gives a smooth map q:U->S^2, homotopic to q_0 on this collar, and a fixed epsilon>0, c>0 such that

    q(x) dot m_i >= c
    whenever x in U and dist(x,F_i)<epsilon.                (3.2)

To justify the uniform neighborhood: (3.1) has the same strictly positive margin on each compact F_i; continuity gives a neighborhood for each, and there are finitely many facets. Choose the approximation error less than a quarter of that margin. Its vector norm stays bounded away from zero, and normalization preserves a positive margin. The normalized straight-line interpolation supplies the homotopy. All derivatives of the fixed q are bounded on a compact subcollar. This step makes no differentiability claim about f at a vertex.

## 4. Smooth convex inner approximations of P

Choose a smooth convex Phi:R->[0,infinity) satisfying Phi=0 on (-infinity,-2], Phi'>0 on (-2,infinity), Phi''>=0, and Phi(0)=1. Such a function can be obtained by twice integrating the function exp(-1/(s+2)) for s>-2, extended by zero, then normalizing. Put

    F_lambda(x) = sum_i Phi(lambda u_i(x)),
    P_lambda = {F_lambda <= 1},  Sigma_lambda = boundary P_lambda,
    I_lambda(x) = {i: u_i(x)>-2/lambda}.

For large lambda, P_lambda is a compact convex domain with smooth boundary, contained in P, containing a fixed ball centered at zero. Indeed if any u_i>0 then Phi(lambda u_i)>1. For an active facet and x in P,

    n_i dot x = u_i(x)+h_i >= h_i-2/lambda >= (min h_i)/2.

Consequently any nonnegative combination of the active n_i has norm at least a positive constant times the sum of its coefficients, uniformly for x in P. On F_lambda=1, the sum of the active Phi' values is bounded below: the finite vector of cutoff arguments can be restricted to [-2,0], with their Phi-values summing to one, a compact set on which that sum never vanishes. Therefore |grad F_lambda|>=c lambda. The implicit-function theorem proves smoothness, including flat facet patches.

For y in boundary P, moving y towards zero by C/lambda makes all u_i at most -2/lambda for fixed sufficiently large C. Thus the radial map

    Pi_lambda:boundary P -> Sigma_lambda

moves every point by at most C/lambda. Radially extend it by

    T_lambda(t y)=t Pi_lambda(y), 0<=t<=1.

These maps and inverses have uniformly bounded Lipschitz constants. One proof uses the radial functions of convex bodies lying between the same two concentric balls. Their reciprocals are restrictions of support functions of the polar bodies, hence have a uniform Lipschitz bound and uniform positive lower bound. The displayed radial extensions consequently are uniformly bi-Lipschitz. We have

    sup_{x in P}|T_lambda(x)-x| <= C/lambda.                 (4.1)

It follows, by transport of the trace inequality on the fixed Lipschitz polytope P, that

    ||a||_{L^4(Sigma_lambda)}^2
       <= C (||grad a||_{L^2(P_lambda)}^2
                    + ||a||_{L^2(P_lambda)}^2)             (4.2)

with C independent of lambda. The same transport, followed by a fixed extension from P, gives uniformly bounded H^1 extensions from P_lambda to a fixed ball containing P. For precision one may extend the radial bi-Lipschitz maps to all of R^3 by the same raywise formula; they remain uniformly bi-Lipschitz. Compose the fixed-domain extension with their inverses. Surface measure changes under the boundary maps are bounded above and below uniformly by the area formula. Equation (4.2) also applies to matrix fields, componentwise or to their norm.

We also need active-facet localization. For any set J of facets with nonempty intersection F_J, the finite system of affine inequalities defining F_J gives

    dist(x,F_J) <= C_J max_{j in J}|u_j(x)|,  x in P.       (4.3)

Here is a direct justification rather than an appeal to closeness of planes. If y is the closest point in F_J and v=x-y, then v belongs to the normal cone of F_J at y. At a fixed face type this cone is the sum of the span of equality normals n_j, j in J, and the nonnegative cone of the remaining active constraint normals. If no positive constant bounds max_{j in J}|n_j dot v| below by |v| for these v satisfying the remaining feasible inequalities, take a limiting unit vector w in that cone, annihilating the equality normals and satisfying n_l dot w<=0 for the other active constraints. Pair its cone representation with w to get 1=|w|^2<=0, a contradiction. There are finitely many face types, so the constants are uniform.

If an intersection F_J is empty, compactness of P gives a positive lower bound for max_{j in J}|u_j| on P. Thus, for large lambda, the active set has nonempty common intersection, and (4.3) applies. A ridge of a three-dimensional convex polytope lies in exactly two facets: a transverse planar section is a convex wedge with two bounding rays. Therefore any common intersection of at least three distinct facets is a vertex. Let V be the finite vertex set. We obtain

    |I_lambda(x)|>=3 => dist(x,V)<=C/lambda.               (4.4)

Also every active i satisfies dist(x,F_i)<=C/lambda, ensuring (3.2) on Sigma_lambda.

## 5. Exact edge contraction, with compatible gluing

At a point of Sigma_lambda outside the vertex neighborhoods in (4.4), the active set has one or two indices. With one index i, the surface lies in the facet plane, its normal is n_i, and set zeta_lambda=m_i.

With two indices i,j the facets are adjacent. Otherwise their intersection is either empty or a vertex, already excluded by the same localization. Let

    alpha_ij=arccos(n_i dot n_j)=pi-theta_P(i,j),
    beta_ij =arccos(m_i dot m_j)=pi-theta_Q(i,j).

Both belong to (0,pi), and the comparison hypothesis gives beta_ij<=alpha_ij. The source normal is

    nu_lambda = [Phi'(lambda u_i)n_i+Phi'(lambda u_j)n_j]
                  / |Phi'(lambda u_i)n_i+Phi'(lambda u_j)n_j|.

It belongs to the minor great-circle arc from n_i to n_j. Let s in [0,1] be its fractional arclength along this arc. Define zeta_lambda as the point at fractional arclength s along the minor arc from m_i to m_j.

The second fundamental form of Sigma_lambda in this two-active region is positive semidefinite of rank at most one: its Hessian formula is a nonnegative combination of n_i tensor n_i and n_j tensor n_j restricted to the tangent plane, and the edge direction orthogonal to both normals is in its kernel. Hence

    ||d nu_lambda||_tr = H_lambda,
    ||d zeta_lambda||_tr
           = (beta_ij/alpha_ij) H_lambda <= H_lambda.       (5.1)

This equality includes zero curvature points. It follows either by differentiating the arc parameter, |d nu|=alpha|ds| and |d zeta|=beta|ds|, or by the one nonzero singular value. In the one-active region both sides of (5.1) vanish.

The construction is independent of the order i,j. It is smooth across transitions from two active indices to one: the vanishing cutoff derivative is flat at -2, and the arc coordinate is a smooth local angle coordinate near either endpoint. A formula using atan2 in a fixed oriented basis of span(n_i,n_j) verifies this without differentiating arccos at 1. Two different pair charts can only overlap in a one-active region or meet a three-active region; the former give the same constant value with the same derivatives, and the latter will be removed. Thus zeta is one well-defined smooth map off the C/lambda vertex neighborhoods.

By (3.2), q has positive inner product with both target endpoints. Minor-arc interpolation is a positive sine-weighted sum of these endpoints, and the sum of the weights is at least one. Therefore

    q(x) dot zeta_lambda(x) >= c>0.                        (5.2)

The constant is uniform in lambda, in edges and in their endpoint limits. This is the hemisphere condition needed for the next step; an arbitrary sphere-valued contraction would not suffice.

## 6. Vertex cutoff and its exact boundary norm

Let delta=lambda^(-1/4). For large lambda the balls of radius 2delta about distinct vertices are disjoint. In such a ball write r=|x-v|. Choose a smooth cutoff t_lambda(r) which equals zero for r<=delta^2 and one for r>=delta, takes values in [0,1], and has

    |t_lambda'(r)| <= C/[r |log delta|]
          on delta^2<r<delta.                              (6.1)

For example apply a fixed smooth step function, flat at 0 and 1, to log(r/delta^2)/|log delta|. Because delta^2=lambda^(-1/2) is much larger than C/lambda, zeta is defined throughout each transition annulus. Define eta_lambda on Sigma_lambda to be q inside r<=delta^2, zeta outside all r<delta balls, and in an annulus the spherical geodesic interpolation

    eta_lambda = G(q,zeta,t),
    G(q,z,t) = exp_q(t log_q z).

Equation (5.2) keeps dist(q,z) uniformly below pi/2. Thus this formula and its derivatives are nonsingular. The flat cutoff and the smooth gluing from Section 5 show that eta is globally smooth, including every edge/face transition and both annular boundaries.

For fixed q, spherical polar coordinates give singular values t and sin(t theta)/sin(theta) for the derivative of z->G(q,z,t), where theta=dist(q,z). Both are at most one on 0<=theta<pi/2. The derivative with respect to q is uniformly bounded on our compact parameter range; the t derivative has length theta<=pi/2. The trace-norm triangle inequality therefore gives on a transition annulus

    ||d eta||_tr <= ||d zeta||_tr + C + C/[r |log delta|].

Outside r<delta, eta=zeta exactly, so (5.1) gives no error. Inside r<=delta^2, eta=q, whose derivative is uniformly bounded, and H_lambda>=0 by convexity. Consequently the nonnegative error

    W_lambda=(||d eta_lambda||_tr-H_lambda)_+

satisfies

    W_lambda <= C sum_{v in V} [1_{r_v<delta}
                + 1_{delta^2<r_v<delta}/(r_v |log delta|)]. (6.2)

Crucially, this error is small in L^2 of the *actual smoothed boundary*, not only pointwise away from vertices. Pull back by Pi_lambda. By (4.1), |Pi_lambda(y)-y|<=C/lambda=o(delta^2). Thus the annular weight pulls back to at most a fixed multiple of

    1_{c delta^2<|y-v|<C delta}/(|y-v| |log delta|),

and its support remains near v. Only facets containing v occur for sufficiently small delta. In the plane of any such facet, polar integration about v gives

    integral_{c delta^2<|y-v|<C delta}
          [1/(|y-v| |log delta|)]^2 dS(y)
       <= (2pi/|log delta|^2) log(C delta/(c delta^2))
       <= C/|log delta|.                                  (6.3)

The indicator in (6.2) has L^2 norm at most C delta. Bounded surface Jacobians and finitely many vertices and facets give

    ||W_lambda||_{L^2(Sigma_lambda)}
          <= C[delta+|log delta|^(-1/2)] =: epsilon_lambda
          ->0.                                           (6.4)

Combining Holder with (4.2), for every H^1 matrix field A,

    integral_{Sigma_lambda} W_lambda |A|^2
       <= C epsilon_lambda
          [integral_{P_lambda}|grad A|^2
                        + integral_{P_lambda}|A|^2].       (6.5)

This is exactly the quadratic-form estimate required to absorb the boundary term in (2.1). No Fefferman-Phong estimate or unspecified small-volume argument is being substituted for it. The L^2 boundary exponent and H^1->L^4 trace are specific to dimension three.

## 7. Degree, existence, and passage to the limit

The same geodesic interpolation supplies a homotopy from eta_lambda to q|Sigma_lambda. It is defined globally: in the inner vertex neighborhoods eta=q; elsewhere every interpolant remains in the verified hemisphere about q. The restriction q|Sigma_lambda has degree one because it is homotopic on the collar to q_0, and radial projection Sigma_lambda->boundary P preserves orientation. Thus eta has degree one.

The outward Gauss map of any smooth convex boundary enclosing zero is homotopic to its radial map: nu(x) dot x>0, since its supporting plane separates zero strictly from the exterior, so normalized straight interpolation has no zero. Its degree is therefore one. As Sigma_lambda is a sphere, eta is homotopic to this Gauss map. All hypotheses of the smooth-domain input in Section 2 now hold separately for every sufficiently large lambda. Strict convexity is not required there; our flat patches are permitted.

Obtain a nonzero A_lambda and normalize integral_{P_lambda}|A_lambda|^2=1. From (2.1) and (6.5), with E_lambda=integral|grad A_lambda|^2,

    E_lambda <= C epsilon_lambda(E_lambda+1).

For large lambda the coefficient is below 1/2; hence E_lambda->0. Uniform extension from Section 4 gives H^1-bounded matrix fields on one fixed ball. Rellich gives a subsequence converging strongly in L^2 and weakly in H^1. On every compact subset of P's interior, the limit A has gradient zero. Since that interior is connected, it is a single constant matrix C.

No mass is lost in the boundary layer. For the extensions B_lambda and their strong L^2 limit B,

    || |B_lambda|^2-|B|^2 ||_{L^1}->0.

Moreover 1_{P_lambda}->1_P almost everywhere, since every interior point eventually has F_lambda=0 and all P_lambda lie inside P. Therefore

    1=lim integral_{P_lambda}|B_lambda|^2
      =integral_P |B|^2=vol(P)|C|^2.

Thus C is nonzero.

Fix a relatively compact open patch in the relative interior of F_i. For all large lambda, Sigma_lambda agrees there with F_i, only i is active, the vertex cutoff is identically one, and eta_lambda=m_i. A fixed small interior half-ball meeting that patch is contained in P_lambda. On it A_lambda converges strongly in H^1 to C: L^2 convergence is inherited, and its gradient energy tends to zero. Continuity of the trace passes the boundary relation to the limit and yields

    c(n_i) C = C c(m_i)  for each facet i.                 (7.1)

Each facet has such a patch. We need no uniform pointwise bound on A_lambda and do not take traces at vertices.

## 8. Clifford algebra finishes the comparison

Taking adjoints of (7.1) and using skew-adjointness gives

    C* c(n_i)=c(m_i) C*.

It follows that C*C commutes with c(m_i) for every i. The target facet normals span R^3: otherwise Q would be invariant under translation in a nonzero common orthogonal direction, contradicting boundedness. The irreducibility of the two-dimensional complex Clifford representation therefore forces C*C=aI. Since C is nonzero, a>0; hence C is invertible. For arbitrary i,j, apply (7.1) twice and add in the opposite order:

    [c(n_i)c(n_j)+c(n_j)c(n_i)] C
       = C [c(m_i)c(m_j)+c(m_j)c(m_i)].

The Clifford relation and cancellation of C give n_i dot n_j=m_i dot m_j. This proves the stated stronger theorem and, by the initial reversal argument, the exact OWR target.

## 9. Audit boundary and credit

Every geometric and limiting link of this candidate is supplied above, including orientation, nonsimple vertices, active-set localization, the critical L^2 boundary norm, the uniform trace constant, and nonvanishing of the limit. The specialized black box is entirely on smooth convex domains and was checked in Brendle's published theorem via the version-pinned author manuscript. The basic Sobolev and elliptic foundations remain imported, not formalized.

The comparison itself is also a consequence of the theorem claimed by Wang, Xie and Yu in arXiv:2606.30130v1, Theorem 1.2; their Definition 2.8 permits maps nonsmooth at vertices. That recent preprint is not fully audited here and no journal acceptance was verified. Bi's arXiv:2608.06320v1 supplied the successful smoothing strategy; it likewise remains a recent preprint in the checked sources. This candidate must receive a fresh, independent full mathematical audit before any repository acceptance or solved classification. Finite computations accompanying it validate only algebraic/packaging diagnostics.

References:
- OWR report, printed p.1198, problem 4: https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1
- Akopyan-Karasev, Conjecture 5.1: https://arxiv.org/abs/1505.05263v2
- Brendle, smooth-domain analytic input: https://arxiv.org/abs/2301.05087v4 and https://doi.org/10.1007/s00222-023-01229-x
- Bi, smooth approximation strategy: https://arxiv.org/abs/2608.06320v1
- Wang-Xie-Yu, three-dimensional preprint: https://arxiv.org/abs/2606.30130v1
- Bar-Hanke-Schick, version-specific caution: https://arxiv.org/abs/2202.05180v2
