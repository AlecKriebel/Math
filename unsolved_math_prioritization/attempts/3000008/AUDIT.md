# Independent audit of the fixed rank block criterion

## Decision and scope

**Accept the restricted mathematical result without a substantive proof correction.** Theorem A, Theorem B, the canonical complement-incidence statement in its expressly indexed model, the maximal-tight-chain construction, and the upper-only rounding lemma are correct. Both finite examples agreed with independent exact reconstruction.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

The complete general mathematical proofs are retained, conditional on standard polynomial-time submodular-minimization and rational-LP oracle tools as accepted dependencies. Those tools are neither re-proved nor implemented here. This is not a computational reproduction package: executable code, raw certificates, numerical instance definitions, explicit finite witnesses and basis lists, matrices, and tables are omitted. The finite examples are separately checked supporting evidence; their omitted inputs cannot be recovered from this edition alone and are not premises of the general theorems.

The unrestricted simultaneous additive Δ−1 guarantee remains unresolved by this work when the relevant component-incidence criterion fails. No novelty, priority, or exhaustive current-literature-status claim is made.

The accepted original report has SHA-256 `4af093aaa6fdb1f8e7af91ce73db59a702fd4824b5dd9b7e0c50ff9cb7abe347`; its candidate manifest has SHA-256 `cf252d22ad409e6443c3b2ebb376381b3a4a20507941a338488289e0a23bccfe`. The original audit report has SHA-256 `72f4ddd92c6c1ddf067e884fe83d39fbc1cae7cb7785dde29d2970d8bf380988`; its manifest has SHA-256 `f4448ab4cf5596e2b9d6cb4ab43179a93a2f7dcc72abb37f49d0511d36b86e55`. These identify the accepted inputs, not the edited public files; ACCEPTANCE.json binds the public edition separately.

## Accepted benchmark and assumptions

The integer normalization in the report is material. For rational degree bounds, it first replaces each lower bound by its ceiling and each upper bound by its floor, then defines `L`. The asserted cost bound is relative to that **integer-bound LP**. It is not a guarantee relative to the potentially smaller optimum of the unrounded rational-bound LP.

An independently checked finite normalization control confirms that the unrounded rational-bound LP can have smaller optimum than every originally feasible integral basis, even when the target allows no degree violation. Its numerical input is omitted from this prose edition. It is a supporting warning about the benchmark, not a premise of the theorem. The normalization-first ordering is part of the accepted statement.

Finite rational costs may be negative. The basis polytope is compact, so feasible LPs have finite optima. The input hyperedges are explicit indexed sets; duplicate rows count separately unless a permitted preprocessing operation removes them. The original-question comparison `L≤OPT` uses original integral feasibility. The upper-only lemma and the face extension need only LP feasibility. Rank-zero and empty-row cases have been identified separately in the report.

## Fixed rank blocks and the same basis guarantee

If the ranks of a partition sum to `r(V)`, then every basis has exactly `r(P_i)` elements in each block: every block contributes at most its rank, and the sum of these upper bounds already equals the basis cardinality. Convex combinations give the same equations throughout the basis polytope.

For an indexed degree set `e`, let `A_e` be the union of the blocks it meets and let `R_e` be their total rank. The identity `x(A_e)=R_e` makes the lower inequality exactly equivalent to the upper inequality on `A_e\e`, with bound `R_e−l_e`. This is an equality of feasible regions, not merely a relaxation or an implication for integral points.

Fix an element `v` in a block `P`. Each original index whose degree set meets `P` contributes exactly one transformed incidence at `v`: either the original upper row contains `v`, or its anchor-complement row does. Indices not meeting the block contribute none. The maximum indexed column incidence is therefore exactly `κ` before optional pruning. The upper-only lemma returns one basis satisfying both transformed upper inequalities. Subtracting its complement count from `R_e` gives the lower bound on that same basis. The LP optimum is unchanged by the transformation, so its cost is at most `L`.

The direct criterion `κ≤Δ` is consequently sufficient. Because every hyperedge containing an element meets that element's block, the unpruned system always has `κ≥Δ`; the criterion in that model is precisely equality. The restriction allows overlapping degree sets and an arbitrarily large total number of such sets.

## Canonical components and exact minimality scope

For a fixed basis, connect a basis element to a nonbasis element whenever their exchange yields another basis. The neighbors of a nonloop nonbasis element are exactly the other members of its fundamental circuit. Hence the basis elements in each graph component span that component; their cardinality is its rank. The component ranks sum to `r(V)`, including isolated loops and coloops.

If a set has the same cardinality in every basis, an exchange edge cannot cross it, because the two bases witnessing that edge would then have different cardinalities in the set. Thus every such set is a union of components. Conversely, unions of these fixed-rank components do have constant cardinality. This proves the finest-partition characterization, and also gives the numerical test `r(A)+r(V\A)=r(V)` by extending bases of `A` and its complement.

Each permissible anchor containing `e` must contain every component met by `e`. Keeping each original upper row and replacing each lower row by just such an anchor complement therefore gives a pointwise lower bound on transformed incidence. The candidate attains it. This proves the stated indexed-model minimality, including duplicate constraints. It says nothing about deleting redundant rows, merging duplicates, linear combinations, further face restriction, or other rounding methods. The report explicitly excludes those stronger interpretations.

At most `r(V)(|V|−r(V))` independence tests suffice for the exchange graph, after greedily finding a basis. Computing ranks, components, and their incidence counts is polynomial.

## Face restriction and maximal tight chains

For a rank-tight chain with differences `D_i`, the direct sum of `(M|S_i)/S_(i−1)` has precisely the bases of `M` that saturate all chain ranks. Arbitrary bases of successive minors may be combined: a basis of a contraction extends any chosen basis of its contracted set. Conversely, a chain-saturating original basis supplies a basis in each minor. Thus the indicated direct sum is genuinely a matroid on the original ground set, and every returned basis is an original basis.

The face-polytope equality follows as well from convex combinations. An average that attains the upper rank bound on a chain set can use only bases attaining that bound. The supplied feasible LP point belongs to this face. The transformed face LP has optimum no larger than its cost, whether or not it has an exactly degree-feasible integral basis. Applying the upper-only lemma to that LP and subtracting fixed anchor ranks proves Theorem B.

For a specified rational point `x`, `f(S)=r(S)−x(S)` is a nonnegative submodular function. Its zero sets form a union-and-intersection closed family containing the empty set and the entire ground set. For distinct `a,b`, minimizing `f` subject to `b∈S` and `a∉S` determines whether every tight set containing `b` must contain `a`. Required and forbidden elements are handled by restricting the domain and adjoining the required element in function evaluations; submodularity is preserved.

The resulting implication relation is a preorder. Its principal down-set at `b` is the intersection of all tight sets containing `b`, and is tight. Every down-set is a union of these principal down-sets, and hence tight; every tight set is a down-set. A topological order of the equivalence classes gives a maximal chain of tight down-sets. Its successive differences are the classes, so its indicators span every tight-set indicator. This establishes both the proposed construction and the minimal-face claim.

Boundary coordinates cause no missing face constraints. If `x_v=0`, then `x(V\{v})=r(V)` and feasibility forces `r(V\{v})=r(V)`; the zero-coordinate equation is the difference of two tight rank equations. Coordinates equal to 1 are likewise captured by their tight singleton ranks. An independent test with a loop, a coloop, and a zero-coordinate face confirms the chain/minor description in this boundary case.

The discovery method uses at most `n(n−1)` constrained submodular minimizations and polynomial further work. It tests the supplied point. It neither finds a favorable optimal point by searching all optima nor proves that one exists whenever the direct test fails.

## Upper only rounding lemma

The proof correctly uses a basic optimum, fixes coordinates equal to zero or one by deletion and contraction, and drops a residual row only when its support has size at most its current integer bound plus `D−1`. At row deletion, all future selections in that row come from this support. Restoring previously selected elements proves the required inequality for the original row.

Feasibility is preserved by coordinate operations, and row deletion only enlarges the feasible region. At every stage, selected cost plus residual optimum is no larger than at the preceding stage. This additive invariant does not use nonnegative costs. It also does not presume an integral point satisfying the original degree rows.

At a fully fractional basic optimum, maximal-chain uncrossing spans the tight rank rows. The stated uncrossing proof is valid: intersection and union with an incomparable chain member are tight, at least one remains outside the chain span, and each has fewer incomparable chain members. Removing the empty indicator leaves independent chain vectors. Augmenting them with independent tight degree rows gives `n=k+|J|`.

Each nonempty chain difference has strictly positive integral `x`-mass, hence mass at least 1. If no degree row can be dropped, its integer support deficit is at least `D`. Thus

`k+|J| ≤ x(S_k) + sum_v (1−x_v)d_J(v)/D ≤ n`.

A strict inequality contradicts basicness. Equality is also impossible: strict positivity forces `S_k=V`, and strict fractionalness forces every `d_J(v)=D`. The resulting identity `sum_(j∈J) 1_(F_j)=D·1_(S_k)` is a nontrivial dependence among the chosen independent rows. The equality case is indispensable; it is not permissible to claim strict token surplus without this dependence argument.

Every progress step removes a coordinate or a row. Once no rows remain, ordinary minimum-cost matroid basis optimization completes the procedure. The original incidence bound remains valid after all deletions and contractions.

The polynomial claim uses established oracle submodular minimization and rational LP optimization/separation, not an implementation in this packet. Rank evaluation is polynomial through independence queries. Rank inequalities and explicit degree rows have polynomially bounded integer coefficients and encoded bounds. Standard rational optimization plus lexicographic refinement yields a basic optimum with polynomial bit complexity. These standard primitives are accepted dependencies, and are not re-proved by the finite checker.

## Independent exact examples and controls

The independently authored historical checker used rational arithmetic and integer enumeration, without floating point, external solver code, assertions, or imports from candidate programs. Graphic ranks were computed by connected-component counts. Gaussian elimination and determinant calculation were written independently. Instance definitions were reconstructed from the report and checked against the retained certificates.

For the graphic `K_5` example, all 125 original bases and all 64 indicated face bases were checked. Rank feasibility was tested on all 1,024 subsets. The independent audit checked the fractional marginals, LP optimality, original integral feasibility, face and original components, the strict improvement in the incidence criterion, exact and relaxed anchor-complement equivalence, and the existence of minimum-cost bases violating the target allowance.

For the KLS example, all 96 bases and all 4,096 rank subsets were checked. The audit verified original feasibility, the unique fully fractional LP optimum, full equation rank, the elementary dropping-test obstruction, failure of the canonical anchor criterion, all constant-cardinality anchors, and the tight-set preorder and chain. It separately verified a convex decomposition into simultaneously relaxed feasible bases. Linearity then shows that some constituent has cost at most the fractional point for every linear objective. This confirms why the stalled vertex is not a cost-preserving existence counterexample.

Additional finite controls checked the exact role of the normalized LP benchmark, the extension to LP-feasible systems with no exactly degree-feasible basis, the selected-cost-plus-residual-optimum invariant with negative costs, the equality dependence in the upper-only counting argument, and rank-face behavior with loops, coloops, and boundary coordinates.

All independent exact tests, candidate-authentication checks, 36 negative controls, and 6 positive controls passed under normal Python, `-O`, and `-OO`. Mutation categories included degree bounds, fractional coordinates, costs, ranks, counts, equation rank, determinant, convex decomposition, chain, anchors, incidence, transformed bounds, and file-inventory corruption. Byte-identical substantive independent receipts were retained for the three modes.

These are historical verification results, not fresh executions during edition preparation. The numerical instance definitions, basis and decomposition lists, coordinate vectors, equation matrices, detailed count tables, raw certificates, and checker programs are omitted. The public references identify the underlying source construction, but do not replace these omitted authored inputs. This edition is not sufficient to reproduce the finite checks. The complete general proofs above and in PROOF.md do not depend on these examples or controls.

## Source scope and residual question

The KLS retained source was inspected for its theorem statements, complete Section 3 proof, Remark 1, and the independence-oracle LP claim. Its reported obstruction agrees exactly with the reconstructed partition blocks and degree sets. The additional costs, counts, and convex decomposition are independently verified calculations rather than assertions attributed to KLS.

The retained generalized-polymatroid paper was checked for the two-sided `2Δ−1` and one-sided `Δ−1` statements, the oracle dependency, and its Section 5 one-sided proof. It does not supply an unrestricted simultaneous `Δ−1` theorem. Both retained PDF text extractions were independently reproduced byte for byte with the installed PDF text extractor. No fresh network retrieval, independent visual PDF audit, or current-status/novelty survey is claimed. Copied source bodies are excluded from this public edition. Preparation of this edition performed byte-integrity and editorial checks only, with no new scholarly-source retrieval, text extraction, visual inspection, literature survey, or mathematical execution.

The accepted outcome is a correct sufficient criterion with a polynomial oracle implementation through standard primitives, and an accurately delimited obstruction audit. The unrestricted case where the relevant component incidence exceeds `Δ` remains unresolved by this packet.

## Public references

- Tamás Király, Lap Chi Lau, Mohit Singh, *Degree Bounded Matroids and Submodular Flows*, Combinatorica 32(6), 703–720 (2012). DOI: https://doi.org/10.1007/s00493-012-2760-6 . Retained public author PDF: https://cs.uwaterloo.ca/~lapchi/papers/submodular.pdf .
- Kristóf Bérczi, André Berger, Matthias Mnich, Roland Vincze, *Degree-Bounded Generalized Polymatroids and Approximating the Metric Many-Visits TSP*, arXiv:1911.09890v2. https://arxiv.org/abs/1911.09890v2 .
- Egres Open, *Bounded degree matroid basis*, retained formulation. https://oldlemon.cs.elte.hu/egres/open/Bounded_degree_matroid_basis .
