# Research log

## 2026-07-27 PDT

- Read and reconstructed every implication in
  `math/lemmas/adjacent_true_twin_reduction.md` at target SHA-256
  `b28262900ddb77d62caea61741e502f2da706900f51ce47165c2582b899c36ae`.
- Audited the \(K_2\) boundary, \(k=1\), configurations containing both
  twins, nonemptiness of the restricted family, attacks at the surviving
  twin, induced-edge preservation, domination of successors, and the
  one-guard/unoccupied-attack quantifiers.
- Built and ran the independent `falsifier.py` through all connected
  unlabeled graphs of orders 1--8.
- Coverage: 12,113 graphs, 4,087 with adjacent true twins, 6,279 twin-pair
  incidences, and 748 equality-hypothesis incidences.
- Outcome: zero static, parameter, nonemptiness, forced-state, or eternal
  closure failures.
- Resources: 1.50 s wall, 1.43 s user, 0.04 s system, 46,153,728-byte
  maximum RSS, no swaps.
- Verdict: **PASS; no change to the target is required.**
