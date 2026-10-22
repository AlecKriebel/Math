# Independent audit: doubling wrapper and small-family reductions

Date: 12 October 2026 UTC. Problem 3100047 / row 1747.

## Disposition

**ACCEPT the separately frozen corrected edition as bounded mathematical results.** Its report is 14,346 bytes with SHA-256 `5a98ac43517ae96fb86064c0b37bbaa3c73195f656b152f8a64cd48200ee202a`. The four-vertex wrapper theorem, exact uniform marginals, unbounded balanced four-/six-word examples, and the stated necessary conditions for a hypothetical unbalanced four-to-six-word family are correct. No further mathematical correction is required.

The original report, 14,229 bytes with SHA-256 `6d743cde81038273a0c6b7f9501376a5b1d75633cc99a255798cc7b91a535e81`, has the same valid algebra and proofs, but its opening dimension-reduction claim needs the scope correction already made in the accepted edition. The original report and original `FREEZE.json` were preserved. Acceptance attaches to the exact corrected bytes, not to possible later edits.

**No general pressing-balance theorem is accepted or claimed.** In particular, this audit does not settle balance for every four-, five-, or six-word pressing matrix, bound counterexample-specific dimension, classify all instructional mixtures, or certify a new literature result. There were no repository, queue, commit, push, or publication actions during this independent audit.

## 1. Frozen inputs and the required correction

Both complete supplied manifests were verified, including every listed byte count and SHA-256. The original audit input inventory independently pins both manifests and all their entries; ORIGINAL_INPUT_PINS.json identifies the accepted proof, audit and evidence inventories for this public edition. Supporting verifier, diagnostic, and output bytes agree across the original and corrected edition; only the report and edition manifest differ. Copies of both report/manifest pairs were retained with the original audit evidence; the complete corrected report and this complete substantive audit are distributed here.

The exact substantive correction is the replacement of the opening sentence:

> A possible finite reduction must permit a stronger operation than deleting fixed-order components or padding.

by the narrower conclusion:

> Thus a reduction based only on word count and variable-component size cannot apply to all matrices. A dimension bound restricted to hypothetical unbalanced families remains possible; these balanced examples do not obstruct it.

This distinction matters. Every wrapper produced here already has many probability-1/2 pairs. Thus it refutes a finite bound on variable-component size that is required to hold for **all** matrices with four or six words. It does not refute such a bound after restricting to hypothetical unbalanced matrices, since that restriction excludes every displayed wrapper. The corrected edition states this explicitly. No change to the construction, proof, enumeration, or small-count restrictions was needed.

## 2. Elementary diagonal identity and forced-prefix padding

All algebra is over F_2. Let c be the diagonal column of a nonsingular symmetric matrix M of order r, and let B=M^{-1}, which is also symmetric. Cancellation of off-diagonal terms gives

    c^T B c = sum_i c_i B_ii.

In the trace expansion of MB, the terms M_ij B_ji and M_ji B_ij cancel for i != j. Its remaining terms are exactly sum_i c_i B_ii. Therefore

    c^T M^{-1} c = trace(MM^{-1}) = r mod 2.

The matrix H=M+cc^T has zero diagonal. The rank-one determinant identity gives det(H)=det(M)(1+r mod 2). Consequently H is nonsingular when r is even. For odd r it is singular; since a rank-one update can reduce rank by at most one, its rank is then exactly r−1. The argument does not require pressability, and the report correctly does not deduce pressability from nonsingularity or from a nonzero diagonal.

For the padding matrix

    P(M) = [[1,c^T],[c,M+cc^T]],

every old diagonal vanishes and the new diagonal is one. The first letter is forced. Its outer-product update leaves exactly M on the old labels and clears the new label. This proves the exact prefix-language identity in both directions, preservation of the number of complete words, and nonsingularity by a unit-pivot Schur complement. Repeating this operation twice preserves parity; a single repetition changes it.

## 3. Exhaustive branch proof of the wrapper theorem

Write the outside labels as a,a',b,b'. The central block H is alternating, the only initial loops are a and b, and their first-letter branches are exchanged by swapping the two side pairs. It is enough to examine the a branch, but the independent implementation tests both.

### 3.1 Initial presses

After a is pressed, a' is black, b is white, and a'b is an edge. No central diagonal changes because a has no central neighbors. All other unpressed diagonals vanish. Hence a' is the unique legal second letter. Pressing a' restores M on the central set. The two unpressed outside-to-central columns both equal c, and their block, in order b,b', is

    K_0 = [[1,1],[1,0]].

In particular, it would be incorrect to infer that all subsequent presses are central just because the intended words have that form. The early-outside branches require explicit exclusion.

### 3.2 Invariant for every legal central prefix

After k central presses, including prefixes that will never complete, let D denote the surviving central block and d its common cross-column to b and b'. Then

    diag(D)=d,
    K_q=[[1+q,1+q],[1+q,q]],  q=k mod 2.

For a legal central press v, d_v=D_vv=1. If z is its central column, the central update is D+zz^T; its diagonal changes from d to d+z. Both cross-columns also change from d to d+z because each outside incidence at v is one. The outside 2-by-2 block toggles in all four positions, giving the next parity block. Removing the cleared coordinate proves the invariant on the remaining labels.

The central principal updates are precisely those obtained by pressing M in the same central order. Unpressed outside coordinates do not change this fact. A legal but noncompletable central prefix is still covered by the invariant and by the next argument.

### 3.3 Even-prefix early-outside branch

Assume the central set is nonempty and q=0. The only legal outside choice is b. Its press turns D into D+dd^T, which is alternating. It also turns b' black, but its surviving cross-column is d+d=0. Thus b' is an isolated black vertex and every central vertex is white.

The sole next legal press is b'. That press cannot affect any central coordinate because its cross-column vanishes. Afterward the nonempty central residual is entirely white and there is no legal move. Full completion is impossible. The alternating block is not prematurely treated as a terminal obstruction: the one legal remaining outside press is explicitly taken and proved incapable of revival.

### 3.4 Odd-prefix early-outside branch

Assume the central set is nonempty and q=1. Here K_1 has b white, b' black, and edge bb' absent. The only legal outside choice is b'. Its press turns the central block into D+dd^T, with zero diagonal. Since its incidence to b is zero, b remains white. Every remaining diagonal, central and outside, is zero. There is no legal next press at all, regardless of the surviving off-diagonal incidences from b to the central set.

This also rules out revival. Off-diagonal edges alone cannot start a press when the entire remaining matrix is white.

### 3.5 Completion and parity

Every successful word starting with a must therefore have prefix aa', then press all central labels without touching the other side pair. Its central order must be a successful full word of M. Conversely, any such central word is legal inside the wrapper.

When the central order has even length r, the terminal outside block is K_0, whose unique complete order is bb'. The symmetric branch gives bb' followed by a central word and then aa'. Thus the complete successful language is exactly

    {aa' σ bb' : σ in Sigma(M)} union {bb' σ aa' : σ in Sigma(M)}.

The two halves are disjoint because their first letters differ. Each has exactly |Sigma(M)| words. A complete successful order supplies unit pivots throughout and proves full rank.

The parity boundary is genuine: after an odd number of central presses the remaining block is K_1. Pressing its single black vertex leaves the other outside vertex white, so full completion fails. The same branch argument shows that the wrapper as defined has no full successful word for any odd-order central matrix, a stronger boundary control than the odd-identity samples in the author's verifier. This audit uses that fact only as a control, not as an extension of the stated even-order theorem.

## 4. Exact uniform probabilities and arbitrarily large examples

Let Z=|Sigma(M)|>0. Each central word appears once in each half, so the total is 2Z and every central-central precedence count doubles. Central-central probabilities are unchanged.

For any central x and any outside y, exactly one of the two halves puts x before y. The count is Z, giving probability 1/2. The same is true for any pair with one vertex in {a,a'} and the other in {b,b'}. The internal side comparisons a<a' and b<b' are fixed. These conclusions use uniform counting of the entire successful language, not arbitrary class weights or conditioning on one half.

The variable-order graph therefore contains every central-to-outside edge and every edge between the two side pairs. It is connected, including all central letters introduced by forced-prefix padding.

For the four-word family, I_2 has two words. Its 2k-fold forced-prefix extension has even order 2+2k and still exactly two words. Wrapping it gives order 6+2k, four words, connected variable-order graph, and exact 2-versus-2 side comparisons.

For the six-word family, the stated 3-by-3 seed is the disjoint union of the forced order 01 and an isolated black vertex 2. Its words are exactly 012, 021, 201. Applying 2k+1 forced-prefix extensions gives even order 4+2k without changing those three choices. Wrapping gives order 8+2k, six words, connected variable-order graph, and exact 3-versus-3 side comparisons.

These are arbitrary-order proofs. Finite checks supplement them but do not substitute for the induction. They disprove universal finite bounds f(4) and f(6) for variable-component size. They do not settle the five-word case, refute counterexample-specific bounds, or address a quotient that is allowed to contract common consecutive ordered subwords.

## 5. Four-to-six-word necessary conditions

### 5.1 Majority order and disjoint inversions

For T in {4,5,6}, a pair is balanced exactly when its two integer orientation counts are both at least two. If no pair is balanced, each pair's minority occurs in at most one word, and every majority is strict.

If the majority tournament contained a directed triangle, every total-order word would violate at least one of its three edges. There would be at least T violations counted with multiplicity. Each triangle edge has at most one violation, so there would be at most three. Since T>=4 this is impossible. A finite tournament without a directed triangle is transitive: any shortest directed cycle of length at least four has a chord creating a shorter directed cycle. The majority order is therefore a total order.

Relative to that total order, no inversion can occur in two successful words. This proves pairwise disjointness of inversion sets. It does not require the majority permutation itself to belong to the language.

### 5.2 Adjacent-swap star and instructional classes

Two permutations differing by one adjacent swap have identical orientations on every other pair. If both are successful, every other inversion would be shared and hence forbidden. One endpoint has no inversions and is the majority permutation; the other has precisely that one inversion. Thus every adjacent edge belongs to a star centered at the majority permutation, if it is present.

Two available swaps on disjoint adjacent-position pairs cannot coexist. Perform one swap, then the other. The first alters only the single intermediate prefix set inside its two-position block; after that block the eliminated set and full residual state agree with the unswapped word. The second block therefore remains legal, including its suffix. The resulting successful word has both inversions and repeats the minority inversion of each one-swap word. This contradicts disjointness. At most two distinct adjacent-position pairs can pairwise overlap, and if two occur their positions are consecutive. The star has at most two leaves; every other adjacent component is a singleton.

For completeness, the instructional-class identity used here can be justified without importing a classification theorem. Recording current press columns as label-indexed rows gives A=U^T U and a unit-upper-triangular U in the successful order. Such a triangular root is unique in a fixed order: the first row is forced by the first row of A, and its removal reduces to the smaller Gram factorization. The words producing a fixed U are exactly the topological orders of its strict nonzero-entry relation. Those orders are the linear extensions of one finite poset and are connected by adjacent swaps of incomparable labels, by moving the target first letter left and proceeding inductively.

Conversely, two adjacent successful presses can swap only when their current mutual edge is zero and both current diagonals are one. The two press columns are then unchanged by swapping and their rank-one updates commute, so the label-indexed root is preserved. Consequently instructional classes equal adjacent-swap components. There is at most one nonsingleton class, with size two or three. No autonomy or V-poset theorem is needed for this conclusion.

### 5.3 Prefix/suffix multiplicity

For a reachable prefix set S, legal elimination makes A[S] invertible and leaves the Schur-complement residual, which depends only on S. Thus every legal prefix order reaching S can concatenate with every successful suffix from that residual.

If F(S)>=2, two prefix permutations differ on some pair inside S. If also G(S)>=2, each of those opposite pair orientations occurs in at least G(S) complete words. Both full-language counts are therefore between 2 and T−2, which is inside the balance interval for T=4,5,6. Contradiction.

Hence min(F(S),G(S))=1 at every reachable and completable state. A reunion of two different prefix paths cannot have two successful continuations. Dead-end legal continuations do not contradict this statement and are not silently counted as successful suffixes.

### 5.4 First and last letters

Every word starting with x other than the majority minimum inverts the minimum-x pair. Such a branch has at most one complete word. Likewise every word ending with a label other than the majority maximum has at most one complete word. These are counts of successful branches; they do not assert that every legal first pivot completes.

All four reductions are necessary conditions only. They neither construct an unbalanced pressing matrix nor prove that no matrix can satisfy the restrictions.

## 6. Independent finite verification

The independent verifier retained with the original audit evidence, and not distributed in this prose-only edition, imports none of the author's modules. It uses an incremental GF_2 row-basis determinant calculation to enumerate all full paths through invertible principal subsets. Those languages are cross-checked against a separately implemented dense rank-one pressing recursion. Failures raise explicit exceptions; no correctness test relies on Python assert statements.

The following bounded checks passed:

- All 14,369 nonsingular symmetric matrices among the 33,866 symmetric matrices of orders 1 through 5 satisfy the diagonal/inverse identity and the exact rank parity of M+cc^T.
- All 1,098 symmetric matrices of orders 1 through 4 were used as central matrices, including singular and nonpressable cases. Central and wrapper languages agree between determinant-path and direct-press enumeration. For even orders 2 and 4 there are respectively 3 and 402 pressable central matrices, and their wrappers have exactly the two stated language halves. Every odd-order wrapper in this exhaustive range has empty complete language.
- For both initial side choices, every legal central prefix of these matrices was checked for the cross-column/diagonal invariant, K parity, and every early-outside branch. This includes noncompletable prefixes. Across orders 1–4, 22,158 such central-prefix occurrences were visited; 8,532 even-prefix and 10,448 odd-prefix fatal branches were checked.
- Ninety-six additional deterministic, distinct order-six unit-upper roots, sampled differently from the author's 32 cases, passed full determinant/direct language comparisons, marginal and connectivity checks, and both fatal-branch tests.
- Both fixed-cardinality families were checked for k=0,...,20: 42 cases, through wrapper orders 46 and 48. Direct enumeration examines every legal branch. Cases with central order at most 12 also receive the independent principal-minor language cross-check.
- All pair-count identities, both fixed side orders, wrapper nonsingularity for every nonempty language, and whole variable-graph connectivity were verified in every applicable wrapper case.

The complete independent output was retained under normal Python, -O, and -OO in the original audit evidence, whose identities are recorded in ORIGINAL_INPUT_PINS.json; raw outputs are not distributed here. Their byte hashes agree. These checks are bounded validation of the proof and implementation, not an exhaustive general pressing-balance census.

## 7. Abstract diagnostic: reproduced counts and limits

The independent diagnostic enumerates permutations using explicit inversion sets and compatibility sets, then counts complete paths in the union of their prefix sets. It reproduces every supplied count:

- n=2,3: no inversion-disjoint cliques of sizes four through six.
- n=4: 16 four-cliques; none is prefix-path closed.
- n=5: 856 four-cliques and 124 five-cliques. Exactly nine four-cliques are prefix-path closed, all containing the majority permutation.
- n=6: 40,711 four-cliques, 13,412 five-cliques, and 1,261 six-cliques. Exactly 225 four-cliques are prefix-path closed: 211 contain the majority permutation and 14 do not. No five- or six-clique is closed in this range.

All 234 closed families across n=5,6 were also checked for the adjacent-star, F/G, and first-/last-branch restrictions, covering 3,338 realized prefix states. This is an abstract consistency check, not a matrix-realizability certificate. A prefix-path-closed inversion-disjoint permutation family need not be the complete pressing language of any symmetric matrix. The diagnostic supplies neither matrix compatibility nor an ambient pressing census, and no theorem above depends on its finite counts.

The original author's wrapper verifier was replayed from a separate copy under normal Python, -O, and -OO. All three outputs exactly reproduce the frozen 100,187-byte SHA-256 `783681b939bb2259f11fe34b4b16fd29548b35c2e7c721d5336df2ad64fbfb49`. The abstract diagnostic was replayed inside a separate working directory, so its hard-coded relative output path could not modify the original freeze. Its 1,821-byte output exactly reproduces SHA-256 `e263a9d61dab2ae195cf3da51880b37f954004fa8e861b502c56b4d1c7f63b4f`.

## 8. Final boundary

The corrected edition gives a valid cardinality-doubling construction, actual balanced unbounded four-/six-word families, and valid necessary restrictions on an unbalanced family of size four through six. The dangerous alternating-residual shortcut is avoided: both possible outside revivals are fully resolved by the parity proof. The original overbroad reduction sentence is corrected in a separate edition rather than silently edited under its old freeze.

The unrestricted conjecture and the entire general four-/five-/six-word cases remain unresolved here. The audit's acceptance must not be represented as either a counterexample to balance or a counterexample-specific dimension obstruction.
