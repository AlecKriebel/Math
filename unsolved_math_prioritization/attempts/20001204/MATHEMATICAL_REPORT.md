# Quartic binary hierarchical models with a big facet

**Problem:** AIM-COMPUTATION-0042 / 20001204, AIM Computational Algebraic Statistics Problem 28.

**Status:** A proved restricted structural characterization, not a solution of the full problem. No claim of global novelty. The standard Lawrence and Graver-basis mechanisms below are credited explicitly. An additional three-facet characterization is given in Section 7.

## 1. Scope, conventions, and main statements

A simplicial complex contains the empty face. Its specified ground set may contain *ghost vertices*, meaning elements whose singleton is not a face. All states are binary unless expressly grouped into supervariables. The matrix A_Γ records all face margins, including the empty-face margin (total count). Recording only facet margins gives the same kernel and fibers. A move g has degree |g⁺|₁=|g⁻|₁. Let md(Γ) denote the smallest possible maximum degree of a Markov basis, with md=0 for a zero kernel.

A nonzero integer kernel vector g is **primitive**, or a Graver move, if no nonzero, distinct kernel vector h satisfies h⁺≤g⁺ and h⁻≤g⁻ coordinatewise. Let gd(Γ) be the largest degree of such a move, with gd=0 for a zero kernel. The finite Graver basis exists by Dickson's lemma; alternatively, only its conformal-decomposition property is needed below.

**Theorem A (quadratic Graver classification).** Let Γ be a binary hierarchical complex on a finite specified ground set. Remove its ghost vertices and call the resulting complex Γ° on its actual vertex set U. The following are equivalent:

1. gd(Γ)≤2.
2. Γ° is a simplex (including the simplex {∅} on U=∅), or Γ° has precisely two facets A and B with min(|A\B|,|B\A|)=1.
3. Γ° is flag and the graph of its missing edges is a star together with isolated vertices, allowing an edgeless graph.

This classifies a stronger invariant than quartic Markov generation; Theorem B explains why it answers a restricted part of the requested problem.

**Theorem B (big-facet quartic classification).** Let Δ be a complex on its actual finite vertex set W. Suppose F=W\{v} is a facet and v∈W. Put Γ=link_v(Δ), retaining the full specified ground set F; some elements of F can be ghosts of Γ. Then md(Δ)≤4 if and only if Γ satisfies Theorem A.

Equivalently, under these hypotheses exactly one of the following holds in the quartic class:

- Δ has exactly two facets. Then md(Δ)=2.
- Δ has exactly three facets F,H₁,H₂ and min(|H₁\H₂|,|H₂\H₁|)=1. Then md(Δ)=4.

If neither condition holds, md(Δ)≥6. This facet formulation assumes F is an actual facet and W has no ghosts. A saturated simplex Δ=2^W has md=0 but does not satisfy that big-facet hypothesis, because W\{v} is not maximal.

In particular, a big-facet complex with four or more facets cannot be quartic. This is a structural test from facets, not a Markov-basis computation for each input.

## 2. Two elementary reductions

**Induced restriction.** A move of Γ|_S can be embedded into Γ by fixing all coordinates outside S at zero. Its margins vanish exactly when the Γ|_S margins vanish. Every conformal summand of an embedded move has the same fixed-coordinate support, so an embedded primitive move remains primitive. Consequently gd(Γ|_S)≤gd(Γ). The analogous zero-margin face of each nonnegative fiber proves md(Γ|_S)≤md(Γ) when the ambient vertices are actual. We use only the Graver statement in the proof of Theorem A.

**Ghost deletion.** If r≥1 ghost vertices are adjoined to Γ°, every column of A_{Γ°} is replaced by q=2^r identical copies. A primitive move of the repeated-column matrix is of one of two types:

- A degree-one difference between two copies of the same column.
- A lift of a primitive move of A_{Γ°}, splitting each signed coefficient among its copies without changing its sign.

Indeed, if opposite signs occur among copies of one original column, their unit difference is a conformal kernel vector, so primitivity forces the first case. Otherwise aggregation over copies is sign-preserving. Any proper conformal decomposition of that aggregate can be distributed among the copies, contradicting primitivity. Conversely a sign-preserving lift of a primitive aggregate cannot have a proper conformal decomposition. Thus

gd(Γ)=max(1,gd(Γ°)) when there is at least one ghost,

and gd(Γ)=gd(Γ°) otherwise. This remains valid when U=∅: A_{Γ°}=[1], and its repeated-column matrix has only linear primitive moves.

These are standard configuration arguments. The ghost description also appears in Bernstein–O'Neill [BO], Section 5, pp. 11–12.

## 3. Four small primitive obstructions

The following table specifies integer kernel vectors by their positive and negative multisets of binary cells. Vertex labels in the facet column are one-based; strings are in vertex order. Repetition denotes multiplicity.

| Complex Γ | Facets | Positive cells | Negative cells | Degree |
|---|---|---|---|---:|
| Three isolated vertices | [1][2][3] | 001,001,110 | 000,011,101 | 3 |
| Four-vertex path P₄ | [12][23][34] | 0001,0100,1110 | 0000,0110,1101 | 3 |
| Two disjoint edges 2K₂ | [12][34] | 0001,0100,1010 | 0000,0110,1001 | 3 |
| Four-cycle C₄ | [12][23][34][14] | 0001,0010,0100,1111 | 0000,0011,0110,1101 | 4 |

All four vectors are primitive circuits. Here are direct analytic certificates, requiring no external computation. For each row of the table, order its distinct displayed cells lexicographically, and let z₁,…,zₘ be the coefficients of a kernel vector supported on those cells. The following selected zero-margin equations are necessary:

- **Three isolated vertices:** the ordered cells are 000,001,011,101,110. The equations z₁+z₂+z₃=0, z₄+z₅=0, z₁+z₂+z₄=0, and z₁+z₅=0 force z=t(−1,2,−1,−1,1).
- **P₄:** the ordered cells are 0000,0001,0100,0110,1101,1110. The equations z₁+z₂=0, z₃+z₄=0, z₅+z₆=0, z₃+z₅=0, and z₁+z₃=0 force z=t(−1,1,1,−1,−1,1).
- **2K₂:** the ordered cells are 0000,0001,0100,0110,1001,1010. The equations z₁+z₂=0, z₃+z₄=0, z₅+z₆=0, z₁+z₃=0, and z₂+z₅=0 force z=t(−1,1,1,−1,−1,1).
- **C₄:** the ordered cells are 0000,0001,0010,0011,0100,0110,1101,1111. The equations z₁+z₂+z₃+z₄=0, z₅+z₆=0, z₇+z₈=0, z₁+z₂=0, z₅+z₇=0, z₁+z₅=0, and z₃+z₆=0 force z=t(−1,1,1,−1,1,−1,−1,1).

Direct substitution into all facet margins verifies the converse in each case. Each displayed generator has no zero coordinate and has a unit coordinate, so the supported integer kernel is exactly its integer span. A nonzero proper conformal kernel vector is impossible. This proves primitivity and the circuit property.

For every k≥3, the boundary complex ∂2^[k] is another obstruction: its integer kernel is generated by the parity vector g_x=(-1)^{x₁+…+x_k}, of degree 2^{k-1}≥4. To see this directly, fixing all but one coordinate gives g_{x with last bit 0}+g_{x with last bit 1}=0; doing so in every coordinate forces all entries from the entry at zero by alternating signs. Conversely these parity vectors have all proper margins zero.

## 4. Proof of Theorem A

First assume Γ has no ghosts. If Γ is not flag, it has a minimal nonface S of cardinality k≥3. Its induced restriction to S is ∂2^S, so Section 3 and induced restriction give gd(Γ)≥2^{k-1}>2.

It remains to consider flag Γ. Let H be the graph of missing edges, so Γ is the clique complex of the complement graph of H.

If H contains a triangle, Γ restricted to its three vertices is three isolated vertices. The first obstruction gives gd(Γ)≥3.

Now suppose H is triangle-free and contains two disjoint edges. The graph induced by their four endpoints must be 2K₂, P₄, or C₄. Indeed, there are zero, one, or two possible cross edges; if there are two, they must be disjoint, since adjacent cross edges create a triangle with one original edge. Three cross edges also create a triangle. The corresponding induced complexes of Γ are respectively C₄, P₄, or 2K₂, since the complement of P₄ is isomorphic to P₄. Section 3 again gives gd(Γ)>2.

A triangle-free graph with no two disjoint edges is a star together with isolated vertices. For completeness, if two edges ab and ac exist, every edge avoiding a would have to be bc in order to meet both, and that would give a triangle. If there is at most one edge the conclusion is immediate.

We have proved that gd(Γ)≤2 forces the star condition. Conversely, an edgeless missing-edge graph means Γ is a simplex and its kernel is zero. For a nonempty star, write c for its center, L for its nonempty leaf set, and S for all the isolated vertices of H. Then Γ has exactly the two facets

S∪{c} and S∪L.

Conditioned on each state s of S, a table is a 2×2^{|L|} matrix with its row and column sums fixed. Different s-strata have disjoint coordinates and independent constraints. A kernel vector in one stratum has columns (a_j,-a_j) and Σ_j a_j=0. Unless zero, there are i,j with a_i>0 and a_j<0; the four-cell unit rectangle using columns i,j is a conformal kernel vector. Thus every primitive vector is precisely such a quadratic rectangle. A primitive vector cannot involve multiple independent s-strata. Consequently gd(Γ)=2.

A complex consisting of two simplices A,B with one exclusive side a singleton has exactly this description, with S=A∩B. Conversely the star description has these two facets. This proves the equivalence for actual vertices. The ghost-deletion result proves the general statement.

## 5. Standard Lawrence identity and proof of Theorem B

The complex Δ in Theorem B is the binary Lawrence lifting of Γ:

Δ=2^F ∪ {T∪{v}:T∈Γ},

with downward closure understood. Split a table into its v=0 and v=1 slices. Its constraints are the Γ-margins of each slice, and their pointwise sum (the complete F-margin). Therefore its matrix has the same kernel and fibers as

Λ(A_Γ) = [[A_Γ,0],[0,A_Γ],[I,I]].

In particular every kernel vector is (g,-g), g∈ker_Z A_Γ.

The well-known Lawrence identity is

md(Δ)=2 gd(Γ).

We include its proof to make the result independent of an external black box. Every integer kernel vector g is a conformal sum of primitive vectors, by repeatedly extracting a proper conformal vector and induction on its l₁ norm. Thus any difference of two Δ-tables can be decomposed into conformal moves (g_i,-g_i). Applying these successively stays coordinatewise between the endpoint tables, so never leaves the nonnegative fiber. These lifted Graver moves form a Markov basis and have degree 2 deg(g_i).

For the reverse inequality take primitive g and the tables

u=(g⁺,g⁻),  w=(g⁻,g⁺).

They have the same sufficient statistic. In any table z of this fiber, the complete F-margin forces z₀+z₁=|g|. Put h=g⁺−z₀. The slice margins imply A_Γ h=0, and the pointwise bounds 0≤z₀≤|g| imply h⁺≤g⁺ and h⁻≤g⁻. Primitivity forces h=0 or h=g. The fiber therefore consists of exactly u and w. Every Markov basis must contain their difference, up to sign, and it has degree 2 deg(g). This proves the identity.

This mechanism is standard: see Sturmfels' Lawrence theorem as cited in [PS], Section 4, and the explicit ghost, cone, and Lawrence Graver descriptions in [BO], Section 5. The big-facet identification itself is [BS-N], Definition 3.4 and Proposition 3.5.

Theorem A now proves the link formulation. Since v is an actual vertex, Γ contains ∅, so the link is never the void complex. The case Γ°={∅} means Γ={∅} on ambient F, all of whose vertices are ghosts. It gives Δ=2^F ∪ 2^{\{v\}}, two disjoint simplices, and degree two. More generally if Γ° is a simplex, Γ has exactly one facet U. Because F is maximal in Δ, U is a proper subset of F, hence there is at least one ghost and gd(Γ)=1. Δ has exactly two facets F,U∪{v} and md(Δ)=2.

Otherwise Γ has precisely two facets A,B with min(|A\B|,|B\A|)=1. Then gd(Γ)=2, even with ghosts, and Δ has exactly the three facets F,A∪{v},B∪{v}. Its Markov degree is exactly four. If the criterion fails, Theorem A exhibits a primitive move of degree at least three and the Lawrence identity gives md(Δ)≥6.

## 6. Consequences and limitations

1. There is a genuinely higher-dimensional quartic family beyond merely attaching a new simplex along a face: any big-facet complex of the displayed three-facet form is quartic. This statement does not assert novelty over known Lawrence or other toric-fiber-product constructions.
2. The obstructions above yield indispensable moves of degrees 6,6,6,8 in their binary Lawrence liftings. For example [123][14][24][34] has an indispensable degree-six move, despite its link being a model with a quadratic Markov basis. Replacing *Graver* by *Markov* in Section 5 is therefore invalid.
3. The theorem classifies all complexes with a big facet, of arbitrarily high dimension and with arbitrarily many variables. It does not classify arbitrary complexes without a big facet. The K₄ graph model, for example, is outside this hypothesis.
4. No graph-minor statement has been inferred for arbitrary complexes. The missing-edge argument uses induced restrictions of flag complexes, not the Bernstein–Sullivant link/deletion minor notion, and not ordinary graph minors.
5. Unimodularity is not substituted for quartic generation. [BS-N] classifies normality of Lawrence-type complexes via unimodularity of their links; that is a different theorem and a larger class than the one classified here.

## 7. A companion characterization for complexes with at most three facets

This corollary combines classical leaf/cone reductions with a small transportation argument. These reductions are known, not claimed as new.

**Theorem C.** A binary complex with at most two facets has md≤2. Suppose it has exactly three distinct facets F₁,F₂,F₃, and set

 a=|(F₁∩F₂)\F₃|,  b=|(F₁∩F₃)\F₂|,  c=|(F₂∩F₃)\F₁|.

Then md≤4 if and only if either at least one of a,b,c is zero, or at least two of a,b,c equal one. In the second case, with all three positive, md=4. If all are positive and at least two are at least two, md≥6.

If, more specifically, a=1 and b,c≥1, then the exact degree is md=2^{1+min(b,c)}.

**Proof.** We first dispose explicitly of any ground-set ghosts. If a configuration matrix A has each column repeated q≥2 times, aggregate a table over those copies. Lift every move in a Markov basis of A by distributing its signed occurrences among copies, and include all degree-one transfers between identical columns. A feasible projected move lifts feasibly by choosing its negative occurrences from occupied copies; after following a base-fiber path, degree-one transfers achieve the desired distribution among copies. Conversely, aggregating any Markov path gives a base-fiber path, with zero steps discarded and degrees never increased. Thus column repetition changes md to max(1,md(A)). Deleting ghost vertices therefore preserves every threshold D≥1 and every exact degree at least two. We may now work on the actual vertex set.

If there is one facet, it contains all actual vertices and the model is saturated, so md=0 before ghosts are restored. If there are exactly two facets F₁,F₂, condition on each state of S=F₁∩F₂. The table in that stratum is a matrix indexed by the states of F₁\S and F₂\S, and the recorded margins are its row and column sums. Quadratic rectangles connect each such transportation fiber: given distinct tables u,v with the same sums, choose a deficit cell (i,j) with uᵢⱼ<vᵢⱼ. Row balance supplies j′ with uᵢⱼ′>vᵢⱼ′, and column balance supplies i′ with uᵢ′ⱼ>vᵢ′ⱼ. Subtract one from those two surplus cells and add one at (i,j) and (i′,j′). The move is feasible, preserves all sums, and reduces the l₁ distance by at least two. Repetition terminates at v. Apply this independently in each S-stratum. Consequently md≤2, also after restoring ghosts.

Now suppose there are exactly three facets. First remove variables belonging to just one facet, separately for each facet. Reattaching such a group is the known saturated-simplex attachment along an existing face, which preserves every Markov-degree threshold D≥2. Thus this deletion preserves the properties md≤2 and md≤4, and preserves the exact degree whenever it is at least two. This follows from the codimension-zero Lift/Quad construction [EKS, Theorem 4.3], together with the fixed-state zero-margin converse. In detail, projected base moves lift degree-preservingly by pairing occurrences with equal separator state; tables with the same projection are connected by quadratic transportation swaps. Fixing all added coordinates in one state realizes every base fiber as a zero-margin slice, proving the converse.

The variables belonging to all three facets are cone vertices. Conditioning on their complete state block splits the matrix into independent copies, so their removal preserves md exactly [EKS, Lemma 5.3(2)]. What remains has disjoint groups A,B,C of sizes a,b,c and facets A∪B,A∪C,B∪C. Regard the groups as supervariables with r=2^a,s=2^b,t=2^c states. This is merely a bijection of cells and margins; no approximation or added constraint occurs.

If one group is empty, one facet contains all remaining variables, so the reduced model is saturated. Reattaching the deleted pieces gives md≤2.

If all groups are nonempty and two have size one, the core is the 2×2×t no-three-way-interaction model. Taking one binary supervariable as the Lawrence coordinate identifies it with the Lawrence lifting of the ordinary 2×t independence configuration. Its primitive moves are exactly the quadratic rectangles by the proof in Section 4, so md=4.

If at least two groups have size at least two, restrict their supervariable states to three distinct values each and restrict the third supervariable to two states. Such state restriction is a face restriction of the nonnegative fibers: one-variable super-margins are recorded, and zero margins force all excluded states to have zero count. Hence the 2×3×3 no-three-way-interaction model is a fiber face of the core. It is the Lawrence lifting of 3×3 independence. The six-edge cycle

 (0,0),(0,1),(1,1),(1,2),(2,2),(2,0)

with alternating coefficients +1,-1,+1,-1,+1,-1 is primitive for row and column sums. Its lift has a two-point fiber and degree six, by Section 5. Thus md≥6.

Finally, the primitive moves of an r×s transportation configuration are the signed simple cycles of K_{r,s}. A direct proof follows by interpreting a zero-margin table as a signed circulation and extracting a conformal directed simple cycle; a primitive circulation must equal one such unit cycle. Their maximal degree is min(r,s), since a bipartite simple cycle visits at most min(r,s) vertices on either side and a cycle of that size exists. Consequently the 2×2^b×2^c model has md=2 min(2^b,2^c), as claimed. This is the classical two-way transportation/ Lawrence mechanism, also consistent with [BO, Proposition 5.3]. ∎

Theorem C is another restricted classification, not a route to declaring the general AIM problem solved.

## 8. Prior work, source status, and novelty boundary

- [AIM] *Computational Algebraic Statistics*, version 27 March 2004, Problem 28, PDF page 8: https://aimath.org/WWN/compalgstat/compalgstat.pdf . The problem is in the section of Seth Sullivant's talk. “Elizabeth Allman” is the next heading; it is not reliable attribution of Problem 28.
- [KNP] Král', Norine, Pangrác, *Markov bases of binary graph models of K₄-minor free graphs*, https://arxiv.org/abs/0810.1979 . The complete graphical subcase is known and is not claimed here.
- [EKS] Engström, Kahle, Sullivant, *Multigraded Commutative Algebra of Graph Decompositions*, https://arxiv.org/abs/1102.2601v5 . Theorem 4.3, Lemma 5.3, and the graph gluing results explicitly supply prior mechanisms used here. The saturated-simplex attachment claim is covered on its forward side by this machinery; its converse is the standard fiber-face argument.
- [PS] Petrović, Stokes, *Betti numbers of Stanley–Reisner rings determine hierarchical Markov degrees*, https://arxiv.org/abs/0910.1610v4 . This gives homological degree obstructions but not the full quartic classification. Section 4 discusses Lawrence configurations; Example 6.1 illustrates failure of a converse to their degree predictions.
- [BS-U] Bernstein, Sullivant, *Unimodular Binary Hierarchical Models*, https://arxiv.org/abs/1502.06131v2 . This classifies a different invariant and uses a different notion of simplicial minor.
- [BS-N] Bernstein, Sullivant, *Normal Binary Hierarchical Models*, https://arxiv.org/abs/1508.05461v2 . Section 3 identifies big-facet models with Lawrence liftings and classifies their normality, not their quartic generation.
- [BO] Bernstein, O'Neill, *Unimodular hierarchical models and their Graver bases*, https://arxiv.org/abs/1704.09018v2 . Section 5 explicitly describes nucleus, ghost, cone, and Lawrence Graver bases, including the transportation-cycle result. This is essential prior art for the present statements. Theorem A/B may be a direct corollary of this classification plus standard facts; no assertion of a new general invariant or new Lawrence construction is made.
- [Survey] Almendra-Hernández, De Loera, Petrović, *Markov bases: a 25 year update*, https://arxiv.org/abs/2306.06270v3 . Current inspected version is dated 9 January 2024.

Current primary metadata were checked on 10 October 2026 for [BO], [BS-U], [BS-N], [PS], [EKS], and [Survey]. No general solution of the AIM problem was located in the bounded search. Search absence is not a novelty certificate or a proof of open status. The authored contribution here is a self-contained restricted classification with exact obstruction certificates and explicit scope; its possible prior derivability must remain visible.
