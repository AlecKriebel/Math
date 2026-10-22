# Crossingless matching Yoneda algebra: audited partial results

Problem 30000930 / OWR-1790-007, rank 661. **Unsolved after five substantive approaches (5/5).** The general weighted all-k comparison remains unresolved in this investigation.

## Current mathematical conclusion

For the two Springer components A = P1 x P1 and B = F2 in the resolved (2,2) Slodowy slice, the Yoneda algebra of their half-canonical sheaves is **abstractly isomorphic, as a cohomologically graded algebra, to the two-matching arc algebra**. The proof uses the published 2024 one-sided module comparisons, proper-support duality, and a two-object rigidity lemma. The [full independent audit](audit/AUDIT.md) passes this restricted conclusion. The result is not asserted to be canonical or trace-preserving; no novelty or priority claim is made.

The [non-blocking clarifications](audit/CLARIFICATIONS.md) accompany the proof: square-zero lines are intrinsic, both endpoint actions are nonzero, and the two half-canonical restrictions are O(-2) and O with product K_C. In the normalized table, the top Serre traces are opposite: tr_A(xy)=1 and tr_B(pq)=-1. Both cannot simultaneously be normalized positively while preserving the claimed graded cyclic trace. The twists cannot be dropped.

The higher-rank calculation proves balance-and-degree constraints in an explicitly hypothetical simultaneous cohomology model. Its k=4 ambiguity is neither a globally associative alternative algebra nor a counterexample to the desired comparison. The local Koszul vanishing does not imply global Yoneda vanishing.

## Source correction and current literature scope

The original f=1 nonassociativity obstruction is retained only for **ordinary complex-oriented Gysin maps**. The original report did not explicitly fix orientation signs, and the final primary article already distinguishes this known obstruction from its weighted associative product. This does not refute the weighted Yoneda comparison. The [complete original audit](safe/history/audit/AUDIT.md) and original author ZIP remain unchanged.

The inspected 2026 Mladenov preprint states collection formality and triviality of a formal deformation of composition, the latter through formal coordinate changes. These are stronger than the older pairwise statements; they still do not supply the explicit weighted arc-surgery product identification in this investigation. The k=2 proof uses the published 2024 theorem and does not depend on that preprint. See [source updates](safe/SOURCE_UPDATES.md) and the audit's literature section. The final AMS article PDF was inaccessible and uninspected; publisher-deposited metadata is not a substitute for its proof. Neither comprehensive current-literature coverage nor global-open status is certified.

## Preserved evidence

- [Full k=2 proof](safe/K2_YONEDA.md), [five approaches](safe/RESEARCH_LOG.md), and [limitations](safe/LIMITATIONS.md)
- [Full continued independent audit](audit/AUDIT.md), [clarifications](audit/CLARIFICATIONS.md), and [exact input binding](audit/BINDING.json)
- [Original audit and source-formulation correction](safe/history/audit/AUDIT.md), [unchanged original archive](safe/history/author-packet.zip), and [history binding](safe/HISTORY_BINDING.json)
- [Fresh publication gate](LIVE_GATE.json)

All 24 continued author archive members and all 8 continued audit archive members are preserved byte-for-byte, as are both ZIPs. The frozen author's pending-audit status and no-remote-write statements record its creation stage; the later bound independent audit supplies the present verdict. Historical claims remain subject to the explicit source correction and current scope above.

## Reproduce

Requires Python 3.10+ and SymPy (checked with 1.14.0). From this directory:

    python3 verify_release.py

This checks the exact payload file set, hash/size bindings, ZIP/extracted equality, all seven history bindings, original-source correction, status and five-approach count, new author and independent computations, and historical replay. The independent checks cover 1,728 generic and 1,728 normal-form associativity triples, 144 basis-change products, 144 trace products, and 2,878 higher-rank triples. The archive-only replay is isolated and network-free. Computations check the stated finite algebraic assertions and do not certify external theorem proofs.

Only authored mathematics/code, full safe audits, and public verification metadata are included. Original source PDFs/text, raw datasets, and private coordination records are excluded. The queue changes only this target's Status, Turns, and previously blank Findings, preserving every other byte, including its historical header, Chat, and DOI.
