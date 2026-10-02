# Turn 3: finite-volume clique integrals with explicit bias bounds

Substantive author turn **3/5**. Work at Poisson intensity 1; scaling handles every positive intensity. Apply CORRECTION_CONE.md to the frozen turn-1 proof. This turn replaces a bare infinite-process Palm expectation by finite-dimensional integrals with controlled spatial and point-count truncation. It does not evaluate those integrals or establish a high-dimensional trend.

Fix d>=1 and 1<=k<=d. Write κ=κ_d, let B_j be the j-th Bell number, and let T_j(t)=Σ_i S(j,i)t^i be the Poisson moment polynomial. Put M=9^d and v=κ/8^d. Define the finite constant

 D = B_{2k}(1+κ2^d)^{2k}
     + sqrt(M B_{4k}) Σ_{j>=0}(1+κ2^{d(j+2)})^{2k} exp(−v2^{jd}/2).       (18)

For L>0 put μ=κL^d and

 p_L = min{1, M[1+κ(L/4)^d] exp(−v(L/8)^d)},
 E_L = sqrt(p_L)[sqrt(D)+sqrt(B_{2k})(1+μ)^k]/(k+1).                    (19)

Let P_L be the Poisson points in B(0,L), with the origin added. Form the ordinary finite-set Delaunay graph, including its convex-hull edges, and let S_L be the number of its k-cliques containing the origin (that is, cliques on k+1 vertices). Then

 | E S_L/(k+1) − b_{d,k} | <= E_L,       E_L -> 0 as L -> infinity.     (20)

The terminology “k-clique” in this paragraph always means the flag k-simplex, not a graph clique on k vertices.

## 1. Explicit shields

A maximal 1/4-separated subset of the unit sphere has at most 9^d members: disjoint radius-1/8 balls about its members fit inside B(0,9/8). Its maximality makes it a 1/4-net. Around each direction take the circular cone of half-angle π/6. The cones cover every direction because chord length <=1/4 implies an angle less than π/6. Every cone contains B(ru/2,r/8) inside B(0,r): its angular radius is at most arcsin(1/4)<π/6 and its farthest point has norm 5r/8. Thus each truncated cone has volume at least vr^d.

For a point x of a locally finite configuration, say it is shielded at scale r if each translated cone contains another point within distance r of x. Two vectors in one cone have mutual angle at most π/3. The corrected turn-1 argument proves that its Voronoi cell is contained in B(x,r), and every Delaunay neighbor is within 2r of x.

Under the point-Palm law, failure of a shield at scale r has probability at most M exp(−vr^d). Adding deterministic points can only improve this event. These statements also hold for any configuration obtained by retaining all the points within distance r of x; no far-away shield points are required.

For later use, apply the turn-1 dyadic degree argument with moment 2k and the explicit M,v. The degree V of the origin has E V^{2k} <= D. Indeed on R<=1 use the Poisson count in B(0,2); on 2^j<R<=2^{j+1} use Cauchy–Schwarz, the count in B(0,2^{j+2}), and the shield tail at 2^j. The Poisson Bell-number bounds give exactly (18). Its terms decay faster than any geometric sequence. In particular D is finite.

## 2. Simultaneous shielding is needed for a clique

It would be insufficient to stabilize only the edges incident to the origin. A clique also contains edges between its other vertices.

Let G_L be the event that the origin and every point of P in B(0,L/4) are shielded at scale L/8, in P with the origin added. A union bound and Mecke's formula give

 P^0(G_L^c) <= M exp(−v(L/8)^d)
                 + |B(0,L/4)| M exp(−v(L/8)^d) <= p_L.               (21)

For the second term, the point whose shield is being tested is planted by Mecke; the additional origin can only help. No independence between shields is assumed.

On G_L, all shield points of the origin lie inside B(0,L), and the origin's finite-set Voronoi cell is contained in B(0,L/8). Every finite-set neighbor of the origin is therefore in B(0,L/4). For each such vertex x, its shield witnesses lie inside B(x,L/8), hence inside B(0,3L/8). Its finite-set cell is contained in B(x,L/8). Any omitted point z outside B(0,L) has distance from x at least 3L/4; for y in that cell,

 |z−y| >= 3L/4−L/8 = 5L/8 > L/8 >= |x−y|.

All omitted Voronoi inequalities are consequently redundant. The finite and infinite Voronoi cells of the origin and of every possible neighboring vertex coincide. Intersections of these cells determine all edges among the candidates, so the entire clique score agrees: S_L=C^F_k(0).

On the complementary event, S_L<=N_L^k and C^F_k(0)<=V^k, where N_L is Poisson(μ). Cauchy–Schwarz and (18) therefore give

 E|S_L−C^F_k(0)| <= sqrt(p_L)[sqrt(D)+sqrt(E N_L^{2k})],

which proves (20). The exponential in L^d dominates the polynomial factors in (19).

## 3. A finite integral formula and a second explicit truncation

For n distinct nonzero points x_1,...,x_n in B(0,L), define c_{n,k}(x_1,...,x_n) to count flag k-simplices containing 0 in their finite Delaunay graph, and set it to zero if n<k. Thus 0<=c_{n,k}<=binomial(n,k)<=n^k. Degenerate input configurations may be assigned any bounded convention; they have Lebesgue measure zero.

The indicator that a pair u,w is a Delaunay edge can be written explicitly as linear feasibility in a center y:

 2y·(w−u)=|w|²−|u|²,
 2y·(z−u)<=|z|²−|u|² for every other input point z.                   (22)

On generic inputs a nonempty intersection is the usual Delaunay edge. The clique score is the sum over k-subsets of products of these pair indicators. Thus the following formula contains only specified finite configurations and finite-dimensional integrals, rather than an unnamed infinite-process event:

 b_{L,m} = e^(−μ)/(k+1) Σ_{n=0}^m (1/n!)
                  ∫_{B(0,L)^n} c_{n,k}(x_1,...,x_n) dx_1...dx_n.   (23)

Conditioning on the Poisson count proves that the infinite sum equals E S_L/(k+1). Its count-truncation error satisfies

 0 <= E S_L/(k+1) − b_{L,m}
    <= [2^(−m) e^μ T_k(2μ)]/(k+1).                                (24)

Indeed 1{N_L>m}<=2^{N_L−m}, while the exponential-tilt identity gives E[N_L^k 2^{N_L}]=e^μ T_k(2μ). Consequently

 |b_{d,k}−b_{L,m}| <= E_L + [2^(−m)e^μ T_k(2μ)]/(k+1).              (25)

For any prescribed positive tolerance, first choose L to make E_L small, then m to control (24). A certified approximation of the finitely many integrals in (23) would then yield a certified value of the clique denominator. Such an integration procedure and useful numerical execution are not supplied by this turn. In particular (23) is not being advertised as an evaluated answer to Bauer's question.

## 4. Scope and credit

The finite-set empty-ball characterization, Poisson conditioning/tilting, Mecke formula, and degree-tail reasoning are standard ingredients; turn 1 credits the primary Poisson reference. This derivation assembles them for the clique score and explicitly handles its second layer of edges. No new external theorem is imported. The original remains unresolved after three author turns. These bounds are deliberately crude and dimension dependent; they do not justify an empirical fraction from an uncorrected finite convex hull, nor an ordering of fractions across dimensions.
