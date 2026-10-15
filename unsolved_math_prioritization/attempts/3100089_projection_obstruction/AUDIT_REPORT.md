# Independent acceptance: unbounded one-vector recovery distance

This is the symbolic-only publication edition of an AI-assisted independent mathematical audit. It is unrefereed and is not external human peer review or proof-assistant certification. The complete symbolic reconstruction below is unchanged. EDITORIAL_MAP.json records the edition changes and exact block hash.

## Verdict

**ACCEPT, with no correction required to the symbolic theorem.** For every rank r≥2 the stated one-vector augmentation has exact minimum recovery distance ceil((r−1)/4), both from the designated two-word reverse fiber to the original successful-word set and from its trajectory to the old-realized trajectory in the full augmented trajectory quotient. The distances are unbounded with r.

The exact word distance is a minimum over the designated two-word fiber. This report does not strengthen that statement to equality for every individual representative without a separate argument.

The original word graph has one vertex. The augmented word graph is connected even under the stronger LCS≥r−1 rule. This is therefore an obstruction to uniformly bounded recovery from an augmentation, not a counterexample to the original connectivity conjecture. It leaves nonlocal retractions, component preservation, and unrestricted path rerouting open.

Reviewed proof: `UNBOUNDED_PATH_PROJECTION.md`, SHA-256 `4a087676e6eda5680af3b19ed6d54543fa1ba277c77bdde26ad9c49d3e24f6a8`, 9,321 bytes. The proof is published byte-for-byte. The original audit report is pinned in EDITORIAL_MAP.json; the public edition has its own pin in MANIFEST.json. Input and audit integrity checks are recorded in VERIFICATION.json. The author's computational checker was only opaque-hashed by the independent auditor, not read, imported, or executed.

## Full symbolic proof audit

### 1. Original configuration and uniqueness

The vectors x₀=e₀ and xᵢ=eᵢ₋₁+eᵢ for 1≤i≤r−1 form a triangular basis of F₂ʳ. Thus their Gram matrix has rank r. Direct inner products give precisely a path on labels 0 through r−1 with one diagonal one, at label 0. Pressing its sole black endpoint removes it and toggles the next endpoint black. This repeats until the last vertex, proving both legality and uniqueness of S=(0,1,…,r−1), including termination of the full matrix.

The vector y=eᵣ₋₁ is the telescoping sum of all xᵢ. For r≥2 it is distinct from every original xᵢ and has norm one. Its sole nonzero old-coordinate inner product is with xᵣ₋₁. Thus adjoining it gives the path on 0,…,r with its two endpoints black, with unchanged rank r. This is a genuine one-vector augmentation within the represented quotient space.

### 2. Every augmented word and every fiber

At each nonterminal stage with at least three remaining vertices, the nonzero matrix is exactly the path on one interval, with two black endpoints. Only these endpoints may be pressed. Pressing one clears its row/column and shortens the interval, retaining two black endpoints. At size two the nonzero block is the rank-one all-ones matrix, so either endpoint press clears it entirely.

All legal choices therefore succeed, and there are r binary choices, hence 2ʳ successful words. Through the first r−1 removals, different endpoint choices give different full matrices: for size at least three the two endpoint update columns are different, so their rank-one outer products are different (their diagonals recover the columns over F₂). Only the final two choices yield the same transition. Consequently there are exactly 2ʳ⁻¹ full trajectories; each has exactly two words, differing only in their last label. This proves the complete fiber description rather than inferring it from selected representatives.

In particular the reverse fiber is exactly (r,r−1,…,2,1) and (r,r−1,…,2,0). Its Gram–Schmidt basis is the reversed standard basis, and its coordinate layers are ({r},{r−1},…,{2},{0,1}). The old trajectory's full augmented fiber is S together with (0,1,…,r−2,r). Both must be considered in the induced quotient, and the manuscript explicitly does so.

### 3. Word graph distance and upper-bound path

Every reverse-fiber word is strictly decreasing while S is increasing; each pair shares an old label, so LCS is exactly one. On equal-length words, r−LCS is half the insertion/deletion distance and satisfies the triangle inequality. A BFM edge has this distance at most four. Every word path from the fiber to S therefore has at least ceil((r−1)/4) edges, counting all internal-fiber moves if used.

For k=0,…,r−1, Wₖ=(0,…,k−1,r,…,k+1) is a valid endpoint-removal word. For k<ℓ its shared prefix and reverse suffix with Wℓ have total length r−(ℓ−k). Taking increments up to four therefore gives BFM edges. The final transition to S has LCS at least k+1 and deficit at most r−k−1; choosing the last k within four of r−1 completes a path with exactly ceil((r−1)/4) edges. The small ranks r≤5 give a single direct edge, agreeing with the same formula.

Thus the minimum distance from the two-word reverse fiber to S is exactly as claimed. The construction uses one of the reverse representatives; the minimum statement is the supported exact assertion.

### 4. Quotient lower bound accounts for free fiber changes

For a trajectory F let p(F) be the number of left removals among its first r−1 presses. Those letters are fixed throughout its fiber, so p is well-defined even when representative changes are free. The final residual pair is {p,p+1}.

Let p(F)=a<b=p(G) and δ=b−a. Consider the labels I={a,…,b+1}. Every representative of F contains δ+1 labels from I in strictly decreasing relative order: a+2,…,b+1 in descending order, followed eventually by its last letter a or a+1. Every representative of G contains δ+1 labels from I in strictly increasing relative order: a,…,b−1 in ascending order, followed eventually by its last letter b or b+1. A common subsequence can retain at most one I-label. At least δ labels of any F representative must therefore be omitted, giving maximum fiber-to-fiber LCS at most r−δ.

This is a bound over every pair of representatives, so no free substitution invalidates it. Every quotient BFM edge changes p by at most four. The reverse and old trajectories have p=0 and p=r−1, respectively. Their quotient distance is at least ceil((r−1)/4).

The canonical trajectories of Wₖ have p=k. The explicit subsequences above attain the upper bound r−|k−ℓ| for their full fibers. The canonical sweep therefore realizes the same lower bound in the quotient. The exact quotient distance follows independently of the word-metric triangle inequality.

### 5. Connectivity is compatible with this obstruction

Within the first r−1 endpoint removals, swapping adjacent opposite-end choices begins at an interval of at least four vertices. Both orders are legal and have identical states after the pair. Their words differ by a swap and have LCS at least r−1. These swaps collect all left removals before the right removals. Changing the final fiber representative then gives Wₚ. Consecutive canonical Wₚ words and the final transition to S each preserve at least r−1 letters. Thus the entire augmented word graph is connected at one-deletion/one-insertion adjacency. The proof does not confuse increasing distance with disconnectedness.

## Independent computational cross-check

The symbolic proof above is complete without computation. Separately, a fresh verifier builds each Gram matrix directly from the coordinate bit-vectors, enumerates the entire literal pressing tree, retains every intermediate full matrix, groups exact trajectories, computes LCS independently as longest increasing subsequences of matched positions, and constructs both full word graphs and full fiber quotients.

For every r from 2 through 10, it independently confirms:

- The unique original success, 2ʳ augmented words, and 2ʳ⁻¹ complete two-word fibers.
- Exact reverse and old full augmented fibers, including the new-label representative of the old trajectory.
- The p-Lipschitz LCS inequality for every unordered pair of augmented successful words.
- Exact word-fiber and trajectory distances by breadth-first search, equal to ceil((r−1)/4).
- Connectivity of all augmented words at LCS≥r−1.
- All canonical words, every pairwise canonical-fiber equality, and the displayed optimal recovery path.

The largest check includes 1,024 successful words, 512 trajectories, and all 523,776 unordered pairs. Across all ranks the verifier checks 698,026 unordered word pairs. Its explicit runtime requirements are not Python assertions and remain active under optimization. Normal, -O, and -OO runs agree. Only aggregate scopes, counts, outcome statuses, and byte/hash pins are included in this public edition; the raw computation output and executable verifier are excluded. See VERIFICATION.json for the published metadata.

## Acceptance boundary

Accepted: a self-contained infinite family with unbounded recovery distance from one-vector norm-one augmentation, with the exact formula for the stated minimum word distance and the quotient distance.

Not claimed: original-conjecture disconnection; failure of unrestricted nonlocal projection or component preservation; general lower bounds for arbitrary augmented configurations; novelty or priority; equality of the word distance for each designated representative separately. No external theorem, source text, or author implementation is necessary for the mathematical proof.

## Edition and reproduction boundary

The audit's separate earlier finite rank-ten supplement and the corresponding acceptance sentence are outside this symbolic-only appendix. That material is not a dependency of the all-rank path proof or any accepted claim here. No raw matrices, word enumeration, certificates, source copies, or code accompany this edition. The complete proof and independent reconstruction are available for mathematical inspection; the omitted checker and raw outputs mean that this is not a self-contained executable reproduction bundle.
