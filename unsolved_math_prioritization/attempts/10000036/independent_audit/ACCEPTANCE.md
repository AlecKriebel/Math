# Acceptance report: internal critical probability one

Problem 10000036 / AMR-099-0036, rank 875. Date: 6 October 2026.

**Decision: ACCEPTED for the exact mathematical theorem in the frozen author packet.**

## Accepted object

- Archive SHA-256: 266debc377c66c6813e9db2b6abc704454ead9cdec47024f5d15338329b2fe05
- Archive size: 13,793 bytes
- PROOF.md SHA-256: c31b7a1cd6a3af04807b20d58f23d79f9d07cf4eb87df26187498f3260f9891d
- PROOF.md size: 16,299 bytes
- All six archive members and their external manifest pins matched before mathematical inspection.

## Exact accepted scope

For every integer d >= 2 there exists a bond-percolation law on the nearest-neighbor edges of Z^d which is invariant under every graph automorphism and mixing under translations, has strictly positive conditional probabilities for both states of every edge given all the other output edges, and almost surely has a unique infinite component C. For almost every resulting graph X, independent Bernoulli bond thinning at every fixed retention parameter p < 1 has no infinite component almost surely. Consequently p_c(X) = p_c(C) = 1 in the quenched sense. The manuscript's additional internal site-thinning conclusion is also valid.

The all-dimensional input is Timar's established one-ended factor-of-iid spanning-tree theorem. The proof then controls every non-tree bypass through the largest finite-side size on its tree path. A convergent conditional union bound gives actual singleton boundaries simultaneously for all starting vertices. Independent thinning must retain infinitely many distinct boundary edges, while the original graph retains coalescing infinite ray tails. Finite energy after forgetting the auxiliary tree follows from the conditional-expectation tower property and strict positivity.

## Review disposition

- Original theorem scope: passed
- Connected one-ended spanning-tree input for every d >= 2: passed
- Measurability and full symmetry: passed
- Marginal ordinary finite energy: passed
- All-vertex Borel-Cantelli and final singleton cuts: passed
- Percolation and uniqueness in the final graph: passed
- Quenched threshold and all-component quantifiers: passed
- Translation mixing: passed
- Internal site-thinning remark: passed
- Required mathematical correction: none

This is a complete affirmative proof under the ordinary finite-energy convention used in the source question. It makes no claim about the stronger uniform finite-energy variant, novelty, priority, or journal acceptance. The close Haggstrom-Mester antecedent is credited. Bounded literature searches are not exhaustive. No finite computation or machine-checked infinite-volume certificate is asserted.

The frozen author packet remains unchanged. This report and AUDIT.md supply the separate post-review disposition; no proof patch is needed.
