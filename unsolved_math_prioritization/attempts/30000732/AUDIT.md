# Complete independent audit and supporting scope records

Target: 30000732 / OWR-1536-002.

This is an AI-assisted, unrefereed partial-report edition. Acceptance records an independent internal AI audit after its two required hypothesis corrections were applied. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. Every written mathematical argument, formula and example in the authored report and audit is retained. Executable code, raw computational datasets, copied source PDFs or extracted source text, source renderings, raw search responses and private coordination material are not distributed. Historical finite checks support the written arguments and cannot be reproduced from this edition alone.

Source retrieval, source inspection and mathematical-check statements describe the original report and independent audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution.

## Historical conditional decision and present disposition

The full original audit is reproduced verbatim below. Its conditional acceptance and instructions to apply CORRECTION.patch describe the original, unpatched report. The exact patch has now been applied to the separate corrected report distributed in PROOF.md; the immutable originals remain unchanged. The audit's isolate counterexamples explain why the two added hypotheses are necessary. Every intended d-regular application has d>=1, so none of its displayed intended bounds changes.

The current acceptance is of the corrected rigorous partial report only. The full subexponential construction question is unresolved by this work. The factor-1/4 versus factor-1/2 caution concerns the inspected derivation and does not refute the source's stronger theorem. References below to checks, receipts or CORRECTION.patch are historical; only authored prose and verification metadata are distributed in these eight files. The exact patch is reproduced in ACCEPTANCE.md.

## Original independent audit, unchanged

# Independent audit of fast regular Maker constructions

Problem 30000732. Audit completed 11 October 2026.

## Decision

**Conditional acceptance as a rigorous partial report, after two required hypothesis corrections. The original research question is not solved.**

The reviewed report has SHA-256 `cc0368b966b87617fcef9f4c164e64ab61515dbf019765ba947203c098f630b5`. Its substantive positive-degree regular-graph arguments are sound. However, Proposition 2 and Lemma 6 are stated for graphs without explicitly excluding isolated vertices. Those unqualified statements are false. The exact two-line correction is supplied in `CORRECTION.patch`; the immutable input has not been edited.

This acceptance does not certify the full proofs of the cited prior upper bounds, assert novelty, or establish the present literature status of the research question.

## Required correction and counterexample

Insert the hypothesis that the graph has no isolated vertices into:

1. Proposition 2: change the opening to “If H has no isolated vertices and Maker can force H on K_L in at most t moves, ...”.
2. Lemma 6: change the opening to “If G has no isolated vertices and Maker can force G in t≥1 moves on some complete board, ...”.

Let H be the disjoint union of K_2 and 100 isolated vertices. On K_102 Maker obtains a copy of H with its first edge, so τ(H)=1. Proposition 2, as originally worded, takes L=102, t=1 and k=2 and asserts that K_110 suffices. But 2H has 204 vertices, so K_110 cannot contain it. Lemma 6, as originally worded, asserts that K_4 suffices for H, although H has 102 vertices.

The failure is precise: untouched vertices can belong to the isolated part of a retained copy, and a simulated copy can include isolated vertices outside the touched-vertex map. The added hypotheses repair exactly these issues. Every d-regular graph used in the report has d≥1, hence has no isolated vertices. Disjoint unions of these graphs have the same property. No displayed bound for the intended problem changes.

There is no additional isolate-related defect in Lemma 1 or the definition of τ. Lemma 1 simulates play on the same fixed vertex-labelled board; its actual and virtual Maker edge sets coincide. Any virtual isolated vertices are also present on the actual board, without requiring them to be touched. Therefore enlarging a complete host still preserves a time bound. The least finite attainable move count is consequently the eventual minimum on all sufficiently large complete boards. For an edgeless graph that count can be zero; no later positive-degree application uses that case.

## The target and its quantifiers

The original [Oberwolfach contribution](https://ems.press/content/serial-article-files/46106), PDF page 9, printed page 1081, has an exponent d in its small-o expression. Visual inspection confirms that it asks for subexponential dependence on d. The game uses prescribed isomorphism types and ordinary, potentially noninduced copies. Neither the inspected problem statement nor the surrounding game definition imposes connectedness. The report correctly keeps the sufficiently large host threshold dependent on the target graph.

The intended outcome is a function f with log f(d)/d tending to zero, together with infinitely many pairwise nonisomorphic d-regular targets for every fixed positive d. Forcing an unspecified member of a family does not satisfy that requirement. The report does not make that substitution.

## Pass simulation and fresh seeds

For Lemma 1, let M be both the actual and virtual Maker set. Maintain B_actual inside the chosen board as a subset of B_virtual, with M disjoint from B_virtual. When an actual Breaker move is virtually free, copy it. Otherwise spend the virtual Breaker move on a virtually free element. Such fictitious ownership can only restrict Maker. The virtual strategy therefore always requests an actually available edge. If no virtual free element remains before the objective has been met, the alleged virtual winning strategy would fail against that legal virtual play, a contradiction. Thus the pass simulation is valid, including when Breaker later claims an edge already declared fictitiously owned.

For the corrected Proposition 2, before stage j there have been at most (j−1)t moves of each player. At most 4(j−1)t vertices are touched. The stated N≥L+4kt leaves an untouched L-set. The preceding stage's final Breaker reply is included in this budget. Run the seed strategy on that fresh set and use Lemma 1 for outside replies. Since H has no isolated vertices, every vertex of every previously retained copy is touched, so the new copy is disjoint from them. Later cross-edges cannot destroy an ordinary subgraph copy. There are at most kt Maker moves.

The report is right not to reserve a fixed partition of boards in advance: Breaker could contaminate such future boards. Choosing a fresh set at each stage avoids that difficulty. For nonempty H, the different orders k|V(H)| ensure pairwise nonisomorphic disjoint unions.

For Corollary 3, an affirmative original answer bounds α_d from above by f(d). In the other direction, finiteness of α_d permits a seed with normalized time below α_d+1 even when the infimum is unattained. The corrected amplification lemma applies because d≥1. Also α_d≥d/2 by edge counting. Thus replacing α_d by α_d+1 does not change whether its logarithm is o(d), and the two formulations are equivalent. No attainment assumption or connectedness assumption has slipped into this equivalence.

## The degree and final edge arguments

An n-vertex d-regular graph needs dn/2 distinct Maker edges. For d≥2, suppose victory were possible on the mth move, where m=dn/2. Every earlier Maker edge would have to lie in the final copy because its edge count equals the total number of Maker edges. Every vertex of the final copy must already be incident to an earlier Maker edge: a newly introduced endpoint would have final degree one. The current graph would therefore be the target with one edge removed, on the complete final active vertex set. Exactly two vertices have degree d−1; all others have degree d. There is only one edge that can restore those degrees, and Breaker can take it after move m−1. If that edge is not free, or the required degree pattern fails, immediate completion is already impossible.

This proves Proposition 4, including its timing. It does not produce a uniform additive improvement in α_d because target orders are unrestricted. Degree one is genuinely different: sufficiently many fresh vertices permit a matching in one Maker move per edge, giving α_1=1/2.

## Potential and complete board compression

For Lemma 5, every currently unblocked winning set A has weight 2 to the power minus its unclaimed-by-Maker size. A Maker move at x doubles exactly the weights of unblocked sets containing x, so the increase equals p(x). A Breaker move at x kills exactly those terms, causing a decrease p(x). After the first Maker move the potential is strictly below one under the initial threshold in the report. At every later Breaker turn choose a free element of maximum p. Removing its terms cannot increase the p-values of any remaining free element. The next Maker increase is therefore no larger than that Breaker decrease. Potential below one after every Maker turn excludes a completed winning set, which would itself contribute one. Strict inequality is necessary for this stated criterion: a single singleton winning set has initial potential 1/2 and Maker wins immediately.

For the corrected Lemma 6, map all touched vertices injectively between the virtual complete board and K_(4t). Before Maker's jth turn, at most 4(j−1) vertices are touched, so at least four small-board vertices remain when j≤t. A Maker edge introduces at most two new endpoints. A Breaker reply then introduces at most two more. Extend the map in the appropriate direction; the large board has more than 4t vertices whenever the small-to-large case is needed. Complete boards ensure every requested edge exists, and the ownership-preserving map ensures that it is unclaimed. The target has no isolated vertices, so its entire vertex set is inside the touched map when the virtual strategy wins. This last sentence is exactly the point repaired by the additional hypothesis.

For Corollary 7, a graph with no isolated vertices has exactly (Q)_n/|Aut(G)| distinct winning edge sets on K_Q when Q≥n. The no-isolates condition makes the support of an edge set determine the copied vertex set. Bounding this count by Q^n/|Aut(G)| and applying the potential threshold on Q=4t excludes every integer t below (2^(m−1)|Aut(G)|)^(1/n)/4. Taking the ceiling gives the report's bound; no endpoint equality is lost. The already explicit no-isolates assumption in Corollary 7 needs no change.

## What the automorphism estimate can prove

For K_(d+1), substituting |Aut|=(d+1)! and integrating log x gives the asserted exponential normalized lower bound with denominator 4e. This excludes that single-clique choice of seed from a subexponential construction.

For k copies of a connected h-vertex graph H, each automorphism permutes the components and then independently chooses an internal automorphism, giving |Aut(H)|^k k!. After dividing the counting bound by kh, using k!≤k^k leaves a constant depending on H and d times k^(1/h−1). Since h≥2, this tends to zero; the ceiling adds at most 1/(kh). Thus the counting bound becomes weaker than edge counting for large k. It is not legitimate to multiply the single-clique lower bound by k. The inequality τ(kH)≤kτ(H) also supplies no reverse inequality. The report's explicit warning preserves possible faster batching strategies.

## Fixed pools and activation

There are at most ∏c_i role-respecting copies when the role pools are fixed and disjoint. Even if some assignments have the same edge set, this remains an upper bound, so the pool proposition does not need a no-isolates assumption. The winning sets all have m edges. The potential criterion therefore prevents success whenever ∏c_i<2^(m−1), regardless of unused edges elsewhere on the board.

For d-regular targets, m=dn/2. Success consequently requires geometric mean pool size at least 2^(d/2−1/n). Under the additional condition that every pool vertex must have a Maker-incident edge by completion, t moves activate at most 2t vertices. Arithmetic–geometric mean then yields the displayed lower bound n·2^(d/2−1/n)/2.

Both restrictions are essential to the conclusion as used here: pools must be predetermined, and all their vertices must be activated. Counting a huge unused pool is not a time lower bound. Adaptive role assignment or adaptively chosen pools can escape these hypotheses. The report correctly declines to treat this as a lower bound on α_d or as a refutation of the earlier adaptive candidate method.

## Pairing and target selection

For fixed x,y and a fresh eligible set U, the edge pairs {xu,yu} are disjoint. Breaker's reply to the first Maker-owned element of an untouched pair claims its mate. A pair already containing a Breaker edge can never become a Maker pair. Arbitrary legal replies to unrelated Maker moves preserve this invariant. The initial absence of Maker spokes is therefore sufficient for the pairing obstruction, while pre-existing spokes can invalidate it. This does not stop an adaptive strategy from preparing a reservoir and choosing x,y later.

On the three-element board in the report, taking the common element first forces one of the two two-element objectives. Each single objective can be blocked immediately after Maker's first move. Hence the quantifier counterexample is correct. It is a logical illustration, not a regular-graph counterexample.

## Literature statements and inspection limits

The [2008 manuscript](https://www.math.tau.ac.il/~krivelev/fastwin.pdf) has an N/4 conversion in Lemma 3.1 on page 9, but its Theorem 2 derivation on page 10 invokes a factor 1/2. These displayed arguments alone do not justify the stronger factor. This audit accepts only the report's independently proved conservative constant; it does not refute the stronger theorem. Page 11 also assigns degree d to order-d cliques, whose degree is d−1. The report correctly uses K_(d+1). The cited general upper bound has exponential dependence on d; its complete construction proof and discrepancy-theorem dependency are not certified here.

The [Gebauer clique preprint](https://arxiv.org/pdf/0909.4362), Corollary 1.8 on PDF page 3, displays 2q^7·2^(2q/3). We verified the displayed statement and its sufficiently-large parameter context, not the entire proof. Conditional on that cited prior theorem, taking q=d+1 and applying corrected amplification yields the stated exponential benchmark. Dividing its logarithm by d gives (2/3)log 2, not zero. The benchmark therefore does not answer the problem.

The [Gebauer size-Ramsey article](https://www.research-collection.ethz.ch/server/api/core/bitstreams/56e3f017-575f-4856-a832-2ffbf307c16b/content), Theorem 1.1 on PDF page 4, printed page 501, asserts a linear number of board edges for each fixed maximum degree. The next page describes the resulting time constants as weaker than the earlier ones. The prescribed blow-up roles and page-9 constants are consistent with the report's discussion. No subexponential conclusion or full proof certification follows from this inspection.

A fixed winning board with M edges permits at most ceil(M/2) simulated Maker moves, even when actual Breaker moves leave that board. This supplies one sufficient method for a time bound. It does not make a lower bound on fixed-board size into a lower bound on adaptive complete-board play.

## Independent verification and reproducibility

The candidate's 32-file closed set, totaling 3,167,515 bytes, was independently enumerated and hashed against the separately supplied seal. No candidate executable was run. Three fresh public PDF downloads matched the candidate snapshots exactly: OWR, the 2008 manuscript, and the clique preprint. Fresh ETH retrieval returned HTTP 429; that article was inspected from the supplied hash-pinned snapshot, without claiming a fresh match. The DOI web resolver attempts were unavailable through the web tool. Exact retrieval and inspection metadata are recorded in `SOURCES.json`.

The independently written finite checks passed under ordinary Python, `-O`, and `-OO`, with explicit exceptions rather than removable assertions. They cover:

- All 32,906 families of nonempty subsets on boards of one through four elements, including Breaker-pass equivalence. The 101 families strictly below the potential threshold all give Breaker wins.
- Pairing games with one through six pairs, and both single objectives and their union in the quantifier example.
- All 174 labelled regular graphs of degree at least two on three through six vertices, with 1,336 edge-deletion restoration checks.
- Four small disjoint-clique automorphism counts by direct permutation enumeration.

The isolate counterexample is elementary vertex counting and is also recorded in the receipts. These computations are illustrations and consistency checks, not substitutes for the proofs or a search for the requested graph family.

## Final disposition

Apply the two explicit hypothesis insertions in any corrected edition before acceptance or publication of the mathematics. Preserve the original sealed input for provenance. After that patch, the report is accepted as a careful partial reduction and restricted-method audit. It proves neither a subexponential construction nor a general obstruction to one. Further work must produce a prescribed positive-degree regular seed sequence with normalized time exp(o(d)), or an argument excluding all such sequences.

## Original report source audit, unchanged

# Source audit and inspection limits

Problem 30000732, checked 11 October 2026. The precise whole-file byte counts and SHA-256 values are in SOURCES.json. Retrieved source bytes and page images are research inputs, not publication deliverables.

## Original target

The 2007 Oberwolfach contribution is on PDF pages 7–9, printed pages 1079–1081. Text from those pages was read; PDF page 9 was rendered and inspected. The superscript in Problem 3.1 is visibly an exponent. The corrected dependence is subexponential in d, with infinitely many d-regular graphs for each fixed d and sufficiently large host size depending on the chosen graph. The author-hosted manuscript dated 6 July 2008, page 10, independently supports that reading. Neither inspected formulation demands connectedness.

## 2008 sparse-graph paper

The complete 12-page extracted text was read, recovering the initially truncated middle proof pages through a targeted read of pages 7–8. Pages 9 and 10 were visually inspected. Its upper construction uses multiple candidates for each target vertex and a discrepancy-game theorem; the latter was not independently re-proved. This packet is not a full independent certification of that upper proof.

Two local cautions were verified:

- Page 9, Lemma 3.1, gives an N/4 delay conversion. Page 10 uses a factor 1/2 when invoking that lemma in Theorem 2. The inspected argument does not establish this stronger factor. The report supplies a complete conservative factor-1/4 proof and does not declare the stronger theorem false.
- The page-11 disjoint-clique remark has a degree-index slip: a clique of order d has degree d−1. The d-regular test family uses cliques of order d+1.

The complete-bipartite lower-bound example concerns degeneracy d. When its order grows with fixed d, its maximum degree grows as well, so that example is not an asymptotic family of d-regular graphs. This is another reason it does not settle the present question.

## Later primary-source checks

The entire PDF of arXiv:0909.4362v2 was retrieved, but only selected sections were inspected. In particular, page 3 and its Corollary 1.8 were read and rendered. The whole-file PDF has 13 pages, although the abstract's comments field says 12. The report uses the polynomial factor in the displayed corollary rather than the shorter abstract's simplified description. The journal article's publication metadata and title were checked through its DOI page. The entire proof was not independently certified.

The entire institutional PDF of Gebauer's 2013 size-Ramsey-for-games article was also retrieved. It has 19 PDF pages including an institutional cover. Selected introductory/theorem sections, the explicit pool constants, and the final discussion were inspected. The article itself says its resulting time constants are weaker than the older sparse-graph constants. No subexponential-in-d conclusion is inferred from its O_d(n) statement. Its full proof was not audited.

## Search boundary

The bounded search considered the original title and variants of “Maker regular graphs subexponential,” the authors' names with the regular-graph question, fixed-graph versus minimum-degree games, fast clique construction, clique factors, and size-Ramsey constructions. The useful later primary sources listed above were inspected; several other hits concerned different games or a different objective. No exact later settlement was located in this bounded search. That negative search result is not a claim of continuing openness or a novelty guarantee.

The report's potential argument, board compression, seed amplification, final-edge argument, fixed-pool count, and pairing response are re-proved there. Existing literature results are labelled separately. The source audit does not promote the full research target to solved status.

## Original report computation-scope narrative, unchanged

The checker and detailed receipts named in this historical narrative are not included in this edition. VERIFICATION.json gives receipt identities and bounded aggregate coverage only. The written examples below remain part of the authored account.

# Computation scope

The mathematical results in REPORT.md are proved symbolically. The accompanying authored checks are finite sanity checks only.

`checks.py` uses a standard-library minimax recursion with no heuristic pruning beyond memoization and short-circuit minimax evaluation. It enumerates the legal choices needed to determine each listed finite game. “states_evaluated” is the number of cached states actually visited, not the number of all possible positions.

The checks cover:

1. Disjoint-pair Maker–Breaker games with 1 through 5 pairs. Breaker wins every tested case, consistent with Proposition 10's general pairing proof.
2. The three-element quantifier counterexample. Breaker wins each of the two single prescribed objectives; Maker wins their union.
3. Three small fixed-pool clique games strictly below the Erdős–Selfridge threshold: K_3 with pools (1,1,1) and (1,1,3), and K_4 with pools (1,1,1,2). Breaker wins all three.
4. All labelled simple regular graphs of degree at least two on 3 through 6 vertices. There are 174 such graphs in the enumeration. Deleting each edge produced 1,336 checks; in each case the deleted edge was the unique simple edge restoring regularity. These checks concern the finite degree claim behind Proposition 4, not a minimax search for full graph-construction games.

Normal, `-O`, and `-OO` Python runs all passed. Validation uses explicit exceptions rather than assertions, so optimized execution does not remove checks. The three JSON receipts record the cases, outcomes and visited-state counts. They differ only in the optimization indicator.

No random trials, asymptotic extrapolation, search over large regular graphs, proof assistant, or complete strategy enumeration for the original problem was used. No third-party source code was executed. PDF text extraction and page rendering were ordinary read-only document-processing operations.

The packet verifier is a separate read-only integrity check. It tests exact closed-set membership, sizes and hashes against an outside seal; it does not certify any mathematical statement.
