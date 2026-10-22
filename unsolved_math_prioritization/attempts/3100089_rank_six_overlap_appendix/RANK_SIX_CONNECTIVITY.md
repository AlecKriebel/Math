# Rank-six pressing connectivity by a complete positive finite certificate

## Status and theorem

**Theorem.** Let A be any successfully pressable symmetric binary matrix of rank six, with an arbitrary finite number of coordinate labels. Its graph of complete successful pressing words, with adjacency LCS at least two, is connected and has diameter at most six.

At rank six, LCS at least two is exactly the original Bixby–Flint–Miklós condition LCS at least r−4, or at most four deletions and four insertions. Together with the previously accepted rank-at-most-five result, this establishes the original bound for every rank at most six, without a restriction on the ambient number of labels.

This is a computer-assisted finite-case proof after an all-ambient symbolic reduction, not a finite extrapolation in ambient size. It does not establish arbitrary-rank BFM connectivity or universal one-vector component preservation. No novelty claim is made.

The only mathematical dependencies are the accepted exact [full-state and trajectory-fiber lemmas](../3100089_positive_connectivity_appendix/STRUCTURAL_LEMMAS.md) and the [five-section terminal-coordinate and signature theorem](../3100089_short_neighbor_terminal_appendix/TERMINAL_COORDINATE_THEOREM.md). The latter was independently accepted in its complete five-section version; see the [complete terminal-coordinate audit](../3100089_short_neighbor_terminal_appendix/TERMINAL_COORDINATE_AUDIT.md). Its imported pressability-existence theorem is explicitly documented there. No no-isolated-word theorem, basis-exchange assertion, or withdrawn Cooper–Davis proof is used here.

## 1. Three all-rank facts used in the reduction

We use the following already proved facts, specialized where necessary to rank six.

1. Every legal press lowers full matrix rank by exactly one, and a successful rank-r word has length r. Gram–Schmidt along it produces an ordered orthonormal basis of its radical quotient. If its labels are s₀,…,sᵣ₋₁, then x_{sᵢ}=fᵢ+Σ_{j<i} lᵢⱼfⱼ.
2. At rank r≥3, any two successful words with the same first label are connected at LCS at least two by a path of at most two edges. This is the accepted shared-letter diameter-two construction on the rank-(r−1) suffixes, with the common first label prepended.
3. At rank six, let T start with a, and express x_a in the orthonormal trajectory basis of another successful word U. If the coefficient string is outside

   E={011111,101111,100011},

   then U and T are connected at LCS at least two by a path of at most four edges. This is Section 5 of the accepted terminal/signature theorem. The strings list coefficients in increasing basis-position order.

The third assertion is a positive bridge result, not merely the necessary-signature obstruction. It handles any two successful words of the full ambient matrix, including omitted labels and rank deficiency in the ambient coordinates.

## 2. Lifting a spanning-coordinate word back to the full matrix

We spell out the lifting fact because it is essential to an all-ambient conclusion.

Let V be the six-dimensional radical quotient of A. Suppose selected actual labels have quotient vectors spanning V, and let B be their principal Gram matrix. If a word of length six is successful for B, then that exact actual-label word is successful for the full A.

Indeed, at every prefix its current principal restriction agrees with the matrix obtained by performing the same presses in B: restriction commutes with the rank-one pressing update when the pressed label belongs to the selected set. Each pivot is therefore legal in the full matrix. The full rank starts at six and drops by one at each of the six legal presses. Its final rank is zero, so the whole original matrix is zero, including every omitted coordinate.

Equivalently, the six pivots exhaust an orthonormal basis of V, so every ambient coordinate has zero residual projection. This is not a congruence argument, a claim about only the selected submatrix, or a presumption that a new formal vector is an actual original label.

Both uses below involve actual labels: a profile certificate presses only the six chosen basis labels, while a first-label certificate uses those six labels and the actual target first label a. For the latter branch the certificate explicitly verifies that x_a is distinct from all six basis vectors, hence a is a different original label.

## 3. Normalization and the finite positive lemma

Fix any successful word S=(s₀,…,s₅) in A and its orthonormal trajectory basis f₀,…,f₅. The six coordinate vectors of S have a unit-lower-triangular coefficient matrix L. Its fifteen entries below the diagonal are arbitrary bits, so there are precisely 2¹⁵=32,768 possibilities.

For a candidate exceptional vector a, the three coefficient strings in E correspond to integer bitmasks

62, 61, 49,

respectively, with the coefficient of f₀ stored in the least significant bit. For each lower-triangular root and each of these three masks, consider the seven labelled vectors x₀,…,x₅,x₆, where the first six are the rows of L and x₆=a. They span V, and (0,1,2,3,4,5) is a successful word on their full seven-by-seven Gram matrix. The seventh vector may repeat an old vector in this formal configuration; the two certificate branches below handle that explicitly.

**Finite positive lemma.** For every one of the 98,304 root/candidate pairs there is a path of at most two LCS-at-least-two edges, starting at (0,1,2,3,4,5), of one of the following types:

- **Profile type.** Every path word uses only the six old labels. Its terminal word U has a nonexceptional coefficient profile for the vector a in U's trajectory basis.
- **First-label type.** The terminal word starts with label 6, and a is different from every row of L.

Every displayed word has length six, uses distinct labels, is legally pressed, and clears the entire seven-by-seven Gram matrix.

This lemma was checked using a complete positive witness collection, whose contents are not distributed in this prose edition. Its exact format, coverage, and verification conditions are stated in the [finite verification contract](FINITE_VERIFICATION_CONTRACT.md). It has exactly one record for each root, with exactly one entry for each candidate mask. The counts are:

- 96,308 profile-type entries: 96,306 have one edge and two have two edges;
- 1,996 first-label-type entries, all with one edge.

No case is discarded because a first press fails in a restricted configuration. No negative search conclusion is needed for the proof: each of the 98,304 inputs has an independently checkable positive witness of one of the two allowed types.

## 4. Completing the arbitrary-ambient rank-six proof

Take any two successful words S and T in the original A, and let a be the first actual label of T. Normalize S as in Section 3.

If x_a has a nonexceptional profile in S's trajectory, Fact 3 connects S to T using at most four edges.

Otherwise the profile is one of the three exceptional masks. Apply the finite positive lemma to the root L and this mask.

In a profile-type entry, replace each formal old label i by the actual label sᵢ. Every certificate word lifts to a full successful word by Section 2, and its LCS bounds are unchanged by this injective relabelling. Thus S is connected by at most two edges to a full successful word U in whose trajectory x_a has a nonexceptional profile. Fact 3 then connects U to T by at most four more edges. The total is at most six.

In a first-label-type entry, the checked distinction x_a∉{x_{s₀},…,x_{s₅}} ensures that label a is not one of S's six labels. Relabel formal 6 by this actual a and the old labels as before. All seven are actual distinct labels, and their vectors span V. Every certificate word therefore lifts to the full A, and LCS is preserved. The resulting terminal word W starts with a. Fact 2 connects W to T by at most two further edges. This branch uses at most four edges (in the supplied certificate, at most three).

These cases exhaust every possible actual first label of T. The theorem follows.

### Duplicate and zero coordinates

Ambient zero vectors never enter a successful word and are automatically cleared. Repeated quotient vectors among ambient labels cause no problem: S's selected vectors are a basis, so its six vectors are distinct. If x_a repeats one of them, a first-label certificate is expressly disallowed; the positive witness must be of profile type and presses only S's six distinct labels. The later positive bridge from U to T already holds for arbitrary labelled configurations, including duplicates. No identification of distinct actual labels is used to increase an LCS.

## 5. Independent verification contract

The verifier need not trust the search, its word counts, the reported list of critical pairs, or any successful-word enumeration. It checks:

1. Every root code 0,…,32,767 occurs exactly once.
2. Each root has precisely the three candidate masks 62,61,49, once each.
3. The lower-triangular vectors are reconstructed directly from the fifteen root bits, in row-major lower-triangle order.
4. Every initial and path word has six distinct labels and is replayed by the literal full seven-by-seven binary press rule to zero.
5. Every consecutive pair has LCS at least two, calculated directly.
6. Every path uses at most two edges.
7. A profile endpoint has a nonexceptional coefficient string. Its coefficients are independently recovered from the synthetic coordinate's entries in the successive pivot columns, not inferred from the search.
8. All words in a profile path use only old labels. A first-label endpoint begins with 6 and its candidate vector is different from all six old vectors.

The author’s verifier performs these checks with full binary matrices and ordinary dynamic-programming LCS. It does not enumerate words or use the builder's determinant recurrence, Gram–Schmidt implementation, or LIS routine. Its validation uses explicit exceptions, so Python optimization does not remove checks.

The [independent audit](RANK_SIX_AUDIT.md) accepted both this finite lemma and the symbolic all-ambient reduction, with no mathematical correction required. The audit reports complete replays in normal Python and both optimization modes.

## 6. Boundary of the result

This is an exact rank-six theorem, with no bound on the ambient number of vertices. Rank at most five was already accepted separately. Rank seven and higher at the original threshold are not covered: LCS at least two is weaker than LCS at least r−4 once r exceeds six.

The result uses no assertion that arbitrary new-letter words have nearby old-only representatives and does not contradict the previously proved unbounded augmentation recovery distance. It does not settle general component preservation. Its finite certificate resolves a bounded-dimensional case left by the all-rank structural theorem.
