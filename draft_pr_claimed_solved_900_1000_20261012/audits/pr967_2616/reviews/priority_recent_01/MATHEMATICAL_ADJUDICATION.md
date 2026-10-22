# Mathematical priority adjudication

## Exact claim and success criterion

A qualifying earlier result must supply, in ZFC for the submitted scope, an infinite countable Hausdorff topological group G admitting a partition into countably infinitely many dense sets and satisfying

\[
\forall (F_n)\ [F_n\subseteq G\text{ finite and pairwise disjoint}]
\quad\exists U\ne\varnothing\text{ open}\quad
\forall N\ \exists n\ge N:\ F_n\cap U=\varnothing.
\]

The open set may depend on the entire block sequence. The threshold in the opposite assertion may depend on U. The empty open set is excluded. Blocks need not cover G or lie in prescribed partition cells. Algebraic resolvability is irrelevant.

## Complete independent reconstruction of the serious exact lead

The lead is Section 3.44, p.60, of the official September mathematical-edition preprint. The following is my own proof verification; no conclusion depends on its label as AI-generated or unconfirmed.

Use positive integers so that the source's count `2^r-1` is literal. Let U be a maximal proper filter extending the cofinite filter. Zorn's lemma supplies one in ZFC. Maximality decides each subset and extending the cofinite filter excludes finite members. Let B be the finite subsets of N with symmetric difference, and for A in U set H_A to the finite subsets of A. These are subgroups; their finite intersections follow the filter intersections. Their cosets form a base. Sums of two H_A-cosets lie in the expected H_A-coset and inversion fixes every element; thus the group operations are continuous. A coordinate on which two supports differ can be deleted using a cofinite A, giving disjoint cosets. B is countably infinite and Hausdorff. Every A is infinite, so every basic open set is infinite.

For each k≥0 put

\[
D_k=\{s\in B:\nu_2(|s|+1)=k\}.
\]

Every nonnegative support size belongs to exactly one such class. In any x+H_A, choose

\[
r=2^k(2q+1)-1\ge |x|.
\]

Select r−|x| points of A outside x. Their support t belongs to H_A, and x△t has size r. Thus every D_k meets every basic open set, and all countably many cells are nonempty.

Now take any pairwise disjoint finite families F_n of supports. Infinitely many empty terms already fail at the open set B. Otherwise remove a finite initial segment beyond all empty terms and the possible term containing the empty support. Define

\[
S_n=\{\max s:s\in F_n\}.
\]

For any r there are only 2^r−1 nonempty supports whose maxima are at most r. Disjointness of the families therefore implies that only finitely many S_n meet {1,…,r}. Starting after any chosen index, this permits a new S_n entirely above the maximum of the last chosen one. Induction yields indices n_j increasing with

\[
\max S_{n_j}<\min S_{n_{j+1}}.
\]

Let E be the union of S_{n_j} for even j. If E belongs to U, use A=E and the odd j; otherwise use A=N\E and the even j. In either case A belongs to U and, for infinitely many j, every s in F_{n_j} has its maximum outside A. No such s is in H_A. The nonempty open subgroup H_A misses infinitely many entire blocks. This proves exactly the required negation.

All auxiliary selections above are finite or countable elementary choices in ZFC. No rapid, selective, Ramsey, P-point, or other special ultrafilter assumption enters.

## Hypothesis-by-hypothesis comparison

| Requirement | Earlier source mechanism | Gap |
|---|---|---|
| Infinite countable group | Finite supports on N, symmetric difference | None |
| Hausdorff group topology | Cofinite coordinate deletion and subgroup base | None |
| Countably infinite dense partition | The same 2-adic support-size coloring as submitted | None |
| Arbitrary finite blocks, not only a fixed partition | Start with any pairwise disjoint F_n | None |
| Eventually hits every nonempty open set fails | One H_A misses an unbounded subsequence | None |
| ZFC | Ordinary free ultrafilter from the cofinite filter | None |
| Boundary cases | Infinitely many empty terms; at most one identity term | None |

Changing N from positive integers to {0,1,…} is a relabeling. It changes a finite counting formula but not the topology or argument. The submitted proof thins point-finite maxima to disjoint maxima; the earlier proof obtains the stronger separated-maxima subsequence. Both are valid consequences of the same bounded-support finiteness. The same dense coloring and obstruction already appear in full in the earlier source; this is not merely a construction-lineage citation.

## Adversarial checks of the earlier proof

- Merely having no convergent point sequence would be insufficient; the maxima proof explicitly defeats finite families of arbitrary growing size.
- Pointwise finiteness of maxima is strong enough for thinning because every already chosen maxima set is finite. The source uses the stronger bounded-support version, making separation possible.
- Choosing the ultrafilter's side of E must be paired with the **opposite** parity of maxima. Both possible ultrafilter choices leave infinitely many original block indices, so the contradiction is to eventual hitting, not just to hitting every block.
- Deleting finite terms can be implemented by passing to a tail. Even arbitrary deletion of finitely many terms and increasing reindexing would preserve eventual hitting; there is no reordering issue.
- All H_A contain the identity, hence are nonempty. The identity's possible presence in an early block does not repair infinitely many late misses.
- The partition proof uses A\x infinite and support extension outside x, preventing cancellation under symmetric difference.
- Hausdorffness uses only a cofinite member. Non-discreteness and support extension use freeness. The parity step uses maximality. These are all supplied by an ordinary free ultrafilter.

No hidden central difficulty has been moved into an unsupported theorem. The only non-elementary existence fact is the elementary Zorn application included above.

## Why recent non-H-separability is insufficient

For a countable crowded T1 space X, mH-separability actually implies the existence of an expansive disjoint finite-block sequence. Enumerate X={x_0,x_1,…} and apply mH to the decreasing dense sets

\[
E_n=X\setminus\{x_0,\ldots,x_n\}.
\]

Finite complements are dense because no nonempty open set of a crowded T1 space is finite. Obtain finite K_n⊆E_n eventually meeting each nonempty open set. A fixed point x_i occurs only in K_n with n<i, so (K_n) is point-finite. Once finitely many K_n have been selected, only finitely many further K_n intersect their finite union. Select an increasing subsequence of pairwise disjoint K_n. Eventual hitting survives passing to any infinite subsequence. Thus this is an expansive sequence.

Dow–Pecoraro's introductory examples are mH-separable (their wH is the monotone variant); their failure of H for some varying sequence cannot serve as failure of blocks from X. This remains true without deciding whether those spaces can carry any compatible group structure. Aurichi–Maesano–Zdomskyy likewise define H with varying dense sequences; a non-H assertion needs an additional argument specializing to E_n or a constant X sequence. I did not find such an exact group obstruction in the inspected recent theorem statements. Those are rejected as standalone deductions, not declared exhaustively irrelevant papers.

An expansive sequence has groupable dense union by definition. For a countable X, any groupable dense subset can be enlarged to a groupable partition of X by adding at most one enumerated omitted point to each finite cell. Conversely a groupable partition is an expansive sequence. This explains why synonym searches matter. It does not identify the target with full H-separability.
