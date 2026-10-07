# Matching-to-TSP reduction and exact PSD lift monotonicity

Status: proved independently below. This document does not validate the proposed exponential PSD lower bound for perfect matching. Every exponential conclusion here is conditional on that input until its separate audit passes.

## 1. Definitions and size convention

For a finite vertex set V with |V|=N>=3, let P_TSP(V) be the convex hull in R^{E(K_V)} of the 0/1 incidence vectors of undirected Hamiltonian cycles (each unordered edge is counted once). For even n>=2, let P_PM(n) be the convex hull in R^{E(K_n)} of the incidence vectors of perfect matchings.

Write S^r for real symmetric r-by-r matrices and S_+^r for its positive semidefinite cone. The exact real PSD extension complexity xc_psd(P) is the least positive integer r for which

    P = pi(L intersect S_+^r),

where L is an affine subspace of S^r and pi:S^r -> R^d is an affine map. Size means the matrix dimension r, not the number r(r+1)/2 of scalar entries, number of equations, coefficient bit length, or number of optimization variables. Equalities are free under this convention. Several PSD blocks of sizes r_i can be embedded as a block diagonal slice of S_+^{sum r_i}; counting only the largest block is a different convention and is not used.

An unrestricted free-variable LMI representation also yields this convention with the same r for bounded nonempty P: represent its affine matrix map as T(z) and output as U(z). For a feasible z_0 and every h in the kernel of the linear part of T, all z_0+t h are feasible for all real t. Boundedness of P forces the linear part of U to vanish on that kernel. Hence U factors affinely through T on its affine image, with an affine extension to S^r, giving precisely the displayed cone-slice form. Conversely parametrizing L gives an LMI representation of size r.

## 2. Faces and images do not increase the size

Suppose P=pi(L intersect S_+^r), and a nonempty face F of P is given by a^T x=b, with a^T x<=b valid for P. Then

    L_F = L intersect {X: a^T pi(X)=b}

is an affine subspace and

    F = pi(L_F intersect S_+^r).

Both inclusions follow directly from pi(L intersect S_+^r)=P: the extra equality selects exactly the points mapping into F. This argument makes no duality, strict-feasibility, boundedness of the lift, closure-of-projection, or nondegeneracy assumption. The same proof works for any finite collection of supporting equalities. If T is an affine map, T(F)=(T composed with pi)(L_F intersect S_+^r). Therefore

    xc_psd(T(F)) <= xc_psd(F) <= xc_psd(P).

For our faces, the additional equalities are explicit coordinate-zero, coordinate-one, or sum-of-fixed-edge equalities. All are pulled back to affine equations in X; no PSD row or column is added. A nonempty intersection of these supporting hyperplanes is a face: summing their nonnegative slacks gives one exposing valid inequality, whose zero set is exactly their intersection.

## 3. The original Yannakakis construction uses 3n cities

Primary source: Mihalis Yannakakis, *Expressing Combinatorial Optimization Problems by Linear Programs*, J. Comput. System Sci. 43(3) (1991), 441-466, DOI https://doi.org/10.1016/0022-0000(91)90024-Y. Theorem 2, printed p.454, constructs three sets each of size 2k in his notation, for 6k cities total. On renaming the matching size n=2k, this is exactly 3n cities. Public primary-text copy: https://www.tcs.tifr.res.in/~prahladh/teaching/2011-12/comm/papers/Yannakakis1991.pdf. Rothvoss arXiv:1311.2369v4, pp.3-4 near Corollary 2, credits the linear-size face projection to Yannakakis: https://arxiv.org/pdf/1311.2369.

Fix even n>=2. Let the 3n cities be

    L={l_i:i in [n]}, D={d_i:i in [n]}, R={r_i:i in [n]}.

Define G_n to have all edges within L, all edges within R, and the 2n edges l_i d_i and d_i r_i. There are no other edges. In K_{3n}, put Z=E(K_{3n})\E(G_n). Define

    F_n={x in P_TSP(3n): x_e=0 for every e in Z}.

Equivalently, F_n is the zero-slack face of the valid inequality sum_{e in Z} x_e>=0. It is nonempty by the explicit completion below. Every point in P_TSP is a convex combination of tour incidence vectors; since all coordinates are nonnegative, the zero constraints force every positively weighted tour to avoid Z. Thus F_n is exactly the convex hull of Hamiltonian cycles of G_n, not a subtour-relaxation feasible region.

The projection is the coordinate restriction

    (rho(x))_{ij}=x_{l_i l_j}, 1<=i<j<=n.

In every Hamiltonian cycle of G_n, d_i has only two available incident edges, so both l_i d_i and d_i r_i are present. Each l_i then has exactly one remaining cycle edge within L, and each r_i has exactly one within R. Consequently the L-edges and R-edges form perfect matchings A and B on the common label set [n]. Replacing each forced path l_i-d_i-r_i by a contracted label i produces the degree-two multigraph with edge multisets A and B. The original tour is connected exactly when this multigraph is connected. Parallel edges are allowed in this contracted description: for n=2, the two matchings are the same label pair and their two copies give a connected two-edge multigraph, corresponding to a genuine six-city Hamiltonian cycle.

For surjectivity, given any perfect matching A, enumerate its k=n/2 pairs as {a_1,b_1},...,{a_k,b_k}. Set

    B={{b_j,a_{j+1}}:1<=j<=k}, with a_{k+1}=a_1.

For k>=2 these edges form a perfect matching disjoint from A; for k=1, B=A as a set of labels. In every case the alternating label walk

    a_1,b_1,a_2,b_2,...,a_k,b_k,a_1

is connected when A/B edges are distinguished. Substituting the forced paths yields a Hamiltonian cycle of G_n whose L-projection is A. It follows, using linearity and convex hulls, that

    rho(F_n)=P_PM(n), and xc_psd(P_TSP(3n))>=xc_psd(P_PM(n)).

The map from tours to pairs (A,B) is a bijection onto pairs of perfect matchings whose union multigraph is connected. The projection to A itself is surjective and is generally not injective. This distinction should be explicit.

## 4. A compressed two-layer version uses 2n cities

This is an independently checked simplification obtained by contracting the forced middle paths, not a claim that Yannakakis printed a 2n-city construction, and not a claimed new lower-bound method.

Let cities be L and R, each indexed by [n]. Let D={l_i r_i:i in [n]} be the diagonal matching, and let Z={l_i r_j:i!=j} be the other cross edges. Define

    F'_n={x in P_TSP(2n): x_e=1 for e in D, x_e=0 for e in Z}.

All these equalities are supporting: 0<=x_e<=1 is valid on P_TSP. More compactly, F'_n is the maximizing face for

    h(x)=sum_{e in D}x_e - sum_{e in Z}x_e <= n,

and equality holds exactly when all displayed coordinate constraints hold. A completion as in section 3 proves the maximum n is attained. Each l_i and r_i has one residual edge in its own layer, so these residual edges form perfect matchings A and B. Contracting D produces the same connected union multigraph. The same rho, restricted to L edges, maps F'_n onto P_PM(n). Therefore

    xc_psd(P_TSP(2n))>=xc_psd(P_PM(n)).

Boundary check n=2: F'_2 consists of the four-city cycle l_1,l_2,r_2,r_1,l_1. No degenerate two-city TSP is used.

Merely setting non-diagonal cross edges to zero is insufficient for this compressed version. For n=4, the tour l_1,l_2,l_3,l_4,r_4,r_3,r_2,r_1,l_1 avoids all such cross edges but its L-projection is a path, not a perfect matching. The coordinate-one diagonal conditions are essential.

## 5. Padding from m cities to every N>=m>=3

Let the old cities be {v} union W with |W|=m-1, and add t=N-m new cities z_1,...,z_t. For t=0 use the identity. For t>=1, force the t path edges

    H={v z_1,z_1 z_2,...,z_{t-1}z_t}

to be present. The face

    C_{m,N}={x in P_TSP(N): sum_{e in H}x_e=t}

is nonempty: take any old tour, choose either incident edge v w, and replace it by v,z_1,...,z_t,w. The defining inequality sum_H x_e<=t is valid because each coordinate is at most one. Equality forces each path edge to have coordinate one.

Define the linear projection

    y_{ij}=x_{ij} for i,j in W,
    y_{v j}=x_{v j}+x_{z_t j} for j in W.

On every tour in this face, each internal new path city has degree two within H and thus no other incident tour edge. The path endpoints v and z_t each have exactly one remaining incident edge. Contracting the path gives a Hamiltonian cycle on the m old cities. When m>=3 the two endpoint neighbors in W are distinct: if they were the same j, the cycle consisting of the path and those two endpoint edges would omit all other old cities, contradicting connectedness. Thus y is an ordinary 0/1 tour incidence vector. Conversely the expansion above supplies every old tour. Convex-hull linearity now proves

    P_TSP(m) = image(C_{m,N}),
    xc_psd(P_TSP(N)) >= xc_psd(P_TSP(m)).

This checks the equations in the lift directly via section 2. It does not presume that TSP polytopes literally include one another as coordinate faces.

## 6. Exact exponent transfer, conditional on matching

Assume some a>0 and even threshold n_0 satisfy

    xc_psd(P_PM(n))>=2^{a n} for every even n>=n_0.

The original 3n construction and padding give, for n=2 floor(N/6),

    xc_psd(P_TSP(N))>=2^{a(2 floor(N/6))},

provided n>=n_0. Since n>N/3-2, this implies a TSP exponent c for every fixed 0<c<a/3 and all sufficiently large N. For a concrete bound, n>=N/4 for N>=24, so c=a/4 works beyond max(24,3n_0+6).

The compressed 2n construction gives the sharper fully explicit bound

    xc_psd(P_TSP(N))>=2^{a(2 floor(N/4))}

for n=2 floor(N/4)>=n_0. Since n>N/2-2, every fixed 0<c<a/2 works eventually. For example n>=N/3 for N>=12, so c=a/3 works beyond max(12,2n_0+4). These are constant-factor exponent losses, not the square-root loss from an n^2-city construction.

The premise quantifies over all sufficiently large even matching sizes. If a separately audited upstream theorem covers only an even arithmetic subsequence with bounded gaps, first pad matching via a face fixing new vertices into specified disjoint pairs: P_PM(n) is an affine image of that face of P_PM(n+2s). This supplies monotonicity in even sizes, and a bounded-gap subsequence is enough for a linear exponent. If the matching gaps are not uniformly bounded, that additional claim requires separate analysis.

## 7. Optional complex convention

If complex Hermitian PSD lifts of size r are discussed, the realification X -> [[Re X,-Im X],[Im X,Re X]] preserves positivity and defines a real affine slice of size 2r with the same output. Hence xc_psd_real(P)<=2 xc_psd_complex(P). A real lower bound 2^{cN} therefore implies a complex lower bound 2^{cN-1}, retaining exponential order. This is a separate conversion and is not part of the real convention above.

## 8. Reproducible finite checks

Run `python3 checks/tsp_reduction_check.py --output checks/tsp_reduction_results.json` from the project directory. The script independently enumerates perfect-matchings pairs for n=2,4,6,8; builds both gadgets as actual simple graphs; rejects disconnected pairs; verifies degrees, tour connectedness, matching projections, equal city counts, and surjectivity for every matching. It compares n=2 original and n=2,4 compressed faces with exhaustive Hamilton-cycle enumeration in the ambient complete graphs. It enumerates all tours in path-padding faces for (m,N)=(3,4),(3,5),(4,5),(4,6),(5,6),(5,7), verifies each projected vector is an old tour, and checks that every old tour has a preimage. Negative controls detect the omitted forced-diagonal conditions and disconnected matching-pair subtours. These checks support the construction but do not replace its proof or validate the exponential matching dependency.
