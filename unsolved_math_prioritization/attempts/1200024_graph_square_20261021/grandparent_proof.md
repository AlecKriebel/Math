# Exact free spanning-forest degree on the binary grandparent graph

Authored mathematical proof, 21 October 2026. No publication action. This document addresses the original graph only; the square is bounded separately by a finite-network flow certificate.

## Statement and conventions

Let T be the (q+1)-regular tree, q >= 2, with a distinguished end xi. Every vertex x has one parent p(x), namely its neighbor towards xi, and q children. Let G_q be the simple graph on V(T) with edges {x,p(x)} and {x,p^2(x)} for every x. All edges have conductance 1. The end-preserving automorphisms of T act transitively on G_q. Hence G_q is connected, infinite, locally finite and vertex transitive. Its degree is (q+1)+(q^2+1).

The graph is genuinely nonunimodular under its full automorphism group, not merely under a chosen transitive subgroup. A parent-type edge lies in q+1 triangles: one through the parent's parent and q through the child's children. A grandparent-type edge lies in exactly one triangle, through the intermediate parent. Thus G_q determines which edges are the edges of T. Among the q+1 recovered T-neighbors of x, the edges of G_q form K_{1,q}; its unique degree-q center is p(x). Consequently every automorphism of G_q preserves the parent map, and Aut(G_q) is exactly the end-preserving automorphism group of T. The stabilizer of x fixes p(x), while the stabilizer of p(x) acts transitively on its q children, including x. The paired suborbit sizes are therefore 1 and q, which violates the standard unimodularity criterion. For q=2 these sizes are 1 and 2.

Write R_F for free effective resistance, defined as the decreasing limit of effective resistances in finite connected free subgraphs exhausting the graph. By the finite Kirchhoff edge-marginal formula and the definition of FUSF as a free exhaustion limit, for every edge {x,y},

P({x,y} belongs to FUSF(G_q)) = R_F(x,y).

No mass transport or unimodular trace is used here.

Let k be the positive root of

q k^2 + (2-q)k - 1 = 0,

and put A=1+qk. Then

R_F(x,p(x)) = 1/[1+(q+1)k],

R_F(x,p^2(x)) = 2/[3+qk].

Consequently

E deg_FUSF(G_q)(x) = (q+1)/[1+(q+1)k] + 2(q^2+1)/[3+qk].

For q=2 this simplifies to

k=1/sqrt(2),
R_F(x,p(x))=(3 sqrt(2)-2)/7,
R_F(x,p^2(x))=(6-2 sqrt(2))/7,
E deg_FUSF(G_2)(x)=(24-sqrt(2))/7,
b_F(G_2)=(10-sqrt(2))/14.

In particular, E deg_FUSF(G_2)(x)>161/50=3.22: indeed sqrt(2)<73/50 because 2<5329/2500, and (24-73/50)/7=161/50.

## Finite branch reduction

For a vertex u with parent a and grandparent b, define a finite branch B_m(u;a,b), m >= 0, as follows. Its interior consists of u and all its descendants through m generations below u. Its boundary consists of a,b. Include every G_q edge incident to its interior with both endpoints in this vertex set. Do not include the edge {a,b} in the branch. The untruncated descendant branch has no attachment to the rest of G_q except at a and b. In B_m, edges to descendants below the truncation are omitted, as required for a free boundary. Thus this finite branch is a two-terminal network attached at a and b.

Let k_m be its effective conductance between a and b. For m=0, the branch is the two unit edges a-u-b in series, so k_0=1/2.

For m+1, each of the q child branches of u has depth m and boundary u,a. Replace each by its equivalent conductance k_m. The remaining u-a conductance is 1+qk_m, and the u-b conductance is 1. The two are in series. Therefore

k_{m+1}=(1+qk_m)/(2+qk_m).

This sequence is increasing and bounded above by 1. For example, the map f(t)=(1+qt)/(2+qt) is increasing, f(1/2)>=1/2, and f(t)<1 for t>=0. Its limit k solves the displayed quadratic. The quadratic has exactly one positive root because its constant term is negative, so this identifies k uniquely.

The identity k=A/(1+A) follows directly from the fixed-point equation, where A=1+qk.

## Explicit finite free exhaustion

Fix x_0=x and its ancestral ray x_i=p^i(x), i>=0. For n>=2 and m>=0, construct H_{m,n} as the union of:

1. The finite ray x_0,...,x_n with all its parent edges and grandparent edges (that is, edges x_i-x_{i+1} and x_i-x_{i+2} whenever the subscripts lie in [0,n]).
2. For every child u of x_0, the branch B_m(u;x_0,x_1). There are q such branches.
3. For i=1,...,n-1 and every child u of x_i other than x_{i-1}, the branch B_m(u;x_i,x_{i+1}). There are q-1 branches at each such i.

Repeated boundary vertices are identified; all distinct edges retain unit conductance. This is a finite connected subgraph of G_q. It need not be declared induced for the argument: free spanning forests and free effective resistance can be obtained from any connected subgraph exhaustion. In fact, there are no missing edges between interiors of different branches because a grandparent edge always joins comparable vertices in the ancestor relation.

The family is increasing in each parameter. The diagonal H_{n,n} exhausts G_q. To check exhaustion, every vertex has an ancestor in common with x: its ray towards xi eventually coalesces with the ray x_0,x_1,... . If it is not on that ray, it lies in exactly one of the attached side descendant branches (or below x_0), at a finite depth. Thus it and all of its incident edges eventually belong to H_{n,n}.

Reduce each attached branch to its conductance k_m. The reduced finite network has vertices x_0,...,x_n. Every skip-one (grandparent) edge has conductance 1. The conductance of x_0-x_1 is

A_m=1+qk_m,

and the conductance of each x_i-x_{i+1}, i>=1, is

c_m=1+(q-1)k_m.

Now consider the effective conductance B_{m,n} between x_1 and x_2 in the subnetwork on x_1,...,x_n. This is the upper network after x_0 and its incident edges have been excluded. Let T_c(t)=c+t/(1+t). Eliminating successively from the upper end gives

B_{m,n}=T_{c_m}^{n-2}(c_m).

For completeness, with only x_1,x_2 the conductance is c_m. Adding one further vertex produces a direct conductance c_m in parallel with an edge of conductance 1 in series with the remaining upper conductance B. Thus the recursion is exactly c_m+B/(1+B). This is valid at every step because the only edges crossing the decomposition are the parent and grandparent edges stated above.

For fixed m, the recursion converges to the unique positive solution B of

B=c_m+B/(1+B).

More directly, on [c_m,infinity), the derivative T'_{c_m}(t)=1/(1+t)^2 is at most 1/(1+c_m)^2, and c_m>=1. Thus convergence to the fixed point is uniformly geometrically fast for all m. It follows that along the actual diagonal exhaustion m=n -> infinity,

B_{n,n} -> B,

where B is the positive root of B=c+B/(1+B), c=1+(q-1)k.

This root equals A. Indeed, c=A-k and k=A/(1+A), so A=c+A/(1+A). Uniqueness of the positive root follows from the quadratic B^2-cB-c=0.

## Resistances and degree

After all these finite reductions, the network relevant to x_0,x_1,x_2 is exactly the triangle with conductances

x_0-x_1: A_m,
x_1-x_2: B_{m,n},
x_0-x_2: 1.

Therefore

R_{H_{m,n}}(x_0,x_1)=1/[A_m+B_{m,n}/(1+B_{m,n})],

R_{H_{m,n}}(x_0,x_2)=1/[1+A_m B_{m,n}/(A_m+B_{m,n})].

Passing along H_{n,n}, A_n -> A and B_{n,n} -> A. Hence

R_F(x_0,x_1)=1/[A+A/(1+A)]=1/[1+(q+1)k],

R_F(x_0,x_2)=1/[1+A/2]=2/[3+qk].

End-preserving tree automorphisms take any parent edge to any other parent edge and any grandparent edge to any other grandparent edge. A vertex has q+1 incident parent-type edges and q^2+1 incident grandparent-type edges. Summing their Kirchhoff probabilities proves the expectation formula.

For q=2, substituting k=1/sqrt(2) and rationalizing gives the displayed simple radicals. The elementary inequality above proves the required strict lower bound without numerical approximation.

## Primary-source support and scope

- Pengfei Tang, *Weights of uniform spanning forests on nonunimodular transitive graphs*, arXiv:1908.09889v2, Section 5.2, defines the grandparent graph exactly this way. Theorem 1.3 and Propositions 5.8-5.9 prove additional structural properties, but those properties are not used in this calculation. https://arxiv.org/pdf/1908.09889
- Itai Benjamini, Russell Lyons, Yuval Peres and Oded Schramm, *Uniform Spanning Forests*, Ann. Probab. 29 (2001), 1–65, author-hosted corrected version of 27 January 2009. Theorem 4.1 gives the finite Kirchhoff identity; Section 5 constructs FUSF by free exhaustion and proves exhaustion independence; Proposition 7.1 gives convergence of free currents; the proof of Theorem 7.3 explicitly states the free edge-marginal identity. These portions were inspected through the web PDF text tool on 21 October 2026. https://rdlyons.pages.iu.edu/pdf/usf.pdf

The author-hosted *Probability on Trees and Networks* book was also sought, but its full PDF exceeded the web-fetch size limit. The foundation claim above relies on the actually inspected BLPS paper, not an assertion of full-book inspection.

The resistance computation in this document is an authored derivation, not a claim that the cited papers contain this exact formula. Nothing here asserts a literature novelty result or publishes any material.
