# A fixed-rank-block criterion for simultaneous degree bounds

## Status and scope

This is an accepted restricted theorem and a delimited audit of a known method obstruction, not a solution of the unrestricted bounded-degree matroid-basis question AMR-029-0008. Neither the general two-sided additive `2Δ−1` theorem nor two separate one-sided outputs supplies the requested simultaneous additive `Δ−1` result. The fixed-rank reduction is an elementary consequence and refinement of the upper-only rounding argument of Király–Lau–Singh (KLS); no novelty is claimed. The obstruction originates in KLS, Remark 1.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

The complete general mathematical proofs are retained, conditional on standard polynomial-time submodular-minimization and rational-LP oracle tools as accepted dependencies. Those tools are neither re-proved nor implemented here. This is not a computational reproduction package: executable code, raw certificates, numerical instance definitions, explicit finite witnesses and basis lists, matrices, and tables are omitted. The finite examples are separately checked supporting evidence; their omitted inputs cannot be recovered from this edition alone and are not premises of the general theorems.

The unrestricted simultaneous additive Δ−1 guarantee remains unresolved by this work when the relevant component-incidence criterion fails. No novelty, priority, or exhaustive current-literature-status claim is made.

## 1. Model

Let `M=(V,I)` be a finite matroid, available through an independent-set oracle. The hyperedges `E` are explicitly listed indexed subsets of `V`; retaining indices permits duplicate constraints. Put

`Δ = max(v in V) #{e in E : v in e}`.

Assume `Δ≥1`. Costs `c_v` are arbitrary finite rational numbers, including negative numbers. Bounds may be rational, encoded in binary: replace each lower bound by its ceiling and each upper bound by its floor. This leaves the integral feasible bases unchanged and only strengthens the desired inequalities. Thus write integer bounds `l_e≤u_e` hereafter. Original integral feasibility is assumed for the original question.

Write `P(M)=conv{1_B : B a basis of M}` and

`L = min{c·x : x in P(M), l_e≤x(e)≤u_e for all e}`.

Then `L≤OPT`, where `OPT` is the optimum cost of an originally feasible basis. In this definition, `L` is the optimum after ceiling/floor normalization of the rational degree bounds. It is not the optimum of the potentially weaker unrounded rational-bound LP; no cost guarantee relative to that weaker benchmark is claimed. Empty hyperedges have already-feasible constant constraints and may be removed. A rank-zero instance is solved by the empty basis. All subsequent claims concern the ordinary nontrivial case.

A *fixed-rank partition* is a partition `P_1,...,P_k` of `V` such that

`sum_i r_M(P_i) = r_M(V)`.

Define its block-incidence number

`κ = max_i #{e in E : e intersects P_i}`.

This counts an edge only once for a block, however many elements it contains there. Necessarily `κ≥Δ` if all original indexed constraints are retained.

## 2. Restricted theorem

**Theorem A (fixed-rank blocks).** Given a fixed-rank partition, there is an independent-set-oracle polynomial-time algorithm returning one basis `B` of `M` such that

`c(B)≤L`, and `l_e−κ+1≤|B∩e|≤u_e+κ−1` for every `e` simultaneously.

Consequently, on the restricted class `κ≤Δ` (equivalently `κ=Δ` for the unpruned indexed system), this solves the exact requested additive `Δ−1` target, with the stronger cost bound `c(B)≤L≤OPT`.

This restriction does not require the hyperedges to be laminar or disjoint. Their number can substantially exceed `Δ`. Each hyperedge may meet many different blocks, and the block matroids need not be representable or uniform.

### Proof

For any basis `B`, independence gives `|B∩P_i|≤r(P_i)` for every `i`. Summing yields equality because both totals equal `r(V)`. Thus every basis, and hence every `x in P(M)`, has

`|B∩P_i|=r(P_i)` and `x(P_i)=r(P_i)`.

For each hyperedge define

`A_e = union{P_i : P_i intersects e}`, and `R_e = sum_{i:P_i intersects e} r(P_i)`.

Then `e⊆A_e` and `x(A_e)=R_e` for every `x in P(M)`. Replace the pair of degree constraints for `e` by the two upper constraints

`x(e)≤u_e`, and `x(A_e\e)≤R_e−l_e`.                 (1)

On `P(M)`, the second is exactly equivalent to `x(e)≥l_e`. The original and transformed LP feasible regions, and their integral feasible bases, are identical.

For `v in P_i`, an original index `e` contributes exactly one incidence to the new indexed upper system if `e` meets `P_i`, and zero otherwise. Indeed, when it meets `P_i`, either `v in e`, or `v in A_e\e`, but never both. Therefore the maximum incidence of (1) is exactly `κ`. Empty rows can be discarded, and identical upper rows can be merged by taking the smaller bound; either operation can only decrease incidence.

Apply the upper-only rounding lemma in Section 6 with the incidence budget `κ`, retaining the original index correspondence. It returns one basis of cost at most the transformed LP optimum `L`, satisfying

`|B∩e|≤u_e+κ−1`, and `|B∩(A_e\e)|≤R_e−l_e+κ−1`.

The fixed-rank identity `|B∩A_e|=R_e` transforms the second inequality into

`|B∩e|≥l_e−κ+1`.

Both inequalities concern the very same returned basis. This proves the theorem.

A rank is computable greedily with a polynomial number of independence queries. The partition condition and all `R_e` are therefore polynomially checkable. At most `2|E|` upper rows are created, each of at most `|V|` elements. Section 6 supplies a polynomial oracle algorithm, and the integer sizes and rational bit lengths grow polynomially. No knowledge of an optimal integral basis is used. ∎

## 3. Canonical blocks and the precise limitation of this reduction

The finest fixed-rank partition can itself be found in polynomial oracle time. Choose any basis `B_0`. On `V`, draw an undirected edge between `b in B_0` and `v not in B_0` whenever `B_0−b+v` is independent. Let `C_1,...,C_t` be the connected components of this graph, including isolated loops and coloops.

For `v not in B_0` that is not a loop, its fundamental circuit relative to `B_0` consists of `v` and exactly those `b` permitting this exchange. It follows that `B_0∩C_i` spans every element of `C_i`; isolated loops have rank zero. Hence

`r(C_i)=|B_0∩C_i|`, and `sum_i r(C_i)=r(V)`.

Conversely, suppose `A⊆V` has constant intersection cardinality with every basis. If an exchange-graph edge crossed `A`, its two associated bases would have different intersection cardinalities with `A`. Therefore no such edge crosses `A`, and `A` is a union of the `C_i`. This also proves that every fixed-rank partition is a coarsening of the component partition. The graph uses at most `|B_0|(|V|−|B_0|)` oracle tests.

For completeness, an equivalent numerical characterization of a constant-cardinality set is

`r(A)+r(V\A)=r(V)`.

The maximum intersection of a basis with `A` is `r(A)` by basis extension, and the minimum is `r(V)−r(V\A)` by extending a basis of the complement. These coincide precisely in the displayed condition.

It follows that the canonical components minimize `κ` among all fixed-rank partitions. Moreover, consider the specific class of reductions that retains each original upper row and replaces each lower row by a complement `A_e\e`, where `A_e⊇e` has constant cardinality in *all* bases of `M`. Every permissible `A_e` must contain each component touching `e`. Thus its incidence at each vertex is at least that obtained using the minimal anchors in Theorem A. In this precise indexed-row model, the canonical construction is pointwise incidence-minimal.

This last statement deliberately excludes deleting redundant constraints, combining duplicate rows, taking linear combinations, restricting to a smaller face, changing the matroid, and other algorithms. It is an obstruction to this particular complement strategy, not to the original problem.

## 4. An adaptive tight-face extension

The reduction becomes stronger when fixed ranks hold on a suitable face rather than on every original basis.

**Theorem B (tight-face certificate).** Let `x` be a feasible point of the original degree-constrained LP, and suppose an explicit chain

`empty=S_0 ⊂ S_1 ⊂ ... ⊂ S_k=V`

satisfies `x(S_i)=r_M(S_i)` for all `i`. Put `D_i=S_i\S_{i−1}` and form

`N = direct_sum_i ((M restricted to S_i) contracted by S_{i−1})`.

Compute the canonical fixed-rank components of `N`, and let `κ_x` be their block-incidence number for the original hyperedges. There is a polynomial oracle algorithm returning one basis of `M` with

`c(B)≤c·x`, and `l_e−κ_x+1≤|B∩e|≤u_e+κ_x−1` for all `e`.

In particular, if `x` is an optimal original LP point and `κ_x≤Δ`, the target follows with cost at most `L≤OPT`.

### Proof

The bases of `N` are exactly those bases of `M` saturating every chain rank. One direction follows by successively extending a basis of `S_{i−1}` to one of `S_i`; contraction describes precisely the added independent elements. In the other direction, a basis saturating the chain has exactly `r(S_i)−r(S_{i−1})` elements in each `D_i`, forming a basis of the stated minor.

Consequently

`P(N) = P(M) intersect {y : y(S_i)=r(S_i) for every i}`.

One can also see this directly from convex combinations of original bases: an average saturates a valid rank upper inequality only when every basis with positive weight saturates it. Thus `x in P(N)`.

Perform the anchor construction of Theorem A on `N`. Its upper-only LP is feasible at `x`, regardless of whether this face contains an originally degree-feasible integral basis. The upper-only lemma of Section 6 needs LP feasibility, not integral feasibility, and returns a basis of `N` costing at most its LP optimum, which is at most `c·x`. The two-sided bounds follow by the same cardinality subtraction. Every basis of `N` is a basis of `M`. Minor independence is tested by ranks: for `X⊆D_i`, it holds exactly when `r_M(S_{i−1}∪X)−r_M(S_{i−1})=|X|`. All tests and transformations are polynomial. ∎

### Finding a maximal tight chain

The theorem can simply use a supplied polynomial-size chain, independently checked using ranks and rational sums. Alternatively a maximal chain for a specified rational LP point `x` can be found using polynomial-time submodular minimization, the same standard oracle primitive underlying rank-polytope separation.

Set `f(S)=r(S)−x(S)≥0`. The zero sets `T` are closed under union and intersection and contain the empty set and `V`. For every ordered pair `a,b`, minimize `f(S)` under `b in S`, `a not in S` by deleting the forbidden element and fixing the required one. Such a tight set exists exactly when the minimum is zero. Define `a≼b` if no such tight set exists; for `a=b` take this relation reflexively. This is the implication preorder “every tight set containing b contains a.” Its equivalence classes and their partial order are polynomially computable.

Every member of `T` is a down-set for this preorder. Conversely, the minimum tight set containing `b` is the intersection of all tight sets containing `b`, namely `{a:a≼b}`. Any down-set is the union of these minimum tight sets, and is therefore tight. A topological order of the quotient classes consequently gives a maximal tight chain by successively taking their union.

These chain indicators span all tight-set indicators: successive differences are the equivalence classes, and every tight set is a union of such classes. Hence the chain cuts out the minimal face of `P(M)` containing `x`. This is not a claim that a polynomial search will find some favorable LP optimum whenever one exists. It is a polynomial criterion for the chosen LP point. A deterministic LP solver's output can be tested and the criterion may fail.

### Separately checked connected graphic evidence

A finite graphic instance on `K_5` was separately checked to show that the tight-face criterion can succeed when the original component criterion fails. The independently checked face had smaller component incidence and gave the requested two-sided allowance at the LP cost benchmark. Some minimum-cost bases failed that allowance, so the example did not merely assert that every minimum-cost basis already satisfies it.

This edition omits the example's numerical degree sets, bounds, costs, fractional point, face-input specification, and explicit basis witnesses. It therefore does not provide a self-contained reconstruction of that particular instance. Its role is supporting evidence for nonvacuity, not a hypothesis or proof step of Theorems A or B. AUDIT.md and VERIFICATION.json state the historical check coverage and its reproduction limits.

## 5. Separately checked KLS method obstruction

The finite construction in KLS Remark 1 was separately checked, together with an added rational objective, as an originally feasible instance having a unique fully fractional cost-optimal LP vertex. The elementary method that only fixes integral coordinates and deletes bounds justified by the individual one-sided dropping tests stalls there. The canonical anchor criterion also fails there.

This is a method obstruction, not a counterexample to the simultaneous additive `Δ−1` target. In particular, a separately checked convex decomposition of the stalled point into relaxed feasible bases proves that, for every linear objective, some basis in that decomposition costs at most the objective's value at the point. This follows immediately because the objective of a convex combination is the same convex combination of the constituent objectives. The stalled vertex therefore does not refute cost-preserving existence or another polynomial-time algorithm.

The numerical partition blocks, indexed degree sets, bounds, costs, coordinates, independent equation rows, determinant witness, and decomposition bases are omitted. The original KLS source documents the underlying obstruction; the additional objective, enumeration, and decomposition are authored checks. The omitted augmented instance is not self-contained or computationally reproducible from this edition alone. None of these finite inputs is needed by the general proofs.

## 6. Upper-only rounding lemma, with the needed LP cost guarantee

The following is the KLS Theorem 2 upper-only argument, included to make the reduction's exact use of cost and feasibility explicit. It is established prior work, not a new theorem claimed here.

**Lemma.** Let `P(M)` together with integer upper rows `x(F_j)≤b_j` be LP-feasible, and let every element occur in at most `D≥1` indexed rows. For rational costs, a polynomial oracle algorithm returns a basis `B` with cost no greater than the initial LP optimum and `|B∩F_j|≤b_j+D−1` for every original row.

At each iteration choose a basic optimum of the current rank LP. Delete zero coordinates. Contract one coordinates and add their elements to the chosen set; subtract their contribution from each incident row bound. If all coordinates are strictly between zero and one, delete any row with

`|F_j|≤b_j+D−1`.                                  (2)

An original row removed this way can never be exceeded by more than `D−1`, because there are at most `|F_j|` still-undecided elements of that row. If all residual rows disappear, the minimum-cost residual basis problem is ordinary matroid optimization. Fixed coordinates, contractions, and deletions preserve feasibility of the current fractional vector on the residual problem; dropping rows only enlarges its feasible set. Thus “cost already selected plus residual optimum” never increases. This is valid for negative costs too.

It remains to show progress. Suppose `0<x_v<1` everywhere and no row satisfies (2). Then for every row, `|F_j|−b_j≥D`.

The tight rank sets are closed under intersection and union by submodularity. A maximal chain of tight rank sets spans all tight rank-set indicators. Here is the uncrossing argument. If a tight set `R` outside the chain's span exists, choose one incomparable with as few chain members as possible. It is incomparable with some chain member `T`. Both `R∩T` and `R∪T` are tight, and their indicators sum to `1_R+1_T`. At least one is still outside the span, but each is incomparable with fewer chain members, a contradiction. Delete any zero empty-set indicator from the chain. Its remaining indicators are independent because their successive nonempty differences are disjoint.

Let this chain be `S_1⊂...⊂S_k`, with `S_0=empty`. Since the LP optimum is basic and no box bound is tight, augment its rank indicators by an independent subset `J` of tight upper rows to get exactly `|V|=k+|J|` independent vectors.

For each chain difference, `x(S_i\S_{i−1})=r(S_i)−r(S_{i−1})` is a positive integer, since the difference is nonempty and every coordinate is positive. It is therefore at least 1. For a tight row `j in J`,

`|F_j|−x(F_j)=|F_j|−b_j≥D`.

Let `d_J(v)` be its number of occurrences among these tight rows. Then

`k+|J| ≤ x(S_k) + (1/D) sum_{j in J} (|F_j|−x(F_j))`

`          = x(S_k) + sum_v ((1−x_v)/D) d_J(v)`

`          ≤ x(V) + sum_v (1−x_v) = |V|`.

If any of these inequalities is strict, it contradicts `|V|=k+|J|`. If all are equalities, strict positivity gives `S_k=V`, and `1−x_v>0` gives `d_J(v)=D` for every `v`. But then

`sum_{j in J} 1_(F_j) = D 1_V = D 1_(S_k)`,

contradicting the chosen linear independence. Hence a progress step always exists.

There are at most `|V|` coordinate removals and as many row removals as the input number of rows. Rank-polytope separation is polynomial in the independent-set-oracle model (KLS explicitly uses this model); adding polynomially many explicit degree inequalities preserves it. Standard rational LP optimization with a separation oracle finds a basic optimum in polynomial oracle time. Ranks are at most `|V|`, updated integer bounds have polynomial bit size, and rational input costs pose no unencoded-real assumption. This proves the lemma, including the stronger initial-LP cost guarantee even without originally feasible integral degree bounds. ∎

## 7. Verification boundary and residual question

The independent historical audit reconstructed the two finite examples using exact rational arithmetic, fresh graphic-rank calculations, exhaustive finite enumeration, and rational Gaussian elimination. Candidate programs were neither imported nor executed by the independent audit. Separate controls addressed LP-only feasibility, negative costs, integer normalization, and boundary coordinates. Normal Python, `-O`, and `-OO` runs passed. These are historical checks; preparation of this prose edition performed no new mathematical computation or scholarly-source inspection.

The complete general mathematical proofs are retained, conditional on standard polynomial-time submodular-minimization and rational-LP oracle tools as accepted dependencies. Those tools are neither re-proved nor implemented here. This is not a computational reproduction package: executable code, raw certificates, numerical instance definitions, explicit finite witnesses and basis lists, matrices, and tables are omitted. The finite examples are separately checked supporting evidence; their omitted inputs cannot be recovered from this edition alone and are not premises of the general theorems.

The unrestricted simultaneous additive Δ−1 guarantee remains unresolved by this work when the relevant component-incidence criterion fails. No novelty, priority, or exhaustive current-literature-status claim is made. No general `Δ−1` rounding algorithm, hardness theorem, or counterexample to the requested polynomial guarantee is claimed. Failure of the canonical criterion excludes only that sufficient criterion in its stated model.

## References

- Tamás Király, Lap Chi Lau, Mohit Singh, *Degree Bounded Matroids and Submodular Flows*, Combinatorica 32(6) (2012), 703–720. DOI: https://doi.org/10.1007/s00493-012-2760-6 . Retained public author version: https://cs.uwaterloo.ca/~lapchi/papers/submodular.pdf . Section 3, Theorem 2 and Remark 1 are the main sources used here.
- Kristóf Bérczi, André Berger, Matthias Mnich, Roland Vincze, *Degree-Bounded Generalized Polymatroids and Approximating the Metric Many-Visits TSP*, arXiv:1911.09890v2 (2019): https://arxiv.org/abs/1911.09890v2 . Section 5 retains two-sided additive `2Δ−1` and one-sided `Δ−1`; it does not supply the missing unrestricted simultaneous guarantee.
- Egres Open, *Bounded degree matroid basis*, retained revision 2046: https://oldlemon.cs.elte.hu/egres/open/Bounded_degree_matroid_basis . This is the target formulation, not a certification of current openness.
