# Turn5: the residual-forest obstruction and a false shortcut refuted

AI-assisted proof candidate; independent review pending. Original unresolved5/5. No sixth author search. Intersection integrality and tight-set uncrossing are classical polymatroid theory; they are credited to Edmonds, with a self-contained special proof below. A primary author exposition checked is W. H. Cunningham, The Coming of the Matroids, Documenta Mathematica Extra Volume ISMP(2012),143–153, Theorem6 printed149–150, https://ems.press/content/book-chapter-files/27359?nt=1 . No novelty certification is made.

## 1. Tight partitions and intersection faces

Let x belong to an integral base polyhedron B(b). Its tight sets T={S:x(S)=b(S)} contain empty and V and are closed under union and intersection. Indeed additivity of x and submodularity of b force equality in the usual uncrossing inequality.

Choose a maximal inclusion chain of tight sets empty=S0<...<Sk=V and let A_i=S_i−S_{i−1}. Every tight set T is a union of whole blocks A_i. Otherwise S_{i−1} union (T intersect S_i), also tight, would be strictly between two consecutive chain sets. Thus the span of all tight constraint rows is exactly the span of the block indicators. The affine hull of the minimal face of B containing x is

y(A_i)=x(A_i), for all i.

This follows directly from finite strict slack in all nontight inequalities: a sufficiently small relative neighborhood in that affine space stays feasible. Its direction space is the set of vectors whose block sums are zero, and its dimension is n-k.

For two base polyhedra containing x, form their tight partitions A and C. Build a bipartite multigraph with one node per A-block and one per C-block, and one edge per coordinate, joining its two blocks. Let it have n edges,k+l nodes and c connected components. After negating the C-side equations, the joint block-sum matrix is the oriented incidence matrix of this graph. Its rank is k+l-c. Therefore the minimal intersection face has dimension

n-k-l+c,

the cycle rank of the graph. In particular x is a vertex of the intersection exactly when this bipartite graph is a forest.

If b1,b2 are integral and x is such a vertex, every block-sum right-hand side is integral (it is a difference of values on the tight chain). On a forest the unique edge-variable solution of these equations is integral by repeatedly removing a leaf and solving for its incident edge. This proves integrality of the intersection without assuming it from the fact that each polyhedron is integral. It is the two-chain incidence proof underlying classical polymatroid intersection.

## 2. Maximal-support symmetric feasible points

Return to the original B in the cube, with total sum0. Its negative is another integral base polyhedron, with rank function b^*(S)=b(V−S). Hence P=B intersect (−B) is integral and contains0. Choose an integer point v of P with maximum support size. Such a point exists because P is bounded and integral. Let Z={i:v_i=0}.

Every nonzero coordinate of v equals1 or−1 and saturates a valid cube bound in both B and−B. Consequently each such coordinate is a singleton in both tight partitions: the corresponding singleton or complementary subset is tight and cannot split a partition block. Delete these singleton edges from the bipartite tight-partition graph, leaving the graph on the zero coordinates Z.

This residual graph must be a forest. If it had a cycle, the joint face would have a nonzero direction supported entirely on Z. Since v is in the relative interior of each minimal face, their intersection would contain a nontrivial segment through v. The intersection of these two faces is integral: their block-product descriptions are integral base polyhedra, or equivalently apply the tight-partition intersection argument above. It has a distinct integral vertex w, with all coordinates outside Z still equal to those of v. At least one zero coordinate has become nonzero, increasing support and contradicting maximality. Thus v is a vertex of P, and its residual graph is acyclic.

Let k_+,k_- be the numbers of remaining blocks on Z for B and−B, and c the number of residual components. For a forest,

|Z|=k_++k_-−c,
dim F_B(v)+dim F_B(−v)=2|Z|−k_+−k_-=|Z|−c.

Here the nonzero-coordinate singleton factors contribute no dimensions. If Z is empty, both original faces have dimension0. If |Z|=1, the only residual edge is an isolated component and again both dimensions are0. Therefore any maximum-support symmetric feasible point with at most one zero coordinate gives an opposite vertex pair of B.

However a nontrivial residual tree can have positive original-face dimensions even though their intersection is a point. A forest does not imply each partition consists of singletons. This is precisely the obstruction this argument leaves unresolved.

## 3. An explicit warning: maximal support does not imply two original vertices

On V={0,1,2,3}, set b(empty)=b(V)=0. Set b(S)=1 for every nonempty proper S except b({0,1})=b({0,2})=2. This is one of the64 reduced four-element submodular functions from Turn1; its elementary square inequalities can also be checked directly.

Let v=(1,0,0,−1). Both v and−v belong to B. The vector−v is a greedy vertex. But

v=(1/2)(1,−1,1,−1)+(1/2)(1,1,−1,−1),

and both displayed distinct endpoints are greedy vertices of B. Hence v is not a vertex. Its tight partition is ({0},{1,2},{3}), whereas the tight partition at−v consists of singletons. The residual graph on coordinates1,2 is a two-edge tree, not two isolated edges.

Nevertheless v has maximum possible support in P=B intersect (−B). A balanced four-coordinate sign vector with no zero entries has two positive coordinates. Feasibility in B forces that positive pair to be {0,1} or {0,2}, since all other pair bounds are1. Its negative would require the complementary pair {2,3} or {1,3} to have bound2, but neither does. Thus P contains no support-four integer point, and every nonzero integer point in it has support2. The chosen v is therefore a maximum-support point without two original-vertex endpoints.

This is not a counterexample to the original conjecture: for instance (0,1,−1,0) and its negative are both vertices. It refutes only the tempting maximal-support shortcut and explains why intersection integrality alone does not finish the problem.

## 4. Exhaustive finite controls and final boundary

The checker re-enumerates every reduced table for n<=5, all zero-total ternary points feasible in both B and−B, and every maximum-support such point. It constructs tight partitions and checks the residual incidence graph is a forest, saturated-coordinate blocks are singletons, and the at-most-one-zero corollary holds. Output:4,276 accepted tables across n1–5;44,879 maximum-support points;223,953 acyclic edge checks. Among these points912 are not vertices of both original polyhedra. The first is the explicit n4 example above. Thus the implementation actively falsifies the overstrong conclusion instead of reporting a misleading general pass.

The five-turn outcome remains unsolved5/5. Proven scoped classes are ground size<=5 (and the corresponding zero-face block reduction), integral root-direction zonotopes, laminar upper-constraint bases, and translated sums of coordinate simplices. A minimum-ground-size counterexample, if one exists, can be reduced to at least six coordinates with all proper canonical ranks positive and outside those all-dimensional classes. The general residual-forest obstruction has not been eliminated. No finite search or special decomposition is claimed to cover every base polyhedron.
