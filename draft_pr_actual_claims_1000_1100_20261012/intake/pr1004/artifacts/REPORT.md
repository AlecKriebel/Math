# Higher-Grassmannian mutation comparison: partial boundaries

Problem 30005082. Assessment: 8 October 2026.

**Disposition: unfinished global target; five substantive approaches exhausted.** This package contains an authored correction of a local formula, exact higher-Grassmannian boundary tests, and a source-scope audit. It does not resolve the general mutation comparison or claim novelty.

## Target and hypotheses

The motivating question in [Oberwolfach Report 17/2022, p.917](https://ems.press/content/serial-article-files/46955) concerns the relationship between combinatorial mutations, cluster mutations and Escobar–Harada flip maps for higher Grassmannians. It follows a discussion of the known two-plane case. The catalogue's bare reference to maximal tropical cones must be restricted: a maximal cone need not define a toric degeneration.

Work with the standard Plücker coordinate ring of the complex Grassmannian `Gr(k,n)`. Its affine cone has dimension `k(n-k)+1`. For a cone-based toric degeneration, require that the initial ideal be prime and binomial. For an Escobar–Harada wall crossing, require two such cones sharing a codimension-one face and compatible full-rank valuations with a common projected valuation. Fix the lattices, grading and initial-term convention before comparing maps. A matching-field construction additionally needs coherence and the SAGBI/initial-ideal equality; coherence alone is insufficient. Cluster coordinates and arbitrary prime-cone valuation coordinates are not automatically the same.

A complete answer would characterize the comparison beyond the known families, with explicit coverage and map identification. None of the finite tests below supplies that coverage.

## Prior results and limitations

- [Clarke–Higashitani–Mohammadi](https://arxiv.org/abs/2010.04079) connect block diagonal matching-field polytopes by combinatorial mutations and establish their toric-degeneration property. These are prior results used to place the block examples below inside the valid class.
- [Clarke–Mohammadi–Zaffalon, v2](https://arxiv.org/abs/2206.13975v2) prove a pattern-avoiding permutation-family theorem. Their Example 5/Table 1 separates six prime types for `Gr(3,6)`, with EEEE unavailable to any matching field. The larger family is still the subject of their Conjecture 1; it must not be treated as proved. Their Example 6 supplies the coherent hexagonal family used in the negative SAGBI control below.
- [Clarke–Higashitani–Mohammadi](https://arxiv.org/abs/2208.04521) relate GT, FFLV and block matching-field polytopes. [Kowaki](https://doi.org/10.1007/s40879-025-00832-x) gives tropical-hyperplane criteria for particular matching-field mutations. These do not classify arbitrary maximal prime-cone wall crossings.
- [Higashitani–Nakajima, v2](https://arxiv.org/abs/2107.04264v2), Proposition 4.3 and Remark 4.4, give the cluster-to-combinatorial factorization. Section 6 discusses a max-convention extension, with explicit convexity cautions. The companion correction checks a defective displayed identity in Proposition 6.5 of that version. The published full text was unavailable in this inspection.
- [Rietsch–Williams](https://arxiv.org/abs/1712.00447v2) supply the rectangle valuation and the corresponding GT body. [Cho–Kim–Kim–Park, June 2026](https://arxiv.org/abs/2606.08570v1) extend cluster-controlled Newton–Okounkov families to partial flag settings; they do not assert that these exhaust all prime tropical-cone degenerations.

The established [Escobar–Harada general adjacent-cone theorem](https://arxiv.org/abs/1912.04809) and its published hypersurface semigroup counterexample are not a solution of this higher-Grassmannian target. The current search is bounded, not a certificate that no other result exists.

## 1. Additive transport by Plücker labels fails

For a triple `I={i<j<k}`, let `v_I^ell` be its `3x6` monomial exponent vector. Use `(i,j,k)` as the row labels unless exactly one element belongs to `{1,...,ell}`, when the first two rows are swapped. These are the block matching fields `B_ell`.

For the diagonal field `B_0`,

    v_134^0 + v_245^0 = v_145^0 + v_234^0.

For `B_1` the same equality fails: the difference is

    e_(1,3) - e_(1,4) + e_(2,4) - e_(2,3).

Therefore no additive map of the value semigroups can send every `v_I^0` to `v_I^1`. In particular no linear lattice map has that labeled action. This does not contradict their known mutation equivalence: a nonlinear mutation need not preserve sums or all generator labels. It also does not disprove an appropriately defined standard-basis wall-crossing bijection.

## 2. Local min/max factorization needs a correction

`CORRECTION.md` proves the ambient identities using a segment `F` orthogonal to the mutation direction `w`:

    Psi_min = phi_(w,F) o epsilon,
    Psi_max = phi_(-w,-F) o epsilon,
    Psi_min = phi_(w,F-F) o Psi_max.

Negating only `w` gives the wrong max formula in general. The defect occurs even at the rectangle valuation of `p_145`, not merely at an artificial ambient vector. The correction repairs a local algebraic identity. Convexity and global prime-cone coverage remain separate questions.

## 3. The unadjusted max extension is nonconvex in Gr(3,6)

Use the rectangle-coordinate order in the correction. For a triple `J`, put
`mu_i=3+i-j_i`, and let the `(r,c)` coordinate count the largest number of boxes on any diagonal of the rectangle `(c^r)` outside `mu`. This constructs the standard rectangle values. Its Newton–Okounkov polytope `P` is their convex hull.

At the `1x1` square set

    T_max(v)_(1x1) = -v_(1x1) + max(v_(1x2)+v_(2x1), v_(2x2)),

and leave all other coordinates fixed. The underlying exchange is
`p_356 p_246 = p_256 p_346 + p_236 p_456`.

Two points of `P` are

    u = val(p_145) = (0,0,0,0,1,1,0,1,2),
    v = val(p_356) = (0,1,1,1,1,2,1,2,2).

Their image midpoint is

    y = (3/2,1/2,1/2,1/2,1,3/2,1/2,3/2,2).

The map `T_max` is an involution. Its unique inverse image of `y` has first coordinate `-1/2`; all points of `P` have nonnegative first coordinate. Hence `y` is outside `T_max(P)` although its two endpoints are in that image. The image is nonconvex.

Thus this particular unadjusted map cannot be a flip between two convex Newton–Okounkov bodies in these coordinates. This is not a counterexample to the actual Escobar–Harada theorem, nor to the min-convention cluster map, nor to equivalence after a suitable coordinate identification.

## 4. Coherence and numerical agreement do not supply the missing bridge

Generate the coherent matching field from the integer matrix

    (0,  0,  0,  0,  0,  0)
    (18, 3, 15,  6,  9, 12)
    (42,35, 28, 21, 14,  7).

For every triple the determinant minimum is unique. Nevertheless its degree-two monomial semigroup has 174 elements, whereas the degree-two Plücker algebra has dimension 175. If the Plücker generators formed a SAGBI basis, these dimensions would agree. Thus this is not a toric degeneration supplied by that matching field. It is a reconstructed known excluded example, not a counterexample inside the required prime-cone class.

The valid block examples agree with the Grassmannian Hilbert dimensions through degree four: `1,20,175,980,4116`. The excluded field yields `1,20,174,968,4040`. Finite agreement is a regression control, not a proof of an all-degree SAGBI property or a converse mutation theorem. The positive block result is imported from the cited theorem.

## 5. Mutation equivalence does not imply direct cone adjacency

Let `A_0,A_1` be the `18x20` exponent matrices of `B_0,B_1`, ordered by the twenty triples. Exact rational elimination gives

    rank(A_0)=rank(A_1)=10,
    rank(stack(A_0,A_1))=12,
    dim(row(A_0) intersect row(A_1))=8.

Their tropical cone spans are these row spaces. Indeed, each weight in a cone is homogeneous on its monomial-free prime binomial initial ideal, hence annihilates the integer relations among the columns; equality of spans follows from dimension ten. Two adjacent maximal cones would have a common face of dimension nine. Their spans intersect in dimension eight, so these two labeled cones cannot be adjacent.

The known combinatorial relation of these block polytopes therefore does not by itself select a single Escobar–Harada wall. A path of compatible adjacent prime cones, and a comparison of its composed maps, still needs to be supplied.

## Verification and stopping boundary

`check_math.py` uses exact integers and fractions. It verifies the formula counterexample, all corrected identities on 2,401 rational test inputs, the nonconvexity certificate, the square exchange as an identity of determinant polynomials, block coherence, ranks, and finite Hilbert counts. The proofs above provide the universal local algebra and separation arguments. Source-based geometric identifications remain cited inputs.

Normal Python, `-O` and `-OO` runs agree byte-for-byte; explicit exception guards survive optimization. These checks do not independently establish all cited theorems. No novelty or journal-status claim follows from them.

After the five approaches, the exact global characterization remains unfinished: coverage outside known families, coordinate-normalized comparison for arbitrary relevant adjacent prime cones, and the treatment of non-degree-one-generated valuation semigroups are unresolved here. The correct queue outcome is exhausted `5/5`, retaining the local correction and partial boundary results.
