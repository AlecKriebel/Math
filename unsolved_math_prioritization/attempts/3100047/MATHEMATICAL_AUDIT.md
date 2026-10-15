# Independent audit of bounded pressing-balance results (row 1747)

## Scope and disposition

This audit concerns symmetric matrices over F2 having at least two successful **full-length** pressing sequences. Each sequence is sampled with equal probability, and a balanced pair means an exact probability in the closed interval [1/3,2/3]. Singular matrices with omitted vertices are outside this formulation. Nonsingularity alone does not guarantee a successful sequence.

The computational claim to be accepted is finite: every such matrix of order at most eight has a balanced pair. Exhaustive coverage uses labelled matrices at small orders and a fully verified orbit cover with every diagonal coloring at orders seven and eight. It is not a theorem at arbitrary order. A separately reviewed structural proof gives an infinite subclass, not a reduction of all pressing graphs to that subclass.

Disposition: ACCEPTED AS BOUNDED RESULTS. Frozen-input pins and validation results accompany this document. The unrestricted full-length conjecture remains unresolved here.

## 1. Independent algebraic derivation

For a symmetric matrix A, a legal press at vertex i has A_ii=1 and sends A to A+c c^T, where c is column i. Symmetry makes c equal to the transpose of row i. The operation clears row and column i. Writing A in the corresponding block order as [[1,b^T],[b,C]], ordinary block elimination gives the residual matrix C+b b^T. Congruence identifies A with diag(1,C+b b^T), so each press lowers rank by exactly one. Full-length success implies nonsingularity.

Write d(S)=det A[S] in F2 and d(empty)=1. A permutation is a successful full-length sequence exactly when d(S)=1 at every prefix set S. Inductively, a prefix with nonzero determinant has a well-defined Schur complement. The next diagonal pivot equals d(S union {i})/d(S), by the block determinant formula. Over F2 every nonzero determinant equals one. Thus the principal-minor condition is necessary and sufficient, without assuming every nonsingular principal submatrix is reachable by one-vertex presses.

There is a fast independent determinant recurrence. For i in nonempty S, let T=S minus {i}. Then

    d(S) = A_ii d(T) + sum over j in T of A_ij d(T minus {j})  (in F2).

Expand the determinant by permutations. For a symmetric matrix, reverse a canonically selected cycle of length at least three; its two terms agree and cancel in characteristic two. The surviving permutations are involutions. Vertex i is either a fixed point, contributing the first term, or is paired with j in a transposition, contributing A_ij A_ji=A_ij. This proves the recurrence for singular and nonsingular A alike. Gaussian elimination, not this recurrence, supplies the independent reference determinants in the auditor's exhaustive small-order checks.

Define F(empty)=1 and, for nonempty S,

    F(S) = d(S) * sum over i in S of F(S minus {i}),

where multiplication by d(S) and the sum now occur in the integers. Define G(V)=d(V), and in decreasing subset order,

    G(S) = d(S) * sum over i outside S of G(S union {i}).

F counts valid prefix paths; G counts paths from S to the full set. Therefore T=F(V)=G(empty) is the number of full successes. The author's scanner sets G(V)=1 only after checking T>0, which is equivalent in its invocation domain.

For distinct x,y, the exact numerator for x before y is

    N_xy = sum over S excluding x,y of F(S) G(S union {x}).

Every successful sequence contributes once, at the transition which appends x. Prefix and suffix choices join uniquely; the Schur complement depends only on S, so their compatibility introduces no hidden factor. The denominator is T. The exact test is

    T <= 3 N_xy <= 2 T.

Also N_xy+N_yx=T. No floating-point threshold is used. In the accepted scans n<=8, T<=8!=40320; every path-product is at most T, and all aggregate counts reported here fit uint64. The audit does not certify arbitrary CLI inputs or unrestricted larger-order aggregate arithmetic.

## 2. Independent coverage proof

The generator writes one code and automorphism count for each uncolored simple graph. Its code lists the upper-triangle edges in increasing larger endpoint order, reading this bit string as a binary integer. A graph's canonical code is the minimum such code among orders whose vertex degrees are nondecreasing.

This is a complete invariant: an isomorphism maps the allowed degree-sorted orders bijectively; conversely an identical edge code is an explicit isomorphism. Every graph admits at least one such order. For a fixed graph, the number of allowed orders attaining its canonical code equals its automorphism-group size: any one attaining order identifies the others bijectively with automorphisms. Restriction to degree-sorted orders loses no automorphism.

The auditor separately enumerated **every** degree-sorted order of **every** listed graph, without the generator's prefix pruning, and recomputed its minimum and the multiplicity of that minimum. The canonical codes are distinct and all automorphism counts agree. Consequently their labelled isomorphism orbits are disjoint and have sizes n!/|Aut(G)|. Their sum equals 2^(n(n-1)/2) at every order through eight, proving no labelled simple graph is omitted. At n=8 this checks all 12,346 representatives and all 2,413,800 degree-sorted permutations; the orbit sum is 268,435,456.

This orbit-sum proof independently establishes coverage and does not merely rely on the familiar number 12,346 or on small-order agreement. The author's augmentation argument is also valid: remove a vertex from any n-vertex graph, relabel the remaining graph to its existing (n-1)-vertex representative, and adjoin the removed vertex with its transported neighborhood. Enumerating all neighborhoods therefore reaches the original isomorphism class. Canonical deduplication preserves precisely the isomorphism classes.

For each uncolored representative, the scanner enumerates all 2^n diagonal assignments. A labelled copy of the underlying graph has the same collection of counts across its diagonal assignments, transported bijectively by an isomorphism. Multiplying the representative's diagonal-summed statistic by n!/|Aut(G)| therefore counts labelled symmetric matrices exactly. No division by the automorphism group of the **colored** graph is required. The raw representative/coloring count is not claimed to count colored isomorphism classes. Existence of a balanced pair is invariant under relabelling.

## 3. A second exhaustive algorithm

The second implementation uses direct rank-one presses, no determinant or subset-DAG formula. Fix an uncolored graph and a permutation of its vertices. Start with zero diagonal; just before pressing the next vertex v, toggle its diagonal to one if necessary, recording that toggle in the initial coloring. Then execute the legal rank-one press.

This finds exactly one initial coloring for the given graph and permutation. A change to the diagonal at an unpressed v leaves every other vertex's column unchanged. It therefore commutes with all earlier presses at different vertices. Moving each just-in-time toggle back to the initial matrix leaves every performed operation unchanged. Conversely the required pivot at each step forces that diagonal toggle uniquely. After all n vertices have been pressed, the matrix is zero. Thus this enumerates all successful colored-graph/permutation pairs exactly once and accumulates their exact pair precedences directly.

The resulting total over all labelled uncolored graphs must also equal n! 2^(n(n-1)/2), which matches the reported totals. This identity alone would not prove balance; the second algorithm checks each diagonal coloring and each pair count. At n=8 it examines 497,790,720 representative/permutation combinations.

## 4. Independent exact checks and countercontrols

The auditor's separately authored Python program exhaustively considers every labelled symmetric matrix through n=5. For each, it compares the complete full-success list from legal rank-one presses with Gaussian-determinant subset counting, including every directed pair numerator. It independently verifies the involution determinant recurrence. For every nonsingular matrix in those scans it verifies the inverse-complement principal-minor identity and the complete reversal bijection of success lists. These checks cover 33,866 matrices in total. They are exhaustive only for these stated orders; the author's additional random spot checks are not used as an exhaustive certificate.

The following controls distinguish the intended statement from tempting stronger or incorrect statements:

* The alternating 2x2 matrix, row masks (2,1), is nonsingular but has no legal first press. It rejects the inference that full rank alone gives a distribution.
* Row masks (6,3,1) have the unique full success (1,0,2), but their principal set {0,2} is the nonsingular alternating 2x2 matrix. That set has no one-at-a-time feasible path. Thus even inside the successfully pressable full-rank domain, nonzero principal determinant does not imply accessible prefix set.
* Row masks (11,7,2,1) have exactly the two successes (0,3,1,2) and (1,2,0,3). The accessible successful-prefix sets X={0,3} and Y={1} satisfy |X|>|Y|, but neither Y union {0} nor Y union {3} is a successful prefix. This disproves greedoid augmentation for that family. The same two supersets have determinant zero, so allowing dead-end legal prefixes does not repair augmentation.
* In that four-vertex fixture, the pairwise orders shared by both successes are just 0 before 3 and 1 before 2. Their intersection poset has six linear extensions, not two. Any poset with both successes as extensions must impose only shared relations and hence permit at least those six extensions. Therefore the complete pressing family cannot be represented by a single arbitrary poset's extension set.
* Row masks (3,1,4) have three successes: (0,1,2), (0,2,1), (2,0,1). Their only balanced pairs have probabilities exactly 1/3 or 2/3. A strict-endpoint mutant is rejected.
* The all-ones singular 2x2 matrix is excluded from the full-length count; its one-vertex successes are not used to refute the intended conjecture.
* Deliberately omitting a representative, duplicating a representative, or corrupting an automorphism count is rejected by the independent orbit verifier.

The four-vertex fixture is itself balanced. It is an obstruction to a proof route, not a counterexample to pressing balance.

## 5. Structural and source audit

The final structural report was read in full. Its elementary arguments are accepted within their stated hypotheses:

1. **Instructional partition.** A successful word produces a label-indexed unit-triangular root U with A=U^T U. Inductive uniqueness in any fixed vertex order is valid. The words producing U are exactly the linear extensions of the acyclic order imposed by its nonzero off-diagonal entries. Distinct roots give disjoint families. Adjacent legal swaps preserve the root, and the usual first-letter movement argument connects every extension family.
2. **Relocation lemma.** For two successful words differing by moving a past b_1,...,b_k, the report writes the block B=R^T R and its incidence column v=R^T z. Both prefix systems force all successive partial sums of z to vanish, so z=v=0. Thus every crossed pair commutes, even accounting for its incidence with later suffix vertices. The two-total-edit and adjacent-swap component claims follow. This argument does not use broader edit connectivity.
3. **V-poset balance.** Internal distributions are preserved because every tuple of component extensions has the same multinomial number of shuffles. For two unique component words of lengths p>=q, the probability Q_k that the kth letter of the longer word precedes the first of the shorter is the stated product. The first crossing below 2/3 occurs by k=p-q+1 and has ratio at least 1/2 to its predecessor, placing it above 1/3. If Q_1 is already at most 2/3, it is at least 1/2. The recursive induction is complete, including unique-extension and singleton boundary cases. The three-word example establishes sharpness.
4. **Inverse reversal.** The kernel correspondence between A[S] and A^{-1}[V minus S] works even when either principal block is singular. Taking complements of all prefix sets proves the bijection of complete successful words. The self-inverse example and all its pair numerators were independently replayed.
5. **Symmetric exchange.** The principal-pivot input/output correspondence is invertible whenever A[X] is. Its support/vanishing conditions match symmetric difference coordinate by coordinate. A nonsingular residual principal block has either a nonzero diagonal at the selected vertex or a nonzero off-diagonal entry in that row, producing the claimed one- or two-element exchange. This proves unordered symmetric exchange, not prefix accessibility.
6. **Necessary conditions.** A strict >2/3 majority triangle contradicts the fact that a total order satisfies at most two of its three comparisons. The block-shuffle and forced-end arguments correctly show that a vertex-minimal counterexample must be connected, have multiple first and last choices, and have multiple instructional classes. These are necessary conditions only.

The auditor separately enumerated all matrices through n=4 to validate the full root-class partition, every successful one-letter relocation, and every feasible-set symmetric-exchange instance. Exact two-chain probabilities were checked for all 5,050 length pairs 1<=q<=p<=100. These are bounded implementation checks accompanying the complete proofs, not substitutes for induction.

The report's additional four-vertex example (13,10,5,3) has all of 0,1,2 available as successful first choices; the only edge between these initially black vertices is 0–2, and its precedence probability is 1/4. Thus even the proposed existence of an adjacent balanced competing-first pair fails. Other pairs in that graph are balanced.

The [Cooper–Gartland–Whitlatch primary paper](https://arxiv.org/abs/1810.07276v2) expressly limits this instructional-poset discussion to full rank. Its Lemma 4 supplies extension families, Definition 6 defines autonomy, and Definition 10 plus Theorems 2–3 identify the autonomous subclass with recursively constructed V-posets. The auditor inspected those statements, including the rendered theorem page. The [older author-hosted PDF](https://people.math.sc.edu/cooper/VPosets.pdf) is a separately pinned snapshot. The official arXiv metadata identifies v2 as revised 14 November 2018; the PDF's typeset date is different. No complete audit of the external autonomy characterization is claimed.

Two source-text defects are documented: Lemma 8 contains a false unrestricted cardinality equality, locally repaired by restricting to extensions starting with the chosen vertex; and the printed induced-bowtie definition omits a comparison. The authored argument uses the recursive V definition and does not rely on either defective line. The autonomous pressing corollary is accepted with the characterization as its explicitly named external theorem.


The two exact implementations were compiled and rerun by the auditor from bytes matching the final source pins. The auditor-side order-six direct scan covers all labelled matrices; the order-seven and order-eight reruns use the independently certified graph lists. All final output aggregates match:

| Order | Labelled matrices covered | Full-length pressable | Nonunique full-length | Counterexamples |
|---|---:|---:|---:|---:|
| 6 | 2,097,152 | 867,654 | 861,174 | 0 |
| 7 | 268,435,456 | 112,476,490 | 112,385,770 | 0 |
| 8 | 68,719,476,736 | 28,758,575,496 | 28,757,486,856 | 0 |

The auditor's exhaustive small-order/canonical verifier passes in normal, -O, and -OO Python modes, using explicit runtime checks rather than optimization-removable assertions. The recorded results agree after ignoring elapsed runtime. Omitted, duplicated, or corrupt representative controls are rejected; input-byte and missing-file controls are also rejected by the frozen-input checker.

## 6. Residual

No unrestricted proof or counterexample is established. Finite verification through eight cannot decide larger orders. The autonomous/V-poset argument covers only its stated subclass. Even a partition of all successes into linear-extension families does not by itself produce one balanced pair under the uniform distribution on their union: a pair or favorable orientation can depend on the block, and each block's weight is its number of extensions. Principal-minor symmetric exchange is weaker than the failed one-vertex greedoid property and supplies no missing probability inequality here. Matrix-inverse reversal preserves the balance question rather than resolving it.
