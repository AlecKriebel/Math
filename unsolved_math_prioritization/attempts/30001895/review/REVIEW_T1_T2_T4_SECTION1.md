# Independent scope audit: TURN1, TURN2, and TURN4 §1

Problem 30001895 / OWR-11136-027. Reviewed 2026-10-03 UTC.

## Disposition

**PASS for the scoped mathematical reductions, credited applications, finite computations, and extremal equality deduction. No substantive mathematical repair is required in the portions reviewed. HOLD for any designation of the full original record as solved: the r-element question remains unresolved after 5/5 author responses.**

The audit independently checked the frozen manifest SHA-256 `32c1dc88b5e6457ab78f98c88aaf82231190601e3cb5f3f6043c8a40613ed79e` and all 53 listed file sizes/hashes. The author package was not edited. No new author proof search or remote write was undertaken. This report does not independently audit TURN3's search trees, TURN4's link certificate, or TURN5's certificates, which are covered by `INDEPENDENT_AUDIT_REPORT.md`.

## 1. Source identity and applicability

- Dol'nikov's Problem 8 is explicitly divided into 2 (hyperplanes) and 2′ (r-element sets), printed pp. 2540–2541. The stated implication from 2 to 2′ does not turn a negative answer to 2 into a negative answer to 2′. The OWR paragraph does not expressly specify finiteness or nonvacuity. [Primary OWR source](https://ems.press/content/serial-article-files/46358).
- The nonvacuous reading is explicit throughout the audited package. Chelnokov–Dol'nikov, Definition 7 and the following conjecture on PDF p. 3, supplies a proposer-authored definition requiring at least p members and identifies the finite hyperplane conjecture. This supports the chosen convention; it must remain visible. Without it, two disjoint 2-sets have the vacuous (3,3)-property but require two points, so the intended theorem is not equivalent to an unrestricted literal-vacuity reading. [Primary paper](https://arxiv.org/abs/1312.4110).
- Keller–Smorodinsky's Theorem 1.1 explicitly produces planar line families, with the stated coefficient 0.01, exponent, and no hidden multiplicative constant. The proof's finite-grid projection and duality produce finite, actual affine lines. The specialization q=3, eta=1/4 gives exponent 23/20 and the sufficient displayed relation log(p)/log(log(p)) ≥ 1200³. Taking p sufficiently large gives a valid violation of p−2. Finiteness and nonvacuity follow from the construction (also tau>p forces at least p members). This credited result applies to part 2, not part 2′. [Theorem and construction](https://arxiv.org/pdf/1809.06451v2).
- Alfaro–Rubio-Montiel–Vázquez-Ávila define the parameter as the maximum cardinality of an edge subset with induced maximum degree at most two. Proposition 5 and Theorem 6 give the claimed bound for simple finite graphs when the whole edge family is not a 2-packing. This is exactly the r=2 inequality required here. The preceding exposition focuses on connected graphs, but the needed general statement is explicit and also follows by adding component inequalities, since at least one component has maximum degree above two. [Publisher article](https://pisrt.org/psr-press/journals/odam/04-vol-7-2024-issue-1/covering-and-2-degree-packing-numbers-in-graphs/), [publisher PDF, p. 3](https://pisrt.org/psrpress/j/odam/2024/1/covering-and-2-degree-packing-numbers-in-graphs.pdf).

These are applicability checks, not a fresh exhaustive literature search or a claim that the general residual question is independently certified open.

## 2. TURN1 reductions

All audited steps pass:

1. A selected p-edge family fails to have a concurrent q-tuple exactly when every vertex belongs to at most q−1 selected edges. Downward closure of packing gives both directions of the (p,q)/packing equivalence.
2. Adding one unused edge increases each degree by at most one. Iteration gives the stated packing growth bound, including its minimum with the family size.
3. In the sufficiency direction, nu_(q−1)<m excludes the capped branch m and permits the claimed inequality chain. In the necessity direction, Delta>r ensures r≤nu_r<m, so p=nu_r+1 and q=r+1 are admissible and nonvacuous. The Delta≤r case of the min-form inequality is automatic.
4. Private padding preserves simplicity, every common intersection of at least two distinct edges, and the transversal number. It also preserves every nu_s for s≥1: original degrees are unchanged and each new vertex has degree at most one. Thus the uniform and bounded-rank formulations truly match, including their minimal-edge counterexamples.
5. The finite-obstruction induction is valid even for arbitrary ground sets/families: a proposed t-cover must hit the distinguished finite edge at some x, leaving a (t−1)-cover of its finite witness avoiding x. Enlarging that witness to at least p edges justifies the infinite-family extension. No finite-family theorem is silently asserted in making this conditional extension.
6. The rank-r common-intersection argument establishes p=q, the sunflower-plus-disjoint-edges example attains the stated target, and r=1 is handled correctly.

The r=2 literature application therefore extends to nonempty rank-at-most-two families for every allowed p,q, including infinite nonvacuous families. The source result itself does not claim this entire extension; it follows from the audited reductions.

## 3. TURN2 structure

The saturated-vertex cover is valid for every inclusion-maximal r-packing, not just a maximum packing. Every omitted edge meets a vertex already used r times. All r incidences of each saturated vertex lie in the selected edges counted by N, so r|S|≤r|N|. Adding a transversal of the residual selected edges covers the whole hypergraph. The formula for Q and the uniform incidence identity are correct.

The extended Fano example has tau=3, nu_3=7 and exactly the two listed maximum packings, with Q=0 and Q=1. The argument about old-vertex pairs and the additional vertex is correct. It refutes completeness of the proposed sufficient certificate, not the target conjecture.

The edge-minimal-counterexample deduction passes. If a deletion had Delta≤r, then nu_r=h−1 and any original degree above r must be r+1, providing the displayed cover contradiction. Otherwise minimality and the one-edge Lipschitz property of tau squeeze all inequalities to equality. This proves criticality, unchanged nu_r after deletion, and the violation by exactly one. Additivity across components plus the already proved nonnegative nu_r−tau establishes connectedness. Critical tau=1 and tau=2 families cannot meet Delta>r, so tau≥3.

The credited critical-edge bound applies to the pair system (e,T_e): diagonal pairs are disjoint, and all off-diagonal intersections are nonempty. The rank/uniform hypotheses and the bound on the number of nonisolated vertices are correct. [Bollobás original scan, Theorem 2, p. 452](https://web.vu.lt/mif/s.jukna/EC_Book_2nd/Bollobas.pdf).

## 4. TURN4 §1 equality deduction

The set pairs (e minus v, T_e), for e incident with v, have sizes r−1 and t−1 and the required cross intersections. Each T_e avoids v, so removing v from other incident edges does not destroy their intersection with T_e. The uniform Bollobás equality statement is explicitly stated in Theorem 2.1, PDF p. 3, of the cited primary paper. It gives one common set W with all complementary partitions, exactly as used. [Gerbner et al.](https://www.renyi.hu/~gerbner/papers/glpps2.pdf).

For an edge f not containing v, meeting every (t−1)-subset of W forces at least r elements of W into f, and uniformity then forces f⊆W. Missing an r-subset of W union {v} would make its (t−1)-element complement a transversal. Thus equality in the degree bound forces the complete family. The n cyclic r-intervals are distinct for r<n and each point occurs exactly r times; counting incidences bounds any r-packing by n. Hence equality families satisfy the target.

The strict critical-edge bound also follows directly from the equality clause of Bollobás's original Theorem 2, visually checked on the supplied p. 452 image: complete (t+r−1)-vertex family, possibly with irrelevant isolated vertices. Both strict restrictions on a minimal counterexample are justified.

## 5. Reproduced and independent computations

All seven author C++ commands were rebuilt with `-O2 -std=c++17 -Wall -Wextra -Werror`. Their JSON outputs and both author Python-check outputs match the frozen results exactly.

The independent reviewer implementation does not import author code or use the author's covering recurrence. It directly enumerates vertex-cover masks. For packing it seeds feasible subsets with their cardinalities and applies a Boolean-lattice subset-maximum transform. It checked **1,116,240 labelled families** across the seven declared cases and reproduced every proper-family, equality, and violation count. In particular, for (n,r)=(6,3), all 1,048,576 families were tested, with 1,039,503 proper cases, 68,760 equalities, and no violation. An extra (4,2) run returned the frozen self-check counts 23,17,0.

A separate reviewer Python implementation, using direct combinations and sets, reproduced the full extended-Fano and simplex reports. It also checked all 128 mixed-rank families on a three-point set:

- 672 (p,q)-equivalence checks, also comparing padded families
- 576 packing-preservation checks under private rank-three padding, with transversal preservation for every family
- 448 packing-growth checks
- 233 finite-obstruction witness constructions
- 195 inclusion-maximal-packing cover certificates

Known negative controls distinguish a maximal K4 triangle from a maximum packing and reject the unguarded tau≤nu_2−1 assertion on two disjoint edges. Nine (r,t) combinations with 2≤r,t≤4 verify the explicit cyclic packing construction. These finite controls support implementation accuracy; they are not substitutes for the general proofs.

Reviewer artifacts in this audit directory:

- `reviewer_t1_enumerate.cpp`, `reviewer_t1_results.json`
- `reviewer_reduction_controls.py`, `reviewer_reduction_controls.json`
- `author_reproduced_t1.json`, `author_reproduced_verify_small.json`, `author_reproduced_structural.json`

## Repairs and restrictions

Required substantive repairs: **none within the assigned scope**.

Optional exposition improvement: add the one-sentence observation that private padding preserves nu_s for every s≥1 when invoking uniformization before edge minimization. This is already an immediate consequence of the construction and is not a gap requiring HOLD.

Keep the nonvacuity convention, credited-theorem status, finite-computation scopes, and unresolved 5/5 disposition explicit. Do not promote these passes to a resolution of the general r-element component or the bundled original record.
