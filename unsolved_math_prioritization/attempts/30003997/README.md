# 30003997: path-cost arborescence hardness

[PROOF.md](PROOF.md) gives a complete 3SAT reduction for the exact fixed-root, destination-dependent path-cost problem. Hardness holds for binary nonnegative costs on a depth-three DAG with maximum nonroot indegree three; shifting the costs gives a strictly positive {1,2} version.

One substantive proof family; separate adversarial AI review passed. See [the report](review/REVIEW.md). The frozen proof retains its submission-time status header. Historical priority is unestablished. The distinct adjacent target30003996 shares the literal-selection idea; duplicate30003998 is covered by this one attempt rather than a new budget or PR.

Run verify.py with standard-library Python3 to print the receipt. The bounded exhaustive control checks449 formulas and12,696 arborescences, with57,135 assertions. The mathematical proof establishes the arbitrary-size reduction; the finite enumeration does not replace it. The coordinating task owns queue updates.
