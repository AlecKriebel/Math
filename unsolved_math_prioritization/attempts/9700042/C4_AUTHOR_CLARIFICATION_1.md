# Author clarification for the frozen C4 proof candidate

Date: 2026-10-07.

Applies to `TURN_C4_BK_POISSON_CANDIDATE.md`, SHA-256 `3ca69bacb1a4458243626ea0adfb360fc991bb2f8e2ed4293fa98b9c85534691`.

The frozen candidate is preserved. Two local precision corrections were identified during independent review; neither changes a numerical estimate or proof dependency.

1. In Section 5, replace `a_j < b_j+h <= 2b_j` by `a_j <= b_j+h <= 2b_j` for a nonlast bad segment. Equality in the first comparison occurs when h divides b_j. The second comparison follows from b_j >= h on these segments.

2. The coarse bound on i_{j+1}-i_j by itself is too loose to prove positive rectangle side lengths for the short final segment. Use the actual endpoint displacements instead. Write x_j=i_j h+delta_j, with 0 <= delta_j < h. Then

   W_j=(x_{j+1}-x_j)+2a_j+h+delta_j-delta_{j+1},

   H_j=(y_{j+1}-y_j)+2a_j+h-delta_j+delta_{j+1}.

   Each quantization remainder after 2a_j is positive, and each actual endpoint coordinate displacement is at least -b_j. Consequently each side is strictly larger than 2a_j-b_j, which is at least h because a_j>b_j and a_j>=h. In particular W_j,H_j>=h for every segment, including the last one, regardless of its level increment tau_j.

These are clarifications of the deterministic enclosure step. They do not assert independent acceptance of the full candidate; the full proof remains subject to the audit outcome.
