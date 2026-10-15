# Source-only model and success criteria

Sealed before opening submission proofs or reviews. Timestamp: 2026-10-14T05:20:45.768542+00:00. Audit completion estimate: 25%.

## Exact target
Let D be the intrinsic Euclidean cone surface of the regular dodecahedron, with its twenty vertices marked. A short geodesic is a finite geodesic segment of positive length whose endpoints are vertices and whose open interior avoids all vertices. It can revisit faces, edges, regular points, or its starting vertex only at the endpoint. Edge segments are boundary cases. The target is universal, with no length, crossing-count, or itinerary bound: if its projected pentagon billiard type is A0, its endpoints have distance other than 2 in the dodecahedral edge graph. An argument only excluding closed saddle connections (distance 0) is insufficient.

Fuchs defines the types from endpoint angles alpha,beta, his Fig.8. In the pentagon, A0 is beta-alpha = 2*pi/5 (see p.506 first sentence and p.505 table); the interior angle is 3*pi/5. Orientation reversal/reflection and endpoint-side conventions must be checked explicitly, not assumed. N denotes the number of linear billiard segments; beta-alpha is a multiple of 2*pi/5 for N even, while alpha+beta is such a multiple for N odd. Degenerate side cases can satisfy both descriptions and require separate treatment.

## Primary geometric framework
The Fox–Kershner unfolding X of D is a degree-10 cyclic branched cover of D, with one point over each vertex and cone angle 18*pi there; genus81, stratum H(8^20). It also has a regular degree-60 translation cover to the double pentagon P=Pi5, genus2, with a unique cone point of angle6*pi. Over that point it has twenty points each with local degree3. Regularity alone does not mean arbitrary automorphisms of P lift, nor that arbitrary affine automorphisms of X descend to D. Any such use requires its own proof.

The double pentagon involution exchanges its two pentagons and has derivative -I. Its five regular fixed points are the five glued edge midpoints; the sixth fixed point is the unique singularity. A saddle connection setwise fixed by this involution has a regular midpoint fixed by it. Consequently its lift to X and image on D have physical midpoint at an edge midpoint (preimage count: 5*60 = 30*10).

## Independent mechanism family, prior to candidate
Promising route: prove A0 is exactly the virtual-Weierstrass class, i.e. projected saddle connection fixed by double-pentagon involution. This is a substantive endpoint-prong equivalence requiring the actual alpha,beta convention. Then a physical order-two rotation of D about the geodesic midpoint reverses the geodesic locally, hence globally by uniqueness on the regular locus. Its endpoints are exchanged. No rotation of order2 fixes a dodecahedron vertex because the vertex stabilizer has order3. If exchanged endpoints were at graph distance2, their unique common neighbor (graph girth5) would be fixed, a contradiction. Thus a valid A0-to-midpoint bridge would prove both the target and the already-known distance0 exclusion without bounded enumeration.

## Success and falsification criteria
1. Prove or independently verify the alpha,beta-to-hyperelliptic equivalence in the precise source convention, including itinerary parity, edge trajectories, and singular endpoint prongs.
2. Prove the relevant midpoint is regular and a physical edge midpoint; do not permit an interior singularity or replace geometric midpoint by arbitrary crossing.
3. Establish actual physical half-turn symmetry at that midpoint and equality of the entire parameterized geodesic with the reversed half-turn image by uniqueness. Do not assume projected path embedded.
4. Verify the graph obstruction: two distinct distance2 vertices have exactly one common neighbor; halfturns have no fixed vertices.
5. If using a cover lift/descend route, specify the cover, deck group, local ramification, normalized subgroup, and all compatibility maps.
6. Any reduction to finitely many classes must prove it covers every source-defined A0 saddle connection, not only numerical examples.
7. A discovered unsupported equivalence or counterexample is a gap in the submitted proof, not by itself a counterexample to the conjecture. Novelty is not presumed.

## Source read depths
Fuchs: local text pp.501–503 plus complete displayed definition; visual pp.502,505,515; text pp.514–515; additionally earlier basic definitions and p.506 remark. Platonic-solids article: definition/unfolding §§2.1–2.2, strata §2.3 excerpts, covering/Veech §2.4, symmetry-descent §3 excerpts, complete displayed §§4.1–4.3 and §5 through Cor.5.5. No computational source appendices read. No candidate or opinions read.

Sources: https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf (Fuchs 2021, DOI10.1007/s40598-020-00170-8); https://arxiv.org/html/1811.04131v2 (Athreya–Aulicino–Hooper). Primary bodies remain private.
