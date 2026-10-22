# Independent mathematical audit of KOU 21.107

Audit date: 8 October 2026 UTC.

## Verdict

The mathematical argument is correct. It establishes in ZFC a countably infinite Hausdorff nondiscrete Boolean topological group that has a partition into countably infinitely many dense subsets but has no expansive sequence of pairwise-disjoint finite subsets. This supplies a negative answer to the precise countable problem KOU-21.107 under the intended nonempty-open-set convention.

No missing hypothesis, special-ultrafilter assumption, invalid infinite selection, or change of quantifier was found. Acceptance here is an independent mathematical assessment, not a claim of external peer review, priority, or confirmation by the problem's editors.

The first reviewed REPORT.md had SHA-256 `2a09489d047601777e93e0440d51c64786c70080844774621640f96bf8f58523`. Its only identified factual correction was the predecessor's page number: Problem 15.80 is on printed/PDF page 97 of version 48, not page 98. The final report, independently reread in full, has SHA-256 `ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca` and is 9,338 bytes. It corrects the page number, accurately distinguishes page 98 in version 47, and explicitly attributes the standard topology. The mathematical proof is unchanged. All identified issues are resolved.

## Exact problem and source boundaries

The complete target paragraph was checked in version 48 of the Kourovka Notebook, dated 6 October 2026. Problem 21.107 is on printed/PDF page 193. It concerns countable topological groups, arbitrary finite disjoint blocks, and eventual intersection with each open set separately. It imposes neither metrizability nor first countability. The omission of the word nonempty is interpreted in its usual meaningful sense; the construction produces a nonempty open obstruction. The box-product example attached to predecessor 15.80, on page 97, is uncountable. Its other comment supplies a dense-partition result, not the non-expansiveness argument needed here. [Kourovka Notebook v48](https://arxiv.org/pdf/1401.0300v48)

On 8 October 2026 the official repository page had no text match for 21.107. That observation does not exclude a solution inside another document, unindexed work, or later developments. [Official repository](https://kourovkanotebookorg.wordpress.com/repository/)

## Ultrafilter existence and actual assumptions

Start with the cofinite filter on the nonnegative integers. The union of a chain of proper filters extending it is again a proper filter extending it: any finitely many members lie together in one member of the chain, and the empty set is in none. Zorn's lemma therefore gives a maximal proper extension, U.

If C is not in U, adjoining C cannot generate a proper extension. Thus some B in U has B intersect C empty, which puts the complement of C in U by upward closure. A proper filter cannot contain both C and its complement. Finally, U contains no finite set because it already contains that finite set's cofinite complement. These facts prove that U is free and decides every subset.

The construction uses freeness, finite intersections, and this complement decision only. There is no invocation of countable completeness, a pseudointersection, a selector, rapidity, the continuum hypothesis, or a Ramsey property. Fixing any free ultrafilter before seeing the block sequence suffices.

## Group and topological axioms

Let G be the finite subsets of the nonnegative integers with symmetric difference. The empty set is the identity, and each element is its own inverse. The finite power sets of the initial intervals cover G; the singleton elements show that G is infinite. Hence G is countably infinite.

For A in U, define H_A to be the finite subsets of A. It is a subgroup because symmetric difference preserves containment in A. The intersection identity H_A intersect H_B equals H_(A intersect B) supplies the required finite-intersection condition. Every group element lies in its own coset of every H_A. If two basic cosets contain x, their intersection is x plus H_(A intersect B). Thus the asserted cosets genuinely constitute a topology base.

At a pair (s,t), the product of the neighborhoods s plus H_A and t plus H_A maps under addition into (s plus t) plus H_A. This establishes joint continuity, not just separate continuity. Inversion is the identity map. No conjugation condition remains in this abelian group.

For distinct s and t, pick k in their symmetric difference. The cofinite set A obtained by removing k lies in U. Their two H_A cosets cannot meet, since meeting would put their difference in H_A, contrary to the presence of k. This proves Hausdorff separation. Every A in U is infinite, so every H_A and every basic coset is infinite. Consequently the topology is nondiscrete. Complements of cosets are unions of other cosets, so the base is also clopen.

## Dense partition

Assign a finite set s the color v_2(|s|+1), where v_2 is the exponent of 2 dividing a positive integer. Every element has exactly one color in the nonnegative integers, including the identity, which has color 0.

Fix an arbitrary color j and an arbitrary basic coset s plus H_A. The integers q = 2^j(2r+1)-1 are unbounded as r grows and all have color j when used as support sizes. Choose one with q at least |s|. The set A minus s is infinite, so it contains a finite set t of exactly q-|s| elements. This includes the permitted case t empty. Since t is disjoint from s, their symmetric difference is their union and has size q. Since t is in H_A, that union is in the prescribed coset and color class.

The choices of coset and color were arbitrary. Every color class therefore meets every nonempty basic open set, hence every nonempty open set, and is dense. This also proves each class is nonempty. The construction gives an actual partition with exactly countably infinitely many pieces, rather than merely two dense sets or a cover with overlapping pieces.

## Universal obstruction to finite blocks

Take an arbitrary infinite sequence (F_n) of pairwise-disjoint finite subsets of G. No covering hypothesis, bound on block sizes, or preliminary relation to U is imposed.

If infinitely many blocks are empty, the nonempty open set G is missed infinitely often. Otherwise, only finitely many empty blocks occur and all can be discarded by deleting a finite initial segment. The identity belongs to at most one block because of pairwise disjointness. Deleting a further finite initial segment, if needed, removes it. The remaining sequence is still infinite, and all its blocks are nonempty and consist of nonidentity elements. Finite initial deletions cannot invalidate a later proof of infinitely many missed original indices.

For each remaining n, let M_n consist of the maximum elements of the finite supports in F_n. Each M_n is finite and nonempty. Exactly 2^k nonempty finite supports have maximum k, because all such supports have the form {k} union t for t contained in {0,...,k-1}. Pairwise-disjoint blocks use each support at most once. Thus k belongs to at most 2^k of the sets M_n. This bound may depend on k; uniform boundedness is unnecessary.

At an induction step, the union E of the finitely many previously chosen maxima sets is finite. For each k in E, only finitely many block indices have k in their maxima set. The union over k in E of these finite exceptional index sets is finite. An index beyond all previously chosen indices and outside all these exceptions exists, because there remain infinitely many indices. This constructs a strictly increasing infinite subsequence with pairwise-disjoint maxima sets.

As an independent check of the thinning step, one can even arrange that every maximum in the next chosen block exceeds every maximum in earlier chosen blocks. For any finite cutoff K, the set of all nonidentity group elements supported in {0,...,K} is finite. Only finitely many disjoint blocks meet that set. Avoid them at the next step. This is ordinary recursion and does not select an ultrafilter member.

Separate the chosen subsequence into even and odd positions, and take C_0 and C_1 to be the unions of their respective maxima sets. These unions are disjoint. A proper filter cannot contain both, since their intersection is empty. Choose a side C_epsilon outside U. The ultrafilter decision property makes A, its complement, a member of U.

For every block on the chosen side and every support s in that block, the maximum of s lies outside A. Hence s is not a subset of A and cannot belong to H_A. Thus one fixed nonempty open identity neighborhood H_A misses all blocks on that side. There are infinitely many such blocks, and their strictly increasing original indices are unbounded.

This gives exactly the negation required: for every candidate disjoint finite-block sequence there exists a nonempty open set such that for every threshold some larger block misses it. It does not merely show occasional failure in finitely many blocks, choose a different neighborhood at each index, or demand one neighborhood defeat all possible sequences. A single neighborhood of the identity suffices because an expansive sequence would have to meet every nonempty open set eventually.

## Literature attribution

The topology is standard. Sipacheva's Section 8, printed/PDF page 25, identifies the filter-relative Mathias topology on finite subsets with the free Boolean linear group topology and describes the finite-subset subgroups as its identity-neighborhood base. The candidate is precisely this construction for a free ultrafilter. One should attribute the topology accordingly and reserve any independently developed claim for the proof presented here, without asserting priority. [O. V. Sipacheva, Free Boolean Topological Groups, arXiv:1612.04878v1](https://arxiv.org/pdf/1612.04878v1)

The identification can also be checked directly: for a finite s and A in U, remove the finite interval through max(s) from A, obtaining B in U. Then s plus H_B consists of finite extensions of s using only B, so the usual Mathias basic neighborhoods and these cosets refine one another. This agreement requires no selective ultrafilter. Stronger properties of other filter topologies and additional selectivity assumptions are irrelevant to the present proof.

## Verification boundary and final assessment

This audit is a direct logical review of the infinite proof, together with exact-source and attribution checks. It does not rely on finite package tests, and no such tests were duplicated. Finite examples cannot establish the free-ultrafilter existence or universal obstruction; the written ZFC argument supplies those steps.

The topology, partition, and obstruction have all been independently rederived above. The final pinned report is accepted as a valid mathematical counterexample to KOU-21.107. The citation correction and construction attribution were verified in the final report; there are no outstanding mathematical or source-scope objections. This audit contains authored mathematical analysis and public bibliographic metadata, with no reproduced source documents, dataset contents, or private material.
