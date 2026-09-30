# Research log

## 2026-09-30 11:31–11:49 UTC — Source and prior-attempt gates

Read the exact pinned record and source-code keyed null prior report, original OWR contribution, and full relevant definitions/proofs of the published 2023 paper. Checked current queue, historical status, all-ref target history, related groups and 140 all-state PRs; no prior target attempt was found. The source question has ordinary computable time bounds and asks equality versus strict containment inside ordinary depth. Source triage used no proof attempt. Completion estimate: 0%. Runtime: gpt-6-astra at xhigh, not ultra.

## 2026-09-30 11:49–11:55 UTC — Two substantive approaches

1. **Oracle elimination.** Restated the sufficient all-string time-bounded comparison and proved that the stronger uniform output-preserving compilation method is impossible for noncomputable A. The correct-stage approximation variant would likewise compute A. The needed nonuniform comparison has not been derived from lowness for unbounded K. Status: blocked at the explicit time-bound gap.
2. **Truth-table transfer and c.e. covering.** Proved the transfer lemma under an unbounded-complexity comparison and applied Nies's published Theorem7.4. Universal equality, or existence of any strictness witness, reduces to c.e. K-trivial oracles. This does not decide either outcome. The weaker Turing-cover theorem was explicitly rejected as insufficient for this argument. Status: valid partial reduction; blocked on the remaining c.e. problem.

The elementary witness restriction X not Turing-reducible to A is a credited consequence of Nies's downward closure and Moser–Stephan shallowness, not a fresh attempt or a classification. Full target remains unsolved, 2/5. Completion estimate: 5%, representing a reduction and precise obstruction rather than a likely solution. No further proof search is continued without a new mechanism. Separate review is required before a draft PR.
