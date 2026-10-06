# Mathematical review checklist

This guide identifies falsifiable obligations in the candidate proof. It does not assert that an independent review has occurred.

1. Source scope: original BHS Question 1.1 and BT Question 1 explicitly use strict single-edge conditional positivity, not uniform finite energy. The construction must be assessed under precisely that convention.
2. Tree input: a connected spanning tree with one end is needed. An arbitrary one-ended spanning forest is insufficient because a non-tree edge can join different components. Verify Timar's isomorphism-equivariant input theorem for every d >= 2, with Pemantle as the d = 2 fallback.
3. Kernel definition: both probabilities lie in (0,1); finite-side sizes and the maximum over the finite tree path are measurable and automorphism-equivariant.
4. Cut geometry: every non-tree edge crossing S_T(t) has t on its tree path. This proves the insertion-rate upper bound. The host graph's bounded degree gives at most Delta |S_T(t)| candidates.
5. Summability: along a ray the finite-side sizes are distinct increasing positive integers, not merely divergent. Hence the sum over ray cuts is bounded by a convergent integer series.
6. Quantifiers: apply Borel-Cantelli conditional on each good T and then intersect over the countable vertex set. It is not necessary to union over all deterministic trees or over uncountably many p.
7. Genuine final cutsets: deleted edges cannot add bypasses. Beyond the final exceptional index the unique crossing tree edge is actually open. The finite side may be disconnected in X, but its whole boundary is still the stated singleton.
8. Quenched thinning: hold X and its witnessed cutsets fixed. Distinct singleton cut edges survive independent thinning with probability p^k. This excludes every infinite component, not merely the root component with a special annealed probability.
9. Marginal finite energy: use conditional expectations after forgetting T. Strict positivity is preserved, but a deterministic uniform bound and its failure are both separate assertions not proved here.
10. Prior work: compare Haggstrom-Mester Section 2 carefully; distinguish their summable preservation of rays from the additional suppression of all non-tree bypasses. Inspect current literature without converting a bounded search into a novelty claim.
11. Integrity: check the externally supplied archive hash, byte count, exact member set and manifest before mathematical inspection. Source metadata records what was actually accessed; no excluded source PDF is supplied inside this packet.

No finite experiment can certify the infinite-volume assertions in this manuscript. The packet intentionally has no computational mathematical claims requiring an executable checker.
