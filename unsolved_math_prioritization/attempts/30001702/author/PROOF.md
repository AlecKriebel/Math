# Facet counts for regular simplicial tori: audited-ready partial result

## Status and exact scope

Let m(d) be the smallest number of d-cells in a finite regular CW decomposition of T^d whose closed cells have the face structure of simplices. This is the simplicial-poset category in Satoshi Murai's contribution to OWR 08/2011, pp. 396–398, Problem 7. The question is whether m(d)=(d+1)! for every positive integer d. This note does **not** prove or refute that assertion in general. It proves restricted cases and gives an explicit remaining obstruction in dimension three. No novelty priority is claimed for consequences of established theorems.

A closed simplex here is embedded, with all of its vertices distinct. Multiple different cells can have the same vertex set. One-vertex Delta-complex models of a torus fail this regularity requirement and cannot be counterexamples.

## 1. A general homological identity and lower bound

Write n=d+1, let f_i count i-cells (f_{-1}=1), and define h by

sum_{k=0}^n h_k t^{n-k} = sum_{k=0}^n f_{k-1}(t-1)^{n-k}.

For reduced Betti numbers beta_j over F_2, define

h''_0=1,
h''_k=h_k-C(n,k) sum_{j=0}^{k-1}(-1)^{k-1-j} beta_j (1<=k<n),
h''_n=beta_{n-1}.

We use the established nonnegativity and symmetry of h'' for an orientable simplicial-cell homology manifold (Murai, Theorem 2.1, recording Novik–Swartz and Novik). The torus satisfies their hypotheses: it is a connected closed orientable manifold, and local homology in a simplicial-poset realization makes its links homology spheres. In particular h''_0=h''_n=1 and h''_k>=0.

For T^d, beta_0=0 and beta_j=C(d,j) for 1<=j<=d. The top h-number is h_n=(-1)^{d+1}, by evaluating the defining polynomial at zero and using chi(T^d)=0. For 1<=k<=d, Pascal's identity gives

sum_{j=0}^{k-1}(-1)^{k-1-j} beta_j = C(d-1,k-1)-(-1)^{k-1}.

Consequently, evaluating the h-polynomial at t=1 and applying Vandermonde's identity gives the exact formula

f_d = C(2d,d) + sum_{k=1}^d h''_k.                                  (1)

For completeness the two sums used here are

sum_{k=1}^d C(d+1,k) C(d-1,k-1) = C(2d,d),
sum_{k=1}^d C(d+1,k)(-1)^{k-1} = 1+(-1)^{d+1}.

The latter cancels h_0+h_n. Thus

f_d >= C(2d,d).

For d>=2, h''_1=h_1=f_0-d-1 and symmetry gives h''_d=h''_1. These are distinct positions, so

f_d >= C(2d,d)+2(f_0-d-1).                                         (2)

The central-binomial lower bound coincides with (d+1)! for d=1,2 but is strictly smaller for every d>=3. Indeed the ratio R_d=(d+1)!/C(2d,d) has R_3=6/5 and

R_{d+1}/R_d=(d+2)(d+1)/(2(2d+1))>1 for d>=2.

Equation (1) does not assert that every nonnegative symmetric h''-vector can be realized by a torus.

## 2. Sharp cases d=1,2

A regular decomposition of a circle has at least two vertices and at least two edges; the two-edge circle attains this. A two-dimensional closed simplicial-cell torus satisfies 3f_2=2f_1 and f_0-f_1+f_2=0. Hence f_2=2f_0>=6, because each triangle has three distinct vertices. The construction in Section 4 attains six. Therefore m(1)=2 and m(2)=6.

## 3. A dimension-three obstruction with precise category controls

Basak–Datta, Theorem 1.4 and Lemma 3.1(v) of arXiv:1308.6137v3, prove f_3>=24 for a contracted pseudotriangulation of T^3, meaning a regular simplicial-cell decomposition with exactly four vertices. Their category agrees with the present one. This does not alone settle decompositions with more vertices.

In dimension three, (1) reads

f_3=20+2(f_0-4)+h''_2.

Since every tetrahedron has four vertices, f_0>=4. Four vertices are handled by Basak–Datta, while f_0>=6 implies f_3>=24 directly. Thus any counterexample in dimension three must have f_0=5 and f_3 in {22,23}. The complete numerical possibilities below follow from f_2=2f_3, Euler characteristic zero, and the definition of h'':

- (f_0,f_1,f_2,f_3)=(5,27,44,22), h''=(1,1,0,1,1).
- (f_0,f_1,f_2,f_3)=(5,28,46,23), h''=(1,1,1,1,1).

In particular every decomposition of T^3 has at least 22 facets. Neither displayed numerical vector is claimed realizable or excluded.

One can sharpen the obstruction: the simple graph underlying its 1-skeleton must be K_5. To justify this step without assuming arbitrary decompositions are balanced, suppose instead that the graph is not K_5. A nonadjacent pair can receive one common color and the other three vertices three different colors. Every tetrahedron then contains all four colors. Form the dual 4-colored multigraph: vertices are tetrahedra and a dual edge through a triangle has the color omitted by that triangle. Every dual vertex has one edge of each color. Connectivity of links identifies original vertices of color c with components of the subgraph omitting color c.

If there is more than one such component, connectedness of the dual graph supplies an edge of color c joining two different components. Its endpoints form a 1-dipole. Cancelling it deletes two dual vertices and preserves the represented PL 3-manifold, by the Ferri–Gagliardi dipole theorem as stated in Murai, Lemma 6.1. Repeating until each color-deleted subgraph is connected produces a contracted pseudotriangulation with no more tetrahedra. The PL hypothesis holds in dimension three: vertex links are triangulated 2-spheres. Basak–Datta now forbids fewer than 24 tetrahedra, a contradiction. This argument establishes the bound for the 4-colorable subclass, not for arbitrary nonbalanced posets.

There is one more elementary necessary condition. Label the five vertices 0,...,4 and let a_i count tetrahedra missing vertex i. The global vertex map to the boundary of the 4-simplex sends the mod-2 fundamental cycle to a top cycle there. A triangle missing i,j lies in exactly two tetrahedron types, so the cycle equation says a_i=a_j modulo 2. Hence all five a_i have the same parity. Their sum is f_3; therefore all a_i are even for the 22-facet candidate and all are odd (and positive) for the 23-facet candidate. This is a condition on vertex-set multiplicities, not a construction or an exhaustive enumeration of gluings.

## 4. The factorial bound for unimodular lattice quotients

Let L be a full-rank lattice in R^d and let K be an L-periodic triangulation of R^d with vertex set exactly L. Suppose every d-simplex has Euclidean volume covol(L)/d!, i.e. it is unimodular relative to L. Let Gamma be a finite-index sublattice of L, and suppose the quotient K/Gamma is a regular simplicial-cell decomposition. Put q=[L:Gamma].

The quotient has exactly q vertices. An embedded d-simplex needs d+1 distinct vertices, so q>=d+1. Volume additivity on R^d/Gamma gives

f_d covol(L)/d! = covol(Gamma) = q covol(L),

and hence f_d=q d! >= (d+1)!. No flat realization, unimodularity, or lattice of lifts has been proved for an arbitrary simplicial-poset torus; this is an explicitly restricted theorem.

The restricted theorem is sharp in every dimension. Use the standard Kuhn triangulation of Z^d: in each translated unit cube and for each permutation pi, take the simplex with vertices

z, z+e_{pi(1)}, ..., z+e_{pi(1)}+...+e_{pi(d)}.

Take Gamma={z in Z^d: sum_i z_i is divisible by d+1}. This is a lattice of index d+1. Each simplex's vertices have successive, distinct coordinate-sum residues, so no two vertices in it are identified. More generally, if a simplex met its translate by a nonzero Gamma-vector, their intersection would be a nonempty common face of this triangulation, containing a lattice vertex; this would identify two vertices of the original simplex, a contradiction. Thus projection embeds every closed simplex and the quotient is regular. The face poset of each cell remains Boolean. Its realization is R^d/Gamma, a torus. There are exactly (d+1)d! facets. This independently verifies the upper bound used throughout this note; it is consistent with the type-A Steinberg construction of Dilks–Petersen–Stembridge.

## 5. Two unsuccessful extension routes

First, the usual staircase triangulation of a product of a p-dimensional and a q-dimensional simplex has C(p+q,p) top simplices. Starting from the factorial-sized torus decompositions above therefore yields (p+q)!(p+1)(q+1) facets in dimension p+q, exceeding the proposed optimum by (p+q)!pq for p,q>=1. This particular product route provides no counterexample. It is not a lower bound on all triangulations of a product.

Second, Avvakumov–Karasev's Corollary 1.2 applies to regular simplicial tori because their closed faces are contractible and the d coordinate classes in H^1(T^d;F_2) have nonzero product. It supplies f_d>=2^d, weaker here than (1). Their random-sign argument assigns probability 2^{-d} to origin containment of a generic simplex. Substituting 1/(d+1)! for that probability would be false; no factorial strengthening follows from that argument without an additional theorem. The 2026 publication is therefore not a full solution of the OWR question.

## Verification boundary

The included executable checks exact arithmetic identities, the two necessary numerical three-dimensional candidates, parity equations, and actual regular Kuhn quotients through dimension five. It verifies every lower interval in those examples, boundary-squared-zero, ridge incidence, and mod-2 Betti numbers through dimension four. Torus homeomorphism and the all-dimensional restricted theorem follow from the geometric proof, not from homology alone. The executable does not search all torus decompositions, certify a new minimal crystallization, or prove the universal factorial claim.

## References

- Original problem: S. Murai, “Face vectors of simplicial cell decompositions of manifolds,” in OWR 08/2011, pp. 396–398. https://doi.org/10.4171/OWR/2011/08
- S. Murai, Face vectors of simplicial cell decompositions of manifolds, arXiv:1010.0319, Theorem 2.1 and Lemma 6.1. https://arxiv.org/abs/1010.0319
- B. Basak and B. Datta, Minimal crystallizations of 3-manifolds, Electron. J. Combin. 21(1) (2014), P1.61; arXiv:1308.6137v3. https://doi.org/10.37236/3956
- K. Dilks, T. K. Petersen and J. R. Stembridge, Affine descents and the Steinberg torus, Adv. Appl. Math. 42 (2009), 423–444; Section 2.4. https://arxiv.org/abs/0709.4291
- S. Avvakumov and R. Karasev, Topological Lower Bounds on the Sizes of Simplicial Complexes and Simplicial Sets, Discrete Comput. Geom. 75 (2026), 661–666. https://doi.org/10.1007/s00454-026-00823-z
