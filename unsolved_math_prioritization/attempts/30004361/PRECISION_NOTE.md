# Precision note: the two symmetric Local Lemma thresholds

This note records the nonblocking wording clarification already identified in the independent audit. It does not replace or revise the preserved original report.

In Section 6, put p = 73/243 and D = 30. The elementary sufficient criterion is

    e p (D + 1) ≤ 1,

or p ≤ 1/(31e). The optimized symmetric criterion is

    p ≤ max(0 ≤ x ≤ 1) x(1 − x)^30 = 30^30/31^31.

These sufficient thresholds differ: the second is strictly larger than the first. They are not equivalent criteria in general. Both fail for p = 73/243 with D = 30. Accordingly, the original word “Equivalently” should be read as reporting the failure of the second calculation in this instance, not as identifying the thresholds.

The mathematical conclusion remains only that these direct sufficient-condition calculations, for the stated independent uniform coloring and dependency bound, do not prove the desired coloring exists. This establishes neither nonexistence of a coloring nor failure of every possible use of the Local Lemma. The audit had already made this distinction; no new substantive approach is counted.
