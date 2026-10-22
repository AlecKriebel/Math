# Independent acceptance of the exact two-move invariant

Auditor: survival lane, shared PASS4.

Reviewed artifact: `pass4_devil/EXACT_TWO_MOVE_INVARIANT.md`, SHA256 `3b26129e44721d05bfab2e21ca675bb2e616e5641a96d32487a2cd3921547e8d`.

**Verdict:** accepted. On every pre-move state with at most sixteen pending position-time pairs, exact two-move online viability implies exact three-move online viability. Together with the bounded-lead count, this supplies a second infinite online strategy for maximum lead sixteen.

## Checks of the nontrivial steps

1. Lemma 3 distinguishes immediate loss from a nonempty safe first-move set. Its exclusions for safe-set sizes 3, 5, 6, 7, 8, and 9 are valid. In the six-point case, occupying fewer than three rows or columns forces a full 2-by-3 product, whose four corner neighborhoods cover at least twenty points. The surviving sizes 1, 2, and 4 have the stated lower bounds on the two timestamp counts.
2. Lemma 4 bounds the union of dangerous centers over every possible new announcement, rather than bounding each individual announcement separately. In each row b=9+, 8, 7, 6, 5, 4, or at most 3, the required timestamp for the new pair follows from the count bounds of Lemma 3. The common-center and seventh-neighbor estimates therefore apply to a fixed original set, uniformly over the new site.
3. In the b+c≤14 case, fewer than sixteen pairs remain after an addition, so all nonimmediate two-move traps are excluded. The exact dangerous-center set is consequently A8(B), including irrelevant announcements.
4. The final m=b=8, c=0 case is not discarded by counting alone. The proof correctly invokes the assumed W2 viability to exclude the unique possible covering of all nine current moves.
5. Choosing a current-safe center outside the robust danger set puts every post-announcement successor in W2. Future timestamps beyond the three displayed layers cannot affect this implication, but are still included in the sixteen-pair total. The actual bounded-lead process preserves that total bound.

No correction is required. The general W_r-to-W_(r+1) criterion is valid as a conditional invariant principle. The reviewed proof establishes only r=2 and budget sixteen; it does not prove a family for unbounded budgets.
