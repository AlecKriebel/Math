# Independent acceptance of the prior result for Erdős Problem 81

Date: 2026-10-06 UTC

## Mathematical decision

**ACCEPTED as a prior mathematical resolution of the exact EP-81 target.**

The accepted result is Obinna Okechukwu's Theorem 1.1 and its chordal specialization, Corollary 1.2, in [*Clique partitions and bounded simplicial defect*, arXiv:2609.20871v1](https://arxiv.org/abs/2609.20871v1), submitted 15 September 2026. The acceptance concerns the main proof in Sections 1–5, including Theorem 1.3 as an intermediate result. It uses established finite LP duality and the established fixed-pattern packing approximation with their precise hypotheses; it introduces no additional conjectural hypothesis.

For s=0, the theorem gives a single constant K_0>=0 such that every finite simple chordal graph G on n vertices satisfies

cp(G) <= floor(n(n+1)/6)+K_0.

The constant is independent of G and n. Therefore, for n>=1,

cp(G) <= n^2/6+(1/6+K_0)n.

The empty graph has cp=0. These are the required uniform quantifiers for EP-81. The stronger eventual conclusion is also accepted: beyond a fixed threshold, the maximum is floor(n(n+1)/6), with the asserted book-graph equality classification.

## Why this is a proof acceptance

The signed fractional argument has been independently derived, including the negative-mass correction for overlapping covers, weighted rather than independent-size rounding, disconnected non-induced templates, host isolates, and the fixed finite set of templates before thresholds are maximized. The integral construction explicitly builds compatible edge-disjoint triangle families. The bounded exceptional set, its incidence inequality, limiting profile optimization, exact reconstruction of the core, strict positive exterior-edge saving, and final minimal-counterexample argument were checked separately. The accompanying reports record those arguments in detail.

In particular, the audit does not treat the qualitative o(n^2) approximation as if it directly supplied O(n). The approximation produces structure; the new exact finite partition construction supplies the sharp count. Likewise, the equality conclusion comes from a finite inequality with strictly positive coefficients after the limits have classified exceptional profiles.

No correction patch to the preprint is needed for the accepted main chain. No newly authored solution of EP-81 is being claimed by this audit.

## Original problem and graph conventions

The primary EOZ reprint, *Clique Partitions of Chordal Graphs*, in *Combinatorics, Geometry and Probability* (1997), printed pages 291–297, defines simple undirected graphs and partitions of edges into arbitrary, not necessarily maximal, complete subgraphs. Its Conjecture 1 on printed page 294 asks for a universal quadratic coefficient 1/6 with a linear additive term. This matches the complete EP-81 record checked by the corpus replay. The [publisher chapter](https://www.cambridge.org/core/books/abs/combinatorics-geometry-and-probability/clique-partitions-of-chordal-graphs/342329633D5A1341FC9A80CA211970EC) confirms the source identity; the full reprint was inspected through the public scan recorded in SOURCE_INSPECTION.json.

The stronger all-order exact bound is separate: EOZ Conjecture 2 and the preprint's Conjecture 7.1 are not asserted to be solved by an eventual theorem. The small-order equality classification is also not asserted. No restriction to split, connected, dense, or large-minimum-degree graphs survives in Corollary 1.2.

## Source status is a separate question

The public arXiv record confirms the preprint's author, title, v1 version, and submission date. This audit does not establish journal acceptance, external referee approval, formal proof-assistant verification, or an official status change on a problem website. Failed or stale problem-page retrievals are not treated as proof of current open or closed status.

Thus the two decisions are deliberately distinct:

- Main theorem validation: accepted by this independent mathematical audit
- Published or community-certified solution status: not established here; the inspected source is an arXiv preprint

## Verification limits

No machine-checked formalization, explicit usable universal threshold, or comprehensive novelty search is claimed. Yuster's published approximation theorem is accepted as an established theorem; its regularity and hypergraph-matching foundations are not re-proved here. Dirac's needed simplicial-pair statement is proved independently in the audit, despite unavailable full access to his original article. Galvin's original Theorem 4.1 and its exact application were inspected. Auxiliary Section 6 is not included in this theorem acceptance.

Finite checks and cryptographic replays establish exactly their stated bounded properties. They do not themselves certify the asymptotic theorem.
