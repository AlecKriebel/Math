# Mathematical scope and proof

Let D_4(N) be the maximum number of nonsimplex facets of a convex 4-polytope with exactly N vertices. Here degenerate means a facet with more than four vertices, not zero volume.

## 1. A previously established positive answer to the 2N question

Joswig and Ziegler's existence theorem gives, for every integer m >= 4, a convex cubical 4-polytope whose graph is the m-cube. We use that published theorem; we do not claim to reprove its construction. See [Neighborly cubical polytopes](https://arxiv.org/abs/math/9812033), Theorem 16.

Its vertex and edge counts are f_0=2^m and f_1=m*2^(m-1). Every facet is a combinatorial 3-cube, with six square ridges; every ridge belongs to exactly two facets. Thus f_2=3f_3. Euler's relation for the boundary 3-sphere gives f_0-f_1+f_2-f_3=0, hence

f_3=(f_1-f_0)/2=(m-2)*2^(m-2).

All facets have eight vertices and are degenerate. At m=10 the face vector is (1024,5120,6144,2048), so D_4(1024)>=2048=2*1024. The ratio f_3/f_0=(m-2)/4 grows without bound. This resolves the existential subquestion, and does not assert such a construction for every N or minimality of N=1024.

## 2. An elementary upper bound and why it does not finish the problem

Take any convex 4-polytope P on N vertices. Fix one ordering of all vertices and use its pulling triangulation on every proper face. Restrictions of these triangulations agree, so they give a simplicial triangulation K of the boundary 3-sphere with the same N vertices. Each original facet is triangulated into tetrahedra. A nonsimplex facet has more than four extreme vertices, all of which occur in its triangulation, and therefore needs at least two tetrahedra. If D is its number of nonsimplex facets and t=f_3(K), then 2D<=t.

Each triangular face of K is in two tetrahedra and each tetrahedron has four triangular faces, so f_2(K)=2t. Euler's relation now gives N-f_1(K)+2t-t=0, or t=f_1(K)-N. Since a simplicial complex has at most one edge on each pair of vertices, f_1(K)<=N(N-1)/2. Consequently

D_4(N)<=floor(N(N-3)/4).

This is a coarse bound, with no sharpness or novelty claim. Together with the cited published lower construction in REPORT.md it leaves a 3/2-versus-2 exponent gap. An existence theorem for an abstract or geometric sphere alone cannot fill it: convex realizability must also be proved. Neither the facet-count identities nor finite arithmetic tests supply that missing realization or a matching upper bound.
