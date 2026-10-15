# Independent adversarial geometry and upper-bound review

Scoped review completed 2026-10-07 05:14:56 UTC (2026-10-06 22:14:56 PDT).
Reviewer: internal independent geometry agent. This is **not** a full-package
review, a priority certification, a proof of the upstream exponential matching
theorem, or formal verification. The reviewer derived the constructions before
reading any other agent's reduction. `proofs/upper_bound.md` was reviewed.

Within this scoped assignment, geometry/projection/upper-bound completion is
100%; full core resolution and publication-package completion are not assessed.

## Exact size convention and monotonicity

For a nonempty polytope P, define its real PSD extension complexity as the least
matrix order r for which

    P = pi(L intersection S_+^r),

where L is an affine subspace of real symmetric r-by-r matrices and pi is an
affine map. Affine equalities are unrestricted. Matrix order is distinct from
the ambient vector-space dimension r(r+1)/2. A product of PSD cones is counted
by the sum of its block orders: impose off-block entries equal to zero to embed
the product in one cone of that summed order. Counting only the largest block
would make an arbitrary LP appear to have PSD size 1 and is not the convention
used here.

Let F={x in P: ell(x)=beta} be a nonempty exposed face, where ell(x)<=beta is
valid on P. Add ell(pi(X))=beta to the equalities defining L. The image of the
resulting affine section is exactly F: both inclusions follow directly from
the original lift's exactness. Thus taking a face cannot increase r, without a
Slater or bounded-lift assumption. Composing pi with any affine map proves the
same monotonicity for affine images. This argument allows affine maps and does
not silently require full dimensionality of P or F.

## Reconstructed 2n-city matching projection

Let n>=2 be even. In K_(2n), denote cities by a_1,...,a_n,b_1,...,b_n. Define

    F_n = {x in P_TSP(2n): x_(a_i,b_i)=1 for every i,
                              x_(a_i,b_j)=0 for i!=j}.

Each equality is a tight valid coordinate bound, since tour coordinates lie
in [0,1]. Equivalently, the single functional

    sum_i x_(a_i,b_i) - sum_(i!=j) x_(a_i,b_j)

has upper bound n and achieves n precisely on F_n. The construction below
establishes nonemptiness, hence F_n is a face.

Every tour in F_n uses a_i b_i and exactly one additional edge incident to each
a_i and b_i. Because all other cross-layer edges are absent, the additional
a-layer edges form a perfect matching M_A and the b-layer edges form a perfect
matching M_B. The linear coordinate projection y_ij=x_(a_i,a_j) therefore maps
F_n into P_PM(n).

For surjectivity, write an arbitrary matching on [n] as disjoint pairs
(u_1,v_1),...,(u_k,v_k), k=n/2. Keep its a-layer matching, all vertical edges,
and the b-layer matching

    b_(v_l) b_(u_(l+1)), l=1,...,k, with u_(k+1)=u_1.

The resulting cycle visits cities in the order

    a_(u_1),a_(v_1),b_(v_1),b_(u_2),a_(u_2),a_(v_2),b_(v_2),
    ...,b_(u_k),a_(u_k),a_(v_k),b_(v_k),b_(u_1),a_(u_1).

Interpret the displayed pattern cyclically as the four-vertex segment for each
pair, joined by the chosen b edges. Every city appears once before the closing
city. In particular, k=1 gives the square
a_(u_1),a_(v_1),b_(v_1),b_(u_1),a_(u_1); no loop is introduced. For k=2 the two
b edges are distinct. Therefore every matching incidence vector is attained;
linearity and convexity establish

    pi(F_n) = P_PM(n),
    sxc_R(P_PM(n)) <= sxc_R(P_TSP(2n)).

The face is not claimed to be isomorphic to the matching polytope: multiple
b-layer completions can have the same a-layer matching. Also, degree-two alone
is insufficient to make the union Hamiltonian; the cyclic joining step is the
essential connectivity check.

## Original Yannakakis 3n construction and attribution

The primary source was obtained and read:

M. Yannakakis, *Expressing Combinatorial Optimization Problems by Linear
Programs*, J. Comput. Syst. Sci. 43 (1991), 441--466,
DOI https://doi.org/10.1016/0022-0000(91)90024-Y.
Theorem 2 proof is printed p. 454, PDF p. 14.
Source URL:
https://www.tcs.tifr.res.in/~prahladh/teaching/2011-12/comm/papers/Yannakakis1991.pdf

The proof uses three equally sized vertex sets L,M,R, each of size 2n in the
source's notation, hence 6n cities for a matching instance on 2n vertices. With
our n denoting the matching-vertex count, it uses exactly 3n cities. L and R
each induce K_n, and the only other allowed edges are l_i m_i and m_i r_i.
Set all disallowed tour coordinates to zero, which defines a face. The middle
vertices have graph degree two and force both edges of each l_i-m_i-r_i path.
Thus every face tour induces perfect matchings on L and R. Every L matching
extends by exactly the cyclic-pair construction above, with each vertical edge
subdivided by m_i. Projection to the L coordinates is P_PM(n).

The two-layer 2n construction is a direct suppression of the middle vertices
with explicit fixed vertical coordinates replacing their degree-two forcing.
It must be credited as a compression of this established reduction, not as a
new lower-bound method. No priority claim about the compressed version is made
by this scoped review.

Private review copy SHA256:
fa18bfad6dd4b90a4711198053407022cf85ad9a7037266e69ad4d21f9ecad9b.
The downloaded PDF and extracted full text are review inputs only; do not
redistribute them in the publication payload without redistribution rights.

## Padding to every city count

For M>=3 add a new city v to K_M. Let

    G = {x in P_TSP(M+1): x_(1,v)=1}.

This is a nonempty face. Contract the forced edge by the linear map

    y_(i,j)=x_(i,j) if i,j!=1 and i,j!=v,
    y_(1,j)=x_(1,j)+x_(v,j) for j in [M] minus {1}.

A Hamiltonian cycle on M+1>=4 cities that uses 1v contracts to a Hamiltonian
cycle on the old M cities. The other neighbors of 1 and v are distinct: if
they coincided, a three-cycle would be an entire connected component, contrary
to Hamiltonicity on at least four cities. Thus contraction does not introduce
a repeated edge. Conversely, split city 1 in any old tour, moving either one
of its two incident tour edges to v and adding 1v. This is a new Hamiltonian
cycle in G, so the image is exactly P_TSP(M). Consequently

    sxc_R(P_TSP(M)) <= sxc_R(P_TSP(M+1)) for M>=3.

For arbitrary N>=4 put n=2 floor(N/4). Then n is even, 2n<=N, and
N-2n is in {0,1,2,3}. Repeating the proved one-city contraction gives

    sxc_R(P_TSP(N)) >= sxc_R(P_PM(2 floor(N/4))).

Since n>N/2-2, a lower bound L(n)=2^(alpha n) on matching transfers as
2^(2 alpha floor(N/4)); any asymptotic exponent below alpha/2 follows after
adjusting the threshold. If the shift-to-exact bridge supplies L(n)-1 instead,
the exact transferred bound is 2^(2 alpha floor(N/4))-1, still exponential in
N. The additive loss must not silently disappear from a nonasymptotic formula.
This is a conditional transfer only: this review does not validate L(n).

## Subset-flow upper bound

For N>=3 fix city 1 and let Q=[N] minus {1}, q=N-1>=2. The source/sink DAG has
vertices s,t and (S,i), where emptyset!=S subset Q and i in S. Its arcs are
s->({i},i), (S,i)->(S union {j},j) for j outside S, and (Q,i)->t, with labels
{1,i},{i,j},{i,1}. The internal state count is q*2^(q-1). The arc count is

    m=2q+q(q-1)*2^(q-2).

Indeed, for each ordered pair i!=j, there are exactly 2^(q-2) subsets S that
contain i and exclude j. This formula applies at the boundary N=3, giving
6 arcs. It equals 2(N-1)+(N-1)(N-2)*2^(N-3).

Every s-t path lists a permutation of Q, and its edge labels give a Hamiltonian
cycle. Each undirected tour has exactly its two orientations as paths. Let
z be a nonnegative flow with divergence +1 at s, -1 at t, and zero elsewhere.
The graph is acyclic because subset cardinality strictly increases between
states. If residual source flow is positive, follow positive arcs: conservation
prevents a stop at an internal state, and acyclicity guarantees arrival at t.
Subtract the minimum flow on the path. At least one positive arc vanishes, so
the process terminates after at most m subtractions. No nonzero residual flow
with zero source value can survive: an acyclic nonempty positive support would
have a source whose outgoing positive flow contradicts conservation. The
extracted path coefficients sum to one. Hence the feasible flow polytope is
the convex hull of unit path incidences and its label-sum image is exactly
P_TSP(N).

Use an m-by-m symmetric matrix X, force all off-diagonal entries to zero, and
impose these divergence equalities on its diagonal. X>=PSD iff all its diagonal
entries are nonnegative. This provides an exact real PSD lift of matrix order
m and proves independently

    sxc_R(P_TSP(N)) <= 2(N-1)+(N-1)(N-2)*2^(N-3) = 2^O(N).

No claim about algorithmic hardness or P versus NP is used. The upper bound
counts the full diagonal matrix order, rather than the largest scalar block.

## Finite checks, observed counts, and limits

`checks/independent_geometry_checks.py` uses Python's standard library only.
It was executed successfully; output is
`checks/independent_geometry_checks.json`.

* All pairs of matchings were enumerated for n=2,4,6,8. Hamiltonian face tours
  were 1,6,120,5040; numbers of extensions per matching were 1,2,8,48. The
  canonical cyclic completion and its 3n subdivision passed in every case.
* A separate all-Hamiltonian-tour enumeration for 4 and 8 cities gave exactly
  the same face-tour sets/counts, independently checking n=2 and n=4.
  The original six-city graph was also checked by enumerating every K_6 tour;
  exactly one tour lies in its face and projects to the unique matching.
* Forced-edge contraction was checked exhaustively for M=3,...,7, including
  equality of the complete image sets with all M-city tours.
  A separately implemented direct forced-path projection was checked for
  M=3,4,5 and each of 1,2,3 new cities. Negative controls reject disconnected
  matching pairs and verify an eight-city counterexample when the vertical
  coordinate-one equations are omitted.
* The subset DAG was constructed independently for N=3,...,8. Arc counts were
  6,18,56,170,492,1358. Every permutation path gave a valid tour, the image set
  equaled all tours, and each tour occurred twice. Deterministic exact rational
  convex combinations checked the +1/-1 conservation convention.

These finite checks catch construction and indexing errors. They are not a
certificate for the upstream exponential theorem or an infinite claim.
All infinite geometric statements above have direct proofs.

At this checkpoint the scoped geometry review found no substantive issue in
the constructions or upper bound. A material source theorem gap would still
block the unconditional exponential TSP conclusion; exact matching input must
be audited separately. A later review of the full manuscript, priority audit,
package, and metadata is still required.
