# Turn 1: exact isolated-vertex normalization

Problem 30003973 / OWR-16627-005. The original implication remains unresolved. This turn tests whether isolated-vertex padding could supply a counterexample and proves that it cannot: every counterexample reduces to one with no isolated vertices. No novelty claim is made for these elementary reductions or the illustrative reverse-direction example.

## 1. Conventions and the precise target

All graphs are finite and simple. A copy is an ordinary subgraph copy, not an induced copy. In particular, additional edges among the vertices of a copy are allowed. A q-edge-coloring is a map E(G)→{1,...,q}; unused colors are permitted. Write G→_q H when every such coloring contains a monochromatic H, and H≡_q H' when this property is identical for every finite host G.

This last definition agrees with equality of the source's families of q-Ramsey-minimal hosts. One direction follows because every Ramsey host contains a minimal Ramsey subgraph by finite descent. The converse follows because membership and nonmembership of every proper subgraph, hence minimality, are determined by the whole Ramsey-host class. Thus no weakening to equality of numerical Ramsey numbers is being made.

The source question is whether H≡_2 H' implies H≡_3 H'. Original Question6 is on printed p2736 of OWR44/2018. Clemens–Liebenau–Reding, arXiv1809.09232v2, Theorem1.5, credits the known transfer for nested targets; Observation1.6 proves additive color transfer and thus transfer to every even color count. Savery's author paper, Question3(a), repeats the unrestricted question. None of those restricted conclusions alone answers it.

## 2. Padding identity

Let H be a graph with at least one edge. Delete all isolated vertices to obtain its edge-bearing core F; write h=|V(H)|. F has no isolated vertices, may be disconnected and has at least one edge. For every finite G and q≥1,

    G→_q H  iff  |V(G)|≥h and G→_q F.                 (1)

If G has fewer than h vertices it contains no H. Otherwise, in any fixed coloring, a monochromatic F can be extended by h−|V(F)| additional distinct vertices to a copy of H. The extra vertices require no edges in the chosen subgraph, and any ambient edges may simply be ignored. Conversely every monochromatic H contains a monochromatic F. This proves(1) for each coloring and then for the universal coloring statement. It is essential here that copies are not induced.

Also, adding isolated host vertices does not change whether a host is q-Ramsey for F, since F has no isolated vertices. Formally, for every t≥0,

    G⊔tK_1 →_q F  iff  G→_q F.                       (2)

Every edge-coloring of the padded host is exactly a coloring of G. In any F-copy all vertices meet an edge, so none can map to the new isolated vertices. This argument works for disconnected F as well as connected F.

## 3. Classification of equivalence after padding

For an edge-bearing graph F let r_q(F) be the ordinary q-color Ramsey number, the least n such that K_n→_q F. It is finite by Ramsey's theorem. Any host G with G→_q F has at least r_q(F) vertices: otherwise extending its coloring to a complete graph contradicts the defining minimality. More explicitly, G⊆K_n and Ramsey behavior is upward closed in the host, so G→_q F implies K_n→_q F.

**Proposition.** Let H,H' each have an edge, let F,F' be their cores and let h=|V(H)|, h'=|V(H')|. Then H≡_q H' if and only if both

- F≡_q F', so that r_q(F)=r_q(F')=:r
- max{h,r}=max{h',r}

hold.

**Necessity of core equivalence.** Given any host G, pad it with enough isolated vertices to obtain a host G* of order at least max{h,h'}. By(1) and(2), G→_q F iff G*→_q H; similarly G→_q F' iff G*→_q H'. The assumed equivalence gives core equivalence for every G. Taking complete hosts gives the common Ramsey number r.

**Necessity of the effective cutoff.** If the two maxima differ, say a=max{h,r}<max{h',r}=b, then K_a is Ramsey for both cores, has enough vertices for H, and has fewer than h' vertices. Thus it is Ramsey for H and not for H', a contradiction.

**Sufficiency.** For a host G of order n, core equivalence makes the two core arrow conditions identical. If they are false, both padded conditions are false. If they are true, n≥r, and the common maximum ensures that n≥h iff n≥h'. Apply(1). ∎

This is a theorem about **all finite hosts**. The computation below merely checks small instances of its elementary identities.

## 4. Reduction of the original problem

**Corollary.** The unrestricted2-to3 implication is true if and only if it is true for graph pairs having no isolated vertices. In particular, isolated-vertex padding cannot create a counterexample from cores that are3-equivalent.

The forward direction is restriction. For the reverse direction, let H≡_2 H'. First dispose of edgeless targets: an edgeless h-vertex target is Ramsey in a host exactly when its order is at least h, independently of q. Two such targets are2-equivalent only when their orders agree. An edgeless target cannot be2-equivalent to one with an edge, as arbitrarily large edgeless hosts distinguish them.

We may therefore assume both targets have edges. By the proposition their cores F,F' are2-equivalent and, with r_2 their common2-color Ramsey number,

    max{h,r_2}=max{h',r_2}.                           (3)

If the implication holds for isolate-free graphs, F≡_3 F'; write r_3 for their common3-color Ramsey number. Since a2-coloring is also a3-coloring with one unused color, r_3≥r_2.

If h=h', the3-color effective cutoffs are equal. If h≠h', equation(3) forces both h and h' to be at most r_2 and hence at most r_3, so again the3-color cutoffs coincide. The proposition now gives H≡_3 H'. ∎

The same proof works with3 replaced by any q≥2, conditional on equivalence of the cores at that q. A counterexample to the original implication must therefore already be present among edge-bearing, isolate-free cores. This closes the proposed padding route but leaves its genuine graph-theoretic difficulty intact.

## 5. A small reverse-direction control

Let P_3 be the path on three vertices, and let H'=P_3⊔K_1. These graphs are **not2-equivalent** but are **q-equivalent for every q≥3**.

For two colors, K_3→_2 P_3: among its three edges, two have the same color and meet. But K_3 cannot contain the four-vertex graph H'. Hence K_3 separates them.

For three colors, r_3(P_3)=5. To see the lower bound, color K_4 by its three perfect matchings; every color class is a matching and so contains no P_3. Every smaller host embeds in this coloring. For the upper bound, in every3-coloring of K_5, the four edges incident to any fixed vertex include two with the same color, producing P_3. Thus r_3(P_3)=5, and monotonicity gives r_q(P_3)≥5 for q≥3.

Since the two target orders3 and4 are then both below the common Ramsey threshold, the proposition proves their equivalence for every q≥3. This example is a simple boundary check of the reverse implication, not a counterexample to the requested2-to3 implication. The source gives stronger examples without isolated vertices, such as K_3 and K_3⊔K_2; those results are credited to the source and not re-proved here.

## 6. Checks and remaining gap

`verify_turn1.py` enumerates finite labeled host graphs up to five vertices. It computes Ramsey predicates by exact dynamic programming over partitions of the host edge set into H-free color classes. For bounded target cores and isolated padding it independently compares those predicates with(1), including targets too large for the host. It checks host-isolate invariance and the displayed small threshold witnesses. Its bounds and counts are explicit in TURN_1_CHECKS.json.

No finite host cutoff certifies universal Ramsey equivalence. No test identifies a new universally2-equivalent nonnested core pair, and no full answer follows from the normalized problem. Completion estimate for the original question:10% (exact boundary reduction, main isolate-free implication unresolved). Four substantive author turns remain after this checkpoint.
