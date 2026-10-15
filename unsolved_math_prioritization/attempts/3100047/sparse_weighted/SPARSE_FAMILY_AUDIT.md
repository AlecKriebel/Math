# Independent audit: endpoint normal form and sparse pressing family

Problem 3100047 / row 1747. Audit date: 12 October 2026 UTC.

## Disposition and scope

**ACCEPT the two bounded arbitrary-order results and the one-moving-block corollary, for the exact original bytes identified by the sparse-proof record in ORIGINAL_INPUT_PINS.json. No mathematical correction is required.** Acceptance does not extend to later edits, to a proof of the unrestricted pressing 1/3–2/3 conjecture, or to a theorem controlling arbitrary instructional-class mixtures. The author explicitly retains those boundaries.

The audit independently derived the determinant identity, endpoint boundary conditions, affine dimension, complete sparse successful language, singleton classes, pair probabilities, and balance value. It did not treat finite experiments as proofs of the arbitrary-order claims. There is no reliance on an external source theorem.

The original report under review is identified as sparse-proof in ORIGINAL_INPUT_PINS.json; its public editorial version is ENDPOINT_NORMAL_FORM_AND_SPARSE_FAMILY.md. The same metadata identifies the original evidence, freeze, audit acceptance and external seal that bind this historical disposition to the accepted original bytes. The accepted report is 14,247 bytes with SHA-256 8a34318df6abbaf85b39ea81e43922b3723fee5f85795e57b9c2e9f00c98b1c1; the accepted FREEZE.json has SHA-256 071a5fdb6ea9ea1358ba9313f0956570c4d14035347c67a663d0f720498a7284.

## 1. Determinant identity and local-to-global reduction

Let U be unit upper triangular over F_2. Then A=U^T U is nonsingular and has the identity as a successful full-length pressing word. Every successful ordering is exactly an ordering whose leading principal determinants all equal 1: successive scalar elimination pivots are their ratios, and the only nonzero scalar is 1.

For an endpoint exchange on an interval [i,i+d], first eliminate the unchanged preceding prefix. The residual restricted to the interval is the Gram matrix of its principal U block. Rows of U later than the interval vanish in these columns. Once the same interval set is eliminated legally in either order, the residual on the unchanged suffix is the same Schur complement. Thus testing the isolated local block is necessary and sufficient, including intervals with a nonempty prefix or suffix.

Here is an independent derivation in zero-based prefix notation, to make the indexing transparent. Write the local root as [[R,c],[0,1]], with R of order d and c=(c_0,...,c_(d−1)). Let v=e_0^T R^(-1) and h_k=sum_(j=0)^k v_j. The altered ordering is (d,1,...,d−1,0). After its first k+1 letters, 0<=k<d, the principal determinant is

F_k = h_k (1 + sum_(j=k+1)^(d−1) c_j) + sum_(j=0)^k v_j c_j.

Indeed, the columns indexed 1,...,k are supported in rows 0,...,k. Their maximal minors are v_0,...,v_k, because deleting row 0 leaves a unit-upper matrix and the cofactor vector is their normalized left-kernel vector. Cauchy–Binet gives h_k times the squared norm of the last column below row k, plus the squared determinant obtained by including its first k+1 entries. Over F_2 squaring is the identity; the last root diagonal contributes the constant 1. This proves the displayed formula. The full (d+1)-set already has determinant 1, so these are all the missing tests.

The author's notation has H_(k+1)=h_k and includes x_d=1 in T. Consequently its identity (1) is exactly this formula. Subtracting neighboring determinants yields the stated homogeneous adjacent constraints, and the first determinant is precisely T_0. This proves both directions of the specified-column normal form; the existence condition alone is correctly not substituted for it.

## 2. Isolated-root boundaries and affine count

The root's consecutive entries equal 1 exactly when its identity ordering has no successful adjacent transposition. For two consecutive legal presses, reversing their order is possible exactly when their current edge is zero; that edge is the corresponding root entry.

For a chain root R of order d>=2, v_0=v_1=1. In this audit's notation h_0=1 and h_1=0. The final chain entry requires c_(d−1)=1. The first determinant forces sum c_j=0. Define z_k=1+sum_(j=0)^k c_j. Then

h_(k−1) z_k + h_k z_(k−1)=0,  1<=k<d,
z_(d−2)=0, z_(d−1)=1.

The last equation is possible only if h_(d−2)=0. It is sufficient: set z_0,...,z_(d−2) all to zero and z_(d−1)=1. This corresponds to the author's explicit column (4). Thus existence holds exactly when H_(d−1)=0 in the author's notation.

Distances 1 and 2 are impossible under the consecutive-entry condition. For d=1 the second initial diagonal is zero. For d=2 the condition asks h_0=0 although h_0=1. At d=3 the required h_1=0 is automatic. These boundary cases are not extrapolated from an inapplicable run formula.

When the condition holds, consider h_0,...,h_(d−2), beginning 1,0 and ending 0. Along a maximal run of ones all associated z entries must be equal, with one free bit. At a zero adjacent to a one, its z entry is forced to zero. A zero whose two neighbors are zero contributes one free bit, except that the right endpoint is already fixed. Therefore the number of free bits is the number of maximal one-runs plus the number of internal zero-triple centers. Translation of indices gives exactly formula (6).

This is a count of distinct final columns for fixed R. Each resulting root is a different unit-upper root in the same identity order; triangular Gram uniqueness implies its matrix is also different. It is not a count of words, classes, or class weights inside one fixed symmetric matrix. The original report states this distinction correctly.

## 3. Complete sparse language, with no missing words

For n=2m>=4, the stated root has columns e_0; e_0+e_1; e_0+e_1+e_2; and e_(j−1)+e_j for j>=3. Their pairwise dot products give exactly the path 1–0–2–3–...–(2m−1) with loops at 0 and 2. Invertibility follows from its triangular diagonal.

The following branching argument proves completeness, not merely successful replay of the proposed words.

- Only 0 and 2 are initially legal.
- Pressing 0 leaves the path 1–2–... with its unique loop at its endpoint 1. At each step there is exactly one legal vertex; its press transfers the loop to the next endpoint. Hence the entire remaining word is forced to be 1,2,...,2m−1.
- Pressing 2 makes 3 the unique looped vertex, so 3 is forced next. If m>=3, pressing 3 leaves the same family on labels (0,1,4,5,...,2m−1). For m=2 it leaves the edge 0–1 with its only loop at 0, forcing 0,1.

Induction therefore gives exactly m words: insert the ordered block (0,1) into one of the m gaps among the fixed ordered blocks (2,3),(4,5),...,(2m−2,2m−1). There is no unexamined initial choice or internal branch. In the even-order family every legal branch described here completes.

Each consecutive pair in any resulting word is adjacent immediately before pressing the earlier member. Before the inserted block, the recurrence follows consecutive edges; at insertion it enters 0 along the current edge; within and after insertion the looped-endpoint path forces consecutive neighbors. Therefore each word's instruction root contains the full consecutive chain, and its instructional poset has exactly that one linear extension. This independently proves singleton classes. The author's alternative argument, using the absence of an adjacent-swap edge and connectedness of each linear-extension class, is also correct.

## 4. Exact probabilities and balance

Index the insertion gap by t=0,...,m−1. For x in {0,1} and y in block (2r,2r+1), 1<=r<m, the event x precedes y is exactly t<r. Thus its exact probability is r/m. The pair 0<1 and all comparisons between tail labels are fixed; there are no others.

The variable-order graph is consequently K_(2,2m−2), with 4m−4 variable unordered pairs, and it is connected. The maximal minority probability is floor(m/2)/m. It equals 1/2 when m is even and is at least 1/3 when m is odd and m>=3. This proves the claimed balance for every member of the family, including the sharp value 1/3 at m=3. The conclusions about unboundedly many singleton classes apply to this explicitly proved family; they do not imply anything about arbitrary class mixtures.

For the one-moving-block corollary, order the q permitted distinct insertion gaps t_1<...<t_q. With k=floor(q/2), the letter immediately after gap t_k exists because k<q. Any fixed member of the moving block precedes it in exactly the first k words. Hence the pair probability is k/q in [1/3,1/2]. This is valid only for the whole uniformly sampled language, as the original report explicitly requires.

## 5. Independent finite checks and controls

independent_verify.py imports none of the author's code. Successful languages are enumerated by principal determinants rather than the author's rank-one-press recursion. Direct pressing is used separately to cross-check resulting roots. All failures use explicit exceptions, not removable Python assert statements.

The completed checks are:

- Every sparse order n=2,...,40. All even orders 4,...,40 have exactly the stated m complete words, singleton chain roots, exact pair counts, and complete variable graph. n=2 is a one-word boundary control.
- Odd orders 3,...,39: exactly floor(n/2) complete words with the last vertex forced, and exactly one legal-but-trapped terminal branch, namely (2,3,...,n−1). These controls show that legal-prefix enumeration does not silently assume completion.
- For n<=12, dense determinant and independent path-determinant recurrence agree on every principal subset. The path recurrence is then used for larger orders: on a selected path component its determinant satisfies D_j=loop_j D_(j−1)+D_(j−2), with missing vertices splitting determinant factors.
- All chain roots and all permitted final columns at distances 2,...,6. This tests 33,866 matrices. Additional deterministic samples of 64 prior roots each at distances 7 and 8 test every final column, giving 46,154 endpoint-column checks in total. In every case the direct leading determinant equals the independently derived formula, success agrees, and the exact total equals the run-count formula.
- All 1,098 unit-upper roots of orders 2,...,5, without the chain restriction, and all 10,650 endpoint intervals. Direct full-matrix determinant tests match the local normal form, covering nonempty prefixes, nonempty suffixes, and adjacent-swap isolation.
- Affine-system Gaussian elimination agrees with the run-count dimension for every inverse first row beginning (1,1) through distance 16, and deterministic long controls at distances 17,31,32,63,64,127,128: 32,956 controls in total. Such rows are realizable by chain roots: keep the superdiagonal and choose each later first-row entry recursively to enforce the chosen inverse row.
- Normal Python, -O, and -OO complete all independent checks and produce byte-identical JSON evidence. Both frozen original verifiers were also replayed in separate copies under all three modes: all six runs passed and reproduced the original JSON bytes exactly. The originals were rehashed afterward and remained unchanged.
- Negative controls changing the sparse chord, omitting the last successful word, or changing the affine count all fail explicitly. These mutations were applied only to temporary copies of the independent verifier.

The exhaustive count histograms through distance 6 agree with the original report: d=2 has one root with zero columns; d=3 has two roots with two columns each; d=4 has four with zero and four with two; d=5 has 32 with zero and 32 with four; d=6 has 512 with zero, 384 with four, and 128 with eight.

These tests corroborate the proofs and check indexing/boundaries. They do not exhaust arbitrary pressing matrices of larger order.

## 6. Final boundary

No defect was found in the frozen mathematical report or the stated proof-evidence claims. The original unrestricted conjecture remains open in this packet. Accepted progress consists of the arbitrary-length endpoint-column normal form/count, the complete sparse family theorem and exact marginals, and the precisely stated whole-language moving-block criterion. Any changed original byte invalidates the sealed acceptance until re-audited.
