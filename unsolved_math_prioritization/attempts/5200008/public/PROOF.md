# Positive words of billiard reflections: reductions and restricted obstructions

**Problem 5200008 / AMR-051-0008. Status: unresolved after five substantive attempts.**

The target is Alexey Glutsyuk's Problem 2 in *Open problems on billiards and geometric optics* [1, p. 6]. Given a smooth closed strictly convex hypersurface gamma in Euclidean space and any prescribed positive C^k tolerance, can every smooth Hamiltonian map of its phase cylinder be approximated in C-infinity by finite compositions of reflections from gamma and hypersurfaces within that tolerance, without inverse reflections?

This note proves conditional reductions and obstructions for restricted families. It does not prove or refute the stated density for all allowed deformations. All existing thin-film density results used here are credited to Glutsyuk and Perline through [2]. No historical novelty or priority is asserted.

## 1. Definitions and the orientation issue

An oriented line is represented by (u,q), where |u|=1, q is perpendicular to u, and the line is q+t u. Its phase space has canonical one-form lambda=q dot du and symplectic form omega=d lambda. A simultaneous change of sign in omega and Hamiltonian convention changes none of the assertions below.

For a strictly convex hypersurface Sigma, T_Sigma reflects the line at its **last** intersection with Sigma in the direction u. If that point is x and the exterior unit normal is n, the outgoing direction is u-2(u dot n)n. The new line is oriented into the convex body. On the open set of transverse secants this is a smooth symplectomorphism. Its next reflection is generally at a different endpoint. The phase cylinder Pi_gamma consists of transverse secants to gamma.

Finite positive words mean finite compositions of these maps, with restrictions to open sets on which every reflection is smooth and defined. The empty word is permitted; excluding it does not affect any density assertion. Closure means uniform convergence with all derivatives on compact subsets, with approximating domains eventually containing each compact subset of the target domain. This is the domain convention in [2, Definition 1.2], not a claim that every approximating word must be smooth on the entire phase cylinder simultaneously.

Let S be this positive-word family for one fixed allowed neighborhood of gamma; write cl(S) for its smooth compact-open closure, with restrictions. The finite-composition continuity argument on compact trajectories shows that cl(S) is closed under every well-defined finite composition. An exhaustion by compact sets and a diagonal choice also shows closure is idempotent. In particular, limits of maps already in cl(S) stay in cl(S).

### Proposition 1: reversibility does not supply allowed inverses

Let J reverse line orientation. Then

    J(u,q)=(-u,q),     J*lambda=-lambda,     J*omega=-omega,
    T_Sigma^(-1) = J T_Sigma J.

Proof. The first identities follow by substitution. To recover the predecessor of a directed line, reflect it at its first endpoint and use the outward direction there. Reversing its orientation turns that endpoint into the last one; applying T_Sigma and reversing once more performs exactly this operation. This proves the last identity. Equivalently, reversing an incoming and outgoing pair exchanges their roles at the same boundary point. Strict convexity makes the required first and last endpoints unique.

On a nonzero-dimensional phase cylinder J is anti-symplectic. No sequence of symplectic maps can converge to J in C^1 on a nonempty open set: pullbacks of omega converge under C^1 convergence, which would give both J*omega=omega and J*omega=-omega. Thus replacing each occurrence of J individually by positive reflection words is impossible. This does **not** prevent approximation of the symplectic composite J T_Sigma J by some different positive words.

The familiar involutivity of reflection in one fixed tangent hyperplane does not imply T_Sigma squared is the identity. The next section supplies an explicit circle counterexample to that identification.

## 2. Exact circle formula and a Hamiltonian test target

Work in the oriented plane, with J_0 the counterclockwise quarter-turn. Write

    u=(cos theta,sin theta),    q=p J_0 u,
    lambda=p dtheta,            omega=dp wedge dtheta.

For the circle of radius R centered at the origin, Pi_R is S^1 times (-R,R). Put

    alpha_R(p)=-2 arccos(p/R),
    T_R(theta,p)=(theta+alpha_R(p) mod 2pi,p).                 (2.1)

To verify this, rotate to u=(1,0). The last point is x=(s,p), where s=sqrt(R^2-p^2)>0. Reflecting in the tangent gives

    u'=(2p^2/R^2-1,-2ps/R^2).

This is the unit vector of angle alpha_R(p). Moreover det(u',x)=p, so the outgoing oriented-line coordinate remains p. This proves (2.1), including the endpoint convention. In particular,

    alpha_R'(p)=2/sqrt(R^2-p^2)>0.                            (2.2)

With i_X omega=-dH, a Hamiltonian depending only on p has flow theta dot=H'(p), p dot=0. Hence T_R is the time-one map of

    H_R(p)=-2p arccos(p/R)+2sqrt(R^2-p^2).                    (2.3)

Its inverse is the time-one map of -H_R. These functions are smooth on the open cylinder and their flows are complete there because p is fixed. No behavior at grazing, p=+/-R, is needed.

For any a<R, the inverse on K=S^1 times [-a,a] is also the restriction of a compactly supported Hamiltonian diffeomorphism of Pi_R: take -chi(p)H_R(p), where chi is smooth, equals one on a neighborhood of [-a,a], and vanishes near +/-R. This flow still fixes p and agrees with T_R^(-1) on K.

## 3. Attempting inversion by recurrence

### Proposition 2: no positive-power recurrence on a momentum band

Fix 0<a<R. No sequence of positive powers of T_R converges uniformly on K=S^1 times [-a,a] to the identity. Nor can positive powers converge there to T_R^(-1).

Proof. The angular displacement of the m-th power has real lift m alpha_R(p). Its variation across the band is

    m(alpha_R(a)-alpha_R(-a))=4m arcsin(a/R).

If this is at least 2pi, its image contains a number congruent to pi modulo 2pi. At that p the angular distance from the identity is exactly pi. Consequently, for every

    m >= ceil(pi/(2 arcsin(a/R)))

the uniform angular distance from the identity is pi. Any bounded sequence of positive integer exponents has a constant subsequence. No fixed positive power is the identity on K, because its angular derivative in p is the strictly positive function m alpha_R'(p). Thus no remaining bounded sequence can converge uniformly to the identity either.

If T_R^m converged to T_R^(-1), composing with the fixed T_R would give T_R^(m+1) converging to the identity; p-invariance keeps K unchanged. This is impossible by the preceding argument. Alternatively, their C^1 shear entries differ by (m+1)alpha_R'(p), but the C^0 argument is stronger.

Each fixed momentum circle has recurrent rotations. This proposition explains precisely why pointwise or measure-theoretic recurrence cannot be promoted to compact-open recurrence of billiard maps. It rules out a particular proposed inverse construction, not the original problem.

## 4. Attempting inversion using concentric deformations

### Proposition 3: quantitative obstruction for all concentric positive words

Fix radii 0<a<R_min<=R_max and a base radius R_0>a. Let W be any finite positive word of reflections in concentric circles whose radii R_j lie in [R_min,R_max]. Then W cannot approach T_R0^(-1) on K even in C^0, regardless of word length. More precisely, if e(W) is the supremum of their angular distance over K, then

    e(W) >= 2 arcsin(a/R_0)>0.                               (4.1)

For a nonempty word of length m, the C^1 shear-entry difference at p=0 satisfies

    |partial_p theta_W - partial_p theta_T_R0^(-1)|
       = 2 sum_j(1/R_j)+2/R_0 >= 2m/R_max+2/R_0.             (4.2)

Proof. The factors commute and preserve p. Their word has real angular displacement

    A(p)=sum_j alpha_Rj(p),    A'(p)=sum_j 2/sqrt(R_j^2-p^2).

Thus A is increasing for m>=1 and constant for the empty word. The inverse target has lift beta(p)=-alpha_R0(p), which is decreasing, with

    beta(a)-beta(-a)=-4 arcsin(a/R_0).

Suppose e(W)<2 arcsin(a/R_0). This is strictly less than pi because a<R_0. There is therefore a unique integer n(p) with

    |A(p)-beta(p)-2pi n(p)| <= e(W)<pi.

Continuity on the connected interval [-a,a] makes this integer constant. Subtract the endpoint inequalities. Since A(a)-A(-a)>=0, they imply

    4 arcsin(a/R_0) <= 2e(W),

a contradiction. This proves (4.1), including the empty word. Differentiation proves (4.2).

The common-radius restriction is essential: general deformed mirrors do not preserve this same p, and their derivative matrices are not upper-triangular shears. The proposition is a genuine non-density result for the concentric subfamily, not a counterexample to a question allowing all small deformations. By the cutoff construction in Section 2, the same obstruction applies to a compactly supported Hamiltonian target.

## 5. A conditional reduction to one inverse

The established input is Glutsyuk's theorem [2, Theorem 1.1 and Theorem 1.13]. For the normal deformation

    gamma_(s,f)={x+s f(x)n(x):x in gamma},
    D_(s,f)=T_gamma_(s,f)^(-1) T_gamma,
    v_f=partial_s D_(s,f)|_(s=0),

the vector fields v_f are Hamiltonian, depend linearly on f, and their generated Lie algebra is C-infinity dense in all Hamiltonian vector fields on Pi_gamma. The Hamiltonian in tangent-ball coordinates (x,w) is -2 f(x)sqrt(1-|w|^2). This is an attributed published theorem; the present note does not claim to replace its Lie-algebra proof.

### Proposition 4: one inverse suffices

For any fixed allowed C^k neighborhood of gamma, assume that the map T_gamma^(-1) on Pi_gamma belongs to cl(S). Then cl(S) contains every Hamiltonian diffeomorphism Pi_gamma to itself. The same argument works on Hamiltonian domains with the domain convention of Section 1.

Proof, with the inverse-removal and domain steps explicit.

**Step 1: admissible small increments.** Fix f. For sufficiently small |s| the normal deformation is a smooth embedded hypersurface in the given C^k neighborhood, and its last-intersection reflection branches are well-defined on each chosen compact set of transverse lines. All deformation arguments here use these branches; no uniform assertion at grazing is required. Define

    E_(s,f)=T_gamma^(-1) T_gamma_(s,f)=D_(s,f)^(-1).

On every chosen compact subset of Pi_gamma, this is well-defined for small |s|, is in cl(S), and has expansion

    E_(s,f)=Id-s v_f+O(s^2)                                  (5.1)

with all derivatives on that compact set. Indeed T_gamma_(s,f) of the compact set remains in Pi_gamma for small |s|, by openness, continuity and compactness. Approximate T_gamma^(-1) on a compact neighborhood of that image and compose. Differentiating the identity E_(s,f)D_(s,f)=Id gives (5.1).

**Step 2: both directions of the thin-film flows.** Fix a time t and a compact set whose full v_f trajectories up to time t are contained in the domain. The increments (5.1) with s=-t/N, or with positive s and the sign of f reversed, give

    (E_(-t/N,f))^N -> flow_(v_f)^t

in C-infinity on that compact set. For sufficiently large N all intermediate points remain in a slightly larger compact trajectory neighborhood. Local error O(N^-2), discrete Gronwall, and induction on the derivative order give global error O(N^-1) at each fixed finite derivative order. Each finite iterate is in cl(S), so the flow is too. Using an exhaustion by compact sets and increasing derivative order gives the stated topology. The sign change is allowed because f and -f are both available normal displacements. Crucially, no negative-time map was assumed to be a positive reflection word.

**Step 3: Lie brackets and sums.** Whenever flows of X and Y for both time signs belong to cl(S), set

    C_h=flow_Y^(-h) flow_X^(-h) flow_Y^h flow_X^h.

With the conventional vector-field bracket [X,Y]=DY X-DX Y, Taylor expansion gives C_h=Id+h^2[X,Y]+O(h^3). Therefore (C_(sqrt(t/N)))^N converges to flow_[X,Y]^t for t>0; exchange X,Y for negative t. The scale is sqrt(t/N), so the limiting time is t. Finite sums follow from the Trotter formula (flow_X^(t/N) flow_Y^(t/N))^N. Real multiples follow by time rescaling. At each use take compact trajectory neighborhoods and then a diagonal sequence. Thus every locally well-defined flow of the Lie algebra generated by the v_f lies in cl(S).

**Step 4: all Hamiltonian maps.** By the credited Lie-algebra density and smooth ODE dependence, flows of arbitrary smooth Hamiltonian vector fields are compact-open limits of flows from the preceding Lie algebra. For a smooth Hamiltonian isotopy F_t, fix a compact initial set. Its trace under F_t, t in [0,1], is compact in the open phase cylinder. Multiply its time-dependent Hamiltonian by a compactly supported cutoff equal to one on a neighborhood of this trace; this does not change the isotopy on the chosen initial set. Time discretization approximates its time-one map by finite products of autonomous Hamiltonian flows. Approximate each of those fields on suitable compact neighborhoods by the dense Lie algebra. The composition continuity and closure already established show F_1 on the chosen compact set is approximable by S. An exhaustion and a diagonal choice complete the proof. For maps between moving domains, use the same compact trace in the domains of the Hamiltonian isotopy. No uniform control near grazing is being asserted.

### Corollary 4.1: exact equivalence for a round base circle

For each fixed allowed neighborhood of a round circle, the original Hamiltonian density statement is equivalent to T_R^(-1) belonging to cl(S). Sufficiency is Proposition 4; necessity follows because T_R^(-1) itself is Hamiltonian by (2.3).

This corollary does not assert that T_gamma is Hamiltonian for every hypersurface in every dimension. Such a claim is unnecessary and has not been used. The criterion identifies a missing construction; it does not provide one. Propositions 2 and 3 show why two natural proposed constructions do not supply it.

## 6. Attempting to extend the concentric obstruction

### Proposition 5: a bounded-word barrier for small nonsymmetric perturbations

Fix R>0, 0<a<R, and a positive integer M. There exists delta_M>0 with the following property. If every factor is reflection in a normal graph over the radius-R circle whose C^2 norm is less than delta_M, then any word of length at most M has C^1 shear-entry error at least 2/R from T_R^(-1) on K=S^1 times [-a,a]. Here error means the supremum of the absolute difference of the angular output derivatives with respect to p, so it is a lower bound for any coordinate C^1 norm dominating that entry.

Proof. Choose a<b<R. The base circle reflection and its first M iterates preserve |p|. The equation defining each last intersection is transverse on |p|<=b. The implicit function theorem and the reflection formula show that C^2-small normal graphs induce C^1-small changes of the reflection map on such compact sets: the intersection derivative uses the boundary tangent, and the derivative of its normal uses second derivatives of the graph. The transverse denominator is uniformly bounded away from zero there.

For each fixed m<=M, continuity of m-fold composition gives uniform C^1 convergence of the perturbed word to T_R^m as all its graph norms tend to zero; intermediate images of K stay in |p|<b after making the norms sufficiently small. There are finitely many lengths, so choose one delta_M which works for all of them and makes the angular shear-entry discrepancy from T_R^m less than 1/R at p=0, for every theta. The base derivative there is 2m/R. Hence every nonempty permitted word has angular shear entry greater than (2m-1)/R, while the inverse has entry -2/R. Their difference is greater than (2m+1)/R, in particular greater than 2/R. The empty word has entry zero and error exactly 2/R. This proves the claim.

Consequently, along shrinking C^2 neighborhoods of the circle, any approximating words for T_R^(-1), if they exist, must have lengths tending to infinity. This is a two-parameter statement. It supplies no word-length bound at one fixed positive neighborhood size and no obstruction to the original density claim.

### Proposition 6: shear sign is not an unrestricted semigroup invariant

For any a_0>0, matrices arbitrarily close to the shear S=[[1,a_0],[0,1]], each with positive upper-right entry, have positive powers with negative upper-right entry. Specifically, for each integer N>=3 set

    epsilon_N=(2-2cos(2pi/N))/a_0,
    A_N=[[1,a_0],[-epsilon_N,1-a_0 epsilon_N]].

Then det(A_N)=1, A_N tends to S, A_N^N=I, and

    A_N^(N-1)=A_N^(-1)
              =[[1-a_0 epsilon_N,-a_0],[epsilon_N,1]].

Proof. Determinant and trace are 1 and 2cos(2pi/N). The two eigenvalues are the distinct N-th roots exp(+/-2pi i/N). Diagonalization over the complex numbers gives A_N^N=I. The inverse formula gives the asserted negative entry. Finally epsilon_N tends to zero.

These are symplectic linear maps of a two-dimensional local model. They are **not** asserted to be derivatives of one family of permitted billiard reflection words on an open set, nor global maps of the cylinder. The proposition defeats the proposed inference from proximity to a positive shear alone. It does not solve optical realizability, simultaneous control across a compact phase region, or any derivative uniformity problem.

## 7. Final gap

A full affirmative result still requires positive reflection words that uniformly approximate the necessary Hamiltonian maps using genuinely unrestricted small hypersurface deformations. A concrete sufficient target is T_gamma^(-1) in the smooth compact-open positive-word closure; for a round circle this target is equivalent to the original density statement. No construction accomplishing it is given here.

A full negative result would need an invariant or closed obstruction valid for all such deformation words, not merely for concentric factors or words with a preassigned bounded length. No such obstruction is proved here. The explicit matrix example explains why the elementary shear obstruction does not extend formally.

Finite exact checks accompanying this note verify algebraic identities and selected controls. The analytic proofs above establish the quantified restricted results. The checks do not settle the open density question and do not validate the conditional hypothesis in Proposition 4.

## References

[1] M. Bialy, C. Fierobe, A. Glutsyuk, M. Levi, A. Plakhov, S. Tabachnikov, *Open problems on billiards and geometric optics*, arXiv:2110.10750, Alexey Glutsyuk, Problem 2, PDF pp. 6-7. https://arxiv.org/abs/2110.10750

[2] A. Glutsyuk, *Density of a thin film billiard reflection pseudogroup in a Hamiltonian symplectomorphism pseudogroup*, Israel Journal of Mathematics 258 (2023), 137-184. DOI: https://doi.org/10.1007/s11856-023-2470-3 . Primary preprint inspected: arXiv:2005.02657v5, September 2025, especially Sections 1.1, 1.4, 1.6, 2.4-2.5, 3.3, and 4.1. https://arxiv.org/abs/2005.02657

[3] B. Albach et al., *Open problems in billiards and quantitative symplectic geometry*, arXiv:2602.12896v1 (2026), optical-transformation question, PDF pp. 19-20. This is related background, not a resolution of [1]. https://arxiv.org/abs/2602.12896
