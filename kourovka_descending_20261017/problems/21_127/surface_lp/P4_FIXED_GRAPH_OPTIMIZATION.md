# A finite matching computes the fixed-graph P4 relative disk loss

Prepared October 24, 2026 UTC. This extends `FIXED_GRAPH_FLOW.md` for the P4 clique-tree graph of tori. It is a finite optimization for covers of ONE GIVEN graph of pieces. It does not optimize over all gluing graphs, does not fill the remaining reservoir boundaries, and does not prove rationality of absolute scl.

## Data

Use the coordinate model of that note. A finite graph B has vertices of types L={a,b}, M={b,c}, R={c,d}. Every edge is a b-edge joining L to M, or a c-edge joining M to R. Multiple edges and disconnected graphs are allowed. The fixed charges q_v and the target set D are arbitrary.

For any finite degree-m cover of B, let r be the number of vertices over D left as annular reservoirs. The other target vertices must actually be mapped disks. Set

    alpha(B,D,q)=inf r/m,

where the infimum is over all such finite covers, integral turn assignments, and choices of reservoirs. The reservoir inner boundaries remain additional, unrestricted boundaries. This is the same local surface problem as in the preceding note.

First let F be the set of vertices in D of type L with q_{v,a}!=0, together with those of type R with q_{v,d}!=0. These are forced exceptions, since no turn can change the a- or d-coordinate. Define D0=D\F.

For x=b or c, call a component C of B_x bad if:

1. C is a tree;
2. all of its vertices belong to D0;
3. its total x-charge is nonzero.

Let U be the bad b-components and V the bad c-components. Make a bipartite multigraph H with vertex set U disjoint union V. Each middle vertex t lying in both a bad b-component C and a bad c-component E contributes one edge C--E. Vertices in D0 lying in just one bad component are also available as private choices to hit that component. Every bad component has at least one available vertex. Let nu(H) be the maximum matching size.

## Theorem

    alpha(B,D,q) = |F| + |U| + |V| - nu(H).          (1)

In particular this fixed-graph stable loss is an integer, and is computable by a finite rational bipartite-matching LP. The infimum need not be attained by one finite cover, since cyclic coordinate components can require an additional reservoir at every finite stage.

## Proof

Every forced vertex has m distinct lifts and each must be an exception, contributing m|F|.

A bad coordinate component is a tree. It has exactly m lifts in any m-cover, each mapped isomorphically to the base component, with the same nonzero total charge. By the finite flow criterion, each lifted bad component must contain an additional exception. A vertex can hit at most one bad b-component and one bad c-component. If it hits both, it is of middle type and gives one edge of the lifted incidence graph H'. The graph H' is an m-cover of H: each lifted tree component contains exactly one lift of each of its base middle vertices, so its incident edge types are preserved bijectively.

For a bipartite graph with vertex set W, where an edge can cover its two endpoints and a private singleton choice can cover any one vertex, the minimum number of choices covering W is

    |W| - nu.

For completeness, a maximum matching covers 2nu vertices using nu choices; cover each unmatched vertex by one singleton, giving |W|-nu choices. In the actual piece problem a genuinely private singleton need not exist: choose ANY piece of the unmatched component instead. It hits that component and may incidentally hit another component, which cannot increase the number of choices. Thus this construction is valid with the actual piece choices as well. For the reverse inequality, Konig's theorem provides an independent set of size |W|-nu (the complement of a minimum vertex cover). Each edge or singleton covers at most one member of that independent set, so at least |W|-nu choices are necessary. This includes isolated vertices and parallel edges. The matching/vertex-cover equality used here has its usual short alternating-path proof: from the unmatched vertices in the left class, let Z be the vertices reachable by paths alternating between unmatched edges left-to-right and matched edges right-to-left. Because the matching has maximum cardinality, Z contains no unmatched right vertex (an alternating path to one would augment it). The set (left minus Z) union (right intersect Z) meets every edge and contains exactly one endpoint of every matched edge, so is a vertex cover of size nu. Its complement is the required independent set.

Furthermore nu(H')=m nu(H). Lifting a maximum matching gives the lower bound. Lifting a minimum vertex cover gives a vertex cover of H' of size m nu(H), giving the reverse bound by Konig's theorem. Therefore every m-cover requires at least

    m(|F|+|U|+|V|-nu(H))

exceptions. This proves the lower bound in (1).

For the upper bound, select in the BASE graph an optimal hitting set E for the bad components, using the matching construction. It has |U|+|V|-nu(H) vertices and is disjoint from F. Treat F union E as permanent reservoirs, and lift this choice to any cover. Every tree coordinate component with nonzero charge now either had an original reservoir, contains a forced exception, or is one of the bad components and has been hit. Thus none of the remaining all-target charged tree obstructions survives.

Apply the finite-cover promotion theorem to the remaining targets D\(F union E). Its proof constructs covers with at most o(m) further exceptions in cyclic components and supplies integral winding assignments. The resulting relative surfaces have

    r <= m(|F|+|U|+|V|-nu(H)) + o(m).

Taking the infimum proves (1). The finite covers can be disconnected; no connectedness assertion is needed.

## What this achieves and what it does not

If e(B) is the number of paired-turn edges and non-target vertices are kept as annuli, the supremum of normalized ordinary Euler characteristics of these particular relative surfaces is

    |D| - e(B) - alpha(B,D,q).

All three terms are explicit for the given graph B. This repairs the false step of promoting every individually adjustable disk: the persistent charged tree components now carry an exact cost.

However an arbitrary admissible surface for a fixed boundary word can have a different graph B, different disk polygons, and a different number of pieces. No finite list or rational cone of all relevant B has been obtained. Moreover the extra reservoir boundaries require their own globally valid filling or gluing argument before an absolute-scl formula can follow. Formula (1) is therefore a local optimization lemma only. Its elementary graph-theoretic ingredients have not been claimed original in the mathematical literature.
