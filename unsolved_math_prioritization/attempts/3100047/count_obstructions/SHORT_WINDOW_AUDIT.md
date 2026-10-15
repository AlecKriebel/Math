# Independent audit of the short-window count obstructions

Problem 3100047 / queue row 1747. Audit completed 12 October 2026 UTC.

## Decision

**ACCEPTED within the expressly limited scope below.** The frozen final report's three local theorems, common-context multiplicities, exceptional-endpoint reductions, and counterexamples are correct. The independent proofs and checks below require no external classification of uniquely pressable matrices. There is no remaining mathematical correction needed for acceptance.

This acceptance does **not** establish balance for every pressing family with four, five, or six full successful words, a finite ambient-dimension bound, a characterization of unique pressability, or a resolution of the general pressing-sequence balance problem. The count thresholds are sufficient consequences of guaranteed word bundles, not claims of optimal thresholds among all realizable pressing languages.

The original audit preserved the originals, created a separate result, and performed no repository or publication action.

## 1. Precisely accepted source

Accepted edition: the window-proof and window-input-manifest records in ORIGINAL_INPUT_PINS.json.

Accepted original report (public editorial version: SHORT_WINDOW_COUNT_OBSTRUCTIONS.md):

- 14,585 bytes
- SHA-256 `1229e7a6179d69f2dac9f0ca3c87c9e793ec6113f6c5ee2fd13ce296bcdf3d7e`

Accepted original edition manifest (window-input-manifest in ORIGINAL_INPUT_PINS.json):

- 1,164 bytes
- SHA-256 `50d6f89d73a561ac8617d8f432d7a81b0f1255f6df4239fe939a94551f416e19`

The separate source freeze record has SHA-256 `ff03092c3cbcae2859522022798488dd0d6254ec5f2a6a39f4a433f4ba8ee97c`. Every file in the source manifest was independently checked against both its byte count and SHA-256 digest. The acceptance applies to these exact final bytes. The earlier 02:27 and 02:28 editions are preserved but are not the acceptance target.

### Corrections and clarifications

The final edition already incorporates the required endpoint correction: symmetric **Gram matrices** of first- and last-deleted triangular root blocks are uniquely pressable, rather than the triangular blocks themselves being described as symmetric pressing matrices. The first Gram matrix represents the Schur residual; the last represents an original principal restriction. Section 7 below verifies both identities explicitly.

One harmless shorthand in Theorem 2 says that two disjoint swaps “preserve that root.” The rigorous content is preservation of the pertinent zero swap conditions under the corresponding reordering, or, equivalently, preservation of the residual after the first swapped pair has been eliminated. It is not literal equality of two differently ordered triangular arrays. The setwise proof in Section 4 below supplies the precise argument and validates the stated theorem without this shorthand. No source edit is needed for this audit's mathematical acceptance.

## 2. Basic elimination and substitution

Let A be a nonsingular symmetric matrix over F2 with nonempty full successful language, and let Z be its cardinality. All successful words are permutations of the same full label set. A pair is balanced exactly when both orientation counts are at least Z/3.

Scalar elimination in a specified order gives the pivot at step j as det(A[S_j])/det(A[S_(j-1)]) whenever the previous pivots exist. Thus full success is equivalent to all leading principal determinants being one. This statement does not equate nonsingularity of an arbitrary principal matrix with existence of a successful coordinate order.

If a legal prefix uses label set S, its remaining matrix is the Schur complement R_S. The formula depends on S alone. For disjoint Q, pressing only Q calculates all its internal pivots within R_S[Q]. If a local Q-order succeeds, eliminating Q leaves R_(S union Q), independently of its order. Therefore any local successful Q-order can replace another in a fixed successful word P Q R, with the same ordered prefix and suffix.

This proves the arbitrary-ambient substitution step required by all three local theorems. Interactions with labels outside Q do not affect internal legality or the eventual suffix state. Empty prefixes and suffixes are permitted.

## 3. Reversal on three labels

After eliminating the common prefix, write the unit upper root for abc as

U = [[1,p,q],[0,1,r],[0,0,1]],  B = U^T U.

Success of cba forces B_cc=1, or q=r. With B_bb=1+p and B_bc=pq+r, its two-label leading determinant gives

(1+p) + (pq+r) = 1,

hence p+pq+r=0. After q=r this is p+pq+q=0. If p=1 the left side is one; if p=0 it is q. Consequently p=q=r=0 and B=I_3.

All six local permutations therefore succeed, and common-context substitution produces six distinct full words. Each of the three internal pairs occurs three times in each direction within this bundle. Extra full words cannot reduce either count. Thus all three pairs are globally balanced whenever Z<=9, with equality included. The hypothesis itself implies Z>=6, so numerical cases Z<6 are simply impossible under the hypothesis.

For the abstract language {012435,012534,013425,230415}, the first two words have common prefix 012 and reversed triples 435 and 534. The theorem forces all six suffix permutations, including 012345. Independent checks also confirm the stated transitive majority order 012345, its absence from the abstract language, and closure under all prefix-set splicings. This is a genuine algebraic obstruction beyond that abstract closure property.

## 4. Three support words on four labels

Assume the common-context words abcd, abdc, and cdab succeed locally.

### Case 1: bacd succeeds

For an adjacent successful pair xy, its two-label residual has first pivot one. The pair can be swapped successfully exactly when their current off-diagonal entry, equivalently the corresponding consecutive root entry, is zero. Thus abcd and bacd permit swapping a,b; abcd and abdc permit swapping c,d.

After eliminating a,b, the residual depends only on {a,b}. It is identical whether the prefix was ab or ba. Since dc succeeds after ab, it also succeeds after ba. Therefore badc succeeds. The four distinct words abcd, abdc, bacd, badc give two orientations of (a,b) each. This argument avoids any literal-root-equality interpretation.

### Case 2: bacd fails but acbd succeeds

Use the four distinct words abcd, abdc, acbd, cdab. In the first two b precedes c, while in the latter two c precedes b. Thus (b,c) has a 2:2 guaranteed bundle.

### Case 3: bacd and acbd fail

Write

U = [[1,p,q,r],[0,1,s,t],[0,0,1,u],[0,0,0,1]].

The adjacent-swap test gives p=s=1 and u=0. Success of cdab begins with B_cc=1+q+s=1, so q=1. Its cda prefix has determinant one. Since det B=1, the cofactor formula equates this determinant with (B^-1)_bb. The b-row of U^-1 is (0,1,s,t+su); its self-dot-product over F2 is 1+s+t+su=t. Thus t=1.

Only r remains. The two matrices are

B_0 = [[1,1,1,0],[1,0,0,1],[1,0,1,1],[0,1,1,0]],

B_1 = [[1,1,1,1],[1,0,0,0],[1,0,1,0],[1,0,0,1]].

In B_0, c is looped, pressing c makes d looped, and pressing c,d leaves I_2 on a,b. Hence both cdab and cdba succeed.

In B_1, d is looped, pressing d leaves c looped, and pressing d,c leaves [[1,1],[1,0]] on a,b. Hence dcab succeeds. Together with the three assumed words, the guaranteed bundle is respectively

- abcd, abdc, cdab, cdba;
- abcd, abdc, cdab, dcab.

Every cross-pair from {a,b} x {c,d} has two occurrences of each direction in these bundles.

The cases exhaust the possibilities. In each case one fixed pair receives at least two full words in each direction after substitution. Thus Z<=6 suffices, including Z=6. The hypothesis and proof force at least four successes, so the conclusion does not assume a realizable Z=3 instance. No failure hypotheses are needed in the theorem statement; failures only select a proof case.

## 5. Relocation of one label

Suppose a b1...bk and b1...bk a succeed in the same context. In the residual write a's diagonal as alpha, the other block as B, and the coupling as v. The first order gives alpha=1. The second gives a successful b-order, hence B=C^T C with C unit upper triangular. Set v=C^T z.

For every first-j restriction, upper triangularity yields v_j=C_j^T z_j. Both B_j and the block on a,b1,...,bj have determinant one. Taking the scalar Schur complement gives

1 = alpha + v_j^T B_j^-1 v_j = 1 + z_j^T z_j = 1 + sum_(i<=j) z_i.

The j=1 equation and differences of successive equations give z_i=0 for every i. Thus v=0. The label a is looped and isolated from this entire local block; it commutes with all its presses. Every one of the k+1 insertion positions is legal, and setwise elimination preserves the suffix.

For j in {1,...,k}, a precedes b_j in exactly j insertion gaps and follows it in exactly k+1-j. Choosing j=floor((k+1)/2) yields lower bound floor((k+1)/2) in each direction and sufficient condition

Z <= 3 floor((k+1)/2).

Boundary checks:

- k=0 has one empty-block insertion and no comparison claim.
- k=1 has a 1:1 bundle and sufficient threshold Z<=3.
- k=2 has a 1:2 bundle for a middle choice, again threshold Z<=3.
- k=3 and k=4 give minority lower bound two, hence threshold six.
- k=5 gives minority lower bound three, hence threshold nine.

At equality the lower count is exactly Z/3. Additional successful local orders may establish balance beyond these sufficient thresholds; no maximality claim is accepted.

## 6. Exact weighted common-context counts

Fix the local label set Q and its ordered support words. For each qualifying preceding set S, a full realization is determined uniquely by:

1. one of the F(S) legal orders of S;
2. the fixed successful local word on Q;
3. one of the G(S union Q) successful completions of the common residual.

Conversely every such choice succeeds by setwise substitution. Thus each local word has exactly F(S)G(S union Q) full realizations.

Different S cannot duplicate a full word: a full permutation contains each member of Q once, and a consecutive occurrence of that fixed label set has one preceding label set. This disjointness is asserted only for the fixed Q; arbitrary different windows must not be summed without further overlap control.

It follows that the six-word triple bundles give exactly 6W distinct full words and 3W per direction of each fixed internal pair. The relocation bundles give (k+1)W words, with jW and (k+1-j)W for the same fixed pair across contexts. The resulting sufficient thresholds Z<=9W and Z<=3 floor((k+1)/2)W are correct, with inclusive endpoints.

The four-label case requires fixing the comparison before summing. Different residual cases can certify different pairs, so summing all case-dependent contexts for a supposed single pair would be invalid. The final report correctly forbids that inference. Restricting to contexts certifying a fixed pair gives at least 2W in each direction and hence sufficient threshold Z<=6W.

F and G are genuine completion counts. A nonsingular principal set may have F=0, and a nonsingular residual may have G=0. In particular I_1 direct-sum [[0,1],[1,0]] is nonsingular and allows a first press, but has no full successful order. Neither the proof nor the checks replace completion existence with determinant nonvanishing alone.

## 7. Exceptional endpoint branches

For Z=4,5,6, the possible forward counts of a balanced pair are respectively {2}, {2,3}, and {2,3,4}. Therefore an unbalanced family has minority count at most one for every pair. All majority probabilities are strictly greater than 2/3.

The majority tournament has no directed triangle: any full permutation satisfies at most two edges of such a triangle, whereas three majority probabilities greater than 2/3 would have sum greater than two. A triangle-free tournament is transitive. Denote its total order by v1,...,vn. This order is a combinatorial majority order; the argument does not claim it is itself successful.

If x!=v1 begins any successful word, every word beginning x reverses the majority comparison with v1. There can be at most one such word. Since the branch is assumed nonempty, it has exactly one word. Prefixing x bijects successful orders of the Schur residual after pressing x with this branch, so that residual is uniquely pressable.

If y!=vn ends any successful word, the same count gives exactly one word in that last-letter branch. Its preceding principal matrix A[E minus {y}] is nonsingular. Every successful order of that principal matrix extends by y, because the final scalar Schur complement is det A / det A[E minus {y}] = 1. This gives unique pressability of the original principal restriction, not of an unrelated Schur residual.

For a successful word with root U in that word's order, write

U = [[1,w],[0,V]].

Then U^T U has lower-right block w^T w + V^T V. Eliminating the first label removes w^T w, leaving V^T V. Thus the first-deleted root block has Gram matrix equal to the first-press Schur residual.

For the final-label deletion, write

U = [[W,c],[0,1]].

The original top-left principal block of U^T U is W^T W. Thus the last-deleted root block has Gram matrix equal to the original principal restriction. These are exactly the two matrices corrected and identified in the final report. If both endpoints are exceptional, both Gram matrices are uniquely pressable by the two proved bijections. No unique-root characterization, truncation experiment, or unpublished classification is used.

## 8. Selected-triple majority counterexample

The symmetric binary matrix with row masks (29,6,31,21,13) has exactly 20 successful full words. Independent determinant enumeration verifies all three selected words 01234, 23104, 24103. Every pairwise strict majority comparison of this triple agrees with total order 21034.

The principal matrix on {2,1} is [[1,1],[1,1]], with determinant zero. Therefore the majority order fails on its second step. This correctly refutes the stronger selected-triple majority-closure shortcut. It provides no unbalanced Z=4,5,6 pressing example and supplies no counterexample to a claim about the majority of the entire language.

The independent output retained with the original audit evidence records the exact 20-word language; it agrees with the author's language list. Raw outputs are not distributed in this prose-only edition.

## 9. Independent executable evidence

The separate independent verifier retained with the original audit evidence, and not distributed in this prose-only edition, imports none of the author's functions. Its legality tests use F2 Leibniz-expansion determinants and leading-set conditions, rather than the author's direct rank-one replay. All checks use explicit exceptions and remain effective under Python -O and -OO.

The independent checks establish:

- All 64 symmetric three-label matrices: exactly one qualifies for the forward/reverse hypothesis, and it is I_3.
- All 1,024 symmetric four-label matrices: six qualify for the support hypothesis, split into three disjoint-swap cases, one middle-swap case, and two residual-classification cases. Their full local language sizes are 24, 12, 8, 6, 4, 4, and each stated pair bound holds.
- 1,834 first- or last-branch bijection checks across successful three- and four-label matrices.
- All 1,099 unit upper roots in dimensions one through five: both Gram identities hold. Relocation qualifiers by dimension are 1,1,2,8,64, exactly the cases with the relocated label isolated within the local block. Every guaranteed insertion and orientation count is checked.
- 100 deterministic ambient examples in dimensions three through six: the weighted identities are checked by enumerating actual full words. There are 29 qualifying triple contexts, 45 three-label relocation contexts, 12 four-label relocation contexts, and 13 four-support contexts certifying fixed pair (0,2). Respectively 12,14,3,4 contexts have multiplicity greater than one. Per-local-word products, aggregate counts, and cross-context disjointness all pass.
- The majority counterexample, the abstract prefix-splicing diagnostic, the nonsingular dead-residual control, and all Z=4,5,6 balanced-count boundaries pass.
- A separate exhaustive check of abstract four-label permutation families of cardinality four through six verifies the majority transitivity and exceptional-endpoint count inference whenever no balanced pair occurs. Explicit five- and six-label adjacent-swap families supply nonvacuous Z=5,6 controls. These are abstract combinatorial controls, not an ambient pressing census.

Both the independent verifier and the author's frozen verifier were executed normally, under -O, and under -OO. Each verifier's three outputs were byte-identical. The three author replays match the archived source outputs exactly. Source hashes were checked again before sealing.

These finite computations corroborate local identities and implementations. The proofs in Sections 2–7 carry the arbitrary-dimensional claims. None of the finite computations provides or assumes an ambient search bound.

## 10. Final acceptance boundary

Accepted: common-context three-reversal and four-support obstructions; arbitrary one-letter relocation and its exact guaranteed insertion counts; properly fixed-pair weighted versions; singleton exceptional-endpoint branches and their precise Gram identities; and the limited selected-triple majority counterexample.

Not established: that every pressing family with four, five, or six successes contains one of these patterns or otherwise must have a balanced pair. That coverage/impossibility step remains open in this packet. Exploratory truncation scripts are excluded from the accepted proof and audit dependencies.

**Final decision: accepted, with no outstanding mathematical correction.**
