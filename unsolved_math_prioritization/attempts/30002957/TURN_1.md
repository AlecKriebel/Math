# Turn1: finite simplex intensities and a planar fraction bound

Substantive author turn **1/5**,2026-10-02. Let P be a homogeneous Poisson point process of intensity λ>0 in R^d, d≥1. Let D_k(P) be its Delaunay k-faces and F_k(P) the(k+1)-vertex cliques of its Delaunay graph, for0≤k≤d. Every member of D_k is a member of F_k. We count each unordered vertex set once.

## Theorem

There are finite positive constants a_{d,k},b_{d,k}, with0<a_{d,k}≤b_{d,k}, such that the barycenter counting measures of D_k and F_k have respective intensities λa_{d,k},λb_{d,k}. Their fraction in expanding cubes converges **in L1** to

    theta_{d,k}=a_{d,k}/b_{d,k}.

The same limit holds when only simplices whose vertices all lie in the observation cube are counted. Thus this is a simplex-typical, intensity-independent fraction, rather than a vertex-Palm or volume-weighted probability. For k=0,1 it equals1. In dimension2,

    2/3 ≤ theta_{2,2} < 1.                     (1)

The exact value in(1) and its higher-dimensional analogues remain uncomputed. The source's broader question is not resolved by this theorem.

## 1. All moments of the Palm degree

Under the point-Palm law P^0, the process is an independent Poisson process together with the origin. Cover the unit sphere by finitely many circular cones C_1,…,C_M of half-angleπ/3, with every direction belonging to one of them. In each cone let R_i be the distance to its nearest Poisson point other than0 and put R=max_i R_i. A cone has positive volumeκ r^d inside B(0,r), whereκ depends only on d and the chosen opening. Therefore

    P^0(R>r) ≤ M exp(−λκ r^d),                (2)

and R is finite almost surely.

If y is in the Voronoi cell of0, choose a cone covering the direction of y and a point z in that cone with||z||≤R. The Voronoi inequality gives2 y·z≤||z||², while the cone angle gives y·z≥||y||||z||/2. Hence||y||≤||z||≤R. The cell of0 is contained in B(0,R). If x is a Delaunay neighbor of0, some y belongs to both Voronoi cells, so||x||≤||x−y||+||y||=2||y||≤2R. Thus its degree V satisfies

    V ≤ #(P∩B(0,2R)),                        (3)

where the added origin is not included on the right.

For any positive integer q, split according to R≤1 and2^j<R≤2^{j+1}, j≥0. By Cauchy–Schwarz, the contribution of the j-th range to E^0 V^q is at most

    (E #(P∩B(0,2^{j+2}))^{2q})^{1/2}
       · P^0(R>2^j)^{1/2}.                    (4)

A Poisson count with meanμ has r-th moment Σ_{i=1}^r S(r,i)μ^i, with nonnegative Stirling coefficients, and hence at most B_r(1+μ)^r, where B_r is the r-th Bell number. The first factor in(4) grows at most polynomially in2^{jd}; the second decays as exp(−c2^{jd}). The series is finite. Consequently V has every finite integer moment. The number C^F_k(0) of flag k-simplices containing0 is at most binomial(V,k), so it is integrable for each fixed k, and the same holds for C^D_k(0).

These are unconditioned point-Palm counts, not the distribution of a uniformly chosen simplex. The factor k+1 below is essential.

## 2. Palm counts, anchors and finite counting measures

For a finite simplex A write b(A) for its barycenter. Let N^F_k(Q) count flag k-simplices with b(A)∈Q. By nonnegative Campbell–Mecke/Tonelli,

    E N^F_k(Q)
      = (λ/(k+1)) ∫_{R^d} E^0 Σ_{A∈F_k(P^0):0∈A}
                                1{x+b(A)∈Q} dx
      = (λ|Q|/(k+1)) E^0 C^F_k(0).             (5)

The first equality distributes unit mass over the k+1 vertices of each simplex. Define

    b_{d,k}(λ)=(1/(k+1))E^0 C^F_k(0),
    a_{d,k}(λ)=(1/(k+1))E^0 C^D_k(0).

Equation(5) and the degree moment bound show local finiteness almost surely and finite intensity for both counting measures. Their atoms need not be assumed distinct. They are measurable translation-covariant functions of P; the standard Delaunay/Voronoi construction is used on its almost-sure general-position event.

Exactly the same calculation holds for any measurable translation-covariant choice of one anchor per simplex. In particular the intensity agrees with the smallest-empty-circumball-center anchoring used in Edelsbrunner–Nikitenko–Reitzner. This justifies using their Delaunay intensity values as the numerator; equality of anchor intensities is not assumed without proof.

Positivity of a_{d,k} follows from a local Delaunay event. Under P^0, place one point near each of e_1,…,e_d and no other points in a sufficiently large fixed ball containing the circumballs of all those perturbed d-simplices with0. The event has positive probability. For sufficiently small neighborhoods,0 and the d chosen points form a Delaunay d-simplex, with all its k-faces. Thus E^0 C^D_k(0)>0. For k=0 the count is1 directly.

Dilation x↦λ^{1/d}x takes the intensity-λ Poisson process to an intensity-one process and preserves all Delaunay/clique incidences. Point-Palm degree and simplex counts are unchanged by that dilation. Hence a_{d,k}(λ),b_{d,k}(λ) do not depend onλ; we drop that argument. In particular both intensities scale linearly withλ, and their ratio is intensity-independent.

## 3. The large-window statement and boundary control

A homogeneous Poisson process is mixing and ergodic. The two counting measures are translation-equivariant factors, hence ergodic as well. The spatial mean ergodic theorem for stationary point processes with finite intensity gives, for Q_R=[−R,R]^d,

    N^F_k(Q_R)/|Q_R| → λb_{d,k},
    N^D_k(Q_R)/|Q_R| → λa_{d,k}                in L1.             (6)

One can use Last–Penrose, Proposition8.13 and Theorem8.14; the latter asserts L1 convergence, which is the mode claimed here. We do not silently replace it by an almost-sure assertion.

Let M^F_k(Q_R) count only flag simplices whose vertices all belong to Q_R. Convexity gives M≤N. Applying the same Palm distribution of mass as in(5),

 E[N^F_k(Q_R)−M^F_k(Q_R)]/|Q_R|
   = (λ/(k+1)) E^0 Σ_{A∋0}
       [1−| intersection_{v∈A}(Q_R−v)|/|Q_R|].                (7)

For each fixed finite A the intersection-volume ratio tends to1. The bracket is in[0,1], and the dominating Palm clique count is integrable. Dominated convergence makes(7) tend to0. Thus the vertex-inside counts have the same L1 intensity limit. The same argument applies to Delaunay faces.

Define a fraction with zero denominator to be0. Sinceλb_{d,k}>0, (6) gives convergence in probability of the ratio to a_{d,k}/b_{d,k}. Every finite-window ratio lies in[0,1] because D_k⊂F_k with matching anchors, so boundedness upgrades it to L1 convergence. The vertex-inside ratio is handled identically. This validates the chosen empirical fraction without appealing to a nonexistent uniform law on all simplices of an infinite process.

For k=0 and k=1 the two collections are identical, giving theta=1. In dimension1 these are all dimensions asked for.

## 4. The planar lower bound

A finite simple planar graph with n≥3 vertices has at most3n−8 distinct triangles. Here is the short proof needed rather than an asymptotic citation. Extend the graph to a maximal planar graph on the same vertex set; this can only add triangles. The n=3 case is immediate. For n≥4, if there is no separating triangle, all triangles are faces of the spherical triangulation, so there are2n−4≤3n−8. If a separating triangle exists, split along it into two triangulations with n_1,n_2≥4 and n_1+n_2=n+3. Every triangle belongs to one side, and the separating triangle is counted twice, so induction gives at most

    (3n_1−8)+(3n_2−8)−1=3n−8.

The graph induced by P∩Q_R is simple and planar in dimension2. Its triangles are exactly the flag triangles all of whose vertices lie in Q_R. Hence M^F_2(Q_R)≤3#(P∩Q_R), including the n<3 cases. Taking expectations, dividing by area and using(7) proves

    λb_{2,2}≤3λ.                              (8)

The known Poisson–Delaunay triangle intensity is2λ (ENR equation(45), p14, agreeing with the classical planar count). Equation(5) validates its anchor transfer. Thus a_{2,2}=2, and(8) implies theta_{2,2}≥2/3.

## 5. A robust positive-probability non-Delaunay clique

Use the deterministic sites

    A=(−1,0), B=(1,0), C=(0,1), P=(0,1/4).

The circumcircle of ABC is centered at0 with squared radius1; P lies strictly inside it. On the other hand, all three pairs have strict empty-circle witnesses relative to these four sites:

    AB: center(0,−3), squared radius10,
    AC: center(−3,3), squared radius13,
    BC: center(3,3), squared radius13.

Each circle passes through its named pair, excludes the opposite vertex, and excludes P strictly. The smallest squared-distance margin at P is9/16, for AB; the other two margins are57/16. The opposite-vertex margins are positive as well. All three closed witness disks lie inside B(0,10).

These strict inequalities persist under sufficiently small perturbations of all four sites. To be precise, for a perturbed pair u,v, project its original witness center onto the perturbed perpendicular bisector; the projected center and its radius depend continuously on u,v near the distinct original pair. The circumcenter of the noncollinear perturbed triple also depends continuously on its vertices. Choose four disjoint open neighborhoods small enough that all these inequalities hold, their disks remain in B(0,10), and the triple's barycenter lies in Q=[−1,1]^2.

The Poisson event of one point in each of those neighborhoods and no other point in B(0,10) has strictly positive probability. Outside points cannot enter the witness disks. Thus the three graph edges exist, while the interior point rules out the ABC Delaunay face. There is at least one non-Delaunay flag triangle with barycenter in Q on this event. By(5),

    λ(b_{2,2}−a_{2,2})|Q| ≥ P(event)>0.

Consequently b_{2,2}>2 and theta_{2,2}<1. This proves(1). No particular numerical perturbation radius or numerical value of the intensity gap is certified by this continuity argument; finite perturbation checks only supplement it.

## 6. Credit and remaining gap

Campbell–Mecke, the Poisson Palm law and spatial mean ergodicity are standard credited tools. ENR supplies the Delaunay numerator. The fraction normalization, all-moment degree control, boundary transfer and planar bound are written out here, without novelty certification. An unevaluated Palm expectation is not presented as a closed answer to the source question. The exact planar fraction, its explicit clique denominator, and the general-dimensional dependence remain open in this attempt. Original unresolved1/5.
