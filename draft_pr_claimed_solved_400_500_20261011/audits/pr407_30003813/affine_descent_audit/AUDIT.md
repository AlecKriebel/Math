# PR407: independent affine-lattice and descent audit

## Verdict and exact object

**PASS for the complete stated mathematical interpretation. Required mathematical repairs: none.** This review does not certify novelty, historical priority, or current openness. Those questions require the separate priority gate. No new substantive author attempt was made; the recorded candidate already contains a complete proof.

The reviewed PR head is `e3f8838a8eac68bbd186fc0234ac2e2a49194626`, with complete selected subtree `b4ee3347c6587b07348b836858c29d7812ebe421`. Every one of the 13 files in `SOURCE_RECEIPT.json` was independently checked for its byte count, SHA-256, and Git blob identity. The proof file has SHA-256 `b1b6e5e20d64f66d8b7621cca491ead60a6ebefcae08dca0e7dd7b6ab03965fa`.

The full candidate proof, source gate, README, status, release explanation, historical research log, previous mathematical audit, both portable checkers, manifest, and recorded results were read. This family received no mathematical conclusions from the other current review family. The previous historical audit was treated as an input to challenge, rather than an authority replacing proof verification. Fresh code imports no candidate checker functions.

## Original target and limits

I independently obtained the [official Oberwolfach report](https://publications.mfo.de/bitstream/handle/mfo/3645/OWR_2018_23.pdf?isAllowed=y&sequence=1), extracted the complete abstract on printed pages 1408-1410, and visually inspected printed page 1410, PDF page 30. The PDF has SHA-256 `28cc8b4c6c445cee7def413c46dac52011589b294c4f0578251d78167295526c` and 1,293,303 bytes. These third-party source bytes and the page rendering are retained privately, outside the public audit package.

The final paragraph asks for the combinatorics of the h-star polynomial of the cube restricted by one chosen weak adjacent-sum inequality for each index `1,...,n-1`. It has no wrap edge. The preceding abstract motivates cyclic-order statistics for another family, but the final question does not require a statistic on the same cyclic-order objects. This distinction is an interpretation of the actual source wording; the candidate states it openly.

The claim audited here is precisely: for every positive integer n, every sign word of length n-1, and every permutation alpha with descent set

`D = {odd i with sign +} union {even i with sign -}`, using one-based indices,

the h-star polynomial is the sum of `z^des(alpha composed with inverse(sigma))` over all permutations sigma whose descent set is exactly D. It gives every coefficient a finite explicitly defined counting set. It does not claim a new theorem, a cyclic-order refinement, or completion of the authors' broader program. This mathematical audit grants none of those stronger claims.

## All-dimensions certificate checked independently

### Affine lattice equivalence, with dilation handled explicitly

At dilation m, write `y_i=x_i` at odd indices and `y_i=m-x_i` at even indices. The map is an affine involution with diagonal linear part having entries ±1 and integral translation. It bijects the integer cube `{0,...,m}^n` to itself. For odd i,

`x_i+x_(i+1)-m = y_i-y_(i+1)`;

for even i it equals `y_(i+1)-y_i`. Both directions of each weak inequality follow immediately, including equality. Thus the four orientation cases in the proof are correct: minus means increasing for odd i and decreasing for even i; plus reverses those choices. The even-coordinate translation is m rather than 1. At m=0 the original and transformed sets both contain exactly the origin.

The directed graph is an orientation of a path, so it cannot contain a directed cycle. Its transitive closure is a partial order. Edge comparisons suffice to enforce the entire closure, so there is no missing non-adjacent restriction. The transformed set is exactly its order polytope, using the convention `y_a <= y_b` for a smaller poset element a.

### Existence of labels, full dimension, and integrality

Every finite directed acyclic graph has a vertex with no predecessor: if none existed, repeatedly following predecessors in a finite set would produce a directed cycle. Repeatedly removing such vertices gives a linear extension and the candidate's deterministic natural labeling algorithm. A bijection alpha on the path vertices is natural exactly when its adjacent inequalities match the orientation. Its descents are therefore exactly D, without any additional condition hidden in the transitive closure.

For each extension word w, the region `0 <= y_(w1) <= ... <= y_(wn) <= 1` is contained in the order polytope. It is a full-dimensional simplex: in the w-coordinate order its vertices are zero and the n suffix-indicator vectors, whose successive differences are the coordinate basis vectors. The edge determinant has absolute value one. The point `y_(wj)=j/(n+1)` lies in its Euclidean interior. At least one extension exists.

Every point of the order polytope belongs to one such simplex by sorting coordinates and resolving ties through a natural labeling. Hence the polytope is a finite union of these integral simplices. Because the polytope is convex and contains all their vertices, it equals their finite vertex convex hull. This establishes full dimension and integrality independently of any external general triangulation theorem. The reflection transfers both properties to the original polytope.

### Boundary allocation has no missing points or overlaps

Fix any natural labeling alpha. Sort the vertices by the distinct lexicographic keys `(y_v,alpha(v))`. Comparable vertices appear in the correct order, even when their coordinates are equal, so this produces a unique linear-extension word w.

For that word, set `a_j=y_(wj)`. Assigned points satisfy weakly increasing coordinates, with a strict increase wherever the label word `alpha(w1),...,alpha(wn)` descends. Conversely, a sequence satisfying these conditions is order preserving because w is an extension. Inside each constant-coordinate block, no adjacent pair of labels can descend. Distinct labels are therefore strictly increasing throughout the entire block. Sorting by the same keys reconstructs w exactly. This proves necessity, sufficiency, exhaustion, and disjointness; it also handles equal-coordinate blocks of arbitrary length rather than only pairwise ties.

Let d be the number of required strict increases. Subtract from a_j the number of required strict increases before j. Adjacent differences stay nonnegative; the first value stays nonnegative; the final value is at most m-d. The inverse adds these same preceding strict steps. For m>=d this is a bijection with weak length-n sequences in `{0,...,m-d}`, counted by `binomial(m+n-d,n)`. For m<d there is no sequence. Equivalently, the first coordinate, successive differences, and final endpoint gap are n+1 nonnegative gaps totaling m-d.

The formal generating series of that count is `z^d/(1-z)^(n+1)`. Summing the disjoint pieces and multiplying by `(1-z)^(n+1)` proves the entire h-star polynomial, rather than only its value at one or its normalized volume. There is no analytic convergence assumption and no appeal to empirical interpolation to obtain the all-dimensions result.

### The inverse and labeling invariance are essential

For an extension word w define the rank permutation sigma by `sigma(w_j)=j`. Its adjacent descents are D, and `w_j=sigma^(-1)(j)`. Hence the label word is `alpha composed with inverse(sigma)`, exactly as displayed, rather than either of the other composition orders. This identifies the extension sum with the fixed-descent-class formula.

The partition proof works separately for every admissible alpha; its lattice-count left side is fixed. Consequently the entire distribution is independent of alpha. Individual permutations can change their statistic when alpha changes, which the candidate correctly permits. The constant coefficient is one: the unique increasing label word corresponds to the extension in natural-label order. The cases n=1, both n=2 signs, alternating sign words, complementation, reversal, and the mixed-sign nonpalindromic example all agree with the theorem.

## Reproduction and falsifiable controls

Both supplied checkers were copied into this audit's private replay area before execution. They were run without modifying the frozen source and reproduced their committed JSON results byte-for-byte:

- Authored verifier: 255 sign words through dimension 8, 46,233 permutation words, 2,558 Ehrhart evaluations, 79,657 pointwise reflection checks, and 12,195 tie-sort checks.
- Previous standalone review controls: 127 sign words through dimension 7; all 5,913 natural labelings; 679,917 relative-descent pairs; 1,277 dense counts; 253 direct grid counts; 245 boundary partitions; and 217 strict-interior reciprocity checks.

The fresh `exact_controls.py` was written for this review, with no candidate-code import and no third-party dependency. It uses explicit dense transition matrices for original adjacent-sum coordinates, enumerates rank permutations by descent sets, and independently reconstructs half-open pieces with their gap vectors. Its checks use explicit exceptions, so optimization does not disable them. Normal and optimized runs both passed, and their results agree after removing the timestamp alone.

Fresh coverage:

- All 511 sign words in dimensions 1 through 9 and all 409,113 rank permutations.
- Every natural labeling through dimension 7, and three selected labeling evaluations per sign word in dimensions 8 and 9: 7,065 evaluations in total. The selections can coincide in a one-element class; this count does not assert that they are all distinct.
- 1,889,517 evaluated alpha/sigma pairs; 6,652 exact formal-series coefficient checks, including vanishing coefficients beyond the claimed numerator degree.
- 7,674 dense original-coordinate lattice counts, including dilations 17 and 23 for every sign word; these are compared with the full binomial formula.
- 180,582 exhaustive pointwise dilation-reflection checks through dimension 6 at m=0,1,2,3; 252 direct grid counts and 20,510 admitted tie-sorted points.
- 612 exhaustive boundary partitions using every natural labeling through dimension 5 at m=0,1,2,3; 33,690 reconstructed points with explicitly validated nonnegative gap vectors, set equality, and multiplicity exactly one.

Five deliberate convention errors were detected. At n=3 with signs `--`, omitting the inverse gives `1+z^2`, while the correct polynomial is `1+z`; using raw vertex labels gives `2z`. Omitting strict gaps allocates the origin twice. Reusing T_1 on the 2-dilate maps an admitted point outside the transformed cube. Reversing equal-value label ties violates a generating comparison already at n=2 and m=0. These controls show that the checker distinguishes the conventions central to the theorem.

Reproduce the fresh controls with:

```sh
python3 -B exact_controls.py --max-n 9 --output replay.json
python3 -BO exact_controls.py --max-n 9 --output optimized_replay.json
```

All arithmetic is exact. These finite checks support and challenge the independently audited all-dimensions proof; they do not replace it. The original source and output pins are in `SOURCE_AUTHENTICATION.json`, `CANDIDATE_REPLAY_INPUTS.json`, `REPRODUCTION_RECEIPTS.json`, and `FINAL_INTEGRITY.json`.

## Exact remaining gap

**Mathematical interpretation gap: none found.** The literal-target resolution is a classical-corollary certificate. Historical priority and whether the result qualifies as an independently novel contribution remain unassessed by this family. No merge, publication, or status reclassification is authorized by this mathematical verdict alone. The parent must apply its separate priority and publication gates.
