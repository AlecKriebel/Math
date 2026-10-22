# Attempt 2: Aggregate the sharp graph theorem over links

Verdict: the exact link identity is proved, but the desired global aggregation fails. This is a substantive attempt at deriving the all-uniformity claim from the graph theorem, not an additional literature-search turn.

## The exact identity

For each (r−3)-subset A of V(H), form the ordinary graph L_A with an edge uv of color c whenever A∪{u,v} is a color-c hyperedge of H; vertices of L_A lie outside A. Write R_A,G_A,B_A for its color counts and τ_A for its number of rainbow triangles.

For an r-set S, let a_S,b_S,c_S count its red, green, and blue (r−1)-subsets. Then

Σ_A τ_A = Σ_{|S|=r} a_S b_S c_S.                            (3)

Proof: a rainbow triangle in L_A gives three differently colored hyperedges whose union is S=A∪{u,v,w}. Conversely, choosing one edge of each color in S gives three distinct deleted vertices u,v,w, since a hyperedge has only one color. Their common intersection is the unique (r−3)-set A=S\{u,v,w}. These constructions are inverse. In particular the same successful S can contribute more than once; counting it once is a different statistic.

Since a_S b_S c_S≥1 for every successful S, the known sharp graph theorem implies

T ≤ Σ_A τ_A ≤ √2 Σ_A √(R_A G_A B_A).                        (4)

Every hyperedge occurs in exactly q=binom(r−1,2) links, so Σ_A R_A=qR and similarly for G,B. Applying Cauchy–Schwarz and then expanding nonnegative sums gives

Σ_A √(R_A G_A B_A)
 ≤ √[(Σ_A R_A)(Σ_A G_A B_A)]
 ≤ √[(Σ_A R_A)(Σ_A G_A)(Σ_A B_A)]
 = q^(3/2) √(RGB).                                         (5)

The resulting bound T≤√2 q^(3/2)√(RGB) loses a factor depending on r and is weaker than the known √(6RGB) once r>3. Thus this aggregation alone is inadequate.

## A five-vertex obstruction to dropping the link multiplicities

Take r=4, V={0,1,2,3,4}, and color all ten triples as follows:

Red: 012, 013, 014, 023, 123, 234.
Green: 024, 134.
Blue: 034, 124.

Here (R,G,B)=(6,2,2). The successful sets are 0124, 0134, 0234, 1234, so T=4. Every one has color multiplicities (2,1,1); therefore the right side of (3) is 8. The four links A={0},{1},{2},{3} each have counts (4,1,1) and one rainbow triangle. The link A={4} has counts (2,2,2) and four rainbow triangles.

Hence Σ_A √(R_A G_A B_A)=8+2√2, whereas √(RGB)=2√6. In particular the tempting aggregation inequality Σ_A √(R_A G_A B_A)≤√(RGB) is false, even with every listed link containing a rainbow triangle. It is not enough simply to discard inactive links. This is not a counterexample to the original conjecture: T²=16<48=2RGB.

For r=4 one can describe the overcount exactly. Every successful 4-set has either three present faces, with multiplicities (1,1,1), or four present faces, with multiplicities a permutation of (2,1,1). If U is the number of successful sets with four faces present, then Σ_A τ_A=T+U. Accordingly (4) improves to T≤√2Σ_A√(R_A G_A B_A)−U. The example still shows that a separate cross-link resource inequality is needed.

## What can be safely aggregated

Suppose H is a union of hypergraphs H_i on pairwise disjoint vertex sets. A successful S cannot use hyperedges from two components: any two of its hyperedges intersect in r−2≥1 vertices. Thus T=Σ_i T_i. If each H_i satisfies T_i≤√(2R_iG_iB_i), then

T ≤ √2 Σ_i √(R_iG_iB_i) ≤ √[2(Σ_iR_i)(Σ_iG_i)(Σ_iB_i)].

The same proof works for any partition of the colored hyperedge families into blocks such that every successful S has all its present hyperedges in one block. For example define blocks as the connected components of the graph joining hyperedges whose intersection has size r−2. Any two faces of a successful S are adjacent, so each successful S belongs to one block.

This proves the conjecture for disjoint unions of common-core blocks from Attempt 1 and reduces a minimal counterexample to one intersection-connected block. The general link family is not such a partition: a single hyperedge occurs in q different links. Removing that reuse while preserving successful sets is the exact outstanding obstruction to this route.
