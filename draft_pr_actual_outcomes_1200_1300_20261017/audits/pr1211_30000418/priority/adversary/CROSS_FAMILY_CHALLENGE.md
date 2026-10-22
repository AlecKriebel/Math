# Post-freeze cross-family challenge

Completed 2026-10-17 17:46:53 UTC. This is a separate follow-up to the independent audit frozen at 17:43:50 UTC. The parent explicitly authorized comparison after confirming that the other audit had frozen at 17:44:16 UTC. All eight files authenticated by my initial freeze manifest remain byte-unchanged. This document does not retroactively merge the two independent investigations.

## Decision

**I identified no actual mathematical or attribution concern that blocks the proposed qualified theorem note, provided its stated credits and limitations are incorporated.** The title “A five-list obstruction on an eleven-vertex tree” accurately describes the proved object. The exact theorem, ordinary palette size 5 / ordinary span 4 / arbitrary-list number 6, is mathematically incompatible with the universal equality printed in Kohl's 2006 Conjecture 4 and dissertation Conjecture 4.4. That is a statement about the old formula, independently of the discovery history.

This is **not clearance for a first-resolution, historically new, smallest, new-method, or current-openness claim**. The missing full primary sources remain substantive gaps. It is also not a prediction of journal novelty standards or external peer review. No publication, candidate edit, Git write, or outside contact was performed during this challenge.

## Challenge of the other frozen report and wording

I read `priority/independent/REPORT.md`, `PROPOSED_FRAMING.md`, `SOURCE_INSPECTION_LOG.md`, the source-comparison code/data, verification record, and freeze manifest. The proposed abstract and attribution paragraphs preserve the distinctions that matter:

- They define the initial-segment ordinary palette and arbitrary positive-integer lists, rather than treating any five spaced integers as an ordinary five-color palette.
- They credit the known tree upper bound to Voigt through Kohl–Schreyer–Tuza–Voigt, following Kohl's actual attribution. An elementary proof included for completeness does not become a new bound.
- They acknowledge the actual 2001 Fiala–Škrekovski cyclic five-list example and cite the inspected preprint for it.
- They distinguish that preprint's content from the bibliographically related 2005 journal article, whose complete text was not obtained.
- They identify the 2006 printed conjecture without asserting that it was open immediately before this work, or that no earlier tree refutation exists.

Those choices address the adverse overlap and uncertainty independently found in my audit. The source gaps do not make an explicitly proved theorem false. They prevent claiming that its negative answer was historically first and may require further attribution if earlier tree examples are subsequently located. Leaving the gaps in a supporting audit, with a concise historical-status qualification in the note, is a defensible treatment of that limitation.

One important boundary deserves emphasis: the other report's observation that accessible later figures do not match this specimen cannot eliminate a **different** earlier countertree. The report correctly leaves the complete 2018/2020/2021 sharpness constructions unresolved; its publication wording does not rely on non-isomorphism as historical clearance. The early Chen/Kuo, Jonas, final Fiala–Škrekovski, and original TCS2005 full-text gaps likewise remain open.

Two small precision items are worth retaining in editing. Give Kohl's full contribution as printed **414–417**, with the conjecture specifically on 416. In any discussion of Yu–Wang–Liu's path value, qualify the statement by its object and range: their `(2,1)`-total path value 5 is stated for `P_k`, `k>=3`; it is not a statement that every short ordinary L(2,1) path needs five labels. Neither item undermines the explicit eleven-vertex theorem.

## Source and finite-comparison challenge

I re-viewed the complete printed page 14 of the actual [KAM2001-530 primary preprint](https://kam.mff.cuni.cz/kamserie/clanky/2001/s530.pdf). The figure has ten vertices, twelve edges, two triangles and a central eight-cycle; the exceptional list is `{1,2,4,5,6}` at the left tip. The remaining lists are `{1,2,3,4,5}`. The displayed ordinary witness and text assert the same five-list separation represented in both auditors' data.

The two independently frozen transcriptions are identical under the explicit map `t0,t1,t2,t3 -> a,b,c,d`, `b0,b1,b2,b3 -> e,f,g,h`, with `x,y` fixed. Their lists and printed ordinary witness also coincide under that map. Their sets of 66 spanning trees coincide exactly. I independently revalidated every one of the other auditor's 66 labeling witnesses, checking list membership, every edge gap, and inequality among all pairs of neighbors. I also ran that auditor's checker under Python `-O`; its graph size/cycle rank, infeasible displayed five-lists, valid ordinary five-label witness, absence of an ordinary four-label solution, completeness of the 66-tree enumeration, and all tree witnesses passed.

The code's use of the maximum required gap on pairs joined by both an edge and a two-edge walk correctly retains gap 2 in the triangles. A connected ten-vertex subgraph with nine edges is a tree, so the enumeration criterion is sound for this simple transcribed graph. The finite data support exactly the narrow transfer exclusion claimed: **deleting edges or vertices while inheriting the displayed lists does not yield a bad tree assignment**. Indeed, any forest subgraph extends to a spanning tree of this connected graph, whose feasible witness restricts to the forest. Distance constraints can only disappear under this restriction.

This check does not exclude different lists, a different historical example, a gadget reduction, an unfolding/universal cover, or another theorem supplying a tree gap. Neither report makes those stronger inferences. Agreement between the audits is corroboration of this particular transcription and calculation, not a certificate of complete historical coverage.

## Recorded status

The separate machine-readable receipt `CROSS_FAMILY_CHALLENGE.json` authenticates the reviewed files, records preservation of the initial freeze, the explicit graph map, revalidation results, and the qualified verdict. Completion of this bounded cross-challenge: **100%**. Historical priority and present openness: **not established**. Local PDF/text/image input copies remain undistributed under `sources/`; no new source body was downloaded for this comparison.
