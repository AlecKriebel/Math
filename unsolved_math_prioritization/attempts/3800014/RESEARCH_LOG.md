# Research log

## 2026-09-30 10:56 UTC: exact source and prior gates
The queued target passed the all-ref attempt, branch,132 all-state PR and related-target gates. The full imported report is only open-status triage. The exact Erickson page asks for any faster algorithm in a reasonable model, and its index explicitly disclaims current open status. Completion estimate:10%.

## 2026-09-30 10:59 UTC: credited algorithm identified
The full Bremner et al. author paper establishes O(n²/log n) real-RAM min-plus convolution; author publication metadata confirms the2006/2014 history. Chan's full primary dominance lemma was retrieved and read. One masked convolution reduces the interval problem, with run-start/end masks correctly handling duplicates. Completion estimate:80%, pending full witness and boundary audit.

## 2026-09-30 11:04 UTC: complete reconstruction
Implemented the known block-dominance mechanism with finite sentinels, lexicographic integer tie-breakers and explicit minimizing indices. A conservative self-contained recurrence proof covers the sorting-based reference implementation. The bound is real-RAM o(n²), not O(n^(2−epsilon)) or a unit-cost bit theorem. Completion estimate:100% of the source's faster-algorithm alternative, as a known-result consequence.

## 2026-09-30 11:08 UTC: freeze
All10,388 exact controls pass. One substantive validation/reconstruction family recorded. The complete proof, implementation, verifier and receipt are frozen for separate review. No original discovery or optimality claim. The parent owns any queue status update after review.

## 2026-09-30 11:11 UTC: review correction to output reporting
The independent reviewer noted that recursive yield-from propagation could add recursion-depth overhead per reported pair in the reference implementation. Replaced it with a shared output list and one leaf append per pair, matching the written O(P) reporting algorithm. No proof statement or mathematical file changed. All10,388 correctness assertions still pass. This is a verification correction within the same validation family, not a new search approach.

## 2026-09-30 11:21 UTC: independent review and publication checkpoint

Completion estimate: 100% of the source’s faster-than-quadratic alternative, in the explicitly stated real-RAM model. Separate review passed after the output-list repair; 10,388 submitted and 22,962 independent assertions pass. One validation/reconstruction family remains recorded in the historical ledger; this is zero new-discovery attempts and a credited known resolution. The reviewed mathematical artifact and final algorithm are unchanged.
