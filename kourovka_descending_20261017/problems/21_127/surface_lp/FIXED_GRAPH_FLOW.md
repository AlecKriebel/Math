# Exact coordinate-winding matching for a fixed graph of pieces

Status: proved local realization lemma, not a finite LP or a solution of 21.127. Prepared October 24, 2026 UTC. No originality claim for the elementary network-flow ingredients.

## Data and boundary of the claim

Let B be a finite graph. A vertex v carries a free abelian group Z^{I_v}. An oriented edge e from u to v carries Z^{I_e}, with I_e a subset of I_u intersection I_v; both edge maps are the coordinate inclusions. Loops and multiple edges are permitted. A vertex has fixed charge q_v in Z^{I_v}. Think of q_v as the sum of the labels of fixed boundary arcs in an annular vertex piece. The winding on the polygonal boundary after turn adjustments is

    w_v = q_v + sum_e epsilon(v,e) t_e,

where t_e belongs to Z^{I_e}, epsilon is +1 at the head and -1 at the tail, and a loop contributes once with each sign. A piece can be capped to a disk exactly when w_v=0, since its target is a torus. Let D be the set of vertices required to be disks. The other vertices are reservoirs: they remain ANNULI with an additional unconstrained interior boundary loop, carrying the inverse of the polygonal winding. That extra boundary is retained, rather than filled or silently cancelled. Its label is what is allowed to change. Increasing genus would NOT absorb a nonzero boundary homology class.

This is only a statement about winding adjustments for the specified finite graph. It does not claim that the reservoirs can be filled at zero cost in a surface with only the original prescribed boundary. In particular, it does not identify a relative surface optimization with absolute scl.

For each coordinate x, let B_x contain the vertices with x in I_v and exactly the edges with x in I_e. Vertices with no such edge remain as isolated vertices. The charge q_{v,x} is an integer.

## Exact relative-surface construction and Euler cost

At every vertex begin with an annulus. Its outer circle is subdivided into the fixed boundary arcs and turns prescribed by the piece data. Given turn windings, map this outer circle to the torus and map the annulus by retracting it onto the outer circle. The inner circle consequently carries the inverse of its outer winding, with boundary orientation. When and only when that winding is zero, the inner circle can be capped by a mapped disk, converting this vertex piece into a disk. Pair turns by opposite parametrizations through the corresponding edge cylinders. This constructs a surface mapping to the graph of tori. The original boundary arcs are unchanged, and the surviving reservoir inner boundaries are additional boundary components.

Thus the winding criterion is equivalent to an ACTUAL surface construction with the stated additional boundaries. If the graph has E paired-turn edges, its Euler characteristic is #capped pieces - |E|, by gluing pieces along intervals. In an M-fold pullback with all vertices over D capped except r exceptions, this is M(|D|-|E|)-r. This is an ordinary Euler-characteristic identity for these relative surfaces. It is not an identification with chi-minus or the absolute scl objective. Capping the surviving nonzero reservoir boundaries is explicitly NOT part of the construction.

## Theorem 1: exact finite matching

There are integral turn windings making every vertex in D a disk if and only if, for every coordinate x and every connected component C of B_x with all its vertices in D,

    sum_{v in C} q_{v,x} = 0.                         (1)

Necessity follows by summing the x-coordinate winding equations over C: every edge term cancels.

For sufficiency, fix x and a component C. If C has a reservoir, choose one as root; if not, choose any root and use (1). Choose a spanning tree, put all non-tree edge flows equal to zero, and eliminate leaves toward the root. At a non-root vertex v in D, choose its parent-edge flow to cancel q_{v,x} plus the already assigned child flows. At a non-root reservoir, do the same if convenient; this is allowed, since its winding need not be nonzero. All choices are integral. The root equation follows from (1) when there is no reservoir, and is unrestricted otherwise. Repeat independently for every coordinate. Coordinates of each edge assemble into an element of Z^{I_e}, so there is no compatibility condition left between them. This proves the theorem, including isolated vertices and loops.

## Theorem 2: asymptotic disk promotion in finite covers

Pull back the above graph, all coordinate labels, and fixed charges to finite covers p:B'->B of degree M. A vertex over D is called an exception if it is permitted to remain a reservoir. There are covers and integral adjustments with the number of exceptions o(M) if and only if the following condition holds:

> For every x and every component C of B_x all of whose vertices lie in D, if C is a tree then its total x-charge is zero.

The convention includes isolated vertices as trees.

**Necessity.** A tree has no nontrivial connected covering. Its inverse image consists of M copies of C. If its charge is nonzero, each copy must contain at least one exception by Theorem 1. Thus at least M exceptions are necessary, and o(M) is impossible. Different coordinates may share exceptions, but this lower bound for one fixed bad component remains valid.

**Sufficiency.** The finite collection of relevant components that are not trees each contains a nontrivial loop gamma_C. Inclusion of a subgraph injects its fundamental group, so this loop remains nontrivial in the free group pi_1(B). For any integer N>=2, residual finiteness gives a finite quotient in which none of gamma_C^j, 1<=j<N, is trivial, simultaneously for all these finitely many loops. Use the regular finite cover defined by its kernel. In each lift of C, the loop's monodromy has order at least N. Consequently every connected lift of C has covering degree at least N. There are therefore at most M/N connected lifts of each relevant C.

Choose one exceptional vertex in each connected lift of each non-tree all-D component with nonzero charge. The union of these choices has at most K M/N vertices, where K is the number of such base components over all coordinates, independent of M and N. Every other all-D component either has zero charge or has an exception. Theorem 1 now supplies all coordinate flows simultaneously. For N->infinity the loss divided by M tends to zero. Components having an original reservoir need no extra exception. For disconnected B, take common-degree disjoint covers of its finitely many components; the same argument applies.

The selected exceptional vertex can absorb arbitrarily large charge. This is allowed for annular reservoir pieces; imposing a bound on those windings would change the theorem.

## The P4 channels and a persistent obstruction

For P4=a--b--c--d, the clique-tree decomposition has vertex labels

    L={a,b}, M={b,c}, R={c,d},

with edge labels {b} on L--M and {c} on M--R. Thus the b- and c-flow graphs are different subgraphs of the graph of pieces. At middle vertices, the two channels do not mix.

Consider the 8-cycle of piece vertices

    M0 --b-- L0 --b-- M1 --c-- R0
       --c-- M2 --b-- L1 --b-- M3 --c-- R1 --c-- M0.

All vertices are prescribed disks. Put q_{M0,b}=1, q_{M2,b}=-1, and all other coordinate charges zero. Every individual vertex's charge is in the span of its incident turn coordinates, so each vertex can separately be made a disk. Nevertheless the b-subgraph has two tree components M0-L0-M1 and M2-L1-M3, with charges +1 and -1. Therefore simultaneous disk realization fails. In EVERY finite cover, at least one exception is required in each copy of each of these disjoint b-components, giving at least 2M exceptions.

There is no hidden global abelianization defect: total charge over the whole graph is zero in every coordinate. The obstruction is the location of charge in separate channels. This is a counterexample to promoting every separately adjustable piece by covers. These data can be realized by a prescribed TWO-component boundary chain. Give L0 outer arcs a,a^{-1}; L1 arcs a^{-1},a; R0 arcs d,d^{-1}; R1 arcs d^{-1},d. At M0 put b on the forward boundary and 1 on the reverse boundary; at M2 put b^{-1} and 1; put 1 on both arcs at M1 and M3. Set initial turn windings zero. The two boundary circles of the thickened cycle read

    w_+ = b a d b^{-1} a^{-1} d^{-1} = [ab,d],
    w_- = d a d^{-1} a^{-1} = [d,a].

The graph-of-tori edge paths collapse in the underlying clique tree, so these are the actual RAAG labels. The six zero-charge pieces can be capped, leaving a four-holed sphere with the two prescribed outer boundaries and two inner reservoir boundaries b and b^{-1}. No annulus can have the two prescribed oriented outer labels: killing c maps to Z^{a,b}*Z^d, where [ab,d] is not conjugate to [a,d], as their cyclically reduced abelian-factor syllables differ. Moreover killing a,c maps the boundary chain to the single free commutator [b,d]; homomorphism monotonicity of chain scl therefore gives scl(w_++w_-)>=1/2. Thus a putative all-disk promotion giving annuli or asymptotically zero cost for this chain would also fail globally.

This remains a chain example used to test a proposed surface mechanism. It is not an irrational element, not a proof about an arbitrary single input word, and not a counterexample to a carefully augmented LP.

## Remaining encoding gap

The theorems reduce exact matching on a specified graph to explicit integral constraints and classify its asymptotic promotion obstruction. The graph of pieces is NOT fixed in an scl computation. Its coordinate components can be arbitrarily large and overlap differently for different coordinates. A finite list of local turn multiplicities does not yet retain the all-disk tree-component charge conditions. No bound on component types, semilinearity theorem for their joint boundary language, or matching finite rational polyhedral description has been proved.

In addition, even an exact relative-disk optimization requires a theorem converting the non-disk reservoirs into an admissible surface for the original element with the claimed asymptotic Euler cost. Neither gap is replaced by the fact that the vertex tori have zero scl. This route remains incomplete for P4, and a fortiori for all RAAGs.
