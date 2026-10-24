# Exact scope reductions and a known rationality subclass

Checkpoint 2026-10-24T20:41:14.571732+00:00; derived reductions, no novelty or full-solution claim. Full discovery estimate10%.

## Finite support loses no ambient commutators

Let g∈[A(Γ),A(Γ)] be represented by a word on a finite set S of vertices. The full induced inclusion A(Γ[S])→A(Γ) is split by the map killing every vertex outside S; all defining commuting relations are preserved. Retraction places g in the smaller commutator subgroup. For every n≥1, monotonicity of commutator length under the inclusion and under the retraction gives equality of the two commutator lengths of g^n. Thus their scl values agree. This settles the potentially infinite defining-graph convention without restricting the question.

The same argument proves any full induced RAAG subgroup is isometric for scl on elements in its commutator subgroup. It does not apply to arbitrary subgroup embeddings, and it does not say every homomorphic image is isometric.

## Exact direct-product formula at the unstabilized level

For finitely many groups G_i and g_i∈[G_i,G_i],

cl_(product G_i)((g_i))=max_i cl_G_i(g_i).

The lower bound is projection monotonicity. For the upper bound write each g_i as a product of at most k commutators, where k is the largest of those lengths. Pad shorter expressions by [1,1]. Taking the componentwise generator tuples gives exactly k commutators in the product, with product(g_i). Apply this equality to all powers, divide by n, and use existence of each scl limit to obtain

scl_(product G_i)((g_i))=max_i scl_G_i(g_i).

The identity/abelian case has length and scl zero. Only finitely many factors matter for a finite-support element, so there is no exchange of an infinite maximum and limit.

## Join-indecomposable reduction

After the finite-support reduction, take Γ finite. The connected components Γ_i of the complement graph have all cross edges in Γ. Therefore Γ is their join and its Artin group is the direct product of A(Γ_i). The projections of a commutator-subgroup element remain in the respective commutator subgroups. If scl(g) were irrational, at least one of the finitely many factor values would equal that irrational maximum. That component group is an induced retract. Hence a hypothetical counterexample can be reduced to a finite support graph whose complement is connected.

This is not a free-product closure theorem. A disconnected support graph gives a free product; an arbitrary word may mix its factors. Rational elementwise scl in the factors alone is not used here to infer rationality for that arbitrary mixed word.

## Verified prior-input subclass

Calegari, *Scl, sails and surgery*, J.Topology4(2011),305–326, RationalityTheorem/Theorem3.14 (arXiv0907.3541v3), proves rational piecewise-linear scl in a finite free product of finitely generated free abelian groups. Root read the actual cached primary theorem statement, also recorded in priority/PRIORITY.md and SOURCE_MANIFEST.json. Thus a graph whose connected components are complete (a disjoint union of cliques) has rational scl for every eligible element.

Combining that prior theorem with the direct-product formula proves the same conclusion when Γ is a join of graphs each a disjoint union of cliques. This contains complete multipartite graphs and direct products of free products of free abelian groups. The conclusion is a straightforward application of credited known results, not an original contribution.

Every graph on at most three vertices belongs to this subclass. Exhaustive labelled-graph enumeration up to five vertices is in graph_subclass.py / graph_subclass.json, with isomorphism classes canonicalized by all permutations. On four vertices the only classes outside **this reduction** are P4 and P3 plus an isolated vertex. This does not assert that no other published method treats those graphs; it identifies the exact limit of the elementary subclass just proved. In particular, the free-product-of-PQL closure needed to treat all cographs is not silently assumed.

## Exact remaining gap

An arbitrary complement-connected non-cluster support graph, and every eligible word on it, remain in scope. A full positive answer needs an exact rationality mechanism beyond this subclass, with a surface realization matching any lower program. A negative answer needs an actual irrational value preserved in the ambient RAAG. Computable rational bounds, a 1/2 gap, or rationality of special chains are insufficient.
