# Independent audit: exact trajectory bridges and coordinate-rich pressing connectivity

## Verdict and frozen scope

**PASS. No substantive mathematical correction is required.** The following claims are accepted for the reviewed original inter-fiber candidate, 7,512 bytes, SHA-256 `fcdef47943f3f654ec14ffc1d2b746ca76f46d7232b80f4b9e778ec32f919118`. This identifies the reviewed original rather than the prepared edition; EDITORIAL_MAP.json records the precise, scope-preserving changes:

1. The maximum longest-common-subsequence length between two exact pressing-trajectory fibers is the maximum strictly increasing chain of nonempty intersections of their ordered layers.
2. Permutations and the four-position operation that replaces each of four orthonormal vectors by the sum of the other three generate all ordered orthonormal bases of the standard binary dot-product space, in every finite dimension.
3. For a symmetric binary matrix that admits a successful pressing word, if **every norm-one vector of its radical quotient is represented by an actual original coordinate vertex**, its successful-word graph is connected with adjacency `LCS >= r-4`, where `r` is the matrix rank.

The third result is conditional on the strong representation hypothesis. It is not a proof of the general Bixby–Flint–Miklós conjecture, a claim of novelty, a theorem for coordinate sets that merely span, or a transfer principle under arbitrary congruences. The audit makes no new assessment of the current literature status of the general conjecture.

The reviewed original structural dependency was 7,461 bytes, SHA-256 `834a488e71a321d82f6f2bac0eb029bc8a03d56cee63e61a6a7c5e0fe8952aa8`. Its Sections 1–3 are sufficient here. Their full-state and Cartesian-fiber assertions were checked directly in this audit as well as in the separate structural audit.

One harmless graph-language convention should be explicit when quoting the edge criterion: an edge **between trajectory vertices of a simple quotient graph** refers to distinct trajectories. The max-LCS identity itself also holds for identical trajectories. A singleton fiber need not contain a non-loop graph edge. This convention does not affect either connectivity proof.

## Definitions and source normalization

A symmetric binary matrix represents the colored graph by its off-diagonal adjacency entries and black diagonal entries. A legal press at `v` requires the current diagonal entry to equal one and updates the full matrix by `M -> M + (M e_v)(M e_v)^T`. Success means that the full original matrix becomes zero, including rows omitted from the word. Every legal press clears its row and column permanently and lowers rank by one. Thus every successful word has length `r` and has distinct labels.

For equal-length words of length `r`, insertion/deletion distance is `2(r-LCS)`. Therefore adjacency `LCS >= r-4` permits at most four deletions and four insertions, a combined budget of eight. It is not a combined four-edit bound. A word-position replacement may require one deletion and one insertion.

This normalization was independently checked against Conjecture 6 on printed page 47 of Eliot Bixby, Toby Flint, and István Miklós, *Proving the pressing game conjecture on linear graphs*, Involve 9:1 (2016), 41–56, DOI 10.2140/involve.2016.9.41. The publisher PDF was opened via the public web, its relevant extracted text inspected, and the supplied rendering of page 47 visually inspected. The conjecture's vertices are successful words and its formal edge condition is exactly the LCS threshold used here. [Publisher PDF](https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf). No outside group-generation theorem is needed or invoked.

## Independent mathematical verification

### 1. The structural facts really concern original labels and full states

Let `V = F_2^n / ker(A)` with its induced nondegenerate symmetric bilinear form. Write `x_v` for the image of original coordinate `v`. Gram–Schmidt on one successful word produces an orthonormal basis `f_1,...,f_r`. With `c_i(v)=B(x_v,f_i)`, the full matrix after its first `k` presses is

`M_k = sum_{i>k} c_i c_i^T`.

This is a full `n`-by-`n` equality, not merely a congruence or a submatrix identity. Indeed the chosen pivot at step `i` has residual column `c_i`, and the press removes precisely its outer product.

A vertex lies in layer `L_j` exactly when `j` is the last nonzero coordinate of `x_v` in this basis. It then has residual vector `f_j` and residual column `c_j` just before step `j`. Every choice from that layer induces the same full next state. The layers are disjoint and nonempty, so arbitrary simultaneous choices give a successful word without repeated labels.

Conversely, a legal press producing that exact transition has update column `d` with `d d^T = c_j c_j^T`. Over the binary field, equality of diagonals forces `d=c_j`. The columns `c_i` are independent, so expansion in the residual columns forces the last nonzero coordinate to be `j`. Thus the fiber really is the entire Cartesian product, in both directions. Original zero rows do not belong to any layer and can never occur in a successful word.

### 2. Maximum LCS is exactly the strict marked-cell chain length

A common subsequence picks strictly increasing positions in each word. Each paired position is a nonempty layer intersection, giving a chain of marked cells and proving the upper bound.

For a strict chain, choose one original vertex in each marked intersection. Those choices are distinct because their first-layer indices are distinct. No chosen vertex can clash with a filler in another layer of either word: layers in each partition are disjoint. Fill the remaining positions arbitrarily; the Cartesian-fiber fact proves both completed words successful. The selected labels form a common subsequence of the chain's length. This proves equality and, for distinct trajectories, the exact inter-fiber edge criterion.

Strict increase in **both** indices is essential. A matching without order, an increasing condition allowing repeated indices, or the number of marked cells alone does not give the required LCS.

### 3. The four-position transformations generate every orthogonal matrix

The four-position block is `I_4 + J_4`: its diagonal is zero and all off-diagonal entries are one. It replaces each selected vector by the other three. Since `J_4^2=0` in characteristic two, the block squares to identity. Direct products of columns give norm one and pairwise inner product zero. Outside the block the basis vectors are fixed.

For an arbitrary orthogonal matrix `Q`, perform left reductions in a residual block of dimension `m`. Its first column `v` has odd weight. If `m>1`, it cannot be the all-ones vector `w`: another orthonormal column `u` would have simultaneously `u dot w = u dot v = 0` and `u dot w = u dot u = 1`. In even dimension `w` has norm zero already. Thus an odd-weight column of weight at least three has a zero coordinate as well as at least three one coordinates.

Select three of its one positions and one zero position. Their indicator `z` has norm zero, and `I + z z^T` is the four-position block. Because `v dot z=1`, it changes `v` to `v+z`, lowering weight by two. Repeat to weight one and swap that coordinate into the first position. Orthogonality then clears the first coordinate of every other column. Induct entirely inside the remaining block, preserving already fixed columns.

The canonical all-ones vector therefore causes no gap. In odd dimension greater than one it is a norm-one vector that cannot be a column of an orthonormal basis; the proof never tries to transform a basis column into it. The same argument applies inside each residual block. In rank one it is the unique basis vector. In ranks two and three every permissible first column already has weight one. In rank zero the empty basis is the unique basis. These cases require no four-position move.

The left/right distinction is important and correct. If left reduction records involutions `L_1,...,L_k` in chronological order, then `L_k ... L_1 Q = I`, hence `Q = L_1 ... L_k`. Starting from the standard ordered basis and applying the same list in that order on the right constructs `Q`. More generally a basis matrix `B` reaches `B Q` by right multiplication. Only this right action changes at most the selected four basis positions. One must not use a left ambient-coordinate action on an arbitrary basis to claim a four-position word bound.

### 4. Strong richness makes every bridge a word in the original graph

For each norm-one quotient vector choose a fixed original representative `rho(y)`. This is possible by hypothesis, and the representative function is injective: one original label has only one quotient image. Thus orthonormal basis vectors receive distinct actual labels.

For any successful word with induced basis `f_1,...,f_r`, the vertex `rho(f_j)` has coordinates zero except for a one at position `j`. It lies in layer `L_j`. Replacing each position separately connects the given word to the representative word while preserving its entire trajectory. Each step retains at least `r-1` positions.

Every ordered orthonormal basis of quotient vectors yields a successful word of these actual representatives. At each stage its next representative has norm one in the remaining perpendicular space; after all `r` presses every coordinate vector has zero projection to the residual space. Consequently the **full original matrix** is zero, including extra, repeated, zero, and norm-zero coordinate vertices. This argument does not demand that the original labels themselves be independent in `F_2^n`; independence is in the quotient, exactly where it is needed.

The basis-generation path is therefore a path of successful words on the original alphabet. A swap changes at most two positions; a four-position transformation changes at most four. Leaving all unaffected positions in their original order gives `LCS >= r-4`. New representatives cannot collide with unaffected representatives because the new list is still an orthonormal basis and hence consists of distinct vectors. Concatenate the initial fiber path, this basis path, and the reversed target fiber path. Every edge meets the original BFM bound.

Rank zero has one successful word, the empty word; the conclusion is immediate. For ranks at most four the threshold is nonpositive and the entire successful-word graph is already complete. The generation argument remains correct in those ranks.

### 5. Why the representation hypothesis cannot be silently weakened

Coordinate images always span the quotient. This is far weaker than representing every norm-one vector. For example, the four standard coordinate vectors span `F_2^4` and give a successful word, but the four-position transformation requires the vectors with masks `14,13,11,7`, none of which is an original vertex in that coordinate set. This example is a failure of that proposed lifting step, **not** a counterexample to general BFM connectivity.

For `r>=1`, the strong condition requires at least `2^(r-1)` distinct original labels, because the norm functional in a standard dot-product space has that many norm-one vectors. It is a genuine additional restriction and is nonvacuous: taking all odd-weight vectors as labeled coordinates includes a standard orthonormal basis. Extra labels of any quotient type are allowed.

The hypothesis that a successful word exists must also remain explicit. Without it, a nonzero alternating quotient has no norm-one vectors, so a superficially similar representation condition is vacuous and supplies no successful word. No conclusion about such an empty state space is intended here.

## Independent bounded checks

A checker was independently authored for this audit. No source-author checker was read, imported, copied, or executed. The checker uses explicit exceptions rather than Python `assert`, so optimized Python cannot disable its validations.

All full checks passed under normal Python, `python -O`, and `python -OO`:

- **49,092 unordered pairs with replacement of ordered partitions**, across every labeled universe of size zero through five and every possible layer count. The marked-grid dynamic program agrees with direct enumeration and intersection of all subsequence sets from all Cartesian-fiber words. This includes 1,480 enumerated fiber words.
- **All 23,818 ordered orthonormal bases in ranks zero through six**, independently enumerated by choosing norm-one mutually orthogonal columns. Counts by rank are `1,1,2,6,48,720,23040`. Every basis passes canonical-vector preservation, the all-ones-column restriction, left reduction, and right reconstruction with correct ordering. A separate generator-closure BFS equals the complete enumeration in ranks zero through five, with 11,156 generator applications.
- **210 deterministic higher-rank algebra samples** in ranks 7, 8, 9, 12, 16, 24, and 32. These are generator-produced samples, not an exhaustive group enumeration. They pass reduction/reconstruction and support-size checks.
- **860 exhaustively enumerated successful words on five explicitly rich test matrices**, at ranks zero through four with 1, 3, 5, 7, and 11 original vertices. The coordinate lists include duplicate and zero images and, where possible, a nonzero norm-zero image. Exact trajectory counts are 1, 1, 2, 6, and 48. All Cartesian-fiber descriptions and 1,202 unordered trajectory pairs with replacement agree with direct full-state pressing and subsequence enumeration.
- **90 deterministic higher-rank rich-graph paths** in ranks five, six, and seven. These test matrices represent all quotient vectors and also contain duplicate and zero images. Input words include nontrivial unit-lower-triangular flags; every fiber replacement preserves all states, and each algebraic basis step uses distinct original labels, is successful on the full matrix, and meets `LCS >= r-4`. Across the graph checks, 2,017 actual edges were checked.
- **Seven negative controls** reject a changed source pin, a repeated-label word, a nonorthogonal basis, an invalid three-position transformation, replacing richness by spanning, confusing four substitutions with a combined four-edit budget, and a marked chain that reuses a layer.

These finite computations are diagnostics supporting the independently checked all-rank proof. They are not an exhaustive check of arbitrary input graphs, not a test of the general BFM conjecture, and not substitutes for the argument.

## Integrity and reproducibility boundary

The reviewed original proof bytes were checked before and after the recorded runs. Preparation reverified both accepted audit bundles and reran their independent checkers under normal Python, -O, and -OO. The complete public aggregate results and checker/result hashes are in VERIFICATION.json; the original-to-prepared proof and audit mapping is in EDITORIAL_MAP.json. All independent mathematical reconstruction text above is preserved exactly.

This prepared edition corrects the bibliographic page range from 41–53 to 41–56, verified against the publisher PDF, without changing the mathematical claims or acceptance. It removes operational references to material outside this appendix. Executable checkers and raw finite-search outputs are not part of this public payload, so this appendix does not claim a self-contained executable reproduction bundle. The full authored proofs and independent mathematical audits are included. Finite checks corroborate those arguments and do not prove an unbounded theorem on their own.
