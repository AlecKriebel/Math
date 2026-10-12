# Independent audit: a scoped four-word pressing reduction

## Verdict and exact scope

**ACCEPTED without a mathematical correction.** The reviewed [reduction](FOUR_WORD_REDUCTION.md) proves necessary conditions for a disconnected original-threshold pressing-word graph with exactly four words. It does not classify four-word languages, prove general four-word connectivity, or prove the proposed one-column rigidity statement.

The complete authored reduction is preserved with the reference and publication-scope edits described in [PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md). The distributed proof and audit are identified in [MANIFEST.json](MANIFEST.json); no mathematical correction was required. This is an AI-assisted, unrefereed mathematical audit, not formal proof-assistant verification or a novelty assessment. The previously accepted restricted-move obstruction is a separate result and was not modified.

The accepted dependencies were read and checked for their required scopes:

- The accepted [trajectory-fiber theorem](../3100089_positive_connectivity_appendix/STRUCTURAL_LEMMAS.md) gives a Cartesian product of last-support layers, with single-position replacement preserving the entire trajectory, in arbitrary ambient dimension.
- The accepted [short-neighbor/two-word theorem](../3100089_short_neighbor_terminal_appendix/SHORT_NEIGHBOR_THEOREM.md) gives a distinct neighbor at LCS at least r−4 for every word of a nonunique language. In particular, a language with exactly two words has an edge.
- The Cooper–Whitlatch unique-root characterization is the named external theorem already used in the accepted short-neighbor proof. Its use here is confined to the two full-rank uniquely pressable restrictions in the proposed disjoint-edge case.
- The separately accepted [arbitrary-ambient rank-six theorem](../3100089_rank_six_overlap_appendix/RANK_SIX_CONNECTIVITY.md) proves connectivity at LCS at least two, and together with the lower-rank result covers ranks at most six. The statement in the reduction is supported by that broader accepted result, rather than only the earlier nonsingular rank-six corollary.

The original threshold is the common successful-word length minus four, as in Bixby, Flint and Miklós, [*Proving the pressing game conjecture on linear graphs*](https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf), Conjecture 6, printed p.47. The named root characterization is Cooper and Whitlatch, [*Uniquely Pressable Graphs: Characterization, Enumeration, and Recognition*](https://people.math.sc.edu/cooper/uniquely-pressables.pdf), Definition 7 and Theorem 1 in the author manuscript dated July 18, 2017. No other external theorem is imported.

## 1. Zero coordinates, rank, and exact fibers

A coordinate with an initially zero row remains zero under every press and cannot be pressed. Deleting all such coordinates preserves the successful words and all pairwise LCS values. Let N be the surviving label set, m its size, r the binary rank, and e=m−r. A legal press reduces full rank by one, so every successful word has exactly r distinct letters.

For a fixed successful word, Gram–Schmidt in the nondegenerate radical quotient supplies an orthonormal basis f₁,…,fᵣ. Let cⱼ(v) be the coefficient of xᵥ on fⱼ. Then

A = Σⱼ cⱼcⱼᵀ,
Mₖ = sum over j>k of cⱼcⱼᵀ. Define Lⱼ to be the labels whose highest nonzero coefficient is j. These disjoint nonempty layers partition N. At step j, a label in Lⱼ has full pivot column cⱼ, so any independent selection of one label from each layer has the same complete matrix trajectory.

Conversely, if a pivot produces the same transition, its update column d satisfies ddᵀ=cⱼcⱼᵀ. Taking diagonals over F₂ gives d=cⱼ. Independence of the coefficient columns then forces the label's highest nonzero coordinate to be j. Thus the trajectory fiber is exactly L₁×⋯×Lᵣ. This also shows why equality of a selected principal state, or mere congruence, would not be enough.

Write lⱼ=|Lⱼ|. Then Σⱼlⱼ=m and

|fiber| = ∏ⱼlⱼ = ∏ⱼ(1+(lⱼ−1)) ≥ 1+Σⱼ(lⱼ−1) = e+1.

The inequality follows by expanding the product into nonnegative integer terms. Every fiber is connected by changing one selected letter at a time; such a step retains r−1 letters, hence is an original-threshold edge. Therefore every component contains at least e+1 words. For a nonunique language the short-neighbor theorem separately excludes singleton components. If the whole graph is disconnected, it has at least two components and consequently

Z ≥ 2 max(2,e+1).

For Z=4 this forces e≤1. Thus all cases with at least two extra nonzero coordinates are excluded, in arbitrary rank. Rank zero is harmless: after zero-row deletion m=e=0 and the only word is empty.

## 2. Fixed-basis counting and the full-rank qualification

Let B⊆N select a basis of the rank-r radical quotient. Its principal Gram matrix A[B] is nonsingular. Restriction commutes with every press at a selected label, so a successful order on A[B] is legal in the full matrix. Its r presses reduce the full rank from r to zero, clearing every ambient coordinate. Conversely a full successful word using precisely B is successful on A[B].

A fiber has at most one word with selected set B. Indeed, a word in that fiber must select one letter from every disjoint layer; if B admits such a selection, membership determines each letter's position uniquely. Thus distinct successful words on B lie in distinct fibers, each with at least e+1 words. This proves

Z(A) ≥ (e+1) Z(A[B]).

The basis/full-rank hypothesis is essential. A rank-deficient restriction may have shorter successful words that do not clear the full ambient matrix. It must not be inserted into this argument merely because it is itself pressable.

## 3. Corank-one omission multigraph

Suppose e=1. Since the positive layer sizes sum to r+1, exactly one layer has size two and all others have size one. Every trajectory fiber therefore has exactly two words, differing at that layer's position. One omits label a and the other omits label b, with a≠b.

Associate one loopless edge ab to every exact trajectory. Parallel edges are permitted. Retain as vertices only labels omitted by some word. Successful words are exactly the endpoint incidences of these edges. Hence |E(H)|=Z/2, and Z is even.

For v in this vertex set, some successful word omits v, so N\{v} is a full-rank coordinate basis. The basis/full-language correspondence above proves

deg_H(v) = Z(A[N\{v}]).

This identity is asserted on the omittable-label vertex set, whose restrictions have rank r. It is not asserted for every label in N. For example, the Gram matrix of e₀,e₁,e₀ has row masks (5,2,5). Every full word includes label 1. Deleting label 1 instead leaves a rank-one restriction with two successful one-letter words, although no full word omits label 1. This explicitly demonstrates the failure of an unrestricted version of the degree identity.

Let h be the unique nonzero kernel vector and K its support. The quotient-coordinate vectors have precisely the single relation Σᵥhᵥxᵥ=0. Removing v leaves a basis exactly when hᵥ=1: a relation among the remaining vectors would be a kernel vector whose v-coordinate is zero. Thus every omitted label belongs to K, while labels outside K are present in every successful word.

Fix a word omitting a∈K and let b be its last selected label in K, at position j. The radical relation gives xₐ=sum over v∈K\{a} of xᵥ. Each selected coordinate at position i is supported on orthonormal positions at most i and has coefficient one at i. The term x_b is therefore the only summand with a nonzero j-coordinate; every other summand has support below j. The sum has highest nonzero coordinate exactly j, without cancellation there. Hence a lies in b's last-support layer. The fiber edge is precisely the pair {a,b}. This proves the terminal-kernel-pair description with full-prefix legality already supplied by the exact fiber theorem.

## 4. Four words force two disjoint omission edges if disconnected

When Z=4, H has two loopless edges and every vertex degree is at most two. Two words incident at the same label v are the complete two-word language of the nonsingular restriction A[N\{v}]; the accepted two-word theorem joins them at deficit at most four. Their local words are full successful words by the rank-exhaustion argument. The two incidences of an individual edge are joined by its deficit-one fiber replacement.

If H's two edges meet, the within-vertex and within-edge connections join all four words. The same argument works for parallel edges. Therefore disconnection of the original graph requires two disjoint edges in H.

All four endpoint degrees are then one, so the four full-rank principal restrictions obtained by omitting those labels each have exactly one successful word. There are exactly two fibers, each containing two words. These are necessary conditions only: other original-threshold edges may connect the fibers even when the omission graph itself is disconnected. No converse is proved or used.

## 5. The one-column-union reduction

Assume the necessary two-disjoint-edge configuration and select the fiber with omission pair {a,b}. Let S omit a, with b at position j. Replacing b by a produces its companion word and the same full trajectory.

The Gram–Schmidt bases agree, not just their Gram matrices. Both residual selected vectors at position j are fⱼ because they have highest coefficient j equal to one; earlier projections remove all lower coefficients. The unchanged later coordinate vectors then produce the same subsequent basis vectors. Alternatively, the shared full update columns determine their pairings with every spanning quotient coordinate and hence determine the same fⱼ in the nondegenerate quotient.

In this common orthonormal basis, U has as columns the selected vectors in S-order. The companion root V keeps the same columns at all positions other than j and replaces column j by the coordinates of xₐ. That column has coefficient one at j and zero below j, so V is again unit upper triangular.

Each omitted-label restriction has exactly one word, by its endpoint degree one. The accepted unique-root characterization therefore puts both U and V in Mᵣ. Its connectedness qualification is satisfied: if a nonsingular matrix with a full successful word had two nonempty components, interleaving the component words would give more than one successful word.

The alternate columns must differ genuinely. If xₐ=x_b, then the nonzero relation supported on {a,b} spans the one-dimensional kernel. Thus K={a,b}, while every omission endpoint must lie in K. That contradicts the other edge's disjoint endpoint pair.

Consequently the whole corank-one coordinate configuration is the union of the r columns of a unique root U and one genuinely distinct alternate j-th column from another unique root V, agreeing with U in all other columns. Its Gram matrix is the original augmented matrix in the corresponding label order. To realize the proposed four-word disconnection it must also have another exact trajectory with a disjoint omitted-label pair.

This is a necessary representation. The assertion that every such one-column union has only its original trajectory remains unproved. This audit neither accepts that assertion nor uses bounded absence evidence to infer it.

## 6. Independent bounded checks

The checker was authored separately for this audit and imports no author search code. It directly enumerates all 33,867 symmetric binary matrices of orders zero through five, retaining all ambient coordinates in every rank-one press. The symbolic arguments above, rather than a finite screen, prove the arbitrary-rank reduction.

Exact counts in each execution mode:

- 31,743 pressable matrices, 282,731 successful words, and 202,175 complete trajectory fibers
- Complete Cartesian-product verification for every fiber
- 65,267 nonzero fixed-basis count inequalities, with exact restriction/full-language agreement
- 12,596 corank-one matrices and 61,922 two-word corank-one fibers
- 34,795 full-rank omission-endpoint degree checks and 60,844 kernel/basis equivalence tests
- 123,844 terminal-pair checks and 61,922 one-column root comparisons
- 1,646 fiber comparisons with both endpoint degrees one, confirming both unique-root conditions; 384 have genuinely distinct alternate columns
- 1,662 corank-one four-word matrices in this bounded family; none has a disjoint-edge omission graph

The last absence is reported only as a bounded fact and is not used to establish rigidity or any general classification. The nonzero count of distinct alternate unique columns also prevents the root comparison check from being vacuous.

Five negative controls reject: extending the degree identity to a rank-deficient restriction; lifting a shorter local successful word without exhausting ambient rank; replacing the product lower bound by equality; assuming every fiber's alternate root column is identical; and assuming every kernel-support label has degree two. Empty-rank conventions are separately checked.

Normal Python, `-O`, and `-OO` runs pass with identical results except for their recorded optimization flag. All conditions use explicit exceptions rather than removable assertions.

## 7. Accepted residual scope

A hypothetical disconnected four-word instance has either:

1. Exactly r nonzero coordinates, a nonsingular full-coordinate case; or
2. Exactly r+1 nonzero coordinates, with the necessary two-disjoint-edge omission configuration and the one-column-union form above.

The separately accepted arbitrary-ambient rank-at-most-six result excludes both possibilities in ranks at most six. The stated remaining cases are therefore of rank at least seven. Neither full-rank four-word connectivity nor corank-one one-column rigidity is established here. The previously accepted eight-vertex example is full rank and has a connected original four-cycle; it remains solely an obstruction to the specified restricted move system.
