# High-degree addendum: the authored graph has no Clebsch homomorphism

12 October 2026 UTC. This addendum supplements [SMALL_COMPLEMENT_PROOFS.md](SMALL_COMPLEMENT_PROOFS.md). It was reviewed as a separately frozen addition to the second-round work and is accepted with the main restricted results. No novelty claim is made.

## Graph and scope

Use the 15-vertex graph from Section 6 of the candidate. Its vertices are t, the three adjacent terminal pairs a_i,b_i (i=1,2,3), and y_ε for ε∈{0,1}³. Each y_ε is adjacent to t and to exactly one endpoint of each pair, selected by ε. The only other edges are a_i b_i. Its maximum degree is **8**, attained at t. It is triangle-free, but it is not subcubic and is **not a counterexample to the cubic weak pentagon conjecture**.

## Proposition

This graph has no homomorphism to any loopless triangle-free graph of maximum degree at most 7. In particular, it has no unrestricted homomorphism to the Clebsch graph, which is triangle-free and 5-regular.

**Proof.** Suppose f is such a homomorphism. Take different binary triples ε and η. At some coordinate i they select different endpoints of a_i b_i. If f(y_ε)=f(y_η)=h, then h is adjacent to both f(a_i) and f(b_i), while f(a_i) is adjacent to f(b_i). These are three distinct vertices: the source edges require distinct images because the target is loopless. They form a triangle, a contradiction. Therefore the eight values f(y_ε) are pairwise distinct. Each is a neighbor of f(t), so f(t) has degree at least 8, again a contradiction. ∎

For the stated Clebsch specialization, use vertices F2^4 and generators {e1,e2,e3,e4,J}. This target is loopless and 5-regular. A triangle would require the sum of three generators, counted with the edge multiplicities, to be zero. A repeated generator leaves a nonzero generator; three distinct unit generators do not sum to zero; and J plus two distinct units does not sum to zero. Thus it is triangle-free.

The candidate already separately proves that the displayed 32-edge bipartite cut is the unique global maximum up to side exchange and that its three-edge complement is a matching. The present argument strengthens its nonextension conclusion to the absence of every Clebsch homomorphism. It does not strengthen the claimed degree range.

The authored addendum checker checked the 28 pair-separation witnesses for the eight y-vertices, the graph's maximum degree and triangle-freeness, and the target's degree and triangle-freeness. The proposition itself is the complete argument above.
