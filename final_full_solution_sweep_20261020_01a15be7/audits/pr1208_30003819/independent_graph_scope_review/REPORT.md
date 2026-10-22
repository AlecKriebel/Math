# PR1208 independent graph and original-scope review

Completed mathematical family: graph reconstruction, adversarial verification, original improvement-request scope. Parent/root must read and adopt this report before any disposition. This report authorizes no publication or service mutation. Overall sweep estimate remains 79%; completion of this assigned independent review is 100% after its final seal.

**Verdict: accept the incidence-dependent theorem without mathematical correction. It gives a complete affirmative answer to the literal first request for an improvement toward Stanley's bound. It does not settle Stanley's full recurrence or the separately posed combinatorial strict-growth question. Novelty and priority are outside this review and remain for the separate family.**

Calling this a structural partial result is reasonable relative to the stronger recurrence endpoint. That label does not establish failure to answer the weaker original improvement request. Conversely, answering that first request does not answer every question grouped under the original heading.

## Immutable object and independence

The reviewed PR is [AlecKriebel/Math #1208](https://github.com/AlecKriebel/Math/pull/1208), immutable head `5b238897f7e3f1008bd44c2cc5b5a01d8fbeae51`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`. The read-only GitHub snapshot confirmed these exact SHAs, draft/open status, and eight added paths. All eight are under `unsolved_math_prioritization/attempts/30003819/`; no QUEUE path is changed. None of the eight paths exists at the supplied base. `input_binding.json` binds head/base, every path and byte digest, the actual body, and scholarly sources. The copied input bytes live only under `private/`.

Before mathematical work I performed my own fresh read-only GWS read of workbook `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, sheet id `1254632077` (Math Puzzles), range A1:AQ1178. At 2026-10-22T05:56:56Z it returned 183 populated rows, with no exact numeric-ID/PR match. This is a checked ledger fact, not a literature-priority conclusion.

I read the visually rendered original and then the candidate PROOF before reading its historical audit or acceptance conclusions. I independently reconstructed the graph mechanism and wrote/reran my own standard-library checker. No candidate, source-author, or historical audit program was imported or executed. Later reading of all eight candidate documents checked consistency and provenance claims against the independently established argument. No other reviewer was contacted. No index, ref, checkout, service, ledger, PR, publication, or remote mutation was made by this reviewer.

## Original question, normalized assumptions, and success criterion

The complete relevant original item is on printed p.1452, PDF p.72, of [OWR23/2018](https://ems.press/content/serial-article-files/46745); its references continue on PDF p.73. It introduces ordinary r-differential posets, states Stanley's proposed local upper recurrence, contrasts Byrnes's global Fibonacci envelope and cumulative upper bound, and asks whether that cumulative bound can be improved in the direction of the recurrence. Its exact request includes: “We ask whether the above inequality can be improved”. A new paragraph then separately asks for a combinatorial proof of strict rank growth.

For the first request I use this falsifiable criterion: an explicit bound for every ordinary r-differential poset, computable before the rank being bounded is chosen, never weaker than Byrnes's bound, never beyond the desired local bound, and strictly stronger for some valid infinite examples. Neither the original text nor its quantifiers requires the improved expression to use rank numbers alone; neither demands the final recurrence itself. Incidence dependence is therefore an openly stated feature, not an added hypothesis restricting the posets. Requiring a rank-number-only correction would impose a further success criterion absent from the printed question.

The source's terminal common-cover equality to one is a typo. Read literally for arbitrary distinct elements, it is already impossible for a minimum and a rank-one element. The intended standard ordinary integer identity is `DU-UD=rI`, allowing zero common covers, as independently confirmed by [Gaetz–Venkataramana, PDF p.2](https://arxiv.org/pdf/1806.03509). Using the literal typo would make the problem vacuous. I instead use the conventional positive-integer r, unweighted incidence definition over Q, a unique minimum, and N grading. Finite ranks follow in the usual setting by finite upward degrees and induction from the minimum; their explicit statement in the candidate does not introduce a substantive special class.

The original strict-growth phrase also needs its known `r=n=1` exception (`p_0=p_1=1`), confirmed on Gaetz–Venkataramana PDF p.4. This does not affect the upper-bound review. It prevents promoting a proof of an unqualified literally false second statement.

## Exact accepted claim

Let `r>=1` be an integer and P an ordinary unweighted differential poset as above. Write `P_j` for rank j and `p_j=|P_j|`. For `j>=1`, let `B_j` be the incidence bipartite graph on `P_(j-1)` and `P_j`, and let

    beta(H)=|E(H)|-|V(H)|+c(H),       b_j=beta(B_j),

retaining isolated vertices. Fix `n>=2`, put `Z=P_(n-2)`, `X=P_(n-1)`, and let S be the z in Z with a successor in X whose complete predecessor set is `{z}`. Let `H_S` retain all X vertices, just S on the Z side, and all their incidence edges. Define `q_n=beta(H_S)`. Then

    0 <= q_n <= b_(n-1),
    p_n <= 1+r sum_(k=0)^(n-2) p_k+(r-1)p_(n-1)-q_n.

The correction is determined by the two preceding incidence levels, does not use `P_n`, and can be positive and attained in an infinite poset. It has sharp coefficient one. Equivalently,

    p_n <= r p_(n-1)+p_(n-2)+b_(n-1)-q_n.

No extra singleton-successor hypothesis is required for this theorem. The extra hypotheses occur only in its stronger consequences.

## Independently checkable graph proof

1. **Pair counts and connectivity.** The diagonal commutator gives `u(x)=d(x)+r`. Its off-diagonal entries equate common predecessor and successor counts. If a pair had two common successors, it would have two common predecessors; this lower pair would again have two common successors. Descent would force two distinct rank-zero elements. Hence all such pair counts are at most one. For connectivity, `B_1` is a star. If `B_j` is connected, its projection on `P_j` using common predecessors is connected, even for a one-vertex projection. The pair identity converts each projected edge into a common successor. Thus all `P_j` vertices are connected inside `B_(j+1)`, and every new upper vertex has a predecessor. Induction proves connectivity of every `B_j`.

2. **Exact slack.** With `e_0=0`, degree summation gives `e_j=e_(j-1)+r p_(j-1)`, hence `e_j=r sum_(k=0)^(j-1)p_k`. Therefore

       b_j=r sum_(k=0)^(j-1)p_k-p_(j-1)-p_j+1,
       p_n=Byrnes_n-b_n,
       b_n-b_(n-1)=r p_(n-1)+p_(n-2)-p_n.

   Byrnes's inequality follows from `b_n>=0`; the full local recurrence would require the stronger `b_n>=b_(n-1)`. This argument never infers the latter from the former.

3. **Witness tree.** For each `z in S` choose a singleton witness `a_z in X`; let `N_z` be every successor of z in X. For each `y in N_z` different from `a_z`, the pair has exactly one common predecessor, so exactly one common successor t in `P_n`. Every predecessor w of t lies in `N_z`: if w differs from `a_z`, its common successor with `a_z` forces a common predecessor, necessarily z. Distinct nonsingleton t above `a_z` cannot share a terminal other than `a_z`, by the at-most-one pair property. Their predecessor sets minus `a_z` partition `N_z` minus `a_z`. Their full stars form a connected tree `T_z` on terminal set `N_z`; if that terminal set has one element, the tree consists of that element and has no internal vertex.

4. **Internal disjointness and replacement.** The witness predecessor sets for different z are disjoint. A rank-n vertex internal to both `T_z` and `T_w` would cover both witnesses, contrary to the pair identity. Thus different trees share only X terminals. Replace each star centered at z in `H_S` by `T_z`, and retain every X vertex. If `T_z` has a internal upper vertices, it has `|N_z|+a-1` edges. Relative to the old star, edges and vertices both change by `a-1`; both connect exactly the same terminal set. Components, including isolated X vertices, are unchanged. The resulting graph K is a subgraph of `B_n`, with `beta(K)=beta(H_S)=q_n`. Cycle-space inclusion now proves `b_n>=q_n`. Combining with the exact slack proves the theorem.

This proof handles cycles in the union of overlapping terminal sets: no claim that the union is a forest is used. Individual replacements are trees, so the pre-existing cycles of `H_S` survive. It also handles multiple witnesses: any choice has the same terminal sets and cycle rank. It uses the whole lower-rank consistency to exclude four-cycles and never assumes the target recurrence.

## Stronger consequences and their boundaries

If every z has a singleton successor (`S=Z`), then `H_S=B_(n-1)` and `q_n=b_(n-1)`, proving the local recurrence at that step. When rank `n-1` was formed by reflection, it has r singleton successors over each z. Hence the *next*, arbitrary admissible extension to rank n satisfies the local inequality. Reflecting rank n itself separately gives equality by the construction's cardinality formula. The two statements have different indexing and both are correct.

For `n>=3`, suppose every z has two distinct singleton witnesses a,b. Then equality in the local bound characterizes reflection, as follows. Now K is connected and contains all X vertices and all edges incident to its internal vertices. Each unused upper vertex t adds exactly `d(t)-1` cycles. Equality forces every unused upper vertex to be singleton. Any nonsingleton upper vertex covering b must lie in K, and must lie in `T_z`, because a witness for another lower predecessor cannot share an upper vertex with b. Let h be the unique common successor of a,b. For each other terminal y, the common successor of b,y lies in `T_z` and also covers a, so uniqueness for a,b forces that successor to be h. Thus h covers all `N_z`, and no other nonsingleton vertex can occur above a terminal pair there. Each z has `u(z)>=2` when `n>=3`, so its h is nonsingleton. These are exactly the reflection blocks. A current x lies in `d(x)` such blocks, so its degree equation forces exactly r extra singleton successors. Conversely the reflection extension has `r|X|+|Z|` vertices, giving equality. One witness is not silently substituted for two.

At rank one there are r elements, each with r+1 successors. For a fixed z, its nonsingleton successors use disjoint nonempty subsets of the other r-1 elements, so there are at most r-1 of them. Every z therefore has at least two singleton successors. The equality theorem gives `p_3<=r p_2+r` for every r, with equality exactly for reflection from rank two.

Boundary checks: no `b_0` is needed. `B_1` is a star with `b_1=0`. At `n=2`, all r rank-one elements are singleton successors of the minimum, `q_2=0`, and the theorem gives `p_2<=r^2+1`. When also `r=1`, the witness replacement is the single-terminal tree, reducing both edges and vertices by one. For empty S, `H_S` consists of isolated X vertices and `q_n=0`. For proper S, isolates contribute equally to V and c and cannot change the cycle rank. The characteristic-zero incidence convention is essential; a cycle-space computation over an arbitrary field does not relax the differential identity to a modular one.

## Strictness, infinite realization, and sharpness

Any valid finite prefix can be extended indefinitely by adding one vertex over the complete current successor set of each vertex two levels below, plus r singleton successors over each current vertex. A current x then gets `d(x)+r` successors, and a current pair gets one common successor for each common predecessor. Every new vertex has a predecessor, and every new rank is finite. This proves all required identities and gives an infinite poset preserving the prefix.

For r=3, start with three rank-one vertices, one rank-two vertex over each pair, and two rank-two singleton successors over each rank-one vertex. Reflect to rank three. The rank sizes are `(1,3,9,30)`; `b_2=b_3=q_3=1`. Byrnes gives 31 and the corrected bound is exactly 30. The infinite extension above realizes this as an infinite example, rather than merely relaxed local data.

For r=1, use Young's lattice through rank five, then reflect twice. The ranks are `(1,1,2,3,5,7,12,19)`. Here `B_6` has 19 edges and 19 vertices and is connected, so `b_6=1`; all required singleton successors exist in rank six, so `q_7=b_7=1`. Byrnes gives 20 and the corrected bound is exactly 19. Continue reflection indefinitely. In either example a coefficient `c>1` would give an upper bound strictly smaller than the attained rank. Thus coefficient one is sharp; no claim that q uses every available structural feature is implied.

The relaxed layers `(1,3,3,7)` do satisfy both middle commutators for r=1, but the bottom has three successors, violating its required degree one. Their bipartite cycle ranks drop from 1 to 0 and `7>3+3`. This is a valid negative control for a proof that discards the lower levels, and supplies no differential-poset counterexample. The pair-block graph projects to a triangle; its actual bipartite incidence graph has a six-cycle.

## Exact remaining gap

Write `L_n=r p_(n-1)+p_(n-2)` and `B_n^*=1+r sum_(k=0)^(n-2)p_k+(r-1)p_(n-1)`. The exact identities give `B_n^*-L_n=b_(n-1)`. The theorem gives

    L_n <= B_n^*-q_n <= B_n^*,

with strict right inequality on the two verified infinite examples. This meets the original first improvement request, uniformly over all posets and all n, with no special-class hypothesis.

The unresolved recurrence requires showing `b_n>=b_(n-1)` in full generality. The theorem only shows `b_n>=q_n`. Its unremoved structural allowance is exactly `b_(n-1)-q_n`. This can be strictly positive in actual ordinary differential posets: Young's lattice at n=6 has ranks `(1,1,2,3,5,7,11)`, `b_5=1`, `q_6=0`, refined/Byrnes bound 13, and target local bound 12. Thus this proof alone cannot promote its bound to the recurrence. This is a limitation of the theorem, not a counterexample to the recurrence. No combinatorial strict-growth proof is supplied by the upper-bound argument.

The graph route is complete for the advertised refinement. Extending it by simply asserting that every previous cycle survives is blocked: it would restate the central required inequality without a new mechanism. A full recurrence proof would need additional information controlling cycles outside this witness-supported subgraph. The literal improvement request has no remaining mathematical gap within this review. A rank-number-only reformulation, if separately required by the human, remains a stronger unsolved task for this packet.

## Fresh independent computation

`checker.py` uses predecessor sets, exact integer counts, ordinary graph traversal, and edge partitions into cliques. Every new nonsingleton upper cover is a clique in the required pair graph, and these cliques partition its edges; remaining singleton multiplicities are forced by degree identities. Selecting the least uncovered edge and trying every eligible clique containing it enumerates all extensions for the fixed prior labeling. Counts are not isomorphism-class counts.

The successful checks reproduce r=1 prefix counts `1,1,1,1,2,7,60` through rank seven, r=2 counts `1,1,4` through rank three, and r=3 counts `1,2,288` through rank three. Top-rank q histograms are 50 zero/10 one for r=1, and 106 zero/182 one for r=3. Both explicit sharp examples, reflection r=1 through 5 through rank five, and Young's lattice through rank twelve pass. The actual trees, component counts, internal disjointness and K cycle ranks were checked across 5764 witness selections. For witness products exceeding 2000, only the first and last selection are computed; the uniform independence of witness choice rests on the proof. Young n=12 retains 52 isolated X vertices in `H_S`.

Negative controls check empty S with four isolated vertices, reject a removed top vertex, reject the invalid relaxed bottom while accepting its two middle identities, and falsify the coefficient-two inequality in both sharp examples. All guards use explicit exceptions and survive optimization. Normal, `-O`, and `-OO` successful result bytes agree; see final receipts for the exact hash. The first checker run exhausted memory because it materialized a Cartesian product before applying the cap; this was corrected by counting first and streaming. That implementation failure was recorded and supplies no mathematical evidence. The completed checker and results are retained, unlike the candidate's historical programs.

Finite checks independently validate the examples, formulas and listed finite cases. They are not an all-rank proof. The universal theorem and infinite continuation are certified here by the written graph and extension arguments.

## Source dependencies and historical-evidence limits

Fresh network retrievals matched the exact candidate source PDFs: OWR 1,261,683 bytes, SHA-256 `6512c6b53d12d362868ca481bc7445bb97fc465da1e37d2ffdf40127d600e97f`; Byrnes 598,546 bytes, SHA-256 `793156b93f5d17f03f4f7b70ecdb353daa48944cc946cc680927ca97d620f0d8`; Gaetz–Venkataramana 141,194 bytes, SHA-256 `834026c42643dac5cd4d9289b4321779f7e2f94ea9bdb2ee9206ac5e15cd1c56`. Web extraction of Byrnes returned 403, but a separate read-only HTTPS retrieval succeeded and the authenticated PDF was inspected locally.

I text-read OWR PDF pp.72–73 and visually inspected p.72. I text-read [Byrnes, Chapter 5, PDF pp.47–51](https://conservancy.umn.edu/server/api/core/bitstreams/45a1bae8-402f-42a7-ad67-4caa7b55d104/content) and visually inspected pp.48 and 51, confirming the cited bound, its separation from Conjecture 5.9, and the rank-inconsistent sentence in the original connectivity proof. The independent induction above avoids that typo. I text-read Gaetz–Venkataramana PDF pp.1–4 and relevant singleton discussion, and visually inspected p.2, confirming the operator convention and reflection construction. No complete-document or comprehensive literature inspection is claimed.

The PR's seven-member digest table inside its eight-member manifest, its acceptance bindings, the actual body digests, and source identities agree. Its historical result-output hashes and original 19-member packet hashes are clearly labeled historical; those absent old programs/receipts were not independently authenticated here. The independent fresh computations corroborate the important mathematical finite claims without treating historical attestations as proof. No novelty, priority, or current-worldwide-openness conclusion follows from the present report.

## Disposition for the parent

Adopt the exact accepted theorem and the first-request scope finding if the separate priority family clears it. Do not exclude it solely because its title/body/audit say partial. Do not describe it as proving the full Stanley recurrence, solving both original questions, supplying combinatorial strict growth, or establishing novelty. The authored proof itself needs no mathematical repair. Every local artifact, copied source, ledger response, and review coordination file is private/unpublished unless the parent explicitly chooses a separately authorized authored release.
